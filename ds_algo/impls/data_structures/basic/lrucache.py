# doubly linked list with dictionary
class LRUCache:
    def __init__(self, capacity: int):
        self.size = capacity
        self.nodes = {}
        self.head = None
        self.tail = None
        
    def get(self, key: int) -> int:
        if key in self.nodes:
            node = self.nodes[key]
            if node == self.tail or len(self.nodes) == 1:
                return node.value
            elif node == self.head:
                self.head = self.head.next
                self.head.prev = None

            self.tail = node.make_latest(self.tail)
            return node.value
        return -1
        
    def put(self, key: int, value: int) -> None:
        if key in self.nodes:
            node = self.nodes[key]
            if node == self.tail or len(self.nodes) == 1:
                node.value = value
                self.nodes[key] = node
                return
            elif node == self.head:
                self.head = self.head.next
                self.head.prev = None

            node.value = value
            self.tail = node.make_latest(self.tail)
            return

        if len(self.nodes) == self.size:
            k = self.head.key
            if self.size == 1:
                self.head = None
            else:
                self.head = self.head.next
                self.head.prev = None
            del self.nodes[k]

        node = LRUNode(key, value, self.tail)
        self.nodes[key] = node
        if len(self.nodes) == 1:
            self.head = node

        self.tail = node
        return

class LRUNode:
    def __init__(self, key, value, prev):
        self.key = key
        self.value = value
        self.prev = prev
        if prev:
            self.prev.next = self
        self.next = None
    
    def make_latest(self, tail):
        if self.prev:
            self.prev.next = self.next
        
        if self.next:
            self.next.prev = self.prev

        self.prev = tail
        self.next = None
        tail.next = self
        return self

class LRUCacheDict:
    def __init__(self, capacity: int):
        self.size = capacity
        self.nodes = {}
        
    def get(self, key: int) -> int:
        if key in self.nodes:
            v = self.nodes[key]
            del self.nodes[key]
            self.nodes[key] = v
            return v
        return -1
        
    def put(self, key: int, value: int) -> None:
        if key in self.nodes:
            del self.nodes[key]
            self.nodes[key] = value
            return

        if len(self.nodes) == self.size:
            for i in self.nodes:
                del self.nodes[i]
                break

        self.nodes[key] = value
        return
