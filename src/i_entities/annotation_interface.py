import abc
from typing import Any
from .serializable import Serializable

class IAnnotation(Serializable, metaclass=abc.ABCMeta):
    """
    Base Class for Annotations.
    All annotation types (e.g., sequence label annotations, classification annotations, etc.) 
    must extend this class. This class provides the fundamental structure and functionality 
    for storing and managing annotations within the system.
    """

    def __init__(self, sample_id: Any, label: Any, annotator_id: Any = None, iteration_id: Any = None, is_valid: bool = False) -> None:
        """
        Initializes an annotation object with the provided details.

        Args:
            sample_id (Any): The ID of the sample associated with this annotation.
            label (Any): The label or annotation value.
            annotator_id (Any, optional): The ID of the annotator who created this annotation. Defaults to None.
            iteration_id (Any, optional): The ID of the iteration in which this annotation was created. Defaults to None.
            is_valid (bool, optional): A flag indicating whether this annotation is valid. Defaults to False.
        """
        self._id: Any = None  # The unique identifier of the annotation (set when saved to the database).
        self.sample_id = sample_id  # The ID of the sample this annotation refers to.
        self.is_valid: bool = is_valid  # The validity flag for the annotation.
        self.iteration = iteration_id  # The ID of the iteration that generated this annotation.
        self.annotator = annotator_id  # The ID of the annotator who created the annotation.
        self.name = self.__class__.get_annotation_name()  # The name of the annotation type (e.g., SequenceLabelAnnotation).
        self.label = label  # The label (or value) for this annotation.

    @classmethod
    def deserialize(cls, data: dict | Any):
        """
        Deserializes a dictionary or a single value into an IAnnotation object. 
        If the input is a dictionary, it extracts the relevant fields to reconstruct the annotation object.
        
        Args:
            data (dict | Any): The serialized data to deserialize. This can either be a dictionary 
                               containing fields of an annotation or a direct label value.

        Returns:
            IAnnotation: An instance of the appropriate annotation class populated with the data.
        """
        obj = cls.__new__(cls)  # Create an empty instance of the class.
        
        # If the data is a dictionary, populate the fields of the annotation object.
        if isinstance(data, dict):
            obj._id = data.get('_id', None)
            obj.is_valid = data.get('is_valid', False)
            obj.iteration = data.get('iteration')
            obj.annotator = data.get('annotator')
            obj.label = data.get('label')
        else:
            # If the data is not a dictionary, assume it is the label itself.
            obj.label = data
        
        return obj

    @classmethod
    def get_annotation_name(cls) -> str:
        """
        Abstract method that should be implemented by subclasses to return the name of the annotation type.
        
        Returns:
            str: The name of the annotation type (e.g., "SequenceLabelAnnotation").
        
        Raises:
            NotImplementedError: If the method is not implemented by the subclass.
        """
        raise NotImplementedError

    def get_value(self) -> Any:
        """
        Returns the value (label) of the annotation.

        Returns:
            Any: The value of the annotation (e.g., a label or classification result).
        """
        return self.label
