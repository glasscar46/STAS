from datetime import datetime
from typing import Any, List
from .serializable import Serializable
from .iteration_state import IterationState

class Iteration(Serializable):
    """
    Represents an iteration in the annotation process. An iteration involves selecting a set of samples, 
    fine-tuning a model, generating annotations for those samples, and tracking the start and end times 
    of the iteration process. This class also allows deserialization of an iteration object from a dictionary.
    """

    def __init__(self, position: int, model_id: Any, sample_ids: List[Any]) -> None:
        """
        Initializes an Iteration object with the specified position, model ID, and list of sample IDs.

        Args:
            position (int): The position of the iteration (e.g., 1 for the first iteration, 2 for the second, etc.).
            model_id (Any): The ID of the model used during this iteration.
            sample_ids (List[Any]): A list of IDs for the samples involved in this iteration.
        """
        self._id: Any = None  # The unique identifier of the iteration (set when the iteration is saved).
        self.position = position  # The iteration's position in the process.
        self.start_time: datetime = datetime.now()  # The timestamp when the iteration started.
        self.end_time: datetime = None  # The timestamp when the iteration ended (set after completion).
        self.model_id: Any = model_id  # The ID of the model used in this iteration.
        self.sample_ids: List[Any] = sample_ids  # The list of sample IDs processed during this iteration.
        self.status = IterationState.INITIALIZED  # The status of the iteration.

    @classmethod
    def deserialize(cls, data: dict):
        """
        Deserializes a dictionary into an Iteration object. This is used to convert stored data into an 
        Iteration object that can be used in the application.

        Args:
            data (dict): A dictionary containing the serialized data for an Iteration object.

        Returns:
            Iteration: A new Iteration object created from the dictionary data.
        """
        if not data:
            return None
        obj = cls.__new__(cls)  # Create an empty instance without calling __init__.
        obj._id = data.get('_id')  # Set the ID of the iteration.
        obj.position = data.get('position')  # Set the position of the iteration.
        obj.start_time = data.get('start_time')  # Set the start time of the iteration.
        obj.end_time = data.get('end_time')  # Set the end time of the iteration.
        obj.model_id = data.get('model_id')  # Set the model ID used in the iteration.
        obj.sample_ids = data.get('sample_ids', [])  # Set the list of sample IDs.
        obj.status = data.get('status')  # Set the status of the iteration.
        return obj
