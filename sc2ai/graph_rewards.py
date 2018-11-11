import numpy as np
from matplotlib import pyplot as plt

rewards = []
with open('rewards.txt', 'r') as f:
    for line in f:
        rewards.append(int(line))

smooth_n = 200

smoothed_rewards = []
for i in range(len(rewards) - smooth_n):
    smoothed_rewards.append(np.sum(rewards[i:i+smooth_n]) / smooth_n)

plt.plot(smoothed_rewards)
plt.show()
