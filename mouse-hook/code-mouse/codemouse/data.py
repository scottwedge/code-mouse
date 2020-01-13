import os
import configparser
from meal import Meal
from config import Config
from datetime import datetime
from subprocess import check_output

def get_path(fname, home=None):
    if home is None:
        home = os.getenv('HOME')
    return os.path.join(home, '.codemouse', fname)

def is_git_repo(path):
    return os.path.exists(os.path.join(path, '.git'))

def load_config():
    config = configparser.ConfigParser()
    config.read(get_path('config'))
    return Config(config['engine'])

def load_projects():
    path = get_path('projects')
    return open(path).read().splitlines()

'''
project\tcommit\ttimestamp\tchanges\tweight
'''
def load_history():
    path = get_path('history')
    history = []
    for line in open(path).read().splitlines():
        project, commit, timestamp, message, changes, weight = line.split('\t')
        history.append(Meal(
            project,
            commit,
            datetime.fromtimestamp(float(timestamp)),
            message,
            float(changes),
            weight=float(weight)
        ))
    return history

# TODO check for chmod
def add_project(path):
    # Check if path exists and is git repo
    if path is None:
        path = os.path.abspath('.')
    if not os.path.exists(path):
        return 'Project does not exist. Please provide a path to the parent directory of an existing git repository.'
    if not is_git_repo(path):
        return 'Project is not a git repository. Please provide a path to the parent directory of an existing git repository.'
    # Check if project already exists
    if project_exists(path):
        return 'Project already exists.'
    # Inject codemouse call into git hook
    hook = os.path.join(path, '.git', 'hooks', 'post-commit')
    hfp = open(hook, 'a')
    hfp.write('codemouse update --project {0}\n'.format(path))
    hfp.close()
    # Update list of projects
    fp = open(get_path('projects'), 'a')
    fp.write('{0}\n'.format(path))
    fp.close()
    project_name = os.path.basename(path)
    return 'Added {0} to the list of projects your mouse feeds from.'.format(project_name)

def is_injected_line(line):
    is_comment = line == '# Used to recompute codemouse health'
    is_code = line.startswith('codemouse update')
    return is_comment or is_code

def project_exists(path):
    projects = open(get_path('projects')).read().splitlines()
    return path in projects

def update_projects():
    projects = load_projects()
    for project_path in projects:
        hook = os.path.join(project_path, '.git', 'hooks', 'post-commit')
        lines = open(hook).read().splitlines()
        with open(hook, 'w') as hfp:
            for line in lines:
                if not is_injected_line(line):
                    hfp.write(line)
                
def update_history(latest):
    fp = open(get_path('history'), 'a')
    fp.write('{0}\n'.format(repr(latest)))
    fp.close()

def get_latest_commit(project_path):
    author = check_output([
        'git',
        'config',
        '--get',
        'user.name',
    ]).strip().decode('utf-8')
    path = os.path.join(project_path, '.git')
    commit = check_output([
        'git',
        '--git-dir',
        path,
        'log',
        '-1',
        '--author={0}'.format(author),
        '--format="commit %H %at %s"',
        '--numstat',
    ]).decode('utf-8')
    return parse_commit(commit, project_path)

def parse_commit(log_output, project_path):
    log_output = log_output.splitlines()
    commit_line = log_output[0].split()
    commit = commit_line[1]
    timestamp = datetime.fromtimestamp(float(commit_line[2]))
    message = ' '.join(commit_line[3:]).strip('"')
    changes = 0
    # The next line is always empty
    for line in log_output[2:]:
        i, d, _ = line.split('\t')
        changes += int(i) + int(d)
    return Meal(project_path, commit, timestamp, message, changes)

'''
arg log_output: result of call to
    git log --author="author" --format="commit %H %at %s" --numstat

commit ee57f69f622c0ade639b8748f3bc4d169e8343c 1578516928 test

2       0       mouse-hook/commit.py
16      0       mouse-hook/logic.py
1       0       test
commit dfe0df38bb16479a13976674f05f3ca4a5e6d1ee 1578514210 test

1       0       test
commit 1611f9efe69e46450890f1ca2ca2559cb9d4c735 1578513385 .gitignore

1       0       .gitignore
'''
def parse_commits(log_output):
    commits = []
    lines = log_output.decode('utf-8').splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        if line.startswith('"commit'):
            commit_line = line.split()
            commit = commit_line[1]
            timestamp = datetime.fromtimestamp(int(commit_line[2]))
            message = ' '.join(commit_line[3:]).strip('"')
            # The next line is always empty
            index += 2
            line = lines[index]
            insertions = 0
            deletions = 0
            while not line.startswith('"commit'):
                i, d, _ = line.split('\t')
                insertions += int(i)
                deletions += int(d)
                index += 1
                if index == len(lines):
                    break
                line = lines[index]
            # Keep list sorted in ascending order by time for clarity
            commits.insert(0, Commit(commit, timestamp, message, insertions, deletions))
    return commits
