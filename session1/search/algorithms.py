"""
Search algorithms: DFS, IDS, BFS, UCS, GREEDY, A*
"""
from dot_util import close_dot, gen_label, gl_astar, gl_greedy, dot_init
from timeit import default_timer as timer
from datastructures.fringe import *
from search import heuristics
import gym_ai_lab
import gym.spaces


def r_dfs(problem, stype, opt=False, avd=False):
    """
    Depth-first search
    :param avd:
    :param opt:
    :param problem: problem
    :param stype: type of search: graph or tree (graph_search or tree_search)
    :return: (path, stats, graph): solution as a path and stats
    The stats are a tuple of (time, expc, max_states): elapsed time, number of expansions, max states in memory
    """
    t = timer()
    path, stats, node, _ = stype(problem, opt=opt, avd=avd, limit=-1)
    return path, (timer() - t, stats[1], gen(), stats[2]), close_dot(stats[1], node)


def r_ids(problem, stype, opt=False, avd=False):
    """
    Iterative deepening depth-first search
    :param avd:
    :param opt:
    :param problem: problem
    :param stype: type of search: graph or tree (dls_gs or dls_ts)
    :return: (path, stats): solution as a path and stats
    The stats are a tuple of (time, npexp, max_depth): elapsed time, number of expansions, max depth reached
    """
    t, depth, stats, cutoff = timer(), 0, [0, 0, 0, 0], True
    graph = dot_init(problem)
    while cutoff:
        path, temp_stats, node, cutoff = stype(problem, opt=opt, avd=avd, limit=depth)
        temp_graph = close_dot(temp_stats[1], node, sub=True)
        depth += 1
        graph += temp_graph
        stats[:-1] = [x + y for x, y in zip(stats[:-1], temp_stats[:-1])]
        stats[-1] = max(stats[-1], temp_stats[-1])
        if path is not None or not cutoff:
            graph = close_dot(stats[0], node, graph)
            return path, (timer() - t, stats[1], gen(), stats[2]), graph


def dls_ts(problem, opt=False, avd=False, limit=-1):
    """
    Depth-limited search (tree search)
    :param avd:
    :param opt:
    :param problem: problem
    :param limit: depth limit budget
    :return: (path, cutoff, stats): solution as a path, cutoff flag and stats
    The stats are a tuple of (time, npexp, gen, max_depth): elapsed time, number of expansions, max depth reached
    """
    return _dls(problem, frozenset(), graph=False, opt=opt, avd=avd, limit=limit)


def dls_gs(problem, opt=False, avd=False, limit=-1):
    """
    Depth-limited search (graph search)
    :param avd:
    :param opt:
    :param problem: problem
    :param limit: depth limit budget
    :return: (path, stats): solution as a path, cutoff flag and stats
    The stats are a tuple of (time, npexp, gen, max_depth): elapsed time, number node from expansions, max depth reached
    """
    return _dls(problem, set(), graph=True, opt=opt, avd=avd, limit=limit)


def _dls(problem, closed=None, graph=False, opt=False, avd=False, limit=-1):
    def _rdls(_p, _node, _limit, _closed, _graph=False, _gl=gen_label, _opt=False, _avd=False):
        """
        Recursive depth-limited search (graph search version)
        :param _p: problem
        :param _node: node to expand
        :param _limit: depth limit budget
        :param _closed: completely explored nodes
        :return: (path, cutoff, expc, gen, max_depth): path, cutoff flag, expanded nodes, max depth reached
        """
        _exp_nodes, _cutoff, _depth_max = 0, False, _node.pathcost

        if _p.goalstate == _node.state:
            return build_path(_node), _exp_nodes, _node.pathcost + 1, _node, False

        if _graph:
            if _node.state not in _closed:
                _closed.add(_node.state)
            else:
                node.close_node(_p, _gl, None, _closed)  # OPTIONAL
                return None, _exp_nodes, _depth_max, None, _cutoff

        if _limit == 0:
            return None, _exp_nodes, _node.pathcost, None, True

        for action in range(_p.action_space.n):
            child = FringeNode(_p.sample(_node.state, action), _node.pathcost + 1, 0, _node, action, problem, _gl)

            if _graph and child.state in _closed:
                child.close_node(_p, _gl, None, _closed)  # OPTIONAL
                continue

            if not _avd or child.state not in build_path(_node):  # Flag on avoid branch tree repetition (avd)

                result, t_expc, t_depth, t_node, t_cut = _rdls(_p, child, _limit - 1, _closed, _graph, _gl, _opt, _avd)

                _exp_nodes += t_expc + 1
                _cutoff = _cutoff or t_cut
                _depth_max = max(t_depth, _depth_max)

                if result is not None:
                    return result, _exp_nodes, _depth_max, t_node, _cutoff

            else:  # OPTIONAL
                child.close_node(_p, _gl, None, _closed)

        return None, _exp_nodes, _depth_max, None, _cutoff

    t = timer()
    path, expc, max_depth, node, cutoff = \
        _rdls(problem, FringeNode(problem.startstate, 0, 0, None, None, problem, gen_label, 'circle', limit, closed),
              limit, closed, graph, _opt=opt, _avd=avd)
    return path, (timer() - t, expc + 1, max_depth + len(closed)), node, cutoff


