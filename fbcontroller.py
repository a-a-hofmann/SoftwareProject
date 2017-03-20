from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *

from pox.lib.recoco import Timer

from datetime import datetime
from collections import defaultdict
from collections import namedtuple
import time
import itertools


import pox.lib.packet as pkt
from pox.lib.packet.ipv4 import ipv4
from pox.lib.packet.arp import arp
from pox.lib.packet.ethernet import ethernet
from pox.lib.addresses import IPAddr,EthAddr


import networkx as nx
from info_manager import *
from update_database import *
from path_table import PathTable

import matplotlib.pyplot as plt

info_manager = informationManager()

main_gui = None
PATH_REFRESH_RATE = 1
PATH_LIMIT = 10

class Forwarding(object):
	"""
	Forwading controller.
	"""

	CONSUMPTION_THRESHOLD = 50
	LB_THRESHOLD = 50

	def __init__(self, G):
		# Network Graph
		self.G = G

		core.openflow.addListeners(self, priority = 0)
		core.listen_to_dependencies(self)
		Timer(PATH_REFRESH_RATE, self.paths, recurring=True)
		Timer(10, self.pre_compute_paths, args={G: G}, recurring=False)


	def pre_compute_paths(self, G):
		"""
		Computes paths between all hosts in the network. It computes up to
		PATH_LIMIT paths per each host.
		All computed paths are saved to a path lookup table path_table.py
		Args:
			G: networkx graph containing the topology of the network.
		"""
		host_ids = set(host.dpid for host in info_manager.hosts)
		host_combinations = itertools.combinations(host_ids, 2)

		for src, dst in host_combinations:
			paths_generator = nx.all_shortest_paths(self.G, src, dst)

			counter = 0
			for path in paths_generator:
				if counter > PATH_LIMIT:
					break
				info_manager.path_table.put_path(path = tuple(paths_generator.next()), src = src, dst = dst)


	def paths(self):
		"""
		Iterates over all hosts and all active paths and
		checks whether their path is still the most efficient one.
		"""

		print "\nIterating over hosts and computing most efficient paths"
		print "---------------\n"

		for host in info_manager.hosts:
			if host.path_list and not host.is_sink:
				print "----- Host {} ------".format(host.ipaddr)
				for path in host.path_list:
					self.check_path(host, path)

		print "---------------\n"


	def check_path(self, host, current_path):
		"""
		For a given path check if there is a more efficient one to destination.
		Args:
			host: Host.
			current_path: Current host's path.
		"""

		src_dpid, src_port = current_path.src_dpid, current_path.src_port
		dst_dpid, dst_port = current_path.dst_dpid, current_path.dst_port

		node_consumptions, node_workloads = info_manager.compute_path_information(current_path.path)
		most_efficient_path = info_manager.get_most_efficient_path(self.G, src_dpid, dst_dpid)
		current_path.set_power_consumption(node_consumptions)
		overloaded_nodes = self.check_nodes_in_path_for_loadbalancing(workloads=node_workloads, path=current_path.path)

		if overloaded_nodes:
			new_path = self.get_path_for_load_balancing(src_dpid, dst_dpid, current_path, overloaded_nodes)

			if new_path:
				"""If there is a new path then reroute traffic.
				Otherwise all other paths are overloaded as well, do nothing"""
				src_host = info_manager.get_host(dpid=src_dpid, port=src_port)
				dst_host = info_manager.get_host(dpid=dst_dpid, port=dst_port)

				new_path = host.create_path(src_host, dst_host, new_path)
				succededRemovingPath = host.remove_path(current_path)
				assert succededRemovingPath

				self.modify_path_rules(most_efficient_path, src_host, dst_host)

				node_consumption_new_path = info_manager.compute_path_information(new_path.path)[0]
				path_consumption = sum(node_consumption_new_path.itervalues())
				new_path.set_power_consumption(node_consumption_new_path)


	def get_path_for_load_balancing(self, src, dst, current_path, overloaded_nodes):
		"""
		Gets a new path from src to dst, taking node workload into account.
		Args:
			src: Source node dpid.
			dst: Destination node dpid.
			current_path: Current path as list of node dpids.
			overloaded_nodes: which nodes are overloaded in the current path.
		Returns:
		 	candidate: new path or None if no path was found.
		"""

		all_paths = info_manager.all_paths(self.G, src, dst)
		all_paths.remove(current_path.path)
		current_path_consumption = current_path.total_consumption

		candidates = []
		for candidate in all_paths:
			overloaded = self.check_nodes_in_path_for_loadbalancing(path=candidate)

			if not overloaded and not any(item[0] in candidate for item in overloaded_nodes):
				"Choose as candidate only if it isn't overloaded as well."
				candidate_path_consumption = sum(info_manager.compute_path_information(candidate)[0].itervalues())
				if current_path_consumption + candidate_path_consumption < self.CONSUMPTION_THRESHOLD:
					candidates.append(candidate)

		if candidates:
			return candidates[0]
		return None


	def check_nodes_in_path_for_loadbalancing(self, workloads=None, path=None):
		"""
		For a given path check if any of the nodes has too much workload.
		Args:
			workloads: dictionary of node dpids and workload of each node (default=None).
			path: path from which to compute node workloads (default=None)
		Returns:
			node_list: list of nodes whose workload is over the threshold
			and their current workload. src and dst nodes are omitted since
			there is nothing that can be done in those cases.
		"""
		if path and not workloads:
			workloads = info_manager.compute_path_information(path)[1]

		overloaded_nodes = []
		for node_id, node_workload in workloads.iteritems():
			if node_workload > self.LB_THRESHOLD:
				overloaded_nodes.append((node_id, node_workload))

		if path:
			src_node, dst_node = path[0], path[-1]
			overloaded_nodes = [overloaded for overloaded in overloaded_nodes if overloaded[0] != src_node and overloaded[0] != dst_node]
		return overloaded_nodes


	def modify_path_rules(self, path, src_host, dst_host):

		print "There is a more efficient path, rerouting to: {}".format(path)
		"modify routing rules for each node in new path"

		msg = of.ofp_flow_mod(command=of.OFPFC_MODIFY)
		msg.match.dl_type = ethernet.IP_TYPE
		msg.match.nw_dst = dst_host.ipaddr
		msg.priority = 65535 #highest priority
		for index, node_dpid in enumerate(path):

			"first node in the path"
			if node_dpid == src_host.dpid:
				msg.match.nw_src = src_host.ipaddr

			if index + 1 < len(path):
				"intermediate node in the path"
				next_node_dpid = path[index + 1]
				out_port = info_manager.get_node_out_port(node_dpid, next_node_dpid)
			else:
				"last node in path"
				msg.match.nw_src = src_host.ipaddr
				out_port = dst_host.port

			# print "Source node {} routing node {} to {} on port {}".format(src_host.dpid, node_dpid, dst_host.ipaddr, out_port)

			msg.actions.append(of.ofp_action_output(port = out_port))
			connection = core.openflow.getConnection(node_dpid)
			connection.send(msg)


	def _handle_ConnectionUp (self,event):

		info_manager.nodes.append(info_manager.Node(event))
		event.connection.send(of.ofp_flow_mod(command=of.OFPFC_DELETE))


	def _handle_ConnectionDown (self,event):

		if event.connection.dpid in info_manager.nodes:
			del info_manager.nodes[event.connection.dpid]

		self.G.remove_node(event.connection.dpid)


	def _handle_openflow_discovery_LinkEvent(self,event):

		dpid1, dpid2 = event.link.dpid1, event.link.dpid2
		port1, port2 = event.link.port1, event.link.port2

		self.G.add_node(dpid1)
		self.G.add_node(dpid2)

		if event.added:
			self.G.add_edge(dpid1,dpid2)
			info_manager.get_node(dpid1).link[dpid1][port1] = dpid2
			info_manager.get_node(dpid1).adjacency[dpid1][dpid2] = port1

		if event.removed:
			if self.G.has_edge(dpid1,dpid2):
					self.G.remove_edge(dpid1,dpid2)


	def _handle_PacketIn (self, event):
		packet = event.parsed

		if packet.type == ethernet.LLDP_TYPE or not packet.parsed:
			return

		src_mac = str(EthAddr(packet.src))
		dst_mac = str(EthAddr(packet.dst))

		dpid = event.connection.dpid
		port = event.port

		a = packet.find('ipv4')
		b = packet.find('arp')
		if a:
			src_ip = a.srcip
			dst_ip = a.dstip
		if b:
			src_ip = b.protosrc
			dst_ip = b.protodst

		src_host = info_manager.get_host(ip=src_ip)
		dst_host = info_manager.get_host(ip=dst_ip)

		if not src_host or not dst_host:
			return

		msg = of.ofp_flow_mod(command=of.OFPFC_ADD)
		msg.data = event.ofp
		msg.match.dl_type = ethernet.IP_TYPE

		if core.openflow_discovery.is_edge_port(dpid, port):
			if not info_manager.get_host(dpid = dpid, port = port):
				info_manager.hosts.append(info_manager.Host(dpid, port, src_mac, src_ip))
			try:
				path = src_host.get_path(src_host.dpid, dst_host.dpid).path
			except:
				try:
					path = info_manager.get_most_efficient_path(self.G, src_host.dpid, dst_host.dpid)
					# path = nx.shortest_path(self.G, src_host.dpid, dst_host.dpid)
					src_host.create_path(src_host, dst_host, path)
				except Exception as e:
					print repr(e)
					return EventHalt
		else:
			path = src_host.get_path(src_host.dpid, dst_host.dpid).path

		if dpid not in path:
			return EventHalt

		msg.match.nw_dst = dst_ip

		if dpid == src_host.dpid:
			"First node in path"
			msg.match.nw_src = src_ip

		node_index = path.index(dpid)
		if node_index + 1 < len(path):
			"All nodes in path but the last"
			next_node_dipd = path[path.index(dpid) + 1]
			out_port = info_manager.get_node_out_port(dpid, next_node_dipd)

		elif node_index + 1 == len(path):
			"Last node in path"
			out_port = dst_host.port
			msg.match.nw_src = src_ip

		# print "PacketIn:\tSource node {} routing node {} to {} on port {}".format(src_host.dpid, dpid, dst_ip, out_port)
		msg.actions.append(of.ofp_action_output(port = out_port))
		event.connection.send(msg)


