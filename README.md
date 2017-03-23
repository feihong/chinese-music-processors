# Chinese Music Processors

These are scripts to help you process metadata for music files downloaded from [Douban Music](https://music.douban.com/) and Youtube.

## Installation

Install the following Firefox addons and user script:

- [Greasemonkey](https://addons.mozilla.org/en-us/firefox/addon/greasemonkey/)
- Greasemonkey [Douban music user script](https://raw.githubusercontent.com/feihong/chinese-music-processors/master/douban_song_metadata.user.js) from this repo
- [Download Youtube Videos as MP4](https://addons.mozilla.org/en-us/firefox/addon/download-youtube/)
- [Cache Download](https://addons.mozilla.org/en-us/firefox/addon/cachedownload/)

Configure Cache Download like so:

![](https://raw.githubusercontent.com/feihong/chinese-music-processors/master/images/cache_download_rule_mp3.png)

- Filename expression: `%filename%.%ext%`
- Regular expression to match files: `.*doubanio\.com.*\.mp3`

![](https://raw.githubusercontent.com/feihong/chinese-music-processors/master/images/cache_download_rule_jpg.png)

- Filename expression: `%filename%.%ext%`
- Regular expression to match files: `.*doubanio\.com.*large.*jpg`

Install dependencies on Ubuntu:

```
apt-get install xclip ffmpeg atomicparsley mp3gain aacgain
```

If you are on 16.04, you may need to download binaries for mp3gain and aacgain. In addition, you'll likely need to build ffmpeg yourself.

- [mp3gain](https://pkgs.org/ubuntu-14.04/ubuntu-universe-amd64/mp3gain_1.5.2-r2-6_amd64.deb.html)
- [aacgain](https://launchpad.net/~stefanobalocco/+archive/ubuntu/ppa/+packages)
- [ffmpeg](https://github.com/feihong/feihong-setup/blob/master/ubuntu/compile_ffmpeg.sh)

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

## Usage

tbd
