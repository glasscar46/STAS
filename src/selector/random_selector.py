from i_entities import ISampleSelector
from random import Random

class RandomSampleSelector(ISampleSelector):
    """A sample selector that selects samples randomly"""
    
    def select(self, sample_size = 100):
        samples = self.dao.getPendingSamples()
        return Random().choices(samples, k=sample_size)