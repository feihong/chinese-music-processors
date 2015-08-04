"""
For all the .mp4 files in a given directory, do the following:

- Extract the audio out into a .m4a file.
- Adjust gain.
- Optionally trim running time.
- Add metadata (title, artist, album, artwork).

Usage: python process_mp4_files.py /path/to/mp4/files/

---

Each input file should use the following format for their filename:

ALBUM  TITLE  ARTIST  [START-END]

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


class Song:
    def __init__(self, mp4_path):
        self.input_file = mp4_file
        name = op.basename(mp4_file).rsplit('.', 1)[0]
        parts = name.split('  ')
        self.album, self.title, self.artist = parts[:3]
        
        dirname = op.dirname(mp4_file)
        self.output_file = op.join(dirname, '%s  %s.m4a' % (self.artist, self.title))

        self.tempdir = tempfile.mkdtemp()
        self.artwork_file = op.join(self.tempdir, 'artwork.jpg')
        
        if len(parts) > 3:
            start, end = parts[3].split('-')
            self.start = self.get_seconds(start)
            self.end = self.get_seconds(end)
        else:
            self.start = self.end = None

    def get_seconds(self, time_str):
        min, sec = time_str.split(':')
        return int(min) * 60 + int(sec)

    @property
    def time_args(self):
        "Return tuple with format (start, duration)."
        if self.start is not None:
            return (self.start, self.end - self.start)
        else:
            return None

    def __str__(self):
        return '%s - %s - %s (%s)' % (self.artist, self.title, self.album, 
            self.time_args)

    def __del__(self):
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


def trim(song):
    start, duration = song.time_args
    tmpfile = op.join(song.tempdir, 'temp.m4a')

    cmd = [
        'ffmpeg',
        '-ss', str(start),
        '-i', song.output_file,
        '-t', str(duration),
        '-acodec', 'copy',
        tmpfile,
    ]
    subprocess.call(cmd)
    shutil.copy(tmpfile, song.output_file)


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
        except:
            continue

        extract_elements(song)
        adjust_gain(song)
        if song.time_args:
            trim(song)
        add_metadata(song)
