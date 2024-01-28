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

#### More On Linux
##### Types Of Commands
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

### Linux Kernel
  * [Official Doc](https://docs.kernel.org/)
  * It is highly unlikely that anything will go wrong within an established operating system, hence learning about them is almost irrelevant
    for developing any middlewares, application softwares and intelligent systems.

#### Completely Fair Scheduler
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

#### Weighted Fair Queueing (WFQ) And O(1) Scheduler
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
      the priority threads assumed to beo non-interactive (the assumption was a heuristic).
