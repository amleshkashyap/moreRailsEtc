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

## Pintos
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

### General
  * Pintos code is a mix of C and assembly code. Assembly code is used at a few places only, and critical modules like loader and
    thread switcher are written in assembly.
  * Pintos registers a 8254 PIT based timer interrupt signal which seems to be the basis for round robin scheduling.

### Loading
  * [Code](https://pintos-os.org/cgi-bin/gitweb.cgi?p=pintos-anon;a=blob_plain;f=src/threads/loader.S;h=dd87ea1c794bc1759ceca654fc953eaea082d763;hb=HEAD)
  * PC BIOS loads the loader into memory - this is from the first sector of first hard disk (master boot record, MBR).
    - 64 bytes of MBR is reserved for partition table by convention
    - 128 bytes granted in pintos for kernel cmdline arguments
    - about 320 bytes left for loader code (512B sector) - written in assembly
  * Loader finds the kernel in the memory, loads it to memory and jumps to its start.
    - kernel code needn't be on the same disk or any specific location - hence loader finds it by reading the partition table of each HDD.
    - after finding the kernel in some partition, the contents are loaded in memory at physical address 128KB
    - entire partition might be large - kernel is at the beginning of the partition. Loader reads upto 512kB (pintos doesn't build kernels
      larger than 512kB).
    - PC BIOS doesn't provide any means to load kernels above 1MB - hence kernels should be small.
    - ELF header of the kernel contains a pointer to the entry point of kernel - loader extracts this and jumps to the pointed location.
      This is to transfer the control to the kernel.
  * Pintos kernel command line
    - Stored in the boot loader
    - user supplied commands (at boot time) are passed to the boot loader (modifying it) at every run, and these are passed to the kernel.

  * Low Level Kernel Init
    - [Code](https://pintos-os.org/cgi-bin/gitweb.cgi?p=pintos-anon;a=blob_plain;f=src/threads/start.S;h=29ffa7a42f3ed45a948befce9bceb9bd3c518ff5;hb=HEAD)

  * High Level Kernel Init


### Threads
  * Thread container should ideally be small (< 1kB) so it doesn't consume its own kernel stack space.
    - Kernel stack should also not grow too large else it can corrupt thread - kernel functions shouldn't allocate large structures/arrays
      as non-static local variables (instead use dynamic allocation).
    - Thread states - running, ready, blocked, dying
  * Thread stack - when thread is running, stack pointer is at the top and unused - when interrupted, all registers must be saved on the
    stack and pointer updated.
    - When interrupted, a frame (with register info) is pushed to the stack - for a user program, it's at the top of the page.
  * Init - A method starts the thread subsystem of pintos which creates the first thread - loader puts the initial thread's stack pointer at
    the top of the page (like a user thread). Initialization is performed very early.
  * Methods provided for thread creation, tick (for time slice consumption and monitoring), start, block, unblock, exit, etc.

  * Switching - thread blocking, exit and yield call the scheduler after disabling interrupts
    - [Code](https://pintos-os.org/cgi-bin/gitweb.cgi?p=pintos-anon;a=blob_plain;f=src/threads/switch.S;h=feca86cd16d02e3d6f31d1dde25cff379c0861a4;hb=HEAD)
    - Records current running thread, determines next thread to run, and perform switching
    - All threads that are not running are within a function1 which returns the new thread to be run and the thread that was put to sleep.
    - function1 saves the registers on stack, stores the CPUs current stack pointer to the stack pointer of the thread being put to sleep
      (so it can be restored in CPU as is later), then restores the stack pointer of the new thread to CPUs stack pointer, and restores the
      registers from the stack.
    - Marks the new thread as running - if the thread being put to sleep was in dying stage, then frees the pages it held - these operations
      can't be done before switching.

  * Running New Thread - A new thread is not part of function1 and has no stack pointers, etc - corner case.
    - At the time of thread creation, scheduler needs to be made aware of the presence of this thread (as it's not in the above function1).
    - Few stack frames are created to resolve this.
    - Topmost stack frame contains the return address which points to another function2.
    - Next stack frame contains function2 - this adjusts the stack pointer and calls the last part of the thread scheduler. Its stack frame
      is filled to point to another function3.
    - function3 enables interrupts and calls the actual function to be performed by the new thread.

### Synchronization
  * Disable Interrupts
    - Simplest way to disable race conditions - kernel thread preemption is performed using timer interrupts. This can happen any time
      and another thread can preempt the running kernel thread - Pintos is a preemptable kernel (usually, Unix kernels are not preemptable,
      and kernel threads can be preempted at points when they explicitly call the scheduler). User threads are always preemptable.
    - Main reason to disable interrupts is to synchronize kernel threads with external interrupts which shouldn't sleep (as given below)
      and hence, synchronisation primitives like locking are not usable within external interrupt handlers.
    - Some external interrupts (non-maskable interrupts, NMI) can't be postponed, even by disabling interrupts - not handled in Pintos.

  * Semaphore - A non-negative integer along with 2 atomic operations, Down (P, Acquire) which waits for the value to be positive and then
    decrements it, and Up (V, Release) which increments the value and wakes up any waiting threads.
    - If thread t1 wants to launch and wait for completion of t2, it can pass a semaphore with value 0 and Down it. When t2 finishes, it
      Ups the semaphore (value = 1, followed by reduction by t1 to 0 within Down operation). This kind of operation (ie, waiting for
      some event to finish) is not suitable for locks, because there's no one else to contend with.
    - If thread t1 wants to access a shared resource, then it can call the Down operation on a semaphore for the resource, which will
      become zero once it becomes 1, and when it's done with the resource, it'll Up it, making the value as 1. This is a lock.
    - Semaphores can be initialized with values > 1, but rarely used.
    - Threads which call the Down operation are actually going to wait till the value has become positive, and hence will run in some kind
      of infinite loop, wasting CPU cycles - similarly, an Up operation should ideally notify all waiting threads - a good OS will identify
      Down threads and put them to sleep - and also wake them up when Up is called. However, I've seen a practical situation in production
      with Ubuntu where a waiting thread was woken up very late and caused problems - it's not clear how much support is provided from
      compilers/interpreters to OS for determining such primitives and whether such OS level primitives can be directly accessed via the
      programming languages for better synchronisation implementation.
    - Up operation is maybe the only synchronisation primitive that is safe to use within external interrupt handlers. Each semaphore
      maintains a list of waiting threads, usually linked list based.

  * Locks - A semaphore initialized with value 1. Lock is different from semaphore in 1 way - only the thread that acquires the lock (Down)
    is allowed to release (Up) it. If a problem requires that different threads perform Up/Down operations, then it's a use case for
    semaphore, not locking. Also, locks are generally (definitely in Pintos) not recursive - it's an error for a thread to try to acquire
    a lock that it holds.

  * Monitors - Consists of data being synchronized, a lock and some conditional variables. A thread should first acquire a monitor lock
    post which it can read/write the data in question or wait for some condition to be satisfied before modifying the data and then
    releasing the monitor lock. Ex, a set of producer threads which are trying to add to a buffer and a set of consumer threads which
    are trying to read from it. If the buffer is full, producer thread can't write - it'll wait till some consumer has consumed something
    from the buffer. Similarly, a consumer thread has to wait till the buffer is empty.

  * Barriers - Barriers are statements that are added to prevent compilers from optimizing infinite loops added for implementing
    synchronisation primitives. Compilers can assume that a local variable (eg, semaphore) is not being changed by a thread and hence,
    infinite loops maybe removed, even though the variable is passed to another thread which can modify it. Optimisation barriers can be
    used to perform other kinds of synchronisation, eg, preventing reordering of statements by a compiler.
    - Compiler treats invocation of externally defined functions as a form of barrier - it assumes that such functions can access any
      statically/dynamically allocated data and any local variable whose address is already taken - explicit barriers omitted?
    - A function serving as a barrier should not be defined in the same file or included headers as the compiler would've parsed them
      already and deemed the barrier to be useless as well - it's not clear how PGO/FDO behave for such barriers.


### Interrupt Handling
  * [Code](https://pintos-os.org/cgi-bin/gitweb.cgi?p=pintos-anon;a=blob_plain;f=src/threads/intr-stubs.S;h=adb674e0f2e36755d95066e2156f53c2876d2ca4;hb=HEAD)
  * Most of the work done by OS relates to handling interrupts.
  * Internal interrupts - caused by CPU instructions, eg, system calls, page faults, divide by zero.
    - In pintos, they're synchronous. They can't be disabled
    - Three types are given in the manual - faults, traps, aborts. These are called exceptions.
    - Internal interrupts can be recursive, ie, while handling one, a page fault may occur
  * External interrupts - caused outside of CPU (CPU core), eg, system timer, keyboard, ports, disk, etc.
    - In pintos, these are asynchronous, and can be disabled.
    - Manual calls them interrupts, triggered by an I/O device.
  * When interrupt is encountered, CPU will save the state in stack and jump to interrupt handler - what does OS do?
    - OS maintain the IDT (interrupt descriptor table) - with information from CPU IDT
    - It pushes the registers not already pushed by the CPU to stack and calls interrupt handler.
  * Interrupt handling levels
    - ON - usual handling
    - dynamic disable - it can take some time during which more external interrupts can occur - relevant for page fault handling
    - OFF - no handling
  * User processes can invoke interrupts explicitly by setting a value - however, the process may still cause indirect interrupts like
    page faults irrespective of the value.
  * When handling internal interrupts, the data structure containing information about the interrupted process/thread is maintained and can
    be modified too - passed to the interrupt handler.
  * External interrupts can't be nested with another internal/external interrupt - and must disable the interrupt when one occurs.
    - External interrupts must not sleep or yield - multiple functions can't be called (eg, acquiring a lock) - sleeping in external
      interrupts will lead to the interrupted threads being put to sleep, and potentially cause deadlocks if a lock is being acquired
      during interrupt which was held by the interrupted thread.
    - These interrupts execute with all resources available exclusively to them, and hence should completely ASAP - for long running
      interrupts, it's useful to utilise the kernel threads (?) instead of CPU.
    - External interrupts are captured outside CPU via programmable interrupt controllers (PIC) - these modules are initialised along with
      IDT - at the completion of interrupts, PIC must be notified (what is the notification mechanism)?

### Memory Allocation
  * Typical page sizes - 512B to 8192B, usually 4096B (4kB).
  * Page Allocator - Allocates memory as pages, often one page at a time (can do more contiguous pages too). Usually maintains 2 pools
    of memory - kernel and user pool - latter for user processes, and by default, allocating half the memory it has to both the pools.
    - Each pool's usage is tracked using a bitmap with 1 bit per page.
    - A request for n pages searches the bitmap for n consecutive bits set to false - first fit strategy.
    - Requests for more than 1 page can lead to fragmentation - with worst cases like absence of 2 contiguous free pages when half full.

  * Block Allocator - can allocate blocks of any size. Uses 2 ways -
    - When requested size is < 1kB (fourth of page size), then the allocation is made from an existing page which is in use for allocating
      blocks of the particular size (blocks are rounded to max of 16 or nearest power of 2)
    - For > 1kB (and some overhead), size is rounded to nearest page size and allocated.
    - Some memory is wasted in both cases, and real operating systems focus on minimizing this wastage.
    - Most small requests do no require a call to page allocator - and calls to page allocator need more than 1 page can fail due to
      fragmentation.


### Virtual Addresses


### Page Table


### Hash Table
