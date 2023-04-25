from os import listdir
from os.path import isfile, join
from rembg import remove
from PIL import Image
from src.octree import Octree
from src.color import Color

BG_PATH = "./dataset/bg/"
NO_BG_PATH = "./dataset/no_bg/"
PALETTE_PATH = "./dataset/palettes/"
QUANTIZED_PATH = "./dataset/quantized/"

### Image processing functions
def remove_backgrounds():
    def remove_background(filename):
        image = Image.open(join(BG_PATH, filename + ".jpg"))
        removed_bg_image = remove(image)
        removed_bg_image.save(join(NO_BG_PATH, filename + ".png"))

    bg_files = [f.split('.')[0] for f in listdir(BG_PATH)
                    if isfile(join(BG_PATH, f))]
    no_bg_files = [f.split('.')[0] for f in listdir(NO_BG_PATH)
                    if isfile(join(NO_BG_PATH, f))]

    files = list(set(bg_files) - set(no_bg_files))
    for file in files:
        remove_background(file)


### Octree functions
def create_octree_from_image(filename, depth):
    image = Image.open(NO_BG_PATH + filename)
    pixels = image.load()
    width, height = image.size

    octree = Octree(depth)
    # add colors to the octree
    for j in range(height):
        for i in range(width):
            octree.add_color(Color(*pixels[i, j]))

    return octree, {"pixels": pixels, "width": width, "height": height}

def create_palette_image(octree, filename, width=16, height=16):
    palette = octree.palette
    palette_image = Image.new('RGB', (width, height))
    palette_pixels = palette_image.load()

    for i, color in enumerate(palette):
        palette_pixels[i%16, i//16] = (color.red, color.green, color.blue)

    palette_image.save(PALETTE_PATH + filename)

def save_quantized_image(octree, filename, img_info):
    pixels, width, height = img_info.values()
    palette = octree.palette

    out_image = Image.new('RGB', (width, height))
    out_pixels = out_image.load()

    for j in range(height):
        for i in range(width):
            index = octree.get_palette_index(Color(*pixels[i, j]))
            color = palette[index]
            out_pixels[i, j] = (color.red, color.green, color.blue)
    out_image.save(QUANTIZED_PATH + filename)

def create_node_id_set_from_image(filename, optimized=True, depth=6, palette_size=256):
    octree, _ = create_octree_from_image(filename, depth)
    if (optimized):
      octree.make_optimized_palette(palette_size)
    else:
      octree.make_palette(palette_size)
    return octree.node_id_set()

def jaccard_similarity_coefficient(set1,set2):
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return len(intersection) / len(union)
