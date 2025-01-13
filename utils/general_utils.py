import streamlit as st
from datetime import datetime
from fractions import Fraction
import json
import subprocess


def calculate_num_chords_per_measure(time_signature):
    """
    Calculate the number of notes based on the number of measures and time signature.
    """
    return int(Fraction(time_signature) * 8)


def validate_parameters(num_measures, time_signature, chord_progression):
    """
    Function to validate the input parameters.
    """
    # if not os.path.exists(output_dir):
    #     st.error("Output directory does not exist.")
    #     return False
    if not chord_progression:
        st.error("Please complete the chord progression.")
        return False
    input_list = chord_progression.split('-')
    required_count = calculate_num_chords_per_measure(time_signature) * num_measures
    
    if len(input_list) != required_count:
        st.error(f"chord_progression has {len(input_list)} items but should have {required_count}.")
        return False
    
    return True


def generate_script(output_dir, bpm, audio_key, time_signature, pitch_range, num_measures, inst, genre,
                        track_role, rhythm, min_velocity, max_velocity, chord_progression, num_generate):
    if not validate_parameters(num_measures, time_signature, chord_progression):
          return
    command = [
        "python3", "generate.py",
        "--checkpoint_dir", "train/pretrained/checkpoint_best.pt",
        "--output_dir", output_dir
    ]
    # command = [
    #     "./chordbase-test",
    #     "--checkpoint_dir", "train/pretrained/checkpoint_best.pt",
    #     "--output_dir", output_dir
    # ]

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
