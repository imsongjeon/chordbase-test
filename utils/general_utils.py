import streamlit as st
from datetime import datetime
from fractions import Fraction
import json
import subprocess


def calculate_num_chords_per_measure(time_signature: str) -> int:
    """
    Calculate the number of notes based on the number of measures and time signature.
    """
    return int(Fraction(time_signature) * 8)


def validate_parameters(num_measures: int, time_signature: str, chord_progression: str) -> bool:
    """
    Function to validate the input parameters.
    """
    # if not os.path.exists(output_dir):
    #     st.error("Output directory does not exist.")
    #     return False
    if not chord_progression:
        st.error("코드 진행을 완성해 주세요.")
        return False
    input_list = chord_progression.split('-')
    required_count = calculate_num_chords_per_measure(time_signature) * num_measures
    
    if len(input_list) != required_count:
        st.error(f"현재 코드 진행에는 {len(input_list)}개의 코드가 있지만, {required_count}개가 있어야 합니다.")
        return False
    
    return True


def generate_script(
        output_dir: str,
        bpm: int,
        audio_key: str,
        time_signature: str,
        pitch_range: str,
        num_measures: int,
        inst: str,
        genre: str,
        track_role: str,
        rhythm: str,
        min_velocity: int,
        max_velocity: int,
        chord_progression: str,
        num_generate: int,
        use_python: bool = False,
    ) -> list:
    if not validate_parameters(num_measures, time_signature, chord_progression):
          return
    if use_python:
        command = [
            "python3", "generate.py",
            "--checkpoint_dir", "train/pretrained/checkpoint_best.pt",
            "--output_dir", output_dir
        ]
    else:
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


def run_script(
    output_dir: str,
    bpm: int,
    audio_key: str,
    time_signature: str,
    pitch_range: str,
    num_measures: int,
    inst: str,
    genre: str,
    track_role: str,
    rhythm: str,
    min_velocity: int,
    max_velocity: int,
    chord_progression: str,
    num_generate: int,
) -> None:
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
