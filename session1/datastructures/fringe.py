"""
Data structures representing the fringe for search methods
"""

import heapq
from collections import deque

from abc import ABC, abstractmethod

import dot_util

_dot = ''
_gen = 0
_closed = None
_fringe = None
enable_graph = True


def dot():
    return _dot


def gen():
    return _gen


class FringeNode:
    """
    Fringe state representation
    """

    def __init__(self, state, pathcost, value, parent,
                 cause=None, p=None, gl=None, shape='circle', limit=-1, cl=None, fr=None):
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

        global _dot
        global _gen
        global _closed
        global _fringe
        global enable_graph
        if enable_graph:
            if parent is None:
                _closed = cl
                _fringe = fr
                _gen = 1
                if limit != -1:
                    _dot = dot_util.dot_init(p, shape, sub=True, cluster=limit) + gl(self, p)
                else:
                    _dot = dot_util.dot_init(p, shape) + "\n" + gl(self, p)
            else:
                _dot += dot_util.gen_trans(parent, self, p, gl, _dot, _gen, _fringe, _closed)
                _gen += 1

    def close_node(self, problem, gl, fringe, closed):
        global _dot
        temp = str()
        for line in _dot.splitlines():
            label = dot_util.gen_code(self)
            if (dot_util.gen_code(self.parent) + " -> " + label) in line:
                line = dot_util.gen_trans(self.parent, self, problem, gl, _dot, _gen, fringe, closed, 'dashed')
            temp += line + "\n"
        _dot = temp.replace("\n\n", "\n").replace("\n\n", "\n")

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
