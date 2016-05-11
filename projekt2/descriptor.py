class Descriptor:
    WIDTH_PARTS = 100.0
    HEIGHT_PARTS = 100.0

    def __init__(self, img):
        self.img = img
        self.edges = []

        top_edge = []
        bottom_edge = []
        for x in range(img.shape[1]):
            top_edge.append(img[1][x])
            bottom_edge.append(img[img.shape[0] - 2][img.shape[1] - 1 - x])

        left_edge = []
        right_edge = []
        for y in range(img.shape[0]):
            left_edge.append(img[img.shape[0] - 1 - y][1])
            right_edge.append(img[y][img.shape[1] - 2])

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
            for channel in range(3):
                result += abs(edge1[i][channel] - edge2[i][channel])
        return result

    def compare(self, other):
        results = {}
        for i in range(1, 5):
            for j in range(1, 5):
                results[(i, j)] = Descriptor.compare_two_edges(self.edges[i - 1], other.edges[j - 1])
                results[(i, -j)] = Descriptor.compare_two_edges(self.edges[i - 1], list(reversed(other.edges[j - 1])))
        return results
