# General
  * Topics on network communication.

## Basics Of Networks

### Layer 1-2 - Physical (bits) and Data Link (frames)
  * Out of scope

### Layer 3 - Network (packets)
  * Uniquely identify hosts, ie, sufficient source and destination information
    - This is the last layer which is readable - basic entity is packet

  * ipv4 packet headers - 20-byte fixed header, 4-byte optional header
    - 32-bit line-1
      - 0-3 (16) - version of protocol
      - 4-7 (16) - IHL (IP header length)
      - 8-13 (64) - DSCP (differentiated services code point)
      - 14-15 (4) - ECN (explicit congestion notification) - network congestion seen till now
      - 16-31 (65536) - length of packet (header + payload)
    - 32-bit line-2
      - 0-15 (65536) - packet identifier - a packet can be fragmented (into one or more ipv4 packets) during transmission but all fragments will contain this identifier
      - 16-18 (8) - flags - to provide information about whether a packet can be fragmented or not - MSB is always 0 so only 4 possible values
      - 19-31 (8192) - fragment offset - exact position of fragment in original packet
    - 32-bit line-3
      - 0-7 (256) - time to live - how many hops (routers) this packet can cross (to avoid looping in the network) - decreased by one at each hop, discarded when it becomes 0
      - 8-15 (256) - only for the network layer of destination host to determine the transport layer protocol - eg, ICMP (1), TCP (6), UDP (17)
      - 16-31 (65536) - checksum of the header for error detection
    - 1 x 32-bit line-4 - source address
    - 1 x 32-bit line-5 - destination address
    - 32-bit line-6
      - optional header
      - used when IHL > 5
      - some usage - 

  * ipv6 headers - contains a 40-byte fixed header and zero or more optional headers (extension headers). following suggests ipv6 is not backward compatible.
    - 32-bit line-1
      - 0-3 (16) - version of protocol
      - 4-9 (64) - DSCP (traffic class)
      - 10-11 (4) - ECN (traffic class)
      - 12-31 (2^20) - flow label - maintain sequential flow of packets belonging to a communication, to avoid reordering - designed for streaming/real-time media
    - 32-bit line-2
      - 0-15 (65536) - payload length - payload length is (extension headers + data) - 64KB is the basic limit (can be increased based on some headers)
      - 16-23 (256) - next header - indicates the type of extension header - if no extension header is present, then indicates the value of upper layer's (transport) packet data unit
      - 24-31 (256) - time to live - hop limit
    - 4 x 32-bit line-3 - source address
    - 4 x 32-bit line-4 - destination address

  * ipv6 extension headers (with next header value) -
    - Hop-By-Hop Options header (0) - read all devices in transit network
    - Routing header (43) - methods to support making routing decisions
    - Fragment header (44) - contains parameters of datagram fragmentation
    - Destination Options header (60) - read by destination services
    - Authentication header (51) - authenticity related information
    - Encapsulating Security Payload header (50) - encryption information
    - Order of ipv6 packet must be in this sequence:
      - ipv6 header -> ext header-0 -> ext header-60-1 -> ext header-43 -> ext header-44 -> ext header-51 -> ext header-50 -> ext header-60-2 -> transport layer header
    - ext header-60-2 is only to be processed by the destination address. ext header-60-1 can be processed by intermediate routers.

### Layer 4 - Transport (segment)
  * TCP/UDP

  * TCP headers -
    - 32-bit line-1
      - 0-15 (65536) - source port
      - 16-31 (65536) - destination port
    - 32-bit line-2 - sequence number
    - 32-bit line-3
      - 0-3 (16) - data offset
      - 4-9 (64) - reserved
      - 10-15 - URG flag
      - 16 - ACK flag
      - 17 - PUSH
      - 18 - RST
      - 19 - SYN
      - 20 - FIN
      - 
    - 32-bit line-4
      - 0-15 - checksum
      - 16-31 - urgent pointer
    - 32-bit line-5
      - options - can be anything between 0-31
      - padding - remaining bit of the 32 bit line
    - data bytes

  * Options (with value)
    - End of options (0) -
    - No operation (1) -
    - Max segment size (2) -
    - Window scale (3) -
    - Sack permitted (4) -
    - Sack (5) -
    - Time stamps (8) -

