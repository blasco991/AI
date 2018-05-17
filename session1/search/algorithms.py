"""
Search algorithms: DFS, IDS, BFS, UCS, GREEDY, A*
"""

from dot_util import dot_init, close_dot as cs, gen_label, gen_trans, gen_code, get_color
from timeit import default_timer as timer
from datastructures.fringe import *
from search import heuristics
import gym.spaces


def dfs(problem, stype):
    """
    Depth-first search
    :param problem: problem
    :param stype: type of search: graph or tree (graph_search or tree_search)
    :return: (path, stats, graph): solution as a path and stats
    The stats are a tuple of (time, expc, maxstates): elapsed time, number of expansions, max states in memory
    """
    t = timer()
    path, _, stats, graph, node = stype(problem, -1, dot_init(problem))
    return path, (timer() - t + stats[0], stats[1], stats[2], stats[3]), cs(graph, stats[1], stats[2], node)


def ids(problem, stype):
    """
    Iterative deepening depth-first search
    :param problem: problem
    :param stype: type of search: graph or tree (dls_gs or dls_ts)
    :return: (path, stats): solution as a path and stats
    The stats are a tuple of (time, npexp, max_depth): elapsed time, number of expansions, max depth reached
    """
    t, depth, stats, cutoff = timer(), 0, [0, 0, 0, 0], True
    graph = dot_init(problem, strict=True)
    while cutoff:
        path, cutoff, temp_stats, temp_graph, node = stype(problem, depth, '')
        depth += 1
        graph += temp_graph
        stats[:-1] = [x + y for x, y in zip(stats[:-1], temp_stats[:-1])]
        stats[-1] = max(stats[-1], temp_stats[-1])
        if path is not None or not cutoff:
            return path, (timer() - t + stats[0], stats[1], stats[2], stats[3]), cs(graph, stats[1], stats[2], node)


def dls_ts(problem, limit, dot_string=''):
    """
    Depth-limited search (tree search)
    :param dot_string:
    :param problem: problem
    :param limit: depth limit budget
    :return: (path, cutoff, stats): solution as a path, cutoff flag and stats
    The stats are a tuple of (time, npexp, gen, max_depth): elapsed time, number of expansions, max depth reached
    """
    t, graph = timer(), dot_string if len(dot_string) > 0 else dot_init(problem, sub=True, cluster=limit)

    path, cutoff, expc, gen, max_depth, graph, node = \
        _rdls(problem, FringeNode(problem.startstate, 0, 0, None), limit, frozenset(), graph, False)

    if not len(dot_string) > 0:
        graph = cs(graph, expc, gen, node if not cutoff else None)

    return path, cutoff, (timer() - t, expc, gen, max_depth), graph, node


def dls_gs(problem, limit, dot_string=''):
    """
    Depth-limited search (graph search)
    :param dot_string:
    :param problem: problem
    :param limit: depth limit budget
    :return: (path, stats): solution as a path, cutoff flag and stats
    The stats are a tuple of (time, npexp, gen, max_depth): elapsed time, number node from expansions, max depth reached
    """
    t, graph = timer(), dot_string if len(dot_string) > 0 else dot_init(problem, sub=True, cluster=limit)

    path, cutoff, expc, gen, max_depth, graph, node = \
        _rdls(problem, FringeNode(problem.startstate, 0, 0, None), limit, set(), graph, True)

    if not len(dot_string) > 0:
        graph = cs(graph, expc, gen, node if not cutoff else None)

    return path, cutoff, (timer() - t, expc, gen, max_depth), graph, node


def bfs(problem, stype):
    """
    Breadth-first search
    :param problem: problem
    :param stype: type of search: graph or tree (graph_search or tree_search)
    :return: (path, stats, graph): solution as a path and stats
    The stats are a tuple of (time, expc, maxstates): elapsed time, number of expansions, max states in memory
    """
    t = timer()
    path, stats, graph, node = stype(problem, QueueFringe(), lambda n: 0, gen_label, dot_init(problem))
    return path, (timer() - t, stats[0], stats[1], stats[2]), cs(graph, stats[0], stats[1], node)


