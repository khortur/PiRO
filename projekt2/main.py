import sys

from skimage import io
from normalizer import Normalizer
from skimage.color import rgb2grey, rgb2hsv

from descriptor import Descriptor
from jigsaw import Jigsaw


def parse_cmd():
    img_path = sys.argv[1] + "\\"
    img_rows = int(sys.argv[2])
    img_cols = int(sys.argv[3])
    return img_path, img_rows, img_cols


def parse_images(img_path, img_num):
    whole_img = io.imread(img_path + "image.png")
    parts = []
    for i in range(img_num):
        img = Normalizer.normalize_one_picture(img_path + str(i) + ".png")
        # Descriptor(img).print_sides()
        # io.imshow(img)
        # io.show()
        parts.append(img)
    return whole_img, parts


def main():
    (img_path, img_rows, img_cols) = parse_cmd()
    (whole_img, parts) = parse_images(img_path, img_rows * img_cols)
    edges_scores = {}
    for i in range(len(parts)):
        edges_scores[i] = {}
        for j in range(1, 5):
            edges_scores[i][j] = []
    for i in range(len(parts)):
        scores = []
        for j in range(len(parts)):
            if i == j:
                continue
            results = Descriptor(parts[i]).compare(Descriptor(parts[j]))
            min_val = 9999999
            min_key = None
            for k in results.keys():
                edges_scores[i][k[0]].append(((j, k[1]), results.get(k)))

                if results.get(k) < min_val:
                    min_val = results.get(k)
                    min_key = k
            print(i, j, (min_key, min_val))
            scores.append((j, (min_val)))
        scores = sorted(scores, key=lambda tup: tup[1])
        print(i, scores)

        for j in range(1, 5):
            edges_scores[i][j] = sorted(edges_scores[i][j], key=lambda tup: tup[1])
            print(edges_scores[i][j])

    j = Jigsaw(edges_scores)

    sol1, sol_val1 = j.solve(img_cols, img_rows)
    sol2, sol_val2 = j.solve(img_rows, img_cols)

    best_solution = sol1
    if sol_val1 < sol_val2:
        best_solution = sol2

    for i in range(len(best_solution)):
        print(best_solution[i])

    # io.imshow(parts[1])
    # io.show()
    # io.imshow(parts[5])
    # io.show()
    #
    # desc1 = Descriptor(parts[1])
    # desc2 = Descriptor(parts[5])
    # print(Descriptor.compare_two_edges(desc1.edges[2], desc2.edges[0]))
    # print(Descriptor.compare_two_edges(desc1.edges[2], list(reversed(desc2.edges[0]))))

if __name__ == "__main__":
    main()
