import json
import re

CLT_CONCEPT_UPDATE = {
    "def": "The Law of Large Numbers (LLN) states that the average of results obtained from a large number of trials tends to approach the expected value. The Central Limit Theorem (CLT) states that, given a sufficiently large sample size, the distribution of sample averages approaches a normal distribution, regardless of the underlying distribution of the individual variables.",
    "definition": "The Law of Large Numbers (LLN) states that the average of results obtained from a large number of trials tends to approach the expected value. The Central Limit Theorem (CLT) states that, given a sufficiently large sample size, the distribution of sample averages approaches a normal distribution, regardless of the underlying distribution of the individual variables.",
    "formula": "$$\\lim_{N \\to \\infty} \\bar{X}_N = \\mu, \\quad \\bar{X}_N \\sim \\mathcal{N}\\left(\\mu, \\frac{\\sigma^2}{N}\\right), \\quad \\text{SE} = \\frac{\\sigma}{\\sqrt{N}}$$",
    "formula_explanation": "",
    "logic": "Allows data scientists to compute confidence intervals and conduct valid hypothesis tests (e.g. A/B testing z-tests) on arbitrary metrics because sample means are guaranteed to be normally distributed.",
    "example": "Rolling 100 dice: Individual dice outcomes are uniform flat [1, 2, 3, 4, 5, 6]. But if you roll 100 dice and sum them, the resulting sum across thousands of trials forms an exquisite bell curve centered at 350.",
    "simple_summary": "LLN guarantees that if you collect enough data, your sample average will reach the true reality (randomness cancels out). CLT proves that along the way, the shape of your uncertainty forms a perfect Gaussian bell curve, regardless of what the original data looked like.",
    "core_terms": [
        {
            "term": "Law of Large Numbers (LLN)",
            "what_is_it": "• As sample size N increases, the sample average inexorably converges to the true expected value: lim (N→∞) X̄_N = μ.\n• Answers the core question: 'If I collect enough data, will my sample average eventually reach true underlying reality? Yes!' Over large samples, random fluctuations cancel each other out.",
            "analogy": "The Casino's Superpower: A gambler might win on spin 1, but over 10,000,000 roulette spins, the casino's average profit inexorably locks into the mathematical expected value (+2.7% house edge). Randomness cancels out.",
            "why_it_matters": "Guarantees that training error converges to true real-world error (Empirical Risk Minimization) as we collect more training data."
        },
        {
            "term": "Central Limit Theorem (CLT)",
            "what_is_it": "• Regardless of the original data's shape (flat uniform, skewed exponential, or two-hump camel curve), the distribution of sample averages always approaches a Gaussian bell curve as sample size N grows.\n• Answers the core question: 'Along the way, what does the shape of my uncertainty look like? A perfect Gaussian normal distribution N(μ, σ²/N).'",
            "analogy": "Rolling a single 6-sided die is completely flat (1 to 6 are equally likely). But roll 100 dice and average their sum across thousands of players: the resulting averages form an exquisite bell curve centered at 3.5.",
            "why_it_matters": "CLT guarantees that mini-batch gradients in Deep Learning are well-behaved Gaussian approximations of the full dataset gradient."
        },
        {
            "term": "Standard Error (SE = σ / √N)",
            "what_is_it": "• The standard deviation of the sample average, measuring how much sample means fluctuate around the true mean μ.\n• The precision of your estimate increases with √N, which is why collecting 4× more data only cuts uncertainty by 2×.",
            "analogy": "If you survey 10 people about an AI feature, your margin of error is wide. Survey 1,000 people, and your estimate tightens drastically because the spread of averages shrinks by √100 ≈ 10×.",
            "why_it_matters": "Tells deep learning engineers exactly how noisy mini-batch gradients will be and governs the sample size needed for reliable AI benchmark evaluations."
        }
    ],
    "types_header": "LLN vs. CLT: Convergence vs. Shape",
    "types_badge": "Theorem Comparison",
    "quick_types": [
        {
            "type": "Core Question",
            "definition": "LLN asks: 'Does the sample mean converge to the true expected value?' CLT asks: 'What is the shape of the uncertainty around that mean?'",
            "looks_like": "Destination (Convergence) vs. Journey (Bell Shape)"
        },
        {
            "type": "Mathematical Output",
            "definition": "LLN produces a single deterministic point: X̄_N → μ. CLT produces a full probability distribution: N(μ, σ²/N).",
            "looks_like": "Point Convergence vs. Gaussian Bell Curve"
        },
        {
            "type": "Mathematical Requirements",
            "definition": "LLN requires i.i.d. samples with finite mean. CLT requires finite mean μ and finite variance σ² (typically N ≥ 30).",
            "looks_like": "Finite Mean vs. Finite Variance (N ≥ 30)"
        },
        {
            "type": "AI Role: Training (ERM)",
            "definition": "LLN guarantees Empirical Risk (training loss) converges to True Risk (unseen data loss) as training sample size grows toward infinity.",
            "looks_like": "Empirical Risk Minimization (ERM): Train Loss → Real Loss"
        },
        {
            "type": "AI Role: Optimization & Evals",
            "definition": "CLT proves mini-batch gradients act as Gaussian noise around the true gradient, and enables confidence intervals in AI benchmark evals.",
            "looks_like": "Gaussian Mini-Batch SGD & A/B Test Confidence Intervals"
        }
    ],
    "symbol_guide": [
        {
            "symbol": "X̄_N",
            "meaning": "Sample Mean",
            "plain_english": "The arithmetic average of N collected observations"
        },
        {
            "symbol": "μ (mu)",
            "meaning": "Population Mean",
            "plain_english": "The true underlying expected value across the entire universe of data"
        },
        {
            "symbol": "N",
            "meaning": "Sample Size",
            "plain_english": "The total number of independent data points collected in the sample or batch"
        },
        {
            "symbol": "N (Normal)",
            "meaning": "Gaussian (Normal) Distribution",
            "plain_english": "The universal bell curve distribution centered at mean μ with variance σ²/N"
        },
        {
            "symbol": "σ (sigma)",
            "meaning": "Population Standard Deviation",
            "plain_english": "The inherent spread or standard deviation of the individual data points"
        },
        {
            "symbol": "SE",
            "meaning": "Standard Error",
            "plain_english": "The spread of the sample average, equal to σ divided by the square root of N"
        }
    ],
    "numerical_example": "Rolling 100 Dice & Roulette Spins:\nSuppose you roll a fair 6-sided die. Single roll outcomes are uniformly flat {1, 2, 3, 4, 5, 6} with true mean μ = 3.5 and standard deviation σ ≈ 1.71.\n1. Law of Large Numbers (LLN): Roll 1 die 5 times → average might be 4.2. Roll 10,000 times → sample average X̄_N locks tightly onto 3.5002 (randomness cancels out).\n2. Central Limit Theorem (CLT): Now roll a batch of N = 100 dice and record their average. Repeat this experiment 1,000 times across 1,000 players.\n3. The Bell Curve & Standard Error: Although individual dice are completely flat (uniform), the 1,000 sample averages form a sharp Gaussian bell curve centered at μ = 3.5 with Standard Error SE = σ / √N = 1.71 / √100 = 0.171.\n4. Nearly 95% of all 100-dice batch averages fall within [3.5 - 2(0.171), 3.5 + 2(0.171)] = [3.16, 3.84], perfectly matching Gaussian prediction intervals.",
    "pitfalls": "Common Pitfall: Confusing the distribution of the raw data with the distribution of sample means. CLT does NOT make your raw dataset normal—it only ensures that the *average* of random samples becomes normally distributed (typically requiring N ≥ 30 with finite variance).",
    "core_logic": "Why this matters: LLN guarantees that training error on finite data converges to real-world generalization error (ERM). CLT guarantees that noisy mini-batch gradients are normally distributed around the true gradient and enables rigorous confidence intervals in AI evaluation.",
    "architectural_logic": "In modern deep learning architectures, CLT provides theoretical backing for stochastic gradient descent (SGD) and diffusion noise schedules, while LLN validates scaling laws—confirming that scaling training tokens systematically drives empirical test loss toward optimal Bayes risk.",
    "connected_logic": [
        {
            "title": "The Casino Superpower: Randomness Cancellation",
            "content": "• A casino never panics when a patron hits a lucky jackpot, because over 10,000,000 spins, the law of large numbers guarantees net profit converges to the +2.7% expected edge.\n• Over large sample counts, positive and negative random deviations inevitably cancel out, turning individual randomness into absolute macro certainty."
        },
        {
            "title": "Why LLN Powers AI: Empirical Risk Minimization (ERM)",
            "content": "• Machine learning seeks to minimize True Risk (expected loss over every possible real-world scenario), but we only possess a training set of size N (Empirical Risk).\n• LLN mathematically guarantees that as training data grows (N → ∞), Empirical Risk converges to True Risk—which is why 'more high-quality data' almost always beats a cleverer algorithm."
        },
        {
            "title": "CLT in Deep Learning: Mini-Batch Stochastic Gradient Descent (SGD)",
            "content": "• Computing true gradients over trillions of tokens for 70B parameter LLMs is physically impossible, so models compute gradients over mini-batches of 128 or 256 samples.\n• Thanks to CLT, even though individual sample gradients are wildly erratic, the batch average gradient behaves as a clean Gaussian variable centered directly at the true gradient: g_batch ~ N(∇L_true, σ² / Batch Size)."
        },
        {
            "title": "CLT in AI Evaluation: A/B Testing & Benchmark Confidence Intervals",
            "content": "• When evaluating if a new model (e.g., GPT-4.5 vs. GPT-4) is superior across 1,000 benchmark prompts, researchers cannot test all infinite prompts in existence.\n• By CLT, the sample win rate follows a normal distribution, allowing researchers to calculate standard error, confidence intervals, and p-values to scientifically prove model improvements aren't just dumb luck."
        }
    ],
    "key_takeaways": [
        "Law of Large Numbers (LLN): Guarantees sample mean converges to true expected value (X̄_N → μ) as N → ∞.",
        "Central Limit Theorem (CLT): Guarantees the distribution of sample averages forms a Gaussian bell curve N(μ, σ²/N) regardless of source distribution.",
        "Precision & Sample Size: The precision of your estimate increases with √N, which is why collecting 4× more data only cuts uncertainty by 2×.",
        "Deep Learning Gradients: CLT guarantees that mini-batch gradients in Deep Learning are well-behaved Gaussian approximations of the full dataset gradient."
    ],
    "definition_bullets": [
        "Law of Large Numbers: Guarantees that as sample size increases, the sample average inexorably converges to the true expected value, canceling out random fluctuations.",
        "Central Limit Theorem: Proves that the distribution of sample averages approaches a normal distribution as sample size grows, regardless of the source distribution's shape."
    ]
}

