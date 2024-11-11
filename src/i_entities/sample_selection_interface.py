import abc
from .dao_interface import IDAO
from .sample_interface import ISample

class ISampleSelector(metaclass=abc.ABCMeta):
    """
    Abstract base class for selecting samples from a data source (such as a database).
    
    The `ISampleSelector` class provides an interface for selecting a subset of samples 
    to be processed or annotated. Subclasses must implement the logic for selecting 
    samples from the data source.
    """
    
    def __init__(self, dao: IDAO):
        """
        Initializes the sample selector with the provided Data Access Object (DAO).

        Args:
            dao (IDAO): An instance of a Data Access Object that provides methods 
                        for interacting with the data source (e.g., a database).
        """
        self.dao = dao

    @abc.abstractmethod
    def select(self, sample_size: int = 100) -> ISample:
        """
        Selects a subset of samples from the data source.

        This method is responsible for selecting the required number of samples 
        from the data source, based on the implementation provided by subclasses.

        Args:
            sample_size (int): The number of samples to select. Default is 100.

        Returns:
            ISample: An instance of a sample, or a list of samples, selected based on the subclass logic.

        Raises:
            NotImplementedError: If not implemented by the subclass.
        """
        raise NotImplementedError
