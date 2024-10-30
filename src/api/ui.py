import streamlit as st
import json
import random
import re
from  dao import MongoDAO
import pandas
from annotated_text import annotated_text
from i_entities import Annotator
from utils.loader import DatasetLoader
from utils.config_loader import ConfigLoader
from i_entities import ISample
from annotation import SequenceLabelAnnotation
from annotation import ClassificationAnnotation
from sample import SampleFactory
from api.controller import AnnotationController



class Application():
    
    def __init__(self):
        self.config = ConfigLoader('config.yaml')
        self.dao = MongoDAO(self.config.get('connection-string'), self.config.get('database-name'))
        self.controller = AnnotationController(None, self.dao, self.config)

        
    def login(self, username, password):
        annotator = Annotator(username, password)
        if self.dao.login(annotator):
            st.session_state.user = annotator
            return True
        return False

    def logout(self):
        if self.dao.logout(st.session_state.user):
            st.session_state.user = None
            return True
        return False

    def visualize_sequence_labels(text, annotations, title):
        # List of (entity, label) tuples to be highlighted
        st.header(title)
        display_text = []
        
        current_index = 0
        for ann in annotations:
            start, end, label = ann
            if start > current_index:
                display_text.append(text[current_index:start])  # add plain text before the entity
            
            # append the entity and its label
            display_text.append((text[start:end], label))
            
            current_index = end
        
        if current_index < len(text):
            display_text.append(text[current_index:])  # add remaining plain text
        
        annotated_text(*display_text)

    def display_aesthetic_text(self, text, title,  max_paragraph_length=200):
        st.header(title)
        sentences = re.split(r'(?<=[.!?]) +', text)
        
        paragraphs = []
        current_paragraph = ""
        
        for sentence in sentences:
            if len(current_paragraph) + len(sentence) <= max_paragraph_length:
                current_paragraph += sentence + " "
            else:
                paragraphs.append(current_paragraph.strip())
                current_paragraph = sentence + " "
        
        # Add the last paragraph if it's not empty
        if current_paragraph:
            paragraphs.append(current_paragraph.strip())
        
        # Display each paragraph in Streamlit
        for paragraph in paragraphs:
            st.markdown(f"<p style='text-align: justify;'>{paragraph}</p>", unsafe_allow_html=True)


    def fetch_pending_annotations(self):
        if self.controller.current_iteration is None:
            return None
        samples = self.dao.getPendingSamples(self.controller.current_iteration.id)
        
        if samples is []:
            return None
        return random.choice(samples)
        
    def validate_annotation(self, annotation, is_accepted):
        self.controller.validate_annotation(annotation, is_accepted)
        return True
    
    def show_annotation(self, sample: ISample):
        if isinstance(sample.labels, SequenceLabelAnnotation):
            self.visualize_sequence_labels(sample.text, sample.labels.get_value(), sample.labels.get_annotation_name())

        elif isinstance(sample.labels, ClassificationAnnotation):
            self.display_aesthetic_text(sample.text, 'Sample Text')
            st.markdown('---')
            self.display_aesthetic_text(sample.labels.get_value(), sample.labels.get_annotation_name())     

    def display_annotations(self):
        annotation = self.fetch_pending_annotations()
        if annotation:
            self.show_annotation(annotation)
            st.write(annotation['text'])  # Display annotation text
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Accept {annotation['id']}"):
                    if self.validate_annotation(annotation, True):
                        st.success("Validation submitted successfully!")
                    else:
                        st.error("Failed to submit validation.")
            with col2:
                if st.button(f"Reject {annotation['id']}"):
                    if self.validate_annotation(annotation, False):
                        st.success("Validation submitted successfully!")
                    else:
                        st.error("Failed to submit validation.")
        else:
            st.toast('There are no pending Annotations in this iteration.')
            
    def main(self):
        # Initialize session state
        if 'user' not in st.session_state:
            st.session_state.user = None

        # Sidebar for navigation
        st.sidebar.title("Navigation")
        if st.session_state.user is None:
            page = st.sidebar.radio("Select Page", ["Login"])
        else:
            page = st.sidebar.radio("Select Page", ["Annotation Validation", "Upload Dataset", "Logout"])

        # Login Page
        if page == "Login":
            st.title("Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type='password')
            if st.button("Login"):
                if self.login(username, password):
                    st.success("Logged in successfully!")
                    page = "Upload Dataset"
                else:
                    st.error("Login failed!")

        # Annotation Validation Page
        elif page == "Annotation Validation":
            if st.session_state.user:
                st.title(f"Welcome, {st.session_state.user._email}")
                self.display_annotations()
            else:
                st.error("Please log in to access this page.")

        # Upload Dataset Page
        elif page == "Upload Dataset":
            if st.session_state.user:
                st.title("Upload Dataset")
                uploaded_file = st.file_uploader("Choose a CSV or JSON file", type=["csv", "json"])

                if st.button("Upload"):
                    print(uploaded_file.__dict__)
                    if uploaded_file.type == "csv":	
                        filename = 'dataset.csv'
                        pandas.read_csv(uploaded_file).to_csv(filename)
                    else:
                        filename = 'dataset.json'
                        json.dump(uploaded_file, filename)
                    try:
                        samples = DatasetLoader(filename, SampleFactory(self.config).get_sample()).run()
                        self.dao.saveSamples(samples)
                    except:
                        st.error('Unable to save uploaded Dataset')
            else:
                st.error("Please log in to access this page.")

        # Logout Handling
        if page == "Logout":
            if self.logout():
                st.success("Logged out successfully!")
                st.session_state.user = None
                st.experimental_rerun()  # Reload the app to update the sidebar

if __name__ == "__main__":
    Application().main()
