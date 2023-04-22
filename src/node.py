from src.color import Color

class Node():
    """
    Octree Node class
    """

    def __init__(self, level, parent, index = 0, parent_id = 0):
        """
        Init new Octree Node
        """
        self.color = Color(0, 0, 0)
        self.pixel_count = 0
        self.palette_index = 0
        self.id = parent_id*8 + index

        # add node to current level
        if level < parent.depth - 1:
            parent.add_level_node(level, self)
            self.children = [None for _ in range(8)]
        else:
            # node is leaf
            self.children = []

    def is_leaf(self):
        """
        Check that node is leaf
        """
        return len(self.children) == 0

    def get_leaf_nodes(self):
        """
        Get all leaf nodes
        """
        leaf_nodes = []
        for node in self.children:
            if not node:
                continue
            if node.is_leaf():
                leaf_nodes.append(node)
            else:
                leaf_nodes.extend(node.get_leaf_nodes())
        return leaf_nodes
    
    def increment_pixel_count(self):
        """
        Increment pixel count
        """
        self.pixel_count += 1

    def add_color(self, color, level, parent):
        """
        Add `color` to the tree
        """
        self.increment_pixel_count()
        index = self.get_color_index_for_level(color, level)

        if not self.children[index]:
            self.children[index] = Node(level, parent, index, self.id)
        
        if self.children[index].is_leaf():
            self.children[index].color.increment(color)
            self.children[index].increment_pixel_count()
            return
        
        self.children[index].add_color(color, level + 1, parent)

    def get_palette_index(self, color, level):
        """
        Get palette index for `color`
        Uses `level` to go one level deeper if the node is not a leaf
        """
        if self.is_leaf():
            return self.palette_index
        index = self.get_color_index_for_level(color, level)
        if self.children[index]:
            return self.children[index].get_palette_index(color, level + 1)
        else:
            # get palette index for a first found child node
            for i in range(8):
                if self.children[i]:
                    return self.children[i].get_palette_index(color, level + 1)

    def remove_leaves(self):
        """
        Add all children pixels count and color channels to parent node 
        Return the number of removed leaves
        """
        result = 0
        for node in self.children:
            if node:
                self.color.increment(node.color)
                result += 1
        
        # empty children list
        self.children = []
        return result - 1

    def get_color_index_for_level(self, color, level):
        """
        Get index of `color` for next `level`
        """
        index = 0
        mask = 0x80 >> level
        if color.red & mask:
            index |= 4
        if color.green & mask:
            index |= 2
        if color.blue & mask:
            index |= 1
        return index

    def get_color(self):
        """
        Get average color
        """
        return Color(
            int(self.color.red / self.pixel_count),
            int(self.color.green / self.pixel_count),
            int(self.color.blue / self.pixel_count))
    
    def __str__(self):
        return "\'"+str(self.id)+"\'" + str(self.color) + "(" + str(self.pixel_count) + ")"
