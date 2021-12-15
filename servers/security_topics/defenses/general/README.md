### Security Attributes -
  * Confidentiality - only the ones who need to know, should know.
  * Integrity - data shouldn't be modified/destroyed.
  * Availability - available on demand/as required.
  * Non repudiation - creator/sender of data can't refuse doing it.
  * Authentication - identify the creator/sender.
  * Authorization - the one requesting the data must be allowed to have it if he has the privileges.


### Tools
  * Symmetric Encryption -
    - Problems - both parties need access to the key.

  * Asymmetric Encryption -
    - Problems - performance issues.

  * Hashing -
    - Problems -

  * Digital Certificates
    - Provides - confidentiality, authentication, integrity, non-repudiation
    - Uses - asymmetric encryption with a public key that is attributable to the owner, hashing
    - Certificate Authorities
      - Problems - can't be relied upon as it involves humans.
    - Problems -

  * End to End Encryption -
    - Problems -

  * Steganography -


### Other Tools
  * Firewalls -

  * Antivirus -
    - No algorithm can perfectly detect all possible viruses.
    - Sandbox detection - tries to execute the program (ie, a potential malware code in a file) in a virtual environment and guessing whether the actions performed by
      the program are malicious or not. Can be very slow, not used widely.
    - Data mining - classify the behaviour of a file as containing a potential malware based on a set of features. Lower accuracy though - a malware writer needs to get
      lucky just once, even a 99.99% accuracy doesn't mean anything (for critical machines at least).
    - Signature based - some kind of signature extracted from known malwares manually or via dynamic code analysis (what exactly?) - then added to the antivirus DB.
      Malwares can partially encrypt themselves or modify themselves after they're done (for the day, say) to avoid matching the existing signatures - so releasing the
      signature generation process might be dangerous too.
    - Heuristics - to capture family of viruses (eg, ).
    - Rootkit detection - Rootkit viruses aim to have complete control of the OS, thus being able to change the antivirus permissions too.
    - Real time protection - when opening emails, using browsers, opening files, connecting external disks, etc.

  * Honeypots - ex. canary tokens

  * Digital Rights Management - 

  * Others - [device guard](https://techcommunity.microsoft.com/t5/iis-support-blog/windows-10-device-guard-and-credential-guard-demystified/ba-p/376419),
    [RASP](https://en.wikipedia.org/wiki/Runtime_application_self-protection)

  * Other General Methods -
    - Update system
    - Strong and unique passwords
    - 2-FA/MFA
    - Password manager
    - HTTPS only
    - Using Linux and antivirus softwares
    - Browsing known websites only
