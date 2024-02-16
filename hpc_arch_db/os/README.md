### Some OS Topics

#### Trivia
  * There are no easy error returns in an operating system. There is a need to recover, clean up the mess, and continue working. That is not an easy problem to solve. Applications, on the other
    hand, can abort, give up, and leave the mess to the OS to clean up. [Someone On Quora]

  * If you want to run exactly one program on one processor core using one console mode, one simple filesystem and one simple ethernet network stack, you’re looking at a project well within the reach
    of <most students spending quite sometime> — assuming you leverage UEFI. Without UEFI, you’re looking at something <fewer students spending more time>.
    The complexity comes in when you want to start relaxing those restrictions. If you download the linux source you’ll see most of the code is device drivers: dozens (or hundreds) of graphics cards,
    network cards, exotic communication hardware, hard drives, etc. Each of these can have their own documented (or undocumented) communication protocols, error messages, initialization routines, etc.
    Next, there are huge piles of code dedicated to making shared-memory parallelism work. Want to run more than one program at a time? (Why would you ever want to do that?) Well, how do they play
    nice with each other? How do you manage to interrupt a running program, save off necessary state, then transfer control to a different program in a manner that appears seamless to the user?
    And once you’ve gotten things tottering along for several mixes of hardware and software, you now need to be able to manage the flood of new devices that arrive week in and week out without
    breaking backwards compatibility for your 1985 version of Tetris. For simple, straightforward, documented hardware, any individual component isn’t that difficult. Getting ten thousand of those
    components to play well with each other is a corporate-sized undertaking. [Someone On Quora]

