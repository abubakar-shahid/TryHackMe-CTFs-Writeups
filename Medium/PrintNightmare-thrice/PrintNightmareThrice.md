# In the task, we are given a pcap file and a .log file. We will be reading each question, and deciding on the spot that which file will be used to answer the specific question. we will be using wireshark or brim for file capture analysis, and process monitor for log analysis.

1. Use wiresahrk to analyze the pcap. Since the PrintNightmare exploit often involves SMB (Server Message Block), use the filter [smb]. This will give only 4 requests, identify the unique one and its ip [20.188.56.147].

2. Since authentication is used, use the filter [smb2]. This will give all the authentication requests. Identify the failed response, and check the user of the request of this response. If the complete user is not visible in the request completely, just click on the request. Go to [SMB2->SMB2 Header->Session Setup Request->Security Blob->GSS-API Generic Security Service Application Program Interface->Simple Protected Negotiation->negTokenTrag->NTLM secure Service Provider]
here you will see multiple fileds assossiated with authentication. The complete username is Domain name\User Name [THM-PRINTNIGHT0\rjones].

3. Similarly as done in the above task, now identify the successful connection request. The process is entirely same. The answer pattern is a little different Domain name/User Name [THM-PRINTNIGHT0/gentilguest].

4. In the same filter, look for the first successful request, that is already found in the above task. Note down the endpoint that the user gets connected to, by going to the path [SMB2->Tree Connect Request->Tree]. Here you will find the exact endpoint. Now look in the traffic again, and observe in the request that identify the creation of files. The first two ones are the required files. You can also simply identify the files and their path by going to the export objects option in wireshark, select smb, and it will show you some files along with their paths. The first two are the correct ones with their same Hostename [\\printnightmare.gentilkiwi.com\IPC$,srvsvc,spoolss].

5. Similarly, go to the export objects again and then select smb. Identify the dlls. There are only two dlls, for which the Hostname is also different. These are the required dlls [\\printnightmare.gentilkiwi.com\print$,\x64\3\mimispool.dll,\W32X86\3\mimispool.dll]

6. Open the .log file in Process Monitor. Go to the filter icon and the filter [Path | contains | mimispool.dll | Include]. This will give you only mimispool.dll files logs, OR you can just simply search for these files usig ctrl+F. In the resulting logs, observe the paths against which the result is also success. The paths to these files is the answer [C:\Windows\system32\spool\drivers\X64\3,C:\Windows\system32\spool\drivers\W32X86\3].

7. Add a filter [printnightmare.gentilkiwi.com]. You will many logs. Look for the paths that start with C: [C:\Windows\System32\spool\SERVERS\printnightmare.gentilkiwi.com].

8. Open the FullEventLogView in windows. Go tho the advanced options (under the 'File' in top left corner). Change the date range to [Show Events from all times]. Change the providers to [Show only the specified ones] and add [Microsoft-Windows-PrintService]. Apply the filter and it will give 187 logs. Find [mimispool.dll] usinf ctrl+F. It will show two logs. Both will be showing the event of adding a printer. In the description, the full path of the printer is given, at the end of which the name of the printer is appended [Kiwi Legit Printer].

9. In the entire analysis, we can notice that the main process is with the id [2604] and the name is [spoolersv.exe]. Since the process id for elevated command prompt is required, which means that the command was run on windows command promtpt. So, in the process monitor, add the filter [cmd.exe]. This will give the child process with id [5408]. Hence the required answer is [5408,spoolersv.exe].

10. Now we know the parent process, so in the FullEventLogView we will find the the parent process id [5408] usinf ctrl+F and start searching for all the events assosiated with this process. Notice that if the description shows any 'command line' field. There are total 6 events that contains command line field and shows the command run on the cmd. Note that in the 4th one, the command includes administrators word, which means that this is the command used to elevate privileges [net localgroup administrators rjones /add].

