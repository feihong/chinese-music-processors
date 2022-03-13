from pathlib import Path
import subprocess


downloads_dir = Path('~/Downloads').expanduser()

for i, mp3_file in enumerate(downloads_dir.glob('*.mp3'), 1):
  output_file = downloads_dir / f'output_{i}.m4a'

  subprocess.run([
      'ffmpeg',
      "-y", # overwrite if file already exists
      "-i", mp3_file,
      "-vn", # ignore video
      "-c:a", "libfdk_aac", # use best encoder
      "-vbr", "4", # use high quality (5 is highest)
      output_file,
    ])

  subprocess.run([
    'aacgain',
    "-r", # apply Track gain automatically (all files set to equal loudness)
    "-k", # automatically lower Track/Album gain to not clip audio
    output_file,
  ])

  print(f'Converted {mp3_file} to {output_file}')
