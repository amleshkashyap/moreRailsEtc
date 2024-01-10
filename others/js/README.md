## General
  * Node version with support for ECMA features - https://node.green/
  * import vs require
  * Arrow functions
  * Prototypes

## Runtime
  * Event driven
  * Thread pool can be increased to boost performance
  * Run multiple instances using pm2 (cluster mode, needs statelessness) to handle more traffic

  * Callbacks <-> Promises - Async/Await
    - One can directly use the await keyword (inside async functions only) before any function which returns a promise.
    - Avoid using callback if possible
    - [Example](https://github.com/redis/ioredis/blob/main/lib/Redis.ts#L174) - uses both callbacks and promises

  * NodeJS is an implementation of the reactor pattern - in the rails world, eventmachine is a robust implementation of the pattern (very
    useful for certain tasks which can be asynchronous, and for scheduling periodic timers)
    - [libuv](http://docs.libuv.org/en/v1.x/design.html) event loop details
    - [eventmachine](https://www.paperplanes.de/2011/4/25/eventmachine-how-does-it-work.html) loop details
    - [General notes](https://www.igvita.com/2008/05/27/ruby-eventmachine-the-speed-demon/) on how to get the best out of reactor pattern.

  * NodeJS' net library provides features for socket programming.
    - NodeJS is natively more suitable for asynchronous and I/O intensive tasks, but can be used for synchronous computation.
    - File read was one of the few synchronous clients provided natively.
    - Client libraries like ioredis and superagent can be used in a synchronous way to provide more functionality, as the socket libraries
      (eg, net) is event driven and can't be directly used for building synchronous clients.
    - Synchronous clients are crucial - from accessing locally hosted services to making http API calls - all of these via socket libraries.
    - Some of the earlier efforts at creating synchronous clients was by forking a [child thread](https://www.npmjs.com/package/sync-socket)
    - Eg, socket libraries in python/ruby have no such problems - it's straightforward to build such clients.
