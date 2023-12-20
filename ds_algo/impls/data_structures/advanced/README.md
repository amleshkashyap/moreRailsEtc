## Redblack Tree
  * Following the definition from CLRS, RB Tree has 5 properties
    1. Nodes are either red or black
    2. Root is black
    3. Leaf is black
    4. A red node can only have black children
    5. For each node, all simple paths from node to its leaves contain the same number of black nodes

  * The red-black insertion/deletion algorithms can be derived by enlisting and fixing for the inputs - CLRS explores all the cases.

  * Insertion
    - Insertion process starts same as normal BST insertion - find where to insert, update pointers, color the node as red.
    - Red is chosen as the initial color to prevent violation of (5) which is more difficult to fix as seen in deletion.
    - A routine is called to fix the violations that may've been created due to insertion.
    - If inserted node is not root and has a black parent, then no violations occur - routine terminates by marking root as black [no-op].
    - Following are the remaining 2 cases which lead to an immediate violation -
      - If inserted node is root, then property (2) is violated - fixup routine will mark it as black and terminate.
      - If the inserted node had a red parent, then property (4) is violated - this can lead to a few scenarios discussed below.

  * BST Deletion - BST deletion scenarios form the basis for generating RBT deletion scenarios -
    - Set-0 - minimal ops
      - In all cases, node being deleted is (n). Also, its parent is (z)
      - C-1 - Delete the root node with no children - tree becomes empty
      - C-2 - Delete a right/left child of root node with no children - make the right/left child of root as nil
      - C-3 - Delete a right/left leaf node - make the right/left child of (z) as nil

    - Set-1 - when the node being deleted has one child - 1 transplant only
      - In all cases, node being deleted is (n) and replaced by its only child (x). Also, (n)'s parent is (z)
      - C-1 - Delete the root node with one child - make (x) as root
      - C-2 - Delete a child of root node (z) with one child - make (x) as (z)'s right/left child
      - C-3 - Delete any other node with just one child - make (x) as the right/left child of (z)

    - Set-2 - when the node being deleted (n) has 2 children, but it's right child (y) has no left child - 1 transplant + minimal ops
      - In all cases, (y) replaces (n). (y) may have a right child (x). Also, (y)'s parent is (z) == (n)
      - C-1 - If (n) was root, then replace (n) by (y)
      - C-2 - If (n) was a child node of root, then replace (n) by (y)
      - C-3 - Even otherwise, replace (n) by (y)

    - Set-3 - when the node being deleted (n) has 2 children, and it's right child (r) has a left child - upto 2 transplants + minimal ops
      - Find the min\_node (y) in the subtree (r) - (y) can't have a left child - but may have a right child (x).
      - If (x) exists, replace (y) by (x).
      - In all cases, (y) replaces (n). Also, (y)'s parent is (z) != (n) [however, (z) maybe (r) but it's irrelevant]
      - C-1 - If (n) was root, replace (n) by (y)
      - C-2 - If (n) was a child node of root, replace (n) by (y)
      - C-3 - Even otherwise, replace (n) by (y)


  * Deletion
    - Deletion process starts same as normal BST deletion - find the node to delete, perform the transplants as needed.
    - All four of the above input sets are considered to detect violations based on (n), (y), (z) and (x). In all cases, color of the
      outgoing node (o) [ie, whose color is lost due to removal/replacement] is noted. Note that (o) being black includes removal of root.

    - RB-Set-0: outgoing node (o) == (n), note color, (o)'s parent (z), (o)'s child (x) == NULL
      - C-1 - If (o) was red, no violation has occurred
      - C-2 - If (o) was black, property (5) is violated

    - RB-Set-1: outgoing node (o) == (n), note color, (o)'s parent (z), (o)'s only child (x)
      - C-1 - If (o) was red, then (z) must be black - hence (x)'s color doesn't matter - no violations have occurred.
      - C-2 - If (o) was black, then property (5) is violated.
      - C-3 - If (o) was black with red (z), and (x) is red, then property (4) is also violated.

    - RB-Set-2: outgoing node (o) == (y), note color [(o) replaces (n) and gets (n)'s color], (o)'s parent (z), (o)'s only right child (x)
      - C-1 - If (o) was red, then its parent (z) must be black - hence (x)'s color doesn't matter - no violations have occurred.
      - C-2 - If (o) was black, then property (5) is violated.
      - C-3 - If (o) was black, and (z) was red, and (x) is also red, then property (4) is also violated.

    - RB-Set-3: outgoing node (o) == (y), note color [(o) replaces (n) and gets (n)'s color], (o)'s parent (z), (o)'s only right child (x)
      - C-1 - If (o) was red, then its parent (z) must be black - hence (x)'s color doesn't matter - no violations have occurred.
      - C-2 - If (o) was black, then property (5) is violated.
      - C-3 - If (o) was black, and (z) was red, and (x) is also red, then property (4) is also violated.

    - In all the above cases, there are 3 nodes of concern.
      - Outgoing node (o) [maybe (n) or (y)] - violations occur only when (o) is black
      - Parent of the outgoing node - (z)
      - Child of the outgoing node - (x) [maybe a left child in RB-Set-1, else a right child always]

    - RB-Set-0 - (z), (o) - black, (x) - black [since NULL]
      - red,   black,   black
      - black, black,   black

    - RB-Set-1 - (z), (o) - black, (x)
      - red,   black,   black
      - red,   black,   red    - fix immediately
      - black, black,   black
      - black, black,   red    - fix immediately

    - RB-Set-2 - (z), (o) - black, (x)
      - red,   black,   black
      - red,   black,   red    - fix immediately
      - black, black,   black
      - black, black,   red    - fix immediately

    - RB-Set-3 - (z), (o) - black, (x)
      - red,   black,   black
      - red,   black,   red    - fix immediately
      - black, black,   black
      - black, black,   red    - fix immediately

    - Totally, it appears that 14 scenarios exist (and then x 3 for the 3 scenarios in basic BST deletion). However, RB-Set-1, RB-Set-2 and
      RB-Set-3 have the same scenarios. Also, half of them can be immediately fixed - in cases when (x) is red, making it black fixes -
      - Violation of property (5) by providing the ancestors with the lost black node
      - All the violations of property (4) above (in C-3) are fixed too by eliminating red-red parent-child

    - Scenarios which remain unfixed are -
      - RB-Set-0 - (z), (o) - black, (x) - black
        - red,   black,  black
        - black, black,  black

      - RB-Set-1, RB-Set-2, RB-Set-3 - (z), (o) - black, (x) - black
        - red,   black,  black
        - black, black,  black

    - Both the above are same, thus leaving with only 2 scenarios to solve for - (z), (o) - black, (x) - black
      - [1] red,   black,   black
      - [2] black, black,   black

    - The fixup routine is called -
      - Argument to the routine is (x), which is replacing (o) in all cases.
      - For RB-Set-0, (x) doesn't exist - it's a null node.
      - Similarly, for RB-Set-2 and RB-Set-3, (x) may not exist.
      - (x) will always be a non-null node for RB-Set-1, and usually be a non-null node for RB-Set-2 and RB-Set-3.

    - The table in deletion section below covers the above 2 cases, and further situations that need to be examined in order to come up
      with a fix.

### Insertion
  * Basic
    - First node     -  property (2) violated
    - Second node    -  no properties violated
    - Node with black parent and red/black uncle - no properties violated

  * Main

  |parent\_color  | parent\_side  |  uncle\_color |  node\_side  |  testcase  |
  |---------------|---------------|---------------|--------------|------------|
  |  red          |  left         |    red        |   left       |            |
  |  red          |  left         |    red        |   right      |            |
  |  red          |  right        |    red        |   left       |            |
  |  red          |  right        |    red        |   right      |            |
  |  red          |  left         |    black      |   left       |            |
  |  red          |  left         |    black      |   right      |            |
  |  red          |  right        |    black      |   left       |            |
  |  red          |  right        |    black      |   right      |            |

### Deletion
  * Covered in CLRS, there are 4 actual scenarios that show up after showing that there are only 2 scenarios that violate red-black
    properties after performing a basic BST deletion on the RBTree, and coloring (x) as black.
   - (z) - earlier, it was a parent of (o), but now a parent of (x)
   - (w) - earlier, it was a sibling of (o), but now a sibling of (x)
   - (z) - earlier, it was a parent of (o), but now a parent of (x) - if (w) is red, (z) must've been black.

  |SI    |  z\_color    |  x\_color  |   w\_color  |   w\_left\_color  |  w\_right\_color  |   Notes      |
  |------|--------------|------------|-------------|-------------------|-------------------|--------------|
  |[2]   |   black      |   black    |    red      |     black         |    black          | CLRS Case-1  |
  |[1/2] |   red/black  |   black    |    black    |     black         |    black          | CLRS Case-2  |
  |[1/2] |   red/black  |   black    |    black    |     red           |    black          | CLRS Case-3  |
  |[1/2] |   red/black  |   black    |    black    |     red/black     |    red            | CLRS Case-4  |

  * Before coding up, following notes -
    - The fixup algorithm will run only for a non-root, black (x)
    - Its goal is to move a black color to ancestors [upto the root], so that all simple paths from the root have 1 less black node -
      it doesn't try to replenish the lost black node within the subtree except for one case (Case-4).
    - Handling T.nil for (x) and (w) -
      - Since (o) was black, (z) had at least 1 black node (2 if (x) existed) in its left subtree (towards (o)) - hence, (w) must exist.
      - At the end of Case-1, (w) becomes it's own older left child, which might've been T.nil
      - At the end of Case-2, (w) is not required immediately and hence it being T.nil is irrelevant - it can be in subsequent steps.
      - At the end of Case-3, (w) is definitely not T.nil as it is it's own left red node (which couldn't be T.nil).
      - At the end of Case-4, (w) being T.nil is irrelevant.
    - The only scenario when it can replenish the lost black node is when the sibling tree of (x) had excessive red nodes which could be
      converted to black along with a rotation. Case-4 provides that red right child with a black parent in the sibling tree, wherein
      a left rotation and recoloring of the rotated node to black leads to restoring of properties.
    - A single shot fix is not possible for any other scenario, eg, Case-3, because left rotation will lead to the sibling becoming
      parent and assuming parent's color, and losing a black node on its right subtree.
    - Case-2 is also a single shot fix if (z) was red, as one extra black is removed from the right sibling to balance the sibling subtrees.
      Finally, the parent (z) is made black to replenish the lost black for the ancestors.
    - Case-3 can be converted to Case-4 in O(1) time - hence Case-3 and Case-4 are fastest.
    - Case-1 can go to either Case-2, Case-3 or Case-4.
    - Case-2 has the potential for worst case complexity O(logN) when (z) is black.
    - Since the fixup moves up the tree, it's complexity is O(logN). BST deletion is O(logN). Rotations and transplants are O(1).
