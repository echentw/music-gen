import itertools

from lib.io import write_wavefile
from lib.tuning_systems import EQUAL_TEMPERAMENT, JUST_INTONATION
from lib.note_names import *

from music_gen import produce_sample, Note
from songs import twinkle, c_scale, chords


def li_ge(tuning_system):
    sustain_patterns = [4, 1.5, 1, 0.5, 2, 1.5, 1, 0.5]

    f_chord = [F3, C4, F4, C4, A4, C4, F4, C4]
    em_chord = [E3, B3, E4, B3, G4, B3, E4, B3]
    am_chord = [A3, E4, A4, E4, C5, E4, A4, E4]
    g_chord = [G3, D4, G4, D4, B4, D4, G4, D4]
    c_chord = [C4, G4, C5, G4, E5, G4, C5, G4]
    dm_chord = [D4, A4, D5, A4, F5, A4, D5, A4]

    harmony_notes = itertools.chain.from_iterable([
        zip(am_chord[:4], sustain_patterns[4:]),
        zip(f_chord, sustain_patterns),
        zip(em_chord, sustain_patterns),
        zip(am_chord, sustain_patterns),

        zip(am_chord, sustain_patterns),
        zip(f_chord, sustain_patterns),
        zip(g_chord, sustain_patterns),
        zip(c_chord, sustain_patterns),

        zip(c_chord, sustain_patterns),
        zip(dm_chord, sustain_patterns),
        zip(em_chord, sustain_patterns),
        zip(am_chord[:4], sustain_patterns[4:]),
        zip(g_chord[:4], sustain_patterns[4:]),

        zip(f_chord, sustain_patterns),
        zip(f_chord, sustain_patterns),
        zip(em_chord, sustain_patterns),
        zip(am_chord, sustain_patterns),
    ])

    melody_notes = [
        (A4, 1), (C5, 1),
        (D5, 1), (C5, 0.5), (A4, 1.5), (A4, 1),
        (A4, 2), (G4, 1.5), (A4, 0.5),
        (A4, 6),

        (A4, 1), (C5, 1),
        (D5, 1), (C5, 0.5), (A4, 1.5), (A4, 1),
        (A4, 2), (G4, 1.5), (E5, 0.5),
        (E5, 6),

        (E5, 1), (F5, 1),
        (E5, 3), (D5, 1),
        (B4, 2), (B4, 0.67), (C5, 0.67), (D5, 0.66),

        (D5, 1), (C5, 0.5), (B4, 1), (C5, 1.5),
        (B4, 1), (A4, 1), (A4, 1), (C5, 1),

        (D5, 1), (C5, 0.5), (A4, 1.5), (A4, 1),
        (A4, 2), (G4, 1.5), (A4, 0.5),
        (A4, 6),
    ]

    notes = []

    current_beat = 0.0
    for note_name, duration in harmony_notes:
        frequency = tuning_system.get_frequency(note_name)
        notes.append(
            Note(frequency, start=current_beat, end=current_beat + duration, intensity=0.1)
        )
        current_beat += 0.5

    current_beat = 0.0
    for note_name, duration in melody_notes:
        frequency = tuning_system.get_frequency(note_name)
        notes.append(
            Note(frequency, start=current_beat, end=current_beat + duration, intensity=0.5)
        )
        current_beat += duration

    return notes


notes = li_ge(tuning_system=JUST_INTONATION)
# notes = chords(tuning_system=JUST_INTONATION)
# notes = c_scale(tuning_system=JUST_INTONATION)
# notes = twinkle(tuning_system=JUST_INTONATION)

sample = produce_sample(notes, beats_per_minute=140)

with open('output.wav', 'wb') as f:
    write_wavefile(f, sample)
