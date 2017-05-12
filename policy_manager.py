from clock import Clock

class PolicyManager(object):

	def __init__(self, policies, clock = None):
		self.clock = clock if clock else Clock(19, 0, 0)
		self.policies = policies


	def toString(self):
		print "Time is {}".format(self.clock)