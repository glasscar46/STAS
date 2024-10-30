import abc
from .dao_interface import IDAO
from .sample_interface import ISample


class ISampleSelector(metaclass=abc.ABCMeta):
    
    def __init__(self, dao:IDAO):
        self.dao = dao
    
    def select(self, sample_size: int = 100)->ISample:
        raise NotImplementedError
