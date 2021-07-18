### Container Image
  * Supposed to be a self-contained and minimal set of softwares needed to run a particular application
    - including OS libraries, web servers, programming languages, development frameworks, DB, cache, etc
  * Can be hosted on some hardware
  * Conceptually, a container is meant to host one service only, so for example, if an application needs to use redis and mysql too, apart from its core service
    which can be a rails/nodejs server, then preferable to run 3 separate containers - not mandatory, just that the CMD commands for Dockerfile (and the setup
    being performed in Dockerfile) might seem a bit odd (eg, CMD/ENTRYPOINT is supposed to execute and just 1 synchronous command).


### Dockers
  * Docker has multiple useful commands, build, run and exec being the most used.
    - build - builds an image from a Dockerfile and a context. Context can be a directory (PATH) or repository (URL) - as mentioned above.
      0. https://docs.docker.com/engine/reference/commandline/build/
      1. Contexts are processed recursively obviously for all its contents.
      2. Context is sent to the Docker daemon recursively, for further processing
         - suitable to keep the main context folder empty with just the Dockerfile.
         - use .dockerignore file in context directory to ignore files if necessary. these are for build performance only.
      3. Docker daemon runs a validation on this Dockerfile for syntax errors before executing the specified commands.
      4. Commands are executed one by one, committed to an intermediate image if needed, and final ID is generated at last.
         - each instruction executed independently, creating a new image (or using a cached copy in the current machine - disable with --no-cache).
      5. Context sent in (2) is deleted at the end.
      6. Can check Buildkit - something with further optimizations like ignoring unnecessary stuff, parallel building, etc.
    - run - start one existing docker image on the machine with certain arguments for mapping.
    - exec - login to a running docker image instance for making changes/tests.
            
  * Dockerfile Commands - https://docs.docker.com/engine/reference/builder/
    1. FROM - use an existing image, eg, node:10-alpine, nginx:1.11-alpine, etc
       - alpine - ??
    2. LABEL
    3. ENV - set environment variables, eg, ENV key=value
    4. ADD - somewhat similar to COPY
    5. VOLUME - create a mount point (which would hold some externally mounted volumes).
    6. USER
    7. COPY - copy some file from one directory to another, eg, COPY \<src\> \<dest\>
       - while building a docker image, there has to be some directory/repository which serves as the the point of invokation of "docker build" - comes handy for
         copying source files/scripts, etc to the docker image. \<dest\> is in docker, \<src\> is wrt the point of invokation.
    8. RUN - execute anything as if being executed on command line, eg, build something, install, create folders, etc. This is primarily for pre-build operations.
       - note - don't use for starting services?
    9. EXPOSE - to expose the ports we want to for our docker image
    10. CMD - execute something as if it's being executed on the command line. This is primarily for post-build operations/for executing the built image.
        - only one CMD command is executed always - the last one is picked up if multiple - note that an image is supposed to provide one service only
    11. ENTRYPOINT - entrypoint definition for the application whose image is being created
        - overrides any CMD commands. typically, use it for invoking script which start dependent services for the application being created.
        - use when a container needs to be used as an executable.
    12. WORKDIR - make any directory as the working directory for the docker image.
    13. ONBUILD
    14. STOPSIGNAL - exit the container.
    15. HEALTHCHECK [options] CMD command - for defining and checking whether the container is healthy (checked by docker)
    16. SHELL - overrides default shell command - ["/bin/sh", "c"] and ["cmd", "/S", "/C"] for linux and windows - by something else.


