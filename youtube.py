"""
For all the .mp4 files in a given directory, do the following:

- Extract the audio out into a .m4a file.
- Adjust gain.
- Add metadata (title, artist, album, artwork).

Each input file should use one of the two following formats for their filename:

ALBUM  ARTIST  TITLE  URL
ARTIST  TITLE  URL

Note that there are two spaces between each element.

"""
import json
import sys
import subprocess
import shutil
import tempfile
from pathlib import Path
import webvtt


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
                print(line)
                args = line.split('  ')
                if len(args) == 4:
                    yield Song(*args)
                else:
                    args_ = [None] + args
                    yield Song(*args_)


class Song:
    def __init__(self, album, artist, title, url):
        self.album = album      # might be None
        self.artist = artist
        self.title = title
        self.url = url
        self.output_file = Path('youtube_songs') / f'{artist}  {title}.m4a'
        self.json_file = self.output_file.with_suffix('.info.json')
        self.subtitle_file = self.output_file.with_suffix('.zh-Hans.vtt')
        self.lyrics_file = self.output_file.with_suffix('.lyrics')


def download_song(song):
    cmd = [
        'youtube-dl',
        '--embed-thumbnail',
        '--write-info-json',
        '--all-subs',
        '--format', 'bestaudio[ext=m4a]',
        '--output', song.output_file,
        song.url
    ]
    subprocess.call(cmd)

    meta = json.loads(song.json_file.read_bytes())
    song.lyrics = meta['description']
    if song.subtitle_file.exists():
        subs = webvtt.read(song.subtitle_file)
        song.lyrics += '\n\n=====\n\n' + '\n'.join(c.text for c in subs.captions)
    song.lyrics_file.write_text(song.lyrics)


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
        '--comment', song.url,
    ]
    if song.album is not None:
        cmd.extend(['--album', song.album])
    cmd.append('--overWrite')
    subprocess.call(cmd)

    # Now add the lyrics. This step can sometimes fail for mysterious reasons,
    # which is why we save it for last.
    cmd = [
        'AtomicParsley',
        str(song.output_file),
        '--lyrics', song.lyrics,
        '--overWrite',
    ]
    retcode = subprocess.call(cmd)
    if retcode != 0:
        # print(' '.join(cmd))
        print(f'AtomicParsley failed to add lyrics to file {song.output_file}')
