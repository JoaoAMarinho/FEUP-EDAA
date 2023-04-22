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
        self.levels = {i: [] for i in range(1, self.depth+1)}
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
        self.root.add_color(color, 1, self)

    def make_palette(self, color_count):
        """
        Make color palette with `color_count` colors maximum
        """
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

        return self._build_palette(color_count)
    
    def make_optimized_palette(self, color_count):
        """
        Make color palette with `color_count` colors maximum
        by removing nodes with the least number of pixels
        """
        leaf_count = len(self.get_leaves())

        # remove leaves level by level
        for level in range(self.depth - 1, -1, -1):
            if leaf_count <= color_count:
                break

            n_level_nodes = len(self.levels[level])
            if n_level_nodes == 0:
                continue

            index = -1
            nodes = self.levels[level]
            nodes.sort(key=lambda x: x.pixel_count)
            for i in range(n_level_nodes):
                node = nodes[i]
                leaf_count -= node.remove_leaves()
                if leaf_count <= color_count:
                    index = i
                    break

            # remove the whole level if all nodes are leaves
            # otherwise keep the remaining ones
            self.levels[level] = [] if index == -1 \
                                    else nodes[index + 1:]
            self.depth -= 1 if index == -1 else 0

        return self._build_palette(color_count)

    def _build_palette(self, color_count):
        """
        Build palette from leaves with `color_count` colors maximum
        """
        palette = []
        palette_index = 0

        for node in self.get_leaves():
            if palette_index >= color_count:
                break
            palette.append(node.get_color())
            node.palette_index = palette_index
            palette_index += 1
        return palette

    def get_palette_index(self, color):
        """
        Get palette index for `color`
        """
        return self.root.get_palette_index(color, 1)

    def node_id_set(self):
        nodes = [self.root]
        nodes_set = set()
        while nodes:
            node = nodes.pop(0)
            if node:
                nodes_set.add(node.id)
                nodes += node.children
        return nodes_set

    def print(self):
        nodes = [self.root]
        next_nodes = []
        level = 0
        while nodes:
            print("LEVEL", str(level))
            level += 1
            for elem in nodes:
                if elem:
                    print(str(elem), end ="|")
                    next_nodes += elem.children
            print("\n")
            nodes = next_nodes
            next_nodes = []

if __name__ == '__main__':
    octree = Octree()
