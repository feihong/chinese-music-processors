Chinese Music Processors
========================

These are scripts to help you process metadata for music files downloaded from Douban Music and Youtube.

Installation
------------

Install the following manually:

- [Greasemonkey](https://addons.mozilla.org/en-us/firefox/addon/greasemonkey/)
- [douban_song_metadata.user.js user script](https://raw.githubusercontent.com/feihong/chinese-music-processors/master/douban_song_metadata.user.js) from this repo
- virtualenvwrapper

You should probably install these, but there are equivalent addons that would also work:

- [Download Youtube Videos as MP4](https://addons.mozilla.org/en-us/firefox/addon/download-youtube/)
- [Cache Download](https://addons.mozilla.org/en-us/firefox/addon/cachedownload/)

Run the following commands:

```
cd /path/to/project
apt-get install xclip ffmpeg mp3gain atomicparsley aacgain

mkvirtualenv music
pip install -r requirements.txt
```
