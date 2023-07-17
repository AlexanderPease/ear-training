import random
import mido
from enum import Enum

MIDI_BEAT = 480  # Standard MIDI ticks per beat value


class NoteDuration(Enum):
    WHOLE = 16
    HALF = 8
    QUARTER = 4
    EIGHTH = 2
    SIXTEENTH = 1

    PER_SECOND = 4


class NotePitch(Enum):
    C = 0
    CSHARP = 1
    D = 2
    DSHARP = 3
    E = 4
    F = 5
    FSHARP = 6
    G = 7
    GSHARP = 8
    A = 9
    ASHARP = 10
    B = 11


class Scale(Enum):
    MAJOR = [0, 2, 4, 5, 7, 9, 11]


class Note:
    def __init__(self, pitch, duration, velocity=127):
        self.pitch = pitch  # C4 = 60
        self.duration = duration  # NoteDuration
        self.velocity = velocity

    def __str__(self):
        return f"{NotePitch(self.pitch % 12).name} {NoteDuration(self.duration).name.capitalize()}"


class Rest(Note):
    def __init__(self, duration):
        self.duration = duration


class Chord(Note):
    def __init__(self, pitches):
        self.pitches = pitches


class Lesson:
    def __init__(self):
        self.melodies = []

    def write_to_midi_file(self, filename):
        # Create a MIDI file object
        midifile = mido.MidiFile(ticks_per_beat=MIDI_BEAT)

        # Add tempo meta message
        midifile.tempo = mido.bpm2tempo(self.melodies[0].tempo)

        # Create a MIDI track
        track = mido.MidiTrack()
        midifile.tracks.append(track)

        for melody in self.melodies:
            track = _write_notes_to_midi_track(track, melody.notes)

        midifile.save(filename)


class Melody:
    def __init__(
        self,
        num_bars,
        note_durations=[NoteDuration.HALF, NoteDuration.QUARTER, NoteDuration.EIGHTH],
        tempo=120,
    ):
        self.tempo = tempo
        self.notes = []

        # Vars for melody generation
        self.note_durations = note_durations
        self.num_bars = num_bars

        self.generate_melody()

    def generate_melody(self):
        """Generates a melody for a certain number of bars."""
        note_pitches = [x + 60 for x in Scale.MAJOR.value]  # C4 is 60

        total_duration = 16 * self.num_bars

        melody = []
        duration_counter = total_duration
        while duration_counter:
            note = Note(
                pitch=random.choice(note_pitches),
                duration=random.choice(self.note_durations).value,
            )

            # Ensure last note does not go too long
            if note.duration > duration_counter:
                note.duration = duration_counter

            melody.append(note)

            duration_counter -= note.duration
        self.notes = melody

    def write_to_midi_file(self, filename):
        # Create a MIDI file object
        midifile = mido.MidiFile(ticks_per_beat=MIDI_BEAT)

        # Add tempo meta message
        midifile.tempo = mido.bpm2tempo(self.tempo)

        # Create a MIDI track
        track = mido.MidiTrack()
        midifile.tracks.append(track)

        track = _write_notes_to_midi_track(track, self.notes)

        midifile.save(filename)


def _write_notes_to_midi_track(track, notes):
    for note in notes:
        print(note)

        # Create note-on message
        msg_on = mido.Message(
            "note_on", note=note.pitch, velocity=note.velocity, time=0
        )
        track.append(msg_on)

        # Create note-off message
        msg_off = mido.Message("note_off", note=note.pitch, velocity=0, time=MIDI_BEAT)
        track.append(msg_off)

    return track
