"""
Utility functions for MDPs
"""

import matplotlib.pyplot as plt


def run_episode(problem, policy, limit):
    """
    Executes an episode within 'env' following 'policy'
    :param problem: problem
    :param policy: policy to follow
    :param limit: maximum number of steps
    :return: reward
    """
    obs = problem.reset()
    done = False
    reward = 0
    s = 0
    while not done and s < limit:
        obs, r, done, _ = problem.step(policy[obs])
        reward += r
        s += 1
    return reward


def map_action(action):
    return {0: '<', 1: '>', 2: '^', 3: 'v'}[action]


def plot(series, title, xlabel, ylabel):
    """
    Plots data
    :param series: data series
    :param title: plot title
    :param xlabel: x labels
    :param ylabel: y labels
    :param ylabel: y labels
    """
    plt.figure(figsize=(15, 10))
    for s in series:
        plt.plot(s["x"], s["y"], label=s["label"])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend(loc="lower right")
    plt.show()
