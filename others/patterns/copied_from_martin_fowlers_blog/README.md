### High Level Discussions
  * Architecture - 

  * QA In Production -
    - Capture the behaviours of the application in production.
    - Are they working as expected? What is not working? What can be improved? What are repetitive and commonly used steps which can be isolated?
    - It doesn't matter if a system can serve thousands of requests if it is functionally incorrect.
    - Ex - take user input, send email - one could track the number of user inputs taken and emails sent and capture mismatch. Can also capture emails which failed
        via the API immediately [to be captured in logs].
    - Ex - count how many times user starts an application but doesn't submit it - is the UI a problem? the browser? or just the user is disinterested?
    - Logs need to be very structured to automate multiple processes, including alerts. Metrics can be captured as well and logged/notified.
    - All of the above doesn't work if there's no alert and no easy way to look at what is going on - dashboards are needed.
    - [Source](https://martinfowler.com/articles/qa-in-production.html)
