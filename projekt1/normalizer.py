import math
import numpy as np
from skimage import io
import skimage.measure as msr
from skimage.transform import rotate, resize


class Normalizer:

    CUT_ANGLE = 165.0
    CUT_LENGTH_PERCENT = 10.0
    APPROXIMATE_PARAMETER_PERCENT = 50.0
    DEFAULT_WIDTH = 100.0
    CHARACTERISTIC_CIRCLE_RADIUS = 3.0
    ANGLE_90_ERROR = 1.1

    def __init__(self):
        pass

    @staticmethod
    def normalize_one_picture(path):

        # Read data
        img = io.imread(path, as_grey=True)

        img[img > 50] = 255
        img[img < 125] = 0

        shape = img.shape
        max_shape = max(shape[0], shape[1])
        approximate_parameter = max_shape/Normalizer.APPROXIMATE_PARAMETER_PERCENT
        cut_length = max_shape/Normalizer.CUT_LENGTH_PERCENT

        # Rotate image
        contours = msr.find_contours(img, 100.0)

        contours = [max(contours, key=len)]

        polygon = msr.approximate_polygon(contours[0], approximate_parameter)

        # Delete first, doubled, point
        polygon = np.delete(polygon, 0, 0)

        # Delete points in a middle of a straight line
        list_of_points_to_remove = []
        for i in range(len(polygon)):
            x, y, z = polygon[i-2], polygon[i-1], polygon[i]
            angle = Normalizer.angle_from_3_points(x, y, z)
            xy = math.hypot(x[0]-y[0], x[1]-y[1])
            yz = math.hypot(z[0]-y[0], z[1]-y[1])
            if ((angle > Normalizer.CUT_ANGLE) and ((xy < cut_length) or (yz < cut_length))) or (angle > 175.0):
                if i-1 < 0:
                    list_of_points_to_remove.append(i-1+len(polygon))
                else:
                    list_of_points_to_remove.append(i-1)

        for i in list_of_points_to_remove:
            polygon = np.delete(polygon, i, 0)
        polygon = np.append(polygon, [polygon[0]], 0)

        # update angle_90_error
        if len(polygon) < 5:
            Normalizer.ANGLE_90_ERROR = 1.05

        w, x, y, z = Normalizer.find_4_basic_points(polygon)

        a = Normalizer.rotate_angle(x, y, z)
        img = io.imread(path, as_grey=True)
        img2 = rotate(img, a, resize=True)

        # normalize size
        contours2 = msr.find_contours(img2, 0.1)

        if len(contours2) > 1:
            maxi = contours2[0]
            for i in contours2:
                if len(i) > len(maxi):
                    maxi = i
            contours2 = [maxi]

        polygon = msr.approximate_polygon(contours2[0], 2.0)

        x = polygon[0]
        y = polygon[0]

        for i in range(len(polygon)):
            if x[1] > polygon[i][1]:
                x = polygon[i]
            if y[1] < polygon[i][1]:
                y = polygon[i]

        # mode : {`constant`, `nearest`, `wrap`, `reflect`}
        img3 = resize(img2, Normalizer.resize_output_shape(x, y, img2), mode='nearest')

        return img3

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

    # return the skeleton of rectangle
    @staticmethod
    def find_4_basic_points(polygon):
        list_of_hypotenuses = []
        for i in range(0, len(polygon)-2):
            x, y, z = polygon[i], polygon[i+1], polygon[i+2]
            list_of_hypotenuses.append([Normalizer.check_if_rectangular_triangle(x, y, z), x, y, z])

        # end values
        x, y, z = polygon[len(polygon)-2], polygon[len(polygon)-1], polygon[1]
        list_of_hypotenuses.append([Normalizer.check_if_rectangular_triangle(x, y, z), x, y, z])

        # find 2 maximums
        if len(list_of_hypotenuses) < 2:
            return [0, 0], [0, 0], [0, 0], [0, 0]
        max1 = list_of_hypotenuses[-2]
        max2 = list_of_hypotenuses[-1]
        for i in range(-1, len(list_of_hypotenuses)-2):
            if list_of_hypotenuses[i][0] + list_of_hypotenuses[i+1][0] > max1[0] + max2[0]:
                max1, max2 = list_of_hypotenuses[i], list_of_hypotenuses[i+1]

        if len(list_of_hypotenuses) > 2:
            if list_of_hypotenuses[-3][0] + list_of_hypotenuses[-2][0] >= max1[0] + max2[0]:
                max1, max2 = list_of_hypotenuses[-3], list_of_hypotenuses[-2]

        return max1[1], max1[2], max1[3], max2[3]

    # returns the length of of the hypotenuse, or -1 if the triangle is not rectangular
    @staticmethod
    def check_if_rectangular_triangle(x, y, z):
        a = math.hypot(x[0]-y[0], x[1]-y[1])
        b = math.hypot(y[0]-z[0], y[1]-z[1])
        c = math.hypot(z[0]-x[0], z[1]-x[1])

        a2 = math.pow(a, 2)
        b2 = math.pow(b, 2)
        c2 = math.pow(c, 2)

        r = -1.0

        if (c2 * Normalizer.ANGLE_90_ERROR > a2 + b2) and (c2 < (a2 + b2) * Normalizer.ANGLE_90_ERROR):
            if (Normalizer.angle_from_3_points(x, y, z) > 100.0) or (Normalizer.angle_from_3_points(x, y, z) < 80.0):
                r = 0.0
            else:
                r = c

        return r

    # return the angle which to rotate figure in degrees
    @staticmethod
    def rotate_angle(x, y, z):
        a = x[0] - y[0]
        c = math.hypot(x[0]-y[0], x[1]-y[1])

        sin = 1.0
        if c > 0:
            sin = a / c

        angle = math.degrees(math.asin(sin))

        # when the base is at the top
        if y[0] < z[0]:
            angle = 180.0 - angle

        return angle

    # return output_shape parameter to skimage.transform.resize function
    @staticmethod
    def resize_output_shape(x, y, img):
        width, height = img.shape

        a = math.hypot(0.0, x[1]-y[1])
        res = Normalizer.DEFAULT_WIDTH / a

        return int(round(width * res)), int(round(height * res))
