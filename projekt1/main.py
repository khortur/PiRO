import sys

from characterisitc import Characteristic
from normalizer import Normalizer


def parse_cmd():
    img_path = sys.argv[1] + "\\"
    img_num = int(sys.argv[2])
    return img_path, img_num


def parse_images(img_path, img_num):
    characteristics = []

    for i in range(img_num):
        img = Normalizer.normalize_one_picture(img_path + str(i) + ".png")
        characteristics.append(Characteristic(img))

    results = []

    for i in range(len(characteristics)):
        unsorted_results = []
        for j in range(len(characteristics)):
            unsorted_results.append([characteristics[i].compare_two_characteristics(characteristics[j]), j])
        results.append(sorted(unsorted_results, key=lambda x: x[0]))

    for i in range(len(results)):
        line = ""
        for j in range(min(len(characteristics) - 1, 10)):
            line += str(results[i][j][1]) + " "
        print(line)


def main():
    (img_path, img_num) = parse_cmd()
    parse_images(img_path, img_num)

if __name__ == "__main__":
    main()
