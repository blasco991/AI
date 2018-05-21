"""
Model free algorithm for solving MDPs
"""

import numpy as np


def value_iteration(problem, maxiters, gamma, delta):
    """
    Performs the value iteration algorithm for a specific environment.
    :param problem: problem
    :param maxiters: max iterations allowed
    :param gamma: gamma value
    :param delta: delta value
    :return: policy
    """
    pass


def model_based(problem, episodes, ep_limit, vmaxiters, gamma, delta):
    """
    Performs the model-based algorithm for a specific environment
    :param problem: problem
    :param episodes: number of episodes for training
    :param ep_limit: limit to episode length
    :param vmaxiters: max iterations allowed for VI
    :param gamma: gamma value
    :param delta: delta value
    :return: (policy, rews, ep_lengths): final policy, rewards for each episode [array], length of each episode [array]
    """
    pass
