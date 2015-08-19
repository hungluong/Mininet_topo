#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import OVSSwitch, RemoteController
from mininet.topo import Topo
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.link import TCLink

setLogLevel ('info')

# Two local and one "external" controller HUNG
# Ignore the warning message that remote isn't yet running

c0 = RemoteController('c0',ip='127.0.0.1')
cmap = {'s1':c0,'s2':c0,'s3':c0,'s4':c0,'s5':c0,'s6':c0}

class Topology(Topo):
	def __init__(self,**opts):
		Topo.__init__(self, **opts)
		h1=self.addHost('h1')
		h2=self.addHost('h2')
		h3=self.addHost('h3')
		h4=self.addHost('h4')
		h5=self.addHost('h5')
		h6=self.addHost('h6')
		s1=self.addSwitch('s1')
		s2=self.addSwitch('s2')
		s3=self.addSwitch('s3')
		s4=self.addSwitch('s4')
		s5=self.addSwitch('s5')
		s6=self.addSwitch('s6')
		self.addLink(h1,s1)
		self.addLink(h2,s2)
		self.addLink(h3,s3)
		self.addLink(h4,s4)
		self.addLink(h5,s5)
		self.addLink(h6,s6)
		self.addLink(s1,s2,bw=20)
                self.addLink(s1,s3,bw=20)
                self.addLink(s2,s4,bw=20)
                self.addLink(s3,s4,bw=20)
		self.addLink(s1,s4,bw=10)
		self.addLink(s1,s5,bw=20)
		self.addLink(s4,s6,bw=20	)

class MultiSwitch (OVSSwitch):
	"Custom Switch() subclass that connects to controllers"
	def start (self,controllers):
	      return OVSSwitch.start(self,[cmap[self.name]])

topo = Topology ()
net = Mininet (topo=topo, link = TCLink, switch=MultiSwitch, build=False)
net.addController(c0)
net.build()
net.start()
CLI(net)
net.stop()
