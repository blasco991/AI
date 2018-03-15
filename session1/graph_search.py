import gym
import search.algorithms as search


envname = "SmallMaze-v0"

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
      "\nExecution time: {0}s\nN° of states expanded: {1}\nMax n° of states in memory: {2}\nSolution: {3}".format(
        round(stats[0], 4), stats[1], stats[2], solution))

# BFS
solution, stats = search.bfs(env, search.graph_search)
# .. print ...

# And so forth....
