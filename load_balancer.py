from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.recoco import Timer

import pox.lib.packet as pkt
from pox.lib.packet.ipv4 import ipv4
from pox.lib.packet.arp import arp
from pox.lib.packet.ethernet import ethernet
from pox.lib.addresses import IPAddr,EthAddr

from collections import defaultdict

class Forwarding(EventMixin):
	
	nodes = []	#list of nodes	

	prev_stats_ports = defaultdict(lambda:defaultdict(lambda:None))	#structure to store ports statistics per node, e.g., [dpid][match] = mbps
	
	lb_threshold = 10.0 #In mbps. Threshold to start balancing the load, include whatever you want to test.
	lb_control = False #control the turn between nodes in the load balancer

	"Method executed when the class is instantiated"
	def __init__(self):

		"Declaring listeners of OpenFlow events"
		self.listenTo(core.openflow)
		"Declaring a timer to periodically (1s) call the method 'request_stats'"
		Timer(1, self.request_stats, recurring=True)
	
	def request_stats(self):
		"Request port statistics of every node in the network"
		for node in self.nodes:
			try:
				core.openflow.getConnection(node).send(of.ofp_stats_request(body=of.ofp_port_stats_request()))
			except:
				pass

	
	"Handle events triggered when a new node is connected"
	def _handle_ConnectionUp (self,event):
		"If the connected node is not in the list of nodes then append it"
		if event.connection.dpid not in self.nodes:
			self.nodes.append(event.connection.dpid)

	def _handle_PortStatsReceived(self,event):
		
		"Get the node id"
		dpid = event.connection.dpid

		def bytes_to_mbps(bytes):
			return bytes/1024.0/1024.0*8	

		for stat in event.stats:
			"Ignore default port"
			if stat.port_no == 65534:
				continue

			"Initialize the dict"		
			if not self.prev_stats_ports[dpid][stat.port_no]:
					self.prev_stats_ports[dpid][stat.port_no] = 0
			"The stat.rx_bytes is cumulative, so we take the delta between the last value (stored in prev_stats) and the current value"
			delta_byte_count = stat.rx_bytes - self.prev_stats_ports[dpid][stat.port_no]
			self.prev_stats_ports[dpid][stat.port_no] = stat.rx_bytes

			mbps = bytes_to_mbps(delta_byte_count)

			if dpid == 1:
				#print "Node=",dpid,"Mbps=",mbps
				if mbps >= self.lb_threshold:
					if self.lb_control == False:
						self.lb_control = True
						out_port = 4
					else:
						self.lb_control = False
						out_port = 5
					msg = of.ofp_flow_mod(command=of.OFPFC_MODIFY_STRICT)
					msg.match.dl_type = 0x800
					msg.match.nw_dst = IPAddr("10.0.0.4")
					msg.priority = 65535 #higher priority
					msg.actions.append(of.ofp_action_output(port = out_port))
					event.connection.send(msg)
					return EventHalt
			#and stat.port_no == 1 is the "incoming" port, i.e., [s1 port whatever <--connectedTo--> port 1 of s2] OR s1 <--connectedTo--> [port 1 of s3]
			if dpid == 2 and mbps >= self.lb_threshold and stat.port_no == 1: 
				print "Node=",dpid, "Mbps=",mbps
			if dpid == 3 and mbps >= self.lb_threshold and stat.port_no == 1:
				print "Node=",dpid, "Mbps=",mbps
				
			#if dpid == 4:
				#print "Node=",dpid,"Mbps=",mbps
			

"Method executed when the controller is started"
def launch():
	"Try to clean anything using 6633/tcp before starting the controller"
	try:
		import os
		os.system("sudo fuser -k 6633/tcp")
	except:
		pass

	"Log and colors"
	import pox.log.color
	pox.log.color.launch()
	import pox.log
	pox.log.launch(format="[@@@bold@@@level%(name)-22s@@@reset] " +"@@@bold%(message)s@@@normal")	

	"Full packets"
	import pox.misc.full_payload as fp
	fp.launch()

	"Component to discover links/topology"
	import pox.openflow.discovery
	pox.openflow.discovery.launch(eat_early_packets=True)

	"Import and start a spanning tree component"
	import pox.openflow.spanning_tree as spt
	spt.launch()

	"Import and start a standard forwarding component"
	import pox.forwarding.l2_learning as forwarding
	forwarding.launch()

	"Start the Forwarding"
	core.registerNew(Forwarding)
	
