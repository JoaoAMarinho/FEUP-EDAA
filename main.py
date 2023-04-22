from src.octree import Octree
from src.color import Color

if __name__ == '__main__':
    octree = Octree()
    octree.add_color(Color(100,100,100))
    octree.add_color(Color(100,150,100))
    octree.add_color(Color(100,200,100))
    octree.add_color(Color(100,100,200))
    octree.add_color(Color(200,100,200))
    octree.add_color(Color(200,100,200))
    octree.add_color(Color(200,100,200))
    octree.add_color(Color(200,100,200))
    octree.add_color(Color(200,100,200))
    # octree.print()

    print("\nREDUCE OCTREEn\n")

    octree.make_palette(16)
    octree.print()