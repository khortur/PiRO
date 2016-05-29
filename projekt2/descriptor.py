class Descriptor:
    WIDTH_PARTS = 100.0
    HEIGHT_PARTS = 100.0
    DISTANCE_FROM_EDGE = 1
    EDGE_WIDTH = 1
    MAX_DIFFERENCE = 2

    def __init__(self, img):
        self.img = img
        self.edges = []

        top_edge = img[Descriptor.DISTANCE_FROM_EDGE, :]
        bottom_edge = img[img.shape[0] - 1 - Descriptor.DISTANCE_FROM_EDGE, :]
        left_edge = img[:, Descriptor.DISTANCE_FROM_EDGE]
        right_edge = img[:, img.shape[1] - 1 - Descriptor.DISTANCE_FROM_EDGE]

        bottom_edge = list(reversed(bottom_edge))
        left_edge = list(reversed(left_edge))

        self.edges.append(top_edge)
        self.edges.append(right_edge)
        self.edges.append(bottom_edge)
        self.edges.append(left_edge)

    def print_sides(self):
        print("TOP: ", self.edges[0])
        print("RIGHT: ", self.edges[1])
        print("BOTTOM: ", self.edges[2])
        print("LEFT: ", self.edges[3])

    @staticmethod
    def compare_two_edges(edge1, edge2):
        result = 0
        for i in range(min(len(edge1), len(edge2))):
            # result += abs(edge1[i] - edge2[i])
            min_val = 99999999
            for x in range(max(0, i - Descriptor.MAX_DIFFERENCE), min(len(edge2), i + Descriptor.MAX_DIFFERENCE)):
                # for w in range(Descriptor.EDGE_WIDTH):
                temp_val = 0
                for channel in range(3):
                    temp_val += abs(edge1[i][channel] - edge2[i][channel])
                min_val = min(min_val, temp_val)
            result += min_val
            # for channel in range(3):
            #     result += abs(edge1[i][channel] - edge2[i][channel])
        return result

    def compare(self, other):
        results = {}
        for i in range(1, 5):
            for j in range(1, 5):
                # results[(i, j)] = Descriptor.compare_two_edges(self.edges[i - 1], other.edges[j - 1])
                results[(i, j)] = Descriptor.compare_two_edges(self.edges[i - 1], list(reversed(other.edges[j - 1])))
        return results
