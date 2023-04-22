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

def jaccard_similarity_coefficient(set1,set2):
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return len(intersection) / len(union)
