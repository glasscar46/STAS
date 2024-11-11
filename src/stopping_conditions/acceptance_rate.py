from typing import Any, List
from i_entities import IStopCondition
from i_entities import IAnnotation

class AcceptanceRateCondition(IStopCondition):
    """
    A stopping condition based on the acceptance rate of the samples in an iteration.

    This class checks whether the proportion of accepted samples (valid annotations)
    in a given iteration exceeds a specified threshold. The threshold is provided in
    the parameters when initializing the condition. If the acceptance rate meets or 
    exceeds the threshold, the stopping condition is met, signaling the end of the iteration.

    Attributes:
        dao (IDAO): The data access object used to retrieve the iteration evaluations.
        params (dict): A dictionary containing the stopping condition parameters, including the threshold.
    """
    
    def evaluate(self, iteration_id: Any) -> bool:
        """
        Evaluates whether the stopping condition based on the acceptance rate is met for the given iteration.

        This method retrieves the evaluations (annotations) for the specified iteration, calculates
        the acceptance rate by dividing the number of accepted samples by the total number of samples,
        and compares it against the threshold. If the acceptance rate is greater than or equal to the 
        threshold, the condition is met, and the method returns `True`; otherwise, it returns `False`.

        Args:
            iteration_id (Any): The ID of the iteration for which to evaluate the stopping condition.

        Returns:
            bool: `True` if the acceptance rate meets or exceeds the threshold, `False` otherwise.

        Raises:
            ValueError: If the 'threshold' parameter is not set in the condition's `params`.
        """
        if 'threshold' not in self.params:
            raise ValueError('threshold parameter not set for AcceptanceRateCondition')

        # Retrieve all evaluation annotations for the given iteration
        evals: List[IAnnotation] = self.dao.getIterationEvals(iteration_id)
        
        # Calculate the number of accepted annotations (valid ones)
        accepted = [item for item in evals if item.is_valid]
        
        # Compare acceptance rate to threshold
        return len(accepted) / len(evals) >= self.params['threshold']
