"""
Passive MDP solving algorithms
"""

import gym.spaces
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
    return _value_iteration(problem, vmaxiters, gamma, delta)


def _q(s, a, p, gamma, v):
    return sum([p.T[s, a, sp] * (p.R[s, a, sp] + gamma * v[sp])
                for sp in range(p.observation_space.n)])


def _value_iteration(problem, vmaxiters, gamma, delta, policy=None, v=None):
    viter, n = 0, problem.observation_space.n
    q, vp, v = np.zeros((n, problem.action_space.n)), np.ones(n), np.zeros(n) if v is None else v

    while (np.abs(v - vp)).max() >= delta and viter < vmaxiters:  # Compute Bellman Equation
        vp = v.copy()
        viter += 1

        for s in range(n):
            if policy is not None:
                v[s] = _q(s, policy[s], problem, gamma, v)
            else:
                for a in range(problem.action_space.n):
                    q[s, a] = _q(s, a, problem, gamma, v)
                v[s] = max(q[s])

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

    while not np.array_equal(pi, pip) and piter < pmaxiters:  # Improve policy
        pip = np.copy(pi)
        piter += 1

        v = _value_iteration(problem, vmaxiters, gamma, delta, pi, v)  # Eval policy

        pi = (problem.T * (problem.R + gamma * v)).sum(axis=2).argmax(axis=1)

    return pi
