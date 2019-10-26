# YouTube Processor

## Commands

Process an entire YouTube playlist

    inv playlist

Process a single link

    inv link <url>

Update youtube-dl

    inv update

Clean up files

    inv clean

## Instructions for processing YouTube playlist

1. Run `inv update` to update youtube-dl
1. Run `inv clean` to clean out the downloads directory
1. Modify `settings.py` to point to the playlist of your choice
1. Run `inv playlist` to download all songs and metadata from that playlist into downloads. Note that it will always try to download video files in the mp4 format.
1. Basic metadata from YouTube is put into `youtube.csv`, copy that file and name it `youtube-rewrite.csv`
1. Edit `youtube-rewrite.csv` so that the metadata for each file is the way that you want
1. Re-run `inv playlist` to convert all mp4 files into m4a files that contain the metadata from `youtube-rewrite.csv`
