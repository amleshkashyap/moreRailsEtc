### Malwares
  * Following seem to be true about most/all of the malwares -
    - In terms of design and development of core functionality, it *may* not be very different than general system/web applications.
    - More significant challenges seem to be with -
      1. Deployment - injecting successfully without giving away identity. This also includes considerations about the target machines for deployment wrt the code.
      2. Executing the software on demand/as required. On demand execution might not be required for all types of malware though.
      3. Fault Tolerance - remaining undetected/indestructible till it's purpose isn't served.
      4. Preserving identity (and/or destroying itself) if captured. It might be difficult for a malware to know that it's been captured though.

  * [Macro virus](https://en.wikipedia.org/wiki/Macro_virus)
    - Macros are rules which help mapping an input to another output. These are present everywhere, application softwares, programming languages, keyboards, etc.
      1. Vim allows us to type a set of characters for deleting, substituting, searching a keyword, etc.
      2. VBA (like most programming languages) supports macros which has access to Windows system calls - VBA scripts can be run from office applications like Word
         and Excel too (macro virus is different from CSV injection though).
      3. Other softwares exist which are specifically made for recording and replaying keyboard and mouse actions for automation.
    - These viruses can attempt for a wide range of exploits.
    - A file containing a malicious macro can execute the later as soon as opened - exploitation is based on privileges allowed to the macro.
    - This file will generally be a application software file like word processor. Also the email attachments. Not all such virus can be detected by antiviruses.
    - See - [kas](https://www.kaspersky.com/resource-center/definitions/macro-virus)

  * [Stealth virus](https://www.techopedia.com/definition/4130/stealth-virus)
    - The goal seems to be that of a typical virus - destroying a file system.
    - Attempts to keep itself out of reach of antiviruses (see how antiviruses detect malwares) -
      1. Hide destroyed files in system memory.
      2. Copy itself to undetectable areas of the computer - which are?
      3. Might change extensions/encoding of each file, and possibly encrypt them with different keys.
    - Can be very hard to detect and remove permanently.
    - See - [kas](https://www.kaspersky.com/resource-center/definitions/stealth-virus)

  * [Polymorphic virus](https://www.techopedia.com/definition/4055/polymorphic-virus)
    - Almost all good, modern viruses will be polymorphic - this would be to avoid detection.
    - Detecting them might involve brute force searches - what would be the search space?
    - See - [kas](https://www.kaspersky.com/resource-center/definitions/what-is-a-polymorphic-virus)

  * Bots, Zombies and Worms -
    - Bots - mostly scripts for running automated tasks - over the internet, eg, spiders.
    - Botnet is a set of devices connected via the internet, with each device running one or more bots. Typical usage other than harming host - spamming, ddos attacks.
    - Protocols - HTTP, IRC but now they're mostly peer to peer, even using digital certificates to identify reliable malware to add to the network.
    - Zombies are the computers infected with a malicious bot.
    - It's one of the ways to avoid detection - spamming and launching ddos attacks from the zombie system via the malware - if caught, it's the host computer.
    - Worms - Replicates itself to spread to other computers, often via network.

  * Rootkits -
    - OS and firmware rootkits -
    - Good rootkits -
    - Mechanism -

  * Key loggers -
    - Monitoring keystrokes - can be in software or hardware - these are not illegal and even used for monitoring employees.

  * Trojan Horse -
    - A bad software disguised as a good one.
    - Can attempt to connect to external bots for instructions on what to do - that must be done via a port.
    - Other malwares can control (at least in theory) and use it for harm - and remain harder to catch.

  * Remote access tools -
    - Legitimate way to gain control over a remote computer - eg, teamviewer, anydesk, even MS Teams gives an option to do this. Malcious ones are available too.

  * Ransomware and Scareware -
    - Most used mode of operation is to encrypt the files on the victim system using a randomly generated symmetric key, which is itself encrypted using another public
      key of the attacker - only the attacker can decrypt the symmetric key using his private key when the victim sends it to him along with some financial instrument.
    - Other types may include restricting access to the system itself instead of encrypting the files, or copying the files and threatening to publish them.
    - Mostly carried out using a Trojan Horse.
    - Scareware - They create fear in the user's about existence of threats in their systems, asking them to install paid software for remedy which might in turn be
      a real malware. Scareware can also be fake threat emails containing info about the victim (but mostly public info) and asking them to pay.

  * Malvertisements, Adwares and Spywares -
    - Malvertisements - Injecting malwares into legitimate advertisements. Most websites have ways to inject advertisements into webpages, making it easier to have
      an existing target location without having to focus on infecting the whole website.
    - One of the ways of operation is to post genuine ads for some time, gaining the website's trust, and later replacing those by malvertisements till detection.
    - Adwares - These are tools for auto-generating advertisements, often without the consent of the user - most of these generated ads are just annoying extra ads,
      but can sometimes perform malicious operations (eg, malvertisements). Other times, these tools might just monitor user activity.
    - Most free softwares on app store are also adwares. Check for the permissions they require, as they might also collect data.
    - Spywares - These softwares silently collect and send information of the host they're installed on. Even completely legitimate softwares can be spywares - apps
      like Google Maps are practically spywares, and most of the social media websites too, including the ones which are selling our data to advertisors.
    - Paid versions of softwares maybe a way to get rid of the ads, but do they stop spying? Informed consent is the term thrown lately to characterize spywares.
    - Lenovo is a large company which used to sell laptops pre-installed with Superfish adware. Any installation with add-ons may contain adwares.

  * Potentially Unwanted Programs -
    - Drive By Attacks - Users can unintentionally download files to their system which might be malwares.

  * Crypto Mining Malware -
    - These malwares don't cause problems with CIA triad, and rather steal the computing resources of the victim for performing crypto mining.
    - Many websites have such malware running in the background when the user visits them, slowing the user's system without their consent.


### Other Threats
  * Browser Hijacking -

  * Spamming

  * Doxing
    - A form of online stalking, acquiring public or semi-public information about people and making them available publically with attention.
    - Very few laws against it.

  * SSL Splitting
    - It's a kind of man in the middle attack. Generally hard to perform because one needs to have control over a network where others are connected to.
    - It involves sitting between the actual client and server, sending https requests to server but communicating with the client using http, thus
      capturing all the information in plaintext - advisable to avoid http based websites always. One can provide their own network in public areas and potentially
      perform this attack.

  * Backdoors
    - Backdoors can be due to programming errors or intentionally provided - in both cases, they're available for everyone to exploit.
