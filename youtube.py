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
import webbrowser
import webvtt
from jinja2 import Template


def process(input_file):
    songs = list(get_songs(input_file))
    for song in songs:
        download_song(song)
        adjust_gain(song)
        add_metadata(song)

    report_file = generate_report(songs)
    webbrowser.open(str(report_file))


def get_songs(input_file):
    with open(input_file) as fp:
        for line in fp:
            line = line.strip()
            if line:
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
        self.lyrics = ''
        self.output_file = Path('youtube_songs') / f'{artist}  {title}.m4a'
        self.info_file = self.output_file.with_suffix('.info.json')
        self.lyrics_file = self.output_file.with_suffix('.lyrics')

    @property
    def extracted_lyrics(self):
        cmd = [
            'ffprobe',
            '-v', 'quiet',
            '-print_format', 'json',
            '-show_format',
            str(self.output_file),
        ]
        output = subprocess.check_output(cmd)
        meta = json.loads(output)
        try:
            return meta['format']['tags']['lyrics']
        except:
            return None


def download_song(song):
    if not song.output_file.exists():
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

    # Get lyrics from video description.
    info = json.loads(song.info_file.read_bytes())
    lyrics_list = [info['description']]

    # Get lyrics from subtitles, if any.
    for ext in ['.zh-Hans.vtt', '.zh-Hant.vtt', '.zh-TW.vtt']:
        caption_file = song.output_file.with_suffix(ext)
        if caption_file.exists():
            vtt = webvtt.read(caption_file)
            lyrics = '\n'.join(c.text for c in vtt.captions)
            lyrics_list.append(lyrics)
            break

    song.lyrics = '\n\n=====\n\n'.join(lyrics_list)
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
        '--genre', '流行 Pop',    # just a default
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
        '--lyricsFile', str(song.lyrics_file),
        '--overWrite',
    ]
    subprocess.call(cmd)

template = Template("""\
<!doctype html>
<html class="no-js" lang="">
<head>
  <meta charset="utf-8">
  <title>YouTube Processing Report</title>
</head>
<body>
{% for song in songs %}
  <p>
    {{ song.output_file }}
    <a href="{{ song.url }}" target="_blank">link</a>
    {% if song.extracted_lyrics == None %}
      <div>
        No lyrics found in output file!
      </div>
    {% endif %}
    <textarea>{{ song.lyrics }}</textarea>
  </p>
{%endfor %}
</body>
""")

def generate_report(songs):
    report_file = Path('youtube-report.html')
    report_file.write_text(
        template.render(songs=songs)
    )
    return report_file
