# 

1. cat etc/machine-id

2. ubuntu@cybertees:/$ cat etc/passwd  gave a suspecious user creation in the most last line

3. untu@cybertees:$ sudo cat /var/spool/cron/crontabs/root  last line is the answer

4. ps aux | grep root  found only one binary file in toooo much long response

5. 2 processes i.e. printer_app and .strokes

6. ubuntu@cybertees:/$ ls -la

7. ubuntu@cybertees:/$ systemctl list-units --type=service   the mysterious services are obvious

8. ubuntu@cybertees:/$ strings /var/log/auth.log | grep mircoservice   the very first add command

9. ubuntu@cybertees:/$ strings /var/log/auth.log | grep ssh   and you will see the requests for login with the host ip

10. ubuntu@cybertees:/$ strings /var/log/auth.log | grep mircoservice   gives a total of 60 lines of data. use AI to detec the number of failure attempts
# Total login failures = 8
# Breakdown:
# Aug 6 01:16:41-01:17:14: 2 failures
# Aug 13 22:15:06-22:15:16: 3 failures (1 direct + "2 more authentication failures")
# Aug 13 22:15:41-22:16:12: 3 failures (1 direct + "2 more authentication failures")

11. ubuntu@cybertees:/$ grep " install " /var/log/dpkg.log   [pscanner] seemed to be suspecious among 22 packages, since it is similar to our scenario

12. buntu@cybertees:/$ dpkg -s pscanner
