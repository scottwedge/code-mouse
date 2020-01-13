from datetime import datetime

class Meal:
    def __init__(self, project, commit, timestamp, message, changes):
        self.weight = None
        self.project = project
        self.commit = commit
        self.timestamp = timestamp
        self.message = ' '.join(message.split())
        self.changes = changes
    
    def update_weight(self, weight):
        self.weight = weight
    
    def __str__(self):
        return '{0}\t{1}\t{2}\t{3}\t{4}\t{5}'.format(
            self.project,
            self.commit,
            self.timestamp,
            self.changes,
            self.weight,
            self.message
        )
