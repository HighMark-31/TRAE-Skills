# Skill: Reinforcement Learning Basics

## Purpose
To implement intelligent agents that learn optimal behaviors through interaction with an environment, using rewards and penalties to guide decision-making.

## When to Use
- When building game-playing AI
- When optimizing control systems (robotics, autonomous vehicles)
- When solving sequential decision problems
- When implementing recommendation systems with user feedback

## Procedure

### 1. Q-Learning Implementation
Implement basic Q-learning algorithm.

```python
import numpy as np
from collections import defaultdict

class QLearningAgent:
    def __init__(self, state_size, action_size, learning_rate=0.1, discount_factor=0.95, epsilon=1.0):
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01
        self.q_table = defaultdict(lambda: np.zeros(action_size))
    
    def choose_action(self, state):
        """Choose action using epsilon-greedy policy."""
        if np.random.random() <= self.epsilon:
            return np.random.choice(self.action_size)
        else:
            return np.argmax(self.q_table[state])
    
    def learn(self, state, action, reward, next_state, done):
        """Update Q-value using Q-learning formula."""
        current_q = self.q_table[state][action]
        
        if done:
            max_next_q = 0
        else:
            max_next_q = np.max(self.q_table[next_state])
        
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * max_next_q - current_q)
        self.q_table[state][action] = new_q
        
        # Decay epsilon
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
    
    def save_q_table(self, filename):
        """Save Q-table to file."""
        dict_q_table = dict(self.q_table)
        np.save(filename, dict_q_table)
    
    def load_q_table(self, filename):
        """Load Q-table from file."""
        dict_q_table = np.load(filename, allow_pickle=True).item()
        self.q_table = defaultdict(lambda: np.zeros(self.action_size), dict_q_table)

# Simple grid world environment
class GridWorld:
    def __init__(self, size=5):
        self.size = size
        self.start = (0, 0)
        self.goal = (size-1, size-1)
        self.obstacles = [(2, 2), (3, 1), (1, 3)]
        self.current_state = self.start
        self.actions = ['up', 'down', 'left', 'right']
    
    def reset(self):
        self.current_state = self.start
        return self.current_state
    
    def step(self, action):
        row, col = self.current_state
        
        if action == 'up':
            new_row, new_col = row - 1, col
        elif action == 'down':
            new_row, new_col = row + 1, col
        elif action == 'left':
            new_row, new_col = row, col - 1
        elif action == 'right':
            new_row, new_col = row, col + 1
        
        # Check boundaries
        if 0 <= new_row < self.size and 0 <= new_col < self.size:
            if (new_row, new_col) not in self.obstacles:
                self.current_state = (new_row, new_col)
        
        # Calculate reward
        if self.current_state == self.goal:
            reward = 10
            done = True
        else:
            reward = -1
            done = False
        
        return self.current_state, reward, done

# Training
env = GridWorld()
agent = QLearningAgent(state_size=env.size*env.size, action_size=4)

episodes = 1000
for episode in range(episodes):
    state = env.reset()
    done = False
    total_reward = 0
    
    while not done:
        action_idx = agent.choose_action(state)
        action = env.actions[action_idx]
        next_state, reward, done = env.step(action)
        
        agent.learn(state, action_idx, reward, next_state, done)
        state = next_state
        total_reward += reward
    
    if episode % 100 == 0:
        print(f"Episode {episode}, Total Reward: {total_reward}, Epsilon: {agent.epsilon:.3f}")
```

### 2. Deep Q-Network (DQN)
Implement deep Q-learning with neural networks.

