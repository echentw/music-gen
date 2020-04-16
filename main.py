import argparse

from lib.io import write_wavefile
from lib.tuning_systems import TUNING_SYSTEMS, DEFAULT_TUNING

from music_gen import produce_sample
from songs import ALL_SONGS, DEFAULT_SONG



parser = argparse.ArgumentParser(description='generate wav file with specified tuning methods')
parser.add_argument(
    '--song', '-s',
    choices=ALL_SONGS.keys(),
    default=DEFAULT_SONG,
    help='name of song to tune (default: %s)' % DEFAULT_SONG)
parser.add_argument(
    '--tuning', '-t',
    choices=TUNING_SYSTEMS.keys(),
    default=DEFAULT_TUNING,
    help='tuning method (default: %s)' % DEFAULT_TUNING)
parser.add_argument(
    '--output-file', '-o',
    default='output.wav',
    help='name of output file (default: "output.wav")')
args = parser.parse_args()

print('saving song with tuning to file:\n'
    + '\tsong: %s\n' % args.song
    + '\ttuning: %s\n' % args.tuning
    + '\toutput file: %s\n' % args.output_file)


notes = ALL_SONGS[args.song](tuning_system=TUNING_SYSTEMS[args.tuning])

sample = produce_sample(notes, beats_per_minute=140)

with open(args.output_file, 'wb') as f:
    write_wavefile(f, sample)
