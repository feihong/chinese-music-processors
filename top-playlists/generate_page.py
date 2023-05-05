from pathlib import Path
import sys
import re
import urllib.parse
import jinja2

urlencode = urllib.parse.urlencode

try:
  input_file = Path(sys.argv[1])
except:
  txt_files = sorted(Path('.').glob('*.txt'), key=lambda f: f.stat().st_mtime, reverse=True)
  input_file = txt_files[0]

output_file = Path('output.html')

def get_tracks(input_file):
  for line in input_file.read_text().strip().splitlines():
    try:
      num, artist, title, suffix = re.match(r'(\d+)、(.+)《(.+)》(.*)', line).groups()
      if suffix == '':
        search = f'{title}  {artist}'
        queries_dict = dict(
          music='https://music.youtube.com/search?' + urlencode({'q': search}),
          youtube='https://youtube.com/results?' + urlencode({'search_query': search}),
          google='https://www.google.com/search?' + urlencode({'q': search}),
        )
      else:
        queries_dict = None

      yield dict(
        num=num,
        title=title,
        artist=artist,
        queries=queries_dict,
        link=suffix if suffix.startswith('https://') else None,
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
        {% if track['link'] %}
          <a href="{{ track['link'] }}" target="_blank">link</a>
        {% endif %}
        {% if track['queries'] %}
          <a href="{{ track['queries']['music'] }}" target="_blank">music</a>
          <a href="{{ track['queries']['youtube'] }}" target="_blank">youtube</a>
          <a href="{{ track['queries']['google'] }}" target="_blank">google</a>
        {% endif %}
      </p>
    {% endfor %}
    <!-- allow user to keep scrolling past content -->
    <div style="height:1000px"></div>
  </body>
</html>
""")

output_file.write_text(tmpl.render(tracks=get_tracks(input_file)))
