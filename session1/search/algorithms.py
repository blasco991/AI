"""
Search algorithms: IDS, BFS, UC, GREEDY, A*
"""

from timeit import default_timer as timer
from datastructures.fringe import *
import matplotlib.pyplot as plt
from search import heuristics
import numpy as np


def print_env(problem):
    return problem.grid.reshape(problem.rows, problem.cols)


def get_color(state, problem):
    color_map = plt.get_cmap('rainbow')
    colors = color_map(np.linspace(0, 1, len(problem.staterange) + 5))
    return '"{}"'.format(str(colors[state])[1:-1])


def close_dot(dot_string, expanded):
    return dot_string + '\n"#{}"\n}}'.format(expanded)


def dot_init(problem, shape='circle', strict=False):
    return "{}digraph {} {{\nnodesep=1\nnode [shape={}]\nedge [arrowsize=0.7]\n/*\n{}\n*/\n" \
        .format('strict ' if strict else '', problem.spec._env_name, shape, print_env(problem))


def gen_code(node):
    return '"' + '.'.join(map(str, build_path(node))) + '"'


def gen_label(child_node, problem, dotted=False):
    color = get_color(child_node.state, problem)

    return '\n{} [label={} style="filled{}", fillcolor={}]' \
        .format(gen_code(child_node), child_node.state, ',dotted' if dotted else '', color)


def gen_trans(node, child_node, action, problem, accumulator, gl):
    state_label = gl(child_node, problem)
    return '{}\n{} -> {} [label="({},{})" ];\n\n' \
        .format('' if state_label in accumulator else state_label,
                gen_code(node), gen_code(child_node),
                problem.actions[action], 1)


def ids(problem, stype):
    """
    Iterative deepening depth-first search
    :param problem: problem
    :param stype: type of search: graph or tree (dls_gs or dls_ts)
    :return: (path, stats): solution as a path and stats
    The stats are a tuple of (time, npexp, maxdepth): elapsed time, number of expansions, max depth reached
    """
    t, depth = timer(), 0
    dot_string = dot_init(problem, strict=True)

    while True:
        solution, cutoff, stats, temp_dot_string = stype(problem, depth)
        depth += 1
        dot_string += temp_dot_string
        if not cutoff:
            return solution, (timer() - t, stats[1], stats[2]), close_dot(dot_string, stats[1])


def dls_ts(problem, limit):
    """
    Depth-limited search (tree search)
    :param problem: problem
    :param limit: depth limit budget
    :return: (path, cutoff, stats): solution as a path, cutoff flag and stats
    The stats are a tuple of (time, npexp, maxdepth): elapsed time, number of expansions, max depth reached
    """
    t = timer()
    path, cutoff, expc, maxdepth, dot_string = \
        rdls_ts(problem, FringeNode(problem.startstate, 0, 0, None), limit)
    return path, cutoff, (timer() - t, expc, maxdepth), dot_string


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
    path, cutoff, expc, maxdepth, dot_string = \
        rdls_gs(problem, FringeNode(problem.startstate, 0, 0, None), limit, closed, '')
    return path, cutoff, (timer() - t, expc, maxdepth), dot_string


def rdls_ts(problem, node, limit, dot_string=""):
    """
    Recursive depth-limited search (tree search version) (avoid branch repetition)
    :param dot_string:
    :param problem: problem
    :param node: node to expand
    :param limit: depth limit budget
    :return: (path, cutoff, expc, maxdepth): path, cutoff flag, expanded nodes, max depth reached
    """
    # dot_string += gen_label(node, problem)

    if problem.goalstate == node.state:
        return build_path(node), False, 0, node.pathcost, dot_string
    if limit == 0:
        return None, True, 0, node.pathcost, dot_string

    exp_nodes, cutoff = 1, False
    depth = 1
    depth_max = 0

    dot_string += gen_label(node, problem, True)
    for action in range(problem.action_space.n):
        child_state = problem.sample(node.state, action)
        if child_state not in build_path(node):
            child_node = FringeNode(child_state, node.pathcost + 1, 0, node)
            dot_string += gen_trans(node, child_node, action, problem, dot_string, gen_label)
            result, cutoff, temp_expc, depth_max, temp_dot_string = rdls_ts(problem, child_node, limit - 1)
            dot_string += temp_dot_string
            depth = depth_max if depth_max > depth else depth
            exp_nodes += temp_expc

            if result is not None:
                return result, False, exp_nodes, depth, dot_string

    if cutoff:
        return None, True, exp_nodes, depth_max, dot_string

    return None, False, exp_nodes, node.pathcost, dot_string


