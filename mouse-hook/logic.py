import math
from state import Dead, States, ExtraStates
from datetime import datetime

DURATION = 'days'           # everything will be computed in terms of this unit
MIN_WEIGHT = 0
MAX_WEIGHT = 100
START_WEIGHT = 30
RATE_OF_DECAY = 1           # how quickly mouse loses weight without food
RATE_OF_GROWTH = 1 / 20.    # for ex, gains 1 unit per 20 staged changes
SATIATION_INTERVAL = 1      # how long before RATE_OF_DECAY kicks in
MAX_WEIGHT_AFTER_FULL = 500


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

'''
arg commit_history: a list of Commit objects [Commit] sorted by ascending date
'''
def compute_historical_weight(commit_history):
    weight = START_WEIGHT
    last_meal = None
    for i, commit in enumerate(commit_history):
        weight += commit.changes * RATE_OF_GROWTH
        if last_meal and i < len(commit_history) - 1:
            weight -= compute_weight_loss(last_meal, commit_history[i + 1].timestamp) 
        else:
            last_meal = commit.timestamp
    return weight

'''
arg commit_history: a list of Commit objects [Commit] sorted by ascending date
'''
def compute_current_weight(commit_history):
    num_commits = len(commit_history)
    if num_commits > 0:
        historical_weight = compute_historical_weight(commit_history)
        last_meal = commit_history[num_commits - 1].timestamp
        return historical_weight - compute_weight_loss(last_meal, datetime.now())
    return START_WEIGHT

'''
arg weight: numerical weight
'''
def get_strength_from_weight(weight):
    return int(weight / MAX_WEIGHT * 100)

'''
arg weight: numerical weight
returns discrete states based on numerical bins
'''
def get_state_from_weight(weight):
    if weight == 0 or weight > MAX_WEIGHT_AFTER_FULL:
        return Dead
    if weight <= MAX_WEIGHT:
        f = weight / MAX_WEIGHT
        states = States
    else:
        f = weight / MAX_WEIGHT_AFTER_FULL
        states = ExtraStates
    bucket = int(math.floor(f / (1. / len(states)))) - 1
    return states[bucket]
    
'''
arg weight: numerical weight
'''
def get_strength_str_from_weight(weight):
    return "I'm at {0}% strength now.".format(get_strength_from_weight(weight))
