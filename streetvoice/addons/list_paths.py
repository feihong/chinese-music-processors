import typing

import mitmproxy.http
from mitmproxy import ctx

class MyAddon:
  def response(self, flow: mitmproxy.http.HTTPFlow):
    """
    The full HTTP response has been read.
    """
    content_type = flow.response.headers.get('content-type')
    if not 'h_610' in flow.request.path:
      return
    # if not content_type.startswith('image'):
    #   return
    # if not flow.request.path.endswith('.ts'):
    #   return
    # if 'playlists' not in flow.request.path:
    #   return

    ctx.log.info(flow.request.path)
    ctx.log.info('  %s' % flow.response.status_code)
    if not content_type:
      ctx.log.warn('  no content-type')
    else:
      ctx.log.info('  ' + content_type)

addons = [
  MyAddon()
]
