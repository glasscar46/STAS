import abc
import copy
from typing import Any, List
from .sample_interface import ISample

class IModel(metaclass=abc.ABCMeta):
    """ A base class for a model to be used for Annotation."""

    def __init__(self) -> None:
        self.id = None
    
    def copy(self):
        new_object = copy.deepcopy(self)
        new_object.id = None
        return new_object

    @abc.abstractmethod
    def finetune(self, samples: List[ISample]):
        "Finetune the model on the given samples."
        raise NotImplementedError
    
    @abc.abstractmethod
    def generateAnnotation(self, samples: List[ISample]) -> List[ISample]:
        """Generate Annotations for the samples given."""
        raise NotImplementedError


    