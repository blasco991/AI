import gym
import gym_ai_lab
import numpy as np
import mdps.utils as utils


# Create and render the environment
env = gym.make("LavaFloor-v0")
env.render()

# Start and goal state identifiers and (x, y) coordinates
start = env.startstate
goal = env.goalstate
print("Start: {0} - {1}\nGoal: {2} - {3}".format(start, env.state_to_pos(start), goal, env.state_to_pos(goal)))

# Available actions
print("Available actions: ", env.actions)

# Transition probability T(0, 'R', 1): probability of transitioning from state (0, 0) to (0, 1) with action 'R'
print("T[0, 1, 1]: ", env.T[0, 1, 1])

# Reward R(0, 'R', 1): reward for transitioning from state (0, 0) to (0, 1) with action 'R'
print("R[0, 1, 1]: ", env.R[0, 1, 1])

# Verify that T is a probability, i.e., for each pair of state/action the sum is 1 (on the third axis of the 3d-array)
print("Sum of probability values:\n", env.T.sum(axis=2))  # Power of numpy

# Generate a random policy for the current environment
p = np.random.choice(env.action_space.n, env.observation_space.n)
print("Random policy: ", p)

# Execute the random policy 10 times and compute the mean reward. Use numpy
rews = np.zeros(10)
for i in range(10):
    rews[i] = utils.run_episode(env, p, 10)  # Limit the number of steps per episode to 10
print("Mean reward: ", rews.mean())

# Plot a log function. Use numpy
x = np.arange(1, 100)
y = np.log(x)
utils.plot([{"x": x, "y": y, "ls": "-", "label": "Log"}], "Log Function", "X", "Y")
