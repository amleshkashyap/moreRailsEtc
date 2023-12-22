from util import Util

class BTreeNode():
    def __init__(self):
        self.values = []
        self.vLen = 0
        self.children = []
        self.isLeaf = True

'''
1. Node x
   a. It has n keys (given by 'vLen' in BTreeNode)
   b. keys are in non-decreasing order
   c. n+1 children pointers (stored in 'children' in BTreeNode)
2. All leaves have same depth, it's also the tree's height
3. minimum degree t (>=2) - min keys in a node (given by 'degree' in BTree)
   a. All nodes except root has at least t-1 keys - t children
   b. At most 2t-1 keys - max 2t children
Ex. when t = 2, it can have 2, 3, 4 children, ie, 2-3-4 tree
'''
class BTree:
    def __init__(self, degree):
        self.degree = degree
        self.min_keys = degree - 1
        self.max_keys = 2 * degree - 1
        self.reset()

    def reset(self):
        self.root = BTreeNode()
        self.size = 0
        self.height = 0
        self.verticalArray = []

    def search(self, node, value):
        i = 0
        while i < node.vLen and value > node.values[i]:
            i += 1

        if i < node.vLen and value == node.values[i]:
            return node, i
        elif node.isLeaf:
            return None
        else:
            child = node.children[i]
            return self.search(child, value)

    def insert_nonfull(self, node, value):
        i = node.vLen - 1
        if node.isLeaf:
            node.values.append(0)
            node.vLen += 1
            while i >= 0 and value < node.values[i]:
                node.values[i+1] = node.values[i]
                i -= 1
            node.values[i+1] = value
        else:
            while i >= 0 and value < node.values[i]:
                i -= 1
            i += 1
            if node.children[i].vLen == self.max_keys:
                self.split_child(node, i)
                if value > node.values[i]:
                    i += 1
            self.insert_nonfull(node.children[i], value)


    def insert(self, value):
        root = self.root
        if root.vLen == self.max_keys:
            node = BTreeNode()
            self.root = node
            node.isLeaf = False
            node.children.append(root)
            self.split_child(node, 0)
            self.insert_nonfull(node, value)
        else:
            self.insert_nonfull(root, value)

    def split_child(self, node, idx):
        # split the node's child at idx with self.max_keys into 2 -> y and z - with self.min_keys each
        # if the child is not leaf, then transfer it's children as well obviously
        # z should also be made a child of node
        # push the median element to node's values
        z = BTreeNode()
        y = node.children[idx]

        z.isLeaf = y.isLeaf
        t = self.min_keys + 1

        # transfer the 2nd half of y to z
        for i in range(self.min_keys):
            z.values.append(y.values[i+t])
        z.vLen = len(z.values)

        # for non-leaf y, transfer the children in second half too
        if not y.isLeaf:
            for i in range(t):
                z.children.append(y.children[i + t])

        median_value = y.values[self.min_keys]
        # reduce y to its first half
        y.values = y.values[:self.min_keys]
        y.vLen = len(y.values)
        y.children = y.children[:t]

        # to insert z as a child of node, allocate space first
        # NOTE: y is already present at idx, z must go at idx+1 as it was the second half
        node.children.append(None)
        for i in range(node.vLen, idx, -1):
            node.children[i+1] = node.children[i]
        node.children[idx+1] = z

        # to insert median_node as a child of node, allocate space first
        # NOTE: median_value will occupy the position at idx since the larger valued child z should be to the right [at idx+1]
        if node.vLen > 0:
            node.values.append(None)
            for i in range(node.vLen-1, idx-1, -1):
                node.values[i+1] = node.values[i]
            node.values[idx] = median_value
        else:
            node.values.append(median_value)
        node.vLen = len(node.values)


    def create_and_print_vertical_array(self):
        root = self.root
        self.verticalArray = []
        self.get_vertical_array(root, self.verticalArray, 1)
        count = 0
        for i in self.verticalArray:
            print("Level: ", count, ", Keys: ", i)
            count += 1


    def get_vertical_array(self, node, array, level):
        if node == None:
            return

        if len(array) < level:
            array.append([])

        if node.isLeaf:
            array[level-1].append(node.values)
            return

        for i in range(node.vLen):
            child = node.children[i]
            self.get_vertical_array(child, array, level+1)

        if len(node.children) > node.vLen:
            child = node.children[-1]
            self.get_vertical_array(child, array, level+1)

        array[level-1].append(node.values)
        return



def insertion_tests(btree, array):
    print(f"Started Insertion For: {array}, tree degree: {btree.degree}")
    for i in array:
        btree.insert(i)
    btree.create_and_print_vertical_array()
    print("")


if __name__ == "__main__":
    # degree-2, max 3, min 1
    #  - 8 sorted nodes - 2 levels
    #  - 9 sorted nodes - 3 levels
    # degree-3, max 5, min 2
    #  - 17 sorted nodes - 2 levels
    #  - 18 sorted nodes - 3 levels
    # degree-4, max 7, min 3
    tests = {
        1: [ [1, 2, 3, 4, 5, 6, 7, 8, 9],   [5, 4, 1, 2, 3] ],
        2: [ [9, 8, 7, 6, 5, 4, 3, 2, 1],   [8, 9, 3, 5, 1, 4, 7, 6, 0, 2] ],
        3: [ [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], [] ]
    }

    for degree in [2, 3, 4]:
        btree = BTree(degree)
        for key, value in tests.items():
            insertion = value[0]
            deletion = value[1]
            insertion_tests(btree, insertion)
            btree.reset()
