import sys
import time
import emoji
import shutil
from colored import fg, bg, stylize

MAX_BAR_SIZE = 65
ANIMATION_TIME = 0.3

mouse_emoji = emoji.emojize(':mouse_face:')

def get_bar_size():
    size = shutil.get_terminal_size((MAX_BAR_SIZE,))
    return min(int(size.columns) - 10, MAX_BAR_SIZE)

def animate(strength, state, color):
    strength_bar_total_size = get_bar_size()
    strength_bar_size = float(strength) / 100 * strength_bar_total_size
    sleep_time = ANIMATION_TIME / strength_bar_size
    for i in range(int(strength_bar_size)):
        time.sleep(sleep_time)
        strength = stylize(' ' * i, bg(color))
        bar = '0% ' + strength + (' ' * (strength_bar_total_size - i)) + '100%'
        sys.stdout.write("\r" + bar)
        sys.stdout.flush()
    
def print_output(mouse):
    state = mouse.get_state()
    strength = mouse.get_strength()
    strength_str = mouse.get_strength_str()
    color = mouse.get_color()
    caption = mouse.get_caption()
    face = emoji.emojize(':{0}:'.format(state['emoji']))
    output_str = stylize('{0} {1}'.format(strength_str, caption), fg(color))
    if strength > mouse.config.max_weight:
        output_str = emoji.emojize(':exclamation_mark:') + ' ' + output_str
    print('\n' + output_str + ' ' + mouse_emoji + ' ' + face)
    if strength > 0 and strength <= mouse.config.max_weight:
        animate(strength, state, color)
    print('\n')
