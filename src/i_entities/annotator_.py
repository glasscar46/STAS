from typing import Any
from .serializable import Serializable

class Annotator(Serializable):

    def __init__(self, email: str, password: str, id: Any = None) -> None:
        self.id = id
        self._email = email
        self._password = password
