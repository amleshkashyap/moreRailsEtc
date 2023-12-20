from util import Util

# Red-Black Trees - DB Transactions - Random Operations (Search/Delete/Add) - 3 Pointers + Color Bit
# AVL Trees - Multiset, Multimap, Map, Set - Frequent Searches - 2 Pointers + Balance Factor
# Splay Trees - Cache, Garbage Collection - Same Element Accessed Frequently - 2 Pointers

# Following the definition from Cormen, RB Tree has 5 properties
#  1. Nodes are either red or black
#  2. Root is black
#  3. Leaf is black
#  4. A red node can only have black children
#  5. For each node, all simple paths from node to its leaves contain the same number of black nodes

class RBNode:
    def __init__(self, value, left, right, color=0):
        self.value = value
        self.left = left
        self.right = right
        self.color = color
        self.parent = None

class RedBlackTree:
    def __init__(self):
        self.name = "RedBlackTree"
        self.black = "\33[40m"
        self.endc = "\033[0m"
        self.red = "\033[41m"
        self.reset()

    def reset(self):
        self.tnil = RBNode('x', None, None, 1)
        self.root = self.tnil
        self.size = 0
        self.treeArray = []
        self.treeWithColor = []
        self.verticalArray = []
        self.verticalWithColor = []
        self.height = 0
        self.balanced = True

    # similar to BST insert
    def insert(self, value):
        node = RBNode(value, self.tnil, self.tnil)
        x = self.root
        y = self.tnil
        while(x != self.tnil):
            y = x
            if value < x.value:
                x = x.left
            else:
                x = x.right

        node.parent = y
        if y == self.tnil:
            self.root = node
        elif value < y.value:
            y.left = node
        else:
            y.right = node

        while node.parent.color == 0:
            if node.parent == node.parent.parent.left:
                node = self.insert_fixup_left_subtree(node)
            else:
                node = self.insert_fixup_right_subtree(node)
        self.root.color = 1
        return self.root

    def insert_fixup_left_subtree(self, node):
        uncle = node.parent.parent.right
        # if uncle was red [and parent is already red]
        #   - make both uncle and parent as black -> this introduces an extra black upon the ancestors
        #   - reduce the extra black by making grandparent as red [since parent of red must be black]
        #   - now, the grandparent may've violated (4) - if yes, perform further fixes on grandparent
        #   - else, terminate
        if uncle.color == 0:
            node.parent.color = uncle.color = 1
            node.parent.parent.color = 0
            node = node.parent.parent
        else:
            # if uncle was black [and parent is already red]
            # if inserted node is a right child, perform left rotation on parent to make it a left child - for ease of fixing
            if node == node.parent.right:
                node = node.parent
                self.left_rotate(node)
            # node is a left child with a red parent and black uncle
            #  - parent must be made black to fix (4) - this will add an extra black in the simple path of its ancestors [violates (5)]
            #  - fix the extra black siutation by making the grandparent as red [since it must've been black]
            #  - this has led violation of (5) again - now there's 1 less black on the simple path towards uncle's side
            #  - fix the 1 less black situation by performing a right rotation on grandparent [which will move the black parent up]
            #  - terminate since no violations of (4)/(5) are present
            node.parent.color = 1
            node.parent.parent.color = 0
            self.right_rotate(node.parent.parent)
        
        return node

    def insert_fixup_right_subtree(self, node):
        uncle = node.parent.parent.left
        if uncle.color == 0:
            node.parent.color = uncle.color = 1
            node.parent.parent.color = 0
            node = node.parent.parent
        else:
            if node == node.parent.left:
                node = node.parent
                self.right_rotate(node)
            node.parent.color = 1
            node.parent.parent.color = 0
            self.left_rotate(node.parent.parent)

        return node

    # same as BST transplant
    def transplant(self, node, child_node):
        if node.parent == self.tnil:
            self.root = child_node
        elif node == node.parent.left:
            node.parent.left = child_node
        else:
            node.parent.right = child_node

        child_node.parent = node.parent
        return

    def search(self, root, value):
        if root == self.tnil:
            return False

        if root.value == value:
            return root

        if value > root.value:
            return self.search(root.right, value)
        else:
            return self.search(root.left, value)

    def min_node(self, node):
        while(node.left != self.tnil):
            node = node.left
        return node

    def left_rotate(self, node):
        if node == self.tnil:
            return

        newRoot = node.right
        node.right = newRoot.left
        node.right.parent = node
        newRoot.left = node
        self.transplant(node, newRoot)
        node.parent = newRoot

    def right_rotate(self, node):
        if node == self.tnil:
            return

        newRoot = node.left
        node.left = newRoot.right
        node.left.parent = node
        newRoot.right = node
        self.transplant(node, newRoot)
        node.parent = newRoot

    def delete(self, value):
        node = self.search(self.root, value)
        if node == False:
            print(f"Given value: {value} not present in tree")
            return self.root

        y = node
        y_color = y.color

        if node.left == self.tnil:
            x = node.right
            self.transplant(node, node.right)
        elif node.right == self.tnil:
            x = node.left
            self.transplant(node, node.left)
        else:
            y = self.min_node(node.right)
            y_color = y.color
            x = y.right
            if y.parent == node:
                x.parent = y
            else:
                self.transplant(y, y.right)
                y.right = node.right
                y.right.parent = y

            self.transplant(node, y)
            y.left = node.left
            y.left.parent = y
            y.color = node.color

        if y_color == 1:
            # if x was either root or red, then properties (2), (4) and (5) will be restored immediately
            while x != self.root and x.color == 1:
                if x == x.parent.left:
                    x = self.delete_fixup_left_subtree(x)
                else:
                    x = self.delete_fixup_right_subtree(x)
            x.color = 1

        return self.root

    # taken from CLRS, uses variables same as the book
    # goal is to bring the subtree one step closer to being balanced at every iteration
    #  - perform rotation to exploit the sibling's subtrees in order to reduce the simple paths that need adjustment
    #  - recolor to minimize the unbalanced simple paths, and examine a new subtree in next iteration
    #  - refer to CLRS and exercises for proof of correctness
    def delete_fixup_left_subtree(self, x):
        w = x.parent.right
        if w.color == 0:
            w.color = 1
            x.parent.color = 0
            self.left_rotate(x.parent)
            w = x.parent.right

        if w == self.tnil:
            x = self.root
            return x

        if w.left.color == w.right.color == 1:
            w.color = 1
            # NOTE: if x's parent was red, then code will terminate with 1 fewer black node in it's ancestors simple paths
            x = x.parent
        elif w.right.color == 1:
            w.left.color = 1
            w.color = 0
            self.right_rotate(w)
            w = x.parent.right
        else:
            w.color = x.parent.color
            x.parent.color = 1
            w.right.color = 1
            self.left_rotate(x.parent)
            x = self.root

        return x

    # in the first iteration of fixup, code will reach here only when the deleted node had just one child and was a right child
    # however, in later iterations, for case-2, x is updated to be it's parent, which will lead to calling this method
    def delete_fixup_right_subtree(self, x):
        w = x.parent.left
        if w.color == 0:
            w.color = 1
            x.parent.color = 0
            self.right_rotate(x.parent)
            w = x.parent.left

        if w == self.tnil:
            x = self.root
            return x

        if w.left.color == w.right.color == 1:
            w.color = 1
            x = x.parent
        elif w.left.color == 1:
            w.right.color = 1
            w.color = 0
            self.left_rotate(w)
            w = x.parent.left
        else:
            w.color = x.parent.color
            x.parent.color = 1
            w.left.color = 1
            self.right_rotate(x.parent)
            x = self.root
        
        return x

    def get_height(self, node):
        if node == self.tnil:
            return 1
        lheight = self.get_height(node.left) + 1
        rheight = self.get_height(node.right) + 1
        return max(lheight, rheight)

    def is_balanced(self, node):
        if node == self.tnil:
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
        if node == self.tnil:
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

    def constructTreeArray(self):
        if self.size > 0:
            return
        self.treeArray = []
        self.verticalArray = []
        self.verticalWithColor = []
        self.treeWithColor = []
        self.height = self.get_height(self.root)
        self.balanced = False if self.is_balanced(self.root) == 0 else True
        self.printable = False if self.is_printable(self.root) == 0 else True
        if self.printable:
            self.get_vertical_array(self.root, 1, self.verticalArray, self.height, self.verticalWithColor)
        else:
            self.get_vertical_array_nonbalanced(self.root, 1, self.verticalArray, self.height, self.verticalWithColor)

        for ar in self.verticalArray:
            for a in ar:
                self.treeArray.append(a)

        for ar in self.verticalWithColor:
            for a in ar:
                self.treeWithColor.append(a)
        self.size = len(self.treeArray) - self.treeArray.count('x')

    def get_vertical_array(self, node, level, array, height, with_color):
        if node == None:
            return

        if len(array) < level:
            array.append([])
            with_color.append([])

        node.height = height - level
        if node.color == 0:
            v = f"{self.red}{node.value}{self.endc}"
        else:
            v = f"{self.black}{node.value}{self.endc}"
        with_color[level-1].append(v)
        array[level-1].append(node.value)
        self.get_vertical_array(node.left, level + 1, array, height, with_color)
        self.get_vertical_array(node.right, level + 1, array, height, with_color)

        if level == height-1:
            if node.left == self.tnil:
                array[level].append("x")
                with_color[level].append(f"{self.black}x{self.endc}")
            if node.right == self.tnil:
                array[level].append("x")
                with_color[level].append(f"{self.black}x{self.endc}")


    def get_vertical_array_nonbalanced(self, node, level, array, height, with_color):
        if level > height:
            return

        if len(array) < level:
            array.append([])
            with_color.append([])

        if node == None:
            node = self.tnil

        node.height = height - level + 1
        if node.color == 0:
            v = f"{self.red}{node.value}{self.endc}"
        else:
            v = f"{self.black}{node.value}{self.endc}"
        array[level-1].append(node.value)
        with_color[level-1].append(v)
        self.get_vertical_array_nonbalanced(node.left, level + 1, array, height, with_color)
        self.get_vertical_array_nonbalanced(node.right, level + 1, array, height, with_color)

