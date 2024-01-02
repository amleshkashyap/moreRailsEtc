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
      suggest that it is (along with below two) an established process in the doamin.
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
