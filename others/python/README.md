#### More Topics
  * Python seems to have a well organized doc/guide ([lang](https://docs.python.org/3/reference/index.html),
    [stdlib](https://docs.python.org/3/library/index.html#library-index)) with all the latest stuff organised in a readable state.
    - Someone has attempted it for [ruby as well](https://rubyreferences.github.io/rubyref/)
    - golang already has it - [lang](https://go.dev/ref/spec), [stdlib](https://pkg.go.dev/std), [all](https://go.dev/doc/)

##### Built-In Support
  * Code object - The actual code (string) of a function, can be extracted from the function object via \_\_code\_\_ method.
    - Returned by the compile() method.
    - Can be passed to exec() or eval() methods for execution.
  * NotImplemented object - when there's a comparison or binary operation on 2 types which are not supported [and error handling isn't present], then this object is
    returned.
  * \_\_dict\_\_() - Writable attributes of an object are stored in this.
  * bisect lib - for large arrays that should remain sorted at the time of inserting an element. There's a method insort() too [?].
  * graphlib - for topological sorting.
  * collections -
    - namedtuple()
    - deque
    - ChainMap - chaining for collisions.
    - Counter
    - OrderedDict
    - defaultdict - calls a factory function to add missing values [?]
    - UserDict, UserList, UserString
  * [collections.abc](https://docs.python.org/3/library/collections.abc.html#collections-abstract-base-classes) -
    - Some base classes to test whether a particular class provides some interface - eg, iterable, hashable, etc.
    - use isinstance() and issubclass() methods.
    - The class, if it provides an interface of the abstract class being checked for, can use the mixins defined by the abstract class?
    - 
  * contextmanager - 'with' statement in python. Difficult topic without relevant examples.
    - contextlib
  * Functional programming modules -
    - itertools - faster iterations methods.
    - functools - acts on/returns functions.
    - operator - efficient functions corresponding to the intrinsic python operations [eg, operator.lt/operator.\_\_lt\_\_ is <].
      - work with itertools as well for faster operations.

  * Data persistence -
    - Serialization - pickle, marshal [unmarshal/unpickle is to be avoided for data from unauthenticated sources - use json in such cases].

  * Data compression/archiving - bz2, zlib, gzip, etc

  * Processing structured files and markups -
    - Files - csv, configparser [ini files], netrc [netrc files], plistlib [Apple plist files]
    - Markups - html, xml.etree.ElementTree, xml.sax parsers
    - Internet - json, mailcap, binhex [binhex4 files], binascii [binary to/from ascii]

  * Crypto - hashlib, secrets

  * OS - os, io, time, argparse, logging
    - ctypes - 

  * Parallel Programming -
    - threading
    - multiprocessing
    - subprocess - create/manage new processes
    - sched - event scheduler
    - queue - 
    - external - celery - background job processing

  * Networking, IPC -
    - asyncio
    - socket, ssl, etc
    - Protocols and Support - webbrowser, urllib, http, ftplib, pop/imap/smtp, uuid, xmlrpc, ipaddress [create/manipulate ipv4/ipv6 addresses/networks]
    - Multimedia - wave [wav files], colorsys
    - Internationalisation - gettext, locale

  * Developer Tools
    - typing - for type system hints [annotations]
    - pydoc
    - test, unittest, doctest, unittest.mock
    - 2to3 - code translator from python2 to python3
