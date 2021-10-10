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

The version of ffmpeg in the repository won't include Fraunhofer FDK AAC encoder (libfdk_aac). You'll need to compile ffmpeg yourself to get access to that encoder: https://gist.github.com/rafaelbiriba/7f2d7c6f6c3d6ae2a5cb

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
