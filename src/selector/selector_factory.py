from typing import Type
from i_entities import ISampleSelector
from .random_selector import RandomSampleSelector
from utils.config_loader import ConfigLoader


class SelectorFactory:
    
    
    def __init__(self, config: ConfigLoader):
        self.config = config
        self.selector = {
            RandomSampleSelector.__name__: RandomSampleSelector
        }
    
    def get_selector(self)-> Type[ISampleSelector]:
        if self.config.get('Selector'):
            selector = self.config.get('Selector')
            if selector not in self.selector:
                raise ValueError('Selector is not recognized by factory.')
            return self.selector.get(selector)
        else:
            raise ValueError('Selector configuration is missing')