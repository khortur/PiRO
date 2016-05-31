from heapq import heappop, heappush

from projekt2.descriptor import Descriptor


class State:
    def __init__(self, unused, max_width, max_height):
        self.unused = unused
        self.max_width = max_width
        self.max_height = max_height
        self.score = 0.0
        self.assigned = [[] for i in range(max_height)]
        self.empty_spaces = [(0, 0)]
        self.avg_edge_score = 100.0
        self.avg_score_count = 0

    def __lt__(self, other):
        # return self.score < other.score
        return self.num_assigned() > other.num_assigned() or \
               (self.num_assigned() == other.num_assigned() and \
                self.predicted_score() < other.predicted_score())

    def get_neighbours(self):
        result = []
        for piece in self.unused:
            for (x, y) in self.empty_spaces:
                for rotation in range(4):
                    rotated_piece = piece.get_rotated(rotation)

                    # DEBUG:
                    # if x != 0 or y != 0:
                    #     print(x, y)
                    #     print(self.assigned)
                    #     print(self.empty_spaces)

                    left_piece = None if x == 0 else self.assigned[y][x - 1]
                    top_piece = None if (y == 0 or len(self.assigned[y - 1]) < x + 1) else self.assigned[y - 1][x]
                    new_score = self.score
                    if top_piece is not None:
                        top_edge_id = (top_piece.img_num, (top_piece.rotation + 2) % 4)
                        bottom_edge_id = (rotated_piece.img_num, rotated_piece.rotation)
                        top_score = Descriptor.compare_two_edges(top_piece.bottom_edge, rotated_piece.top_edge,
                                                                 top_edge_id, bottom_edge_id)
                        self.avg_score_count += 1
                        self.avg_edge_score = ((self.avg_edge_score * (
                        self.avg_score_count - 1)) + top_score) / self.avg_score_count
                        new_score += top_score

                    if left_piece is not None:
                        left_edge_id = (left_piece.img_num, (left_piece.rotation - 1) % 4)
                        right_edge_id = (rotated_piece.img_num, (rotated_piece.rotation + 1) % 4)
                        left_score = Descriptor.compare_two_edges(left_piece.right_edge, rotated_piece.left_edge,
                                                                  left_edge_id, right_edge_id)
                        self.avg_score_count += 1
                        self.avg_edge_score = ((self.avg_edge_score * (
                        self.avg_score_count - 1)) + left_score) / self.avg_score_count
                        new_score += left_score

                    new_unused = self.unused[:]
                    new_unused.remove(piece)
                    new_empty_spaces = self.empty_spaces[:]
                    new_empty_spaces.remove((x, y))
                    if x < self.max_width - 1 and (x + 1, y) not in new_empty_spaces:
                        new_empty_spaces.append((x + 1, y))
                    if y < self.max_height - 1 and len(self.assigned[y + 1]) == x and (
                    x, y + 1) not in new_empty_spaces:
                        new_empty_spaces.append((x, y + 1))
                    new_state = State(new_unused, self.max_width, self.max_height)
                    new_state.score = new_score
                    new_state.empty_spaces = new_empty_spaces
                    for i in range(len(self.assigned)):
                        for j in self.assigned[i]:
                            new_state.assigned[i].append(j)
                    new_state.assigned[y].append(rotated_piece)
                    result.append(new_state)
        return result

    def is_final(self):
        for i in self.assigned:
            if len(i) < self.max_width:
                return False
        return True

    def predicted_score(self):
        return self.score + (self.max_height * self.max_width - self.num_assigned()) * self.avg_edge_score

    def num_assigned(self):
        result = 0
        for i in self.assigned:
            result += len(i)
        return result

    @staticmethod
    def solve(pieces, max_width, max_height):
        print("Started SOLVE")
        descriptors = [Descriptor(pieces[i], i) for i in range(len(pieces))]
        fringe = []
        heappush(fringe, State(descriptors, max_width, max_height))
        while len(fringe) > 0:
            print("Fringe size: ", len(fringe))
            current_state = heappop(fringe)
            print("Assigned: ", current_state.num_assigned())
            print("Score: ", current_state.score)
            print("Predicted score: ", current_state.predicted_score())
            if current_state.is_final():
                return current_state.score, current_state

            neighbours = current_state.get_neighbours()
            for n in neighbours:
                heappush(fringe, n)
        return None, None
