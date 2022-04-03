#### Summary
  * Basic Topics
    - Middleware DS
    - Difficult DB queries, which ones to take/avoid, query optimization, more DB topics
    - Basic architecture and HPC - performance, microarchitecture (uArch), shared and distributed memory parallelism

  * Others
    - Resources, snippets, software examples
    - Primarily - C++/Go/C

  * Trivia -
    - When in doubt, use brute force - KT
    - C++ enables zero-overhead abstractions to get us away from hardware without adding cost - BS


#### A Basic Lecture
  * Source - [Carl Cook](https://www.youtube.com/watch?v=NH1Tta7purM)
  * A compiler explorer exists which can help with comparing compilers - [godbolt](https://godbolt.org/)
  * OS/Compiler/CPU/Drivers/Libraries are obvious performance effectors - too many details to know already. But there's more -
    - CPUs are configurable - not everything exposed though
    - Ex - threading, CPU base speed, QoS [cache/bandwidth sharing]
  * Specifically for high performant systems -
    - One needs good wires and cables, needs to be as close to the sources of data as possible [2015 NSE scam]
    - As much as possible, hardcode things - or use configs - reduce abstractions and runtime resolutions.
    - May need to optimize the compilers and OS themselves.
    - [Stolen From](https://www.quora.com/C-C++-is-used-in-low-latency-systems-like-finance-for-its-speed-What-are-some-ways-expert-C++-developers-actually-get-this-speed-boost/answer/Eric-Lau-12)
  * [CRTP](https://en.wikipedia.org/wiki/Curiously_recurring_template_pattern)
  * RVO and NRVO -
  * More On Techniques -
    - delete involves no system calls
      - glibc free has 400 LOC
    - Reusing objects instead of freeing
      - Also avoids memory fragmentation
    - If delete is really important, try doing it from a different thread
    - Exceptions, when not thrown, are pretty much zero cost - use them
    - Avoid using exceptions for control flow - it's slow and code looks bad
    - Prefer templates to branches - avoid if
      - Replace if's by templates as much as possible
    - Branch predictors are expensive -
      - branch prediction is to reduce latency for majority of cases, at the cost of higher/typical latencies for minority of the cases.
      - but when we want to reduce latency for all cases [for a small part of the code], we don't want branch predictors - and thus, branches.
    - Multithreading should be avoided [vectorization is good though] -
      - synchronization is expensive.
      - some locks will still be required - if not at software level then at hardware level.
      - multithreading is much more useful to reduce the runtime when the runtime is huge - libs involved might have high overheads for low latency requirements.
    - Low latency programming really seems to be about -
      - accurate performance analysis
      - analyzing the runtime of various program snippets - a very large list [some known, many unknowns]
      - replacing slower snippets by functionally equivalent faster snippets


#### Middleware Topics
  * [Unix domain sockets](https://en.wikipedia.org/wiki/Unix_domain_socket)
  * [rapidjson](https://github.com/Tencent/rapidjson)


#### DB Arch and Queries
  * Indexing
  * Difficult Queries and Optimizations


#### uArch
  * Skylake
    - [SoC](https://en.wikichip.org/wiki/intel/microarchitectures/skylake_(client%29#Entire_SoC_Overview_.28quad.29)
    - [Core](https://en.wikichip.org/wiki/intel/microarchitectures/skylake_(client%29#Individual_Core)
      - [Details](https://en.wikichip.org/wiki/intel/microarchitectures/skylake_(client%29#Pipeline)
    - [Memory Hierarchy](https://en.wikichip.org/wiki/intel/microarchitectures/skylake_(client%29#Memory_Hierarchy)
  * Zen
    - [SoC](https://en.wikichip.org/wiki/amd/microarchitectures/zen#Entire_SoC_Overview)
      - [Numa Unit](https://en.wikichip.org/wiki/amd/microarchitectures/zen#CPU_Complex_.28CCX.29)
    - [Core](https://en.wikichip.org/wiki/amd/microarchitectures/zen#Individual_Core)
      - [Details](https://en.wikichip.org/wiki/amd/microarchitectures/zen#Pipeline)
    - [Memory Hierarchy](https://en.wikichip.org/wiki/amd/microarchitectures/zen#Memory_Hierarchy)

##### uArch Units, Implications, Known Practices
  * Branch Predictor
  * TLB
  * L1 Instruction and Data Caches
  * SMP
  * Decoder
  * Integer Unit
  * FP and SIMD Units
  * L2/L3 Caches
    - datatypes are typically 4B/8B, but we read 64B from cachelines so why not read an array always?
  * Prefetchers
  * DRAM, Beyond
  * Pre/Post Unit Queues/Buffers
  * Typical Latencies
