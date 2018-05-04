"""
Passive MDP solving algorithms
"""

import numpy as np


def actions_from_state(actions, s):
    return [actions[s]] if not isinstance(actions, dict) else list(actions.keys())


def value_iteration(problem, vmaxiters, gamma, delta):
    """
    Performs the value iteration algorithm for a specific environment.
    :param problem: problem
    :param vmaxiters: max iterations allowed
    :param gamma: gamma value
    :param delta: delta value
    :return: policy
    """
    return _value_iteration(problem, vmaxiters, gamma, delta, problem.actions)[0]


def _value_iteration(problem, vmaxiters, gamma, delta, actions):
    viter = 0
    v = np.zeros(problem.observation_space.n)
    vp = np.ones(problem.observation_space.n)
    pi = np.zeros(problem.observation_space.n, dtype="int8")

    while max(np.abs(v - vp)) >= delta and viter < vmaxiters:
        vp = np.copy(v)
        viter += 1

        for s in range(problem.observation_space.n):
            v[s] = max([np.sum([problem.T[s, a, sp] * (problem.R[s, a, sp] + gamma * v[sp])
                                for sp in range(problem.observation_space.n)])
                        for a in actions_from_state(actions, s)])

    for s in range(problem.observation_space.n):
        pi[s] = np.argmax([np.sum([problem.T[s, a, sp] * (problem.R[s, a, sp] + gamma * v[sp])
                                   for sp in range(problem.observation_space.n)])
                           for a in problem.actions.keys()])

    return np.asarray(pi), v


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
    piter = 0
    pi = np.zeros(problem.observation_space.n, dtype="int8")
    pip = np.ones(problem.observation_space.n, dtype="int8")

    while not np.array_equal(pi, pip) and piter < pmaxiters:
        pip = pi
        piter += 1

        pi, v = _value_iteration(problem, vmaxiters, gamma, delta, pi)

        for s in range(problem.observation_space.n):
            pi[s] = np.argmax([np.sum([problem.T[s, a, sp] * (problem.R[s, a, sp] + gamma * v[sp])
                                       for sp in range(problem.observation_space.n)])
                               for a in problem.actions.keys()])

    return np.asarray(pi)
