import gym
import shutil
import pathlib
import search.algorithms as search
from dot_util import compile_dot_files, handle_path

path = "../viz/artifacts/tsd"
handle_path(path)

envs = ["XSMaze-v0", "SmallMaze-v0", "GrdMaze-v0", "BlockedMaze-v0", "CompMaze-v0", "BigMaze-v0"]

algs = {"dfs": search.tree_search, "r_dfs": search.dls_ts,
        # "r_ids": search.dls_ts, "ids": search.tree_search,
        # "bfs": search.tree_search,
        # "ucs": search.tree_search,
        "greedy": search.tree_search,
        "astar": search.tree_search}

for i, env_name in enumerate(envs):
    print("\n----------------------------------------------------------------")
    print("\tTREE SEARCH AVOID BRANCH TREE REPETITION")
    print("\tEnvironment: ", env_name)
    print("----------------------------------------------------------------\n")

    env = gym.make(env_name)
    env.render()

    for j, (alg, method) in enumerate(algs.items()):

        solution, stats, graph = getattr(search, alg)(env, method, False, True)
        if solution is not None:
            solution = [env.state_to_pos(s) for s in solution]

        print("\n\n{0}:\n----------------------------------------------------------------"
              "\nExecution time: {1}s"
              "\nN° of states expanded: {2}"
              "\nN° of states generated: {3}"
              "\nMax n° of states in memory: {4}"
              "\nSolution: {5}"
              .format(alg.upper(), round(stats[0], 4), stats[1], stats[2], stats[3], solution))

        with open("{}/dot/{}-{}_{}-{}.dot".format(path, i, env_name, j, alg), "w") as text_file:
            print(graph, file=text_file)

# compile_dot_files(path)
