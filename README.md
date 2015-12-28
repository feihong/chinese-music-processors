Chinese Music Processors
========================

These are scripts to help you process metadata for music files downloaded from Douban Music and Youtube.

Installation
------------

Install the following Firefox addons and user script:

- [Greasemonkey](https://addons.mozilla.org/en-us/firefox/addon/greasemonkey/)
- Greasemonkey [Douban music user script](https://raw.githubusercontent.com/feihong/chinese-music-processors/master/douban_song_metadata.user.js) from this repo
- [Download Youtube Videos as MP4](https://addons.mozilla.org/en-us/firefox/addon/download-youtube/)
- [Cache Download](https://addons.mozilla.org/en-us/firefox/addon/cachedownload/)

Configure Cache Download like so:

![](https://raw.githubusercontent.com/feihong/chinese-music-processors/master/images/cache_download_rule.png)

- Filename expression: `%filename%.%ext%`
- Regular expression to match files: `.*douban\.com.*\.mp3`

Install dependencies on Ubuntu:

```
apt-get install xclip ffmpeg mp3gain atomicparsley aacgain
```

If you don't already have it, install virtualenvwrapper:

```
pip install virtualenvwrapper
```

Now you can install the Python scripts:

```
git clone https://github.com/feihong/chinese-music-processors
cd chinese-music-processors
mkvirtualenv music
pip install -r requirements.txt
```
