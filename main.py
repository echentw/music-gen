import itertools

from lib.io import write_wavefile
from lib.tuning_systems import EQUAL_TEMPERAMENT, JUST_INTONATION, PYTHAGOREAN_TUNING
from lib.note_names import *

from music_gen import produce_sample, Note
from songs import twinkle, c_scale, chords, li_ge



notes = li_ge(tuning_system=PYTHAGOREAN_TUNING)
# notes = chords(tuning_system=JUST_INTONATION)
# notes = c_scale(tuning_system=JUST_INTONATION)
# notes = twinkle(tuning_system=JUST_INTONATION)

sample = produce_sample(notes, beats_per_minute=140)

with open('output.wav', 'wb') as f:
    write_wavefile(f, sample)
