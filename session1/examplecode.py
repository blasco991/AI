"""
Some example code
"""

import gym
import gym_ai_lab
from datastructures.fringe import *

# Create and render the environment
env = gym.make("SmallMaze-v0")
env.render()

# Start and goal state identifiers and (x, y) coordinates
start = env.startstate
goal = env.goalstate
print("Start: {0} - {1}\nGoal: {2} - {3}".format(start, env.state_to_pos(start), goal, env.state_to_pos(goal)))

# Available actions
print("Available actions: ", env.actions)

# Children of the start state (actions are deterministic in this environment)
for action in range(env.action_space.n):  # Loop over the available actions
    print("From state {0} with action {1} -> state {2}".format(env.state_to_pos(start), action,
                                                               env.state_to_pos(env.sample(start, action))))

# How to use the fringe
fringe = PriorityFringe()
# FringeNode constructor takes 4 parameters:
# 1 - the state embedded in the node
# 2 - path cost (from the root node to the current one)
# 3 - the value of the node (used for ordering within PriorityFringe)
# 4 - parent node (None if we are building the root)
node = FringeNode(start, 0, 0, None)  # Node of the start state
fringe.add(node)

child = FringeNode(env.sample(start, 0), 1, 0, start)  # Child node
if child.state not in fringe:
    fringe.add(child)

child = FringeNode(env.sample(start, 0), 1, 0, start)  # Other child node
if child.state in fringe and child.value < fringe[child.state].value:  # Replace node of the same
    fringe.replace(child)

print("Empty Fringe: ", fringe.is_empty())
frnode = fringe.remove()  # Get node with highest priority
print("Fringe size: ", len(fringe))
