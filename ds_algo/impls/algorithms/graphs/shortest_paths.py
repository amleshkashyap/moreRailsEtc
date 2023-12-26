class Vertex:
    def __init__(self, key):
        self.key = key
        self.reset()

    def reset(self):
        self.color = 0
        self.prev = None
        self.vstart = self.vend = None

    def can_visit(self):
        return (self.color == 0)

    def is_visiting(self):
        return (self.color == 1)

    def visiting(self, time):
        self.color = 1
        self.vstart = time

    def visited(self, time):
        self.color = 2
        self.vend = time

# assumes input edges to be
#  1. an array of triplets - u, v, w
#  2. an adjacency matrix (2D Square Matrix)
# weight 0 denotes no edge
# stores vertices as dictionary - key: node key, value: Vertex object
# stores edges as an array of size 2 arrays
# stores weights in 2D dictionaries - key: node key, value: dictionary -> key: adjacent node key, value: edge weight
# perform topological sort at initialisation to find which SSSP method to use
class Graph:
    def __init__(self, edges):
        if len(edges) < 3:
            print("Invalid Input: graph must have 3 edges")
        elif len(edges[0]) < 2:
            print("Invalid Input: adjacency list must have at least 2 vertices")
        elif len(edges[0]) > 3 and len(edges[0]) != len(edges):
            print(f"Invalid Input: adjacency matrix must have same rows and columns: {len(edges)}")
        self.reset(edges)

    def reset(self, edges):
        is_list = True
        if len(edges[0]) > 3:
            is_list = False
        self.edges = []
        self.weights = {}
        self.has_negative_weight = False
        self.vertices = {}
        if not is_list:
            self.convert_to_adjacency_list(edges)
        else:
            self.create_adjacency_list(edges)

        self.vertices_set = False
        self.is_dag = False
        self.tsorted = []
        # self.dfs()
        self.topological_sort()

    def create_adjacency_list(self, edges):
        if len(edges[0]) == 2:
            weights = [1] * len(edges)
        else:
            weights = [x[2] for x in edges]
            if min(weights) < 0:
                self.has_negative_weight = True

        count = 0
        for i in edges:
            u, v = i[0], i[1]
            if u == v:
                print(f"Edge to self not allowed, vertex: {u}")
                return

            if u not in self.vertices:
                self.vertices[u] = Vertex(u)
            if v not in self.vertices:
                self.vertices[v] = Vertex(v)

            w = weights[count]
            if w == 0:
                count += 1
                continue

            self.edges.append([u, v])
            if u in self.weights:
                self.weights[u][v] = w
            else:
                self.weights[u] = { v: w }
            count += 1

    def add_edge(self, edge, weight=1):
        u, v = edge
        if u == v:
            print(f"Edge to self not allowed, vertex: {u}")
            return

        if u not in self.vertices:
            self.vertices[u] = Vertex(u)
        if v not in self.weights:
            self.vertices[v] = Vertex(v)

        if weight == 0:
            return

        self.edges.append(edge)
        if u in self.weights:
            self.weights[u][v] = weight
        else:
            self.weights[u] = { v: weight }

    def convert_to_adjacency_list(self, matrix):
        for i in range(len(matrix)):
            self.weights[i] = {}
            self.vertices[i] = Vertex(i)
            for j in range(len(matrix[0])):
                if i == j:
                    continue

                w = matrix[i][j]
                if w == 0:
                    continue

                if w < 0:
                    self.has_negative_weight = True
                self.edges.append([i, j])
                self.weights[i][j] = w

    def reset_vertices(self):
        for key, v in self.vertices.items():
            v.reset()

    def dfs(self):
        if self.vertices_set:
            self.reset_vertices()

        time = 0
        for key, v in self.vertices.items():
            if v.can_visit():
                time = self.dfs_visit(v, time)
        self.vertices_set = True

    def dfs_visit(self, v, time):
        time += 1
        v.visiting(time)
        if v.key in self.weights:
            for key in self.weights[v.key]:
                u = self.vertices[key]
                if u.can_visit():
                    u.prev = v
                    time = self.dfs_visit(u, time)
        time += 1
        v.visited(time)
        return time

    def topological_sort(self):
        if self.vertices_set:
            self.reset_vertices()

        res = True
        for key, v in self.vertices.items():
            if v.can_visit():
                res = self.tsort_visit(v)
                if res == False:
                    break
        if res == True:
            self.is_dag = True
        self.vertices_set = True

    def tsort_visit(self, v):
        v.visiting(0)
        if v.key in self.weights:
            for key in self.weights[v.key]:
                u = self.vertices[key]
                if u.is_visiting():
                    return False
                if u.can_visit():
                    res = self.tsort_visit(u)
                    if res == False:
                        return False
        v.visited(0)
        self.tsorted.append(v)
        return True

    def print_graph(self):
        for key in self.weights:
            w = self.weights[key]
            for i in w:
                print(f"{key} --> {i}, dist: {w[i]}")

