## Containers
  * For providing efficient implementations, usually self balancing tree is the underlying data structure - however, pretty much no
    programming language provides a tree data structure natively - in the real world, application of trees can be very custom and hence,
    best to implement by hand.

### Single Value Containers
  * [C++](https://cplusplus.com/reference/stl/)
    - array - fixed size arrays
    - vector - dynamic arrays
    - deque - double ended queue
    - queue - single ended queue
    - list - doubly linked list
    - slist - singly linked list
    - stack

  * [Python](https://docs.python.org/3/library/index.html)
    - list
    - heapq - binary heaps
    - tuple
    - bytes - immutable array of bytes
    - bytearray - mutable array of bytes
    - str - immutable array of unicodes
    - collections.deque
    - queue.Queue - multithread access with locking
    - queue.LifoQueue
    - multiprocessing.Queue - multiprocess access with locking
    - queue.PriorityQueue

  * [Ruby](https://ruby-doc.org/3.2.2/)
    - Array
    - Vector and Matrix
    - Range

  * [NodeJS](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects)
    - Array (they've many more types of array)

  * [Golang](https://pkg.go.dev/std)
    - array
    - list - doubly linked list
    - heap
    - ring - circular linked list

### Associative Containers
  * C++
    - map
    - unordered\_map
    - set
    - unordered\_set
    - multiset - usually implemented [as BST](https://cplusplus.com/reference/set/multiset/)

  * Python -
    - dict
    - collections.defaultdict - returns default values for missing keys
    - collections.OrderedDict - preserves the insertion order of keys
    - set
    - frozenset
    - collections.Counter

  * Ruby
    - Hash
    - Set

  * NodeJS
    - Map
    - Set

  * Golang
    - map
