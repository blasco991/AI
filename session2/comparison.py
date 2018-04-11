import numpy as np
import gym
import gym_ai_lab
import mdps.passive as mdp
import mdps.utils as utils


# Learning parameters
delta = 1e-3
gamma = 0.7
maxiters = 50  # Max number of iterations to perform

envname = "BiggerLavaFloor-v0"

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
rewards = np.zeros(len(liters))  # Rewards array
c = 0

# Value iteration
for i in liters:
    reprew = np.zeros(rep)
    # Repeat multiple times and compute mean reward
    for j in range(rep):
        policy = mdp.value_iteration(env, i, gamma, delta)  # Compute policy
        reprew[j] = utils.run_episode(env, policy, elimit)  # Execute policy
    rewards[c] = reprew.mean()
    c += 1
    print("\rValue Iteration: {0}%".format(int(c / len(liters) * 100)), end="")
series.append({"x": liters, "y": rewards, "ls": "-", "label": "Value Iteration"})

print()

vmaxiters = 5  # Max number of iterations to perform while evaluating a policy
rewards = np.zeros(len(liters))  # Rewards array
c = 0

# Policy iteration
for i in liters:
    reprew = np.zeros(rep)
    # Repeat multiple times and compute mean reward
    for j in range(rep):
        policy = mdp.policy_iteration(env, i, vmaxiters, gamma, delta)  # Compute policy
        reprew[j] = utils.run_episode(env, policy, elimit)  # Execute policy
    rewards[c] = reprew.mean()
    c += 1
    print("\rPolicy Iteration: {0}%".format(int(c / len(liters) * 100)), end="")
series.append({"x": liters, "y": rewards, "ls": "-", "label": "Policy Iteration"})

utils.plot(series, "Learning Rate", "Iterations", "Reward")
