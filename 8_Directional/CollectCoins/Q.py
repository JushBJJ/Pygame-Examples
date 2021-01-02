import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn
import math
import random
from collections import namedtuple

import gym

# Tictactoe


class Game:
    def __init__(self):
        self.actions = 9
        self.game = torch.tensor([[35, 35, 35], [35, 35, 35], [35, 35, 35]])

        self.rows = self.game.shape[0]
        self.cols = self.game.shape[1]

        self.nd_size = self.game.shape[0]*self.game.shape[1]
        self.turn = 0

        self.symbols = [ord("X"), ord("O")]

    def checkWin(self):
        win = 0.1

        # *Check Horizontal
        for j in range(self.game.shape[0]):
            if torch.all(self.game[j] == self.symbols[self.turn]).item():
                win = self.turn
            break

        # *Check Vertical
        for i in range(self.game.shape[1]):
            temp = 0

            for j in range(self.game.shape[0]):
                if torch.all(self.game[j][i] == self.symbols[self.turn]).item():
                    temp += 1

            if temp == 3:
                win = self.turn
                break

        # *Check Diagonal (Left to Right)
        sym = self.symbols[self.turn]

        a = self.game[0][0] == sym
        b = self.game[1][1] == sym
        c = self.game[2][2] == sym

        if a and b and c:
            win = self.turn

        # *Check Diagonal (Right to Left)
        a = self.game[0][2] == sym
        b = self.game[1][1] == sym
        c = self.game[2][0] == sym

        if a and b and c:
            win = self.turn

        # *Check if game is draw
        if win != self.turn:
            if ord("#") in self.game and ord("X") in self.game and ord("O") in self.game:
                win = 0.1
            elif ord("#") not in self.game:
                win = -1

        # -1 = Draw
        # 1 = O Wins
        # 0 = X Wins
        # 0.1 = Game still going

        return win

    def doAction(self, action):
        repeated = False
        # Empty (Hashtag) ascii number
        htag = ord("#")

        if action < 3 and self.game[0][action] == htag:
            self.game[0][action] = self.symbols[self.turn]

        elif action >= 3 and action < 6:
            if self.game[1][action-3] == htag:
                self.game[1][action-3] = self.symbols[self.turn]
            else:
                repeated = True

        elif action >= 6:
            if self.game[2][action-6] == htag:
                self.game[2][action-6] = self.symbols[self.turn]
            else:
                repeated = True
        else:
            repeated = True

        result = self.checkWin()

        # -1 = Draw
        # 1 = O Wins
        # 0 = X Wins
        # 0.1 = Game still going

        if result == -1:
            reward = 0.5
            done = True

        elif result == self.turn:
            reward = 5
            done = True

        elif result == 0.1:
            reward = -0.1
            done = False
        else:
            reward = -5
            done = True

        if repeated == False:
            if self.turn == 0:
                self.turn = 1
            else:
                self.turn = 0
        else:
            reward = -100

        state = self.game.reshape((self.nd_size))
        return reward, state, done, repeated

    def reset(self):
        self.game[0][:] = 35
        self.game[1][:] = 35
        self.game[2][:] = 35

        state = self.game.reshape((self.nd_size))
        self.turn = 0
        return state

    def render(self):
        for j in range(self.rows):
            for i in range(self.cols):
                print(chr(self.game[j][i]), " ", end="")

            print()


Transition = namedtuple('Transition',
                        ('state', 'action', 'next_state', 'reward', 'done'))


class ReplayMemory(object):

    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = []
        self.position = 0

    def push(self, *args):
        """Saves a transition."""
        if len(self.memory) < self.capacity:
            self.memory.append(None)
        self.memory[self.position] = Transition(*args)
        self.position = (self.position + 1) % self.capacity

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)


