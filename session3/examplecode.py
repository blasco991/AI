import gym
import gym_ai_lab
import numpy as np
import gym.spaces


# Create and render the environment
env = gym.make("CliffWalking-v0")
print()
env.render()

print()

# Execute a random policy in a specific environment. Print the reward
p = np.random.choice(env.action_space.n, env.observation_space.n)
ep_limit = 20
s = env.reset()  # Reset the environment
el = 0
rew = 0
for _ in range(ep_limit):
    sp, r, d, _ = env.step(p[s])  # Execute a step
    rew += r
    el += 1
    if d or el == ep_limit:  # If d == True, the episode has reached a terminal state
        break
    s = sp
print("Execution reward: ", rew)

# Draw a number from a specific probability distribution
print("\nChoose from a spceific distribution: ", np.random.choice(5, p=[0.1, 0.2, 0.5, 0.1, 0.1]))

# List of successors from state 36 (start) indexed by action number: (prob, succ_state, reward, terminal)
print("\nSuccessors from state 36 indexed by action number: ", env.P[36])

# Divide 2 n-dimensional arrays element wise (skip divisions by 0)
a = np.asarray([[10, 10, 8], [10, 10, 20]], dtype="float16")
b = np.asarray([[2, 2, 0], [2, 2, 0]], dtype="float16")
np.divide(a, b, out=a, where=b != 0)
print("\nElement wise division (skip divisions by 0):\n", a)