def rdls_gs(problem, node, limit, closed, dot_string=""):
    """
    Recursive depth-limited search (graph search version)
    :param dot_string:
    :param problem: problem
    :param node: node to expand
    :param limit: depth limit budget
    :param closed: completely explored nodes
    :return: (path, cutoff, expc, maxdepth): path, cutoff flag, expanded nodes, max depth reached
    """
    dot_string += gen_label(node, problem)

    if problem.goalstate == node.state:
        return build_path(node), False, 0, node.pathcost, dot_string
    if limit == 0:
        return None, True, 0, node.pathcost, dot_string

    exp_nodes, cutoff = 1, False
    depth = 0

    if node.state not in closed:
        closed.add(node.state)
        dot_string += gen_label(node, problem, True)
        for action in range(problem.action_space.n):
            child_node = FringeNode(problem.sample(node.state, action), node.pathcost + 1, 0, node)
            dot_string += gen_trans(node, child_node, action, problem, dot_string, gen_label)
            result, temp_cutoff, temp_exp_nodes, depth_max, temp_dot_string = \
                rdls_gs(problem, child_node, limit - 1, closed)

            dot_string += temp_dot_string
            depth = depth_max if depth_max > depth else depth
            exp_nodes += temp_exp_nodes
            cutoff = cutoff or temp_cutoff

            if result is not None:
                return result, cutoff, exp_nodes, depth, dot_string

        if cutoff:
            return None, True, exp_nodes, depth, dot_string

    return None, False, exp_nodes, depth, dot_string


def bfs(problem, stype):
    """
    Breadth-first search
    :param problem: problem
    :param stype: type of search: graph or tree (graph_search or tree_search)
    :return: (path, stats, graph): solution as a path and stats
    The stats are a tuple of (time, expc, maxstates): elapsed time, number of expansions, max states in memory
    """
    t = timer()
    path, stats, graph = stype(problem, QueueFringe(), lambda n, c: 0, gen_label, gen_trans, dot_init(problem))
    return path, (timer() - t, stats[0], stats[1]), graph


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
        return (n.pathcost + 1) if n is not None else 0

    dot_string = dot_init(problem)
    t = timer()
    path, stats, dot_string = stype(problem, PriorityFringe(), g, gen_label, gen_trans, dot_string)
    return path, (timer() - t, stats[0], stats[1]), dot_string


def greedy(problem, stype):
    """
    Greedy best-first search
    :param problem: problem
    :param stype: type of search: graph or tree (graph_search or tree_search)
    :return: (path, stats): solution as a path and stats
    The stats are a tuple of (time, expc, maxstates): elapsed time, number of expansions, max states in memory
    """

    def g(n, c):
        """
        Path cost function
        :param n: node
        :param c:
        :return: L1 norm distance value
        """
        return heuristics.l1_norm(problem.state_to_pos(n.state), problem.state_to_pos(problem.goalstate)) \
            if n is not None else 0

    def gl(node, p, dotted=False):
        color = get_color(node.state, problem)

        return '\n{} [label="<f0>{} |<f1> c:{}" style="filled{}", fillcolor={}]' \
            .format(gen_code(node), node.state, node.pathcost, ',dotted' if dotted else '', color)

    def gt(node, child_node, action, problem, accumulator, gl):
        state_label = gl(child_node, problem)
        return '{}{} -> {} [label="({},{})" ];\n\n' \
            .format('' if state_label in accumulator else state_label,
                    gen_code(node), gen_code(child_node),
                    problem.actions[action], 1)

    dot_string = dot_init(problem, "record")
    t = timer()
    path, stats, graph = stype(problem, PriorityFringe(), g, gl, gt, dot_string)
    return path, (timer() - t, stats[0], stats[1]), graph


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
        return n.pathcost + heuristics.l1_norm(problem.state_to_pos(n.state),
                                               problem.state_to_pos(problem.goalstate)) \
            if n is not None else 0

    def gl(node, p, dotted=False):
        color = get_color(node.state, problem)

        return '\n{} [label="<f0>{} |<f1> c:{} |<f2> f: {} ({}+{})", style="filled{}", fillcolor={}]' \
            .format(gen_code(node), node.state, node.pathcost,
                    f(node, None), node.pathcost,
                    heuristics.l1_norm(p.state_to_pos(node.state), p.state_to_pos(p.goalstate)),
                    ',dotted' if dotted else '', color)

    def gt(node, child_node, action, problem, accumulator, gl):
        state_label = gl(child_node, problem)
        return '{}{} -> {} [label="({},{})" ];\n\n' \
            .format('' if state_label in accumulator else state_label,
                    gen_code(node), gen_code(child_node),
                    problem.actions[action], 1)

    dot_string = dot_init(problem, "record")
    t = timer()
    path, stats, graph = stype(problem, PriorityFringe(), f, gl, gt, dot_string)
    return path, (timer() - t, stats[0], stats[1]), graph


