#### FringeNode constructor takes 4 parameters, plus 7 optional parameter to generate the dot GRAPH:
1. the state embedded in the node
2. path cost (from the root node to the current one)
3. the value of the node (used for ordering within PriorityFringe)
4. parent node as FringeNode instance (None if we are building the root) 
5. cause the action that generated this state (None or not specified if we are building the root) 
6. problem the problem instance  
7. gen_label function 
8. shape of node (if not specified the default circle shape is gonna be used) 
9. limit if is limited search (if not specified not limited)
10. closed if exist
11. fringe if exist

```
node = FringeNode(start, 0, 0, None,
                  cause=None, problem=env, shape='box', gen_label=gen_label, fringe=fringe)
fringe.add(node)

child = FringeNode(env.sample(start, 0), 1, 0, node,
                   cause=0, problem=env, gen_label=gen_label, fringe=fringe)  # Child node

if child.state not in fringe:
    fringe.add(child)

child = FringeNode(env.sample(start, 1), 1, 0, node,
                   cause=1, problem=env, gen_label=gen_label)  # Other child node
if child.state in fringe and child.value < fringe[child.state].value:  # Replace node of the same
    fringe.replace(child)

print("\n" + close_dot(2))```
