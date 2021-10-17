import sys
from main import process_playlist

try:
  url = sys.argv[1]
except:
  url = None

process_playlist(url)
