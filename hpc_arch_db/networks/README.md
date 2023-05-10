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
