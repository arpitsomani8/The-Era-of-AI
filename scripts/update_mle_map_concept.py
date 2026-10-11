import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
CONCEPTS_PATH = os.path.join(ROOT_DIR, "src", "data", "concepts.json")
ALL_CONCEPTS_PATH = os.path.join(SCRIPT_DIR, "data_sources", "all_concepts.json")
MATH_PY = os.path.join(SCRIPT_DIR, "data_sources", "concepts_math.py")

mle_map_concept = {
    "id": "concept_mle_map",
    "title": "Maximum Likelihood (MLE) vs MAP Estimation",
    "topic_id": "math_prob",
    "topic_label": "Probability & Statistical Inference",
    "category": "math",
    "category_label": "Mathematical Foundations",
    "raw_subtopic": "Maximum Likelihood Estimation (MLE) vs MAP Estimation",
    "def": "Maximum Likelihood Estimation (MLE) chooses parameters that make observed data most probable without prior assumptions. Maximum A Posteriori (MAP) balances data likelihood with prior beliefs to prevent overfitting.",
    "formula": "$$\\theta_{\\text{MLE}} = \\arg\\max_\\theta \\sum_{i=1}^N \\log P(x_i \\mid \\theta), \\quad \\theta_{\\text{MAP}} = \\arg\\max_\\theta \\left[ \\sum_{i=1}^N \\log P(x_i \\mid \\theta) + \\log P(\\theta) \\right]$$",
    "logic": "MLE forms standard deep learning loss functions (MSE and Cross-Entropy) via Negative Log-Likelihood. MAP introduces regularization: placing a Gaussian prior on weights derives L2 weight decay, while a Laplace prior derives L1 lasso sparsity.",
    "example": "Flipping a coin 10 times with 7 heads: MLE concludes θ = 0.70 based purely on data. MAP incorporates a fair-coin prior to estimate θ ≈ 0.64, preventing extreme conclusions from small samples.",
    "tags": [
        "MLE",
        "MAP",
        "Frequentist",
        "Bayesian",
        "L1 Regularization",
        "L2 Regularization"
    ],
    "raw_sub": "Maximum Likelihood Estimation (MLE) vs MAP Estimation",
    "definition": "MLE finds parameters that maximize the probability of observed data without any priors. MAP finds parameters that maximize the posterior, balancing data likelihood against prior beliefs.",
    "formula_explanation": "MLE maximizes the log-likelihood of observed samples xᵢ. MAP adds the log-prior log P(θ), penalizing unlikely parameter configurations to regularize model complexity.",
    "simple_summary": "MLE says: 'I only trust the data I saw.' MAP says: 'I trust the data, but I balance it with common sense.' On small data, MAP prevents wild conclusions; on huge data, both reach the same answer.",
    "core_terms": [
        {
            "term": "Maximum Likelihood Estimation (MLE)",
            "what_is_it": "• The Frequentist method: picks parameters that make observed training data as probable as possible: θ_MLE = argmax P(Data | θ).\n• Relies 100% on the data with zero prior assumptions—fits the sample perfectly, but can overfit on small batches.",
            "analogy": "A literal courtroom judge who only considers physical evidence presented in the trial, ignoring all outside context or prior reputation.",
            "why_it_matters": "Inverting likelihood into Negative Log-Likelihood (NLL) directly derives standard AI loss functions (MSE and Cross-Entropy)."
        },
        {
            "term": "Maximum A Posteriori (MAP)",
            "what_is_it": "• The Bayesian method: balances observed data against prior knowledge: θ_MAP = argmax [P(Data | θ) · P(θ)].\n• Incorporates baseline beliefs to keep estimates grounded when training data is noisy or scarce.",
            "analogy": "An experienced doctor who examines test results but also factors in your age, family history, and general lifestyle before making a diagnosis.",
            "why_it_matters": "Directly derives L1 (Lasso) and L2 (Weight Decay) regularization in deep neural networks."
        },
        {
            "term": "The Coin Flip Experiment (Data vs. Prior)",
            "what_is_it": "• Flipping a coin 10 times and observing 7 Heads and 3 Tails:\n• MLE strictly follows data: θ = 7/10 = 0.70. MAP balances with a 50/50 prior: θ ≈ 0.64, avoiding extreme conclusions.",
            "analogy": "If you flip a coin 3 times and get 3 heads, MLE claims tails is impossible (θ = 1.0), while MAP recognizes 3 flips is just a small sample.",
            "why_it_matters": "Demonstrates why unregularized models overfit on small datasets and why Bayesian priors keep AI stable."
        }
    ],
    "types_header": "MLE vs. MAP: The Grand Duality",
    "types_badge": "Estimation Comparison",
    "quick_types": [
        {
            "type": "Core Philosophy",
            "definition": "MLE: Frequentist (only trust observed data). MAP: Bayesian (balance data with prior knowledge).",
            "looks_like": "Data-Only vs. Data + Prior Knowledge"
        },
        {
            "type": "Mathematical Objective",
            "definition": "MLE: argmax P(Data | θ). MAP: argmax [P(Data | θ) · P(θ)].",
            "looks_like": "Pure Likelihood vs. Posterior Mode"
        },
        {
            "type": "Small-Sample Risk",
            "definition": "MLE: Extreme overfitting (3 heads in 3 flips → θ = 1.0). MAP: Prior prevents wild conclusions (θ ≈ 0.60).",
            "looks_like": "High Overfitting Risk vs. Grounded by Prior"
        },
        {
            "type": "The Regularization Duality",
            "definition": "Setting a Gaussian prior creates L2 Regularization (Weight Decay); a Laplace prior creates L1 Regularization (Lasso).",
            "looks_like": "Standard Loss + L1 / L2 Penalty"
        },
        {
            "type": "As Data Grows (N → ∞)",
            "definition": "As sample size grows toward infinity, the data completely overwhelms the prior—both converge to the identical answer!",
            "looks_like": "N → ∞: θ_MAP converges to θ_MLE"
        }
    ],
    "symbol_guide": [
        {
            "symbol": "θ (theta)",
            "meaning": "Model Parameter",
            "plain_english": "The unknown weight, probability, or setting being estimated"
        },
        {
            "symbol": "argmax_θ",
            "meaning": "Argument of Maximum",
            "plain_english": "The specific parameter value θ that produces the highest score"
        },
        {
            "symbol": "P(xᵢ | θ)",
            "meaning": "Sample Likelihood",
            "plain_english": "Probability of observing sample xᵢ given parameter setting θ"
        },
        {
            "symbol": "P(θ)",
            "meaning": "Parameter Prior",
            "plain_english": "Prior probability distribution penalizing unlikely parameter values"
        },
        {
            "symbol": "N",
            "meaning": "Sample Size",
            "plain_english": "Total number of observations in the training dataset"
        }
    ],
    "numerical_example": "Estimating Coin Bias θ from 10 flips (7 Heads, 3 Tails):\n\n1. Maximum Likelihood Estimation (MLE):\n   • Likelihood L(θ) = θ⁷(1 - θ)³\n   • Maximizing gives d/dθ [7 log θ + 3 log(1 - θ)] = 7/θ - 3/(1 - θ) = 0\n   --> θ_MLE = 7 / 10 = 0.70 (Pure data: 70% heads)\n\n2. Maximum A Posteriori (MAP with Prior):\n   • Assume a fair-coin prior Beta(α=3, β=3) representing 2 virtual heads and 2 virtual tails: P(θ) ∝ θ²(1 - θ)²\n   • Posterior: P(θ | Data) ∝ θ⁷⁺² (1 - θ)³⁺² = θ⁹ (1 - θ)⁵\n   • Peak value = (7 + 2) / (10 + 4) = 9 / 14 ≈ 0.643\n   --> θ_MAP ≈ 0.64 (Pulled back toward 0.50 by common sense!)\n\nInsight:\nAs flips increase to 1,000 (700 Heads, 300 Tails), θ_MAP = 702 / 1004 = 0.699 ≈ θ_MLE. Data overwhelms the prior!",
    "pitfalls": "Common Trap: Thinking MLE and MAP give different results on massive datasets. When N is in the millions (like LLM pretraining data), the data term completely dominates the prior term, causing MAP and MLE to converge to the exact same parameter weights.",
    "core_logic": "Ridge regression is mathematically identical to MAP estimation assuming a zero-mean Gaussian prior on weights; Lasso regression is MAP with a zero-mean Laplace prior on weights.",
    "architectural_logic": "In deep learning frameworks, Negative Log-Likelihood (NLL) forms the loss objective. Weight decay in optimizers like AdamW implements MAP estimation with a zero-mean Gaussian prior, regularizing billions of parameters to prevent overfitting without requiring full Bayesian integration.",
    "connected_logic": [
        {
            "title": "Negative Log-Likelihood: All AI Losses in Disguise",
            "content": "• Machine learning minimizes error rather than maximizing probability, turning products into sums via -log P(Data | θ).\n• Assuming Gaussian noise derives Mean Squared Error (MSE); assuming Bernoulli outcomes derives Binary Cross-Entropy (BCE)."
        },
        {
            "title": "The Gaussian Prior & L2 Regularization (Weight Decay)",
            "content": "• Placing a zero-mean Gaussian prior θ ~ N(0, σ²) penalizes -log P(θ) = λ ∑ θᵢ².\n• This is mathematically identical to L2 Regularization, shrinking weights toward zero to prevent memorizing random noise."
        },
        {
            "title": "The Laplace Prior & L1 Regularization (Lasso Sparsity)",
            "content": "• Placing a Laplace prior (with a sharp pointy peak at zero) penalizes -log P(θ) = λ ∑ |θᵢ|.\n• This is mathematically identical to L1 Regularization, driving unimportant weights to absolute zero for automatic feature selection."
        },
        {
            "title": "Sample Size Asymptotics: When Data Overwhelms the Prior",
            "content": "• With small samples (e.g. 5 records), the prior protects the model from catastrophic overfitting.\n• When dataset size grows to millions (N → ∞), the data evidence completely overwhelms the prior, causing MAP and MLE to converge to the identical answer."
        }
    ],
    "key_takeaways": [
        "MLE chooses parameters that maximize data likelihood alone (Frequentist approach).",
        "MAP incorporates a prior belief to prevent overfitting on small samples (Bayesian approach).",
        "Standard deep learning loss functions (MSE, Cross-Entropy) are Negative Log-Likelihood (NLL) in disguise.",
        "MAP with a Gaussian prior derives L2 Regularization; MAP with a Laplace prior derives L1 Regularization.",
        "As sample size N grows to infinity, MAP converges to MLE as data overwhelms the prior."
    ],
    "definition_bullets": [
        "MLE: Parameter estimation maximizing data probability without prior assumptions.",
        "MAP: Bayesian estimation balancing data likelihood with parameter prior beliefs.",
        "Regularization Duality: L2 weight decay is MAP with a Gaussian prior; L1 lasso is MAP with a Laplace prior."
    ]
}

