import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
CONCEPTS_PATH = os.path.join(ROOT_DIR, "src", "data", "concepts.json")
ALL_CONCEPTS_PATH = os.path.join(SCRIPT_DIR, "data_sources", "all_concepts.json")
MATH_PY = os.path.join(SCRIPT_DIR, "data_sources", "concepts_math.py")

dist_concept = {
    "id": "concept_prob_distributions",
    "title": "Distributions: Gaussian, Bernoulli & Poisson",
    "topic_id": "math_prob",
    "topic_label": "Probability & Statistical Inference",
    "category": "math",
    "category_label": "Mathematical Foundations",
    "raw_subtopic": "Distributions: Gaussian (Bell Curve), Bernoulli, Poisson",
    "def": "Probability distributions map uncertainty by quantifying the likelihood of different outcomes. Bernoulli governs binary choices, Poisson counts rare discrete events, and Gaussian models continuous natural bell curves.",
    "formula": "$$P(y) = p^y (1-p)^{1-y}, \\quad P(k) = \\frac{\\lambda^k e^{-\\lambda}}{k!}, \\quad p(x) = \\frac{1}{\\sqrt{2\\pi\\sigma^2}} e^{-\\frac{(x-\\mu)^2}{2\\sigma^2}}$$",
    "logic": "The choice of loss function directly mirrors the assumed data distribution: Bernoulli leads to Binary Cross-Entropy, Poisson leads to Poisson deviance loss, and Gaussian noise mathematically justifies Mean Squared Error (MSE).",
    "example": "Bernoulli classifies spam vs. not spam (0 or 1); Poisson predicts server API requests per second (λ = 5); Gaussian models continuous prediction errors and generative diffusion noise.",
    "tags": [
        "Probability Distributions",
        "Gaussian",
        "Bernoulli",
        "Poisson",
        "Binary Cross-Entropy",
        "Diffusion Models"
    ],
    "raw_sub": "Distributions: Gaussian (Bell Curve), Bernoulli, Poisson",
    "definition": "A probability distribution maps uncertainty, defining which outcomes are likely or rare. Three distributions form the bedrock of AI: Bernoulli (binary choices), Poisson (discrete counts), and Gaussian (continuous bell curve).",
    "formula_explanation": "Bernoulli uses parameter p for binary success. Poisson uses arrival rate λ for integer counts k. Gaussian uses mean μ and variance σ² for continuous values, forming the universal bell curve via the Central Limit Theorem.",
    "simple_summary": "Think of distributions as maps of uncertainty. Bernoulli decides Yes or No; Poisson counts how many times something happens; Gaussian describes the smooth bell curve of nature and generative AI.",
    "core_terms": [
        {
            "term": "Bernoulli Distribution (The Binary Choice)",
            "what_is_it": "• Models a single trial with only two possible outcomes: Success (1) with probability p, or Failure (0) with probability 1 - p.\n• Discrete distribution with mean E[X] = p and variance Var(X) = p(1 - p).",
            "analogy": "A single coin toss: Heads (1) with 50% probability, Tails (0) with 50% probability.",
            "why_it_matters": "Powers all binary classification (Spam / Not Spam), Sigmoid outputs, Dropout regularization, and Binary Cross-Entropy (BCE) loss."
        },
        {
            "term": "Poisson Distribution (The Event Counter)",
            "what_is_it": "• Models the count of independent, rare events occurring in a fixed window of time or space at an average rate λ.\n• A unique mathematical property: its Mean and Variance are always identical (E[X] = λ, Var(X) = λ).",
            "analogy": "Counting incoming customer support chats in a 10-minute window, where you average 3 chats per interval.",
            "why_it_matters": "Drives Poisson count regression and manages AI infrastructure (GPU cluster scheduling and API token rate-limiting)."
        },
        {
            "term": "Gaussian / Normal Distribution (The Bell Curve)",
            "what_is_it": "• A continuous, symmetrical bell curve governed by mean μ (center) and variance σ² (spread).\n• By the Central Limit Theorem (CLT), summing multiple independent random variables naturally produces a Gaussian curve.",
            "analogy": "Human adult heights: most people cluster near the average (5'9\"), with very few people under 4'5\" or over 7'0\".",
            "why_it_matters": "The mathematical foundation of Mean Squared Error (MSE), neural network weight initialization, VAEs, and modern Generative Diffusion models."
        }
    ],
    "types_header": "The Three Pillar Distributions of AI",
    "types_badge": "Distribution Comparison",
    "quick_types": [
        {
            "type": "Bernoulli Distribution",
            "definition": "Discrete Binary {0, 1}. Mean = p, Variance = p(1 - p).",
            "looks_like": "Binary Classification, Sigmoid, Dropout, BCE Loss"
        },
        {
            "type": "Poisson Distribution",
            "definition": "Discrete Counts {0, 1, 2, ..., ∞}. Mean = λ, Variance = λ (Identical!).",
            "looks_like": "Count Regression, API Rate-Limits, GPU Queueing"
        },
        {
            "type": "Gaussian (Normal) Distribution",
            "definition": "Continuous (-∞, ∞). Symmetrical bell curve with Mean = μ, Variance = σ².",
            "looks_like": "Noise Modeling, MSE Loss, Weight Init, Diffusion Models"
        },
        {
            "type": "Central Limit Theorem (CLT)",
            "definition": "Summing random variables from ANY distribution naturally converges into a Gaussian bell curve.",
            "looks_like": "Real-world noise & signals naturally become Gaussian"
        },
        {
            "type": "Generative AI (Diffusion & VAEs)",
            "definition": "Diffusion models sample pure Gaussian noise N(0, I) and iteratively denoise it to create images.",
            "looks_like": "Stable Diffusion & Midjourney: X ~ N(0, I)"
        }
    ],
    "symbol_guide": [
        {
            "symbol": "p",
            "meaning": "Bernoulli success probability",
            "plain_english": "Probability of outcome 1 occurring (output of Sigmoid)"
        },
        {
            "symbol": "y ∈ {0, 1}",
            "meaning": "Binary target outcome",
            "plain_english": "The ground truth binary label (e.g. 1 = Spam, 0 = Clean)"
        },
        {
            "symbol": "λ (lambda)",
            "meaning": "Poisson rate parameter",
            "plain_english": "Average number of events expected per time interval"
        },
        {
            "symbol": "k",
            "meaning": "Event count",
            "plain_english": "Actual number of observed events in Poisson distribution"
        },
        {
            "symbol": "μ, σ²",
            "meaning": "Gaussian Mean and Variance",
            "plain_english": "Center location and width spread of the normal bell curve"
        },
        {
            "symbol": "e",
            "meaning": "Euler's constant",
            "plain_english": "Base of the natural logarithm (e ≈ 2.718)"
        }
    ],
    "numerical_example": "Calculating probabilities for all three distributions:\n\n1. Bernoulli (Spam Classifier with p = 0.8):\n   • P(Spam = 1) = 0.8\n   • P(Not Spam = 0) = 1 - 0.8 = 0.2\n   • Mean = 0.8, Variance = 0.8 × 0.2 = 0.16\n\n2. Poisson (API Server averaging λ = 3 calls/sec):\n   • Probability of receiving exactly k = 2 calls in a second:\n     P(2) = (3² × e⁻³) / 2! = (9 × 0.0498) / 2 = 0.224 (22.4% chance)\n   • Mean = 3 calls, Variance = 3 (Identical!)\n\n3. Gaussian (Feature with μ = 10, σ = 2):\n   • 68% of samples lie within 1σ: [8, 12]\n   • 95% of samples lie within 2σ: [6, 14]\n   • A sample of x = 16 is 3σ away (extremely rare, ~0.15% chance).",
    "pitfalls": "Common Trap: Applying Gaussian MSE loss to binary classification problems. Squaring errors on 0/1 targets creates non-convex surfaces with vanishing gradients; always use Bernoulli-derived Binary Cross-Entropy (BCE) for binary tasks.",
    "core_logic": "Selecting loss functions depends on the assumed output distribution: Gaussian assumption leads to Mean Squared Error; Bernoulli assumption leads to Binary Cross-Entropy; Poisson assumption leads to Poisson deviance loss.",
    "architectural_logic": "In Generative AI, Latent Diffusion and VAE architectures depend fundamentally on Gaussian distributions. By projecting high-dimensional images into standard normal latent spaces N(0, I), generative models can synthesize novel images by sampling random Gaussian vectors and predicting denoised outputs.",
    "connected_logic": [
        {
            "title": "Bernoulli & The Secret of Binary Cross-Entropy",
            "content": "• In binary classification, Sigmoid outputs probability p of a Bernoulli distribution.\n• Binary Cross-Entropy loss (-[y log p + (1 - y) log(1 - p)]) is mathematically the exact negative log-likelihood of that Bernoulli trial."
        },
        {
            "title": "Poisson: The Equal Mean & Variance Anomaly",
            "content": "• For Poisson distributions, the mean and variance are mathematically identical: E[X] = Var(X) = λ.\n• When modeling event counts (like website hits or purchases), if variance far exceeds the mean, models switch to Negative Binomial to handle overdispersion."
        },
        {
            "title": "Gaussian & The Justification for MSE Loss",
            "content": "• In linear regression, assuming prediction noise is Gaussian makes minimizing Mean Squared Error (MSE) identical to Maximum Likelihood Estimation (MLE).\n• The Central Limit Theorem explains why noise is Gaussian: summing countless microscopic random factors naturally forms a bell curve."
        },
        {
            "title": "Generative AI: Diffusion Models & VAEs",
            "content": "• VAEs regularize latent codes into a standard Gaussian N(0, I) so models can synthesize new samples from random numbers.\n• Diffusion models (Stable Diffusion, Midjourney) initialize from pure Gaussian noise, iteratively removing predicted noise to produce photorealistic images."
        }
    ],
    "key_takeaways": [
        "Bernoulli models single binary outcomes (0 or 1); its log-likelihood forms Binary Cross-Entropy loss.",
        "Poisson models independent event counts over intervals; its Mean and Variance are uniquely identical (λ).",
        "Gaussian (Normal) models continuous data; the Central Limit Theorem explains why real-world noise is Gaussian.",
        "Minimizing Mean Squared Error (MSE) is mathematically optimal when noise follows a Gaussian distribution.",
        "Modern Generative AI (Diffusion models and VAEs) samples Gaussian noise to synthesize brand-new images."
    ],
    "definition_bullets": [
        "Bernoulli: Discrete binary distribution ({0, 1}) powering classifiers and BCE loss.",
        "Poisson: Discrete count distribution ({0, 1, 2, ...}) with equal mean and variance (λ).",
        "Gaussian (Normal): Symmetrical continuous bell curve underlying MSE loss and generative diffusion."
    ]
}

