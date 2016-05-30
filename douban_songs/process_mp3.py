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
import tempfile
import pprint
import os
import os.path as op
import shutil
import codecs

import yaml
from mutagen.id3 import ID3, ID3NoHeaderError


def main():
    if len(sys.argv) > 1:
        # Get input from YAML file.
        yaml_str = open(sys.argv[1]).read()
        root = yaml.load(yaml_str)
    else:
        # Get input from JSON string on clipboard.
        json_str = get_clipboard_text()
        root = json.loads(json_str)

    # Write readable input to a yaml file.
    with open('last-input.yaml', 'w') as fp:
        yaml.safe_dump(root, fp, default_flow_style=False, allow_unicode=True)

    with open('last-input.json', 'w') as fp:
        fp.write(json.dumps(root, indent=2))

    songs = [Song(s) for s in root['playlist']]

    download_media(songs)
    for song in songs:
        process_song(song)


def download_media(songs):
    for song in songs:
        if not op.exists(song.filename):
            download(song.url)

        if not op.exists(song.image_filename) or op.getsize(song.image_filename) == 0:
            download(song.image_url, song.image_filename)

def process_song(song):
    if op.exists(song.new_filename):
        print(u'Skipping %s' % song.filename)
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
        song.filename
    ]
    subprocess.call(cmd)


def convert(song):
    """
    Convert the given song from MP3 to AAC. For more information about the
    parameters, see: https://trac.ffmpeg.org/wiki/Encode/AAC

    """
    cmd = [
        'ffmpeg',
        '-i', song.filename,
        '-vn',                  # ignore video
        '-c:a', 'libfdk_aac',   # use best encoder
        '-vbr', '4',            # use high quality
        song.new_filename,
    ]
    subprocess.call(cmd)


def download(url, dest=None):
    cmd = ['wget', url]
    if dest:
        cmd.extend(['-O', dest])
    retcode = subprocess.call(cmd)
    if retcode != 0:
        raise Exception('Unable to download file at ' + url)


def add_metadata(song):
    """
    Add metadata to the given song's AAC file.

    """
    cmd = [
        'AtomicParsley',
        song.new_filename,
        '--title', song.title,
        '--artist', song.artist,
        '--genre', song.genre,
        '--year', song.year,
        '--comment', song.artist_url,
        '--artwork', song.image_filename,
        '--overWrite',
    ]
    retcode = subprocess.call(cmd)
    if retcode != 0:
        print ' '.join(cmd)
        raise Exception('AtomicParsley failed on file ' + song.new_filename)

    # Now add the lyrics. This step can sometimes fail for mysterious reasons,
    # which is why we save it for last.
    cmd = [
        'AtomicParsley',
        song.new_filename,
        '--lyrics', song.lyrics,
        '--overWrite',
    ]
    retcode = subprocess.call(cmd)
    if retcode != 0:
        print ' '.join(cmd)
        raise Exception('AtomicParsley failed to add lyrics to file ' + song.new_filename)


class Song:
    def __init__(self, dictionary):
        self.d = dictionary

        self.title = unescape(self.d['title'])      # get rid of &amp; etc
        self.url = self.d['url']
        self.lyrics = self.d['lyrics']
        self.artist = unescape(self.d['artist']['name'])
        self.artist_url = self.d['artist']['url']
        self.image_url = self.d['artist']['picture']
        self.genre = self.d['artist']['style']
        self.year = self.d['publish_date'][:4]
        self.filename = self.url.rsplit('/', 1)[1]
        self.new_filename = format_filename('%s  %s.m4a' % (
            self.artist, self.title))
        self.image_filename = self.get_image_filename()

    @property
    def comments(self):
        return json.dumps(self.d)

    def get_image_filename(self):
        try:
            audio = ID3(self.filename)
            images = audio.getall('APIC')
        except ID3NoHeaderError:
            images = None

        if images:
            # Use the first embedded image.
            image = images[0]
            if image.mime in ('image/jpeg', 'image/jpg'):
                ext = '.jpg'
            elif image.mime == 'image/png':
                ext = '.png'
            else:
                raise Exception('Encountered unexpected image type %s in %s' % (
                    image.mime, self.filename))
            filename = op.splitext(self.filename)[0] + ext
            path = op.join('images', filename)

            # Extract the embedded image to the images directory.
            if not op.exists(path):
                with open(path, 'wb') as fp:
                    fp.write(image.data)
            return path
        else:
            # Use the downloaded image.
            filename = self.image_url.rsplit('/', 1)[1]
            return op.join('images', filename)


def format_filename(s):
    return s.replace('/', '_')


def get_clipboard_text():
    if sys.platform == 'darwin':
        return subprocess.check_output('pbpaste')
    else:
        return subprocess.check_output(['xclip', '-o'])


def unescape(s):
    import htmllib
    p = htmllib.HTMLParser(None)
    p.save_bgn()
    p.feed(s)
    return p.save_end()


if __name__ == '__main__':
    main()
