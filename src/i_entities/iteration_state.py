from enum import StrEnum

class IterationState(StrEnum):
    
    INITIALIZED = 'INITIALIZED'
    STARTED = 'STARTED'
    FINETUNING = 'FINETUNING'
    ANNOTATING = 'ANNOTATING'
    VALIDATING = 'VALIDATING'
    COMPLETE = 'COMPLETE'
    
    