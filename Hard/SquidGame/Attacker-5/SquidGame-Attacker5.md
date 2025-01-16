# Squid Game - Attacker 5

## Challenge Information
- **Challenge Name**: Squid Game - Attacker 5
- **Category**: Malware Analysis
- **Difficulty Level**: Hard

## Analysis Steps

1. Running the command:
```bash
olevba attacker5.doc
```
gave the result in which the malicious content was not visible. So now running the command:
```bash
strings attacker5.doc | grep -E "[A-Za-z0-9+/=]{20,}"
```
we got some data that is encoded only. Here we can also see a variable named `Caption`, and the value of this is the answer `CobaltStrikeIsEverywhere`.

2. In the above retrieved data, we got a `base64` encoding. Go to `cyberchef` and decode it. Add the filter of `Remove Null Bytes` as well. It will give some content in which we can see that there is some more `base64` encoding. Copy this and again try decoding it using `cyberchef`. Add the filter of `Gunzip` and remove the filter of null bytes. It will again give some content. Scroll down and observe that there is a for loop in which `-bxor` operator is being used. Very next to it, the key `35` is present. This XOR key is commonly associated with `PowerShell` scripts in `Cobalt Strike` payloads.

3. Now in the same content, we can again see a `base64` encoding. Try decoding it on `cyberchef` again. Remove the previous filters and now add the filter of XOR with key 35 in Decimal. In the output content, the content is not readable. But at the end of the content, there is an `ip address` `176.103.56.89`, which is the answer.

4. In the same unreadable content, look carefully: there is a `user-agent` also present `Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727)`.

5. Since, the content is now unpredictable, lets save this file and try to do some more experiments. The file will be saved as a `dat` file from `cyberchef`. After downloading the file, open the terminal in the directory where the file is present and run the command:
```bash
scdbgc -f ~/Downloads/file_name.dat -s -1
```
This will fetch all the content of the `shellcode`. This content contains answer to all the further parts. For now, the path value can be seen as `/SjMR`.

6. In the same content, the port can be observed as well `8080`.

7. In the same content, the two API's are also visible `LoadLibraryA, InternetOpenA`.
