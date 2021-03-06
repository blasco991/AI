import gym
import search.algorithms as search

# path = "artifacts/ts"
# envs = ["XSMaze-v0", "SmallMaze-v0", "GrdMaze-v0", "BlockedMaze-v0", "CompMaze-v0", "BigMaze-v0"]
envs = ["SmallMaze-v0", "GrdMaze-v0"]  # , "BlockedMaze-v0"]

algs = {"r_ids": search.dls_ts, "ids": search.tree_search}

for i, env_name in enumerate(envs):
    print("\n----------------------------------------------------------------")
    print("\tTREE SEARCH")
    print("\tEnvironment: ", env_name)
    print("----------------------------------------------------------------\n")

    env = gym.make(env_name)
    env.render()

    for (alg, method) in algs.items():

        solution, stats, graph = getattr(search, alg)(env, method, opt=False, avd=True)
        if solution is not None:
            solution = [env.state_to_pos(s) for s in solution]

        print("\n\n{0}:\n----------------------------------------------------------------"
              "\nExecution time: {1}s"
              "\nN° of states expanded: {2}"
              "\nN° of states generated: {3}"
              "\nMax n° of states in memory: {4}"
              "\nSolution: {5}"
              .format(alg.upper(), round(stats[0], 4), stats[1], stats[2], stats[3], solution))


algs = {"r_ids": search.dls_gs, "ids": search.graph_search}

for i, env_name in enumerate(envs):
    print("\n----------------------------------------------------------------")
    print("\tTREE SEARCH")
    print("\tEnvironment: ", env_name)
    print("----------------------------------------------------------------\n")

    env = gym.make(env_name)
    env.render()

    for (alg, method) in algs.items():

        solution, stats, graph = getattr(search, alg)(env, method, False)
        if solution is not None:
            solution = [env.state_to_pos(s) for s in solution]

        print("\n\n{0}:\n----------------------------------------------------------------"
              "\nExecution time: {1}s"
              "\nN° of states expanded: {2}"
              "\nN° of states generated: {3}"
              "\nMax n° of states in memory: {4}"
              "\nSolution: {5}"
              .format(alg.upper(), round(stats[0], 4), stats[1], stats[2], stats[3], solution))
