import abc
from typing import Any
from .serializable import Serializable
from .annotation_interface import IAnnotation

class ISample(Serializable, metaclass=abc.ABCMeta):

    def __init__(self, text: str) -> None:
        self.text = text
        self.labels : IAnnotation = None
        self.validated: bool = False
        self.id = None

    # @property
    # def text(self) -> str:
    #     return self.text
    
    # @property
    # def id(self) -> str:
    #     return self.id
    
    # @property.setter
    # def id(self, id: Any):
    #     self.id = id
    
    # @property
    # def labels(self) -> IAnnotation:
    #     return self.labels

    # @labels.setter
    # def labels(self, label: IAnnotation):
    #     self.labels = label

    @classmethod
    def deserialize(cls, data: dict):
        obj = cls.__new__(cls)
        obj.id = data.get('id')
        obj.validated = data.get('validated', False)
        obj.text = data.get('text','')
        obj.labels = obj.labels.__class__.deserialize(data.get('labels'))
        return obj