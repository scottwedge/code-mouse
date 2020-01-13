import os
import stat
import configparser
from datetime import datetime
from subprocess import check_output
from codemouse.meal import Meal
from codemouse.config import Config

def get_path(fname=''):
    return os.path.join(os.getenv('HOME'), '.codemouse', fname)

def touch(fname):
    fp = open(get_path(fname), 'w')
    fp.close()

# TODO use class instead
def copy_config():
    config = '''
    [engine]
    duration = 'days'
    min_weight = 0.
    max_weight = 100.
    start_weight = 30.
    max_weight_after_full = 250.
    rate_of_decay = 1.
    rate_of_growth = 1 / 20.
    satiation_interval = 1.
    '''
    fp = open(get_path('config'), 'w')
    for line in config.splitlines():
        fp.write('{0}\n'.format(line))
    fp.close()

def is_git_repo(path):
    return os.path.exists(os.path.join(path, '.git'))

def init_directory():
    path = get_path()
    if not os.path.exists(path):
        os.mkdir(path)
        touch('projects')
        touch('history')
        copy_config()

def load_config():
    init_directory()
    config = configparser.ConfigParser()
    config.read(get_path('config'))
    return Config(config['engine'])

def load_projects():
    path = get_path('projects')
    return open(path).read().splitlines()

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
    # Make file executable
    os.chmod(hook, stat.S_IRWXU)
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
