import os, sys, zipfile, tempfile, runpy

ZIP = os.path.join(os.path.dirname(__file__), 'Noctix-GitHub-READY.zip')
APP = os.path.join(tempfile.gettempdir(), 'noctix_app')
if not os.path.isdir(APP) or not os.path.exists(os.path.join(APP, 'main.py')):
    import shutil
    shutil.rmtree(APP, ignore_errors=True)
    os.makedirs(APP, exist_ok=True)
    with zipfile.ZipFile(ZIP) as z:
        z.extractall(APP)
os.chdir(APP)
sys.path.insert(0, APP)
runpy.run_path(os.path.join(APP, 'main.py'), run_name='__main__')
