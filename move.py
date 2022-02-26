from concurrent.futures import process
import sys
from pathlib import Path
from datetime import datetime
import shutil
from dotenv import dotenv_values

config = dotenv_values('.env')

today = datetime.today()
target_dir = Path(config['target_dir']).expanduser() / f'{today.year}-{today.month:02}'
if not target_dir.exists():
  target_dir.mkdir()

processed_songs = list(Path('.').glob('**/output/*.m4a'))
for file in processed_songs:
  print(file)

result = input(f'\nMove these {len(processed_songs)} files to {target_dir}? ')
if result.strip().lower() == 'n':
  sys.exit(0)

for file in processed_songs:
  shutil.move(file, target_dir)
