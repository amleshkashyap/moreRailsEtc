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

###### ACID, Locking And Transactions
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

###### Architecture, Data Structures, Configs And Optimisations

##### Other Key Functionalities

#### Basics Of Consistency Models


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
