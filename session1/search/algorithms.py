"""
Search algorithms: IDS, BFS, UC, GREEDY, A*
"""

from timeit import default_timer as timer
from datastructures.fringe import *


def ids(problem, stype):
    """
    Iterative deepening depth-first search
    :param problem: problem
    :param stype: type of search: graph or tree (dls_gs or dls_ts)
    :return: (path, stats): solution as a path and stats
    The stats are a tuple of (time, npexp, maxdepth): elapsed time, number of expansions, max depth reached
    """
    t = timer()
    # from depth = 0 to infinity
    #   solution, cutoff, stats = stype(problem, depth)
    # return solution, (timer() - t, expc, maxdepth)


def dls_gs(problem, limit):
    """
    Depth-limited search (tree search)
    :param problem: problem
    :param limit: depth limit budget
    :return: (path, stats): solution as a path, cutoff flag and stats
    The stats are a tuple of (time, npexp, maxdepth): elapsed time, number of expansions, max depth reached
    """
    pass


def dls_ts(problem, limit):
    """
    Depth-limited search (tree search)
    :param problem: problem
    :param limit: depth limit budget
    :return: (path, cutoff, stats): solution as a path, cutoff flag and stats
    The stats are a tuple of (time, npexp, maxdepth): elapsed time, number of expansions, max depth reached
    """
    t = timer()
    path, cutoff, expc, maxdepth = rdls_ts(problem, FringeNode(problem.startstate, 0, 0, None), limit)
    return path, cutoff, (timer() - t, expc, maxdepth)


def rdls_gs(problem, node, limit, closed):
    """
    Recursive depth-limited search (graph search version)
    :param problem: problem
    :param node: node to expand
    :param limit: depth limit budget
    :param closed: completely explored nodes
    :return: (path, cutoff, expc, maxdepth): path, cutoff flag, expanded nodes, max depth reached
    """
    pass


def rdls_ts(problem, node, limit):
    """
    Recursive depth-limited search (tree search version)
    :param problem: problem
    :param node: node to expand
    :param limit: depth limit budget
    :return: (path, cutoff, expc, maxdepth): path, cutoff flag, expanded nodes, max depth reached
    """
    pass


def bfs(problem, stype):
    """
    Breadth-first search
    :param problem: problem
    :param stype: type of search: graph or tree (graph_search or tree_search)
    :return: (path, stats): solution as a path and stats
    The stats are a tuple of (time, expc, maxstates): elapsed time, number of expansions, max states in memory
    """
    t = timer()
    path, stats = stype(problem, QueueFringe())
    return path, (timer() - t, stats[0], stats[1])


def ucs(problem, stype):
    """
    Uniform-cost search
    :param problem: problem
    :param stype: type of search: graph or tree (graph_search or tree_search)
    :return: (path, stats): solution as a path and stats
    The stats are a tuple of (time, expc, maxstates): elapsed time, number of expansions, max states in memory
    """
    def g(n, c):
        """
        Path cost function
        :param n: node
        :param c: child state of 'n'
        :return: path cost from root to 'c'
        """
        if n is None:
            return 0
        return n.pathcost + 1

    t = timer()
    path, stats = stype(problem, PriorityFringe(), g)
    return path, (timer() - t, stats[0], stats[1])


def greedy(problem, stype):
    """
    Greedy best-first search
    :param problem: problem
    :param stype: type of search: graph or tree (graph_search or tree_search)
    :return: (path, stats): solution as a path and stats
    The stats are a tuple of (time, expc, maxstates): elapsed time, number of expansions, max states in memory
    """
    pass


def astar(problem, stype):
    """
    A* best-first search
    :param problem: problem
    :param stype: type of search: graph or tree (graph_search or tree_search)
    :return: (path, stats): solution as a path and stats
    The stats are a tuple of (time, expc, maxstates): elapsed time, number of expansions, max states in memory
    """
    pass


def graph_search(problem, fringe, f=lambda n, c: 0):
    """
    Graph search
    :param problem: problem
    :param fringe: fringe data structure
    :param f: node evaluation function
    :return: (path, stats): solution as a path and stats
    The stats are a tuple of (expc, maxstates): number of expansions, max states in memory
    """
    pass


def tree_search(problem, fringe, f=lambda n, c: 0):
    """
    Tree search
    :param problem: problem
    :param fringe: fringe data structure
    :param f: node evaluation function
    :return: (path, stats): solution as a path and stats
    The stats are a tuple of (expc, maxstates): number of expansions, max states in memory
    """
    pass


def build_path(node):
    """
    Builds a path going backward from a node
    :param node: node to start from
    :return: path from root to 'node'
    """
    path = []
    while node.parent is not None:
        path.append(node.state)
        node = node.parent
    return tuple(reversed(path))
