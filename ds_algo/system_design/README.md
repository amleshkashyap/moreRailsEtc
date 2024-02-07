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

### LLD/HLD
  * [Ref](https://www.interviewbit.com/low-level-design-interview-questions/)
  * HLD - Components, interactions, database design
  * LLD - Classes, design patterns, object creation, data flow across objects. Interviews expect a simplified view
    - [Ex](https://lldcoding.com/)
    - Object oriented programming
    - Object oriented principles
      - YAGNI - You Ain't Gonna Need It - build only what's needed
      - DRY - Don't Repeat Yourself
      - SOLID
    - UML Diagrams
      - Structural - Static system view
      - Behavioural - Dynamic system view
    - Design Patterns
    - ER Diagrams

  * Structural Diagrams
    - Composite Structure
    - Deployment
    - Packages
    - Profile
    - Classes - x
    - Objects
    - Components

  * Behavioural Diagrams
    - State machines
    - Communication
    - Usecases - x
    - Activities
    - Sequence
    - Timings
    - Interaction overview

  * Breakdown
    - Requirements - 3%
    - Design - 8%
    - Implementation - 7%
    - Testing - 15%
    - Maintenance - 67% - LLD is about designing reusable, extensible and maintenable code architecture

  * LLD Example
    ```
           -------------------------                             --------------------------
          | Game                    |                           | Players                  |
          |-------------------------|                           |--------------------------|
          | board: Board            |                           | position: int            |
          |-------------------------|                           |--------------------------|
          | dice: Dice              |   <------------------     | name: string             |
          |-------------------------|                           |--------------------------|
          | players: List<Players>  |                           |                          |
          |-------------------------|                           | setPosition(int)         |
          | status: GameStatus      |                           |--------------------------|
          |-------------------------|                           | getPosition()            |
          |                         |                            --------------------------
          | startGame()             |
          |-------------------------|          -----------                                     -------------
          | makeMove(Players)       |         | Dice      |                                   |  GameStatus |
          |-------------------------|  <----  |-----------|                                   |    (enum)   |
          | addPlayers(Players)     |         | maxValue  |                                   |-------------|
           -------------------------          |-----------|                                   | NOT STARTED |
                       ^                      |           |                                   |-------------|
                       |                      | roll()    |                                   | RUNNING     |
                       |                       -----------                                    |-------------|
                       |                                                                      | FINISHED    |
                                                                                               -------------
           -----------------------------------------                    ---------------------
          | Board                                   |                  | SpecialEntity       |
          |-----------------------------------------|                  |---------------------|
          | dimension: int                          |                  | start: int          |
          |-----------------------------------------|                  |---------------------|
          | specialEntities: List<SpecialEntity>    |                  | end: int            |
          |-----------------------------------------|                  |---------------------|
          |                                         |                  |                     |
          | printBoard()                            |                  | getEndPosition()    |
          |-----------------------------------------|  <-----------    |---------------------|
          | hasSpecialEntity(int)                   |                  | getActionPosition() |
          |-----------------------------------------|                   ---------------------
          | getSpecialEntity(int)                   |                 /                       \
          |-----------------------------------------|         ---------                        ---------
          | addSpecialEntity(SpecialEntity)         |        | Snake   |                      | Ladder  |
          |-----------------------------------------|        |---------|                      |---------|
          | getTotalCells()                         |        |         |                      |         |
           -----------------------------------------         | getID() |                      | getID() |
                                                              ---------                        ---------
    ```

### DB Normalisation (RDBMS Only)
  * Sample User Data
    ```
     R1
       -----------------------------------------------------------------------------------------------------------------------
      | book  |  author     | info                                         | publisher    | price ($) | seller (city)         |
      |-------|-------------|----------------------------------------------|--------------|-----------|-----------------------|
      | Drama | James (UK)  | 300 pages (hardcover, 800 gms, fiction)      | Penguin (UK) | 140       | Drake  (Omaha)        |
      | War   | Jacob (USA) | 120 pages (hardcover, 400 gms, non-fiction)  | Harper (USA) | 90        | Drake  (Juneau)       |
      | Drama | James (UK)  | 300 pages (paperback, 500 gms, fiction)      | Penguin (UK) | 115       | Erik   (Marietta)     |
      | War   | Jacob (USA) | 120 pages (hardcover, 400 gms, non-fiction)  | Harper (USA) | 90        | Erik   (Chillicothe)  |
       -----------------------------------------------------------------------------------------------------------------------
    ```

  * Above data has multiple values for an attribute (eg, author, info, publisher), which violates 1NF (ie, an attribute can't have a relation
    as value). Following table is in 1NF.
    ```
     R2
      --------------------------------------------------------------------------------------------------------------------------------------
     | title | author | author_country | pages | cover_type | weight | genre       | publisher | pub_country | price | seller | seller_city |
     |-------|--------|----------------|-------|------------|--------|-------------|-----------|-------------|-------|--------|-------------|
     | Drama | James  | UK             | 300   | hardcover  | 800    | fiction     | Penguin   | UK          | 140   | Drake  | Omaha       |
     | Drama | James  | UK             | 300   | paperback  | 500    | fiction     | Penguin   | UK          | 115   | Erik   | Marietta    |
     | War   | Jacob  | USA            | 120   | hardcover  | 400    | nonfiction  | Harper    | USA         | 90    | Drake  | Juneau      |
     | War   | Jacob  | USA            | 120   | hardcover  | 400    | nonfiction  | Harper    | USA         | 90    | Erik   | Chillicothe |
      --------------------------------------------------------------------------------------------------------------------------------------
    ```

  * Keys
    - Superkey - Set of attributes that uniquely identifies each tuple of a relation. In the above relation R2, title, cover\_type, seller
      and seller\_city can identify every tuple uniquely.
      - All attributes combined is a trivial superkey.

    - Candidate Key - A superkey S, from which removal of 1 attribute results in the new set S' not remaining a superkey (minimal superkey).
      - For R2, title, cover\_type, seller and seller\_city is a minimal superkey and the only candidate key.
      - There is a functional dependency from the candidate key to all the attributes in the relation.

    - Primary Key - A specific choice made from the candidate keys for identifying tuples uniquely.


  * Attributes
    - Prime - All attributes in the set of all candidate keys form the set of prime attributes.
    - Non Prime - All attributes minus prime attributes.

  * Dependencies
    - Functional - In a relation R, a set of attributes (X, Y) are functionally dependent iff each X value in R is associated with only
      one Y value in R. It's given by X -> Y, and Y is said to be functionally dependent on X. Eg, in R2, author -> author\_country is a
      functional dependency, where author\_country can be determined by the author. More examples in R2 -
      - title -> author (but author -> title isn't a FD)
      - title -> pages
      - title -> publisher
      - title -> cover\_type
      - title, author -> author (NOTE: this is a trivial dependency)
      - title, cover\_type -> weight (NOTE: a paperback will have lesser weight - hence, title -> weight is not a FD)
      - publisher -> pub\_country
      - author -> publisher (NOTE: this is a constraint provided by the customer during requirements gathering that a author always works
        for a publisher, and both of them always belong to the same country - the schema design should ideally conform to this constraint,
        however, a change in this constraint by the user due to say, expansion, or relaxed policies will lead to additional work later)

    - Transitive - If functional dependencies X -> Y and Y -> Z exist, and Y -> X is not a functional dependency, then X -> Z is transitive.
      - In R2, title -> author and author -> author\_country are FD - hence, title -> author\_country is transitive.

    - Trivial - A functional dependency X -> Y is trivial if Y is a proper subset of X.
    - Multivalued - See 4NF.

  * Candidate Key Algorithm
    ```
      # takes a list of attributes att and list of functional dependencies fd as input
    ```

  * 1NF - All attributes should have only 1 value. R1 -> R2 is a 1NF conversion.
  * 2NF - Any non prime attribute must not depend on a proper subset of any candidate key.
    - In R2, title, cover\_type, seller, seller\_city are prime attributes.
    - However, multiple non-prime attributes (eg, author, publisher, pages, etc) depend on title, a subset of the candidate key.
    - Also, the non-prime attributes price and weight depends on another subset of candidate key - title, cover\_type
    - A 2NF relation R3, with 3 tables Books, Prices and BookSellers are created as below.
    - In Books, title is the only candidate key, with all other non-prime attributes depending on it.
    - In Prices, title + cover\_type is the only candidate key, with all other non-prime attributes depending on it.
    - In BookSellers, title + seller + seller\_city is the only candidate key - there are no non-prime attributes.
   ```
    R3

    Books
      ---------------------------------------------------------------------------------
     | title | author | author_country | pages | genre       | publisher | pub_country |
     |-------|--------|----------------|-------|-------------|-----------|-------------|
     | Drama | James  | UK             | 300   | fiction     | Penguin   | UK          |
     | War   | Jacob  | USA            | 120   | nonfiction  | Harper    | USA         |
      ---------------------------------------------------------------------------------

    Prices
      -------------------------------------
     | title | cover_type | weight | price |
     |-------|------------|--------|-------|
     | Drama | hardcover  | 800    | 140   |
     | Drama | paperback  | 500    | 115   |
     | War   | hardcover  | 400    | 90    |
      -------------------------------------

    BookSellers
      ------------------------------
     | title | seller | seller_city |
     |-------|--------|-------------|
     | Drama | Drake  | Omaha       |
     | Drama | Erik   | Marietta    |
     | War   | Drake  | Juneau      |
     | War   | Erik   | Chillicothe |
      ------------------------------

   ```

  * 3NF - Any non prime attribute must not have a transitive dependency with the primary key.
    - In R3, Prices and BookSellers are free from any such transitive dependencies (eg, price doesn't depend on the weight or weight doesn't
      depend on the price, when title + cover\_type are taken out of the picture).
    - A 3NF relation R4 with 5 tables is created as below.
   ```
    R4

    Books
      --------------------------------------
     | title | author | pages | genre       |
     |-------|--------|-------|-------------|
     | Drama | James  | 300   | fiction     |
     | War   | Jacob  | 120   | nonfiction  |
      --------------------------------------

    AuthorPublisher
      --------------------
     | author | publisher |
     |--------|-----------|
     | James  | Penguin   |
     | Jacob  | Harper    |
      --------------------

    Publishers
      -------------------------
     | publisher | pub_country |
     |-----------|-------------|
     | Penguin   | UK          |
     | Harper    | USA         |
      -------------------------

    Prices
      -------------------------------------
     | title | cover_type | weight | price |
     |-------|------------|--------|-------|
     | Drama | hardcover  | 800    | 140   |
     | Drama | paperback  | 500    | 115   |
     | War   | hardcover  | 400    | 90    |
      -------------------------------------

    BookSellers
      ------------------------------
     | title | seller | seller_city |
     |-------|--------|-------------|
     | Drama | Drake  | Omaha       |
     | Drama | Erik   | Marietta    |
     | War   | Drake  | Juneau      |
     | War   | Erik   | Chillicothe |
      ------------------------------
   ```

  * BCNF - In a relation R, for every dependency X -> Y, at least one of the following should be true -
    - Y is a subset of X
    - X is a superkey

  * 4NF - For 3 disjoint set of attributes X, Y, Z, and for a particular X[c], if one takes all X[c].Y.Z triplets, and X[c] is found to be
    associated with same Y, irrespective of Z, then there's a multivalued dependency X ->> Y.
    - Assume that with R4, everything is working fine, however, customer notifies that the sellers have expanded their operations. He also
      provides the list of books being sold as per the BookSellers table below (all other tables remain the same).
   ```
    R5

    BookSellers
     ------------------------------
    | title | seller | seller_city |
    |-------|--------|-------------|
    | Drama | Drake  | Omaha       |
    | Drama | Drake  | Juneau      |
    | Drama | Drake  | Marietta    |
    | War   | Drake  | Omaha       |
    | War   | Drake  | Juneau      |
    | War   | Drake  | Marietta    |
    | Drama | Erik   | Juneau      |
    | Drama | Erik   | Marietta    |
    | Drama | Erik   | Chillicothe |
    | War   | Erik   | Juneau      |
    | War   | Erik   | Marietta    |
    | War   | Erik   | Chillicothe |
     ------------------------------
   ```
    - R5 has 3 attributes and all 3 are prime, also part of candidate key (2NF). There's no transitive dependency yet (3NF).
    - Picking up Drake as X[c] and combining with all other Y and Z -
      - Drake.Drama.Omaha
      - Drake.Drama.Juneau
      - Drake.Drama.Marietta
      - Drake.War.Omaha
      - Drake.War.Juneau
      - Drake.War.Marietta
    - There's redundancy - table mentions that Drake sells Drama and War, in 3 tuples. Same for Erik.
      - This a multivalued dependency seller ->> title
   ```
    R6

    BookSellers
     ----------------
    | seller | title |
    |--------|-------|
    | Drake  | Drama |
    | Drake  | War   |
    | Erik   | Drama |
    | Erik   | War   |
     ----------------

    SellerCities
     ----------------------
    | seller | city        |
    |--------|-------------|
    | Drake  | Omaha       |
    | Drake  | Juneau      |
    | Drake  | Marietta    |
    | Erik   | Juneau      |
    | Erik   | Marietta    |
    | Erik   | Chillicothe |
     ----------------------
   ```
    - Note that an assumption is made on the given data by customer that a seller sells all the books he has in all the cities he is
      located in - this assumption can go wrong, eg, if Erik got located in Juneau now, but he isn't selling Drama there. If that was the
      case, R6 shouldn't be created.
