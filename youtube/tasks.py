import subprocess
import os
from pathlib import Path
from invoke import task


@task
def clean(ctx):
  """
  Clean up files

  """
  import main

  def rm(file_):
    if file_.exists():
      os.remove(file_)

  rm(main.csv_file)
  rm(main.rewrite_csv_file)

  for file_ in download_dir.iter_dir():
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
