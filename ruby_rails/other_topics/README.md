### Notes On "-w" While Interpretation -
  * Whitespace after a method name

### Notes On Syntactic Structure -
  * Primary expressions - basic unit of syntax which directly represent values, eg, number, string, variables, self, nil, etc
  * Expression - basic unit of syntax, built by combining primary expressions with operators, and evaluating to a value, eg, "x = x + 1"
  * Statements - another basic unit, built by combining expressions with keywords, eg, if, while statements
  * Methods, Classes, Modules - above combine to make methods, which can combine to form classes (related methods) and modules (unrelated methods)
  * Blocks and Body - basically, everything inside, say, a loop, ie, the body of the loop, can also be represented via '{ }', in which case it becomes block. Put
    another way, keywords serve as '{' or '}' in case of multiline Ruby code.
  * Never put a space between method name and opening paranthesis

### Notes On Encoding - Mostly Irrelevant
  * Obviously by default Ruby uses ASCII. And supports other encodings too. In fact, define your own encoding or whatever, just map it to ASCII and tell Ruby how to
    read it (how to tell?)
  * Source Encoding - this means the encoding used to read a particular Ruby script by the interpreter.
    1. In 1.8, only 1 type of encoding could be supported for all Ruby scripts for a process (ASCII, or anything else) since it was done via a command line options
       related to "-K". Later, each of the scripts could have a different encoding, which needs to be specified at the top of the script (line 1, or line 2 in case
       line 1 is a shebang).
    2. Also, the specification of the encoding is flexible, ie, is only requires having a few characters (eg, #, coding, utf-8, :, =) in order to identify the encoding,
       so a user can specify additional characters too (eg, prefixes to 'coding') in case it helps them indicate about the encoding to their editor too (eg, vim, emacs,
       VS, etc). Also, either case is supported.
    3. \_\_ENCODING\_\_ is a keyword that returns an Encoding object and can be used anywhere in the program to return the current file's encoding.
    4. UTF-8 can also be identified using Byte Order Mark. See book for examples when needed.
  * Default External Encoding - this means the encoding used to read all other files (I/O) except for Ruby scripts.
    1. By default, it's picked up from the system's locale (env/bash settings). Also, there can be only 1 encoding for a single Ruby process. This is exactly what was
       being used in 1.8 and earlier to support an encoding other than ASCII for all the Ruby scripts.
    2. Can be specified via "-E"/"--encoding" options now. Only 1 per process though.
    3. Encoding.default\_external and Encoding.locale\_charmap (from the locale) - these are methods of the metaclass of Encoding class.

### Program Execution
  * Start Of Execution - Interpreter first looks for BEGIN statement, if found, executes related code block, and then returns back to line-1 to continue further
    execution. No main method.
  * Module, Class, Method definitions - In compiled languages, these are obviously special keywords processed by compiler to do various things studied in Compiler
    Design. Ruby interpreters consider these as statements and executes them, so a class or method definition is executed and a new class/method comes into existence
    (which probably means they're organized somehow, maybe similar to things studied in Compiler Design). At the time a method is called, the actual method statements
    are executed.
  * Termination - (a) some statement is encountered which leads to termination, (b) reaches the end of file - most frequent cases. (c) reads a line with the token
    \_\_END\_\_.. Unless explicitly terminated via exit! method, the program will (a) execute code blocks related to the END statements, (b) execute code blocks
    registered with the at\_exit method (a shutdown hook).


### Load
  * Expects complete filename with extension to be loaded. Usually expects .rb type of files.
  * Freshly loads whenever called - no caching.
  * loads with whatever $SAFE variable value is used - relevance?
  * Uses $LOAD\_PATH global variable value of Ruby for loading when absolute path not present - it returns and array of pre-saved paths for Ruby to load from.
    - Search start from start of the array
    - from 1.9, gems are the initial part of this array (with highest version of a particular gem being the default - modifiable though)
    - these are followed by site specific libraries (??), OS libraries specific for Ruby, standard library and OS default libraries.
    - use "--disable-gems" if program uses no gems - for some perf improvements - rare.
    - can add further libraries with "-I" cmd option
    - $LOAD\_PATH can be modified from within a Ruby program
    - $LOAD\_PATH is ignored when absolute paths (starts with / or ~) are given to load/require.
  * loaded files don't have access to the local scope of their place of invocation - global vars/constants which are defined before are available though.
    - local variables of the loaded files are destroyed after execution is complete, obviously.
    - the constants/globals defined/modified in the loaded file are however retained - so it can change the global state of the program.
    - when the file is changed, and then we do a load again on that (in the same context though - eg, single irb session) - some warnings are thrown. these changes
      should preferably be wrt the constants (classes/modules are also constants).
    - load can't be used for nesting though, ie, open a class, load some methods from a file - doesn't work. new classes can be added to the global state though.
    - there's no object passed to the loaded file, and thus the default object at start of loaded file is main.
    - load(file) - can be considered similar to doing - eval File.read(file)
  * When a non-nil/non-false 2nd argument is passed to load, it doesn't allow the file to change the global state of the program as before
    - basically, constants defined/modified in the file aren't reflected in the global state of the program
    - global variables can still be modified though
    - it is achieved by "wrapping the file and loading it inside an anonymous module" - unlike before, any constants of the file aren't remembered.
    - Sandbox env's don't use require, and loads are always wrapped - it's considered safe, and used infrequently.
    - load(file, true) - can be considered similar to doing - Module.new.module\_eval(File.read(file))
    - good article here - https://practicingruby.com/articles/ways-to-load-code
  * Autoloading - lazy loading of files on a need basis. register uninitialized constants to be loaded from a specific file, when referenced.
    - autoload :some\_class, "filename\_to\_load"
    - uses require for loading rather than load
    - autoload?/Module.autoload? with a symbol argument will give the filename that'll be loaded when the symbol is referenced (nil if not registered/loaded already).

### Require
  * Can work with just a name - if 2 files of same name but different extensions are present in the relevant directory searched first, .rb is given highest preference,
    followed by relevant binary files of the OS (eg, .so/.dll).
    - thus, can work both with ruby source code and binaries - preferred for binaries though.
  * Caches the loaded files in global variable $LOADED\_FEATURES - since 1 file can be given by more than one, but not too many path strings, there's barely any
    duplications/reloads.
  * require is safer than load via some $SAFE variable related thing (for tainted objects).


### What Is Different About Ruby?
  * Purely Object Oriented Languages
    - everything is an object in such languages
    - basic datatypes are not present - so there's no direct mapping to memory to think about, for ex, Booleans are 1-byte in C, so are chars etc, but in a pure
      object oriented language, Booleans have to be objects, and thus, they need to have some instance methods on them. Thus the concept of TrueClass, FalseClass and
      NilClass - and their objects true, false and nil have some methods defined for them. We don't have to think about memory if we don't want to.
    - These languages are written in something like C (Python, Ruby), and uses Structs (see metaprogramming) to handle classes (and thus, "datatypes").
    - Structs in C are composed of multiple simpler datatypes and pointers, thus, consume more memory.
  * C++ is mostly object oriented, similar to Java, but not pure OO.
  * Inbuilt pubsub mechanism in standard lib - https://ruby-doc.org/stdlib-2.6.3/libdoc/observer/rdoc/Observable.html

### Ruby Memory
  * true, false, nil and Fixnum integers are objects which are not represented using Structs, their value can be operated directly from memory - they're fast.
  * ObjectSpace module provides methods to interact with the garbage collection facility, and allows traversal of living objects. ObjectSpace from standard library
    is a more interesting module - it extends the core ObjectSpace.
  * memsize\_of and memsize\_of(class) method of this module can be utilized to see the memory usage. ex, ObjectSpace.memsize\_of({}) gives 40 bytes.
    - https://gettalong.org/blog/2017/memory-conscious-programming-in-ruby.html
    - https://www.sitepoint.com/ruby-uses-memory/

### Ruby Parallelism
  * When multithreading in Ruby, be careful while modifying an object via different threads - instance/class variables aren't thread safe - this is of relevance when
    threads are invoked from within the code (and hence, can potentially operate on same object).
  * Ruby multithreading seems like pthreads - create new thread and join it back - probably languages don't do OpenMP kind of thing that much.
  * Ruby multiprocessing - one can fork off a completely new process from within Ruby.

### Concurrency In Web Apps
  * Software concurrency is a difficult thing, unlike hardware concurrency, which is well defined - eg, for a small supercomputer, it looks like this -
    system -> level-1 -> level-2 -> ... -> fast-group-1 (set of cpu/gpu, eg, blade/rack/node) -> chip (eg, multicore cpu/gpu) -> 1/many threads
  * In sidekiq, organization per sidekiq process is - (queues, workers) -> jobs -> actual code with loops - can utilize threading at any place. now the basic unit
    of work in sidekiq is job, ie, a queue can have 10s of workers, with each workers having 10s of jobs (or, a worker having 10s of queues), but finally, sidekiq
    actually does the computation at job level - thus concurrency works there. One can complicate things by spawning threads within jobs (they're Ruby threads) -
    and then, have a great time debugging, if not done carefully. Concurrency in kue.js (not sure of bull.js) works similarly - cluster are like MPI (core-level).
    - https://github.com/Automattic/kue#processing-concurrency
    - https://blog.appsignal.com/2019/10/29/sidekiq-optimization-and-monitoring.html
    - https://dzone.com/articles/thread-safe-apis-and-sidekiq
    - https://github.com/mperham/sidekiq/wiki/Problems-and-Troubleshooting#threading
  * Now since sidekiq threads are operating on jobs, what is thread safety? Rails is running constantly, and a sidekiq process is separately running, and then
    something is sent to sidekiq for execution - still, how likely it is that multiple threads of sidekiq access same class/instance variables?
