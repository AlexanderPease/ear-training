import time
import fluidsynth
import mido
import pygame


from models.melody import Melody, Lesson, NoteDuration

TEMP_MIDI_FILE = "temp.midi"
SOUNDFONT_FILE = "soundfonts/Steinway_Model_D274_II.sf2"


def play_midi_file(filename):
    """Plays midi file with sine waves."""
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        # check if playback has finished
        time.sleep(1)

    pygame.mixer.quit()


def play_midi_file_with_soundfont(filename, soundfont):
    """Plays midi file with soundfont.
    TODO: No errors, but also no sound."""
    fs = fluidsynth.Synth(soundfont)

    mid = mido.MidiFile(filename)
    print(mid)
    for i, track in enumerate(mid.tracks):
        print("Track {}: {}".format(i, track.name))
        for msg in track:
            print(msg)
            if not msg.is_meta:
                data = msg.dict()
                fs.noteon(0, data["note"], data["velocity"])
                fs.noteoff(0, data["note"])


if __name__ == "__main__":
    # Generate the melody
    lesson = Lesson()
    for i in range(10):
        melody = Melody(num_bars=1, note_durations=[NoteDuration.QUARTER], tempo=120)
        lesson.melodies.append(melody)
    lesson.write_to_midi_file(TEMP_MIDI_FILE)
    # melody = Melody(num_bars=1, note_durations=[NoteDuration.QUARTER], tempo=120)
    # melody.write_to_midi_file(TEMP_MIDI_FILE)

    # Play the melody
    play_midi_file(TEMP_MIDI_FILE)
    # play_midi_file_with_soundfont(TEMP_MIDI_FILE, SOUNDFONT_FILE)
