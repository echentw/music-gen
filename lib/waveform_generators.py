import itertools
import math


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
