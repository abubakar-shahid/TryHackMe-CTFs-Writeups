# Warzone 1

## Challenge Information
- **Challenge Name**: Warzone 1
- **Category**: Packet Analysis
- **Difficulty Level**: Medium

## Task Description
In the lab, we have to analyze the suspecious traffic. In this lab, rather than using `Wireshark` for the packet analysis, we will be using `Brim`, which is more helpful in visualization of the information. Moreover, we will be using an online platform `VirusTotal`, which is an opensource online platform to provide information about the malicious ipaddresses, softwares, etc.

## Investigation Steps

1. So in the first task, we will first open the pcap file in the Brim. It will load all the data and you will see a very colorful data. Now simply apply the filter of `http` in the search bar. This will show only the http requests. Now, in the each request try hovering over the fields of the request. You will notice a field `alert signature`. Copy its value, since this is the signature of the malware command `ET Malware MirrorBlast CnC Activity M3`.

2. In the same request, there is the source ipaddress `172.16.1.102`. Write it in the defang format `172[.]16[.]1[.]102`

3. Similarly, there is the destination ipaddress `169.239.128.11`. Write it in the defanf format `169[.]239[.]128[.]11`

4. Also notice each and eveything in the same request in which we found the malware signature. Notice that there is also a field of the malware family `MirrorBalst`. Go to the `VirusTotal` official website and go the `Community` tab. Notice that there are many files of the graphs with the name of mirrorblast. Here, some are written with their threat groups as well `TA505`.

5. The malware family is the same as for the previous task `MirrorBalst`.

6. Now first of all, identify the files transfered by the identified ipaddresses. There are two `msi` files, that are the malwares. Note down their filenames. Now go the VirusTotal website and open the `Relations` tab. Search for the noted filenames and figure out the `Type` in the `Communicating Files` table. The type of the msi files will be `Windows Installer`.

7. For this task, I used WireShark. Since it is asking for the flagged ipaddress, add a filter of the ipaddress `172.16.1.102`. Follow the stream and figure out the user-agent in the request headers `REBOL View 2.7.8.3.1`.

8. I again used the WireShark, and add the http filter. Notice the ipaddresses used in the file transferring process. There are two more addresses `185.10.68.235`, `192.36.27.92`. Write them in defang format with command separated #185[.]10[.]68[.]235,192[.]36[.]27[.]92.

9. Similary, add the http filter and notice the two `msi` files transfered `filter.msi`, `10opd3r_load.msi`. Write them comma separated.

10. Now follow the stream for the first downladed msi file `filter.msi`. Scroll down at the end of the stream. You will notice some loooong paragraphs. Look in the last paragraph and find the file paths that are hidden here
`C:\ProgramData\001\arab.bin`, `C:\ProgramData\001\arab.exe`. Write them comma separated. An important thing that I noticed here is that the path of the `arab.exe` is not completely given. Assume the same path as for the `arab.bin`.

11. Now follow the stream for the second downladed msi file `10opd3r_load.msi`. Scroll down at the end of the stream. You will notice some loooong paragraphs again. Look in the last paragraph and find the file paths that are hidden here
`C:\ProgramData\Local\Google\rebol-view-278-3-1.exe`, `C:\ProgramData\Local\Google\exemple.rb`. Write them comma separated.
