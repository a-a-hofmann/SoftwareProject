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


class Firewall(EventMixin):

	nodes = [] 			#list of nodes.
	prev_stats_flows = defaultdict(lambda:defaultdict(lambda:None)) #structure to store flows statistics per node, e.g., [dpid][match] = mbps

	"Variables used in the firewall. Include whatever you want to test"
	blocked_tcp_ports = [] 		#list of tcp blocked ports. E.g., [80, 443]
	blocked_udp_ports = [] 		#list of udp blocked ports.
	black_list = [] #ip/mac addresses. E.g., MAC/IP --> ["00:00:00:00:00:01", "10.0.0.2"]
	icmp_threshold = 0.1 		#in mbps

	"Method executed when the class is instantiated"
	def __init__(self):
		"Declaring listeners of OpenFlow events. In this application we are going to hear 'ConnectionUp', 'PacketIn' and 'FlowStats' events"
		self.listenTo(core.openflow)
		"Declaring a timer to periodically (1s) call the method 'request_stats', which will request"
		Timer(1, self.request_stats, recurring=True)

	def request_stats(self):
		"Request flow statistics of every node in the network"
		for node in self.nodes:
			core.openflow.getConnection(node).send(of.ofp_stats_request(body=of.ofp_flow_stats_request()))

	"Handle events triggered when a new node is connected"
	def _handle_ConnectionUp (self,event):
		"If the connected node is not in the list of nodes then append it"
		if event.connection.dpid not in self.nodes:
			self.nodes.append(event.connection.dpid)

	"Install a flow rule to drop packets"
	def block_host(self, ip=None, mac=None, port=None):
		msg = of.ofp_flow_mod()
		msg.priority = 65535 #higher priority
		if ip: #if it was received an IP address then we will block by IP address
			msg.match.dl_type = ethernet.IP_TYPE
			msg.match.nw_src = IPAddr(ip)
		elif mac: #otherwise, the block is by MAC address
			msg.match.dl_src = EthAddr(mac)
		if port:
			msg.match.tp_dst = port
		msg.actions.append(of.ofp_action_output(port=of.OFPP_CONTROLLER))
		for node in self.nodes:
			try:
				core.openflow.getConnection(node).send(msg)
			except:
				continue

	'''
	This method handle packets sent by switches when they do not have a rule specifying how to handle the packet.
	In this case we are going to use this method to block when the first packets are sent.
	'''
	def _handle_PacketIn(self, event):
		"Parse the packet"
		packet = event.parsed
		"Check its type"
		ipv4_pkt = packet.find('ipv4')
		arp_pkt = packet.find('arp')
		if ipv4_pkt:
			src_ip = ipv4_pkt.srcip
		elif arp_pkt:
			src_ip = arp_pkt.protosrc
			src_mac = arp_pkt.hwsrc

		for address in self.black_list:
			if "." in address:
				self.block_host(ip=address)
			elif ":" in address:
				self.block_host(mac=address)

	'''
	This method handle flow statistics periodically requested to the devices. The period is defined in the timer declared at the '__init__' (in our case 1 second).
	We will use the method to obtain flow's statiscs and block users based on a few rules created as example.
	'''
	def _handle_FlowStatsReceived(self,event):

		"Get the node providing flow statiscs"
		dpid = event.connection.dpid

		def bytes_to_mbps(bytes):
			return bytes/1024.0/1024.0*8

		for stat in event.stats:

			"See the match structure in: https://www.opennetworking.org/images/stories/downloads/sdn-resources/onf-specifications/openflow/openflow-spec-v1.0.0.pdf"
			match = stat.match
			src_ip = match.nw_src

			"Skip LLDP (Link Layer Discovery) packets. The 'continue' skip this loop interaction"
			if match.dl_type == ethernet.LLDP_TYPE:
				continue
			"Initiate 'prev_stats_flows' in its first usage"
			if not self.prev_stats_flows[match][dpid]:
				self.prev_stats_flows[match][dpid] = 0
			"Get the previous byte_count"
			prev_byte_count = self.prev_stats_flows[match][dpid]
			"Store the current counter for bytes. This is done in a per-flow basis which means that we are obtaining the bandwidth usage of each flow-rule installed in the node"
			self.prev_stats_flows[match][dpid] = stat.byte_count
			"Calculate the mbps"
			mbps = bytes_to_mbps(stat.byte_count - prev_byte_count)

			"Firewall rules"

			"1 - if the protocol is ICMP and its bandwidth exceeds a certain bandwidth threshold"
			if match.nw_proto == ipv4.ICMP_PROTOCOL and mbps > self.icmp_threshold:
				self.block_host(ip=src_ip)

			"2 - if the protocol is TCP and the destination port is in the blocked list"
			if match.nw_proto == ipv4.TCP_PROTOCOL and match.tp_dst in self.blocked_tcp_ports:
				self.block_host(ip=src_ip)

			"3 - if the protocol is UDP and the destination port is in the blocked list"
			if match.nw_proto == ipv4.UDP_PROTOCOL and match.tp_dst in self.blocked_udp_ports:
				self.block_host(ip=src_ip)


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

	"Start the Firewall"
	core.registerNew(Firewall)
