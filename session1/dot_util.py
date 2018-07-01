import os
import sys
import gym.spaces
import subprocess
import numpy as np
import matplotlib.pyplot as plt

from search import heuristics as h

sys.setrecursionlimit(10000)
color_map = plt.get_cmap('rainbow')
colors = None
sub_c = 0


def env_to_str(problem):
    return '/*\n{}\n*/\n'.format(problem.grid.reshape(problem.rows, problem.cols))


def env_to_html(problem):
    html = str()
    i = 0
    for row in problem.grid.reshape(problem.rows, problem.cols):
        html += "<tr>"
        for element in row:
            html += "<td bgcolor={}>{}:{}</td>".format(get_color(i), element, i)
            i += 1
        html += "</tr>"
    return html


def dot_init(problem, shape='circle', sub=False, cluster=0):
    global colors, sub_c
    sub_c = str(cluster) + "_"
    colors = color_map(np.linspace(0, 1, len(problem.staterange) * 2))
    html_table = '\nsubgraph MAP {label=Map;map [shape=plaintext label=<<table' \
                 ' border="1" cellpadding="5" cellspacing="0" cellborder="1">' + env_to_html(problem) + '</table>>]}'

    return '{} {{ label="{}" {} {} ' \
        .format('digraph {}'.format(problem.spec._env_name) if not sub else '\nsubgraph cluster{}'.format(cluster),
                'Limit: {}'.format(cluster) if sub else problem.spec.id,
                'nodesep=1 ranksep="1.2" node [shape=' + shape + '] edge [arrowsize=0.7]' if not sub else '',
                html_table if not sub else ' ')


def get_color(state):
    # return '"{}"'.format("#" + str(matplotlib.colors.rgb2hex(colors[state + 2])[1:-1]))
    return '"{}"'.format(str(colors[state + 2])[1:-1])


def close_dot(expanded, nodes=None, dot=None, sub=False):
    root, s_node = nodes[0], nodes[1]
    dot_string = root.dot() if dot is None else dot
    if s_node is not None and dot is None:
        temp = str()
        for line in dot_string.splitlines():
            if line.strip().startswith(tuple(map(gen_code, build_path_n(s_node)))):
                line = line.replace('color=black', 'color=black color=red')
            if any(nodepath in line.strip()
                   for nodepath in (tuple(map(lambda s: '-> ' + s, map(gen_code, build_path_n(s_node)))))):
                line = line.replace('color=grey', 'color=grey color=red')
            temp += line + "\n"
        dot_string = temp[:-2]

    return root.gen(), dot_string \
           + ('{}"#exp {}, #gen {}{}" [ shape=box ]; }}'
              .format(' ' if sub else '\n', expanded, root.gen(),
                      ', cost:{}'.format(s_node.pathcost) if s_node is not None else '')
              if dot is None else '\n}')


def gen_code(node):
    return '"' + str(sub_c) + '.'.join(map(lambda n: str(n.state), build_path_n(node))) + '{}"' \
        .format('-' + str(node.cause) if node.cause is not None else '')
    """return '"' + str(0) + '.'.join(map(lambda n: str(n.state), build_path_n(node))) + '{}"' \
        .format('-' + str(node.cause) if node.cause is not None else '')"""


def gen_label(n, p, exp=False, j=None):
    color = get_color(n.state)

    return '{} [label={} style=filled color={} fillcolor={} {}]; {} ' \
        .format(gen_code(n), '" ' + str(n.state) + ' "' if exp or p.goalstate == n.state else n.state,
                'black' if exp or n.state == p.goalstate else 'grey', color,
                'peripheries=2' if p.goalstate == n.state else '',
                '/*GOALSTATE*/' if p.goalstate == n.state else '')


def gl_greedy(n, p, exp=False, j=None):
    label = '{}'.format(n.state) if j is None else '{}  [{}]'.format(n.state, j)
    return '{} [label="<f0>{} |<f1> cost: {}" style=filled color={} fillcolor={}]; {} ' \
        .format(gen_code(n), label, n.pathcost,
                'black' if exp or p.goalstate == n.state else 'grey', get_color(n.state),
                '/*GOALSTATE*/' if p.goalstate == n.state else '')


def gl_astar(n, p, exp=False, j=None):
    def f(c=None):
        return h.l1_norm(p.state_to_pos(c), p.state_to_pos(int(p.goalstate))) + n.pathcost + 1

    label = '{}'.format(n.state) if j is None else '{}  [{}]'.format(n.state, j)
    return '{} [label="<f0>{} |<f1> cost: {} |<f2> f: {} ({}+{})", style=filled color={} fillcolor={}]; {} ' \
        .format(gen_code(n), label, n.pathcost, f(n.state),
                n.parent.pathcost if n.parent is not None else 0,
                h.l1_norm(p.state_to_pos(n.state), p.state_to_pos(p.goalstate)),
                'black' if exp or p.goalstate == n.state else 'grey', get_color(n.state),
                '/*GOALSTATE*/' if p.goalstate == n.state else '')


def gen_trans(node, child_node, problem, gl, accumulator, j=None):
    state_label = gl(node, problem, True)
    child_state_label = gl(child_node, problem)
    return '\n{}{} {} -> {} [label="({},{})" headlabel=" {} " color=grey ]; ' \
        .format(state_label if state_label not in accumulator else '',
                child_state_label if child_state_label not in accumulator else '',
                gen_code(node), gen_code(child_node), problem.actions[child_node.cause],
                child_node.pathcost - node.pathcost, j if j is not None else '')


def build_path_n(node):
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
    print('\nCompiling DOT file to PNG')
    for filename in os.listdir('{}/dot'.format(path)):
        subprocess.run(["dot", "{}/dot/{}".format(path, filename), "-Tpng", "-o{}/png/{}.png".format(path, filename)])
    print("\nGenerated dot files in:\t{}".format(path))
