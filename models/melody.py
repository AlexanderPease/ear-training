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

    @property
    def midi_ticks(self):
        return int(self.value * MIDI_BEAT / NoteDuration.QUARTER.value)


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
    MINOR = [0, 2, 3, 5, 7, 8, 10]


class Note:
    def __init__(self, pitch, duration, velocity=127):
        self.pitch = pitch  # NotePitch; C4 = 60
        self.duration = duration  # NoteDuration
        self.velocity = velocity

    def __str__(self):
        return f"{NotePitch(self.pitch % 12).name} {NoteDuration(self.duration).name.capitalize()}"

    def write_to_midi_track(self, track, start_tick):
        msg_on = mido.Message(
            "note_on", note=self.pitch, velocity=self.velocity, time=start_tick
        )
        track.append(msg_on)

        msg_off = mido.Message(
            "note_off", note=self.pitch, time=self.duration.midi_ticks
        )
        track.append(msg_off)

        start_time = 0  # Notes do not delay the subsequent note's start time
        return track, start_time


class Rest(Note):
    def __init__(self, duration):
        self.duration = duration

    def write_to_midi_track(self, track, start_tick):
        return track, start_tick + self.duration.midi_ticks


class Lesson:
    def __init__(self, tempo=120, interstitial_notes=[]):
        self.melodies = []
        self.tempo = tempo
        self.interstitial_notes = interstitial_notes

    def write_to_midi_file(self, filename):
        # Create a MIDI file object
        midifile = mido.MidiFile(ticks_per_beat=MIDI_BEAT)

        # Create a MIDI track
        track = mido.MidiTrack()
        midifile.tracks.append(track)

        # Set tempo
        midi_tempo = mido.bpm2tempo(self.tempo)
        track.append(mido.MetaMessage("set_tempo", tempo=midi_tempo))

        start_tick = 0
        for melody in self.melodies:
            for note in melody.notes:
                track, start_tick = note.write_to_midi_track(track, start_tick)

            # TODO if last melody, break
            for note in self.interstitial_notes:
                track, start_tick = note.write_to_midi_track(track, start_tick)

        midifile.save(filename)


class Melody:
    def __init__(
        self,
        num_bars,
        note_durations=[NoteDuration.HALF, NoteDuration.QUARTER, NoteDuration.EIGHTH],
        key=NotePitch.C,
        scale=Scale.MAJOR,
    ):
        self.key = key.value
        self.scale = scale.value

        # Vars for melody generation
        self.note_durations = note_durations
        self.num_bars = num_bars

        self.notes = self._generate_melody()

    def _generate_melody(self):
        """Generates a melody for a certain number of bars."""
        note_pitches = [x + self.key + 60 for x in self.scale]  # C4 is 60

        total_duration = 16 * self.num_bars

        melody = []
        duration_counter = total_duration
        while duration_counter:
            note = Note(
                pitch=random.choice(note_pitches),
                duration=random.choice(self.note_durations),
            )

            # Ensure last note does not go too long
            if note.duration.value > duration_counter:
                continue

            melody.append(note)

            duration_counter -= note.duration.value
        return melody
