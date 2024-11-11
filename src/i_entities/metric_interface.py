import abc
from typing import Any, List
from i_entities.sample_interface import ISample

class IMetric(metaclass=abc.ABCMeta):
    """
    The base class for evaluation metrics used to assess the quality or progress
    of the annotation process. 

    All evaluation metric classes should inherit from this class and implement the 
    `evaluate` method to define the specific evaluation logic for assessing the 
    annotations or the annotation process.
    """

    @classmethod
    @abc.abstractmethod
    def evaluate(self, samples: List[ISample]) -> Any:
        """
        Evaluates the annotation process based on the provided list of samples.
        
        This abstract method must be implemented by subclasses to define how the 
        annotation process is evaluated. Subclasses may use the annotations in the 
        samples to perform different types of evaluations such as checking accuracy, 
        consistency, or other metrics.
        
        Args:
            samples (List[ISample]): A list of annotated samples to evaluate. Each 
                                      sample should implement the `ISample` interface, 
                                      which provides access to the data and annotations.
        
        Returns:
            Any: The result of the evaluation, which may vary depending on the specific 
                 implementation of the metric. It could be a boolean, a score, or any 
                 other result that indicates how well the annotations meet the evaluation criteria.
        
        Raises:
            NotImplementedError: If the method is not implemented by a subclass.
        """
        raise NotImplementedError
