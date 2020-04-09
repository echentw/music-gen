import itertools

from lib.note_names import *
from music_gen import Note


def twinkle(tuning_system):
    harmony_notes = [
        C3, G3, E3, G3,
        C3, G3, E3, G3,
        C3, A3, F3, A3,
        C3, G3, E3, G3,

        B2, G3, D3, G3,
        C3, G3, E3, G3,
        B2, G3, D3, G3,
        C3, G3, E3, G3,
    ]

    melody_notes = [
        (C4, 1),
        (C4, 1),
        (G4, 1),
        (G4, 1),
        (A4, 1),
        (A4, 1),
        (G4, 2),

        (F4, 1),
        (F4, 1),
        (E4, 1),
        (E4, 1),
        (D4, 1),
        (D4, 1),
        (C4, 2),
    ]

    notes = []

    current_beat = 0.0
    for note_name in harmony_notes:
        frequency = tuning_system.get_frequency(note_name)
        notes.append(
            Note(frequency, current_beat, current_beat + 0.5)
        )
        current_beat += 0.5

    current_beat = 0.0
    for note_name, duration in melody_notes:
        frequency = tuning_system.get_frequency(note_name)
        notes.append(
            Note(frequency, current_beat, current_beat + duration)
        )
        current_beat += duration

    return notes


def c_scale(tuning_system):
    return [
        Note(tuning_system.get_frequency(C3), 0, 1),
        Note(tuning_system.get_frequency(D3), 1, 2),
        Note(tuning_system.get_frequency(E3), 2, 3),
        Note(tuning_system.get_frequency(F3), 3, 4),
        Note(tuning_system.get_frequency(G3), 4, 5),
        Note(tuning_system.get_frequency(A3), 5, 6),
        Note(tuning_system.get_frequency(B3), 6, 7),
        Note(tuning_system.get_frequency(C4), 7, 8)
    ]


def chords(tuning_system):
    chords = [
        (C4, E4, G4),
        (C4, F4, A4),
        (C4, E4, G4),
        (B3, D4, G4),
        (C4, E4, G4),
    ]

    duration = 1.5

    return itertools.chain.from_iterable(
        (
            Note(
                tuning_system.get_frequency(note_name),
                duration * i,
                duration * (i + 1)
            )
            for note_name in chord_note_names
        )
        for chord_note_names, i in zip(chords, itertools.count(0))
    )
