NOTE_LETTERS = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
OCTAVES = [0, 1, 2, 3, 4, 5, 6, 7, 8]


note_names = [
    f'{note_letter}{octave}'
    for note_letter in NOTE_LETTERS
    for octave in OCTAVES
]


__all__ = note_names


for note_name in note_names:
    globals()[note_name] = note_name
