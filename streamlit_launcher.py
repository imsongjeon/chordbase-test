import os
import subprocess
import sys

def launch_streamlit_app():
    # Use 'streamlit run' to launch this file as a Streamlit app
    subprocess.run([sys.executable, "-m", "streamlit", "run", "chordbase_streamlit_page.py"])

if __name__ == "__main__":
    launch_streamlit_app()