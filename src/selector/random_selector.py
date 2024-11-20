from i_entities import ISampleSelector
from random import Random

class RandomSampleSelector(ISampleSelector):
    """
    A sample selector that selects samples randomly.

    This class implements the `ISampleSelector` interface and selects a given number of 
    samples at random from the pool of pending samples. It uses Python's built-in `random.choices()`
    method to perform the random selection.

    Attributes:
        dao (IDAO): The data access object used to retrieve the pending samples from the data store.

    Methods:
        select(sample_size: int): Selects a specified number of samples randomly from the pending samples.
    """
    
    def select(self, sample_size: int = 100):
        """
        Selects a specified number of samples randomly.

        This method retrieves the list of pending samples from the data access object and selects
        a given number of samples at random using the `random.choices()` method. It returns the
        selected samples.

        Args:
            sample_size (int): The number of samples to select. Defaults to 100.

        Returns:
            list: A list of randomly selected samples from the pool of pending samples.
        """
        samples = self.dao.getPendingSamples()
        if len(samples)<= sample_size:
            return samples
        return Random().choices(samples, k=sample_size)
