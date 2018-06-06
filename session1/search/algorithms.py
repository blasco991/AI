"""
Search algorithms: DFS, IDS, BFS, UCS, GREEDY, A*
"""
from dot_util import dot_init, close_dot as cs, gen_label, gen_trans, gen_code, get_color
from timeit import default_timer as timer
from datastructures.fringe import *
from search import heuristics
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
    path, stats, graph, node, _ = stype(problem, dot_init(problem), opt=True, avd=avd, limit=-1)
    return path, (timer() - t + stats[0], stats[1], stats[2], stats[3]), cs(graph, stats[1], stats[2], node)


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
    graph = dot_init(problem, strict=True)
    while cutoff:
        path, temp_stats, temp_graph, node, cutoff = stype(problem, '', opt=opt, avd=avd, limit=depth)
        depth += 1
        graph += temp_graph
        stats[:-1] = [x + y for x, y in zip(stats[:-1], temp_stats[:-1])]
        stats[-1] = max(stats[-1], temp_stats[-1])
        if path is not None or not cutoff:
            return path, (timer() - t, stats[1], stats[2], stats[3]), cs(graph, stats[1], stats[2], node)


def dls_ts(problem, dot='', opt=True, avd=True, limit=-1):
    """
    Depth-limited search (tree search)
    :param avd:
    :param opt:
    :param dot:
    :param problem: problem
    :param limit: depth limit budget
    :return: (path, cutoff, stats): solution as a path, cutoff flag and stats
    The stats are a tuple of (time, npexp, gen, max_depth): elapsed time, number of expansions, max depth reached
    """
    return _dls(problem, dot, frozenset(), graph=False, opt=opt, avd=avd, limit=limit)


def dls_gs(problem, dot='', opt=False, avd=False, limit=-1):
    """
    Depth-limited search (graph search)
    :param avd:
    :param opt:
    :param dot:
    :param problem: problem
    :param limit: depth limit budget
    :return: (path, stats): solution as a path, cutoff flag and stats
    The stats are a tuple of (time, npexp, gen, max_depth): elapsed time, number node from expansions, max depth reached
    """
    return _dls(problem, dot, set(), graph=True, opt=opt, avd=avd, limit=limit)


def _dls(problem, dot='', closed=None, graph=False, opt=False, avd=False, limit=-1):
    def _rdls(_problem, _node, _limit, _closed, _dot='', _graph=False, _gl=gen_label, _opt=False, _avd=False):
        """
        Recursive depth-limited search (graph search version)
        :param _dot:
        :param _problem: problem
        :param _node: node to expand
        :param _limit: depth limit budget
        :param _closed: completely explored nodes
        :return: (path, cutoff, expc, gen, max_depth): path, cutoff flag, expanded nodes, max depth reached
        """
        # _dot += _gl(_node, _problem)
        _exp_nodes, _gen, _cutoff, _depth_max = 0, 0, False, _node.pathcost

        if _problem.goalstate == _node.state:
            return build_path(_node), _exp_nodes, _gen, _node.pathcost + 1, _dot, _node, False

        if _graph:
            if _node.state not in _closed:
                _closed.add(_node.state)
            else:
                return None, _exp_nodes, _gen, _depth_max, _dot, None, _cutoff

        if _limit == 0:
            return None, _exp_nodes, _gen, _node.pathcost, _dot, None, True

        for action in range(_problem.action_space.n):
            child_node = FringeNode(_problem.sample(_node.state, action), _node.pathcost + 1, 0, _node)
            # _dot += gen_trans(_node, child_node, action, _problem, _dot, _gl)
            _gen += 1

            if _graph and child_node.state in _closed:
                continue

            if not _avd or child_node.state not in build_path(_node):  # Flag on avoid branch tree repetition (avd)
                # _dot += _gl(_node, _problem, True)

                result, temp_expc, temp_gen, temp_depth, temp_dot, temp_node, temp_cutoff = \
                    _rdls(_problem, child_node, _limit - 1, _closed, '', _graph, _gl, _opt, _avd)

                _gen += temp_gen
                _exp_nodes += temp_expc + 1
                # _dot += temp_dot
                _cutoff = _cutoff or temp_cutoff
                _depth_max = max(temp_depth, _depth_max)

                if result is not None:
                    return result, _exp_nodes, _gen, _depth_max, _dot, temp_node, _cutoff

        return None, _exp_nodes, _gen, _depth_max, _dot, None, _cutoff

    t, dot = timer(), dot if len(dot) > 0 else dot_init(problem, sub=True, cluster=limit)

    path, expc, gen, max_depth, dot, node, cutoff = \
        _rdls(problem, FringeNode(problem.startstate, 0, 0, None), limit, closed, dot, graph, _opt=opt, _avd=avd)

    if not len(dot) > 0:
        dot = cs(dot, expc, gen, node if not cutoff else None)

    return path, (timer() - t, expc + 1, gen + 1, max_depth), dot, node, cutoff
    # TODO max_depth + len(closed)) IMPORTANTE!!!


