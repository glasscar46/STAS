import json
import csv
import os
from typing import List, Type
from i_entities import ISample

class DatasetLoader:
    
    def __init__(self, file_path: str, sample_class: Type[ISample]):
        """Initialize with file path and the sample/annotation classes to use for deserialization."""
        self.file_path = file_path
        self.raw_data = []
        self.sample_class = sample_class
        self.dataset = []

    def load_dataset(self):
        """Load the dataset based on the file extension (JSON or CSV) and convert to sample objects."""
        file_extension = os.path.splitext(self.file_path)[1].lower()
        if file_extension == '.json':
            self._load_json()
        elif file_extension == '.csv':
            self._load_csv()
        else:
            raise ValueError("Unsupported file format. Please provide a JSON or CSV file.")
        
        # Convert raw data into objects of the sample class
        self.dataset = [self._create_sample_from_data(data) for data in self.dataset]

    def _load_json(self):
        """Load and parse the Doccano JSON dataset."""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            self.raw_data = json.load(f)
        print(f"Loaded {len(self.raw_data)} records from JSON.")

    def _load_csv(self):
        """Load and parse the Doccano CSV dataset."""
        with open(self.file_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            self.raw_data = [row for row in reader]
        print(f"Loaded {len(self.raw_data)} records from CSV.")

    def _create_sample_from_data(self, data: dict):
        """Convert raw data into an instance of the provided sample class."""
        sample = self.sample_class.deserialize(data)
        sample.id = data.get('id')
        sample.validated = True
        sample.labels.is_valid = True
        return sample

    def get_samples(self):
        """Return the loaded and converted sample objects."""
        return self.dataset
    
    def run(self) -> List[ISample]:
        """"Runs the data loader and returns the samples"""
        self.load_dataset()
        return self.get_samples()