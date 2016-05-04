import numpy as np
from skimage import io

from normalizer import Normalizer


class Characteristic:

    def __init__(self, img):
        self.img = img
        self.list_of_angles = []

        self.img[self.img > 0.3] = 1.0
        self.img[self.img < 0.5] = 0.0

        self.calculate_list_of_angles()

    def compare_two_characteristics(self, ch2):
        if len(self.list_of_angles) != len(ch2.list_of_angles):
            smaller = min([self.list_of_angles, ch2.list_of_angles], key=len)
            bigger = max([self.list_of_angles, ch2.list_of_angles], key=len)
        else:
            smaller = self.list_of_angles
            bigger = ch2.list_of_angles

        min_sum_of_diffs = -1.0
        for i in range(len(bigger)-len(smaller)+1):
            sum_of_diffs = 0.0
            for j in range(len(smaller)):
                diff = abs(bigger[j+i] - smaller[-j])
                sum_of_diffs += diff
            if min_sum_of_diffs > sum_of_diffs or min_sum_of_diffs < 0.0:
                min_sum_of_diffs = sum_of_diffs

        return min_sum_of_diffs

    def calculate_list_of_angles(self):
        list_of_heights = self.calculate_list_of_heights()

        for i in range(5, len(list_of_heights)-5):
            x = [i-5, list_of_heights[i-5]]
            y = [i, list_of_heights[i]]
            z = [i+5, list_of_heights[i+5]]

            angle = Normalizer.angle_from_3_points(x,y,z)

            self.list_of_angles.append(angle)

        return

    def calculate_list_of_heights(self):
        list_of_heights = []
        for i in range(np.shape(self.img)[1]):
            temp = self.calculate_height_of_column(i)

            if temp >= 0:
                list_of_heights.append(temp)

        return list_of_heights

    def calculate_height_of_column(self, column_id):
        height = -1
        for i in range(np.shape(self.img)[0]):
            if self.img[i][column_id] > 0.0:
                height = i
                break

        return height

    def test(self):
        print("debug")
        io.imshow(self.img)
        io.show()