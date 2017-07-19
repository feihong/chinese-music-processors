"""
For all the .mp4 files in a given directory, do the following:

- Extract the audio out into a .m4a file.
- Adjust gain.
- Add metadata (title, artist, album, artwork).

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
import subprocess
import shutil
import tempfile
from pathlib import Path


def process(input_file):
    for song in get_songs(input_file):
        download_song(song)
        adjust_gain(song)
        add_metadata(song)


def get_songs(input_file):
    with open(input_file) as fp:
        for line in fp:
            line = line.strip()
            if line:
                args = line.split('  ')
                yield Song(*args)


class Song:
    def __init__(self, album, artist, title, url):
        self.album = album
        self.artist = artist
        self.title = title
        self.url = url
        self.output_file = Path('youtube_songs') / '{}  {}.m4a'.format(artist, title)


def download_song(song):
    cmd = [
        'youtube-dl',
        '--embed-thumbnail',
        '--format', 'bestaudio[ext=m4a]',
        '--output', song.output_file,
        song.url
    ]
    subprocess.call(cmd)


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
        '--comment', song.url,
        '--overWrite',
    ]
    subprocess.call(cmd)
