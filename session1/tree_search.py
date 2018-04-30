import os
import subprocess

import gym
import gym_ai_lab
from urllib.parse import quote
import search.algorithms as search

envs = ["SmallMaze-v0", "GrdMaze-v0", "BlockedMaze-v0"]

for envname in envs:
    print("\n----------------------------------------------------------------")
    print("\tTREE SEARCH")
    print("\tEnvironment: ", envname)
    print("----------------------------------------------------------------\n")

    env = gym.make(envname)
    env.render()

    """"# DFS
    solution, _, stats = search.dls_ts(env, )
    print("\n\nDFS:\n----------------------------------------------------------------"
          "\nExecution time: {0}s\nN° of states expanded: {1}\nMax n° of states in memory: {2}\nSolution: {3}"
          .format(round(stats[0], 4), stats[1], stats[2], solution))
    """
    # IDS
    solution, stats, graph = search.ids(env, search.dls_ts)
    if solution is not None:
        solution = [env.state_to_pos(s) for s in solution]
    print("\n\nIDS:\n----------------------------------------------------------------"
          "\nExecution time: {0}s\nN° of states expanded: {1}\nMax n° of states in memory: {2}\nSolution: {3}"
          .format(round(stats[0], 4), stats[1], stats[2], solution))
    with open("artifacts/ts/{}_{}.md".format("ids", envname), "w") as text_file:
        print("```plantuml\n{}```".format(graph), file=text_file)
    with open("artifacts/ts/dot/{}_{}.dot".format("ids", envname), "w") as text_file:
        print(graph, file=text_file)

    for alg in ["bfs", "ucs", "greedy", "astar"]:
        solution, stats, graph = getattr(search, alg)(env, search.tree_search)
        if solution is not None:
            solution = [env.state_to_pos(s) for s in solution]
        print("\n\n{}:\n----------------------------------------------------------------"
              "\nExecution time: {}s\nN° of states expanded: {}\nMax n° of states in memory: {}\nSolution: {}"
              .format(alg.upper(), round(stats[0], 4), stats[1], stats[2], solution))
        with open("artifacts/ts/{}_{}.md".format(alg, envname), "w") as text_file:
            print("```plantuml\n{}```".format(graph), file=text_file)
        with open("artifacts/ts/dot/{}_{}.dot".format(alg, envname), "w") as text_file:
            print(graph, file=text_file)

print()
for filename in os.listdir('artifacts/ts/dot'):
    p = subprocess.Popen(["/usr/local/bin/dot",
                          "artifacts/ts/dot/{}".format(filename), "-Tpng",
                          "-oartifacts/ts/png/{}.png".format(filename)])
    print("Generated:\t" + "artifacts/ts/png/{}.png".format(filename))
