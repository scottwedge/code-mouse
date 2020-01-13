import os
from datetime import datetime
from colored import fg, stylize

YELLOW = '220'

class Meal:
    def __init__(self, project, commit, timestamp, message, changes, weight=None):
        self.weight = weight
        self.project = project
        self.commit = commit
        self.timestamp = timestamp
        self.message = ' '.join(message.split())
        self.changes = changes
    
    def update_weight(self, weight):
        self.weight = weight
    
    def pretty_print(self, mouse):
        project_name = os.path.basename(self.project)
        commit = 'commit {0} to {1} @ {2}'.format(self.commit[:6], project_name, self.timestamp)
        commit = stylize(commit, fg(YELLOW))
        changes = 'Changes: {0}'.format(self.changes)
        weight = 'Weight: {0}'.format(self.weight)
        strength = mouse.get_strength()
        color = mouse.get_color()
        strength = 'Strength: ' + stylize('{0}%'.format(strength), fg(color))
        message = '\t{0}'.format(self.message)
        print('{0}\n{1}\n{2}\n{3}\n{4}\n'.format(
            commit,
            changes,
            weight,
            strength,
            message
        ))

    def __repr__(self):
        return '{0}\t{1}\t{2}\t{3}\t{4}\t{5}'.format(
            self.project,
            self.commit,
            self.timestamp.timestamp(),
            self.message,
            self.changes,
            self.weight
        )
    
    def graph(self):
        pass
