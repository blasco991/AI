import gym
import gym_ai_lab
import search.algorithms as search

envs = ["SmallMaze-v0", "GrdMaze-v0"]  # , "BlockedMaze-v0"]

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
    solution, stats = search.ids(env, search.dls_ts)
    if solution is not None:
        solution = [env.state_to_pos(s) for s in solution]
    print("\n\nIDS:\n----------------------------------------------------------------"
          "\nExecution time: {0}s\nN° of states expanded: {1}\nMax n° of states in memory: {2}\nSolution: {3}"
          .format(round(stats[0], 4), stats[1], stats[2], solution))

    # BFS
    solution, stats = search.bfs(env, search.tree_search_plus)
    if solution is not None:
        solution = [env.state_to_pos(s) for s in solution]
    print("\n\nBFS TS+:\n----------------------------------------------------------------"
          "\nExecution time: {0}s\nN° of states expanded: {1}\nMax n° of states in memory: {2}\nSolution: {3}"
          .format(round(stats[0], 4), stats[1], stats[2], solution))

    # UCS
    solution, stats = search.ucs(env, search.tree_search_plus)
    if solution is not None:
        solution = [env.state_to_pos(s) for s in solution]
    print("\n\nUCS TS+:\n----------------------------------------------------------------"
          "\nExecution time: {0}s\nN° of states expanded: {1}\nMax n° of states in memory: {2}\nSolution: {3}"
          .format(round(stats[0], 4), stats[1], stats[2], solution))

    # A*
    solution, stats = search.astar(env, search.tree_search_plus)
    if solution is not None:
        solution = [env.state_to_pos(s) for s in solution]
    print("\n\nA* TS+:\n----------------------------------------------------------------"
          "\nExecution time: {0}s\nN° of states expanded: {1}\nMax n° of states in memory: {2}\nSolution: {3}"
          .format(round(stats[0], 4), stats[1], stats[2], solution))

    # Greedy
    solution, stats = search.greedy(env, search.tree_search_plus)
    if solution is not None:
        solution = [env.state_to_pos(s) for s in solution]
    print("\n\nGreedy TS+:\n----------------------------------------------------------------"
          "\nExecution time: {0}s\nN° of states expanded: {1}\nMax n° of states in memory: {2}\nSolution: {3}"
          .format(round(stats[0], 4), stats[1], stats[2], solution))
    """
    # Greedy
    solution, stats = search.greedy(env, search.tree_search)
    if solution is not None:
        solution = [env.state_to_pos(s) for s in solution]
    print("\n\nGreedy:\n----------------------------------------------------------------"
          "\nExecution time: {0}s\nN° of states expanded: {1}\nMax n° of states in memory: {2}\nSolution: {3}"
          .format(round(stats[0], 4), stats[1], stats[2], solution))
    """
