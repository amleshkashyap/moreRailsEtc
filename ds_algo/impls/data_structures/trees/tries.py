class Trie(object):
    import string

    def __init__(self):
        self.children = {}
        self.isLeaf = False

    def insert(self, word):
        char = word[0].lower()
        if char not in self.children.keys():
            node = Trie()
            self.children[char] = node
        else:
            node = self.children[char]

        if len(word) == 1:
            node.isLeaf = True
            return
        node.insert(word[1:])

    def search(self, word):
        if len(self.children) == 0:
            return False
        char = word[0].lower()
        if char in self.children.keys():
            root = self.children[char]
            if len(word) == 1:
                if root.isLeaf == True:
                    return True
                else:
                    return False
            found = root.search(word[1:])
            return found
        else:
            return False

    def startsWith(self, prefix):
        if len(self.children) == 0:
            return False
        char = prefix[0].lower()
        if char in self.children.keys():
            if len(prefix) == 1:
                return True
        else:
            return False
        root = self.children[char]
        found = root.startsWith(prefix[1:])
        return found

    def searchWithDot(self, word):
        pass
        

class Trie(object):
    def __init__(self):
        self.children = {}
        self.isLeaf = False

    def insert(self, word):
        root = self
        for char in word.lower():
            if char not in root.children.keys():
                root.children[char] = Trie()
            root = root.children[char]

        root.isLeaf = True

    def search(self, word):
        root = self
        for char in word.lower():
            if char not in root.children.keys():
                return False
            root = root.children[char]

        return root.isLeaf

    def startsWith(self, prefix):
        root = self
        for char in prefix.lower():
            if char not in root.children.keys():
                return False
            root = root.children[char]

        return True


# Fast without recursion

class TrieWithDict(object):
    def __init__(self):
        self.children = {"children": {}, "leaf": False}

    def insert(self, word):
        root = self.children
        for char in word.lower():
            if char not in root["children"].keys():
                root["children"][char] = {"children": {}, "leaf": False}
            root = root["children"][char]

        root["leaf"] = True

    def search(self, word):
        root = self.children
        for char in word.lower():
            if char not in root["children"].keys():
                return False
            root = root["children"][char]

        return root["leaf"]

    def startsWith(self, prefix):
        root = self.children
        for char in prefix.lower():
            if char not in root["children"].keys():
                return False
            root = root["children"][char]

        return True


class WordDictionary(object):
    def __init__(self):
        # self.children = {}
        # self.isLeaf = False
        # self.hasLeafChild = False
        self.children = {"children": {}, "leaf": False}


    def addWord(self, word):
        """
        :type word: str
        :rtype: None
        """
        # char = word[0].lower()
        # if char == ".":
        #     if len(word) == 1:
        #         self.isLeaf = True
        #     return
        # if char not in self.children.keys():
        #     node = WordDictionary()
        #     self.children[char] = node
        # else:
        #     node = self.children[char]

        # if len(word) == 1:
        #     node.isLeaf = True
        #     self.hasLeafChild = True
        #     return
        # node.addWord(word[1:])
        root = self.children["children"]
        count = 0
        for char in word.lower():
            count += 1
            if char not in root.keys():
                root[char] = {"children": {}, "leaf": False}
            if count == len(word):
                root[char]["leaf"] = True
            root = root[char]["children"]

    def search(self, word):
        """
        :type word: str
        :rtype: bool
        """
        # char = word[0].lower()
        # if char in self.children.keys():
        #     root = self.children[char]
        #     if len(word) == 1:
        #         return root.isLeaf
        #     return root.search(word[1:])
        # elif char == ".":
        #     if len(word) == 1:
        #         return self.hasLeafChild
        #     for c, node in self.children.items():
        #         if node.search(word[1:]) == True:
        #             return True
        # return False
        # print(word, self.children)
        roots = [self.children["children"]]
        count = 0
        for char in word.lower():
            count += 1
            to_traverse = len(roots)
            rcount = 0
            while(len(roots) > 0):
                root = roots.pop(0)
                rcount += 1
                if char in root.keys():
                    if count == len(word):
                        if root[char]["leaf"] == True:
                            return True
                        continue
                    roots.append(root[char]["children"])
                elif char == ".":
                    if count == len(word):
                        for c, node in root.items():
                            if node["leaf"] == True:
                                return True
                        continue
                    for c, node in root.items():
                        roots.append(node["children"])
                if rcount == to_traverse:
                    break

        return False




# Your WordDictionary object will be instantiated and called as such:
# obj = WordDictionary()
# obj.addWord(word)
# param_2 = obj.search(word)

