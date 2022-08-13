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