### Docker Compose
  * Docker compose simplifies the building and management of multiple dependent containers. Docker compose is something like a prequel to Kubernetes.
  * The list of commands is much large since it's supposed to simplify multiple things, including container communication - features above are present obviously.
  * Specified in a YAML file, version compatibilities - https://docs.docker.com/compose/compose-file/
  * Commands For docker-compose - https://docs.docker.com/compose/compose-file/compose-file-v3/
    1. build - context, dockerfile, args, labels, network, target (multistage builds?), shm\_size (for /dev/shm of container), cache\_from
    2. command - overrides the default command (ie, in the CMD of Dockerfile).
    3. configs - for services like redis container, can pass the config file to start? (only 3.3+ versions).
    4. container\_name - instead of the default name generated.
    5. depends\_on - "up" is in order of dependency, "up \<service\>" starts the depencies of the service too, "stop" stops in order of dependency.
    6. deploy - replicas, mode, labels, max\_replicas\_per\_node, restart\_policy (for exiting containers)
       - resources - limits, reservations - for memory, cpu, swap
    7. device, dns, dns\_search - for device mappings, custom dns and dns\_domains list
    8. entry\_point (overrides ENTRYPOINT), env\_file (supply env\_files), environment (custom key-value pairs)


### Kubernetes
  * Container Orchestration - automate the deployment, management, scaling and networking of a large number of containers.
    - Leads to ease of management for microservices based applications.
    - Ex - provisioning/deployment, resource allocation, scheduling, scaling up/down, load balancing, monitoring health, secure communication etc
    - sounds like a mixture of web and application servers?
    - Tools - Kubernetes, Docker Swarm, Apache Mesos, Amazon ECS/EKS
  * Kubernetes - Kubernetes cluster consists of a set of worker hardware (node) running containers - 1 cluster >= 1 node
    - typically it's the next step after docker-compose when there's a huge number of instances.
    - https://kubernetes.io/docs/concepts/overview/components/
    - https://dzone.com/articles/from-docker-compose-to-kubernetes
  * Components of Kubernetes
    - Pod - Group of one or more containers deployed to a single node. All containers in a pod share - IP address, hostname, set of storage/volumes, etc
    - Control Plane - there are so many containers, they need to be managed so that consistency, availability and partition tolerance (lost information doesn't
      effect the whole application) are high, and resources are utilized efficiently so that costs are low. Control plane handles that.
      1. kube-apiserver - exposes the k8s APIs
      2. etcd - consistent, high availability key-value store.
      3. kube-controller-manager - node controller, job controller (pods for one-time jobs), endpoints controller (join service to pods), service/token controllers
      4. cloud-controller-manager - link k8s cluster to cloud provider's APIs, only for those components that actually need cloud providers.
      5. kube-scheduler - for scheduling pods to nodes based on criterion like policies, contraints, affinities, requirements, and more.
    - Node -
      1. kubelet - 1 per node to ensure pods in the node are healthy - doesn't manage containers not created by kubernetes.
      2. kube-proxy - network communication between pods to other network sessions inside/outside cluster. Uses OS packet filtering layer (??), else does itself.
      3. container runtime - docker, containerd
    - Add-Ons -
      1. DNS serves - generally in every cluster, serves DNS records for k8s services.
      2. web-UI
      3. container resource monitoring
      4. cluster level logger
  * Controller pattern - a controller tracks at least one k8s resource type (k8s objects) - controllers try to keep the current state close to the desired state
    specified for the objects.
    - This can be achieved via calling the k8s APIs (which in turn do something to bring the current state to desired) - eg, Job controller for multiple pods.
    - Also, if some external k8s cluster needs to be communicated with to facilitate the desired state, controllers can directly do it.


