from fractions import Fraction
import streamlit as st

def validate_chords(measure_chords: list) -> bool:
    err_msg_list = []
    for i, chord in enumerate(measure_chords):
        if not chord:
            if i == 0:
                err_msg_list.append(f"Chord 1은 필수 입력 항목입니다.")
            continue
        if not validate_chord_input(chord):
            err_msg_list.append(f"Chord {i + 1}: {chord}는 유효한 코드가 아닙니다.")

    if err_msg_list:
        st.error("\n\n".join(err_msg_list))
        return False
    return True


def validate_chord_input(chord: str) -> bool:
    CHORD_OPTIONS = ['C', 'C#', 'D', 'D#', 'E', 'F#', 'F', 'G', 'G#', 'A', 'A#', 'B']
    CHORD_QUALITY_OPTIONS = ['m', 'dim', 'm7', 'maj7', 'm7b5', 'dim7', 'sus4']

    for chord_option in CHORD_OPTIONS:
        if chord.startswith(chord_option):
            quality = chord[len(chord_option):]
            if '#' in quality:
                continue
            if quality in CHORD_QUALITY_OPTIONS or quality == '':
                return True
            else:
                return False
    return False


def validate_measure(measure_chords_str: str, num_chords_per_measure: int) -> bool:
    if not measure_chords_str:
        return False
    measure_chords = measure_chords_str.split('-')
    filtered_measure_chords = [chord for chord in measure_chords if chord.strip()]
    chord_count = len(filtered_measure_chords)
    if chord_count != num_chords_per_measure:
        st.error(f"{chord_count}개의 코드가 입력되었습니다. {num_chords_per_measure}개의 코드가 필요하며, 각 코드는 -(하이픈)으로 구분되어야 합니다.")
        return False
    if not validate_chords(measure_chords):
        return False
    return True


def create_chord_progression(measure_chords: list) -> str:
    for i, chord in enumerate(measure_chords):
        if not chord and i > 0:
            measure_chords[i] = measure_chords[i - 1]
    return '-'.join(measure_chords)



def process_chord_progression(input_chord_progression, time_signature):
    if not input_chord_progression:
        return ""
    input_list = input_chord_progression.split('-')
    output_list = []
    for chord in input_list:
        output_list.extend([chord] * int(Fraction(time_signature) * 8))
    return "-".join(output_list)