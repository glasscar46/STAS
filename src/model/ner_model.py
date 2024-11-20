import io
from copy import deepcopy
import spacy
from spacy.training import Example
from typing import Any, List
from i_entities import ISample
from i_entities import IModel
from annotation import SequenceLabelAnnotation

class NERModel(IModel):
    """
    A subclass of IModel that uses a spaCy-based model to perform Named Entity Recognition (NER).
    
    This model loads a pre-trained spaCy NER model, fine-tunes it on a set of annotated samples, 
    and generates NER annotations (entities) for new text samples. The annotations are represented
    by `SequenceLabelAnnotation` objects, which provide information about spans of text and their labels.
    """

    def __init__(self) -> None:
        """
        Initializes the NERModel with a pre-trained spaCy NER model.

        The model is loaded from the `en_core_web_sm` spaCy model, which is a small pre-trained 
        model for English that includes a named entity recognizer.
        """
        super().__init__()
        self.model = spacy.load("en_core_web_sm")
    
    def load(self, model_bytes: io.BytesIO):
        """
        Loads the model from a BytesIO buffer.

        Args:
            model_bytes (io.BytesIO): A BytesIO buffer containing the model's serialized data.

        This method allows for loading a model that was previously serialized and stored.
        """
        # Load the model from the buffer
        self.model = spacy.load(model_bytes)
    
    def save(self) -> io.BytesIO:
        """
        Save the model to a BytesIO buffer.

        Returns:
            io.BytesIO: A buffer containing the serialized model data.
        
        This method serializes the current model to a BytesIO buffer for storage or transport.
        """
        buffer = io.BytesIO()
        buffer.write(self.model.to_bytes())  # Serialize the spaCy model
        buffer.seek(0)  # Go back to the start of the buffer
        return buffer
    
    def finetune(self, samples: List[ISample]):
        """
        Fine-tunes the spaCy model on the provided annotated samples.

        This method takes a list of annotated samples and updates the spaCy model 
        by further training it on the provided data.

        Args:
            samples (List[ISample]): A list of annotated samples for fine-tuning.
        
        Each sample should contain text and entity annotations that the model can learn from.
        """
        examples = []
        for sample in samples:
            # Assuming the sample has 'text' and 'annotations' attributes where annotations
            # are in the form [(start_index, end_index, label), ...]
            doc = self.model.make_doc(sample.text)  # Create a spaCy doc from the text
            gold = doc.copy()
            # Create spaCy's entity objects (EntitySpan)
            ents = [doc.char_span(start, end, label=label,alignment_mode='contract') for start, end, label in sample.labels.label]
            gold.ents = ents  # Assign the entities to the doc
            examples.append(Example(doc,gold))
            # Update the model with the new document
        self.model.update(examples)  # Update with the annotated data
    
    def generateAnnotation(self, samples: List[ISample], iteration_id: Any) -> List[ISample]:
        """
        Generates NER annotations for the provided samples using the spaCy model.

        This method processes the text of each sample, applies the NER model, and creates 
        `SequenceLabelAnnotation` objects for each sample, which contain the recognized entities.

        Returns:
            List[ISample]: A list of annotated samples with named entities.
        """
        annotated_samples = []
        
        for sample in samples:
            # Use spaCy's NER model to process the text
            doc = self.model(sample.text)  # Process the text with spaCy
            
            # Collect the entities found by the model
            annotations = [(ent.start_char, ent.end_char, ent.label_) for ent in doc.ents]
            
            # Create a SequenceLabelAnnotation object for each sample
            annotation = SequenceLabelAnnotation(
                sample_id=sample._id,
                labels=annotations,
                iteration_id=iteration_id
            )
            
            # Create a copy of the sample and assign the annotation
            annotated_sample = deepcopy(sample)  # Assuming the sample can be deep-copied
            annotated_sample.labels = annotation  # Assign the annotation to the sample
            annotated_samples.append(annotated_sample)
        
        return annotated_samples
