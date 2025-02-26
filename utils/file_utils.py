import json
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile

def import_parameters_from_json(uploaded_file: UploadedFile) -> dict:
    """
    Import parameters from a JSON file.
    """
    try:
        # Read and parse the JSON file
        parameters = json.load(uploaded_file)
        
        # Display the imported parameters
        st.success("File imported successfully!")
        print("Imported parameters:", parameters)
        return parameters
    except Exception as e:
        st.error(f"Error importing parameters: {e}")
        return {}