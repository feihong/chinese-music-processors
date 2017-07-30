"""
Process MP3 files downloaded from Douban music.

Dependencies:
- Commands: xclip, ffmpeg, mp3gain, atomicparsley
- Python modules: mutagen

Sources:
https://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu#RevertingChangesMadebyThisGuide
https://trac.ffmpeg.org/wiki/CompilationGuide/MacOSX
https://trac.ffmpeg.org/wiki/Encode/AAC
https://pypi.python.org/pypi/pyaml/
https://wiki.python.org/moin/EscapingHtml

"""
import sys
import json
import subprocess
import pprint
from pathlib import Path
import html

import yaml
from mutagen.id3 import ID3, ID3NoHeaderError


input_dir = Path.home() / 'Downloads/douban-songs'
output_dir = Path(__file__).parent / 'douban_songs'


def process(input_file):
    with open(input_file) as fp:
        playlist = json.load(fp)

    songs = [Song(s) for s in playlist]

    download_media(songs)
    for song in songs:
        process_song(song)


def download_media(songs):
    for song in songs:
        # if not song.input_file.exists():
        #     download(song.url, song.input_file)

        if not song.image_file.exists() or song.image_file.stat().st_size == 0:
            download(song.image_url, song.image_file)


def process_song(song):
    if song.output_file.exists():
        print('Skipping {}'.format(song.input_file))
        return

    adjust_gain(song)
    convert(song)
    add_metadata(song)


def adjust_gain(song):
    """
    Adjust the gain on the given song so the volume is neither too loud nor too
    soft. We use mp3gain here instead of aacgain because it's completely
    lossless.

    """
    cmd = [
        'mp3gain',
        # Apply Track gain automatically (all files set to equal loudness)
        '-r',
        # Automatically lower Track/Album gain to not clip audio
        '-k',
        str(song.input_file),
    ]
    subprocess.call(cmd)


def convert(song):
    """
    Convert the given song from MP3 to AAC. For more information about the
    parameters, see: https://trac.ffmpeg.org/wiki/Encode/AAC

    """
    cmd = [
        'ffmpeg',
        '-i', str(song.input_file),
        '-vn',                  # ignore video
        '-c:a', 'libfdk_aac',   # use best encoder
        '-vbr', '4',            # use high quality
        str(song.output_file),
    ]
    subprocess.call(cmd)


def download(url, dest):
    cmd = ['wget', url, '-O', str(dest)]
    retcode = subprocess.call(cmd)
    if retcode != 0:
        raise Exception('Unable to download file at ' + url)


def add_metadata(song):
    """
    Add metadata to the given song's AAC file.

    """
    cmd = [
        'AtomicParsley',
        str(song.output_file),
        '--title', song.title,
        '--artist', song.artist,
        '--genre', song.genre,
        '--year', song.year,
        '--comment', song.artist_url,
        '--artwork', str(song.image_file),
        '--overWrite',
    ]
    retcode = subprocess.call(cmd)
    if retcode != 0:
        print(' '.join(cmd))
        raise Exception('AtomicParsley failed on file ' + song.new_filename)

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
        print(' '.join(cmd))
        raise Exception('AtomicParsley failed to add lyrics to file ' + song.new_filename)


class Song:
    def __init__(self, dictionary):
        self.d = dictionary

        self.title = html.unescape(self.d['title'])      # get rid of &amp; etc
        self.url = self.d['url']
        self.lyrics = self.d['lyrics']
        self.artist = html.unescape(self.d['artist']['name'])
        self.artist_url = self.d['artist']['url']
        self.image_url = self.d['artist']['picture']
        self.genre = self.d['artist']['style']
        self.year = self.d['publish_date'][:4]
        input_filename = self.url.rsplit('/', 1)[1]
        self.input_file = input_dir / input_filename
        output_filename = format_filename('%s  %s.m4a' % (
            self.artist, self.title))
        self.output_file = output_dir / output_filename
        self.image_file = self._get_image_file()

    @property
    def comments(self):
        return json.dumps(self.d)

    def _get_image_file(self):
        # try:
        #     audio = ID3(str(self.input_file))
        #     images = audio.getall('APIC')
        # except ID3NoHeaderError:
        #     images = None
        #
        # if images:
        #     # Use the first embedded image.
        #     image = images[0]
        #     if image.mime in ('image/jpeg', 'image/jpg'):
        #         ext = '.jpg'
        #     elif image.mime == 'image/png':
        #         ext = '.png'
        #     else:
        #         raise Exception('Encountered unexpected image type %s in %s' % (
        #             image.mime, self.filename))
        #
        #     result = output_dir / 'images' / self.input_file.stem + ext
        #
        #     # Extract the embedded image to the images directory.
        #     if not result.exists():
        #         with result.open('wb') as fp:
        #             fp.write(image.data)
        #
        #     return result
        # else:

        # Use the downloaded image.
        filename = self.image_url.rsplit('/', 1)[1]
        return output_dir / 'images' / filename


def format_filename(s):
    return s.replace('/', '_')


if __name__ == '__main__':
    main()
