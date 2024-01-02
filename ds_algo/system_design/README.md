# General
  * Service - Any application that must run a server of its own, eg, express, mysql, redis, rails, nginx. Any interaction of a service with
    the OS that would involve a port other than the one used by the service is considered an inter service interaction.

## Communication
  * Client Server
    - REST
    - gRPC
    - Websocket
    - Webhook - event driven, another microservice notifies a service (usually at a REST endpoint) about an event completion.
    - GraphQL - querying mechanism for client to fetch required data from server, can be used between servers too. Requesting entity doesn't
      have to rely on a code change in responding entity for fetching/not fetching existing data. A misbehaving requesting entity can cause
      performance problems in the responder.

  * Inter Service
    - REST
    - gRPC
    - Websocket

  * Intra Service
    - Method Call
    - System Call


## Data Serialization
  * Any data required for transfer or storage must be packable/unpackable in a well defined format.
  * Common Formats
    - JSON - transit
    - Protobuf - transit
    - CSV, XML, YAML - file storage/lookup
    - BSON - database storage/lookup

## Data For Lookup
  * Global Data Structure
  * File On Host
  * Database
  * Cache

## Application Performance
  * Communication
  * Data Structure
  * File Access
  * Storage
  * Cache


## Generic Notes
  * General API Guidelines
    - Resource names
    - Plurals
    - Idempotency
    - Versioning
    - Pagination
    - Sorting
    - Filtering
    - Nested resources
    - Rate limiting

  * Proxy
    - Forward - proxy is supposed to capture outgoing requests from clients and direct them to destination. used for protecting identity,
      blocking access to certain servers, and escaping restrictions from servers.
    - Reverse - proxy is supposed to capture incoming requests to servers, and redirect them (like a load balancer). used for load
      balancing, preventing DDoS, caching and secure communication.

  * Load Balancing Algorithms
    - Round Robin
    - Sticky Round Robin
    - Weighted Round Robin
    - IP/URL Hashing
    - Least Connections
    - Least Time

  * URL, URI, URN
    - URL - scheme + domain name + port + resource path + query + anchor
    - URI - scheme + authority + resource path + query
    - URN - scheme + namespace + namespace specific string

  * Query Execution
    - Relational Engine - Application -> Command Parser -> Query Optimiser -> Query Executor -> Storage Engine
    - Storage Engine -
      - Reads - Access Methods -> Buffer Manager
      - Writes - Access Methods -> Transaction Manager -> Lock Manager

  * Microservices Best Practices
    - Separate data store
    - Similar maturity level of different service code
    - Separate build for each microservice
    - Single responsibility
    - Containerized
    - Stateless servers
    - Domain driven design
      - Entities -> Use Cases -> Controllers -> [Infrastructure, Library, Network, UI, API, Devices, IO, DB]
    - Micro frontends
    - Orchestrated services
