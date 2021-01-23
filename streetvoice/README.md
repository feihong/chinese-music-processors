# StreetVoice scraper

## Prerequisites

    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.37.1/install.sh | bash
    brew install aacgain atomicparsley mitmproxy
    brew install ffmpeg --with-fdk-aac

## Installation

    yarn install

To proxy https, visit the [magic domain mitm.it](http://mitm.it) and follow the instructions to install the mitmproxy certificate.

## Usage

1. `source ~/.nvm/nvm.sh` (if `nvm` is not started automatically in `~/.bash_profile`)
1. `yarn upgrade:python` to upgrade mitmproxy and other Python dependencies (optional)
1. `yarn clean` to clear downloaded assets from previous run
1. `yarn start`
1. Load a playlist page ([example](https://streetvoice.com/megafeihong/playlists/608652/))
1. Start playing playlist
1. Switch to album cover mode
1. To help keep track of progress, click '列表' on the top menu
1. Don't let your computer go to sleep
1. Wait until all tracks have played
1. `ctrl+c` to stop proxy
1. `yarn process` to start generation of `m4a` files
1. Generated files will be in `output` folder

## Commands

    mitmdump -ns addons/list_paths.py -r dumpfile
    mitmdump -ns addons/dump_all_cover_art.py -r dumpfile

## Types of urls

Song metadata (html): https://streetvoice.com/megafeihong/playlists/583232/

Lyrics (json): https://streetvoice.com/api/v3/songs/579453/?only_fields=lyrics,lyrics_is_lrc&_=1555736582256

Link song id to audio filename (json): https://streetvoice.com/api/v3/songs/579029/hls/

Single slice of audio: https://cfhls.streetvoice.com/music/mi/ss/missbac/UFytKaN2SdsVNuToEZmbEk.mp3.hls.mp3-00019.ts

Cover art: https://cfstatic.streetvoice.com/song_covers/go/od/goodband/eHuHxnUpXxqEt4j8a7i9Za.jpg?x-oss-process=image/resize,m_fill,h_610,w_610,limit_0/interlace,1/quality,q_85/format,jpg

## Troublshooting

If mitmproxy reports inability to connect to certain servers, then you may need to upgrade it by running
`yarn upgrade:python`.
