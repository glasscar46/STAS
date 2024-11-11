from typing import Type
from i_entities import ISampleSelector
from .random_selector import RandomSampleSelector
from utils.config_loader import ConfigLoader


class SelectorFactory:
    """
    A factory class to create sample selectors based on the provided configuration.

    This class is responsible for creating instances of sample selectors based on the configuration 
    passed during initialization. It supports different types of selectors, allowing the system to be 
    extended in the future with additional selection strategies.

    Attributes:
        config (ConfigLoader): The configuration loader that provides the necessary settings 
                               to select the appropriate sample selector.
        selector (dict): A dictionary mapping selector names to selector class types.

    Methods:
        get_selector() -> Type[ISampleSelector]: Returns the appropriate sample selector class 
                                                 based on the provided configuration.
    """
    
    def __init__(self, config: ConfigLoader):
        """
        Initializes the SelectorFactory with the provided configuration.

        Args:
            config (ConfigLoader): The configuration loader that contains settings for selecting 
                                    the sample selector.
        """
        self.config = config
        self.selector = {
            RandomSampleSelector.__name__: RandomSampleSelector
        }
    
    def get_selector(self) -> Type[ISampleSelector]:
        """
        Returns the appropriate sample selector class based on the configuration.

        This method reads the configuration to determine which sample selector to instantiate.
        If the configuration specifies a valid selector, it returns the corresponding class.
        If no selector is configured or the specified selector is invalid, it raises a ValueError.

        Returns:
            Type[ISampleSelector]: The class of the selected sample selector.

        Raises:
            ValueError: If no selector is configured or if the configured selector is not recognized.
        """
        if self.config.get('Selector'):
            selector = self.config.get('Selector')
            if selector not in self.selector:
                raise ValueError('Selector is not recognized by factory.')
            return self.selector.get(selector)
        else:
            raise ValueError('Selector configuration is missing')
