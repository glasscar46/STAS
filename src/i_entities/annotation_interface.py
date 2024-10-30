import abc
from typing import Any
from .serializable import Serializable

class IAnnotation(Serializable, metaclass=abc.ABCMeta):
    """Base Class for Annotations.
      All annotations must extend this class.
    """
    
    def __init__(self, sample_id: Any, label: Any,  annotator_id: Any = None, iteration_id: Any = None, is_valid: bool = False) -> None:
        self.id: Any = None
        self.sample_id = sample_id
        self.is_valid: bool = is_valid
        self.iteration = iteration_id
        self.annotator = annotator_id
        self.name = self.__class__.get_annotation_name()
        self.label = label
        
    

    @classmethod
    def deserialize(cls, data: dict| Any):
        obj = cls.__new__(cls)
        if isinstance(data, dict):
            obj.is_valid = data.get('is_valid', False)
            obj.is_valid = data.get('validated', False)
            obj.iteration = data.get('iteration')
            obj.annotator = data.get('annotator')
            obj.label = data.get('label')
        else:
            obj.label = data
        return obj

    @classmethod
    def  get_annotation_name(cls) -> str:
        raise NotImplementedError
    
    def get_value(self) -> Any:
        """This method returns the value of the annotation."""
        return self.label