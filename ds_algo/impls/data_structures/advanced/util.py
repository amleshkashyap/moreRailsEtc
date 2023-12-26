class Util:
    @staticmethod
    def search(root, value, tnil):
        if root == tnil:
            return False

        if root.value == value:
            return root

        if value > root.value:
            return Util.search(root.right, value, tnil)
        else:
            return Util.search(root.left, value, tnil)

    @staticmethod
    def min_node(node, tnil):
        while(node.left != tnil):
            node = node.left
        return node

    @staticmethod
    def get_height(node, tnil):
        if node == tnil:
            return 1
        lheight = Util.get_height(node.left, tnil) + 1
        rheight = Util.get_height(node.right, tnil) + 1
        return max(lheight, rheight)

    @staticmethod
    def is_balanced(node, tnil):
        if node == tnil:
            return 1

        lh = Util.is_balanced(node.left, tnil)
        if lh == 0:
            return 0

        rh = Util.is_balanced(node.right, tnil)
        if rh == 0:
            return 0

        if abs(lh - rh) > 1:
            return 0

        return max(lh, rh) + 1

    @staticmethod
    def is_printable(node, tnil):
        if node == tnil:
            return 1

        lh = Util.is_printable(node.left, tnil)
        if lh == 0:
            return 0

        rh = Util.is_printable(node.right, tnil)
        if rh == 0:
            return 0

        if lh != rh:
            return 0

        return max(lh, rh) + 1

    # same as BST transplant
    @staticmethod
    def transplant(node, child_node, tree):
        if node.parent == tree.tnil:
            tree.root = child_node
        elif node == node.parent.left:
            node.parent.left = child_node
        else:
            node.parent.right = child_node

        child_node.parent = node.parent
        return

    @staticmethod
    def left_rotate(node, tree):
        if node == tree.tnil:
            return

        newRoot = node.right
        node.right = newRoot.left
        node.right.parent = node
        newRoot.left = node
        Util.transplant(node, newRoot, tree)
        node.parent = newRoot

    @staticmethod
    def right_rotate(node, tree):
        if node == tree.tnil:
            return

        newRoot = node.left
        node.left = newRoot.right
        node.left.parent = node
        newRoot.right = node
        Util.transplant(node, newRoot, tree)
        node.parent = newRoot

    @staticmethod
    def insertion_test(tree, array):
        for i in array:
            print(f"Inserting: {i}, root: {tree.root.value}, rootparent: {tree.root.parent.value if tree.root.parent else None}")
            tree.insert(i)
            tree.size = 0
            tree.constructTreeArray()
            if tree.height < 8:
                print("Stored Tree")
                Util.print_array_as_tree(tree.treeArray, tree.treeWithColor)
                print("")
                print(f"Vertical Tree: {tree.verticalArray}")
            else:
                print("Vertical Tree Lines")
                for ar in tree.verticalArray:
                    print(ar)
                print("")

    @staticmethod
    def deletion_test(tree, array):
        for i in array:
            print(f"Deleting: {i}, root: {tree.root.value}, rootparent: {tree.root.parent.value if tree.root.parent else None}")
            tree.delete(i)
            tree.size = 0
            tree.constructTreeArray()
            if tree.height < 8:
                print("Stored Tree")
                Util.print_array_as_tree(tree.treeArray, tree.treeWithColor)
                print("")
                print(f"Vertical Tree: {tree.verticalArray}")
            else:
                print("Vertical Tree Lines")
                for ar in tree.verticalArray:
                    print(ar)
                print("")

    @staticmethod
    # works only for single digit numbers
    def print_array_as_tree(array, with_color=[]):
        if len(array) == 0:
            return

        redblack = True
        if len(with_color) == 0:
            redblack = False
            with_color = array

        lines = {}
        lines1 = {}
        Util.print_tree(array, with_color, 0, lines, lines1, 0)
        max_height = len(lines.keys()) - 1
        max_digit_space = {}
        for key, value in lines.items():
            max_num = 0
            for i in range(len(value)):
                if value[i] != 'x' and value[i] > max_num:
                    max_num = value[i]
            max_space = len(str(max_num))
            if key > 0:
                max_space = max(max_space, max_digit_space[key-1])
            max_digit_space[key] = max_space
            for i in range(len(value)):
                t_value = str(value[i])
                if len(t_value) < max_space:
                    value[i] = t_value + (max_space - len(t_value)) * " "

        spaces = {}
        # idx 0 - spaces before first node
        # idx 1 - spaces between every node with common parent
        # idx 2 - spaces between last and first node with different parent
        spaces[max_height] = [0, 3, 1]

        for i in range(max_height-1, -1, -1):
            cur, spaces[i] = [], []
            for j in range(3):
                # calculated by taking the average of idx of the child nodes of this node, with spaces added
                this_node_idx = (2 * spaces[i+1][0] + (j * 2) * (spaces[i+1][1] + spaces[i+1][2] + (2 * max_digit_space[i+1])) + spaces[i+1][1] + max_digit_space[i+1])//2
                cur.append(this_node_idx)
                spaces[i].append(cur[j] - (-1 if j == 0 else cur[j-1]) - 1)
    
        max_length = sum(spaces[0])
    
        for key, value in lines.items():
            t_line = lines1[key]
            arrows = max_length * list(" ")
            string = " " * spaces[key][0]
            for i in range(0, len(value), 2):
                arrows[len(string) + max_digit_space[key]] = "/"
                if i+1 < len(value):
                    string += (" " * spaces[key][1]).join([str(value[i]), str(value[i+1])])
                    arrows[len(string) - max_digit_space[key] - 1] = "\\"
                else:
                    string += str(value[i])
                string += " " * spaces[key][2]
            print("".join(arrows[:len(string)])) if key > 0 else None
            if redblack:
                Util.print_line(string, t_line)
            else:
                print(string)

    @staticmethod
    def print_line(string, line):
        digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "x"]
        count = 0
        new_string = ""
        for i in string:
            if i in digits:
                new_string += str(line[count])
                count += 1
            else:
                new_string += " "
        print(new_string)

    @staticmethod
    def print_tree(array, with_color, index, lines, lines1, level):
        if index < len(array):
            if lines.get(level) == None:
                lines[level] = []
                lines1[level] = []
            lines[level].append(array[index])
            lines1[level].append(with_color[index])
            left_index = 2 * index + 1
            right_index = 2 * index + 2
            Util.print_tree(array, with_color, left_index, lines, lines1, level + 1)
            Util.print_tree(array, with_color, right_index, lines, lines1, level + 1)
