from src.octree import Octree
from src.color import Color
from random import randint
from src.utils import *

def test_jaccard():

    octree1 = build_rand_octree(10)
    octree2 = build_rand_octree(10)

    reduce_octree(octree1,16)
    reduce_octree(octree2,16)

    similarity = jaccard_similarity_coefficient(octree1.node_id_set(), octree2.node_id_set())

    print("Similarity = " + str(similarity))

def reduce_octree(octree, n_colors):
    print("\nREDUCE OCTREE\n")
    palette = octree.make_palette(n_colors)
    octree.print()

    print("\nPALLET\n")
    for elem in palette:
        print(str(elem), end = "|")

    print("\nLEAVES\n")
    for elem in octree.get_leaves():
        print(str(elem), end = "|")
    print("\n")

def build_octree():
    octree = Octree()

    for r in range(0,255,50):
        for g in range(0,255,50):
            for b in range(0,255,50):
                octree.add_color(Color(r,g,b))

    return octree

def build_rand_octree(x):
    octree = Octree()

    for x in range(0, x):
        r = randint(0,255)
        g = randint(0,255)
        b = randint(0,255)
        octree.add_color(Color(r,g,b))

    return octree

if __name__ == '__main__':
    test_jaccard()