# takes an initialised Graph object in which shortest paths have to be found
# executes the shortest path procedures and prints output
class ShortestPaths:
    def __init__(self, graph=None):
        self.maxval = 999999999
        if graph:
            self.reset(graph)

    def reset(self, graph):
        self.priority_queue = []
        self.edges = graph.edges
        self.weights = graph.weights
        self.has_negative_weight = graph.has_negative_weight
        self.is_dag = graph.is_dag
        self.vertices = list(graph.vertices.keys())
        self.len_vertices = len(self.vertices)
        self.tsorted = graph.tsorted
        self.distances = {}
        self.previous = {}

    '''
      # Single source shortest paths, if they exist, will not have a cycle
        - A negative cycle will mean such a path can't exist (as one can keep looping through the cycle to get shorter paths)
        - A positive cycle will mean that the cycle can be removed to obtain a shorter path
      # Hence, finding SSSP in DAG is a straightforward procedure - even if negative weight edges are present
      # Finding if a graph is DAG is also straightforward using a slightly modified DFS procedure
      # If a graph was not DAG, but had negative weight edges, then Bellman Ford can be used to detect negative cycle or find shortest path
        - It works by running relaxation procedure V-1 times - if at Vth iteration, weights are still decreasing, then it outputs False
        - Else, a shortest path has been found already
      # Else, Dijkstra's procedure can be used
        - At every step, the smallest distance vertex is to be used for relaxation of adjacent edges
        - New distances should be updated and next smallest distance vertex is to be found
        - Each of these are removed from the min-heap
      # Relaxation procedure works by examining various edges for finding a shorter distance between 2 vertices, ie, if there was a path
        from s -> v [s, v1, v2, .., v -> intermediates vertices can be absent too] which didn't include u, but a path from s -> u was found
        such that len(s -> u) + len(u -> v) < len(s -> v), then one will discard the older path from s -> v, and visit v via s -> u -> v.
        - Initially, it's assumed that all the vertices are at infinite distance
        - Then one can start by checking the neighbours of s, performing a BFS on the entire graph (ie, Bellman Ford) or a greedy selection
          using Dijkstra's procedure, which may perform BFS on the nearby neighbours.

      # Good resource to visualize graphs - https://visualgo.net/en/sssp [with some incorrect implementations of SSSP]
    '''
    def single_source(self, vertex):
        self.initialise_single_source(vertex)
        if self.is_dag:
            print("DAG SSSP")
            res = self.dag_single_source(vertex)
            if res:
                print(f"Source: {vertex}, Distances: {self.distances}, Path: {self.previous}")
        elif self.has_negative_weight:
            print("Bellman Ford SSSP")
            res = self.bellman_ford_single_source(vertex)
            if res:
                print(f"Source: {vertex}, Distances: {self.distances}, Path: {self.previous}")
        else:
            print("Djikstra SSSP")
            res = self.dijkstra_single_source(vertex)
            if res:
                print(f"Source: {vertex}, Distances: {self.distances}, Path: {self.previous}")

    def initialise_single_source(self, vertex):
        for key in self.vertices:
            self.distances[key] = self.maxval
        self.distances[vertex] = 0

    def initialise_priority_queue(self, vertex):
        self.priority_queue = [ [vertex, 0] ]
        for key in self.vertices:
            if key != vertex:
                self.priority_queue.append([key, self.maxval])

    # update the min heap with newly computed distances
    # min heapify by distance
    def adjust_priority_queue(self):
        for i in range(len(self.priority_queue)):
            v = self.priority_queue[i][0]
            self.priority_queue[i][1] = self.distances[v]

        size = len(self.priority_queue)
        startIdx = size//2 - 1
        for i in range(startIdx, -1, -1):
            self.min_heapify(self.priority_queue, size, i)

    def min_heapify(self, array, size, idx):
        l = 2 * idx + 1
        r = 2 * idx + 2
        min_idx = idx
        if l < size and array[l][1] < array[min_idx][1]:
            min_idx = l
        if r < size and array[r][1] < array[min_idx][1]:
            min_idx = r

        if idx != min_idx:
            array[idx], array[min_idx] = array[min_idx], array[idx]
            self.min_heapify(array, size, min_idx)

    def relax(self, u, v):
        if self.distances[v] == self.distances[u] == self.maxval:
            return

        w = self.weights[u][v]
        if self.distances[v] > self.distances[u] + w:
            self.distances[v] = self.distances[u] + w
            self.previous[v] = u

    def dijkstra_single_source(self, vertex):
        self.initialise_priority_queue(vertex)
        while(len(self.priority_queue) > 0):
            u = self.priority_queue[0][0]
            self.priority_queue = self.priority_queue[1:]
            if u in self.weights:
                for v in self.weights[u]:
                    self.relax(u, v)
            self.adjust_priority_queue()
        return True

    def dag_single_source(self, vertex):
        for k in self.tsorted:
            u = k.key
            if u in self.weights:
                for v in self.weights[u]:
                    self.relax(u, v)
        return True

    def bellman_ford_single_source(self, vertex):
        for i in range(self.len_vertices - 1):
            for edge in self.edges:
                u, v = edge
                self.relax(u, v)

        for edge in self.edges:
            u, v = edge
            if self.distances[v] == self.distances[u] == self.maxval:
                continue
            w = self.weights[u][v]
            if self.distances[v] > self.distances[u] + w:
                print(f"Graph Has A Negative Weight Cycle For Source: {vertex}, At Edge: {u}, {v}")
                return False
        return True
            
    def all_pairs(self):
        pass


