from clock import Clock
from merging_policy import MergingPolicy
from load_balancing_policy import LoadBalancingPolicy
import traceback
from policy_manager import PolicyManager


class TimeBasedPolicyManager(PolicyManager):
	"""
    Manages policies based on the time of day.
    """

	def __init__(self, policies = [], clock = None):
		PolicyManager.__init__(self, policies)
		self.clock = clock if clock else Clock(20, 0, 0)


	def print_time(self):
		print "Time is {}".format(self.clock)


	def apply_active_policies(self):
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
		if self.clock.isEnergySavingsTime():
			print "Running in energy savings mode."
			self.active_policies = [policy for policy in self.policies if isinstance(policy, MergingPolicy)]
		else:
			print "Running in load balancing mode."
			self.active_policies = [policy for policy in self.policies if isinstance(policy, LoadBalancingPolicy)]

		assert len(self.active_policies) == 1
