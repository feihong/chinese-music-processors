# Chinese Music Processors

These are scripts to help you process metadata for music files downloaded from YouTube and [StreetVoice](https://streetvoice.com).

## Prerequisites

Python 3

## Installation

Install Python dependencies:

    make install

Create `.env` file for store some settings

    cp .env.example .env

### Mac dependencies

    brew install aacgain atomicparsley imagemagick
    brew tap homebrew-ffmpeg/ffmpeg
    brew install homebrew-ffmpeg/ffmpeg/ffmpeg --with-fdk-aac

### Linux dependencies

    sudo apt-get install atomicparsley mp3gain imagemagick
    sudo snap install aacgain

### ffmpeg

The version of ffmpeg in the repository has an inferior AAC encoder and doesn't include the much better Fraunhofer FDK AAC encoder (libfdk_aac). You'll need to compile ffmpeg yourself to get access to that encoder.

Install ffmpeg build dependencies:

```
sudo apt-get update -qq && sudo apt-get -y install \
  autoconf \
  automake \
  build-essential \
  cmake \
  git-core \
  libass-dev \
  libfreetype6-dev \
  libgnutls28-dev \
  libmp3lame-dev \
  libsdl2-dev \
  libtool \
  libva-dev \
  libvdpau-dev \
  libvorbis-dev \
  libxcb1-dev \
  libxcb-shm0-dev \
  libxcb-xfixes0-dev \
  meson \
  ninja-build \
  pkg-config \
  texinfo \
  wget \
  yasm \
  zlib1g-dev
```

Install dependencies for popular features:

```
sudo apt-get install libx264-dev libx265-dev libnuma-dev libfdk-aac-dev
```

Compile with some unneeded features disabled:

```
mkdir -p ~/ffmpeg_sources ~/bin
cd ~/ffmpeg_sources
wget -O ffmpeg-snapshot.tar.bz2 https://ffmpeg.org/releases/ffmpeg-snapshot.tar.bz2
tar xjvf ffmpeg-snapshot.tar.bz2
cd ffmpeg
PATH="$HOME/bin:$PATH" PKG_CONFIG_PATH="$HOME/ffmpeg_build/lib/pkgconfig" ./configure \
  --prefix="$HOME/ffmpeg_build" \
  --pkg-config-flags="--static" \
  --extra-cflags="-I$HOME/ffmpeg_build/include" \
  --extra-ldflags="-L$HOME/ffmpeg_build/lib" \
  --extra-libs="-lpthread -lm" \
  --ld="g++" \
  --bindir="$HOME/bin" \
  --enable-gpl \
  --enable-gnutls \
  --enable-libfdk-aac \
  --enable-libfreetype \
  --enable-libx264 \
  --enable-libx265 \
  --enable-nonfree
PATH="$HOME/bin:$PATH" make
make install
hash -r
```

Compilation takes a pretty good chunk of time. Remember to clean up the `ffmpeg_sources` and `ffmpeg_build` directories after you're done.

## References

- https://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu
- https://trac.ffmpeg.org/wiki/CompilationGuide/MacOSX
- https://trac.ffmpeg.org/wiki/Encode/AAC
- [MP4 tags](https://mutagen.readthedocs.io/en/latest/api/mp4.html?highlight=FORMAT_JPEG#mutagen.mp4.MP4Tags)
