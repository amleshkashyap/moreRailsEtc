## [Bochs](https://bochs.sourceforge.io/)
  * Intel x86 simulator
    - CPU
      - 386, 486, pentium
      - pentium 6 and ahead
      - x86-64 extensions
      - floating point units
    - Common I/O Devices
      - keyboard, mouse, VGA card/monitor, hard disk
      - PCI, USB, CD-ROM, sound card, network card, floppy disk
      - multiprocessors, parallel and serial ports, 3D video card, game port
    - BIOS, CMOS
    - Virtualization - no

  * Can run on different host platforms - x86, MIPS, Sun, Alpha
    - Due to complete hardware simulation, it's very slow
    - Commercial emulators (vmware) achieves higher speed with virtualization, but can't run on non-x86 (or whatever they were designed for)

  * Basics
    - Bochs interacts with the host OS regularly
    - For user input via keyboard, an event goes to device model for keyboard
    - For disk space in the simulator, a disk image file is present on the host machine
    - When simulator has an application that sends a network packet, Bochs uses host OS network card to send it outside
    - Eg, sending a network packet in FreeBSD has different code than Windows XP - hence, certain features are not supported on all host OS

## [QEMU](https://www.qemu.org/docs/master/system/index.html)
  * Machine and userspace emulator, virtualizer
    - Can emulate hardware without hardware virtualization - speed maybe better than bochs as it uses dynamic translation.
    - Can integrate with KVM/Xen hypervisors to provide emulated hardware, letting the hypervisor manage the CPU.
    - Can provide userspace API virtualization (linux/BSD kernels) - only CPU and syscall emulation

## Instruction Sets
  * Widely Used
    - x86 (CISC) - Family of instruction set from Intel's processors with 16, 32 and 64 bit variants
      - Intel 8086 - First 16 bit x86 implementation (1978)
      - Intel 80386 (i386/IA32) - First 32 bit x86 implementation (1985)
      - Intel Itanium (IA64) - First 64 bit x86 implementation (2001)
      - AMD Opteron (x86-64/AMD64/Intel 64) - First x86-64 implementation. x86-64 is the most widely used (2003)

    - MIPS (RISC) - Family of instruction set by MIPS technologies.
      - R2000 (MIPS I) - First processor by MIPS with 32 bit addressing (1986)
      - R4000 (MIPS III) - First processor with 64 bit addressing (1991)

    - ARM (RISC) - From ARM
      - ARM1 - First from ARM with 32 bit addressing (1985)
      - ARM Cortex-A57 - First from ARM with 64 bit addressing (2012)

## IA-32 And Intel 64
### Basic Execution Environment
  * Address Space
  * Basic program execution registers
  * x87 FPU registers
  * MMX registers
  * XMM registers
  * YMM registers
  * Bounds registers
  * BNDCFGU and BNDSTATUS
  * Stack
  * Descriptor table registers - local, global and interrupt descriptor table registers (LDTR, GDTR, IDTR) - holds 32/64 bit addresses

  * I/O ports
  * Control registers
  * Memory management registers
  * Debug registers
  * Memory type range registers (MTRR)
  * Model specific registers (MSR)
  * Machine check registers
  * Performance monitoring counters

  * Flat memory model
    - appears as a single, contiguous address space which holds code, data and stack.
    - linear address space (0 to 2^x - 1, x = [32,64]) - byte addressable
  * Segmented memory model -
    - to place code, data and stack in separate memory segments, with one component not growing too large
  * Real address memory model

  * Modes Of Operation
    - Protected mode - any address model can be used. This is the default mode.
    - Real address mode
    - System management mode - processor switches to a separate address space (system management RAM)
    - Compatibility mode
    - 64-bit mode

