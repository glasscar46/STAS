from typing import Type
from i_entities import ISample
from utils.config_loader import ConfigLoader
from .sequence_to_Sequence_sample import SequenceToSequenceSample
from .TextClassificationSample import TextClassificationSample

class SampleFactory:
    
    def __init__(self, config: ConfigLoader):
        self.config = config
        self.samples = {
            SequenceToSequenceSample.__name__: SequenceToSequenceSample,
            TextClassificationSample.__name__: TextClassificationSample
        }
    
    def get_sample(self)->Type[ISample]:
        if not self.config.get('sampleClass'):
            raise ValueError('sampleClass is not configured')
        
        if self.config.get('sampleClass') not in self.samples:
            raise ValueError('sampleClass is not configured')
        
        return self.samples.get(self.config.get('sampleClass'))