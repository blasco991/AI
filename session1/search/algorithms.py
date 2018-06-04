"""
Search algorithms: DFS, IDS, BFS, UCS, GREEDY, A*
"""

from dot_util import dot_init, close_dot as cs, gen_label, gen_trans, gen_code, get_color
from timeit import default_timer as timer
from datastructures.fringe import *
from search import heuristics
import gym.spaces


def dfs(problem, stype, otp=False, avd=False):
    """
    Depth-first search
    :param avd:
    :param otp:
    :param problem: problem
    :param stype: type of search: graph or tree (graph_search or tree_search)
    :return: (path, stats, graph): solution as a path and stats
    The stats are a tuple of (time, expc, max_states): elapsed time, number of expansions, max states in memory
    """
    t = timer()
    path, _, stats, graph, node = stype(problem, -1, dot_init(problem), otp=otp, avd=avd)
    return path, (timer() - t + stats[0], stats[1], stats[2], stats[3]), cs(graph, stats[1], stats[2], node)


def ids(problem, stype, otp=False, avd=False):
    """
    Iterative deepening depth-first search
    :param avd:
    :param otp:
    :param problem: problem
    :param stype: type of search: graph or tree (dls_gs or dls_ts)
    :return: (path, stats): solution as a path and stats
    The stats are a tuple of (time, npexp, max_depth): elapsed time, number of expansions, max depth reached
    """
    t, depth, stats, cutoff = timer(), 0, [0, 0, 0, 0], True
    graph = dot_init(problem, strict=True)
    while cutoff:
        path, cutoff, temp_stats, temp_graph, node = stype(problem, depth, '', otp=otp, avd=avd)
        depth += 1
        # graph += temp_graph
        stats[:-1] = [x + y for x, y in zip(stats[:-1], temp_stats[:-1])]
        stats[-1] = max(stats[-1], temp_stats[-1])
        if path is not None or not cutoff:
            return path, (timer() - t, stats[1], stats[2], stats[3]), cs(graph, stats[1], stats[2], node)


def dls_ts(problem, limit, dot='', otp=False, avd=False):
    """
    Depth-limited search (tree search)
    :param avd:
    :param otp:
    :param dot:
    :param problem: problem
    :param limit: depth limit budget
    :return: (path, cutoff, stats): solution as a path, cutoff flag and stats
    The stats are a tuple of (time, npexp, gen, max_depth): elapsed time, number of expansions, max depth reached
    """
    return _dls(problem, limit, dot, frozenset(), False, otp, avd)


def dls_gs(problem, limit, dot='', otp=False, avd=False):
    """
    Depth-limited search (graph search)
    :param avd:
    :param otp:
    :param dot:
    :param problem: problem
    :param limit: depth limit budget
    :return: (path, stats): solution as a path, cutoff flag and stats
    The stats are a tuple of (time, npexp, gen, max_depth): elapsed time, number node from expansions, max depth reached
    """
    return _dls(problem, limit, dot, {problem.startstate}, True, otp)


def _dls(problem, limit, dot='', closed=None, graph=False, otp=False, avd=False):
    t, dot = timer(), dot if len(dot) > 0 else dot_init(problem, sub=True, cluster=limit)

    path, cutoff, expc, gen, max_depth, dot, node = \
        _rdls(problem, FringeNode(problem.startstate, 0, 0, None), limit, closed, dot, graph, otp=otp, avd=avd)

    if not len(dot) > 0:
        dot = cs(dot, expc, gen, node if not cutoff else None)

    return path, cutoff, (timer() - t, expc + 1, gen + 1, max_depth + len(closed)), dot, node
    # TODO chiedere a Riccardo se non ha dimenticato closed !!!


