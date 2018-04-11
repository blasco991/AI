import numpy as np
import gym
import gym_ai_lab
import mdps.passive as mdp


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

print("\n\nValue Iteration:\n----------------------------------------------------------------"
      "\n{0}".format(np.vectorize(env.actions.get)(mdp.value_iteration(env, maxiters, gamma, delta).reshape(
                                                                       env.rows, env.cols))))
