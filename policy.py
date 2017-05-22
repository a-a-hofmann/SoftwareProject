from abc import ABCMeta, abstractmethod

class Policy(object):
    """
    Abstract policy.
    """
    
    __metaclass__ = ABCMeta

    def __init__(self):
        pass


    @abstractmethod
    def apply(self):
        pass
