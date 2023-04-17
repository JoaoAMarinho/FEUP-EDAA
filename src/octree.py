class Node(object):
    def __init__(self):
        self.children = [None] * 8
        self.isLeaf = True

class Octree(object):
    def __init__(self):
        self.root = Node()

    def insert(self):
        print("To implement.")
