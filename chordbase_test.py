import sys
import streamlit as st
from datetime import datetime
from fractions import Fraction
import json
import subprocess
import os


def calculate_num_chords(num_measures, time_signature):
    """
    Calculate the number of notes based on the number of measures and time signature.
    """
    return num_measures * Fraction(time_signature) * 8
def import_parameters_from_json(uploaded_file):
    """
    Import parameters from a JSON file.
    """
    try:
        # Read and parse the JSON file
        parameters = json.load(uploaded_file)
        
        # Display the imported parameters
        st.success("File imported successfully!")
        return parameters
    except Exception as e:
        st.error(f"Error importing parameters: {e}")
        return {}


def validate_parameters(num_measures, time_signature, chord_progression):
    """
    Function to validate the input parameters.
    """
    # if not os.path.exists(output_dir):
    #     st.error("Output directory does not exist.")
    #     return False
    input_list = chord_progression.split('-')
    required_count = calculate_num_chords(num_measures, time_signature)
    
    if len(input_list) != required_count:
        st.error(f"chord_progression has {len(input_list)} items but should have {required_count}.")
        return False
    
    return True


def generate_script(output_dir, bpm, audio_key, time_signature, pitch_range, num_measures, inst, genre,
                        track_role, rhythm, min_velocity, max_velocity, chord_progression, num_generate):
    if not validate_parameters(num_measures, time_signature, chord_progression):
          return
    # command = [
    #     "python3", "generate.py",
    #     "--checkpoint_dir", "train/pretrained/checkpoint_best.pt",
    #     "--output_dir", output_dir
    # ]
    command = [
        "./chordbase-test",
        "--checkpoint_dir", "train/pretrained/checkpoint_best.pt",
        "--output_dir", output_dir
    ]

    command += ["--bpm", str(bpm)]
    command += ["--audio_key", audio_key]
    command += ["--time_signature", time_signature]
    command += ["--pitch_range", pitch_range]
    command += ["--num_measures", str(num_measures)]
    command += ["--inst", inst]
    command += ["--genre", genre]
    command += ["--track_role", track_role]
    command += ["--rhythm", rhythm]
    command += ["--min_velocity", str(min_velocity)]
    command += ["--max_velocity", str(max_velocity)]
    command += ["--chord_progression", chord_progression]
    command += ["--num_generate", str(num_generate)]
    # command += ["--top_k", str(top_k)]
    # command += ["--temperature", str(temperature)]
    return command


def run_generate_script(output_dir, bpm, audio_key, time_signature, pitch_range, num_measures, inst, genre,
                        track_role, rhythm, min_velocity, max_velocity, chord_progression, num_generate):
    """
    Function to run the generate.py script with the selected parameters.
    """
    # Generate the command
    command = generate_script(output_dir, bpm, audio_key, time_signature, pitch_range, num_measures, inst, genre,
                        track_role, rhythm, min_velocity, max_velocity, chord_progression, num_generate)
    # Run the script
    print("Running command:", command)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.success(f"[{current_time}] Generating MIDI files. Please wait...")

    result = subprocess.run(command, capture_output=True, text=True)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if result.returncode == 0:
        st.success(f"[{current_time}] File generated successfully in the output directory: {output_dir}")
    else:
        st.error(f"[{current_time}] Error: {result.stderr}")


# Streamlit UI
st.title("Chordbase MIDI File Generator")

AUDIO_KEY_LIST = ["C", "C#", "Db", "D", "Eb", "E", "F", "F#", "Gb", "G", "Ab", "A", "Bb", "B",
    "Cm", "C#m", "Dm", "D#m", "Ebm", "Em", "Fm", "F#m", "Gm", "G#m", "Abm", "Am", "A#m", "Bbm", "Bm"]
TIME_SIGNITURE_LIST = ["4/4", "3/4", "6/8", "12/8"]
PITCH_RANGE_LIST = ["very_low", "low", "mid_low", "mid", "mid_high", "high", "very_high"]
NUM_MEASURES_LIST = [4, 8, 16]
INST_LIST = ["accordion", "acoustic_bass", "acoustic_guitar", "acoustic_piano", "banjo", "bassoon", "bell", 
    "brass_ensemble", "celesta", "choir", "clarinet", "drums_full", "drums_tops", "electric_bass", 
    "electric_guitar_clean", "electric_guitar_distortion", "electric_piano", "fiddle", "flute", 
    "glockenspiel", "harp", "harpsichord", "horn", "keyboard", "mandolin", "marimba", "nylon_guitar", 
    "oboe", "organ", "oud", "pad_synth", "percussion", "recorder", "sitar", "string_cello", 
    "string_double_bass", "string_ensemble", "string_viola", "string_violin", "synth_bass", 
    "synth_bass_808", "synth_bass_wobble", "synth_bell", "synth_lead", "synth_pad", "synth_pluck", 
    "synth_voice", "timpani", "trombone", "trumpet", "tuba", "ukulele", "vibraphone", "whistle", 
    "xylophone", "zither", "orgel", "synth_brass", "sax", "bamboo_flute", "yanggeum", "vocal"]
GENRE_LIST = ["newage", "cinematic"]
TRACK_ROLE_LIST = ["main_melody", "sub_melody", "accompaniment", "bass", "pad", "riff"]
RHYTHM_LIST = ["standard", "triplet"]


