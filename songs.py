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



ALL_SONGS = {
    'twinkle': twinkle,
    'c_scale': c_scale,
    'chords': chords,
    'li_ge': li_ge
}
DEFAULT_SONG = 'li_ge'
assert DEFAULT_SONG in ALL_SONGS, 'default song not present in ALL_SONGS'
