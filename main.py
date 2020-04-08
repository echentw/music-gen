import sys
import wave
import math
import itertools
import functools
import struct
from typing import Iterable


def decay_generator(total_frames):
    decay_factor = 0.99996

    start_frames = 500
    end_frames = 1000
    middle_frames = total_frames - start_frames - end_frames

    for i in range(start_frames):
        yield i / start_frames

    for i in range(middle_frames):
        yield decay_factor ** i

    last_decayed_value = decay_factor ** middle_frames

    for i in range(end_frames):
        yield last_decayed_value * (end_frames - i - 1) / end_frames

    while True:
        yield 0


def sine_wave_generator(frequency, amplitude=0.2, framerate=44100):
    period = framerate / frequency
    amplitude = min(max(amplitude, 0.0), 1.0)
    return (
        amplitude * math.sin(2.0 * math.pi * frame / period)
        for frame in itertools.count(0)
    )


def square_wave_generator(frequency, amplitude=0.2, framerate=44100):
    def sign(x):
        return 1 if x >= 0 else -1

    amplitude = min(max(amplitude, 0.0), 1.0)
    sine_wave = sine_wave_generator(frequency, amplitude=amplitude, framerate=framerate)
    return (
        amplitude * sign(value)
        for value in sine_wave
    )


def sawtooth_wave_generator(frequency, amplitude=0.2, framerate=44100):
    period = framerate / frequency
    amplitude = min(max(amplitude, 0.0), 1.0)

    def sawtooth(x):
        return 2 * ((x / period) - math.floor(x / period)) - 1

    return (
        amplitude * sawtooth(frame)
        for frame in itertools.count(0)
    )


def wave_generator(frequency, duration_frames, amplitude=0.2, framerate=44100):
    wave_iter = sine_wave_generator(frequency, amplitude=amplitude, framerate=framerate)
    # wave_iter = square_wave_generator(frequency, amplitude=amplitude, framerate=framerate)
    # wave_iter = sawtooth_wave_generator(frequency, amplitude=amplitude, framerate=framerate)
    decay_iter = decay_generator(duration_frames)
    return (
        decay_factor * value
        for decay_factor, value in zip(decay_iter, wave_iter)
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
    # intensity is the same as amplitude
    def __init__(self, frequency, start, end, intensity=0.2):
        self.frequency = frequency
        self.start = start
        self.end = end
        self.intensity = intensity

    def duration_frames(self, beats_per_minute, framerate=44100):
        beats_to_frame_factor = int(60 / beats_per_minute * framerate)
        start_frame = int(math.floor(self.start * beats_to_frame_factor))
        end_frame = int(math.ceil(self.end * beats_to_frame_factor))
        return end_frame - start_frame + 1

    def __eq__(self, other):
        return (
            self.frequency == other.frequency and
            self.start == other.start and
            self.end == other.end and
            self.intensity == other.intensity
        )

    def __hash__(self):
        return hash((self.frequency, self.start, self.end, self.intensity))


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
                current_waves[note] = wave_generator(
                    note.frequency,
                    note.duration_frames(beats_per_minute=beats_per_minute, framerate=framerate),
                    amplitude=note.intensity
                )
            all_notes_index += 1

        # Second, yield the next sound data
        value = 0.0
        for wave in current_waves.values():
            value += next(wave)

        value = min(max(value, -1.0), 1.0)

        yield (value, value)


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

C0 = 261.63
D0 = C0 * frequency_ratios[0]
E0 = C0 * frequency_ratios[1]
F0 = C0 * frequency_ratios[2]
G0 = C0 * frequency_ratios[3]
A0 = C0 * frequency_ratios[4]
B0 = C0 * frequency_ratios[5]

C1 = C0 * frequency_ratios[6]
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

C3 = C2 * frequency_ratios[6]
D3 = C3 * frequency_ratios[0]
E3 = C3 * frequency_ratios[1]
F3 = C3 * frequency_ratios[2]
G3 = C3 * frequency_ratios[3]
A3 = C3 * frequency_ratios[4]
B3 = C3 * frequency_ratios[5]


def li_ge():
    sustain_patterns = [4, 1.5, 1, 0.5, 2, 1.5, 1, 0.5]

    f_chord = [F0, C1, F1, C1, A1, C1, F1, C1]
    em_chord = [E0, B0, E1, B0, G1, B0, E1, B0]
    am_chord = [A0, E1, A1, E1, C2, E1, A1, E1]
    g_chord = [G0, D1, G1, D1, B1, D1, G1, D1]
    c_chord = [C1, G1, C2, G1, E2, G1, C2, G1]

    harmony_notes = itertools.chain.from_iterable([
        [(A0, 2), (E1, 1.5), (A1, 1), (E1, 0.5)],
        zip(f_chord, sustain_patterns),
        zip(em_chord, sustain_patterns),
        zip(am_chord, sustain_patterns),

        zip(am_chord, sustain_patterns),
        zip(f_chord, sustain_patterns),
        zip(g_chord, sustain_patterns),
        zip(c_chord, sustain_patterns),
    ])

    melody_notes = [
        (A1, 1),
        (C2, 1),

        (D2, 1),
        (C2, 0.5),
        (A1, 1.5),
        (A1, 1),

        (A1, 2),
        (G1, 1.5),
        (A1, 0.5),

        (A1, 6),
        (A1, 1),
        (C2, 1),

        (D2, 1),
        (C2, 0.5),
        (A1, 1.5),
        (A1, 1),

        (A1, 2),
        (G1, 1.5),
        (E2, 0.5),

        (E2, 8),
    ]

    notes = []

    current_beat = 0.0
    for frequency, duration in harmony_notes:
        notes.append(
            Note(frequency, start=current_beat, end=current_beat + duration, intensity=0.1)
        )
        current_beat += 0.5

    current_beat = 0.0
    for frequency, duration in melody_notes:
        notes.append(
            Note(frequency, start=current_beat, end=current_beat + duration, intensity=0.5)
        )
        current_beat += duration

    return notes



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


notes = li_ge()
sample = get_sample(notes, beats_per_minute=120)
with open('output.wav', 'wb') as f:
    write_wavefile(f, sample)
