import gym
import pathlib
import gym_ai_lab
import search.algorithms as search
from dot_util import compile_dot_files, close_dot

path = "../viz/artifacts/tsd"
for folder in ["dot", "md", "png"]:
    pathlib.Path(path + "/" + folder).mkdir(parents=True, exist_ok=True)

envs = ["XSMaze-v0", "SmallMaze-v0", "GrdMaze-v0", "BlockedMaze-v0", "CompMaze-v0", "BigMaze-v0"]
# envs = ["SmallMaze-v0", "GrdMaze-v0", "BlockedMaze-v0"]

# "dfs": search.dls_ts,  "ucs": search.tree_search,
algs = {"dfs": search.tree_search, "ids": search.tree_search, "bfs": search.tree_search,
        "greedy": search.tree_search, "astar": search.tree_search}

for env_name in envs:
    print("\n----------------------------------------------------------------")
    print("\tTREE SEARCH")
    print("\tEnvironment: ", env_name)
    print("----------------------------------------------------------------\n")

    env = gym.make(env_name)
    env.render()

    for (alg, method) in algs.items():

        solution, stats, graph = getattr(search, alg)(env, method, False, True)
        if solution is not None:
            solution = [env.state_to_pos(s) for s in solution]

        print("\n\n{0}:\n----------------------------------------------------------------"
              "\nExecution time: {1}s"
              "\nN° of states expanded: {2}"
              # "\nN° of states generated: {3}"
              "\nMax n° of states in memory: {4}"
              "\nSolution: {5}"
              .format(alg.upper(), round(stats[0], 4), stats[1], stats[2], stats[3], solution))

        with open("{}/md/{}_{}.md".format(path, env_name, alg), "w") as text_file:
            print("```plantuml\n{}```".format(graph), file=text_file)

        with open("{}/dot/{}_{}.dot".format(path, env_name, alg), "w") as text_file:
            print(graph, file=text_file)

compile_dot_files(path)