# Buffer-Tree

## B-Trees Issue

B-Tree are not very useful for building dinamically destructors. Every time we do a deletion or an insertion we need to access/perform an I/O operation over a block of information.

So they do not introduce improvements in the sorting performance.

## Notes

- Each node contains a buffer
- Operations are done in a "lazy way" - operations are inserted in a buffer and latter on, when a buffer is full, we propagate the operations
- Meaning that 1 single I/O operation can pass a whole block of operations down the tree path

Basic tree definition:
- Buffers with size M in each internal node
- Iternal nodes have (M/B)*(1/4) ... M/B children
- Leaf nodes have B/4 ... B size

Updates:
- Before inserting in root buffer, B update elements are keept in internal memory (with timestamps)
- When the buffer runs full we perform a `buffer-emptying` operation
  - Note: Buffer can be larger than M at a certain time, during the top-down emptying process
  - Rebalancing is needed when a leaf-node's buffer is being emptied
- This operation is followed with a degree fixing (rebalancing) if needed

Buffer emptying (internal node):
- Load first M elements into memory and sort them (M/B I/O operations)
- Merge with elements from memory
- Scan through sorted list while:
  - Removing matching insert/delete
  - Distribute elements to child buffers (push down)
- Recursively empty full child buffers
- Emptying a buffer of size X takes O(X/B + M/B) = O(X/B) I/Os

Buffer emptying (leaf node with K elements in leaves):
- Sort as before
- Merge buffer elements with leaf elements
- Remove matching insert/delete and if K' is lower than K:
  - Add K-K' "dummy" elements and insert in "dummy" leaves
- Otherwise:
  - Place K elements in leaves
  - Repeatedly insert block of elements in leaves and rebalance

**Invariant**:
Buffers of nodes on path from root to emptied leaf-node are also empty.

**Insert rebalanncing** (splits) works as in normal B-Trees.

**Delete rebalancing** requires the emptying of sibling nodes first and then the fuse of v with v'.

Analysis:
- Without rebalancing, a buffer emptying of a node with X>=M elements (full) takes O(X/B) I/Os
  - Total full node emptying cost O(N/B.log(M/B) N/B) I/Os
  - Height = log(M/B) N/B
- Delete rebalancing takes O(M/B) I/Os
  - Cost of one split/fuse O(M/B) I/Os
- During N updates
  - Total cost O(N/B . log (M/B) (N/B) ) I/Os

## Thesis

N/B -> number of blocks

M/B -> number of blocks that fit in internal memory

An algorithm uses a linear number of I/Os if it uses O(n) I/Os, such that n = N/B (number of blocks).
