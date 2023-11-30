from util import Util

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.color = None
        self.height = 0
        self.parent = None

###########################################################################################
  # Insert and Delete - without any height adjustment - maintaining the BST property
  # Create BST from sorted array
  # Get height and whether tree is balanced
  # Print the tree - levelwise left to right and zigzag (Upto depth 7, single digit numbers only)
  #  - For non height balanced trees, print 'x'
  # Search within a subtree
  # Min value within a subtree
  # Traversals
  # Rotations
###########################################################################################

class BinarySearchTree:
    def __init__(self):
        self.name = "BinarySearchTree"
        self.root = None
        self.xnode = Node('x')
        self.size = 0
        self.height = 0
        self.balanced = True
        self.treeArray = []
        self.verticalArray = []
        self.detailedVerticalArray = []

    def sortedArrayToBST(self, array):
        if len(array) == 0:
            return

        mid = len(array)//2

        root = Node(array[mid])

        root.left = self.sortedArrayToBST(array[:mid])
        if root.left != None:
            root.left.parent = root
        root.right = self.sortedArrayToBST(array[mid+1:])
        if root.right != None:
            root.right.parent = root
        return root

    def get_height(self, node):
        if node == None:
            return 0
        lheight = self.get_height(node.left) + 1
        rheight = self.get_height(node.right) + 1
        return max(lheight, rheight)

    def constructTreeArray(self):
        if self.size > 0:
            return
        self.treeArray = []
        self.verticalArray = []
        self.detailedVerticalArray = []
        self.height = self.get_height(self.root)
        self.balanced = False if self.is_balanced(self.root) == 0 else True
        self.printable = False if self.is_printable(self.root) == 0 else True
        if self.printable:
            self.get_vertical_array(self.root, 1, self.verticalArray, self.height, self.detailedVerticalArray)
        else:
            self.get_vertical_array_nonbalanced(self.root, 1, self.verticalArray, self.height, self.detailedVerticalArray)

        for ar in self.verticalArray:
            for a in ar:
                self.treeArray.append(a)
        self.size = len(self.treeArray) - self.treeArray.count('x')
        
    def get_vertical_array(self, node, level, array, height, detailed):
        if node == None:
            return

        if len(array) < level:
            array.append([])
            detailed.append([])

        node.height = height - level
        array[level-1].append(node.value)
        detailed[level-1].append(node)
        self.get_vertical_array(node.left, level + 1, array, height, detailed)
        self.get_vertical_array(node.right, level + 1, array, height, detailed)

        if level == height-1:
            if node.left == None:
                array[level].append("x")
            if node.right == None:
                array[level].append("x")

    def get_vertical_array_nonbalanced(self, node, level, array, height, detailed):
        if level > height:
            return

        if len(array) < level:
            array.append([])
            detailed.append([])

        if node == None:
            node = self.xnode

        node.height = height - level + 1
        array[level-1].append(node.value)
        detailed[level-1].append(node)
        self.get_vertical_array_nonbalanced(node.left, level + 1, array, height, detailed)
        self.get_vertical_array_nonbalanced(node.right, level + 1, array, height, detailed)

    # creates tree array first
    def get_zigzag_array(self):
        if self.size == 0:
            self.constructTreeArray()
        array = self.verticalArray.copy()
        for i in range(self.height):
            if i%2 == 1:
                array[i].reverse()
        return array

    def insert(self, node, value):
        if node == None:
            node = Node(value)
            return node
        elif value < node.value:
            node.left = self.insert(node.left, value)
            if node.left != None:
                node.left.parent = node
        else:
            node.right = self.insert(node.right, value)
            if node.right != None:
                node.right.parent = node

        return node

    def insert_and_balance(self, node, value):
        pass

    def min_node(self, node):
        while(node.left != None):
            node = node.left
        return node

    def delete(self, node, value):
        if node == None:
            return None

        if node.value > value:
            node.left = self.delete(node.left, value)
            return node
        elif node.value < value:
            node.right = self.delete(node.right, value)
            return node

        if node.left is None:
            tmp = node.right
            del node
            return tmp
        elif node.right is None:
            tmp = node.left
            del node
            return tmp
        else:
            parent = node
            successor = node.right
            while successor.left is not None:
                parent = successor
                successor = successor.left

            # when right child [larger value] didn't have any left child
            # then it's value can be safely placed in node and it's right child can be mapped to node directly, since it'll be deleted
            if parent == node:
                node.right = successor.right
            # when right child [larger value] did have a left child [but not anymore]
            # then it's value can be safely placed in node, and it's right child can be mapped to it's parent, since it'll be deleted
            else:
                parent.left = successor.right

            node.value = successor.value
            del successor

        return node

    def search(self, node, value):
        if node == None or node.value == value:
            return node

        if value < node.value:
            return self.search(node.left, value)
        else:
            return self.search(node.right, value)

    # from Cormen
    def delete_new(self, value):
        node = self.search(self.root, value)
        if node is None:
            return self.root

        if node.left is None:
            self.transplant(node, node.right)
        elif node.right is None:
            self.transplant(node, node.left)
        else:
            min_node = self.min_node(node.right)
            if min_node.parent != node:
                self.transplant(min_node, min_node.right)
                min_node.right = node.right
                min_node.right.parent = min_node
            self.transplant(node, min_node)
            min_node.left = node.left
            min_node.left.parent = min_node

        return self.root

    def is_balanced(self, node):
        if node == None:
            return 1

        lh = self.is_balanced(node.left)
        if lh == 0:
            return 0

        rh = self.is_balanced(node.right)
        if rh == 0:
            return 0

        if abs(lh - rh) > 1:
            return 0

        return max(lh, rh) + 1

    def is_printable(self, node):
        if node == None:
            return 1

        lh = self.is_printable(node.left)
        if lh == 0:
            return 0

        rh = self.is_printable(node.right)
        if rh == 0:
            return 0

        if lh != rh:
            return 0

        return max(lh, rh) + 1

    def get_inorder_array(self, node, array):
        if node == None:
            return
        self.get_inorder_array(node.left, array)
        array.append(node.value)
        self.get_inorder_array(node.right, array)

    def get_preorder_array(self, node, array):
        if node == None:
            return
        array.append(node.value)
        self.get_preorder_array(node.left, array)
        self.get_preorder_array(node.right, array)

    # this method makes newRoot as the child of node's parent
    # then makes newRoot's parent as node's parent
    # finally, makes newRoot as node's new parent
    # expects node and newRoot to be non-nil
    # from Cormen
    def transplant(self, node, newRoot):
        # if node was the root, then leftN is the new root
        if node.parent == None:
            self.root = newRoot
        # if node was a right child of another subtree, then leftN becomes the right child
        elif node.parent.right == node:
            node.parent.right = newRoot
        # if node was the left child of another subtree, then leftN becomes the left child
        else:
            node.parent.left = newRoot

        if newRoot != None:
            newRoot.parent = node.parent

    # node is the root of the subtree to be right rotated
    def right_rotate(self, node):
        if node == None:
            return

        # left child will be the new root
        newRoot = node.left

        # the left child subtree of newRoot will remain unchanged, but it's right child subtree has to change and become left child of node - store it
        node.left = newRoot.right
        if node.left != None:
            node.left.parent = node

        # node has to be the new right child subtree of leftN [with larger value]
        newRoot.right = node
        self.transplant(node, newRoot)
        node.parent = newRoot

    def left_rotate(self, node):
        if node == None:
            return

        # right child will be the new root - node's right is empty and can be replaced now
        newRoot = node.right

        # the right child subtree of newRoot will be unchanged, but its left child subtree has to be the right child subtree of node so store it
        # after this, newRoot's left can be populated as it's empty
        node.right = newRoot.left
        if node.right != None:
            node.right.parent = node

        # node is the new left child subtree of newRoot [with smaller value]
        newRoot.left = node
        # this method makes newRoot take the place of node, and makes newRoot as node's parent [node as left/right child is decided already]
        self.transplant(node, newRoot)
        node.parent = newRoot

    def print_inorder_with(self, node):
        if node == None:
            return

        self.print_inorder(node.left)
        print(node.value, node.parent.value if node.parent else None)
        self.print_inorder(node.right)
        return node

    def print_vertical_with_details(self):
        count = 0
        for ar in self.detailedVerticalArray:
            for a in ar:
                if a.value == 'x':
                    continue
                print(count * "    " + f"Key: {a.value}, Height: {a.height}")
            count += 1



