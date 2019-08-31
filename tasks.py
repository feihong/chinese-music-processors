import subprocess
from invoke import task


@task
def douban(ctx, input_file='input.json'):
    "Process songs from Douban Music"
    from douban import process
    process(input_file)


@task
def youtube(ctx, input_file='input.txt'):
    "Process songs from YouTube"
    import youtube2
    youtube2.process(input_file)


@task
def m4a(ctx):
    "Process m4a files"
    from m4a_file import process
    process()
