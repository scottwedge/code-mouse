import os
from subprocess import check_output
from output import print_output
from commit import parse_commits
from logic import compute_current_weight

'''
This script is run from the post-commit git hook. It checks for the environment variables
MOUSE_WEIGHT to see if there is an existing state. If there is, it computes the weight delta given
the existing weight, time of last meal, and the changes and timestamp from the current commit.
Otherwise, it uses the following command to compute the historical weight:

git log --author="author" --format="commit %H %at %s" --numstat

The git config command is used to obtain the user's name:

git config --list | grep '^user.name'

If no username is set, the mouse will feed on every author's code contributions, rather
promiscuously. After it computes the weight, it updates the environment variable with the current
weight for next time. This is because the weight periodically returns to 0 if the mouse gets fed
too much.
'''

author = check_output([
    'git',
    'config',
    '--get',
    'user.name',
])

mouse_weight = os.environ.get('MOUSE_WEIGHT')
try:
    mouse_weight = float(mouse_weight)
except ValueError:
    mouse_weight = None

commit_history = check_output([
    'git',
    'log',
    '--author={0}'.format(author),
    '--format="commit %H %at %s"',
    '--numstat',
])
commits = parse_commits(commit_history)
weight = compute_current_weight(commits, mouse_weight)
print_output(weight)

os.environ['MOUSE_WEIGHT'] = str(weight)
