# Convert MP3 files to AAC format

Works for `music.163.com` and `muxiv.net`.

## Muxiv.net

Seems like Firefox is the best browser to download the MP3 files from Muxiv. However, `Save All As HAR` doesn't work. The best method is:

1. Right-click on the `.mp3` link
1. Select `Copy > Copy as cURL`
1. Open terminal, `cd` to `~/Downloads`, paste the command, adding `--output input.mp3` to the end to save to a file

## Commands

Convert all MP3 files in `Downloads` directory and convert them all to M4A files:

    make
