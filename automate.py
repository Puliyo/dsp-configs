from git import Repo
from pathlib import Path

from scripts.logger import get_logger
from scripts.hosts import generate

"""
First you will need to setup authentication and clone.
Start python in interpreter mode and import this script, run the clone method.d

Once authentication and cloning complete, this script can be called (python3 <this-script>)
to pull, run the generate methods in each scripts under scripts directory, and push.
"""

pwd = Path(__file__).resolve().parent

logger = get_logger(__name__)

def clone(username: str, password: str):
    remote = f"https://{username}:{password}@github.com/Puliyo/dsp-configs.git"
    Repo.clone_from(remote, pwd)

def run_scripts():
    generate(pwd)

if __name__ == '__main__':
    # git pull
    logger.info('running git pull')
    repo = Repo(pwd)
    repo.git.pull()
    # generate
    logger.info('running generators')
    run_scripts()
    # git push
    logger.info('running add all')
    repo.git.add(all=True)
    repo.git.commit('-m', 'Auto commit change')
    origin = repo.remote(name="origin")
    logger.info('running push')
    origin.push()