if __name__ == "__main__":
    list_tests = [
        [ [0, 1, 2],  [0, 2, 2], [0, 3, 4], [1, 3, 1],  [2, 3, 1] ],
        [ [0, 1, -2], [0, 2, 2], [0, 3, 4], [1, 3, -1], [2, 3, 1] ],
        [ [0, 1, 10], [0, 4, 5], [1, 2, 1], [1, 4, 2],  [2, 3, 4], [3, 0, 7], [3, 2, 6], [4, 1, 3], [4, 2, 9], [4, 3, 2] ]
    ]

    matrix_tests = [
        [ [0, 2, 2, 4],     [2, 0, 0, 1],     [2, 0, 0, 1],     [0, 1, 0, 0] ],
        [ [0, -2, 2, 4],    [3, 0, 0, -1],    [2, 0, 0, 1],     [0, -1, 0, 0] ],
        [ [0, 6, 0, 0, 7],  [0, 0, 5, -4, 8], [0, -2, 0, 0, 0], [2, 0, 7, 0, 0], [0, 0, -3, 8, 0] ],
        [ [0, 6, 0, 0, 7],  [0, 0, 5, -4, 8], [0, -2, 0, 0, 0], [4, 0, 7, 0, 0], [0, 0, -3, 8, 0] ],
        [ [0, 10, 0, 0, 5], [0, 0, 1, 0, 2],  [0, 0, 0, 4, 0],  [7, 0, 6, 0, 0], [0, 3, 9, 2, 0] ]
    ]

    spath = ShortestPaths()
    for i in list_tests:
        graph = Graph(i)
        graph.print_graph()
        spath.reset(graph)
        spath.single_source(0)
        spath.reset(graph)
        spath.single_source(2)
        print("")

    for i in matrix_tests:
        graph = Graph(i)
        graph.print_graph()
        spath.reset(graph)
        spath.single_source(0)
        spath.reset(graph)
        spath.single_source(2)
        print("")
