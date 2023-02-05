from pathlib import Path

input_files = Path('.').glob('*.txt')
for input_file in input_files:
  print(input_file)
