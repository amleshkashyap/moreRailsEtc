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
