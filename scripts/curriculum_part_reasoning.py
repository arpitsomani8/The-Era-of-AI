# scripts/curriculum_part_reasoning.py
# 5 Reasoning & Test-Time Compute Concepts

def get_reasoning_concepts():
    topic_id = "genai_reasoning_test_time"
    topic_label = "Reasoning Models, Test-Time Compute & System 2 AI"
    cat = "genai"
    cat_label = "Transformers & Generative AI"

    return [
        {
            "id": "concept_prm_vs_orm",
            "title": "Process Reward Models (PRM) vs Outcome Reward Models (ORM)",
            "topic_id": topic_id, "topic_label": topic_label, "category": cat, "category_label": cat_label,
            "raw_subtopic": "Process Reward Models (PRM) vs Outcome Reward Models (ORM)", "raw_sub": "Process Reward Models (PRM) vs Outcome Reward Models (ORM)",
            "def": "The paradigm shift in reinforcement learning from AI feedback comparing Outcome Reward Models (ORM, providing a single scalar grade only after final solution completion) against Process Reward Models (PRM, scoring step-by-step reasoning validity at each mathematical or logical derivation).",
            "definition": "The paradigm shift in reinforcement learning from AI feedback comparing Outcome Reward Models (ORM, providing a single scalar grade only after final solution completion) against Process Reward Models (PRM, scoring step-by-step reasoning validity at each mathematical or logical derivation).",
            "formula": "$$\\text{ORM}: R = f(\\mathbf{x}, y_{\\text{final}}), \\quad \\text{PRM}: R = \\prod_{k=1}^K P(\\text{Step } k \\text{ is valid} | \\mathbf{x}, s_{1:k-1}), \\quad \\mathcal{L}_{\\text{PRM}} = -\\sum_{k=1}^K \\log P(z_k | s_k)$$",
            "formula_explanation": "",
            "logic": "ORM suffers from credit assignment failure: if a model arrives at the correct final number through two offsetting mathematical errors, ORM rewards the flawed logic ('lucky hallucination'). PRM evaluates every step independently, pruning flawed branches the instant an error occurs.",
            "core_logic": "ORM suffers from credit assignment failure: if a model arrives at the correct final number through two offsetting mathematical errors, ORM rewards the flawed logic ('lucky hallucination'). PRM evaluates every step independently, pruning flawed branches the instant an error occurs.",
            "architectural_logic": "",
            "example": "Olympiad mathematics theorem proving (OpenAI PRM800K): In a 12-step proof, step 5 makes an invalid algebraic substitution. PRM flags step 5 with reward 0.02, triggering immediate backtracking before wasting tokens on steps 6-12.",
            "tags": ["PRM", "ORM", "Reasoning Models", "Step-Level Verification"],
            "simple_summary": "An Outcome Reward Model (ORM) is like a teacher who only looks at the final answer on a math test without reading your work. A Process Reward Model (PRM) is a teacher who checks every single line of your work, rewarding you for correct steps and catching errors the moment they happen.",
            "core_terms": [
                {
                    "term": "Outcome Reward Model (ORM)",
                    "what_is_it": "A reward model that evaluates only the final answer at the very end of the trajectory, returning a binary or scalar score.",
                    "analogy": "Judging a chef's meal purely on whether the customer swallowed it, without checking if they used expired ingredients.",
                    "why_it_matters": "Easy to collect automatically, but encourages shortcut hallucinations and flawed reasoning chains."
                },
                {
                    "term": "Process Reward Model (PRM)",
                    "what_is_it": "A trained discriminator that evaluates the logical correctness of every individual reasoning step in a chain of thought.",
                    "analogy": "A math tutor sitting beside you pointing out: 'Step 1 is correct, Step 2 is correct, wait—in Step 3 you forgot a minus sign!'.",
                    "why_it_matters": "Enables precise credit assignment and powers search algorithms to explore multiple alternative paths."
                },
                {
                    "term": "PRM800K Dataset",
                    "what_is_it": "The milestone dataset released by OpenAI containing 800,000 human step-level correctness labels across 75,000 math solutions.",
                    "analogy": "A massive answer key where every line of math has a green checkmark or red X.",
                    "why_it_matters": "Proved that step-level supervision drastically outperforms outcome-only supervision on hard reasoning tasks."
                },
                {
                    "term": "Step Boundary Token",
                    "what_is_it": "A special token (e.g. '\\n\\n' or '<step>') marking where one logical inference ends and the next begins.",
                    "analogy": "The semicolon at the end of a line of code or a period at the end of a sentence.",
                    "why_it_matters": "Signals to the PRM when to pause generation and emit a step score."
                }
            ],
            "symbol_guide": [
                {"symbol": "s_k", "meaning": "Reasoning step k in the chain of thought", "plain_english": "e.g. 'Differentiating both sides gives 2x + 2y y' = 0'"},
                {"symbol": "z_k", "meaning": "Ground-truth validity label for step k", "plain_english": "1 = valid step, 0 = invalid reasoning"},
                {"symbol": "R_{step}", "meaning": "PRM step probability score", "plain_english": "Confidence from 0.0 to 1.0 that this step is mathematically sound"}
            ],
            "numerical_example": "Math problem solved with 4 steps. ORM check: Final answer is correct (Reward = 1.0). But PRM check reveals: Step 1 = 0.99, Step 2 = 0.98, Step 3 = 0.04 (false assumption), Step 4 = 0.01 (accidental cancellation yielding right number). Total PRM product = 0.99 × 0.98 × 0.04 × 0.01 = 0.00038. PRM correctly rejects the solution, preventing reinforcement of bad logic.",
            "pitfalls": "Novice Trap: High computational cost of PRM verification. Running a separate PRM model forward pass on every single line of text can quadruple inference latency. Modern systems use small distilled verifiers or run PRMs only at critical branch decision points.",
            "key_takeaways": [],
            "definition_bullets": [
                "Step-Level Feedback: Evaluating logical validity at every individual step in a chain of thought.",
                "Credit Assignment Precision: Overcoming the limitation of lucky hallucinations in outcome-only rewards.",
                "Branch Pruning: Halting and backtracking immediately when an invalid derivation is detected.",
                "Foundation of System 2 AI: Powers guided search algorithms for complex reasoning problems."
            ]
        },
        {
            "id": "concept_test_time_search_mcts",
            "title": "Test-Time Search: Monte Carlo Tree Search (MCTS) & Beam Search",
            "topic_id": topic_id, "topic_label": topic_label, "category": cat, "category_label": cat_label,
            "raw_subtopic": "Test-Time Search: Monte Carlo Tree Search (MCTS) & Beam Search", "raw_sub": "Test-Time Search: Monte Carlo Tree Search (MCTS) & Beam Search",
            "def": "Inference-time search algorithms that explore multiple reasoning trajectories, maintain tree-structured state hypotheses, and guide path selection using Monte Carlo Tree Search (MCTS, AlphaGo-style) or Best-of-N / Beam Search with verifier scoring.",
            "definition": "Inference-time search algorithms that explore multiple reasoning trajectories, maintain tree-structured state hypotheses, and guide path selection using Monte Carlo Tree Search (MCTS, AlphaGo-style) or Best-of-N / Beam Search with verifier scoring.",
            "formula": "$$\\text{UCT}: a^* = \\arg\\max_a \\left[ Q(s, a) + c_{\\text{puct}} P(s, a) \\frac{\\sqrt{\\sum_{b} N(s, b)}}{1 + N(s, a)} \\right], \\quad \\text{Best-of-N}: y^* = \\arg\\max_{y_i \\in \\{y_1, \\dots, y_N\\}} V_{\\text{PRM}}(y_i)$$",
            "formula_explanation": "",
            "logic": "Standard greedy decoding generates tokens sequentially without looking ahead: once a wrong token is generated, the model cannot undo it. Test-Time Search treats reasoning as a tree exploration problem: generating multiple candidate steps, evaluating node values, and expanding promising branches while pruning dead ends.",
            "core_logic": "Standard greedy decoding generates tokens sequentially without looking ahead: once a wrong token is generated, the model cannot undo it. Test-Time Search treats reasoning as a tree exploration problem: generating multiple candidate steps, evaluating node values, and expanding promising branches while pruning dead ends.",
            "architectural_logic": "",
            "example": "Autonomous competitive coding (Codeforces): An LLM generates 64 candidate solution branches. MCTS expands each branch, runs unit test verifiers, and backtracks from compilation errors to discover the optimal O(N log N) algorithm.",
            "tags": ["MCTS", "Test-Time Search", "Beam Search", "Best-of-N", "Tree-of-Thoughts"],
            "simple_summary": "Greedy LLMs blurt out the first thought that comes to mind without thinking ahead. Test-Time Search is like a chess player thinking 5 moves in advance: exploring multiple possible paths, testing which ones look promising, and backing up to try another branch if one leads to a dead end.",
            "core_terms": [
                {
                    "term": "Monte Carlo Tree Search (MCTS)",
                    "what_is_it": "A 4-phase search algorithm (Selection, Expansion, Simulation/Evaluation, Backpropagation) that builds a search tree of reasoning steps.",
                    "analogy": "A mountain climber scouting multiple routes up a cliff face with safety ropes before choosing the safest ascent.",
                    "why_it_matters": "The core algorithm behind AlphaGo, AlphaZero, and modern reasoning architectures."
                },
                {
                    "term": "Best-of-N Sampling (Rejection Sampling)",
                    "what_is_it": "Sampling N complete solutions in parallel at high temperature and selecting the trajectory with the highest reward model score.",
                    "analogy": "Taking 20 photos with a burst camera and picking the single photo where everyone is smiling.",
                    "why_it_matters": "The simplest and most effective test-time compute scaling technique."
                },
                {
                    "term": "Tree-of-Thoughts (ToT)",
                    "what_is_it": "Framing problem solving as search over a tree where each node represents a coherent partial thought or reasoning phase.",
                    "analogy": "Solving a crossword puzzle by penciling in pencil letters, evaluating word intersections, and erasing mistakes.",
                    "why_it_matters": "Enables deliberate exploration and self-evaluation on non-trivial logic puzzles."
                },
                {
                    "term": "Majority Voting (Self-Consistency)",
                    "what_is_it": "Generating 40 different reasoning paths and taking the mathematical answer that appears most frequently (mode).",
                    "analogy": "Asking 10 independent accountants to audit your taxes and adopting the refund number that 8 of them agree on.",
                    "why_it_matters": "Significantly boosts accuracy on mathematical and factual benchmarks with zero model retraining."
                }
            ],
            "symbol_guide": [
                {"symbol": "Q(s, a)", "meaning": "Action-value score of expanding step a in state s", "plain_english": "Expected quality of this reasoning branch"},
                {"symbol": "N(s, a)", "meaning": "Visit count for step a", "plain_english": "How many times search explored this path"},
                {"symbol": "c_{\\text{puct}}", "meaning": "Exploration constant", "plain_english": "Balances exploring untested branches vs exploiting top branches"}
            ],
            "numerical_example": "A hard logic puzzle has 12% accuracy with single greedy generation. Generating N = 64 parallel solutions with temperature T = 0.7: Best-of-N using PRM scoring boosts accuracy to 84%. Majority voting among the top 10 PRM-scored paths boosts accuracy to 89% without changing a single weight in the model.",
            "pitfalls": "Novice Trap: Reward Hacking (Goodhart's Law) during Best-of-N search! As N scales into thousands, the search algorithm inevitably finds bizarre adversarial solutions that exploit blind spots in the reward model, scoring 99.9% on the verifier while producing total nonsense to human evaluators.",
            "key_takeaways": [],
            "definition_bullets": [
                "Tree Exploration: Treating multi-step reasoning as a tree of search hypotheses.",
                "Monte Carlo Tree Search: Balancing exploration and exploitation of reasoning branches via UCT.",
                "Best-of-N Sampling: Generating multiple diverse solutions and selecting the highest verifier score.",
                "Majority Voting: Clustering final answers across stochastic paths to filter out random arithmetic errors."
            ]
        },
        {
            "id": "concept_cot_self_correction_verification",
            "title": "Chain-of-Thought (CoT) Self-Correction & Verification Loops",
            "topic_id": topic_id, "topic_label": topic_label, "category": cat, "category_label": cat_label,
            "raw_subtopic": "Chain-of-Thought (CoT) Self-Correction & Verification Loops", "raw_sub": "Chain-of-Thought (CoT) Self-Correction & Verification Loops",
            "def": "Iterative agentic feedback mechanisms where an LLM generates an initial reasoning scratchpad, invokes deterministic verification tools (Python REPL, linters, SAT solvers), and engages in introspective self-correction to rectify discovered logical fallacies.",
            "definition": "Iterative agentic feedback mechanisms where an LLM generates an initial reasoning scratchpad, invokes deterministic verification tools (Python REPL, linters, SAT solvers), and engages in introspective self-correction to rectify discovered logical fallacies.",
            "formula": "$$\\text{Trajectory}: s_0 \\xrightarrow{\\text{Generate}} y^{(0)} \\xrightarrow{\\text{Verify}} \\mathcal{E} \\xrightarrow{\\text{Critique}} c^{(0)} \\xrightarrow{\\text{Refine}} y^{(1)}, \\quad \\text{Stop when } \\text{Verify}(y^{(t)}) = \\text{PASS}$$",
            "formula_explanation": "",
            "logic": "Pure LLM intrinsic self-correction (asking an LLM 'Are you sure?' without external feedback) often degrades performance because the model second-guesses correct answers. Grounded self-correction with deterministic tool verification (e.g. running unit tests or symbolic solvers) provides undeniable empirical ground truth, enabling reliable iterative repair.",
            "core_logic": "Pure LLM intrinsic self-correction (asking an LLM 'Are you sure?' without external feedback) often degrades performance because the model second-guesses correct answers. Grounded self-correction with deterministic tool verification (e.g. running unit tests or symbolic solvers) provides undeniable empirical ground truth, enabling reliable iterative repair.",
            "architectural_logic": "",
            "example": "Code generation with test execution: The model writes a Python graph function. A sandboxed Python subprocess executes edge cases and throws an `IndexError`. The model inspects the stack trace, diagnoses an off-by-one loop boundary, and emits the corrected patch.",
            "tags": ["Self-Correction", "Verification Loops", "Chain-of-Thought", "Reflexion"],
            "simple_summary": "Instead of expecting the AI to get code or math right on its very first try, verification loops let the AI run its code in a safe sandbox, read the error message, and fix its own mistakes until all tests pass.",
            "core_terms": [
                {
                    "term": "Grounded Self-Correction",
                    "what_is_it": "Refining an answer based on concrete external feedback (compiler error, unit test failure, calculator output).",
                    "analogy": "A mechanic test-driving a car after replacing a spark plug to confirm the engine stopped misfiring.",
                    "why_it_matters": "Reliably fixes bugs rather than getting confused in conversational circles."
                },
                {
                    "term": "Reflexion Framework (Shinn et al.)",
                    "what_is_it": "An architecture where an agent converts environment failure signals into verbal self-reflection summaries stored in episodic memory.",
                    "analogy": "An athlete keeping a journal of what went wrong in today's game to avoid repeating the same mistake tomorrow.",
                    "why_it_matters": "Improves decision-making across sequential trials without updating model weights."
                },
                {
                    "term": "Intrinsic vs Extrinsic Verification",
                    "what_is_it": "Intrinsic uses the LLM's own internal judgment to check itself; extrinsic uses deterministic compilers, linters, and APIs.",
                    "analogy": "Proofreading your own essay (intrinsic) versus running it through a grammar checker and spelling dictionary (extrinsic).",
                    "why_it_matters": "Extrinsic verification provides 100% mathematical certainty that pure neural networks lack."
                },
                {
                    "term": "Backtracking Trigger",
                    "what_is_it": "The logic that detects when an ongoing chain of thought is caught in an unproductive loop and resets to a prior checkpoint.",
                    "analogy": "Realizing you entered a dead-end maze corridor and walking back to the last fork in the road.",
                    "why_it_matters": "Prevents spending the entire token budget in an unrecoverable hallucination spiral."
                }
            ],
            "symbol_guide": [
                {"symbol": "\\mathcal{E}", "meaning": "Execution or verification error signal", "plain_english": "The compiler error or test failure output"},
                {"symbol": "c^{(t)}", "meaning": "Verbal critique / reflection summary at step t", "plain_english": "The model's diagnosis of what went wrong"},
                {"symbol": "y^{(t)}", "meaning": "Refined solution output at iteration t", "plain_english": "The updated answer"}
            ],
            "numerical_example": "Initial pass on LeetCode problem: Model generates Python code $y^{(0)}$. Sandbox executes 5 tests: 4 pass, 1 fails with `AssertionError: Expected 0 on empty list, got -1`. Verifier injects error. Model generates critique: 'I forgot to check if len(nums) == 0 before indexing'. Model emits $y^{(1)}$ with guard clause. Tests re-run: 5/5 pass. Final response returned.",
            "pitfalls": "Novice Trap: Asking an LLM to self-correct without giving it the exact error message. Vague prompts like 'Please double check your answer' frequently cause the model to change a perfectly correct answer into a wrong answer due to sycophancy bias.",
            "key_takeaways": [],
            "definition_bullets": [
                "Grounded Verification: Using external tools (compilers, calculators) to generate indisputable error signals.",
                "Reflexion Memory: Storing verbal self-critiques to guide subsequent repair attempts.",
                "Intrinsic Failure Modes: Models struggle to self-correct without external grounding or specialized verifiers.",
                "Iterative Convergence: Progressively improving candidate solutions until verification criteria are satisfied."
            ]
        },
        {
            "id": "concept_inference_scaling_laws",
            "title": "Inference Scaling Laws & Compute-Optimal Search Strategies",
            "topic_id": topic_id, "topic_label": topic_label, "category": cat, "category_label": cat_label,
            "raw_subtopic": "Inference Scaling Laws & Compute-Optimal Search Strategies", "raw_sub": "Inference Scaling Laws & Compute-Optimal Search Strategies",
            "def": "The empirical scaling laws governing test-time compute (Snell et al., Brown et al.), demonstrating that trading additional floating-point operations (FLOPs) at inference time (via extended thinking tokens, search, and verification) can achieve performance equivalent to scaling pre-training compute by 10x-100x.",
            "definition": "The empirical scaling laws governing test-time compute (Snell et al., Brown et al.), demonstrating that trading additional floating-point operations (FLOPs) at inference time (via extended thinking tokens, search, and verification) can achieve performance equivalent to scaling pre-training compute by 10x-100x.",
            "formula": "$$\\text{Total Compute} = C_{\\text{pretrain}} + N_{\\text{queries}} \\times C_{\\text{inference}}, \\quad \\text{Performance} \\propto \\alpha \\ln(C_{\\text{pretrain}}) + \\beta \\ln(C_{\\text{inference\\_search}})$$",
            "formula_explanation": "",
            "logic": "Traditional scaling laws (Kaplan, Chinchilla) focused exclusively on pre-training compute: train a bigger model on more tokens. Inference scaling laws prove that spending 1,000 thinking tokens at test time allows an 8B parameter model to outperform a 70B parameter model on complex reasoning tasks.",
            "core_logic": "Traditional scaling laws (Kaplan, Chinchilla) focused exclusively on pre-training compute: train a bigger model on more tokens. Inference scaling laws prove that spending 1,000 thinking tokens at test time allows an 8B parameter model to outperform a 70B parameter model on complex reasoning tasks.",
            "architectural_logic": "",
            "example": "OpenAI o1 and o3 reasoning models: For simple queries ('What is the capital of France?'), the model spends 0 thinking tokens. For complex cryptography and theorem proofs, the model spends 15,000 internal thinking tokens, dynamically adjusting inference compute to problem difficulty.",
            "tags": ["Inference Scaling", "Test-Time Compute", "Reasoning Tokens", "Compute Optimal"],
            "simple_summary": "In the past, to make AI smarter, you had to spend $100 million training a gigantic model. Inference scaling laws prove a smaller model can give genius-level answers if you let it 'think longer' and generate hidden reasoning tokens before answering.",
            "core_terms": [
                {
                    "term": "Thinking Tokens (<thought>)",
                    "what_is_it": "Internal chain-of-thought tokens generated by the model during inference that are hidden from the final user response.",
                    "analogy": "Writing scratch notes and doing rough math on scrap paper before writing your final answer on the exam sheet.",
                    "why_it_matters": "Provides dynamic scratchpad compute where the model can plan, deliberate, and self-correct."
                },
                {
                    "term": "Compute-Optimal Search",
                    "what_is_it": "The optimal allocation of FLOPs between candidate sampling budget, beam width, and verifier evaluations to maximize accuracy per dollar.",
                    "analogy": "Deciding whether to take 10 quick guesses or 3 very thorough, calculated guesses on an exam.",
                    "why_it_matters": "Prevents spending massive inference budgets on diminishing-return marginal gains."
                },
                {
                    "term": "Difficulty-Adaptive Inference",
                    "what_is_it": "Dynamically allocating more inference compute to hard questions and minimal compute to trivial lookups.",
                    "analogy": "A human thinking for 0.1 seconds to answer '2+2' but thinking for 30 minutes to solve an organic chemistry problem.",
                    "why_it_matters": "Dramatically lowers average server operating costs while maintaining frontier performance."
                },
                {
                    "term": "Chinchilla Pre-training vs Inference Tradeoff",
                    "what_is_it": "The economic tradeoff between spending capital upfront on pre-training larger models versus spending operational compute at inference serving.",
                    "analogy": "Buying a massive expensive industrial tractor versus renting a compact tractor with high-efficiency attachments.",
                    "why_it_matters": "Guides multi-million-dollar AI infrastructure deployment decisions."
                }
            ],
            "symbol_guide": [
                {"symbol": "C_{\\text{inference}}", "meaning": "Inference compute FLOPs allocated per prompt", "plain_english": "Tokens generated × model parameters"},
                {"symbol": "N_{\\text{queries}}", "meaning": "Total lifetime query volume served", "plain_english": "How many times users prompt the model"},
                {"symbol": "\\beta", "meaning": "Inference scaling efficiency exponent", "plain_english": "How steeply accuracy climbs as thinking time increases"}
            ],
            "numerical_example": "A standard 8B model scores 42% on AIME math benchmark. By scaling test-time compute with 4,000 thinking tokens and Best-of-32 search, the 8B model's score jumps to 78%, matching a 70B parameter model that ran with 0 search. Pre-training compute was 9x cheaper, trading upfront training cost for test-time deliberation.",
            "pitfalls": "Novice Trap: Assuming test-time scaling works for all tasks. On factual knowledge recall tasks ('Who was the 14th President of the US?'), allocating 5,000 thinking tokens does not help if the underlying model weights simply never learned the fact during pre-training. Test-time scaling accelerates algorithmic reasoning, not missing memory.",
            "key_takeaways": [],
            "definition_bullets": [
                "Thinking Tokens: Internal scratchpad compute where models deliberate before emitting final answers.",
                "Inference Scaling: Allocating extra test-time compute can match models 10x larger.",
                "Difficulty Adaptation: Dynamically sizing inference compute budget based on prompt complexity.",
                "Reasoning vs Knowledge: Test-time search excels at multi-step logic but cannot conjure missing factual knowledge."
            ]
        },
        {
            "id": "concept_reasoning_distillation_system1",
            "title": "System 2 Reasoning Distillation into System 1 Fast Models",
            "topic_id": topic_id, "topic_label": topic_label, "category": cat, "category_label": cat_label,
            "raw_subtopic": "System 2 Reasoning Distillation into System 1 Fast Models", "raw_sub": "System 2 Reasoning Distillation into System 1 Fast Models",
            "def": "The post-training methodology (DeepSeek-R1, Llama-Distill) where synthetic long-form reasoning trajectories generated by frontier System 2 models are curated and distilled into lightweight, high-speed System 1 models via Supervised Fine-Tuning (SFT) and Direct Preference Optimization (DPO).",
            "definition": "The post-training methodology (DeepSeek-R1, Llama-Distill) where synthetic long-form reasoning trajectories generated by frontier System 2 models are curated and distilled into lightweight, high-speed System 1 models via Supervised Fine-Tuning (SFT) and Direct Preference Optimization (DPO).",
            "formula": "$$\\mathcal{L}_{\\text{Distill}} = -\\sum_{t=1}^T \\log P_{\\text{Student}}(y_t | y_{<t}, x; \\theta_{\\text{small}}), \\quad \\text{where } y \\sim \\pi_{\\text{Teacher-R1}}(\\cdot | x) \\text{ filtered by } \\text{Verifier}(y) = 1$$",
            "formula_explanation": "",
            "logic": "Running huge 671B reasoning models with MCTS at inference time is too expensive for consumer hardware. By using the large reasoning model to generate 800,000 verified reasoning trajectories, small 1.5B to 8B student models can be trained directly on these thinking patterns, acquiring emergent reasoning capabilities at standard inference speeds.",
            "core_logic": "Running huge 671B reasoning models with MCTS at inference time is too expensive for consumer hardware. By using the large reasoning model to generate 800,000 verified reasoning trajectories, small 1.5B to 8B student models can be trained directly on these thinking patterns, acquiring emergent reasoning capabilities at standard inference speeds.",
            "architectural_logic": "",
            "example": "DeepSeek-R1-Distill-Qwen-1.5B: A tiny 1.5B parameter model trained on verified reasoning chains from DeepSeek-R1 (671B) scores 83% on MATH-500, outperforming massive non-reasoning foundation models like GPT-4o-mini and Claude 3.5 Sonnet (raw).",
            "tags": ["Distillation", "System 1 vs System 2", "DeepSeek R1", "Synthetic Reasoning Data"],
            "simple_summary": "Large reasoning models think deeply, but they are slow and expensive. Reasoning distillation takes thousands of their best step-by-step solutions and trains a tiny, ultra-fast model (1.5B or 8B) on them, teaching the small model how to think like a genius without the massive server cost.",
            "core_terms": [
                {
                    "term": "System 1 vs System 2 AI",
                    "what_is_it": "System 1 is fast, instinctive, automatic token generation; System 2 is slow, deliberate, introspective step-by-step reasoning.",
                    "analogy": "Solving '2+2=4' instantly in your head (System 1) versus writing out multi-digit long division on paper (System 2).",
                    "why_it_matters": "The central cognitive architecture framing modern AI reasoning research."
                },
                {
                    "term": "Synthetic Reasoning Data Generation",
                    "what_is_it": "Using frontier teacher models with MCTS and verifiers to generate millions of high-quality, verified reasoning chains.",
                    "analogy": "A grandmaster writing detailed annotations for 100,000 chess games for young students to study.",
                    "why_it_matters": "Bypasses the human labeling bottleneck with scalable, automated high-quality training tokens."
                },
                {
                    "term": "Rejection Sampling Filtering",
                    "what_is_it": "Only including synthetic reasoning chains that successfully passed independent unit tests, compilers, or answer verifiers.",
                    "analogy": "Throwing away all recipe attempts where the cake tasted burnt before compiling the master cookbook.",
                    "why_it_matters": "Ensures student models are trained exclusively on mathematically sound, hallucination-free derivations."
                },
                {
                    "term": "Edge Deployment of Reasoning Models",
                    "what_is_it": "Running distilled 1.5B to 8B reasoning models locally on laptops, smartphones, or embedded devices with zero cloud latency.",
                    "analogy": "Having a pocket calculator that can solve advanced calculus without needing internet access.",
                    "why_it_matters": "Brings private, offline, sub-50ms reasoning capabilities to consumer hardware."
                }
            ],
            "symbol_guide": [
                {"symbol": "\\pi_{\\text{Teacher}}", "meaning": "Frontier large reasoning model (e.g. 671B R1)", "plain_english": "The giant teacher generating reasoning tokens"},
                {"symbol": "\\theta_{\\text{small}}", "meaning": "Compact student model weights (e.g. 1.5B or 8B)", "plain_english": "The fast student model being fine-tuned"},
                {"symbol": "\\text{Verifier}(y)", "meaning": "Independent verification check", "plain_english": "1 if mathematically verified, 0 if flawed"}
            ],
            "numerical_example": "DeepSeek-R1 (671B MoE) generates 800,000 verified reasoning trajectories across math and coding. Fine-tuning an 8B Llama model on this dataset for 3 epochs produces DeepSeek-R1-Distill-Llama-8B. Benchmark: MATH-500 score jumps from 52% (raw Llama-8B) to 89.1%, running at 85 tokens/second locally on a MacBook M3.",
            "pitfalls": "Novice Trap: Distilling unverified teacher chains. If the teacher's hallucinations or circular loops are distilled into the student without rejection sampling verification, the student model inherits and amplifies the teacher's bad thinking habits (Distillation Collapse).",
            "key_takeaways": [],
            "definition_bullets": [
                "System 1/2 Synthesis: Distilling deliberate System 2 reasoning chains into fast System 1 student models.",
                "Rejection Sampling Quality: Training strictly on verified teacher trajectories passing automated tests.",
                "Consumer Hardware Viability: Enables 1.5B to 8B models to beat giant non-reasoning foundation models.",
                "Edge Intelligence: Bringing advanced multi-step problem solving to local devices without cloud dependency."
            ]
        }
    ]

print("Reasoning module ready.")
