# B-Tree

B-Tree are well balanced trees aimed at storing, accessing, editing multiple values (just like a database).

Since each search requires a certain number of read calls, and the nodes are blocks of information, we will not only return the searched value but the whole block, thus why the tree is good for storing and accessing data. 

Each node can have more than one value (key), and the number of children is given by the length of a node + 1.

These trees allow for some of the binary search tree algorithms.

Internal nodes are the ones which are not leaf nodes.

## 1. Definition

For a node x:
- x.n -> # keys
- x.key1 <= x.key2 ...
- x.leaf -> indicates if a node is a leaf or not
- for a certain number of keys, there are keys + 1 child pointers (x.c1, x.c2, ...)

All leafs have the same height, h.

Nodes have lower and upper bounds on the number of keys they can have:
- t is a fixed integer >= 2 called the minimum degree
- every node other than the root must have at least t-1 keys, therefore t children
- every node may contain at most 2t-1 keys, and thus 2t children
- a node is said to be full when it contains the most number of keys

## 2. Theorem

For any B-tree with height h and degree t >= 2:
h <= log t(n+1/2)

## 3. Basic operations

### Seaching a B-tree

As input we need the key to be searched and the root node as a pointer.

The time complexity is O(t.h)=O(t.log t(n))

### Creating

Start by creating an empty tree and then insert new keys.

Both create and insert have allocate-node calls which take O(1).

### Inserting

We still search for the leaf position at which to insert. However we cannot simply create a new leaf node and insert it.

We introduce an operation that splits a full node y around its median key into two nodes having only t-1 keys each.

We then move the median value upwards into the parent node.

Since it might be very costfull to rearange the tree once a node is full, we will splite every time we traverse the tree and find a full node.

#### B-Tree Split Child Procedure

We input  a nonfull parent node and the index of the child which is full and to be splited.

Then split the node in two and pass the median to the parent node.

Time complexity is O(t.h) = O(t.log t(n)).

This procedure only gains height by splitting the root node.
