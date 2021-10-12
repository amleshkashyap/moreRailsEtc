### Security Practices

### Basic Authentication
  * Username and password sent by the client to server to verify the user. Many possible forms, eg, plain-text username and encrypted password or plain text
    password which is then passed to a hash function which was used to create a hash before storing it in the DB.
  * Other forms include username:session\_id pair.

#### Session Based Authentication
  * Session created by server, stored within cookies (ie, session id) on client's browser.
  * Client (eg, browser, postman) sends cookie with every request to verify itself (this is also a source of CSRF attacks as mentioned above).
  * Scaling can be a problem if huge number of users.
  * More suitable for browser/UI based applications.

#### Token Based Authentication
  * For example, JSON Web Tokens, created by server with a secret and sent to the client which may store it in local storage. Client sends this as header in every
    request.
  * Since JWT is a specification, with standard headers and payload (can be custom too) which are further encoded to prepare the signature, and the three
    are then encoded to prepare the final token - using the secret - all of this can be recreated without storage, or can reduce the DB queries - but that's not
    the real reason for using it (ie, reducing DB queries).
  * When JWT is sent as part of Authorization header - somehow reduces CORS issues. Performing a CSRF might be difficult, as their are no cookies to be used by
    default with every request made to a target website - Authorization header needs to be populated with JWT stored in local storage.
  * Shouldn't store for too long in the browser storage.
  * May lead to scaling issues if too much info stored in server.
  * JWT Can grow large in size because more information is stored.
  * More suitable for backend/API only applications.
  * Playground - https://jwt.io/#debugger-io

### Application Specific Security
  * Descriptions from Node's [helmet](https://github.com/helmetjs/helmet) and [mozilla developer documents](https://developer.mozilla.org/en-US/docs/Web/HTTP).

#### Headers -
  * Content Security Policy -
    - Can mitigate the risks of XSS attacks.
      1. Browser's which support CSP will load scripts from servers which are configured to be trusted - however, server still needs to perform escaping properly.
      2. Protocols (scheme) can be configured - content to be loaded only via these protocols
    - These types of content can be setup for having valid sources - fonts, iframes, images, manifest files, media files, URL's to be loaded from scripts,
      objects, prefetches, scripts, stylesheets, worker scripts.
    - For every type of content, the valid sources can be specified as host URL or some scheme (eg, https), along with some other values.
    - 'Content-Security-Policy' and 'Strict-Transport-Security' are the relevant headers.
  * Cross Origin Resource Sharing
    - Can be utilized to indicate to (compatible) browsers about the origins (domain/scheme/port) from which resources can be loaded (default: same origin).
    - Browsers make preflight requests to the specified origins to check if they'll allow the requests for loading content - not all requests need it (GET/POST/HEAD).
    - 'Access-Control-Allow-Origin' - this header can be utilized to allow applications of different domains to load content from the server.
    - Other related headers -
      1. Request - Origin, Access-Control-Request-Method, Access-Control-Request-Headers
      2. Response - Access-Control-Expose-Headers, Access-Control-Max-Age, Access-Control-Allow-Credentials, Access-Control-Allow-Methods, Access-Control-Allow-Headers

#### Cookies
  * Secure - Cookies set without secure flag can be accessed from the browser via unencrypted connections. This can be an issue if the cookie contains
    session or access control information.
  * No HTTP - Cookies set without nohttp flag can be accessed by scripts and transmitted to other sites - can be harmful if cookie has session/privilege info.
  * SameSite - Cookies set without samesite attribute can be used by scripts to make cross site requests (CSRF attacks).

### Widely Used Standards
  * Assumes -
    - Authentication is - (1) username/password, (2) optional OTP/MFA
    - Authorization is - (1) session validity, (2) privilege level

#### Single Sign On (SSO) - 
  * A company can have multiple web systems - asking user to create multiple accounts individually may have multiple problems.
  * Take centralized/fully decentralized/partially decentralized user databases - we've following cases - (note: assume no scaling/fault tolerance concerns) -
    - 1/0/0 - a single database for all valid users with all information related to the user for specific system (eg, privileges)
    - 1/0/1 - a single database for basic info of all valid users, and system specific databases for further information
    - 0/1/0 - all user databases are system specific
    - 0/1/1, 0/0/1 aren't possible because partially decentralized doesn't work without centralized.
    - 0/0/0, 1/1/1, 1/1/0 - makes no sense
  * Now the various web systems can - (1) have the same DNS parent, (2) have different DNS parent (eg, abc.shopify.com, xyz.shopify.com)
  * For systems which have same DNS parent, one can use cookies as an authentication mechanism across systems - ie, SSO.
  * For different DNS parent though, individual authentication would be required.
  * In either of above, authorization will require more system specific info (unless we store privilege info in cookies for same DNS parent case).

#### SAML
  * Open standard for security protocols.
  * Has 3 entities involved -
    - Principal - ie, some user, often human
    - Identity provider - performs - (a) complete authentication, (b) major parts of authorization
    - Service provider - backend to the user interface, makes requests to and checks for responses from identity provider before performing the requested action
  * Has following major statements (starting SAML 1.0) -
    - Authentication - authentication related information processed and retured by IdP
    - Attribute - 
    - Authorization decision - whether or not the principal is permitted to access the requested resource
  * SAML 2.0 has more features -
    - Authentication request - in SAML 1.x, authentication request was made directly to the IdP by the browser, 
    - Artifact resolution -
    - Name identifier management -
    - Single logout -
    - Name identifier mapping -
  * SAML 2.0 Workflow -
    - Service provider makes requests/queries for the principal and IdP responds accordingly with assertions, which are then used for further decisions.
    - Principal makes a request to service provider, service provider checks if any info related user exists already, if yes, makes decision.
    - If it doesn't exist, then it makes a request to IdP by redirecting user to IdP, embedding user credentials in the request
    - IdP uses the credentials to identify user, and the service provider input to create an "assertion", ie, some kind of decisions based on given info - responds.
    - This response is then used to make a request back to service provider which checks the contents for some info (Basic Assertion Fields below)
    - Presents the user with the resource if verified.
  * Basic Assertion (Response) Fields -
    - Issuer - IdP's unique ID
    - Signature - digital signature
    - Subject - identity information of the principal
    - Conditions - conditions for the assertion to be valid, eg, session expiry
    - Attributes - can have any key-value pair, eg, principal's privileges
    - Authorization Decision - whether the IdP's assertion permits the principal for the requested query
    - Artifact -
  * Communication Protocols, Data Structure and Security Additions -
    - HTTP, TLS -
    - XML, XACML, Encryption -
