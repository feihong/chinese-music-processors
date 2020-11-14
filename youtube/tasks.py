import subprocess
import os
from pathlib import Path
from invoke import task


@task
def update(ctx):
  """
  Update dependencies such as youtube-dl, etc.

  """
  subprocess.call(['pipenv', 'update'])


@task
def clean(ctx):
  """
  Clean up files

  """
  import main

  def rm(file_):
    if file_.exists():
      os.remove(file_)

  rm(main.json_file)

  for file_ in main.download_dir.iterdir():
    if file_.name != '.gitkeep':
      os.remove(file_)


@task
def playlist(ctx):
  """
  Process YouTube playlist

  """
  import main
  main.process_playlist()


@task
def link(ctx, url):
  """
  Process video link

  """
  import main
  main.process_link(url)
