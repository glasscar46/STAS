import asyncio
import json
import threading
from typing import Any, List
from i_entities import IModel
from i_entities import ISample
from i_entities import IDAO
from i_entities import Iteration
from i_entities import IStopCondition
from i_entities import Experiment
from selector import SelectorFactory
from metric import MetricFactory
from i_entities import IterationState
from utils.config_loader import ConfigLoader


class AnnotationController:
    """
    Controls the annotation process, including managing iterations, validation of annotations, 
    and stopping conditions. It interacts with the model, database (DAO), and annotation process.
    """

    def __init__(self, model: IModel, dao: IDAO, config: ConfigLoader) -> None:
        """
        Initializes the AnnotationController with the given model, data access object (DAO), and configuration.

        Args:
            model (IModel): The model responsible for generating annotations.
            dao (IDAO): The data access object for interacting with the database.
            config (ConfigLoader): The configuration loader for managing app settings.
        """
        self._model = model
        self._dao: IDAO = dao
        self._stopping_conditions: List[IStopCondition] = []
        self.current_iteration: Iteration = None
        self.position = 0
        self.config = config
        self.max_iteration = config.get('max-iteration', 10)  # Maximum number of iterations
        self.sample_selector = SelectorFactory(self.config).get_selector()  # Sample selector
        #self.metrics = MetricFactory(self.config).get_metric()
        self.sample_size = config.get('sample-size', 100)  # Size of each sample set per iteration
        self.loadExperiment()

    def saveExperiment(self, status: str = None):
        if not status:
            status = self.current_iteration.status
        self._dao.saveExperiment(Experiment(self.current_iteration._id,self.position, status))

    def loadExperiment(self):
        experiment = self._dao.getExperiment()
        if experiment:
            self.current_iteration = self._dao.getIteration(experiment.current_iteration)
            self.position = experiment.position
        

    def run_in_background(self, func, *args):
        loop = asyncio.new_event_loop()  # Create a new event loop for the background task
        asyncio.set_event_loop(loop)  # Set the event loop for the thread
        loop.run_until_complete(func(*args))  # Run the async function until completion

    def validate_annotation(self, sample: ISample, is_valid: bool = False):
        """
        Validates an annotation, marking it as valid or invalid, and persists the result in the database.

        Args:
            sample (ISample): The annotation sample to validate.
            is_valid (bool): Whether the annotation is valid (True) or invalid (False).
        """
        sample.labels.is_valid = is_valid
        sample.validated = is_valid
        self._dao.updateAnnotation(sample)
        if is_valid:
            self._dao.saveSampleAnnotation(sample)  # Save valid annotations to samples
        self.check_iteration_complete()  # Check if stopping conditions are met after each validation

    async def run_iterative_process(self):
        """
        Runs the iterative section of the annotation process, starting new iterations until 
        the maximum number of iterations is reached or the stopping conditions evaluate to true
        or there are no more samples to be annotated.

        If the number of iterations exceeds the maximum, the process is finalized.
        """
        if self.position < self.max_iteration or not self.evaluate_stopping_conditions() or len(self._dao.getPendingSamples()) > 0:
            self.position += 1
            # Start a new iteration in background
            print("running iterative process")
            threading.Thread(target=self.run_in_background, args=(self.startIteration,), name='Iteration_thread').start()
        else:
            self.finalize_process()

    def run_process(self):
        """
        Starts the annotation process by invoking the iterative process.

        This method is responsible for beginning the iterative annotation process.
        """
        print('Process Initialized')
        self._dao.saveExperiment(Experiment(None,0))
        threading.Thread(target=self.run_in_background, args=(self.run_iterative_process,), name='Process thread').start()

    async def finalize_process(self):
        """
        Finalizes the annotation process by annotating any remaining samples, 
        running an evaluation, and completing the process.

        This method should be called when the iterative process reaches its conclusion.
        """
        # Annotate all remaining samples and persist
        samples = self._dao.getPendingSamples()
        samples = self._model.generateAnnotation(samples)
        self._dao.saveAnnotations([sample.labels for sample in samples])
        for sample in samples:
            sample.validated = True
            self._dao.saveSampleAnnotation(sample)
        self._dao.saveAnnotations([sample.labels for sample in samples])
        
        golden_samples = self._dao.getGoldenSamples()
        await asyncio.to_thread(self._model.finetune, self._dao.getGoldenSamples(False))
        generated = await asyncio.to_thread(self._model.generateAnnotation, golden_samples.copy())
        
        metrics = {}
        for metric in self.metrics:
            metrics[metric.__name__]=metric.evaluate(generated, golden_samples)
        
        with open('metrics.json') as f:
            json.dump(metrics,f)
        self.saveExperiment('PROCESS COMPLETE')

    def check_iteration_complete(self):
        """
        Auxiliary method that checks if all validations have been made. When true, 
        the current iteration is ended.

        This method is typically invoked after validating an annotation.
        """
        if not self._dao.getPendingAnnotation(self.current_iteration._id):
            print('Ending Iteration')
            threading.Thread(target=self.run_in_background,args=(self.end_iteration,),name='end iteration Thread').start()  # End the current iteration if all samples have been validated.

    def persistModelAnnotations(self, samples: List[ISample]):
        """
        Persists the annotations generated by the model into the database.

        Args:
            samples (List[ISample]): The list of samples for which annotations are generated.
        """
        if self.current_iteration is None:
            return
        self._dao.saveAnnotations([sample.labels for sample in samples])  # Save the model-generated annotations

    async def startIteration(self):
        """
        Starts a new iteration of the annotation process, selecting a sample of data, 
        fine-tuning the model, generating annotations, and persisting the results.

        This method runs asynchronously, and the fine-tuning process is executed
        in a separate background task.
        """
        samples = self.sample_selector(self._dao).select(self.sample_size)  # Select the sample for annotation
        
        # Run fine-tuning in a background task
        await self.finetune_and_process(samples)

    async def finetune_and_process(self, samples: List[ISample]):
        """
        Fine-tune the model asynchronously and process the results.
        This function will wait for the fine-tuning to complete and
        then continue with saving the model and generating annotations.
        """
        model = self._model.copy()
        
        # Create a new iteration and save it
        self.current_iteration = Iteration(self.position, None, [sample._id for sample in samples])
        self.current_iteration.status = IterationState.FINETUNING
        self.saveExperiment(self.current_iteration.status)
        self.current_iteration._id = await asyncio.to_thread(self._dao.saveIteration, self.current_iteration)

        # Start the fine-tuning process
        print('Finetuning is starting')
        gold_set = await asyncio.to_thread(self._dao.getGoldenSamples,True)
        tset = gold_set + await asyncio.to_thread(self._dao.getGoldenSamples, False)
        await asyncio.to_thread(model.finetune, tset)  # Run fine-tuning in a separate thread
        print('Finetuning is complete')

        # Once fine-tuning is done, continue with the rest of the function
        model_id = await asyncio.to_thread(self._dao.saveModel, model)  # Save the fine-tuned model

        # update iteration and save it
        self.current_iteration.model_id = model_id
        self.current_iteration.status = IterationState.ANNOTATING
        await asyncio.to_thread(self._dao.updateIteration, self.current_iteration)
        self.saveExperiment(self.current_iteration.status)

        # Generate annotations for the samples and persist them
        samples = model.generateAnnotation(samples,self.current_iteration._id)
        await self.persistModelAnnotations(samples)

        # Update iteration status to "validating"
        self.current_iteration.status = IterationState.VALIDATING
        await asyncio.to_thread(self._dao.updateIteration, self.current_iteration)
        await asyncio.to_thread(self.saveExperiment, self.current_iteration.status)

    async def persistModelAnnotations(self, samples: List[ISample]):
        """
        Persist the annotations generated by the fine-tuned model.
        """
        # This can involve saving annotations to the database
        await asyncio.to_thread(self._dao.saveAnnotations, [sample.labels for sample in samples])

    async def end_iteration(self):
        """
        Ends the current iteration, marking it as completed and triggering the next iteration 
        if applicable. If no more iterations remain, the process is finalized.

        This method is typically called after a stopping condition is met.
        """
        self.current_iteration.status = IterationState.COMPLETE
        self._dao.updateIteration(self.current_iteration)
        self.current_iteration = None  # Reset current iteration
        threading.Thread(target=self.run_in_background, args=(self.run_iterative_process,), name='Process thread').start()  # Start the next iteration if needed

    def evaluate_stopping_conditions(self) -> bool:
        """
        Evaluates the stopping conditions to check if the annotation process should end.

        Returns:
            bool: True if any of the stopping conditions are met, False otherwise.
        """
        for condition in self._stopping_conditions:
            if condition.evaluate(self.current_iteration):  # Evaluate each stopping condition
                return True
        return False
