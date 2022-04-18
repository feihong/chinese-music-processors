from pathlib import Path
import re
import urllib.parse
import jinja2

input_file = Path('2020-2021-hot.txt')
output_file = Path('output.html')

def get_tracks():
  for line in input_file.read_text().strip().splitlines():
    try:
      num, title, artist = re.match(r'(\d+)、(.+)《(.+)》', line).groups()
      query = 'https://www.youtube.com/results?' + urllib.parse.urlencode({'search_query': f'{title}  {artist}'})
      yield dict(num=num, title=title, artist=artist, query=query)
    except:
      continue

tmpl = jinja2.Template("""
<!doctype html>
<html lang="en">
  <head>
    <title>EarGod List</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no, viewport-fit=cover">
  </head>
  <body>
    {% for track in tracks %}
      <p>
        {{ track['num'] }}
        <a href="{{ track['query'] }}" target="_blank">{{ track['title'] }}</a>
        ✪ {{ track['artist'] }}
      </p>
    {% endfor %}
  </body>
</html>
""")

output_file.write_text(tmpl.render(tracks=get_tracks()))
