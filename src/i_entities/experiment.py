from datetime import datetime
from typing import Any
from .serializable import Serializable

class Experiment(Serializable):
    """
    Represents an experiment in a process.
    
    Attributes:
        current_iteration (Any): The ID or object representing the current iteration in the experiment.
        position (int): The position or step in the experiment process.
        status (str): The current status of the experiment (e.g., 'STARTED', 'COMPLETED', 'FAILED').
        create_time: The time the `Experiment` object was created.
    """

    def __init__(self, iteration_id: Any, position: int, status='STARTED'):
        """
        Initializes an instance of the Experiment class.

        Args:
            iteration_id (Any): The identifier for the current iteration. 
            position (int): The position of the iteration in the sequence of iterations.
            status (str, optional): The status of the experiment. Default is 'STARTED'.
        """
        self.current_iteration = iteration_id
        self.position = position
        self.status = status
        self.create_time = datetime.now()