class DQN(nn.Module):
    def __init__(self, stateDim, actions):
        super(DQN, self).__init__()
        self.Q = np.zeros((1, actions))

        self.lastActon = 0
        self.states = []

        self.alpha = 1e-4
        self.gamma = 0.99
        self.actions = actions
        self.stateDim = stateDim
        self.steps = 0
        self.eps = 0.1
        self.epsEnd = 0.9
        self.epsDecay = 0.2
        self.memory = ReplayMemory(100000)
        self.batchSize = 64

        # *Model
        print("State Dim: ", stateDim)
        self.l1 = nn.Linear(stateDim, 64)
        self.l2 = nn.Linear(64, 128)
        self.l3 = nn.Linear(128, 16)
        self.l4 = nn.Linear(16, self.actions)

        self.relu = nn.ReLU()

        self.optimizer = torch.optim.RMSprop(self.parameters(), lr=self.alpha)
        self.lossF = nn.MSELoss()

    def forward(self, x):
        x = torch.tensor(x).to(torch.float32)

        y = self.relu(self.l1(x))
        y = self.relu(self.l2(y))
        y = self.relu(self.l3(y))
        y = torch.tanh(self.l4(y))

        return y

    def optimize(self, episode):
        self.batchSize = int(len(self.memory)/3)
        print("Optimizing ", self.batchSize)
        miniBatch = self.memory.sample(self.batchSize)

        for state, action, next_state, reward, done in miniBatch:
            target = (reward + self.gamma * self.forward(next_state).max())
            target_f = self.forward(state)

            loss = self.lossF(target_f[action], target)
            self.optimizer.zero_grad()

            loss.backward()

            for param in self.parameters():
                param.grad.data.clamp_(-1, 1)

            self.optimizer.step()

        if self.eps < self.epsEnd and episode % 100 == 0:
            self.eps += 1e-1

            print("EPS: ", self.eps)

    def doAction(self, state):
        sample = random.random()

        self.steps += 1

        if sample < self.eps:
            with torch.no_grad():
                return self.forward(state).argmax().item()
        else:
            print("Randomized Action.")
            return torch.tensor([[random.randrange(self.actions)]])

    def addState(self, state):
        n = 0

        if str(state) not in self.states:
            self.states.append(str(state))
            if self.Q[0].all() == 0:
                self.Q[0] = np.ones(self.actions)
            else:
                self.Q = np.vstack((self.Q, np.ones(self.actions)))
            n = 1

        return n


env = gym.make("CartPole-v1")
state = env.reset()

print("\nOB space: ", env.observation_space.shape[0],
      "\nAction Space: ", env.action_space.n)

Q = DQN(env.observation_space.shape[0], env.action_space.n)
# Q2 = DQN(state.size(), env.actions)
env.render()

steps = 1

costs = []
cost = 0

states = []
n_states = 0

rewards = []
xrewards = 0

avgRewards = []
totalReward = 0
avgReward = 0

avgCosts = []
totalCost = 0
avgCost = 0

epsilon = []

episodes = 10000
done = False

for i in range(1, episodes):
    xrewards = 0
    env.reset()
    done = False

    while done == False:
        action = int(Q.doAction(state))
        # reward, next_state, done, repeated = env.doAction(action)
        next_state, reward, done, _ = env.step(action)

        print("Reward: ", reward)

        Q.memory.push(state, action, next_state, reward, done)
        state = next_state

        if i % 100 == 0:
            env.render()

        # Q2.memory.push(state, action, next_state, reward, done)

        # if repeated:
        #    continue

        if done:
            print("Episode Done.")
            print(
                f"Episode: {i}\n\tQ1 Reward: {reward}\n\tQ2 Reward: {reward}\n\tQ1 EPS: {Q.eps}\n\tSteps: {steps}")
            break

        """if steps % 1 == 0:
            print("Cost: ", cost, "\tEpisode: ", i, " Step: ", steps,
                  " Reward: ", reward, "Epilson: ", Q.eps)"""

        """action = int(Q2.doAction(next_state))
        reward2, state, done, repeated = env.doAction(action)

        Q2.memory.push(next_state, action, state, reward2, done)
        Q.memory.push(next_state, action, state, reward2, done)"""

        steps += 1
        print(
            f"Episode: {i}\n\tQ1 Reward: {reward}\n\tQ2 Reward: {reward}\n\tQ1 EPS: {Q.eps}\n\tSteps: {steps}")

    print(i)
    print(i % 100)

    if i % 100 == 0:
        print("Optimizing...")
        Q.optimize(i)

        # Q2.optimize(i)

env.close()

rewards.append(xrewards)
costs.append(cost)

avgReward = totalReward/i
avgRewards.append(avgReward)

avgCost = totalCost/i
avgCosts.append(avgCost)

states.append(n_states)
epsilon.append(Q.eps)

cost = 0
done = False
state = env.reset()

f, axs = plt.subplots(2, 2)

l, = axs[0, 0].plot(costs)
l1, = axs[0, 0].plot(avgCosts)

axs[0, 0].set_xlabel("Episodes")
axs[0, 0].set_ylabel("Cost Value")

l.set_label("Cost")
l1.set_label("Average Costs")

axs[0, 0].legend()

l, = axs[0, 1].plot(states)
axs[0, 1].set_xlabel("Steps")
axs[0, 1].set_ylabel("States Discovered")

l.set_label("States")
axs[0, 1].legend()

l, = axs[1, 0].plot(rewards)
l1, = axs[1, 0].plot(avgRewards)

axs[1, 0].set_xlabel("Episodes")
axs[1, 0].set_ylabel("rewards")

l.set_label("Rewards")
l1.set_label("avgRewards")

axs[1, 0].legend()

l, = axs[1, 1].plot(gammas)

axs[1, 1].set_xlabel("Episodes")
axs[1, 1].set_ylabel("Gamma Value")
l.set_label("Gamma")
axs[1, 1].legend()

plt.show()
