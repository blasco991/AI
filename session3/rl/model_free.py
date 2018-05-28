"""
Model free algorithms for solving MDPs
"""
import numpy as np
import gym.spaces


def epsilon_greedy(q, state, epsilon):
    """
    Epsilon-greedy action selection function
    :param q: q table
    :param state: agent's current state
    :param epsilon: epsilon parameter
    :return: action
    """
    return np.random.randint(0, len(q[state])) if np.random.random() < epsilon else q[state].argmax()


def softmax(q, state, t):
    """
    Softmax action selection function
    :param q: q table
    :param state: agent's current state
    :param t: t parameter (temperature)
    :return: action
    """
    p = np.divide(np.exp(np.divide(q[state], t)), np.sum(np.exp(np.divide(q[state], t)), axis=0))
    return np.random.choice(len(q[state]), p=p)


def q_learning(problem, episodes, alpha, gamma, expl_func, expl_param):
    """
    Performs the Q-Learning algorithm for a specific environment
    :param problem: problem
    :param episodes: number of episodes for training
    :param alpha: alpha parameter
    :param gamma: gamma parameter
    :param expl_func: exploration function (epsilon_greedy, softmax)
    :param expl_param: exploration parameter (epsilon, T)
    :return: (policy, rews, ep_lengths): final policy, rewards for each episode [array], length of each episode [array]
    """
    N = problem.observation_space.n
    A = problem.action_space.n
    Q = np.random.rand(N, A)
    rewards, lengths = np.zeros(episodes), np.zeros(episodes)

    for e in range(episodes):
        s = problem.reset()
        done = False
        reward = 0
        i = 0

        while not done:
            a = expl_func(Q, s, expl_param)
            sp, r, done, _ = problem.step(a)
            Q[s, a] = Q[s, a] + alpha * (r + gamma * (Q[sp, a] - Q[s, a]).max())
            r += reward
            s = sp
            i += 1

        lengths[e], rewards[e] = i, reward

    pi = Q.argmax(axis=1)

    return pi, rewards, lengths


def sarsa(problem, episodes, alpha, gamma, expl_func, expl_param):
    """
    Performs the SARSA algorithm for a specific environment
    :param problem: problem
    :param episodes: number of episodes for training
    :param alpha: alpha parameter
    :param gamma: gamma parameter
    :param expl_func: exploration function (epsilon_greedy, softmax)
    :param expl_param: exploration parameter (epsilon, T)
    :return: (policy, rews, ep_lengths): final policy, rewards for each episode [array], length of each episode [array]
    """
    N = problem.observation_space.n
    A = problem.action_space.n
    Q = np.random.rand(N, A)
    rewards, lengths = np.zeros(episodes), np.zeros(episodes)

    for e in range(episodes):
        i = 0
        reward = 0
        done = False

        s = problem.reset()
        a = expl_func(Q, s, expl_param)
        while not done:
            sp, r, done, _ = problem.step(a)
            ap = expl_func(Q, sp, expl_param)
            Q[s, a] = Q[s, a] + alpha * (r + gamma * (Q[sp, ap] - Q[s, a]))
            r += reward
            s = sp
            a = ap
            i += 1

        lengths[e], rewards[e] = i, reward

    pi = Q.argmax(axis=1)

    return pi, rewards, lengths
