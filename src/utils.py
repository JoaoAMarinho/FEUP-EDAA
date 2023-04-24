from os.path import join
from PIL import Image
from rembg import remove
from src.octree import Octree
from src.color import Color

INPUT_PATH = "./dataset/bg/"
OUTPUT_PATH = "./dataset/no_bg/"

def create_octree_image(filepath, depth):
    image = Image.open(filepath)
    pixels = image.load()
    width, height = image.size

    octree = Octree(depth)
    # add colors to the octree
    for j in range(height):
        for i in range(width):
            octree.add_color(Color(*pixels[i, j]))

    return octree, {"pixels": pixels, "width": width, "height": height}


def create_palette_image(palette, filepath, width=16, height=16):
    palette_image = Image.new('RGB', (width, height))
    palette_pixels = palette_image.load()

    for i, color in enumerate(palette):
        palette_pixels[i%16, i//16] = (color.red, color.green, color.blue)

    palette_image.save(filepath)


def remove_background(filepath):
    filename = filepath.split(".", 1)[0]

    image = Image.open(join(INPUT_PATH, filepath))
    removed_bg_image = remove(image)
    removed_bg_image.save(join(OUTPUT_PATH, filename + ".png"))

def jaccard_similarity_coefficient(set1,set2):
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return len(intersection) / len(union)
