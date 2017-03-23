import subprocess
from invoke import task


@task
def douban(ctx, yaml_file=None):
    "Process songs from Douban Music"
    from douban import process
    process(yaml_file)


@task
def youtube(ctx):
    "Process songs from YouTube"
    pass
