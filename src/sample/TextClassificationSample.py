from i_entities import ISample
from annotation import ClassificationAnnotation

class TextClassificationSample(ISample):
    """
    A sample used in a text classification annotation task.

    This class extends the base `ISample` class and represents a sample that can be
    used in a text classification task. It stores the text of the sample along with
    a classification annotation that labels the text according to predefined categories.

    Attributes:
        labels (ClassificationAnnotation): The annotation object that contains the 
                                          classification label for the text.
    """
    
    def __init__(self, text: str) -> None:
        """
        Initializes a new text classification sample with the given text.

        Args:
            text (str): The text of the sample that needs to be classified.
        """
        super().__init__(text)
        self.labels: ClassificationAnnotation

    @classmethod
    def get_annotation_class(cls) -> ClassificationAnnotation:
        """
        Returns the annotation class that should be used for this sample type.

        This method returns the `ClassificationAnnotation` class, indicating that 
        this sample type is annotated with a classification label.

        Returns:
            ClassificationAnnotation: The class that defines the annotation for 
                                      classification tasks.
        """
        return ClassificationAnnotation
