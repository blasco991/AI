import numpy as np
import gym
import gym_ai_lab
import mdps.planning as mdp
from timeit import default_timer as timer

# Learning parameters
delta = 1e-3
gamma = 0.9
maxiters = 50  # Max number of iterations to perform

envname = "LavaFloor-v0"

print("\n----------------------------------------------------------------")
print("\tEnvironment: ", envname)
print("----------------------------------------------------------------\n")

env = gym.make(envname)
env.render()
print("\n{}".format(env.actions))

t = timer()
policy, i = mdp.value_iteration(env, maxiters, gamma, delta)
policy = policy.reshape(env.rows, env.cols)

print("\n\nValue Iteration:\n--------------------------------------------"
      "\nExecution time: {}s\n"
      "\nPolicy:\n\n{}\n"
      "\niterations: {}\n\n"
      .format(round(timer() - t, 4), np.vectorize(env.actions.get)(policy), i))
