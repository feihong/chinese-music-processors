# YouTube Processor

## Commands

Process an entire YouTube playlist

    make playlist

Process a single link

    pipenv run inv link <url>

Update youtube-dl

    make update

Clean up files

    make clean

## Instructions for processing YouTube playlist

1. Run `inv update` to update youtube-dl
1. Run `inv clean` to clean out the downloads directory
1. Modify `settings.py` to point to the playlist of your choice
1. Run `inv playlist` to download all songs and metadata from that playlist into downloads. Note that it will always try to download video files in the mp4 format.
1. Basic metadata from YouTube is put into `youtube.json`
1. Edit `youtube.json` so that the metadata for each file is the way that you want. Note that you can't proceed to the next step unless you fill in the artist field.
1. Re-run `inv playlist` to convert all mp4 files into m4a files that contain the metadata from `youtube.json`
