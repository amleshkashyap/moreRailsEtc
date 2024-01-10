## General
  * There is a lot of terminology associated with java and its various usages due to widespread use. Focusing only on its abilities as a
    general programming language and framework support around web application development (ie, J2SE and J2EE).

  * J2SE is the specification for language capabilities and library support - eg, java class library, JVM specification. OpenJDK is
    considered a reference implementation for J2SE specifications since version 7.

  * J2EE - Java is so big that folks have written specifications for how to write/deploy enterprise applications in java - few companies
    have implemented the runtime support for these specifications with varying capabilities.
    - Eg, mysql has an enterprise edition, but there's no specification (AFAIK) for SQL EE. C++ has specifications for language capabilities
      but nothing for enterprise.
    - J2EE is big, but the web profile consists of modules like these -
      - Servlet, Server Pages (JSP)
      - Java Enterprise Beans (EJB) - APIs that the EJB container will support to provide transactions (JTA based), RPC (RMI), concurrency
        control, job scheduling, asynchronous and event driven programming, deployment, dependency injection and access control for business
        objects. Contracts between EJB and clients, as well as EJB and EJB containers are documented.
      - Java Persistence (JPA) - ORM
      - Java Transaction (JTA) - For distributed transactions
      - Contexts And Dependency Injection (CDI)
      - Java Restful Web Services (JAX-RS) - ex, jersey (reference), jello, Apache TomEE 
      - Java Messaging Service (JMS) - 
      - More - Java Websocket, Java JSON Processing (JSON-P)
      - Others - Expression Language, Standard Tag Library, Bean Validation
    - Spring (and Springboot) are not part of the above specifications but closely related to JAX-RS, and an additional feature of EJB.
    - While it looks like a lot of material, it makes enterprise application development very standardized, and leads to lower burden and
      lesser bugs for larger organisations - however, not sure how much of the scalability burden is lifted by these standards.

  * JVM, JRE, JDK - Part of J2SE, whose reference implementation is OpenJDK.
