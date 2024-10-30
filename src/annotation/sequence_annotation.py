from i_entities import IAnnotation
from typing import Any, List, Tuple

class SequenceLabelAnnotation(IAnnotation):
    """Base class of  labels for sequence to sequence tasks."""
    
    def __init__(self, sample_id: Any, labels: List[Tuple[int, int, str]], annotator_id: Any = None, iteration_id: Any = None, is_valid: bool = False):
        """
        SequenceLabelAnnotation holds a list of labels where each label is a tuple of
        (start_index, end_index, label)
        """
        super().__init__(sample_id, labels, annotator_id, iteration_id, is_valid)
        self.label: List[Tuple[int, int, str]]
    
    @classmethod
    def get_annotation_name(cls) -> str:
        return "sequence_labeling"
    
    def get_value(self) -> List[Tuple[int, int, str]]:
        """Returns the list of labels (spans) in the form of (start_index, end_index, label)."""
        return self.label