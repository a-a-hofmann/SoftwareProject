from clock import Clock
from MergingPolicy import MergingPolicy
from load_balancing_policy import LoadBalancingPolicy

class PolicyManager(object):

	def __init__(self, policies = [], clock = None):
		self.clock = clock if clock else Clock(21, 50, 0)
		self.policies = [policy['policy'] for policy in policies]
		self.active_policies = [policy['policy'] for policy in policies if policy['active']]


	def add_policy(self, policy, is_active = False):
		self.policies.append(policy)
		if is_active:
			self.active_policies.append(policy)


	def remove_policy(self, policy):
		self.policies.remove(policy)


	def print_time(self):
		print "Time is {}".format(self.clock)


	def apply_policy(self):
		if not self.active_policies:
			print "WARN: No active policy!"
			return

		"If has policies, check if we need to switch policies."
		self.check_policies()

		"Apply all active policies."
		for policy in self.active_policies:
			try:
				policy.apply()
			except AttributeError:
				print "{} is not a policy! Removing from policies!".format(policy)
				assert self.active_policies.remove(policy)
				assert self.policies.remove(policy)


	def check_policies(self):
		if self.clock.isEnergySavingsTimeForDemo():
			print "Running in energy savings mode."
			self.active_policies = [policy for policy in self.policies if isinstance(policy, MergingPolicy)]
			assert len(self.active_policies) == 1
		else:
			print "Running in load balancing mode."
			self.active_policies = [policy for policy in self.policies if isinstance(policy, LoadBalancingPolicy)]
			assert len(self.active_policies) == 1
