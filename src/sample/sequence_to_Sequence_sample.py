from i_entities import ISample
from annotation import SequenceLabelAnnotation

class SequenceToSequenceSample(ISample):
    """The base class for a sequence to sequence sample."""
    
    def __init__(self, text):
        super().__init__(text)
        self.labels: SequenceLabelAnnotation