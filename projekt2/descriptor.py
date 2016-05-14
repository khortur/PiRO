class Descriptor:
    WIDTH_PARTS = 100.0
    HEIGHT_PARTS = 100.0
    DISTANCE_FROM_EDGE = 0
    EDGE_WIDTH = 3

    def __init__(self, img):
        self.img = img
        self.edges = []

        top_edge = []
        bottom_edge = []
        for x in range(Descriptor.DISTANCE_FROM_EDGE, img.shape[1] - Descriptor.DISTANCE_FROM_EDGE):
            top_edge.append(img[Descriptor.DISTANCE_FROM_EDGE:Descriptor.EDGE_WIDTH, x])
            bottom_edge.append(img[img.shape[0] - 1 - Descriptor.DISTANCE_FROM_EDGE - Descriptor.EDGE_WIDTH:img.shape[0] - 1 - Descriptor.DISTANCE_FROM_EDGE, x])

        left_edge = []
        right_edge = []
        for y in range(Descriptor.DISTANCE_FROM_EDGE, img.shape[0] - Descriptor.DISTANCE_FROM_EDGE):
            left_edge.append(img[y, Descriptor.DISTANCE_FROM_EDGE:Descriptor.EDGE_WIDTH])
            right_edge.append(img[y, img.shape[0] - 1 - Descriptor.DISTANCE_FROM_EDGE - Descriptor.EDGE_WIDTH:img.shape[1] - 1 - Descriptor.DISTANCE_FROM_EDGE])

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
        max_difference = 3
        for i in range(min(len(edge1), len(edge2))):
            # result += abs(edge1[i] - edge2[i])
            min_val = 99999999
            for x in range(max(0, i - max_difference), min(len(edge2), i + max_difference)):
                for w in range(Descriptor.EDGE_WIDTH):
                    temp_val = 0
                    for channel in range(3):
                        temp_val += abs(edge1[i][w][channel] - edge2[i][w][channel])
                    min_val = min(min_val, temp_val)
            result += min_val
        return result

    def compare(self, other):
        results = {}
        for i in range(1, 5):
            for j in range(1, 5):
                results[(i, j)] = Descriptor.compare_two_edges(self.edges[i - 1], other.edges[j - 1])
                results[(i, -j)] = Descriptor.compare_two_edges(self.edges[i - 1], list(reversed(other.edges[j - 1])))
        return results
