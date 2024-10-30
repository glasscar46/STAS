from typing import Any, List
from uuid import UUID
import pymongo
from pymongo import MongoClient
from logging import Logger
import pymongo.collection
import pymongo.errors
from i_entities import IAnnotation
from i_entities import Annotator
from i_entities import IDAO
from i_entities import Iteration
from i_entities import ISample
from i_entities import IModel

class MongoDAO(IDAO):
    """A MongoDB database implementation of the DAO interface."""

    def __init__(self, connection_string: str, database_name="stas") -> None:
        super().__init__(connection_string, database_name)

    def connect(self):
        self.mongo_client = MongoClient(
            self.connection_string, uuidRepresentation="standard"
        )
        self.database = self.mongo_client[self.database_name]

    def get_collection(
        self, collection_name: str, count=0
    ) -> pymongo.collection.Collection:
        return self.database.get_collection(collection_name)

    def saveSample(self, sample: ISample, count=0):
        try:
            collection = self.get_collection("Sample")
            return collection.insert_one(sample.serialize()).inserted_id
        except pymongo.errors.ConnectionFailure:
            if count >= 3:
                raise
            self.connect()
            return self.saveSample(sample, count + 1)

    def saveSamples(self, samples: List[ISample], count=0):
        try:
            collection = self.get_collection("Sample")
            return collection.insert_many([sample.serialize() for sample in samples])
        except pymongo.errors.ConnectionFailure:
            if count >= 3:
                raise
            self.connect()
            return self.saveSamples(samples, count + 1)

    def updateAnnotation(self, sample: ISample, count=0):
        try:
            collection = self.get_collection("Annnotation")
            collection.update_one({"_id": sample.labels.id}, sample.labels.serialize())
        except pymongo.errors.ConnectionFailure:
            if count >= 3:
                raise
            self.connect()
            return self.updateAnnotation(sample, count + 1)

    def getSample(self, id: UUID, count=0) -> ISample:
        try:
            collection = self.get_collection("Sample")
            return ISample.deserialize(collection.find_one({"_id": id}))
        except pymongo.errors.ConnectionFailure:
            if count >= 3:
                raise
            self.connect()
            return self.getSample(id, count + 1)

    def getPendingAnnotation(self, iteration_id: Any, count=0) -> List[ISample]:
        try:
            collection = self.get_collection("Sample")
            pipeline = [
                {"$match": {"validated": False}},
                {
                    "$lookup": {
                        "from": "Annotation",
                        "localField": "$_id",
                        "foreignField": "$sample_id",
                        "as": "labels",
                        "pipeline": [{"$match": {"iteration": iteration_id}}],
                    }
                },
                {"$unwind": "$labels"},
            ]
            result = collection.aggregate(pipeline).to_list()
            return [ISample.deserialize(sample) for sample in result]
        except pymongo.errors.ConnectionFailure:
            if count >= 3:
                raise
            self.connect()
            return self.getPendingAnnotation(iteration_id, count + 1)

    def saveAnnotation(self, annotation: IAnnotation, count):
        try:
            collection = self.get_collection("Annotation")
            return collection.insert_one(annotation.serialize()).inserted_id
        except pymongo.errors.ConnectionFailure:
            if count >= 3:
                raise
            self.connect()
            return self.saveAnnotation(annotation, count + 1)

    def saveAnnotations(self, annotations: List[IAnnotation], count):
        try:
            collection = self.get_collection("Annotation")
            return collection.insert_many(
                [annotation.serialize() for annotation in annotations]
            ).inserted_id
        except pymongo.errors.ConnectionFailure:
            if count >= 3:
                raise
            self.connect()
            return self.saveAnnotations(annotations, count + 1)

    def saveAnnotator(self, annotator: Annotator, count=0):
        try:
            collection = self.get_collection("Annotator")
            return collection.insert_one(annotator.serialize()).inserted_id
        except pymongo.errors.ConnectionFailure:
            if count >= 3:
                raise
            self.connect()
            return self.saveAnnotator(annotator, count + 1)

    def saveIteration(self, iteration: Iteration, count=0) -> Any:
        try:
            collection = self.get_collection("Iteration")
            return collection.insert_one(iteration.serialize()).inserted_id
        except pymongo.errors.ConnectionFailure:
            if count >= 3:
                raise
            self.connect()
            return self.saveIteration(iteration, count + 1)

    def updateIteration(self, iteration: Iteration, count=0) -> Any:
        try:
            collection = self.get_collection("Iteration")
            collection.update_one({"_id": iteration.id}, iteration.serialize())
        except pymongo.errors.ConnectionFailure:
            if count == 3:
                raise
            self.connect()
            return self.self.updateIteration(iteration, count + 1)

    def getIterationEvals(self, iteration_id: Any, count=0) -> List[IAnnotation]:
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
            return self.getIterationEvals(iteration_id, count + 1)
    
    def login(self, annotator: Annotator)-> Annotator:
        try:
            collection = self.get_collection("Annotator")
            result = collection.find_one({'email': annotator._email, 'password': annotator._password})
            return Annotator.deserialize(result)
        except:
            pass
    
    def logout(self, annotator: Annotator):
        return True

    def getIteration(self, id: Any):
        pass
    
    def getPendingSamples(self):
        pass
    
    def saveModel(self, model: IModel):
        pass

    # TODO: saving models
