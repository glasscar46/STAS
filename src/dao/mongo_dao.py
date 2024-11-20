from typing import Any, List, Type
import io
from uuid import UUID
import uuid
import gridfs
import pymongo
from pymongo import MongoClient
import pymongo.collection
import pymongo.errors
from i_entities import IAnnotation
from i_entities import Annotator
from i_entities import IDAO
from i_entities import Iteration
from i_entities import ISample
from i_entities import IModel
from i_entities import log_method
from i_entities import Experiment


class MongoDAO(IDAO):
    """A MongoDB database implementation of the DAO interface."""

    def __init__(self, connection_string: str, database_name="stas") -> None:
        super().__init__(connection_string, database_name)

    @log_method
    def connect(self):
        self.mongo_client = MongoClient(
            self.connection_string, uuidRepresentation="standard"
        )
        self.database = self.mongo_client[self.database_name]

    def add_document_id(self, document: dict):
        if not document.get("_id"):
            document["_id"] = uuid.uuid4()
        return document

    @log_method
    def get_collection(
        self,
        collection_name: str,
    ) -> pymongo.collection.Collection:
        return self.database.get_collection(collection_name)

    @log_method
    def getfs(self) -> gridfs.GridFS:
        return gridfs.GridFS(self.database)

    @log_method
    def saveSample(self, sample: ISample, count=0):
        try:
            collection = self.get_collection("Sample")
            return collection.insert_one(
                self.add_document_id(sample.serialize())
            ).inserted_id
        except pymongo.errors.ConnectionFailure:
            if count >= 3:
                raise
            self.connect()
            return self.saveSample(sample, count + 1)

    @log_method
    def saveSampleAnnotation(self, sample: ISample, count=0):
        try:
            collection = self.get_collection("Sample")
            return collection.update_one(
                {"_id": sample._id}, {"$set": sample.serialize()}
            )
        except pymongo.errors.ConnectionFailure:
            if count >= 3:
                raise
            self.connect()
            return self.saveSample(sample, count + 1)

    @log_method
    def saveSamples(self, samples: List[ISample], count=0):
        try:
            collection = self.get_collection("Sample")
            return collection.insert_many(
                [self.add_document_id(sample.serialize()) for sample in samples]
            )
        except pymongo.errors.ConnectionFailure:
            if count >= 3:
                raise
            self.connect()
            return self.saveSamples(samples, count + 1)

    @log_method
    def updateAnnotation(self, sample: ISample, count=0):
        try:
            collection = self.get_collection("Annotation")
            print({"_id": sample.labels._id}, {"$set": sample.labels.serialize()})
            collection.update_one(
                {"_id": sample.labels._id}, {"$set": sample.labels.serialize()}
            )
        except pymongo.errors.ConnectionFailure:
            if count >= 3:
                raise
            self.connect()
            return self.updateAnnotation(sample, count + 1)

    @log_method
    def getSample(self, id: UUID, count=0) -> ISample:
        try:
            collection = self.get_collection("Sample")
            return self.sample_class.deserialize(collection.find_one({"_id": id}))
        except pymongo.errors.ConnectionFailure:
            if count >= 3:
                raise
            self.connect()
            return self.getSample(id, count + 1)

    @log_method
    def getPendingAnnotation(self, iteration_id: Any, count=0) -> List[ISample]:
        try:
            collection = self.get_collection("Sample")
            pipeline = [
                {"$match": {"validated": False}},
                {
                    "$lookup": {
                        "from": "Annotation",
                        "localField": "_id",
                        "foreignField": "sample_id",
                        "as": "labels",
                        "pipeline": [
                            {
                                "$match": {
                                    "iteration": iteration_id,
                                    "is_valid": None,
                                    "annotator": None,
                                }
                            },
                            {"$limit": 1},
                        ],
                    }
                },
                {"$unwind": "$labels"},
                {"$limit": 1},
            ]
            result = collection.aggregate(pipeline).to_list()
            if len(result) == 1:
                return self.sample_class.deserialize(result.pop())
            return None
        except pymongo.errors.ConnectionFailure:
            if count >= 3:
                raise
            self.connect()
            return self.getPendingAnnotation(iteration_id, count + 1)

    @log_method
    def saveAnnotation(self, annotation: IAnnotation, count=0):
        try:
            collection = self.get_collection("Annotation")
            return collection.insert_one(
                self.add_document_id(annotation.serialize())
            ).inserted_id
        except pymongo.errors.ConnectionFailure:
            if count >= 3:
                raise
            self.connect()
            return self.saveAnnotation(annotation, count + 1)

    @log_method
    def saveAnnotations(self, annotations: List[IAnnotation], count=0):
        try:
            collection = self.get_collection("Annotation")
            return collection.insert_many(
                [
                    self.add_document_id(annotation.serialize())
                    for annotation in annotations
                ]
            ).inserted_ids
        except pymongo.errors.ConnectionFailure:
            if count >= 3:
                raise
            self.connect()
            return self.saveAnnotations(annotations, count + 1)

    @log_method
    def saveAnnotator(self, annotator: Annotator, count=0):
        try:
            collection = self.get_collection("Annotator")
            return collection.insert_one(
                self.add_document_id(annotator.serialize())
            ).inserted_id
        except pymongo.errors.ConnectionFailure:
            if count >= 3:
                raise
            self.connect()
            return self.saveAnnotator(annotator, count + 1)

    @log_method
    def saveIteration(self, iteration: Iteration, count=0) -> Any:
        try:
            collection = self.get_collection("Iteration")
            return collection.insert_one(
                self.add_document_id(iteration.serialize())
            ).inserted_id
        except pymongo.errors.ConnectionFailure:
            if count >= 3:
                raise
            self.connect()
            return self.saveIteration(iteration, count + 1)

    @log_method
    def updateIteration(self, iteration: Iteration, count=0) -> Any:
        try:
            collection = self.get_collection("Iteration")
            collection.update_one(
                {"_id": iteration._id}, {"$set": iteration.serialize()}
            )
        except pymongo.errors.ConnectionFailure:
            if count == 3:
                raise
            self.connect()
            return self.updateIteration(iteration, count + 1)

    @log_method
    def getIterationAnnotations(self, iteration_id: Any, count=0) -> List[IAnnotation]:
        """Returns the annotations made in the iteration."""
        try:
            collection = self.get_collection("Annotation")
            result = collection.find({"iteration": iteration_id})
            result = result.to_list()
            return [IAnnotation.deserialize(annotation) for annotation in result]
        except pymongo.errors.ConnectionFailure:
            if count == 3:
                raise
            self.connect()
            return self.getIterationAnnotations(iteration_id, count + 1)

    @log_method
    def setup_database(self, annotator: Annotator, count=0):
        try:
            users_collection = self.get_collection("Annotator")
            existing_user = users_collection.find_one({"email": annotator.email})

            if not existing_user:
                # Create the master user
                users_collection.insert_one(self.add_document_id(annotator.serialize()))
                print(f"Master user '{annotator.email}' created successfully.")
        except pymongo.errors.ConnectionFailure:
            if count == 3:
                raise
            self.connect()
            return self.setup_database(annotator, count + 1)

    @log_method
    def login(self, email: str) -> Annotator:
        try:
            collection = self.get_collection("Annotator")
            result = collection.find_one({"email": email})
            return Annotator.deserialize(result)
        except:
            pass

    @log_method
    def getIteration(self, id: Any, count=0):
        try:
            collection = self.get_collection("Iteration")
            return Iteration.deserialize(collection.find_one({"_id": id}))
        except pymongo.errors.ConnectionFailure:
            if count >= 3:
                raise
            self.connect()
            return self.getPendingSamples(count + 1)

    @log_method
    def getPendingSamples(self, count=0) -> List[ISample]:
        try:
            collection = self.get_collection("Sample")
            result = collection.find({"validated": False})
            return [
                self.sample_class.deserialize(sample) for sample in result.to_list()
            ]
        except pymongo.errors.ConnectionFailure:
            if count >= 3:
                raise
            self.connect()
            return self.getPendingSamples(count + 1)

    @log_method
    def saveModel(self, model: IModel):
        """
        Save the model to MongoDB using GridFS.
        This function delegates the saving task to the model's specific method.
        """
        self.connect()
        fs = self.getfs()
        model_bytes = model.save()  # Save the model into the BytesIO buffer
        model_bytes.seek(0)  # Reset the buffer's pointer to the beginning
        file_id = fs.put(model_bytes)  # Save model to GridFS
        return file_id

    @log_method
    def loadModel(self, model_class: Type[IModel], model_id):
        self.connect()
        model_bytes = self.getfs().get(model_id).read()  # Retrieve the model file
        model = model_class()
        model.id = model_id  # Instantiate the model class
        model.load(
            model_bytes
        )  # Delegate the loading task to the model's specific method
        return model

    def saveExperiment(self, experiment: Experiment, count=0):
        """Saves an Experiment."""
        try:
            colection = self.get_collection("Experiment")
            colection.insert_one(self.add_document_id(experiment.serialize()))
        except pymongo.errors.ConnectionFailure:
            if count >= 3:
                raise
            self.connect()
            return self.saveExperiment(experiment, count + 1)

    def getExperiment(self, count=0) -> Experiment:
        """Returns the last saved Experiment."""
        try:
            colection = self.get_collection("Experiment")
            result = colection.find({}).to_list()
            result = [Experiment.deserialize(item) for item in result]
            result.sort(key=lambda x: x.create_time)
            if len(result) > 0:
                return result.pop()
            return None
        except pymongo.errors.ConnectionFailure:
            if count >= 3:
                raise
            self.connect()
            return self.saveExperiment(count + 1)

    def getGoldenSamples(self, tuggle: bool = True, count=0) -> List[ISample]:
        try:
            collection = self.get_collection("Sample")
            result = collection.find({"gold_set": tuggle, "validated": True})
            return [
                self.sample_class.deserialize(sample) for sample in result.to_list()
            ]
        except pymongo.errors.ConnectionFailure:
            if count >= 3:
                raise
            self.connect()
            return self.getGoldenSamples(count + 1)
