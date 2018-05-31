"""
Model free algorithm for solving MDPs
"""
import numpy as np
import mdps


def value_iteration(problem, maxiters, gamma, delta):
    return mdps.planning.value_iteration(problem, maxiters, gamma, delta)


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
    N, A = problem.observation_space.n, problem.action_space.n
    pi, problem.T, problem.R = np.random.choice(A, N), np.zeros((N, A, N)), np.zeros([N, A, N])
    rewards, lengths = np.zeros(episodes), np.zeros(episodes)
    sT = np.zeros((N, A, N), dtype=int)
    sR = np.zeros((N, A, N), dtype=int)

    for e in range(episodes):
        s, done, i = problem.reset(), False, 0

        while not done and i < ep_limit:
            sp, r, done, _ = problem.step(pi[s])
            sT[s, pi[s], sp] += 1
            sR[s, pi[s], sp] += r
            rewards[e] += r
            i += 1
            s = sp

        lengths[e] += i
        st_sum = sT.sum(axis=2, keepdims=True)
        np.divide(sT, st_sum, out=problem.T, where=st_sum != 0)
        np.divide(sR, st_sum, out=problem.R, where=st_sum != 0)
        pi = value_iteration(problem, vmaxiters, gamma, delta)

    return pi, rewards, lengths
