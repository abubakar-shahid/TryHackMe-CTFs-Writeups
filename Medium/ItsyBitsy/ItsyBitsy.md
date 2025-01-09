# Here, we will be using an online web app 'Elastic', where all the logs are already present. Figure out the usage of the application and start your investigation!

1. Open the given ip address in the attackbox. A web app [elastic] will open. Go to the menu and navigate to the discover tab. There is a search bar in the right corner. Add the date filter [1st March, 2022]->[now]. Search, and the total number of events appearing will be the answer [1482].

2. I could see a lot of requests from the source.ip: 192.166.65.52. So i decided to add a filter that will give me requests other than that of this ip. Hence, i added a filter [NOT source_ip: "192.166.65.52"]. It gave me only 2 logs, which gave me the required ip [192.166.65.54].

3. In the same request, there is the name of the binary in the [user_agent] field [bitsadmin].

4. In the same request, there is the name of the site in the [host] field [pastebin.com].

5. The full url is the combination of [host] and [uri]. Here, it was [pastebin.com/yTg0Ah6a].

6. Open the link [https://pastebin.com/yTg0Ah6a] in your browser. A file will appear with the name [secret.txt].

7. The content of the file is also visible in the pastebin web app [THM{SECRET__CODE}].
