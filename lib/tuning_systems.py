class TuningSystem:
    def __init__(self, ref_note_name, ref_note_frequency, frequency_ratios):
        self.ref_note_name = ref_note_name
        self.ref_note_frequency = ref_note_frequency

        self.octave_ratio = frequency_ratios[-1]

        frequency_ratios = [1.0] + frequency_ratios[:-1]
        note_letters = ['C', 'D', 'E', 'F', 'G', 'A', 'B']

        self.note_values = {
            note_letter: value
            for note_letter, value in zip(note_letters, frequency_ratios)
        }

    def get_frequency(self, note_name):
        return self.ref_note_frequency * self.get_frequency_ratio(self.ref_note_name, note_name)

    def get_frequency_ratio(self, note_name1, note_name2):
        """
        Ex: note1 = 'C4', note2 = 'C5', return value = 2
        """
        letters = note_name1[0], note_name2[0]
        octaves = int(note_name1[1]), int(note_name2[1])
        return self._get_octave_ratio(*octaves) * self._get_note_letter_ratio(*letters)

    def _get_note_letter_ratio(self, note_letter1, note_letter2):
        """
        Returns the ratio of note_letter2 / note_letter1.
        Assumes the notes are in the same octave.
        """
        return self.note_values[note_letter2] / self.note_values[note_letter1]

    def _get_octave_ratio(self, octave1, octave2):
        return self.octave_ratio ** (octave2 - octave1)


JUST_INTONATION = TuningSystem(
    ref_note_name='A4',
    ref_note_frequency=440.0,
    frequency_ratios=[
        9/8,
        5/4,
        4/3,
        3/2,
        5/3,
        15/8,
        2,
    ]
)


EQUAL_TEMPERAMENT = TuningSystem(
    ref_note_name='A4',
    ref_note_frequency=440.0,
    frequency_ratios=[
        2 ** (1/12 * 2),
        2 ** (1/12 * 4),
        2 ** (1/12 * 5),
        2 ** (1/12 * 7),
        2 ** (1/12 * 9),
        2 ** (1/12 * 11),
        2,
    ]
)
