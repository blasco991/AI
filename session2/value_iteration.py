import numpy as np
import gym
import gym_ai_lab
import mdps.planning as mdp
from timeit import default_timer as timer


# Learning parameters
delta = 1e-3
gamma = 1.0
maxiters = 50  # Max number of iterations to perform

envname = "LavaFloor-v0"

print("\n----------------------------------------------------------------")
print("\tEnvironment: ", envname)
print("----------------------------------------------------------------\n")

env = gym.make(envname)
env.render()

t = timer()
policy = mdp.value_iteration(env, maxiters, gamma, delta)

print("\n\nValue Iteration:\n----------------------------------------------------------------"
      "\nExecution time: {0}s\nPolicy:\n{1}".format(round(timer() - t, 4), np.vectorize(env.actions.get)(policy.reshape(
                                                                                        env.rows, env.cols))))