### Layer 5 - Session
  * SSL/TLS - Out of scope

### Layer 6 - Presentation 
  * Data conversion from source host's representation to destination host?
  * MIME

### Layer 7 - Application (data)
  * Webserver understands this protocol, takes the data and communicates to application server or directly the application in it's native language
    - nginx receives the request, sends to passenger which converts it to rack conventions and sends to rails application [which can be a rack application].

  * HTTP/SMTP/FTP

  * HTTP fields -
    - HTTP method
    - path
    - hostname
    - query params
    - HTTP headers


## Load Balancers

### AWS Load Balancers
  * ELB
    - Layer 4 (TCP) and Layer 7 (HTTP)
    - Routing decision params - port number
    - Can terminate TLS traffic
    - Can't forward traffic to more than one port per instance
    - Can't forward to IP addresses - only EC2 instances or containers
    - Doesn't support websockets directly - can use Layer 4 [what?]

  * Application Load Balancer
    - Layer 7
    - Routing decision params - hostname, path, query params, HTTP methods, HTTP headers, source IP, port number
    - Can route to many ports on a single target


## System Calls For Sockets
  * [Ref](https://man7.org/linux/man-pages/man2/socket.2.html)
  * [Specs](https://pubs.opengroup.org/onlinepubs/009604499/functions/socket.html)
  * Sockets are relevant for building any client or server application. Following method descriptions are useful to understand the basic
    operations going underneath and are the tools for building such applications.
    - [This repo](https://github.com/jams2/py-dict-client/blob/main/dictionary_client/dictionary_client.py) writes a client for the DICT
      protocol (a tiny but real protocol with barely any clients - explore socket programming details).

  * Structures
   ```
     struct sockaddr {
       sa_family_t sa_family;
       char        sa_data[14];
     }

     struct sockaddr_un {          // Unix Domain Socket Struct
       sa_family_t sun_family;     // Value is always AF_UNIX
       char        sun_path[108];  // Pathname
     }

     struct pollfd {
        int fd;           // File descriptor
        short events;     // Requested events
        short revents;    // An output value - filled by kernel with events that actually occurred
     }
   ```

  * int socket (int domain, int type, int protocol)
    - Creates an unbound socket in a communication domain, and returns the lowest numbered fd not opened for the process, for operating on
      the socket.
    - domain - Communications domain for which socket is created - it selects the protocol family. Some types for web apps -
      - AF\_UNIX - Local communication.
      - AF\_LOCAL - Same as AF\_UNIX
      - AF\_INET - IPv4 protocols
      - AF\_INET6 - IPv6 protocols
      - AF\_NETLINK - Kernel user interface device
      - AF\_PACKET - Low level packet interface
      - AF\_RDS - Reliable Datagram Socket protocols
      - AF\_PPPOX - PPP transport layer for L2 tunnels (L2TP, PPPoE)
      - AF\_BLUETOOTH - Bluetooth low level protocols
      - AF\_ALG - Kernel crypto API
      - AF\_VSOCK - Hypervisor guest communications (VMWare Sockets)

    - type - Socket type which determines the semantics of the communication.
      - SOCK\_STREAM - Sequenced, reliable, 2-way, connection based byte streams. Out of band data transmission maybe supported
      - SOCK\_DGRAM - Connectionless, unreliable messages of fixed maximum length (datagrams)
      - SOCK\_SEQPACKET - Sequenced, reliable, 2-way, connection based data transmission path for datagrams of fixed max length - consumer
        must read an entire packet with each system call (as max buffer size is known).
      - SOCK\_RAW - Raw access to the network protocol
      - SOCK\_RDM - Reliable datagram layer that doesn't guarantee ordering
      - SOCK\_PACKET - Obsolete. Used to receive raw packet from the device driver. (Use `packet` syscall).
      - SOCK\_NONBLOCK - Sets the O\_NONBLOCK status flag on the open fd which is referred by the return fd value. It's a performance
        enhancement. To specify this type, take a bitwise 'or' of the required type's value with this value.
      - SOCK\_CLOEXEC - Sets the close-on-exec flag on the returned fd. Value can be set with bitwise 'or' as above.

    - protocol - Specifies the particular protocol to be used. Usually, for a given domain and socket type, support for only one protocol
      exists, and a value of 0 should be fine. However, if multiple protocols exist, value should ideally be provided.
      - ip, tcp, udp
      - There are separate system calls to obtain the protocol numbers or convert protocol string to number.

    - Errors
      - EACCES - Permission to create a socket of the type/protocol is denied.
      - EAFNOSUPPORT - Address family not supported
      - EINVAL - Protocol is unknown/unavailable
      - EINVAL - Invalid flags in type
      - EMFILE - Per process limit on number of open fd has been reached
      - ENFILE - System wide limit for number of open fd has been reached
      - EPROTONOSUPPORT - Protocol not supported by the address family or the implementation
      - ENOBUFS - Insufficient resources available to perform the operations
      - ENOMEM - Insufficient memory available to fulfill the request
      - EPROTOTYPE - Socket type not supported by protocol (From Spec)

  * Socket Types. For SOCK\_STREAM
    - Fully duplex byte streams which do not preserve record boundaries.
    - Socket must be in connected state for data exchanges.
    - `connect` syscall can be used to connect to another socket.
    - `read`, `write`, `send`, `recv` and variants can be used for data exchange - out of band data may be sent/received as well.
    - Protocols implementing this type must ensure that data is not lost/duplicated.
    - If a piece of data for which buffer space is available can't be transmitted in some timeframe, then the connection is considered dead.
      When SO\_KEEPALIVE is enabled, protocol checks if other end is still alive.
    - When a process sends or receives on a broken stream, SIGPIPE is raised which can cause the process to exit if not handled.
    - SOCK\_SEQPACKET has the same syscalls - however, `read` will return only the requested amount of data, discarding the rest.
      Message boundaries are also preserved in the incoming datagram.
    - SOCK\_DGRAM and SOCK\_RAW allow sending/receiving datagrams via `sendto` and `recvfrom`.
    - When the network signals an error to the protocol module (eg, ICMP or IP message), the error code is set for the socket, which is
      returned on the next operation on the socket. Per socket error queue can also be enabled for more details as these operations are
      asynchronous.
    - Operations are available to send signals when out of band data arrives (SIGURG) or socket breaks unexpectedly (SIGPIPE) for a process
      or process group. It's possible for process and process groups can receive I/O notifications and asynchronous notifications for I/O - 
      for such processes/groups, SIGIO can be set during errors.
    - Various configurations for sockets are given [here](https://man7.org/linux/man-pages/man7/socket.7.html).
    - For sockets of TCP protocol, multiple configurations are available to extract more performance based on the physical resources
      available to the service. Eg, Window scaling allows the use of large TCP windows (> 64kB) to support links with high latency and/or
      bandwidth. At least some of these configurations can be set at the socket level as well, and others are global. Configuration files
      are available in `/proc/sys/net/ipv4/`.
      - Configs for tcp protocol implementation are given [here](https://man7.org/linux/man-pages/man7/tcp.7.html).

  * int connect (int sockfd, const struct sockaddr \*addr, socklen\_t addrlen)
    - Connects the socket referred to by sockfd to the address specified by addr (whose length is given by addrlen), returning success flag.
      - Passing length for pointers is present across C methods - check arbitrary memory manipulation
    - Format of address in addr is specified by the address space of sockfd.
    - For sockfd of type SOCK\_DGRAM, addr refers to the default address for exchange of datagrams.
    - For sockfd of type SOCK\_SEQPACKET and SOCK\_STREAM, connection is attempted with another socket bound to addr.
    - Some sockets may connect only once (UNIX domain sockets), while others may connect multiple times to change their association (eg, UNIX
      datagram sockets)
    - Errors
      - EACCES - Write permission is denied on the socket file or search permission denied for directory of the file.
      - EACCES - An SELinux policy denied connection (eg, a policy where HTTP proxy can only connect to ports for HTTP servers, but proxy
        tried to connect to a different port).
      - EADDRINUSE - Local address already in use.
      - EADDRNOTAVAIL - sockfd was not bound to an address, and upon binding it to an ephemeral port, all port numbers are in use.
      - EAFNOSUPPORT - Given address didn't have the correct address family is `sa\_family` field.
      - EAGAIN - For nonblocking UNIX domain sockets, this means that the socket is nonblocking and connection cannot be completed
        immediately. For other sockets, this means there are insufficient entries in routing cache (what?)
      - EALREADY - Socket is nonblocking and previous connection attempt is not yet completed.
      - EBADF - sockfd is not a valid open fd.
      - ECONNREFUSED - connect () on the stream socket found no one listening on the remote address.
      - EFAULT - socket structure address is outside user's address space.
      - EINPROGRESS - Socket is nonblocking and connection can't be completed immediately (for UNIX domain sockets, its EAGAIN). It's
        possible to do `select`/`poll` for completion by selecting the socket for writing. After `select` indicates writability, use
        `getsockopt` to read SO\_ERROR option at SOL\_SOCKET level to determine if connect completed successfully/unsuccessfully.
      - EINTR - Syscall interrupted by another signal which was caught.
      - EISCONN - Socket already connected.
      - ENETUNREACH - Network is unreachable.
      - ENOTSOCK - The fd given by sockfd is not a socket.
      - EPROTOTYPE - Socket type doesn't support the requested protocol (eg, connecting a UNIX domain datagram socket to stream socket).
      - ETIMEDOUT - Timeout when attempting connection - for IP sockets, timeouts maybe very long if syncookies are set.

  * int accept (int sockfd, <> addr, <> addrlen)
    - For connection based socket types.
    - Extracts the first connection request on the queue for pending connections for the listening socket sockfd, creates a new connected
      socket and returns a fd to this new socket. New socket is not in listening state, and sockfd is unaffected.

  * int bind (int sockfd, const struct sockaddr \*addr, socklen\_t addrlen)
    - A socket created using `socket` exists in a name space without any address assigned to it - bind assigns the address addr to sockfd.

  * int listen (int sockfd, int backlog)
    - Marks sockfd as passive socket, ie, a socket that will be used to accept incoming connection requests using `accept`. Relevant only
      for connection based socket types.
    - backlog specifies the max length to which the queue of pending connections for sockfd may grow. If a connection request arrives when
      queue is full, client may receive an error (ECONNREFUSED) or if retransmission is supported by the protocol, request maybe ignored
      so that the client may reattempt successfully.
    - Errors
      - EADDRINUSE - Another socket already listening on the same port.
      - EADDRINUSE - sockfd was not bound to an address, and upon binding it to an ephemeral port, all port numbers are in use.
      - EBADF - sockfd is not a valid file descriptor.
      - ENOTSOCK - The fd given by sockfd is not a socket.
      - EOPNOTSUPP - The socket type doesn't support listen.

  * send

  * recv

  * int select (int nfds, <> readfds, <> writefds, <> exceptfds, <> timeout)

  * int poll (struct pollfd \*fds, nfds\_t nfds, int timeout)
    - Similar to select, it waits for one of a set of fd to become ready to perform I/O.
    - `epoll` extends poll further but specific to linux.
    - timeout is for blocking poll for an event till -
      - an fd becomes ready
      - call is interrupted by signal handler
      - timeout expires
    - Returns a non-negative value which refers to the number of elements in fds whose revents fields have been set to non-zero value (error
      signal/event). Return value 0 refers to timeout and -1 refers to an error in execution of poll.
    - List of bits for events/revents
      - POLLIN - Data is available to be read. (Also, connection setup has completed for connection oriented protocols).
      - POLLPRI - An exception condition on fd - eg, out of band data on TCP socket, cgroup.events file is modified
      - POLLOUT - Writing is possible, but a write larger than the available space in a socket/pipe will still block.
      - POLLRDHUP - Stream socket peer closed connection or shut down writing.
      - POLLERR - Error (only written in revents, ignored in events). Also set for a fd referring to the write end of a pipe when read
        end is closed.
      - POLLHUP - When reading from a channel like pipe or stream socket, this indicates that the peer closed its end of the channel.
        Subsequent reads from the channel will return 0 after all outstanding data is consumed. This is returned in revents and ignored
        in events.
      - POLLNVAL - Invalid request. fd not open (only in revents).
      - POLLRDNORM/POLLWRNORM - Same as POLLIN/POLLOUT
      - POLLRDBAND/POLLWRBAND - Priority band data can be read/written.

    - Errors
      - EFAULT - fds points outside the process' accessible address space.
      - EINTR - A signal encountered before any requested event.
      - EINVAL - nfds value exceeds the configured threshold (RLIMIT\_NOFILE). (Also, timeout value is negative).
      - ENOMEM - Unable to allocate memory for kernel data structures.

  * Glossary
    - Out of band data
    - Record boundary
    - Syncookies

## Role Of Webservers

### Nginx


## Kubernetes Env

### Ingress Nginx


## Application <-> Webserver <-> Kubernetes Env <-> DNS

### Application <-> Webserver
  * HTTP Connections

  * Websocket Connections

  * Services Within Kubernetes

### Webserver <-> Kubernetes Env


### Kubernetes Env <-> DNS


## Maglev (Load Balancer, 2016)
  * [Source](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/44824.pdf)
  * [Ref](https://www.the-paper-trail.org/post/2020-06-23-maglev/)

  * Background
    - A network load balancer typically consists of multiple devices located between routers and service endpoints. Load balancer maps
      each packet to its corresponding service, and forwards it to one of the service endpoints.
    - Network load balancers were typically implemented in hardware, and have limitations.
      - Scalability is constrained by max capacity of a single unit
      - Generally deployed as a pair, they only provide 1+1 redundancy, hence affecting high availability
      - Since they're specialised hardware, they are hard/impossible to change once produced (limited flexibility)
      - Expensive to upgrade - requires purchasing and installing new hardware.
    - A software load balancer tries to overcome the above limitations (high throughput, upgrades, etc), but introduces a new limitation -
      - Machines hosting the software load balancers can fail/need upgrade - and connection information in those machines can be lost.
      - NOTE: The problem of service endpoints (actual servers) changing is faced even by hardware load balancers.
    - Equal Cost Multipath Routing (ECMP, 2005+) - Decision about the next hop made at the router to balance load - multiple best paths to a
      particular destination are assigned equal weights, and one of them might be chosen by the router based on the traffic. In a naive
      routing strategy (no ECMP), router might choose only 1 best path for all the packets, increasing congestion. 
      - Per Destination - In this (default) strategy, ECMP guarantees that packets with same 5-tuple hash will take the same path.
      - Per Packet - Paths are chosen to distribute packets using some round robin strategy. Inappropriate when sequence matters.
      - [Ref](https://avinetworks.com/glossary/equal-cost-multi-path-routing-ecmp/)

  * More Background
    - VIP (Virtual IP) - A service can have multiple endpoints - for every service, the group of endpoints are assigned one or more VIP.
    - Maglev maps each VIP with a set of service endpoints and informs the routers via BGP (Border Gateway Protocol, 1989)
    - Routers announce them to the backbone.
    - All of these VIPs are then shared over the internet so that connections can be made.
    - 5-tuple hash - source IP, source port, destination IP, destination port, IP protocol number

  * Basic Steps While Accessing GCP Service
    - Browser issues a DNS query which is served by authoritative DNS servers (possibly from cache).
    - DNS server assigns the user to a nearby frontend location [considering geolocation and current load on the frontend location], and
      return a VIP belonging to the selected location.
    - Browser attempts to establish a connection with the above VIP.
    - When router receives a VIP packet, it forwards it to one of the machines hosting Maglev into the cluster via ECMP.
    - When Maglev receives a VIP packet, it selects a service endpoint from the set mapped to the VIP, and encapsulates the packet using
      GRE (Generic Routing Encapsulation, 1994) with the outer IP header destined to the endpoint.
    - When the packet arrives at a service endpoint, it's decapsulated and consumed - response is put in a IP packet with source address
      being the VIP and destination address being that of the browser.
    - DSR (Direct Server Return) is used to send response directly to the browser without involving Maglev.

  * Maglev Components/Deployment
    - Controller - responsible for checking the health of forwarder. If forwarder goes down, then the controller sends a message to the
      routers via BGP to deem itself unhealthy for future packets.
    - VIP announcer - Announces the VIPs to routers via BGP. Part of the controller.
    - Forwarder - Maintains a health checker, a set of backend pools, and a config manager
    - Config objects - contain the VIPs that the Maglev service will serve. It maybe present in a file, or a received from other systems
      via RPC.
    - Backend pools - Consists of 2 things -
      - Physical IP addresses for the endpoints of a particular service
      - Other backend pools which can be for other service endpoints
    - Forwarder health checker - checks the health of IP addresses in the backend pools. Since one physical machine with 1 physical IP
      address maybe serving multiple services (hence maybe part of multiple backend pools), health checks are done using IP address.
    - Config manager - Parses and validates config objects before modifying forwarder behaviour. Configs are committed atomically - hence,
      a Maglev machine can become out of sync (also possible during health checks). To keep up with the requests, consistent hashing is
      used to switch between Maglevs with similar backend pools.
    - Sharding - Maglevs can be sharded within a cluster to isolate VIPs for performance and quality of service (as well as testing
      without interfering with regular traffic).

  * VIP Matching
    - Each cluster has a globally identifiable IP. A particular service is configured as different VIP in different clusters.
    - They've different classes of clusters, serving different VIP sets - external prefix length is same for same cluster class, but may
      differ for different cluster classes.
    - During emergencies, traffic might need to be routed to a different cluster (from some maglev) - one way would be to define all VIPs
      in all clusters that may receive redirected traffic - but it can cause synchronization and scalability problems.
    - They assign same suffix for a particular VIP across all clusters of a class -
      - First, a longest prefix match is done on the packet to determine the cluster class.
      - A longest suffix match is done to identify the backend pool in the cluster class.
      - They configure maglevs with a large prefix group for each cluster class from which the prefix for a new cluster in the same class
        will be allocated. This avoids the need for regular synchronisation of prefixes (NOTE: largest prefix match would guarantee that
        whatever prefix is chosen will belong to that cluster class, even though the particular prefix was not used in the past).
    - VIP - \<Prefix Group, IP Suffix, port, protocol\>
    - When a packet belonging to a different prefix group is identified, the packet is encapsulated by maglev and send it towards the
      relevant cluster - then the receiving cluster's maglev will decapsulate it and process accordingly.

  * Forwarder
    - Steering module - receives the packets from NIC, computes 5-tuple hash and puts them in receiving queue based on the hash. Performs
      hashing instead of round robin in the general case - (1) it lowers the packet reordering probability within a connection due to
      varying speeds of packet threads, (2) backend selection is to be performed only once for each connection, and eliminating the
      possibility of different backend pool selection due to race conditions caused by health updates (if the backend selection ran and
      found a backend whose health got updated, then it has to rerun?)
    - Receiving queue - each queue is mapped to 1 packet thread
    - Packet thread - tries to map a packet to a VIP (filters out packets not mapping to any VIP). Recomputes 5-tuple hash and looks for the
      hash value in connection table. If a match is found and backend is healthy, then the result is reused. Else, consults the consistent
      hashing module and selects a new backend pool for the packet - and adds the entry to its connection table with same hash computed
      earlier for the packet. If no backend pool is available, packet is dropped. After backend is selected, packet is encapsulated with
      proper (?) GRE/IP header and sent to transmission queue.
    - Connection table - this is maintained for every packet thread to avoid contention (and collision?). Stores backend pool results for
      recent connections.
    - Consistent hashing module -
    - Transmission queue -
    - Muxing module - Polls the transmission queues and passes packets to NIC.

  * Fast Packet Processing
    - Numbers
      - Expected packet traffic - 10Gbps
      - Packet size - 1,500 bytes, Packets - ~890K packets per second (pps)
      - Packet size - 100 bytes, Packets - ~13Mpps

    - When maglev daemon inits, it allocates a packet pool which is shared with the NIC - details are not provided, but the Ref seems to
      suggest that it is (along with below two) an established process in the domain.
      - Assumption is that it's shared between the host machine's NIC and maglev, which is a userspace application.
      - Goal seems to be to capture packets coming from router to maglev host NIC directly to maglev instead of going via OS - however,
        initial implementation of maglev didn't have this optimisation.

    - Steering and Muxing modules maintain a ring queue, where each entry is a pointer to a packet in the packet pool.
      - Packet pool seems to have the capacity to contain only a fixed number of packets - also, packets are not copied to maglev. Once the
        packet pool capacity is reached within a specific periodic timer delay [heavy overload, see below], then packets are dropped.
      - Apart from this, they have 3 pointers which point to the queue itself.
      - Steering module has pointers to mark the last received, last processed and first reserved packets.
      - Muxing module has pointers to mark the first ready, last sent and recycled packets.
      - NIC places the new packets at received pointer and forwards it.
      - Steering module sends the received packets to packet threads and marks them processed.
      - Above also maintains the unused packet slots in the pool as reserved - the difference in available and unused is not clear.
      - On the sending side (towards the service endpoint machines), NIC sends packets marked by sent pointer and advances it (ie, the
        Muxing module would've logically marked them as sent, and NIC would be doing the job of actually sending them).
      - Muxing module marks the packets returned by packet threads by the ready pointer.
      - Also, the packets sent by NIC are marked as recycled.

    - Packets don't share data with each other to avoid contention.
      - 1 packet thread has the affinity set to 1 CPU core for best performance.
      - Packets are processed in batches when possible - batch processing is done if a specific batch size is reached or a periodic timer
        expires [event loops] - batch sizes maybe adjusted dynamically.
      - When maglev has no traffic, then a packet may have to wait for upto 1 periodic timer delay [50 us] to be processed (NOTE: with
        10Mpps processing speed, each packet will take 0.1us for processing, so total 50.1us]
      - When maglev has traffic, then assuming a packet pool size of 3000, with 10Mpps speed, entire packet pool can be processed in 300us,
        ie, that's the max a packet has to wait when processed in large batch of 3000 (after reaching 3000, packets will be dropped).

  * Backend Selection
    - After getting the 5-tuple hash, if the hash exists in connection table, then the packet is sent to the backend given in the table (if
      it is healthy). This is helpful to handle following scenarios -
      - Backends have gone unhealthy
      - Backends has been added/removed
      - Weight of backends have changed

    - If the 5-tuple hash is not present in the connection table, then a new one is assigned and entry is added to the table.

    - Above connection tracking based approach "assumes" that all packets with same 5-tuple hash will be sent to the same maglev (as
      connection tables are per maglev) - this is not guaranteed when maglev machines change (eg, restarts due to updates, addition/removal
      of maglev hosts for any reason).
      - New/different maglev machines to which the traffic will be forwarded by router in such scenarios are not going to have the correct
        connection tables, hence connections will break.

    - Apart from the above, another limitation is that the connection table size [finite] maybe reached due to high traffic and there'll
      be no space to assign new entries - this limitation is more signficant when each host machine has multiple maglev deployments, as
      well as other service deployments, which share the memory. For handling these limitations to ensure reliable packet delivery,
      consistent hashing is used.

  * Consistent Hashing
    - Limitations of (local) connection table could be overcome by sharing connection states across all maglevs - but that needs heavy
      synchronization. A maglev daemon doesn't even share connection states among packet threads within itself.
    - General distributed hashing problem - given a set of n options to place an entity, agree on k options. The k=1 case can be solved
      using consistent hashing as well [general is solved using rendezvous hashing].
    - Here, the n options can be given by a large lookup table. Consistent hashing implicitly provides the below -
      - Load balancing - by choosing k=1 option for an entity, not all entities can be potentially sent to a particular option (similar
        to what was done by ECMP), which is desirable for load balancing.
      - Minimal disruption - when n is increased/decreased, the existing entities will need minimal/no changes in their options.
    - For maglev, load balancing is a more critical metric to focus on during implementation, and some disruptions are fine (connection loss)
    - When a connections affinity to maglev changes (during upgrade/health checks, etc), then the connection resets/losses are proportional
      to the lookup table disruption (ie, number of entries added/removed/shuffled in the lookup table).
    - The hashing begins by calculating the permutation table - permutation table is populated using offset and skip which are dependent
      on the backend ID and lookup table size - even if a backend is added/removed, rest of the backends will have the same permutation
      table. Permutation table is a matrix where each column i gives the preferred index list in lookup table for any backend i.
    - The outer for loop runs for every backend i (total N backends), and finds an index c in the lookup table (size M) for it - c is
      chosen from the preference list for a backend i, and finalised when an empty c is found in the lookup table. Once the outer for
      loop completes (N iters), there will still be M-N positions left, which need to be occupied by the same N backends - this is handled
      by the outermost while loop which is alive till the lookup table is full (M iters - hence giving worst case O(M^2) for N = M).
    - In Fig.4, they show where consistent hashing (and VIP matching) is placed - when a packets 5-tuple hash is not found in the local
      connection table, consistent hashing is utilised. Similarly, before reaching the 5-tuple hashing stage, VIP matching is performed which
      can lead to packet loss on a miss. GRE is run after the above 2 (for packet forwarding, fragment redirection and VIP matching).
    - It's not clear how the packets are mapped to the lookup table created using their procedure - but it should ideally be using the
      5-tuple hash they calculated, and once a backend is picked up, would be stored in connection table.

  * Fragment Handling
    - If a packet is larger than the MTU (maximum transmission unit) of a network link, the packet is broken to fragments (say 2) - the
      first one will have all the information but the second one will have only limited info. There's an additional latency incurred
      by fragmentation - during the time of breakdown, and while reassembly. It also increases the chances of packet loss, which can lead
      to even further latency due to retransmission.
    - In their example, if a datagram is split into 2 fragments, then first one will have both L3/L4 headers, but second one will have only
      L3 header.
      - To handle fragments, first requirement is that all the fragments must be received by the same maglev (else it'll lose the packet).
      - Also, maglev hashing should be in a position to select the same backend for unfragmented packets, first fragment and non-first
        fragments - since maglev hashing is more inclined towards achieving bandwidth and is okay with some connection losses, fragmented
        packets may lead to more connection losses.
    - For the first requirement, each maglev has info about all maglevs in the cluster. On receiving a fragment, it takes the 3-tuple hash
      (as some routers use 3-tuple hash for non-first first fragments, and 5-tuple for first fragments), and redirects it to the correct
      maglev - this works as all fragments of a packet will have the same 3-tuple. GRE is used for only 1 redirection per fragment.
    - For the second requirement, each maglev has a fixed size fragment table which maintains forwarding decision for first fragment -
      - Upon receiving a non-first fragment, its searched in the table for a match, if found, then immediately forwarded.
      - If a match is not found (out of order fragments), then it's stored in the table till first fragment is received or entry expires.
      - This adds an additional hop for fragments and can lead to packet reordering. Also, additional space required for the table.

  * Monitoring And Debugging
    - Black Box - Agents spread across the world check for reachability and latency of configured VIPs.
    - White Box - Maglev hosts export metrics via HTTP server, which is monitored by another system for every host, and sends alerts.
    - Packet Tracer Tool - Similar to X-trace (?). Constructs and sends payloads which are marked in a way that Maglev recognizes them (via
      specific L3/L4 headers). Payloads contain IP addresses where maglev sends debugging information. The packets usually target specific
      VIP and are routed to frontend - when maglev receives such a packet, it forwards it, but also sends some information like its
      host IP and selected backend to the IP in the payload. Packet tracer packets are rate limited.
