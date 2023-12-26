## Shortest Paths In Graphs

### General
  * The shortest path s -> v can be given by [s, v1, v2, .., vk, v], where k >= 0
  * All vertices are unique, there are a total of k+2 vertices.
  * If a shortest path [v0, v1, .., vk] exists, then
    - All subpaths [vi, ..., vj] of the above are also shortest - for if they were not, then above won't be a shortest path because of
      shortest path just being a sum of all edge weights - if another subset of edges existed, they'd provide a smaller sum.
    - If s -> .. -> vk -> v is the shortest path from s to v, then s -> .. -> vk must be a shortest path from s to vk

  * Convergence Property - If s -> .. vk is a shortest path from s to vk, and s -> .. -> vk -> v is a shortest path from s to v, then
    the distance s -> .. -> vk -> v will not change after relax(vk, v) was called - ie, if the path turned out to be the shortest at the
    end of execution, then the path distance it holds would've remained the same after relax(vk, k).

  * Path Relaxation Property - If s -> .. -> vk -> v is a shortest path from s to v, then this must've happened after all the relaxations
    were performed on the intermediate edges - however, since it's the shortest path, no future relaxations would have any affect on it (it's
    similar to the convergence property).

### Bellman Ford Execution
  * In the first outer loop iteration, only the vertices which are adjacent to the source will have their distances updated from inf.
  * If source has no adjacent vertices, then none of the distances will be updated and one would waste power by running further.
  * Similarly, in the second loop iteration, all the edges that include the vertices adjacent to the source will be updated, and so on.
  * Hence, the outer loop should execute for a maximum of V times, where V is the number of vertices in the graph
    - In the worst case scenario, an edge e(w, x) will get a relevant distance when it's source w is reachable via another edge e1(v, w),
      which in turn is reachable via e2(u, v) and so on till the source.
    - Linked List with V nodes, with each node having one edge to next node and key with weight, is a good example of worst case scenario.
  * With the above, a quick optimisation visible is that of collecting the results of relax(u, v) for all edges, and terminating if all
    of them performed no-ops.
  * Runtime is O(VE)
