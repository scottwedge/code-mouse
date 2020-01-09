import os
import sys
import time
import emoji
import logic
from colored import fg, bg, stylize
from commit import parse_commits
from subprocess import check_output

'''
This script is run in the post-commit git hook. It checks for the environment variable MOUSE_WEIGHT
to see if there is an existing mouse weight. If there is, it computes the weight delta given the
existing mouse weight and the current commit. Otherwise it uses the following command to compute the
historical weight:

git log --author="author" --format="commit %H %at %s" --numstat

The git config command is used to obtain the user's name:

git config --list | grep '^user.name'

If no username is set, the mouse will feed on every author's code contributions, rather
promiscuously. After it computes the weight, it updates the environment variable with the current
weight for next time. This is because the weight periodically returns to 0 if the mouse gets fed
too much.
'''

MAX_BAR_SIZE = 55
ANIMATION_TIME = 0.3

def get_bar_size():
    _, columns = os.popen('stty size', 'r').read().split()
    return min(int(columns) - 10, MAX_BAR_SIZE)

def animate(strength):
    strength_bar_total_size = get_bar_size()
    strength_bar_size = float(strength) / 100 * strength_bar_total_size
    sleep_time = ANIMATION_TIME / strength_bar_size
    for i in range(int(strength_bar_size)):
        time.sleep(sleep_time)
        strength = stylize(' ' * i, bg(state['color']))
        bar = '0% ' + strength + (' ' * (strength_bar_total_size - i)) + '100%'
        sys.stdout.write("\r" + bar)
        sys.stdout.flush()

author = check_output([
    'git',
    'config',
    '--get',
    'user.name',
])
commit_history = check_output([
    'git',
    'log',
    '--author={0}'.format(author),
    '--format="commit %H %at %s"',
    '--numstat',
])
commits = parse_commits(commit_history)
weight = logic.compute_current_weight(commits)
state = logic.get_state_from_weight(weight)
strength = logic.get_strength_from_weight(weight)
strength_str = logic.get_strength_str_from_weight(weight)
mouse = emoji.emojize(':mouse_face:')
face = emoji.emojize(':{0}:'.format(state['emoji']))

output_str = stylize('{0} {1}'.format(strength_str, state['caption']), fg(state['color']))
if strength > logic.MAX_WEIGHT:
    output_str = emoji.emojize(':exclamation_mark:') + ' ' + output_str
else:
    output_str = stylize('Thank you :D ', fg(state['color'])) + output_str
print('\n' + output_str + ' ' + mouse + ' ' + face)

if strength > 0 and strength <= logic.MAX_WEIGHT:
    animate(strength)

print('\n')
