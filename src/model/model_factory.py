from typing import Type
from i_entities import IModel
from utils.config_loader import ConfigLoader
from .ner_model import NERModel


class ModelFactory:
    """
    A factory class that creates model instances based on configuration settings.

    The `ModelFactory` class allows dynamic creation of model objects. This design pattern abstracts the 
    model creation logic and allows for easier extension if additional model types are added in the future.

    Attributes:
        config (ConfigLoader): The configuration loader that provides settings for selecting the model class.
        models (dict): A dictionary that maps model class names to their corresponding class types.
    """
    
    def __init__(self, config: ConfigLoader):
        """
        Initializes the ModelFactory with a configuration loader.

        Args:
            config (ConfigLoader): The configuration loader that is used to retrieve configuration settings.
        """
        self.config = config
        # A dictionary that maps model class names to their corresponding model classes
        self.models = {
            NERModel.__name__: NERModel
        }
    
    def get_model(self) -> Type[IModel]:
        """
        Retrieves the model class based on the configuration setting.

        This method checks the configuration (`modelName`) to determine which model class to return.
        If the `modelName` is not configured or invalid, it raises a ValueError.

        Returns:
            Type[IModel]: The class type of the model (either `SequenceToSequenceModel` or `TextClassificationModel`).

        Raises:
            ValueError: If `modelName` is not configured or is not a valid option in the `models` dictionary.
        """
        if not self.config.get('modelName'):
            raise ValueError('modelName is not configured')
        
        if self.config.get('modelName') not in self.models:
            raise ValueError(f"{self.config.get('modelName')} is not a valid model name")
        
        # Return the class corresponding to the configured model class name
        return self.models.get(self.config.get('modelName'))
