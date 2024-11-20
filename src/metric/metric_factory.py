from typing import List, Type
from i_entities import IMetric
from utils.config_loader import ConfigLoader

class MetricFactory:
    """
    A factory class that creates metric instances based on configuration settings.

    The `MetricFactory` class allows dynamic creation of metric objects. This design pattern abstracts the 
    metric creation logic and allows for easier extension if additional metric types are added in the future.

    Attributes:
        config (ConfigLoader): The configuration loader that provides settings for selecting the metric class.
        metrics (dict): A dictionary that maps metric class names to their corresponding class types.
    """
    
    def __init__(self, config: ConfigLoader):
        """
        Initializes the MetricFactory with a configuration loader.

        Args:
            config (ConfigLoader): The configuration loader that is used to retrieve configuration settings.
        """
        self.config = config
        # A dictionary that maps metric class names to their corresponding metric classes
        self.metrics = {
        }
    
    def get_metric(self) -> List[Type[IMetric]]:
        """
        Retrieves the metric class based on the configuration setting.

        This method checks the configuration (`metricClass`) to determine which metric class to return.
        If the `metricClass` is not configured or invalid, it raises a ValueError.

        Returns:
            List[Type[IMetric]]: A list of class type of the metrics.

        Raises:
            ValueError: If `metrics` is not configured or contains an invalid option in the `metrics` list.
        """
        if not self.config.get('metrics'):
            raise ValueError('metrics is not configured')

        def _get_metric(metric)-> IMetric:
            if self.config.get(metric) not in self.metrics:
                raise ValueError(f'"{metric}" is not known')
            return self.config.get(metric)
        
        # Return the class corresponding to the configured metric class name
        return [_get_metric(metric) for metric in self.config.get('metrics')]
