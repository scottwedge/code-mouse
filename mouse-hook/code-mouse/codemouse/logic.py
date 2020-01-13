import math
import data
import printer
from datetime import datetime
from state import Dead, States, ExtraStates

DURATION = 'days'           # everything will be computed in terms of this unit
MIN_WEIGHT = 0
MAX_WEIGHT = 100
START_WEIGHT = 30
RATE_OF_DECAY = 1           # how quickly mouse loses weight without food
RATE_OF_GROWTH = 1 / 20.    # for ex, gains 1 unit per 20 staged changes
SATIATION_INTERVAL = 1      # how long before RATE_OF_DECAY kicks in
MAX_WEIGHT_AFTER_FULL = 250

'''
arg t1: datetime obj
arg t2: datetime obj
'''
def get_timestamp_diff(t1, t2):
    delta = t2 - t1
    if DURATION == 'days':
        return delta.days
    if DURATION == 'hours':
        return delta.seconds / 3600
    if DURATION == 'minutes':
        return delta.seconds / 60

'''
arg t1: datetime obj
arg t2: datetime obj
'''
def compute_weight_loss(t1, t2):
    duration_since_last = get_timestamp_diff(t1, t2)
    loss = (duration_since_last - SATIATION_INTERVAL) * RATE_OF_DECAY
    return loss if loss > 0 else 0

def compute_weight_gain(commit):
    return commit.changes * RATE_OF_GROWTH

'''
arg commit_history: a list of Commit objects [Commit] sorted by ascending date
'''
def compute_historical_weight(commit_history):
    weight = START_WEIGHT
    last_meal = None
    for i, commit in enumerate(commit_history):
        weight += compute_weight_gain(commit)
        if last_meal and i < len(commit_history) - 1:
            weight -= compute_weight_loss(last_meal, commit_history[i + 1].timestamp) 
        else:
            last_meal = commit.timestamp
    return weight

'''
arg commit_history: a list of Commit objects [Commit] sorted by ascending date
'''
def compute_current_weight_from_history(commit_history):
    historical_weight = compute_historical_weight(commit_history)
    last_meal = commit_history[len(commit_history) - 1].timestamp
    return historical_weight - compute_weight_loss(last_meal, datetime.now())

'''
arg commit_history: a list of Commit objects [Commit] sorted by ascending date
'''
def compute_current_weight_from_state(commit_history, weight):
    last_commit = commit_history[len(commit_history) - 1]
    gain = compute_weight_gain(last_commit)
    loss = compute_weight_loss(last_commit.timestamp, datetime.now())
    return weight + gain - loss

'''
arg commit_history: a list of Commit objects [Commit] sorted by ascending date
'''
def compute_current_weight(commit_history, weight=None):
    if len(commit_history) == 0:
        return START_WEIGHT
    if weight is None:
        return compute_current_weight_from_history(commit_history)
    return compute_current_weight_from_state(commit_history, weight)
