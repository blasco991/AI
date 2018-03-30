import gym
import gym_ai_lab
import search.algorithms as search

envs = ["SmallMaze-v0", "GrdMaze-v0", "BlockedMaze-v0"]

for envname in envs:

    print("\n----------------------------------------------------------------")
    print("\tGRAPH SEARCH")
    print("\tEnvironment: ", envname)
    print("----------------------------------------------------------------\n")

    env = gym.make(envname)
    env.render()

    # Suggestion: test the depth-limited search by itself before IDS

    # IDS
    solution, stats = search.ids(env, search.dls_gs)
    if solution is not None:
        solution = [env.state_to_pos(s) for s in solution]
    print("\n\nIDS:\n----------------------------------------------------------------"
          "\nExecution time: {0}s\nN° of states expanded: {1}\nMax n° of states in memory: {2}\nSolution: {3}"
          .format(round(stats[0], 4), stats[1], stats[2], solution))

    # BFS
    solution, stats = search.bfs(env, search.graph_search)
    if solution is not None:
        solution = [env.state_to_pos(s) for s in solution]
    print("\n\nBFS:\n----------------------------------------------------------------"
          "\nExecution time: {0}s\nN° of states expanded: {1}\nMax n° of states in memory: {2}\nSolution: {3}"
          .format(round(stats[0], 4), stats[1], stats[2], solution))

    # UCS
    solution, stats = search.ucs(env, search.graph_search)
    if solution is not None:
        solution = [env.state_to_pos(s) for s in solution]

    print("\n\nUCS:\n----------------------------------------------------------------"
          "\nExecution time: {0}s\nN° of states expanded: {1}\nMax n° of states in memory: {2}\nSolution: {3}"
          .format(round(stats[0], 4), stats[1], stats[2], solution))

    # Greedy
    solution, stats = search.greedy(env, search.graph_search)
    if solution is not None:
        solution = [env.state_to_pos(s) for s in solution]

    print("\n\nGreedy:\n----------------------------------------------------------------"
          "\nExecution time: {0}s\nN° of states expanded: {1}\nMax n° of states in memory: {2}\nSolution: {3}"
          .format(round(stats[0], 4), stats[1], stats[2], solution))

    # A*
    solution, stats = search.astar(env, search.graph_search)
    if solution is not None:
        solution = [env.state_to_pos(s) for s in solution]

    print("\n\nA*:\n----------------------------------------------------------------"
          "\nExecution time: {0}s\nN° of states expanded: {1}\nMax n° of states in memory: {2}\nSolution: {3}"
          .format(round(stats[0], 4), stats[1], stats[2], solution))
