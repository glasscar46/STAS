from typing import Any, List
from i_entities import IStopCondition
from i_entities import IAnnotation

class AcceptanceRateCondition(IStopCondition):
    """A condition based on the acceptance rate of the samples in an iteration."""
    
    
    def evaluate(self, iteration_id: Any)-> bool:
        if 'threshold' not in self.params:
            raise ValueError('threshold parameter not set for AcceptanceRateCondition')

        evals:List[IAnnotation] = self.dao.getIterationEvals(iteration_id)
        accepted = [item for item in evals if item.is_valid ]
        return len(accepted)/ len(evals) >= self.params['threshold']