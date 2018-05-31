import numpy as np
import gym
import gym_ai_lab
import rl.model_based as mb
import rl.model_free as mf
import rl.utils as utils
from timeit import default_timer as timer


envname = "CliffWalking-v0"

print("\n----------------------------------------------------------------")
print("\tEnvironment: ", envname)
print("----------------------------------------------------------------\n")

env = gym.make(envname)
env.render()

# Learning parameters
episodes = 500
ep_limit = 50
vmaxiters = 50
alpha = 0.3
gamma = 0.95
epsilon = 0.1
delta = 1e-3

rewser = []
lenser = []

litres = np.arange(1, episodes + 1)  # Learning iteration values
window = 10  # Rolling window
mrew = np.zeros(episodes)
mlen = np.zeros(episodes)

t = timer()

# Model-based
_, rews, lengths = mb.model_based(env, episodes, ep_limit, vmaxiters, gamma, delta)
rews = utils.rolling(rews, window)
rewser.append({"x": np.arange(1, len(rews) + 1), "y": rews, "ls": "-", "label": "Model-Based"})
lengths = utils.rolling(lengths, window)
lenser.append({"x": np.arange(1, len(lengths) + 1), "y": lengths, "ls": "-", "label": "Model-Based"})

# Q-Learning
_, rews, lengths = mf.q_learning(env, episodes, alpha, gamma, mf.softmax, epsilon)
rews = utils.rolling(rews, window)
rewser.append({"x": np.arange(1, len(rews) + 1), "y": rews, "ls": "-", "label": "Q-Learning"})
lengths = utils.rolling(lengths, window)
lenser.append({"x": np.arange(1, len(lengths) + 1), "y": lengths, "ls": "-", "label": "Q-Learning"})

# SARSA
_, rews, lengths = mf.sarsa(env, episodes, alpha, gamma, mf.softmax, epsilon)
rews = utils.rolling(rews, window)
rewser.append({"x": np.arange(1, len(rews) + 1), "y": rews, "ls": "-", "label": "SARSA"})
lengths = utils.rolling(lengths, window)
lenser.append({"x": np.arange(1, len(lengths) + 1), "y": lengths, "ls": "-", "label": "SARSA"})

print("Execution time: {0}s".format(round(timer() - t, 4)))

utils.plot(rewser, "Rewards", "Episodes", "Rewards")
utils.plot(lenser, "Lengths", "Episodes", "Lengths", "upper right")
