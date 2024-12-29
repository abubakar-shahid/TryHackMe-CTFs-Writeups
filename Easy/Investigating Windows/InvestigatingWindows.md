1. After opening the windows machine, Press [Win + R], type [msinfo32], and press Enter. This will display the informatin of the windows. The very first line, against the [OS Name] contains the answer: [Windows Server 2016].

2. To get the last logged user, Press [Win + R], type [regedit], and press Enter.
Navigate to: [HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Authentication\LogonUI]
Look for the key [LastLoggedOnUser], which will display the last user's name: [Administrator].

3. To get the exact timing for John, we can use the powershell rather than searching in the eventlogs manually. Use the command [Get-EventLog -LogName Security | Where-Object {$_.EventID -eq 4624 -and $_.Message -match "John"} | Select-Object -First 1]. It gave the Time and Date [Mar 02 17:48] but this was not in the required format. So lets add a filter:
[Get-EventLog -LogName Security | Where-Object {$_.EventID -eq 4624 -and $_.Message -match "John"} | Select-Object -First 1 | ForEach-Object { ($_.TimeGenerated).ToString("MM/dd/yyyy h:mm:ss tt") }]. This gave the exact answer: 
[03/02/2019 5:48:32 PM].
----- Or -----
Run the command in powershell [net user John]. This will give all the information about this user. In the output information, check the field [Last logon]. It gives the last login date and time [3/2/2019 5:48:32 PM]. The correct required format is [03/02/2019 5:48:32 PM].

4. Press [Win + R], type [regedit], and press Enter. Navigate to [HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run]. There will be a service named [UpdateSvc] against which under the Data column the ipaddress is mentioned [10.34.2.3].

5. In the powershell run the command [Get-LocalGroupMember -Group "Administrators"]. It will list the 3 users with administrative privileges [Administrator, Guest, Jenny]. The exact answer is [Jenny, Guest].

6. Navigate to the directory [C:\Windows\System32\Tasks]. Here are a list of tasks for the windows. Here is the malicious task located [Clean file system].

7. Open this file in the notepad and search for the command to be executed [C:\TMP\nc.ps1], giving the file [nc.ps1].

8. Very next to this line, there is a filed of Arguments in which the port is given [1348].

9. Run the command in powershell [net user Jenny]. This will give all the information about this user. In the output information, check the field [Last logon]. It is written [never], and this is the answer because Jenny never logged in.

10. If we run the [net user] command for all the users one by one, we will come to know that all the admin users were created on 2nd March, 2019. Moreover, the last logged in user [Administrator] also last logged in on the same date. So from this concept, I tried the date [03/02/2019] which was the correct answer.

11. Since the last logged in user is Administrator, he is the person who is responsible for the compromise of the system. So we will check when this user was created and given the elevated privileges. Open Event Viewer [Win + R], type [eventvwr]. Navigate to [Windows Logs > Security]. Filter for suspicious logon events: [Event ID 4624: Successful Logon]. [Event ID 4672: Special privileges assigned to new logons]. Also add a filter of the form date [02/02/2019] till date [04/02/2019] to show the logs for the [03/02/2019] only. At the time [4:04:49 PM], we can observe that a logon happened right after which a special login happened and right after that at [4:04:50 PM] the user [Administrator] was created with root previliges. So the required time and date is [03/02/2019 4:04:49 PM].

12. In the directory where the nc.ps1 file is present [C:\TMP\], there is a suspecious text file [mim-out]. Open it and we will get the tool used [Mimikatz].

13. Open the hosts file in [C:\Windows\System32\drivers\etc\hosts.txt] in notepad. It is a local configuration file used to map hostnames to IP addresses. It allows the system to resolve domain names to IP addresses before querying a DNS server. Attackers can manipulate the hosts file to redirect legitimate domains to malicious IPs for Malware Abuse. Hence, check for any connection with any browser and we will see a connection with google at [76.32.97.132], which is the required ipaddress.

14. We will check the web server's upload directory for suspicious files: [C:\inetpub\wwwroot]. Here we will find some files having extension [.jsp]. 

15. Open [Windows Firewall and Advanced Security]. Click on [Inbound Rules] and then click on [Allow outside connections for development]. Here is the port [1337] under the column [Local Port].

16. In the [hosts.txt] file, the site against which we found the C2 ip is [google.com].

