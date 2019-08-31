import typing
import re
from pathlib import Path
import mitmproxy.http
from mitmproxy import ctx

class MyAddon:
  def response(self, flow: mitmproxy.http.HTTPFlow):
    """
    The full HTTP response has been read.
    """
    content_type = flow.response.headers.get('content-type')
    path = flow.request.path
    match = re.match(r'\/song_covers\/\w+\/\w+\/\w+\/(\w+)[.]', path)
    if match and 'h_610' in path and content_type.startswith('image'):
      ctx.log.info(flow.request.path)
      image_id = match.group(1)
      _, ext = content_type.split('/')
      image_file = (Path('cover-art') / image_id).with_suffix('.' + ext)
      ctx.log.info(str(image_file))
      image_file.write_bytes(flow.response.content)

addons = [
  MyAddon()
]
