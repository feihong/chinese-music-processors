"""
Download all the songs inside a YouTube playlist and for each song:

- add metadata
- adjust gain
- add artwork

"""
import json
import subprocess
from pathlib import Path
import csv

import webvtt

import settings

here = Path(__file__).parent

download_dir = here / 'downloads'
output_dir = here / 'output'
csv_file = here / 'youtube.csv'
rewrite_csv_file = here / 'youtube-rewrite.csv'


def main():
  download_songs()
  generate_csv()
  add_metadata()


def download_songs():
  m4a_files = list(download_dir.glob('*.m4a'))
  if len(m4a_files) == 0:
    cmd = [
        'youtube-dl',
        '--write-thumbnail',
        '--write-info-json',
        '--all-subs',
        '--format', 'bestaudio[ext=m4a]',
        '--output', f'{download_dir}/%(title)s-%(id)s.%(ext)s',
        settings.YOUTUBE_PLAYLIST,
    ]
    subprocess.call(cmd)

    print(f'Files downloaded in {download_dir}')


def generate_csv():
  with csv_file.open('w') as fp:
    writer = csv.writer(fp)
    writer.writerow(['id', 'title', 'artist', 'album', 'url'])

    for info in get_info_objects():
      writer.writerow([
        info['id'],
        info['title'],  # title probably needs to be edited
        '',             # artist is filled in by user
        '',             # album is filled in by user
        f"https://youtu.be/{info['id']}"
      ])

  print('\nGenerated youtube.csv, edit it, and save to youtube-rewrite.csv!')


def add_metadata():
  if not rewrite_csv_file.exists():
    return

  metas = None
  with rewrite_csv_file.open() as fp:
    reader = csv.DictReader(fp)
    metas = list(reader)

  for meta in metas:
    input_file = next(download_dir.glob(f'*-{meta["id"]}.m4a'))
    output_file = output_dir / f"{meta['artist']}  {meta['title']}.m4a"

    add_metadata_for_file(input_file, output_file, meta)


def add_metadata_for_file(input_file, output_file, meta):
  info_file = next(download_dir.glob(f'*-{meta["id"]}.info.json'))
  info = json.loads(info_file.read_text())

  lyrics_lst = [info['description']]

  # Get lyrics from subtitles, if any.
  for ext in ['.zh-Hans.vtt', '.zh-Hant.vtt', '.zh-TW.vtt']:
    caption_file = input_file.with_suffix(ext)
    if caption_file.exists():
        vtt = webvtt.read(caption_file)
        text = '\n'.join(c.text for c in vtt.captions)
        lyrics_lst.append(text)
        break  # process at most one caption file

  lyrics = '\n\n=====\n\n'.join(lyrics_lst)

  cmd = [
    'ffmpeg',
    '-y',
    '-i', str(input_file),
    '-acodec', 'copy',  # copy audio without additional processing
    '-vn',              # ignore video
    '-metadata', 'genre=流行 Pop',  # just a placeholder
    '-metadata', f"title={meta['title']}",
    '-metadata', f"artist={meta['artist']}",
    '-metadata', f"album={meta['album']}",
    '-metadata', f"comment={meta['url']}",
    '-metadata', f"lyrics={lyrics}",
    str(output_file)
  ]
  subprocess.call(cmd)

  cmd = [
    'aacgain',
    '-r',  # apply Track gain automatically (all files set to equal loudness)
    '-k',  # automatically lower Track/Album gain to not clip audio
    str(output_file)
  ]
  subprocess.call(cmd)

  image_file = next(download_dir.glob('*-' + info['id'] + '.jpg'))
  cmd = [
    'AtomicParsley',
    str(output_file),
    '--artwork', str(image_file),
    '--overWrite'
  ]
  subprocess.call(cmd)

  print(f'\nOutput files generated in {output_file}')


def get_info_objects():
  for info_file in download_dir.glob('*.info.json'):
    yield json.loads(info_file.read_text())


if __name__ == '__main__':
  main()
