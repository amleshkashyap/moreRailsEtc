## HTTP Semantics
  * [Source](https://httpwg.org/http-core/draft-ietf-httpbis-semantics-latest.html)

### Terminology
  * Resources - Target of an HTTP request is a resource - nature of resource is not limited. Resources are identified via URI. 
  * Representations - Information that is intended to reflect a past, current or desired state of a given resource in a format that's readable via the protocol.
  * Connection, Client, Server - usual. Server must not assume that 2 requests on the same connection are from the same user agent.
  * User agent - a client program, eg, web browser, spiders, CLI, mobile phones, etc.
  * Messages
  * Origin server - a program that can generate authoritative responses for a given target resource, eg, web servers, automation units, traffic cameras, etc.
  * Intermediaries - 3 common ones - proxy, gateway and tunnel.
  * Caches
  * Identifiers - URI
  * Fields

### Method Definitions
  * General -
    - Headers can be used to specialize the semantics of methods, eg, execute the API operation if the state satisfies the condition stated in certain header.
    - HTTP is supposed to work as an interface to distributed object systems - request method invokes an action to be applied on target resource in pretty much the similar fashion as RMI can be
      sent to a target object.
    - HTTP methods are, unlike distributed objects, not resource specific [ie, a system might have multiple resources, HTTP methods are not specific to those] - methods define some semantics which
      may or may not be implemented by individual resources in a system.

  * Basic Definitions -
    - GET - transfer the current representation of target resource.
    - HEAD - same as GET, don't transfer the representation.
    - POST - perform resource specific processing on the request content.
    - PUT - replace all representations of target resource with request content.
    - DELETE - remove all representations of target resource.
    - CONNECT - establish a tunnel to the server identified by the target resource.
    - OPTIONS - describe communication options for the taget resource.
    - TRACE - perform a message loop back test along the path of target resource - what does that mean?
    - PATCH - not defined in above doc - 

  * A general purpose server must support GET and HEAD methods, everything else is optional.

  * Safe Methods -
    - Methods whose defined semantics are read-only are considered safe - GET, HEAD, OPTIONS and TRACE are safe by definition.
    - It's use should not cause a loss of information - however, the implementation can always stray and allow harmful behaviour - as long as it doesn't hold the client responsible for it.
      - Eg, requests can append to a log file after completion which can lead to disk space full and server failure - but that's acceptable.
    - This categorization allows automated retrieval and cache perf optimisation without any loss of information.
    - User agent though, has to distinguish between safe and unsafe methods to appropriately make the requests.
    - Certain query params used to perform change or removal of target resource should not be allowed as part of safe methods.

  * Idempotent Methods -
    - A method is idempotent if the intended effect on server of multiple identical requests with the method is same as the effect of single request.
    - Each of these identical requests can be logged separately and can perform different bookkeeping actions.
    - This is a key property since requests can fail or client can go down - the intended effect of retries must remain the same even though the responses might differ.
    - Client should not retry a non-idempotent request unless it knows that it is idempotent or that the original request was not applied for sure.
    - A proxy must not retry a non-idempotent request, and a client must not retry a failed automatic retry - unless there are such guarantees provided by the server.

  * Caching -
    - Use of request and response headers to be explicit about what can be cached and for how long, under what conditions, etc.
    - Most caching implementations support GET/HEAD methods, although there are no restrictions for other methods.

#### GET
  * Target URI can be used to differentiate between the potential sameness of responses.
  * HTTP interface for a resource can be implemented as a tree of content objects, a database record or a gateway to another information system.
  * Range transfer is an advanced topic for partial representation transfer.
  * Participants of HTTP communication are usually unaware of intermediaries along the request chain - hence, any contract between client/server related to transfer of content in GET requests, unless
    it can be guaranteed to be a direct communication, should not be entertained by server or implemented by the client.
  * Responses -
    - 200

#### HEAD
  * Identical to GET except server should not send the full representation - although metadata can be sent to inform the clients.
  * Server should respond with the same headers as that of a GET request on the URI - but if some headers rely on the generation of actual content, which, if skipped, can be omitted as well.
  * HEAD requests can be used to reject requests and close connections as well.


#### POST
  * Requests that the target resource processes the information enclosed in the request according to implemented semantics.
    - Client can provide a block of data to the server.
    - Posting a message to a message pool [eg, mailing list].
    - Create a new resource.
    - Append more information to an existing resource.

  * Almost all the HTTP response codes defined can be a response in a POST request [except 206, 304 and 416].
    - Creation should result in 201 - along with a Content-Location header that provides an identifier for the primary resource created, and a representation describing the status of request.
    - Server can also redirect the user agent to the GET URI of another target resource [via Content-Location header] if it determines that the representation sent in the request already exists
      as a different object.

  * Responses can be cached only if the expiration header and Content-Location header is provided - to be able to track and expire the potentially changing resource.


#### PUT
  * Requests that the target resource be created or replaced with the state in the enclosed information in the request.
    - Parallel PUT operations can lead to loss of observability of individual requests - hence, a successful response should focus on the guarantee that the requests intent was achieved.
    - If PUT created a new representation of the target resource, then 201 should be returned.
    - If an existing representation was successfully modified, then 200 or 204 [no content in response] can be returned.

  * Server should validate that the PUT representation (ie, request body) is consistent with the configured constraints for the target resource.
    - If the PUT representation is not consistent, then either they should be made consistent before processing [change request body, change target resource configuration] or respond with an
      appropriate error message to explain why it can't be processed (eg, 409, 415).

  * HTTP doesn't specify how a PUT method effects the state of an origin server beyond the client's expression of intent (via request body) and the semantic of server.
    - It doesn't define what a resource might be, how the resource state is stored, how much storage changes can happen due to resource state change or how resource state is translated to
      its representation.
    - Server should ignore unrecognizable header and trailer fields [what's that?] received in a PUT request.
    - Server must not send a validator field [eg, etag] or Last-Modified field in the response - unless the representation remained unchanged.

  * Difference in PUT and POST - different intent for the enclosed representation.
    - POST intention is to allow the server to handle the enclosed representation according to the resource semantics.
    - PUT intention is to replace the state of the target resource.
    - PUT is idempotent and visible to intermediaries [not necessarily completely visible] - but exact sequence of operations are visible to the server only.

  * Interpretation of PUT request -
    - User agent should know which target resource.
    - Note that the definition of PUT request doesn't suggest redirection - hence, implementation of an intent to change the state of a target resource via a user agent should ideally be a POST
      request so that in case the server finds out that the suggested representation already exists as a different resource or that the requested resource has been moved to a different URI, and wants
      to respond with the target URI of this resource, then it can do so and it's upto the user agent to decide what to do with this new target object.
    - A PUT request can have side effects to other resources.
    - Responses to the PUT method are not cacheable.

  * Responses -
    - 200 - action successful, return the target's representation.
    - 201 - created a new representation of the target.
    - 204 - action successful, no content.
    - 409 - precondition failed
    - 415 - invalid media type

#### DELETE
  * Requests that the server remove the association between the target resource and its functionality.
    - This expects a deletion operation on the URI mapping of the origin server rather than an actual deletion of the target resource from server.
    - HTTP doesn't specify anything about what the delete operation entails - eg, removal of the resource from storage, archival, etc.

  * This operation is usually not allowed for all the resources.
    - User should have some 

  * Responses -
    - 202 - if action will likely succeed but not yet finished.
    - 204 - action has finished, no further information to be supplied.
    - 200 - action has finished, return the representation which describes the status.

  * If client sends some message in the request, then it's interpretation is left upto the server.
    - DELETE operation on a target URI which passes through a cache must invalidate it at successful response.

#### CONNECT
  * Requests that the recipient [ie, user-agent] establish a tunnel to the destination server, identified by the request target and then restrict to blind forwarding of data in both directions
    till the tunnel is closed.
    - Client must send a port number - server responds with 400 if it's empty or invalid.
    - Use authentication if required while creating a tunnel.
    - 

  * TODO


#### OPTIONS
  * Requests information about the communication options available for the target resource.
    - If the request target is `*`, then it applies to the server in general - else for specific target resources, it applies accordingly.
    - 

### Headers
  * Conditional
    - If-Match - Can be used with any method involved in selection or modification of a representation to abort the request if the selected representations current entity tag is not a member of the
      value of this header.
      - If the given pre condition is not satisfied, then request method must not be performed and server can return a 412.
      - If the request is supposed to change the state but finds out that it's already changed, then it can return with a 200 kind response.
    - If-None-Match
    - If-Modified-Since
    - If-Unmodified-Since - 
    - If-Range -

  * Precedence Of Preconditions -
    ```
    1. If-Match -> true -> continue with If-None-Match below
                -> false -> return 412 (or determine if state change has already succeeded)

    2. If-Unmodified-Since -> true -> continue with If-None-Match below
                           -> false -> same as above

    3. If-None-Match -> true -> continue with If-Range below
                     -> false -> GET/HEAD -> return 304
                              -> others -> return 412

    4. If-Modified-Since (and If-None-Match not present) -> GET/HEAD -> true -> 
                                                                     -> false -> return 304

    5. If-Range -> GET -> true -> Range -> true -> return 206
                       -> false -> return 200

    6. Else - perform the requested operation for the given method
    ```

  * Range - range headers are useful if the client is capable of storing partial representations, and then querying the server for the remainder of the representation to later merge and create the
    full representation locally. For now, it is out of scope.


### Caching
  * Headers -

## REST Semantics
  * [Source](https://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm)


## API Design And Implementation Basics
  * [Basic-SO](https://stackoverflow.blog/2020/03/02/best-practices-for-rest-api-design/)
  * [Basic-Swagger](https://swagger.io/resources/articles/best-practices-in-api-design/)
  * [Apigee]() - TODO
  * [A]() - TODO
  * [G](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/32713.pdf) - TODO
  * [G](https://cloud.google.com/apis/design)


## Basic Application
  * Since APIs are exposed to users, they can be exercised in a variety of ways, thus leading to multiple possible outcomes - add system failures in the mix and the list grows.

### Committer APIs
  * Eg, POST, PUT, PATCH, DELETE
  * There can be multiple possible scenarios for APIs making commits to persistent storage.
  * User makes an API call and it succeeds - best case.
  * User makes an API call and it fails without committing - retry is safe.
  * User makes an API call and it fails before the last commit - retry might not be safe.
    - It can fail because of system going down.
    - It can fail because of DB connection lost.
    - It can fail because of client timeout.
    - It can fail because of server eviction [depends on the policy used].
  * 2 [or more] users make the same API call, first one fails before the last commit, but second one succeeds - can lead to inconsistencies.
  * 2 [or more] users make an API call wherein both operate on the same DB record. Following subset -
    - 2 [or more] users make an API call, where first one is a new version of the API and second one is the older version.
