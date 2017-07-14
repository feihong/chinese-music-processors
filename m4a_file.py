"""
Each input file should use the following format for their filename:

ALBUM  ARTIST  TITLE

Note that there are two spaces between each element.

"""
import sys
import subprocess
import shutil
from pathlib import Path


def process():
    output_dir = Path(__file__).parent / 'm4a_songs'

    for m4a_file in output_dir.glob('*.m4a'):
        print(m4a_file)
        song = Song(m4a_file)

        shutil.copy(song.input_file, song.output_file)
        adjust_gain(song)
        add_metadata(song)


class Song:
    def __init__(self, m4a_file):
        self.input_file = m4a_file
        self.album, self.artist, self.title = m4a_file.stem.split('  ')

        self.output_file = (m4a_file.parent / 'output' /
            Path('{}  {}.m4a'.format(self.artist, self.title)))

        artwork_file = (m4a_file.parent /
            Path(self.artist).with_suffix('.jpg'))
        self.artwork_file = artwork_file if artwork_file.exists() else None


def adjust_gain(song):
    cmd = [
        'aacgain',
        '-r',       # apply Track gain automatically (all files set to equal loudness)
        '-k',       # automatically lower Track/Album gain to not clip audio
        str(song.output_file),
    ]
    subprocess.call(cmd)


def add_metadata(song):
    cmd = [
        'AtomicParsley',
        str(song.output_file),
        '--title', song.title,
        '--artist', song.artist,
        '--album', song.album,
        '--artwork', str(song.artwork_file),
        '--overWrite',
    ]
    subprocess.call(cmd)
