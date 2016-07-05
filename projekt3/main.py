import sys
import time
from shaper import Shaper
from edger import Edger
from comparator import Comparator


def parse_cmd():
    img_path = sys.argv[1] + "\\"
    img_number = int(sys.argv[2])
    return img_path, img_number


def parse_images(img_path, img_num):
    parts_descriptions = []
    for i in range(img_num):
        path = img_path + str(i) + ".png"

        s = Shaper()
        polygon, corners, edges_description, contour, img = s.give_description(path)

        e = Edger()
        edges_points = e.select_edges(corners, edges_description, contour)
        edges_characteristics = e.get_n_characteristics(edges_points, img, 16)
        parts_descriptions.append([i, edges_characteristics])

        # # TODO remove
        # print(i)

    c = Comparator()
    array_of_comparisons, array_of_comparisons2 = c.make_ranking(parts_descriptions)

    result = []
    for i in range(len(array_of_comparisons)):
        pom = []
        for k in range(len(array_of_comparisons[i][0])):
            for j in range(4):
                if array_of_comparisons[i][j][k][0] < 10000.0:
                    if array_of_comparisons[i][j][k][1] not in pom:
                        pom.append(array_of_comparisons[i][j][k][1])
        for k in range(len(array_of_comparisons)):
            if (k not in pom) and (k != i):
                pom.append(k)
        result.append(pom)

    for i in range(len(result)):
        s = ""
        for j in range(len(result[i])):
            s += str(result[i][j]) + " "
        print(s)

    return


def main():
    (img_path, img_number) = parse_cmd()
    parse_images(img_path, img_number)


if __name__ == "__main__":
    t0 = time.clock()
    main()

    # # TODO remove
    # print(time.clock() - t0, "seconds process time")