### Hardware/Software Communication
  * Commonly studied in computer networking, with the typical 7-layered OSI model (Application, Presentation, Session, Transport, Network, DataLink, Physical).
    - All topics in this heading need more clarity
  * Apart from internet (wide area network), there are multiple other types of settings where non-software components communicate with each other
    - LAN
    - Chips (cores till L3 cache)
    - RAM
    - Communication across various components of processors - chips to DRAM, external hardware ports, GPUs, etc
    - Audio and Video - eg, HDMI-2.1
    - Speeds of various channels used in the above - https://en.wikipedia.org/wiki/List_of_interface_bit_rates

  * Direct communication typically consists of -
    1. identification protocols - authorization - not so crucial intra OS processes
    2. security protocols - throughout the time when the components are talking - not so crucial for intra OS processes
    3. a software framework - eg, unix domain sockets, network sockets, protocol buffers - more crucial for intra OS processes
    4. actual communication - consists of commands (depends on the amount of functionality to be provided) and the data to be exchanged
    5. a set of well defined, possible paths on top of the transfer medium for movement of data, ie, network topology - eg, mesh, ring, bus, star, graphs, etc.
    6. a transfer medium - the underlying hardware - always crucial

  * OSI model allows one to create a simulator where different features and actual physical components can be modeled (eg, routers, bridges, etc).
    - Various components of these simulators can be used for creating networking in software where multiple related software components are involved.
    - Ex of such softwares - operating system (via system calls), web servers (unix domain sockets), now kubernetes
    - The reason why one would like to do so, is because of the immense control it can provide over the movement of information, as well as the ease of accessing it.

  * Softwares in a system often communicate with each other with no need of internet -
    - OS and applications - system calls (how?)
    - web-servers and applications - unix domain sockets, on system buses (mostly like bus topology), via HTTP
      1. chips can have data packets transferred across its various components (eg, L2 to L3 cache, L3 to memory) via different topologies.
    - web-server and OS - network sockets provided by OS is used to send receive information in/out of the computer (to/from web-servers)
    - two process instances of an application - eg, via MPI's communication specifications
    - in charm++ chares - message passing of "void \*args" (ie, marshalled/serialized parameters), different from MPI.

  * More Examples - not necessarily within a system, but closeby - protocols become more prevalent
    - MongoDB - Wire protocol, which is a socket based, request/response protocol
    - Notification system - websockets, which are bidirectional communication channels for pubsub - different security than HTTP (now WSS)
    - Microservices - RPC and gRPC protocols - for softwares spread across systems and connected via network
      1. data is serialized and passed via something called protocol buffers (sounds similar to the message passing among chares in (5) above)

  * Microservices etc
    - With a huge number of microservices running and communicating with each other in typical distributed systems, it's harder to monitor what's actually
      happening (what went wrong in normal communication?).
    - It's definitely not possible to control routing (eg, all the examples described above are typically a direct communication from one machine to another
      (or one process to another in case of intra OS communication).
    - This leads to other problems like unbalanced load across service instances (assuming random assignment of who'll serve a request), unmonitored inter-service
      communication (leading to security issues?), etc? what else?


### Service Mesh, Service Proxy
  * Service proxy is a "client side proxy for microservice applications" allowing application components to send/receive traffic.
    - Clients connects to service proxy and requests for some resource, and service proxy chooses the appropriate microservice that'll respond.
    - It can also be used to control the number of services required for serving certain client sizes, global/local load balancing, monitoring and analytics, security
      features, etc.
    - Source - https://avinetworks.com/glossary/service-proxy/
  * Service mesh is an extention of service proxy - features like monitoring, networking and security are left for automated management rather than developer
    worrying for it. Typically when an application is made up of many microservices and multiple instances of each microservice, etc.
    - All traffic is monitored through service proxies - one per microservice instance? - these make the data-plane for the service mesh.
    - There's generally a control plane for managing traffic, enforcing policies and other configurations.
  * Envoy -
    - Self contained process running across every application server - an Envoy. A mesh can have multiple envoys (as many as the application servers).
    - Applications send and receive message to/from localhost - they don't know anything about network.
    - This allows for application servers of different languages communicating via Envoys.
    - HTTP L7 filter - buffering, rate limiting, routing/forwarding, etc
    - L3/L4 filters -
    - HTTP/2 support - any combination of HTTP/1.1 and HTTP/2 clients/servers can be bridged.
  * Istio Service Mesh -
    - Manage traffic between services and outside services (allows blue green deployments, control over specific routes for services, load balancing configuration
      between services, etc)
    - metrics and logs related to the services for health, dependencies, security and overall monitoring
    - uses mutual TLS (??) instead of bearer tokens - somehow gives better authentication, encryption in traffic transit, monitor who accessed sensitive data, etc.
