import numpy as np
import matplotlib.pyplot as plt
import sys
import getopt
import math
import glob
import os
import skimage
import skimage.io as io
import skimage.data as data
import skimage.color as color

from skimage.measure import label
from skimage.transform import rotate
from skimage.transform import resize

# parameters
default_width = 300.0


def process_one_picture(path):
    # read data
    img = io.imread(path, as_grey=True)

    # rotate image
    contours = skimage.measure.find_contours(img, 100.0)
    polygon = skimage.measure.approximate_polygon(contours[0], 2.0)

    # print(len(polygon))
    # print(polygon)
    # print(find_4_basic_points(polygon))

    w, x, y, z = find_4_basic_points(polygon)
    # print(w, x, y, z)
    # io.imshow(img)
    # io.show()

    a = rotate_angle(x, y, z)
    img2 = rotate(img, a, resize=True)
    # io.imshow(img2)
    # io.show()

    # normalize size
    contours2 = skimage.measure.find_contours(img2, 0.3)
    polygon2 = skimage.measure.approximate_polygon(contours2[0], 2.0)

    w, x, y, z = find_4_basic_points(polygon2)

    # mode : {`constant`, `nearest`, `wrap`, `reflect`}
    img3 = resize(img2, resize_output_shape(x, y, img2), mode='nearest')
    io.imshow(img3)
    io.show()

    # # Display the image and plot all contours found
    # fig, ax = plt.subplots()
    # ax.imshow(img, interpolation='nearest', cmap=plt.cm.gray)
    #
    # for n, contour in enumerate(contours):
    #     ax.plot(contour[:, 1], contour[:, 0], linewidth=2)
    #
    # ax.axis('image')
    # ax.set_xticks([])
    # ax.set_yticks([])
    #
    # # io.imshow(img)
    # io.show()
    pass


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
    max1 = list_of_hypotenuses[-2]
    max2 = list_of_hypotenuses[-1]
    for i in range(-1, len(list_of_hypotenuses)-2):
        if list_of_hypotenuses[i][0] + list_of_hypotenuses[i+1][0] > max1[0] + max2[0]:
            max1, max2 = list_of_hypotenuses[i], list_of_hypotenuses[i+1]

    return max1[1], max1[2], max1[3], max2[3]


# returns the length of of the hypotenuse, or -1 if the triangle is not rectangular
def check_if_rectangular_triangle(x, y, z):
    a = math.hypot(x[0]-y[0], x[1]-y[1])
    b = math.hypot(y[0]-z[0], y[1]-z[1])
    c = math.hypot(z[0]-x[0], z[1]-x[1])

    a2 = math.pow(a, 2)
    b2 = math.pow(b, 2)
    c2 = math.pow(c, 2)

    r = -1.0

    if (c2 * 1.1 > a2 + b2) and (c2 < (a2 + b2) * 1.1):
        r = c

    return r


# return the angle which to rotate figure in degrees
def rotate_angle(x, y, z):
    a = x[0] - y[0]
    c = math.hypot(x[0]-y[0], x[1]-y[1])

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

    a = math.hypot(x[0]-y[0], x[1]-y[1])
    res = default_width / a

    return int(round(width * res)), int(round(height * res))


def main():
    # process_one_picture('daneA/set0/5.png')
    os.chdir("daneA/set0")
    for file in glob.glob("*.png"):
        process_one_picture(file)

if __name__ == "__main__":
    main()