#################### Test utils

def tree_tests(bst, source_array, t_type):
    print(f"#### Test Case For {bst.name}, Type: {t_type} ####")
    print(f"Source Array: {source_array}")
    bst.size = 0
    i_array = []
    bst.get_inorder_array(bst.root, i_array)
    print(f"Inorder tree array: {i_array}")
    p_array = []
    bst.get_preorder_array(bst.root, p_array)
    # print(f"Preorder tree array: {p_array}")
    bst.constructTreeArray()
    print(f"Tree size: {bst.size}, height: {bst.height}, tree as heap: {bst.treeArray}")
    if bst.height < 8:
        print("Stored Tree")
        Util.print_array_as_tree(bst.treeArray)
        print("")
        print(f"Vertical Tree: {bst.verticalArray}")
    else:
        print("Vertical Tree Lines")
        for ar in bst.verticalArray:
            print(ar)
        print("")
    z_array = bst.get_zigzag_array()
    zz_array = []
    for ar in z_array:
        for a in ar:
            zz_array.append(a)
    if bst.height < 8:
        pass
        # print(f"Zigzag Traversal: {zz_array}")
        # Util.print_array_as_tree(zz_array)
    else:
        pass
        # print("Zigzag Traversal Lines")
        # for ar in z_array:
            # print(ar)
    # print("")
    print(f"Tree is balanced: {bst.balanced}")
    bst.print_vertical_with_details()
    # print("")
    print("")

