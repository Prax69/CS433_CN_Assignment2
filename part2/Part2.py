# !/usr/bin/python
import sys
sys.path.append('/usr/bin/mn')  # Replace with the actual path to your Mininet installation
import argparse
import os
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.node import Controller

parser = argparse.ArgumentParser(description='TCP Client-Server Program with Configurable Parameters')
parser.add_argument('--config', choices=['b', 'c','d'], default='b', help='Configuration (b or c or d)')
parser.add_argument('--congestion', default='cubic', help='Congestion control scheme')
parser.add_argument('--linkloss', type=float, default=0.0, help='Link loss percentage')
args = parser.parse_args()

class NetworkTopo(Topo):
    def build(self, **_opts):

        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')


        h1 = self.addHost(name='h1',
                          ip='10.0.0.251/24')
        h2 = self.addHost(name='h2',
                          ip='10.0.0.252/24')
        h3 = self.addHost(name='h3',
                          ip='10.0.0.253/24')
        h4 = self.addHost(name='h4',
                          ip='10.0.0.254/24')

        for h,s in [(h1,s1),(h2,s1),(h3,s2),(h4,s2)]:
        	self.addLink(h,s,bw='10Mbps')
        self.addLink(s1,s2,bw='10Mbps',loss=args.linkloss)
        


def run(config, congestion, linkloss):

    topo = NetworkTopo()
    net = Mininet(topo=topo)

    
    net.start()
    
    net['h4'].cmd('iperf -s -p 5000 &')
    net['h4'].cmd('iperf -s -p 5001 &')
    net['h4'].cmd('iperf -s -p 5002 &')
    cap = net['h4'].popen(f'timeout 8000 tcpdump -i any -w part({config}){congestion}.pcap')
    
    if (config == 'c'):
    	net['h1'].cmd(f'iperf -c 10.0.0.254 -p 5000 -Z {congestion} -t 5 &')
    	net['h2'].cmd(f'iperf -c 10.0.0.254 -p 5001 -Z {congestion} -t 5 &')
    	net['h3'].cmd(f'iperf -c 10.0.0.254 -p 5002 -Z {congestion} -t 5')
    	
    else:
    	net['h1'].cmd(f'iperf -c 10.0.0.254 -p 5001 -Z {congestion} -t 5')
    
    
    
    net.stop()
    

if __name__ == '__main__':
    
    setLogLevel('info')
    run(args.config, args.congestion, args.linkloss)
