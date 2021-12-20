import argparse
import numpy as np
from PIL import Image
from pathlib import Path


class pixelArtGenerator:

    def __init__(self, gradations= 6, pixel_step = 10):
        self.step = pixel_step
        self.gradation = 255 / gradations

    def get_pixel_color(self, img_array, i, j):
        return np.sum(img_array[i: i + self.step, j: j + self.step]) // (self.step ** 2)

    def set_pixel_color(self, img_array, i, j, s):
        img_array[i: i + self.step, j: j + self.step] = int(s // self.gradation) * self.gradation / 3
        return img_array

    def generate(self, image):
        img_array = np.array(image)
        h, w = len(img_array), len(img_array[1])
        for i in range(0, h, self.step):
            for j in range(0, w, self.step):
                color = self.get_pixel_color(img_array, i, j)
                img_array = self.set_pixel_color(img_array, i, j, color)
        return Image.fromarray(img_array)


def create_argparse():
    cli_parser = argparse.ArgumentParser()
    cli_parser.add_argument("-o", "--output", help="Output file name", required=True, type=Path)
    cli_parser.add_argument("-i", "--input", help="Input file name", required=True, type=Path)
    cli_parser.add_argument("-g", "--gradation", help="Gradations step", default=6, type=int)
    cli_parser.add_argument("-s", "--size", help="Pixel size", default=10, type=int)
    return cli_parser

if __name__ == "__main__":
    parser = create_argparse()
    args = parser.parse_args()
    img = Image.open(args.input)
    generator = PixelArtGenerator(args.gradation, args.size)
    generator.generate(img).save(args.output)