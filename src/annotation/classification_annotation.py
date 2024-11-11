from enum import Enum
from i_entities import IAnnotation

class ClassificationAnnotation(IAnnotation):
    """
    The base class for text classification annotations.

    This class is used to annotate text samples with a classification label.
    It extends the `IAnnotation` class and provides additional functionality
    for handling annotations specific to text classification tasks, where 
    each sample is assigned a label from a predefined set of categories.

    Attributes:
        sample_id (Any): The ID of the sample being annotated.
        label (Enum): The classification label assigned to the sample.
        annotator_id (Any, optional): The ID of the annotator who made the annotation.
        iteration_id (Any, optional): The ID of the iteration in which the annotation was made.
        is_valid (bool): Indicates whether the annotation is valid or not.

    Methods:
        get_annotation_name() -> str:
            Returns the name of the annotation type, which is "Classification" for this class.
    """

    def __init__(self, sample_id, label: Enum, annotator_id=None, iteration_id=None, is_valid=False):
        """
        Initializes a ClassificationAnnotation object with the given parameters.

        Args:
            sample_id (Any): The ID of the sample being annotated.
            label (Enum): The classification label assigned to the sample.
            annotator_id (Any, optional): The ID of the annotator who made the annotation. Defaults to None.
            iteration_id (Any, optional): The ID of the iteration in which the annotation was made. Defaults to None.
            is_valid (bool): Indicates whether the annotation is valid or not. Defaults to False.
        """
        super().__init__(sample_id, label, annotator_id, iteration_id, is_valid)

    @classmethod
    def get_annotation_name(cls) -> str:
        """
        Returns the name of the annotation type for classification tasks.
        This method can be overwritten by subclasses to give custom names.

        Returns:
            str: The name of the annotation type".
        """
        return "Classification"