### Interrupts And Exceptions
  * Info for each exception/interrupt
    - Exception Class - Class can be fault, trap or abort. Some are fault or trap depending on when they're detected.
    - Description -
    - Exception Error Code - Whether an error code is saved for the exception.
    - Saved Instruction Pointer - Return instruction from interrupt.
    - Program State Change - Effect of the interrupt on the state of currently running thread/task

  * Interrupts
    - 0 (Divide Error Exception) - DIV, IDIV instructions
    - 1 (Debug Exception) - Code/data reference
    - 2 (NMI Interrupt) - Non maskable external interrupts
    - 3 (Breakpoint Exception) - INT3 instruction
    - 4 (Overflow Exception) - INTO instruction
    - 5 (Bound Range Exceeded Exception) - BOUND instruction
    - 6 (Invalid Opcode Exception) - UD instruction
    - 7 (Device Not Available Exception) - Floating point, WAIT/FWAIT instructions
    - 8 (Double Fault Exception) - Any instruction that can generate an exception + NMI + interrupts (INTR)
    - 9 (CoProcessor Segment Overrun) - Not available after i386
    - 10 (Invalid TSS Exception) - Task switch or TSS access
    - 11 (Segment Not Present) - Loading segment registers
    - 12 (Stack Fault Exception) - Stack operations, SS register loads
    - 13 (General Protection Exception) - Memory reference, protection checks
    - 14 (Page Fault Exception) - Memory reference
    - 16 (x87 Floating Point Error) - Floating point, WAIT/FWAIT instructions
    - 17 (Alignment Check Exception) - Data reference in memory
    - 18 (Machine Check Exception) - Error codes and source are model dependent
    - 19 (SIMD Floating Point Exception) - SIMD floating point instructions
    - 20 (Virtualization Exception) - EPT violations (if supported)
    - 21 (Control Protection Exception) - RET, IRET, RSTORSSP, SETSSBSY instructions
    - 32-255 (Maskable Interrupts, User Defined) - INTR pin, INT n instructions

  * Page Fault Exception
    - When paging is enabled (PG flag in CR0), processor detected one of the following while translation
      - Present flag (P) is set to 0 in the PDE/PTE
      - Procedure doesn't have sufficient privilege (eg, user mode procedure trying to access kernel mode page).
      - Code in user mode attempts to write a read only page. If WP flag is set in CR0, supervisor mode code writing to a read only page
        will also generate a page fault.
      - Instruction fetch to a vaddr that translates to a physical address in a memory page with execute disable bit being set.
      - One or more reserved bits in PDE/PTE is set to 1.
      - Shadow stack access is made to a page that is not a shadow stack page.

    - Exception Error Code On Stack (Bits)
      - 0 (P flag) - If the flag is 0, then translation didn't occur as the present bit was 0 in PDE/PTE.
      - 1 (W/R) - If the flag is 1, then the exception was caused due to a write operation.
      - 2 (U/S) - If the flag is 1, then the exception was caused due to an operation done in user mode.
      - 3 (RSVD flag) - If the flag is 1, then translation didn't occur as reserved bit was set in PDE/PTE.
      - 4 (I/D flag) - If the flag is 1, then the operation was an instruction fetch.
      - 5 (PK flag) - If the flag is 1, then operation was a data access to an address with a protection key, but protection key rights
          register didn't allow the access.
      - 6 (SS) - If the flag is 1, then the operation was a shadow stack access.
      - 7 (HLAT) -
      - 15 (SGX) - If the flag is 1, exception is unrelated to paging and resulted from SGX specific acess control requirements. This is set
        only if bit-0 is 1, and bit-3 and bit-5 are 0.

    - CR2 Register - It's loaded with the 32-bit address that caused the exception - it can be used to locate the PTE/PDE or any
      supplemental table entries to bring the page to memory from swap/filesystem. Another page fault can occur during execution of the
      page fault handler - handler must save the CR2 value before another page fault can occur. If page fault is caused by a page level
      protection violation, the "accessed" bit will still be set in PDE - whether it'll be set in PTE is model specific.

    - Saved Instruction Pointer
    - Program State Change - Usually, this doesn't happen during page fault because no instruction is executed (eg, even loading the
      instruction might've failed). After the page fault handler has corrected the violation (eg, by loading the missing page), execution
      of the program can resume.

    - A page fault can occur during a task switch for following reasons, which will lead to program state changes -
      - While writing the state of the original task into TSS of the task.
      - While reading GDT to locate TSS descriptor of new task.
      - While reading TSS of new task.
      - While reading segment descriptors of the segment selectors from the new task.
      - While reading the LDT of the new task to verify the segment registers stored in new TSS.
    - In the last 2 cases, page fault occurs in context of the new task, and EIP refers to the first instruction of the new task - If an OS
      allows for page faults during task switches, page fault handler should be called via task gate.
    - If page fault occurs during task switch, processor will load all information from new TSS (without performing any typical checks,
      like `limit`, `present`, `type`) before generating the exception - segment selectors won't have reliable information.

    - A page fault can occur during a stack switch as well.
      - Eg, a MOV instruction for stack switching with 16-bit registers (old software) can cause a page fault, general protection fault
        or alignment check fault after the segment selector has been loaded to SS, but before ESP is loaded - this leads to an inconsistent
        state with correct SS but old ESP.
      - Processor doesn't use the incosistent stack pointer if exception handler switches to a well defined stack, eg, when switching
        across privilege levels, or if the exception handler is a task (eg, thread with an esp). However, when stack switch is happening
        at the same privilege level and from the same task, processor will attempt to use inconsistent stack pointer.


