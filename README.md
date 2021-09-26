# Chinese Music Processors

These are scripts to help you process metadata for music files downloaded from YouTube and [StreetVoice](https://streetvoice.com).

## Installation

### Mac

```
brew install aacgain atomicparsley wget
brew install ffmpeg --with-fdk-aac
```

### Linux

Install dependencies on Ubuntu:

```
sudo apt-get install ffmpeg atomicparsley mp3gain
sudo snap install aacgain
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

If you don't already have it, install pipenv:

```
pip3 install --user pipenv
```

Now you can install the Python scripts:

```
git clone https://github.com/feihong/chinese-music-processors
cd chinese-music-processors
pipenv install
```

## References

- https://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu#RevertingChangesMadebyThisGuide
- https://trac.ffmpeg.org/wiki/CompilationGuide/MacOSX
- https://trac.ffmpeg.org/wiki/Encode/AAC
