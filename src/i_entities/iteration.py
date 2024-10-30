from datetime import datetime
from typing import Any, List
from .serializable import Serializable

class Iteration(Serializable):

    def __init__(self, position: int, model_id: Any, sample_ids: List[Any]) -> None:
        self.id: Any = None
        self.position = position
        self.start_time: datetime = datetime.now()
        self.end_time: datetime = None
        self.model_id: Any = model_id
        self.sample_ids: List[Any] = sample_ids
        self.status: str = " INITIALIZED"

    @classmethod
    def deserialize(cls, data: dict):
        obj = cls.__new__(cls)
        obj.id = data.get('id')
        obj.position = data.get('position')
        obj.start_time = data.get('start_time')
        obj.end_time = data.get('end_time')
        obj.model_id = data.get('model_id')
        obj.sample_ids = data.get('sample_ids', [])
        obj.status = data.get('status') 
        return obj