def update_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    found = False
    for item in data:
        if item.get('id') == 'concept_clt_lln':
            item.update(CLT_CONCEPT_UPDATE)
            found = True
            break
            
    if not found:
        print(f"Warning: concept_clt_lln not found in {filepath}")
        return False
        
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Successfully updated {filepath}")
    return True

# Update concepts.json and all_concepts.json
update_json_file('src/data/concepts.json')
update_json_file('scripts/data_sources/all_concepts.json')

# Now update concepts_math.py
def update_concepts_math():
    filepath = 'scripts/data_sources/concepts_math.py'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We can parse out MATH_CONCEPTS, find concept_clt_lln, update it, and write it back formatted.
    # Or load concepts_math module dynamically and dump it.
    import importlib.util
    spec = importlib.util.spec_from_file_location("concepts_math", filepath)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    
    for item in mod.MATH_CONCEPTS:
        if item.get('id') == 'concept_clt_lln':
            item.update(CLT_CONCEPT_UPDATE)
            break
            
    new_content = '"""\nConcepts Database: Mathematical Foundations (19 Concepts)\n"""\n\nMATH_CONCEPTS = ' + json.dumps(mod.MATH_CONCEPTS, indent=4, ensure_ascii=False) + '\n'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Successfully updated {filepath}")

update_concepts_math()