def basic_tests(bst1, sorted_array, bst2, random_array):
    bst1.root = bst1.sortedArrayToBST(sorted_array)
    tree_tests(bst1, sorted_array, "treeCreatedFromSortedArray")
    bst1.root = bst1.delete(bst1.root, 3)
    tree_tests(bst1, sorted_array, "nodeDeletion")

    for i in random_array:
        bst2.root = bst2.insert(bst2.root, i)
    tree_tests(bst2, random_array, "treeCreatedFromRandomArray")

def deletion_test(bst, array):
    bst.root = bst.sortedArrayToBST(array)
    tree_tests(bst, array, "treeCreatedFromSortedArray")
    bst.root = bst.delete_new(5)
    tree_tests(bst, array, "Existing Node Deletion")
    bst.root = bst.delete_new(9)
    tree_tests(bst, array, "Existing Node Deletion")
    bst.root = bst.delete_new(9)
    tree_tests(bst, array, "Absent Node Deletion")

def rotation_test(bst, array):
    bst.root = bst.sortedArrayToBST(array)
    tree_tests(bst, array, "treeCreatedFromSortedArray")
    bst.right_rotate(bst.root)
    tree_tests(bst, array, "Right Rotate Root")
    bst.right_rotate(bst.root.left)
    tree_tests(bst, array, "Right Rotate Left Subtree")
    bst.left_rotate(bst.root.left)
    tree_tests(bst, array, "Left Rotate Left Subtree")
    bst.left_rotate(bst.root)
    tree_tests(bst, array, "Left Rotate Root")

if __name__ == "__main__":
    array = [8, 7, 6, 4, 4, 5, 3, 3, 3, 2, 3, 1, 5, 2, 1, 1, 2, 1, 1, 2]
    sorted_array = sorted(array)

    array = [8, 4, 5, 3, 9, 2, 6, 7, 0, 1]
    bst = BinarySearchTree()
    bst1 = BinarySearchTree()
    basic_tests(bst, sorted_array, bst1, array)

    array = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    bst = BinarySearchTree()
    deletion_test(bst, array)

    array = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    bst = BinarySearchTree()
    rotation_test(bst, array)
