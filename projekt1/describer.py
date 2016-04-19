from normalizer import Normalizer


class Describer:
    PARTS_AMOUNT = 30

    def __init__(self, img):
        self.img = img
        self.width = img.shape[1]
        self.height = img.shape[0]

    def as_angles(self):
        angles = []

        for x1 in range(0, self.width, int(self.width / Describer.PARTS_AMOUNT)):
            x2 = min(self.width - 1, x1 + self.width / Describer.PARTS_AMOUNT)
            xs = (x1 + x2) / 2

            y1 = self.find_highest_set(x1)
            y2 = self.find_highest_set(x2)
            ys = self.find_highest_set(xs)

            if y1 != -1 and y2 != -1 and ys != -1:
                angles.append(Normalizer.angle_from_3_points([x1, y1], [xs, ys], [x2, y2]))

        return angles

    def find_highest_set(self, x):
        return max(range(self.height), key=lambda y: y if self.img[y, x] > 0.0 else -1)
