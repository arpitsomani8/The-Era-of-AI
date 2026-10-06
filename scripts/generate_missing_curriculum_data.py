# scripts/generate_missing_curriculum_data.py
import json

# 1. New Topics definition
NEW_TOPICS = [
    {
        "id": "dl_rl_foundations",
        "category": "dl",
        "label": "Reinforcement Learning (RL) & Decision Foundations",
        "level": 2,
        "x": 840,
        "y": 70,
        "def": "The paradigm of machine learning where an autonomous agent learns optimal behavioral policies through sequential trial-and-error interactions with a dynamic environment to maximize cumulative scalar rewards.",
        "formula": "Bellman Optimality: Q^*(s,a) = R(s,a) + \\gamma \\sum_{s'} P(s'|s,a) \\max_{a'} Q^*(s',a') | Policy Gradient: \\nabla_\\theta J(\\theta) = \\mathbb{E}_{\\pi_\\theta} [\\nabla_\\theta \\log \\pi_\\theta(a|s) Q^{\\pi}(s,a)]",
        "logic": "Unlike supervised learning with static labels, RL models sequential credit assignment: determining which historical action caused a delayed reward or penalty in environments with transition uncertainty.",
        "example": "Autonomous driving robotics and game agents (AlphaGo, Dota 2): The agent controls steering and acceleration actions based on sensor state inputs, optimizing for distance traveled without collisions.",
        "subtopics": [
            "Markov Decision Processes (MDP) & Bellman Equation",
            "Q-Learning & Deep Q-Networks (DQN)",
            "Policy Gradients & REINFORCE Algorithm",
            "Actor-Critic Architectures (A2C & PPO)",
            "Exploration vs Exploitation (Epsilon-Greedy & UCB)"
        ],
        "connections": ["dl_root"]
    },
    {
        "id": "ml_time_series",
        "category": "ml",
        "label": "Time Series Analysis & Forecasting Dynamics",
        "level": 2,
        "x": -300,
        "y": -940,
        "def": "Statistical and machine learning methodologies for sequential, timestamped observations where temporal dependency, trend, seasonal periodicity, and non-stationarity govern future state predictions.",
        "formula": "ARIMA(p,d,q): \\Phi(B)(1 - B)^d X_t = \\Theta(B) \\epsilon_t | Autocorrelation: \\rho_k = \\frac{\\sum (X_t - \\bar{X})(X_{t-k} - \\bar{X})}{\\sum (X_t - \\bar{X})^2}",
        "logic": "Standard cross-validation leaks future information into the past. Time series models enforce strict chronological causality through rolling-origin evaluation and temporal feature engineering.",
        "example": "Retail demand forecasting: Predicting hourly sales of 10,000 SKUs using rolling lag features, calendar holidays, and historical promo windows to minimize warehouse inventory stockouts.",
        "subtopics": [
            "Stationarity, Autocorrelation (ACF/PACF) & Differencing",
            "ARIMA, SARIMAX & Exponential Smoothing",
            "Modern Forecasting: Prophet & Temporal Fusion Transformers (TFT)",
            "Time-Series Feature Engineering & Lag Variables",
            "Rolling-Window & Expanding-Window Cross Validation"
        ],
        "connections": ["ml_root"]
    },
    {
        "id": "ml_recsys",
        "category": "ml",
        "label": "Recommender Systems (RecSys) & Retrieval Architecture",
        "level": 2,
        "x": 100,
        "y": -940,
        "def": "Information filtering engines that predict user preference or engagement ratings across millions of catalog items using matrix factorization, two-tower vector embeddings, and ranking cascades.",
        "formula": "Matrix Factorization: \\min_{P,Q} \\sum_{(u,i) \\in R} (r_{ui} - p_u^T q_i)^2 + \\lambda (\\|p_u\\|^2 + \\|q_i\\|^2) | NDCG@K = \\frac{DCG@K}{IDCG@K}",
        "logic": "Industrial recommendation uses a multi-stage funnel: fast candidate generation (retrieving top 1,000 from 100M items in 10ms) followed by heavy neural scoring and calibration.",
        "example": "E-commerce and streaming homepages (Netflix, Amazon): Personalizing real-time video carousels based on watch history, session clicks, and collaborative user interaction clusters.",
        "subtopics": [
            "Collaborative Filtering & Matrix Factorization (SVD & ALS)",
            "Two-Tower Neural Retrieval Architectures",
            "Deep & Cross Networks (DCN) & Wide & Deep Learning",
            "Candidate Generation vs Heavy Ranking Stages",
            "RecSys Evaluation Metrics: NDCG, MRR & Hit Rate@K"
        ],
        "connections": ["ml_root"]
    },
    {
        "id": "dl_gnn",
        "category": "dl",
        "label": "Graph Neural Networks (GNN) & Geometric Deep Learning",
        "level": 2,
        "x": 1260,
        "y": 70,
        "def": "Deep learning architectures designed for non-Euclidean graph topologies where nodes, edges, and relational message-passing aggregate neighborhood features invariant to graph isomorphism.",
        "formula": "GCN Layer: H^{(l+1)} = \\sigma\\left(\\tilde{D}^{-\\frac{1}{2}} \\tilde{A} \\tilde{D}^{-\\frac{1}{2}} H^{(l)} W^{(l)}\\right) | Message Passing: m_{v} = \\sum_{u \\in \\mathcal{N}(v)} M(h_u, h_v, e_{uv})",
        "logic": "Standard convolutions assume rigid 2D grids (pixels). GNNs generalize convolution by aggregating permutation-invariant feature messages across variable-degree neighbor graphs.",
        "example": "Financial fraud rings and drug discovery: Predicting toxic molecular properties by modeling chemical bonds as graph edges and atomic elements as feature-laden nodes.",
        "subtopics": [
            "Graph Representations, Adjacency Matrices & Node Features",
            "Graph Convolutional Networks (GCN) & Message Passing",
            "Graph Attention Networks (GAT) & Edge Attentions",
            "Inductive Graph Representation (GraphSAGE)",
            "Link Prediction & Node Classification Pipelines"
        ],
        "connections": ["dl_root"]
    },
    {
        "id": "eval_xai",
        "category": "eval",
        "label": "Explainable AI (XAI) & Model Interpretability",
        "level": 2,
        "x": 520,
        "y": 540,
        "def": "Theoretical frameworks and empirical diagnostics that deconstruct black-box machine learning decisions into human-interpretable feature attributions, counterfactuals, and sensitivity profiles.",
        "formula": "Shapley Value: \\phi_i(v) = \\sum_{S \\subseteq N \\setminus \\{i\\}} \\frac{|S|!(|N|-|S|-1)!}{|N|!} (v(S \\cup \\{i\\}) - v(S)) | LIME: \\xi(x) = \\arg\\min_{g \\in G} \\mathcal{L}(f, g, \\pi_x) + \\Omega(g)",
        "logic": "High predictive accuracy without transparency creates catastrophic risks in regulated sectors. Explainability methods guarantee fairness, uncover spurious shortcuts, and satisfy GDPR compliance.",
        "example": "Credit underwriting and medical triage: Explaining why a mortgage applicant was flagged as high risk by quantifying the exact marginal contribution of debt-to-income ratio vs credit history.",
        "subtopics": [
            "SHAP (Shapley Additive Explanations) & Game Theory",
            "LIME (Local Interpretable Model-agnostic Explanations)",
            "Integrated Gradients & Neural Saliency Maps",
            "Permutation Feature Importance & Partial Dependence Plots (PDP)",
            "Model Governance, Auditing & Regulatory AI Compliance"
        ],
        "connections": ["eval_root"]
    },
    {
        "id": "genai_audio_speech",
        "category": "genai",
        "label": "Audio, Speech AI & Voice Intelligence",
        "level": 2,
        "x": 840,
        "y": 520,
        "def": "Multimodal neural architectures that process continuous 1D acoustic sound waves, spectrogram representations, and speech tokens for transcription, synthesis, and voice interaction.",
        "formula": "STFT: X(\\tau, \\omega) = \\int_{-\\infty}^{\\infty} x(t) w(t-\\tau) e^{-j\\omega t} dt | CTC Loss: \\mathcal{L}_{\\text{CTC}} = -\\log \\sum_{\\pi \\in \\mathcal{B}^{-1}(y)} P(\\pi|x)",
        "logic": "Raw audio samples arrive at 16,000 to 48,000 Hz. Audio AI transforms raw pressure waves into 2D time-frequency Mel-spectrograms before feeding them into deep conformer or transformer encoders.",
        "example": "Real-time multilingual voice assistants (Whisper, ElevenLabs): Streaming acoustic transcription and zero-shot voice cloning with sub-200ms latency for conversational human-AI phone support.",
        "subtopics": [
            "Audio Preprocessing: Mel-Spectrograms, STFT & Waveforms",
            "Automatic Speech Recognition (ASR & Whisper Architecture)",
            "CTC (Connectionist Temporal Classification) Loss Mechanics",
            "Text-to-Speech (TTS) & Neural Audio Synthesizers",
            "Real-Time Streaming Voice Agents & Audio Embeddings"
        ],
        "connections": ["genai_root"]
    },
    {
        "id": "genai_reasoning_test_time",
        "category": "genai",
        "label": "Reasoning Models, Test-Time Compute & System 2 AI",
        "level": 2,
        "x": 1260,
        "y": 520,
        "def": "Frontier architectures and search algorithms that scale inference-time compute (test-time search, verification loops, and process reward guidance) to solve complex multi-step reasoning problems.",
        "formula": "Test-Time Scaling: \\text{Accuracy} \\propto f(N_{\\text{search}}, N_{\\text{tokens}}) | PRM Value: R_{\\text{step}} = P(\\text{Step } k \\text{ is correct} | s_{1:k-1})",
        "logic": "Standard LLMs generate next tokens impulsively (System 1 fast thinking). Reasoning models (like OpenAI o1/o3 and DeepSeek R1) allocate adaptive compute at inference time to deliberate, verify, and backtrack.",
        "example": "Autonomous competitive coding and formal mathematical proofs: An agent generates multiple solution trajectories, evaluates step-level validity with a verifier, and prunes flawed logic branches.",
        "subtopics": [
            "Process Reward Models (PRM) vs Outcome Reward Models (ORM)",
            "Test-Time Search: Monte Carlo Tree Search (MCTS) & Beam Search",
            "Chain-of-Thought (CoT) Self-Correction & Verification Loops",
            "Inference Scaling Laws & Compute-Optimal Search Strategies",
            "System 2 Reasoning Distillation into System 1 Fast Models"
        ],
        "connections": ["genai_root"]
    }
]

print(f"Loaded {len(NEW_TOPICS)} new topics definitions.")
