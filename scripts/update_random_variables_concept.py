import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
CONCEPTS_PATH = os.path.join(ROOT_DIR, "src", "data", "concepts.json")
ALL_CONCEPTS_PATH = os.path.join(SCRIPT_DIR, "data_sources", "all_concepts.json")
MATH_PY = os.path.join(SCRIPT_DIR, "data_sources", "concepts_math.py")

rv_concept = {
    "id": "concept_random_variables_variance",
    "title": "Random Variables, Expectation & Variance",
    "topic_id": "math_prob",
    "topic_label": "Probability & Statistical Inference",
    "category": "math",
    "category_label": "Mathematical Foundations",
    "raw_subtopic": "Random Variables, Expectation (Mean μ) & Variance (σ²)",
    "def": "A random variable maps uncertain real-world events to numbers. Expectation (μ) is the probability-weighted center of gravity, and variance (σ²) measures the dispersion of outcomes around that mean.",
    "formula": "$$\\mathbb{E}[X] = \\sum_{i} x_i P(X = x_i), \\quad \\text{Var}(X) = \\mathbb{E}[(X - \\mu)^2] = \\mathbb{E}[X^2] - (\\mathbb{E}[X])^2, \\quad \\sigma = \\sqrt{\\text{Var}(X)}$$",
    "logic": "Machine learning optimizes expected risk over uncertain distributions. The bias-variance tradeoff governs generalization, while batch and layer normalization force intermediate activations to mean 0 and variance 1 to stabilize training.",
    "example": "Rolling a fair die: Outcomes 1 through 6 with probability 1/6 yield an expected value μ = 3.5, variance σ² = 2.92, and standard deviation σ = 1.71.",
    "tags": [
        "Probability",
        "Random Variables",
        "Expectation",
        "Variance",
        "Bias-Variance Tradeoff",
        "Normalization"
    ],
    "raw_sub": "Random Variables, Expectation (Mean μ) & Variance (σ²)",
    "definition": "A random variable maps uncertain events to numbers. Expectation (μ) is the probability-weighted average outcome, and variance (σ²) quantifies how far individual outcomes disperse from that center.",
    "formula_explanation": "E[X] calculates the weighted mean across all outcomes. Var(X) measures expected squared deviations from μ. The standard deviation σ = √Var brings variance back to human-readable original units.",
    "simple_summary": "A random variable turns real-world uncertainty into numbers. Expectation tells you where the center is, while variance and standard deviation tell you how wild the swings are around that center.",
    "core_terms": [
        {
            "term": "Random Variable (X)",
            "what_is_it": "• A mathematical rule or function that maps real-world uncertain events into numbers (e.g., Coin Heads → 1, Tails → 0).\n• Comes in two flavors: Discrete (countable outcomes like dice or classes) and Continuous (smooth ranges like house prices or embeddings).",
            "analogy": "A roulette wheel: the spinning ball is an uncertain event; the number pocket it lands in is the random variable X.",
            "why_it_matters": "In AI, every input feature, model prediction, and loss value is represented and evaluated as a random variable."
        },
        {
            "term": "Expectation (E[X] or μ)",
            "what_is_it": "• The probability-weighted average of all possible outcomes—the overall 'center of gravity' of your data.\n• While individual samples fluctuate randomly, their combined average naturally settles onto this expected value.",
            "analogy": "A casino's house edge: an individual spin is random, but over millions of spins, the casino expects to win an exact fixed percentage.",
            "why_it_matters": "Training machine learning models is mathematically defined as minimizing expected loss over the data distribution."
        },
        {
            "term": "Variance (σ²) & Standard Deviation (σ)",
            "what_is_it": "• Variance (σ²) measures volatility—how far individual outcomes spread from the mean: Var(X) = E[(X - μ)²].\n• Standard Deviation (σ = √Var) takes the square root to return the volatility spread back to original human-readable units.",
            "analogy": "Two investment portfolios with the same 8% average return: one stays between 7–9% (low variance), while the other swings from -40% to +60% (high variance).",
            "why_it_matters": "Squaring deviations prevents positive and negative errors from canceling, while penalizing large outlier errors quadratically."
        }
    ],
    "types_header": "Probability Foundations in Modern AI",
    "types_badge": "Statistical Pillars",
    "quick_types": [
        {
            "type": "Discrete vs. Continuous",
            "definition": "Discrete: Countable outcomes (PMF, classes 0-9). Continuous: Infinite flow (PDF, temperatures, embeddings).",
            "looks_like": "Coin Flips {0, 1} vs. Embedding Vectors [-1.4, 0.8]"
        },
        {
            "type": "Bias-Variance Tradeoff",
            "definition": "Total Error = (Bias)² + Variance + Noise. High bias underfits; high variance overfits.",
            "looks_like": "Underfitting (Too Simple) vs. Overfitting (Too Wild)"
        },
        {
            "type": "BatchNorm & LayerNorm",
            "definition": "Stabilizes deep networks by forcing internal activations to zero mean and unit variance.",
            "looks_like": "Standardized Activations: μ = 0, σ² = 1"
        },
        {
            "type": "Generative Diffusion & VAEs",
            "definition": "Generates images by starting with Gaussian noise X ~ N(0, 1) and predicting conditional expectations.",
            "looks_like": "Noise Removal: E[Image | Noisy Image]"
        },
        {
            "type": "Standard Deviation (σ)",
            "definition": "Square root of variance; restores the volatility spread to original, interpretable data units.",
            "looks_like": "σ = √Var(X) (e.g. ±$15,000 price spread)"
        }
    ],
    "symbol_guide": [
        {
            "symbol": "X",
            "meaning": "Random Variable",
            "plain_english": "A function mapping uncertain events to numbers"
        },
        {
            "symbol": "E[X] (μ)",
            "meaning": "Expected Value / Mean",
            "plain_english": "Probability-weighted average outcome (center of gravity)"
        },
        {
            "symbol": "P(X = xᵢ)",
            "meaning": "Probability Mass / Density",
            "plain_english": "The likelihood of outcome xᵢ occurring"
        },
        {
            "symbol": "Var(X) (σ²)",
            "meaning": "Variance",
            "plain_english": "Expected squared deviation measuring outcome volatility"
        },
        {
            "symbol": "σ (sigma)",
            "meaning": "Standard Deviation",
            "plain_english": "Spread of the distribution in original data units (√Var)"
        }
    ],
    "numerical_example": "Calculating Expectation & Variance for a fair 6-sided die:\nOutcomes: x ∈ {1, 2, 3, 4, 5, 6}, each with probability P(x) = 1/6.\n\n1. Expectation (Mean μ = E[X]):\n   • E[X] = (1 + 2 + 3 + 4 + 5 + 6) / 6 = 21 / 6 = 3.5\n   --> The expected center of gravity is 3.5.\n\n2. Second Moment (E[X²]):\n   • E[X²] = (1² + 2² + 3² + 4² + 5² + 6²) / 6 = (1 + 4 + 9 + 16 + 25 + 36) / 6\n   • E[X²] = 91 / 6 ≈ 15.167\n\n3. Variance (Var(X) = E[X²] - (E[X])²):\n   • Var(X) = 15.167 - (3.5)² = 15.167 - 12.25 = 2.917\n\n4. Standard Deviation (σ):\n   • σ = √2.917 ≈ 1.708\n   --> An individual roll typically fluctuates from the mean (3.5) by about ±1.71.",
    "pitfalls": "Common Trap: Forgetting that variance is measured in squared units! If predicting house prices in dollars, variance is in dollars². Always take the square root to report the Standard Deviation (σ) in actual dollars.",
    "core_logic": "Machine learning models are function approximators trained over empirical samples drawn from an underlying random distribution. Optimizing loss is equivalent to minimizing expected risk E[ℒ(y, ŷ)].",
    "architectural_logic": "In deep architectures, activation drift destabilizes gradients. Batch Normalization and Layer Normalization compute mini-batch expectations μ and variances σ² to standardize feature distributions to zero mean and unit variance, enabling stable training of deep Transformers.",
    "connected_logic": [
        {
            "title": "The Bias-Variance Tradeoff: Fundamental Law of ML",
            "content": "• Model prediction error decomposes into Error = Bias² + Variance + Irreducible Noise.\n• High bias underfits by missing the underlying trend; high variance overfits by memorizing training noise and fluctuating wildly on new test data."
        },
        {
            "title": "Batch & Layer Normalization: Taming Covariate Shift",
            "content": "• Unconstrained activations drift across training steps, causing gradient instability in deep architectures.\n• BatchNorm and LayerNorm force intermediate activations to have mean μ = 0 and variance σ² = 1, enabling stable training for 100+ layer Transformers."
        },
        {
            "title": "Generative AI: Denoising via Conditional Expectation",
            "content": "• Modern image generators (Diffusion Models, VAEs) initialize from pure Gaussian noise: X ~ N(0, 1).\n• The model learns the conditional expectation E[Image | Noisy Image], systematically subtracting noise step-by-step to unveil clean artwork."
        },
        {
            "title": "Why We Square the Difference (X - μ)²",
            "content": "• Squaring ensures positive and negative deviations never cancel each other out to zero.\n• It penalizes large errors quadratically (an error of 10 is penalized 100x vs. an error of 1), focusing optimization on catastrophic outliers."
        }
    ],
    "key_takeaways": [
        "A Random Variable (X) is a function that maps real-world uncertain events to numbers.",
        "Expectation (E[X] or μ) is the probability-weighted center of gravity of all outcomes.",
        "Variance (Var(X) or σ²) measures spread; Standard Deviation (σ = √Var) restores original units.",
        "The Bias-Variance tradeoff governs ML: high bias underfits, high variance overfits.",
        "BatchNorm/LayerNorm standardize activations to μ = 0, σ² = 1, stabilizing deep Transformers."
    ],
    "definition_bullets": [
        "Random Variable (X): Rule mapping uncertain real-world outcomes into numbers.",
        "Expectation (E[X]): Probability-weighted average outcome (center of gravity).",
        "Variance (σ²): Measurement of dispersion and volatility around the expected value."
    ]
}

