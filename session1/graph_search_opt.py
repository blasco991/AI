import gym
import gym_ai_lab
import search.algorithms as search
from dot_util import compile_dot_files, close_dot

path = "artifacts/gs"
# envs = ["XSMaze-v0", "SmallMaze-v0", "GrdMaze-v0", "BlockedMaze-v0", "CompMaze-v0", "BigMaze-v0"]
envs = ["SmallMaze-v0", "GrdMaze-v0", "BlockedMaze-v0"]

algs = {"dfs": search.dls_gs, "ids": search.dls_gs, "bfs": search.graph_search, "ucs": search.graph_search,
        "greedy": search.graph_search, "astar": search.graph_search}

for env_name in envs:
    print("\n----------------------------------------------------------------")
    print("\tGRAPH SEARCH")
    print("\tEnvironment: ", env_name)
    print("----------------------------------------------------------------\n")

    env = gym.make(env_name)
    env.render()

    for (alg, method) in algs.items():

        solution, stats, graph = getattr(search, alg)(env, method, True)
        if solution is not None:
            solution = [env.state_to_pos(s) for s in solution]

        print("\n{}:\n----------------------------------------------------------------"
              "\nExecution time: {}s"
              "\nN° of states expanded (subject to expansion): {}"
              "\nN° of states generated: {}"
              "\nMax n° of states in memory: {}"
              "\nSolution: {}"
              .format(alg.upper(), round(stats[0], 4), stats[1], stats[2], stats[3], solution))

        with open("{}/md/{}_{}.md".format(path, env_name, alg), "w") as text_file:
            print("```plantuml\n{}```".format(graph), file=text_file)

        with open("{}/dot/{}_{}.dot".format(path, env_name, alg), "w") as text_file:
            print(graph, file=text_file)

compile_dot_files(path)