### Privilege Levels
  * Protection Rings - Higher level means lower privilege.
    - 0 - Kernel
    - 1, 2 - OS Services (eg, device drivers)
    - 3 - User applications

  * Gate - Code modules in lower privilege segments can access modules in higher privilege segments via this tightly controlled and
    protected interface. Trying to access higher privilege segments Without going through a gate and without having sufficient access
    rights causes a General Protection Exception.
    - Accessing higher privilege segment has a mechanism similar to `Far CALL` operation, with some differences.
    - Segment selector provided in the CALL instruction references a call gate descriptor which provides -
      - Access right information
      - Segment selector for code segment of called procedure
      - Offset in the code segment (EIP)
    - Processor switches to a new stack to execute the called procedure - each privilege level has its own stack.
      - Segment selector and stack pointer for level 3 stack is stored in SS and ESP respectively.
      - When a call to a more privileged segment occurs, these are saved by the processor.
      - Segment selectors and stack pointers for levels 0, 1, 2 are saved in Task State Segment (TSS)

  * CALL operation between privilege levels - this is how a system call would also work (moving from level 3 to level 0) -
    - Perform a privilege check
    - Temporarily save contents of SS, ESP, CS and EIP (for the calling procedure)
    - Load the segment selector and stack pointer for new stack in a different privilege level from the TSS into SS/ESP, and switch to ESP.
    - Push the temporarily stored SS and ESP values of calling procedure to the new stack.
    - Copy params from caller stack to new stack - value from call gate descriptor tells the number of params to be copied.
    - Push the temporarily stored CS and EIP values to the new stack.
    - Do some operations if shadow stack is enabled.
    - Load the segment selector for new code segment and instruction pointer from call gate to CS and EIP.
    - Begin execution of called procedure at new privilege level.

  * RET operation between privilege levels
    - Perform a privilege check
    - Restore CS and EIP registers to values prior to the call.
    - Do some operations if shadow stack is enabled.
    - If RET has an optional n argument, increment stack pointer by number of bytes specified with n operand to release parameter from stack.
      If call gate descriptor specifies that one or more params be copied from one stack to another, RET n instruction must be used to
      release the params from both stacks (??). n operand gives the number of bytes occupied on each stack by the params. On return,
      processor increments ESP by n for each stack to move past these params on the stack (ie, make them disappear).
    - Restore SS and ESP registers to values prior to the call, switch back to the stack of the calling procedure.
    - If RET has an optional n argument, increment stack pointer by bytes specified by n as given above.
    - Resume execution of calling procedure.

  * CALL and RET operation for interrupt and exception handling procedures are similar to the above.

## uArch
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

### uArch Units, Implications, Known Practices
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
