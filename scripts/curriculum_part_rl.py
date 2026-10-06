# scripts/curriculum_part_rl.py
# 5 Reinforcement Learning Concepts

def get_rl_concepts():
    topic_id = "dl_rl_foundations"
    topic_label = "Reinforcement Learning (RL) & Decision Foundations"
    cat = "dl"
    cat_label = "Deep Learning Foundations"

    return [
        {
            "id": "concept_mdp_bellman",
            "title": "Markov Decision Processes (MDP) & Bellman Equation",
            "topic_id": topic_id, "topic_label": topic_label, "category": cat, "category_label": cat_label,
            "raw_subtopic": "Markov Decision Processes (MDP) & Bellman Equation", "raw_sub": "Markov Decision Processes (MDP) & Bellman Equation",
            "def": "The formal mathematical framework for sequential decision making defined by 5-tuple (S, A, P, R, gamma), where the Markov property dictates that future transitions depend solely on the current state and action, governed recursively by the Bellman Optimality Equation.",
            "definition": "The formal mathematical framework for sequential decision making defined by 5-tuple (S, A, P, R, gamma), where the Markov property dictates that future transitions depend solely on the current state and action, governed recursively by the Bellman Optimality Equation.",
            "formula": "$$V^*(s) = \\max_{a} \\left[ R(s,a) + \\gamma \\sum_{s'} P(s'|s,a) V^*(s') \\right], \\quad Q^*(s,a) = R(s,a) + \\gamma \\sum_{s'} P(s'|s,a) \\max_{a'} Q^*(s',a')$$",
            "formula_explanation": "",
            "logic": "The Bellman equation decomposes the value of a decision into immediate reward plus discounted future returns, turning infinite-horizon planning into a recursive dynamic programming problem.",
            "core_logic": "The Bellman equation decomposes the value of a decision into immediate reward plus discounted future returns, turning infinite-horizon planning into a recursive dynamic programming problem.",
            "architectural_logic": "",
            "example": "Grid navigation robot: In state s (current room), choosing action a (move north) yields immediate reward R=-1 (fuel cost). Bellman equation sums this with the discounted value of the adjacent room V(s').",
            "tags": ["Reinforcement Learning", "MDP", "Bellman Equation", "Dynamic Programming"],
            "simple_summary": "An MDP is the rulebook of a game where an agent takes actions in states to get rewards. The Bellman equation is a recursive formula that calculates the total value of your current move based on today's prize plus the expected rewards of all future moves.",
            "core_terms": [
                {
                    "term": "Markov Property",
                    "what_is_it": "The condition that future states depend only on the present state and action, not on the entire history of past states.",
                    "analogy": "In a game of chess, the best next move depends solely on the current piece positions on the board, not on what order you moved them in 20 turns ago.",
                    "why_it_matters": "Massively simplifies planning because the agent only needs to remember where it is right now."
                },
                {
                    "term": "State Value Function V(s)",
                    "what_is_it": "The expected total cumulative reward an agent will receive starting from state s and following policy pi.",
                    "analogy": "How good a chess position feels overall for white, regardless of which move is played next.",
                    "why_it_matters": "Allows comparing which world states are safe vs dangerous."
                },
                {
                    "term": "Action Value Function Q(s, a)",
                    "what_is_it": "The expected total cumulative reward of taking a specific action a in state s, and then continuing with policy pi.",
                    "analogy": "Calculating how good it is specifically to move your Queen to e4 right now.",
                    "why_it_matters": "Directly guides decision making: pick the action with highest Q(s, a)."
                },
                {
                    "term": "Discount Factor (gamma)",
                    "what_is_it": "A scalar between 0 and 1 that determines how much future rewards are valued compared to immediate rewards.",
                    "analogy": "Receiving $100 today (gamma=0) versus waiting 10 years for $100 (gamma=0.99 discounts future uncertainty).",
                    "why_it_matters": "Prevents infinite return sums in non-terminating tasks and models realistic urgency."
                }
            ],
            "symbol_guide": [
                {"symbol": "S, A", "meaning": "State space and Action space", "plain_english": "All possible situations and all possible choices"},
                {"symbol": "P(s'|s,a)", "meaning": "Transition probability", "plain_english": "Chance of landing in state s' after taking action a in s"},
                {"symbol": "\\gamma", "meaning": "Discount factor (0 to 1)", "plain_english": "Controls patience: closer to 1 means patient, closer to 0 means short-sighted"}
            ],
            "numerical_example": "Immediate reward R = +10. Discount factor gamma = 0.9. Expected next state value V(s') = 100. Bellman calculation: Q(s,a) = 10 + 0.9 × 100 = 10 + 90 = 100. If an alternative action yielded R = +20 but next state value was only 50: Q = 20 + 0.9 × 50 = 65. The agent picks the first action because long-term future is worth more.",
            "pitfalls": "Novice Trap: Setting gamma = 1.0 in continuous non-terminating environments. This causes value functions to diverge to infinity, breaking numerical stability during gradient updates.",
            "key_takeaways": [],
            "definition_bullets": [
                "Markov Property: Future states depend only on the current state, not past history.",
                "State Value V(s): Total expected future reward from being in state s.",
                "Action Value Q(s, a): Total expected future reward from taking action a in state s.",
                "Discount Factor: Balances immediate gratification against long-term future rewards."
            ]
        },
        {
            "id": "concept_q_learning_dqn",
            "title": "Q-Learning & Deep Q-Networks (DQN)",
            "topic_id": topic_id, "topic_label": topic_label, "category": cat, "category_label": cat_label,
            "raw_subtopic": "Q-Learning & Deep Q-Networks (DQN)", "raw_sub": "Q-Learning & Deep Q-Networks (DQN)",
            "def": "A model-free temporal difference control algorithm that iteratively learns optimal action-values without environment transition dynamics, scaled to high-dimensional state spaces via Deep Q-Networks (DQN) with experience replay and target networks.",
            "definition": "A model-free temporal difference control algorithm that iteratively learns optimal action-values without environment transition dynamics, scaled to high-dimensional state spaces via Deep Q-Networks (DQN) with experience replay and target networks.",
            "formula": "$$Q(s, a) \\leftarrow Q(s, a) + \\alpha \\left[ r + \\gamma \\max_{a'} Q(s', a') - Q(s, a) \\right], \\quad \\mathcal{L}_{\\text{DQN}}(\\theta) = \\mathbb{E}\\left[ \\left( r + \\gamma \\max_{a'} Q(s', a'; \\theta^-) - Q(s, a; \\theta) \\right)^2 \\right]$$",
            "formula_explanation": "",
            "logic": "Classical Q-learning stores values in a discrete table, which explodes exponentially with continuous states. DQN replaces the table with a deep neural network Q(s, a; theta), stabilized using Experience Replay and frozen Target Networks.",
            "core_logic": "Classical Q-learning stores values in a discrete table, which explodes exponentially with continuous states. DQN replaces the table with a deep neural network Q(s, a; theta), stabilized using Experience Replay and frozen Target Networks.",
            "architectural_logic": "",
            "example": "DeepMind Atari 2600 (Breakout): The state is raw screen pixels (84x84x4). DQN outputs Q-values for actions (left, right, fire), learning superhuman paddle control purely from score rewards.",
            "tags": ["Q-Learning", "DQN", "Experience Replay", "Target Network"],
            "simple_summary": "Q-Learning learns the value of every action by trying things and adjusting its guesses based on actual surprises (temporal difference). DQN uses a deep neural network to handle video game screens and complex states.",
            "core_terms": [
                {
                    "term": "Temporal Difference (TD) Error",
                    "what_is_it": "The gap between the estimated return from your next step and your original prediction for your current step: [r + gamma max Q(s', a') - Q(s, a)].",
                    "analogy": "Expecting a flight to take 3 hours, but after hour 1 the pilot announces only 1 hour remains (adjusting expectations on the fly without waiting to land).",
                    "why_it_matters": "Enables bootstrapping: learning at every single step without waiting for the whole game to finish."
                },
                {
                    "term": "Experience Replay Buffer",
                    "what_is_it": "A circular memory buffer storing past transitions (s, a, r, s', done) sampled randomly in mini-batches to train the neural network.",
                    "analogy": "Studying for an exam by drawing random flashcards from different chapters rather than re-reading the book in strict page order.",
                    "why_it_matters": "Breaks temporal correlation between consecutive frames and stabilizes gradient descent."
                },
                {
                    "term": "Target Network (theta^-)",
                    "what_is_it": "A secondary frozen copy of the neural network used solely to compute target Q-values, updated periodically every C steps.",
                    "analogy": "Shooting at a stationary bullseye target that only moves once every 10 minutes, rather than chasing a target tied to your own arrow.",
                    "why_it_matters": "Prevents feedback loops where updating Q(s, a) shifts the target it is trying to reach."
                },
                {
                    "term": "Off-Policy Learning",
                    "what_is_it": "Learning the optimal target policy (greedy max) while actively executing an exploratory behavior policy (epsilon-greedy).",
                    "analogy": "Watching amateur skateboarders try random stunts to learn what the ideal championship trick should be.",
                    "why_it_matters": "Allows the agent to explore safely without biasing the final optimal policy."
                }
            ],
            "symbol_guide": [
                {"symbol": "\\alpha", "meaning": "Learning rate", "plain_english": "How fast the agent updates its Q-values"},
                {"symbol": "\\theta", "meaning": "Online network weights", "plain_english": "The active weights being trained right now"},
                {"symbol": "\\theta^-", "meaning": "Target network weights", "plain_english": "The frozen weights calculating the goal"}
            ],
            "numerical_example": "Current Q(s, a) = 4.0. Agent takes action, gets reward r = +2. Next state max Q(s', a') = 5.0. Gamma = 0.9. TD Target = 2 + 0.9 × 5.0 = 6.5. TD Error = 6.5 - 4.0 = +2.5. With learning rate alpha = 0.1, new Q(s, a) = 4.0 + 0.1 × 2.5 = 4.25.",
            "pitfalls": "Novice Trap: Updating the target network every single step. This completely destroys training stability and causes Q-values to explode or diverge toward positive infinity.",
            "key_takeaways": [],
            "definition_bullets": [
                "Temporal Difference Error: Updating estimates using the immediate reward and subsequent state estimate.",
                "Experience Replay: Sampling random past transitions to break temporal correlations.",
                "Target Network: A frozen duplicate network that provides stable training targets.",
                "Off-Policy: Learning the optimal greedy strategy while exploring with random actions."
            ]
        },
        {
            "id": "concept_policy_gradients_reinforce",
            "title": "Policy Gradients & REINFORCE Algorithm",
            "topic_id": topic_id, "topic_label": topic_label, "category": cat, "category_label": cat_label,
            "raw_subtopic": "Policy Gradients & REINFORCE Algorithm", "raw_sub": "Policy Gradients & REINFORCE Algorithm",
            "def": "A class of reinforcement learning algorithms that directly parameterize and optimize the policy distribution pi_theta(a|s) via gradient ascent on expected trajectory returns without requiring intermediate action-value functions, formalized by the Policy Gradient Theorem and Monte Carlo REINFORCE.",
            "definition": "A class of reinforcement learning algorithms that directly parameterize and optimize the policy distribution pi_theta(a|s) via gradient ascent on expected trajectory returns without requiring intermediate action-value functions, formalized by the Policy Gradient Theorem and Monte Carlo REINFORCE.",
            "formula": "$$\\nabla_\\theta J(\\theta) = \\mathbb{E}_{\\tau \\sim \\pi_\\theta}\\left[ \\sum_{t=0}^T \\nabla_\\theta \\log \\pi_\\theta(a_t | s_t) G_t \\right], \\quad G_t = \\sum_{k=t}^T \\gamma^{k-t} R_{k+1}$$",
            "formula_explanation": "",
            "logic": "Instead of guessing values Q(s,a) and picking the max, policy gradients directly increase the probability of actions that led to high rewards and decrease the probability of actions that led to poor outcomes.",
            "core_logic": "Instead of guessing values Q(s,a) and picking the max, policy gradients directly increase the probability of actions that led to high rewards and decrease the probability of actions that led to poor outcomes.",
            "architectural_logic": "",
            "example": "Continuous robotic arm joint control: Rather than discretizing continuous motor torques into buckets, a policy network outputs the mean and variance of a Gaussian distribution pi(torque|joint_angles).",
            "tags": ["Policy Gradient", "REINFORCE", "Monte Carlo", "Continuous Control"],
            "simple_summary": "Policy Gradients skip the math of estimating values and directly tweak the neural network's action probabilities: if an entire game went well, make all the moves you took more likely in the future.",
            "core_terms": [
                {
                    "term": "Policy Function pi_theta(a|s)",
                    "what_is_it": "A neural network that takes state s as input and outputs a probability distribution over possible actions.",
                    "analogy": "A basketball coach calling play probabilities from the bench based on defensive matchups.",
                    "why_it_matters": "Naturally handles continuous action spaces (like exact steering wheel angles or throttle percentages)."
                },
                {
                    "term": "Log Derivative Trick",
                    "what_is_it": "The mathematical identity nabla pi = pi * nabla log(pi) allowing the gradient of an expectation to be computed by sampling actual trajectories.",
                    "analogy": "Figuring out the popularity of a movie by polling random moviegoers leaving the theater.",
                    "why_it_matters": "Enables computing analytical gradients of unknown environment transition dynamics."
                },
                {
                    "term": "Return G_t",
                    "what_is_it": "The cumulative discounted sum of rewards collected from time step t until the end of the episode.",
                    "analogy": "Total points accumulated on the scoreboard from the current quarter until the final whistle.",
                    "why_it_matters": "Acts as the multiplier: actions followed by huge positive returns are heavily reinforced."
                },
                {
                    "term": "Baseline Subtraction",
                    "what_is_it": "Subtracting an independent baseline value b(s) from return G_t: nabla log pi * (G_t - b(s)).",
                    "analogy": "Grading on a curve: only reward students who beat the class average, rather than giving everybody bonus points.",
                    "why_it_matters": "Drastically reduces gradient variance without introducing any mathematical bias."
                }
            ],
            "symbol_guide": [
                {"symbol": "\\tau", "meaning": "A complete trajectory/episode", "plain_english": "The entire sequence of states and actions from start to game over"},
                {"symbol": "G_t", "meaning": "Discounted return from step t", "plain_english": "Total future reward from step t onwards"},
                {"symbol": "J(\\theta)", "meaning": "Expected cumulative reward objective", "plain_english": "The overall score we want to maximize"}
            ],
            "numerical_example": "Agent took action 'jump' with probability pi = 0.20 (log pi = -1.609). Episode finished with return G_t = +50. Baseline b(s) = +20. Advantage = 50 - 20 = +30. Gradient pushes probability up proportionally to 30 × nabla log pi. On next visit to this state, probability of jumping rises to 0.35.",
            "pitfalls": "Novice Trap: High variance in Monte Carlo returns. Because G_t depends on a long chain of stochastic events until the end of the episode, gradient estimates fluctuate wildly, requiring millions of samples to converge.",
            "key_takeaways": [],
            "definition_bullets": [
                "Policy Function: Outputs a continuous or discrete probability distribution over actions.",
                "Log-Derivative Trick: Converts expectation gradient into sample trajectory averages.",
                "Return G_t: Total discounted reward earned from current step until episode termination.",
                "Baseline Subtraction: Lowers gradient variance by rewarding actions relative to an average benchmark."
            ]
        },
        {
            "id": "concept_actor_critic_ppo",
            "title": "Actor-Critic Architectures (A2C & PPO)",
            "topic_id": topic_id, "topic_label": topic_label, "category": cat, "category_label": cat_label,
            "raw_subtopic": "Actor-Critic Architectures (A2C & PPO)", "raw_sub": "Actor-Critic Architectures (A2C & PPO)",
            "def": "Hybrid reinforcement learning frameworks combining a parameterized Actor policy with a Critic value function, refined by Proximal Policy Optimization (PPO) using clipped surrogate objectives to enforce trust region update bounds.",
            "definition": "Hybrid reinforcement learning frameworks combining a parameterized Actor policy with a Critic value function, refined by Proximal Policy Optimization (PPO) using clipped surrogate objectives to enforce trust region update bounds.",
            "formula": "$$\\mathcal{L}_{\\text{PPO}}(\\theta) = \\hat{\\mathbb{E}}_t \\left[ \\min\\left( r_t(\\theta) \\hat{A}_t, \\; \\text{clip}(r_t(\\theta), 1-\\epsilon, 1+\\epsilon) \\hat{A}_t \\right) \\right], \\quad r_t(\\theta) = \\frac{\\pi_\\theta(a_t|s_t)}{\\pi_{\\theta_{\\text{old}}}(a_t|s_t)}$$",
            "formula_explanation": "",
            "logic": "Pure policy gradients suffer from high variance, while pure Q-learning struggles with continuous actions. Actor-Critic bridges both: the Actor proposes actions, the Critic grades them, and PPO's clipping prevents disastrously large policy updates.",
            "core_logic": "Pure policy gradients suffer from high variance, while pure Q-learning struggles with continuous actions. Actor-Critic bridges both: the Actor proposes actions, the Critic grades them, and PPO's clipping prevents disastrously large policy updates.",
            "architectural_logic": "",
            "example": "ChatGPT RLHF and OpenAI Five (Dota 2): PPO acts as the standard engine for aligning LLM outputs with human preference reward models without suffering catastrophic policy collapse.",
            "tags": ["Actor-Critic", "PPO", "A2C", "RLHF", "Clipping"],
            "simple_summary": "Actor-Critic is a two-person team: the Actor performs actions, and the Critic grades how good they were. PPO adds a safety guardrail (clipping) so the Actor never changes its behavior too drastically in a single step.",
            "core_terms": [
                {
                    "term": "Actor",
                    "what_is_it": "The policy network pi_theta(a|s) responsible for selecting which actions to take.",
                    "analogy": "An actor on stage performing lines and movements.",
                    "why_it_matters": "Learns what to do in every situation."
                },
                {
                    "term": "Critic",
                    "what_is_it": "The value network V_phi(s) that evaluates how promising each state is.",
                    "analogy": "A theatre director in the front row critiquing the actor's performance.",
                    "why_it_matters": "Replaces noisy Monte Carlo episode returns with a smooth, low-variance baseline."
                },
                {
                    "term": "Advantage Function A(s, a)",
                    "what_is_it": "A measure of how much better an action was compared to the average expected action in that state: A(s, a) = Q(s, a) - V(s).",
                    "analogy": "Beating your personal best record on a 100m sprint.",
                    "why_it_matters": "Isolates the specific contribution of your choice from general good or bad luck."
                },
                {
                    "term": "PPO Clipping",
                    "what_is_it": "Constraining the probability ratio r_t(theta) between [1 - epsilon, 1 + epsilon] (typically epsilon = 0.2).",
                    "analogy": "A speed limiter on a car preventing sudden dangerous acceleration.",
                    "why_it_matters": "Guarantees monotonic policy improvement and prevents catastrophic policy unlearning."
                }
            ],
            "symbol_guide": [
                {"symbol": "r_t(\\theta)", "meaning": "Probability ratio between new and old policy", "plain_english": "How much more or less likely the action is now vs before"},
                {"symbol": "\\hat{A}_t", "meaning": "Estimated advantage score", "plain_english": "Positive means action was better than average, negative means worse"},
                {"symbol": "\\epsilon", "meaning": "Clipping threshold (usually 0.1 to 0.2)", "plain_english": "The maximum allowable policy shift per step"}
            ],
            "numerical_example": "Advantage A_t = +2.5. Old policy probability = 0.20, new policy probability = 0.30. Ratio r_t = 0.30 / 0.20 = 1.50. With epsilon = 0.2, the ratio is clipped to 1 + 0.2 = 1.20. PPO takes min(1.50 × 2.5, 1.20 × 2.5) = min(3.75, 3.00) = 3.00, safely bounding gradient magnitude.",
            "pitfalls": "Novice Trap: Not normalizing the advantage estimates across the batch. Subtracting batch mean and dividing by standard deviation is mandatory in PPO; omitting it causes training to stall or destabilize.",
            "key_takeaways": [],
            "definition_bullets": [
                "Actor: The parameterized policy network choosing actions.",
                "Critic: The value network providing low-variance baseline evaluations.",
                "Advantage: Quantifies whether an action outperformed the average state expectation.",
                "PPO Clipping: Restricts policy changes to a trust region [1 - eps, 1 + eps]."
            ]
        },
        {
            "id": "concept_exploration_exploitation_ucb",
            "title": "Exploration vs Exploitation (Epsilon-Greedy & UCB)",
            "topic_id": topic_id, "topic_label": topic_label, "category": cat, "category_label": cat_label,
            "raw_subtopic": "Exploration vs Exploitation (Epsilon-Greedy & UCB)", "raw_sub": "Exploration vs Exploitation (Epsilon-Greedy & UCB)",
            "def": "The fundamental dilemma in reinforcement learning between exploiting currently known high-reward actions versus exploring uncharted actions to discover superior long-term policies, solved via Epsilon-Greedy, Upper Confidence Bound (UCB), and Thompson Sampling.",
            "definition": "The fundamental dilemma in reinforcement learning between exploiting currently known high-reward actions versus exploring uncharted actions to discover superior long-term policies, solved via Epsilon-Greedy, Upper Confidence Bound (UCB), and Thompson Sampling.",
            "formula": "$$\\text{UCB1}: a_t = \\arg\\max_{a} \\left[ \\hat{Q}(a) + c \\sqrt{\\frac{\\ln t}{N(a)}} \\right], \\quad \\epsilon\\text{-Greedy}: a_t = \\begin{cases} \\arg\\max_a Q(a) & \\text{with prob } 1 - \\epsilon \\\\ \\text{random action} & \\text{with prob } \\epsilon \\end{cases}$$",
            "formula_explanation": "",
            "logic": "Greedy exploitation alone causes premature convergence to suboptimal local traps. The UCB formula implements 'optimism in the face of uncertainty': actions with few historical visits receive an uncertainty bonus.",
            "core_logic": "Greedy exploitation alone causes premature convergence to suboptimal local traps. The UCB formula implements 'optimism in the face of uncertainty': actions with few historical visits receive an uncertainty bonus.",
            "architectural_logic": "",
            "example": "Online ad click-through rate optimization (Multi-Armed Bandits): Balancing showing proven top-converting ads (exploitation) against testing brand new ads with unknown appeal (exploration).",
            "tags": ["Exploration", "Exploitation", "Multi-Armed Bandits", "UCB"],
            "simple_summary": "The dilemma between ordering your favorite pizza (exploitation) versus trying a brand new restaurant that might be incredible or terrible (exploration). UCB gives extra bonus points to dishes you've never tried before.",
            "core_terms": [
                {
                    "term": "Exploitation",
                    "what_is_it": "Choosing the action with the highest estimated reward based on data collected so far.",
                    "analogy": "Going to your favorite restaurant because you know the burger is an 8/10.",
                    "why_it_matters": "Maximizes immediate reward payoff."
                },
                {
                    "term": "Exploration",
                    "what_is_it": "Choosing actions with high uncertainty to gather new information about their true payoffs.",
                    "analogy": "Trying the brand new bistro down the block that might be a 10/10.",
                    "why_it_matters": "Prevents getting stuck forever in a mediocre routine."
                },
                {
                    "term": "Upper Confidence Bound (UCB)",
                    "what_is_it": "Adding an uncertainty bonus proportional to sqrt(ln t / N(a)) to action values.",
                    "analogy": "Giving an untested job applicant the benefit of the doubt during the initial interview.",
                    "why_it_matters": "Guarantees logarithmic regret bounds; rarely-tried actions are systematically explored."
                },
                {
                    "term": "Epsilon Decay Schedule",
                    "what_is_it": "Starting with high randomness (e.g. epsilon = 1.0) and gradually annealing down to a low value (e.g. 0.05) as training progresses.",
                    "analogy": "A young toddler exploring everything randomly, maturing into an adult with focused preferences.",
                    "why_it_matters": "Ensures wide coverage early on and stable, greedy execution later."
                }
            ],
            "symbol_guide": [
                {"symbol": "\\hat{Q}(a)", "meaning": "Average empirical reward of action a", "plain_english": "The track record score so far"},
                {"symbol": "N(a)", "meaning": "Number of times action a has been selected", "plain_english": "How many times you tried this choice"},
                {"symbol": "t", "meaning": "Total decision rounds so far", "plain_english": "Overall experience counter"}
            ],
            "numerical_example": "Action A has average reward Q = 8.0, tested N = 100 times. Action B has average reward Q = 7.0, tested N = 4 times. Total trials t = 104. UCB bonus for A = 2 × sqrt(ln 104 / 100) = 2 × 0.215 = 0.43 -> Score = 8.43. UCB bonus for B = 2 × sqrt(ln 104 / 4) = 2 × 1.077 = 2.15 -> Score = 9.15. The agent chooses B because high uncertainty outweighs the slightly lower average.",
            "pitfalls": "Novice Trap: Using a static epsilon = 0.2 during production serving. This wastes 20% of all customer requests on pure random noise! In production, use Thompson Sampling or decay epsilon to near-zero.",
            "key_takeaways": [],
            "definition_bullets": [
                "Exploitation: Capitalizing on the best known action to maximize immediate reward.",
                "Exploration: Trying uncertain actions to discover superior alternatives.",
                "Upper Confidence Bound: Assigns uncertainty bonuses to rarely tested options.",
                "Epsilon Annealing: Gradually shifting behavior from high randomness to greedy execution."
            ]
        }
    ]

print("RL concepts module ready.")
