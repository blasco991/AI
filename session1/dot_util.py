import os
import subprocess

import matplotlib.pyplot as plt
import numpy as np


def env_to_str(problem):
    return problem.grid.reshape(problem.rows, problem.cols)


def env_to_html(problem):
    html = str()
    for row in problem.grid.reshape(problem.rows, problem.cols):
        html += "<tr>"
        for element in row:
            html += "<td>{}</td>".format(element)
        html += "</tr>"
    return html


def dot_init(problem, shape='circle', strict=False):
    html_table = '\n\nsubgraph MAP {\nlabel=Map;\nmap [shape=plaintext label=<\
    <table border="1" cellpadding="5" cellspacing="0" cellborder="1">\n' + env_to_html(problem) + '\n</table>>]}\n'

    return "{}digraph {} {{{}\nnodesep=1 ranksep=0.5\nnode [shape={}]\nedge [arrowsize=0.7]\n/*\n{}\n*/\n" \
        .format('strict ' if strict else '', problem.spec._env_name, html_table, shape, env_to_str(problem))


def get_color(state, problem):
    color_map = plt.get_cmap('rainbow')
    colors = color_map(np.linspace(0, 1, len(problem.staterange) * 2))
    return '"{}"'.format(str(colors[state + 2])[1:-1])


def close_dot(dot_string, expanded, node=None):
    if node is not None:
        temp = str()
        for line in dot_string.splitlines():
            if line.strip().startswith(tuple(map(gen_code, build_path_n(node)))):
                line = line.replace('color=black', 'color=red')
            if any(nodepath in line.strip()
                   for nodepath in (tuple(map(lambda s: '-> ' + s, map(gen_code, build_path_n(node)))))):
                line = line.replace('];', 'color=red ];')
            temp += line + "\n"
        dot_string = temp
    return dot_string + '\n"#{}"\n}}'.format(expanded)


def gen_code(node):
    from search.algorithms import build_path
    return '"' + '.'.join(map(str, build_path(node))) + '"'


def gen_label(node, problem, exp=False):
    color = get_color(node.state, problem)

    return '\n{} [label={} style=filled color={} {} fillcolor={}]' \
        .format(gen_code(node), node.state,
                'black' if exp or problem.goalstate == node.state else 'white',
                'peripheries=2' if problem.goalstate == node.state else '', color)


def gen_trans(node, child_node, action, problem, accumulator, gl):
    state_label = gl(child_node, problem)
    return '{}\n{} -> {} [label="({},{})" ];\n\n' \
        .format('' if state_label in accumulator else state_label,
                gen_code(node), gen_code(child_node),
                problem.actions[action], 1)


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
    return tuple(reversed(path))


def compile_dot_files(path):
    for filename in os.listdir('{}/dot'.format(path)):
        subprocess.run(
            ["dot", "{}/dot/{}".format(path, filename), "-Tpng",
             "-o{}/png/{}.png".format(path, filename)])
    print("\n\nGenerated dot files in:\t{}".format(path))