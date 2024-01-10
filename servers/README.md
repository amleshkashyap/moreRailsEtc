### Notes
  * Must read - https://stackoverflow.com/a/4113570
  * For RoR - https://scoutapm.com/blog/which-ruby-app-server-is-right-for-you

### Web, Application Servers
  * NodeJS Deployment Examples
    - nginx + pm2 + express
    - nginx + phusion passenger + express

  * RoR Deployment Examples
    - nginx + phusion passenger + rails
    - nginx + puma + rails
    - ingress + puma + rails

  * Python Deployment Examples
    - nginx + gunicorn with flask/django
    - nginx + phusion passenger + flask/django

  * Others
    - nginx + go (+ gin/fiber for similarity)
    - nginx + tomcat + springboot

### Application State
  * Production applications should not store data in process
    - Eg, data, states, websocket sessions and session data must be shared via DB or pubsub system
    - Eg, any shared data like whether a HTTP resource is already locked, must not be held in local files or global variables, unless the
      the application is always going to run as a single process

  * If application is not stateless, it will be very difficult to scale it on the same server (eg, via pm2/nginx) and across multiple servers
    - When a centralized load balancer (eg, ingress controller, maglev) is used, they must direct the traffic to the same machine in order
      to maintain a "session", if the application process is the one maintaining state - this may not lead to efficient load balancing.
    - Such load balancers have to be in sticky mode
    - To avoid such problems, session information can be stored in a DB like redis
    - Databases can be used to share state between processes (eg, using redis instead of global variables for locking)

  * If building stateless applications, unnecessary race conditions can be avoided.
    - Eg, if a client library to some server is configured to store data locally instead of a shared server, it can lead to all kinds
      of race conditions based on how the library is used.

### Containers, Dockers

### Pods, Kubernetes