def ucs(problem, stype):
    """
    Uniform-cost search
    :param problem: problem
    :param stype: type of search: graph or tree (graph_search or tree_search)
    :return: (path, stats): solution as a path and stats
    The stats are a tuple of (time, expc, maxstates): elapsed time, number of expansions, max states in memory
    """

    def g(n, c=None):
        """
        Path cost function
        :param n: node
        :param c: child state of 'n'
        :return: path cost from root to 'c'
        """
        return (n.pathcost + 1) if n is not None else 0

    t = timer()
    path, stats, graph, node = stype(problem, PriorityFringe(), g, gen_label, dot_init(problem))
    return path, (timer() - t, stats[0], stats[1], stats[2]), cs(graph, stats[0], stats[1], node)


def greedy(problem, stype):
    """
    Greedy best-first search
    :param problem: problem
    :param stype: type of search: graph or tree (graph_search or tree_search)
    :return: (path, stats): solution as a path and stats
    The stats are a tuple of (time, expc, maxstates): elapsed time, number of expansions, max states in memory
    """

    def g(n, c=None):
        """
        Path cost function
        :param n: node
        :param c: child state of 'n'
        :return: L1 norm distance value
        """
        return heuristics.l1_norm(problem.state_to_pos(n.state), problem.state_to_pos(problem.goalstate)) \
            if n is not None else 0

    def gl(n, p, exp=False, j=None):
        color = get_color(n.state, p)
        code = gen_code(n)
        label = '{}'.format(n.state) if j is None else '{}  [{}]'.format(n.state, j)

        return '\n{} [label="<f0>{} |<f1> c:{}" style=filled color={} fillcolor={}]' \
            .format(gen_code(n), label, n.pathcost,
                    'black' if exp or problem.goalstate == n.state else 'white', color)

    t = timer()
    path, stats, graph, node = stype(problem, PriorityFringe(), g, gl, dot_init(problem, "record"))
    return path, (timer() - t, stats[0], stats[1], stats[2]), cs(graph, stats[0], stats[1], node)


def astar(problem, stype):
    """
    A* best-first search
    :param problem: problem
    :param stype: type of search: graph or tree (graph_search or tree_search)
    :return: (path, stats): solution as a path and stats
    The stats are a tuple of (time, expc, maxstates): elapsed time, number of expansions, max states in memory
    """

    def f(n, c=None):
        """
        f(n) = g(n) + h(n)
        :param n: node
        :param c: child state of 'n'
        :return: L1 norm distance value
        """
        return n.pathcost + heuristics.l1_norm(problem.state_to_pos(n.state), problem.state_to_pos(problem.goalstate)) \
            if n is not None else 0

    def gl(n, p, exp=False, j=None):
        color = get_color(n.state, p)
        label = '{}'.format(n.state) if j is None else '{}  [{}]'.format(n.state, j)

        return '\n{} [label="<f0>{} |<f1> c:{} |<f2> f: {} ({}+{})", style=filled color={} fillcolor={}]' \
            .format(gen_code(n), label, n.pathcost, f(n, None), n.pathcost,
                    heuristics.l1_norm(p.state_to_pos(n.state), p.state_to_pos(p.goalstate)),
                    'black' if exp or problem.goalstate == n.state else 'white', color)

    t = timer()
    path, stats, graph, node = stype(problem, PriorityFringe(), f, gl, dot_init(problem, "record"))
    return path, (timer() - t, stats[0], stats[1], stats[2]), cs(graph, stats[0], stats[1], node)


