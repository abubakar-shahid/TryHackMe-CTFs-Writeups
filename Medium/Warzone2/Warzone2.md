# Warzone 2

## Challenge Information
- **Challenge Name**: Warzone 2
- **Category**: Packet Analysis
- **Difficulty Level**: Medium

## Investigation Steps

1. Using brim, add a filter of `network trojan`. Copy the alert.signature field.

2. Using brim, add a filter of `potential corporate`. Copy the alert.signature field.

3. Copy the ip of any of the requests from the above filters and write it in defang format.

4. Using wireshark, add the filter of the same ip. Note the get request for a malicious file. The answer will be in the format: host[.]com/uri[.]cab. You can see the host by following the stream.

5. Using brim, add the filter of same ip. Go to the details of the request in which the file is requested. In the filed `sub`, there is the hash of the file in the request of this field. Search this hash on the virustotal and you will see the payload name.

6. Using wireshark, follow the stream of the request where the get request for this .cab file is made. Note down the user-agent.

7. `method=="GET" | cut ip, host, status_code` and we will see only two domains with status code 200.

8. Using brim, add a filter of `"Not Suspicious Traffic"`. Note the two addresses and write in defang format.

9. Using brim, add filter of `64.225.65.166 | cut query`. It will give all 3 assossiated domains.

10. Using brim, add filter of `142.93.211.176 | cut query`. It will give the assossiated domain.
