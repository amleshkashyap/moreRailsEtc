# DFS - use the visited concept, or mark existing data structure with visited (less memory)
# Loop in graph - use the visiting concept
# Graph traversal with unique nodes - add a node only when it's first visit completes (ie, when visited is marked True for first time)
# in python [[]] * n creates a weird thing
# Graph BFS can be tricky - one must maintain the levels for a correct traversal
#  - Graph DFS is much simpler
#  - Need to add some problems demonstrating BFS and DFS and some variations

class Graph:
    def __init__(self):
        self.graphArray = []
        return

    def constructGraphFromArray(self, array):
        pass