def dfs(problem, stype, opt=False, avd=True, limit=-1):
    """
    Breadth-first search
    :param limit:
    :param avd:
    :param opt:
    :param problem: problem
    :param stype: type of search: graph or tree (graph_search or tree_search)
    :return: (path, stats, graph): solution as a path and stats
    The stats are a tuple of (time, expc, max_states): elapsed time, number of expansions, max states in memory
    """
    t = timer()
    path, stats, node, _ = stype(problem, StackFringe(), lambda n, c: 0, gen_label, opt, avd, limit)
    return path, (timer() - t, stats[0], gen(), stats[1]), close_dot(stats[0], node)


def ids(problem, stype, opt=False, avd=False):
    """
    Iterative deepening depth-first search
    :param avd:
    :param opt:
    :param problem: problem
    :param stype: type of search: graph or tree (dls_gs or dls_ts)
    :return: (path, stats): solution as a path and stats
    The stats are a tuple of (time, npexp, max_depth): elapsed time, number of expansions, max depth reached
    """
    t, depth, stats, cutoff = timer(), 0, [0, 0, 0, 0], True
    graph = dot_init(problem)
    while cutoff:
        path, temp_stats, node, cutoff = stype(problem, StackFringe(), opt=opt, avd=avd, limit=depth)
        temp_graph = close_dot(temp_stats[0], node, sub=True)
        depth += 1
        graph += temp_graph
        stats[:-1] = [x + y for x, y in zip(stats[:-1], temp_stats[:-1])]
        stats[-1] = max(stats[-1], temp_stats[-1])
        if path is not None or not cutoff:
            graph = close_dot(stats[0], node, graph)
            return path, (timer() - t, stats[0], gen(), stats[1]), graph


def bfs(problem, stype, opt=False, avd=False):
    """
    Breadth-first search
    :param avd:
    :param opt:
    :param problem: problem
    :param stype: type of search: graph or tree (graph_search or tree_search)
    :return: (path, stats, graph): solution as a path and stats
    The stats are a tuple of (time, expc, max_states): elapsed time, number of expansions, max states in memory
    """
    t = timer()
    path, stats, node, _ = stype(problem, QueueFringe(), lambda n, c: 0, gen_label, opt, avd)
    return path, (timer() - t, stats[0], gen(), stats[1]), close_dot(stats[0], node)


def ucs(problem, stype, opt=False, avd=False):
    """
    Uniform-cost search
    :param avd: 
    :param opt:
    :param problem: problem
    :param stype: type of search: graph or tree (graph_search or tree_search)
    :return: (path, stats): solution as a path and stats
    The stats are a tuple of (time, expc, max_states): elapsed time, number of expansions, max states in memory
    """

    def g(n, c=None):
        """
        Path cost function
        :param n: node
        :param c: child state of 'n'
        :return: path cost from root to 'c'
        """
        return n.pathcost + 1 if n is not None else 0

    t = timer()
    path, stats, node, _ = stype(problem, PriorityFringe(), g, gen_label, opt=opt, avd=avd)
    return path, (timer() - t, stats[0], gen(), stats[1]), close_dot(stats[0], node)


