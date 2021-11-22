### Web Browsers
  * Browser/Layout/Rendering Engine -
    - Transforms HTML and other resources to an interactive visual representation on user's device. Creates the visual structure (layout) and fills it up (render). 
    - Enforces security policies, handle web navigation, data submission via forms, implements DOM data structure.
    - Are used outside web browsers as well, eg, email clients.
    - Ex. Blink (Chromium), Gecko (Firefox, Thunderbird), Webkit (Safari, all iOS browsers)
  * JS Engine -
    - Communicates to the browser engine via DOM.
  * Other Features -
    - Caching
    - Browsing history
    - Storing passwords
    - Bookmarks
  * Network Security Services - Collection of libraries to support cross platform development of security enabled clients/servers, with support for hardware
    acceleration and smart cards.

#### Security Features Of Browsers
  * Cookies
    - Stores login creentials, site preferences as well as tracking user behaviour.
    - 
  * Local Storage -
  * SSL/TLS -
  * HTTPS -
  * Certificate Transparency
  * Secured Context - 
  * Content Security Policy, CORS, Strict Transport Security
  * Private Browsing
  * NoScript - Major sources of privacy attacks are related to javascript and adobe flash player - NoScript allows whitelisting known website to run these.
  * [Google Chrome](https://safety.google/security-privacy/) doesn't really list much wrt security
  * Least Privilege Mode - when using a browser from a guest account (a least privilege account).
  * Websites need information about the browser during communication - this can allow for exploitation of vulnerabilities in specific browser versions as well.


### Security Practices

#### Basic Authentication
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


### OWASP - Application Security Verification Standard
  * Something like a set of metrics or guidebook for developing secure applications. Following levels -
    - Level-1 - Low assurance, existence of this level of security can be ensured via penetration testing (SAST/DAST find issues that should never be present)
    - Level-2 - For applications with sensitive data.
    - Level-3 - Critical applications, eg, high value transactions, sensitive personal data (health records), etc.

#### Authentication
  * A modern standard (NIST) believes the following -
    - Usernames and knowledge based authentication (eg, city one was born in) - these are public information
    - SMS/email notifications - restricted authenticators
    - Passwords (memorized secret) - already breached - so password history, complexity and rotation is useless (according to the standard).
  * Password Security - eg, PINs, security patterns, passphrase, pick the correct image, etc.
    - MFA is almost a must have - via existing tokens or third party MFA services.
    - Users have established identities on other services, eg, FB.
    - All requirements are mandatory for all 3 levels.
    - Requirements - (a) min 12 characters, (b) allowed passwords - min 64 and max 128 characters, (c) allow neutral characters like emojis in password, (d) password
      change requires previous password, (e) users should be able to change their password, (f) 
  * Authenticator Security
  * Authenticator Lifecycle - 
  * Credential Storage - these can't be checked via pentesting, all requirements are Level-2 and above.
    - Requirements - (a) passwords should be salted and hashed (to be resistant to offline attacks), (b) salt - min length 32 bit, chosen arbitrarily to avoid
      collision among credentials - **shall** store a unique salt and hash for every credential to be stored, (c) if PBKDF2 is used, iteration count to be a huge
      number, recommended min value 100,000, (d) if bcrypt is used, work factor to be large, recommended min value 10, (e) additional iteration of key derivation fn
  * Credential Recovery
  * Lookup Secret Verifier
  * Out of Band Verifier
  * One Time Verifier
  * Cryptographic Verifier
  * Service Authentication - needs a source code review as it deals with intra application security.

#### Session Management
  * Following - (a) sessions should be unique to a user, and can't be guessed/shared, (b) invalidate sessions when not required, timeout shortly after inactivity
  * Fundamental Session Management Security -
    - Requirement - application can't reveal session token in URL params.
  * Session Binding -
    - Requirements - (a) new session token on user authentication, (b) min 64 bits of entropy for session token (ie, min 2^64 values of token), (c) session tokens
      to be stored in browser via secure cookies or HTML5 session storage, etc, (d) generate session tokens using approved cryptographic algorithms
  * Session Termination -
    - Requirements - (a) logout and expiration should invalidate session token and gimmicks like back button shouldn't resume an authenticated session,
      (b) if not logging out automatically, then perform re-authentication periodically (whether active or idle) - varies according to Level, (c) after a password
      change, allow termination of all other sessions (preferably do it automatically - although (b) should ensure that), (d) users should be able to view and logout
      of all active sessions and devices.
  * Cookie Based Session Management -
    - Requirements - (a) cookie based tokens to have 'secure' attribute, (b) they should also have 'HttpOnly' attribute, (c) they should also utilize 'SameSite'
      attribute to prevent CSRF attacks, (d) they should also use the "__Host-" prefix to send it to hosts that initially set it => are browsers supporting this?
      (e) 
  * Token Based Session Management -
    - Requirements - 
  * Federated Re-Authentication -
    - Requirements -
  * Defenses Against Session Management Exploits - this is concerned with multiple active sessions simultaneously, and half open attacks (half authenticated users).
    - Requirements - ensure a fully valid login session, or require re-authentication or secondary verification before sensitive transactions and account changes.

#### Validation, Sanitization and Encoding
  * Most common security vulnerablity. Leads to all major attacks - (a) SQL injection, (b) XSS, (c) file system attacks, (d) buffer overflows, etc. Following -
    - Input validation and output encoding - should work together to prevent injection (SQL injection, non-persistent XSS, etc).
    - Input data should be strongly typed, validated, range and length checked - at least, sanitized or filtered.
    - Output data to be encoded or escaped as per the context.
  * Input Validation -
  * Sanitization and Sandboxing
  * Output Encoding and Injection Prevention -
    - Requirements -
  * Memory, String and Unmanaged Code - only when application uses systems language or unmanaged code.
    - Requirements - (a) use memory safe string (??), safe memory copy and pointer arithmetic - to detect/prevent stack/buffer/heap overflows, (b) format strings
      to not take external/unknown/hostile inputs, (c) sign, range and input validation to prevent integer overflows (already handled in many OO languages)
  * Deserialization Prevention -
    - Requirements - (a) serialized objects should use integrity checks (isn't that quite impractical?), or are encrypted to prevent hostile object creation or data
      tampering, (b) XML parsers to use the most restrictive configuration possible (avoiding unsafe features like external entity resolution), (c) avoid the
      deserialization of untrusted data - also check if third party libraries are doing any such thing (eg, JSON/XML/YAML parsers).

#### Communication
  * Following -
    - Require TLS and strong encryption, irrespective of the data criticality - stay current with the changing recommendations on TLS, using latest versions.
    - Follow latest guidance - especially on configurations and preferred algorithms/ciphers - check configurations periodically to ensure secure communication.
    - Avoid weak or soon to be deprecated algorithms/ciphers.
    - Disable deprecated or known insecure algorithms/ciphers.
  * Client Communication Security - all communication using TLS-1.2 or above.
    - Requirements - (a) TLS should be used for all client connectivity, (b) use updated TLS testing tools to ensure that only strong cipher suites are enabled and
      strongest are being used, (c) use the latest version of TLS (1.2/1.3 or whatever is approved)
  * Server Communication Security - min Level-2.
    - Requirements - (a) connections to/from server should use trusted TLS certificates. for internal communication, trust only internal certificate authorities  and
      self-signed certificates, (b) 

#### API and Web Services
  * Applications using JSON/XML/GraphQL (and other service layer APIs) should have the following -
    - Authentication, session management and authorization of all web services - in adequate amounts??
    - Input validation of all parameters moving from lower to higher trust levels.
    - Effective security controls for all APIs - including cloud and serverless.
  * Generic Web Service Security -
  * Restful Web Services -
  * SOAP Web Services -
  * GraphQL Web Services -


#### Configuration
  * Following -
    - Application should have a secure, repeatable and automatable environment.
    - Hardened third party library, dependency and configuration management - outdated and insecure components to be rejected by the application.
  * Build and Deploy -
  * Dependency
  * Unintended Security Disclosures -
  * HTTP Security Headers -
  * HTTP Request Header Validation
