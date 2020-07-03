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


def process_playlist():
    download_songs(settings.YOUTUBE_PLAYLIST)
    generate_csv()
    add_metadata()


def process_link(url):
    download_songs(url)

    input_file = next(download_dir.glob('*.mp4'))
    output_file = input_file.with_suffix('.m4a')
    info_file = input_file.with_suffix('.info.json')
    info = json.loads(info_file.read_text())
    info['url'] = info['webpage_url']
    add_metadata_for_file(input_file, output_file, info)


def download_songs(url):
    files = list(download_dir.glob('*.mp4'))
    if len(files) > 0:
        return

    cmd = [
        'youtube-dl',
        '--write-thumbnail',
        '--write-info-json',
        '--all-subs',
        '--format', '[ext=mp4]',
        '--output', f'{download_dir}/%(title)s-%(id)s.%(ext)s',
        url,
    ]
    subprocess.call(cmd)

    # Nicely format the info.json files
    for info_file in download_dir.glob('*.info.json'):
        obj = json.loads(info_file.read_text())
        with info_file.open('w') as fp:
            json.dump(obj, fp, indent=2, ensure_ascii=False)

    print(f'Files downloaded in {download_dir}')


def generate_csv():
    with csv_file.open('w') as fp:
        writer = csv.writer(fp)
        writer.writerow(['title', 'artist', 'album', 'url', 'path'])

        for info in get_info_objects():
            writer.writerow([
                info['title'],  # title probably needs to be edited
                '',             # artist is filled in by user
                '',             # album is filled in by user
                f"https://youtu.be/{info['id']}",
                info['path'],
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
        input_file = Path(meta['path'])
        info_file = input_file.with_suffix('.info.json')
        info = json.loads(info_file.read_text())
        info.update(meta)

        output_file = output_dir / f"{meta['artist']}  {meta['title']}.m4a"

        add_metadata_for_file(input_file, output_file, info)


def add_metadata_for_file(input_file, output_file, meta):
    lyrics_lst = [meta.get('description', '')]

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
        '-metadata', f"artist={meta.get('artist', '')}",
        '-metadata', f"album={meta.get('album', '')}",
        '-metadata', f"comment={meta['url']}",
        '-metadata', f"lyrics={lyrics}",
        str(output_file)
    ]
    subprocess.call(cmd)

    cmd = [
        'aacgain',
        # apply Track gain automatically (all files set to equal loudness)
        '-r',
        '-k',  # automatically lower Track/Album gain to not clip audio
        str(output_file)
    ]
    subprocess.call(cmd)

    image_file = input_file.with_suffix('.png')
    if not image_file.exists():
        image_file = input_file.with_suffix('.jpg')

    if image_file.exists():
        cmd = [
            'AtomicParsley',
            str(output_file),
            '--artwork', str(image_file),
            '--overWrite'
        ]
        subprocess.call(cmd)
    else:
        webp_file = input_file.with_suffix('.webp')
        if webp_file.exists():
            # Convert to png if format is webp
            cmd = [
                'ffmpeg',
                '-y', # overwrite if file already exists
                '-i', str(webp_file),
                str(image_file.with_suffix('.png')),
            ]
            print(cmd)
            subprocess.call(cmd)

        print(f'No valid image file was found for {input_file}')

    print(f'\nOutput files generated in {output_file}')


def get_info_objects():
    for info_file in download_dir.glob('*.info.json'):
        info = json.loads(info_file.read_text())
        video_file = (info_file.parent / info_file.stem).with_suffix('.mp4')
        info['path'] = str(video_file)
        yield info
