import numpy as np
import gym
import gym_ai_lab
import mdps.passive as mdp


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

print("\n\nPolicy Iteration:\n----------------------------------------------------------------"
      "\n{0}".format(np.vectorize(env.actions.get)(mdp.policy_iteration(env, pmaxiters, vmaxiters, gamma,
                                                                        delta).reshape(env.rows, env.cols))))
