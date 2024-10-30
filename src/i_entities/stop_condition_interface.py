import abc
from typing import Any

from i_entities import Iteration
from .dao_interface import IDAO

class IStopCondition(metaclass=abc.ABCMeta):
    """The base class for all stopping conditions of the iterative annotation condition"""

    def __init__(self, dao:IDAO, params: Any):
        self.dao = dao
        self.params = params
        
    @abc.abstractmethod
    def evaluate(self, iteration: Iteration)-> bool:
        raise NotImplementedError