# 1. Update src/data/concepts.json
with open(CONCEPTS_PATH, 'r', encoding='utf-8') as f:
    concepts = json.load(f)

for idx, c in enumerate(concepts):
    if c['id'] == 'concept_mle_map':
        concepts[idx] = mle_map_concept
        break

with open(CONCEPTS_PATH, 'w', encoding='utf-8') as f:
    json.dump(concepts, f, indent=2, ensure_ascii=False)
print("Updated src/data/concepts.json for concept_mle_map successfully!")

# 2. Update scripts/data_sources/all_concepts.json
if os.path.exists(ALL_CONCEPTS_PATH):
    with open(ALL_CONCEPTS_PATH, 'r', encoding='utf-8') as f:
        all_concepts = json.load(f)
    for idx, c in enumerate(all_concepts):
        if c['id'] == 'concept_mle_map':
            all_concepts[idx] = mle_map_concept
            break
    with open(ALL_CONCEPTS_PATH, 'w', encoding='utf-8') as f:
        json.dump(all_concepts, f, indent=2, ensure_ascii=False)
    print("Updated scripts/data_sources/all_concepts.json successfully!")

# 3. Update concepts_math.py
if os.path.exists(MATH_PY):
    import importlib.util
    spec = importlib.util.spec_from_file_location("concepts_math", MATH_PY)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    math_concepts = mod.MATH_CONCEPTS
    for idx, c in enumerate(math_concepts):
        if c['id'] == 'concept_mle_map':
            math_concepts[idx] = mle_map_concept
            break
    with open(MATH_PY, "w", encoding="utf-8") as f:
        f.write('"""\nConcepts Database: Mathematical Foundations (19 Concepts)\n"""\n\nMATH_CONCEPTS = ' + json.dumps(math_concepts, indent=4, ensure_ascii=False) + '\n')
    print("Updated concepts_math.py successfully!")
