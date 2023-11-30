class QuadTreeNode:
    def __init__(self, bit, isLeaf, topLeft, topRight, bottomLeft, bottomRight, parent):
        self.bit = bit
        self.isLeaf = isLeaf
        self.topLeft = topLeft
        self.topRight = topRight
        self.bottomLeft = bottomLeft
        self.bottomRight = bottomRight
        self.parent = parent
        self.type = None

class QuadTree:
    def __init__(self):
        self.height = 0
        self.size = 0
        self.root = None

    def reset(self):
        self.height = 0
        self.size = 0
        self.root = None

    def createFromMatrix(self, grid):
        matrix = []
        n = len(grid)
        if n == 1:
            self.root = QuadTreeNode(grid[0][0], 1, None, None, None, None, None)
            self.root.type = "root"
            return self.root

        max_sum = n * n
        c_sum = 0
        for i in range(n):
            matrix.append([])
            for j in range(n):
                matrix[i].append(QuadTreeNode(grid[i][j], 1, None, None, None, None, None))
                c_sum += grid[i][j]

        if c_sum == 0:
            self.root = QuadTreeNode(0, 1, None, None, None, None, None)
        elif c_sum == max_sum:
            self.root = QuadTreeNode(1, 1, None, None, None, None, None)
        else:
            self.root = self.build_quad_tree(matrix)

        self.root.type = "root"
        return self.root

    def build_quad_tree(self, matrix):
        if len(matrix) == 1:
            return matrix[0][0]

        n = len(matrix)
        n_matrix = []
        for i in range(0, n, 2):
            n_matrix.append([])
            idx = len(n_matrix) - 1
            for j in range(0, n, 2):
                topLeft = matrix[i][j]
                topRight = matrix[i][j+1]
                bottomLeft = matrix[i+1][j]
                bottomRight = matrix[i+1][j+1]
                node = QuadTreeNode(0, 0, topLeft, topRight, bottomLeft, bottomRight, None)
                if (topLeft.bit == topRight.bit == bottomLeft.bit == bottomRight.bit) & (topLeft.isLeaf & topRight.isLeaf & bottomLeft.isLeaf & bottomRight.isLeaf):
                    node.topLeft = node.topRight = node.bottomLeft = node.bottomRight = None
                    node.isLeaf = 1
                    node.bit = topLeft.bit
                    topLeft = topRight = bottomLeft = bottomRight = None
                else:
                    topLeft.parent = topRight.parent = bottomLeft.parent = bottomRight.parent = node
                    topLeft.type = "topLeft"
                    topRight.type = "topRight"
                    bottomLeft.type = "bottomLeft"
                    bottomRight.type = "bottomRight"
                n_matrix[idx].append(node)

        return self.build_quad_tree(n_matrix)

    def traverseLeftToRight(self, root, level=0):
        if level == 0:
            print(level, root.bit, "root")
            
        if root.topLeft != None:
            print(" " * (level + 1), level + 1, root.topLeft.bit, root.topLeft.type)

        if root.topRight != None:
            print(" " * (level + 1), level + 1, root.topRight.bit, root.topRight.type)

        if root.bottomLeft != None:
            print(" " * (level + 1), level + 1, root.bottomLeft.bit, root.bottomLeft.type)

        if root.bottomRight != None:
            print(" " * (level + 1), level + 1, root.bottomRight.bit, root.bottomRight.type)

        if root.topLeft != None:
            self.traverseLeftToRight(root.topLeft, level + 1)

        if root.topRight != None:
            self.traverseLeftToRight(root.topRight, level + 1)

        if root.bottomLeft != None:
            self.traverseLeftToRight(root.bottomLeft, level + 1)

        if root.bottomRight != None:
            self.traverseLeftToRight(root.bottomRight, level + 1)


if __name__ == "__main__":
    testcases = [
            [[0,1],[1,0]],
            [[1,1,1,1,0,0,0,0],[1,1,1,1,0,0,0,0],[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1],[1,1,1,1,0,0,0,0],[1,1,1,1,0,0,0,0],[1,1,1,1,0,0,0,0],[1,1,1,1,0,0,0,0]],
            [[1,1],[1,1]],
            [[1]],
            [[0]],
            [[1,1,0,0],[0,0,1,1],[1,1,0,0],[0,0,1,1]],
            [[1,1,0,0,1,1,0,0],[0,0,1,1,0,0,1,1],[1,1,0,0,1,1,0,0],[0,0,1,1,0,0,1,1],[1,1,0,0,1,1,0,0],[0,0,1,1,0,0,1,1],[1,1,0,0,1,1,0,0],[0,0,1,1,0,0,1,1]]
    ]

    tree = QuadTree()
    for i in range(len(testcases)):
        t = testcases[i]
        print(f"i: {i}, Creating and Printing")
        root = tree.createFromMatrix(t)
        tree.traverseLeftToRight(root)
        tree.reset()
