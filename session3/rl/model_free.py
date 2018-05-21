"""
Model free algorithms for solving MDPs
"""


import numpy as np


def epsilon_greedy(q, state, epsilon):
    """
    Epsilon-greedy action selection function
    :param q: q table
    :param state: agent's current state
    :param epsilon: epsilon parameter
    :return: action
    """
    pass


def softmax(q, state, t):
    """
    Softmax action selection function
    :param q: q table
    :param state: agent's current state
    :param t: t parameter (temperature)
    :return: action
    """
    pass


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
    pass


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
    pass
