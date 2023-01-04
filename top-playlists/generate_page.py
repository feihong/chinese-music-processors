from pathlib import Path
import re
import urllib.parse
import jinja2

urlencode = urllib.parse.urlencode

input_file = Path('mandogap-albums-2022.txt')
output_file = Path('output.html')

def get_tracks():
  for line in input_file.read_text().strip().splitlines():
    try:
      num, artist, title = re.match(r'(\d+)、(.+)《(.+)》', line).groups()
      search = f'{title}  {artist}'
      yield dict(
        num=num,
        title=title,
        artist=artist,
        music_query='https://music.youtube.com/search?' + urlencode({'q': search}),
        youtube_query='https://youtube.com/results?' + urlencode({'search_query': search}),
        google_query='https://www.google.com/search?' + urlencode({'q': search})
      )
    except:
      continue

tmpl = jinja2.Template("""
<!doctype html>
<html lang="en">
  <head>
    <title>Top Playlist</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no, viewport-fit=cover">
  </head>
  <body>
    {% for track in tracks %}
      <p>
        {{ track['num'] }}《{{ track['title'] }}》{{ track['artist'] }}
        <a href="{{ track['music_query'] }}" target="_blank">music</a>
        <a href="{{ track['youtube_query'] }}" target="_blank">youtube</a>
        <a href="{{ track['google_query'] }}" target="_blank">google</a>
      </p>
    {% endfor %}
  </body>
</html>
""")

output_file.write_text(tmpl.render(tracks=get_tracks()))
