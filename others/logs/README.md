## General

### Ubuntu Logs
  * [Source](https://help.ubuntu.com/community/LinuxLogFiles)

#### System Logs
  * Authorization - tracks usage of authorization system, eg, Pluggable Authentication Module, sudo command, remote logins to sshd. Stored at /var/log/auth.log
    - Ex. grep sshd /var/log/auth.log | less

  * Daemons - Stored at /var/log/daemon.log - contains information about system and application daemons.
  * Debug - Stored at /var/log/debug and provides detailed information about Ubuntu and applications which log to syslogd at DEBUG level.
  * Kernel - Stored at /var/log/kern.log and provides detailed information about kernel.
  * Kernel Ring Buffer - Not really a log file but an area in running kernel which can be queried for kernel bootup messages via dmesg utility.
    - Ex. by default, system initialization script /etc/init.d/bootmisc.sh sends all bootup messages to /var/log/dmesg as well.
  * System - Stored at /var/log/syslog and contains the most amount of details. Also contains everything that used to be in /var/log/messages

#### Application And Other Logs, Daemons
  * Many applications also create logs in /var/log - eg, apache, nginx, upstart.
  * Login Failures - use faillog to query the logs in /var/log/faillog
  * Last Logins - /var/log/lastlog - use lastlog to query this
  * Login Records - use who. Stored in /var/log/wtmp
  * syslogd - awaits messages from numerous sources and routes the messages to the appropriate file or network destination. Usually contain hostname, timestamp and logs.
    - Configured in /etc/syslog.conf
    - logger tool can be used to echo messages to /var/log/syslog
  * More commands
    - klogd - kernel log daemon logs
    - savelog - log file saving utility

#### More Logs
  * [Source](https://stackify.com/linux-logs/)
  * /var/log/utmp - current login state by user
  * /var/log/btmp - recording of failed login attempts
  * /var/log/pureftp.log - FTP logins and auth information for pureftp
  * /var/log/xferlog - 
  * /var/log/mail.log - logs for email related services running on the machine, eg, postfix, smtpd


### Windows Logs


### Kubernetes Logs
  * Usual
  * Introduces contextual logging which reduces boilerplate code for logging.
