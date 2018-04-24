import numpy as np
import gym
import gym_ai_lab
import mdps.passive as mdp
from timeit import default_timer as timer


# Learning parameters
delta = 1e-3
gamma = 1.0
pmaxiters = 50  # Max number of policy improvements to perform
vmaxiters = 5  # Max number of iterations to perform while evaluating a policy

envname = "LavaFloor-v0"

print("\n----------------------------------------------------------------")
print("\tEnvironment: ", envname)
print("----------------------------------------------------------------\n")

env = gym.make(envname)
env.render()

t = timer()
policy = mdp.policy_iteration(env, pmaxiters, vmaxiters, gamma, delta)

print("\n\nPolicy Iteration:\n----------------------------------------------------------------"
      "\nExecution time: {0}s\nPolicy:\n{1}".format(round(timer() - t, 4), np.vectorize(env.actions.get)(policy.reshape(
                                                                                        env.rows, env.cols))))
