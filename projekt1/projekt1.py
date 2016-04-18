import math
import glob
import os
import numpy as np
import matplotlib.pyplot as plt
import skimage
import skimage.io as io

from skimage.measure import label
from skimage.transform import rotate
from skimage.transform import resize

# parameters
default_width = 100.0
characteristic_circle_radius = 3.0
angle_90_error = 1.1


def normalize_one_picture(path):
    global angle_90_error

    # paramters
    cut_angle = 165.0
    cut_length_percent = 10.0
    approximate_parameter_percent = 50.0

    # read data
    img = io.imread(path, as_grey=True)

    img[img > 50] = 255
    img[img < 125] = 0

    # paramters cd
    shape = img.shape
    bigger_shape = shape[0]
    if shape[1] > bigger_shape:
        bigger_shape = shape[1]
    approximate_parameter = bigger_shape/approximate_parameter_percent
    cut_length = bigger_shape/cut_length_percent

    # rotate image
    contours = skimage.measure.find_contours(img, 100.0)
    # print(len(contours))

    if len(contours) > 1:
        maxi = contours[0]
        for i in contours:
            if len(i) > len(maxi):
                maxi = i
        contours = [maxi]
    # print(len(contours))

    polygon = skimage.measure.approximate_polygon(contours[0], approximate_parameter)

    # ulepszenie polygon'a'
    polygon2 = np.delete(polygon, 0, 0)
    # print(polygon2)
    list_of_points_to_remove = []
    for i in range(len(polygon2)):
        # if i < len(polygon2)-1:
        angle = angle_from_3_points(polygon2[i-2], polygon2[i-1], polygon2[i])
        x, y, z = polygon2[i-2], polygon2[i-1], polygon2[i]
        xy = math.hypot(x[0]-y[0], x[1]-y[1])
        yz = math.hypot(z[0]-y[0], z[1]-y[1])
        if ((angle > cut_angle) and ((xy < cut_length) or (yz < cut_length))) or (angle > 175.0):
            if i-1 < 0:
                list_of_points_to_remove.append(i-1+len(polygon2))
            else:
                list_of_points_to_remove.append(i-1)
    # print("list_of_points_to_remove:")
    # print(list_of_points_to_remove)
    # print("end")

    for i in list_of_points_to_remove:
        polygon2 = np.delete(polygon2, i, 0)
    polygon = np.append(polygon2, [polygon2[0]], 0)
    # print(polygon2)

    # update angle_90_error
    if len(polygon2) < 5:
        angle_90_error = 1.05

    w, x, y, z = find_4_basic_points(polygon)

    # io.imshow(img)
    # io.show()

    p = [w.tolist(), x.tolist(), y.tolist(), z.tolist()]
    p2 = np.asarray(p)

    polygons = [p2]

    # polygons.append(p)
    # print(polygons)
    # print(polygon)

    # # wyswietlenie polygona
    # fig, ax = plt.subplots()
    # ax.imshow(img, interpolation='nearest', cmap=plt.cm.gray)
    # for n, contour in enumerate(polygons):
    #     ax.plot(contour[:, 1], contour[:, 0], linewidth=5)
    #
    # for n, contour in enumerate([polygon]):
    #     ax.plot(contour[:, 1], contour[:, 0], 'ro')
    #
    # ax.axis('image')
    # ax.set_xticks([])
    # ax.set_yticks([])
    # io.imshow(img)
    # io.show()

    # ax.plot(contour[:, 1], contour[:, 0], 'ro')

    # print(len(contours))
    # print(len(polygon))
    # print(polygon)
    # print(find_4_basic_points(polygon))

    w, x, y, z = find_4_basic_points(polygon)
    # print(w, x, y, z)
    # io.imshow(img)
    # io.show()

    a = rotate_angle(x, y, z)
    img = io.imread(path, as_grey=True)
    img2 = rotate(img, a, resize=True)
    # io.imshow(img2)
    # io.show()

    # normalize size
    contours2 = skimage.measure.find_contours(img2, 0.1)

    if len(contours2) > 1:
        maxi = contours2[0]
        for i in contours2:
            if len(i) > len(maxi):
                maxi = i
        contours2 = [maxi]

    polygon2 = skimage.measure.approximate_polygon(contours2[0], 2.0)

    x = polygon2[0]
    y = polygon2[0]

    for i in range(len(polygon2)):
        if x[1] > polygon2[i][1]:
            x = polygon2[i]
        if y[1] < polygon2[i][1]:
            y = polygon2[i]

    # mode : {`constant`, `nearest`, `wrap`, `reflect`}
    img3 = resize(img2, resize_output_shape(x, y, img2), mode='nearest')

    return img3


# return the skeleton of rectangle
def find_4_basic_points(polygon):
    list_of_hypotenuses = []
    for i in range(0, len(polygon)-2):
        x, y, z = polygon[i], polygon[i+1], polygon[i+2]
        list_of_hypotenuses.append([check_if_rectangular_triangle(x, y, z), x, y, z])

    # end values
    x, y, z = polygon[len(polygon)-2], polygon[len(polygon)-1], polygon[1]
    list_of_hypotenuses.append([check_if_rectangular_triangle(x, y, z), x, y, z])

    # x, y, z = polygon[len(polygon)-1], polygon[1], polygon[2]
    # list_of_hypotenuses.append([check_if_rectangular_triangle(x, y, z), x, y, z])

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
def check_if_rectangular_triangle(x, y, z):
    global angle_90_error

    a = math.hypot(x[0]-y[0], x[1]-y[1])
    b = math.hypot(y[0]-z[0], y[1]-z[1])
    c = math.hypot(z[0]-x[0], z[1]-x[1])

    a2 = math.pow(a, 2)
    b2 = math.pow(b, 2)
    c2 = math.pow(c, 2)

    r = -1.0

    if (c2 * angle_90_error > a2 + b2) and (c2 < (a2 + b2) * angle_90_error):
        if (angle_from_3_points(x, y, z) > 100.0) or (angle_from_3_points(x, y, z) < 80.0):
            r = 0.0
        else:
            r = c

    return r


# return the angle which to rotate figure in degrees
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
def resize_output_shape(x, y, img):
    global default_width

    width, height = img.shape

    # a = math.hypot(x[0]-y[0], x[1]-y[1])
    a = math.hypot(0.0, x[1]-y[1])
    res = default_width / a

    return int(round(width * res)), int(round(height * res))


# return angle between 3 points
def angle_from_3_points(x, y, z):
    a = math.hypot(x[0]-y[0], x[1]-y[1])
    b = math.hypot(y[0]-z[0], y[1]-z[1])
    c = math.hypot(z[0]-x[0], z[1]-x[1])

    a2 = math.pow(a, 2)
    b2 = math.pow(b, 2)
    c2 = math.pow(c, 2)

    angle = math.acos((a2 + b2 - c2) / (2 * a * b))

    return int(round(math.degrees(angle)))


def main():
    os.chdir("daneA/set0")

    for file in glob.glob("*.png"):
        img = normalize_one_picture(file)
        io.imshow(img)
        print(file)
        io.show()

    return 0

if __name__ == "__main__":
    main()
