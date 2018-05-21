"""
Utility functions for MDPs
"""

import matplotlib.pyplot as plt
import numpy as np
import time


def run_episode(problem, policy, limit, rendering=False, sleep_time=1):
    """
    Executes an episode within 'env' following 'policy'
    :param problem: problem
    :param policy: policy to follow
    :param limit: maximum number of steps
    :param rendering: rendering flag. True if yes, False otherwise
    :param sleep_time: number of seconds to sleep after rendering
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
        if rendering:
            problem.render()
            time.sleep(sleep_time)
    return reward


def plot(series, title, xlabel, ylabel, leg_location="lower right"):
    """
    Plots data
    :param series: data series
    :param title: plot title
    :param xlabel: x labels
    :param ylabel: y labels
    :param ylabel: y labels
    :param leg_location: label location
    """
    plt.figure(figsize=(15, 10))
    for s in series:
        plt.plot(s["x"], s["y"], label=s["label"])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend(loc=leg_location)
    plt.show()


def rolling(a, window):
    shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
    strides = a.strides + (a.strides[-1],)
    return np.mean(np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides), -1)
