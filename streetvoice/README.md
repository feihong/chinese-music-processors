# StreetVoice scraper

## Installation

Install Python dependencies:

    make install

You have to manually install the mitmproxy certificate in Firefox:

1. Visit the [magic domain mitm.it](http://mitm.it) and download the .pem file
1. Open Certificate Manager by going to Preferences > Privacy & Security > Security > Certificates > View Certificates...
1. Click Import...
1. Select .pem file you downloaded
1. Tick both checkboxes
1. In the Authorities tab, you should see mitmproxy

## Usage

1. `make upgrade` to upgrade mitmproxy (optional)
1. `make clean` to clear downloaded assets from previous run
1. Start the proxy: `make proxy`
1. Open playlist page
1. Start playing playlist
1. Switch to album cover mode
1. To help keep track of progress, click '列表' on the top menu
1. Don't let your computer go to sleep
1. Wait until all tracks have played
1. `ctrl+c` to stop proxy
1. `make process` to start generation of `m4a` files
1. Generated files will be in `output` folder

## Commands

View contents of dumpfile visually

    mitmweb -r dumpfile

## Troubleshooting

If mitmproxy reports inability to connect to certain servers, then you may need to upgrade it by running
`make upgrade`.

## Notes

We now only support Firefox because it works well with mitmproxy and it's pretty easy to configure.

We used to use Brave because its [command line interface is quite convenient](https://support.brave.com/hc/en-us/articles/360044860011-How-Do-I-Use-Command-Line-Flags-in-Brave-) was quite convenient and nice. However, Brave no longer seems to work with mitmproxy.

In the past, we used Puppeteer to open up a separate browser instance that is automatically configured to use mitmproxy. This is convenient, but Puppeteer eats up CPU like crazy. Playwright is similar to Puppeteer and has a somewhat nicer API, but after opening a browser window, it can't download any media files (this issue appears on both Mac and Linux).
