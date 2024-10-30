from i_entities import ISample
from annotation import ClassificationAnnotation

class TextClassificationSample(ISample):
    """The base class for a class classification sample."""
    
    def __init__(self, text):
        super().__init__(text)
        self.labels: ClassificationAnnotation