import random
import time

import fluidsynth

# from fluidsynth.fluidsynth import FluidSynth

SOUNDFONT_FILE = "soundfonts/Steinway_Model_D274_II.sf2"


def play_melody(melody, tempo, fs):
    for note in melody:
        fs.noteon(0, note[0], 127)
        time.sleep(note[1])
        fs.noteoff(0, note[0])


def generate_melody(num_notes, note_duration, scale):
    melody = []
    for i in range(num_notes):
        pitch = random.choice(scale) + 60
        start_time = i * note_duration
        end_time = start_time + note_duration
        melody.append((pitch, end_time))
    return melody


if __name__ == "__main__":
    # Set the key signature and scale for F major
    key_signature = 5  # F major
    scale = [0, 2, 4, 5, 7, 9, 11]  # F G A Bb C D E

    # Set the number of notes in the melody and the duration of each note
    num_notes = 16
    note_duration = 0.5  # In seconds

    # Set the tempo (beats per minute)
    tempo = 120

    # Generate the melody
    melody = generate_melody(num_notes, note_duration, scale)

    # Create the FluidSynth instance and load the SoundFont file
    # print("FluidSynth version:", fluidsynth)
    fs = fluidsynth.Synth()
    fs.start()
    sfid = fs.sfload(SOUNDFONT_FILE)
    fs.program_select(0, sfid, 0, 0)

    # Play the melody
    play_melody(melody, tempo, fs)

    # Clean up and close the FluidSynth instance
    fs.delete()
