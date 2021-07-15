### Web vs Application Servers
  * It's difficult for me to find examples for software which purely are one of the above.
  * Web servers are supposed to handle requests directly from web. They obviously contain a set of operations (including authentication).
    - Apache, nginx can be thought of pure web servers.
    - They're heavily tested and are robust against multiple known vulnerabilities.
    - They're typically always used for serving static files directly.
  * Application servers are supposed to manage applications. They too contain a set of operations.
    - Typical management work includes - restarting dead instances, load balancing, limiting existing instances, monitoring memory usage, etc
    - Application servers are supposed to communicate with web servers in order to host the application on the internet
    - They can do this via something called reverse proxying.
    - ex. Tomcat, Unicorn (to be used with Nginx), Flask's built-in server
    - See this for a larger list, although it's not straightforward - https://en.wikipedia.org/wiki/List_of_application_servers
  * A software can serve as both - web server and application server - by integrating operations of the above two in a single software -
    - One way to serve as both is standalone mode of Phusion Passenger (see article below)
    - Another way to do it is via becoming a part of a web server, eg, Apache/Nginx, as done by Phusion Passenger.
    - ExpressJS can serve as a standalone web server.


### Automation Software and Watchdogs
  * Capistrano - can be though of as a set of scripts for automating actions like - uploading code, installing gems, restarting existing instances, etc
  * Watchdogs - They're supposed to monitor if all servers/automation software is running or not - if watchdog stops, then nothing to monitor them.

### NodeJS and pm2
  * pm2 is a popular process management tool for NodeJS applications.
  * NodeJS' event loop based architecture makes it very suitable as a web server too.


### Phusion Passenger
  * Must read basics - https://www.phusionpassenger.com/library/walkthroughs/basics/ruby/fundamental_concepts.html
  * Architecture - https://www.phusionpassenger.com/documentation/Design%20and%20Architecture.html

##### Request Handler
  * receives SCGI format request from webserver (webserver has HTTP request from client)
  * listens on Unix domain socket file called "request" (instance directory?)
  * creates a Client object for each request from webserver
    - Client object has all context related to request
    - it's closed once requesthandler is done - although there might be some other processes still attached to Client - so requesthandler pointer is set to NULL
      so that other processes can accordingly discard their pointers - Client is deleted when there's no pointers attached to it
  * forwards request to application pool which can select and create appropriate application process to handle the request
    - ApplicationPool might not be able to spawn a process immediately, but it maintains all the info and responds back to handler when it does create, with a 
      Session object (or exception)
    - the session object is utilized by the requesthandler to forward the request to that process after establishing a connection - protocol for this connection
      should be preferred by the process (ie, the appropriate application process) and supported by the requesthandler.
    - application process does the work, and responds to request handler with HTTP response, which is postprocessed by handler and sent to web server
    - if exception raised by application pool, handler sends the exception to web server
  * i/o model -
    - event i/o model - single thread, single process, i/o event multiplexing via syscalls like epoll - handle multiple clients at once
    - uses libev and libuv libraries to handle the above multiplexing - nginx uses this too (unlike 1 process/client or 1 thread per client)

##### Application Pool
  * keeps track of application processes, spawns processes, routes requests to appropriate processes and does load balancing, monitor CPU/mem usage of processes,
    enforce limitations like max processes and mem usage per process, restart process on demand and the ones which crash, queueing requests coming to these
    processes if the process can't handle above a certain amount (specified by process to the application pool), queueing requests while application is being spawned
  * different classes -
    - pool class - request handler interacts with application pool via this class. inside function "checkoutSession()", call "pool->asyncGet(options, callback)"      
      which responds with a Session object or exception
    - group class - represents one application and can contain multiple processes of the application
    - process class - an OS process which is an instance of an application. it has multiple sockets to listen for requests. maintains book-keeping, like the
      total Sessions currently open (with the request handler). contains communication channel with OS. instance objects are created via ApplicationPool Spawner.
    - socket class - single server socket on which process listens for request. Sessions created via sockets and sockets maintains the Sessions it has.
    - session class - information about a single request/response. book-keeping information updated upon create/delete session.
    - options class - parameter to the Pool::asyncGet() method.

##### Application Pool Spawner Subsystem
  * actual spawning of application processes with the related information in process object. encapsulate low-level info about process spawning (but doesn't handle
    management which is taken care by application pool).
  * multiple spawn methods - direct (via loader), smart (via preloader, only in RoR), dummy (only for unit tests)
  * to spawn a process, different components work together - one is Spawner which sets up the communication channels, working directory, env vars, etc and then
    is the loader/preloader which does programming languages specific env initialization, server setup, etc and communicates all this to Spawner via the 
    communication channels setup earlier.
  * spawner - 
    - determines which user the process should run as
    - sets up communication channel - Unix domain socket (it can be like TCP/UDP/SCTP), two processes can open the same socket and transfer data. this channel
      is just stdin, stdout and stderr for the forked process - Spawner (parent process) sends data to this child via stdin, and child sends to parent by writing
      to stdout or stderr. parent process waits till the child exits or communicates over the channel.
    - forks a (child) process


### Puma
  * Typically run as standalone - default web server for rails applications.
  * Some details of architecture - https://github.com/puma/puma/blob/master/docs/deployment.md
  * Deployment modes - https://github.com/puma/puma/blob/master/docs/deployment.md
