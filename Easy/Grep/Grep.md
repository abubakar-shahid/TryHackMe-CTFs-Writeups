# Grep

## Challenge Information
- **Challenge Name**: Grep
- **Category**: OSINT & Web Exploitation
- **Difficulty Level**: Easy

## Initial Enumeration

1. Since the task is of OSINT, we can clearly observe that the very first task is directly linked to it. Lets just visit the ip address given for the machine. But oops! it does not give any page. Lets run nmap on it with some details as well:
```bash
nmap -sV -A <IP_ADRESS>
```
In the complete result, we can see this kind of line `ssl-cert: Subject: commonName=grep.thm/organizationName=SearchME/stateOrProvinceName=Some-State/countryName=US`. This suggests that there is a service named `grep.thm` is running on this port. To access this service, add it to `/etc/hosts` by running the command:
```bash
echo "<IP_ADDRESS> grep.thm" | sudo tee -a /etc/hosts
```
Now open it in your browser `https://grep.thm`. This will open a webpage. If we observed the title of the room, in the right eye of the avatar, there is the logo of github. So lets just try to search this webpage in github. Go to your github account and write `Welcome to SearchME!` in the search bar. This will open a file containing this text. This file belongs to the repo `https://github.com/supersecuredeveloper/searchmecms`. Open this repo. This keyword was present in the `/public/html/index.php` file. Since we are looking for an api key, we should checkout commit history. Go to the commit history and there is a commit named `Fix: remove key`. Open this commit and there we find the api key that was removed from the code `ffe60ecaa8bba2f12b43d1a4b15b8f39`.

2. Coming back to the home page of the webapp, we can see two options. `Login` and `Register`. Since we do not have hint of any account, lets make our own account. Fill up the required fields, oops! It gives an error of expired key. So this is the place where we need that api key. We will use burpsuite to perform this registration. Open the burpsuite interception, fill in the inputs and make a request. In the captured request, there is a field for api key. Replace the api key with the one we found earlier, and forward the request. This will successfully register our account. Now go to the login page and login into the app with the same credentials that we used to register the new account. We do not need api key this time. Simple login will take use to a home page, where there is the flag in front of us `ffe60ecaa8bba2f12b43d1a4b15b8f39`.

3. If we observe the repository, there is a file `upload.php` in `/api` directory. Analyzing the code, we come to know that it allows users to upload any file on the server which is saved to the directory `/uploads`. It also checks whether the file being uploaded is valid `JPG, JPEG, PNG, BMP` or not. For this, it is checking:
```php
'jpg' => 'ffd8ffe0'
'png' => '89504e47'
'bmp' => '424d'
```
So, if need to upload any of our other format file, we have to use these headers to enumerate the file uploading. So lets just upload our reverse shell code for this. Download the php reverse shell code from `https://github.com/pentestmonkey/php-reverse-shell/blob/master/php-reverse-shell.php`. Make sure to change line 49 and 50 with your ipaddress and the port where you want to receive the reversed shell. Run this port:
```bash
nc -lvnp PORT
```
For the code of reverse shell, copy the code into a file. Open that file in CyberChef. Make its hex using the recipe `to hex`. Then add `ff d8 ff e0` in the start of that hex values. Save this file as `shell.php`. This file will act as a JPEG file. You can also verify this `file shell.jpeg` which will confirm that this file contains jpeg contents. Upload this file in the url `https://grep.thm/api/upload.php`. After successful uploading, go to the path `https://grep.thm/public/html/uploads`. Here our uploaded file `shell.php` is present. Make sure that we have our desired port already running. Now, click on this shell and it will get executed and we will get a shell on our terminal where we ran out port using nc. Now, if we studied the very first page that we found on simple `http://<IP_ADDRESS>`, we can see that the directory `/var/www` is important one. And we can also see this directory in the shell we have accessed. So lets navigate to this. Here we have some more directories, first lets just navigate to the very first one `backup` which already seems suspecious due to its name. Here, we found a `users.sql` file. Read its contents:
```bash
cat users.sql
```
And here we go! We found the email of the admin `admin@searchme2023cms.grep.thm`. Here the passoword of the admin is also given but is is hashed.

4. In the `/var/www` directory, there is also a folder named `leadchecker` in which we can a file named `check_email.php`. So most probably this is the application because it also have an index.php file as well and there are also some certificates starting with the names `leak`. So the answer is `leakchecker.grep.thm`.

5. Add this in the hosts as well:
```bash
echo "<IP_ADDRESS> leakchecker.grep.thm" | sudo tee -a /etc/hosts
```
Now we can access this on the browser as well `https://leakchecker.grep.thm`. But this is saying permission denied. Lets check for any open ports, since we have to open this webpage in any case:
```bash
nmap -sV -A leakchecker.grep.thm
```
But this is giving only 3 ports which are not accessible. It means we have to try all ports rather than only 1000 common ones. Running the command:
```bash
nmap -p- leakchecker.grep.thm
```
This will run check for all the ports. This will give as a port `51337`. So lets open the webpage with this port `https://leakchecker.grep.thm:51337/`. This takes us to a webpage where we will enter the same email that we found for the admin. On submitting the email, we will the password for the admin: `admin_tryhackme!`.
