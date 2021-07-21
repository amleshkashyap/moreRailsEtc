### Ex. Google Cloud
  * Anthos - Faster application modernization.
    - Run k8s clusters in existing cloud and on-premise infrastructure.
    - Configure and send security policies across all k8s clusters.
    - Service mesh powered by Istio, which is based on Envoy.

  * Google Kubernetes Engine - 
    - Scaling upto 15,000 nodes.
    - Vulnerability scanning of containers, data encryption
    - Standard operation (ie, manually managed) and completely managed.
    - Full k8s APIs, 4-way autoscaling (??), multi-cluster support, horizontal autoscaling for pods based on hardware utilization (or custom)
    - Use existing k8s apps (see below)
    - Other features - IAM, hybrid networking (cluster IPs coexist with private IPs - Google VPN), security, compliance, logging, monitoring, cluster templates,
      auto scale/upgrade/repair, resource limits, container isolation, GPU/TPU support, existing dashboard, persistent disks (HDD/SSD), load balancing, etc. (AWS).

  * AppSheet - Readymade APIs for some common business operations, no code.
    - Order approvals, notifications, etc - instead of whatsapp
    - One app across mobile, web, tablet
    - Connects to google sheets, salesforce and other data sources to load/export info
    - "Anticipate and automate" data collection
    - Apps built will have NLP/Speech for commands, CV for annotations, etc

  * Bare Metal Solution for Oracle - port Oracle workloads, eg, clustered DB, replication configs, perf optimizations, etc, to Google cloud (running directly on
    google hardware - why do such a thing - https://techcrunch.com/2019/11/20/google-cloud-launches-bare-metal-solution/
    - the idea seems to be to port from on-premise to cloud environment, with minimal changes.

  * Kubernetes Applications - "Enterprise-ready" containerized applications with deployment templates for plug and play kinda feel.
    - can be run on Anthos, in the cloud (?), on premise and in k8s clusters of other environments (eg, EKS/ECS).
    - ready to integrate with best-practice production release and deployment workflows. container images and config files provided to customers, apps packaged using
      open source frameworks like Helm.
    - Application examples - gitlab, neo4j, wordpress, prometheus, etc.
    - Over 100 - https://console.cloud.google.com/marketplace/browse?filter=solution-type:k8s&\_ga=2.178189541.1172728229.1626532708-1641089445.1626532708

  * Knative - k8s based platform to build, deploy, manage modern serverless workloads.
    - Features - autoscaling, in-cluster build, scale-to-zero, eventing framework, connect own loggers/monitoring tools, etc
    - Eventing framework - scalable from few events to live streams, custom event pipelines to integrate with existing systems, etc.
    - Automate the building, deployment and management of applications.
    - Available on cloud, on premise, third party data-centers.

  * Cloud Code - programming on cloud feels like local machine - for k8s apps (??). Support for VS, IntelliJ, Shell.

  * Cloud Run - Deploy highly scalable containerized apps on a fully managed serverless platform.
    - Container and Knative open standards.
    - Autoscaling, replication, security, logging/monitoring, asynchronous event triggers from 60+ GCloud sources (Cloud Audit Logs) or Custom sources (Cloud pubsub).
    - Portable, TLS, websockets and gRPC.

  * Cloud Functions - AWS lambdas (code snippets that respond to events).
    - Connect/extend multiple services (eg, multiple cloud runs above)
    - runs only in response to events.
    - second offering from google for serverless computing

  * Workflows - arrange google cloud and HTTP based API services
    - error handling for workflow steps.
    - pass variable values between workflow steps.
    - Built in authentication for GCP
    - conditional step executions, logging, external API calls, low latency.

  * Tekton - 


### Ex. AWS
  * Lambda - serverless, FaaS
    - possibility of deployment without any manual intervention - using serverless.yml.
    - can mention the various events on which the lambda has to react upon, and how it'll react.

  * SQS - queueing service for sharing messages.

