import json
import streamlit as st

from utils.chord_progress_utils import create_chord_progression, process_chord_progression, validate_chords, validate_measure
from utils.file_utils import import_parameters_from_json
from utils.general_utils import calculate_num_chords_per_measure, generate_script, run_script

# Streamlit UI
st.title("Chordbase MIDI File Generator")

AUDIO_KEY_LIST = ["C", "C#", "Db", "D", "Eb", "E", "F", "F#", "Gb", "G", "Ab", "A", "Bb", "B",
    "Cm", "C#m", "Dm", "D#m", "Ebm", "Em", "Fm", "F#m", "Gm", "G#m", "Abm", "Am", "A#m", "Bbm", "Bm"]
TIME_SIGNITURE_LIST = ["4/4", "3/4", "6/8", "12/8"]
PITCH_RANGE_LIST = ["very_low", "low", "mid_low", "mid", "mid_high", "high", "very_high"]
NUM_MEASURES_LIST = [4, 8, 16]
INST_LIST = ["acoustic_piano", "string_ensemble", "accordion", "acoustic_bass", "acoustic_guitar", "banjo", "bassoon", "bell", 
    "brass_ensemble", "celesta", "choir", "clarinet", "drums_full", "drums_tops", "electric_bass", 
    "electric_guitar_clean", "electric_guitar_distortion", "electric_piano", "fiddle", "flute", 
    "glockenspiel", "harp", "harpsichord", "horn", "keyboard", "mandolin", "marimba", "nylon_guitar", 
    "oboe", "organ", "oud", "pad_synth", "percussion", "recorder", "sitar", "string_cello", 
    "string_double_bass", "string_viola", "string_violin", "synth_bass", 
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
    print(default_params)
    
st.markdown("---")

st.markdown("### Generate MIDI")
# User input fields
output_dir = st.text_input("Output Directory (저장 디렉토리)", value=default_params["output_dir"])
num_measures = st.selectbox(
    "Number of Measures (마디 수)",
    NUM_MEASURES_LIST,
    index=NUM_MEASURES_LIST.index(default_params["num_measures"])
)
bpm = st.number_input("BPM (Beats Per Minute)", min_value=1, max_value=300, step=1, value=default_params["bpm"])
audio_key = st.selectbox("Audio Key (음조)", AUDIO_KEY_LIST, index=AUDIO_KEY_LIST.index(default_params["audio_key"]))
time_signature = st.selectbox(
    "Time Signature (박자)",
    TIME_SIGNITURE_LIST,
    index=TIME_SIGNITURE_LIST.index(default_params["time_signature"])
)
pitch_range = st.selectbox(
    "Pitch Range (음역대)",
    PITCH_RANGE_LIST,
    index=PITCH_RANGE_LIST.index(default_params["pitch_range"])
)
inst = st.selectbox("Instrument (악기)", INST_LIST, index=INST_LIST.index(default_params["inst"]))
genre = st.selectbox("Genre (장르)", GENRE_LIST, index=GENRE_LIST.index(default_params["genre"]))
track_role = st.selectbox(
    "Track Role (트랙 역할)",
    TRACK_ROLE_LIST,
    index=TRACK_ROLE_LIST.index(default_params["track_role"])
)
rhythm = st.selectbox("Rhythm (리듬)", RHYTHM_LIST, index=RHYTHM_LIST.index(default_params["rhythm"]))
min_velocity = st.slider("Minimum Velocity", 1, 127, value=default_params["min_velocity"])
max_velocity = st.slider("Maximum Velocity", 1, 127, value=default_params["max_velocity"])
num_generate = st.number_input(
    "Number of Files to Generate (생성 파일 수)",
    min_value=1, step=1, value=default_params["num_generate"]
)
# top_k = st.number_input("Top K", min_value=1, step=1, value=default_params["top_k"], disabled=True)
# temperature = st.number_input("Temperature", min_value=0.1, step=0.1, value=default_params["temperature"], disabled=True)

st.markdown("#### Chord Progression (코드 진행)")
input_method = st.selectbox(
    "코드 진행 입력 방식을 선택하세요",
    ["default", "new"],
    format_func=lambda x: "기존 방식" if x == "default" else "새로운 방식(테스트 중)",
    index=0,
)

if input_method == "default":
    chord_progression = st.text_area(
        "Chord Progression (코드 진행)",
        placeholder="C-C-E-E-G-G ...",
        value=default_params["chord_progression"]
    )
elif input_method == "new":
    use_chord_input = st.checkbox("코드 입력 사용")
    chords = []
    measure_validation_results = [False] * num_measures
    chord_progression_list = []
    num_chords_per_measure = calculate_num_chords_per_measure(time_signature)
    for measure_num in range(num_measures):
        st.markdown(f"##### Measure {measure_num + 1}")
        if use_chord_input:
            measure_chords = [None] * num_chords_per_measure
            cols = st.columns(num_chords_per_measure)
            for col_num in range(num_chords_per_measure):
                with cols[col_num]:
                    measure_chords[col_num] = st.text_input(
                        f"Chord {col_num + 1}", 
                        key=f"measure_{measure_num}_chord_{col_num}"
                    )
            chord_validation_result = validate_chords(measure_chords)

            chords.append(measure_chords)

            measure_chord_value = create_chord_progression(measure_chords) if chord_validation_result else ""
        else:
            measure_chord_value = ""
        measure_chords_str = st.text_input(
            f"Chords",
            key=f"measure_{measure_num}_chords",
            value=measure_chord_value,
        )
        measure_validation_result = validate_measure(measure_chords_str, num_chords_per_measure)
        measure_validation_results[measure_num] = measure_validation_result
        chord_progression_list.append(measure_chords_str)

    chord_progression = '-'.join(chord_progression_list) if all(measure_validation_results) else ''

# Run Button
if st.button("Run", disabled=True):
    run_script(
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

st.text_area(
    "Output Chord Progression",
    value=process_chord_progression(input_chord_progression, time_signature),
    placeholder=process_chord_progression("Am-F-C-G", time_signature)
)

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