def greedy(problem, stype, opt=False, avd=False):
    """
    Greedy best-first search
    :param avd:
    :param opt:
    :param problem: problem
    :param stype: type of search: graph or tree (graph_search or tree_search)
    :return: (path, stats): solution as a path and stats
    The stats are a tuple of (time, expc, max_states): elapsed time, number of expansions, max states in memory
    """

    def g(n, c=None):
        """
        Path cost function
        :param n: node
        :param c: child state of 'n'
        :return: L1 norm distance value
        """
        return heuristics.l1_norm(problem.state_to_pos(c), problem.state_to_pos(problem.goalstate))

    t = timer()
    path, stats, node, _ = stype(problem, PriorityFringe(), g, gl_greedy, opt=opt, avd=avd, shape='record')
    return path, (timer() - t, stats[0], gen(), stats[1]), close_dot(stats[0], node)


def astar(problem, stype, opt=False, avd=False):
    """
    A* best-first search
    :param avd:
    :param opt:
    :param problem: problem
    :param stype: type of search: graph or tree (graph_search or tree_search)
    :return: (path, stats): solution as a path and stats
    The stats are a tuple of (time, expc, max_states): elapsed time, number of expansions, max states in memory
    """

    def f(n, c=None):
        """
        f(n) = g(n) + h(n)
        :param n: node
        :param c: child state of 'n'
        :return: L1 norm distance value
        """
        return 0 if n is None else \
            heuristics.l1_norm(problem.state_to_pos(c), problem.state_to_pos(int(problem.goalstate))) + n.pathcost + 1

    t = timer()
    path, stats, node, _ = stype(problem, PriorityFringe(), f, gl_astar, opt=opt, avd=avd, shape='record')
    return path, (timer() - t, stats[0], gen(), stats[1]), close_dot(stats[0], node)


def tree_search(problem, fringe, f=lambda n, c: 0, gl=gen_label, opt=False, avd=False, limit=-1, shape='circle'):
    return _search(problem, fringe, f, shape, gl, graph=False, opt=opt, avd=avd, limit=limit)


def graph_search(problem, fringe, f=lambda n, c: 0, gl=gen_label, opt=False, avd=False, limit=-1, shape='circle'):
    return _search(problem, fringe, f, shape, gl, graph=True, opt=opt, avd=avd, limit=limit)


def _search(p, fringe, f, shape, gl=gen_label, graph=False, opt=False, avd=False, limit=-1):
    """
    Search (avoid branch repetition)
    :param graph: enable graph search
    :param gl: function that generate DOT label for a given node
    :param p: problem
    :param fringe: fringe data structure
    :param f: node evaluation function
    :return: (path, stats): solution as a path and stats
    The stats are a tuple of (expc, max_states): number of expansions, generated states, max states in memory
    """
    closed = {p.startstate} if graph else frozenset()
    expc, i, max_states, = 0, 0, 0
    fringe.add(FringeNode(p.startstate, 0, f(None, p.startstate), None, None, p, gl, shape, limit, closed, fringe))

    while not fringe.is_empty():
        expc += 1
        max_states, node = max(max_states, len(fringe) + len(closed)), fringe.remove()

        if node.state == p.goalstate:
            return build_path(node), [expc, max_states], node, False

        if graph and node.state not in closed:
            closed.add(node.state)

        if limit == i:
            return None, [expc, max_states], None, True

        for action in range(p.action_space.n):
            child_state = p.sample(node.state, action)

            child_node = FringeNode(child_state, node.pathcost + 1, f(node, child_state), node, action, p, gl)

            if not avd or child_state not in build_path(node):  # Flag on avoid branch tree repetition (avd)

                if not graph and not opt:  # TREE SEARCH not opt
                    fringe.add(child_node)

                elif graph or opt:  # TREE SEARCH opt and GRAPH_SEARCH
                    if child_state not in closed and child_state not in fringe:
                        fringe.add(child_node)

                    elif child_state in fringe:
                        # if child_state IN fringe but NOT in closed
                        if child_node.value < fringe[child_state].value:
                            # if child_state IN fringe -> check pathcost
                            fringe.replace(child_node)
                        else:  # OPTIONAL
                            child_node.close_node(p, gl, fringe, closed)
                    else:  # OPTIONAL
                        child_node.close_node(p, gl, fringe, closed)
                else:  # OPTIONAL
                    child_node.close_node(p, gl, fringe, closed)
            else:  # OPTIONAL
                child_node.close_node(p, gl, fringe, closed)

        i += 1

    return None, [expc, max_states], None, False


def build_path(node):
    """
    Builds a path going backward from a node
    :param node: node to start from
    :return: path from root to 'node'
    """
    path = []
    while node is not None:  # root Node must be in build_path
        path.append(node.state)
        node = node.parent
    return reversed(path)