default_params = {
    "output_dir": "./output",
    "bpm": 120,
    "audio_key": "C",
    "time_signature": "4/4",
    "pitch_range": "mid",
    "num_measures": 8,
    "inst": "acoustic_piano",
    "genre": "newage",
    "track_role": "main_melody",
    "rhythm": "standard",
    "min_velocity": 70,
    "max_velocity": 100,
    "chord_progression": "",
    "num_generate": 1,
    # "top_k": 1,
    # "temperature": 1.0,
}

st.markdown("### Import Parameters")
uploaded_file = st.file_uploader("Choose a file to import parameters", type=["json"])
if uploaded_file is not None:
    imported_params = import_parameters_from_json(uploaded_file)
    default_params.update(imported_params)
    
st.markdown("---")
st.markdown("### Generate MIDI")
# User input fields
output_dir = st.text_input("Output Directory", value=default_params["output_dir"])
bpm = st.number_input("BPM (Beats Per Minute)", min_value=1, max_value=300, step=1, value=default_params["bpm"])
audio_key = st.selectbox("Audio Key", AUDIO_KEY_LIST, index=AUDIO_KEY_LIST.index(default_params["audio_key"]))
time_signature = st.selectbox("Time Signature", TIME_SIGNITURE_LIST, index=TIME_SIGNITURE_LIST.index(default_params["time_signature"]))
pitch_range = st.selectbox("Pitch Range", PITCH_RANGE_LIST, index=PITCH_RANGE_LIST.index(default_params["pitch_range"]))
num_measures = st.selectbox("Number of Measures", NUM_MEASURES_LIST, index=NUM_MEASURES_LIST.index(default_params["num_measures"]))
inst = st.selectbox("Instrument", INST_LIST, index=INST_LIST.index(default_params["inst"]))
genre = st.selectbox("Genre", GENRE_LIST, index=GENRE_LIST.index(default_params["genre"]))
track_role = st.selectbox("Track Role", TRACK_ROLE_LIST, index=TRACK_ROLE_LIST.index(default_params["track_role"]))
rhythm = st.selectbox("Rhythm", RHYTHM_LIST, index=RHYTHM_LIST.index(default_params["rhythm"]))
min_velocity = st.slider("Minimum Velocity", 1, 127, value=default_params["min_velocity"])
max_velocity = st.slider("Maximum Velocity", 1, 127, value=default_params["max_velocity"])
chord_progression = st.text_area("Chord Progression", placeholder="C-C-E-E-G-G ...", value=default_params["chord_progression"])
num_generate = st.number_input("Number of Files to Generate", min_value=1, step=1, value=default_params["num_generate"])
# top_k = st.number_input("Top K", min_value=1, step=1, value=default_params["top_k"], disabled=True)
# temperature = st.number_input("Temperature", min_value=0.1, step=0.1, value=default_params["temperature"], disabled=True)

# Run Button
if st.button("Run", disabled=True):
    run_generate_script(
        output_dir=output_dir,
        bpm=bpm,
        audio_key=audio_key,
        time_signature=time_signature,
        pitch_range=pitch_range,
        num_measures=num_measures,
        inst=inst,
        genre=genre,
        track_role=track_role,
        rhythm=rhythm,
        min_velocity=min_velocity,
        max_velocity=max_velocity,
        chord_progression=chord_progression,
        num_generate=num_generate,
        # top_k=top_k,
        # temperature=temperature
    )

if st.button("Create Script", disabled=False):
    command = generate_script(
        output_dir=output_dir,
        bpm=bpm,
        audio_key=audio_key,
        time_signature=time_signature,
        pitch_range=pitch_range,
        num_measures=num_measures,
        inst=inst,
        genre=genre,
        track_role=track_role,
        rhythm=rhythm,
        min_velocity=min_velocity,
        max_velocity=max_velocity,
        chord_progression=chord_progression,
        num_generate=num_generate,
        # top_k=top_k,
        # temperature=temperature
    )
    if command:
        st.text_area("Script", value=" ".join(command), height=200)

st.markdown("---")
st.markdown("### Chord Progression Tool")
input_chord_progression = st.text_input("Input Chord Progression", placeholder="Am-F-C-G")

def process_chord_progression(input_chord_progression, time_signature):
    if not input_chord_progression:
        return ""
    input_list = input_chord_progression.split('-')
    output_list = []
    for chord in input_list:
        output_list.extend([chord] * int(Fraction(time_signature) * 8))
    return "-".join(output_list)

st.text_area("Output Chord Progression", value=process_chord_progression(input_chord_progression, time_signature), placeholder=process_chord_progression("Am-F-C-G", time_signature))

st.markdown("---")
st.markdown("### Export Parameters")
parameters = {
    "output_dir": output_dir,
    "bpm": bpm,
    "audio_key": audio_key,
    "time_signature": time_signature,
    "pitch_range": pitch_range,
    "num_measures": num_measures,
    "inst": inst,
    "genre": genre,
    "track_role": track_role,
    "rhythm": rhythm,
    "min_velocity": min_velocity,
    "max_velocity": max_velocity,
    "chord_progression": chord_progression,
    "num_generate": num_generate,
    # "top_k": top_k,
    # "temperature": temperature
}
export_file_name = st.text_input("Enter export file name (without extension):", value="export")
st.download_button("Download", json.dumps(parameters, indent=4), f"{export_file_name}.json")
