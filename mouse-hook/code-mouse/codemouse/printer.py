import os
import sys
import time
import emoji
from colored import fg, bg, stylize

MAX_BAR_SIZE = 55
ANIMATION_TIME = 0.3

mouse_emoji = emoji.emojize(':mouse_face:')

def get_bar_size():
    _, columns = os.popen('stty size', 'r').read().split()
    return min(int(columns) - 10, MAX_BAR_SIZE)

def animate(strength, state):
    strength_bar_total_size = get_bar_size()
    strength_bar_size = float(strength) / 100 * strength_bar_total_size
    sleep_time = ANIMATION_TIME / strength_bar_size
    for i in range(int(strength_bar_size)):
        time.sleep(sleep_time)
        strength = stylize(' ' * i, bg(state['color']))
        bar = '0% ' + strength + (' ' * (strength_bar_total_size - i)) + '100%'
        sys.stdout.write("\r" + bar)
        sys.stdout.flush()
    
def print_output(mouse):
    state = mouse.get_state()
    strength = mouse.get_strength()
    strength_str = mouse.get_strength_str()
    face = emoji.emojize(':{0}:'.format(state['emoji']))
    output_str = stylize('{0} {1}'.format(strength_str, state['caption']), fg(state['color']))
    if strength > mouse.Config.MAX_WEIGHT:
        output_str = emoji.emojize(':exclamation_mark:') + ' ' + output_str
    elif strength > 30:
        output_str = stylize('Thank you :D ', fg(state['color'])) + output_str
    print('\n' + output_str + ' ' + mouse_emoji + ' ' + face)
    if strength > 0 and strength <= mouse.Config.MAX_WEIGHT:
        animate(strength, state)
    print('\n')
