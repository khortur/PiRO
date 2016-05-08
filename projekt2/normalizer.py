import numpy as np
from skimage import io
from skimage import transform as tf
import skimage.measure as msr
import math


class Normalizer:
    CUT_ANGLE = 165.0
    CUT_LENGTH_PERCENT = 10.0

    @staticmethod
    def find_4_points(img_bin):
        a, b, c, d = [0, 0], [0, 0], [0, 0], [0, 0]
        t = True

        for i in range(len(img_bin)):
            for j in range(len(img_bin[i])):
                if img_bin[i][j] == 255:
                    if t:
                        a = [j, i]
                        t = False
                    c = [j, i]

        t = True
        for j in range(len(img_bin[0])):
            for i in range(len(img_bin)):
                if img_bin[i][j] == 255:
                    if t:
                        b = [j, i]
                        t = False
                    d = [j, i]

        return [a, b, c, d]

    @staticmethod
    def angle_from_3_points(x, y, z):

        delta = 0.001

        a = math.hypot(x[0]-y[0], x[1]-y[1])
        b = math.hypot(y[0]-z[0], y[1]-z[1])
        c = math.hypot(z[0]-x[0], z[1]-x[1])

        if (abs(a + b - c) < delta) or (abs(a + c - b) < delta) or (abs(b + c - a) < delta):
            return 180

        a2 = math.pow(a, 2)
        b2 = math.pow(b, 2)
        c2 = math.pow(c, 2)

        angle = math.acos((a2 + b2 - c2) / (2 * a * b))

        return int(round(math.degrees(angle)))

    @staticmethod
    def result_contains_point(point, result):
        for i in range(4):
            if (point[0] == result[i][0]) and (point[1] == result[i][1]):
                return True
        return False

    @staticmethod
    def find_4_points_2(img):
        contours = msr.find_contours(img, 100.0)

        contours = [max(contours, key=len)]

        polygon = msr.approximate_polygon(contours[0], 2.0)

        # find 4 points with smallest angles
        polygon_with_angles = []
        polygon = np.delete(polygon, 0, 0)
        for i in range(len(polygon)):
            x, y, z = polygon[i-2], polygon[i-1], polygon[i]
            angle = Normalizer.angle_from_3_points(x, y, z)
            polygon_with_angles.append((angle, polygon[i-1]))

        polygon_with_angles = sorted(polygon_with_angles, key=lambda ang: ang[0])

        result = []
        for i in range(4):
            result.append(polygon_with_angles[i][1])

        # make good order
        result_ordered = []
        for i in range(len(polygon)):
            if Normalizer.result_contains_point(polygon[i], result):
                result_ordered.append(polygon[i])

        for i in range(4):
            result_ordered[i][0], result_ordered[i][1] = result_ordered[i][1], result_ordered[i][0]

        return result_ordered

    @staticmethod
    def normalize_one_picture(path):
        img = io.imread(path)

        # binary picture
        img_bin = io.imread(path, as_grey=True)
        for i in range(len(img_bin)):
            for j in range(len(img_bin[i])):
                if img[i][j][3] > 123:
                    img_bin[i][j] = 255
                else:
                    img_bin[i][j] = 0

        polygon = np.asarray(Normalizer.find_4_points_2(img_bin))

        # # show picture with founded corners
        # fig, ax = plt.subplots()
        # ax.imshow(img, interpolation='nearest', cmap=plt.cm.gray)
        # for n, contour in enumerate([polygon]):
        #     ax.plot(contour[:, 0], contour[:, 1], 'ro')
        #
        # ax.axis('image')
        # ax.set_xticks([])
        # ax.set_yticks([])
        # io.imshow(img)
        # io.show()

        # remove perspective
        src = np.array((
            (0, 0),
            (0, 300),
            (300, 300),
            (300, 0)
        ))
        dst = polygon
        t_form = tf.ProjectiveTransform()
        t_form.estimate(src, dst)
        warped = tf.warp(img, t_form, output_shape=(300, 300))

        return warped
