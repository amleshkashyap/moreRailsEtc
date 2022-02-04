### OWASP Top 10 Attacks
  * Broken Access Control - Since 2017
    - Even if an application has implemented access control, it might not be complete - SAST/DAST can't identify this. They can identify whether implemented or not.
    - Can remain undetected due to weak automation for detecting this, as well as lack of functional testing.
    - Effects - attacker can enter with higher privileges.
    - Vulnerabilities and Methods -
      1. Modify the URL, HTML page, using custom API attack scripts, etc
      2. Permit/View/Edit other users content. Allow the primary key to be changed.
      3. Elevation of privileges.
      4. Replaying or tampering a JWT access control token, cookie, hidden field manipulation (application specific) to elevate privileges.
      5. CORS miconfiguration - how?
      6. Access API with missing access controls for PUT/POST/DELETE

  * Cryptographic Failures (Earlier, Sensitive Data Exposure) - Since 2017
    - Stealing of keys, clear text data from servers, man in the middle attacks.
    - Unencrypted sensitive data, weak key generation, weak algorithm/protocol/cipher usage, etc.
    - Data in transit is easier to steal than the ones at rest.
    - Vulnerabilities and Methods -
      1. Passwords, credit card info, health records, personal info, business secret - are these in clear text? HTTP, SMTP, FTP protocols.
      2. Internal traffic - load balancers, web servers, backend
      3. Sensitive data and backup storage - clear text?
      4. Browser security directives and headers missing? Verification of server certificate not performed?
      5. Old crypto algorithms.

  * Injection (Including - Cross Site Scripting XSS) - Since 2003
    - Environment variables, parameters, external/internal web services, users - these can potentially inject data in the application.
    - Prevalent in legacy systems - SQL queries, LDAP (for directory based authentication), XPath (query language for parsing XML), NoSQL queries, OS commands,
      XML parsers, SMTP headers, ORM queries. Scanners and fuzzers can find these vulnerabilities.
    - Vulnerabilities and Methods -
      1. User supplied data isn't validated, filtered, sanitized.
      2. Dynamic queries executed without proper escaping.
      3. Needs thorough automation testing of - parameters, headers, URL, cookies, JSON, SOAP, XML data inputs - these are also the target of most Zaproxy attacks.
    - XSS - Found in 2/3rd of applications. Automated tools can find all three forms of this vulnerability for established frameworks. Following types -
      1. Non-persistent - Can occur when data provided by web client (via query params mostly), is parsed and displayed by the server without proper sanitization.
         HTML documents have a structure wherein control statements, formatting and actual content are present. When client sends some data to the server, the data
         may contain malicious code, which, if not sanitized, will be sent as it is to the client for display, and the client (browser) will execute that code.
      2. Persistent - Unlike the above, in this attack, nothing needs to be rendered, rather a script is embedded by a user in their own DB info - then when another
         user opens their info, the script is executed, thus collecting information about the other person silently.
      3. DOM XSS - JS frameworks and SPAs.
    - Effects of XSS - Dangerous when server is executing unexpected code on client's browser.
    - Escaping - Replacing some special characters (eg, <, >, ", &, etc) with others. Inbuilt functions are present in some languages for this.

  * Insecure Design - Since 2021
    - CWEs - Generation of error messages containing sensitive information, unprotected storage/insufficient protection of credentials
    - A secure design might have imperfect implementation which will lead to a different set of vulnerabilities.
    - Secure design constantly evaluates threats - eg, looking for changes to the data flow, or access control.
    - Suitable to have a professional do the evaluation.
    - Compilation of use cases and misuse cases for the every service/features, limiting the resource consumption by each user/layer/tier.

  * Security Misconfiguration - Since 2017
    - Access default accounts, unused pages, unprotected files/directories - gives more knowledge of system.
    - Can be done at any level of the stack - network services, web server, application server, DB, framework, VMs, containers, storage, etc - how??
    - Effects - Can result in limited data access to complete control of the system.
    - Vulnerabilities and Methods -
      1. Improper configurations on cloud services.
      2. Unnecessary features - ports, services, pages, accounts, privileges
      3. Default account/password enabled and unchanged.
      4. Error handling reveals lot of information (full stack traces).
      5. Latest security features not enabled/not configured.
      6. Security settings of application server, web framework, libraries and DB are not set to secure values.
      7. Security headers/directives (eg, [this](https://github.com/github/secure_headers)).
      8. Out of date or vulnerable software.

  * Vulnerable and Outdated Components - Since 2017
    - Known vulnerabilities will generally have existing scripts to exploit them - new vulnerabilities have to be identified and exploited which is hard.
    - Effects - Known vulnerabilities in critical application components can be very harmful.
    - Vulnerabilities and Methods -
      1. Version of client/server side components and libraries.
      2. Other vulnerable/unsupported components like OS, web server, DBMS, APIs, runtime environments, libraries.
      3. Security misconfigurations above.
      4. Updates and scans for recently found vulnerabilities.

  * Identification and Authentication Failures - Since 2003
    - Session management attacks for unexpired session tokens.
    - Attackers have existing list of username/password, also usage of dictionary attacks.
    - Confirmation of user identity, authentication, and session management are critical.
    - Vulnerabilities and Methods -
      1. Reusing passwords is common for users - allowing credential stuffing is insecure.
      2. Allowing brute force/other automated attacks.
      3. Allowing default, well known and weak passwords.
      4. Allowing weak credential recovery - eg, knowledge based answers.
      5. Allowing plain text, encrypted, weakly hashed passwords.
      6. Missing multi-factor authentication.
      7. Not invalidating session IDs - user sessions and authentication tokens (eg, SSO tokens) aren't invalidated for a long period.
      8. Expose session ID in URL.

  * Software and Data Integrity Failures - Since 2021
    - CWEs - Inclusion of functionality from untrusted control spheres, downloading code without integrity checks, deserialization of untrusted data.
    - Applications relying upon - plugins/libraries/modules from untrusted sources, CDNs, insecure CI/CD pipeline, updating the app without integrity checks.
    - Tools - Dependency Check, CycloneDX from OWASP for components without any known vulnerabilities.

  * Security Logging and Monitoring Failures - Since 2017
    - Systems can be exploited for long durations without being detected.
    - Check the logs after penetration testing - the actions should've been recorded sufficiently to understand the potential damages.
    - Most attacks start by probing for vulnerabilities and assessing whether their actions are being monitored (ie, whether vulnerabilities are removed quickly).
    - Vulnerabilities and Methods -
      1. Insufficient logs for - logins, failed logins, critical transactions
      2. No monitoring of logs, especially for suspicious activity.
      3. Penetration testing and scans by DAST tools don't generate alerts.

  * Server Side Request Forgery (SSRF) - Since 2021
    - Occurs when a webserver fetches from a remote resource without validating the user supplied URL - an attacker can make the server fetch unsafe items.
    - Increasing prevalence due to a drive for user convenience.
    - Prevention -
      1. Segregation of remote resource access functionalities in a separate network.
      2. Sanitize and validate client supplied data, disabling HTTP redirections, not sending raw responses back to client, enforcing scheme/port, etc.


### Older OWASP Top 10 Attacks
  * XML External Entities - 2017
    - Application accepts XML directly from untrusted sources
    - Application injects untrusted data into XML, followed by processing of that XML
    - Effects - extract data, execute remote request from server, scan internal systems, perform DoS and other attacks.
    - Maybe easier to detect via SAST tools than DAST.

  * Insecure Deserialization - 2017
    - Deserialization of JSON/XML/YAML is common - this attack, if successfully planned, can execute arbitrary code while deserialization. A deserialized object
      is often directly converted to a data structure in the application.
    - Other places where deserialization occurs - caching, persisting to DB and file system, authentication tokens, cookies, HTML form params, network protocols.
    - Effects - If executed successfully, then very severe.
    - Only way to prevent this is to not accept serialized objects from untrusted sources, or serialize only using primitive data types.

  * Insecure Direct Object Reference - 2004, 2007

  * Failure to Restrict URL Access/Missing Function Level Access Control - 2003-2013

  * Cross Site Request Forgery - 2007-2013
    - Session information stored in browsers can be utilized to access components of the target website by sending content to a victim which has hidden URLs which
      perform malicious operations unknown to the victim.

  * Unvalidated Redirects/Forwards - 2013

  * Insecure Communications/Insufficient Transport Layer Protection - 2003-2010

  * Insecure Cryptographic Storage - 2003-2010

  * Malicious File Execution - 2007, 2010
    - Direct usage of potentially hostile inputs - frameworks allow usage of external object references - URL and file system references. Prevalent with PHP.

  * Information Leakage and Improper Error Handling - 2003-2007
    - Leakage of internal workings, configurations, sensitive data, internal state (eg, time taken for operations, different responses to slightly different inputs),
      detailed debug error messages (stack traces, failed SQL queries). A function for login should ideally generate same text for no user/bad password inputs.


### Other OWASP Attacks
  * CSV Injection -
    - In CSV files, a cell starting with = is treated as a formula. Also, a normal cell can be ended using "," or ";" and then new entries started with =.
    - If application is allowing uploading of CSV files, or converting user input to CSV and uploading it to server, then restrictions are required.
    - Formula can be utilised for -
      1. 
      2. 
      3. 
    - 
  * Host Header Injection -
    - Virtual Hosting -
      1. Name based - 
      2. IP Address based -
      3. Port based -
    - 
  * Typosquatting -
    - Owning domain names created by changing spelling of the original domain - eg, Goggle.com - and hosting ads, alternative apps or other malicious apps.
    - Also created using different top level domain, eg, .co, .com, .org, .cm, etc


### Common Weakness Enumeration
  * Another list of security weaknesses for softwares and hardwares - huge list.
  * [Software](https://cwe.mitre.org/data/definitions/699.html)


### Components That Facilitate Attacks
  * Cookies -
  * Headers -
  * URLs -
  * Body -
  * Code -
  * Architecture -

### Which Components Can Be Exploited By An Attack
  * Database
  * Files
