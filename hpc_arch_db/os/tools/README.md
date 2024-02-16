## Arbitrary Memory Manipulation Using C
  * Unknown buffers - `void *`
  * Writing to a memory location - `memcpy (void * dest, const void *src, size_t n)`
    - If a pointer to src is available, then the address `&src` can be passed along with relevant size
    - This is useful for writing data directly to virtual memory pages (which are zeroed bytes of, say, 4kB).

  * Setting bytes to a contiguous memory location - `memset (void *str, int c, size_t n)`
  * Arbitrary data copying across data types - this can be used to perform arbitrary paddings.
    ```
    void *zz = malloc (sizeof (int));
    memset (zz, 0, sizeof (int));      // zero out the memory location - 0x00000000
    uint8_t one = 255;
    for (int i = 0; i < 4; i++) {
      memcpy (zz + i, &one, sizeof (uint8_t));    // set 1 byte per iteration - 0xff000000 -> 0xffff0000 -> 0xffffff00 -> 0xffffffff
      int val = *((int *) zz);
      printf("int value after: %d, %d, %x\n", i, val, val);
    }
    ```
  * Double Pointers - A pointer to another pointer stores the address of the first pointer -> this can be used to deal with storing
    addresses in a defined format so as to be able to fetch them later in a different context. This is used to setup the execution's
    stack pointer for passing the command line arguments (argc, argv).
    - Arbitrary copying example
    ```
      void *ptr = malloc (sizeof (char *));                  // data in heap
      memcpy (ptr, "one", sizeof (char *));
      printf("ptr at: %p, value is: %s\n", ptr, ptr);
      void *nptr = "two";                                    // data in stack
      printf("nptr at: %p, value is: %s\n", nptr, nptr);
      char **store = malloc (sizeof (char *));               // a double pointer to store the "value of address" in a pointer
      memcpy (store, &ptr, sizeof (char *));                 // store the "value of address" stored at ptr
      int address = *((int *) store);                        // get the above "value of address" from store
      printf("value: %s, address: %p\n", *store, address);   // value - one, address - from ptr
      memcpy (store, &nptr, sizeof (char *));
      address = *((int *) store);
      printf("value: %s, address: %p\n", *store, address);   // value - two, address - from nptr
    ```

## Pintos
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
    - Loader's last action is to transform control to kernel's entry point start () - it switches the CPU from 16-bit real mode to 32-bit
      protected mode.
    - It obtains the machine's memory size from the BIOS (which can detect upto 64MB RAM - max supported by pintos). It's stored as pages.
    - It then enables the A20 line, the 20th address line - which is fixed at 0, thus disabling any accesses to memory beyond 2^20 (1MB).
      Any OS that needs more memory has to enable it.
    - Loader creates a basic page table - which maps the 64MB at the base of virtual memory (starting at 0) to the identical physical
      addresses. It also maps the same physical memories starting at LOADER\_PHYS\_BASE (default 0xc0000000 - 3GB) - this is the only
      mapping required by Pintos, but it still needs to enable the former mapping. Pintos is at 0x20000, but wants to be at 0xc0020000 -
      it can't jump there without enabling it, and it can't enable it without jumping there (as it needs to be there).
    - After initialising page tables, CPUs control registers are loaded to turn on protected mode, and sets up segment registers. Interrupts
      are disabled. Then it calls main ().

  * High Level Kernel Init
    - Calls bss\_init - which clears kernel's BSS, a segment initialized to all zeroes. Any variable declared outside a function without
      being initialized (eg, static variables) resides in BSS - BSS is all zeroes, and there's no section in process image for it - memset
      is used to set it to all zeroes.
    - Then command line arguments are parsed. thread\_init () is called to initialize the thread system.
    - Kernel page allocator is initialized with palloc\_init (). Arbitrary memory block allocation is initialized via malloc\_init ().
      Page table for the kernel is setup via paging\_init (). tss\_init () and gdt\_init () are called to setup task segment and file
      descriptor table for allowing the execution of user program's.
    - intr\_init () sets up the IDT for interrupt handling - timer\_init () and kbd\_init () are used to setup timer and keyboard interrupts.
      input\_init () merges the serial and keyboard input in one stream. Handling interrupts from user programs is setup via
      exception\_init () and syscall\_init ().
    - thread\_start () is called to create the idle\_thread and enable interrupts. Serial port I/O via interrupts is initialized, and
      timer is caliberated for accurate short delays. IDE disks and filesystem is also initialized.
    - run\_actions () executes the action provided in the command line, which is used for running tests and user programs (via run\_test ()
      and process\_execute () - former is run as kernel threads). Main thread then calls thread\_exit () and lets others run.
    - Running the tests for first project always exit along with main thread as tests create kernel threads and operations are ordered in
      a way that main thread should be the last remaining non-idle thread - any bugs in the implementation leads to page faults.


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

