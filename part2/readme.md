### Run code in command prompt like:
  ```ruby
$ sudo python3 Part2.py --config d --congestion vegas --linkloss 3
```
Linkloss parameter set default to 0, to be utilised when config set to 'd'. <br />
Code takes 5-6 s to run and after which you can access your pcap file which is stored in the same folder as the code with name 'part({config}){congestion}.pcap'.

### Implementation
To parse arguments like config and congestion control from command prompt we had to import an arg parser. <br>
```ruby
import argparse
```
Then with an initaition of a parser object we retrieved the arguments config, congestion, linkloss. <br>

Topology was very straight forward and in each link we specified a 10Mbps bandwidth cap, with specifying linkloss in s1-s2 link, to only work with config set to d. <br>

Since h4 as a server could only connect to a single client by default we specified three hosts on three different ports of h4 so it can listen to packets from all three clients simultaneously. <br>
Moreover, we tcpdumped data coming to h4 to obtain pcap files for output. <br>
To make sure all three clients could send packets simultaneously we started the transactions from first two clients in background.
