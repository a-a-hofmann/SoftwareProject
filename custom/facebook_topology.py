from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

import os


'''
To execute:
sudo mn --custom ~/mininet/custom/facebook_topology.py --topo mytopo --mac --controller remote
'''


class MyTopo(Topo):
    def __init__(self, **params):
        global h

	try:
		os.system("sudo fuser -k 6633/tcp")
	except:
		pass

	# Initialize topology
        Topo.__init__(self, **params)

	net = Mininet(link=TCLink)

	info('*** Adding controller\n')
	c0 =net.addController(name='c0',
                      controller=Controller,
                      protocol='tcp',
                      port=6633)

	info( '*** Add hosts\n')

	H1 = net.addHost('h1')
	H2 = net.addHost('h2')
	H3 = net.addHost('h3')
	H4 = net.addHost('h4')
	#H5 = net.addHost('h5')
	#H6 = net.addHost('h6')
	#H7 = net.addHost('h7')
	#H8 = net.addHost('h8')
	#H9 = net.addHost('h9')
	#H10 = net.addHost('h10')
	#H11 = net.addHost('h11')
	#H12 = net.addHost('h12')
	#H13 = net.addHost('h13')
	#H14 = net.addHost('h14')
	#H15 = net.addHost('h15')
	#H16 = net.addHost('h16')
	H17 = net.addHost('h17')
	H18 = net.addHost('h18')
	#H19 = net.addHost('h19')
	#H20 = net.addHost('h20')
	#H21 = net.addHost('h21')
	#H22 = net.addHost('h22')

	info( '*** Add switches\n')

	S1 = net.addSwitch('s1')
	S2 = net.addSwitch('s2')
	S3 = net.addSwitch('s3')
	S4 = net.addSwitch('s4')
	S5 = net.addSwitch('s5')
	S6 = net.addSwitch('s6')
	S7 = net.addSwitch('s7')
	S8 = net.addSwitch('s8')
	S9 = net.addSwitch('s9')
	S10 = net.addSwitch('s10')
	S11 = net.addSwitch('s11')
	S12 = net.addSwitch('s12')
	S13 = net.addSwitch('s13')
	S14 = net.addSwitch('s14')
	S15 = net.addSwitch('s15')
	S16 = net.addSwitch('s16')
	S17 = net.addSwitch('s17')
	S18 = net.addSwitch('s18')
	S19 = net.addSwitch('s19')
	S20 = net.addSwitch('s20')
	S21 = net.addSwitch('s21')
	S22 = net.addSwitch('s22')
	S23 = net.addSwitch('s23')
	S24 = net.addSwitch('s24')
	S25 = net.addSwitch('s25')
	S26 = net.addSwitch('s26')
	S27 = net.addSwitch('s27')
	S28 = net.addSwitch('s28')

	info( '*** Add links\n')

	LINK_CAPACITY = 1000 #Mbps
	QUEUE_SIZE = 5000

	#EDGE SWITCHES <--> SPINE SWITCHES

	# S1 <--> S5, S6, S7, S8

	net.addLink(S1, S5, bw=LINK_CAPACITY, port1=1, port2=1, max_queue_size=QUEUE_SIZE)
	net.addLink(S1, S6, bw=LINK_CAPACITY, port1=2, port2=1, max_queue_size=QUEUE_SIZE)
	net.addLink(S1, S7, bw=LINK_CAPACITY, port1=3, port2=1, max_queue_size=QUEUE_SIZE)
	net.addLink(S1, S8, bw=LINK_CAPACITY, port1=4, port2=1, max_queue_size=QUEUE_SIZE)

	# S2 <--> S5, S6, S7, S8

	net.addLink(S2, S5, bw=LINK_CAPACITY, port1=1, port2=2, max_queue_size=QUEUE_SIZE)
	net.addLink(S2, S6, bw=LINK_CAPACITY, port1=2, port2=2, max_queue_size=QUEUE_SIZE)
	net.addLink(S2, S7, bw=LINK_CAPACITY, port1=3, port2=2, max_queue_size=QUEUE_SIZE)
	net.addLink(S2, S8, bw=LINK_CAPACITY, port1=4, port2=2, max_queue_size=QUEUE_SIZE)

	# S3 <--> S9, S10, S11, S12

	net.addLink(S3, S9, bw=LINK_CAPACITY, port1=1, port2=1, max_queue_size=QUEUE_SIZE)
	net.addLink(S3, S10, bw=LINK_CAPACITY, port1=2, port2=1, max_queue_size=QUEUE_SIZE)
	net.addLink(S3, S11, bw=LINK_CAPACITY, port1=3, port2=1, max_queue_size=QUEUE_SIZE)
	net.addLink(S3, S12, bw=LINK_CAPACITY, port1=4, port2=1, max_queue_size=QUEUE_SIZE)

	# S4 <--> S9, S10, S11, S12

	net.addLink(S4, S9, bw=LINK_CAPACITY, port1=1, port2=2, max_queue_size=QUEUE_SIZE)
	net.addLink(S4, S10, bw=LINK_CAPACITY, port1=2, port2=2, max_queue_size=QUEUE_SIZE)
	net.addLink(S4, S11, bw=LINK_CAPACITY, port1=3, port2=2, max_queue_size=QUEUE_SIZE)
	net.addLink(S4, S12, bw=LINK_CAPACITY, port1=4, port2=2, max_queue_size=QUEUE_SIZE)


	#SPINE SWITCHES <--> FABRIC SWITCHES

	# S5 <--> S13, S14, S17, S18

	net.addLink(S5, S13, bw=LINK_CAPACITY, port1=3, port2=1, max_queue_size=QUEUE_SIZE)
	net.addLink(S5, S14, bw=LINK_CAPACITY, port1=4, port2=1, max_queue_size=QUEUE_SIZE)
	net.addLink(S5, S17, bw=LINK_CAPACITY, port1=5, port2=1, max_queue_size=QUEUE_SIZE)
	net.addLink(S5, S18, bw=LINK_CAPACITY, port1=6, port2=1, max_queue_size=QUEUE_SIZE)

	# S6 <--> S13, S14, S17, S18

	net.addLink(S6, S13, bw=LINK_CAPACITY, port1=3, port2=2, max_queue_size=QUEUE_SIZE)
	net.addLink(S6, S14, bw=LINK_CAPACITY, port1=4, port2=2, max_queue_size=QUEUE_SIZE)
	net.addLink(S6, S17, bw=LINK_CAPACITY, port1=5, port2=2, max_queue_size=QUEUE_SIZE)
	net.addLink(S6, S18, bw=LINK_CAPACITY, port1=6, port2=2, max_queue_size=QUEUE_SIZE)

	# S7 <--> S13, S14, S17, S18

	net.addLink(S7, S13, bw=LINK_CAPACITY, port1=3, port2=3, max_queue_size=QUEUE_SIZE)
	net.addLink(S7, S14, bw=LINK_CAPACITY, port1=4, port2=3, max_queue_size=QUEUE_SIZE)
	net.addLink(S7, S17, bw=LINK_CAPACITY, port1=5, port2=3, max_queue_size=QUEUE_SIZE)
	net.addLink(S7, S18, bw=LINK_CAPACITY, port1=6, port2=3, max_queue_size=QUEUE_SIZE)

	# S8 <--> S13, S14, S17, S18

	net.addLink(S8, S13, bw=LINK_CAPACITY, port1=3, port2=4, max_queue_size=QUEUE_SIZE)
	net.addLink(S8, S14, bw=LINK_CAPACITY, port1=4, port2=4, max_queue_size=QUEUE_SIZE)
	net.addLink(S8, S17, bw=LINK_CAPACITY, port1=5, port2=4, max_queue_size=QUEUE_SIZE)
	net.addLink(S8, S18, bw=LINK_CAPACITY, port1=6, port2=4, max_queue_size=QUEUE_SIZE)

	# S9 <--> S15, S16, S19, S20

	net.addLink(S9, S15, bw=LINK_CAPACITY, port1=3, port2=1, max_queue_size=QUEUE_SIZE)
	net.addLink(S9, S16, bw=LINK_CAPACITY, port1=4, port2=1, max_queue_size=QUEUE_SIZE)
	net.addLink(S9, S19, bw=LINK_CAPACITY, port1=5, port2=1, max_queue_size=QUEUE_SIZE)
	net.addLink(S9, S20, bw=LINK_CAPACITY, port1=6, port2=1, max_queue_size=QUEUE_SIZE)

	# S10 <--> S15, S16, S19, S20

	net.addLink(S10, S15, bw=LINK_CAPACITY, port1=3, port2=2, max_queue_size=QUEUE_SIZE)
	net.addLink(S10, S16, bw=LINK_CAPACITY, port1=4, port2=2, max_queue_size=QUEUE_SIZE)
	net.addLink(S10, S19, bw=LINK_CAPACITY, port1=5, port2=2, max_queue_size=QUEUE_SIZE)
	net.addLink(S10, S20, bw=LINK_CAPACITY, port1=6, port2=2, max_queue_size=QUEUE_SIZE)

	# S11 <--> S15, S16, S19, S20

	net.addLink(S11, S15, bw=LINK_CAPACITY, port1=3, port2=3, max_queue_size=QUEUE_SIZE)
	net.addLink(S11, S16, bw=LINK_CAPACITY, port1=4, port2=3, max_queue_size=QUEUE_SIZE)
	net.addLink(S11, S19, bw=LINK_CAPACITY, port1=5, port2=3, max_queue_size=QUEUE_SIZE)
	net.addLink(S11, S20, bw=LINK_CAPACITY, port1=6, port2=3, max_queue_size=QUEUE_SIZE)

	# S12 <--> S15, S16, S19, S20

	net.addLink(S12, S15, bw=LINK_CAPACITY, port1=3, port2=4, max_queue_size=QUEUE_SIZE)
	net.addLink(S12, S16, bw=LINK_CAPACITY, port1=4, port2=4, max_queue_size=QUEUE_SIZE)
	net.addLink(S12, S19, bw=LINK_CAPACITY, port1=5, port2=4, max_queue_size=QUEUE_SIZE)
	net.addLink(S12, S20, bw=LINK_CAPACITY, port1=6, port2=4, max_queue_size=QUEUE_SIZE)

	#FABRIC SWITCHES <--> TOR SWITCHES

	# S13 <--> S21, S22, S23, S24

	net.addLink(S13, S21, bw=LINK_CAPACITY, port1=5, port2=1, max_queue_size=QUEUE_SIZE)
	net.addLink(S13, S22, bw=LINK_CAPACITY, port1=6, port2=1, max_queue_size=QUEUE_SIZE)
	net.addLink(S13, S23, bw=LINK_CAPACITY, port1=7, port2=1, max_queue_size=QUEUE_SIZE)
	net.addLink(S13, S24, bw=LINK_CAPACITY, port1=8, port2=1, max_queue_size=QUEUE_SIZE)

	# S14 <--> S21, S22, S23, S24

	net.addLink(S14, S21, bw=LINK_CAPACITY, port1=5, port2=2, max_queue_size=QUEUE_SIZE)
	net.addLink(S14, S22, bw=LINK_CAPACITY, port1=6, port2=2, max_queue_size=QUEUE_SIZE)
	net.addLink(S14, S23, bw=LINK_CAPACITY, port1=7, port2=2, max_queue_size=QUEUE_SIZE)
	net.addLink(S14, S24, bw=LINK_CAPACITY, port1=8, port2=2, max_queue_size=QUEUE_SIZE)

	# S15 <--> S21, S22, S23, S24

	net.addLink(S15, S21, bw=LINK_CAPACITY, port1=5, port2=3, max_queue_size=QUEUE_SIZE)
	net.addLink(S15, S22, bw=LINK_CAPACITY, port1=6, port2=3, max_queue_size=QUEUE_SIZE)
	net.addLink(S15, S23, bw=LINK_CAPACITY, port1=7, port2=3, max_queue_size=QUEUE_SIZE)
	net.addLink(S15, S24, bw=LINK_CAPACITY, port1=8, port2=3, max_queue_size=QUEUE_SIZE)

	# S16 <--> S21, S22, S23, S24

	net.addLink(S16, S21, bw=LINK_CAPACITY, port1=5, port2=4, max_queue_size=QUEUE_SIZE)
	net.addLink(S16, S22, bw=LINK_CAPACITY, port1=6, port2=4, max_queue_size=QUEUE_SIZE)
	net.addLink(S16, S23, bw=LINK_CAPACITY, port1=7, port2=4, max_queue_size=QUEUE_SIZE)
	net.addLink(S16, S24, bw=LINK_CAPACITY, port1=8, port2=4, max_queue_size=QUEUE_SIZE)

	# S17 <--> S25, S26, S27, S28

	net.addLink(S17, S25, bw=LINK_CAPACITY, port1=5, port2=1, max_queue_size=QUEUE_SIZE)
	net.addLink(S17, S26, bw=LINK_CAPACITY, port1=6, port2=1, max_queue_size=QUEUE_SIZE)
	net.addLink(S17, S27, bw=LINK_CAPACITY, port1=7, port2=1, max_queue_size=QUEUE_SIZE)
	net.addLink(S17, S28, bw=LINK_CAPACITY, port1=8, port2=1, max_queue_size=QUEUE_SIZE)

	# S18 <--> S25, S26, S27, S28

	net.addLink(S18, S25, bw=LINK_CAPACITY, port1=5, port2=2, max_queue_size=QUEUE_SIZE)
	net.addLink(S18, S26, bw=LINK_CAPACITY, port1=6, port2=2, max_queue_size=QUEUE_SIZE)
	net.addLink(S18, S27, bw=LINK_CAPACITY, port1=7, port2=2, max_queue_size=QUEUE_SIZE)
	net.addLink(S18, S28, bw=LINK_CAPACITY, port1=8, port2=2, max_queue_size=QUEUE_SIZE)

	# S19 <--> S25, S26, S27, S28

	net.addLink(S19, S25, bw=LINK_CAPACITY, port1=5, port2=3, max_queue_size=QUEUE_SIZE)
	net.addLink(S19, S26, bw=LINK_CAPACITY, port1=6, port2=3, max_queue_size=QUEUE_SIZE)
	net.addLink(S19, S27, bw=LINK_CAPACITY, port1=7, port2=3, max_queue_size=QUEUE_SIZE)
	net.addLink(S19, S28, bw=LINK_CAPACITY, port1=8, port2=3, max_queue_size=QUEUE_SIZE)

	# S20 <--> S25, S26, S27, S28

	net.addLink(S20, S25, bw=LINK_CAPACITY, port1=5, port2=4, max_queue_size=QUEUE_SIZE)
	net.addLink(S20, S26, bw=LINK_CAPACITY, port1=6, port2=4, max_queue_size=QUEUE_SIZE)
	net.addLink(S20, S27, bw=LINK_CAPACITY, port1=7, port2=4, max_queue_size=QUEUE_SIZE)
	net.addLink(S20, S28, bw=LINK_CAPACITY, port1=8, port2=4, max_queue_size=QUEUE_SIZE)


	#Sources
	net.addLink(S21, H1, port1=5)
	net.addLink(S21, H2, port1=6)
	net.addLink(S21, H3, port1=7)
	net.addLink(S21, H4, port1=8)
	#net.addLink(S21, H19,port1=9)
	'''
	net.addLink(S22, H5, port1=5)
	net.addLink(S22, H6, port1=6)
	net.addLink(S22, H7, port1=7)
	net.addLink(S22, H8, port1=8)
	#net.addLink(S22, H20,port1=9)

	net.addLink(S25, H9, port1=5)
	net.addLink(S25, H10, port1=6)
	net.addLink(S25, H11, port1=7)
	net.addLink(S25, H12, port1=8)
	#net.addLink(S23, H21,port1=9)

	net.addLink(S26, H13, port1=5)
	net.addLink(S26, H14, port1=6)
	net.addLink(S26, H15, port1=7)
	net.addLink(S26, H16, port1=8)
	#net.addLink(S24, H22,port1=9)
	'''
	#Sinks
	net.addLink(S2, H18, port1=5)
	net.addLink(S27, H17, port1=5)

	info( '\n*** Adding MAC addresses\n')


	H1.setMAC("00:00:00:00:00:01")
	H2.setMAC("00:00:00:00:00:02")
	H3.setMAC("00:00:00:00:00:03")
	H4.setMAC("00:00:00:00:00:04")
	H17.setMAC("00:00:00:00:00:17")
	H18.setMAC("00:00:00:00:00:18")
	'''
	H1.setIP("10.0.0.1",24)
	H2.setIP("10.0.0.2",24)
	H3.setIP("10.0.0.3",24)
	H4.setIP("10.0.0.4",24)
	H17.setIP("10.0.0.17",24)
	H18.setIP("10.0.0.18",24)
	'''
	count = 1
	for h in net.hosts:
		h.setMAC("0:0:0:0:0:"+str(count))
		count += 1
		h.setIP("10.0.0."+str(count))

	info( '*** Starting Network\n')
	net.start()	

	info( '*** Creating QoS queues\n')

	for switch in range(21,28):
		for port in range (5,9):
			os.system('ovs-vsctl -- set port s'+str(switch)+'-eth'+str(port)+' qos=@newqos -- --id=@newqos create qos type=linux-htb \
			queues=0=@q0,1=@q1 -- --id=@q0 create queue other-config:min-rate=10000 \
			other-config:max-rate=40000 -- --id=@q1 create queue other-config:min-rate=1000 \
			other-config:max-rate=10000')
	#msg = "drone"

	print "*** Generating Traffic"

	h18 = net.getNodeByName("h18")
	h1 = net.getNodeByName("h1")
	h2 = net.getNodeByName("h2")
	h3 = net.getNodeByName("h3")

	h18.cmd("iperf -s -u -p 5000 > h18.txt &")
	h1.cmd("./test.sh 5000 > h1.txt &")
	h2.cmd("./test.sh 5000 > h2.txt &")
	h3.cmd("./test.sh 5000 > h3.txt &")

	print "*** Starting CLI"
	CLI(net)
	'''H1.cmd(msg)
	H2.cmd(msg)
	H3.cmd(msg)
	H4.cmd(msg)'''

	net.stop()

topos = {
        'mytopo': (lambda: MyTopo())
}
