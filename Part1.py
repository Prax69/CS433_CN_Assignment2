# !/usr/bin/python
import sys
sys.path.append('/usr/bin/mn')  # Replace with the actual path to your Mininet installation

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.node import Controller


class LinuxRouter(Node):
    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()


class NetworkTopo(Topo):
    def build(self, **_opts):
        # Add 2 routers in two different subnets
        ra = self.addHost('ra', cls=LinuxRouter, ip='10.0.0.1/24')
        rb = self.addHost('rb', cls=LinuxRouter, ip='10.1.0.1/24')
        rc = self.addHost('rc', cls=LinuxRouter, ip='10.2.0.1/24')

        # Add 2 switches
        sa = self.addSwitch('s1')
        sb = self.addSwitch('s2')
        sc = self.addSwitch('s3')

        # Add host-switch links in the same subnet
        self.addLink(sa,
                     ra,
                     params2={'ip': '10.0.0.1/24'})

        self.addLink(sb,
                     rb,
                     params2={'ip': '10.1.0.1/24'})
                     
        self.addLink(sc,
                     rc,
                     params2={'ip': '10.2.0.1/24'})
        

        # Add router-router link in a new subnet for the router-router connection
        self.addLink(ra,
                     rb,
                     params1={'ip': '10.100.0.1/24'},
                     params2={'ip': '10.100.0.2/24'})

        self.addLink(rb,
                     rc,
                     params1={'ip': '10.100.1.1/24'},
                     params2={'ip': '10.100.1.2/24'})

        self.addLink(rc,
                     ra,
                     params1={'ip': '10.100.2.1/24'},
                     params2={'ip': '10.100.2.2/24'})

        # Adding hosts specifying the default route
        h1 = self.addHost(name='h1',
                          ip='10.0.0.251/24',
                          defaultRoute='via 10.0.0.1')
        h2 = self.addHost(name='h2',
                          ip='10.0.0.252/24',
                          defaultRoute='via 10.0.0.1')
        h3 = self.addHost(name='h3',
                          ip='10.1.0.251/24',
                          defaultRoute='via 10.1.0.1')
        h4 = self.addHost(name='h4',
                          ip='10.1.0.252/24',
                          defaultRoute='via 10.1.0.1')
        h5 = self.addHost(name='h5',
                          ip='10.2.0.251/24',
                          defaultRoute='via 10.2.0.1')
        h6 = self.addHost(name='h6',
                          ip='10.2.0.252/24',
                          defaultRoute='via 10.2.0.1')

        # Add host-switch links
        for h,s in [(h1,sa),(h2,sa),(h3,sb),(h4,sb),(h5,sc),(h6,sc)]:
        	self.addLink(h,s)
        


def run():
    topo = NetworkTopo()
    net = Mininet(topo=topo)

    # Add routing for reaching networks that aren't directly connected
    info(net['ra'].cmd("ip route add 10.1.0.0/24 via 10.100.0.2"))
    info(net['ra'].cmd("ip route add 10.2.0.0/24 via 10.100.2.1")) #comment this line to make packets from subnet1 follow ra->rb->rc path
    info(net['rb'].cmd("ip route add 10.0.0.0/24 via 10.100.0.1"))
    info(net['rb'].cmd("ip route add 10.2.0.0/24 via 10.100.1.2"))
    info(net['rc'].cmd("ip route add 10.0.0.0/24 via 10.100.2.2"))
    info(net['rc'].cmd("ip route add 10.1.0.0/24 via 10.100.1.1"))
    info(net['ra'].cmd("ip route show"))
    info(net['rb'].cmd("ip route show"))
    info(net['rc'].cmd("ip route show"))
    net.start()
    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run()
