from info_manager import *
from fbcontroller import *

class MergingPolicy(object):

	_PATH_MERGING_THRESHOLD = 3
	_CONSUMPTION_THRESHOLD = 5

	def __init__(self, controller, info_manager):
		self.info_manager = info_manager
		self.controller = controller


	@property
	def PATH_MERGING_THRESHOLD(self):
		return self._PATH_MERGING_THRESHOLD


	@PATH_MERGING_THRESHOLD.setter
	def PATH_MERGING_THRESHOLD(self, new_limit):
		assert new_limit > 0
		self._PATH_MERGING_THRESHOLD = new_limit


	@property
	def CONSUMPTION_THRESHOLD(self):
		return self._CONSUMPTION_THRESHOLD


	@CONSUMPTION_THRESHOLD.setter
	def CONSUMPTION_THRESHOLD(self, new_limit):
		assert new_limit > 0
		self._CONSUMPTION_THRESHOLD = new_limit


	def apply(self):
		all_active_paths = self.info_manager.get_all_active_paths()
		for src in all_active_paths:
			for dst in all_active_paths[src]:
				src_dst_paths = all_active_paths[src][dst]
				if src_dst_paths and self.should_merge(src_dst_paths):
						"There are multiple paths between the same src and dst active. Check if can merge"
						self.check_if_can_merge(src_dst_paths)


	def check_if_can_merge(self, paths):
		"""
			Checks if the given paths can be merged into one path or fewer paths.
			Merging should only happen if it doesn't lead to the overloading of a path.
			Args:
				paths: list of path objects.
		"""
		"Just use the first path in paths"
		new_path = list(paths)[0]
		new_path.total_consumption = self.compute_consumption(new_path)

		"If any other path is already using new_path, do not consider for merging"
		paths = [path for path in paths if path.path != new_path.path]
		paths = paths[:self._PATH_MERGING_THRESHOLD]

		print "Paths considered for merging:"
		for path in paths:
			print "\t{}".format(path.path)

		print "Merging traffic into one path:\t{}".format(new_path)
		for path in paths:
			if path != new_path and path.path != new_path.path:
				path_consumption = self.compute_consumption(path)

				if self.can_merge(path_consumption, new_path.total_consumption):
					new_path.total_consumption += path_consumption
					"Extract src and dst info from all paths"
					src_host, dst_host = self.info_manager.get_hosts_from_path(path)
					print "Modifying rules for ({}, {}):\told path={}\tnew path={}".format(src_host, dst_host, path, new_path)
					self.controller.modify_path_rules(new_path.path, src_host, dst_host, is_split=False)
					path.is_active = False
					if not new_path in src_host.path_list:
						src_host.create_path(src_host, dst_host, new_path.path, is_active = True)

		print "\n------------------------------\n"


	def should_merge(self, paths):
		"""
			Returns true if there are multiple DISTINCT paths between the same src and dst.
			For example if paths contains [Path([1, 2, 3], src1, dst), Path([1, 2, 3], src2, dst)],
			this method will return False.
		"""
		return len(paths) > 1 and len(set(tuple(path.path) for path in paths)) > 1


	def can_merge(self, path1_consumption, path2_consumption):
		"""
			Checks wheter merging paths together would mean going over the
			consumption threshold.
			Args:
				path1_consumption: consumption.
				path2_consumption: consumption.
			Returns:
				True iff sum of consumption is less then CONSUMPTION_THRESHOLD.
		"""
		return path1_consumption + path2_consumption > self.CONSUMPTION_THRESHOLD


	def compute_consumption(self, path):
		return sum(self.info_manager.compute_path_information(path.path)[0].itervalues())
