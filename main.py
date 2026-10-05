import os, sys, zipfile, tempfile, runpy, shutil, sqlite3

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

# Runtime compatibility patch:
# the packaged legacy Tools module calls asyncio.run() while it is being
# imported by the bot event loop. That raises "asyncio.run() cannot be
# called from a running event loop". Remove that import-time call and
# initialize the small prefix database safely before the bot starts.
tools_path = os.path.join(APP_ROOT, 'bot', 'utils', 'Tools.py')
if os.path.isfile(tools_path):
    with open(tools_path, 'r', encoding='utf-8') as f:
        tools_code = f.read()
    tools_code = tools_code.replace(
        'asyncio.run(setup_db())',
        '# Import-time asyncio.run removed by the production launcher.'
    )
    with open(tools_path, 'w', encoding='utf-8') as f:
        f.write(tools_code)

db_dir = os.path.join(APP_ROOT, 'bot', 'db')
os.makedirs(db_dir, exist_ok=True)
prefix_db = os.path.join(db_dir, 'prefix.db')
with sqlite3.connect(prefix_db) as db:
    db.execute(
        'CREATE TABLE IF NOT EXISTS prefixes '
        '(guild_id INTEGER PRIMARY KEY, prefix TEXT NOT NULL)'
    )
    db.commit()

os.chdir(APP_ROOT)
sys.path.insert(0, APP_ROOT)
runpy.run_path(target, run_name='__main__')
