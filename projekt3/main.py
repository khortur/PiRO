import sys
import time
from skimage import io
from shaper import Shaper


def parse_cmd():
    img_path = sys.argv[1] + "\\"
    img_number = int(sys.argv[2])
    return img_path, img_number


def parse_images(img_path, img_num):
    parts_descriptions = []
    for i in range(img_num):
        s = Shaper()
        polygon, corners, edges_description = s.give_description(img_path + str(i) + ".png")
        parts_descriptions.append((polygon, corners, edges_description))
    return


def main():
    (img_path, img_number) = parse_cmd()
    parse_images(img_path, img_number)


if __name__ == "__main__":
    t0 = time.clock()
    main()
    print(time.clock() - t0, "seconds process time")