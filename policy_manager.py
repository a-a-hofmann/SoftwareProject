from clock import Clock
from abc import ABCMeta, abstractmethod

class PolicyManager(object):
    """
    Abstract policy manager.
    A valid policy should have an apply() method in order to be used from the policy manager.
    """

    __metaclass__ = ABCMeta

    def __init__(self, policies = []):
		self.policies = [policy['policy'] for policy in policies]
		self.active_policies = [policy['policy'] for policy in policies if policy['active']]


    def add_policy(self, policy, is_active = False):
		self.policies.append(policy)
		if is_active:
			self.active_policies.append(policy)


    def remove_policy(self, policy):
		self.policies.remove(policy)


    @abstractmethod
    def apply_active_policies(self):
        """
		Iterates through all active policies and applies them in order.
		"""
        pass


    @abstractmethod
    def check_policies(self):
        """
		Checks which policies to keep active.
		"""
        pass
