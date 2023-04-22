from src.node import Node

class Octree():
    """
    Octree Quantizer class for image color quantization

    Use MAX_DEPTH to limit the number of levels, can not be greater than 8
    due to how colors are represented (8 bits per channel)
    """

    MAX_DEPTH = 8

    def __init__(self, depth=MAX_DEPTH):
        """
        Init Octree Quantizer
        """
        self.depth = depth
        self.levels = {i: [] for i in range(self.depth)}
        self.root = Node(0, self)

    def get_leaves(self):
        """
        Get all leaves
        """
        return self.root.get_leaf_nodes()

    def add_level_node(self, level, node):
        """
        Add `node` to the nodes at `level`
        """
        self.levels[level].append(node)

    def add_color(self, color):
        """
        Add `color` to the Octree
        """
        if color.is_transparent():
            return
        # passes self value as `parent` to save nodes to levels dict
        self.root.add_color(color, 0, self)

    def make_palette(self, color_count):
        """
        Make color palette with `color_count` colors maximum
        """
        palette = []
        palette_index = 0
        leaf_count = len(self.get_leaves())

        # remove leaves level by level
        for level in range(self.depth - 1, -1, -1):
            if leaf_count <= color_count:
                break

            n_level_nodes = len(self.levels[level])
            if n_level_nodes == 0:
                continue

            index = -1
            for i in range(n_level_nodes):
                node = self.levels[level][i]
                leaf_count -= node.remove_leaves()
                if leaf_count <= color_count:
                    index = i
                    break

            # remove the whole level if all nodes are leaves
            # otherwise keep the remaining ones
            self.levels[level] = [] if index == -1 \
                                    else self.levels[level][index + 1:]
            self.depth -= 1 if index == -1 else 0

        # build palette
        for node in self.get_leaves():
            if palette_index >= color_count:
                break
            if node.is_leaf():
                palette.append(node.get_color())
            node.palette_index = palette_index
            palette_index += 1
        return palette
    
    def make_palette_2(self, color_count):
        """
        Make color palette with `color_count` colors maximum
        """
        palette = []
        palette_index = 0
        leaf_count = len(self.get_leaves())
        # reduce nodes
        # up to 8 leaves can be reduced here and the palette will have
        # only 248 colors (in worst case) instead of expected 256 colors
        for level in range(self.depth - 1, -1, -1):
            if leaf_count <= color_count:
                    break
            if self.levels[level]:
                nodes = self.levels[level]
                nodes.sort(key=lambda x: x.pixels)
                for node in nodes:
                    leaf_count -= node.remove_leaves()
                    if leaf_count <= color_count:
                        break
                self.levels[level] = []
        # build palette
        for node in self.get_leaves():
            if palette_index >= color_count:
                break
            if node.is_leaf():
                palette.append(node.get_color())
            node.palette_index = palette_index
            palette_index += 1
        return palette

    def get_palette_index(self, color):
        """
        Get palette index for `color`
        """
        return self.root.get_palette_index(color, 0)

if __name__ == '__main__':
    octree = Octree()
