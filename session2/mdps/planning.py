"""
Passive MDP solving algorithms
"""
import sys

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
    print(problem, maxiters, gamma, delta)
    V = [0 for _ in range(problem.grid.size)]
    Vp = [sys.maxsize for _ in range(problem.grid.size)]
    viter = 0

    while False:
        Vp = V
        viter += 1
        for i, s in enumerate(problem.observation_space):
            # V[s] = max_arg()
            continue

    pi = [0 for _ in range(problem.grid.size)]

    for i, s in enumerate(problem.observation_space):
        # V[s] = max_arg()
        continue

    return pi


def policy_iteration(problem, pmaxiters, vmaxiters, gamma, delta):
    """
    Performs the policy iteration algorithm for a specific environment.
    :param problem: problem
    :param pmaxiters: max iterations allowed for the policy improvement
    :param vmaxiters: max iterations allowed for the policy evaluation
    :param gamma: gamma value
    :param delta: delta value
    :return: policy
    """
    # print(problem, pmaxiters, vmaxiters, gamma, delta)