### Schedulers
  * Scheduler Goals
    - Maximize throughput
    - Minimize wait time
    - Minimize latency or response time
    - Maximize fairness
    - Meeting deadlines (for real time systems)

  * Threads performing high IO require fast response times to keep the devices busy, but need little CPU time. CPU bound threads have the
    opposite requirement. Other threads have varying requirements.

  * Priority Scheduling
    - Highest priority threads are always picked up first.
    - If multiple threads have the same priority, perform round-robin scheduling among them.
    - This can lead to starvation, eg, if a high priority thread is waiting to acquire a lock held by a lower priority thread which was
      created earlier and had acquired the lock, then the low priority thread will never get a chance to run (it'll get a chance since
      the high priority thread will call sema\_down and move itself to blocked state.

  * Multilevel Feedback Queue Scheduler (from 4.4BSD)
    - Maintains multiple queues of ready to run threads, each queue with a different priority.
    - Scheduler chooses a thread from highest priority non-empty queue in round robin order.
    - Doesn't include priority donation.
    - Niceness - an integer value [-20, 20], where value > 0 means the thread is ready to sacrifice its CPU time to another thread with
      value < 0 (value 0 is neutral thread). Threads start with a nice value of zero, and child threads inherit the value from parent.
    - There are 64 queues for the 64 possible priority values in pintos (0-63).
    - Priority is calculated at initialisation and at every fourth clock tick (for every thread) using this formula
      ```
        priority = PRIORITY_MAX - (recent_cpu / 4) - (nice * 2)
        recent_cpu = (2 * load_avg) / (2 * load_avg + 1) * recent_cpu + nice
        load_avg = (59/60) * load_avg + (1/60) * ready_threads
      ```
    - Calculated priority is rounded to the nearest integer, and should lie in the range 0-63. Also, the used coefficients are not based on
      any insight, they work well empirically. Goal is to prevent starvation (and deadlocks without priority donation) - a starving thread
      will have a recent\_cpu value of 0, and will ideally receive a high enough priority at some point to be scheduled.
    - Fixed point computations are not supported in kernels as not all the hardware they'll run on will have a floating point unit, hence
      the thread switchers don't copy floating point registers as well.
    - In Pintos, priority is calculated every 4th timer tick for every thread, recent\_cpu is calculated every second for every thread and
      load\_avg is calculated every second (for the system). In addition, recent\_cpu is incremented by 1 for the running thread every timer
      tick. Nice can be updated manually for the running thread, and must lead to priority recalculation. Priority recalculations will lead
      to a thread being moved from one priority ready list to another priority ready list.

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

  * Task-State Segment (TSS) - Most x86 OSes ignore TSS.
    - For interrupts that occur in user mode, stack switching can only be done using TSS.
    - When interrupt occurs in user mode (ring 3), processor consults ss0 and esp0 members of the current TSS to determine the stack to use
      for handling the interrupt - at least these fields must be initialized and available to support interrupts in user mode.
    - When code interrupted by the interrupt handler is in the same ring as the interrupt handler, then it's kernel mode - TSS irrelevant.

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


### Page Table
  * Virtual Address
    - Bits 0-11 - It has the page offset which is directly used as the frame's offset
    - Bits 12-21 - 10 bits for page table index
    - Bits 22-31 - 10 bits for page directory index

  * Page Directory
    - This stores Page Directory Entries (PDE). Each PDE has the 20 bit physical address (MSB) of a page table and 12 bit flags (LSB).
    - First 10 bits of (1024 PDEs) of a virtual address are used to find the PDE - from the PDE, the base address of a page table is found.
    - Page directory maybe per thread/process - in pintos, every thread holds a pointer to a page directory.

  * Page Table
    - This stores Page Table Entries (PTE). Each PTE has the 20 bit physical base address (MSB) of the page and 12 bit flags (LSB).
    - Second 10 bits of the virtual address (1024 PTEs per page table) are used to find the PTE in that page table obtained from PDE.
    - There are 1024 page tables (or 1 contiguous page table segmented as 1024 entries of PDE), with 1024 addresses each - accounting for
      first 20 bits of the virtual address - 1024 * 1024 addresses with 4kB data storage starting at each address (4GB RAM).
    - Note that page directory can be created completely at bootup as it points to 1024 addresses which can also be fixed, ie, all 1024 page
      tables can also be initialized at their base address. However, PTEs need to be dynamic.
    - In pintos, page directory and tables are stored in the kernel space. It's mostly the same for linux. Ideally though, it appears that
      these tables should reside in non-pageable memory (else, PDE will also have to be dynamic - some non-pageable memory has to be used).

  * Numbers
    - Each page directory is 4kB (4 * 1024), and each page table is the same size.
    - If a process uses all memory available for it, it'll create 768 page tables + 1 page directory ~ 3 MB memory.
    - Each 4kB thread struct stores a pointer to a new page directory. Roughly 330 user threads can be created.

  * PTE Format
    - PTE contain 32-bit lines, where the 20 MSBs contain the physical base address. Remaining 12 bits (0-11) are given below.
    - PTE\_P (bit 0) - Present bit. When 0, an attempt to access the page leads to page fault.
    - PTE\_W (bit 1) - When 1, page is writable, when 0, writing leads to page fault.
    - PTE\_U (bit 2) - When 1, user process may access the page, when 0, only kernel can access, user access leads to page fault.
    - PTE\_A (bit 5) - Accessed bit
    - PTE\_D (bit 6) - Dirty bit
    - PTE\_AVL (bits 9-11) - Custom usage
    - PTE\ADDR (bits 12-32) - 20 bits of physical frame address.

  * Accessed And Dirty Bits
    - 80x86 hardware provides assistance for implementing page replacement algorithms using these 2 bits in the PTE.
    - At read/write to a page, accessed bit is set to 1 in PTE - at write, dirty bit is set to 1 in PTE - by the CPU. CPU doesn't reset them
      but the OS can.
    - Multiple pages may refer to the same frame (aliased frame) - when such a frame is accessed, these 2 bits are updated only in one of
      the PTEs (the one currently active), not the others.
      - In pintos, every virtual page is aliased to its kernel virtual page.
      - Eg, when multiple processes are created that use the same executable file - then read only pages maybe shared, thus creating alias
        frames (instead of maintaining copies of the process in memory).


## Executable And Linkable Format (ELF)
  * [Ref](https://refspecs.linuxfoundation.org/elf/elf.pdf)
  * Created by assembler and link editor (linker), to be transformed to a process image, to be executed directly on a processor.
    - Dynamic linker and interpreter will control the execution of programs during runtime (if required).
  * It is highly unlikely that anything will go wrong during object file and process image generation, program loading, dynamic linking and
    program execution, on established operating systems, programming languages and processor implementations - hence learning about them
    is almost irrelevant for developing most middlewares, application software, intelligent systems or even new operating systems.

  * Types
    - Relocatable - Holds code and data suitable for linking with other object files to create an executable or shared object file.
    - Executable - Program suitable for execution.
    - Shared Object - Holds code and data for linking - (1) Link editor may process it with other relocatable and shared object files to
      create another object file, (2) Dynamic linker can combine it with an executable file and other shared objects to create process image.

  * Executables are created from object files and libraries via linking
    - Linker resolves the references (including subroutines and data references) among object files, adjusts absolute references in
      object files, and relocates instructions.
    - Static Linking - Set of object files, system libraries and library archives are statically bound, references are resolved and a self
      contained executable file is created.
    - Dynamic Linking - This executable is not self contained - when this executable is loaded, other shared resources and dynamic
      libraries must be made available in the system.
    - Resolving references at execution for a dynamically linked executable is defined by the linkage model of OS, and contains processor
      specific components.

  * Examples

  ```
    Linking

     ----------------------
    | ELF Header           |
    |                      |
    | Program Header Table |
    | (optional)           |
    |                      |
    | Section 1            |
    | ...                  |
    | Section n            |
    | ...                  |
    | Section Header Table |
     ----------------------


    Execution

     ----------------------
    | ELF Header           |
    |                      |
    | Program Header Table |
    |                      |
    | Segment 1            |
    | ...                  |
    | Segment n            |
    | ...                  |
    | Section Header Table |
    | (optional)           |
     ----------------------
  ```

  * Sections
    - Contains all information about an object file except ELF header, program header table and section header table.
    - Every section has one section header describing it - section headers may exist without a section.
    - Each section occupies a contiguous sequence of bytes within the file.
    - Sections in a file may not overlap - no byte in a file resides in more than one section.
    - An object file may have inactive space, and all the tables combined might not cover every byte in an object file.
    - Reserved section table header indexes -
      - SHN\_UNDEF (0) - Undefined, missing or irrelevant section reference.
      - SHN\_LORESERVE (0xff00) - Lower bound of reserved indexes.
      - SHN\_LOPROC (0xff00) - Reserved for processor specific semantics (lower bound)
      - SHN\_HIPROC (0xff1f) - Same as above (upper bound)
      - SHN\_ABS (0xfff1) - Absolute values for the references - symbols are not affected by relocation.
      - SHN\_COMMON (0xfff2) - Common symbols, eg, FORTRAN COMMON, unallocated C external variables.
      - SHN\_HIRESERVE (0xffff) - Upper bound of reserved indexes. Section header table doesn't contain entries for the reserved indexes.

  * Executable (ELF) Header (Elf32\_Ehdr) - This is at the top of the object file and contains metadata about the file.
    - e\_ident - Initial bytes mark the file as an object file and provide machine independent data for decoding the contents of the file.
      There is a specification for this identification, table with values and details can be found in Ref.
    - e\_type - File type
      - ET\_NONE   (0)      - No file type
      - ET\_REL    (1)      - Relocatable file
      - ET\_EXEC   (2)      - Executable file
      - ET\_DYN    (3)      - Shared object file
      - ET\_CORE   (4)      - Core file
      - ET\_LOPROC (0xff00) - Processor specific
      - ET\_HIPROC (0xffff) - Processor specific
    - e\_machine - Specifies the required architecture for the file. Following are some examples -
      - ET\_NONE - No machine
      - EM\_386 - Intel
      - EM\_MIPS - MIPS RS3000 Big Endian
    - e\_version - Object file version. EV\_NONE (invalid), EV\_CURRENT (current).
    - e\_entry - Provides the virtual address to which system first transfers control. If no entry point, value is 0.
    - e\_phoff - Contains offset for program header table file in bytes. 0 if no PH.
    - e\_shoff - Contains offset for section header table file in bytes. 0 if no SH.
    - e\_flags - Processor specific flags.
    - e\_ehsize - Size of ELF header in bytes.
    - e\_phentsize - Size of each entry (all have same size) in the program header table.
    - e\_phnum - Number of entries in the program header table.
    - e\_shentsize - Size of each entry (all have same size) in the section header table.
    - e\_shnum - Number of entries in the section header table.
    - e\_shstrndx - Section header table index of the entry associated with the section name string table.

  * Program Header (Elf32\_Phdr) - Describes how to create a process image - files used to build a process image must have a program header
    table - relocatable files don't need one. Each header describes a segment, or other information needed by the system to prepare the
    program for execution. A "segment" contains one or more sections.
    - p\_type - Segment type.
      - PT\_NULL - Unused segment.
      - PT\_LOAD - A loadable segment with sizes p\_filesz and p\_memsz. Bytes from the file are mapped to the beginning of the memory
        segment - if p\_memsz is larger than p\_filesz, extra 0s are appended. File size shouldn't be larger than memory size. Loadable
        segment entries in the program header are present in ascending order by p\_vaddr.
      - PT\_DYNAMIC - Dynamic linking info
      - PT\_INTERP - Name of dynamic loader (String which provides the interpreter to be invoked).
      - PT\_NOTE - Auxiliary info (along with location and size)
      - PT\_SHLIB - Reserved segment type with unspecified semantics. In System V, a program that contains an array element of this type
        (in the program header) does not conform to the ELF specifications.
      - PT\_PHDR - Specifies the location and size of the program header table, in file and process image. If this is present, then
        it must precede any loadable segment entry. Also, it should not appear more than once
      - PT\_STACK - Stack segment
    - p\_offset - Offset for the first byte of the segment from the beginning of the object file.
    - p\_vaddr - Virtual address for the first byte of the segment in process image (process image goes to RAM).
    - p\_paddr - When physical addressing is relevant, this member provides that address (this is OS specific).
    - p\_filesz - Segment size in bytes (in the object file).
    - p\_memsz - Segment size in bytes (in the process image, ie, main memory).
    - p\_flags
      - PT\_X - Executable
      - PT\_W - Writable
      - PT\_R - Readable
    - p\_align - Value to which the segments are aligned in memory and in file. 0/1 mean no alignment is required. Else, the value should be
      an integral power of 2.
      - p\_vaddr ~ p\_offset % PGSIZE
      - p\_vaddr = p\_offset % p\_align

  * Note Section
    - Sometimes, an object file needs to be marked with special information for conformation, compatibility, etc. SHT\_NOTE and PT\_NOTE
      members can be used for such purposes.
    - namesz, name
    - descsz, desc
    - type

  * Section Header
    - sh\_name - An index for the section header string table -> at that index, name of the section is found
    - sh\_type - categorizes the section's content and semantics
      - SHT\_NULL (0) - Section header is marked as inactive, and no associated section is present.
      - SHT\_PROGBITS (1) - Section holds information defined by the program.
      - SHT\_SYMTAB (2), SHT\_DYNSYM (11) - Section contains a symbol table.
      - SHT\_STRTAB (3) - Section holds a string table.
      - SHT\_RELA (4) - Section holds relocation entries with explicit addends.
      - SHT\_HASH (5) - Section holds a symbol hash table.
      - SHT\_DYNAMIC (6) - Section holds information for dynamic linking.
      - SHT\_NOTE (7) - Section holds information about marking the file.
      - SHT\_NOBITS (8) - This section occupies no space in the file, but a conceptual offset value sh\_offset is present for process image.
      - SHT\_REL (9) - Section holds relocation entries without addends. Object files can have multiple relocation sections of either type.
      - SHT\_SHLIB (10) - Reserved with unspecified semantics.
      - SHT\_LOPROC (0x70000000) - Reserved for processor specific semantics.
      - SHT\_HIPROC (0x7fffffff) - Same as above
      - SHT\_LOUSER (0x80000000) - Specifies the lower bound of range of indexes reserved for application programs.
      - SHT\_HIUSER (0x8fffffff) - Specifies the upper bound of range of indexes reserved for application programs.
    - sh\_flags - 1-bit flag to support miscellaneous attributes
      - SHF\_WRITE - Section contains data that should be writable during process execution.
      - SHF\_ALLOC - Section occupies memory during process execution - however, not all sections are present in the process image.
      - SHF\_EXECINSTR - Section contains executable machine instructions.
      - SHF\_MASKPROC - Bits are reserved for processor specific semantics.
    - sh\_addr - If the section appears in the memory image of a process, then the address of its first byte is given by this member.
    - sh\_offset - Gives the byte offset from the beginning of the object file to the first byte of the section.
    - sh\_size - Size of section in bytes
    - sh\_link - Holds the section table header index link, whose meaning depends on the section type.
    - sh\_info - Extra information whose meaning depends on the section type.
    - sh\_addralign - section may hold a different datatype (eg, doubleword), hence the entire section needs to be aligned - the value is
      given by this member. 0/1 mean no alignment.
    - sh\_entsize - Some sections hold a table of fixed size entries (eg, symbol table). This member gives the size of each entry in bytes.
      If 0, then section doesn't contain a table of fixed size entries.

  * Special Sections
    - Some sections in ELF are predefined and hold program and control information.
    - .bss - Holds uninitialised data that contributes to the process image - system initializes the data with 0s. Also, it's of SHT\_NOBITS
      type, and holds no file space.
    - .comment - Includes version control information.
    - .data, .data1 - Section holds initialized data that is part of the process image.
    - .debug - Section holds information for symbolic debugging.
    - .dynamic - Section holds dynamic linking information, and has attributes like SHF\_ALLOC and SHF\_WRITE.
    - .hash - Holds symbol table hash.
    - .line - Holds line number information for symbolic debugging - connects source program and machine code.
    - .note -
    - .rodata, .rodata1 - Holds read only data that contributes to non-writable segment in the process image.
    - .shstrtab - Holds section names (string table).
    - .strtab - Holds string, mostly associated with symbol table entries. If the object file has a loadable segment that includes symbol
      string table, then this section will have SHF\_ALLOC attribute.
    - .symtab - Holds a symbol table. If the object file has a loadable segment that includes the symbol table, SHF\_ALLOC will be set.
    - .text - Holds the executable instructions of a program.

  * String Table
    - String tables hold strings, which are used by object file to represent symbol and section names.
    - First and last byte of the table consist of null character.
    - Examples
    ```
      idx     +0    +1    +2    +3    +4    +5    +6    +7    +8    +9
        0     \0    n     a     m     e     .     \0    v     a     r
       10     i     a     b     l     e     \0    a     b     l     e
       20     \0    \0    x     x     \0


      index      string
          0      none
          1      name.
          7      variable
         11      able
         16      able
         24      null
    ```

  * Symbol Table
    - Holds information needed to locate and relocate program's symbolic definition and references.
    - st\_name - Holds an index to the symbol string table
    - st\_value - Can be some value based on the context.
      - In relocatable files, it holds alignment constraints if the corresponding section is SHN\_COMMON
      - In executable and shared object files, st\_value holds the virtual address.
    - st\_size - Size of the symbol.
    - st\_info - Symbol's type and binding attributes.
    - st\_other - Ignore
    - st\_shndx - Holds the index of the section header table entry, as a symbol table entry should belong to one section.

  * Relocation
    - Connecting symbolic references to symbolic definitions.
    - Eg, when program calls a function, the "call" instruction must transfer control to the proper destination address at execution.
    - These files must have information that describes how to modify the section contents, helping create the correct process image.
    - struct Elf32\_Rel
      - r\_offset - Provides the location at which to apply the relocation action. For a relocatable file, the value is the byte offset
        from the beginning of the section to the storage unit affected by relocation. For executables/shared objects, value is the virtual
        address of the storage unit affected by the relocation.
      - r\_info - Provides the symbol table index wrt which the relocation must be made and the relocation type. Eg, "call" instructions
        relocation entry would hold the symbol table index of the function being called. If the index is STN\_UNDEF (undefined symbol index),
        relocation uses 0 as the symbol value. Relocation types are processor specific.
    - struct Elf32\_Rela
      - r\_offset
      - r\_info
      - r\_addend - A constant added used to compute the value to be stored in the relocatable field.
    - A relocation section references two other sections, symbol table, and section to modify. sh\_info and sh\_link from the section header
      table structure are used for these.

### Unix System V Specific
  * Special Sections
    - .dynstr - Section holds the strings for dynamic linking, mostly the ones that represent names associated with symbol table entries.
    - .dynsym - Holds the dynamic linking symbol table.
    - .fini - Holds executable instructions that contribute to process termination.
    - .init - Holds executable instructions that contribute to process initialisation - this is executed before calling the program entry.
    - .interp - Holds the path name of a program interpreter.
    - .relname, .relaname - Holds relocation information.

  * Symbol Table
    - Function symbols (STT\_FUNC) in shared object files - When another object file references a function from a shared object, link editor
      automatically creates a procedure linkage entry table for the referenced symbol. Shared objects with type other than STT\_FUNC are
      not automatically referenced via this procedure linkage table.
    - Global vs Weak Symbols
      - When combining several relocatable object files (via link editor), multiple definitions of STB\_GLOBAL symbols with same name are
        not allowed. Also, if a global symbol exists, then adding weak symbols with same name doesn't lead to errors (global definition is
        picked up, ignoring the weak symbols). Also, if a common symbol (st\_shndx = SHN\_COMMON) exists with a name, then adding weak
        symbols with same name is not an error, and they'll be ignored.
      - When link editor searches the archive libraries, it extracts archive members that contain the definitions of undefined global
        symbols - however, undefined weak symbols are unresolved and have value = 0.

  * Program Header
    - p\_paddr - This contains the physical address. Physical addressing is ignored for application programs, hence this member is not
      relevant for executables and shared objects.

  * Base Address
    - Virtual addresses in program headers need not be the actual virtual address in process image.
    - Since executables typically have the absolute code, segments must reside at the virtual addresses used to build the executable
      file (for correct process execution).
    - Also, shared object segments typically contain position independent code, which allows for segments virtual address to change across
      various processes without invalidating process execution behaviour.
    - Systems choose virtual addresses for processes, but for segments, relative positions are maintained. Since position independent code
      uses relative addressing between segments, the difference between virtual address in object file and process image must match for
      every segment.
    - For any one executable or shared object in a given process, the difference between the virtual address of a segment in memory and
      virtual address in the file (for that segment) is a constant value called base address.
    - Base address is used for relocating process image during dynamic linking.
    - For executables/shared objects, base address is calculated using during execution using - virtual memory load address, maximum page
      size, lowest virtual address of a program's loadable segment (lowest p\_vaddr value for a PT\_LOAD segment).
    - Example
    ```
      Source    |    Text     |     Data     |   Base Address
      -------------------------------------------------------
        File    |    0x200    |    0x2a400   |     0x0

      Process 1 |  0x80081200 |  0x800ab400  |   0x80081000

      Process 2 |  0x900c0200 |  0x900ea400  |   0x900c0000
    ```

  * Segments
    - Segment permissions are given by - 0 (none), 1 (ex only), 2 (wr only), 3 (wr, ex), 4 (rd only), 5 (rd, ex), 6 (rd, wr), 7 (rd, wr, ex)
    - Text segments contain read only instructions and data, and usually include the following sections.
    ```
       ---------
      |.text    |
      |---------|
      |.rodata  |
      |---------|
      |.hash    |
      |---------|
      |.dynsym  |
      |---------|
      |.dynstr  |
      |---------|
      |.plt     |
      |---------|
      |.rel.got |
       ---------
    ```
    - Data segments contain writable data and instructions, usually with these sections - .data, .dynamic, .got, .bss

  * Program Interpreter
    - An executable that participates in dynamic linking has a PT\_INTERP program header element. During execution, system retrieves a
      path name from the segment of this type, and creates a process image from the interpreter's file segment (not from the actual
      executables file segments) - then the control is passed to the interpreter to provide an environment for the application program.
    - Interpreter can receive control in 2 ways - (1) either a file descriptor to the executable file, which can be then used to read and
      map the executable file segments in memory, (2) system may load the executable file in the memory instead of providing a fd to the
      interpreter.
    - An interpreter maybe an executable or a shared object - (1) shared object (typical) - loaded as position independent, with addresses
      varying across processes. It'll usually not conflict with the original segment address of the original executable file, (2) executable,
      which is loaded at a fixed address - virtual addresses may collide and interpreter needs to resolve it.

  * Dynamic Linker
    - When building an executable file that needs dynamic linking, link editor adds a program header entry of type PT\_INTERP.
    - The dynamic linker, along with executable file, creates the process image
      - Adds memory segments of the executable file in the process image
      - Adding shared memory segments
      - Performing relocations for executable and its shared objects
      - Closing the fd that was used to read the executable file (if one was given)
      - Transferring control to program to make it appear as if the program was directly executed
    - Link editor also constructs other data that assist the dynamic linker - these data reside in loadable segments
      - .dynamic section (SHT\_DYNAMIC)
      - .hash section for symbol hash table
      - .got and .plt sections which hold 2 tables - global offset table (got) and procedure linkage table (plt). Former is used for
        position independent code, latter for functions (as given above).
    - Dynamic linker relocates the memory image and updates the absolute addresses (which differ from address in file) before giving the
      control to the process. Dynamic linker is permitted to evaluate PLT entries lazily, avoiding symbol resolution and relocation
      overhead for functions that are not called. If LD\_BIND\_NOW is set, all the relocations have to be done beforehand though.
    - Note: Lazy binding usually improves the overall application performance by skipping some linking overheads, but can be undesirable
      the following situations - (1) first reference to a shared object function takes longer than the subsequent references - some
      applications may find this intolerable, (2) if an error occurs and dynamic linker is unable to resolve the symbol, it will terminate
      the program - this can happen at arbitrary times and some applications may find it intolerable. When lazy binding is turned off,
      such failures occur at the process initialization.

  * Dynamic Section

  * Shared Object Dependencies
    - When link editor processes archive libraries, it extracts the library members and copies them to the object file. These are statically
      linked. Shared objects also provides these services which are attached to the process image.
    - When creating memory segments for process image, the dependencies (recorded in DT\_NEEDED) tell the shared objects required.
      Symbolic references are resolved via BFS, starting from the symbol table of the executable, followed by the symbol table of DT\_NEEDED
      entries at various depths, in order.

  * Global Offset Table
    - Holds abolute addresses for position independent addresses in private data. This table is essential for dynamic linking to work.

  * Procedure Linkage Table
    - Redirects position independent function calls to absolute addresses. Link editor can't resolve the execution transfers (eg, function
      calls) from one executable/shared object to another - these control transfer entries are present in PLT.

  * Hash Table
  * Initialization And Termination
    - Example
    ```

     -- NEEDED lists

      a.out -> b -> d -> e
          b -> d -> f
          d -> e -> g

     -- Dependency Graph

           a.out
         /   |   \
        b -> d -> e
        |    |
        f    g

     -- Orderings

      e -> g -> d -> f -> b -> a.out

      g -> f -> e -> d -> b -> a.out

    ```

  * Program Loading
    - When system creates/augments a process image, it copies a segment from the file to a virtual memory segment. When the system will
      physically read the file depends on the program execution behaviour, system load, etc. A process doesn't require a physical page unless
      unless it references a logical page during execution, and processes leave many pages unreferenced - hence delaying physical reads
      is an obvious choice for improving performance.
    - The executable and shared object files must have segment images whose file offsets and virtual addresses are congruent modulo the
      page size, in order to be able to achieve the above efficiency (ie, copy paste with no extra ops). For intel arch, virtual addresses
      are congruent modulo 4KB (0x1000) or large powers of 2.
    - In the below executable file example, file offsets and virtual addresses are congruent modulo 4KB for text and data. However, 4 file
      pages hold impure text/data -
      - First text page contains ELF header, program table header and other information.
      - Last text page holds a copy of the beginning of data.
      - First data page has a copy of the end of the text.
      - Last data page may contain file information not relevant to the running process.


  * Executable File Example
    ```
      Offset      File                  Virtual Address

            0  ----------------------
              |  ELF Header          |
              |----------------------|
              | Program Header Table |
              |----------------------|
              | Other Information    |
              |----------------------|
        0x100 | Text Segment         |  0x8048100 (134512896)
              |    ...               |
              | 0x2be00 B (179712)   |  0x8073eff (134692607)
              |----------------------|
      0x2bf00 | Data Segment         |  0x8074f00 (134696704)
              |    ...               |
              | 0x4e00 B (19968)     |  0x8079cff (134716671)
              |----------------------|
      0x30d00 | Other Information    |
               ----------------------
    ```

  * Process Image Segment Example
    ```
      Virtual Address           Contents        Segment

                        --------------------
            0x8048000  | Header Padding     |
                       | 0x100 B (256)      |
                       |--------------------|
            0x8048100  | Text Segment       |
                       |    ...             |   Text
                       | 0x2be00 B          |
                       |--------------------|
            0x8073f00  | Data Padding       |
                       | 0x100 B            |
                       |--------------------|
            0x8074000  | Text Padding       |
                       | 0x100 B            |
                       |--------------------|
            0x8074f00  | Data Segment       |
                       |    ...             |   Data
                       | 0x4e00 B           |
                       |--------------------|
            0x8079d00  | Uninitialized Data |
                       | 0x1024 B (4132)    |
                       |--------------------|
            0x807ad24  | Page Padding       |
                       | 0x2dc B (732)      |
                        --------------------
    ```

## System V Application Binary Interface
