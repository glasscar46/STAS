from typing import Type
from i_entities import ISample
from utils.config_loader import ConfigLoader
from .sequence_to_Sequence_sample import SequenceToSequenceSample
from .TextClassificationSample import TextClassificationSample

class SampleFactory:
    """
    A factory class that creates sample instances based on configuration settings.

    The `SampleFactory` class allows dynamic creation of sample objects, such as `SequenceToSequenceSample`
    or `TextClassificationSample`, based on the configuration provided. This design pattern abstracts the 
    sample creation logic and allows for easier extension if additional sample types are added in the future.

    Attributes:
        config (ConfigLoader): The configuration loader that provides settings for selecting the sample class.
        samples (dict): A dictionary that maps sample class names to their corresponding class types.
    """
    
    def __init__(self, config: ConfigLoader):
        """
        Initializes the SampleFactory with a configuration loader.

        Args:
            config (ConfigLoader): The configuration loader that is used to retrieve configuration settings.
        """
        self.config = config
        # A dictionary that maps sample class names to their corresponding sample classes
        self.samples = {
            SequenceToSequenceSample.__name__: SequenceToSequenceSample,
            TextClassificationSample.__name__: TextClassificationSample
        }
    
    def get_sample(self) -> Type[ISample]:
        """
        Retrieves the sample class based on the configuration setting.

        This method checks the configuration (`sampleClass`) to determine which sample class to return.
        If the `sampleClass` is not configured or invalid, it raises a ValueError.

        Returns:
            Type[ISample]: The class type of the sample (either `SequenceToSequenceSample` or `TextClassificationSample`).

        Raises:
            ValueError: If `sampleClass` is not configured or is not a valid option in the `samples` dictionary.
        """
        if not self.config.get('sampleClass'):
            raise ValueError('sampleClass is not configured')
        
        if self.config.get('sampleClass') not in self.samples:
            raise ValueError('sampleClass is not configured')
        
        # Return the class corresponding to the configured sample class name
        return self.samples.get(self.config.get('sampleClass'))
