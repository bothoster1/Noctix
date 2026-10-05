import os, sys, zipfile, tempfile, runpy, shutil

ZIP = os.path.join(os.path.dirname(__file__), 'Noctix-GitHub-READY.zip')
APP = os.path.join(tempfile.gettempdir(), 'noctix_app')

shutil.rmtree(APP, ignore_errors=True)
os.makedirs(APP, exist_ok=True)

with zipfile.ZipFile(ZIP) as z:
    z.extractall(APP)

# The packaged ZIP may contain a top-level folder. Find the real launcher.
target = None
for root, dirs, files in os.walk(APP):
    if 'main.py' in files:
        target = os.path.join(root, 'main.py')
        break

if target is None:
    for root, dirs, files in os.walk(APP):
        if 'Noctix.py' in files:
            target = os.path.join(root, 'Noctix.py')
            break

if target is None:
    raise FileNotFoundError('Noctix launcher was not found inside Noctix-GitHub-READY.zip')

APP_ROOT = os.path.dirname(target)
os.chdir(APP_ROOT)
sys.path.insert(0, APP_ROOT)
runpy.run_path(target, run_name='__main__')
