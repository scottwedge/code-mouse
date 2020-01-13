import math
import data
import printer
from datetime import datetime
from state import Dead, States, ExtraStates

class Mouse:
    Config = data.load_config()

    def __init__(self):
        self.weight = None
        self.strength = None
        self.state = None
        self.last_meal = None
        self.history = None
        self.projects = None
    
    def load(self):
        self.projects = data.load_projects()
        self.history = data.load_history()
        self.weight = self.get_last_weight_in_history()
    
    '''
    Updates weight based on time of last meal
    '''
    def update(self):
        if len(self.history) > 0:
            last_meal = self.history[len(self.history) - 1].timestamp
            loss = self.compute_weight_loss(last_meal, datetime.now())
            self.weight -= loss
        else:
            self.weight = float(self.Config.start_weight)
        
    '''
    Updates weight and history with latest commit. Called on post-commit hook
    '''
    def update_with_latest_commit(self, project_path):
        commit = data.get_latest_commit(project_path)
        weight = self.compute_current_weight(commit)
        commit.update_weight(weight)
        self.history.append(commit)
        data.update_history(commit)

    def add_project(self, project_path=None):
        val = data.add_project(project_path)
        print(val)

    def get_strength(self):
        return int(self.weight / Mouse.Config.MAX_WEIGHT * 100)
    
    def get_strength_str(self):
        return "I'm at {0}% strength now.".format(self.get_strength())
    
    def get_last_weight_in_history(self):
        if len(self.history) > 0:
            last = self.history[len(self.history) - 1]
            return last.weight
    
    def print_projects(self):
        if self.projects and len(self.projects) > 0:
            for project in self.projects:
                print(project)
        else:
            print('Your mouse has no projects yet')

    def print_history(self):
        if self.history and len(self.history) > 0:
            for meal in self.history:
                print(meal)
        else:
            print('Your mouse has not fed yet')

    def print_health(self):
        printer.print_output(self)
    
    def print_config(self):
        self.Config.display()

    '''
    returns discrete states based on numerical bins
    '''
    def get_state(self):
        if self.weight == 0 or self.weight > Mouse.Config.MAX_WEIGHT_AFTER_FULL:
            return Dead
        if self.weight <= Mouse.Config.MAX_WEIGHT:
            f = self.weight / Mouse.Config.MAX_WEIGHT
            states = States
        else:
            f = self.weight / Mouse.Config.MAX_WEIGHT_AFTER_FULL
            states = ExtraStates
        bucket = int(math.ceil(f / (1. / len(states)))) - 1
        return states[bucket]

    def get_timestamp_diff(self, t1, t2):
        delta = t2 - t1
        if Mouse.Config.DURATION == 'days':
            return delta.days
        if Mouse.Config.DURATION == 'hours':
            return delta.seconds / 3600
        if Mouse.Config.DURATION == 'minutes':
            return delta.seconds / 60

    def compute_weight_loss(self, t1, t2):
        duration_since_last = self.get_timestamp_diff(t1, t2)
        loss = (duration_since_last - Mouse.Config.SATIATION_INTERVAL) * Mouse.Config.RATE_OF_DECAY
        return float(loss) if loss > 0 else 0.

    def compute_weight_gain(self, commit):
        return float(commit.changes) * Mouse.Config.RATE_OF_GROWTH

    def compute_current_weight(self, commit):
        t1 = commit.timestamp
        t2 = datetime.now()
        gain = self.compute_weight_gain(commit)
        loss = self.compute_weight_loss(t1, t2)
        self.weight = self.weight + gain - loss
        return float(self.weight)