#### Basics
  * Find process tree (and tree for one pid) - `pstree -p` (`pstree -s -p <pid>`)
  * Find the information stored by OS for a process - `/proc/<pid>/`
    - Ex. environment variables being utilized by a process can be inspected in `/proc/<pid>/environ`
  * Find the logs for init processes - `/var/log/<process>`
    - Logs for upstart processes - `/var/log/upstart/<process>`
  * Bash - An `sh` compatible language interpreter which can read from the standard input or from a file.
    - Login shell - (a) first character of argument zero is `-`, (b) started with `--login` option.
    - Interactive shell - (a) started without non-option arguments and without `-c` option (and standard input/error are connected to the terminal), (b) started with `-i` option.
    - When bash is invoked as an interactive login shell, or as non-interactive shell with `--login`, it -
      - reads and executes commands from the file `/etc/profile` (if it exists)
      - looks for `~/.bash_profile`, `~/.bash_login` and `~/.profile` - reads and executes the commands in the first file that was found and is readable.
      - above behaviour can be inhibited using `--noprofile`.
      - when exiting the login shell, it reads and executes commands from `~/.bash_logout` and `/etc/bash.bash_logout` (if they exist).
    - When bash is invoked as an interactive, non-login shell -
      - reads and executes commands from `~/.bashrc`, if it exists.
      - above can be inhibited using `--norc`
      - above can be overridden using `--rcfile <file>` wherein bash will read from <file> instead.
    - When bash is started non-interactively (eg, to run a shell script), it looks for `BASH_ENV` env var, reads it value (if exists), and uses that value as the filename to be read and executed.
    <br/>
    - When bash is invoked by the name sh, it tries to mimic the startup behaviour of sh (while conforming to POSIX standards).
      - When invoked as interactive login shell, or non-interactive shell with `--login`, it attempts to read and execute from `/etc/profile` and `~/.profile` (note the differences from above). This
        behavior can be inhibited using `--noprofile` option.
      - When invoked as an interactive shell, it looks for the value in `ENV` env var, and uses that as the filename to be read and executed.
      - Any shell invoked with as sh doesn't attempt to read and execute from any files other than the above, hence, `--rcfile` doesn't work with bash as sh as well.
      - When invoked as a non-interactive shell, it doesn't attempt to read any startup files.
      - After any startup files to be read are read, bash enters POSIX mode.
    <br/>
    - When bash is started in POSIX mode (`--posix` option), it follows POSIX standard for startup files.
      - When started as an interactive shell, it reads the `ENV` env var, and uses the value as the startup filename.
      - No other startup files are read.
    <br/>
    - bash will attempt to determine whether its being run with its standard input connected to a network connection - usually `rshd` (remote shell) or `sshd` (secure shell).
      - If it determines that its being run like this, then it'll read and execute from `~/.bashrc` - however, it won't be done if bash is run as sh.
      - This behaviour can be inhibited using `--norc` or overridden using `--rcfile` (but usually, `rshd` won't allow these options to be specified or doesn't specify them while invocation).
    <br/>
    - When shell is started wherein the effective user id is not equal to the real user id, and `-p` isn't supplied -
      - no startup files are read
      - shell functions aren't inherited from the environment - what are these functions?
      - `SHELLOPTS`, `BASHOPTS`, `CDPATH` and `GLOBIGNORE` variables are ignored (if they're present in the environment)
      - effective user id is set to the real user id.
      - When `-p` option is supplied, then user id reset doesn't happen (ie, above), rest of it happens as above.
    - [Official Doc](https://linux.die.net/man/1/bash)

  * ssh -
    - An interesting note about ssh is its ability to create bidirectional channels which can be helpful for parallel operations on a remote machine, ie, invoke some command and get the results
      back to local in batches - [source](https://levelup.gitconnected.com/how-to-take-backup-of-a-database-through-ssh-tunneling-451a6cccecda).

  * systemd -

## Linux Commands
  * [Official Doc](https://linux.die.net/man/)
  * User Commands and Tools - file manipulation, compilers, browsers, file/image viewers/editors, etc.
    - These yield a status value at termination (`$?` contains the result of last executed command in most shells - 0 is success, fail can be from 1-255, values can indicate reasons).
    - Most commands we use belong to this category, types being - path/file/directory ops, disk ops, process ops, etc.
    - Shell examples - ash, chsh, csh, zsh, bash, sh

  * System Calls - entry point to the linux kernel, usually invoked via wrappers written in C (which also do other operations required to invoke a system call, eg, trap to kernel mode).
    - System calls will usually return 0 on success, but some don't. Errors are usually negative numbers, but C always return -1, with actual value put into `errno`.
    - Sometimes, system calls need to be invoked directly (when C doesn't have a wrapper for it).
    - Sometims, a test macro is required to be specified in order to get the declaration of a system call from the header file.

  * Library Functions - most are part of Standard C library (`libc`), some are from others (eg, math `libm`, real time `librt`).

  * Special Files - eg, devices

  * File Formats -

  * Games -

  * Conventions and Miscellaneous - eg, character set standard, file system layout, conventions and protocols, etc.

  * Administration and Privilege Commands - only usable by superuser, eg, system admin commands, daemons, hardware related commands, etc. These also return an exit status like normal user commands.
    - There are at least 3500 such commands, trying to list out the broad categories.
    - Daemons (250+) -
      - zfs filesystem daemon
      - zabbix daemons - agent, proxy and server
      - yum update notifier
      - NIS password update (yppasswdd, rpc.yppasswd)
      - extended root, extended network services
      - cluster namespace
      - layer 2 tunnelling protocol
      - name service switch for resolving names from NT servers
      - software watchdog, simplified software watchdog and watchdog multiplexing
      - wireless access point roaming for WLAN
      - vtun daemons - 
      - very secure FTP
      - virtual power control
      - uucp execution, uucp file transfer
      - uuid generation
      - event managing daemons - udevd, udevsend and udevcontrol
      - udisks
      - tyrion
      - dynamic adaptive system tuning
      - postfix address rewriting/resolving
      - userspace bandwidth manager
      - tinc VPN
      - lightweight HTTP proxy
      - mac time server
      - trusted computing resources
      - swift daemons - swift-proxy-server, object server, object replicator, object auditor, container info updator, list container contents, replicate containers, container auditor,
        swift-auth-server, account data server, replicate accounts, remove data of deleted accounts, account auditor - swift is a programming language for Apple products.
      - server side rpcsec_gss (svcgssd, rpc.svcgssd), rpcsec_gss (gssd, rpc.gssd)
      - init daemon control tools - start, stop, status
      - NSM service (statd, rpc.statd)
      - system security services
      - openssh
      - SRCP speaking
      - responder to SNMP request packets
      - sendmail socket map
      - SMART disk monitoring
      - LDAP daemons - standalone, standalone update replication
      - shinken daemons - scheduler, receiver, poller, reactionner, arbiter, broker
      - sun grid engine daemons - master control, shadow master
      - setroubleshoot
      - serial communications
      - sensor info logging
      - scan files for scannedonly samba
      - SANE network
      - reverse name resolution for iptraf
      - security enhanced policy for rtkit_daemon processes
      - NFS mount (mountd, rpc.mountd)
      - 

## Linux Kernel
  * [Official Doc](https://docs.kernel.org/)
  * It is highly unlikely that anything will go wrong within an established operating system, hence learning about them is almost irrelevant
    for developing any middlewares, application softwares and intelligent systems.

### Scheduling Basics
  * [Ref](https://man7.org/linux/man-pages/man7/sched.7.html)

  * Scheduler decides which runnable thread will be executed next.
    - Each thread has a static priority and a scheduling policy which are used to decide about scheduling.
    - Real time policies lead to a priority value in the range of 1-99 (for normal policies, it's 0) - however, POSIX standard requires that
      a minimum 32 distinct priorities be supported, which is what is implemented in most systems.
    - All scheduling is preemptive - if a thread with higher static priority becomes ready to run, current thread should be preempted.

  * SCHED\_FIFO
    - Works with static priorities higher than 0, ie, when a SCHED\_FIFO thread is runnable, it immediately preempts any currently running
      thread of type SCHED\_OTHER, SCHED\_BATCH or SCHED\_IDLE. Following rules -
      - A running SCHED\_FIFO thread which is preempted will stay at the front of the list for its priority (this is unlike the 4.4BSD
        scheduler where preemption led to being pushed to the end) and resume execution once higher priority threads finish.
      - When a blocked SCHED\_FIFO thread becomes runnable (say due to a sema\_up operation), its inserted at the end of the list for its
        priority (same as 4.4BSD scheduler).
      - If the priority of a running/runnable SCHED\_FIFO thread is changed using a system call, thread's position in the new priority list
        will depend on the direction of change of priority, eg, its pushed at the front/back of the list for new priority if priority was
        lowered/raised.
      - A thread which calls sched\_yield will be put at the end of the list.
    - A SCHED\_FIFO thread keeps running until it's either blocked by an I/O requested, preempted by a higher priority thread or it calls
      sched\_yield.

  * SCHED\_RR
    - Everything for SCHED\_FIFO applies to SCHED\_RR, with the addition that thread's run for a maximum of a time quantum - if it's been
      running for a duration >= time quantum, it'll be put at the end of the list for its priority (4.4BSD scheduler).
    - A SCHED\_RR thread which has been preempted by a higher priority thread will run for the remaining portion of its time quantum (at the
      time it was preempted) when it resumes execution.

  * SCHED\_DEADLINE
    - Currently implemented using Global Earliest Deadline First (GEDF) along with Constant Bandwidth Server (CBS).
    - A sporadic task is one that has a sequence of jobs - each job is activated at most once per period.
      - Each job has a deadline before which it should finish execution and a computation time which is the CPU time necessary for execution.
      - The moment when a task wakes up when a new job has to be executed is called arrival time (also request/release time)
      - start time is when the task starts its execution. absolute deadline is given by relative deadline + arrival time.
    - The parameters for the policy have these guidelines -
      - Runtime - A value larger than the average execution time, or worst case execution time if required.
      - Deadline - Relative deadline
      - Period - Period of the task
      - Runtime <= Deadline <= Period
      - All of these params should have a value of at least 1024 (nanoseconds) and less than 2^63.
    - CBS guarantees non interference between tasks, by throttling threads that attempt to overrun their specified runtime.
    - Kernel has to prevent a situation where set of SCHED\_DEADLINE threads is not schedulable with the given constraints.
      - When the policy is being set or changed for a thread, scheduler calculates if it can result in a feasible scheduling or not - if
        not, the system call fails with EBUSY.
      - SCHED\_DEADLINE threads are the highest priority threads in the system - if one is present, it'll preempt any other running thread
        with a different scheduling policy.
    - Calling sched\_yield results in yielding the CPU and waiting for a new period to begin.
      - Trying to fork a thread from a SCHED\_DEADLINE thread leads to EAGAIN.
      ```
          arrival/wakeup                    absolute deadline
                |    start time                    |
                |        |                         |
                v        v                         v
           -----x--------xooooooooooooooooo--------x--------x---
                         |<- comp. time ->|
                         |<-- Runtime ------->|
                |<----------- Deadline ----------->|
                |<-------------- Period ------------------->|
      ```

  * SCHED\_OTHER (SCHED\_NORMAL)
    - Can only be used at a static priority of 0. It's the default policy for threads that don't require realtime mechanisms.
    - There's a list of threads for static priority 0 - however, for threads within this list, a dynamic priority is also maintained - this
      dynamic priority is based on the nice value, and it's increased for each time quantum the thread is ready to run not scheduled, thus
      ensuring fair progress.
    - nice value is discussed in pintos, and it's a per thread attribute.
    - In CFS scheduler, relative differences in nice values have a much stronger effect, eg, for each unit of difference in nice value,
      there's a 1.25x difference between the threads chances of being picked up by the scheduler. Lower nice values (+19) leads to very
      little CPU to a process when there's other high priority load on the system, and higher nice values (-20) leads to providing the CPU
      to such application almost always.

  * SCHED\_BATCH
    - Can be used only at static priority of 0, and has a dynamic priority within that list.
    - This policy assumes that such a thread is CPU-intensive, applying a scheduling penalty during wakeup (due to sleep or sema, etc), thus
      being slightly disfavored for scheduling.
    - Useful for workloads that are noninteractive, but don't want to lower their nice value, and for workloads that want a deterministic
      scheduling policy without interactivity causing extra preemption.

  * SCHED\_IDLE
    - Can be used only at static priority of 0.
    - nice value has no effect in this policy.
    - Intended for running extremely low priority jobs (eg, a job with nice value less than +19 in SCHED\_NORMAL mode).

  * Resetting scheduling policy for child processes
    - Each thread has a reset-on-fork flag - if this is set, children created by fork don't inherit privileged scheduling policies.
    - It is intended for media playback applications and can be used to prevent applications evading the RLIMIT\_RTTIME resource limit by
      creating multiple child processes.
    - If the calling thread (for fork) has policy of SCHED\_FIFO or SCHED\_RR, policy is set to SCHED\_OTHER in child processes.
    - If calling thread has a negative nice value, it is reset to zero in child thread.
    - After the reset-on-fork flag is enabled, it can be reset only if the thread is privileged. This flag is disabled for children of fork.

  * Privileges and resource limits
    - RLIMIT\_RTPRIO limit defines a ceiling on an unprivileged thread's static priority for SCHED\_RR and SCHED\_FIFO policies.
      - If an unprivileged thread has a nonzero RTLIMIT\_RTPRIO, it can change its scheduling policy and priority (but priority value must
        be <= max (current\_priority, RTLIMIT\_RTPRIO)).
      - If RTLIMIT\_RTPRIO is 0, then priority can either be lowered, or policy can be changed to a non real-time policy.
      - User?
      - An unprivileged thread can switch from SCHED\_IDLE to SCHED\_OTHER or SCHED\_BATCH policy if its nice value falls within the range
        permitted by its RLIMIT\_NICE resource limit.
    - Privileged threads (CAP\_SYS\_NICE) ignore the RLIMIT\_RTPRIO limit - they can make arbitrary changes to priority and policy.
      - Eg, only a privileged thread can set or modify the SCHED\_DEADLINE policy.

  * Limiting CPU usage of real-time and deadline processes
    - A nonblocking infinite loop in a real-time thread can potentially block all other threads from accessing CPU forever - earlier, such
      processes could be killed by running a shell scheduled with higher static priority.
    - A new resource limit, RLIMIT\_RTTIME is available to set a ceiling on the CPU time that a real-time process may consume.
    - Two proc files are also available that can be used to reserve a certain amount of CPU time to be used by non real-time processes.
      - `/proc/sys/kernel/sched_rt_period_us` - Specifies a scheduling period equivalent to 100% CPU bandwidth, with values ranging from 1
        to INT\_MAX - giving an operating range of 1 ms to 35 mins, with default value of 1,000,000 (1 second).
      - `/proc/sys/kernel/sched_rt_runtime_us` - Specifies how much 'period' time can be used by all real-time and deadline processes, with
        values ranging from -1 to INT\_MAX-1, where -1 makes runtime same as period. Default value is 950,000 (0.95 sec).

  * Autogroup feature
    - To improve interactive desktop performance in case of multiprocess, CPU intensive workloads, eg, building the linux kernel with
      parallel build processes. Only processes with the non real-time policies are grouped by this feature.
    - Kernel should be configured with CONFIG\_SCHED\_AUTOGROUP (or from `/proc/sys/kernel/sched_autogroup_enabled`) - autogroup works
      in conjunction with CFS.
    - New autogroup is created when a new session is created via `setsid` (eg, when new terminal is started). Processes created via `fork`
      inherit the parent's autogroup, ie, all processes in a session are part of same autogroup. Autogroup is automatically destroyed when
      the last process in the group terminates.
    - When autogroup is enabled, all members of an autogroup are placed in the same kernel scheduler `task group` - CFS ensures that the
      CPU cycles are equally distributed within various task groups.
    - Say 2 autogroups, one with 10 build processes for linux kernel, and another with a video player, are running on a single CPU system
      (affinity for process to specific CPU can also be set using `taskset`) - without autogroup, video player would receive 9% of CPU time,
      but with autogroup, it'll receive about 50%.
    - The file `/proc/<pid>/autogroup` contains the nice value for an autogroup - this nice value's behaviour is the same as it is for a
      thread but it applies to the autogroup. CPU cycles received by a specific process within an autogroup is a function of the product of
      this nice value and the process' nice value.
    - Using cgroups CPU controller to place processes in cgroups other than the root CPU cgroup overrides the effect of autogrouping.

  * nice value and group scheduling
    - Task groups are formed in following situations
      - All threads in a CPU cgroup form a task group - parent being the task groups of parent cgroup.
      - With autogrouping, all threads of an autogroup form a task group - root task group is the parent of every autogroup.
      - With autogrouping, root task group consists of all processes in the root CPU cgroup that were not placed in a new autogroup.
      - Without autogrouping, root task group consists of all processes in the root CPU cgroup.
      - If group scheduling is disabled (ie, kernel configured without CONFIG\_FAIR\_GROUP\_SCHED), then all processes are placed in a single
        task group (equivalent to older linux scheduling with poor interactivity).
    - With group scheduling, nice value of a thread has an effect in scheduling decisions only relative to other threads in the same task
      group - unlike the typical usage of nice value to manipulate the priority across all normal policy processes. This neutrality of nice
      value is a benefit of autogroup, but there's a situation when the benefit of nice value (priority manipulation) is completely eroded.
      - For 2 CPU bound processes, lying in 2 autogroups, changing the nice value of 1 process doesn't effect the scheduler's decision for
        the process in another session - a workaround possibly exists.

  * Miscellaneous
    - Response time - A blocked high priority thread waiting for I/O has a certain response time before it's scheduled again - this response
      time can be reduced by the device driver by using a `slow interrupt` interrupt handler.
    - Child threads inherit the scheduling policy and params during fork and execve.
    - For real-time processes, memory locking is usually required to avoid paging delays.
    - cgroups CPU controller can be used to limit the CPU consumption of groups of processes


### Process Management Basics
  * NUMA - When memory is divided into multiple memory nodes. Access time depends on the distance between the accessing CPU node and the
    memory node. Access to local memory node for a CPU is faster than other memory nodes or memory bus shared by all CPUs.
    - numa\_maps (`/proc/<pid>/numa_maps`) - File has info about process' NUMA memory policy and allocations.
      - Each line has info about the memory range used by the process, and the effective policy for that memory range. One line per unique
        memory range.
      - When this read-only file is opened for reading, kernel scans the virtual address space of the process and reports memory usage.
    - First field has the starting address of the memory range which can be correlated with `/proc/<pid>/maps` which contains the end
      address of the range along with other info (eg, access permissions).
    - Second field has the effective memory policy (which can be different from the one set by the process, due to swapping).
    - N\<node\>=\<nr\_pages\> - Number of pages allocated on \<node\>. \<nr\_pages\> has the pages mapped for the process. Page migration
      and memory reclaim may've unmapped pages in the memory range and will show up again when process references them. If it's a shared
      memory area or file mapping, other processes might've pages mapped in the range.
    - file=\<filename\> - File backing the memory range. File maybe private, and write access may've generated copy on write pages in the
      memory range (displayed as anonymous pages).
    - heap - Memory range for heap.
    - stack - Memory range used for stack.
    - huge - Page count for hugepages only.
    - anon=\<pages\> - Anonymous pages in the range.
    - dirty=\<pages\> - dirty pages in the range.
    - mapped=\<pages\> - mapped pages in the range (excluding anon and dirty pages).
    - mapmax=\<count\> - Maximum mapcount (processes mapping a single page) found during scan - indicates degree of sharing in memory range.
    - swapcache=\<count\> - Pages with an associated entry on swap device.
    - active=\<pages\> - Pages in active list. It's shown only if different from total pages in the range (indicating inactive pages that
      maybe swapped out soon).
    - writeback=\<pages\> - Pages being written out to disk.

### System Calls For Execution And Synchronization
  * Structures
    ```
      struct clone_args {
        u64 flags;         //
        u64 pidfd;         // PID file descriptor address
        u64 child_tid;     // Where to store child TID in child's memory
        u64 parent_tid;    // Where to store child TID in parent's memory
        u64 exit_signal;   // Signal for parent on child termination
        u64 stack;         // Pointer to lowest byte of stack
        u64 stack_size;
        u64 tls;
        u64 set_tid;
        u64 set_tid_size;
        u64 cgroup;
      }
    ```

  * pid\_t waitpid (pid\_t pid, int \*\_Nullable wstatus, int options)
  * long syscall (SYS\_clone3, struct clone\_args \*cl\_args, size\_t size)
  * pid\_t fork (void)
  * int execve (const char \*pathname, char \*const \_Nullable argv[], char \*const \_Nullable envp[])
  * void \_exit (int status)

  * long syscall (SYS\_futex, uint32\_t \*uaddr, int futex\_op, uint32\_t val, const struct timespec \*timeout,
      uint32\_t \*uaddr2, uint32\_t val3)
    - futex - fast user space mutex - for fast locking and semaphores, supported by Linux.

### System Calls For Memory/Virtual Memory
  * long set\_mempolicy (int mode, const unsigned long \*nodemask, unsigned long maxnode)
    - Sets the NUMA memory policy of calling thread.
    - NUMA machines have different memory controllers at different distances from specific CPUs - policy defines from where will the
      memory be allocated for the thread (default policy).
    - Allocation of pages in process' address space outside of memory ranges, can be performed using `mbind` system call.
    - Memory policy is not remembered if the page is swapped out - when that page is brought back to memory, it'll use the policy of the
      thread or the memory range that is in effect at the time the page is (re) allocated.
    - nodemask gives a bitmask of node IDs pointing upto maxnode bits. nodemask = NULL or maxnode = 0 gives empty set of nodes in args.
    - Flags supported by mode
      - MPOL\_F\_NUMA\_BALANCING - If mode is MPOL\_BIND, enable kernel NUMA balancing for the thread if supported. EINVAL is set if the
        flag is not supported or used with mode other than MPOL\_BIND.
      - MPOL\_F\_RELATIVE\_NODES - A nonempty nodemask specifies node IDs that are relative to the current set of node IDs allowed by the
        current cpuset of the process (this seems to be to not fallback to system policy in case someone else has set a cpuset).
      - MPOL\_F\_STATIC\_NODES - A nonempty nodemask specifies physical node IDs. nodemask will not be remapped when the process moves
        to a different cpuset context, or the nodes allowed by the process' current cpuset context changes - why is such a flag allowed then
        if it poses risks like these?
    - mode values
      - MPOL\_DEFAULT - Any nondefault thread memory policy should be removed and system default should be used which is local allocation,
        ie, allocate memory on the node of the CPU that triggered the allocation. If local node has no memory, then attempt to allocate
        memory from a nearby node. nodemask should be NULL.
      - MPOL\_BIND - Restricts memory allocation to the nodes specified in nodemask. If multiple nodes are specified, allocations will
        happen at the node with lowest numeric ID till its full, followed by next higher ID, etc - but not from a node outside nodemask.
      - MPOL\_INTERLEAVE - Interleaves page allocation across the nodes specified in nodemask in numeric node ID order. This optimizes for
        bandwidth instead of latency by spreading out allocations (and hopefully, accesses) across multiple nodes.
      - MPOL\_PREFERRED - Can be used to specify one or more nodes in nodemask - allocates memory from the first node given in nodemask (ie,
        preferred node). If preferred node is exhausted, or nothing is given in nodemask, system default policy is used.
      - MPOL\_LOCAL - Allocate memory on the node that triggered the allocation. If memory not available or not able to allocate because
        of the cpuset of process, memory allocated from other nodes (but reverted to local node once available). nodemask is NULL.
    - Errors
      - EFAULT - Part of all the memory range given by nodemask is outside the accessible address space.
      - EINVAL - One of many validations for input failed - eg, mode is invalid, mode is MPOL\_DEFAULT but nodemask is non-NULL, mode is
        MPOL\_BIND or MPOL\_INTERLEAVE and nodemask is NULL, maxnode gives more than a page worth of bits, nodemask specifies a node ID
        that is larger than the maximum supported node ID, etc.
      - ENOMEM - Insufficient kernel memory available.

  * void \*mmap (void \*addr, size\_t length, int prot, int flags, int fd, off\_t offset)
    - Creates a new mapping (of the given file fd) in the virtual address space of the caller

  * int munmap (void \*addr, size\_t length)

  * int mlock (const void \*addr, size\_t len)
  * int munlock (const void \*addr, size\_t len)

### System Calls For Scheduling
  * Structures
    ```
      struct sched_param {
        int sched_priority;
      }

      struct sched_attr {
        u32 size;              // Size of this structure
        u32 sched_policy;      // Policy
        u64 sched_flags;       // Flags
        u32 sched_nice;        // Nice value (only for SCHED_OTHER and SCHED_BATCH)
        u32 sched_priority;    // Static priority (only for SCHED_FIFO, SCHED_RR)
        u64 sched_runtime;     // For SCHED_DEADLINE, along with below two
        u64 sched_deadline;
        u64 sched_period;
      }
    ```
  * int sched\_yield (void)
    - Called thread\_yield () in pintos, this is used to immediately yield the CPU for the kernel to schedule a new process - thread is
      moved to the end of the queue corresponding to its static priority. If the caller thread is the only highest priority thread, it'll
      be rescheduled.
    - In linux, sched\_yield always succeeds (no errors).
    - sched\_yield is to be used with real time scheduling policies (SCHED\_FIFO or SCHED\_RR) - using with nondeterministic policies
      (eg, SCHED\_OTHER) is unspecified. This call should be avoided in applications as the caller thread might be holding resources
      required by other threads, and will lead to performance degradation.

  * int sched\_setparam (pid\_t pid, const struct sched\_param \*param)
    - Sets the scheduling params associated with the scheduling policy for thread with given pid. If pid is 0, it's for current thread.
    - Checks the validity of the param for scheduling policy of thread. param-\>sched\_priority must lie in a specific interval.
    - Errors
      - EINVAL - param is NULL or pid is negative, or param doesn't make sense for the scheduling priority.
      - EPERM - Caller doesn't have the appropriate privileges.
      - ESRCH - Thread with given pid couldn't be found.

  * int nice (int inc)
    - Adds inc to the nice value of the current thread (as in 4.4BSD scheduler, this reduces priority for execution).
    - Range - +19 to -20.
    - Usually, only privileged processes can decrease their nice value.
    - Returns the newly set nice value - since -1 is a valid return value, errno must be set beforehand and checked afterwards for error
      (NOTE: errno variable is per thread [ref](https://stackoverflow.com/a/1694170)).
    - Error
      - EPERM - Process tried to reduce its nice value but doesn't have the privileges.

  * int sched\_setscheduler (pid\_t pid, int policy, const struct sched\_param \*param)
    - Sets the scheduling policy as well as params for the thread given by pid. If pid is 0, it's for current thread.
    - Normal policies - For these, sched\_priority should be 0.
      - SCHED\_OTHER - Standard round-robin time sharing policy.
      - SCHED\_BATCH - Batch style execution
      - SCHED\_IDLE - For running very low priority background jobs.
    - Real time policies - sched\_priority can be given with an allowed value (1-99 usually). SCHED\_RESET\_ON\_FORK flag can be set in
      which case, children created by `fork` don't inherit the scheduling policie.
      - SCHED\_FIFO - FIFO
      - SCHED\_RR - RR
    - Errors
      - EINVAL - pid is negative, or param is NULL, or policy is invalid, or param is invalid for the policy.
      - EPERM - Calling thread doesn't have appropriate privileges.
      - ESRCH - Thread ID with given pid not found.

  * int syscall (SYS\_sched\_setattr, pid\_t pid, struct sched\_attr \*attr, unsigned int flags)
    - glibc doesn't provide a wrapper for the sched\_setattr syscall.
    - Fields in attr
      - size - This is = sizeof (struct sched\_attr). If given struct has smaller size, remaining fields are assumed to be 0. If given
        struct is larger, kernel verifies that additional fields are 0 - if not, fails with E2BIG - this is for extensibility, ie,
        applications sending larger structures today won't break in future even if sizeof (struct sched\_attr) increases. It can also
        help the applications to detect if it's an older kernel (can't they find this info in a structured way?)
      - sched\_policy - SCHED\_* values for different policies, including SCHED\_DEADLINE
      - sched\_flags - OR of one or more flags.
        - SCHED\_FLAG\_RESET\_ON\_FORK - Given above.
        - SCHED\_FLAG\_RECLAIM - Allows SCHED\_DEADLINE thread to reclaim bandwidth unused by other realtime threads.
        - SCHED\_FLAG\_DL\_OVERRUN -
      - sched\_nice - For nice value.
      - sched\_priority - Static priority.
      - sched\_runtime - Given in ns.
      - sched\_deadline - ns
      - sched\_period - ns
    - flags argument should be 0, present for extensibility.
    - Errors
      - EINVAL
      - ESRCH
      - E2BIG
      - EBUSY - SCHED\_DEADLINE control failure
      - EINVAL - Invalid input params.
      - EPERM - Insufficient privileges. CPU affinity mask of the thread pid doesn't include all CPUs.

### Completely Fair Scheduler
  * Default scheduler for the "normal" threads (with no real time constraints) - maximize CPU utlilisation and interactive performance.
  * Schedulable Entities
    - Thread (minimum schedulable entity, ie, task)
    - Group of threads
    - Multithreaded processes
    - All processes of a user
  * Each task embeds a member (sched\_entity) that represent all the schedulable entities that the task belongs to.
    - Per CPU run queue sorts the sched\_entity structures in time ordered fashion in a red black tree, where leftmost node is occupied by
      the entity which has the least slice of execution. Nodes are indexed by processor execution time in ns.
    - For every process, maximum execution time is calculated, which represents the time that would've been alloted to the process on an
      "ideal processor". max\_exec\_time = waiting\_time / processes

  * Scheduling
    - Choose leftmost node of the tree and send for execution.
    - If execution completed, remove from the system and tree.
    - If process reaches max\_exec\_time or stopped (interrupt, syscall), reinserted to the tree based on new execution time.
    - Select new leftmost node of the tree.
    - Node insertion is O(log(N)) and picking for scheduling is O(1).

  * Upcoming scheduler - Earlier Eligible Virtual Deadline First Scheduling (1995)
    - Priorities based on - virtual time, eligible time, virtual requests, virtual deadlines

### Weighted Fair Queueing (WFQ) And O(1) Scheduler
  * WFQ is a network scheduling algorithm
    - Allows the scheduler to specify the fraction of capacity that needs to be given for each flow.
    - Weights are dynamic and can be updated based on needs, to ensure quality of service.
    - The algorithm involves basic computation and can be found on Wikipedia.

  * O(1) Scheduler (2003)
    - Before this, linux scheduling was O(n) (eg, 4.4BSD Scheduler) - this one gave a major boost.
    - Two arrays were maintained - active and expired - once a running thread was preempted after its time quantum, it was moved to the
      expired array - once the active array became empty, pointer is switched to make the expired array as the active array and vice versa.
      Since it's similar to FIFO, it was O(1).
    - All the scheduling algorithms in 2003 linux were O(1), allowing it to handle huge number of tasks - this was due to 2 queues -
      runqueues, priority arrays. However, the interactivity of the OS wasn't as efficient.
    - Scheduler would try to identify interactive processes by analyzing average sleep time (time spent waiting for input) - processors with
      long sleep times are probably waiting for user input, thus categorized as interactive, and receiving a priority bonus and lowering
      the priority threads assumed to be non-interactive (the assumption was a heuristic).

### Cgroups
  * [Ref](https://man7.org/linux/man-pages/man7/cgroups.7.html)
    - Control groups allow processes to be organized in hierarchical groups, and its usage of various resource types can be limited and
      monitored. It's provided via the pseudo-filesystem cgroupfs. Grouping is implemented in cgroup kernel code, resource limits and
      monitoring are implemented in per resource type subsystems (memory, CPU, etc).
    - Subsystem is a kernel component that modifies the behaviour of processes in a cgroup, eg, limiting the CPU time and memory available
      to a cgroup, tracking the CPU time used by a cgroup, freezing/resuming processes in the cgroup. Also called (resource) controllers.
    - Hierarchies are defined by creating, removing and renaming subdirectories within cgroupfs. Limits, controls and accounting given
      by cgroups are applicable in the hierarchy underneath the cgroup where the attributes are defined, ie, descendant cgroups can't
      exceed the limits posed on the higher level of hierarchy.
    - Information for specific process can be found in `/proc/<pid>/cgroup`

  * v1 vs v2

#### Cgroups v1
  * Tasks and Processes
  * Mounting Controllers
  * Unmounting Controllers
  * Controllers
    - cpu (CONFIG\_CGROUP\_SCHED) - cgroups can be guaranteed a minimum number of CPU shares when system is busy - when system is not
      busy, then there's no upper limit.
    - cpuacct (CONFIG\_CGROUP\_CPUACCT) - Accounting for CPU usage by groups of processes.
    - cpuset (CONFIG\_CPUSETS) - Bind the processes in a cgroup to a specified set of CPUs and NUMA nodes.
    - memory (CONFIG\_MEMCG) - Supports limiting and monitoring the process memory, kernel memory and swap.
    - devices
    - freezer
    - net\_cls (CONFIG\_CGROUP\_NET\_CLASSID) - Places a classid on the network packets created by the cgroup. This applies only to
      packets leaving the cgroup, not arriving. Can be used in firewalls and shaping outgoing traffic. Not present in v2.
    - blkio
    - perf\_event
    - net\_prio - Not present in v2.
    - huge\_tlb
    - pids (CONFIG\_CGROUP\_PIDS) - Limiting the number of processes created in the cgroup and descendants.
    - rdma (CONFIG\_CGROUP\_RDMA) -

### Filesystem System Calls
  * int fcntl (int fd, int cmd, ... \/\* arg \/\*)
    - [Ref](https://man7.org/linux/man-pages/man2/fcntl.2.html)

  * int open (const char \*pathname, int flags, ...)
  * int creat (const char \*pathname, mode\_t mode)
  * int close (int fd)
  * off\_t lseek (int fd, off\_t offset, int whence)
  * ssize\_t write (int fd, const void \*buf, size\_t count)
  * ssize\_t read (int fd, void \*buf, size\_t count)
  * int unlink (const char \*pathname)

  * int mkdir (const char \*pathname, mode\_t mode)
  * int chdir (const char \*path)
  * int syscall (SYS\_readdir, unsigned int fd, struct\_old\_linux\_dirent \*dirp, unsigned int count)

### List Of Standard Signals In Linux
  * Source - [Ref1](https://faculty.cs.niu.edu/~hutchins/csci480/signals.htm), [Ref2](https://man7.org/linux/man-pages/man7/signal.7.html)
  * Actions - Dump (Terminate and dump core). Stop (Stop/pause program)

  * SIGHUP (1, POSIX) - Hangup controlling process or terminal. Terminate.
  * SIGINT (2, POSIX) - Interrupt (Ctrl C) from keyboard. Terminate.
  * SIGQUIT (3, POSIX) - Quit from keyboard (Ctrl \). Dump.
  * SIGILL (4, POSIX) - Illegal instruction. Dump.
  * SIGTRAP (5) - Breakpoint for debugging. Dump.
  * SIGABRT (6, POSIX) - Abnormal termination. Dump.
  * SIGIOT (6) - Equivalent to SIGABRT. Dump.
  * SIGBUS (7) - Bus error. Dump.
  * SIGFPE (8, POSIX) - Floating point exception. Dump.
  * SIGKILL (9, POSIX) - Force process termination. Terminate.
  * SIGUSR1 (10, POSIX) - Available for processes. Terminate.
  * SIGSEGV (11, POSIX) - Invalid memory reference. Dump.
  * SIGUSR2 (12, POSIX) - Available for processes. Terminate.
  * SIGPIPE (13, POSIX) - Write to pipe with no readers. Terminate.
  * SIGALRM (14, POSIX) - Real timer clock. Terminate.
  * SIGTERM (15, POSIX) - Process termination. Terminate.
  * SIGSTKFLT (16) - Coprocessor stack error - Terminate.
  * SIGCHLD (17, POSIX) - Child process stopped/terminated or got a signal if tracing. Ignore.
  * SIGCONT (18, POSIX) - Resume execution if stopped. Continue.
  * SIGSTOP (19, POSIX) - Stop process execution via Ctrl Z. Stop.
  * SIGSTP (20, POSIX) - Stop process issued from TTY. Stop.
  * SIGTTIN (21, POSIX) - Background process requires input. Stop.
  * SIGTTOU (22, POSIX) - Background process requires output. Stop.
  * SIGURG (23) - Urgent condition on socket. Ignore.
  * SIGXCPU (24) - CPU time limit exceeded. Dump.
  * SIGXFSZ (25) - File size limit exceeded. Dump.
  * SIGVTALRM (26) - Virtual timer clock. Terminate.
  * SIGPROF (27) - Profile timer clock. Terminate.
  * SIGWINCH (28) - Window resize. Ignore.
  * SIGIO (29) - I/O possible. Terminate.
  * SIGPOLL (29) - Equivalent to SIGIO. Terminate.
  * SIGPWR (30) - Power supply failure. Terminate.
  * SIGSYS (31) - Bad system call. Dump.
  * SIGUNUSED (31) - Equivalent to SIGSYS. Dump



### Man Pages
  ```
    1. Executable programs or shell commands
    2. System calls (functions provided by the kernel)
    3. Library calls (functions within program libraries)
    4. Special files (usually found in /dev)
    5. File formats and conventions, e.g. /etc/passwd
    6. Games
    7. Miscellaneous (including macro packages and conventions), e.g. man(7), groff(7)
    8. System administration commands (usually only for root)
    9. Kernel routines [Non standard]
  ```

### Examples
  * Examples on Ubuntu 20.04.4 LTS
  * numa\_maps (similar to a process image corresponding to a ELF binary)
   ```
    From local redis server v7.2.3

      55eae82eb000 default file=/usr/bin/redis-check-rdb mapped=13 active=0 N0=13 kernelpagesize_kB=4
      55eae835f000 default file=/usr/bin/redis-check-rdb mapped=216 active=201 N0=216 kernelpagesize_kB=4
      ...
      55eae85a0000 default file=/usr/bin/redis-check-rdb anon=65 dirty=65 active=0 N0=65 kernelpagesize_kB=4
      55eae85e3000 default anon=25 dirty=25 active=0 N0=25 kernelpagesize_kB=4
      55eae9cae000 default heap anon=43 dirty=43 active=0 N0=43 kernelpagesize_kB=4
      7f4dd040c000 default anon=2 dirty=2 active=0 N0=2 kernelpagesize_kB=4
      ...
      7f4dd2690000 default file=/usr/lib/locale/locale-archive mapped=1 mapmax=15 N0=1 kernelpagesize_kB=4
      ...
      7f4dd35a9000 default file=/usr/lib/x86_64-linux-gnu/libgpg-error.so.0.28.0 mapped=1 mapmax=30 N0=1 kernelpagesize_kB=4
      7f4dd35ad000 default file=/usr/lib/x86_64-linux-gnu/libgpg-error.so.0.28.0 mapped=19 mapmax=13 N0=19 kernelpagesize_kB=4
      ...
      7f4dd35ce000 default file=/usr/lib/x86_64-linux-gnu/libgcrypt.so.20.2.5 mapped=8 mapmax=36 N0=8 kernelpagesize_kB=4
      7f4dd35da000 default file=/usr/lib/x86_64-linux-gnu/libgcrypt.so.20.2.5 mapped=16 mapmax=13 N0=16 kernelpagesize_kB=4
      ...
      7f4dd36ec000 default file=/usr/lib/x86_64-linux-gnu/liblz4.so.1.9.2 mapped=1 mapmax=33 N0=1 kernelpagesize_kB=4
      7f4dd36ee000 default file=/usr/lib/x86_64-linux-gnu/liblz4.so.1.9.2 mapped=13 mapmax=12 N0=13 kernelpagesize_kB=4
      ...
      7f4dd370d000 default file=/usr/lib/x86_64-linux-gnu/liblzma.so.5.2.4 mapped=1 mapmax=35 N0=1 kernelpagesize_kB=4
      7f4dd3710000 default file=/usr/lib/x86_64-linux-gnu/liblzma.so.5.2.4 mapped=8 mapmax=13 N0=8 kernelpagesize_kB=4
      ...
      7f4dd3736000 default file=/usr/lib/x86_64-linux-gnu/librt-2.31.so
      7f4dd3738000 default file=/usr/lib/x86_64-linux-gnu/librt-2.31.so mapped=4 mapmax=5 N0=4 kernelpagesize_kB=4
      ...
      7f4dd3740000 default file=/usr/lib/x86_64-linux-gnu/libsystemd.so.0.28.0 mapped=8 mapmax=38 N0=8 kernelpagesize_kB=4
      7f4dd3750000 default file=/usr/lib/x86_64-linux-gnu/libsystemd.so.0.28.0 mapped=43 mapmax=21 N0=43 kernelpagesize_kB=4
      ...
      7f4dd37ee000 default anon=2 dirty=2 active=0 N0=2 kernelpagesize_kB=4
      7f4dd37f1000 default file=/usr/lib/x86_64-linux-gnu/libc-2.31.so mapped=32 mapmax=23 N0=32 kernelpagesize_kB=4
      7f4dd3813000 default file=/usr/lib/x86_64-linux-gnu/libc-2.31.so mapped=298 mapmax=26 N0=298 kernelpagesize_kB=4
      ...
      7f4dd39e3000 default file=/usr/lib/x86_64-linux-gnu/libpthread-2.31.so mapped=6 mapmax=12 N0=6 kernelpagesize_kB=4
      7f4dd39e9000 default file=/usr/lib/x86_64-linux-gnu/libpthread-2.31.so mapped=17 mapmax=17 N0=17 kernelpagesize_kB=4
      ...
      7f4dd3a06000 default file=/usr/lib/dcaenabler/libcrypto.so.1.1 mapped=35 mapmax=4 N0=35 kernelpagesize_kB=4
      7f4dd3a7d000 default file=/usr/lib/dcaenabler/libcrypto.so.1.1 mapped=268 mapmax=6 N0=268 kernelpagesize_kB=4
      ...
      7f4dd3cf2000 default file=/usr/lib/dcaenabler/libssl.so.1.1
      7f4dd3d0e000 default file=/usr/lib/dcaenabler/libssl.so.1.1 mapped=16 mapmax=3 N0=16 kernelpagesize_kB=4
      ...
      7f4dd3d8a000 default file=/usr/lib/x86_64-linux-gnu/libdl-2.31.so mapped=1 mapmax=17 N0=1 kernelpagesize_kB=4
      7f4dd3d8b000 default file=/usr/lib/x86_64-linux-gnu/libdl-2.31.so mapped=2 mapmax=22 N0=2 kernelpagesize_kB=4
      ...
      7f4dd3d90000 default file=/usr/lib/x86_64-linux-gnu/libm-2.31.so mapped=13 mapmax=8 N0=13 kernelpagesize_kB=4
      7f4dd3d9d000 default file=/usr/lib/x86_64-linux-gnu/libm-2.31.so mapped=66 mapmax=8 N0=66 kernelpagesize_kB=4
      ...
      7f4dd3ef4000 default file=/usr/lib/x86_64-linux-gnu/ld-2.31.so
      7f4dd3ef5000 default file=/usr/lib/x86_64-linux-gnu/ld-2.31.so mapped=35 mapmax=24 N0=35 kernelpagesize_kB=4
      ...
      7f4dd3f23000 default anon=1 dirty=1 active=0 N0=1 kernelpagesize_kB=4
      7ffc2e66e000 default stack anon=6 dirty=6 active=1 N0=6 kernelpagesize_kB=4
      7f4dd3f23000 default anon=1 dirty=1 active=0 N0=1 kernelpagesize_kB=4
      7ffc2e66e000 default stack anon=6 dirty=6 active=1 N0=6 kernelpagesize_kB=4
      7ffc2e7e6000 default
      7ffc2e7ea000 default
   ```
