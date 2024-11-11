import abc
from typing import Any

from i_entities import Iteration
from .dao_interface import IDAO

class IStopCondition(metaclass=abc.ABCMeta):
    """
    Base class for stopping conditions used in the iterative annotation process.

    This class serves as the foundation for defining different stopping conditions 
    that can be applied to terminate the iterative process. Any specific 
    stopping condition must extend this class and implement the `evaluate` method.

    Attributes:
        dao (IDAO): The data access object used to interact with the database.
        params (Any): Parameters that can be used to configure the stopping condition.
    """

    def __init__(self, dao: IDAO, params: Any):
        """
        Initializes the stopping condition with the provided DAO and parameters.

        Args:
            dao (IDAO): The data access object used to interact with the database.
            params (Any): Configuration parameters for the stopping condition.
        """
        self.dao = dao
        self.params = params
        
    @abc.abstractmethod
    def evaluate(self, iteration: Iteration) -> bool:
        """
        Evaluates the stopping condition based on the current iteration.

        This method must be implemented in subclasses to define the logic for 
        determining whether the iterative process should stop or continue.

        Args:
            iteration (Iteration): The current iteration of the annotation process.

        Returns:
            bool: True if the stopping condition is met (i.e., the process should stop),
                  False if the process should continue.
        """
        raise NotImplementedError
