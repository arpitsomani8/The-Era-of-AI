import json

KL_DIVERGENCE_UPDATE = {
    "def": "Kullback-Leibler (KL) Divergence measures how different one probability distribution is from another. It quantifies the information penalty or wasted bits suffered when using an approximating distribution Q to represent the true distribution P.",
    "definition": "Kullback-Leibler (KL) Divergence measures how different one probability distribution is from another. It quantifies the information penalty or wasted bits suffered when using an approximating distribution Q to represent the true distribution P.",
    "formula": "$$D_{\\text{KL}}(P \\parallel Q) = \\sum_{x} P(x) \\log\\left( \\frac{P(x)}{Q(x)} \\right) = H(P, Q) - H(P)$$",
    "formula_explanation": "",
    "logic": "Always non-negative (D_KL ≥ 0) via Gibbs' inequality, and zero if and only if P = Q. Used in Variational Autoencoders (VAEs) and RLHF / DPO to prevent fine-tuned models from drifting too far from their base pre-trained models.",
    "example": "Comparing P = [0.8, 0.2] with Q = [0.5, 0.5]: D_KL(P || Q) = 0.8 log₂(0.8/0.5) + 0.2 log₂(0.2/0.5) ≈ 0.278 bits. Reverse D_KL(Q || P) ≈ 0.322 bits, illustrating that divergence is asymmetric.",
    "simple_summary": "KL Divergence measures the wasted bits when approximating reality P with model Q (Cross-Entropy minus True Entropy). It is always ≥ 0, asymmetric, and powers RLHF alignment in LLMs, VAE latent spaces, and Knowledge Distillation.",
    "core_terms": [
        {
            "term": "KL Divergence (Relative Entropy)",
            "what_is_it": "• A statistical measure of the difference between two probability distributions: D_KL(P || Q) = H(P, Q) - H(P).\n• Quantifies the 'wasted bits' or extra information penalty suffered when using model Q to approximate reality P.",
            "analogy": "Packing clothes for a vacation: P is the actual weather, Q is your forecast. If Q matches P, you packed perfectly (0 wasted space). If Q is wrong, the excess luggage represents KL Divergence.",
            "why_it_matters": "The fundamental objective measuring how far an AI model's beliefs deviate from true data or reference behaviors."
        },
        {
            "term": "Forward KL (Mean-Seeking / Zero-Avoiding)",
            "what_is_it": "• Evaluates D_KL(P || Q) by averaging under the true distribution P: wherever reality occurs (P > 0), model Q must not be zero.\n• Forces the model to spread out broadly to cover all modes, preferring a safe, blurry over-generalization to missing any real data.",
            "analogy": "A search party that spreads wide across the entire forest so that no area is left unchecked, even if members are spread thin.",
            "why_it_matters": "The underlying foundation of Maximum Likelihood Estimation (MLE) and standard supervised classification."
        },
        {
            "term": "Reverse KL (Mode-Seeking / Zero-Forcing)",
            "what_is_it": "• Evaluates D_KL(Q || P) by averaging under model distribution Q: wherever reality is zero (P = 0), model Q must also be zero.\n• Forces the model to lock onto a single high-probability mode with laser precision while ignoring alternative peaks.",
            "analogy": "A specialist investor who puts all capital into the single safest asset rather than spreading funds across uncertain bets.",
            "why_it_matters": "Drives variational inference in VAEs and acts as the alignment anchor in RLHF, preventing LLMs from generating unnatural outputs."
        }
    ],
    "types_header": "Properties & Directions of KL Divergence",
    "types_badge": "Divergence Dynamics",
    "quick_types": [
        {
            "type": "Non-Negativity (Gibbs' Inequality)",
            "definition": "D_KL(P || Q) ≥ 0 always. It reaches exactly 0 if and only if P = Q (perfect model match).",
            "looks_like": "D_KL(P || Q) ≥ 0, with D_KL = 0 ⟺ P = Q"
        },
        {
            "type": "Asymmetry (Not a Metric Distance)",
            "definition": "D_KL(P || Q) ≠ D_KL(Q || P). Direction dictates whether the model behaves as mean-seeking or mode-seeking.",
            "looks_like": "Direction Matters: D_KL(P || Q) ≠ D_KL(Q || P)"
        },
        {
            "type": "The Infinite Blind Spot",
            "definition": "If P(x) > 0 but Q(x) = 0, P(x)/Q(x) explodes to infinity, producing an infinite divergence penalty.",
            "looks_like": "P(x) > 0 and Q(x) = 0 → D_KL = ∞"
        },
        {
            "type": "Forward KL: Mean-Seeking",
            "definition": "Covers the entire distribution P by spreading out mass (zero-avoiding). Used in Supervised Learning & MLE.",
            "looks_like": "Wide, smooth coverage across all data modes"
        },
        {
            "type": "Reverse KL: Mode-Seeking",
            "definition": "Locks tightly onto the primary peak of P (zero-forcing). Used in VAE latent spaces and RLHF alignment.",
            "looks_like": "Sharp, focused concentration on primary peak"
        }
    ],
    "symbol_guide": [
        {
            "symbol": "D_KL(P || Q)",
            "meaning": "KL Divergence",
            "plain_english": "Information penalty in bits or nats when approximating distribution P with Q"
        },
        {
            "symbol": "P(x)",
            "meaning": "True Distribution",
            "plain_english": "The ground truth or target reference probability distribution"
        },
        {
            "symbol": "Q(x)",
            "meaning": "Model Distribution",
            "plain_english": "The predicted or approximating probability distribution"
        },
        {
            "symbol": "H(P, Q)",
            "meaning": "Cross-Entropy",
            "plain_english": "Total average cost of describing reality P using model Q"
        },
        {
            "symbol": "H(P)",
            "meaning": "Shannon Entropy",
            "plain_english": "Irreducible baseline uncertainty inherent in the true distribution P"
        },
        {
            "symbol": "∑ (Sigma)",
            "meaning": "Summation",
            "plain_english": "Adds up the probability-weighted log-ratios across all possible states x"
        }
    ],
    "numerical_example": "Comparing True Distribution P = [0.8, 0.2] with Model Q = [0.5, 0.5]:\n1. Log Ratios:\n   • State 1: P(1)/Q(1) = 0.8 / 0.5 = 1.6  --> log₂(1.6) ≈ 0.678 bits\n   • State 2: P(2)/Q(2) = 0.2 / 0.5 = 0.4  --> log₂(0.4) ≈ -1.322 bits\n\n2. Weighted Sum:\n   • D_KL(P || Q) = 0.8 · log₂(1.6) + 0.2 · log₂(0.4)\n   • D_KL(P || Q) = 0.8(0.678) + 0.2(-1.322) = 0.542 - 0.264 ≈ 0.278 bits.\n\n3. The Asymmetry Check: D_KL(Q || P) = 0.5 log₂(0.5/0.8) + 0.5 log₂(0.5/0.2) = 0.5(-0.678) + 0.5(1.322) ≈ 0.322 bits.\nNotice that D_KL(P || Q) ≠ D_KL(Q || P) — proving direction matters!",
    "pitfalls": "Common Pitfall: Treating KL Divergence as a symmetric distance function. Setting D_KL(P || Q) as an objective encourages broad distribution-covering (mean-seeking), whereas D_KL(Q || P) forces sharp mode-seeking. Confusing the order causes severe training instability in generative models.",
    "core_logic": "Why this matters: KL Divergence measures the exact difference between Cross-Entropy and True Shannon Entropy: D_KL(P || Q) = H(P, Q) - H(P). It grounds the loss formulations of VAEs, Knowledge Distillation, and RLHF alignment.",
    "architectural_logic": "In LLM post-training (RLHF / PPO / DPO), the objective includes a KL penalty -β D_KL(π_θ || π_ref) against the frozen reference model. This prevents reward model over-optimization (reward hacking) and keeps the model from drifting into hallucinated nonsense.",
    "connected_logic": [
        {
            "title": "RLHF in LLMs: The Alignment Bungee Cord",
            "content": "• When fine-tuning LLMs with human feedback, maximizing reward alone causes reward hacking (incoherent responses that game the reward model).\n• Adding a Reverse KL penalty -β D_KL(π_θ || π_ref) acts as an invisible bungee cord, keeping the updated model anchored safely near the original base LLM."
        },
        {
            "title": "Variational Autoencoders: Organizing Latent Space",
            "content": "• VAEs compress images into latent codes z; the loss balances pixel reconstruction error against D_KL(q(z|x) || N(0, I)).\n• This KL term forces the learned latent space into a continuous, smooth standard Gaussian bell curve without empty holes or dead zones."
        },
        {
            "title": "t-SNE: Preserving High-Dimensional Manifolds",
            "content": "• t-SNE computes pairwise neighborhood similarities P in high-dimensional space and sets up low-dimensional student-t coordinates Q in 2D.\n• Minimizing D_KL(P || Q) via gradient descent forces 2D points to faithfully reflect the local cluster topology of high-dimensional embeddings."
        },
        {
            "title": "Knowledge Distillation: Compressing Frontier Models",
            "content": "• Distilling a massive 70B parameter teacher into an 8B edge-device student involves passing the same inputs through both models.\n• The student is trained to minimize the KL divergence between its soft output probabilities and the teacher's logits, transferring nuanced reasoning dark knowledge."
        }
    ],
    "key_takeaways": [
        "Fundamental Identity: Cross-Entropy = Shannon Entropy + KL Divergence (H(P, Q) = H(P) + D_KL(P || Q)).",
        "Non-Negative & Asymmetric: Always ≥ 0, equals 0 only when P = Q, but D_KL(P || Q) ≠ D_KL(Q || P).",
        "Forward vs. Reverse: Forward KL seeks the mean (zero-avoiding); Reverse KL seeks the mode (zero-forcing).",
        "Modern AI Linchpin: Essential for RLHF alignment in LLMs, continuous latent spaces in VAEs, and Knowledge Distillation."
    ],
    "definition_bullets": [
        "KL Divergence: An asymmetric statistical measure of information lost or extra bits wasted when approximating true distribution P with model Q.",
        "Relative Entropy: Another name for KL Divergence, reflecting how much information one distribution contains relative to another."
    ]
}

def update_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    found = False
    for item in data:
        if item.get('id') == 'concept_kl_divergence':
            item.update(KL_DIVERGENCE_UPDATE)
            found = True
            break
            
    if not found:
        print(f"Warning: concept_kl_divergence not found in {filepath}")
        return False
        
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Successfully updated {filepath}")
    return True

# Update concepts.json and all_concepts.json
update_json_file('src/data/concepts.json')
update_json_file('scripts/data_sources/all_concepts.json')

# Update concepts_math.py
def update_concepts_math():
    filepath = 'scripts/data_sources/concepts_math.py'
    import importlib.util
    spec = importlib.util.spec_from_file_location("concepts_math", filepath)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    
    for item in mod.MATH_CONCEPTS:
        if item.get('id') == 'concept_kl_divergence':
            item.update(KL_DIVERGENCE_UPDATE)
            break
            
    new_content = '"""\nConcepts Database: Mathematical Foundations (19 Concepts)\n"""\n\nMATH_CONCEPTS = ' + json.dumps(mod.MATH_CONCEPTS, indent=4, ensure_ascii=False) + '\n'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Successfully updated {filepath}")

update_concepts_math()
