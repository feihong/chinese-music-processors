"""
For all the .mp4 files in a given directory, do the following:

- Extract the audio out into a .m4a file.
- Adjust gain.
- Add metadata (title, artist, album, artwork).

Usage: python process_mp4_files.py /path/to/mp4/files/

---

Each input file should use the following format for their filename:

ALBUM  ARTIST  TITLE

Note that there are two spaces between each element.

---

In order to run this script, you must have ffmpeg, aacgain, and AtomicParsley
installed.

On Ubuntu:

apt-get install ffmpeg
add-apt-repository ppa:stefanobalocco/ppa
apt-get update
apt-get install aacgain
apt-get install atomicparsley

On Mac:

brew install ffmpeg
brew install aacgain
brew install atomicparsley

---

Sources:
http://www.linuxquestions.org/questions/linux-software-2/best-way-to-extract-aac-from-mp4-losslessly-852936/
http://archive09.linux.com/feature/59957
http://ubuntuforums.org/showthread.php?t=2194537

"""

import sys
import os
import os.path as op
import subprocess
import shutil
import tempfile
from pathlib2 import Path


class Song:
    def __init__(self, mp4_file):
        self.input_file = mp4_file
        stem = Path(mp4_file).stem
        self.album, self.artist, self.title = stem.split('  ')

        parent = Path(mp4_file).parent
        self.output_file = str(parent.joinpath(
            '%s  %s.m4a' % (self.artist, self.title)))

        self.artwork_file = None
        for ext in ('.jpg', '.png'):
            imgfile = parent.joinpath(stem + ext)
            if imgfile.exists():
                self.artwork_file = str(imgfile)
                break

        if not self.artwork_file:
            self.tempdir = tempfile.mkdtemp()
            self.artwork_file = op.join(self.tempdir, 'artwork.jpg')

    def __str__(self):
        return '%s - %s - %s (%s)' % (self.artist, self.title, self.album)

    def __del__(self):
        if hasattr(self, 'tempdir') and op.exists(self.tempdir):
            shutil.rmtree(self.tempdir)


def extract_elements(song):
    cmd = [
        'ffmpeg',
        '-i', song.input_file,
        '-vn',               # ignore video
        '-acodec', 'copy',   # copy, dont' reencode
        song.output_file
    ]
    subprocess.call(cmd)

    if not op.exists(song.artwork_file):
        cmd = [
            'ffmpeg',
            '-ss', '0',
            '-i', song.input_file,
            '-frames:v', '1',
            song.artwork_file,
        ]
        subprocess.call(cmd)


def adjust_gain(song):
    cmd = [
        'aacgain',
        '-r',       # apply Track gain automatically (all files set to equal loudness)
        '-k',       # automatically lower Track/Album gain to not clip audio
        song.output_file
    ]
    subprocess.call(cmd)


def add_metadata(song):
    cmd = [
        'AtomicParsley',
        song.output_file,
        '--title', song.title,
        '--artist', song.artist,
        '--album', song.album,
        '--artwork', song.artwork_file,
        '--overWrite',
    ]
    subprocess.call(cmd)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        dirname = sys.argv[1]
    else:
        dirname = '.'
    mp4_files = (f for f in os.listdir(dirname) if f.endswith('.mp4'))

    for mp4_file in mp4_files:
        try:
            song = Song(op.join(dirname, mp4_file))
        except Exception as ex:
            continue

        extract_elements(song)
        adjust_gain(song)
        add_metadata(song)