# 1. Update src/data/concepts.json
with open(CONCEPTS_PATH, 'r', encoding='utf-8') as f:
    concepts = json.load(f)

for idx, c in enumerate(concepts):
    if c['id'] == 'concept_prob_distributions':
        concepts[idx] = dist_concept
        break

with open(CONCEPTS_PATH, 'w', encoding='utf-8') as f:
    json.dump(concepts, f, indent=2, ensure_ascii=False)
print("Updated src/data/concepts.json for concept_prob_distributions successfully!")

# 2. Update scripts/data_sources/all_concepts.json
if os.path.exists(ALL_CONCEPTS_PATH):
    with open(ALL_CONCEPTS_PATH, 'r', encoding='utf-8') as f:
        all_concepts = json.load(f)
    for idx, c in enumerate(all_concepts):
        if c['id'] == 'concept_prob_distributions':
            all_concepts[idx] = dist_concept
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
        if c['id'] == 'concept_prob_distributions':
            math_concepts[idx] = dist_concept
            break
    with open(MATH_PY, "w", encoding="utf-8") as f:
        f.write('"""\nConcepts Database: Mathematical Foundations (19 Concepts)\n"""\n\nMATH_CONCEPTS = ' + json.dumps(math_concepts, indent=4, ensure_ascii=False) + '\n')
    print("Updated concepts_math.py successfully!")
