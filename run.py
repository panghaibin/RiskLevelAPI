import os
import sys
from git import Repo
from datetime import datetime, timezone, timedelta
from risklevel import main as risklevel_main

ABS_PATH = os.path.dirname(os.path.abspath(__file__))
API_PATH = os.path.join(ABS_PATH, 'Archive')


if len(sys.argv) == 2 and sys.argv[1] == 'init':
    clone_path = input('Input the remote repository path: ')
    print('Cloning...')
    repo = Repo.clone_from(clone_path, API_PATH)
    repo.git.checkout('api')
    repo.git.pull()
    print('API folder initialized')
    print('Run `python3 run.py` to start fetching data')
    sys.exit(0)

if not os.path.exists(API_PATH):
    print('API folder not found.')
    print('Run `python3 run.py init` to initialize the API folder.')
    sys.exit(1)

repo = Repo(API_PATH)
repo.git.pull()
assert os.path.exists(os.path.join(API_PATH, 'latest.json'))

fetch_result = risklevel_main()
if fetch_result:
    repo.git.add(update=True)
    # get commit message as "Update at Sat Aug 13 22:29:33 CST 2022"
    current_time = datetime.now(tz=timezone(timedelta(hours=8))).strftime("%a %b %d %H:%M:%S %z %Y")
    current_time = current_time.replace('+0800', 'CST')
    repo.git.commit('-m', f'Update at {current_time}')
    repo.git.push()
    print('Update successful')
else:
    print('No update needed')
