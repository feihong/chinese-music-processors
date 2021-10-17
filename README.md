# Chinese Music Processors

These are scripts to help you process metadata for music files downloaded from YouTube and [StreetVoice](https://streetvoice.com).

## Prerequisites

### Linux

    curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
    # Update ~/.profile and ~/.bashrc according to instructions, then logout/login

### Mac

    brew update
    brew install pyenv
    echo 'eval "$(pyenv init --path)"' >> ~/.zprofile
    echo 'eval "$(pyenv init -)"' >> ~/.zshrc

### Install latest version of Python 3

    pyenv install 3.10.0
    pyenv global 3.10.0

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

### Python dependencies

    pip install --user --requirement requirements.txt

## References

- https://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu#RevertingChangesMadebyThisGuide
- https://trac.ffmpeg.org/wiki/CompilationGuide/MacOSX
- https://trac.ffmpeg.org/wiki/Encode/AAC
