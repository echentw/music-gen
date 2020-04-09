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
