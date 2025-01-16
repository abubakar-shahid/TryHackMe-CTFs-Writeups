# New Hire Old Artifacts

## Challenge Information
- **Challenge Name**: New Hire Old Artifacts
- **Category**: Log Analysis
- **Difficulty Level**: Medium

## Task Description
In the given scenario, we have to analyze the given splunk and just answer the questions. Open the given ip address in your own browser if you have a vpn, otherwise use the attack box and access the ip address in its browser.

## Investigation Steps

1. Search for `Password Viewer` on the Splunk. The path found will be `C:\Users\FINANC~1\AppData\Local\Temp\11111.exe`

2. We can see tht comapy name on the results: `NirSoft`

3. Search with a filter of:
```bash 
Image="*\\Local\\Temp\\*.exe" NOT "*11111.exe"
| sort _time
| table _time Image OriginalFileName 
| where OriginalFileName != ""
```
This will give the file names: `PalitExplorer.exe,IonicLarge.exe`

4. Search with a filter of:
```bash 
Image="*\\IonicLarge.exe" DestinationIp=*
| regex DestinationIp="^\d{1}\.\d{3}\.\d{3}\.\d{2}$"
| table DestinationIp
```
sort for ascending order. This will give the ip address: `2.56.59.42`. Defang this URL: `2[.]56[.]59[.]42`

5. use a filter of:
```bash
EventCode 12: Registry object created/deleted
Image="*\\IonicLarge.exe" EventCode=12
```
This will give the answer: `HKLM\SOFTWARE\Policies\Microsoft\Windows Defender`

6. taskkill /im then go to CommandLine5. the answer will be `phcIAmLJMAIMSa9j9MpgJo1m.exe, WvmIOrcfsuILdX6SNwIRmGOJ.exe`

7. Use a filter of:
```bash
EventCode=1 Image="*\\powershell.exe" *defender*
| table CommandLine _time
| sort _time
```
visit the last one form the 4 that appear. The command is: `powershell WMIC /NAMESPACE:\\root\Microsoft\Windows\Defender PATH MSFT_MpPreference call Add ThreatIDDefaultAction_Ids=2147735503 ThreatIDDefaultAction_Actions=6 Force=True`

8. ThreatIDDefaultAction_Ids in all the 4 events: `2147735503,2147737010,2147737007,2147737394`

9. use a filter of: 
```bash
Image="C:\\Users\\Finance01\\AppData\\*\\*.exe"
| table Image _time
| sort _time
| dedup Image
```
It will reveal the path: `C:\\Users\\Finance01\\AppData\\Roaming\\EasyCalc\\EasyCalc.exe`

10. use filter: 
```bash
Image="C:\\Users\\Finance01\\AppData\\Roaming\\EasyCalc\\EasyCalc.exe"
```
then open ImageLoaded and athe first 3 are the answer: `nw_elf.dll,ffmpeg.dll,nw.dll`
