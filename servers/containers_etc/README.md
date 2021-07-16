### Container Image
  * Supposed to be a self-contained and minimal set of softwares needed to run a particular application
    - including OS libraries, web servers, programming languages, development frameworks, DB, cache, etc
  * Can be hosted on some hardware
  * Conceptually, a container is meant to host one service only, so for example, if an application needs to use redis and mysql too, apart from its core service
    which can be a rails/nodejs server, then preferable to run 3 separate containers - not mandatory, just that the CMD commands for Dockerfile (and the setup
    being performed in Dockerfile) might seem a bit odd (eg, CMD/ENTRYPOINT is supposed to execute and just 1 synchronous command).
  * 


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
    2. LABEL - 
    3. ENV - set environment variables, eg, ENV key=value
    4. ADD - somewhat similar to COPY
    5. VOLUME - create a mount point (which would hold some externally mounted volumes).
    6. USER -
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
    13. ONBUILD -
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
