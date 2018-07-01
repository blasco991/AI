"""
Data structures representing the fringe for search methods
"""

import heapq
from dot_util import dot_init, gen_trans
from collections import deque

from abc import ABC, abstractmethod

dot = ''
gen = 0


class FringeNode:
    """
    Fringe state representation
    """

    def __init__(self, state, pathcost, value, parent, cause, problem, gl, shape='circle', limit=None):
        """
        Creates a representation of a node in the fringe
        :param state: the state embedded in the node
        :param pathcost: path cost from the root node to this one
        :param value: value of a node
        :param parent: parent node
        :param cause: parent node
        """
        self.state = state
        self.cause = cause
        self.value = value
        self.parent = parent
        self.removed = False
        self.pathcost = pathcost

        global dot
        global gen
        if parent is None:
            gen = 1
            if limit != -1:
                dot = dot_init(problem, shape, sub=True, cluster=limit) + gl(self, problem)
            else:
                dot = dot_init(problem, shape) + "\n" + gl(self, problem)
        else:
            dot += gen_trans(parent, self, problem, gl, dot, gen)
            gen += 1

    def __lt__(self, other):
        """
        Compare function between nodes - 'lower than'
        :param other: object to compare to
        :return: True if lower, False otherwise
        """
        return self.value < other.value

    def __hash__(self):
        """
        Hash value of a node: the unique integer identifier of its state
        :return: unique integer identifier of the embedded state
        """
        return self.state

    def dot(self):
        return dot

    def gen(self):
        return gen


class Fringe(ABC):
    """
    General fringe abstract class
    """

    def __init__(self, fringe=None):
        """
        Initializes the fringe
        :param fringe: initial fringe
        """
        self.fringe = fringe
        self.frdict = {}  # For quick access to fringe content
        self.frlen = 0

    def is_empty(self):
        """
        Checks if the fringe is empty
        :return: True if empty, False otherwise
        """
        return self.frlen == 0

    @abstractmethod
    def add(self, n):
        """
        Adds a new state to the fringe
        :param n: node to be added to the fringe
        """
        raise NotImplementedError

    def replace(self, n):
        """
        Replaces the node with state 'n.state' with the new node 'n'
        :param n: node with the state to replace
        """
        self.frdict[n.state].removed = True
        self.frdict[n.state] = n
        self.frlen -= 1
        self.add(n)

    @abstractmethod
    def remove(self):
        """
        Returns (and removes) the first node of the fringe (depending on how the fringe storres the nodes)
        :return: removed node
        """
        raise NotImplementedError

    def __len__(self):
        """
        Returns the current length of the fringe
        :return: current length of the fringe
        """
        return self.frlen

    def __contains__(self, item):
        """
        Checks if the fringe contais the state item
        :param item: state item to search within the fringe
        :return: True if contained, False otherwise
        """
        return item in self.frdict

    def __getitem__(self, i):
        """
        Indexing function: returns the node embedding a specified state (if in the fringe)
        :param i: index (state)
        :return: node
        """
        return self.frdict[i]


class QueueFringe(Fringe):
    """
    Queue implementation of the fringe (FIFO)
    """

    def __init__(self):
        super().__init__(deque())

    def add(self, n):
        self.frdict[n.state] = n
        self.fringe.append(n)
        self.frlen += 1

    def remove(self):
        while True:
            n = self.fringe.popleft()
            if not n.removed:
                if n.state in self.frdict:
                    del self.frdict[n.state]
                self.frlen -= 1
                return n


class StackFringe(Fringe):
    """
    Stack implementation of the fringe (LIFO)
    """

    def __init__(self):
        super().__init__([])

    def add(self, n):
        self.frdict[n.state] = n
        self.fringe.append(n)
        self.frlen += 1

    def remove(self):
        while True:
            n = self.fringe.pop()
            if not n.removed:
                if n.state in self.frdict:
                    del self.frdict[n.state]
                self.frlen -= 1
                return n


class PriorityFringe(Fringe):
    """
    Ordered implementation of the fringe
    """

    def __init__(self):
        super().__init__([])

    def add(self, n):
        heapq.heappush(self.fringe, n)
        self.frdict[n.state] = n
        self.frlen += 1

    def remove(self):
        while True:
            n = heapq.heappop(self.fringe)
            if not n.removed:
                if n.state in self.frdict:
                    del self.frdict[n.state]
                self.frlen -= 1
                return n
