from util import Util
from collections import deque

class BTreeNode():
    def __init__(self):
        self.values = deque()
        self.children = deque()
        self.isLeaf = True

'''
1. Node x
   a. It has n keys (given by len(values), and stored in values of BTreeNode)
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
        # degree = t
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
        while i < len(node.values) and value > node.values[i]:
            i += 1

        if i < len(node.values) and value == node.values[i]:
            return node, i
        elif node.isLeaf:
            return None
        else:
            child = node.children[i]
            return self.search(child, value)

    def insert_nonfull(self, node, value):
        i = len(node.values) - 1
        if node.isLeaf:
            node.values.append(0)
            while i >= 0 and value < node.values[i]:
                node.values[i+1] = node.values[i]
                i -= 1
            node.values[i+1] = value
        else:
            while i >= 0 and value < node.values[i]:
                i -= 1
            i += 1
            if len(node.children[i].values) == self.max_keys:
                self.split_child(node, i)
                if value > node.values[i]:
                    i += 1
            self.insert_nonfull(node.children[i], value)


    def insert(self, value):
        root = self.root
        if len(root.values) == self.max_keys:
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
        t = self.degree

        # transfer the 2nd half of y to z
        for i in range(self.min_keys):
            z.values.append(y.values[i+t])

        # for non-leaf y, transfer the children in second half too
        if not y.isLeaf:
            for i in range(t):
                z.children.append(y.children[i + t])

        median_value = y.values[self.min_keys]
        # reduce y to its first half
        values, children = deque(), deque()

        for i in range(min(self.min_keys, len(y.values))):
            values.append(y.values[i])

        for i in range(min(t, len(y.children))):
            children.append(y.children[i])

        y.values = values
        y.children = children

        # to insert z as a child of node, allocate space first
        # NOTE: y is already present at idx, z must go at idx+1 as it was the second half
        node.children.append(None)
        for i in range(len(node.children)-2, idx, -1):
            node.children[i+1] = node.children[i]
        node.children[idx+1] = z

        # to insert median_node as a child of node, allocate space first
        # NOTE: median_value will occupy the position at idx since the larger valued child z should be to the right [at idx+1]
        if len(node.values) > 0:
            node.values.append(None)
            for i in range(len(node.values)-2, idx-1, -1):
                node.values[i+1] = node.values[i]
            node.values[idx] = median_value
        else:
            node.values.append(median_value)


    def create_and_print_vertical_array(self):
        root = self.root
        self.verticalArray = []
        self.get_vertical_array(root, self.verticalArray, 1)
        count = 0
        for i in self.verticalArray:
            print("Level: ", count, ", Keys: ", i)
            count += 1

    # adds the values of z at the end of y. adds children too if they exist
    def merge_nodes(self, y, z):
        y.values += z.values
        y.children += z.children
        z.values = z.children = []
        return

    # only scenario when this method is called on a node with <= t-1 values is when node = root
    # if root is a leaf node, then removal is permissible for any number of keys
    def delete(self, node, value):
        if node == self.root and len(node.values) == 0:
            print("Tree is empty")
            return

        i = 0
        t = self.degree
        keys = len(node.values)
        children = len(node.children)

        while(i < keys and value > node.values[i]):
            i += 1

        '''
        print(f"Deleting: {value}, at i: {i}, values: {node.values}, children: {children}")
        if children > 0:
            for j in node.children:
                print(j.values)
        print("")
        '''
        if i == keys:
            if node.isLeaf or children <= i:
                print(f"Given key: {value} not present in the tree")
                return

            # value maybe present in the last child
            child = node.children[i]
        elif node.values[i] == value:
            if node.isLeaf:
                del node.values[i]
                return

            y = node.children[i]
            z = None
            if children > i+1:
                z = node.children[i+1]

            if len(y.values) >= t:
                if y.isLeaf:
                    node.values[i] = y.values[-1]
                    y.values.pop()
                    return

                # y has t values, hence safe to descend
                to_replace = y.values[-1]
                self.delete(y, to_replace)
                node.values[i] = to_replace

            elif z and len(z.values) >= t:
                if z.isLeaf:
                    node.values[i] = z.values[0]
                    z.values.popleft()
                    return

                # z has t values, hence safe to descend
                to_replace = z.values[0]
                self.delete(z, to_replace)
                node.values[i] = to_replace
            else:
                # remove z if it exists
                if z:
                    self.merge_nodes(y, z)
                    del node.children[i+1]

                del node.values[i]
            return
        elif i >= children:
            # no further children to be checked
            print(f"Given key: {value} not present in the tree")
            return
        else:
            child = node.children[i]

        if len(child.values) >= t:
            self.delete(child, value)
            return

        y_keys = z_keys = 0

        if children == 1:
            y = z = None
        elif i == 0:
            y = None
            z = node.children[1]
            z_keys = len(z.values)
        elif i == children - 1:
            y = node.children[i-1]
            y_keys = len(y.values)
            z = None
        else:
            y = node.children[i-1]
            y_keys = len(y.values)
            z = node.children[i+1]
            z_keys = len(z.values)

        '''
          child is the left child of key node.values[i]
          y is the left sibling of child, ie, left shared child of the key before node.values[i]
          z is the right sibling of child, ie, right shared child of node.values[i]

          1. if y exists, then node.values[i-1] must exist
          2. swapping of children with y would mean y -> node.values[i-1] -> child
          3. swapping of children with z would mean child -> node.values[i] -> z
        '''

        if y_keys >= t:
            child.values.appendleft(node.values[i-1])
            node.values[i-1] = y.values.pop()
            if len(y.children) == len(y.values) + 1:
                child.children.appendleft(y.children.pop())
        elif z_keys >= t:
            child.values.append(node.values[i])
            node.values[i] = z.values.popleft()
            if len(z.children) > 0:
                child.children.append(z.children.popleft())
        else:
            # since every node encountered must've at least t keys - where t >= 2
            # a node with 1 key would mean it was root
            make_root = False
            if len(node.values) == 1:
                make_root = True

            if y:
                y.values.append(node.values[i-1])
                self.merge_nodes(y, child)
                del node.values[i-1]
                del node.children[i]
                child = y
            elif z:
                child.values.append(node.values[i])
                self.merge_nodes(child, z)
                del node.values[i]
                del node.children[i+1]

            if make_root:
                self.root = child

        self.delete(child, value)


    def get_vertical_array(self, node, array, level):
        if node == None:
            return

        if len(array) < level:
            array.append([])

        if node.isLeaf:
            array[level-1].append(node.values)
            return

        for i in range(len(node.values)):
            child = node.children[i]
            self.get_vertical_array(child, array, level+1)

        if len(node.children) > len(node.values):
            child = node.children[-1]
            self.get_vertical_array(child, array, level+1)

        array[level-1].append(node.values)
        return



def insertion_tests(btree, array):
    print(f"Started Insertion For: {array}, tree degree: {btree.degree}")
    for i in array:
        print(f"Inserting: {i}, root values: {btree.root.values}")
        btree.insert(i)
    btree.create_and_print_vertical_array()
    print("")

def deletion_tests(btree, array):
    print(f"Started Deletion For: {array}, tree degree: {btree.degree}")
    for i in array:
        print(f"Deleting: {i}, root values: {btree.root.values}")
        btree.delete(btree.root, i)
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
        1: [ [1, 2, 3, 4, 5, 6, 7, 8, 9],   [5, 4, 1, 2, 3, 6, 8, 9, 7, 0] ],
        2: [ [9, 8, 7, 6, 5, 4, 3, 2, 1],   [8, 9, 3, 5, 1, 4, 7, 6, 0, 2] ],
        3: [ [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], [0, 1, 2, 3, 4, 5, 19] ]
    }

    for degree in [2, 3, 4]:
        btree = BTree(degree)
        for key, value in tests.items():
            insertion = value[0]
            deletion = value[1]
            deletion_tests(btree, [1])
            insertion_tests(btree, insertion)
            deletion_tests(btree, deletion)
            btree.reset()