class WordDictionary(object):

    def __init__(self):
        self.children = {}
        self.isLeaf = False
        

    def addWord(self, word):
        """
        :type word: str
        :rtype: None
        """
        char = word[0].lower()
        # if char == ".":
        #     if len(word) == 1:
        #         self.isLeaf = True
        #     return
        if char not in self.children.keys():
            node = WordDictionary()
            self.children[char] = node
        else:
            node = self.children[char]

        # print("ok1", word, self.children)
        if len(word) == 1:
            node.isLeaf = True
            return
        node.addWord(word[1:])
        

    def search(self, word):
        """
        :type word: str
        :rtype: bool
        """
        char = word[0].lower()
        # print("ok2", word, self.children)
        if char in self.children.keys():
            root = self.children[char]
            if len(word) == 1:
                if root.isLeaf == True:
                    return True
                else:
                    return False
            found = root.search(word[1:])
            return found
        elif char == ".":
            if len(word) == 1:
                for c, node in self.children.items():
                    if node.isLeaf == True:
                        return True
                return False
            found = False
            for c, node in self.children.items():
                t_found = node.search(word[1:])
                if t_found == True:
                    found = True
            return found
        else:
            return False
            
        


# Your WordDictionary object will be instantiated and called as such:
# obj = WordDictionary()
# obj.addWord(word)
# param_2 = obj.search(word)



# Given an m x n board of characters and a list of strings words, return all words on the board.

# Each word must be constructed from letters of sequentially adjacent cells, where adjacent cells are horizontally or vertically neighboring. The same letter cell may not be used more than once in a word.

# m == board.length
# n == board[i].length
# 1 <= m, n <= 12
# board[i][j] is a lowercase English letter.
# 1 <= words.length <= 3 * 104
# 1 <= words[i].length <= 10
# words[i] consists of lowercase English letters.
# All the strings of words are unique.

# Optimisations
#   - If words to be searched < 10, then it doesn't make sense to find out all the possible words
#   - If given words to be searched have pretty much the same prefix, then all possible words don't need to be built
#   - Indexing can be performed
class Solution:
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        """
        :type board: List[List[str]]
        :type words: List[str]
        :rtype: List[str]
        """
        nodes = {}
        chars = {}
        result = []

        for i in range(len(board)):
            for j in range(len(board[i])):
                key = f'{i},{j}'
                char = board[i][j]
                nodes[key] = TrieNode(key, char)
                if chars.get(char):
                    chars[char].append(key)
                else:
                    chars[char] = [key]

        for key, node in nodes.items():
            i, j = list(map(int, (key.split(","))))
            all_keys = []
            if i < len(board) - 1:
                all_keys.append(f'{i+1},{j}')
            if i > 0:
                all_keys.append(f'{i-1},{j}')
            if j < len(board[i]) - 1:
                all_keys.append(f'{i},{j+1}')
            if j > 0:
                all_keys.append(f'{i},{j-1}')

            for k in all_keys:
                node.addChild(nodes[k])
            # print(node.key, node.char, [(x.key, x.char) for x in node.children])

        trieOpt = Trie()
        uniquePrefix = []
        for word in words:
            char = word[0]
            if char not in uniquePrefix:
                uniquePrefix.append(char)

        # if len(uniquePrefix) > 4 and len(board[0]) > 8:
        if len(words) < 20 or (len(board[0]) > 11 and len(uniquePrefix) > 4):
            for word in words:
                if word[0] not in chars:
                    continue
                elif len(word) == 1:
                    result.append(word)
                    continue
                char = word[0]
                keys_to_traverse = chars[char]
                for key in keys_to_traverse:
                    node = nodes[key]
                    if node.search(word[1:], [key]) == True:
                        result.append(word)
                        break
            return result

        for key, node in nodes.items():
            if node.char in uniquePrefix:
                node.createAndAddWords(1, [key], node.char, trieOpt)


        for word in words:
            if word[0] not in chars:
                continue
            elif len(word) == 1:
                result.append(word)
                continue
            if trieOpt.startsWith(word) == True:
                result.append(word)
        return result


class TrieNode(object):
    def __init__(self, key, char):
        self.key = key
        self.char = char
        self.children = []

    def addChild(self, node):
        self.children.append(node)

    def createAndAddWords(self, depth, visited, fullWord, trieOpt):
        if depth == 10 or len(self.children) == 0:
            trieOpt.insert(fullWord)
            return
        found = False
        for node in self.children:
            if node.key in visited:
                continue
            found = True
            visited.append(node.key)
            node.createAndAddWords(depth + 1, visited, fullWord + node.char, trieOpt)
            visited.remove(node.key)
        if found == False:
            # print("Adding", fullWord)
            trieOpt.insert(fullWord)
            return

    def search(self, word, visited):
        char = word[0]
        for node in self.children:
            if node.key in visited or char != node.char:
                continue
            if len(word) == 1:
                return True
            visited.append(node.key)
            if node.search(word[1:], visited) == True:
                return True
            visited.remove(node.key)
        return False

class Trie():
    def __init__(self):
        self.children = {"children": {}}
        self.indexes = {}

    def insert(self, word):
        root = self.children
        for char in word:
            if char not in root["children"].keys():
                root["children"][char] = {"children": {}}
            root = root["children"][char]


    def startsWith(self, prefix):
        root = self.children
        for char in prefix:
            if char not in root["children"].keys():
                return False
            root = root["children"][char]
        return True
