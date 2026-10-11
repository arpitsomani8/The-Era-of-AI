# -*- coding: utf-8 -*-
"""
Script to modernize and standardize concept_q_learning_dqn in src/data/concepts.json
and scripts/data_sources/all_concepts.json.
"""

import json

new_concept = {
    "id": "concept_q_learning_dqn",
    "title": "Q-Learning & Deep Q-Networks (DQN)",
    "topic_id": "dl_rl_foundations",
    "topic_label": "Reinforcement Learning (RL) & Decision Foundations",
    "category": "dl",
    "category_label": "Deep Learning Foundations",
    "raw_subtopic": "Q-Learning & Deep Q-Networks (DQN)",
    "def": "Q-Learning is a model-free, off-policy temporal difference reinforcement learning algorithm that learns optimal action-values Q(s,a) through environmental interaction without requiring transition models. Deep Q-Networks (DQN) scale Q-learning to high-dimensional state spaces by approximating Q-functions with deep neural networks, stabilized via experience replay buffers and decoupled target networks.",
    "definition": "In reinforcement learning, Q-Learning is a foundational model-free, off-policy, value-based algorithm that iteratively learns the optimal action-value function Q*(s,a) representing the expected discounted cumulative return of executing action a in state s and following the optimal policy thereafter. As an off-policy algorithm, Q-Learning learns about the greedy optimal target policy while behaving according to an exploratory policy, such as epsilon-greedy. The tabular update applies the Bellman optimality equation directly to update Q-table entries via temporal-difference (TD) errors: Q(s,a) <- Q(s,a) + alpha [r + gamma max_a' Q(s',a') - Q(s,a)]. For high-dimensional or continuous state spaces where tabular storage suffers from the curse of dimensionality, Deep Q-Networks (DQN) replace discrete tables with deep parameterized neural networks Q(s,a; theta). To overcome severe training instabilities arising from correlated sequential data and non-stationary targets (the 'deadly triad' of function approximation, bootstrapping, and off-policy learning), DQN introduces two critical stabilizing innovations: (1) Experience Replay, which stores observed transitions (s, a, r, s', done) in a cyclic buffer and trains on uniformly sampled minibatches to break temporal autocorrelations, and (2) Decoupled Target Networks (parameterized by theta^-), which freeze target generation for periodic intervals to eliminate the moving-target instability.",
    "simple_summary": "Imagine training a robot to navigate a bustling warehouse. At first, the robot knows nothing about the floor plan. In Tabular Q-Learning, the robot keeps a physical scorecard (a Q-table) where every room has a row and every movement (Up, Down, Left, Right) has a column. Whenever it moves, gets a reward, and sees what its best next move would be, it updates that score. But what if the warehouse has cameras capturing 84x84 pixel video frames with millions of possible visual states? A scorecard would need more rows than atoms in the universe. That is why Deep Q-Networks (DQN) were invented: they replace the scorecard with a deep neural network that looks at the camera screen and directly estimates the value of every action. To keep the robot from getting dizzy and destabilizing, DQN stores its memories in an 'experience replay' bank to study random past moments, and uses a separate, slowly-updating 'target network' as a steady teacher.",
    "definition_bullets": [
        "Model-Free & Off-Policy Foundation: Learns optimal action values Q*(s,a) without transition dynamics P(s'|s,a), decoupling exploration policy from target greedy policy.",
        "Bellman Optimality TD Update: Adjusts value estimates proportional to temporal-difference error delta = r + gamma max_a' Q(s',a') - Q(s,a) using learning rate alpha.",
        "Function Approximation with Deep Neural Networks: Maps raw states s to vectors of Q-values across all discrete actions in a single forward pass Q(s; theta).",
        "Experience Replay Stabilization: Stores transition tuples in a cyclic buffer and trains on random minibatches to eliminate temporal autocorrelation and enhance sample efficiency.",
        "Target Network Decoupling: Maintains a separate frozen network theta^- to generate stable bootstrapped regression targets, updated periodically or via Polyak soft averaging."
    ],
    "core_terms": [
        {
            "term": "Temporal Difference (TD) Target",
            "what_is_it": "The bootstrapped regression target estimate for an action value.",
            "definition": "The numerical quantity y = r + gamma (1 - done) max_a' Q(s', a'; theta^-) representing the immediate observed reward plus the discounted optimal future value estimated by the target network.",
            "analogy": "A relay racer passing a baton: your estimated lap time is the seconds you just ran plus the teammate's estimated split time.",
            "why_it_matters": "Provides the training supervision signal for gradient descent in DQN without requiring full episode rollouts, enabling online sample-efficient learning."
        },
        {
            "term": "Experience Replay Buffer",
            "what_is_it": "A cyclic memory buffer storing past environmental transitions.",
            "definition": "A bounded FIFO dataset D = {(s_t, a_t, r_t, s_{t+1}, done_t)} that stores transition tuples collected during online environment interaction and serves random minibatches for network updates.",
            "analogy": "A student reviewing flashcards drawn randomly from their entire school semester rather than cramming only the last 5 minutes of lecture.",
            "why_it_matters": "Breaks the strong temporal autocorrelation of consecutive RL frames, stabilizes neural network gradient steps, and reuses scarce historical transitions multiple times."
        },
        {
            "term": "Target Network (θ⁻)",
            "what_is_it": "A stabilized, lagging copy of the online Q-network.",
            "definition": "A neural network parameterized by theta^- with identical architecture to the online network theta, used solely to compute next-state values max_a' Q(s', a'; theta^-) and held fixed or updated via slow Polyak tracking.",
            "analogy": "A coach holding a stationary archery target so the archer can aim steadily, rather than running while holding the target.",
            "why_it_matters": "Eliminates the deadly feedback loop where updating theta simultaneously moves the regression target, preventing divergence and severe policy oscillation."
        },
        {
            "term": "Epsilon-Greedy Exploration",
            "what_is_it": "A stochastic balance mechanism between exploratory search and greedy exploitation.",
            "definition": "An action selection policy where the agent selects a random action with probability epsilon and executes the greedy action argmax_a Q(s,a) with probability 1 - epsilon, typically annealed over time.",
            "analogy": "Dining out: 90% of the time you order your favorite dish, but 10% of the time you try a mystery item on the menu to discover if it is even better.",
            "why_it_matters": "Ensures the agent visits diverse regions of the state-action space early in training, avoiding premature convergence to suboptimal myopic policies."
        },
        {
            "term": "Double DQN (DDQN)",
            "what_is_it": "An architectural extension decoupling action selection from evaluation.",
            "definition": "An enhancement that addresses maximization overestimation bias by using the online network theta to select the best action a* = argmax_a' Q(s', a'; theta) and the target network theta^- to evaluate its value Q(s', a*; theta^-).",
            "analogy": "Separation of judicial powers: one person proposes the suspect (selection) and an independent judge evaluates the sentence (evaluation).",
            "why_it_matters": "Substantially reduces the systematic positive overestimation bias inherent in the standard max operator, leading to faster convergence and superior stability."
        }
    ],
    "symbol_guide": [
        {
            "symbol": "Q(s,a)",
            "name": "Action-Value Function",
            "meaning": "Expected cumulative discounted reward from state s taking action a under policy pi."
        },
        {
            "symbol": "α",
            "name": "Learning Rate (alpha)",
            "meaning": "Step-size scalar in (0, 1] weighting the degree to which TD errors update Q-values."
        },
        {
            "symbol": "γ",
            "name": "Discount Factor (gamma)",
            "meaning": "Temporal discount multiplier in [0, 1) balancing immediate reward versus long-term returns."
        },
        {
            "symbol": "δ",
            "name": "Temporal Difference Error",
            "meaning": "The discrepancy delta = y - Q(s,a) between the bootstrapped target and current estimate."
        },
        {
            "symbol": "θ",
            "name": "Online Network Weights",
            "meaning": "Trainable parameter vector of the primary deep neural network actively updated by gradient descent."
        },
        {
            "symbol": "θ⁻",
            "name": "Target Network Weights",
            "meaning": "Frozen or slowly updated parameters providing stable next-state value estimations."
        },
        {
            "symbol": "ε",
            "name": "Exploration Probability (epsilon)",
            "meaning": "Probability of choosing a random uniform action in epsilon-greedy behavioral exploration."
        }
    ],
    "formula": "$$\\text{Tabular Q-Learning Bellman Update: } Q(s,a) \\leftarrow Q(s,a) + \\alpha \\left[ r + \\gamma \\max_{a' \\in \\mathcal{A}} Q(s',a') - Q(s,a) \\right]$$\n\n$$\\text{Temporal Difference Error: } \\delta = y - Q(s,a), \\quad \\text{where } y = r + \\gamma (1 - d) \\max_{a'} Q(s', a')$$\n\n$$\\text{Standard DQN Loss Function: } \\mathcal{L}(\\theta) = \\mathbb{E}_{(s,a,r,s',d) \\sim \\mathcal{D}} \\left[ \\left( r + \\gamma (1-d) \\max_{a'} Q(s', a'; \\theta^-) - Q(s,a;\\theta) \\right)^2 \\right]$$\n\n$$\\text{Double DQN (DDQN) Target: } y^{\\text{Double}} = r + \\gamma (1-d) Q\\left(s', \\arg\\max_{a'} Q(s', a'; \\theta); \\theta^-\\right)$$\n\n$$\\text{Dueling DQN Value-Advantage Decomposition: } Q(s,a; \\theta) = V(s; \\theta_v) + \\left( A(s,a; \\theta_a) - \\frac{1}{|\\mathcal{A}|} \\sum_{a' \\in \\mathcal{A}} A(s,a'; \\theta_a) \\right)$$\n\n$$\\text{Polyak Target Network Soft Update: } \\theta^- \\leftarrow \\tau \\theta + (1 - \\tau) \\theta^-, \\quad \\tau \\ll 1$$\n\n$$\\text{Smooth L1 (Huber) Loss: } \\mathcal{L}_{\\delta}(e) = \\begin{cases} 0.5 e^2 & \\text{if } |e| \\le 1 \\\\ |e| - 0.5 & \\text{otherwise} \\end{cases}$$",
    "logic": "The evolution from Tabular Q-Learning to Deep Q-Networks marks one of the most consequential transitions in reinforcement learning. Q-Learning operates as a model-free, off-policy temporal-difference control algorithm. Unlike Monte Carlo methods that require entire episodes to terminate before computing returns G_t, Q-Learning bootstraps immediately at step t+1 by computing the TD target y = r + gamma max_a' Q(s',a'). The update moves the current estimate toward the target with learning rate alpha. In small discrete state spaces, Q-tables are mathematically guaranteed to converge to the optimal action-value function Q* under standard Robbins-Monro stochastic approximation conditions (all state-action pairs visited infinitely often, and learning rate step sizes satisfying sum alpha_t = inf and sum alpha_t^2 < inf). However, when transitioning to high-dimensional state spaces—such as visual pixel matrices or robotics joint vectors—tabular representation collapses due to the curse of dimensionality. Deep Q-Networks (DQN) resolve this by approximating Q*(s,a) using a deep convolutional or feed-forward neural network parameterized by theta. Instead of accepting both state s and action a as inputs, the architecture takes state s as input and outputs a vector of Q-values across all discrete actions simultaneously in a single forward pass, drastically reducing inference latency. However, applying naive gradient descent with deep neural networks to off-policy RL triggers the 'deadly triad'—the combination of function approximation, bootstrapping, and off-policy training that frequently causes numerical divergence. DQN stabilizes learning through two foundational mechanisms: First, Experience Replay breaks the temporal autocorrelation between successive transitions by storing transitions in a circular buffer and drawing independent and identically distributed (i.i.d.) minibatches. Second, Decoupling Target Networks parameterizes a separate target network theta^- to generate regression targets, preventing the harmful feedback loop where weight updates shift both predictions and targets simultaneously. To eliminate maximization bias caused by Jensen's inequality and noisy function approximation, Double DQN (DDQN) decouples action selection (using online weights theta) from action evaluation (using target weights theta^-). Furthermore, Dueling DQN separates the network into two streams: a scalar state-value stream V(s) and an action-advantage stream A(s,a), ensuring that states with intrinsically high or low values are learned efficiently even when action choices produce subtle differences.",
    "example": "Consider training an automated guided vehicle (AGV) in a dynamic distribution warehouse. The state space S consists of an 8-dimensional vector: LiDAR obstacle distances, current velocity, battery charge, and distance to destination pallet. The discrete action space A consists of 4 motor commands: {Turn Left, Turn Right, Move Forward, Reverse}. When approaching an aisle intersection, taking 'Move Forward' yields an immediate reward r = +3 for advancing toward the pallet, and transitions to state B where the target network predicts max_a' Q(B, a'; theta^-) = 8.0. With gamma = 0.9 and previous estimate Q(A, Forward; theta) = 4.0, the TD target is 3 + 0.9(8.0) = 10.2, yielding a positive TD error delta = +6.2. By storing this transition in an experience replay buffer with 100,000 steps and training with mini-batches of size 64 using Adam with learning rate 1e-3, the AGV learns to balance battery preservation, obstacle avoidance, and pallet retrieval without ever requiring a manual blueprint of the warehouse.",
    "numerical_example": "Step 1: Tabular Q-Learning Step-by-Step Numerical Update (Matching User Notes)\nSuppose an agent is in state A and chooses action 'right', transitioning to state B:\n  - Current Q-value:                 Q(A, right) = 4.0\n  - Observed immediate reward:       r = +3.0\n  - Best Q-value in next state B:    max_{a'} Q(B, a') = 8.0\n  - Learning rate:                   alpha = 0.5\n  - Discount factor:                 gamma = 0.9\n\nCalculate TD Target y:\n  y = r + gamma * max_{a'} Q(B, a')\n  y = 3.0 + 0.9 * (8.0) = 3.0 + 7.2 = 10.2\n\nCalculate Temporal Difference Error delta:\n  delta = y - Q(A, right) = 10.2 - 4.0 = +6.2\n\nApply Q-Learning Update:\n  Q_new = Q_old + alpha * delta\n  Q_new = 4.0 + 0.5 * (6.2) = 4.0 + 3.1 = 7.1\nThe Q-value updates from 4.0 to 7.1, moving halfway (alpha = 0.5) toward the target of 10.2.\n\nStep 2: Tabular Gridworld Implementation with Epsilon Decay & Terminal Masking (Matching User Notes)\n```python\nimport numpy as np\nimport random\n\nn_states, n_actions = 25, 4\nQ = np.zeros((n_states, n_actions))\nalpha, gamma = 0.1, 0.95\nepsilon, epsilon_min, epsilon_decay = 1.0, 0.05, 0.995\n\n# Simulated episode transition\nstate = 0\naction = random.randrange(n_actions) if random.random() < epsilon else int(np.argmax(Q[state]))\nnext_state, reward, terminated = 1, 10.0, False\n\n# Terminal state masking: do NOT bootstrap past terminal state\ntarget = reward if terminated else reward + gamma * np.max(Q[next_state])\nQ[state, action] += alpha * (target - Q[state, action])\nepsilon = max(epsilon_min, epsilon * epsilon_decay)\nprint(f'Updated Q(0, {action}): {Q[state, action]:.4f}, New Epsilon: {epsilon:.4f}')\n```\n\nStep 3: PyTorch Deep Q-Network Batch Optimization Pipeline (Matching User Notes)\n```python\nimport torch\nimport torch.nn as nn\nimport torch.nn.functional as F\n\nclass QNetwork(nn.Module):\n    def __init__(self, state_dim=8, n_actions=4):\n        super().__init__()\n        self.net = nn.Sequential(\n            nn.Linear(state_dim, 128), nn.ReLU(),\n            nn.Linear(128, 128), nn.ReLU(),\n            nn.Linear(128, n_actions)\n        )\n    def forward(self, x): return self.net(x)\n\nonline_net = QNetwork(8, 4)\ntarget_net = QNetwork(8, 4)\ntarget_net.load_state_dict(online_net.state_dict())\noptimizer = torch.optim.Adam(online_net.parameters(), lr=1e-3)\n\n# Synthetic batch: 32 samples\nstates = torch.randn(32, 8)\nactions = torch.randint(0, 4, (32,))\nrewards = torch.randn(32)\nnext_states = torch.randn(32, 8)\nterminated = torch.zeros(32, dtype=torch.bool)\nterminated[0] = True  # Sample 0 is terminal\n\n# 1. Forward pass online network & gather taken actions\nq_values = online_net(states)\nchosen_q = q_values.gather(1, actions.unsqueeze(1)).squeeze(1)\n\n# 2. Compute Target with target network (no gradient tracking)\nwith torch.no_grad():\n    next_q = target_net(next_states).max(dim=1).values\n    targets = rewards + 0.99 * (~terminated).float() * next_q\n\n# 3. Smooth L1 Loss & Gradient Clipping\nloss = F.smooth_l1_loss(chosen_q, targets)\noptimizer.zero_grad()\nloss.backward()\ntorch.nn.utils.clip_grad_norm_(online_net.parameters(), max_norm=10.0)\noptimizer.step()\nprint(f'Calculated Huber Loss: {loss.item():.4f}')\n```\n\nStep 4: Double DQN (DDQN) Overestimation Bias Elimination\nConsider next state s' with target network predictions Q(s', a; theta^-) and online predictions Q(s', a; theta):\n  - Online net Q(s', :; theta):   [ 5.8,  6.2,  4.1,  5.9 ] -> argmax is Action 1 (Q = 6.2)\n  - Target net Q(s', :; theta^-): [ 5.9,  5.4,  4.3,  6.0 ]\nStandard DQN Target (Maximizes noisy target values):\n  max_{a'} Q(s', a'; theta^-) = max(5.9, 5.4, 4.3, 6.0) = 6.0 (Picks Action 3)\nDouble DQN Target (Online picks action, Target evaluates):\n  Online picks a* = argmax(5.8, 6.2, 4.1, 5.9) = Action 1\n  Target evaluates Action 1: Q(s', 1; theta^-) = 5.4\nResult: DDQN target is 5.4 instead of 6.0, successfully stripping out +0.6 of overestimation bias!\n\nStep 5: Dueling DQN Architecture Value-Advantage Arithmetic\nSuppose for a state s, the Value stream predicts V(s) = 10.0, and the Advantage stream predicts A(s, :) = [ -2.0, +4.0, +1.0 ] across 3 actions.\n  Mean advantage: mean(A) = (-2.0 + 4.0 + 1.0) / 3 = 3.0 / 3 = 1.0\nCalculate Q-values via Q(s,a) = V(s) + (A(s,a) - mean(A)):\n  Q(s, a_0) = 10.0 + (-2.0 - 1.0) = 10.0 - 3.0 = 7.0\n  Q(s, a_1) = 10.0 + (+4.0 - 1.0) = 10.0 + 3.0 = 13.0\n  Q(s, a_2) = 10.0 + (+1.0 - 1.0) = 10.0 + 0.0 = 10.0\nNotice that the average of Q-values is (7.0 + 13.0 + 10.0) / 3 = 30.0 / 3 = 10.0 = V(s), ensuring exact identifiability!",
    "types_header": "Value-Based Reinforcement Learning Frameworks",
    "types_badge": "Tabular & Deep Q-Architectures",
    "quick_types": [
        {
            "name": "Tabular Q-Learning",
            "description": "Classical model-free off-policy algorithm storing Q-values in discrete 2D matrices, guaranteed to converge in small finite MDPs under sufficient exploration."
        },
        {
            "name": "Vanilla Deep Q-Network (DQN)",
            "description": "Deep neural network function approximator mapping states to action values, stabilized by an experience replay buffer and periodic target network copies."
        },
        {
            "name": "Double Deep Q-Network (DDQN)",
            "description": "Decouples action selection (online network) from action evaluation (target network), eliminating systematic positive overestimation bias in TD targets."
        },
        {
            "name": "Dueling Deep Q-Network (Dueling DQN)",
            "description": "Dual-stream neural network architecture factoring Q(s,a) into state value V(s) and advantage A(s,a), drastically accelerating learning in states where actions yield similar outcomes."
        }
    ],
    "connected_logic": [
        {
            "title": "Bootstrapping & Temporal-Difference Control",
            "description": "Theoretical mechanics of updating value functions using single-step empirical rewards and discounted downstream estimates.",
            "points": [
                "Bootstraps immediately at time step t+1 without requiring complete episode termination or trajectory rollouts.",
                "Updates parameter weights proportional to TD error delta = r + gamma max Q(s',a') - Q(s,a).",
                "Operates off-policy: evaluates the optimal greedy policy while actively following an exploratory behavioral policy."
            ]
        },
        {
            "title": "Experience Replay Memory Dynamics",
            "description": "Overcoming the deadly triad in deep reinforcement learning through i.i.d. sampling from a historical replay memory.",
            "points": [
                "Buffers transition tuples (s, a, r, s', done) in a bounded FIFO queue, retaining tens of thousands of past interactions.",
                "Draws uniform random minibatches, breaking strong temporal correlations between consecutive sequential frames.",
                "Reuses rare transitions across multiple optimization epochs, dramatically boosting overall sample efficiency."
            ]
        },
        {
            "title": "Target Network Decoupling & Stability",
            "description": "Resolving the moving-target divergence problem in regression by freezing target network parameter updates.",
            "points": [
                "Maintains secondary parameters theta^- exclusively for calculating downstream bootstrapped TD targets.",
                "Freezes theta^- for fixed intervals or performs slow Polyak tracking theta^- <- tau theta + (1-tau) theta^-.",
                "Prevents parameter updates from shifting predictions and regression targets simultaneously, guaranteeing bounded loss curves."
            ]
        },
        {
            "title": "Overestimation Bias & Architectural Enhancements",
            "description": "Advanced modifications including Double DQN, Dueling DQN, and Prioritized Replay that elevate baseline DQN to production performance.",
            "points": [
                "Double DQN eliminates maximization bias by selecting best actions with online network and evaluating with target network.",
                "Dueling DQN separates state values from action advantages, improving credit assignment across invariant states.",
                "Prioritized Experience Replay (PER) samples transitions according to TD error magnitude, prioritizing critical learning moments."
            ]
        }
    ],
    "pitfalls": [
        "Treating Q-Values as Action Probabilities: Q-values represent expected discounted cumulative returns (-inf to +inf), not normalized action probabilities that sum to 1.",
        "Omitting Epsilon-Greedy Annealing or Exploration: An agent that exploits greedily from initialization gets trapped in early local optima, never discovering superior distant reward paths.",
        "Improper Terminal-State Masking: Bootstrapping past terminal states (failing to multiply next-state values by 1 - done) propagates nonexistent future returns into game-over states.",
        "Overly Frequent Target Network Updates: Updating target network parameters theta^- every single optimization step reintroduces moving-target instability and causes training divergence.",
        "Applying Discrete DQN to Continuous Action Spaces: DQN relies on the max_a operator across discrete output nodes; continuous action spaces require Actor-Critic algorithms like DDPG, TD3, or SAC."
    ],
    "key_takeaways": [
        "Q-Learning learns optimal action values Q*(s,a) off-policy via Bellman temporal-difference errors without requiring environment transition models.",
        "DQN scales Q-learning to complex continuous states by parameterizing Q-functions with deep neural networks that output values for all actions in one forward pass.",
        "Experience replay and frozen target networks resolve the 'deadly triad' of function approximation, bootstrapping, and off-policy data.",
        "Double DQN and Dueling DQN eliminate overestimation bias and separate state values from action advantages, creating a robust deep RL foundation."
    ],
    "tags": [
        "Reinforcement Learning",
        "Q-Learning",
        "Deep Q-Networks",
        "DQN",
        "Experience Replay",
        "Target Network",
        "Double DQN",
        "Epsilon-Greedy"
    ]
}

def update_concepts_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        concepts = json.load(f)
    
    found = False
    for i, c in enumerate(concepts):
        if c.get('id') == new_concept['id']:
            concepts[i] = new_concept
            found = True
            break
            
    if not found:
        concepts.append(new_concept)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(concepts, f, indent=2, ensure_ascii=False)
        f.write('\n')
        
    print(f"Updated {filepath} successfully (found={found}, total={len(concepts)})")

update_concepts_file('src/data/concepts.json')
update_concepts_file('scripts/data_sources/all_concepts.json')
