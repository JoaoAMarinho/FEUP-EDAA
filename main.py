from src.octree import Octree
from src.color import Color

if __name__ == '__main__':
    octree = Octree()
    octree.add_color(Color(100,100,100))
    octree.add_color(Color(100,150,100))
    octree.add_color(Color(100,200,100))
    octree.add_color(Color(100,100,200))
    octree.add_color(Color(0,0,200))
    octree.add_color(Color(200,100,200))
    octree.add_color(Color(0,100,200))
    octree.add_color(Color(200,0,200))
    octree.add_color(Color(10,100,200))
    # octree.print()

    print("\nREDUCE OCTREE\n")

    palette = octree.make_palette(4)
    octree.print()

    print("\nPALLET\n")
    for elem in palette:
        print(str(elem), end = "|")

    print("\nLEAVES\n")
    for elem in octree.get_leaves():
        print(str(elem), end = "|")
