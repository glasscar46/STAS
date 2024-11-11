import abc
from typing import Any
from .serializable import Serializable
from .annotation_interface import IAnnotation

class ISample(Serializable, metaclass=abc.ABCMeta):
    """
    Abstract base class representing a sample in the annotation process.

    The `ISample` class is meant to be extended by specific sample types 
    (such as text samples or image samples). This class provides common 
    functionality for handling sample data, such as storing text, associating 
    annotations with the sample, and tracking whether the sample has been validated.
    """

    def __init__(self, text: str) -> None:
        """
        Initializes the sample with the given text.

        Args:
            text (str): The text content associated with the sample.
        """
        self.text = text
        self.labels: IAnnotation = None  # Holds the annotation(s) for this sample
        self.validated: bool = False     # Flag to indicate whether the sample has been validated
        self._id = None                  # Unique identifier for the sample (to be set later)

    @classmethod
    @abc.abstractmethod
    def get_annotation_class(cls) -> IAnnotation:
        """
        Returns the appropriate annotation class for the sample.

        This method must be implemented by subclasses to return the 
        annotation class that corresponds to the sample type (e.g., 
        SequenceLabelAnnotation, ClassificationAnnotation).

        Returns:
            IAnnotation: The annotation class associated with the sample type.
        
        Raises:
            NotImplementedError: If not implemented by the subclass.
        """
        raise NotImplementedError

    @classmethod
    def deserialize(cls, data: dict):
        """
        Deserializes a sample from a dictionary of data.

        This method is responsible for creating a new sample object from 
        serialized data, such as data retrieved from a database. It assigns 
        the sample's ID, text, validated flag, and associated labels.

        Args:
            data (dict): A dictionary containing the serialized data for the sample. 
                         Expected keys include '_id', 'text', 'validated', and 'labels'.
        
        Returns:
            ISample: An instance of the sample class, with the attributes set based on the provided data.
        """
        obj = cls.__new__(cls)  # Create a new instance without calling __init__
        obj._id = data.get('_id')
        obj.validated = data.get('validated', False)
        obj.text = data.get('text', '')
        # Deserialize the labels using the appropriate annotation class
        obj.labels = cls.get_annotation_class().deserialize(data.get('labels'))
        return obj
