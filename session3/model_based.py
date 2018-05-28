import numpy as np
import gym
import gym_ai_lab
import rl.model_based as mb
import rl.utils as utils
from timeit import default_timer as timer

envname = "CliffWalking-v0"

print("\n----------------------------------------------------------------")
print("\tEnvironment: ", envname)
print("----------------------------------------------------------------\n")

env = gym.make(envname)
env.render()
print()

actions = {0: "U", 1: "R", 2: "D", 3: "L"}

# Learning parameters
episodes = 500
ep_limit = 50
vmaxiters = 50
gamma = 0.95
delta = 1e-3

t = timer()

# Model-Based
policy, rews, lengths = mb.model_based(env, episodes, ep_limit, vmaxiters, gamma, delta)
print("\nExecution time: {0}s\nPolicy:\n{1}\n"
      .format(round(timer() - t, 4), np.vectorize(actions.get)(policy.reshape(env.shape))))
utils.run_episode(env, policy, 20)
