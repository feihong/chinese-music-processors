# This module is deprecated, use Makefile again
from pathlib import Path
from invoke import task


@task
def playlist(ctx, url=None):
  """
  Process YouTube playlist

  """
  import main
  main.process_playlist(url)


@task
def link(ctx, url):
  """
  Process video link

  """
  import main
  main.process_link(url)


@task
def search_urls(ctx):
  """
  For each track, print a lyrics search url

  """
  import main
  main.print_search_urls()