def _rdls(problem, node, limit, closed, dot='', graph=False, gl=gen_label, otp=False, avd=False):
    """
    Recursive depth-limited search (graph search version)
    :param dot:
    :param problem: problem
    :param node: node to expand
    :param limit: depth limit budget
    :param closed: completely explored nodes
    :return: (path, cutoff, expc, gen, max_depth): path, cutoff flag, expanded nodes, max depth reached
    """
    # dot += gl(node, problem)
    exp_nodes, gen, cutoff, depth_max = 0, 0, False, node.pathcost

    if problem.goalstate == node.state:
        return build_path(node), False, exp_nodes, gen, node.pathcost + 1, dot, node
    if limit == 0:
        return None, True, exp_nodes, gen, node.pathcost, dot, None

    for action in range(problem.action_space.n):
        child_node = FringeNode(problem.sample(node.state, action), node.pathcost + 1, 0, node)
        # dot += gen_trans(node, child_node, action, problem, dot, gl)
        gen += 1

        if graph:
            if child_node.state not in closed:
                closed.add(child_node.state)
            else:
                continue

        if not avd or child_node.state not in build_path(node):  # Flag on avoid branch tree repetition (avd)
            # dot += gl(node, problem, True)
            result, temp_cutoff, temp_expc, temp_gen, temp_depth, temp_dot, temp_node = \
                _rdls(problem, child_node, limit - 1, closed, '', graph, gl)

            gen += temp_gen
            exp_nodes += temp_expc + 1
            dot += temp_dot
            cutoff = cutoff or temp_cutoff
            depth_max = max(temp_depth, depth_max)

            if result is not None:
                return result, cutoff, exp_nodes, gen, depth_max, dot, temp_node

    return None, cutoff, exp_nodes, gen, depth_max, dot, None


def bfs(problem, stype, otp=False, avd=False):
    """
    Breadth-first search
    :param avd:
    :param otp:
    :param problem: problem
    :param stype: type of search: graph or tree (graph_search or tree_search)
    :return: (path, stats, graph): solution as a path and stats
    The stats are a tuple of (time, expc, max_states): elapsed time, number of expansions, max states in memory
    """
    t = timer()
    path, stats, graph, node = stype(problem, QueueFringe(), lambda n: 0, gen_label, dot_init(problem), otp, avd)
    return path, (timer() - t, stats[0], stats[1], stats[2]), cs(graph, stats[0], stats[1], node)


def ucs(problem, stype, otp=False, avd=False):
    """
    Uniform-cost search
    :param avd: 
    :param otp:
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
        return n.pathcost + 1

    t = timer()
    path, stats, graph, node = \
        stype(problem, PriorityFringe(), g, gen_label, dot_init(problem), otp=otp, avd=avd, is_ucs=True)
    return path, (timer() - t, stats[0], stats[1], stats[2]), cs(graph, stats[0], stats[1], node)


def greedy(problem, stype, otp=False, avd=False):
    """
    Greedy best-first search
    :param avd:
    :param otp:
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
        return heuristics.l1_norm(problem.state_to_pos(n.state), problem.state_to_pos(problem.goalstate))

    def gl(n, p, exp=False, j=None):
        label = '{}'.format(n.state) if j is None else '{}  [{}]'.format(n.state, j)
        return '\n{} [label="<f0>{} |<f1> c:{}" style=filled color={} fillcolor={}]' \
            .format(gen_code(n), label, n.pathcost,
                    'black' if exp or problem.goalstate == n.state else 'white', get_color(n.state, p))

    t = timer()
    path, stats, graph, node = \
        stype(problem, PriorityFringe(), g, gl, dot_init(problem, "record"), otp=otp, avd=avd)
    return path, (timer() - t, stats[0], stats[1], stats[2]), cs(graph, stats[0], stats[1], node)


