from concurrent.futures import process
import sys
from pathlib import Path
from datetime import datetime
import shutil
from dotenv import dotenv_values

target_dir = Path(dotenv_values('.env')['target_dir']).expanduser()

today = datetime.today()
month_dir = target_dir / f'{today.year}-{today.month:02}'
if not month_dir.exists():
  month_dir.mkdir()

processed_songs = list(Path('.').glob('**/output/*.m4a'))
for file in processed_songs:
  print(file)

result = input(f'\nMove these {len(processed_songs)} files to {month_dir}? ')
if result.strip().lower() == 'n':
  sys.exit(0)

for file in processed_songs:
  shutil.move(file, month_dir)
