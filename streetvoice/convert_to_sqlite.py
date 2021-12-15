"""
Dump flows into sqlite database so that you can randomly access them.
"""
import os.path
import sqlite3
import mitmproxy.http
from mitmproxy import ctx

class MyAddon:
    def __init__(self):
      filename = 'dumpfile.db'
      if os.path.exists(filename):
        os.remove(filename)
      self.conn = sqlite3.connect(filename)
      self.conn.execute('CREATE TABLE dump (path text, content_type text, data blob)')

    def response(self, flow: mitmproxy.http.HTTPFlow):
      """
      The full HTTP response has been read.
      """
      try:
        # ctx.log.info(flow.request.path)
        res = flow.response
        content_type = res.headers.get('content-type')
        if content_type:
          self.conn.execute(
            'INSERT INTO dump VALUES (?, ?, ?)',
            (
              flow.request.path,
              content_type,
              res.content,
            )
          )
      except Exception as e:
        ctx.log.error(str(e))

    def done(self):
      self.conn.commit()
      self.conn.close()
      print('\nDone!\n')

addons = [
  MyAddon()
]
