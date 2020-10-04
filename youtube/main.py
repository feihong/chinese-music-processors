"""
Download all the songs inside a YouTube playlist and for each song:

- add metadata
- adjust gain
- add artwork

"""
import json
import subprocess
from pathlib import Path
import functools

import webvtt

import settings

here = Path(__file__).parent

download_dir = here / 'downloads'
output_dir = here / 'output'
json_file = here / 'youtube.json'


def process_playlist():
    download_songs(settings.YOUTUBE_PLAYLIST)
    generate_json()
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
    """
    If downloads folder doesn't have any mp4 files, download files from given YouTube URL.

    """
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


def generate_json():
    """
    If youtuble.json doesn't exist, read .info.json files from downloads directory and generate it

    """
    if json_file.exists():
        return

    def gen():
        for info in get_info_objects():
            yield dict(
                title=info['title'],
                artist='',
                album='',
                genre='流行 Pop',  # just a placeholder
                link=f"https://youtu.be/{info['id']}",
                path=info['path'],
                start=None,
                end=None,
            )

    json_file.write_text(
        json.dumps(list(gen()), indent=2, ensure_ascii=False)
    )

    print('\nGenerated youtube.json, edit it, and run `inv playlist` again!')



def add_metadata():
    """
    If youtube.json file exists, iterate over its entries and generate corresponding .m4a files in output directory

    """
    if not json_file.exists():
        return

    metas = json.loads(json_file.read_text())

    for meta in metas:
        if not meta['artist']:
            print('You have not filled the artist field yet')
            break
        input_file = Path(meta['path'])
        info_file = input_file.with_suffix('.info.json')
        info = json.loads(info_file.read_text())
        info.update(meta)

        output_file = output_dir / f"{meta['artist']}  {meta['title']}.m4a"

        add_metadata_for_file(input_file, output_file, info)


def add_metadata_for_file(input_file, output_file, meta):
    lyrics_lst = [meta.get('description', '')]

    # Get lyrics from captions, if any.
    caption_extensions = ['.zh.vtt', '.zh-Hans.vtt', '.zh-Hant.vtt', '.zh-CN.vtt', '.zh-TW.vtt']
    for ext in caption_extensions:
        caption_file = input_file.with_suffix(ext)
        if caption_file.exists():
            vtt = webvtt.read(caption_file)
            text = '\n'.join(c.text for c in vtt.captions)
            lyrics_lst.append(text)
            break  # don't need to process all caption files

    lyrics = '\n\n=====\n\n'.join(lyrics_lst)

    cmd = [
        'ffmpeg',
        '-y',
        '-i', str(input_file),
        '-acodec', 'copy',  # copy audio without additional processing
        '-vn',              # ignore video
        ('-ss', meta.get('start')),
        ('-to', meta.get('end')),
        '-metadata', f"genre={meta['genre']}",
        '-metadata', f"title={meta['title']}",
        '-metadata', f"artist={meta.get('artist', '')}",
        '-metadata', f"album={meta.get('album', '')}",
        '-metadata', f"comment={meta['webpage_url']}",
        '-metadata', f"lyrics={lyrics}",
        str(output_file)
    ]
    call_process(cmd)

    cmd = [
        'aacgain',
        # apply Track gain automatically (all files set to equal loudness)
        '-r',
        '-k',  # automatically lower Track/Album gain to not clip audio
        str(output_file)
    ]
    subprocess.call(cmd)

    image_file = input_file.with_suffix('.jpg')
    if image_file.exists():
        # Use imagemagick to fix .jpg file so it can be used by AtomicParsley
        cmd = ['convert', image_file, image_file]
        call_process(cmd)
    else:
        # Use imagemagick to convert .webp file to .jpg file so it can be used by AtomicParsley
        webp_file = input_file.with_suffix('.webp')
        if webp_file.exists():
            cmd = ['convert', webp_file, image_file]
            call_process(cmd)

    cmd = [
        'AtomicParsley',
        str(output_file),
        '--artwork', str(image_file),
        '--overWrite'
    ]
    call_process(cmd)

    print(f'\nOutput files generated in {output_file}')


def get_info_objects():
    for info_file in download_dir.glob('*.info.json'):
        info = json.loads(info_file.read_text())
        video_file = (info_file.parent / info_file.stem).with_suffix('.mp4')
        info['path'] = str(video_file)
        yield info


def call_process(cmd):
    def reducer(acc, item):
        if type(item) == tuple:
            if item[-1] is None:
                return acc
            else:
                return acc + list(item)
        else:
            return acc + [item]

    # Get rid of tuple elements whose second elements are None
    cmd = functools.reduce(reducer, cmd, [])
    print(f'Running command: {cmd}')
    subprocess.call(cmd)
