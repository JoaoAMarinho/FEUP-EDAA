from os.path import join
from PIL import Image
from rembg import remove

INPUT_PATH = "./dataset/bg/"
OUTPUT_PATH = "./dataset/no_bg/"

def remove_background(filepath):
    filename = filepath.split(".", 1)[0]

    image = Image.open(join(INPUT_PATH, filepath))
    removed_bg_image = remove(image)
    removed_bg_image.save(join(OUTPUT_PATH, filename + ".png"))
