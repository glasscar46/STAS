from typing import Any
from .serializable import Serializable

class Annotator(Serializable):

    def __init__(self, email: str, password: str, id: Any = None) -> None:
        self._id = id
        self.email = email
        self.password = password
