```
FIND PythonScript, PCAP FILE, AND REPORT IN THIS FOLDER

For different subparts of question, certain lines need to be commented out and some uncommented in. Refer the report or go through the code itself

pcap file for ra router present as ra.pcap
```
### Implementation
The router class implemented similar to the example code. <br>
The topology contructed with each router having 2 hosts its same subnet. Router to host connection made with an intermediate switch. <br>
The hosts connected directly by specifying configurations of which interface to use for these links. <br>
After setting up this topology, in the run function we add specific entries to route table to specify path routers follow when moving from one subnet to another. <br>
Example 
```ruby
info(net['ra'].cmd("ip route add 10.1.0.0/24 via 10.100.0.2"))
```
Above adds entry to ra router to go via 10.100.0.2 (interface of rb router connection to ra) entry to enter subnet 10.1.0.0. <br>

in subpart(c) where route is to be changed we change the entries like the above. In the code you can just comment line 97 and uncomment line 98. <br>

in subpart(b) where we wish to monitor packets using wireshark, we can tcpdump packets of rb and view them on wireshark. In the code you can just uncomment line 109,110 and 113.
