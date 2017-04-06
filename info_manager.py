from collections import defaultdict
from datetime import datetime
from pox.lib.addresses import IPAddr,EthAddr
from update_database import *
import networkx as nx
from path_table import PathTable
from path import Path


MIN_WORKLOAD = 0.1
SC_THRESHOLD = 5
ALR_1_THRESHOLD = 10

dirty = False

class informationManager():

	hosts = []
	nodes = []
	path_table = None

	all_active_paths = defaultdict(lambda: defaultdict(set))

	def get_all_active_paths(self):
		self.path_table.print_active_paths()
		return self.path_table.get_active_paths()
		# global dirty
		# print "Is dirty or not? {}".format(dirty)
		# if dirty:
		# 	print "Dirty, rebuilding cache"
		# 	self.all_active_paths = defaultdict(lambda: defaultdict(set))
		# 	for host in self.hosts:
		# 		if not host.is_sink:
		# 			for path in host.path_list:
		# 				src, dst = path.path[0], path.path[-1]
		# 				if src != dst:
		# 					self.all_active_paths[src][dst].add(path)
		# 	dirty = False
		#
		# 	for src in self.all_active_paths:
		# 		for dst in self.all_active_paths[src]:
		# 			print "{}-{}:\t{}".format(src, dst, self.all_active_paths[src][dst])

			# return self.all_active_paths
		# else:
		# 	print "Using cached"
		# 	for src in self.all_active_paths:
		# 		for dst in self.all_active_paths[src]:
		# 			print "{}-{}:\t{}".format(src, dst, self.all_active_paths[src][dst])
		# 	return self.all_active_paths


	def get_most_efficient_path(self, G, src, dst):
		"""
		For a given source src and destination dst, compute the most energy efficient path.
		Args:
			G: graph.
			src: source obj.
			dst: destination obj.
		Returns:
			path_consumption: consumption of the path as a whole.
			node_consumptions: dict of node dpids and node consumption
		"""
		all_paths = self.all_paths(G, src, dst)
		all_paths_consumptions = [sum(self.compute_path_information(path.path)[0].itervalues()) for path in all_paths]

		#print "All paths: [{}, {}]".format(src, dst)
		# print "\n\n"
		# i = 1
		# for path in all_paths:
		# 	print "Path {}".format(i)
		# 	print path
		# 	print all_paths_consumptions[i - 1], "\n\n"
		# 	i += 1
		#print "---"

		minimal_path = min(all_paths_consumptions)
		minimal_path_index = all_paths_consumptions.index(minimal_path)
		print "Minimal path: ", all_paths[minimal_path_index]
		print "Minimal Path consumption: " + str(minimal_path)
		return all_paths[minimal_path_index]


	def all_paths(self, G, src, dst):
		"""
		For a given source src and destination dst, compute all shortest paths.
		Args:
			G: graph.
			src: source obj.
			dst: destination obj.
		Returns:
			list of all paths between src and dst.
		"""
		print "Fetching all paths between {}-{}".format(src, dst)
		if self.path_table.has_path(src.dpid, dst.dpid):
			"Using cached path"
			print "Using cached paths between {}-{}".format(src, dst)
			return [p for p in self.path_table.get_path(src.dpid, dst.dpid)]
		else:
			"Compute and cache new path"
			print "Computing all paths between {}-{}".format(src, dst)
			for path in nx.all_shortest_paths(G, src.dpid, dst.dpid):
				pathObj = Path.of(src, dst, path)
				self.path_table.put_path(pathObj, src.dpid, dst.dpid)

			return self.path_table.get_path(src.dpid, dst.dpid)


	def compute_path_information(self, path):
		"""
		For a given path compute path consumption, per node consumption, path
		workload and per node workload.
		Args:
			path: list of node dpids representing a path.
		Returns:
			path_consumption: consumption of the path as a whole.
			node_consumptions: dict of node dpids and node consumption.
			node_workloads: dict of node dpids and their workload.
			path_workload: workload of the path as a whole.
		"""
		node_consumptions = {}
		node_workloads = {}
		for path_node_id in path:
			node = self.get_node(path_node_id)
			proportional, baseline, constant = node.get_consumption()
			node_consumptions[path_node_id] = proportional
			node_workloads[path_node_id] = node.get_workload()
		return node_consumptions, node_workloads


	def set_gui(self, gui):

		def create_host(dpid, port, macaddr, ip, is_sink=False):
			host = self.Host(dpid, port, macaddr, ip)
			if not host.is_sink:
				self.hosts.append(host)
			return host

		if gui == "rnp":
			create_host(1,7, EthAddr("00:00:00:00:00:01"),IPAddr("10.0.0.1"))
			create_host(1,8, EthAddr("00:00:00:00:00:02"),IPAddr("10.0.0.2"))
			create_host(12,5, EthAddr("00:00:00:00:00:03"),IPAddr("10.0.0.3"))
			create_host(12,6, EthAddr("00:00:00:00:00:04"),IPAddr("10.0.0.4"))
			create_host(15,3, EthAddr("00:00:00:00:00:05"),IPAddr("10.0.0.5"))
			create_host(15,4, EthAddr("00:00:00:00:00:06"),IPAddr("10.0.0.6"))
			create_host(7,7, EthAddr("00:00:00:00:00:07"),IPAddr("10.0.0.7"))
			create_host(7,8, EthAddr("00:00:00:00:00:08"),IPAddr("10.0.0.8"))
		elif gui == "fb":
			#### USERS PARAMETERS ####
			bp_1 = create_host(21,5, EthAddr("00:00:00:00:00:01"),IPAddr("10.0.0.1"))
			bp_1.set_netw_tokens(50.0, 4) 	#number of tokens/number of renews
			bp_1.max_latency = 100		#latency (ms)
			bp_1.max_jitter = 50		#jitter (ms)
			bp_1.max_loss = 5 		#loss (%)
			bp_1.max_workload = 1		#workload threshold (Mbps)
 			###
			gp1_1 = create_host(21,6, EthAddr("00:00:00:00:00:02"),IPAddr("10.0.0.2"))
			gp1_1.set_netw_tokens(30.0, 4)	#number of tokens/number of renews
			gp1_1.max_latency = 100		#latency (ms)
			gp1_1.max_jitter = 50		#jitter (ms)
			gp1_1.max_loss = 5		#loss (%)
			gp1_1.max_workload = 0.5	#workload threshold (Mbps)
			###
			gp2_1 = create_host(21,7, EthAddr("00:00:00:00:00:03"),IPAddr("10.0.0.3"))
			gp2_1.set_netw_tokens(20.0, 4)	#number of tokens/number of renews
			gp2_1.max_latency = 100		#latency (ms)
			gp2_1.max_jitter = 50		#jitter (ms)
			gp2_1.max_loss = 5		#loss (%)
			gp2_1.max_workload = 0.1	#workload threshold (Mbps)
			###
			gp2_2 = create_host(21,8, EthAddr("00:00:00:00:00:04"),IPAddr("10.0.0.4"))
			gp2_2.set_netw_tokens(10.0, 4)	#number of tokens/number of renews
			gp2_2.max_latency = 100		#latency (ms)
			gp2_2.max_jitter = 50		#jitter (ms)
			gp2_2.max_loss = 5		#loss (%)
			gp2_2.max_workload = 0.1	#workload threshold (Mbps)
			###########################
			'''
			create_host(22,5, EthAddr("00:00:00:00:00:05"),IPAddr("10.0.0.5"))
			create_host(22,6, EthAddr("00:00:00:00:00:06"),IPAddr("10.0.0.6"))
			create_host(22,7, EthAddr("00:00:00:00:00:07"),IPAddr("10.0.0.7"))
			create_host(22,8, EthAddr("00:00:00:00:00:08"),IPAddr("10.0.0.8"))
			create_host(25,5, EthAddr("00:00:00:00:00:09"),IPAddr("10.0.0.9"))
			create_host(25,6, EthAddr("00:00:00:00:00:10"),IPAddr("10.0.0.10"))
			create_host(25,7, EthAddr("00:00:00:00:00:11"),IPAddr("10.0.0.11"))
			create_host(25,8, EthAddr("00:00:00:00:00:12"),IPAddr("10.0.0.12"))
			create_host(26,5, EthAddr("00:00:00:00:00:13"),IPAddr("10.0.0.13"))
			create_host(26,6, EthAddr("00:00:00:00:00:14"),IPAddr("10.0.0.14"))
			create_host(26,7, EthAddr("00:00:00:00:00:15"),IPAddr("10.0.0.15"))
			create_host(26,8, EthAddr("00:00:00:00:00:16"),IPAddr("10.0.0.16"))
			'''

			snk1 = create_host(27,5, EthAddr("00:00:00:00:00:17"),IPAddr("10.0.0.5"), True)
			snk2 = create_host(2,5, EthAddr("00:00:00:00:00:18"),IPAddr("10.0.0.6"), True)

			global dirty
			dirty = True
		else:
			print "***** PLEASE, SPECIFY SPECIFY THE TOPOLOGY USER INTERFACE USING THE PARAMETER '--topo='\nE.g., --topo=fb or --topo=rnp"


	def update_network_consumption(self):
		proportional, baseline, constant = 0,0,0
		for node in self.nodes:
			if node.consumption:
				for triple in node.consumption:
					p,b,c = triple
					proportional += p
					baseline += b
					constant += c
				del node.consumption[:]
				update_node_data(node.id, node.get_workload(), proportional, baseline, constant)
			else:
				p, b, c = node.get_consumption(node.get_workload())
				proportional += p
				baseline += b
				constant += c

			node.reset_port_workload()

		update_total_consumption(proportional, baseline, constant)
		update_total_consumption_with_policy(proportional, baseline, constant)


	def get_host_consumption(self, host, host_wl):

		shared_nodes = {}
		power_consumption = {}


		def dst_is_not_sink(d, p):
			dst = self.get_host(dpid=d, port=p)
			if not dst.is_sink:
				return True

		"for each user path"
		for host_path in host.path_list:

			if dst_is_not_sink(host_path.dst_dpid, host_path.dst_port):
				continue

			"for each node in the user path"
			for host_node in host_path.path:
				aux_shared_nodes = []
				"for each host in the list of hosts"
				for other_host in self.hosts:
					"do not account the same user twice"
					if other_host.macaddr != host.macaddr and not other_host.is_sink:
						"for each path in the user path"
						for other_path in other_host.path_list:
							if dst_is_not_sink(other_path.dst_dpid, other_path.dst_port):
								continue
							"for each node in the user path"
							for other_host_node in other_path.path:
								"if the node is the same and it's not in the list of shared nodes, we append it"
								if host_node == other_host_node and host_node not in aux_shared_nodes:
									aux_shared_nodes.append(host_node)

						"count the number of shared nodes between 'other hosts', EXCLUDING the host being compared"
						for node in aux_shared_nodes:
							if node not in shared_nodes:
								"Why '2': because we need to include the nodes of the user path"
								shared_nodes[node] = 2.0
							else:
								shared_nodes[node] += 1.0
		consumption = 0

		node_object = None
		for node, counter in shared_nodes.iteritems():

			node_object = self.get_node(node)
			node_wl = 0

			for port, wl in node_object.aux_workload.iteritems():
				node_wl += wl
			if node_wl < MIN_WORKLOAD:
				consumption += node_object.DEVICE_SLEEP/counter
			elif node_wl <= SC_THRESHOLD:
				consumption += node_object.DEVICE_SLEEP/counter * node_object.tOn + (node_object.CHASSIS/counter * host_wl/node_object.LINK_CAPACITY) + (node_object.INTERFACE * host_wl * node_object.ALR_1) * node_object.tOn
			else:
				if node_wl > 0 and node_wl <= ALR_1_THRESHOLD:
					aux = node_object.INTERFACE * host_wl * node_object.ALR_1
				elif node_wl > ALR_1_THRESHOLD:
					aux = node_object.INTERFACE * host_wl
				consumption += (node_object.CHASSIS/counter * host_wl/node_object.LINK_CAPACITY) + aux

		if node_object:
			node_object.aux_workload = node_object.aux_workload.fromkeys(node_object.aux_workload, 0)

		return to_kw(consumption)

	def get_hosts_from_path(self, path):
		src_dpid, src_port = path.src_dpid, path.src_port
		dst_dpid, dst_port = path.dst_dpid, path.dst_port
		src_host = self.get_host(dpid=src_dpid, port=src_port)
		dst_host = self.get_host(dpid=dst_dpid, port=dst_port)
		return src_host, dst_host

	class Host(object):

		class powerToken(object):
			predefined_tokens = 0
			tokens = 0
			threshold = 0
			decrease_rate = False
			nrenewals = 0

		class packetLoss(object):
			workload = []
			def __init__(self, src_mac, dst_mac, dpid):
				self.src_mac = src_mac
				self.dst_mac = dst_mac
				self.dpid = dpid

		def find_pktloss_object(self, src_mac, dst_mac, dpid):
			for l in self.loss:
				if l.src_mac == src_mac and l.dst_mac == dst_mac and l.dpid == dpid:
					return l
			else:
				l = self.packetLoss(src_mac, dst_mac, dpid)
				self.loss.append(l)
				return l

		def update_wl_pktloss(self, src_mac, dst_mac, mbps, dpid):
			"traverse the list of 'pktloss' objects"
			self.find_pktloss_object(src_mac, dst_mac, dpid).workload.append(mbps)

		def calc_pktloss(self, src_mac, dst_mac, src_dpid, dst_dpid):

			"get the workload historic between src and dst"
			l_src = self.find_pktloss_object(src_mac, dst_mac, src_dpid).workload
			l_dst = self.find_pktloss_object(dst_mac, src_mac, dst_dpid).workload

			"calculate losses"
			if len(l_src) > 0 and len(l_dst) > 0:
				"mean loss"
				l = []
				for a,b in zip(l_src,l_dst):
					if a>b:
						loss = ((a-b)*100)/100.0
						l.append(loss)
				if len(l)>0:
					mean_loss = sum(l)/float(len(l))
				else:
					mean_loss = 0

				"last samples"
				a = l_src[len(l_src)-1]
				b = l_dst[len(l_dst)-1]
				if a > b:
					loss = ((a-b)*100)/100.0
				else:
					loss = 0
				return loss, mean_loss
			else:
				return 0,0

		max_workload = 0
		max_latency = 0
		max_latency_threshold = 0
		max_jitter = 0
		max_jitter_threshold = 0
		max_loss = 0
		max_loss_threshold = 0

		def __init__(self, dpid, p, macaddr, ip):
			self.dpid = dpid
			self.port = p
			self.macaddr = macaddr
			self.ipaddr = ip
			self.netw_tokens = self.powerToken()
			self.path_list = []
			self.workload = 0
			self.jitter = []
			self.is_sink = False
			self.loss = []


		def __repr__(self):
			return "Ip = {}\tdpid = {}\tport = {}".format(self.ipaddr, self.dpid, self.port)


		def __str__(self):
			return self.__repr__()


		def create_path (self, src, dst, p, is_active = False):
			src_dpid, src_port = src.dpid, src.port
			dst_dpid, dst_port = dst.dpid, dst.port

			p = Path(src_dpid, src_port, dst_dpid, dst_port, p)
			p.is_active = is_active

			self.path_list.append(p)

			global dirty
			dirty = True
			print "Setting flag to Dirty"
			return p


		def get_path(self, src_dpid, dst_dpid, src_port=None, dst_port=None):
			if src_port and dst_port:
				for p in self.path_list:
					if p.src_dpid == src_dpid and p.src_port == src_port:
						if p.dst_dpid == dst_dpid and p.dst_port == dst_port:
							return p
			else:
				for p in self.path_list:
					if p.src_dpid == src_dpid and p.dst_dpid == dst_dpid:
						return p


		def remove_path(self, src_dpid, dst_dpid, src_port=None, dst_port=None):
			if src_port and dst_port:
				path = self.get_path(src_dpid, dst_dpid, src_port, dst_port)
			else:
				path = self.get_path(src_dpid, dst_dpid)
			if path:
				self.path_list.remove(path)

				global dirty
				dirty = True
				return True
			else:
				return False


		def remove_path(self, path):
			if path in self.path_list:
				self.path_list.remove(path)

				global dirty
				dirty = True
				return True
			else:
				return False


		def set_netw_tokens(self, ntokens, nrenewals):
			assert ntokens > 0
			self.netw_tokens.tokens = ntokens
			self.netw_tokens.predefined_tokens = ntokens
			self.netw_tokens.nrenewals = nrenewals
			self.netw_tokens.threshold = ntokens * 0.2

			update_user_tokens(self.macaddr, ntokens, nrenewals, ntokens * 0.2)


		def calc_jitter(self, latency):
			self.jitter.append(latency)
			if len(self.jitter) > 1:
				return abs(self.jitter[len(self.jitter)-2] - self.jitter[len(self.jitter)-1])
			else:
				return 0.0


		def update_tokens(self, cons):
			if self.is_sink:
				return
			if self.netw_tokens.predefined_tokens == 0:
				return
			if self.netw_tokens.tokens >= cons:
				if self.netw_tokens.tokens < self.netw_tokens.threshold:
					#print self.ipaddr, "ENERGY THRESHOLD REACHED --> Running out of power, check usage policy"
					pass
				self.netw_tokens.tokens = self.netw_tokens.tokens - cons
				update_user_tokens(self.macaddr, self.netw_tokens.tokens, self.netw_tokens.nrenewals, self.netw_tokens.threshold)
			else:
				#print self.ipaddr, "MAX ENERGY REACHED --> out of power, check renewal policy"
				if self.netw_tokens.nrenewals > 0:
					self.netw_tokens.nrenewals = self.netw_tokens.nrenewals - 1
					self.netw_tokens.tokens = self.netw_tokens.predefined_tokens
					update_user_tokens(self.macaddr, self.netw_tokens.tokens, self.netw_tokens.nrenewals, self.netw_tokens.threshold)
				else:
					self.netw_tokens.decrease_rate = True


	class Node(object):

		CHASSIS = 200.0
		INTERFACE = 50.0/3.0
		ALR_1 = .85
		DEVICE_SLEEP = 120.0
		tOn = .11
		LINK_CAPACITY = 1000.0

		link = defaultdict(lambda:defaultdict(lambda:None))
		adjacency = defaultdict(lambda:defaultdict(lambda:None))


		def __init__(self, event):
			self.event = event
			self.connection = event.connection
			self.id = event.connection.dpid
			self.consumption = []

			self.port_workload = {}
			self.aux_workload = {}


		def set_workload(self, port, w):
			try:
				wl = self.port_workload[port]
				self.port_workload[port] = w + wl
			except:
				self.port_workload[port] = w

			self.aux_workload = self.port_workload


		def get_workload(self):
			return sum(self.port_workload.itervalues())


		def get_port_workload(self, port):
			try:
				return self.port_workload[port]
			except:
				return 0


		def reset_port_workload(self):
			self.port_workload = self.port_workload.fromkeys(self.port_workload, 0)


		def get_consumption(self, w = None):
			PORTS = 0
			if not w:
				w = self.get_workload()
			def baseline_consumption(wl):
				aux = 0
				for wl in self.port_workload.itervalues():
					aux += self.INTERFACE * wl
				return self.CHASSIS + aux
			if w < MIN_WORKLOAD:
				consumption = self.DEVICE_SLEEP
			elif w <= SC_THRESHOLD:
				for port, wl in self.port_workload.iteritems():
					PORTS += self.INTERFACE * wl * self.ALR_1
				consumption = (self.DEVICE_SLEEP * self.tOn) + (self.CHASSIS + PORTS * self.tOn)
			else:
				for port, wl in self.port_workload.iteritems():
					if wl > 0 and wl <= ALR_1_THRESHOLD:
						PORTS += self.INTERFACE * wl * self.ALR_1
					elif wl > ALR_1_THRESHOLD:
						PORTS += self.INTERFACE * wl
				consumption = self.CHASSIS + PORTS

			baseline = to_kw(baseline_consumption(w))
			proportional = to_kw(consumption)

			self.consumption.append((proportional,baseline, 1200))
			return to_kw(consumption),baseline, 1200


		def get_node_out_port(self, dpid, dst_dpid):
			"""
			Gets the out port for a given node to its destination.
			Args:
				dpid: node dpid.
				dst: node destination dpid:
			Returns:
				the out port for the node dpid to dst_dpid link.
			"""
			return self.adjacency[dpid][dst_dpid]


	def get_node_out_port(self, dpid, dst_dpid):
		"""
		Gets the out port for a given node to its destination.
		Args:
			dpid: node dpid.
			dst: node destination dpid:
		Returns:
			the out port for the node dpid to dst_dpid link.
		"""
		return self.get_node(dpid).get_node_out_port(dpid, dst_dpid)


	def get_node(self, dpid):
		for node in self.nodes:
			if node.id == dpid:
				return node


	def get_host(self, mac=None, ip=None, dpid=None, port=None):
		if dpid and port:
			for h in self.hosts:
				if h.dpid == dpid and h.port == port:
					return h
		if mac:
			for h in self.hosts:
				if h.macaddr == mac:
					return h
		elif ip:
			for h in self.hosts:
				if h.ipaddr == ip:
					return h


def to_kw(watts):
	return watts/1000.000
