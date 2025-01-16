# IronShade

## Challenge Information
- **Challenge Name**: IronShade
- **Category**: Forensics
- **Difficulty Level**: Medium

## Investigation Steps

### Step 1: Check Machine ID
`cat etc/machine-id`

### Step 2: Check Suspicious User Creation
`ubuntu@cybertees:/$ cat etc/passwd` gave a suspicious user creation in the last line.

### Step 3: Check Root's Crontab Entries
`ubuntu@cybertees:/$ sudo cat /var/spool/cron/crontabs/root` last line is the answer.

### Step 4: Search for Root Processes
`ps aux | grep root` found only one binary file in a very long response.

### Step 5: Identify Suspicious Processes
2 processes i.e. `printer_app` and `.strokes`

### Step 6: List All Files with Permissions
`ubuntu@cybertees:/$ ls -la`

### Step 7: List All Running Services
`ubuntu@cybertees:/$ systemctl list-units --type=service` the mysterious services are obvious.

### Step 8: Search for Microservice Additions
`ubuntu@cybertees:/$ strings /var/log/auth.log | grep mircoservice` the very first add command.

### Step 9: Check SSH Login Attempts
`ubuntu@cybertees:/$ strings /var/log/auth.log | grep ssh` and you will see the requests for login with the host IP.

### Step 10: Analyze Microservice Login Failures
`ubuntu@cybertees:/$ strings /var/log/auth.log | grep mircoservice` gives a total of 60 lines of data.

### Login Failure Analysis
- **Total login failures**: 8
- **Breakdown**:
  - Aug 6 01:16:41-01:17:14: 2 failures
  - Aug 13 22:15:06-22:15:16: 3 failures (1 direct + "2 more authentication failures")
  - Aug 13 22:15:41-22:16:12: 3 failures (1 direct + "2 more authentication failures")

### Step 11: Check Installed Packages
`ubuntu@cybertees:/$ grep " install " /var/log/dpkg.log` `pscanner` seemed to be suspicious among 22 packages, since it is similar to our scenario.

### Step 12: Check Pscanner Package Details
`ubuntu@cybertees:/$ dpkg -s pscanner`