Payload = namedtuple('Payload', 'timeSent')

class Monitoring (object):

	count_port_stats_adaptive = 0
	count_port_stats_straight = 0
	count_flow_stats_adaptive = 0
	count_flow_stats_straight = 0

	prev_stats_flows = defaultdict(lambda:defaultdict(lambda:None))
	prev_stats_ports = defaultdict(lambda:defaultdict(lambda:None))

	MIN_WORKLOAD = 0.1

	def __init__ (self, G):

		self.G = G

		core.openflow.addListeners(self)
		core.listen_to_dependencies(self)
		self.polling_timer = Timer(5, self.request_stats, recurring=True)
		Timer(1, self.get_controller_usage, recurring=True)


	def request_stats(self):
		# Get consumption of each node in the topology
		for i in range(len(info_manager.nodes)):
			self.count_flow_stats_straight += 1
			self.count_port_stats_straight += 1

		nodes_list = []
		for h in info_manager.hosts:
			border_node = info_manager.get_node(h.dpid)
			try:
				core.openflow.getConnection(border_node.id).send(of.ofp_stats_request(body=of.ofp_flow_stats_request()))
				self.count_flow_stats_adaptive += 1
				for p in h.path_list:
					path = p.path
					for node in path:
						if node not in nodes_list:
							nodes_list.append(node)
			except:
				continue

		aux = 0
		for node in nodes_list:
			aux += 1
			core.openflow.getConnection(node).send(of.ofp_stats_request(body=of.ofp_port_stats_request()))
			self.count_port_stats_adaptive += 1

		if aux == 0:
			self.count_port_stats_adaptive = 0

		update_monitoring_stats(self.count_flow_stats_straight, self.count_flow_stats_adaptive, self.count_port_stats_straight, self.count_port_stats_adaptive)
		info_manager.update_network_consumption()


	def get_controller_usage(self):
		import commands
		import psutil
		#cpu_cmd = "top -bn 2 -d 0.01 -n2 | grep '^%Cpu' | tail -n 1 | gawk '{print $2+$4+$6}'" #not working
		#out1,cpu = commands.getstatusoutput(cpu_cmd)
		cpu = psutil.cpu_percent(interval=None)
		mem_cmd = "free | grep Mem | awk '{print $3/$2 * 100.0}'"
		out1,mem = commands.getstatusoutput(mem_cmd)
		update_system_utilization(float(cpu), float(mem))


	def bytes_to_mbps(self, bytes):
		return bytes/1024.0/1024.0*8

	def probe_packet(self, src, dst):

		src_host = info_manager.get_host(mac=src)
		dst_host = info_manager.get_host(mac=dst)

		''' Based on OpenNetMon
		van Adrichem, N.L.M.; Doerr, C.; Kuipers, F.A., OpenNetMon: Network monitoring in OpenFlow Software-Defined Networks'''

		ip_pck = pkt.ipv4(protocol=253, dstip = IPAddr("224.0.0.255"))
		pl = Payload(time.time())
		ip_pck.set_payload(repr(pl))

		packet = pkt.ethernet(type=pkt.ethernet.IP_TYPE)
		packet.src = EthAddr(src_host.macaddr)
		packet.dst = EthAddr(dst_host.macaddr)
		packet.set_payload(ip_pck)

		msg = of.ofp_packet_out()
		msg.actions.append(of.ofp_action_output(port = src_host.port))
		msg.data = packet.pack()
		core.openflow.getConnection(src_host.dpid).send(msg)

		packet = pkt.ethernet(type=pkt.ethernet.IP_TYPE)
		packet.src = EthAddr(src_host.macaddr)
		packet.dst = EthAddr(dst_host.macaddr)
		packet.set_payload(ip_pck)

		msg = of.ofp_packet_out()
		msg.actions.append(of.ofp_action_output(port = of.OFPP_CONTROLLER))
		msg.data = packet.pack()
		core.openflow.getConnection(src_host.dpid).send(msg)


	def _handle_PortStatsReceived(self,event):

		dpid = event.connection.dpid
		node = info_manager.get_node(dpid)

		node.reset_port_workload()

		for stat in event.stats:

			if stat.port_no == 65534:
				continue

			if not self.prev_stats_ports[dpid][stat.port_no]:
				self.prev_stats_ports[dpid][stat.port_no] = 0

			delta_byte_count = stat.rx_bytes - self.prev_stats_ports[dpid][stat.port_no]
			self.prev_stats_ports[dpid][stat.port_no] += delta_byte_count

			mbps = self.bytes_to_mbps(delta_byte_count)

			global main_gui

			main_gui.hosts_list = info_manager.hosts

			if mbps == 0:
				dpid_dst = node.link[node.id][stat.port_no]
				main_gui.paintlink[dpid_dst][dpid] = mbps
				main_gui.paintlink[dpid][dpid_dst] = mbps

			elif mbps >= self.MIN_WORKLOAD:
				node.set_workload(stat.port_no, mbps)
				dpid_dst = node.link[node.id][stat.port_no]
				main_gui.paintlink[dpid_dst][dpid] = mbps
				main_gui.paintlink[dpid][dpid_dst] = mbps

				h = info_manager.get_host(dpid = dpid, port = stat.port_no)
				if not h:
					continue
				if mbps > h.workload:
					mbps = float(h.workload)
					h.workload = 0.0
				if h.netw_tokens.decrease_rate:
					update_workload(h.macaddr, h.max_workload)

				user_consumption = info_manager.get_host_consumption(h, mbps)
				#print h.macaddr, mbps, user_consumption
				h.update_tokens(user_consumption)
				update_user_consumption(h.macaddr, user_consumption)

		# consumption = node.get_consumption()[0]
		# if consumption > 0.12:
		# 	print "Node {} stats:\t{}".format(node.id, consumption)
		# 	print "\tPorts listening:\t{}".format([stat.port_no for stat in event.stats])

		proportional, baseline, constant = node.get_consumption()
		update_switch_consumption(dpid, proportional, baseline, constant)


	def _handle_FlowStatsReceived(self,event):

		dpid = event.connection.dpid
		node = info_manager.get_node(dpid)


		for stat in event.stats:

			match = stat.match

			''' Based on OpenNetMon
			van Adrichem, N.L.M.; Doerr, C.; Kuipers, F.A., OpenNetMon: Network monitoring in OpenFlow Software-Defined Networks'''

			if match.dl_type != pkt.ethernet.LLDP_TYPE and not (match.dl_type == pkt.ethernet.IP_TYPE and match.nw_proto == 253
				and match.nw_dst == IPAddr("224.0.0.255")) and match.dl_type != 0x806:

				if not self.prev_stats_flows[match][dpid]:
					self.prev_stats_flows[match][dpid] = 0, 0, 0, 0

				prev_packet_count, prev_byte_count, prev_duration_sec, prev_duration_nsec = self.prev_stats_flows[match][dpid]
				delta_packet_count = stat.packet_count - prev_packet_count
				delta_byte_count = stat.byte_count - prev_byte_count
				delta_duration_sec = stat.duration_sec - prev_duration_sec
				delta_duration_nsec = stat.duration_nsec - prev_duration_nsec
				self.prev_stats_flows[match][dpid] = stat.packet_count, stat.byte_count, stat.duration_sec, stat.duration_nsec

				mbps = self.bytes_to_mbps(delta_byte_count)

				src_host = info_manager.get_host(ip=match.nw_src)
				dst_host = info_manager.get_host(ip=match.nw_dst)

				"Check if host has tokens otherwise consider the best effort workload"
				if src_host.netw_tokens.predefined_tokens != 0 and src_host.netw_tokens.decrease_rate:
					if mbps > self.MIN_WORKLOAD:
						mbps = src_host.max_workload

				"Send probe packet if the host has tokens"
				path = src_host.get_path(src_host.dpid, dst_host.dpid)
				if mbps >= self.MIN_WORKLOAD:
					if dpid == src_host.dpid or dpid == dst_host.dpid:
						src_host.update_wl_pktloss(src_host.macaddr, dst_host.macaddr, mbps, dpid)
						loss, mean_loss = src_host.calc_pktloss(src_host.macaddr, dst_host.macaddr, src_host.dpid, dst_host.dpid)
						update_pkt_loss(src_host.macaddr, dst_host.macaddr, loss, src_host.max_loss)

					self.probe_packet(src_host.macaddr, dst_host.macaddr)

					path.workload = mbps
					src_host.workload = mbps
					update_workload(src_host.macaddr, mbps)
					continue


	def _handle_PacketIn(self, event):

		'''Based on OpenNetMon
		van Adrichem, N.L.M.; Doerr, C.; Kuipers, F.A., OpenNetMon: Network monitoring in OpenFlow Software-Defined Networks'''

		timeRecv = time.time()
		packet = event.parsed

		src_mac = str(EthAddr(packet.src))
		dst_mac = str(EthAddr(packet.dst))

		if packet.effective_ethertype != pkt.ethernet.IP_TYPE:
			return

		ip_pck = packet.find(pkt.ipv4)

		if ip_pck is None or not ip_pck.parsed:
			return

		if ip_pck.protocol != 253 or ip_pck.dstip != IPAddr("224.0.0.255"):
			return
		else:
			payload = eval(ip_pck.payload)
			dst_host = info_manager.get_host(mac=packet.dst)

			if dst_host:
				latency = round(timeRecv - payload.timeSent, 4)
				src_host = info_manager.get_host(mac=packet.src)
				update_latency(src_mac, dst_mac, latency, src_host.max_latency)
				update_jitter(src_mac, dst_mac, src_host.calc_jitter(latency), src_host.max_jitter)
				return EventHalt

