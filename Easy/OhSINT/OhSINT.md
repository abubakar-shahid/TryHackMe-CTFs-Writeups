# OhSINT

## Challenge Information
- **Challenge Name**: OhSINT
- **Category**: OSINT
- **Difficulty Level**: Easy

## Initial Analysis
First of all, download the image from the browser by right clicking on the image. Then run exiftool on the downloaded file `exiftool WindowsXP_1551719014755.jpg`. This will reveal some information about the downloaded file. In the given information, there is a column of `Copyright` against which it is written `OWoodflint`. Search this on the google and we can see a twitter account with this name and a github repository as well. Open these both in the separate tabs.

## Investigation Steps

1. First of all, come to the twitter account. The profile picture is of a cat, so the answer is `cat`.

2. Now come to the github repo, Read the `Readme.md` file where the user has mentioned that he is from London, and the answer is also `London`.
A proper way to find the location was using Wigle.net. In the twitter account of this user, he has given a BSSID for his house wifi. Note this BSSID. Now go to Wigle.net and make an account. In the menu, click `View` and then `Advanced Search`. Enter the BSSID and then click the query button. This will give some information in the form of a single row and the location as well `London`.

3. In the given table, the 3rd column `SSID` gives us the answer `UnileverWifi`.

4. The gmail was given in the github repository `OWoodflint@gmail.com`.

5. The site where we found the email is `Github`.

6. There is also a link to a wordpress website. Open this link and there is written that in which city is the user currently `New York`.

7. To get the password, we have to analyze the source code of this website. Right click in the website page and click download. It will save the entire html of the website. Now in the code, search for `Im in New York right now, so I will update this site right away with new photos!`. Very next to this paragraph tag, there is another paragraph tag in which the password is written `pennYDr0pper.!`.
