from skimage.transform import rotate


class Descriptor:
    WIDTH_PARTS = 100.0
    HEIGHT_PARTS = 100.0
    DISTANCE_FROM_EDGE = 1
    EDGE_WIDTH = 1
    MAX_DIFFERENCE = 2

    score_cache = {}

    def __init__(self, img, img_num):
        self.img = img
        self.edges = []
        self.img_num = img_num

        self.top_edge = img[Descriptor.DISTANCE_FROM_EDGE, :]
        self.bottom_edge = img[img.shape[0] - 1 - Descriptor.DISTANCE_FROM_EDGE, :]
        self.left_edge = img[:, Descriptor.DISTANCE_FROM_EDGE]
        self.right_edge = img[:, img.shape[1] - 1 - Descriptor.DISTANCE_FROM_EDGE]

        self.bottom_edge = list(reversed(self.bottom_edge))
        self.left_edge = list(reversed(self.left_edge))

        self.edges.append(self.top_edge)
        self.edges.append(self.right_edge)
        self.edges.append(self.bottom_edge)
        self.edges.append(self.left_edge)

        self.rotation = 0

    def print_sides(self):
        print("TOP: ", self.edges[0])
        print("RIGHT: ", self.edges[1])
        print("BOTTOM: ", self.edges[2])
        print("LEFT: ", self.edges[3])

    def get_rotated(self, rotation):
        rotated_img = rotate(self.img, rotation * 90.0)
        result = Descriptor(rotated_img, self.img_num)
        result.rotation = (self.rotation + rotation) % 4
        return result

    @staticmethod
    def compare_two_edges(edge1, edge2, e1_id=(-1, -1), e2_id=(-1, -1)):
        # print(e1_id, e2_id)
        if (e1_id, e2_id) in Descriptor.score_cache.keys():
            return Descriptor.score_cache[(e1_id, e2_id)]
        if (e2_id, e1_id) in Descriptor.score_cache.keys():
            return Descriptor.score_cache[(e2_id, e1_id)]

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

        Descriptor.score_cache[(e1_id, e2_id)] = result

        return result

    def compare(self, other):
        results = {}
        for i in range(1, 5):
            for j in range(1, 5):
                # results[(i, j)] = Descriptor.compare_two_edges(self.edges[i - 1], other.edges[j - 1])
                results[(i, j)] = Descriptor.compare_two_edges(self.edges[i - 1], list(reversed(other.edges[j - 1])))
        return results
