import numpy as np
import gym
import gym_ai_lab
import mdps.planning as mdp
from timeit import default_timer as timer

# Learning parameters
from mdps import utils

delta = 1e-3
gamma = 0.9
pmaxiters = 50  # Max number of policy improvements to perform
vmaxiters = 5  # Max number of iterations to perform while evaluating a policy

for envname in ["LavaFloor-v0", "NiceLavaFloor-v0", "VeryBadLavaFloor-v0", "BiggerLavaFloor-v0", "HugeLavaFloor-v0"]:
    print("\n----------------------------------------------------------------")
    print("\tEnvironment: ", envname)
    print("----------------------------------------------------------------\n")

    env = gym.make(envname)
    env.render()
    print("\n{}".format(env.actions))

    t = timer()
    policy = mdp.policy_iteration(env, pmaxiters, vmaxiters, gamma, delta)
    policy = policy.reshape(env.rows, env.cols)

    print("\n\nPolicy Iteration:\n--------------------------------------------"
          "\nExecution time: {}s\n"
          "\nPolicy:\n\n{}\n\n{}\n"
          .format(round(timer() - t, 4), np.vectorize(env.actions.get)(policy), np.vectorize(utils.map_action)(policy)))
