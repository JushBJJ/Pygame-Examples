import matplotlib.pyplot as plt
import numpy as np


class DQN:
    def __init__(self, actions):
        self.Q = np.zeros((1, actions))

        self.lastActon = 0
        self.states = []

        self.alpha = 0.00001
        self.discount_factor = 0.9
        self.epsilon = 0.1
        self.actions = actions

    def step(self, old_state, new_state, action, reward):
        old_state = self.states.index(str(old_state))
        new_state = self.states.index(str(new_state))

        oldQ = self.Q[old_state][action]
        self.Q[old_state][action] = oldQ+self.alpha * \
            (reward+self.discount_factor*self.Q[new_state, ].argmax()-oldQ)

        return self.Q[old_state][action]

    def increaseEpilison(self):
        self.epsilon += 0.01 if self.epsilon < 0.99 else 0

    def policy(self, state):
        state = self.states.index(str(state))
        A = np.ones(self.actions, dtype=float)*self.epsilon/self.actions
        best_action = np.argmax(self.Q[state])
        A[best_action] += (1.0-self.epsilon)
        return A

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
