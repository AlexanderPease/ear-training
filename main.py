import random
import time
import fluidsynth
import mido
import subprocess
from enum import Enum

TEMP_MIDI_FILE = "temp.midi"
SOUNDFONT_FILE = "soundfonts/Steinway_Model_D274_II.sf2"


class NoteDuration(Enum):
    WHOLE = 16
    HALF = 8
    QUARTER = 4
    EIGHTH = 2
    SIXTEENTH = 1

    PER_SECOND = 4


class Note:
    def __init__(self, pitch, duration, velocity=127):
        self.pitch = pitch
        self.duration = duration
        self.velocity = velocity


# class Melody:
#     def __init__(self, num_bars, notes=[], tempo=120):
#         self.num_bars = num_bars
#         self.notes = notes
#         self.tempo = tempo


# def play_melody(melody, tempo, synthID, seq):
#     tempo_factor = NoteDuration.PER_SECOND.value * 60 / tempo
#     beat_counter = 0
#     for note in melody:
#         seq.note_on(
#             absolute=False,
#             channel=0,
#             key=note.pitch,
#             velocity=note.velocity,
#             time=beat_counter / tempo_factor,
#             dest=synthID,
#         )
#         beat_counter += note.duration
#         seq.note_off(
#             absolute=False,
#             channel=0,
#             key=note.pitch,
#             time=beat_counter / tempo_factor,
#             dest=synthID,
#         )


# def play_melody(melody, tempo, synth, port):
#     import mido

#     ticks_per_beat = 480  # Assuming a standard MIDI ticks per beat value

#     # Calculate the time per tick based on the tempo
#     microseconds_per_beat = int(60 * 1e6 / tempo)
#     ticks_per_microsecond = ticks_per_beat / microseconds_per_beat

#     start_time = time.time()

#     # for note in melody:
#     note = melody[0]
#     note_start_time = start_time
#     note_end_time = start_time + 1000
#     # note_start_time = start_time + int(note.start_time / ticks_per_microsecond)
#     # note_end_time = start_time + int(note.end_time / ticks_per_microsecond)

#     # Schedule note-on event
#     on_msg = mido.Message(
#         "note_on", note=note.pitch, velocity=note.velocity, time=note_start_time
#     )
#     port.send(on_msg)

#     # Schedule note-off event
#     off_msg = mido.Message("note_off", note=note.pitch, velocity=0, time=note_end_time)
#     port.send(off_msg)


def write_melody_to_midi_file(melody, tempo, filename):
    ticks_per_beat = 480  # Assuming a standard MIDI ticks per beat value

    # Create a MIDI file object
    midifile = mido.MidiFile(ticks_per_beat=ticks_per_beat)

    # Add tempo meta message
    midifile.tempo = mido.bpm2tempo(tempo)

    # Create a MIDI track
    track = mido.MidiTrack()

    # Append track to the MIDI file
    midifile.tracks.append(track)

    for note in [melody[0]]:
        tick_start = 0
        tick_end = 480
        # tick_start = int(note.start_time)
        # tick_end = int(note.end_time)

        # Create note-on message
        msg_on = mido.Message(
            "note_on", note=note.pitch, velocity=note.velocity, time=tick_start
        )
        track.append(msg_on)

        # Create note-off message
        msg_off = mido.Message("note_off", note=note.pitch, velocity=0, time=tick_end)
        track.append(msg_off)

    # Save the MIDI file
    midifile.save(filename)


def play_midi_file(filename, soundfont):
    from timidity import Parser, play_notes
    import numpy as np

    ps = Parser(filename)

    play_notes(*ps.parse(), np.sin)

    # timidity_cmd = ["timidity", "-A", soundfont, filename]
    # subprocess.run(timidity_cmd)


# def play_midi_with_soundfont(midi_file, soundfont_file):
#     # Create the fluidsynth synthesizer
#     fs = fluidsynth.Synth()

#     # Load the soundfont
#     sfid = fs.sfload(soundfont_file)

#     # Connect the audio driver
#     fs.start(driver="coreaudio")

#     # Load and play the MIDI file
#     fs.midifile_load(midi_file, True)

#     # Wait until the MIDI file playback is finished
#     while fs.active():
#         pass

#     # Stop and delete the synthesizer
#     fs.stop()
#     fs.delete()


def generate_melody(
    bars, note_durations=[NoteDuration.HALF, NoteDuration.QUARTER, NoteDuration.EIGHTH]
):
    """Generates a melody for a certain number of bars."""
    MAJOR_SCALE = [0, 2, 4, 5, 7, 9, 11]
    note_pitches = [x + 60 for x in MAJOR_SCALE]  # C4 is 60

    total_duration = 16 * bars

    melody = []
    duration_counter = total_duration
    while duration_counter:
        note = Note(
            pitch=random.choice(note_pitches),
            duration=random.choice(note_durations).value,
        )

        # Ensure last note does not go too long
        if note.duration > duration_counter:
            note.duration = duration_counter

        melody.append(note)

        duration_counter -= note.duration
    return melody


if __name__ == "__main__":
    bars = 2
    note_durations = [NoteDuration.QUARTER]

    # Generate the melody
    melody = generate_melody(bars, note_durations)

    # Create the FluidSynth instance and load the SoundFont file
    # fs = fluidsynth.Synth()
    # fs.start()
    # sfid = fs.sfload(SOUNDFONT_FILE)
    # fs.program_select(0, sfid, 0, 0)

    # Sequencer
    # seq = fluidsynth.Sequencer()
    # synthID = seq.register_fluidsynth(fs)

    # Play the melody
    write_melody_to_midi_file(melody, 120, TEMP_MIDI_FILE)
    play_midi_file(TEMP_MIDI_FILE, SOUNDFONT_FILE)
    # play_midi_with_soundfont(TEMP_MIDI_FILE, SOUNDFONT_FILE)

    # Clean up and close the FluidSynth instance
    # fs.delete()
