# Pickle Rick

## Challenge Information
- **Challenge Name**: Pickle Rick
- **Category**: Web Exploitation
- **Difficulty Level**: Easy

## Investigation Steps

1. **Initial Reconnaissance and Access:**
First of all, I opened the URL and read the paragraph appearing on the screen carefully. It said that "logon to my computer and find the last three secret ingredients to finish my pickle-reverse potion." It also said that I do not know my password. Hence, the username must be somewhere near. So I opened the source code page and found the username `R1ckRul3s` in the comments. Now we had to find the login page. So I used `gobuster` for directory enumeration using the command:
```bash
gobuster dir -u http://<ip_address>/ -w /usr/share/wordlists/dirb/common.txt -x php,html,txt
```
This gave me some files: `login.php`, `robots.txt`, etc. I opened the `robots.txt`: `http://<ip_address>/robots.txt`, where I found a string `Wubbalubbadubdub` which I doubted that it must be the password. However, now I opened the `login.php` page: `http://<ip_address>/login.php` and a login form appeared. Here I entered the username `R1ckRul3s` and password `Wubbalubbadubdub` which successfully logged me into the dashboard. Now on the dashboard, an input field was appearing with a placeholder "Commands" with a button "Execute". So I executed the command `ls` which gave me some files. On the top, there was a text file `Sup3rS3cretPickl3Ingred.txt`. I opened it in the browser: `http://<ip_address>/Sup3rS3cretPickl3Ingred.txt`, and it gave me the first answer: **mr. meeseek hair**.

2. **Finding Second Ingredient:**
There was another file `clue.txt`. I also opened that in the browser: `http://<ip_address>/clue.txt`. This gave a clue to look around the file system. So, I ran the following commands:
```bash
whoami
ls /
ls /home/
ls /home/rick/
cat /home/rick/"second ingredients"
less /home/rick/"second ingredients"
```
The 1st command revealed the logged in user: `www-data`. Then the 2nd command gave the main directory where I then found the home directory and followed the rick where I found the second ingredient file. On using the `cat` command, it showed a warning. So I used `less` command which revealed the second answer: **1 jerry tear**.

3. **Finding Third Ingredient:**
Since, there is no other main clue on the entire webpage, and we found 2 answers within the filesystem. So, it means that we have to find the last one here as well. Let's try to see `/root` directory:
```bash
ls /root
```
but it showed nothing. Let's try to access it using the `sudo` command:
```bash
sudo ls /root
```
and boom! It did not ask for any password. But why did this happen? Let's check this:
```bash
sudo -l
```
which shows that root can do anything without the password. However, the root directory contains the 3rd file. Let's read its content:
```bash
sudo less /root/3rd.txt
```
and finally! It gave the 3rd answer as well: **fleeb juice**.
