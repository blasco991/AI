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
    N = problem.observation_space.n
    A = problem.action_space.n
    problem.T = np.full((N, A, N), 0.25, dtype=float)
    problem.R = np.full([N, A, N], 1)
    pi = np.random.choice(A, N)
    rewards, lengths = np.zeros(episodes), np.zeros(episodes)
    episode = []

    for e in range(episodes):
        i = 0
        reward = 0
        done = False
        s = problem.reset()

        # sT = np.full((N, A, N), 0, dtype=int)
        # sR = np.full((N, A, N), 0, dtype=int)

        episode.append([])
        while not done and i < ep_limit:
            sp, r, done, _ = problem.step(pi[s])
            episode[e].append((s, pi[s], sp, r))
            # sT[s, pi[s], sp] += 1
            # sR[s, pi[s], sp] += r

            reward += r
            i += 1
            s = sp

        # problem.T += np.divide(sT, sT.sum(axis=2, keepdims=True))  # how i divide by sa??? maybe broadcasting
        lengths[e], rewards[e] = i, reward

        for s in range(N):
            for a in range(A):
                sa = len([ei for ei in episode[e] if ei[0] == s and ei[1] == a])
                for sp in range(N):
                    match = [ei[3] for ei in episode[e] if ei[0] == s and ei[1] == a and ei[2] == sp]
                    sasp = len(match)
                    r = sum(match)
                    if sa != 0:
                        problem.T[s, a, sp] = sasp / sa
                    if sasp != 0:
                        problem.R[s, a, sp] = r / sasp

        pi = value_iteration(problem, vmaxiters, gamma, delta)

    return pi, rewards, lengths
