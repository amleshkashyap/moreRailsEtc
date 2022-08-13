### Generic Dumping Ground for the Infinite Things


#### Modern Usage of Algorithms -
  * Kubernetes Scheduler -
    - Filtering of nodes according to user specification
    - Scoring of matching nodes after the above filtering
    - Round robin scheduling for the highest scoring nodes
    - Limitations - scheduling is pod by pod, ie, each pod of every node is evaluated for scheduling.
    - Gang scheduling - related threads/processes to run in parallel on different processors - there might be dependencies among them as well.
      1. When 2 or more threads/processes are ready to communicate, then they'll be ready simultaneously.
      2. Ousterhouse matrix - rows are time slices and columns are processors - threads/processes for each job are in one row (distributed across processors).

#### Some Algorithms in Practice
  * Source - https://cstheory.stackexchange.com/questions/19759/core-algorithms-deployed/19773#19773
  * Linux - 
    - Linked List and variants
    - Priority sorted lists - 
    - Red-black trees - (a) scheduling, (b) virtual memory management, (c) track file descriptors, etc
    - Interval trees - 
    - Radix trees - memory management, file system lookups, networking functionalities, store pointers to struct pages
    - Priority heaps - cgroups (isolates a group of processes)
    - Hash functions
    - Hash tables - inodes, file system integrity checks
    - Bit arrays - flags, interrupts, etc
    - Semaphores
    - Binary search - interrupt handling, register cache lookup
    - Binary search using B-Trees
    - DFS - directory configuration
    - BFS - locking correctness at runtime??
    - Merge sort - garbage collection, file system management
    - Bubble sort
    - Knuth Morris Pratt string matching - ??
    - Boyer Moore pattern matching - ??

  * Chromium Web Browser -
    - Splay trees
    - Bresenham's algorithm
    - Binary trees
    - Red black trees
    - AVL trees
    - Rabin-Karp string matching - compression (of what?)
    - Suffixes of automaton - 
    - Bloom Filter - 

  * Allocation/Scheduling Algorithms -
    - LRU, FIFO, Round Robin
    - Clock Algorithm - page frame replacement
    - Buddy Memory Allocation Algorithm - 

  * Tools -
    - Thompson-McNaughton-Yamada construction of NFA's from RE - grep, awk
    - Topological Sort - tsort
    - Aho-Corasick string matching algorithm - fgrep
    - Boyer Moore algorithm - GNU grep
    - Dynamic Programming Algo for Levenshtein distance - diff
    - LALR parsing - yacc, bison
    - Gestalt Pattern Matching - difflib [python]
    - 
