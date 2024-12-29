# In the machine, we are given 5 .doc files each with an attacker number. Lets start with the first file and use OleTools for the analysis of hidden malicious content within this word document. We will be also using Exiftool and Strings for some simple tasks.
[https://srilambdaman.medium.com/tryhackme-squid-game-attacker-2-ddeb75195a8f]

1. Lets use oledump to analyze the content imbedded in the doc file. Use the command [oledump.py attacker1.doc] and it will give all the embedded objects. The output will show us total 12 streams. One of them have [M] after the object number. This is the maloc that we are looking for, with stream [8]. Now, lets run a command to see all the contents of the dump. Use the command [olevba attacker1.doc] to see all the content. But in our case, all the contents are present as VBA objects and are strongly obfustaced. In the analysis given at the end of the result, we can see that a shell is used. In the VBA objects, there was a command starting with [VBA.Shell] that also gives us an evidence that a shell is executed, also, the command itself is the command, with a hint that the attacker is replacing [[] with [A]. However, coming to the result part, it is also mentioned that base64 strings are used. Now, to deobfuscate the contents, we can run [oledump.py -s a attacker1.doc -S], which will deobfuscate all the streams of the content. If you think that the result is too long, try running the command for a specific stream, start with 1 [oledump.py -s 1 attacker1.doc -S] and see which stream gives you the required result. On the stream 4 [oledump.py -s 4 attacker1.doc -S], it gave some result [P^O^W^E^R^S^H^E^L^L ^-^N^o^P^r^o^f^i^l^e^ -^E^x^e^cutionPolicy B^^^yp^ass -encodedcommand 'encoded command']. The command contains too many [[] which we will replace with [A]. Then this command will become entirely base64 encoded. Decode this to string. Use cyberchef and add the filter of [Remove Null Bytes] and [Remove Special Characters] and you will get the exact code that the attacker has used. The domain that the attacker has used is in the line [15] of the code that we extracted, [http://fpetraardella.band/xap_102b-AZ1/704e.php?l=litten4.gas].

2. The filename that the attacker is trying to drop is at the end of line [18] [QdZGP.exe].

3. In the same line [18], the folder that the attacker is trying to use for storing the response of the shell, is [CommonApplicationData]. Do some google search and find the windows path that stored this folder [%ProgramData%].

4. In the line 21, the object that the attacker is trying to access is [CLSID C08AFD90-F2A1-11D1-8455-00A0C91F3880]. This is the class id of this foler. Search this on google and we will get the name of the object [ShellBrowserWindow].

5. In the line [7], the link of the php file is given. The exact answer is without the http header [176.32.35.16/704e.php].

6. By running the strins command [strings attacker1.doc | grep -E '\b[0-9]{3}-[0-9]{3}-[0-9]{4}\b'], which defines the range of the required phone number (given in the question), it will give us the exact answer [213-446-1757].

7. By running the command that we did in the first task [olevba attacker1.doc], we get a result analysis at the end of the obfuscated contents. The very first row of the results table has the answer [AutoExec].

8. For this kind of information, we can also use the [Exiftool]. Run the command [exiftool attacker1.doc | grep "Subject"]. This will give the exact answer [West Virginia Samanta].

9. For this, we can use the [exiftool] as well as the [oletimes]. Oletimes is recommended as it will give in the exact format. Exiftool have different date format [yyyy:dd:mm hh:mm:ss], while we require in [yyyy-mm-dd hh:mm:ss]. So, run the command [oletimes attacker1.doc] and it will give the exact answer [2019-02-07 23:45:30.]

10. Use the command [oledump.py attacker1.doc] and it will give all the embedded objects. The output will show us total 12 streams. One of them have [M] after the object number. This is the maloc that we are looking for, with stream [8].

11. From the above information, the name of the maloc stream is [ThisDocument].

