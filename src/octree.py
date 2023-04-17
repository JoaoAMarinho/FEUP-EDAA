class Node(object):
    def __init__(self):
        self.children = [None] * 8
        self.isLeaf = True

class Octree(object):
    def __init__(self):
        self.root = Node()

    def insert(self):
        print("To implement.")
        #1. Start with root node as current node.
        #2. If the given point is not in cuboid represented by current node, stop insertion
        #    with error.
        #3. Determine the appropriate child node to store the point.
        #4. If the child node is empty node, replace it with a point node representing the
        #    point. Stop insertion.
        #5. If the child node is a point node, replace it with a region node. Call insert for
        #    the point that just got replaced. Set current node as the newly formed region
        #    node.
        #6. If selected child node is a region node, set the child node as current node.
        #    Goto step 2.
