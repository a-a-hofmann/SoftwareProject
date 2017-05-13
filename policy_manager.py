from clock import Clock
from merging_policy import MergingPolicy
from load_balancing_policy import LoadBalancingPolicy
import traceback


class PolicyManager(object):
	"""
    Manages policies for green traffic engineering. 
    A valid policy should have a apply() method in order to be used from the policy manager.
    """

	def __init__(self, policies = [], clock = None):
		self.clock = clock if clock else Clock(20, 0, 0)
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


	def apply_active_policies(self):
		"""
		Iterates through all active policies and applies them in order.
		"""
		if not self.active_policies:
			print "WARN: No active policy!"
			return

		"If has policies, check if we need to switch policies."
		self.check_policies()

		"Apply all active policies."
		for policy in self.active_policies:
			try:
				policy.apply()
			except AttributeError as e:
				print "{} is not a policy! Removing from policies!".format(policy)
				print "Exception:\n{}".format(repr(e))
				print traceback.format_exc()
				assert self.active_policies.remove(policy)
				assert self.policies.remove(policy)


	def check_policies(self):
		"""
		Checks which policies to keep active.
		For more complex policies/modeling should be changed.
		"""
		if self.clock.isEnergySavingsTimeForDemo():
			print "Running in energy savings mode."
			self.active_policies = [policy for policy in self.policies if isinstance(policy, MergingPolicy)]
		else:
			print "Running in load balancing mode."
			self.active_policies = [policy for policy in self.policies if isinstance(policy, LoadBalancingPolicy)]
		
		assert len(self.active_policies) == 1
