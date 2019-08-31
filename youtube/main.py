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

# import webvtt  # currently not used

import settings

here = Path(__file__).parent

download_dir = Path(here) / 'downloads'
output_dir = Path(here) / 'output'
csv_file = Path(here) / 'youtube.csv'
rewrite_csv_file = Path(here) / 'youtube-rewrite.csv'


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

  rewrite_meta = {}
  with rewrite_csv_file.open() as fp:
    reader = csv.DictReader(fp)
    for row in reader:
      rewrite_meta[row['id']] = row

  for info in get_info_objects():
    id = info['id']
    input_file = next(download_dir.glob('*-' + id + '.m4a'))
    meta = rewrite_meta[id]
    output_file = output_dir / f"{meta['artist']}  {meta['title']}.m4a"

    add_metadata_for_file(input_file, output_file, meta, info)


def add_metadata_for_file(input_file, output_file, meta, info):
  # todo: add subtitles to lyrics as well?

  cmd = [
    'ffmpeg',
    '-y',
    '-i', str(input_file),
    '-metadata', f"title={meta['title']}",
    '-metadata', f"artist={meta['artist']}",
    '-metadata', f"album={meta['album']}",
    '-metadata', f"comment={meta['url']}",
    '-metadata', f"lyrics={info['description']}",
    '-metadata', 'genre=流行 Pop',  # just a placeholder
    '-vn',
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

  print(f'Output files generated in {output_file}')


def get_info_objects():
  for info_file in download_dir.glob('*.info.json'):
    yield json.loads(info_file.read_text())


if __name__ == '__main__':
  main()
