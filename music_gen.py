import inspect
import wave
import math

from lib.waveform_generators import sine_wave_generator
from lib.envelope_generators import decay_generator


def compose_wave(
    wave_generator_func,
    envelope_generator_func,
    frequency,
    duration_frames,
    amplitude=0.2,
    framerate=44100
):
    wave_generator = wave_generator_func(frequency, amplitude=amplitude, framerate=framerate)
    envelope_generator = envelope_generator_func(duration_frames)
    return (
        amplitude_factor * wave_value
        for amplitude_factor, wave_value in zip(envelope_generator, wave_generator)
    )


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


def produce_sample(notes, beats_per_minute=60, framerate=44100):
    beats_to_frame_factor = int(60 / beats_per_minute * framerate)

    time_notes = []
    for note in notes:
        time_notes.append((note.start * beats_to_frame_factor, note))
        time_notes.append((note.end * beats_to_frame_factor, note))
    time_notes = sorted(time_notes, key=lambda x: x[0])

    time_notes_index = 0

    current_waves = dict()

    total_frames = int(time_notes[-1][0])

    for frame_index in range(total_frames + 1):
        # First, update current_waves
        while time_notes_index < len(time_notes) and time_notes[time_notes_index][0] <= frame_index:
            note = time_notes[time_notes_index][1]
            if note in current_waves:
                del current_waves[note]
            else:
                current_waves[note] = compose_wave(
                    wave_generator_func=sine_wave_generator,
                    envelope_generator_func=decay_generator,
                    frequency=note.frequency,
                    duration_frames=note.duration_frames(beats_per_minute=beats_per_minute, framerate=framerate),
                    amplitude=note.intensity
                )
            time_notes_index += 1

        # Second, yield the next sound data
        value = 0.0
        for wave in current_waves.values():
            value += next(wave)

        value = min(max(value, -1.0), 1.0)

        yield (value, value)
