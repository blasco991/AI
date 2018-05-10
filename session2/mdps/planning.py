"""
Passive MDP solving algorithms
"""

import numpy as np
import gym.spaces


def value_iteration(problem, vmaxiters, gamma, delta):
    """
    Performs the value iteration algorithm for a specific environment.
    :param problem: problem
    :param vmaxiters: max iterations allowed
    :param gamma: gamma value
    :param delta: delta value
    :return: policy
    """
    return _value_iteration(problem, vmaxiters, gamma, delta)


def _value_iteration(problem, vmaxiters, gamma, delta, policy=None, v=None):
    viter, n = 0, problem.observation_space.n
    q, vp, v = np.zeros(n), np.ones(n), np.zeros(n) if v is None else v

    while (np.abs(v - vp)).max() >= delta and viter < vmaxiters:
        vp = v.copy()
        viter += 1

        if policy is not None:
            """for s in range(n):
                v[s] = (problem.T[s, policy[s]:policy[s] + 1, :] * (problem.R[s, policy[s]:policy[s] + 1, :] + gamma * v))
                .sum()"""
            """for s in range(n):
                v[s] = ((problem.T * (problem.R + gamma * v))[s:s + 1, policy[s]:policy[s] + 1, :]).sum()"""
            """for s in range(n):
                v[s] = ((problem.T * (problem.R + gamma * v)).take(indices=policy[s], axis=0)).sum()"""
            v = np.compress([1, 1, 1, 1], problem.T * (problem.R + gamma * v), axis=1).sum(axis=2).max(1)

        else:
            v = (problem.T * (problem.R + gamma * v)).sum(axis=2).max(axis=1)

    return (problem.T * (problem.R + gamma * v)).sum(axis=2).argmax(axis=1) if policy is None else v


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
    piter, n = 0, problem.observation_space.n
    pi, pip = np.zeros(n, dtype="int8"), np.ones(n, dtype="int8")

    v = _value_iteration(problem, vmaxiters, gamma, delta, pi, np.zeros(n))

    while not np.array_equal(pi, pip) and piter < pmaxiters:
        pip = np.copy(pi)
        piter += 1

        v = _value_iteration(problem, vmaxiters, gamma, delta, pi, v)
        pi = (problem.T * (problem.R + gamma * v)).sum(axis=2).argmax(axis=1)

    return pi
