# -*- coding: utf-8 -*-
"""
Script to modernize and standardize concept_actor_critic_ppo in src/data/concepts.json
and scripts/data_sources/all_concepts.json.
"""

import json

new_concept = {
    "id": "concept_actor_critic_ppo",
    "title": "Actor-Critic Architectures (A2C & PPO)",
    "topic_id": "dl_rl_foundations",
    "topic_label": "Reinforcement Learning (RL) & Decision Foundations",
    "category": "dl",
    "category_label": "Deep Learning Foundations",
    "raw_subtopic": "Actor-Critic Architectures (A2C & PPO)",
    "def": "Actor-Critic architectures are a class of reinforcement learning algorithms that combine a parameterized policy (the Actor) with a learned state-value function (the Critic) to compute low-variance advantage estimates A(s,a) = Q(s,a) - V(s). Advantage Actor-Critic (A2C) executes synchronous multi-environment updates, while Proximal Policy Optimization (PPO) stabilizes training via a clipped probability-ratio surrogate objective that bounds policy shifts across multiple minibatch epochs.",
    "definition": "In modern reinforcement learning, Actor-Critic architectures bridge policy-based and value-based methods to overcome the high sample variance of pure Monte Carlo policy gradients (REINFORCE) and the instability of pure value-function approximation (DQN). The framework bifurcates the agent into two interacting neural networks: (1) The Actor, parameterized by theta, directly models behavioral policy pi_theta(a|s) to sample actions, and (2) The Critic, parameterized by phi, models the state-value function V_phi(s) to evaluate environmental states and provide a baseline for credit assignment. The key training signal is the Advantage Function A^pi(s,a) = Q^pi(s,a) - V^pi(s), which quantifies whether a chosen action yielded returns superior or inferior to expected state performance. Advantage Actor-Critic (A2C) computes advantages via 1-step or k-step temporal-difference (TD) errors and executes synchronous updates across parallel environment rollouts. Proximal Policy Optimization (PPO; Schulman et al., 2017) further refines this architecture by resolving the policy instability problem. By defining the probability ratio r_t(theta) = pi_theta(a_t|s_t) / pi_theta_old(a_t|s_t) and introducing a clipped surrogate objective min(r_t A_t, clip(r_t, 1 - epsilon, 1 + epsilon) A_t), PPO limits the incentive for destructively large policy displacements. Combined with Generalized Advantage Estimation (GAE(gamma, lambda)), PPO enables sample-efficient reuse of rollout data across multiple minibatch optimization epochs, representing the industrial gold standard for both continuous robotic control and reinforcement learning from human feedback (RLHF).",
    "simple_summary": "Think of an Actor-Critic system as a movie director and an actor rehearsing on stage. The Actor makes creative choices and performs actions (e.g., turning left, accelerating, or swinging a tennis racket). The Critic sits in the audience and acts as the evaluator, judging how promising the current situation looks based on years of experience. Instead of waiting for the entire movie to be released to find out if an acting choice was good (like REINFORCE does), the Critic gives instant feedback: 'That movement was 3.8 points better than average!' This is the Advantage signal. In Advantage Actor-Critic (A2C), multiple actors rehearse in parallel studios simultaneously, and the director updates their script in lockstep. But what happens if the actor changes their style too radically after one rehearsal and completely ruins their technique? That is where Proximal Policy Optimization (PPO) shines: PPO puts mathematical guardrails (a clipping boundary, usually around 20%) on how much the actor's habits can change in one practice session. PPO prevents catastrophic policy collapse and allows the model to safely review and practice on the same rehearsal footage multiple times.",
    "definition_bullets": [
        "Actor-Critic Separation: Decouples action generation (Actor policy pi_theta) from state evaluation (Critic value function V_phi), dramatically slashing gradient variance.",
        "Advantage Function Credit Assignment: Measures relative action quality A^pi(s,a) = Q(s,a) - V(s); positive advantages increase action probabilities, while negative advantages reduce them.",
        "A2C Synchronous Architecture: Executes coordinated parallel environment rollouts, training a shared or dual-headed network via a unified loss combining actor, critic, and entropy terms.",
        "Generalized Advantage Estimation (GAE): Blends multi-step TD errors via decay parameter lambda in [0, 1] to achieve optimal bias-variance trade-offs in advantage estimation.",
        "PPO Clipped Surrogate Objective: Restricts policy updates via min(r_t A_t, clip(r_t, 1 - epsilon, 1 + epsilon) A_t), preventing destructive policy updates and enabling multi-epoch minibatch reuse."
    ],
    "core_terms": [
        {
            "term": "Actor-Critic Paradigm",
            "what_is_it": "A hybrid reinforcement learning framework uniting policy search and value approximation.",
            "definition": "An architecture where an Actor network pi_theta(a|s) outputs action probabilities, and a Critic network V_phi(s) outputs scalar state values to compute bootstrapped advantage targets for policy updates.",
            "analogy": "A student (Actor) solving math problems on a chalkboard, guided by an expert teacher (Critic) pointing out whether each step is better or worse than typical attempts.",
            "why_it_matters": "Combines the continuous-action capabilities of policy gradients with the lower sample variance and faster convergence of value bootstrapping."
        },
        {
            "term": "Advantage Function A(s,a)",
            "what_is_it": "A baseline-centered metric quantifying relative action performance.",
            "definition": "The difference A^pi(s,a) = Q^pi(s,a) - V^pi(s), representing how much better or worse taking action a in state s is compared to the expected return of following policy pi from state s.",
            "analogy": "Performance relative to par in golf: shooting 3 strokes on a par-4 hole represents a 1-under advantage (-1 relative to par, or +1 stroke advantage).",
            "why_it_matters": "Acts as the directional steering wheel for the Actor: positive advantages reward actions, negative advantages penalize them, and zero advantages leave policies stable."
        },
        {
            "term": "Generalized Advantage Estimation (GAE)",
            "what_is_it": "An exponential weighting framework for multi-step temporal-difference advantages.",
            "definition": "An advantage estimator formulated as A_t^GAE(gamma, lambda) = sum_{l=0}^inf (gamma * lambda)^l delta_{t+l}^V, where delta_t^V = r_t + gamma V(s_{t+1}) - V(s_t) is the 1-step TD error.",
            "analogy": "Exponential moving average of financial forecasts: weighting tomorrow's data heavily while giving decaying credibility to estimates further down the timeline.",
            "why_it_matters": "Provides a smooth dial between low-variance 1-step TD estimation (lambda = 0) and zero-bias Monte Carlo rollouts (lambda = 1), optimizing sample efficiency in PPO."
        },
        {
            "term": "PPO Clipped Surrogate Objective",
            "what_is_it": "A bounded policy loss function preventing excessive policy divergence.",
            "definition": "A pessimistic objective L^CLIP(theta) = E[min(r_t(theta) A_t, clip(r_t(theta), 1 - epsilon, 1 + epsilon) A_t)] that truncates the probability ratio r_t = pi_theta / pi_old to [1 - epsilon, 1 + epsilon].",
            "analogy": "A speed governor installed on an engine: allowing acceleration when safe, but physically preventing the RPM from shooting into the redline zone.",
            "why_it_matters": "Prevents catastrophic performance collapse in policy gradient optimization, enabling safe, sample-efficient reuse of collected rollout data across multiple gradient epochs."
        },
        {
            "term": "Policy Entropy Bonus H(π)",
            "what_is_it": "A regularization term promoting exploratory distribution spread.",
            "definition": "An information-theoretic entropy term H(pi(s)) = -sum_a pi(a|s) log pi(a|s) added to the objective with coefficient c_e to prevent the policy from collapsing prematurely into a deterministic distribution.",
            "analogy": "A company investing 10% of its budget into experimental R&D to avoid becoming locked into a single product line that might soon become obsolete.",
            "why_it_matters": "Maintains behavioral exploration early in training, preventing the Actor from getting trapped in suboptimal local optima with near-zero exploration probability."
        }
    ],
    "symbol_guide": [
        {
            "symbol": "π_θ(a|s)",
            "name": "Actor Policy Distribution",
            "meaning": "Parameterized probability distribution mapping environmental states s to action probabilities or Gaussian parameters."
        },
        {
            "symbol": "V_ϕ(s)",
            "name": "Critic Value Function",
            "meaning": "Estimated expected discounted cumulative return from state s, parameterized by neural weights phi."
        },
        {
            "symbol": "A_t",
            "name": "Advantage Signal",
            "meaning": "Quantifies the margin by which the taken action outperformed or underperformed expected state value."
        },
        {
            "symbol": "r_t(θ)",
            "name": "Probability Ratio",
            "meaning": "Ratio r_t = pi_theta(a_t|s_t) / pi_theta_old(a_t|s_t) measuring the magnitude of policy displacement."
        },
        {
            "symbol": "ϵ",
            "name": "PPO Clip Parameter (epsilon)",
            "meaning": "Hyperparameter (typically 0.1 to 0.3) setting the maximum allowable unconstrained ratio deviation."
        },
        {
            "symbol": "λ",
            "name": "GAE Bias-Variance Parameter",
            "meaning": "Exponential decay factor in [0, 1] balancing 1-step TD bootstrapping (lambda=0) and Monte Carlo rollouts (lambda=1)."
        },
        {
            "symbol": "H(π_θ)",
            "name": "Policy Entropy",
            "meaning": "Measurement of stochastic randomness in the action distribution, regularized to sustain exploration."
        }
    ],
    "formula": "$$\\text{1-Step Temporal Difference Advantage: } \\hat{A}_t = r_t + \\gamma (1 - d_t) V_\\phi(S_{t+1}) - V_\\phi(S_t)$$\n\n$$\\text{Generalized Advantage Estimation (GAE): } \\hat{A}_t^{\\text{GAE}}(\\gamma, \\lambda) = \\sum_{l=0}^{\\infty} (\\gamma \\lambda)^l \\delta_{t+l}^V, \\quad \\delta_t^V = r_t + \\gamma (1 - d_t) V(S_{t+1}) - V(S_t)$$\n\n$$\\text{A2C Total Multi-Task Loss: } \\mathcal{L}_{\\text{A2C}}(\\theta, \\phi) = \\mathcal{L}_{\\text{actor}}(\\theta) + c_v \\mathcal{L}_{\\text{critic}}(\\phi) - c_e \\mathcal{H}(\\pi_\\theta)$$\n\n$$\\text{PPO Probability Ratio: } r_t(\\theta) = \\frac{\\pi_\\theta(A_t \\mid S_t)}{\\pi_{\\theta_{\\text{old}}}(A_t \\mid S_t)} = \\exp\\left( \\log \\pi_\\theta(A_t \\mid S_t) - \\log \\pi_{\\theta_{\\text{old}}}(A_t \\mid S_t) \\right)$$\n\n$$\\text{PPO Clipped Surrogate Objective: } L^{\\text{CLIP}}(\\theta) = \\hat{\\mathbb{E}}_t \\left[ \\min\\left( r_t(\\theta) \\hat{A}_t, \\, \\text{clip}(r_t(\\theta), 1 - \\epsilon, 1 + \\epsilon) \\hat{A}_t \\right) \\right]$$\n\n$$\\text{PPO Total Optimization Objective: } \\mathcal{L}_{\\text{PPO}}(\\theta, \\phi) = - L^{\\text{CLIP}}(\\theta) + c_1 \\mathbb{E}_t \\left[ (V_\\phi(S_t) - V_t^{\\text{target}})^2 \\right] - c_2 \\mathbb{E}_t [\\mathcal{H}(\\pi_\\theta(\\cdot \\mid S_t))]$$",
    "logic": "The progression from REINFORCE to Actor-Critic methods, and subsequently to PPO, represents the resolution of two fundamental challenges in deep reinforcement learning: variance reduction and optimization stability. In classical REINFORCE, policy gradient updates use raw empirical returns G_t. Because G_t accumulates stochastic environmental transitions and action choices across an entire trajectory, its gradient estimator exhibits extreme variance, demanding millions of environment interactions. The Actor-Critic framework replaces full Monte Carlo returns with a learned Critic network V_phi(s). By evaluating the Advantage A(s,a) = r + gamma V_phi(s') - V_phi(s), the actor receives credit assignment immediately at each step without waiting for episode termination, slashing variance while maintaining low bias if the critic is well-trained. Advantage Actor-Critic (A2C) standardizes this concept into a synchronous, multi-environment architecture where multiple parallel agent threads collect rollouts simultaneously, aggregating experience to update a shared neural backbone with an actor policy head and critic value head. The loss function balances three distinct gradients: the policy loss weighted by advantages, the critic mean-squared error loss, and an entropy regularization penalty that prevents policy collapse into premature determinism. However, standard A2C still takes first-order gradient steps on on-policy data: each rollout can only be used for a single gradient update before becoming stale, because large parameter shifts alter action probabilities drastically and can trigger catastrophic policy divergence. Proximal Policy Optimization (PPO) resolves this dilemma by constructing a surrogate objective that allows multiple epochs of minibatch SGD over the same collected rollout. Using importance sampling, PPO defines the probability ratio r_t(theta) = pi_theta / pi_old. If an action achieved positive advantage (A_t > 0), increasing its probability improves the objective; however, PPO clips r_t at 1 + epsilon, removing any incentive to push the ratio higher and preventing overconfident policy jumps. Conversely, if an action yielded negative advantage (A_t < 0), PPO clips r_t at 1 - epsilon, limiting the penalty if the probability has already dropped significantly. When paired with Generalized Advantage Estimation (GAE(gamma, lambda)), which smoothly blends 1-step TD bootstrapping with multi-step returns, PPO achieves unprecedented training stability across continuous robotics, visual navigation, and large language model alignment (RLHF).",
    "example": "Consider training an autonomous quadcopter drone to navigate through a dense forest with wind turbulence. The state space S includes 3D velocity, gyroscope angular rates, distance sensors to surrounding trees, and goal waypoint coordinates. The action space A consists of 4 continuous motor thrust commands. In an Actor-Critic architecture, the Actor network outputs the mean and variance of a 4D Gaussian distribution for rotor thrust, while the Critic network estimates how many total seconds the drone will survive without crashing from the current state. When the drone executes a sharp bank to avoid a sudden tree branch, it receives r = +3 and transitions to a clear corridor where V_phi(s') = 12.0. With gamma = 0.9 and previous state value V_phi(s) = 10.0, the calculated advantage is A_t = 3 + 0.9(12.0) - 10.0 = +3.8. In PPO, this high positive advantage reinforces the banking maneuver across 4 minibatch epochs, but the clip boundary (epsilon = 0.2) stops the probability ratio from exceeding 1.20, ensuring the drone does not over-correct into an uncontrollable roll.",
    "numerical_example": "Step 1: One-Step Temporal Difference Advantage Calculation (Matching User Notes)\nSuppose a critic estimates current state value V(s) = 10.0.\nThe agent executes action 'turn_right', receives reward r = +3.0, and transitions to state s' where the critic predicts V(s') = 12.0.\nGiven discount factor gamma = 0.9:\n  - Estimated Current State Value: V(s) = 10.0\n  - Immediate Observed Reward:     r = 3.0\n  - Next State Estimated Value:    V(s') = 12.0\nCalculate One-Step Advantage Target A_hat:\n  A_hat = r + gamma * V(s') - V(s)\n  A_hat = 3.0 + 0.9 * (12.0) - 10.0\n  A_hat = 3.0 + 10.8 - 10.0 = 13.8 - 10.0 = +3.8\nResult: The action yielded an advantage of +3.8, proving it outperformed the policy's average baseline expectation.\n\nStep 2: Generalized Advantage Estimation (GAE) Multi-Step Induction Walkthrough\nConsider a 3-step rollout with discount gamma = 0.99 and GAE parameter lambda = 0.95:\nSuppose calculated 1-step TD errors are delta_0 = +1.0, delta_1 = -0.5, and delta_2 = +2.0 (with terminal s_3 where delta_3 = 0):\n  - Step 2 GAE: A_2^GAE = delta_2 = +2.0\n  - Step 1 GAE: A_1^GAE = delta_1 + (gamma * lambda) * A_2^GAE\n                 gamma * lambda = 0.99 * 0.95 = 0.9405\n                 A_1^GAE = -0.5 + 0.9405 * (2.0) = -0.5 + 1.881 = +1.381\n  - Step 0 GAE: A_0^GAE = delta_0 + (gamma * lambda) * A_1^GAE\n                 A_0^GAE = 1.0 + 0.9405 * (1.381) = 1.0 + 1.2988 = +2.2988\nNotice how GAE smoothly blends multi-step information with exponential decay (gamma * lambda)^l.\n\nStep 3: PPO Clipped Surrogate Objective Numerical Cases (Matching User Notes)\nLet clipping parameter epsilon = 0.2 (clipping interval [1 - epsilon, 1 + epsilon] = [0.8, 1.2]).\n\nCase A: Positive Advantage with Moderate Ratio Shift\n  - Advantage: A_t = +2.5\n  - Old policy prob: pi_old = 0.20, New policy prob: pi_new = 0.22\n  - Ratio: r_t = 0.22 / 0.20 = 1.10\n  - Clipped ratio: clip(1.10, 0.8, 1.2) = 1.10\n  - Unclipped term: 1.10 * 2.5 = 2.75 | Clipped term: 1.10 * 2.5 = 2.75\n  - Objective: min(2.75, 2.75) = 2.75 (Unclipped update accepted!)\n\nCase B: Positive Advantage with Excessive Ratio Jump\n  - Advantage: A_t = +2.5\n  - Old prob: pi_old = 0.20, New prob: pi_new = 0.30\n  - Ratio: r_t = 0.30 / 0.20 = 1.50\n  - Clipped ratio: clip(1.50, 0.8, 1.2) = 1.20\n  - Unclipped term: 1.50 * 2.5 = 3.75 | Clipped term: 1.20 * 2.5 = 3.00\n  - Objective: min(3.75, 3.00) = 3.00 (Clipped! Further probability inflation gives ZERO additional gradient!)\n\nCase C: Negative Advantage with Large Probability Drop\n  - Advantage: A_t = -2.0\n  - Old prob: pi_old = 0.50, New prob: pi_new = 0.25\n  - Ratio: r_t = 0.25 / 0.50 = 0.50\n  - Clipped ratio: clip(0.50, 0.8, 1.2) = 0.80\n  - Unclipped term: 0.50 * (-2.0) = -1.00 | Clipped term: 0.80 * (-2.0) = -1.60\n  - Objective: min(-1.00, -1.60) = -1.60 (Clipped! Limits excessive punishment on the policy!)\n\nStep 4: PyTorch PPO Policy Loss Implementation (Matching User Notes)\n```python\nimport torch\nimport torch.nn as nn\nfrom torch.distributions import Categorical\n\ndef ppo_policy_loss(distribution, actions, old_log_probs, advantages, clip_eps=0.2):\n    # 1. Evaluate log-probability under new policy theta\n    new_log_probs = distribution.log_prob(actions)\n    # 2. Compute probability ratio r_t = pi_theta / pi_theta_old\n    ratio = torch.exp(new_log_probs - old_log_probs)\n    # 3. Formulate unclipped and clipped surrogate objectives\n    unclipped = ratio * advantages\n    clipped = torch.clamp(ratio, 1.0 - clip_eps, 1.0 + clip_eps) * advantages\n    # 4. Pessimistic minimum (negated for gradient descent minimization)\n    policy_loss = -torch.minimum(unclipped, clipped).mean()\n    return policy_loss\n\n# Verification test with Case B numbers\nold_lp = torch.tensor([torch.log(torch.tensor(0.20))])\nnew_lp = torch.tensor([torch.log(torch.tensor(0.30))])\nadv = torch.tensor([2.5])\n\nratio = torch.exp(new_lp - old_lp)  # 1.50\nuncl = ratio * adv                   # 3.75\ncl = torch.clamp(ratio, 0.8, 1.2) * adv  # 3.00\nloss = -torch.minimum(uncl, cl).mean()    # -3.00\nprint(f'PPO Ratio: {ratio.item():.2f}, Expected Loss: {loss.item():.2f}')\n```\n\nStep 5: A2C Multi-Task Total Loss Calculation\nSuppose in a batch of 64 transitions:\n  - Actor Policy Loss:  L_actor  = -1.85\n  - Critic MSE Loss:    L_critic = 0.40  (value error)\n  - Policy Entropy:     H(pi)    = 1.15  (natural nats of entropy)\n  - Hyperparameters:    c_v = 0.5 (critic coeff), c_e = 0.01 (entropy coeff)\nCalculate Combined A2C Loss:\n  L_total = L_actor + c_v * L_critic - c_e * H(pi)\n  L_total = -1.85 + 0.5 * (0.40) - 0.01 * (1.15)\n  L_total = -1.85 + 0.20 - 0.0115 = -1.6615",
    "types_header": "Advanced Policy Gradient Architectures",
    "types_badge": "Actor-Critic & Trust-Region Methods",
    "quick_types": [
        {
            "name": "Advantage Actor-Critic (A2C)",
            "description": "Synchronous, deterministic parallel-environment architecture updating shared network backbones via multi-step TD advantages without experience replay."
        },
        {
            "name": "Proximal Policy Optimization (PPO-Clip)",
            "description": "State-of-the-art policy optimization algorithm bounding probability ratios via clipping, enabling multiple epochs of minibatch SGD per rollout with high empirical stability."
        },
        {
            "name": "Trust Region Policy Optimization (TRPO)",
            "description": "Precursor to PPO that enforces hard statistical trust-region constraints using average Kullback-Leibler (KL) divergence and Fisher information matrix conjugate gradients."
        },
        {
            "name": "Continuous Gaussian Actor-Critic",
            "description": "Continuous-action formulation where the actor outputs Gaussian mean mu(s) and log standard deviation log_sigma(s), optimizing robotic locomotion and flight control."
        }
    ],
    "connected_logic": [
        {
            "title": "Actor-Critic Bootstrapping & Variance Reduction",
            "description": "Synergistic relationship between policy-based action generation and value-based state evaluation.",
            "points": [
                "Substitutes high-variance Monte Carlo episode returns with low-variance 1-step or k-step TD advantage estimates.",
                "Enables online learning at each environment step without requiring complete episode termination rollouts.",
                "Maintains a symbiotic balance: the Critic improves advantage quality while the Actor discovers high-value states."
            ]
        },
        {
            "title": "GAE Multi-Step Advantage Formulation",
            "description": "Exponentially decaying temporal-difference mechanics balancing bias and variance in advantage estimation.",
            "points": [
                "Computes GAE via recursive backward accumulation A_t = delta_t + (gamma * lambda) A_{t+1}.",
                "Interpolates between low-variance 1-step TD estimation (lambda = 0) and zero-bias Monte Carlo returns (lambda = 1).",
                "Forms the universal advantage estimator standard for PPO across discrete and continuous benchmark tasks."
            ]
        },
        {
            "title": "PPO Clipped Surrogate Optimization",
            "description": "Pessimistic clipping mechanics preventing catastrophic policy collapse during multi-epoch minibatch updates.",
            "points": [
                "Quantifies policy displacement using importance ratio r_t(theta) = pi_theta(a|s) / pi_theta_old(a|s).",
                "Applies sign-sensitive clipping min(r_t A_t, clip(r_t, 1-eps, 1+eps) A_t) to nullify gradients from excessive updates.",
                "Enables safe reuse of rollout experience across 4 to 10 minibatch optimization epochs."
            ]
        },
        {
            "title": "A2C Synchronous Multi-Environment Architecture",
            "description": "Parallel rollout execution and multi-task loss balancing across actor, critic, and entropy objectives.",
            "points": [
                "Gathers synchronized experiences across N parallel environment instances, breaking temporal correlation without replay buffers.",
                "Combines policy surrogate loss, critic value regression MSE, and entropy bonus into a unified gradient graph.",
                "Employs policy entropy regularization H(pi) to prevent premature deterministic policy collapse."
            ]
        }
    ],
    "pitfalls": [
        "Confusing State Value with Advantage: State Value V(s) is the expected total return from a state; Advantage A(s,a) = Q(s,a) - V(s) measures how much better a specific action is compared to that expectation.",
        "Using Raw Immediate Rewards as Advantages: Setting A_t = r_t ignores future discounted value V(s_{t+1}) and misleads the actor into myopic single-step greed.",
        "Updating Old Log-Probabilities During PPO Optimization: Overwriting old_log_probs inside the minibatch loop resets the ratio r_t to 1.0, destroying PPO's clipping mechanism and causing divergence.",
        "Bootstrapping Past True Terminal States: Failing to mask next-state values (1 - done) at true environment termination allows nonexistent future value to corrupt advantage calculations.",
        "Neglecting Policy Entropy Regularization: Setting entropy coefficient c_e = 0 can cause policy distributions to collapse to near 1.0 on a single action within early iterations, extinguishing exploration."
    ],
    "key_takeaways": [
        "Actor-Critic architectures unite policy optimization (Actor) with state evaluation (Critic) to achieve low-variance advantage-based credit assignment.",
        "A2C executes synchronous multi-environment rollouts and optimizes a joint objective balancing policy advantage, critic MSE, and entropy exploration.",
        "PPO establishes industry-standard stability by clipping the probability ratio r_t within [1 - epsilon, 1 + epsilon], enabling multi-epoch minibatch training without catastrophic collapse.",
        "Generalized Advantage Estimation (GAE) provides the optimal bias-variance trade-off parameter lambda, bridging 1-step TD bootstrapping with Monte Carlo returns."
    ],
    "tags": [
        "Reinforcement Learning",
        "Actor-Critic",
        "A2C",
        "PPO",
        "GAE",
        "Proximal Policy Optimization",
        "Advantage Function",
        "PyTorch"
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