def _rdls(problem, node, limit, closed, dot_string='', graph=False, gl=gen_label):
    """
    Recursive depth-limited search (graph search version)
    :param dot_string:
    :param problem: problem
    :param node: node to expand
    :param limit: depth limit budget
    :param closed: completely explored nodes
    :return: (path, cutoff, expc, gen, max_depth): path, cutoff flag, expanded nodes, max depth reached
    """
    dot_string += gl(node, problem)
    exp_nodes, gen, cutoff, depth, depth_max = 0, 0, False, node.pathcost, node.pathcost

    if graph:
        if node.state not in closed:
            closed.add(node.state)
        else:
            return None, False, 0, 0, depth_max, dot_string, None

    if limit == 0:
        return None, True, 1, 0, node.pathcost, dot_string, None
    if problem.goalstate == node.state:
        return build_path(node), False, 1, 0, node.pathcost, dot_string, node

    for action in range(problem.action_space.n):
        child_node = FringeNode(problem.sample(node.state, action), node.pathcost + 1, 0, node)
        dot_string += gen_trans(node, child_node, action, problem, dot_string, gl)
        gen += 1

        if child_node.state not in build_path(node):
            dot_string += gl(node, problem, True)

            result, temp_cutoff, temp_expc, temp_gen, depth, temp_dot_string, temp_node = \
                _rdls(problem, child_node, limit - 1, closed, '', graph, gl)

            gen += temp_gen
            exp_nodes += temp_expc
            dot_string += temp_dot_string
            cutoff = cutoff or temp_cutoff
            depth_max = max(depth, depth_max)

            if result is not None:
                return result, cutoff, exp_nodes, gen, depth_max, dot_string, temp_node

    return None, cutoff, exp_nodes, gen, depth_max, dot_string, None


def tree_search(problem, fringe, f=lambda n, c=None: 0, gl=gen_label, dot_string=''):
    return _search(problem, fringe, f, gl, dot_string, False)


def graph_search(problem, fringe, f=lambda n, c=None: 0, gl=gen_label, dot_string=''):
    return _search(problem, fringe, f, gl, dot_string, True)


def _search(problem, fringe, f=lambda n, c=None: 0, gl=gen_label, dot_string='', graph=True):
    """
    Search (avoid branch repetition)
    :param graph: enable graph search
    :param dot_string:
    :param gl:
    :param problem: problem
    :param fringe: fringe data structure
    :param f: node evaluation function
    :return: (path, stats): solution as a path and stats
    The stats are a tuple of (expc, #gen, maxstates): number of expansions, generated states, max states in memory
    """
    i, j, gen, max_states, closed, root = 0, 0, 1, 0, set(), FringeNode(problem.startstate, 0, 0, None)
    fringe.add(root)
    dot_string += gl(root, problem)

    while j >= 0:
        fringe_size = len(fringe) if not closed else len(fringe) + len(closed)
        max_states = max(max_states, fringe_size)

        if fringe.is_empty():
            return None, [i, gen, max_states], dot_string, None

        node = fringe.remove()
        if node.state == problem.goalstate:
            dot_string += gl(node, problem, True, j)
            return build_path(node), [i, gen, max_states], dot_string, node

        if graph:
            if node.state not in closed:
                closed.add(node.state)
            else:
                continue

        has_exp = False
        for action in range(problem.action_space.n):
            child_node = FringeNode(problem.sample(node.state, action), node.pathcost + 1, f(node), node)
            has_exp = has_exp or True
            gen += 1

            if child_node.state not in build_path(node):
                dot_string += gen_trans(node, child_node, action, problem, dot_string, gl)
                fringe.add(child_node)

        if has_exp:
            dot_string += gl(node, problem, True)
            i += 1


def build_path(node):
    """
    Builds a path going backward from a node
    :param node: node to start from
    :return: path from root to 'node'
    """
    path = []
    while node is not None:  # IMPORTANT the root node must be in the path!
        path.append(node.state)
        node = node.parent
    return tuple(reversed(path))
