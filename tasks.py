import subprocess
from invoke import task


@task
def douban(ctx, yaml_file=None):
    "Process songs from Douban Music"
    from douban import process
    process(yaml_file)


@task
def youtube(ctx, input_file):
    "Process songs from YouTube"
    from youtube import process
    process(input_file)


@task
def m4a(ctx):
    "Process m4a files"
    from m4a_file import process
    process()