def insertion_test(rbt, array):
    for i in array:
        print(f"Inserting: {i}, root: {rbt.root.value}, rootparent: {rbt.root.parent.value if rbt.root.parent else None}")
        rbt.insert(i)
        rbt.size = 0
        rbt.constructTreeArray()
        if rbt.height < 8:
            print("Stored Tree")
            Util.print_array_as_tree(rbt.treeArray, rbt.treeWithColor)
            print("")
            print(f"Vertical Tree: {rbt.verticalArray}")
        else:
            print("Vertical Tree Lines")
            for ar in rbt.verticalArray:
                print(ar)
            print("")


def deletion_test(rbt, array):
    for i in array:
        print(f"Deleting: {i}, root: {rbt.root.value}, rootparent: {rbt.root.parent.value if rbt.root.parent else None}")
        rbt.delete(i)
        rbt.size = 0
        rbt.constructTreeArray()
        if rbt.height < 8:
            print("Stored Tree")
            Util.print_array_as_tree(rbt.treeArray, rbt.treeWithColor)
            print("")
            print(f"Vertical Tree: {rbt.verticalArray}")
        else:
            print("Vertical Tree Lines")
            for ar in rbt.verticalArray:
                print(ar)
            print("")

if __name__ == "__main__":
    tests = {
            1: [ [0, 1, 2, 3, 4, 5, 6, 7, 8],                                  [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 2, 3, 4, 5] ],
            2: [ [9, 8, 7, 6, 5, 4, 3, 2, 1, 0],                               [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 2, 3, 4, 5] ],
            3: [ [9, 8, 7, 4, 5, 3],                                           [3, 4, 5, 7, 8, 9] ],
            4: [ [8, 7, 6, 3, 4, 2, 9], [8] ],
            4: [ [8, 7, 6, 4, 4, 5, 3, 3, 3, 2, 3, 1, 5, 2, 1, 1, 2, 1, 1, 9], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 2, 3, 4, 5] ]
    }
    rbt = RedBlackTree()
    for key, value in tests.items():
        insert = value[0]
        delete = value[1]
        insertion_test(rbt, insert)
        deletion_test(rbt, delete)
        rbt.reset()
