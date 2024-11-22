from i_entities import IAnnotation
from typing import Any, List, Tuple

class SequenceLabelAnnotation(IAnnotation):
    """
    Base class for labels used in sequence-to-sequence tasks.

    This class represents annotations for sequence labeling tasks where each label corresponds
    to a span of text. The label itself is a tuple that contains the start and end indices of 
    the span, along with the label that classifies the span of text. This is typical in sequence
    labeling tasks such as named entity recognition (NER), part-of-speech tagging, etc.

    Attributes:
        sample_id (Any): The ID of the sample being annotated.
        label (List[Tuple[int, int, str]]): A list of tuples where each tuple contains:
            - `start_index` (int): The start index of the labeled span in the text.
            - `end_index` (int): The end index of the labeled span.
            - `label` (str): The label assigned to the span (e.g., "PERSON", "LOCATION").
        annotator_id (Any, optional): The ID of the annotator who made the annotation.
        iteration_id (Any, optional): The ID of the iteration in which the annotation was made.
        is_valid (bool): A boolean flag indicating whether the annotation is valid or not.

    Methods:
        get_annotation_name() -> str:
            Returns the name of the annotation type, which is "sequence_labeling" for this class.

        get_value() -> List[Tuple[int, int, str]]:
            Returns the list of labels, where each label is represented as a tuple of 
            (start_index, end_index, label).
    """
    
    def __init__(self, sample_id: Any, labels: List[Tuple[int, int, str]], annotator_id: Any = None, iteration_id: Any = None, is_valid: bool = None):
        """
        Initializes a SequenceLabelAnnotation object with the given parameters.

        Args:
            sample_id (Any): The ID of the sample being annotated.
            labels (List[Tuple[int, int, str]]): A list of labels, each represented as a tuple.
                                                 Each tuple contains:
                                                 - `start_index` (int): The start index of the span.
                                                 - `end_index` (int): The end index of the span.
                                                 - `label` (str): The label for the span (e.g., "PERSON").
            annotator_id (Any, optional): The ID of the annotator. Defaults to None.
            iteration_id (Any, optional): The ID of the iteration in which the annotation was made. Defaults to None.
            is_valid (bool): A flag indicating whether the annotation is valid. Defaults to None.
        """
        super().__init__(sample_id, labels, annotator_id, iteration_id, is_valid)
        self.label: List[Tuple[int, int, str]] = labels
    
    @classmethod
    def get_annotation_name(cls) -> str:
        """
        Returns the name of the annotation type for sequence labeling tasks.

        Returns:
            str: The name of the annotation type, which is "sequence_labeling".
        """
        return "sequence_labeling"
    
    def get_value(self) -> List[Tuple[int, int, str]]:
        """
        Returns the list of labels (spans) for the sequence labeling task.

        Each label is represented as a tuple of (start_index, end_index, label), where:
            - `start_index` is the start index of the span.
            - `end_index` is the end index of the span.
            - `label` is the label assigned to the span.

        Returns:
            List[Tuple[int, int, str]]: A list of labeled spans, each represented as a tuple.
        """
        return self.label
