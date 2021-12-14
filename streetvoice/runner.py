import sys
import signal
import time
import subprocess

mode, *scripts = sys.argv[1:]

def run_script(name):
  cmd = None
  if name.endswith('.py'):
    cmd = ['python', 'src/' + name]
  elif name.endswith('.js'):
    cmd = ['node', 'src/' + name]
  else:
    cmd = ['make', name]

  print(' '.join(cmd))
  return subprocess.Popen(cmd)

if mode == 'sequential':
  for script in scripts:
    process = run_script(script)
    process.wait()
elif mode == 'parallel':
  processes = [run_script(s) for s in scripts]

  def signal_handler(signum, frame):
    for p in processes:
      p.terminate()
    sys.exit(0)

  signal.signal(signal.SIGINT, signal_handler)

  while True:
    time.sleep(60)
