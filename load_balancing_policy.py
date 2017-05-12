from info_manager import *
from fbcontroller import *
from path import Path

class LoadBalancingPolicy(object):

	_CONSUMPTION_THRESHOLD = 5
	_LB_THRESHOLD = 1


	def __init__(self, fbcontroller, info_manager):
		self.info_manager = info_manager
		self.fbcontroller = fbcontroller


	@property
	def CONSUMPTION_THRESHOLD(self):
		return self._CONSUMPTION_THRESHOLD


	@CONSUMPTION_THRESHOLD.setter
	def CONSUMPTION_THRESHOLD(self, new_limit):
		assert new_limit > 0
		self._CONSUMPTION_THRESHOLD = new_limit


	@property
	def LB_THRESHOLD(self):
		return self._LB_THRESHOLD


	@LB_THRESHOLD.setter
	def LB_THRESHOLD(self, new_limit):
		assert new_limit > 0
		self._LB_THRESHOLD = new_limit


	def apply(self):
		path_host_map = self.info_manager.get_active_path_hosts_dict()
		for path in path_host_map:
			host_list = path_host_map[path]
			if host_list and len(host_list) > 1:
				self.check_if_should_split(path, host_list)


	def check_if_should_split(self, path, host_pairs):
		print "Check if should split ({}, {}):\t{}".format(path[0], path[-1], path)
		overloaded_nodes = self.check_nodes_in_path_for_loadbalancing(path=path)
		print "Overloaded nodes {}".format(overloaded_nodes)
		if overloaded_nodes:
			"Split list of hosts into two, one half will use a new path."
			new_path = self.get_path_for_load_balancing(path[0], path[-1], path, overloaded_nodes)

			if new_path:
				n_hosts = len(host_pairs)
				second_half_hosts = host_pairs[n_hosts/2:]

				print "Splitting traffic from {} to {}".format(path, new_path)
				for src, dst in second_half_hosts:
					self.fbcontroller.modify_path_rules(new_path, src, dst, is_split=True)
					pathObj = Path.of(src, dst, new_path, is_active=True)
					if not pathObj in src.path_list:
						src.path_list.append(pathObj)


					self.info_manager.path_table.put_path(src=src.dpid, dst=dst.dpid, path=pathObj)

					self.info_manager.path_table.set_path_active(src.dpid, dst.dpid, Path.of(src, dst, list(path)), False) # Set old path as inactive
			else:
				print "No new path available!"

	def get_path_for_load_balancing(self, src, dst, current_path, overloaded_nodes):
		"""
		Gets a new path from src to dst, taking node workload into account.
		Args:
			src: Source node dpid.
			dst: Destination node dpid.
			current_path: Current path as Path obj.
			overloaded_nodes: which nodes are overloaded in the current path.
		Returns:
		 	candidate: new path or None if no path was found.
		"""
		all_paths = self.info_manager.all_paths(self.fbcontroller.G, src_dpid=src, dst_dpid=dst)
		print "Current path:\t{}".format(current_path)
		all_paths.remove(list(current_path))
		print "All paths:\t{}".format(all_paths)

		current_path_consumption = sum(self.info_manager.compute_path_information(current_path)[0].itervalues()) #self.compute_consumption(current_path)

		candidates = []
		for candidate in all_paths:
			overloaded = self.check_nodes_in_path_for_loadbalancing(path=candidate)

			if not overloaded and not any(item[0] in candidate for item in overloaded_nodes):
				"Choose as candidate only if it isn't overloaded as well."
				candidate_path_consumption = self.compute_consumption(candidate) #sum(info_manager.compute_path_information(candidate)[0].itervalues())
				if current_path_consumption + candidate_path_consumption < self._CONSUMPTION_THRESHOLD:
					candidates.append(candidate)

		return candidates[0] if candidates else None


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
			workloads = self.info_manager.compute_path_information(path)[1]

		overloaded_nodes = []
		for node_id, node_workload in workloads.iteritems():
			if node_workload > self._LB_THRESHOLD:
				overloaded_nodes.append((node_id, node_workload))

		if path:
			src_node, dst_node = path[0], path[-1]
			overloaded_nodes = [overloaded for overloaded in overloaded_nodes if overloaded[0] != src_node and overloaded[0] != dst_node]
		return overloaded_nodes


	def compute_consumption(self, path):
		return sum(self.info_manager.compute_path_information(path)[0].itervalues())
