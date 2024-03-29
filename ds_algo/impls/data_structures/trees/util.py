class Util:
    @staticmethod
    # works only for single digit numbers
    def print_array_as_tree(array):
        if len(array) == 0:
            return

        lines = {}
        Util.print_tree(array, 0, lines, 0)
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
            print(string)

    @staticmethod
    def print_tree(array, index, lines, level):
        if index < len(array):
            if lines.get(level) == None:
                lines[level] = []
            lines[level].append(array[index])
            left_index = 2 * index + 1
            right_index = 2 * index + 2
            Util.print_tree(array, left_index, lines, level + 1)
            Util.print_tree(array, right_index, lines, level + 1)
