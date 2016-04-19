import sys

from skimage import io

import numpy as np

from describer import Describer
from normalizer import Normalizer
from characterisitc import Characteristic


def parse_cmd():
    img_path = sys.argv[1] + "\\"
    img_num = int(sys.argv[2])
    return img_path, img_num


def parse_images(img_path, img_num):
    characteristics = []

    for i in range(img_num):
        img = Normalizer.normalize_one_picture(img_path + str(i) + ".png")

        # print(img)
        # desc = Describer(img)
        io.imshow(img)
        # print(img_path + str(i) + ".png")
        # print(desc.as_angles())
        # io.show()

        characteristics.append(Characteristic(img))

        # images = []
        # for i in range(img_num):
        #     images.append(parse_image(img_path + str(i) + ".png"))
        # images.append(parse_image(img_path + "7.png"))
        # return images

    results = []

    for i in range(len(characteristics)):
        results.append([])

        for j in range(len(characteristics)):
            results[i].append([characteristics[i].compare_two_characteristics(characteristics[j]), j])
        results[i].sort()

    for i in range(len(results)):
        print(results[i])


def main():
    # np.set_printoptions(threshold=np.nan)
    (img_path, img_num) = parse_cmd()
    parse_images(img_path, img_num)

if __name__ == "__main__":
    main()
