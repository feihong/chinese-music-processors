# Chinese Music Processors

These are scripts to help you process metadata for music files downloaded from [Douban Music](https://music.douban.com/) and Youtube.

## Installation

### Mac

```
brew install mp3gain aacgain atomicparsley wget
brew install ffmpeg --with-fdk-aac
```

### Linux

Install dependencies on Ubuntu:

```
apt-get install xclip ffmpeg atomicparsley mp3gain aacgain
```

If you are on 16.04, you may need to download binaries for mp3gain and aacgain. In addition, you'll need to build ffmpeg yourself since version you get from apt-get doesn't include some AAC-related features.

- [mp3gain](https://pkgs.org/ubuntu-14.04/ubuntu-universe-amd64/mp3gain_1.5.2-r2-6_amd64.deb.html)
- [aacgain](https://launchpad.net/~stefanobalocco/+archive/ubuntu/ppa/+packages)
- [ffmpeg](https://github.com/feihong/feihong-setup/blob/master/ubuntu/compile_ffmpeg.sh)

Sources:
- http://www.linuxquestions.org/questions/linux-software-2/best-way-to-extract-aac-from-mp4-losslessly-852936/
- http://archive09.linux.com/feature/59957
- http://ubuntuforums.org/showthread.php?t=2194537

### Python

If you don't already have it, install virtualenvwrapper and pipenv:

`pip3 install virtualenvwrapper pipenv`

Now you can install the Python scripts:

```
git clone https://github.com/feihong/chinese-music-processors
cd chinese-music-processors
mkvirtualenv -p python3 music
pipenv install
```

### Browser

In Firefox, you need to install the Douban Music Metadata add-on:

- Visit the [Debugging Page](about:debugging)
- Check `Enable add-on debugging`
- Click on `Load Temporary Add-on`
- Navigate to the project directory, select `webextension/manifest.json`

## Usage

### 豆瓣音乐 (Douban Music)

#### Download songs

- Visit [豆瓣音乐](https://music.douban.com/), and then click on an artist page, e.g. [放肆的肆](https://site.douban.com/wpoxs/)
- Click on the "play" or "add" button next to song titles to add songs to the [Music Player](https://music.douban.com/artists/player/)
- Click on the Douban Music Metadata icon in your toolbar and select `Automatically download files`
- Songs that you play in the player will automatically download to `~/Downloads/douban-songs`
- Once all songs have been downloaded, click on add-on icon and select `Show metadata`
- A small metadata section will appear at the top of the page
- Click `Copy to clipboard`
- Create a file called `input.json` in project directory and paste the metadata into it
- In terminal, navigate to project directory and run

```
workon music
inv douban
```

### YouTube

Create `input.txt` file that contains metadata for the music videos you want to download from YouTube. Then run:

```
workon music
pipenv install youtube-dl  # upgrade to latest version
inv youtube
```

## References

- https://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu#RevertingChangesMadebyThisGuide
- https://trac.ffmpeg.org/wiki/CompilationGuide/MacOSX
- https://trac.ffmpeg.org/wiki/Encode/AAC
