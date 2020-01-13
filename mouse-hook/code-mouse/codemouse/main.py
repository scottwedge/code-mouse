'''
Usage:
------
List options:
    $ codemouse
    $ codemouse --help
Activate codemouse for the current working git directory:
    $ codemouse init
View your mouse's vitals:
    $ codemouse health
View your mouse's feeding history:
    $ codemouse log
List active projects:
    $ codemouse list -o projects
Edit active projects:
    $ codemouse edit -o projects
List config variables:
    $ codemouse list -o config
Edit config:
    $ codemouse edit -o config
Update (called by hook):
    $ codemouse update --project /path/to/project
'''

import emoji
import argparse
from mouse import Mouse

mouse = emoji.emojize(':mouse_face:')
description = mouse + '\tA mouse that feeds on code\t' + mouse

parser = argparse.ArgumentParser(
    description=description,
    usage='''
        init        activate codemouse for the current working git directory
        health      display your mouse's current health
        log         display your mouse's feeding history
        list -o     list active projects or config options
        edit -o     edit activate projects or config options
    ''')

parser.add_argument('command', choices=['init', 'health', 'log', 'list', 'edit', 'update'])
parser.add_argument('-o', '--opt', choices=['projects', 'config'])
parser.add_argument('--project', help='Path to parent directory of git repository')

args = parser.parse_args()
command = args.command

mouse = Mouse()
mouse.load()
mouse.update()

# Initialize codemouse for current git repository
if command == 'init':
    mouse.add_project()
# Print mouse's current health
elif command == 'health':
    mouse.print_health()
# Display feeding history
elif command == 'log':
    mouse.print_history()
# List active projects or config options
elif command == 'list':
    if args.opt == 'projects':
        mouse.print_projects()
    elif args.opt == 'config':
        mouse.print_config()
    else:
        parser.print_help()
# Edit active projects or config options
elif command == 'edit':
    if args.opt == 'projects':
        print('TODO: edit projects')
    elif args.opt == 'config':
        print('TODO: edit config')
    else:
        parser.print_help()
# Otherwise this is an update command requiring project path
elif args.project:
    mouse.update_with_latest_commit(args.project)
    mouse.print_health()

