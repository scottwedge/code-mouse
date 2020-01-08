'''
MOUSE LOGIC
* Rate of decay d(t) - how quickly mouse loses weight without food
* Rate of growth g - how quickly mouse gains weight with food
* Satiation interval s - how long before d(t) kicks in
* +/- change = 1 unit of food
* For now, mouse is represented by circle with radius r
* r += g * units of food
* after duration s without food (time since last commit): r -= r * d(t)
'''

'''
param commit_history: a list of Commit objects [Commit]
'''
def compute_weight(commit_history):
    pass
