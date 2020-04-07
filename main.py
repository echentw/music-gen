import sys
import wave
import math
import itertools
import functools
import struct
from typing import Iterable


def decay(ratio: float = 0.9997):
    def func(ratio, n):
        return ratio ** n

    partial_func = functools.partial(func, ratio)

    return map(func, itertools.count(0))


# def decay_func(frame_index, total_frames):
#     


def sine_wave(frequency, framerate=44100, amplitude=0.5, decay_factor=1.0):
    period = framerate / frequency
    amplitude = min(max(amplitude, 0.0), 1.0)
    return (
        (decay_factor ** frame) * amplitude * math.sin(2.0 * math.pi * frame / period)
        for frame in itertools.count(0)
    )


def write_wavefile(f, samples, nframes=None, nchannels=2, sampwidth=2, framerate=44100, bufsize=2048):
    def grouper(n, iterable, fillvalue=None):
        "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
        args = [iter(iterable)] * n
        return itertools.zip_longest(fillvalue=fillvalue, *args)

    "Write samples to a wavefile."
    if nframes is None:
        nframes = 0

    w = wave.open(f, 'wb')
    w.setparams((nchannels, sampwidth, framerate, nframes, 'NONE', 'not compressed'))

    max_amplitude = float(int((2 ** (sampwidth * 8)) / 2) - 1)

    # split the samples into chunks (to reduce memory consumption and improve performance)
    for chunk in grouper(bufsize, samples):
        frames = b''.join(b''.join(struct.pack('h', int(max_amplitude * sample)) for sample in channels) for channels in chunk if channels is not None)
        w.writeframesraw(frames)

    w.close()


class Note:
    def __init__(self, frequency, start, end):
        self.frequency = frequency
        self.start = start
        self.end = end

    def __eq__(self, other):
        return (
            self.frequency == other.frequency and 
            self.start == other.start and
            self.end == other.end
        )

    def __hash__(self):
        return hash((self.frequency, self.start, self.end))


def get_sample(notes, beats_per_minute=60, framerate=44100):
    beats_to_frame_factor = int(60 / beats_per_minute * framerate)

    all_notes = []
    for note in notes:
        all_notes.append((note.start * beats_to_frame_factor, note))
        all_notes.append((note.end * beats_to_frame_factor, note))
    all_notes = sorted(all_notes, key=lambda x: x[0])

    all_notes_index = 0

    current_waves = dict()

    total_frames = int(all_notes[-1][0])

    for frame_index in range(total_frames + 1):
        # First, update current_waves
        while all_notes_index < len(all_notes) and all_notes[all_notes_index][0] <= frame_index:
            note = all_notes[all_notes_index][1]
            if note in current_waves:
                del current_waves[note]
            else:
                current_waves[note] = sine_wave(note.frequency, amplitude=0.1, decay_factor=0.99998)
                # current_waves[note] = sine_wave(note.frequency, amplitude=0.2)
            all_notes_index += 1

        # Second, yield the next sound data
        amplitude = 0.0
        for wave in current_waves.values():
            amplitude += next(wave)

        yield (amplitude, amplitude)


just_intonation = [
    9/8,
    5/4,
    4/3,
    3/2,
    5/3,
    15/8,
    2,
]

equal_temperament = [
    2 ** (1/12 * 2),
    2 ** (1/12 * 4),
    2 ** (1/12 * 5),
    2 ** (1/12 * 7),
    2 ** (1/12 * 9),
    2 ** (1/12 * 11),
    2,
]

frequency_ratios = just_intonation
# frequency_ratios = equal_temperament


C1 = 261.63

B0 = C1 * frequency_ratios[5] / frequency_ratios[6]

D1 = C1 * frequency_ratios[0]
E1 = C1 * frequency_ratios[1]
F1 = C1 * frequency_ratios[2]
G1 = C1 * frequency_ratios[3]
A1 = C1 * frequency_ratios[4]
B1 = C1 * frequency_ratios[5]

C2 = C1 * frequency_ratios[6]
D2 = C2 * frequency_ratios[0]
E2 = C2 * frequency_ratios[1]
F2 = C2 * frequency_ratios[2]
G2 = C2 * frequency_ratios[3]
A2 = C2 * frequency_ratios[4]
B2 = C2 * frequency_ratios[5]

def twinkle():
    harmony_notes = [
        C1, G1, E1, G1,
        C1, G1, E1, G1,
        C1, A1, F1, A1,
        C1, G1, E1, G1,

        B0, G1, D1, G1,
        C1, G1, E1, G1,
        B0, G1, D1, G1,
        C1, G1, E1, G1,
    ]

    melody_notes = [
        (C2, 1),
        (C2, 1),
        (G2, 1),
        (G2, 1),
        (A2, 1),
        (A2, 1),
        (G2, 2),

        (F2, 1),
        (F2, 1),
        (E2, 1),
        (E2, 1),
        (D2, 1),
        (D2, 1),
        (C2, 2),
    ]

    notes = []

    current_beat = 0.0
    for frequency in harmony_notes:
        notes.append(
            Note(frequency, current_beat, current_beat + 0.5)
        )
        current_beat += 0.5

    current_beat = 0.0
    for frequency, duration in melody_notes:
        notes.append(
            Note(frequency, current_beat, current_beat + duration)
        )
        current_beat += duration

    return notes


def c_scale():
    return [
        Note(C1, 0, 1),
        Note(D1, 1, 2),
        Note(E1, 2, 3),
        Note(F1, 3, 4),
        Note(G1, 4, 5),
        Note(A1, 5, 6),
        Note(B1, 6, 7),
        Note(C2, 7, 8)
    ]


def chords():
    return [
        # Note(B0, 0, 3),
        # Note(D1, 0, 3),
        # Note(G1, 0, 3),
        # Note(D2, 0, 3),

        Note(C1, 0, 1), Note(E1, 0, 1), Note(G1, 0, 1),
        Note(C1, 1, 2), Note(F1, 1, 2), Note(A1, 1, 2),
        Note(C1, 2, 3), Note(E1, 2, 3), Note(G1, 2, 3),
        Note(B0, 3, 4), Note(D1, 3, 4), Note(G1, 3, 4),
        Note(C1, 4, 6), Note(E1, 4, 6), Note(G1, 4, 6),
    ]



notes = twinkle()
sample = get_sample(notes, beats_per_minute=80)
with open('output.wav', 'wb') as f:
    write_wavefile(f, sample)
