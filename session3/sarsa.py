import numpy as np
import gym
import gym_ai_lab
import rl.model_free as mf
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
alpha = 0.3
gamma = 0.95
epsilon = 0.1

t = timer()

# SARSA epsilon greedy
policy, rews, lengths = mf.sarsa(env, episodes, alpha, gamma, mf.epsilon_greedy, epsilon)
print("Execution time: {0}s\nPolicy:\n{1}\n".format(round(timer() - t, 4), np.vectorize(actions.get)(policy.reshape(
    env.shape))))
utils.run_episode(env, policy, 20)
