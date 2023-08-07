## General

### Trivia
  * Data storage to various components is a daily task.
  * Let's say someone has 5000 images stored in an android phone's internal storage [OnePlus] and they want to move them to another storage. Considerations -
    - Created at - images have been captured across many months, and during the time, other data has been added to internal storage as well.
    - Name - even though images have structured filenames, so do some other files created in internal storage [eg, videos].
    - Transfer To And Via -
      - Laptop - wire, bluetooth
      - USB Stick - directly inserted to phone
      - External Hard Disk Drive - HDD connected to laptop via cable and phone connected to laptop via cable
      - Memory Card - in the same phone
      - Cloud Storage - via the internet
      - Another Phone - via wire (?), bluetooth, apps over wifi, other mediums (?)

  * It's worth noting that one could see a considerable amount of speed differences when transferring from phone's internal storage to external HDD via laptop -
    - What causes this? It's obviously about the storage and access patterns, ex -
      - Files on internal storage are sorted by Name in Windows laptop - when one moves the first 250 files, it's exceptionally slow, but if they move the last 250 files, it's very fast at the
        beginning and remains like that upto a threshold.
      - If one changes the sorting order in UI, then does it change anything? [NOTE: sorting orders like Created At/Modified At are pretty much same as Name because of the names assigned to the
        images and hence, not much changes in few basic checks]
      - When one changes the number of files to transfer, does the order matter?
      - When one puts the files in directories [ie, another internal, faster move], then does it help?
      - Can one change the wire types or interfaces? (not so easy on a laptop)
      - Worth asking - OS GUI sorting options wrt actual layout on disk, how can the concepts of DBMS be utilized here or in general [or are they already being utilized], indexing and reindexing in
        the middle of data movement, why data move operation doesn't delete the data immediately after moving, etc.
    - What options does one have to achieve uniform speed [or no options]?
    - How much does this transfer rely on storage's storing and access algorithms?
    - What are the advantages and applications of answering the above questions?


