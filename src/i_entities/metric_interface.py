import abc
from typing import List

from i_entities.sample_interface import ISample

class IMetric(metaclass=abc.ABCMeta):
    """The base class for evaluation metrics of the annotation process."""

    @classmethod
    @abc.abstractmethod
    def evaluate(self, samples: List[ISample])-> bool:
        raise NotImplementedError
