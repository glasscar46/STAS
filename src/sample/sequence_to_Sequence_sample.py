from typing import Type
from i_entities import ISample
from annotation import SequenceLabelAnnotation

class SequenceToSequenceSample(ISample):
    """
    A sample used in a sequence-to-sequence annotation task.

    This class extends the base `ISample` class and represents a sample that is used in sequence-to-sequence
    tasks, where each input sequence is annotated with corresponding labels that also form a sequence (e.g., 
    named entity recognition or part-of-speech tagging).

    Attributes:
        labels (SequenceLabelAnnotation): The annotation object that contains the sequence label(s) for the text.
    """
    
    def __init__(self, text: str) -> None:
        """
        Initializes a new sequence-to-sequence sample with the given text.

        Args:
            text (str): The input text that needs to be annotated in a sequence-to-sequence task.
        """
        super().__init__(text)
        self.labels: SequenceLabelAnnotation

    @classmethod
    def get_annotation_class(cls) -> SequenceLabelAnnotation:
        """
        Returns the annotation class that should be used for this sample type.

        This method returns the `SequenceLabelAnnotation` class, indicating that this sample type is annotated 
        with sequence labels for each token or sequence element in the text.

        Returns:
            SequenceLabelAnnotation: The class that defines the annotation for sequence-to-sequence tasks.
        """
        return SequenceLabelAnnotation
