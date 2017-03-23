import subprocess
from invoke import task


@task
def douban(ctx):
    "Process songs from Douban Music"
    pass


@task
def youtube(ctx):
    "Process songs from YouTube"
    pass
