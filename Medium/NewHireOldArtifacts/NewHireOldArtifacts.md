# In the given scenario, we have to analyze the given splunk and just answer the questions. Open the given ip address in your own browser if you have a vpn, otherwise use the attack box and access the ip address in its browser.

1. Password Viewer

2. 

3. Image="*\\Local\\Temp\\*.exe" NOT "*11111.exe"
| sort _time
| table _time Image OriginalFileName 
| where OriginalFileName != ""

4. Image="*\\IonicLarge.exe" DestinationIp=*
| regex DestinationIp="^\d{1}\.\d{3}\.\d{3}\.\d{2}$"
| table DestinationIp

sort for ascending order

5. EventCode 12: Registry object created/deleted
Image="*\\IonicLarge.exe" EventCode=12

6. taskkill /im then go to CommandLine5

7. EventCode=1 Image="*\\powershell.exe" *defender*
| table CommandLine _time
| sort _time

visit the last one form the 4 that appear

8. ThreatIDDefaultAction_Ids in all the 4 events

9. Image="C:\\Users\\Finance01\\AppData\\*\\*.exe"
| table Image _time
| sort _time
| dedup Image

10. Image="C:\\Users\\Finance01\\AppData\\Roaming\\EasyCalc\\EasyCalc.exe" then open ImageLoaded and athe first 3 are the answer
