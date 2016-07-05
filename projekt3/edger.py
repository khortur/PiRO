class Edger:
    THRESHOLD = 0.3
    GAUSS_FILTER = [[2.0,  4.0,  5.0,  4.0, 2.0],
                    [4.0,  9.0, 12.0,  9.0, 4.0],
                    [5.0, 12.0, 15.0, 12.0, 5.0],
                    [4.0,  9.0, 12.0,  9.0, 4.0],
                    [2.0,  4.0,  5.0,  4.0, 2.0]]

    def select_edges(self, corners, edges_description, contour):
        edges_points = []

        contour_long = [[0, 0]] * (len(contour) * 2)
        contour_long[0:len(contour)] = contour
        contour_long[len(contour):(len(contour) * 2)] = contour

        indices_of_corners = []
        t = 0
        for i in range(len(contour_long)):
            if self.similar_coordinates(contour_long[i], corners[t]):
                t += 1
                indices_of_corners.append(i)
                if t > 3:
                    t = 0

        for i in range(4):
            size = (indices_of_corners[i+1] - indices_of_corners[i] + 1)
            pom = [[0, 0]] * size
            pom[0:size] = contour_long[indices_of_corners[i]:indices_of_corners[i+1]+1]

            for j in range(len(pom)):
                pom[j][0] = int(pom[j][0])
                pom[j][1] = int(pom[j][1])

            edges_points.append([edges_description[i], pom])

        return edges_points

    def get_n_characteristics(self, edges_points, img, n=16):
        edges_characteristics = []

        for i in range(len(edges_points)):
            last_index_of_points = len(edges_points[i][1])-1

            pom = []
            for j in range(n):
                point_index = int(float(j) / float(n-1) * float(last_index_of_points))
                point = edges_points[i][1][point_index]

                av = self.calculate_average_point(point, img)
                pom.append(av)

            edges_characteristics.append([edges_points[i][0], pom])

        return edges_characteristics

    @staticmethod
    def calculate_average_point(point, img):
        r, b, g = 0.0, 0.0, 0.0
        gauss = 0

        for i in range(5):
            for j in range(5):
                x = point[0]-2+i
                y = point[1]-2+j

                alpha = img[x][y][3]
                if alpha > 0.5:
                    r += (img[x][y][0] * Edger.GAUSS_FILTER[i][j])
                    b += (img[x][y][1] * Edger.GAUSS_FILTER[i][j])
                    g += (img[x][y][2] * Edger.GAUSS_FILTER[i][j])
                    gauss += Edger.GAUSS_FILTER[i][j]

        if gauss > 0:
            r /= gauss
            b /= gauss
            g /= gauss

        return [r, b, g]

    @staticmethod
    def similar_coordinates(a, b):
        x = abs(a[0]-b[0])
        y = abs(a[1]-b[1])

        if (x < Edger.THRESHOLD) and (y < Edger.THRESHOLD):
            return True

        return False
