# -*- coding: utf-8 -*-
"""
Script to modernize and standardize concept_mdp_bellman in src/data/concepts.json
and scripts/data_sources/all_concepts.json.
"""

import json

new_concept = {
    "id": "concept_mdp_bellman",
    "title": "Markov Decision Processes (MDP) & Bellman Equation",
    "topic_id": "dl_rl_foundations",
    "topic_label": "Reinforcement Learning (RL) & Decision Foundations",
    "category": "dl",
    "category_label": "Deep Learning Foundations",
    "raw_subtopic": "Markov Decision Processes (MDP) & Bellman Equation",
    "def": "A Markov Decision Process (MDP) is the formal mathematical framework for modeling sequential decision-making under uncertainty, defined by the 5-tuple (S, A, P, R, gamma). The Bellman Equation decomposes value functions recursively into immediate rewards and discounted future state values, establishing the foundation for dynamic programming, value iteration, policy iteration, and reinforcement learning algorithms like Q-learning.",
    "definition": "In reinforcement learning and stochastic control theory, a Markov Decision Process (MDP) provides the rigorous mathematical formalism for sequential decision-making where outcomes are partly random and partly under the control of an autonomous agent. Defined as a 5-tuple M = (S, A, P, R, gamma), an MDP formalizes the discrete-time interaction loop: at each time step t, the agent observes environmental state s in S, selects action a in A according to policy pi(a|s), transitions to next state s' in S according to transition probability P(s'|s,a), and receives a scalar reward R(s,a,s'). The foundational assumption is the Markov Property: the conditional probability distribution of future states depends solely upon the present state and action, rendering the past history conditionally independent. The Bellman Equation provides the cornerstone mathematical identity of reinforcement learning by decomposing the expected cumulative return (discounted sum of rewards G_t) into a recursive relationship: the value of any state equals the expected immediate reward plus the discounted expected value of successor states. Distinguishing between Bellman Expectation Equations (which evaluate a fixed behavioral policy pi) and Bellman Optimality Equations (which characterize the unique optimal policy pi*), this recursive decomposition forms the theoretical foundation for dynamic programming algorithms (Value Iteration and Policy Iteration) and model-free temporal difference methods such as Q-learning and Deep Q-Networks (DQN).",
    "simple_summary": "Imagine training an autonomous delivery robot or an intelligent energy grid battery controller. At every moment, the agent asks two questions: 'Where am I right now?' (State) and 'Which action should I take?' (Action). Taking an action might yield an immediate small reward—like moving smoothly—or a large immediate bonus, like grabbing a package, but it might also risk driving into an obstacle or depleting the battery. An MDP is the formal rulebook of this world, specifying states, available actions, transition chances (including random wheel slips), and reward payouts. The Bellman Equation is the agent's wisdom calculator: it proves that the true value of being in any spot is not just the immediate prize you pick up on the spot, but the immediate reward PLUS the discounted future value of all future positions that spot enables you to reach. By breaking a lifetime of decisions into one step plus the future, the Bellman Equation allows machines to look ahead, avoid immediate gratification traps, and discover optimal long-term survival and success strategies.",
    "definition_bullets": [
        "MDP 5-Tuple Formulation: Formally structured as (S, A, P, R, gamma), defining states, actions, transition probability matrix P(s'|s,a), reward function R(s,a,s'), and discount factor gamma in [0, 1).",
        "The Markov Property: Assumes future transitions depend strictly on current state and action P(S_{t+1}|S_t, A_t) = P(S_{t+1}|S_t, A_t, S_{t-1}, ...), requiring informative state design.",
        "Recursive Return Decomposition: Total return G_t = sum_{k=0}^inf gamma^k R_{t+k+1} breaks into immediate reward R_{t+1} plus discounted return gamma G_{t+1}.",
        "Bellman Expectation vs. Optimality: Expectation equations average over policy actions and transitions to evaluate a policy; optimality equations apply max_{a} to discover the optimal policy.",
        "Foundation of RL & Dynamic Programming: Serves as the mathematical backbone for Value Iteration, Policy Iteration, Temporal Difference learning, and Q-learning updates."
    ],
    "core_terms": [
        {
            "term": "Markov Property",
            "what_is_it": "The memoryless conditional independence axiom of stochastic processes.",
            "definition": "The mathematical condition where the conditional probability distribution of future states of the process depends only upon the present state and action, and not on the sequence of preceding events: P(S_{t+1}|S_t, A_t) = P(S_{t+1}|S_t, A_t, S_{t-1}, ...).",
            "analogy": "A game of chess: the best next move depends solely on the current board arrangement, regardless of whether a knight arrived there via ten moves or three.",
            "why_it_matters": "Enables compact state representations and guarantees that optimal decision policies need only condition on current state features rather than exhaustive historical logs."
        },
        {
            "term": "Discount Factor (gamma)",
            "what_is_it": "A decay multiplier balancing immediate versus future reward utility.",
            "definition": "A real scalar hyperparameter gamma in [0, 1) that exponentially discounts rewards received k time steps into the future by gamma^k, ensuring mathematical convergence of infinite-horizon returns.",
            "analogy": "Financial interest and inflation: receiving $100 today is worth more than receiving $100 five years from now due to compounding opportunity and temporal uncertainty.",
            "why_it_matters": "Prevents infinite return sums in continuing tasks, bounds value functions mathematically, and controls whether an agent acts myopically (gamma near 0) or strategically farsighted (gamma near 1)."
        },
        {
            "term": "State-Value Function V(s)",
            "what_is_it": "The expected long-term return starting from a given state.",
            "definition": "The expected cumulative discounted return an agent will accumulate when starting in state s and following behavioral policy pi thereafter: V^pi(s) = E_pi[G_t | S_t = s].",
            "analogy": "The appraised market value of a house: not the cash found on the floor today, but the expected long-term utility and equity gained from living in it.",
            "why_it_matters": "Provides a comprehensive scalar evaluation of how favorable a situation is, allowing agents to navigate toward high-value regions of the environment."
        },
        {
            "term": "Action-Value Function Q(s,a)",
            "what_is_it": "The expected long-term return of executing a specific action in a state.",
            "definition": "The expected cumulative discounted return obtained by taking action a in state s, and subsequently following policy pi: Q^pi(s,a) = E_pi[G_t | S_t = s, A_t = a].",
            "analogy": "A crossroads fork in the road: evaluating the overall destination quality of taking the left turn versus the right turn before continuing your journey.",
            "why_it_matters": "Allows direct action ranking and greedy policy extraction without requiring access to environment transition probabilities P(s'|s,a), forming the core of Q-learning."
        },
        {
            "term": "Bellman Optimality Operator",
            "what_is_it": "A non-linear dynamic programming operator computing optimal values.",
            "definition": "A mathematical contraction mapping operator T* that maps value functions to updated value functions by taking the supremum over actions: (T* V)(s) = max_a sum_{s'} P(s'|s,a)[R(s,a,s') + gamma V(s')].",
            "analogy": "A master strategist always assuming optimal play: at every juncture, choosing the single move that yields the highest sum of immediate return and future victory.",
            "why_it_matters": "Guarantees monotonic convergence to a unique optimal value function V* via Banach's Fixed-Point Theorem, powering Value Iteration and deep reinforcement learning."
        }
    ],
    "symbol_guide": [
        {
            "symbol": "S",
            "name": "State Space",
            "meaning": "The complete set of all valid environmental states s in S observable by the agent."
        },
        {
            "symbol": "A",
            "name": "Action Space",
            "meaning": "The set of all possible decisions or motor actions a in A available to the agent."
        },
        {
            "symbol": "P(s'|s,a)",
            "name": "Transition Probability",
            "meaning": "The conditional probability of transitioning to state s' given current state s and action a."
        },
        {
            "symbol": "R(s,a,s')",
            "name": "Reward Function",
            "meaning": "The scalar feedback reward emitted by the environment following transition from s to s' via action a."
        },
        {
            "symbol": "γ",
            "name": "Discount Factor (gamma)",
            "meaning": "Decay scalar in [0, 1) quantifying temporal preference and guaranteeing finite infinite-horizon returns."
        },
        {
            "symbol": "V^π(s)",
            "name": "State-Value Function",
            "meaning": "Expected discounted cumulative return starting from state s under policy pi."
        },
        {
            "symbol": "Q^*(s,a)",
            "name": "Optimal Action-Value Function",
            "meaning": "Maximum achievable expected return starting from state s, taking action a, and adhering to the optimal policy."
        }
    ],
    "formula": "$$\\mathcal{M} = \\langle \\mathcal{S}, \\mathcal{A}, \\mathcal{P}, \\mathcal{R}, \\gamma \\rangle, \\quad \\gamma \\in [0, 1)$$\n\n$$\\text{Discounted Cumulative Return: } G_t = \\sum_{k=0}^{\\infty} \\gamma^k R_{t+k+1} = R_{t+1} + \\gamma G_{t+1}$$\n\n$$\\text{Bellman Expectation for } V^\\pi(s): \\quad V^\\pi(s) = \\sum_{a \\in \\mathcal{A}} \\pi(a|s) \\sum_{s' \\in \\mathcal{S}} \\mathcal{P}(s'|s,a) \\left[ \\mathcal{R}(s,a,s') + \\gamma V^\\pi(s') \\right]$$\n\n$$\\text{Bellman Expectation for } Q^\\pi(s,a): \\quad Q^\\pi(s,a) = \\sum_{s' \\in \\mathcal{S}} \\mathcal{P}(s'|s,a) \\left[ \\mathcal{R}(s,a,s') + \\gamma \\sum_{a' \\in \\mathcal{A}} \\pi(a'|s') Q^\\pi(s',a') \\right]$$\n\n$$\\text{Bellman Optimality for } V^*(s): \\quad V^*(s) = \\max_{a \\in \\mathcal{A}} \\sum_{s' \\in \\mathcal{S}} \\mathcal{P}(s'|s,a) \\left[ \\mathcal{R}(s,a,s') + \\gamma V^*(s') \\right]$$\n\n$$\\text{Bellman Optimality for } Q^*(s,a): \\quad Q^*(s,a) = \\sum_{s' \\in \\mathcal{S}} \\mathcal{P}(s'|s,a) \\left[ \\mathcal{R}(s,a,s') + \\gamma \\max_{a' \\in \\mathcal{A}} Q^*(s',a') \\right]$$\n\n$$\\text{Value Iteration Update Rule: } V_{k+1}(s) \\leftarrow \\max_{a \\in \\mathcal{A}} \\sum_{s' \\in \\mathcal{S}} \\mathcal{P}(s'|s,a) \\left[ \\mathcal{R}(s,a,s') + \\gamma V_k(s') \\right]$$\n\n$$\\text{Temporal Difference (TD) Error: } \\delta_t = R_{t+1} + \\gamma \\max_{a'} Q(S_{t+1}, a') - Q(S_t, A_t)$$",
    "logic": "In sequential decision-making under uncertainty, an autonomous agent interacts iteratively with an environment to optimize cumulative long-term feedback. The Markov Decision Process (MDP) formalizes this interaction through five mathematical components: states S, actions A, transition probabilities P, rewards R, and discount factor gamma. Central to the entire framework is the Markov Property, which asserts that the environmental dynamics are completely summarized by the present state and action: knowing the historical path of how the agent arrived at state s provides zero additional predictive information regarding next state s'. When real-world states violate this condition—such as a robot whose velocity is omitted from its position state—the system becomes a Partially Observable MDP (POMDP) or requires state augmentation with historical features. The agent's decision rule is formalized by policy pi, which maps states to action probability distributions pi(a|s). Rather than maximizing single-step rewards, the agent optimizes the expected discounted return G_t. Introducing gamma in [0, 1) serves two vital mathematical functions: it guarantees finite discounted returns in non-terminating infinite-horizon tasks (sum of gamma^k bounded by R_max / (1 - gamma)), and it mathematically models temporal risk and delayed payoff trade-offs. The Bellman Equation establishes a foundational recursive bridge by decomposing G_t into immediate reward R_{t+1} plus discounted future return gamma G_{t+1}. Under a fixed policy pi, the Bellman Expectation Equation expresses state value V^pi(s) as an expectation averaged over policy actions and environmental transitions. To discover the globally optimal policy, the Bellman Optimality Equation replaces the policy expectation with a supremum over actions max_a. This transforms linear policy evaluation into a non-linear optimization operator. In dynamic programming, Value Iteration iteratively applies this Bellman optimality backup operator across all states. Because the Bellman backup operator is a gamma-contraction mapping under the L-infinity norm, Banach's Fixed-Point Theorem guarantees that Value Iteration converges geometrically to a unique optimal value function V* regardless of initial values. When transition probabilities P and reward function R are unknown, model-free reinforcement learning replaces dynamic programming backups with sample transitions, bootstrapping value estimates via Temporal Difference (TD) learning and Q-learning updates.",
    "example": "Consider an autonomous warehouse forklift robot navigating a slippery logistics grid. The state space S encompasses grid coordinates (x, y) and load status. The action space A includes moving {Up, Down, Left, Right}. Due to wet concrete, moving Right has transition probability P = 0.8 of moving Right, P = 0.1 of remaining stationary, and P = 0.1 of slipping Downward. Navigating into a loading dock confers R = +10, colliding with shelving incurs R = -50, and standard steps incur R = -1 battery drain. Using the Bellman equation with gamma = 0.9, the planner evaluates two paths: a short path adjacent to shelves with high immediate speed but high slip risk, versus a longer clear path. Although the dangerous path offers quicker immediate gratification, the Bellman discounted future value of potential collision drops its value to 8.6, whereas the longer safe path yields a state value of 14.6, proving how Bellman planning prevents myopic catastrophic decisions.",
    "numerical_example": "Step 1: Discounted Return Calculation (Matching User Notes)\nSuppose an agent executes a three-step trajectory receiving rewards R_1 = +2, R_2 = +5, and R_3 = +10, with discount factor gamma = 0.9.\n  - Step 1 Reward (t=0 to 1):  R_1 = +2\n  - Step 2 Reward (t=1 to 2):  R_2 = +5\n  - Step 3 Reward (t=2 to 3):  R_3 = +10\nCalculate Discounted Cumulative Return G_0:\n  G_0 = R_1 + gamma * R_2 + gamma^2 * R_3\n  G_0 = 2 + 0.9 * (5) + (0.9)^2 * (10)\n  G_0 = 2 + 4.5 + 0.81 * (10)\n  G_0 = 2 + 4.5 + 8.1 = 14.6\nNotice that the delayed reward of +10 contributes only 8.1 to G_0 because of geometric discounting.\n\nStep 2: One-Step Bellman Evaluation & Immediate Gratification Dilemma\nSuppose an agent in state A can choose between two actions:\n  - Action 1 (Safe Investment): Immediate reward R = +2, leads to state B with known value V^pi(B) = 10.0.\n      Q(A, Action 1) = R + gamma * V(B) = 2 + 0.9 * (10.0) = 2 + 9.0 = 11.0\n  - Action 2 (Myopic Temptation): Immediate reward R = +5, leads to state C with known value V^pi(C) = 4.0.\n      Q(A, Action 2) = R + gamma * V(C) = 5 + 0.9 * (4.0) = 5 + 3.6 = 8.6\nEvaluation Decision:\n  Even though Action 2 yields 2.5x higher immediate reward (+5 vs +2), the Bellman state-action evaluation proves Action 1 delivers superior long-term return (11.0 vs 8.6).\n\nStep 3: Analytical Solution of a Two-State MDP Linear System (Matching User Notes)\nConsider a cyclic deterministic MDP with states A and B and gamma = 0.5:\n  - Transition A -> B yields reward R(A, B) = +2\n  - Transition B -> A yields reward R(B, A) = +3\nFormulate Bellman Expectation System of Linear Equations:\n  V(A) = 2 + 0.5 * V(B)\n  V(B) = 3 + 0.5 * V(A)\nSubstitute V(B) into V(A):\n  V(A) = 2 + 0.5 * (3 + 0.5 * V(A)) = 2 + 1.5 + 0.25 * V(A) = 3.5 + 0.25 * V(A)\n  V(A) - 0.25 * V(A) = 3.5  =>  0.75 * V(A) = 3.5\n  V(A) = 3.5 / 0.75 = 14 / 3 = 4.667\nSubstitute V(A) back to find V(B):\n  V(B) = 3 + 0.5 * (14 / 3) = 3 + 7 / 3 = 16 / 3 = 5.333\nBoth state values exceed individual transition rewards because of recurring future cycles discounted geometrically.\n\nStep 4: Python Value Iteration Implementation (Matching User Notes)\n```python\n# Value Iteration for 2-State Deterministic MDP\ngamma = 0.9\nmdp = {\n    'A': {'left': ('A', -1), 'right': ('B', 2)},\n    'B': {'left': ('A', 0),  'right': ('B', 1)}\n}\nV = {'A': 0.0, 'B': 0.0}\n\nfor iteration in range(100):\n    new_V = {}\n    for state, actions in mdp.items():\n        action_values = [\n            reward + gamma * V[next_s]\n            for next_s, reward in actions.values()\n        ]\n        new_V[state] = max(action_values)\n    delta = max(abs(new_V[s] - V[s]) for s in V)\n    V = new_V\n    if delta < 1e-8:\n        print(f'Converged in {iteration + 1} iterations!')\n        break\n\n# Extract Greedy Optimal Policy pi*(s)\npolicy = {}\nfor state, actions in mdp.items():\n    policy[state] = max(\n        actions,\n        key=lambda a: actions[a][1] + gamma * V[actions[a][0]]\n    )\nprint('Optimal State Values:', {k: round(v, 4) for k, v in V.items()})\nprint('Optimal Policy:', policy)\n# Output: Optimal State Values: {'A': 11.0, 'B': 10.0}, Optimal Policy: {'A': 'right', 'B': 'right'}\n```\n\nStep 5: Temporal Difference (TD) Error in Q-Learning\nIn model-free RL, the agent updates Q(s,a) without knowing P or R:\n  - Current estimate:        Q(S_t, A_t) = 4.0\n  - Observed transition:     reward r = +2, next state S_{t+1} has max_{a'} Q(S_{t+1}, a') = 8.0\n  - Discount factor:         gamma = 0.9\n  - Learning rate:           alpha = 0.2\nCalculate Temporal Difference Error delta:\n  delta = r + gamma * max_{a'} Q(S_{t+1}, a') - Q(S_t, A_t)\n  delta = 2 + 0.9 * (8.0) - 4.0 = 2 + 7.2 - 4.0 = 5.2\nApply Q-Learning Update:\n  Q(S_t, A_t) <- Q(S_t, A_t) + alpha * delta = 4.0 + 0.2 * (5.2) = 4.0 + 1.04 = 5.04",
    "types_header": "Reinforcement Learning Decision Frameworks",
    "types_badge": "MDP & Value Function Taxonomies",
    "quick_types": [
        {
            "name": "Fully Observable MDP (FOMDP)",
            "description": "Standard MDP framework where the agent receives complete, uncorrupted state observations S_t satisfying the Markov property, allowing direct state-to-action policy mapping."
        },
        {
            "name": "Partially Observable MDP (POMDP)",
            "description": "Generalization where true environmental state S_t is concealed; the agent receives sensory observation O_t via observation probability P(O_t|S_t) and maintains a belief state distribution."
        },
        {
            "name": "Bellman Expectation Formulation (Policy Evaluation)",
            "description": "Linear system of equations evaluating state values V^pi or action values Q^pi under a fixed behavioral policy pi by averaging over action choices and transition probabilities."
        },
        {
            "name": "Bellman Optimality Formulation (Control & Q-Learning)",
            "description": "Non-linear system of equations utilizing the max_a operator to discover the optimal value function V* and optimal policy pi*, forming the mathematical backbone of Q-learning."
        }
    ],
    "connected_logic": [
        {
            "title": "Markov State Transition Dynamics & Policy Execution",
            "description": "Mathematical framework governing how an autonomous agent navigates stochastic environments through sequential observations, policy actions, and state transitions.",
            "points": [
                "Formulates world transitions via conditional probability matrix P(s'|s,a), ensuring row probabilities sum to 1.",
                "Imposes the Markov Property: current state features encapsulate all relevant historical trajectory context.",
                "Executes actions via policy pi(a|s), supporting both deterministic decisions and stochastic probability distributions."
            ]
        },
        {
            "title": "Discounted Infinite-Horizon Return & Dynamic Programming",
            "description": "Theoretical justification for geometric reward discounting and recursive return decomposition in continuing reinforcement learning tasks.",
            "points": [
                "Compounds discount factor gamma in [0, 1) across time steps k as gamma^k, bounding cumulative infinite sums.",
                "Recursively partitions total return G_t into immediate reward R_{t+1} plus discounted downstream return gamma G_{t+1}.",
                "Balances short-term operational performance against long-term strategic success, preventing shortsighted myopic failures."
            ]
        },
        {
            "title": "Bellman Expectation vs. Optimality Equations",
            "description": "The mathematical distinction between evaluating a given policy and searching for the globally optimal behavioral policy.",
            "points": [
                "Expectation Equation averages over policy probabilities pi(a|s), producing solvable linear systems for fixed policies.",
                "Optimality Equation applies the non-linear max_a operator, defining upper bound performance limits V*(s) and Q*(s,a).",
                "Extracts the optimal policy pi*(s) greedily from Q*(s,a) without requiring environment transition models."
            ]
        },
        {
            "title": "Value Iteration & Temporal-Difference (TD) Foundations",
            "description": "Bridging model-based dynamic programming backups to model-free online reinforcement learning algorithms.",
            "points": [
                "Value Iteration iteratively applies Bellman optimality backups across states, guaranteed to converge via Banach fixed-point theorem.",
                "Model-free RL eliminates requirement for known transition matrix P by sampling real experience transitions (s, a, r, s').",
                "Q-learning updates Q-tables via Temporal Difference error delta = r + gamma max Q(s',a') - Q(s,a), converging asymptotically."
            ]
        }
    ],
    "pitfalls": [
        "Confusing Immediate Reward with Cumulative State Value: Reward R_{t+1} is an ephemeral scalar feedback for one transition, whereas State Value V(s) is the expected discounted cumulative return over the entire infinite trajectory.",
        "Misinterpreting or Omitting the Discount Factor (gamma): Setting gamma = 1 in continuing tasks causes return sums to diverge to infinity; setting gamma too low (e.g. 0.1) induces extreme short-sighted myopic policies.",
        "Conflating Policy Evaluation with Policy Optimization: The Bellman Expectation equation averages over actions using policy probabilities pi(a|s), whereas the Bellman Optimality equation selects the greedy maximum max_a.",
        "Ignoring Stochastic Transition Uncertainty: Assuming deterministic transitions when the environment has transition probabilities P(s'|s,a) leads to catastrophic failures in real robotics where slip or sensor noise occurs.",
        "Violating the Markov Property through Inadequate State Engineering: Omitting critical historical information (such as velocity, acceleration, or temporal demand trend) forces non-Markovian dynamics into an MDP solver."
    ],
    "key_takeaways": [
        "MDPs formalize sequential decision-making via the 5-tuple (S, A, P, R, gamma) where the Markov property guarantees that the future depends solely on the current state and action.",
        "The Bellman Equation recursively decomposes expected returns into immediate rewards plus discounted future values: V(s) = R + gamma V(s').",
        "Value Iteration applies the Bellman Optimality backup operator iteratively, mathematically guaranteed to converge to V* via the Banach contraction mapping theorem.",
        "Q-learning translates the Bellman optimality equation into an online model-free algorithm by computing temporal-difference (TD) errors between experienced transitions and bootstrapped targets."
    ],
    "tags": [
        "Reinforcement Learning",
        "Markov Decision Process",
        "Bellman Equation",
        "Dynamic Programming",
        "Value Iteration",
        "Q-Learning",
        "Temporal Difference",
        "Optimal Control"
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
