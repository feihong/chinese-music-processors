# StreetVoice scraper

## Installation

    make install

You have to manually install the mitmproxy certificate:

1. Visit the [magic domain mitm.it](http://mitm.it) and download the .pem file (you might have to do this Firefox)
1. Open Brave
1. Go to Settings > Privacy & security > Security > Manage certificates > Authorities
1. Click Import
1. Select .pem file you downloaded
1. In the Authorities, you should see org-mitmproxy

## Usage

1. Close all Brave browser windows (to guarantee that traffic goes through proxy)
1. `make upgrade` to upgrade mitmproxy (optional)
1. `make clean` to clear downloaded assets from previous run
1. `yarn start`
1. Open playlist page
1. Start playing playlist
1. Switch to album cover mode
1. To help keep track of progress, click '列表' on the top menu
1. Don't let your computer go to sleep
1. Wait until all tracks have played
1. `ctrl+c` to stop proxy and browser
1. `yarn process` to start generation of `m4a` files
1. Generated files will be in `output` folder

## Commands

    mitmdump -ns addons/list_paths.py -r dumpfile
    mitmdump -ns addons/dump_all_cover_art.py -r dumpfile

## Troubleshooting

If mitmproxy reports inability to connect to certain servers, then you may need to upgrade it by running
`make upgrade`.

## Todo

- Replace `npm-run-all` with `parallel` command
- Rewrite scripts in Deno instead of Node

## Notes

Currently we use Brave because its [command line interface is quite convenient](https://support.brave.com/hc/en-us/articles/360044860011-How-Do-I-Use-Command-Line-Flags-in-Brave-).

In the past, we used Puppeteer to open up a separate browser instance that is automatically configured to use mitmproxy. This is convenient, but Puppeteer eats up CPU like crazy. Playwright is similar to Puppeteer and has a somewhat nicer API, but after opening a browser window, it can't download any media files (this issue appears on both Mac and Linux).