# 1. Update src/data/concepts.json
with open(CONCEPTS_PATH, 'r', encoding='utf-8') as f:
    concepts = json.load(f)

for idx, c in enumerate(concepts):
    if c['id'] == 'concept_random_variables_variance':
        concepts[idx] = rv_concept
        break

with open(CONCEPTS_PATH, 'w', encoding='utf-8') as f:
    json.dump(concepts, f, indent=2, ensure_ascii=False)
print("Updated src/data/concepts.json for concept_random_variables_variance successfully!")

# 2. Update scripts/data_sources/all_concepts.json
if os.path.exists(ALL_CONCEPTS_PATH):
    with open(ALL_CONCEPTS_PATH, 'r', encoding='utf-8') as f:
        all_concepts = json.load(f)
    for idx, c in enumerate(all_concepts):
        if c['id'] == 'concept_random_variables_variance':
            all_concepts[idx] = rv_concept
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
        if c['id'] == 'concept_random_variables_variance':
            math_concepts[idx] = rv_concept
            break
    with open(MATH_PY, "w", encoding="utf-8") as f:
        f.write('"""\nConcepts Database: Mathematical Foundations (19 Concepts)\n"""\n\nMATH_CONCEPTS = ' + json.dumps(math_concepts, indent=4, ensure_ascii=False) + '\n')
    print("Updated concepts_math.py successfully!")
