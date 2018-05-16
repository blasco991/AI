import numpy as np
import gym
import gym_ai_lab
import mdps.planning as mdp
import mdps.utils as utils
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
print("\n")

series = []  # Series of learning rates to plot
liters = np.arange(maxiters + 1)  # Learning iteration values
liters[0] = 1
elimit = 100  # Limit of steps per episode
rep = 10  # Number of repetitions per iteration value
virewards = np.zeros(len(liters))  # Rewards array
c = 0

t = timer()

# Value iteration
for i in liters:
    reprew = 0
    policy = mdp.value_iteration(env, i, gamma, delta)  # Compute policy
    # Repeat multiple times and compute mean reward
    for _ in range(rep):
        reprew += utils.run_episode(env, policy, elimit)  # Execute policy
    virewards[c] = reprew / rep
    c += 1
    print("\rValue Iteration: {0}%".format(int(c / len(liters) * 100)), end="")
series.append({"x": liters, "y": virewards, "ls": "-", "label": "Value Iteration"})

print()

vmaxiters = 5  # Max number of iterations to perform while evaluating a policy
pirewards = np.zeros(len(liters))  # Rewards array
c = 0

# Policy iteration
for i in liters:
    reprew = 0
    policy = mdp.policy_iteration(env, i, vmaxiters, gamma, delta)  # Compute policy
    # Repeat multiple times and compute mean reward
    for _ in range(rep):
        reprew += utils.run_episode(env, policy, elimit)  # Execute policy
    pirewards[c] = reprew / rep
    c += 1
    print("\rPolicy Iteration: {0}%".format(int(c / len(liters) * 100)), end="")
series.append({"x": liters, "y": pirewards, "ls": "-", "label": "Policy Iteration"})

print("\n\nExecution time: {0}s".format(round(timer() - t, 4)))
np.set_printoptions(linewidth=10000)
print("Leaning rate comparison:\nVI: {0}\nPI: {1}".format(virewards, pirewards))

utils.plot(series, "Learning Rate", "Iterations", "Reward")

# Try also on HugeLavaFloor-v0 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
