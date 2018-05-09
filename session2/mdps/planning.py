"""
Passive MDP solving algorithms
"""

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


def _q(s, a, p, r, gamma, v, n):
    return np.sum((p[s, a, sp] * (r[s, a, sp] + gamma * v[sp]) for sp in range(n)))


def _value_iteration(problem, vmaxiters, gamma, delta, policy=None, v=None):
    viter, n = 0, problem.observation_space.n
    q, vp, v = np.zeros(n), np.ones(n), np.zeros(n) if v is None else v

    while (np.abs(v - vp)).max() >= delta and viter < vmaxiters:
        vp = v.copy()
        viter += 1

        q = (problem.T * (problem.R + gamma * v)).sum(axis=2)

        if policy is not None:
            for s in range(n):
                for a in range(problem.action_space.n):
                    q[s][a] = q[s][a] if a == policy[s] else 1

        v = q.max(axis=1)

    return (problem.T * (problem.R + gamma * v)).sum(axis=2).argmax(axis=1) \
        if policy is None else (v, q)


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
    v = np.zeros(n)

    # v, q = _value_iteration(problem, vmaxiters, gamma, delta, pi, np.zeros(n))

    while not np.array_equal(pi, pip) and piter < pmaxiters:
        pip = np.copy(pi)
        piter += 1

        v, q = _value_iteration(problem, vmaxiters, gamma, delta, pi, v)
        pi = np.argmax(q, axis=1)

    return pi