## Filesystem
  * Filesystems are the tools which help users in creating, viewing and maintaining a coherent and readable organisation of their data stored in some storage medium - facilitated via OS which may
    also do it simply using RAM, instead of having a database of it's own (not possible always though).
    - In the lustre filesystem discussed earlier, concepts of metadata store and directory store were discussed which will be detailed.
    - Without a filesystem, it won't be possible to know what data is stored where in the storage.
    - Filesystems can organize data in various settings and interconnects - eg, local storage, via network, a mapping to another filesystem, dynamic process data (procfs)
    - Filesystems don't provide the consistency and duplication related features of DBMS and only useful for ease of storage rather than structured data storage and processing.
    - While filesystem and storing something in disk are isolated concepts, one can see the files stored by DBMS on their machines.
      - [More](https://hidetatz.medium.com/how-innodb-writes-data-on-the-disk-1b109a8a8d14)
    - This lack of structure may explain why a structure like BTree (ie, sorted storage) wasn't the first choice for filesystems in earlier days.
    - Ex. tmpfs, ext4, vfat, overlay

  * Layers (Basic)
    - User Interface Layer - provides APIs like open/close/write. Manages file table entries and per process descriptors. Provides file access, directory operations, security and protection.
    - Virtual Layer - can support multiple physical file systems via a single UI layer.
    - Physical Layer - processes data blocks being read/written, buffering and memory management, placement of blocks in storage, interact with device drivers, etc.

  * Disk and FS Organisation
    - Sector - it's the smallest unit of information storage on the physical disk. It is also used as a logical entity by softwares, mapping 1:1 with a physical disk sector. A disk can read/write
      one full sector only.
    - Track - a continuous set of sectors on a physical disk -> seek time is about the mechanical pointer traversing from one track to the required track.
    - Block (or Cluster, as in FAT and others) - a logical set of sectors, used by filesystems as the upper limit of data to fetch/output at once - this may form the basis of parameters to be used
      in B-Tree implementations. The set of sectors needn't represent contiguous sectors.

  * inode
    - Describes a file system object, eg, file or directory - it's a single data container or a datatype and can be the object stored in other aggregation structures.
    - Stores attributes (eg, last change, access, modification, owners, permissions) and disk block location of above object's data.
    - In older filesystems, inodes were allocated at the time of creation in a fixed storage space, leading to fixed number of inodes - now, it's allowed to grow.
    - inodes don't contain hard link names, just the metadata.
    - Unix directories are list of structures - each of which contains one filename and one inode number - filesystem driver searches for a filename and gets the inode number for more details.

  * POSIX inode
    - device id - identifies the device containing a file (defines the scope for uniqueness of a file - ie, device id + a unique serial number within a device can uniquely identify a file)
    - file serial number
    - file mode - file type, how the owners of file can access it (eg, owner, group, others)
    - link count - how many hard links point to the file
    - user id of file's owner
    - group id of file
    - device id of file if it's a device file (device driver)
    - size of file
    - timestamps - inode change time (ctime), file change time (mtime), last accessed time (atime)
    - preferred I/O block size
    - number of blocks allocated to the file

  * inode Characteristics
    - Files can have multiple names - they can hard link to the same inode. Symbolic links are files themselves, which point to other files/directories.
    - Persistence - inodes with no hard links are garbage and freed like a garbage collector does - removal is deferred.
    - Conversion and directory path removal - when a program opens a file, OS converts it to inode number and discards the filename - the filename of the opened file can't be accessed from the opened
      file. Path of the current working directory is accessible because of the inode of current directory will be present in parent directory (going backwards).
    - Directory hard linking - directories were allowed to be hard linked, hence the DS was a directed graph instead of a DAG. These are usually not allowed now due to possible confusions.
    - When moving a file to a different directory in same filesystem, or altering the disk location due to fragmentation, inode number remains same - this allows for a lot of flexibility which lacks
      in other filesystems like FAT.
    - Above also provides other flexibilities - eg, allow a running process to access a library file even when other process is replacing it -
      - During replacement, a new inode entry is created (without changing the number, or the existing one is updated with a lock in place, barring others from reading/writing), which is then used for
        subsequent accesses for the filename, however, the older entry exists and is not cleared from the central store and disk till all processes using it have not completed.
      - Above should be atomic. Allows for seamless upgrades without affecting running processes.
    - Inlining - if the data in a file is very small, then it might as well be stored in the inode itself to save storage space and provide more perf - this is inlining. eg, ext2 and above use this
      often for storing a symbolic link completely in an inode (for data < 60B - fast symlinks). ext4 provides an inline_data config for similar purposes.
    - FAT - FAT and derivatives change the data structure as well during relocation, and might require more adjustments (because of a missing centralised management system with invariants like inode).
      - Used linked list and arrays which worked well as storage sizes were small during the time.
    - NTFS - has a master file table storing files in B-Tree - files have ID, the timestamps, device ID, reference count, file size, permissions and other attributes. Also has concept of inlining.
      - This is used even today in Windows.
    - HFS - macOS - based on B-Trees.
    - ext2 -
      - Block groups - contains superblock, block group descriptor table, block bitmap, inode bitmap, inode table, and data blocks.
      - Superblock - crucial data for booting the operating system - copies are made in multiple block groups.
      - Group Descriptor Table - stores group descriptors which contain location of block bitmap, inode bitmap and start of inode table for every block group.
      - ext3 and ext4 had implemented HTree (similar to BTree).
      - Currently, the standard is - [Btrfs](https://en.wikipedia.org/wiki/Btrfs) - will return to this.
    - It wouldn't be surprising if more system/applications software use similar concepts for their features/guarantees.

  * Other Features
    - Space management - manage fragmentation
    - Filenames
    - Directories

  * Types
    - Disk - FAT, ext, NTFS, UDF, etc
    - Flash - JFFS, YAFFS, LogFS
    - Tape -
    - DB - Hadoop and GFS (replaced by Colossus), 
    - Transactional - 
    - Network Based -
    - Others - 

  * Limitations
    - Converting the filesystem type
      - In place conversion - migration can be conservative. eg, tools for FAT -> NTFS migration are available but not the reverse. ext2 <-> ext3, ext3 <-> btrfs, ext4 <-> btrfs, etc. ext3 -> ext4
      - Different filesystem - migrations like FAT to ext2 are possible.
    - Long paths and filenames - compatibility and robustness of the migration tool are critical.


## Some Topics
  * [Source](https://dl.acm.org/doi/pdf/10.1145/3212477.3220266)

  * Familiarity with database and storage internals facilitates architectural decisions and helps in explaining why a system behaves in a certain way, troubleshoot and fine tune systems, etc.
  * Majority of systems use 2 designs for storage - read-optimized B-Trees and write optimized LSM (log-structured merge).


### B-Trees
  * Used in databases (InnoDB, Postgre) and file systems (HFS, ext4).
  * Reduction of tree depth is a frequent operation - often using rotation (what are the efficient algorithms?)
  * B-Trees are generic binary trees with following properties -
    - Sorted - sequential scans, simplifies lookups - how?
    - Self Balancing - explicit balancing not required during insertion/deletion - split a full node into 2 when full, merge nodes when occupancy below threshold
    - Gurantees logarithmic lookup
  * What is stored in the nodes - it can't be just numbers

### LSM
  * Data is stored in a table in memory, organised as a fast DS like BST or skip list - when the size of this table reaches a threshold, contents are flushed to disk.
  * Read operation involves reading from disk as well as the table in memory and collating the results which are propagated.
  * SSTables (Sorted String Tables) - stored as index and data blocks - index block contains keys mapped to data block pointers, pointing to the actual record.
    - Index table often implemented using B-Tree or hash table for efficient storage/retrieval.
    - Used for memory resident tables.
    - Immutatble - hence, written sequentially and hold no empty spaces for in place modifications.
    - Merge sort might be used to collate results across SSTables and disk - a compaction is often performed using merge sort to clean data as there might be versioned data, redundant data which
      got deleted, etc that needn't be present or written to disk.
  * Bloom Filters - it provides false positives but doesn't provide false negatives - ie, if it says that a key is not present, then it's definitely not present.
    - A key might be in SSTable or definitely not in SSTable.
  

## RAID Basics
  * TODO


## Storage And Databases
  * [Source](https://dl.acm.org/doi/pdf/10.1145/2693193.2696453)
  * Having all features in a single database will lead to performance cost, apart from complexity.

### HDD
  * Interface Bandwidths -
    - SATA - 750 MB/s - used with HDD/SSD
      - With 7200 RPM HDD - 250 random locations per second with a seek time of 4 ms - upto 150 MB/s
      - Sequential read/write after seeking to the location are much faster due to algorithms being optimised for that from the beginning
      - With SSD - SSD seeks are upto 60x faster than HDD, allowing upto 3-10x bandwidth over HDD with same SATA spec
      - Storage cells in SSD's have a fixed lifetime and can handle a limited number of writes before failure - SSD's have specialized firmware that spreads writes across disks, performs garbage
        collection and other bookkeeping operations.
    - PCI 3.0/4.0 (NVMe) - 40/64 GB/s - used with SSD and others
    - Memory Bus - 14.9 GB/s - used in RAMs

### Page Cache
  * Based on the same old principle - same/nearby data will be read/written frequently in a short time period - more true for databases.
    - OS kernel stores the contents of files in memory pages, mapped to disk.
    - Uses the write-back mechanism.
    - Read will return data from memory cache if data is synchronized with disk [ie, some other program hasn't changed the data in that disk location].
    - Gains are huge, for both read and write operations (writes depending on the replacement policy implemented).

  * Pitfalls -
    - Can lead to loss of data during unpredictable failures - lookout for databases which use page caches excessively.

  * Cache Coherence - fastest and most energy efficient way to maintain data consistency.
    - More speed may come at increased implementation complexity (ie, race conditions) and more energy consumption (more computational threads/hardware)
    - Snooping based - write update and write invalidate - doesn't scale well
      - MOESI - modified, owned, exclusive, shared, invalid - implementation dictates if a cache is writing another owned line, then others sharing it will invalidate or update their copies.
      - MESIF - MESI + forward - forward state is for clean lines, and it can be evicted without notice, unlike owned state - data in S and F states are clean. Reading from RAM is S state.
    - Directory based - various kinds of matrices to reduce storage and lookup costs.

  * Cache Replacement - any fixed size cache implementation must have efficient implementation of replacement policy/algorithm - much better if configurable based on application.

### Databases
  * Considerations -
    - Data model
    - API
    - Transactions
    - Persistence
    - Indexing

  * Data Models
    - Relational - Conserves hard disk by minimizing data duplication (normalisation). Reduced disk costs have made this less lucrative.
      - Storage model doesn't help with storing/retrieving huge amounts of data - there's no way to get data from huge storage without iterating through the indexes (or worst case, the actual stored
        rows directly) - it's also going to be very slow when joining and sorting results when the stored data and results are huge.
      - Efficient storage, schema driven consistency, more tools and community support - slow and more complex, with more tuning options to learn.
    - Key Value - Low complexity, efficient storage model (better compression), low runtime overhead.
      - Being used as event log collectors.
      - Embedded in applications as internal data stores.
      - Homogeneous record size and data replication allows for better compression, allowing better performance even over low bandwidth SATA interfaces.
      - Leads to low consistency and higher application complexity.
    - Hierarchical (Document Data) - Offers storage of data in a manner they're operated in applications (as objects).
      - Keys can store associations to other documents.
      - Higher data duplication and less scope for compression - but can be overcome by using newer interfaces.
      - Highest storage use, arbitrary data layout, no schema and consistency checks (most of the time).

  * API
    - In Process vs Out Of Process (mostly out of process now, further far with ORMs)
    - SQL vs Not SQL

  * Transactions
    - ACID
    - Common Implementation Steps
      - Log incoming request to transaction log (write ahead log) - prevents data during system failure, allows restart of transaction
      - Serialize new values to index and tables without affecting others - most difficult to implement
      - Obtain write locks on cells to modify - lock a row, entire table, or a memory page
      - Move values
      - Flush changes to disk
      - Record transaction completion in logs

  * Persistence - Persistence (not necessarily durability) is the key feature of all databases (transactions, schemas and indexing are optional).
    - High performance in one storage method will lead to poor performance in other methods, eg, high performance in inserting large amounts of data sequentially may lead to low performance for
      random updates due to the application's usage of certain data structures tuned/created for specific needs.
    - Row Based - Uses a tree or similar compact data structure to store data row by row.
      - B+ Trees for fast random retrievals
      - LSM for high volume sequential writes
    - Column Based - 
    - Memory Only - Uses a wide variety of tree data structures for higher read/write speeds.
    - Distributed - 


## Monitoring
  * Predictable failures - mechanical wear and degradation of storage surface. Can be tracked.
  * Unpredictable failures - sudden mechanical failures, eg, due to improper handling.
  * Mechanical failures account for 60% of all failures. There are known symptoms of an imminent failure -
    - increased heat output
    - increased noise levels
    - problems with read/write of data
    - increased disk sectors damaged

  * Latest technology monitors hard drive activities and tries to prevent failures by attempting to detect and repair sector errors.
  * Offline monitoring has been on place to check for health during inactive periods [as opposed to online monitoring during access by OS].
  * From a 2005 study -
    - Negligible correlation found in temperature and drive usage with failures
    - About 56% of failures occurred without recording 4 major metrics - scan errors, reallocation count, offline reallocations, probational count
    - About 36% of failures occurred without recording any SMART metric except temperature - that limits the efficient of SMART data in anticipating failures [but much better than nothing] 