def graph_search(problem, fringe, f=lambda n, c: 0, gl=gen_label, gt=gen_trans, dot_string=''):
    """
    Graph search (avoid branch repetition)
    :param dot_string:
    :param gt:
    :param gl:
    :param problem: problem
    :param fringe: fringe data structure
    :param f: node evaluation function
    :return: (path, stats): solution as a path and stats
    The stats are a tuple of (expc, maxstates): number of expansions, max states in memory
    """
    closed = set()
    i, max_states = 1, 0
    root = FringeNode(problem.startstate, 0, 0, None)
    fringe.add(root)
    dot_string += gl(root, problem)

    while i > 0:
        tmp = len(fringe) + len(closed)
        max_states = tmp if tmp > max_states else max_states

        if fringe.is_empty():
            return None, [i, max_states], close_dot(dot_string, max_states)

        node = fringe.remove()
        if node.state == problem.goalstate:
            return build_path(node), [i, max_states], close_dot(dot_string, max_states)

        if node.state not in closed:
            closed.add(node.state)
            temp_size = len(fringe)
            for action in range(problem.action_space.n):
                child_state = problem.sample(node.state, action)
                if child_state not in build_path(node):
                    child_node = FringeNode(child_state, node.pathcost + 1, f(node, child_state), node)
                    dot_string += gt(node, child_node, action, problem, dot_string, gl)

                    if child_state not in fringe and child_state not in closed:
                        fringe.add(child_node)
                        dot_string += gl(node, problem, True)

            if len(fringe) > temp_size:
                dot_string += gl(node, problem, True)
                i += 1


def tree_search(problem, fringe, f=lambda n, c: 0, gl=gen_label, gt=gen_trans, dot_string=''):
    """
    Tree search
    :param dot_string:
    :param gt:
    :param gl:
    :param problem: problem
    :param fringe: fringe data structure
    :param f: node evaluation function
    :return: (path, stats): solution as a path and stats
    The stats are a tuple of (expc, maxstates): number of expansions, max states in memory
    """
    i, max_states = 0, 0
    root = FringeNode(problem.startstate, 0, 0, None)
    fringe.add(root)
    dot_string += gl(root, problem)

    while True:

        if fringe.is_empty():
            return None, [i, max_states], close_dot(dot_string, i)

        node = fringe.remove()
        if node.state == problem.goalstate:
            return build_path(node), [i, max_states], close_dot(dot_string, i)

        temp_size = len(fringe)
        for action in range(problem.action_space.n):
            child_state = problem.sample(node.state, action)
            child_node = FringeNode(child_state, node.pathcost + 1, f(node, child_state), node)
            if child_state not in build_path(node) and child_state not in fringe:
                fringe.add(child_node)
                dot_string += gl(node, problem, True)

            dot_string += gt(node, child_node, action, problem, dot_string, gl)

        if len(fringe) > temp_size:
            dot_string += gl(node, problem, True)
            i += 1

        max_states = len(fringe) if len(fringe) > max_states else max_states


def tree_search_plus(problem, fringe, f=lambda n, c: 0, gl=gen_label, gt=gen_trans, dot_string=''):
    """
    Tree search (avoid branch repetition)
    :param dot_string:
    :param gt:
    :param gl:
    :param problem: problem
    :param fringe: fringe data structure
    :param f: node evaluation function
    :return: (path, stats): solution as a path and stats
    The stats are a tuple of (expc, maxstates): number of expansions, max states in memory
    """
    i, max_states = 0, 0
    root = FringeNode(problem.startstate, 0, 0, None)
    fringe.add(root)
    dot_string += gl(root, problem)

    while True:

        if fringe.is_empty():
            return None, [i, max_states], close_dot(dot_string, i)

        node = fringe.remove()
        dot_string += gl(node, problem, True)
        if node.state == problem.goalstate:
            return build_path(node), [i, max_states], close_dot(dot_string, i)

        temp_size = len(fringe)
        for action in range(problem.action_space.n):
            child_state = problem.sample(node.state, action)
            if child_state not in build_path(node):
                child_node = FringeNode(child_state, node.pathcost + 1, f(node, child_state), node)
                if child_state not in fringe:
                    fringe.add(child_node)
                    dot_string += gt(node, child_node, action, problem, dot_string, gl)

        if len(fringe) > temp_size:
            dot_string += gl(node, problem, True)
            i += 1

        max_states = len(fringe) if len(fringe) > max_states else max_states


def build_path(node):
    """
    Builds a path going backward from a node
    :param node: node to start from
    :return: path from root to 'node'
    """
    path = []
    while node is not None:
        path.append(node.state)
        node = node.parent
    return tuple(reversed(path))
