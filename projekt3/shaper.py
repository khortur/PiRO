import numpy as np
from skimage import io
import skimage.measure as msr
import math
import matplotlib.pyplot as plt


class Shaper:
    # zwraca 4 listy i obrazek powiekszony o obramowanie:
    # 1) polygon - lista z glownymi punktami ksztaltu
    # 2) corners - lista naroznikow
    # 3) edges_description - lista liczb, ktore opisuja kolejne krawedzie:
    #    0 -> nie ma wypustki, 1 -> wypustka wypukla, -1 -> wypustka wklesla
    # 4) contour - kontur figury
    # 5) img - obrazek powiekszony o obramowanie
    def give_description(self, path):
        img = io.imread(path)
        shape = img.shape
        w = shape[1]
        h = shape[0]
        base_size = h + 20, w + 20, 4
        base = np.zeros(base_size)
        base[10:h + 10, 10:w + 10, 0:4] = img
        base = base.astype(float)
        base[0:h + 20, 0:w + 20, 0:4] = base / 255.0
        img2 = base

        # binary picture
        img_bin = io.imread(path, as_grey=True)
        for i in range(len(img_bin)):
            for j in range(len(img_bin[i])):
                if img[i][j][3] > 123:
                    img_bin[i][j] = 1.0
                else:
                    img_bin[i][j] = 0.0

        shape = img_bin.shape
        w = shape[1]
        h = shape[0]
        base_size = h + 20, w + 20
        base = np.zeros(base_size)
        base[10:h + 10, 10:w + 10] = img_bin
        img_bin = base

        # contour's points
        contours = msr.find_contours(img_bin, 0.5)
        contours = [max(contours, key=len)]
        polygon = msr.approximate_polygon(contours[0], 5.2)

        polygon = self.remove_flat_points(polygon)
        corners = self.find_4_corners(polygon)
        edges_description = self.describe_edges(corners, polygon)

        # #TODO do usuniecia
        # print(edges_description)
        #
        # # wyswietlenie polygona
        # fig, ax = plt.subplots()
        # ax.imshow(img2, interpolation='nearest', cmap=plt.cm.gray)
        #
        # for n, contour in enumerate([corners]):
        #     ax.plot(contour[:, 1], contour[:, 0], linewidth=5)
        #
        # for n, contour in enumerate([polygon]):
        #     ax.plot(contour[:, 1], contour[:, 0], 'ro')
        #
        # ax.axis('image')
        # ax.set_xticks([])
        # ax.set_yticks([])
        # io.imshow(img2)
        # io.show()
        # #TODO koniec usuniecia

        return polygon, corners, edges_description, contours[0], img2

    # robi liste 4 liczb, ktore opisuja kolejne krawedzie:
    # 0 -> nie ma wypustki, 1 -> wypustka wypukla, -1 -> wypustka wklesla
    def describe_edges(self, corners, polygon):
        polygon_long = [[0, 0]] * (len(polygon) * 2)
        polygon_long[0:len(polygon)] = polygon
        polygon_long[len(polygon):(len(polygon) * 2)] = polygon

        indices_of_corners = []
        t = 0
        for i in range(len(polygon_long)):
            if (polygon_long[i][0] == corners[t][0]) and (polygon_long[i][1] == corners[t][1]):
                t += 1
                indices_of_corners.append(i)
                if t > 3:
                    t = 0

        edges_description = []
        for i in range(4):
            if (indices_of_corners[i] + 3) > indices_of_corners[i + 1]:
                edges_description.append(0)
            else:
                a = polygon_long[indices_of_corners[i]]
                b = polygon_long[indices_of_corners[i + 1]]

                # c = polygon_long[indices_of_corners[i + 2]]
                d = polygon_long[indices_of_corners[i + 3]]

                xi = int((indices_of_corners[i] + indices_of_corners[i + 1]) / 2)
                x = polygon_long[xi]

                alpha = self.angle_from_3_points(x, a, d)
                betcha = self.angle_from_3_points(b, a, d)

                if alpha > betcha:
                    edges_description.append(1)
                else:
                    edges_description.append(-1)

        return edges_description

    def remove_flat_points(self, polygon):
        # delete first point
        polygon = np.delete(polygon, 0, 0)

        polygon2 = []
        for i in range(-2, len(polygon) - 2):
            if self.angle_from_3_points(polygon[i], polygon[i + 1], polygon[i + 2]) < 160:
                polygon2.append(polygon[i + 1])

        return np.asarray(polygon2)

    def find_4_corners(self, polygon):
        corners = []
        linked_corners = []
        pom = []

        for i in range(-2, len(polygon) - 2):
            pom.append([polygon[i + 1], min([self.distance_between_2_points(polygon[i], polygon[i + 1]),
                                             self.distance_between_2_points(polygon[i + 1], polygon[i + 2])])])

        pom = sorted(pom, reverse=True, key=lambda p: p[1])

        for i in range(4):
            corners.append(pom[i][0])

        for point in polygon:
            for corner in corners:
                if (point[0] == corner[0]) and (point[1] == corner[1]):
                    linked_corners.append(point)

        return np.asarray(linked_corners)

    @staticmethod
    def distance_between_line_segment_and_point(line_segment, point):
        x0, y0 = point[0], point[1]
        x1, y1 = line_segment[0][0], line_segment[0][1]
        x2, y2 = line_segment[1][0], line_segment[1][1]

        distance = abs(((y2 - y1) * x0) - ((x2 - x1) * y0) + (x2 * y1) - (y2 * x1)) / math.sqrt(
            math.pow((y2 - y1), 2) + math.pow((x2 - x1), 2))

        return distance

    @staticmethod
    def distance_between_2_points(x, y):
        d = math.hypot(x[0] - y[0], x[1] - y[1])
        return d

    @staticmethod
    def angle_from_3_points(x, y, z):

        delta = 0.001

        a = math.hypot(x[0] - y[0], x[1] - y[1])
        b = math.hypot(y[0] - z[0], y[1] - z[1])
        c = math.hypot(z[0] - x[0], z[1] - x[1])

        if (abs(a + b - c) < delta) or (abs(a + c - b) < delta) or (abs(b + c - a) < delta):
            return 180

        a2 = math.pow(a, 2)
        b2 = math.pow(b, 2)
        c2 = math.pow(c, 2)

        angle = math.acos((a2 + b2 - c2) / (2 * a * b))
        angle2 = int(round(math.degrees(angle)))

        return angle2
