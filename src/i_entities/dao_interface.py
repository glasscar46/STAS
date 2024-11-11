import abc
from typing import Any, List
from .iteration import Iteration
from .model_interface import IModel
from .sample_interface import ISample
from .annotation_interface import IAnnotation
from .annotator_ import Annotator


class IDAO():
    
    def __init__(self, connection_string: str, database_name: str) -> None:
        self._connection_string = connection_string
        self.database_name = database_name
        self.connect()

    @property
    def connection_string(self):
        
        
        return self._connection_string

    @abc.abstractmethod
    def connect(self):
        raise NotImplementedError

    @abc.abstractmethod
    def saveSample(self, sample: ISample):
        raise NotImplementedError

    @abc.abstractmethod
    def saveSampleAnnotation(self, sample: ISample):
        raise NotImplementedError

    @abc.abstractmethod
    def saveSamples(self, samples: List[ISample]):
        raise NotImplementedError

    @abc.abstractmethod
    def updateAnnotation(self, sample: ISample):
        raise NotImplementedError
    
    @abc.abstractmethod
    def getSample(self, id: Any) -> ISample:
        raise NotImplementedError
    
    @abc.abstractmethod
    def getPendingSamples(self) -> List[ISample]:
        raise NotImplementedError
    
    @abc.abstractmethod
    def getPendingAnnotation(self, iteration_id: Any) -> List[ISample]:
        raise NotImplementedError

    @abc.abstractmethod
    def saveAnnotation(self, annotation: IAnnotation):
        raise NotImplementedError

    @abc.abstractmethod
    def saveAnnotations(self, annotations: List[IAnnotation]):
        raise NotImplementedError
    
    @abc.abstractmethod
    def saveAnnotator(self, annotator: Annotator):
        raise NotImplementedError

    @abc.abstractmethod
    def login(self, annotator: Annotator)-> Annotator:
        raise NotImplementedError

    @abc.abstractmethod
    def logout(self, annotator: Annotator):
        raise NotImplementedError
    
    @abc.abstractmethod
    def saveModel(self, model: IModel) -> Any:
        """Saves a model and returns its identifier"""
        raise NotImplementedError

    @abc.abstractmethod 
    def saveIteration(self, iteration: Iteration) -> Any:
        """Saves an Iteration and returns its identifier"""
        raise NotImplementedError

    @abc.abstractmethod 
    def updateIteration(self, iteration: Iteration) -> Any:
        """Updates an Iteration and returns the result of the update"""
        raise NotImplementedError

    @abc.abstractmethod 
    def getIteration(self, id: Any) -> Iteration:
        """Returns the Iteration with the given id."""
        raise NotImplementedError
    
    @abc.abstractmethod
    def getIterationEvals(self, iteration_id: Any)-> List[IAnnotation]:
        """Returns the annotations made in the iteration."""
        raise NotImplementedError
    
    @abc.abstractmethod
    def setup_database(self, annotator: Annotator):
        """Sets up the master user."""
        raise NotImplementedError