# General
  * [DB Engines](https://db-engines.com/en/ranking)

## Types of DB [source](https://www.mongodb.com/databases/types)
  * Hierarchical Databases [since 60s] - Tree like structure, high performance. Eg, Windows Registry
  * Relational Databases [since 70s] - SQL, AWS Aurora, AWS RDS, AWS Redshift.
  * Non-relational Databases -
    - Structured documents - MongoDB [JSON based, transactional], AWS DocumentDB, GCP BigTable
    - Key value stores - Redis [transactional], AWS ElastiCache [not durable], AWS MemoryDB [durable]
    - Graph stores - Neo4j, AWS Neptune
    - Dynamic columns - Cassandra [non-transactional] [more](https://www.mongodb.com/compare/cassandra-vs-mongodb), AWS Keyspaces
    - Crypto - AWS LedgerDBS
    - DynamoDB - it's a combination of multiple DBs, but essentially it's a key value store which can be extended to dynamic columns as well - supports transactions [stores in-memory + SSD].
  * [AWS Offering](https://docs.aws.amazon.com/whitepapers/latest/aws-overview/database.html)


## ODBC - Open Database Connectivity
  * Standard API for accessing DBMS.
  * Independent of database and OS, portable.
  * Application uses ODBC `driver` manager for issuing commands, which are then passed to the DBMS.
  * Any ODBC compliant application can access any DBMS with a driver.
  * Before ODBC, accessing a DB from another language application [eg, C/Fortran] was difficult - Embedded SQL was created to simplify this by allowing SQL statements in the code which were then
    converted during compile time to kind of a script which would automatically call another function from a library which would actually pass it to the DB.
  * Embedded SQL only allowed having the actual SQL statement to be run, with all values - ie, static SQL. Dynamic SQL within programs happened after this.
  * JDBC is the ODBC for Java - JDBC to ODBC interfaces (called `bridge`) are present to allow Java programs to work even without JDBC.
  * ODBC Drivers -
    - Finding, connecting and disconnecting the DBMS
    - Sending SQL commands to DBMS (also, converting/interpreting unsupported commands from application - eg, if a functionality  is not supported directly by a DBMS can be emulated via the driver
      by another set of functionalities)
    - Convert data from DBMS formats to ODBC standards for further consumption.
    - ODBC drivers needn't work only with DBMS as the data source - eg, some drivers exist for CSV files - they work in several ways, eg, emulating a small database within the driver.
  * ODBC Driver Managers -
    - A layer on top of drivers, often with a GUI, to enumerate, monitor and manager the underlying drivers.
    - Data Source Name - to connect to specific data sources, authentication etc for them - in the underlying drivers.
  * ODBC Bridges - Drivers that use another drivers.
    - ODBC to JDBC and vice versa
    - Others

## Vertical Scaling
  * Normalisation - split columns into separate tables, join via index
  * Increasing compute resources - more RAM and CPU

## Horizontal Scaling
  * Relational Databases - very difficult to scale them horizontally as the data relationship needs to be preserved.
    - Usually, replication is used to balance the load as most operations are read operations, works well if writes are not heavy [hence, replicates quickly] and main database doesn't go down.
    - MySQL provides tools to handle the above - [NDB](https://www.mysql.com/products/cluster/) is not a drop in replacement, involves multiple concepts.
    - Spanner is a different implementation of the same objective though, specifically built for the objective.
    - Differences with InnoDB - https://dev.mysql.com/doc/mysql-cluster-excerpt/5.7/en/mysql-cluster-ndb-innodb-engines.html
    - https://www.quora.com/Why-does-Quora-use-MySQL-as-the-data-store-instead-of-NoSQLs-such-as-Cassandra-MongoDB-or-CouchDB-Are-they-doing-any-JOINs-over-MySQL-Are-there-plans-to-switch-to-another-DB/answer/Adam-DAngelo
    - Ruby lib - https://github.com/tumblr/jetpants

  * Non Relational Databases - the primary reason for their popularity is that they're horizontally scalable due to independence of rows and no JOIN queries.
    - Still needs schema for independent tables to avoid manual validations.

  * NewSQL - some databases have come up which are relational yet make it easier to scale horizontally. Ex. Spanner, CockroachDB, TiDB
    - [Ref](https://softwareengineeringdaily.com/2019/02/24/what-is-new-about-newsql/)
    - Google Spanner probably provides total ordering unlike Lamport clock without extra variables.
    - https://martinfowler.com/articles/patterns-of-distributed-systems/clock-bound.html
    - [Spanner vs CloudSQL](https://stackoverflow.com/a/60413249)
    - First join implementation by cockroachDB - https://www.cockroachlabs.com/blog/cockroachdbs-first-join/
    - CockroachDB's SQL compatibility without atomic clocks - https://www.nextplatform.com/2017/02/22/google-spanner-inspires-cockroachdb-outrun/

  * Database Partitioning and Sharding -
    - Partitioning involves splitting the tables into multiple smaller tables.
    - Sharding is a type of partitioning where tables are split into smaller tables using a shard key, and those tables are then distributed across different physical machines. Schema is replicated.
    - MySQL server allows to very quickly perform horizontal partitioning of tables on the same machine [perhaps across multiple disk volumes too] - that improves performance, and isn't sharding.

  * Distributed Joins -
    - https://www.singlestore.com/blog/scaling-distributed-joins/
    - https://ignite.apache.org/docs/latest/SQL/distributed-joins
    - https://stackoverflow.com/questions/59811150/how-do-database-joins-work-in-a-distributed-relational-database

## MySQL
### Basics
  * Basic features -
    - Written in C/C++ - tested on multiple architectures, with multiple compilers.
    - Tested using commercial and open source memory leak detectors.
    - Multithreading using kernel threads to utilize hardware directly.
    - Transactional [InnoDB] and non-transactional [MyISAM] storage engines.
    - Storage engine is customisable - useful for in-house databases with specific needs but SQL based API.
    - Fast thread based memory allocation. Very fast join operations. In-memory hash table implementations which serve as temporary tables [like redis?]
    - Very fast SQL functions - almost no memory allocation after query initialization.
    - Eg, some user has 2 lakh tables and 5 billion rows.
    - Supports 64 indexes per table [1 to 16 columns per index].
    - Connections can be made via multiple protocols [eg, TCP, unix sockets, named pipes, etc]
    - ODBC/JDBC/ADO.NET interfaces available for applications' ORM's.
    - Multiple language character sets supported - in fact, optimized sorting functions for a particular charset is used while operating.
    - [Tools](https://dev.mysql.com/doc/refman/8.0/en/tools-used-to-create-mysql.html)

  * [New Features](https://dev.mysql.com/doc/refman/8.0/en/mysql-nutshell.html) - outside scope currently.
  * [Non Portable Features](https://dev.mysql.com/doc/refman/8.0/en/extensions-to-ansi.html)
  * [Foreign Key Problems](https://dev.mysql.com/doc/refman/8.0/en/ansi-diff-foreign-keys.html) - foreign key restrictions are relaxed in InnoDB which may lead to problems.
  * Handling Constraints -
    - Invalid/improper data is rejected and the statement is aborted [SQL strict mode] in v8. In v5, default was to perform a coerce and convert to the closest valid value [ruby-like].
    - Enum and Set - changes in default behaviours for errorneous insertions.
    - Primary Key and Unique Index - Most errors occur due to violation of primary/unique/foreign key constraints, and in transactional engines like InnoDB, this leads to a rollback. For MyISAM,
      it would lead to a halt of processing for any further rows. Options are available to log the insertions/updates and show warnings etc.
    - Foreign Key - MySQL supports ON UPDATE and ON DELETE foreign key refs in CREATE/ALTER TABLE statements with these options - RESTRICT, CASCADE, SET NULL, NO ACTION. SET DEFAULT is supported in
      MySQL (as mentioned above, there's no uniqueness contraint on foreign keys in MySQL) but rejected by InnoDB (why? which constraint is violated?)

### InnoDB
  * Benefits -

  * Best Practices -
    - Primary key for every table.
    - Use joins when data is pulled from multiple tables. MySQL enforces foreign key columns to be indexed which improves performance. Furthermore, all delete and update operations are propagated to
      the associated tables.
    - Turn of autocommit - are they sequential? [as it's mentioned that storage speed can limit it]
    - Sets of DML operations can be grouped into transactions manually via the START TRANSACTION and COMMIT. Avoid huge insert/delete/update that don't commit for a long time.
    - Avoid LOCK TABLE statements - that defeats the purpose of InnoDB [unless there's too many deadlocks which can't be fixed via the code - rare]. InnoDB is supposed to carry out multiple
      concurrent transactions, modifying the same table, not losing reliability and performance - all by virtue of acquring row level locks.
    - innodb\_file\_per\_table should be enabled [default in v8] to keep indexes and metadata in separate files.
    - Evaluate if data and access pattern can benefit from InnoDB's table/page compression - how?
    - Run the server with --sql\_mode=NO\_ENGINE\_SUBSTITUTION to avoid table creation with unnecessary storage engines.

#### ACID And Locking
  * Double Write Buffer - A storage area where pages flushed from buffer pool are written before being written to the final position in the data files [ie, just before final storage]. This is for
    improving the chances of protecting data during a crash. Since this write is done using a single system call, perf overhead is low.

  * ACID
    - Atomicity - via transactions. See autocommit setting. Related - COMMIT/ROLLBACK.
    - Consistency - double write buffer, crash recovery
    - Isolation - via transactions and locking. See `data_locks` and `data_lock_waits` for lock info.
    - Durability - involves interaction with another unreliable entity. See `innodb_flush_log_at_trx_commit`, `sync_binlog`, `innodb_file_per_table`. Others -
      - Write buffer of storage device.
      - Battery backed cache in storage device.
      - Underlying OS and it's support for fsync [for double write buffer efficiency].
      - Uninterrupted power supply to all servers and storage devices.
      - Backup strategy.
      - Distributed systems - characteristics of the data centers, network connection between data centers.

  * Locking
    - Shared and exclusive locks - usual. It looks like these may not be used by default [instead record locks are used with S and X versions]. Clarify.
    - Intention locks - shared (IS) and exclusive - usual. It looks like these may not be used by default [instead, gap locks are used]. Clarify.
    - Record locks - this is always on the index records, if a table has no indexes, then a hidden index is created for locking. Benefit is speed.
    - Gap locks - It's a lock on a gap between index records. Formally, it's the set ((smallest\_index - 1), largest\_index] requested in the query. Consider these -
      - `select * from t where c1 between 10 and 20;` - mysql needs to know why this query is made [for read or update] and then might assign a stronger `gap S-lock` (than IS lock) to prevent any
        insertions in these rows - this is done to prevent a change in indexes which can effect the subsquent grant of records locks. This kind of statements will always lead to a gap lock whether or
        not there's any indexing on the columns involved. Gap lock acquired for indexes (9, 20]
      - `select * from t where c1 = 10;` - this will not lead to a gap lock before the record lock, iff, c1 has a unique index on it. For ex, if there was no indexing on c1, or c1 was part of a multi
        column index, that would've led to a gap lock.
      - Gap locks have 2 inconsistent characteristics - (a) share and exclusive gap locks have the same privilege, (b) gap locks can be granted to different transactions even if some records are
        common between them. Couple of reasons given - gap locks are one step before the actual locks which will make the update to DB - hence, they're safely granted even though there's an
        overlap [subsequent locks will not be granted though]. Also, if an index is purged while 2 transactions hold conflicting gap locks, the locks will need to merge [?].
      - Gap locks can be disabled for performance wrt search/scan operations - however, they can't be disabled for foreign key and unique key checks.
      - Gap locking leads to some behaviours - ??
    - Next key locks - a combination of record lock on the index record and gap lock on the gap before the index record.
      - InnoDB performs row-level locking by setting a shared/exclusive lock on the index records encountered while searching/scanning the table's index - these are record locks [RS/RX].
      - With next key locks, even the gap before the locked indexes are locked with the respective gap locks. This way, if a transaction holds a lock on an index pos R, then another transaction can't
        insert a new index record in the gap preceding R in the index order.
      - Also, in situations when R is the largest pos, a next key lock must also lock the gap after R so that another transaction doesn't insert after R - example is given in below lock.
    - Insert intention locks - A type of gap lock set by INSERT operations prior to insertion.
      - This is the last level lock to be obtained before the actual X lock is obtained.
      - This signals an intent to insert to an index so that multiple transactions inserting in the same gap need not wait if they're inserting at different positions in the gap.
      - Eg, client A creates a table and inserts indexes 90 and 102, followed by starting a transaction and selecting rows > 100 for update. client B starts a transaction to insert index 101.
        One of the possible executions for the above is that client B acquires a insert intention lock and waits for X locks. Now client A might get a X lock for 102, or client B might get the X lock
        to insert to 101, post which client A gets the X lock for 101 and 102. In either case, both client transactions would've acquired a gap lock for the gap before 102 [since 101 wasn't present].
      - Now if client B acquires X lock and inserts 101 while client A was waiting, then a violation of isolation principle has occurred as client A encounters a phantom row when it resumes the update.
        Hence, with next key locks [which I presume can't be fully disabled to prevent such violations], client B will never be allowed to insert before client A has completed [this is a use case for
        next key locks]. Also, the next key lock in this case must be acquired after 102 for client A, so that another client C is not able to insert after 102 [as the query is for > 100].
    - AUTO-INC locks - Acquired by transactions for insertion into tables with AUTO\_INCREMENT columns. See `innodb_autoinc_lock_mode`.
    - Predicate locks -

  * Locks Set By Different Statements -
    - Select..From -
    - Select..For Update, Select..For Share -
    - Select..For Update, Select..For Share, Delete, Update -
    - Select..For Update -
    - Update..Where -
    - Update -
    - Delete From..Where -
    - Insert -
    - Insert..On Duplicate Key Update -
    - Replace -
    - Insert Into T Select..From S Where.. -
    - Lock Tables -

#### Transactions And Deadlocks
  * Consistent Read - A read operation that uses snapshot information to present query results at a given time, irrespective of any intermediate changes done to the record in other concurrent
    transactions. This serves as a primary ingredient to define the isolation level behaviours.

  * Phantom Rows - This occurs within a transaction when the same query produces a different set of rows at different times. These can be prevented by enabling next key locks. As gap locking can
    be disabled fully [except for foreign key and unique key checks], phantom row might be a real problem.

  * Isolation Levels [From 1992 standard] -
    - Repeatable Read - Default level in InnoDB. Consistent reads within a transaction read the snapshot established by the first read [this is similar to what is offered by Redis transactions, hence
      they don't recommend any reads within a transaction]. This offers higher concurrency as transactions don't need to communicate the changes.
    - Read Committed - Each consistent read within/across a transaction sets and reads its own fresh snapshot. Snapshot is reset based on the last commit to the record. This is slower but more
      accurate.
    - Read Uncommitted - Each consistent read can have uncommitted versions of the record from other transactions [which may eventually rollback] - this can lead to dirty reads. This maybe slower
      and can be less accurate if there are frequent rollbacks.
    - Serializable - This is similar to repeatable read. If `autocommit` is enabled, then every SELECT statement is a transaction.

  * Transaction Scheduling -
    - Contention Aware Transaction Scheduling is used to prioritize transactions waiting for locks. It considers the number of transactions blocked by a transaction and assigns weights.
    - When weights are equal, then the longest waiting transaction has the priority.
    - Earlier, a FIFO algorithm was used for scheduling for situations with low contention - this is completely removed in v8.
    - See - TRX\_SCHEDULE\_WEIGHT (scheduling weight) column in INFORMATION\_SCHEMA.INNODB\_TRX table. TRX\_STATE table indicates transaction state. INNODB\_METRICS for these metrics - 
      - `lock_rec_release_attempts` - attempts to release locks - since locks are released one by one in the second phase of a transaction.
      - `lock_rec_grant_attempts` - attempts to grant records locks.
      - `lock_schedule_refreshes` - number of times wait-for graph was analyzed to update the TRX\_SCHEDULE\_WEIGHT.

#### Architecture, Data Structures, Configs And Optimisations

### Other Key Functionalities
  * Postgre vs MySQL - implementation of join can lead to one being chosen over the other as the first choice when a horizontal partitioning library is to be built?
    - https://medium.com/@hnasr/postgres-vs-mysql-5fa3c588a94e
    - https://dba.stackexchange.com/questions/49232/postgresql-vs-mysql-which-is-better-for-join-queries-writing-datainserts
  * Generic - why a complex system can't be made simpler by breaking it - https://towardsdev.com/dont-make-your-apis-simple-377e60ae8840
    - Goal of simplification is to connect the dots faster [not to simplify the system itself], not leaving it for a select few to ever understand and monopolize!!


## Redis
### Basics

### [Transactions](https://redis.io/docs/manual/transactions/)
  * In redis, transactions are truly isolated - no other command will be entertained while a transaction is ongoing - this implies the following wrt the implementation -
    - All transaction statements are queued, and then committed during the isolation period.
    - Since statements are getting queued, any data manipulation which relies on the result of one of these statements will not be correct - hence, such [or any] reads are discouraged.
  * Apart from the above, redis transactions are different from SQL in another key way - they don't rollback as often.
    - SQL transactions need to rollback when integrity constraints aren't satisfied - a feature exists in redis transactions called WATCH which does a very basic check of whether a watched key
      has been modified just before committing a transaction.
  * All the above are present to maintain simplicity - redis is similar to nodejs architecture - single threaded but asynchronous - hence, above was probably the optimal way to have a transaction.

## MongoDB
### Basics
### [Transactions](https://www.mongodb.com/docs/manual/core/transactions/)

## [Spanner](https://cloud.google.com/spanner)
  * Reference - https://static.googleusercontent.com/media/research.google.com/ro//archive/spanner-osdi2012.pdf

### Basic Features
  * Scalable, multi-version, globally distributed and synchronously replicated.
  * Auto resharding of data across machines [with increasing data or changing number of servers].
  * Auto migration of data across machines [and datacenters] for load balancing and fault tolerance.
    - This is important because otherwise, developers have to manage it [so that their joins work].
    - An example from a similar DB - https://www.quora.com/How-does-TiDB-compare-with-MySQL/answer/Li-Shen-137
    - Ex - https://www.quora.com/Is-MySQL-good-for-a-large-database/answer/Greg-Kemnitz
  * Focus - manage cross datacenter data replication.
  * Configs - which datacenter contains what data, control read latency [distance of datacenter from user], control write latency [distance between replicas], control availability, durability and
    performance [number of replicas].
  * Consistency features - externally consistent read/writes, globally consistent read at a timestamp across databases.
  * How's - stored in semi relational schemas, versioned data (timestamped at commit to allow configurable garbage collection and allow old reads if needed), transactional, SQL like interface.
    - Consistency achieved via globally meaningful [?] commit timestamps even in distributed servers - how??
    - Provides serializability guarantees at global scale - if transaction T1 commits before T2 starts, then commit timestamp ct1 < ct2.
    - The distributed timestamp consistency which is a known problem wrt the mechanical clock error - is the core problem handled for doing the above.
    - TrueTime API - exposes uncertainty so that the DB can adjust it's operations, if high, then DB slows down. Goal is to keep the uncertainty small - GPS and atomic clocks - [?]

### General Resource Hierarchies
  * GCP -
    - region -> datacenters -> zones <-> cluster
    - A zone is a set of servers [a compute cluster] located in some room of a datacenter, with a risk of one/all of them going down.

  * AWS -
    - region -> availability zones <-> cluster
    - One datacenter is an availability zone (or cluster).

### Details
  * A deployment is called universe -> running globally [hence finite universes]
    - Divided into set of zones - a zone is roughly similar to a BigTable instance.
    - A zone has a zonemaster which assigns data to multiple spanservers within the zone, which serves it to the clients.
    - A zone also has a location proxy used by clients to find their spanserver.
    - Each universe has a universemaster to monitor zonemasters, and placement driver to communicate with spanservers to move around the data as required.

  * Spanserver -
    - Handles thousands of tables [similar BigTable tablet] which also hold the global timestamp.
    - Tablet state is stored in B-Tree like files and write-ahead log inside Colossus.
    - A spanserver implements paxos state machine on top of each tablet to support replication - earlier, multiple paxos state machines per tablet were tried and discarded due to high complexity.
    - Paxos has long lived leaders and time based leader leases, with length of 10s [default] - paxos writes are logged twice - in tablet logs and paxos logs.
    - Paxos group is a collection of tablet replicas - reads are from any sufficiently updated replica and writes invoke the paxos protocol at leader.
    - At the leader replica spanserver, a lock table is for concurrency control - lock table has state for 2PL, mapping key ranges to lock state
    - Long lived transactions are implemented which perform poorly for optimistic 2PL in presence of conflicts.
    - At the leader replica spanserver, a transaction manager is implemented for distributed transactions - for transactions within a paxos group [more frequent], this manager is skipped.
    - For transactions involving more than one paxos group, group leaders coordinate to perform 2P commits - they elect a `coordinated` leader (from the `participant` leaders).
    - Like all states, transaction manager state is also stored and replicated among the tablets of the paxos group.

  * Directory -
    - Apart from key value mappings, a set of contiguous keys with a common prefix (called `directories`) are also stored by a paxos group. This is actually the unit of data in Spanner, and any
      data movement takes place directory-wise - as contiguous data is more likely to be accessed consecutively, it makes sense to organise them. All data in a directory has same replication
      configuration.
    - Spanner might move directories for (note: expect 50MB directories to be moved within few seconds - this is handled by Movedir background task, which also handles numReplicas) -
      - Load balancing by moving from one paxos group to other.
      - Put directories frequently accessed together in the same paxos group.
      - Move directories to a group closer to it's accessors
    - Last two points above implies that the performance optimisations are primarily driven by access pattern and distance between the user and the data (or that's what they've observed over years).
    - The organization of contiguous data as directories within a Spanner tablet reflects a key departure from BigTable tablet.
    - Movedir is optimized - it first moves almost all the data, then performs a transaction to move the remaining small amount of data and update the metadata of both affected paxos groups.
    - Directories are the unit whose geographic placement can be specified by users. Admins can -
      - Control the number and type of replicas
      - Geographic placement of replicas
      - Eg, an app may store each end user's data in it's own directory, with user A having 3 replicas in EU, and user B having 5 replicas in NA [how?]

  * TrueTime API - the key to having a truly distributed DB based just on timestamps!!
    - TT.now() - returns TTInterval (earliest, latest) which guarantees to provide an interval between which this TT.now() was invoked.
    - TT.after(t) - true if t has definitely passed
    - TT.before(t) - true if t has definitely not arrived
    - TrueTime is implemented by a set of time master machines per datacenter and a timeslave daemon per machine.
    - Most time masters have a GPS receivers with dedicated antennas and are separated physically to reduce effects of antenna failures.
    - Remaining time masters are equipped with atomic clocks [Armageddon masters]. Both masters have similar cost. A master can evict itself if it's diverged significantly from other masters.
    - Each timeslave daemon polls multiple masters, in the same datacenter, some Armageddon masters, as well as in other datacenters. They use Marzullo's algo to reject liar masters and synchronize
      local clocks with the non-liars.
    - Daemons poll every 30 seconds, and the worst case clock drift is 200micro sec/sec, giving a max bound of 6ms (+1ms for communication, bounded at 7ms)
      - But this can fail if the underlying assumptions about the clock correctness at master doesn't hold, or the communication delay is exceeded.
      - They acknowledge a datacenter wide growth in the bound in the face of time master unavailability and localized growth in the bound in case of communication delays.

  * Concurrency Control - how TrueTime is used for concurrency control and strong (external) consistency guarantees.
    - Distinguish Paxos writes from Spanner client writes.
    - Supported operations -
      - Read write transactions
      - Read only transactions
      - Snapshot read with a client provided timestamp
      - Snapshot read with a client provided bound
    - Read only transactions must be declared so, rather than calling them read write transaction without a write - this helps executing them at a system chosen timestamp without locks.

  * Add More

### Bigtable
  * A key value like DB, with one row key [the primary id] having multiple column families, each column family having multiple unique columns.
    - Every column can have multiple cells, where timestamps and corresponding data is stored providing additional information and recovery option.
    - How are these timestamps different from the one captured by Spanner?
  * [Ref](https://cloud.google.com/bigtable/docs/overview)
  * [vs Cassandra](https://cloud.google.com/bigtable/docs/cloud-bigtable-for-cassandra-users)
  * A BigTable instance is organized as containing one or more clusters, each cluster having one or more nodes. Table and clusters belong to an instance.
    - Each cluster is located in one zone - but one region can have multiple zones [and hence clusters].
    - Each instance also has a frontend server.
    - Each table [or tablet] is mapped to one node, and is stored in a colossus unit with multiple SSTables and write ahead buffer.
  * Request from client goes to frontend server, which sends it to the cluster, which has nodes handling part of all the requests. Nodes are the concurrency unit which can be increased if required to
    increase cluster throughput. Clusters can be replicated for fault tolerance and load balancing.
  * A table is sharded into blocks of contiguous rows [each block is a `tablet`]. Tablets are stored on Colossus, in SSTable format. One tablet is associated with one node [so increasing nodes will
    lead to readjustment]. All writes are stored in shared logs of Colossus once acknowledged by Bigtable.
  * Data is never stored in nodes, it contains only pointers to the set of tablets mapped to it.
    - This leads to highly performant readjustment of nodes as well as migration in the face of failure.
    - Failure doesn't lead to lost data, but pointers are lost - how are they retrieved?
  * Load balancing - Bigtable zone consisting of multiple clusters is managed by a single process which balances workloads/data within a cluster. It automatically splits large and hotspot tablets
    into half and merges small and less accessed tablets together, followed by readjusting them between nodes. Automated handling in face of traffic is a big positive of using this.
    - It's useful to understand the stored data keys and choose the appropriate row key so that writes are evenly distributed.
    - Related rows can be grouped together for increase read efficiency.
  * This is not SQL compliant ofcourse.

### Colossus
  * Lustre filesystem -
    - One or more metadata servers (MDS) - each having one or more metadata target (MDT) device - to store namespace metadata like filename, directory, access permission and file layout. Involved only
      in pathname and permission checks, avoiding major computations leading to I/O bottlenecks in face of high traffic. Directory subtrees are stored in a distributed fashion on MDTs.
    - One or more object storage servers (OSS) - each storing file data on one or more object storage target (OST) devices - typically 2-8 OST per OSS, where each OST handles a single local disk FS.
    - Clients - who access the data. Lustre presents all clients with a unified namespace of all files and data, and allows concurrent and coherent read/write access to the underlying FS.
    - MDT, OST and client can either reside on a single node, or across nodes. One MDT and OST can either be a part of single FS, or multiple MDT + OST can be part of different FS on a single node [?].
    - When spread across different nodes, they can communicate via LNet which internally uses different interconnection channels, from Intel's Infiniband to custom network of Cray.
    - More details - out of scope. [Ref](https://en.wikipedia.org/wiki/Lustre_(file_system))
  * [Ref](https://cloud.google.com/blog/products/storage-data-transfer/a-peek-behind-colossus-googles-file-system)
  * Control plane consists of metadata server [like Lustre MDS], custodians, curators and file system server.
  * Client library - for any application to interact with colossus in order to get storage space.
  * Metadata server - Curators store the metadata in this entity which somehow uses BigTable.
  * Custodian - background storage manager - tasks like disk space balancing and RAID reconstruction. Handles durability, availability and efficiency.
  * Provides a shared storage pool for all applications which they think as isolated file system.
  * Can juggle the workload types based on latency needs, eg, tasks not critical in time are provided resources which are idle [but are for a different task]?
    - Apps use different storage tiers by specifying their I/O, availability and durability requirements.
  * Amount of hardware installed is very high and some or the other unit will fail, requiring strong fault tolerance provided by Colossus.
  * [Ref2](https://news.ycombinator.com/item?id=32674678)

### Terms
  * GPS clock - Obtained from radio stations. Combines time estimates from multiple satellite atomic clocks with error estimates provided by multiple ground stations.
    - GPS Disciplined Oscillator - Combination of GPS receivers and stable oscillators whose output is controlled to agree with signals from GPS and GNSS satellites.
    - Accurate to nanoseconds and a good enough workaround for timing applications.
    - Used for UTC time calculation.
  * Atomic clock - [out of scope](https://en.wikipedia.org/wiki/Atomic_clock). Uncertainty of 1 second in 300 million years.
  * Paxos -
  * Bigtable [DB] - not so good when schema is complex and evolving constantly, need strong consistency during wide area replication.
  * Megastore [DB] - semi relational, synchronous replication, low write throughput.


## Other Modern DBMS
### SpiceDB
  * Ref - https://github.com/authzed/spicedb
  * https://authzed.com/blog/what-is-google-zanzibar