"@param topo: used to specify the topology GUI"
def launch (topo = None):
	try:
		import os
		os.system("sudo fuser -k 6633/tcp")
		os.system("sudo fuser -k 8090/udp")
	except:
		pass

	import pox.log.color
	pox.log.color.launch()
	import pox.log

	pox.log.launch(format="[@@@bold@@@level%(name)-22s@@@reset] " +"@@@bold%(message)s@@@normal")

	import pox.openflow.discovery
	pox.openflow.discovery.launch(eat_early_packets=True)

	import pox.misc.full_payload as fp
	fp.launch()

	import pox.py as py
	py.launch()

	def open_gui():
		global main_gui
		if topo == "fb":
			import fbgui as gui
			info_manager.set_gui(topo)
			main_gui = gui
			gui = gui.launch()
			gui.mainloop()
			info_manager.pre_compute_paths()
		elif topo == "rnp":
			import rnpgui as gui
			info_manager.set_gui(topo)
			main_gui = gui
			gui = gui.launch()
			gui.mainloop()
		else:
			return
	if topo:
		from threading import Thread
		graphicsThread = Thread(target = open_gui)
		graphicsThread.daemon = True
		graphicsThread.start()
		G = nx.Graph()
		info_manager.path_table = PathTable()
		core.registerNew(Forwarding, G)
		core.registerNew(Monitoring, G)