def dfs(problem, stype, opt=False, avd=True, limit=-1):
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
    path, stats, graph, node, _ = stype(problem, StackFringe(), lambda n, c: 0, gen_label, dot_init(problem), opt, True)
    return path, (timer() - t, stats[0], stats[1], stats[2]), cs(graph, stats[0], stats[1], node)


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
    graph = dot_init(problem, strict=True)
    while cutoff:
        path, temp_stats, temp_graph, node, cutoff = \
            stype(problem, StackFringe(), dot='', opt=opt, avd=avd, limit=depth)
        depth += 1
        graph += temp_graph
        stats[:-1] = [x + y for x, y in zip(stats[:-1], temp_stats[:-1])]
        stats[-1] = max(stats[-1], temp_stats[-1])
        if path is not None or not cutoff:
            return path, (timer() - t, stats[0], stats[1], stats[2]), cs(graph, stats[0], stats[1], node)


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
    path, stats, graph, node, _ = stype(problem, QueueFringe(), lambda n, c: 0, gen_label, dot_init(problem), opt, avd)
    return path, (timer() - t, stats[0], stats[1], stats[2]), cs(graph, stats[0], stats[1], node)


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
    path, stats, graph, node, _ = \
        stype(problem, PriorityFringe(), g, gen_label, dot_init(problem), opt=opt, avd=avd)
    return path, (timer() - t, stats[0], stats[1], stats[2]), cs(graph, stats[0], stats[1], node)


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

    def gl(n, p, exp=False, j=None):
        label = '{}'.format(n.state) if j is None else '{}  [{}]'.format(n.state, j)
        return '\n{} [label="<f0>{} |<f1> c:{}" style=filled color={} fillcolor={}]' \
            .format(gen_code(n), label, n.pathcost,
                    'black' if exp or problem.goalstate == n.state else 'white', get_color(n.state, p))

    t = timer()
    path, stats, graph, node, _ = \
        stype(problem, PriorityFringe(), g, gl, dot_init(problem, "record"), opt=opt, avd=avd)
    return path, (timer() - t, stats[0], stats[1], stats[2]), cs(graph, stats[0], stats[1], node)


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

    def gl(n, p, exp=False, j=None):
        label = '{}'.format(n.state) if j is None else '{}  [{}]'.format(n.state, j)
        return '\n{} [label="<f0>{} |<f1> c:{} |<f2> f: {} ({}+{})", style=filled color={} fillcolor={}]' \
            .format(gen_code(n), label, n.pathcost, f(n.parent, n.state),
                    n.parent.pathcost if n.parent is not None else 0,
                    heuristics.l1_norm(p.state_to_pos(n.state), p.state_to_pos(p.goalstate)),
                    'black' if exp or problem.goalstate == n.state else 'white', get_color(n.state, p))

    t = timer()
    path, stats, graph, node, _ = \
        stype(problem, PriorityFringe(), f, gl, dot_init(problem, "record"), opt=opt, avd=avd)
    return path, (timer() - t, stats[0], stats[1], stats[2]), cs(graph, stats[0], stats[1], node)


def tree_search(problem, fringe, f=lambda n, c: 0, gl=gen_label, dot='', opt=False, avd=False, limit=-1):
    return _search(problem, fringe, f, gl, dot, graph=False, opt=opt, avd=avd, limit=limit)


def graph_search(problem, fringe, f=lambda n, c: 0, gl=gen_label, dot='', opt=False, avd=False, limit=-1):
    return _search(problem, fringe, f, gl, dot, graph=True, opt=opt, avd=avd, limit=limit)


def _search(problem, fringe, f, gl=gen_label, dot='', graph=True, opt=False, avd=False, limit=-1):
    """
    Search (avoid branch repetition)
    :param graph: enable graph search
    :param dot:
    :param gl:
    :param problem: problem
    :param fringe: fringe data structure
    :param f: node evaluation function
    :return: (path, stats): solution as a path and stats
    The stats are a tuple of (expc, generated, max_states): number of expansions, generated states, max states in memory
    """
    root = FringeNode(problem.startstate, 0, f(None, problem.startstate), None)
    expc, i, gen, max_states, closed, = 0, 0, 1, 0, set()
    fringe.add(root)
    # dot += gl(root, problem)

    while not fringe.is_empty():
        expc += 1
        max_states, node = max(max_states, len(fringe) + len(closed)), fringe.remove()

        if node.state == problem.goalstate:
            # dot += gl(node, problem, True, i)
            return build_path(node), [expc, gen, max_states], dot, node, False

        if graph and node.state not in closed:
            closed.add(node.state)

        if limit == i:
            return None, [expc, gen, max_states], dot, None, True

        for action in range(problem.action_space.n):
            child_state = problem.sample(node.state, action)

            if not avd or child_state not in build_path(node):  # Flag on avoid branch tree repetition (avd)
                child_node = FringeNode(child_state, node.pathcost + 1, f(node, child_state), node)
                # dot += gen_trans(node, child_node, action, problem, dot, gl)
                gen += 1

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

    return None, [expc, gen, max_states], dot, None, False


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
    return reversed(path)
