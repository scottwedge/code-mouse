from datetime import datetime

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
    
    # TODO make pretty
    def __str__(self):
        return '{0}\t{1}\t{2}\t{3}\t{4}\t{5}'.format(
            self.project,
            self.commit,
            self.timestamp,
            self.message,
            self.changes,
            self.weight
        )

    def __repr__(self):
        return '{0}\t{1}\t{2}\t{3}\t{4}\t{5}'.format(
            self.project,
            self.commit,
            self.timestamp.timestamp(),
            self.message,
            self.changes,
            self.weight
        )
