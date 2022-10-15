### Generic Dumping Ground for the Infinite Things

#### Distributed Computing Concepts [Needs Cleanup]

##### Problems with local and global clocks -
  * Source - https://martinfowler.com/articles/patterns-of-distributed-systems/time-bound-lease.html#wall-clock-not-monotonic
  * Computers have 2 mechanisms to represent time -
    - Wall clock time - measured using a crystal oscillator [a mechanical system with potential to go wrong]. If crystals oscillate fast or slow, then the wall clock time can go ahead/behind the
      actual time. To handle this, machines have a NTP server to sync times with well known internet sources - this can lead to incorrect wall clock timestamps [after the sync] and is not usually
      used by languages/libraries.
    - Monotonic clock - these are guaranteed to preserve the order, as it's an internal mechanism [probably using some counter] which always moves forward. This, along with the wall clock time,
      can be utilized to achieve ordered timestamp values [values might not be accurate but ordering of values will be]. Languages have APIs to fetch both monotonic and wall clock times.
  * However, above can't be used to assert the accurate ordering of timestamps across servers - as discussed above, since timestamp values can be approximations within a server, there's no way
    to order the timestamps with 100% accuracy across servers. This creates a need for having a global clock for distributed systems to achieve total ordering, if required.

##### Consistency Models
  * Source - https://jepsen.io/consistency

  * Concepts
    - System - A distributed system is a concurrent system and most of the techniques used are similar to those used for single node concurrent systems.
    - Process - Programs which are 'logically single threaded' (eg, an API call).
      - Emphasis on synchronity, or, sequential order of operations.
      - The whole set of operations performed by a usual OS process or even thread need not be synchronous.
      - On the other hand, multiple processes spread across multiple systems might be performing operations in an ordered fashion.
      - Note that most of the consistency models will usually define themselves [and appear logically correct] wrt an object (defined below), but in distributed systems, there are multiple objects
        which are being acted upon by multiple processes, often operating concurrently. An implementer need not have the strongest consistency model for their system [high complexity], depending on
        the workload (processes) they expect and data that they handle - and may decide to implement weaker models [which would often be faster with lower complexity].
    - Operations - A transition from one state to another. Also used interchangeably with transactions.
      - Function performed, arguments accepted and results returned - eg, sub-operation.
      - Invocation and completion times
      - Concurrency
      - Crashes - any kind of failure in completing the operation.
    - Object - Entities in the system which suffer reads and writes, eg, global variables, tables, databases, caches.
      - An operation belongs to a process and can include multiple objects.
      - However, same objects can be part of the operations of another process - this is where consistency comes into picture.
    - Histories - Collection of operations. Operations can be ordered based on their invocation and completion times, which will also capture any concurrency.
    - Consistency models - A set of histories.
      - A set of histories can be good, ie, satisfy all the requirements of an observer (eg, an organizations SLA).
      - The same set of histories above can be bad from the perspective of another observer or even to the common sense.
      - Consistency models need not follow a hierarcy always, eg, a linearizable model is always sequential, but might not be related to another model.

  * A Hierarchy (representing strong/weak consistency)
    - Strict Serializable - Multi-object (system-wide). Implies that operations appear to have occurred in some order, consistent with the real time ordering of those operations.
      It implies serializability and linearizability. Its the serializability's total order of transactional multi-object operations plus linearizability's real time constraint.
      Eg, a strictly serializable database is an linearlizable object in which the object's state is the entire database [and not just one/more tables].
      - Serializable - Multi-object (system-wide). Operations appears to have occurred in a total order [atomic]. Eg, if a process A completes a write w, and another process B begins a read r, then
        serializability doesn't guarantee that r is from w. Even though system wide, it can lead to incorrect orderings because it doesn't guarantee any adherence to the real time ordering of
        operations - so 2 processes can still have incorrect values in their sub-operations.
        - Repeatable Read
          - Cursor Stability
            - Read Committed
            - Read Uncommitted
          - Monotonic Atomic View
            - Read Committed
            - Read Uncommited
        - Snapshot Isolation
          - Monotonic Atomic View
            - Read Committed
            - Read Uncommitted

      - Linearizable - Single object. Implies that every operation appears to have taken place atomically in some order, consistent with the real time ordering of those operations.
        However, scope for an object varies - eg, linearizability can be provided on individual keys in a key-value store, or on multiple keys, or in multiple tables in a database but not
        between different databases, leading to incorrect reads. This is still a very strong model, and probably better than serializability.
        - Sequential - Single object. Implies that operations appear to take place in some total order, which is consistent with the order of operations on individual process. In a distributed system,
          2 processes might be far ahead/behind of each other [which would be great, they would've probably completed in order] - but may be closer, in which case they might be updating shared
          objects and reading stale values - although their orders will be preserved, ie, if a process A has seen some state change by a process B, then it will never observe a state prior to B.
          - Causal
            - Writes Follow Reads
            - PRAM (Pipeline Random Access Memory) - Attempts to achieve better concurrency/performance. Any pair of writes executed by a single process are observed (by every other process) in the
              order that the process executed them - but writes from different processes maybe observed in different orders.
              - Monotonic Reads
              - Monotonic Writes - If a process performs write w1 and then w2, then all processes observe w1 before w2 - however, this doesn't guarantee that the values will be like that as some
                other process might've changed it - but the operational sequence is guaranteed.
              - Read Your Writes

##### More Concepts
  * Client, Server - Server consists of a leader and its followers (internally, can be one or many clusters). Client is the one making requests to the server.

  * Effects Of Serializability And Linearizability
    - Serializability guarantees preservance of order across all objects of the system, but data might be stale in case an older process is still to be executed [ie, a command from leader to
      followers]. But if clients can live with older data for sometime, then serializability is sufficient.
    - Linearizability guarantees that client will receive the most recent value - important for operations like leases.
    - Partitioning in Kafka - Each partition in Kafka has one server that plays the role of a leader, while there can be none or more servers that act as followers. Leader performs the task of all
      read and write request, while the followers passively replicate the leader.
    - If leader is partitioned from the rest of the cluster (ie, followers), clients can get stale data from leader.
    - When followers are partitioned, then they might send stale data to the client - they need to query the leader and receive the latest value before updating the client.

  * Versioned Value
    - Nodes in a distributed system need to know which value for a key is the most recent, as well as know the previous values to rollback operations if required. Also for debugging.
    - Most DBs often have the capability to store a version number at every update to a record - version number increments at every update.
    - This also helps with allowing reading a value when a write lock has been obtained - correct values can be read later
    - Ordering of versioned keys should be simple enough to be able to quickly navigate to a particular version [apparently, an important operation, eg, rollbacks].
    - Multiversion Concurrency Control - This leads to reduced locking problems in DB. MySQL with InnoDB implements MVCC.
    - Databases use Versioned Value to implement MVCC and transaction isolation -
      - When there are multiple requests accessing the same data, locking is used to block other processes when one is writing.
      - With Versioned Value, every write request adds a new record, and requests can be non-blocking [can lead to stale reads].
    - Locks -
      - Shared - Multiple holders possible. Record can't change till all holders have released the lock. Exclusive lock can't be obtained if shared lock has been obtained.
      - Exclusive - Only one holder at a time. Record can change. There can be a situation in automated DB writes where a series of writes are fired on a list of records by two different
        processes, and both are done from within a transaction - then a zig-zag kind of pattern of obtaining locks can be encountered and can lead to unexpected situations.
        - These should be held for the shortest possible time.
        - Don't hold the lock across system or function calls where the entity no longer runs on the processor - it can cause a deadlock.
        - If entity exits unexpectedly, lock must be freed - else deadlock.
      - Concept of locks come in handy while discussing leases.

  * Consistent Core
    - A large system [eg, a k8s cluster with multiple pods] often has some common requirements -
      - Selecting a master server for a specific task [leader].
      - Managing group membership information.
      - Mapping of data partitions.
    - This needs -
      - A strong guarantee of consistency - linearizability
      - Fault tolerance
    - Quorum based approach can be used but its througput degrades with increasing number of nodes.
    - Consistent core is an approach to provide strong consistency for large clusters without implementing quorum based algorithms.
      - It proposes using a smaller cluster dedicated to maintain consistency and be fault tolerant [quorum based], while the actual cluster can keep growing in size.
      - This can be a 3-5 node cluster which provides linearizability along with fault tolerance.
      - It can be used for maintaining metadata and taking cluster wise decisions like lease for the larger cluster.
    - Metadata Storage - Using consensus algorithms, eg, raft (add details).
      - Store group membership, task distribution across servers. Servers can register themselves via Consistent Core and clients can see this list of servers.
    - Handling Clients -
      - Finding the leader
      - Handling duplicate requests - previously, a client made a request which the leader completed, but then crashed before returning the response. In that case, when client sends the request
        again, the request shouldn't be redone by the new leader.

  * Lease [eg, time to live]
    - Multiple server nodes need exclusive access to certain resources, and during that, they can become unavailable due to an unexpected crash or an operational halt. However, this shouldn't
      lead to cutting off the access to those resources for other nodes.
    - To handle the above, a node must ask for a lease to the resource for a finite [and small] amount of time - the node may request to extend the lease if needed.
    - The lease can be handled in Consistent Core - leader and followers should replicate the lease for fault tolerance.
    - The cluster node owning the lease should periodically refresh it.
    - Leader tracks the timeouts of leases [even though followers also hold the leases - this is the Consistent Core].


##### Distributed Algorithms
  * Lamport's Clock
    - Source - https://martinfowler.com/articles/patterns-of-distributed-systems/lamport-clock.html
    - Partially Ordered Sets - (P, <=, <) - A poset consists of a set P and a binary relation (eg, <= for non-strict, and < for strict) such that for certain pair of elements in the set, one
      element precedes the other in the ordering. Not every pair of elements need to be comparable though - if they were, it would be a Totally Ordered Set.
    - The problem is of determining the order of multiple events accurately. The problem is relevant only for multiple servers as timestamp is sufficient for total ordering on a single server.
    - Lamport's Clock provides a partial order for any system by providing ordering between interacting events (-> represents happened before) -
      - It provides a one way relationship for events A and B with logical timestamps T(A) and T(B) => if A -> B, then T(A) < T(B) - this is called clock consistency condition.
      - The strong clock consistency condition says the above as well as => if T(A) < T(B), then A -> B [two way].
      - One can also say this - T(A) < T(B) implies that A may've happened before B or maybe incomparable to B, but didn't happen after B.
      - It can be used to create a total ordering of the system - ties can be broken using process IDs or some arbitrary methods. However, it will not imply causal relation between events.
      - Lamport's clock only shows non-causality - if A -> C and B -> C, then C did not cause A and B, the cause for C can't be determined.
      - In message passing scenario, a send must've happened before the receive.
    - See lamport\_clock.py.

  * Vector Clock

  * Election Algorithm


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
