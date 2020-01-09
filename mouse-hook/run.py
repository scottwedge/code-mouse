import sys
import time
import emoji
import logic
from colored import fg, bg, stylize
from commit import parse_commits
from subprocess import check_output

'''
git log --author="author" --format="commit %H %at %s" --numstat
'''

def animate(strength):
    animation_time = 0.3
    strength_bar_total_size = 50
    strength_bar_size = float(strength) / 100 * strength_bar_total_size
    sleep_time = animation_time / strength_bar_size

    for i in range(int(strength_bar_size)):
        time.sleep(sleep_time)
        strength = stylize(' ' * i, bg(state['color']))
        bar = '0% ' + strength + (' ' * (strength_bar_total_size - i)) + '100%'
        sys.stdout.write("\r" + bar)
        sys.stdout.flush()

author = 'Morg'
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
print('\n' + output_str + ' ' + mouse + ' ' + face)

if strength > 0 and strength <= logic.MAX_WEIGHT:
    animate(strength)

print('\n')

# test line
