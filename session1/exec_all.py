import os
import gym
import subprocess
import gym_ai_lab
import search.algorithms as search

for stg in ["ts", "tsp", "gs"]:

    path = 'artifacts/{}'.format(stg)
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
        if stg != 'tsp':
            # IDS
            solution, stats, graph = search.ids(env, getattr(search, "dls_{}".format(stg)))
            if solution is not None:
                solution = [env.state_to_pos(s) for s in solution]
            print("\n\nIDS:\n----------------------------------------------------------------"
                  "\nExecution time: {0}s\nN° of states expanded: {1}\nMax n° of states in memory: {2}\nSolution: {3}"
                  .format(round(stats[0], 4), stats[1], stats[2], solution))
            with open("{}/md/{}_{}.md".format(path, envname, "ids"), "w") as text_file:
                print("```plantuml\n{}```".format(graph), file=text_file)
            with open("{}/dot/{}_{}.dot".format(path, envname, "ids"), "w") as text_file:
                print(graph, file=text_file)

        for alg in ["bfs", "ucs", "greedy", "astar"]:
            solution, stats, graph = getattr(search, alg)(env, search.tree_search)
            if solution is not None:
                solution = [env.state_to_pos(s) for s in solution]
            print("\n\n{}:\n----------------------------------------------------------------"
                  "\nExecution time: {}s\nN° of states expanded: {}\nMax n° of states in memory: {}\nSolution: {}"
                  .format(alg.upper(), round(stats[0], 4), stats[1], stats[2], solution))
            with open("{}/md/{}_{}.md".format(path, envname, alg), "w") as text_file:
                print("```plantuml\n{}```".format(graph), file=text_file)
            with open("{}/dot/{}_{}.dot".format(path, envname, alg), "w") as text_file:
                print(graph, file=text_file)

    for filename in os.listdir('{}/dot'.format(path)):
        p = subprocess.Popen(
            ["dot", "{}/dot/{}".format(path, filename), "-Tpng",
             "-o{}/png/{}.png".format(path, filename)])
        print("Generated:\t" + "{}/png/{}.png".format(path, filename))
