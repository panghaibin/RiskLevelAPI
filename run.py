import os
from git import Repo
from risklevel import main as risklevel_main

ABS_PATH = os.path.dirname(os.path.abspath(__file__))
API_PATH = os.path.join(ABS_PATH, 'Archive')

if not os.path.exists(API_PATH):
    clone_path = input('Please input the path of the repository with GitHub token: ')
    repo = Repo.clone_from(clone_path, API_PATH)
    # switch branch to 'api'
    repo.git.checkout('api')
    repo.git.pull()

assert os.path.exists(os.path.join(API_PATH, 'latest.json'))

repo = Repo(API_PATH)
# pull the latest changes
repo.git.pull()

fetch_result = risklevel_main()
if fetch_result:
    repo.git.add(update=True)
    # commit as "Update at `TZ=Asia/Shanghai date`"
    repo.git.commit('-m', os.popen('echo "Update at `TZ=Asia/Shanghai date`"').read().strip())
    # push to remote
    repo.git.push()
    print('Update successful')
else:
    print('No update')
