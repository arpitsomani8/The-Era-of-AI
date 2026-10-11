# -*- coding: utf-8 -*-
"""
Script to modernize and standardize concept_policy_gradients_reinforce in src/data/concepts.json
and scripts/data_sources/all_concepts.json.
"""

import json

new_concept = {
    "id": "concept_policy_gradients_reinforce",
    "title": "Policy Gradients & REINFORCE Algorithm",
    "topic_id": "dl_rl_foundations",
    "topic_label": "Reinforcement Learning (RL) & Decision Foundations",
    "category": "dl",
    "category_label": "Deep Learning Foundations",
    "raw_subtopic": "Policy Gradients & REINFORCE Algorithm",
    "def": "Policy Gradients are a foundational family of reinforcement learning algorithms that directly parameterize and optimize behavioral policies pi_theta(a|s) via gradient ascent on expected return J(theta) without requiring intermediate action-value functions. REINFORCE is the canonical Monte Carlo policy gradient algorithm that updates network weights using sampled complete trajectory returns weighted by log-action gradients, stabilized via state-dependent baselines.",
    "definition": "In reinforcement learning, Policy Gradient methods directly optimize a parameterized policy pi_theta(a|s) = P(A_t = a | S_t = s; theta) to maximize the expected cumulative trajectory return J(theta) = E_{tau ~ pi_theta}[G_0]. Unlike value-based approaches such as Q-learning and DQN that learn action values and select greedy actions, policy gradients bypass value function approximation and directly output action probability distributions (for discrete actions via softmax logits) or continuous distribution parameters (such as the mean and variance of a Gaussian distribution for robotic joint control). The core mathematical foundation is the Policy Gradient Theorem, which proves that the gradient of expected return nabla_theta J(theta) can be computed as E_{pi_theta}[G_t nabla_theta log pi_theta(A_t | S_t)] without requiring knowledge of or differentiation through environmental transition dynamics P(s'|s,a). REINFORCE (Williams, 1992) is the episodic Monte Carlo implementation of this theorem: the agent rolls out complete trajectories, computes discounted empirical returns G_t from step t onward, and updates policy parameters in the direction that reinforces actions yielding above-average returns. While REINFORCE provides an unbiased gradient estimator, Monte Carlo trajectory rollouts inherently suffer from high variance; introducing an action-independent baseline b(s) (such as a learned value critic V_phi(s)) reduces variance without introducing gradient bias, providing the direct architectural bridge to modern Actor-Critic algorithms like A2C and PPO.",
    "simple_summary": "Imagine teaching a basketball player how to shoot a free throw. In value-based methods (like Q-learning), the player would attempt to calculate a numerical score for every conceivable millimeter of arm angle, finger snap, and knee bend before taking a shot. In policy gradient methods, the player skips the exhaustive scorecard and directly learns the shooting motion itself! The neural network outputs probabilities for each movement. If a shot swishes through the net (high return), the brain uses calculus to slightly increase the probability of repeating that exact motor sequence in similar court situations. If a shot misses badly, the likelihood of that movement is dialed down. The REINFORCE algorithm is the classic playbook for this: play an entire game, look back at which shots yielded victories, and adjust your muscle memory accordingly. To prevent wildly inconsistent updates, a 'baseline' is subtracted so the player only reinforces shots that were genuinely better than their average skill level.",
    "definition_bullets": [
        "Direct Policy Parameterization: Models policy distributions pi_theta(a|s) directly using deep neural networks, supporting continuous action controls and stochastic exploration.",
        "The Policy Gradient Theorem: Proves nabla_theta J(theta) = E[G_t nabla_theta log pi_theta(A_t|S_t)], enabling model-free optimization without differentiating transition dynamics.",
        "Log-Derivative Score Trick: Converts intractable trajectory distribution gradients into expectations of log-probabilities via nabla pi = pi nabla log pi.",
        "Episodic Monte Carlo Execution: REINFORCE collects complete episodes to evaluate exact discounted returns G_t before executing gradient ascent parameter updates.",
        "Variance Reduction via Baselines: Subtracts an action-independent state baseline b(s) to compute advantage A_t = G_t - b(s), dramatically stabilizing training without biasing gradients."
    ],
    "core_terms": [
        {
            "term": "Policy Gradient Theorem",
            "what_is_it": "The foundational mathematical theorem enabling model-free policy optimization.",
            "definition": "A theorem proving that the gradient of expected cumulative return J(theta) with respect to policy parameters theta equals the expected value of the product of action return G_t and the log-action gradient: nabla_theta J(theta) = E_{pi_theta}[sum_t G_t nabla_theta log pi_theta(A_t | S_t)].",
            "analogy": "A coach advising an athlete: you do not need to model the laws of aerodynamics to improve; you just observe which swings scored runs and practice those swings more often.",
            "why_it_matters": "Eliminates the impossible requirement of computing derivatives through environmental state transitions P(s'|s,a), making deep RL feasible in complex black-box simulators."
        },
        {
            "term": "Log-Derivative (Score Function) Trick",
            "what_is_it": "The algebraic identity enabling expectation-based differentiation.",
            "definition": "The mathematical identity nabla_theta pi_theta(a|s) = pi_theta(a|s) nabla_theta log pi_theta(a|s), derived from the derivative rule d/dx log f(x) = f'(x) / f(x).",
            "analogy": "Transforming multiplication of probabilities across a chain into a simple addition of logs, allowing easy calculus without numeric underflow.",
            "why_it_matters": "Allows expressing the derivative of an intractable expectation as an expectation of derivatives, enabling sample-based Monte Carlo estimation."
        },
        {
            "term": "REINFORCE Algorithm (Monte Carlo Policy Gradient)",
            "what_is_it": "The canonical episodic on-policy reinforcement learning algorithm.",
            "definition": "An on-policy policy gradient method that samples full trajectories using current policy pi_theta, calculates discounted returns G_t in reverse from episode termination, and applies stochastic gradient ascent.",
            "analogy": "A theatrical troupe rehearsing a full play from start to finish before taking director notes on which scenes elicited audience applause.",
            "why_it_matters": "Serves as the theoretical and algorithmic bedrock from which all modern policy optimization methods (Actor-Critic, TRPO, PPO) are derived."
        },
        {
            "term": "State Baseline b(s)",
            "what_is_it": "A variance-reduction scalar function subtracted from returns.",
            "definition": "Any function b(s) depending on state s but independent of chosen action a, subtracted from empirical return G_t in the policy gradient update: nabla_theta J = E[(G_t - b(S_t)) nabla_theta log pi_theta(A_t|S_t)].",
            "analogy": "Grading on a curve: your test score is evaluated relative to the class average, ensuring a hard test where everyone scores 50% does not punish good students.",
            "why_it_matters": "Drastically decreases gradient sample variance while leaving the mathematical expected gradient provably unbiased, since E_{a}[b(s) nabla_theta log pi_theta(a|s)] = 0."
        },
        {
            "term": "Advantage Function A(s,a)",
            "what_is_it": "A metric quantifying how much better a specific action is compared to baseline expectations.",
            "definition": "The difference A(s,a) = Q(s,a) - V(s), or its Monte Carlo empirical realization A_t = G_t - b(S_t), indicating whether an action yielded superior or inferior return relative to average state value.",
            "analogy": "Beating market expectations: a stock gaining 5% when the general market dropped 2% represents a strong positive advantage of +7%.",
            "why_it_matters": "Provides directional signals: positive advantages increase action probabilities; negative advantages penalize actions even if raw rewards were positive."
        }
    ],
    "symbol_guide": [
        {
            "symbol": "π_θ(a|s)",
            "name": "Parameterized Policy",
            "meaning": "Conditional probability distribution over actions a given state s, parameterized by neural weights theta."
        },
        {
            "symbol": "J(θ)",
            "name": "Expected Trajectory Return",
            "meaning": "The objective scalar function to be maximized: expected cumulative discounted return across trajectories."
        },
        {
            "symbol": "G_t",
            "name": "Discounted Empirical Return",
            "meaning": "Sum of discounted rewards received from step t+1 through episode end: sum_{k=0} gamma^k R_{t+k+1}."
        },
        {
            "symbol": "∇_θ log π_θ(a|s)",
            "name": "Score Function (Policy Gradient)",
            "meaning": "Direction in parameter space that maximally increases the log-probability of taking action a in state s."
        },
        {
            "symbol": "b(s)",
            "name": "State Baseline",
            "meaning": "Action-independent reference value (often learned state-value V_phi(s)) subtracted to reduce variance."
        },
        {
            "symbol": "A_t",
            "name": "Advantage Estimate",
            "meaning": "Relative performance metric A_t = G_t - b(S_t) dictating magnitude and sign of policy updates."
        },
        {
            "symbol": "α",
            "name": "Policy Learning Rate",
            "meaning": "Step-size scalar controlling parameter displacement during stochastic gradient ascent."
        }
    ],
    "formula": "$$\\text{Expected Return Objective: } J(\\theta) = \\mathbb{E}_{\\tau \\sim \\pi_\\theta} [G_0] = \\int P(\\tau; \\theta) G(\\tau) d\\tau$$\n\n$$\\text{Policy Gradient Theorem: } \\nabla_\\theta J(\\theta) = \\mathbb{E}_{\\pi_\\theta} \\left[ \\sum_{t=0}^{T-1} G_t \\nabla_\\theta \\log \\pi_\\theta(A_t \\mid S_t) \\right]$$\n\n$$\\text{Log-Derivative Identity: } \\nabla_\\theta \\pi_\\theta(a \\mid s) = \\pi_\\theta(a \\mid s) \\frac{\\nabla_\\theta \\pi_\\theta(a \\mid s)}{\\pi_\\theta(a \\mid s)} = \\pi_\\theta(a \\mid s) \\nabla_\\theta \\log \\pi_\\theta(a \\mid s)$$\n\n$$\\text{REINFORCE Episodic Parameter Update: } \\theta \\leftarrow \\theta + \\alpha \\sum_{t=0}^{T-1} G_t \\nabla_\\theta \\log \\pi_\\theta(A_t \\mid S_t)$$\n\n$$\\text{REINFORCE with Baseline: } \\nabla_\\theta J(\\theta) = \\mathbb{E}_{\\pi_\\theta} \\left[ \\sum_{t=0}^{T-1} (G_t - b(S_t)) \\nabla_\\theta \\log \\pi_\\theta(A_t \\mid S_t) \\right]$$\n\n$$\\text{Unbiased Baseline Expectation Proof: } \\sum_{a \\in \\mathcal{A}} \\nabla_\\theta \\pi_\\theta(a \\mid s) b(s) = b(s) \\nabla_\\theta \\sum_{a} \\pi_\\theta(a \\mid s) = b(s) \\nabla_\\theta (1) = 0$$\n\n$$\\text{PyTorch Surrogate Loss Minimization: } \\mathcal{L}(\\theta) = - \\sum_{t=0}^{T-1} \\log \\pi_\\theta(A_t \\mid S_t) \\cdot \\hat{A}_t$$",
    "logic": "Policy Gradient methods provide the theoretical foundation for optimizing agent behavior directly in continuous and stochastic action domains. Unlike value-based architectures (Q-learning and DQN) which optimize scalar action-value functions and select actions via argmax, policy-based methods directly parameterize a conditional probability distribution pi_theta(a|s). In discrete action spaces, the network outputs unnormalized logits passed through a Softmax layer to construct a Categorical distribution. In continuous action domains, the network outputs the mean mu_theta(s) and standard deviation sigma_theta(s) of a multivariate Gaussian distribution, enabling smooth and direct continuous torque or velocity control that is impossible for discrete Q-tables. The central algorithmic challenge in policy optimization is that the objective J(theta) depends on parameter vector theta in two distinct ways: theta determines which actions are chosen, and the chosen actions determine which states are visited by the environment. Differentiating through environmental state transitions P(s'|s,a) is intractable in model-free settings. The Policy Gradient Theorem resolves this dilemma by employing the log-derivative trick: by multiplying and dividing the gradient of trajectory probabilities by P(tau; theta), the gradient of expected return simplifies to the expectation of the product of return G_t and the score function nabla_theta log pi_theta(A_t|S_t). The REINFORCE algorithm implements this theorem via episodic Monte Carlo rollouts: an agent interacts with the environment for an entire episode, accumulates rewards, and computes discounted returns G_t in backward induction. The policy parameters are then updated using stochastic gradient ascent: actions followed by high cumulative returns have their log-probabilities boosted, while actions followed by low returns have their log-probabilities reduced. However, because Monte Carlo returns compound stochasticity across all future steps, raw REINFORCE suffers from high gradient variance. Introducing an action-independent baseline b(s)—most commonly a learned state-value critic V_phi(s)—centers returns into advantages A_t = G_t - b(S_t). Subtracting b(s) is mathematically guaranteed to leave the expectation unbiased while drastically reducing gradient variance, forming the direct architectural bridge to Actor-Critic algorithms.",
    "example": "Consider training a robotic surgical needle insertion arm to stitch tissue. The state space S consists of high-resolution endoscopic visual features and 6-axis force feedback sensors. The action space A consists of continuous 3D force vectors [F_x, F_y, F_z] and needle roll angle. A value-based Q-learning algorithm would require discretizing the continuous 4D force-angle space into millions of discrete bins, causing severe discretization errors and latency. In contrast, a Policy Gradient network directly outputs the mean vector mu_theta(s) and standard deviation sigma_theta(s) of a 4D Gaussian distribution. When inserting the needle, sampling an action that achieves clean penetration with low tissue tear yields a high episode return G_t = +50. If the baseline expected return is b(s) = +20, the advantage is A_t = +30. The policy gradient update immediately shifts mu_theta(s) toward that successful force trajectory while reducing exploration variance sigma_theta(s), smoothly converging to superhuman surgical precision.",
    "numerical_example": "Step 1: Trajectory Discounted Return & Credit Assignment Walkthrough (Matching User Notes)\nConsider an agent completing a three-step trajectory with rewards r_1 = 1, r_2 = 2, and r_3 = 5, with discount factor gamma = 0.9.\nCompute empirical discounted returns G_t in reverse induction:\n  - Step 2 Return (t=2, terminal step):  G_2 = r_3 = 5.0\n  - Step 1 Return (t=1):                  G_1 = r_2 + gamma * G_2 = 2 + 0.9 * (5.0) = 2 + 4.5 = 6.5\n  - Step 0 Return (t=0, episode start):  G_0 = r_1 + gamma * G_1 = 1 + 0.9 * (6.5) = 1 + 5.85 = 6.85\nNotice how Step 0 receives credit for the distant r_3 = 5 reward discounted by gamma^2 = 0.81 (0.81 * 5 = 4.05).\n\nStep 2: Binary Sigmoid Policy Numerical Update (Matching User Notes)\nSuppose an agent chooses between Left and Right in state s using a scalar parameter theta with sigmoid probability:\n  p(Right) = sigma(theta) = 1 / (1 + e^{-theta})\nDerivative of log-probability for choosing Right:\n  d/d_theta [ log p ] = 1 - p\nGiven initial parameter theta = 0.0 (where p = 0.5):\n  - Agent chooses action:       Right\n  - Observed trajectory return: G = 4.0\n  - Policy learning rate:       alpha = 0.1\nCalculate single-sample REINFORCE update:\n  theta_new = theta_old + alpha * G * (1 - p)\n  theta_new = 0.0 + 0.1 * (4.0) * (1 - 0.5) = 0.0 + 0.1 * (4.0) * (0.5) = 0.0 + 0.2 = +0.2\nEvaluate updated action probability:\n  p_new(Right) = sigma(0.2) = 1 / (1 + e^{-0.2}) = 1 / (1 + 0.8187) = 1 / 1.8187 = 0.5498 (55.0%)\nThe positive return of +4 successfully reinforced the chosen action from 50.0% to 55.0%!\n\nStep 3: Complete PyTorch REINFORCE Implementation (Matching User Notes)\n```python\nimport torch\nimport torch.nn as nn\nfrom torch.distributions import Categorical\n\nclass PolicyNetwork(nn.Module):\n    def __init__(self, state_dim=4, n_actions=2):\n        super().__init__()\n        self.net = nn.Sequential(\n            nn.Linear(state_dim, 128), nn.ReLU(),\n            nn.Linear(128, n_actions)\n        )\n    def forward(self, x):\n        logits = self.net(x)\n        return Categorical(logits=logits)\n\npolicy = PolicyNetwork(4, 2)\noptimizer = torch.optim.Adam(policy.parameters(), lr=1e-3)\ngamma = 0.99\n\n# Simulated Episode Data: 3 steps\nstates = [torch.randn(4), torch.randn(4), torch.randn(4)]\nactions = [torch.tensor(1), torch.tensor(0), torch.tensor(1)]\nrewards = [1.0, 2.0, 5.0]\n\n# 1. Compute discounted returns in reverse\nreturns, G = [], 0.0\nfor r in reversed(rewards):\n    G = r + gamma * G\n    returns.insert(0, G)\nreturns = torch.tensor(returns, dtype=torch.float32)\n\n# 2. Return normalization for numerical variance reduction\nreturns = (returns - returns.mean()) / (returns.std(unbiased=False) + 1e-8)\n\n# 3. Evaluate log-probabilities and compute surrogate loss\nlog_probs = []\nfor s, a in zip(states, actions):\n    dist = policy(s)\n    log_probs.append(dist.log_prob(a))\nlog_probs = torch.stack(log_probs)\n\n# Minimize negative expected return (gradient ascent)\nloss = -(log_probs * returns).sum()\noptimizer.zero_grad()\nloss.backward()\noptimizer.step()\nprint(f'REINFORCE Surrogate Loss: {loss.item():.4f}')\n```\n\nStep 4: Baseline Variance Reduction & Advantage Arithmetic (Matching User Notes)\nSuppose a robot executes two separate episodes from the same initial state s_0 where the learned baseline is b(s_0) = 5.0:\n  - Episode 1: Action A_1 is taken, yielding high return G_1 = 8.0\n      Advantage: A_1 = G_1 - b(s_0) = 8.0 - 5.0 = +3.0 (Positive Advantage -> Boosts probability of A_1)\n  - Episode 2: Action A_2 is taken, yielding weak return G_2 = 2.0\n      Advantage: A_2 = G_2 - b(s_0) = 2.0 - 5.0 = -3.0 (Negative Advantage -> Penalizes probability of A_2)\nEven though Episode 2 had a positive absolute return (+2.0), subtracting baseline b=5 correctly identifies it as below average, preventing bad moves from being reinforced!\n\nStep 5: Mathematical Proof of Unbiased Baseline Expectation\nWe verify that subtracting b(s) does not change the expected gradient:\n  E_{a ~ pi}[ b(s) nabla_theta log pi_theta(a|s) ]\n  = sum_{a} pi_theta(a|s) * b(s) * (nabla_theta pi_theta(a|s) / pi_theta(a|s))\n  = b(s) * sum_{a} nabla_theta pi_theta(a|s)\n  = b(s) * nabla_theta [ sum_{a} pi_theta(a|s) ]\nSince probabilities sum to 1 (sum_{a} pi_theta(a|s) = 1) and the gradient of a constant is 0:\n  = b(s) * nabla_theta (1) = b(s) * 0 = 0 (Q.E.D.)",
    "types_header": "Policy-Based Reinforcement Learning Frameworks",
    "types_badge": "Policy Gradients & Trajectory Optimization",
    "quick_types": [
        {
            "name": "Vanilla REINFORCE (Monte Carlo Policy Gradient)",
            "description": "Foundational episodic on-policy algorithm weighting log-probability gradients directly by empirical discounted returns G_t."
        },
        {
            "name": "REINFORCE with State-Dependent Baseline",
            "description": "Variance-reduced variant subtracting a learned state-value baseline b(s) = V_phi(s) to compute advantage A_t = G_t - b(S_t) without introducing gradient bias."
        },
        {
            "name": "Continuous Gaussian Policy Gradients",
            "description": "Continuous-action policy formulation parameterizing Gaussian mean mu_theta(s) and standard deviation sigma_theta(s), directly optimizing robotics joint torques."
        },
        {
            "name": "Advantage Actor-Critic (A2C Bridge)",
            "description": "Transition from Monte Carlo rollouts to bootstrapping by employing a critic network to estimate 1-step TD advantages, eliminating the need to wait for episode termination."
        }
    ],
    "connected_logic": [
        {
            "title": "Likelihood-Ratio & Score Function Mechanics",
            "description": "Mathematical derivation of the policy gradient theorem using the log-derivative identity to bypass transition derivatives.",
            "points": [
                "Replaces intractable environmental transition gradients with expected log-action scores nabla_theta log pi_theta(a|s).",
                "Scales parameter updates by cumulative trajectory returns G_t, performing stochastic gradient ascent on J(theta).",
                "Naturally optimizes stochastic policies, avoiding premature determinism and enabling active environmental exploration."
            ]
        },
        {
            "title": "Episodic Monte Carlo Credit Assignment",
            "description": "Mechanisms governing how temporal returns from completed episodes propagate credit back to historical decisions.",
            "points": [
                "Computes discounted return G_t in reverse induction from terminal step T back to initial step 0.",
                "Discounts distant rewards by gamma^k, ensuring credit assignment prioritizes causally proximal actions.",
                "Suffers from sample variance because returns compound stochasticity across long unconstrained trajectories."
            ]
        },
        {
            "title": "State Baseline Variance Reduction",
            "description": "Analytical proof and practical application of subtracting action-independent baselines to stabilize policy gradients.",
            "points": [
                "Subtracts baseline b(s) from empirical return G_t to formulate centered advantage estimates A_t = G_t - b(s).",
                "Guaranteed to be unbiased because the expected baseline gradient across actions equals zero identically.",
                "Transforms positive returns into negative advantages if performance falls below expected state value V(s)."
            ]
        },
        {
            "title": "Actor-Critic & Modern Policy Optimization Bridge",
            "description": "Evolutionary trajectory from raw episodic REINFORCE to modern Actor-Critic algorithms like A2C and PPO.",
            "points": [
                "Replaces full-episode Monte Carlo returns with 1-step TD bootstrapped advantage targets r + gamma V(s') - V(s).",
                "Divides architecture into Actor (policy distribution) and Critic (value baseline), drastically slashing variance.",
                "Forms the direct mathematical foundation for Proximal Policy Optimization (PPO) and trust-region methods."
            ]
        }
    ],
    "pitfalls": [
        "Confusing Gradient Ascent with Minimization: Policy gradients maximize expected return J(theta); in PyTorch, you must minimize negative return loss = -(log_probs * returns).sum() to achieve gradient ascent.",
        "Attempting Off-Policy Updates Without Importance Sampling: REINFORCE is strictly on-policy; evaluating returns from past policy checkpoints without importance sampling ratio pi_theta / pi_old causes massive gradient divergence.",
        "Premature Policy Entropy Collapse: Fast learning rates can cause action probabilities to collapse to near 1.0 on a single action early in training, completely extinguishing exploration.",
        "Omitting Baseline or Return Normalization: Raw unbounded rewards cause gradient explosion or massive variance where all positive actions are reinforced regardless of relative quality.",
        "Credit Assignment Dilution in Long Episodes: In episodes with hundreds of steps, compounding Monte Carlo returns obscure which specific action caused a delayed reward, requiring Actor-Critic bootstrapping."
    ],
    "key_takeaways": [
        "Policy Gradients optimize expected returns directly by parameterizing behavioral policies pi_theta(a|s), excelling in continuous and stochastic action domains.",
        "The Policy Gradient Theorem employs the log-derivative trick to compute exact expected gradients without requiring environmental transition models.",
        "REINFORCE collects complete episodes and updates policy parameters in the direction of actions yielding high discounted returns G_t.",
        "Subtracting an action-independent baseline b(s) provably preserves unbiasedness while drastically reducing gradient variance, bridging REINFORCE to Actor-Critic."
    ],
    "tags": [
        "Reinforcement Learning",
        "Policy Gradients",
        "REINFORCE",
        "Monte Carlo",
        "Baseline",
        "Advantage",
        "PyTorch",
        "Actor-Critic"
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
