import json
import csv
import os
from typing import List, Type
from i_entities import ISample

class DatasetLoader:
    """
    A class for loading and processing datasets from either JSON or CSV formats.

    The `DatasetLoader` class is responsible for loading data from a specified file (either JSON or CSV),
    parsing the data, and converting it into instances of the provided sample class (`ISample`). Optionally,
    it can handle annotated data by marking the samples as validated.

    Attributes:
        file_path (str): Path to the dataset file (JSON or CSV).
        raw_data (list): Raw data loaded from the file before conversion.
        sample_class (Type[ISample]): The class used to deserialize the data into sample objects.
        dataset (list): The list of sample objects after deserialization.
        annotated (bool): Flag indicating whether the dataset contains annotated data (default: False).
    """
    
    def __init__(self, file_path: str, sample_class: Type[ISample], annotated=False):
        """
        Initializes the DatasetLoader with the file path and sample class.

        Args:
            file_path (str): Path to the dataset file (either JSON or CSV).
            sample_class (Type[ISample]): The class used to convert raw data into sample objects.
            annotated (bool): A flag indicating whether the dataset contains annotations (default: False).
        """
        self.file_path = file_path
        self.raw_data = []
        self.sample_class = sample_class
        self.dataset = []
        self.annotated = annotated

    def load_dataset(self):
        """
        Loads the dataset based on the file extension (JSON or CSV) and converts raw data into sample objects.

        This method inspects the file extension of the given dataset file path. If the file is a JSON or CSV file,
        it calls the appropriate private method to load the data and then converts the raw data into instances of
        the provided `sample_class`.

        Raises:
            ValueError: If the file format is neither JSON nor CSV.
        """
        file_extension = os.path.splitext(self.file_path)[1].lower()
        if file_extension == '.json':
            self._load_json()
        elif file_extension == '.csv':
            self._load_csv()
        else:
            raise ValueError("Unsupported file format. Please provide a JSON or CSV file.")
        
        # Convert raw data into objects of the sample class
        self.dataset = [self._create_sample_from_data(data) for data in self.raw_data]

    def _load_json(self):
        """
        Loads and parses a JSON dataset (e.g., from Doccano) into raw data.

        This method reads a JSON file from the file path and parses it into a list of dictionaries (raw data).
        Each dictionary corresponds to a sample in the dataset.

        After loading the data, it prints how many records were loaded.

        Raises:
            FileNotFoundError: If the file at `self.file_path` does not exist.
        """
        with open(self.file_path, 'r', encoding='utf-8') as f:
            self.raw_data = json.load(f)
        print(f"Loaded {len(self.raw_data)} records from JSON.")

    def _load_csv(self):
        """
        Loads and parses a CSV dataset (e.g., from Doccano) into raw data.

        This method reads a CSV file from the file path and parses it into a list of dictionaries (raw data).
        Each dictionary corresponds to a sample, where the keys are column headers and the values are cell data.

        After loading the data, it prints how many records were loaded.

        Raises:
            FileNotFoundError: If the file at `self.file_path` does not exist.
        """
        with open(self.file_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            self.raw_data = [row for row in reader]
        print(f"Loaded {len(self.raw_data)} records from CSV.")

    def _create_sample_from_data(self, data: dict):
        """
        Converts raw data (in dictionary form) into an instance of the provided sample class.

        This method deserializes the raw data using the `sample_class`, sets the sample's ID,
        and marks it as validated if `annotated` is set to `True`.

        Args:
            data (dict): A dictionary representing a single sample from the raw dataset.

        Returns:
            ISample: An instance of the provided `sample_class` populated with the data.
        """
        sample = self.sample_class.deserialize(data)
        sample._id = data.get('id')
        if self.annotated:
            sample.validated = True
            sample.labels.is_valid = True
        else:
            sample.labels = None
        return sample

    def get_samples(self):
        """
        Returns the loaded and converted sample objects.

        This method returns the dataset after the raw data has been processed and converted into
        instances of the provided sample class.

        Returns:
            list: A list of sample objects created from the raw data.
        """
        return self.dataset
    
    def run(self) -> List[ISample]:
        """
        Runs the data loader and returns the loaded sample objects.

        This method combines the loading and sample creation process. It first loads the dataset (either JSON or CSV),
        converts the raw data into sample objects, and then returns the resulting list of samples.

        Returns:
            List[ISample]: A list of sample objects after loading and conversion.
        """
        self.load_dataset()
        return self.get_samples()
