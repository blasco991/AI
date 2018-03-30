"""
Search algorithms: IDS, BFS, UC, GREEDY, A*
"""

from timeit import default_timer as timer
from datastructures.fringe import *
from search import heuristics


def ids(problem, stype):
    """
    Iterative deepening depth-first search
    :param problem: problem
    :param stype: type of search: graph or tree (dls_gs or dls_ts)
    :return: (path, stats): solution as a path and stats
    The stats are a tuple of (time, npexp, maxdepth): elapsed time, number of expansions, max depth reached
    """
    t, depth, stats, cutoff, solution = timer(), 0, (), True, None

    while cutoff:
        depth += 1
        solution, cutoff, stats = stype(problem, depth)
    return solution, (timer() - t, stats[1], stats[2])


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


def rdls_ts(problem, node, limit):
    """
    Recursive depth-limited search (tree search version)
    :param problem: problem
    :param node: node to expand
    :param limit: depth limit budget
    :return: (path, cutoff, expc, maxdepth): path, cutoff flag, expanded nodes, max depth reached
    """
    exp_nodes, cutoff = 0, False
    depth = 1

    if problem.goalstate == node.state:
        return build_path(node), False, exp_nodes, node.pathcost
    elif limit == 0:
        return "cutoff", True, exp_nodes, node.pathcost

    for action in range(problem.action_space.n):
        child_node = FringeNode(problem.sample(node.state, action), node.pathcost + 1, 0, node)
        result, cutoff, temp_expc, temp_max = rdls_ts(problem, child_node, limit - 1)
        exp_nodes += temp_expc + 1
        depth += temp_max

        if isinstance(result, tuple):
            return result, cutoff, exp_nodes, depth

    if cutoff:
        return "cutoff", True, exp_nodes, node.pathcost + limit

    return None, False, exp_nodes, node.pathcost + limit


def dls_gs(problem, limit):
    """
    Depth-limited search (graph search)
    :param problem: problem
    :param limit: depth limit budget
    :return: (path, stats): solution as a path, cutoff flag and stats
    The stats are a tuple of (time, npexp, maxdepth): elapsed time, number node from expansions, max depth reached
    """
    t = timer()
    closed = set()
    path, cutoff, expc, maxdepth = rdls_gs(problem, FringeNode(problem.startstate, 0, 0, None), limit, closed)
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
    exp_nodes, cutoff = 0, False
    depth = 1

    if problem.goalstate == node.state:
        return build_path(node), cutoff, exp_nodes, node.pathcost
    elif limit == 0:
        return "cutoff", True, exp_nodes, node.pathcost

    if node.state not in closed:
        closed.add(node.state)
        exp_nodes += 1
        for action in range(problem.action_space.n):
            child_node = FringeNode(problem.sample(node.state, action), node.pathcost + 1, 0, node)
            result, cutoff, temp_exp_nodes, temp_max = rdls_gs(problem, child_node, limit - 1, closed)
            exp_nodes += temp_exp_nodes + 1
            depth += temp_max

            if isinstance(result, tuple):
                return result, cutoff, exp_nodes, depth

    if cutoff:
        return "cutoff", True, exp_nodes, node.pathcost + limit

    return None, cutoff, exp_nodes, node.pathcost + limit


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

    def h(n, c):
        """
        Path cost function
        :param n: node
        :param c:
        :return: L1 norm distance value
        """
        return heuristics.l1_norm(problem.state_to_pos(n.state), problem.state_to_pos(problem.goalstate))

    t = timer()
    path, stats = stype(problem, PriorityFringe(), h)
    return path, (timer() - t, stats[0], stats[1])


def astar(problem, stype):
    """
    A* best-first search
    :param problem: problem
    :param stype: type of search: graph or tree (graph_search or tree_search)
    :return: (path, stats): solution as a path and stats
    The stats are a tuple of (time, expc, maxstates): elapsed time, number of expansions, max states in memory
    """

    def f(n, c):
        """
        f(n) = g(n) + h(n)
        :param n: node
        :param c:
        :return: L1 norm distance value
        """
        return n.pathcost + heuristics.l1_norm(problem.state_to_pos(n.state), problem.state_to_pos(problem.goalstate))

    t = timer()
    path, stats = stype(problem, PriorityFringe(), f)
    return path, (timer() - t, stats[0], stats[1])


def graph_search(problem, fringe, f=lambda n, c: 0):
    """
    Graph search
    :param problem: problem
    :param fringe: fringe data structure
    :param f: node evaluation function
    :return: (path, stats): solution as a path and stats
    The stats are a tuple of (expc, maxstates): number of expansions, max states in memory
    """
    closed = set()
    i, max_states = 1, 0
    fringe.add(FringeNode(problem.startstate, 0, 0, None))

    while i > 0:
        tmp = len(fringe.fringe) + len(closed)
        max_states = tmp if tmp > max_states else max_states

        if fringe.is_empty():
            return None, [i, max_states]

        node = fringe.remove()
        if node.state == problem.goalstate:
            return build_path(node), [i, max_states]

        if node.state not in closed:
            closed.add(node.state)
            for action in range(problem.action_space.n):
                state = problem.sample(node.state, action)
                if state not in fringe:
                    i += 1
                    fringe.add(FringeNode(state, node.pathcost + 1, f(node, state), node))


def tree_search(problem, fringe, f=lambda n, c: 0):
    """
    Tree search
    :param problem: problem
    :param fringe: fringe data structure
    :param f: node evaluation function
    :return: (path, stats): solution as a path and stats
    The stats are a tuple of (expc, maxstates): number of expansions, max states in memory
    """
    i, max_states = 1, 0
    fringe.add(FringeNode(problem.startstate, 0, 0, None))

    while True:
        max_states = len(fringe.fringe) if len(fringe.fringe) > max_states else max_states

        if fringe.is_empty():
            return None, [i, max_states]

        node = fringe.remove()
        if node.state == problem.goalstate:
            return build_path(node), [i, max_states]

        for action in range(problem.action_space.n):
            i += 1
            fringe.add(FringeNode(problem.sample(node.state, action), node.pathcost + 1,
                                  f(node, problem.sample(node.state, action)), node))


def tree_search_plus(problem, fringe, f=lambda n, c: 0):
    """
    Tree search
    :param problem: problem
    :param fringe: fringe data structure
    :param f: node evaluation function
    :return: (path, stats): solution as a path and stats
    The stats are a tuple of (expc, maxstates): number of expansions, max states in memory
    """
    i, max_states = 1, 0
    fringe.add(FringeNode(problem.startstate, 0, 0, None))

    while True:
        max_states = len(fringe.fringe) if len(fringe.fringe) > max_states else max_states

        if fringe.is_empty():
            return None, [i, max_states]

        node = fringe.remove()
        if node.state == problem.goalstate:
            return build_path(node), [i, max_states]

        for action in range(problem.action_space.n):
            child_state = problem.sample(node.state, action)
            child_node = FringeNode(child_state, node.pathcost + 1, f(node, child_state), node)
            if child_state not in build_path(node) and child_state not in fringe:
                i += 1
                fringe.add(child_node)


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
