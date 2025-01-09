# 

1. using brim, add a filter of [network trojan]. copy the alert.signature field

2. using brim, add a filter of [potential corporate]. copy the alert.signature field

3. copy the ip of any of the requests from the above filters and write it in defang format

4. using wireshark, add the filter of the same ip. note the get request for a malicious file. the answer will be in  the format: host[.]com/uri[.]cab. you can see the host by following the stream.

5. using brim, add the filter of same ip. go to the details of the request in which the file is requested. in the filed [sub], there is the hash of the file in the request of this field. search this hash on the virustotal and you will see the payload name.

6. using wireshark, follow the stream of the request where the get request for this .cab file is made. note down the user-agent.

7. [method=="GET" | cut ip, host, status_code] and we will see only two domains with status code 200.

8. using brim, add a filter of ["Not Suspicious Traffic"]. note the two addresses and write in defang format.

9. using brim, add filter of [64.225.65.166 | cut query]. it will give all 3 assossiated domains

10. using brim, add filter of [142.93.211.176 | cut query]. it will give the assossiated domain

