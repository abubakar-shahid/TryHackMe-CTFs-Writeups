# DockMagic

## Challenge Information

* **Challenge Name**: DockMagic
* **Category**: Web
* **Difficulty Level**: Medium

## Investigation Steps

1. **Perform Nmap Scan**: Since we are given an ip address only, lets try out the nmap `nmap -sC -sV -A -T4 <IP_ADDRESS>`. This nmap command performs the following actions:

   * `-sC`: Runs default scripts from Nmap's script engine for additional service information.
   * `-sV`: Detects service versions of open ports.
   * `-A`: Enables OS detection, version detection, script scanning, and traceroute.
   * `-T4`: Sets the timing template to "aggressive" for faster scanning.
   * `IP_ADDRESS`: Specifies the target IP address to scan.

   The result of the command is as follows:

   ```text
   # nmap -sC -sV -A -T4 10.10.67.200
   # Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-12-21 01:59 PKT
   # Nmap scan report for site.empman.thm (10.10.67.200)
   # Host is up (0.22s latency).
   # Not shown: 997 closed tcp ports (conn-refused)
   # PORT     STATE    SERVICE VERSION
   # 22/tcp   open     ssh     OpenSSH 8.4p1 Debian 5+deb11u1 (protocol 2.0)
   # | ssh-hostkey:
   # |   3072 e6:b7:14:81:2d:c6:43:bd:f7:8e:ee:b3:7e:32:d3:09 (RSA)
   # |   256 7d:64:9d:6c:8d:24:9d:53:b4:7a:ac:c8:f9:da:8b:74 (ECDSA)
   # |_  256 d1:30:1a:39:c6:46:9a:47:91:12:c6:4d:0d:b9:4e:26 (ED25519)
   # 80/tcp   open     http    nginx 1.18.0 (Ubuntu)
   # |_http-server-header: nginx/1.18.0 (Ubuntu)
   # |_http-title: EmpMan
   # 6692/tcp filtered unknown
   # Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

   # Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
   # Nmap done: 1 IP address (1 host up) scanned in 33.04 seconds
   ```

2. **Identify the Hostname**: The result shows some open ports, out of which 1 is running on http '80' with a title 'EmpMan'. We can also observe a line `Nmap scan report for site.empman.thm (IP_ADDRESS)`. Nmap automatically resolves the hostname if the target server is configured with one. In this case, it identified `site.empman.thm`. If Nmap had shown something different, that would have been used instead.

3. **Add the Host to Host Configurations**: However, to visit this site, we have to add it in our host configurations. Simply, run the command `echo "<IP_ADDRESS> site.empman.thm" >> /etc/hosts` and now you can access the domain.

4. **Access the Main Website**: When we open the link `http://<IP_ADDRESS>`, it redirects us to the `site.empman.thm` which means that there might be other hosts.

5. **Brute Force the Subdomains**: So lets just brute force the subdomains. Using command `gobuster vhost -u http://site.empman.thm -w /usr/share/wordlists/SecLists/Discovery/DNS/subdomains-top1million-5000.txt` gives another host `backup`.

6. **Add the Backup Host**: So jsut add this to the etc/hosts in the similar way as done before `echo "10.10.67.200 backup.empman.thm" >> /etc/hosts`.

7. **Access the Backup Host**: Open the link `http://backup.empman.thm`. It will reveal a webpage containing a zip file named `ImageMagick.zip`.

8. **Download the File**: Download this file.

---
