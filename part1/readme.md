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
