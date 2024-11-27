# STAS

## Overview

The **STAS System** is a modular framework designed to facilitate the iterative annotation process for machine learning tasks such as text classification and sequence labeling. This system automates the annotation process by allowing machine learning models to label data, which can then be reviewed and validated by human annotators. The system provides a flexible architecture for managing sample selection, annotation, stopping conditions, and iterative fine-tuning of models.

With the inclusion of a **Streamlit-based graphical user interface (GUI)**, the system allows users to interact with the application, manage the annotation process, validate annotations, and upload datasets through an intuitive web interface.

## Key Features

- **Iterative Annotation**: Automates the process of fine-tuning models and annotating data iteratively, ensuring continual model improvement.
- **Configurable Stopping Conditions**: Allows you to define custom conditions to stop the annotation process based on metrics such as the acceptance rate or other criteria.
- **Flexible Annotation Model**: Supports both text classification and sequence labeling annotation tasks.
- **Sample Selection**: Automatically selects samples for annotation using different selection strategies (e.g., random selection).
- **Streamlit UI**: Provides a simple and interactive web interface for annotators to log in, manage annotations, validate sample labels, and upload datasets.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [System Architecture](#system-architecture)
- [Components](#components)
  - [Sample Types](#sample-types)
  - [Annotation Types](#annotation-types)
  - [Stopping Conditions](#stopping-conditions)
  - [Sample Selectors](#sample-selectors)
  - [Model Interface](#model-interface)
  - [Streamlit GUI](#streamlit-gui)
- [Extending the Annotation System](#Extending-the-Annotation-System)
- [Contributing](#contributing)
- [License](#license)

## Installation

To install and use the annotation system, follow these steps:

1. **Clone the repository**:

   ```bash
   
   git clone https://github.com/glasscar46/stas.git
   cd stas
   ```

2. **Install dependencies**:

   You can install the required dependencies using `pip`:

   ```bash
   pip install -r requirements.txt
   ```

3. **Install Streamlit**:

   Since the system uses Streamlit for the GUI, make sure you have Streamlit installed:

   ```bash
   pip install streamlit
   ```

4. **Configure the system**:

   The system is configured through a `config.yaml` file. You need to define various parameters, such as the sample class to use, the stopping conditions, and other model configurations.

## Usage

### Running the Streamlit Application

To run the Streamlit web interface, use the following command:

```bash
streamlit run api/ui.py
```

This will start the Streamlit app and open it in your browser, where you can interact with the system. The GUI allows you to log in, view annotations, validate them, and upload datasets directly.

### Configuring the System

The system can be configured through a `config.yaml` file. The configuration includes various options for managing the annotation process, sample selection, and stopping conditions.

Here’s an example of the configuration:

```yaml
database-name: 'stas'
connection-string: 'mongodb://localhost:27017'
max-iterations: 10
sample-size: 100
sampleClass: 'SequenceToSequenceSample'
modelName: 'NERModel'
Selector: 'RandomSampleSelector'
master-email: 'admin@email.com'
master-password: 'admin@email.com'
secret-key: 'example-secretkey'
metrics: 
  - None
```

### Authentication and User Roles

The system supports user authentication through the Streamlit interface. Users must log in to manage annotations or upload datasets. The login process is based on the user's credentials (username and password), which are stored in the database.

### Uploading Datasets

You can upload datasets in CSV or JSON format directly through the Streamlit interface. This can be done on the **"Upload Dataset"** page in the GUI. The dataset can be marked as annotated (part of a golden set) or not annotated.

## System Architecture

The architecture of the Annotation System follows a modular design, with key components:

### 1. **Annotation Controller**
   - Manages the overall annotation process.
   - Coordinates the iterative fine-tuning of models and annotation of data.
   - Evaluates stopping conditions to determine when the annotation process should stop.

### 2. **Sample Selector**
   - Responsible for selecting samples for annotation based on a specific strategy.
   - Examples include random selection (`RandomSampleSelector`).

### 3. **Sample Types**
   - Define the structure of the samples to be annotated.
   - Examples include `TextClassificationSample` (for text classification) and `SequenceToSequenceSample` (for sequence labeling).

### 4. **Annotation Types**
   - Define the annotation structure for different tasks.
   - Examples include `ClassificationAnnotation` (for text classification) and `SequenceLabelAnnotation` (for sequence labeling).

### 5. **Model Interface**
   - Models used for annotation are required to implement the `IModel` interface.
   - Models must have the ability to fine-tune on annotated data and generate annotations for new samples.

### 6. **Stopping Conditions**
   - Define conditions for stopping the iterative annotation process.
   - Examples include `AcceptanceRateCondition` and other custom conditions.

## Components

### Sample Types

1. **TextClassificationSample**: A sample for text classification tasks, containing a text and a classification annotation (`ClassificationAnnotation`).
2. **SequenceToSequenceSample**: A sample for sequence labeling tasks, containing a text and a sequence of span-based labels (`SequenceLabelAnnotation`).

### Annotation Types

1. **ClassificationAnnotation**: Represents annotations for text classification tasks. The label is a single value (e.g., "positive", "negative").
2. **SequenceLabelAnnotation**: Represents annotations for sequence labeling tasks. The label is a list of tuples, where each tuple contains a start index, an end index, and a label.

### Stopping Conditions

1. **AcceptanceRateCondition**: A stopping condition based on the acceptance rate of annotations. The process stops when the acceptance rate meets or exceeds a given threshold.

### Sample Selectors

1. **RandomSampleSelector**: A sample selector that selects samples randomly from the pool of unannotated samples.

### Model Interface

The models that annotate samples must implement the `IModel` interface. Models are expected to:
- **finetune**: Fine-tune the model using annotated data.
- **generateAnnotation**: Generate annotations for a given set of samples.

## Streamlit GUI

The **Streamlit GUI** serves as the front-end interface for users (annotators, administrators) to interact with the annotation system. It provides an intuitive and user-friendly experience for managing the annotation process, validating annotations, and uploading datasets.

### Features of the Streamlit UI

- **Login Page**: Allows annotators to log in using their credentials.
- **Manage Process**: After logging in, users are presented with a dashboard where they can:
  - Start the annotation process.
  - View the current iteration details, such as the number of pending samples and the status of the process.
- **Annotation Validation**: Users can view and validate annotations (accept or reject them). Annotations are displayed based on their type (e.g., sequence labeling or classification).
- **Dataset Upload**: Annotators can upload new datasets in CSV or JSON format and save them to the database. The dataset can be marked as annotated or unannotated.
- **Logout**: Users can log out, which clears their session state and redirects them back to the login page.

### Key Functions in the UI

1. **Manage Process**: 
   - Start or restart the annotation process.
   - View iteration statistics, such as the number of samples, the number of pending validations, and overall progress.
   
2. **Annotation Validation**: 
   - View pending annotation samples.
   - Accept or reject annotations based on their accuracy.

3. **Upload Dataset**: 
   - Upload datasets in CSV or JSON format.
   - Choose whether the dataset is annotated or unannotated.

4. **Login/Logout**: 
   - Annotators must log in to access annotation tasks.
   - The logout functionality clears the session state and returns the user to the login screen.

### Streamlit UI Flow

1. **Login**: Annotators log in with their username and password.
2. **Manage Process**: Users can initiate or restart the annotation process and view iteration details.
3. **Annotation Validation**: Users can validate and manage pending annotations.
4. **Upload Dataset**: Annotators can upload new datasets to the system.
5. **Logout**: Annotators can log out, clearing their session.

## Extending the Annotation System

The **Annotation System** is designed with flexibility and extensibility in mind, allowing you to easily add new features, sample types, annotation methods, stopping conditions, or even custom user interfaces. Below are some of the key ways you can extend and customize the system to fit your specific needs.

### 1. **Adding New Sample Types**

The system supports multiple types of samples (e.g., `TextClassificationSample`, `SequenceToSequenceSample`). If you need to add support for additional sample types (such as for new machine learning tasks), you can extend the `ISample` interface and implement your own sample class.

**Steps to add a new sample type:**
- Define a new class that implements the `ISample` interface. 
- Implement the necessary methods such as `deserialize()` to convert raw data into your sample type and `get_sample_type()` to define its characteristics.
- Update the `SampleFactory` to include your new sample type, allowing it to be selected dynamically based on the configuration.

**Example**:
```python
from i_entities import ISample
from annotation import SequenceLabelAnnotation

class MyNewSample(ISample):
    def __init__(self, text):
        self.text = text
        self.labels = SequenceLabelAnnotation()  # Example annotation type
    
    @classmethod
    def deserialize(cls, data):
        return cls(data['text'])
    
    def get_sample_type(self):
        return 'MyNewSampleType'
```

### 2. **Adding New Annotation Types**

If your project involves a different kind of annotation (e.g., multiple-choice labeling, sentiment analysis), you can add custom annotation types by creating new classes that implement the `IAnnotation` interface.

**Steps to add a new annotation type:**
- Define a new annotation class that extends the `IAnnotation` interface.
- Implement methods like `get_value()`, `get_annotation_name()`, and any additional methods specific to your task.
- Update the relevant sample type class to use this new annotation class.

**Example**:
```python
from i_entities import IAnnotation

class SentimentAnnotation(IAnnotation):
    def __init__(self, sample_id, label, annotator_id=None, iteration_id=None, is_valid=False):
        super().__init__(sample_id, label, annotator_id, iteration_id, is_valid)
    
    @classmethod
    def get_annotation_name(cls) -> str:
        return "Sentiment"
    
    def get_value(self):
        return self.label
```

### 3. **Customizing Sample Selection Strategies**

The system provides a `SampleSelector` interface that allows you to define custom strategies for selecting samples for annotation (e.g., random selection, uncertainty sampling). You can extend the sample selection mechanism by adding new selectors.

**Steps to add a new sample selector:**
- Define a new class that implements the `ISampleSelector` interface.
- Implement the `select()` method to define your custom selection logic (e.g., select the least confident samples, or samples that are most uncertain).
- Update the `SelectorFactory` to include your new selector, ensuring that it can be dynamically chosen based on configuration.

**Example**:
```python
from i_entities import ISampleSelector
from random import Random

class UncertaintySampleSelector(ISampleSelector):
    def select(self, sample_size=100):
        samples = self.dao.getPendingSamples()
        # Custom logic to select uncertain samples
        uncertain_samples = [s for s in samples if s.is_uncertain()]
        return uncertain_samples[:sample_size]
```

### 4. **Customizing Stopping Conditions**

The system supports different stopping conditions, such as stopping based on the acceptance rate of annotations. You can add custom stopping conditions that determine when the annotation process should be halted.

**Steps to add a new stopping condition:**
- Define a new class that implements the `IStopCondition` interface.
- Implement the `evaluate()` method to determine whether the stopping condition has been met.
- Update the configuration (`config.yaml`) to include your new stopping condition type.

**Example**:
```python
from i_entities import IStopCondition

class IterationCountStopCondition(IStopCondition):
    def evaluate(self, iteration_id: Any) -> bool:
        max_iterations = self.params.get('max_iterations', 10)
        current_iteration = self.dao.getIteration(iteration_id)
        return current_iteration.count >= max_iterations
```

### 5. **Integrating with External Models**

The system is designed to integrate with external machine learning models that can generate annotations (e.g., NLP models for text classification). You can extend the system by implementing your own `IModel` interface for a specific model.

**Steps to integrate a custom model:**
- Define a model class that implements the `IModel` interface.
- Implement the `generateAnnotation()` method to use the model to generate annotations for new samples.
- Optionally, implement the `finetune()` method to fine-tune the model on newly annotated data.

**Example**:
```python
from i_entities import IModel

class MyCustomModel(IModel):
    def finetune(self, samples):
        # Fine-tune the model on the given samples
        pass

    def generateAnnotation(self, sample):
        # Generate annotation for a given sample
        return "Positive"  # Example output
```

### 6. **Extending the Streamlit UI**

You can customize the **Streamlit UI** to add additional pages, visualizations, or functionality to suit your project’s needs.

**Steps to extend the UI:**
- Modify the `Application` class to add new pages or views.
- Use Streamlit's built-in functions (`st.write()`, `st.button()`, `st.selectbox()`, etc.) to create custom widgets for the new features.
- Ensure that the new features interact with the backend, such as interacting with the database or calling existing methods to process annotations.

**Example**:
```python
class Application:
    def __init__(self):
        self.config = ConfigLoader('config.yaml')
        self.dao = MongoDAO(self.config.get('connection-string'), self.config.get('database-name'))
        self.controller = AnnotationController(self.dao, self.config)

    def display_summary(self):
        st.header("Process Summary")
        # Display overall statistics, such as number of samples annotated, validation rate, etc.
        stats = self.dao.getAnnotationStats()
        st.write(stats)

    def main(self):
        page = st.sidebar.selectbox("Select Page", ["Annotation", "Summary"])
        if page == "Annotation":
            self.display_annotations()
        elif page == "Summary":
            self.display_summary()
```

### 7. **Implementing Custom User Roles and Permissions**

The system currently supports basic user authentication, but you can extend it by adding different user roles and permissions. For example, you could differentiate between **admin** users who can modify the annotation process and **annotators** who can only validate annotations.

**Steps to implement roles and permissions:**
- Extend the `Annotator` class to include roles (e.g., `admin`, `annotator`).
- Modify the login logic to check the user role.
- Implement role-based access control in the Streamlit UI to show different options for different user types.

**Example**:
```python
class Annotator:
    def __init__(self, email, password, role="annotator"):
        self.email = email
        self.password = password
        self.role = role  # New role attribute

    def is_admin(self):
        return self.role == "admin"
```

### 8. **Adding Additional Data Formats**

Currently, the system supports dataset uploads in CSV and JSON formats. If you need to support other formats (e.g., Excel, XML), you can extend the **DatasetLoader** class to handle these formats.

**Steps to add support for new formats:**
- Update the `DatasetLoader` class to include logic for parsing new file types (e.g., Excel, XML).
- Implement custom parsing functions for the new formats (e.g., `pandas.read_excel()` for Excel files).
- Modify the dataset upload interface in the Streamlit UI to allow users to select the new file type.

---

### Conclusion

The **Annotation System** is highly modular and can be easily extended to accommodate various needs and tasks. Whether you need to add new sample types, annotation strategies, stopping conditions, or even integrate with external models, the system provides a flexible architecture for doing so. Additionally, the **Streamlit GUI** offers a straightforward way to interact with the system, and you can customize the interface to fit the specific workflow of your annotation process.

If you have a specific use case that requires additional functionality, feel free to extend any of the core components or add new ones to make the system fit your needs.


## Contributing

We welcome contributions to the Annotation System. If you have an idea for a feature or have found a bug, please feel free to submit an issue or create a pull request.

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/feature-name`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature/feature-name`).
6. Create a new pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.

