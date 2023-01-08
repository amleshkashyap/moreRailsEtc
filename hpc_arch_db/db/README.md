### General
  * Types of DB [source](https://www.mongodb.com/databases/types)
    - Hierarchical Databases [since 60s] - Tree like structure, high performance. Eg, Windows Registry
    - Relational Databases [since 70s] - SQL, AWS Aurora, AWS RDS, AWS Redshift
    - Non-relational Databases [?] -
      - Structured documents - MongoDB [JSON based, transactional], AWS DocumentDB
      - Key value stores - Redis [transactional], AWS ElastiCache [not durable], AWS MemoryDB [durable]
      - Graph stores - Neo4j, AWS Neptune
      - Dynamic columns - Cassandra [non-transactional] [more](https://www.mongodb.com/compare/cassandra-vs-mongodb), AWS Keyspaces
      - Crypto - AWS LedgerDBS
      - DynamoDB - it's a combination of multiple DBs, but essentially it's a key value store which can be extended to dynamic columns as well - supports transactions [stores in-memory + SSD].
    - [AWS Offering](https://docs.aws.amazon.com/whitepapers/latest/aws-overview/database.html)

  * ODBC - Open Database Connectivity
    - Standard API for accessing DBMS.
    - Independent of database and OS, portable.
    - Application uses ODBC `driver` manager for issuing commands, which are then passed to the DBMS.
    - Any ODBC compliant application can access any DBMS with a driver.
    - Before ODBC, accessing a DB from another language application [eg, C/Fortran] was difficult - Embedded SQL was created to simplify this by allowing SQL statements in the code which were then
      converted during compile time to kind of a script which would automatically call another function from a library which would actually pass it to the DB.
    - Embedded SQL only allowed having the actual SQL statement to be run, with all values - ie, static SQL. Dynamic SQL within programs happened after this.
    - JDBC is the ODBC for Java - JDBC to ODBC interfaces (called `bridge`) are present to allow Java programs to work even without JDBC.
    - ODBC Drivers -
      - Finding, connecting and disconnecting the DBMS
      - Sending SQL commands to DBMS (also, converting/interpreting unsupported commands from application - eg, if a functionality  is not supported directly by a DBMS can be emulated via the driver
        by another set of functionalities)
      - Convert data from DBMS formats to ODBC standards for further consumption.
      - ODBC drivers needn't work only with DBMS as the data source - eg, some drivers exist for CSV files - they work in several ways, eg, emulating a small database within the driver.
    - ODBC Driver Managers -
      - A layer on top of drivers, often with a GUI, to enumerate, monitor and manager the underlying drivers.
      - Data Source Name - to connect to specific data sources, authentication etc for them - in the underlying drivers.
    - ODBC Bridges - Drivers that use another drivers.
      - ODBC to JDBC and vice versa
      - Others


#### MySQL
##### Basics
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

##### InnoDB
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

###### ACID And Locking
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
    - Gap locks - It's a lock on a gap between index records. Formally, it's the set [(smallest\_index - 1), largest\_index] requested in the query. Consider these -
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

###### Transactions And Deadlocks
  * Consistent Read - A read operation that uses snapshot information to present query results at a given time, irrespective of any intermediate changes done to the record in other concurrent
    transactions. This serves as a primary ingredient to define the isolation level behaviours.

  * Phantom Rows - This occurs within a transaction when the same query produces a different set of rows at different times. These can be prevented by enabling next key locks. As gap locking can
    be disabled fully [except for foreign key and unique key checks], phantom read might be a real problem.

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

###### Architecture, Data Structures, Configs And Optimisations

##### Other Key Functionalities


#### Redis
##### Basics

##### [Transactions](https://redis.io/docs/manual/transactions/)
  * In redis, transactions are truly isolated - no other command will be entertained while a transaction is ongoing - this implies the following wrt the implementation -
    - All transaction statements are queued, and then committed during the isolation period.
    - Since statements are getting queued, any data manipulation which relies on the result of one of these statements will not be correct - hence, such [or any] reads are discouraged.
  * Apart from the above, redis transactions are different from SQL in another key way - they don't rollback as often.
    - SQL transactions need to rollback when integrity constraints aren't satisfied - a feature exists in redis transactions called WATCH which does a very basic check of whether a watched key
      has been modified just before committing a transaction.
  * All the above are present to maintain simplicity - redis is similar to nodejs architecture - single threaded but asynchronous - hence, above was probably the optimal way to have a transaction.

#### MongoDB
##### Basics

##### [Transactions](https://www.mongodb.com/docs/manual/core/transactions/)