def astar(problem, stype, otp=False, avd=False):
    """
    A* best-first search
    :param avd:
    :param otp:
    :param problem: problem
    :param stype: type of search: graph or tree (graph_search or tree_search)
    :return: (path, stats): solution as a path and stats
    The stats are a tuple of (time, expc, max_states): elapsed time, number of expansions, max states in memory
    """

    def f(n, c=None):
        """
        f(n) = g(n) + h(n)
        :param n: node
        :param c: child state of 'n' ??? goalstate
        :return: L1 norm distance value
        """
        return n.pathcost + heuristics.l1_norm(problem.state_to_pos(n.state), problem.state_to_pos(problem.goalstate))

    def gl(n, p, exp=False, j=None):
        label = '{}'.format(n.state) if j is None else '{}  [{}]'.format(n.state, j)
        return '\n{} [label="<f0>{} |<f1> c:{} |<f2> f: {} ({}+{})", style=filled color={} fillcolor={}]' \
            .format(gen_code(n), label, n.pathcost, f(n, None), n.pathcost,
                    heuristics.l1_norm(p.state_to_pos(n.state), p.state_to_pos(p.goalstate)),
                    'black' if exp or problem.goalstate == n.state else 'white', get_color(n.state, p))

    t = timer()
    path, stats, graph, node = \
        stype(problem, PriorityFringe(), f, gl, dot_init(problem, "record"), otp=otp, avd=avd)
    return path, (timer() - t, stats[0], stats[1], stats[2]), cs(graph, stats[0], stats[1], node)


def tree_search(problem, fringe, f=lambda n: 0, gl=gen_label, dot='', otp=False, avd=False,
                is_ucs=False):
    return _search(problem, fringe, f, gl, dot, graph=False, otp=otp, avd=avd, is_ucs=is_ucs)


def graph_search(problem, fringe, f=lambda n: 0, gl=gen_label, dot='', otp=False, avd=False,
                 is_ucs=False):
    return _search(problem, fringe, f, gl, dot, graph=True, otp=otp, avd=avd, is_ucs=is_ucs)


def _search(problem, fringe, f, gl=gen_label, dot='', graph=True, otp=False, avd=False, is_ucs=False):
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
    i, j, gen, max_states, closed, root = 0, 0, 1, 0, set(), FringeNode(problem.startstate, 0, 0, None)
    fringe.add(root)
    # dot += gl(root, problem)

    while not fringe.is_empty():

        max_states = max(max_states, len(fringe) + len(closed))
        node, has_exp = fringe.remove(), False

        if node.state == problem.goalstate:
            # dot += gl(node, problem, True, j)
            return build_path(node), [i + 1, gen, max_states], dot, node

        if graph:
            if node.state not in closed:
                closed.add(node.state)
            else:
                continue

        for action in range(problem.action_space.n):
            child_node = FringeNode(problem.sample(node.state, action), node.pathcost + 1, f(node), node)
            # dot += gen_trans(node, child_node, action, problem, dot, gl)
            gen += 1

            if not avd or child_node.state not in build_path(node):  # Flag on avoid branch tree repetition (avd)

                if not graph and not otp:  # TREE SEARCH not otp
                    has_exp = has_exp or True
                    fringe.add(child_node)

                elif graph or otp:  # TREE SEARCH otp and GRAPH_SEARCH
                    has_exp = has_exp or True
                    if child_node.state not in closed and child_node.state not in fringe:
                        fringe.add(child_node)
                    elif child_node.state in fringe and is_ucs:
                        # if child_state IN fringe but NOT in closed
                        f_node = next((n for n in fringe.fringe if n.state == child_node.state), None)
                        if f_node is not None and child_node.pathcost < f_node.pathcost:
                            # if child_state IN fringe -> check pathcost
                            fringe.replace(child_node)

        # dot += gl(node, problem, has_exp)
        if has_exp:
            i += 1

    return None, [i, gen, max_states], dot, None


def build_path(node):
    """
    Builds a path going backward from a node
    :param node: node to start from
    :return: path from root to 'node'
    """
    path = []
    while node is not None:  # IMPORTANT the ROOT node must be in the path!
        path.append(node.state)
        node = node.parent
    return reversed(path)