```python
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque
import random

class DQN(nn.Module):
    def __init__(self, state_size, action_size):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(state_size, 64)
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, action_size)
    
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)

class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=10000)
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.batch_size = 32
        
        self.model = DQN(state_size, action_size)
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)
    
    def remember(self, state, action, reward, next_state, done):
        """Store experience in replay memory."""
        self.memory.append((state, action, reward, next_state, done))
    
    def act(self, state):
        """Choose action using epsilon-greedy policy."""
        if np.random.random() <= self.epsilon:
            return random.randrange(self.action_size)
        
        state = torch.FloatTensor(state).unsqueeze(0)
        q_values = self.model(state)
        return np.argmax(q_values.detach().numpy()[0])
    
    def replay(self):
        """Train on a batch of experiences."""
        if len(self.memory) < self.batch_size:
            return
        
        minibatch = random.sample(self.memory, self.batch_size)
        states = torch.FloatTensor([t[0] for t in minibatch])
        actions = torch.LongTensor([t[1] for t in minibatch])
        rewards = torch.FloatTensor([t[2] for t in minibatch])
        next_states = torch.FloatTensor([t[3] for t in minibatch])
        dones = torch.FloatTensor([t[4] for t in minibatch])
        
        current_q_values = self.model(states).gather(1, actions.unsqueeze(1))
        next_q_values = self.model(next_states).max(1)[0].detach()
        target_q_values = rewards + (1 - dones) * self.gamma * next_q_values
        
        loss = nn.MSELoss()(current_q_values.squeeze(), target_q_values)
        
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
    
    def save(self, filename):
        """Save model."""
        torch.save(self.model.state_dict(), filename)
    
    def load(self, filename):
        """Load model."""
        self.model.load_state_dict(torch.load(filename))

# Usage
env = GridWorld()
state_size = env.size * env.size
action_size = 4

agent = DQNAgent(state_size, action_size)

episodes = 500
for episode in range(episodes):
    state = env.reset()
    state_flat = np.array(state).flatten()
    done = False
    total_reward = 0
    
    while not done:
        action = agent.act(state_flat)
        next_state, reward, done = env.step(env.actions[action])
        next_state_flat = np.array(next_state).flatten()
        
        agent.remember(state_flat, action, reward, next_state_flat, done)
        state = next_state
        state_flat = next_state_flat
        total_reward += reward
    
    agent.replay()
    
    if episode % 50 == 0:
        print(f"Episode {episode}, Total Reward: {total_reward}, Epsilon: {agent.epsilon:.3f}")
```

### 3. Policy Gradient Implementation
Implement REINFORCE algorithm.

```python
class PolicyGradientAgent:
    def __init__(self, state_size, action_size, learning_rate=0.01):
        self.state_size = state_size
        self.action_size = action_size
        self.gamma = 0.99
        
        # Policy network
        self.policy = nn.Sequential(
            nn.Linear(state_size, 128),
            nn.ReLU(),
            nn.Linear(128, action_size),
            nn.Softmax(dim=-1)
        )
        
        self.optimizer = optim.Adam(self.policy.parameters(), lr=learning_rate)
    
    def choose_action(self, state):
        """Choose action based on policy."""
        state = torch.FloatTensor(state)
        probs = self.policy(state)
        
        # Sample from probability distribution
        action_dist = torch.distributions.Categorical(probs)
        action = action_dist.sample()
        
        return action.item(), action_dist.log_prob(action)
    
    def update_policy(self, rewards, log_probs):
        """Update policy using REINFORCE."""
        returns = []
        R = 0
        
        # Calculate discounted returns
        for r in reversed(rewards):
            R = r + self.gamma * R
            returns.insert(0, R)
        
        returns = torch.FloatTensor(returns)
        log_probs = torch.stack(log_probs)
        
        # Calculate loss
        policy_loss = []
        for log_prob, R in zip(log_probs, returns):
            policy_loss.append(-log_prob * R)
        
        policy_loss = torch.stack(policy_loss).sum()
        
        # Update policy
        self.optimizer.zero_grad()
        policy_loss.backward()
        self.optimizer.step()

# Training
env = GridWorld()
agent = PolicyGradientAgent(state_size=env.size*env.size, action_size=4)

episodes = 1000
for episode in range(episodes):
    state = env.reset()
    state_flat = np.array(state).flatten()
    done = False
    rewards = []
    log_probs = []
    
    while not done:
        action, log_prob = agent.choose_action(state_flat)
        next_state, reward, done = env.step(env.actions[action])
        
        rewards.append(reward)
        log_probs.append(log_prob)
        
        state = next_state
        state_flat = np.array(state).flatten()
    
    agent.update_policy(rewards, log_probs)
    
    if episode % 100 == 0:
        print(f"Episode {episode}, Total Reward: {sum(rewards)}")
```

## Constraints
- **Training Time**: RL requires many episodes to converge
- **Hyperparameter Sensitivity**: Performance highly depends on hyperparameter tuning
- **Sample Efficiency**: Traditional RL is sample inefficient
- **Exploration vs. Exploitation**: Balancing exploration and exploitation is crucial
- **Reward Design**: Poor reward design leads to unexpected behaviors
- **Computational Resources**: Deep RL requires significant computational power

## Expected Output
Intelligent agents that learn optimal policies through experience, capable of making sequential decisions in complex environments.
