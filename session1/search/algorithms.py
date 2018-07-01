"""
Search algorithms: DFS, IDS, BFS, UCS, GREEDY, A*
"""
from dot_util import close_dot, gen_label, gl_astar, gl_greedy
from timeit import default_timer as timer
from datastructures.fringe import *
from search import heuristics


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
    path, stats, nodes, _ = stype(problem, opt=True, avd=avd, limit=-1)
    gen, graph = close_dot(stats[1], nodes)
    return path, (timer() - t, stats[1], gen, stats[2]), graph


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
        path, temp_stats, nodes, cutoff = stype(problem, opt=opt, avd=avd, limit=depth)
        gen, temp_graph = close_dot(temp_stats[1], nodes, sub=True)
        depth += 1
        graph += temp_graph
        stats[:-1] = [x + y for x, y in zip(stats[:-1], temp_stats[:-1])]
        stats[-1] = max(stats[-1], temp_stats[-1])
        if path is not None or not cutoff:
            nodes = (nodes[0], None)
            gen, graph = close_dot(stats[0], nodes, graph)
            return path, (timer() - t, stats[1], gen, stats[2]), graph


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
    def _rdls(_problem, _node, _limit, _closed, _graph=False, _gl=gen_label, _opt=False, _avd=False):
        """
        Recursive depth-limited search (graph search version)
        :param _problem: problem
        :param _node: node to expand
        :param _limit: depth limit budget
        :param _closed: completely explored nodes
        :return: (path, cutoff, expc, gen, max_depth): path, cutoff flag, expanded nodes, max depth reached
        """
        _exp_nodes, _cutoff, _depth_max = 0, False, _node.pathcost

        if _problem.goalstate == _node.state:
            return build_path(_node), _exp_nodes, _node.pathcost + 1, _node, False

        if _graph:
            if _node.state not in _closed:
                _closed.add(_node.state)
            else:
                return None, _exp_nodes, _depth_max, None, _cutoff

        if _limit == 0:
            return None, _exp_nodes, _node.pathcost, None, True

        for action in range(_problem.action_space.n):
            child_node = \
                FringeNode(_problem.sample(_node.state, action), _node.pathcost + 1, 0, _node, action, problem, _gl)
            # _dot += gen_trans(_node, child_node, action, _problem, _gl)

            if _graph and child_node.state in _closed:
                continue

            if not _avd or child_node.state not in build_path(_node):  # Flag on avoid branch tree repetition (avd)
                # _dot += _gl(_node, _problem, True)

                result, temp_expc, temp_depth, temp_node, temp_cutoff = \
                    _rdls(_problem, child_node, _limit - 1, _closed, _graph, _gl, _opt, _avd)

                _exp_nodes += temp_expc + 1
                _cutoff = _cutoff or temp_cutoff
                _depth_max = max(temp_depth, _depth_max)

                if result is not None:
                    return result, _exp_nodes, _depth_max, temp_node, _cutoff

        return None, _exp_nodes, _depth_max, None, _cutoff

    t = timer()
    root = FringeNode(problem.startstate, 0, 0, None, None, problem, gen_label, 'circle', limit)
    path, expc, max_depth, node, cutoff = _rdls(problem, root, limit, closed, graph, _opt=opt, _avd=avd)
    return path, (timer() - t, expc + 1, max_depth + len(closed)), (root, node), cutoff


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
    path, stats, nodes, _ = stype(problem, StackFringe(), lambda n, c: 0, gen_label, opt, avd, limit)
    gen, graph = close_dot(stats[0], nodes)
    return path, (timer() - t, stats[0], gen, stats[1]), graph


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
        path, temp_stats, nodes, cutoff = stype(problem, StackFringe(), opt=opt, avd=avd, limit=depth)
        gen, temp_graph = close_dot(temp_stats[0], nodes, sub=True)
        depth += 1
        graph += temp_graph
        stats[:-1] = [x + y for x, y in zip(stats[:-1], temp_stats[:-1])]
        stats[-1] = max(stats[-1], temp_stats[-1])
        if path is not None or not cutoff:
            nodes = (nodes[0], None)
            gen, graph = close_dot(stats[0], nodes, graph)
            return path, (timer() - t, stats[0], gen, stats[1]), graph


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
    gen, graph = close_dot(stats[0], node)
    return path, (timer() - t, stats[0], gen, stats[1]), graph


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
    path, stats, nodes, _ = stype(problem, PriorityFringe(), g, gen_label, opt=opt, avd=avd)
    gen, graph = close_dot(stats[0], nodes)
    return path, (timer() - t, stats[0], gen, stats[1]), graph


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
    path, stats, nodes, _ = stype(problem, PriorityFringe(), g, gl_greedy, opt=opt, avd=avd, shape='record')
    gen, graph = close_dot(stats[0], nodes)
    return path, (timer() - t, stats[0], gen, stats[1]), graph


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
        return heuristics.l1_norm(problem.state_to_pos(c), problem.state_to_pos(int(problem.goalstate))) \
               + n.pathcost + 1 if n is not None else 0

    t = timer()
    path, stats, nodes, _ = stype(problem, PriorityFringe(), f, gl_astar, opt=opt, avd=avd, shape='record')
    gen, graph = close_dot(stats[0], nodes)
    return path, (timer() - t, stats[0], gen, stats[1]), graph


def tree_search(problem, fringe, f=lambda n, c: 0, gl=gen_label, opt=False, avd=False, limit=-1, shape='circle'):
    return _search(problem, fringe, f, shape, gl, graph=False, opt=opt, avd=avd, limit=limit)


def graph_search(problem, fringe, f=lambda n, c: 0, gl=gen_label, opt=False, avd=False, limit=-1, shape='circle'):
    return _search(problem, fringe, f, shape, gl, graph=True, opt=opt, avd=avd, limit=limit)


def _search(problem, fringe, f, shape, gl=gen_label, graph=False, opt=False, avd=False, limit=-1):
    """
    Search (avoid branch repetition)
    :param graph: enable graph search
    :param gl:
    :param problem: problem
    :param fringe: fringe data structure
    :param f: node evaluation function
    :return: (path, stats): solution as a path and stats
    The stats are a tuple of (expc, max_states): number of expansions, generated states, max states in memory
    """
    root = FringeNode(problem.startstate, 0, f(None, problem.startstate), None, None, problem, gl, shape, limit)
    expc, i, max_states, closed, = 0, 0, 0, {root.state}
    fringe.add(root)

    while not fringe.is_empty():
        expc += 1
        max_states, node = max(max_states, len(fringe) + len(closed)), fringe.remove()

        if node.state == problem.goalstate:
            return build_path(node), [expc, max_states], (root, node), False

        if graph and node.state not in closed:
            closed.add(node.state)

        if limit == i:
            return None, [expc, max_states], (root, None), True

        for action in range(problem.action_space.n):
            child_state = problem.sample(node.state, action)

            if not avd or child_state not in build_path(node):  # Flag on avoid branch tree repetition (avd)
                child_node = FringeNode(
                    child_state, node.pathcost + 1, f(node, child_state), node, action, problem, gl)

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
        i += 1

    return None, [expc, max_states], (root, None), False


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
