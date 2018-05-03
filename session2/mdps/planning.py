"""
Passive MDP solving algorithms
"""
import sys

import numpy as np


def value_iteration(problem, vmaxiters, gamma, delta):
    """
    Performs the value iteration algorithm for a specific environment.
    :param problem: problem
    :param vmaxiters: max iterations allowed
    :param gamma: gamma value
    :param delta: delta value
    :return: policy
    """
    viter = 0
    v = [0 for _ in range(problem.observation_space.n)]
    vp = [1 for _ in range(problem.observation_space.n)]
    pi = [0 for _ in range(problem.observation_space.n)]

    while max(np.abs(np.subtract(v, vp))) > delta and viter < vmaxiters:
        vp = v
        viter += 1
        for s in range(problem.observation_space.n):
            v[s] = max([np.sum([problem.T[s, a, sp] * (problem.R[s, a, sp] + gamma * vp[sp])
                                for sp in range(problem.observation_space.n)])
                        for a in problem.actions.keys()])

    for s in range(problem.observation_space.n):
        values = {(a, s): np.sum([problem.T[s, a, sp] * (problem.R[s, a, sp] + gamma * vp[sp])
                                  for sp in range(problem.observation_space.n)])
                  for a in problem.actions.keys()}
        pi[s] = max(values, key=values.get)[0]

    return np.array(pi).astype(int), viter


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
    v = [0 for _ in range(problem.observation_space.n)]
    vp = [1 for _ in range(problem.observation_space.n)]
    pi = [0 for _ in range(problem.observation_space.n)]
    pip = [1 for _ in range(problem.observation_space.n)]

    piter = 0

    while not np.array_equal(pi, pip) and piter < pmaxiters:
        pip = pi
        viter = 0
        piter += 1
        while max(np.abs(np.subtract(v, vp))) > delta and viter < vmaxiters:
            vp = v
            viter += 1
            for s in range(problem.observation_space.n):
                v[s] = np.sum([problem.T[s, pi[s], sp] * (problem.R[s, pi[s], sp] + gamma * vp[sp])
                               for sp in range(problem.observation_space.n)])

        for s in range(problem.observation_space.n):
            values = {(a, s): np.sum([problem.T[s, a, sp] * (problem.R[s, a, sp] + gamma * vp[sp])
                                      for sp in range(problem.observation_space.n)])
                      for a in problem.actions.keys()}
            pi[s] = max(values, key=values.get)[0]

    return np.array(pi).astype(int), piter
