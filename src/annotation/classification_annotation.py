from enum import Enum
from i_entities import IAnnotation

class ClassificationAnnotation(IAnnotation):
    """The base class for text classification annotations."""
    
    def __init__(self, sample_id, label: Enum, annotator_id = None, iteration_id = None, is_valid = False):
        super().__init__(sample_id, label, annotator_id, iteration_id, is_valid)