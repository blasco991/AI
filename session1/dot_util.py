import os
import pathlib
import shutil
import sys
import subprocess
import numpy as np
import matplotlib.pyplot as plt

from datastructures import fringe
from datastructures.fringe import gen, enable_graph
from search import heuristics as h

sys.setrecursionlimit(10000)
color_map = plt.get_cmap('rainbow')
colors = None
sub_c = 0


def handle_path(path):
    for folder in ["dot", "png"]:
        shutil.rmtree(path + "/" + folder, ignore_errors=True)
        pathlib.Path(path + "/" + folder).mkdir(parents=True, exist_ok=True)


def _env_to_str(problem):
    return '/*\n{}\n*/\n'.format(problem.grid.reshape(problem.rows, problem.cols))


def _env_to_html(problem):
    html = str()
    i = 0
    for row in problem.grid.reshape(problem.rows, problem.cols):
        html += "<tr>"
        for element in row:
            html += "<td bgcolor={}>{}:{}</td>".format(_get_color(i), element, i)
            i += 1
        html += "</tr>"
    return html


def dot_init(problem, shape='circle', sub=False, cluster=0):
    global colors, sub_c
    sub_c = str(cluster) + "_"
    colors = color_map(np.linspace(0, 1, len(problem.staterange) * 2))
    html_table = '\nsubgraph MAP {label=Map;map [shape=plaintext label=<<table' \
                 ' border="1" cellpadding="5" cellspacing="0" cellborder="1">' + _env_to_html(problem) + '</table>>]}'

    return '{} {{ label="{}" {} {} ' \
        .format('digraph {}'.format(problem.spec._env_name) if not sub else '\nsubgraph cluster{}'.format(cluster),
                'Limit: {}'.format(cluster) if sub else problem.spec.id,
                'nodesep=1 ranksep="1.2" node [shape=' + shape + ' penwidth=2] edge [arrowsize=0.7]' if not sub else '',
                html_table if not sub else ' ')


def _get_color(state):
    # return '"{}"'.format("#" + str(matplotlib.colors.rgb2hex(colors[state + 2])[1:-1]))
    return '"{}"'.format(str(colors[state + 2])[1:-1])


def close_dot(expanded, s_node=None, dot=None, sub=False):
    dot_string = fringe.dot() if dot is None else dot
    if s_node is not None and dot is None:
        temp = str()
        for line in dot_string.splitlines():
            if line.strip().startswith(tuple(map(gen_code, _build_path_n(s_node)))):
                line = line.replace('color=black', 'color=black color=red')
            if any(nodepath in line.strip()
                   for nodepath in (tuple(map(lambda s: '-> ' + s, map(gen_code, _build_path_n(s_node)))))):
                line = line.replace('color=grey', 'color=grey color=red')
            temp += line + "\n"
        dot_string = temp[:-2]

    return dot_string \
           + ('{}"#exp {}, #gen {}{}" [ shape=box ]; }}'
              .format(' ' if sub else '\n', expanded, gen(),
                      ', cost:{}'.format(s_node.pathcost) if s_node is not None else '') if dot is None else '\n}') \
        if fringe.enable_graph else ''


def gen_code(node):
    return '"' + str(sub_c) + '.'.join(map(lambda n: str(n.state), _build_path_n(node))) + '{}"' \
        .format('-' + str(node.cause) if node.cause is not None else '')


def gen_label(n, p, exp=False):
    color = _get_color(n.state)

    return '{} [label="{}" style=filled color={} fillcolor={} {}];' \
        .format(gen_code(n), n.state, 'black' if exp or n.state == p.goalstate else 'grey', color,
                'peripheries=2 /*GOALSTATE*/' if p.goalstate == n.state else '')


def gl_greedy(n, p, exp=False, j=None):
    label = '{}'.format(n.state) if j is None else '{}  [{}]'.format(n.state, j)
    return '{} [label="<f0>{} |<f1> cost: {}" style=filled color={} fillcolor={}]; {} ' \
        .format(gen_code(n), label, n.pathcost,
                'black' if exp or p.goalstate == n.state else 'grey', _get_color(n.state),
                '/*GOALSTATE*/' if p.goalstate == n.state else '')


def gl_astar(n, p, exp=False, j=None):
    def f(_n):
        return h.l1_norm(p.state_to_pos(_n.state), p.state_to_pos(p.goalstate)) + _n.pathcost

    label = '{}'.format(n.state) if j is None else '{}  [{}]'.format(n.state, j)
    return '{} [label="<f0>{} |<f1> cost: {} |<f2> f: {} ({}+{})", style=filled color={} fillcolor={}]; {} ' \
        .format(gen_code(n), label, n.pathcost, f(n), n.pathcost,
                h.l1_norm(p.state_to_pos(n.state), p.state_to_pos(p.goalstate)),
                'black' if exp or p.goalstate == n.state else 'grey', _get_color(n.state),
                '/*GOALSTATE*/' if p.goalstate == n.state else '')


def gen_trans(node, child_node, problem, gl, accumulator, j=None, fringe=None, closed=None, style=''):
    state_label = gl(node, problem, True)
    child_state_label = gl(child_node, problem)
    return '\n{}{} {} -> {} [label="({},{})" headlabel=" {} " style="{}" color=grey ]; {} {}' \
        .format(state_label if state_label not in accumulator else '',
                child_state_label,
                gen_code(node), gen_code(child_node), problem.actions[child_node.cause],
                child_node.pathcost - node.pathcost, j if j is not None else '', style,
                '{}'.format('"{}c" [label="Closed: {}" shape=box];'.format(sub_c, closed)
                            if not isinstance(closed, frozenset) else ''),
                '{}'.format('"{}fr" [label="Fringe: {}" shape=box];'
                            .format(sub_c, list(map(lambda n: str(n), fringe.frdict))) if fringe is not None else '')
                )


def _build_path_n(node):
    """
    Builds a path going backward from a node
    :param node: node to start from
    :return: path from root to 'node'
    """
    path = []
    while node is not None:
        path.append(node)
        node = node.parent
    return reversed(path)


def compile_dot_files(path):
    if enable_graph:
        print('\nCompiling DOT file to PNG')
        for filename in os.listdir('{}/dot'.format(path)):
            subprocess.run(
                ["dot", "{}/dot/{}".format(path, filename), "-Tpng", "-o{}/png/{}.png".format(path, filename)])
        print("\nGenerated dot files in:\t{}".format(path))
