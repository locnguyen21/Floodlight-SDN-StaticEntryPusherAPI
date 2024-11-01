from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel

class MyTopo(Topo):
    def build(self):
        # Create a switch
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        # Create a host
        h1 = self.addHost('h1', ip='10.0.0.1')
        h2 = self.addHost('h2', ip='10.0.0.2')
        # Link the switch and host
        self.addLink(h1, s1)
        self.addLink(h2, s3)
        self.addLink(s1,s2)
        self.addLink(s2,s3)

def run():
    topo = MyTopo()
    net = Mininet(topo=topo, controller=RemoteController('c0', ip='10.2.221.172', port=6653))
    net.start()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run() 