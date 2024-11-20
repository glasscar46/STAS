import threading
import streamlit as st
import json
import random
import re
import pandas
import datetime
import jwt
import bcrypt
from annotated_text import annotated_text
from streamlit_option_menu import option_menu
from i_entities import Annotator
from i_entities import ISample
from utils.loader import DatasetLoader
from utils.config_loader import ConfigLoader
from annotation import SequenceLabelAnnotation
from annotation import ClassificationAnnotation
from sample import SampleFactory
from model import ModelFactory
from dao import MongoDAO
from api.controller import AnnotationController


class Application():
    """
    Main application class for managing the annotation process, user authentication, 
    visualization of annotations, and dataset upload in the Streamlit interface.
    """
    SECRET_KEY = None
    
    def __init__(self):
        """
        Initializes the application, loads the configuration, sets up database connections, 
        and prepares the annotation controller.
        """
        self.config = ConfigLoader('config.yaml')  # Load configuration from a YAML file
        self.dao = MongoDAO(self.config.get('connection-string'), self.config.get('database-name'))  # Database connection
        self.dao.set_sample_class(SampleFactory(self.config).get_sample())
        model = ModelFactory(self.config).get_model()
        self.controller = AnnotationController(model(), self.dao, self.config)  # Annotation controller
        self.SECRET_KEY = self.config.get('secret-key')
        self.setup()  # Set up the database
        
    def setup(self):
        """
        Sets up the database using the master annotator credentials from the configuration.
        """
        annotator = Annotator(self.config.get('master-email'), self.hash_password(self.config.get('master-password')))
        self.dao.setup_database(annotator)  # Initializes database with the master annotator

    def create_user(self, username, password):
        hashed_password = self.hash_password(password)
        annotator= Annotator(username, hashed_password)
        self.dao.saveAnnotator(annotator)

    def generate_jwt(self, user_id):
        expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=3)
        payload = {
            "user_id": user_id,
            "exp": expiration
        }
        token = jwt.encode(payload, self.SECRET_KEY, algorithm="HS256")
        return token

    def verify_jwt(self, token):
        try:
            decoded = jwt.decode(token, self.SECRET_KEY, algorithms=["HS256"])
            return decoded
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def hash_password(self, password: str):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


    def verify_password(self, stored_hash, password: str):
        return bcrypt.checkpw(password.encode('utf-8'), stored_hash)

    def login(self, username, password):
        """
        Logs in a user by verifying their credentials and storing the session state.

        Args:
            username (str): The username of the annotator.
            password (str): The password of the annotator.

        Returns:
            bool: True if login is successful, False otherwise.
        """
        annotator = self.dao.login(username)
        if annotator and self.verify_password(annotator.password, password):
            token = self.generate_jwt(str(annotator.email))
            return token, annotator
        return None, None

    def logout(self):
        """
        Logs out the current user by clearing the session state.

        Returns:
            bool: True if logout is successful, False otherwise.
        """
        st.session_state.user = None  # Clear the user from session state
        st.session_state.jwt_token = None
        return True

    def visualize_sequence_labels(self, text, annotations, title):
        """
        Visualizes sequence label annotations by displaying the annotated text with labels.

        Args:
            text (str): The text to annotate.
            annotations (list): A list of tuples containing (start, end, label) for sequence labels.
            title (str): The title to display for the annotation visualization.
        """
        st.header(title)
        display_text = []  # List to hold the annotated text
        
        current_index = 0
        for start, end, label in annotations:
            # Add the plain text before the annotation
            if start > current_index:
                display_text.append(text[current_index:start])
            
            # Add the annotation (text[start:end], label)
            display_text.append((text[start:end], label))
            current_index = end  # Update the current index
        
        # Add remaining plain text after the last annotation
        if current_index < len(text):
            display_text.append(text[current_index:])
        
        # Display the annotated text
        annotated_text(*display_text)

    def display_aesthetic_text(self, text, title, max_paragraph_length=200):
        """
        Splits long text into smaller paragraphs and displays them in a justified format.

        Args:
            text (str): The text to display.
            title (str): The title to display above the text.
            max_paragraph_length (int): The maximum length of each paragraph.
        """
        st.header(title)
        sentences = re.split(r'(?<=[.!?]) +', text)  # Split the text into sentences
        
        paragraphs = []  # List to hold the paragraphs
        current_paragraph = ""  # Current paragraph being built
        
        for sentence in sentences:
            # If the sentence fits in the current paragraph, add it
            if len(current_paragraph) + len(sentence) <= max_paragraph_length:
                current_paragraph += sentence + " "
            else:
                paragraphs.append(current_paragraph.strip())  # Add the current paragraph
                current_paragraph = sentence + " "
        
        # Add the last paragraph if it's not empty
        if current_paragraph:
            paragraphs.append(current_paragraph.strip())
        
        # Display each paragraph in a justified format
        for paragraph in paragraphs:
            st.markdown(f"<p style='text-align: justify;'>{paragraph}</p>", unsafe_allow_html=True)

    def fetch_pending_annotations(self):
        """
        Fetches a random pending annotation sample from the database.

        Returns:
            ISample: A random pending annotation sample, or None if no pending annotations exist.
        """
        if self.controller.current_iteration is None:
            return None
        
        samples = self.dao.getPendingAnnotation(self.controller.current_iteration._id)
        
        if not samples:
            return None
        
        return random.choice(samples)

    def validate_annotation(self, annotation:ISample, is_accepted):
        """
        Validates an annotation (accepts or rejects it).

        Args:
            annotation (ISample): The annotation sample to validate.
            is_accepted (bool): Whether the annotation is accepted (True) or rejected (False).

        Returns:
            bool: True if the annotation was successfully validated, False otherwise.
        """
        annotation.labels.annotator = st.session_state.user._id
        self.controller.validate_annotation(annotation, is_accepted)
        return True

    def show_annotation(self, sample: ISample):
        """
        Displays an annotation sample based on its type (sequence label or classification).

        Args:
            sample (ISample): The annotation sample to display.
        """
        if isinstance(sample.labels, SequenceLabelAnnotation):
            self.visualize_sequence_labels(sample.text, sample.labels.get_value(), sample.labels.get_annotation_name())
        elif isinstance(sample.labels, ClassificationAnnotation):
            self.display_aesthetic_text(sample.text, 'Sample Text')
            st.markdown('---')
            self.display_aesthetic_text(sample.labels.get_value(), sample.labels.get_annotation_name())

    def display_annotations(self):
        """
        Fetches and displays pending annotations along with options to accept or reject them.
        """
        if self.controller.current_iteration:
            # Fetch a sample from the database (for testing purposes, using hardcoded index)
            annotation = self.dao.getPendingAnnotation(self.controller.current_iteration._id)
            if annotation:
                self.show_annotation(annotation)  # Show the annotation sample
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"Accept"):
                        if self.validate_annotation(annotation, True):
                            st.success("Validation submitted successfully!")
                            st.rerun()
                        else:
                            st.error("Failed to submit validation.")
                with col2:
                    if st.button(f"Reject"):
                        if self.validate_annotation(annotation, False):
                            st.success("Validation submitted successfully!")
                        else:
                            st.error("Failed to submit validation.")
            else:
                st.toast('There are no pending Annotations in this iteration.')
        else:
            st.toast('There is no ongoing process.')

    def upload_document(self, uploaded_file, annotated=False):
        """
        Uploads a dataset file (CSV or JSON) and saves it to the database.

        Args:
            uploaded_file (file-like object): The file to upload.
            annotated (bool): Whether the dataset is annotated (True) or not (False).
        """
        if uploaded_file.type == "text/csv":
            filename = 'data/dataset.csv'
            pandas.read_csv(uploaded_file).to_csv(filename)
        else:
            filename = 'data/dataset.json'
            json_data = json.loads(uploaded_file.getvalue().decode("utf-8"))
            with open(filename, 'w') as file:
                json.dump(json_data, file)
        
        try:
            samples = DatasetLoader(filename, SampleFactory(self.config).get_sample(), annotated).run()
            self.dao.saveSamples(samples)
            st.success('Data uploaded and saved Successfully')
        except Exception as e:
            st.error(f'Unable to save uploaded Dataset: {e}')

    def main(self):
        """
        Main method that runs the Streamlit app, including user login, sidebar navigation,
        and page display for managing the process, validating annotations, and uploading datasets.
        """
        if "jwt_token" not in st.session_state:
            st.session_state.user = None

        # Sidebar for navigation
        options=["Manage Process", "Annotation Validation", "Upload Dataset", "Logout"]
        icons=["gear", "check2-square", "cloud-upload", "box-arrow-right"]
        if st.session_state.user is None or not self.verify_jwt(st.session_state.jwt_token):
            options = ["Login"]
            icons = ["box-arrow-left"]
        with st.sidebar:
            page = option_menu(
                "Menu",
                options=options,
                icons=icons,
                menu_icon="cast",
                default_index=0,
                styles={
                    "container": {"padding": "0!important", "background-color": "transparent"},
                    "icon": {"color": "black", "font-size": "18px"},
                    "nav-link": {
                        "font-size": "20px",
                        "text-align": "left",
                        "margin": "0px",
                        "--hover-color": "#aaa",
                    },
                    "nav-link-selected": {"background-color": "#fff", "color": "black"},
                }
            )

        # Login Page
        if page == "Login":
        # Login or Register
            choice = st.radio("Choose an option", ["Login", "Register"])

            if choice == "Login":
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")

                if st.button("Login"):
                    token , annotator = self.login(username, password)
                    if token:
                        st.session_state["jwt_token"] = token
                        st.session_state['user'] = annotator
                        st.rerun()
                    else:
                        st.error("Invalid credentials")

            elif choice == "Register":
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")

                if password != confirm_password:
                    st.error("Passwords do not match")

                if st.button("Register"):
                    if self.dao.login(username):
                        st.error("Username already exists")
                    else:
                        self.create_user(username, password)
                        st.success("User registered successfully! Please log in.")

        if page == "Manage Process":
            if st.button('Start Iterative Process'):
                with st.spinner("Starting Iterative Process, please wait..."):
                    self.controller.run_process()
                    st.success(threading.enumerate())
            if st.button('Restart Iterative Process'):
                pass
            # dashboard showing the current iteration details(number of samples, status, number of pending validations)


        # Annotation Validation Page
        elif page == "Annotation Validation":
            if st.session_state.user:
                st.title(f"Welcome, {st.session_state.user.email}")
                self.display_annotations()
            else:
                st.error("Please log in to access this page.")

        # Upload Dataset Page
        elif page == "Upload Dataset":
            if st.session_state.user:
                st.title("Upload Dataset",)
                uploaded_file = st.file_uploader("Choose a CSV or JSON file", type=["csv", "json"])

                col_1, col_2 = st.columns(2)
                with col_1:
                    if st.button('Upload Annotated Dataset', help='This button will upload the dataset as part of the Golden set(i.e manually annotated)'):
                       self.upload_document(uploaded_file, True) 
                with col_2:
                    if st.button('Upload Dataset'):
                        self.upload_document(uploaded_file, False) 
            else:
                st.error("Please log in to access this page.")

        # Logout Handling
        if page == "Logout":
            if self.logout():
                st.success("Logged out successfully!")
                st.session_state.user = None
                st.rerun()  # Reload the app to update the sidebar

app = Application()
if __name__ == "__main__":
    app.main()
