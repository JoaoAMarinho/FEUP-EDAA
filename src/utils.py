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
IMAGE_SIZE = 518400

### Image processing functions
def remove_backgrounds(bg_path=BG_PATH, no_bg_path=NO_BG_PATH):
    def remove_background(filename):
        image = Image.open(join(bg_path, filename + ".jpg"))
        removed_bg_image = remove(image)
        removed_bg_image.save(join(no_bg_path, filename + ".png"))

    bg_files = [f.split('.')[0] for f in listdir(bg_path)
                    if isfile(join(bg_path, f))]
    no_bg_files = [f.split('.')[0] for f in listdir(no_bg_path)
                    if isfile(join(no_bg_path, f))]

    files = list(set(bg_files) - set(no_bg_files))
    for file in files:
        remove_background(file)

### Comparison pipeline functions
def create_features_labels(RIPENESS_LEVELS):
    X = []
    y = []
    for ripeness_level in RIPENESS_LEVELS:
        path = NO_BG_PATH + ripeness_level
        files = [f"{ripeness_level}/{f}" for f in listdir(path) 
                 if isfile(join(path, f))]
        X.extend(files)
        y.extend([ripeness_level] * len(files))

    return X, y


### Octree functions
def create_octree_from_image(filename, depth, resize=False):
    image = Image.open(NO_BG_PATH + filename)

    if resize:
        width, height = image.size
        curr_size = width * height
        factor = curr_size // IMAGE_SIZE
        if factor > 1:
            image = image.resize((width // factor, height // factor))

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

def create_node_id_set_from_image(filename, optimized=True,
                                  depth=6, palette_size=256, resize=False):
    octree, _ = create_octree_from_image(filename, depth, resize)
    if optimized:
        octree.make_optimized_palette(palette_size)
    else:
        octree.make_palette(palette_size)
    return octree.node_id_set()

def jaccard_similarity_coefficient(set1,set2):
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return len(intersection) / len(union)
