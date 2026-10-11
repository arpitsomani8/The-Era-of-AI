import json

SHANNON_ENTROPY_UPDATE = {
    "def": "Shannon Entropy is a concept from Information Theory that measures how uncertain or unpredictable an outcome is. The amount of information in a message is directly proportional to how much it surprises you.",
    "definition": "Shannon Entropy is a concept from Information Theory that measures how uncertain or unpredictable an outcome is. The amount of information in a message is directly proportional to how much it surprises you.",
    "formula": "$$H(X) = -\\sum_{i=1}^n P(x_i) \\log_2 P(x_i), \\quad I(x_i) = -\\log_2 P(x_i)$$",
    "formula_explanation": "",
    "logic": "A deterministic event with probability 1.0 contains 0 bits of information (0 entropy, no surprises). Maximum entropy occurs when all outcomes are equally likely (maximum unpredictability).",
    "example": "A fair coin has H = -(0.5 log₂ 0.5 + 0.5 log₂ 0.5) = 1.0 bit of entropy. A rigged coin that lands on heads 99% of the time has H = 0.08 bits (almost no surprise).",
    "simple_summary": "Shannon Entropy measures average uncertainty or surprise in a system. Guaranteed events carry zero bits (no surprise), while rare events carry high surprise. It sets the absolute limit on data compression and powers Decision Trees and Cross-Entropy loss in AI.",
    "core_terms": [
        {
            "term": "Shannon Entropy H(X)",
            "what_is_it": "• A measure of the average uncertainty or unpredictability across all possible outcomes in a probability distribution.\n• Quantifies the expected amount of 'surprise' you receive when observing the system: H(X) = -∑ P(xᵢ) log₂ P(xᵢ).",
            "analogy": "A completely biased coin landing Heads 100% of the time has 0 entropy (zero surprise, zero new info). A fair 50/50 coin has maximum entropy (1 full bit of surprise every flip).",
            "why_it_matters": "The foundation of Cross-Entropy loss in neural networks, split criteria in Decision Trees, and exploration in Reinforcement Learning."
        },
        {
            "term": "Surprisal (Self-Information I(x))",
            "what_is_it": "• The amount of information contained in a single specific event: I(x) = -log₂ P(x).\n• Information is directly proportional to surprise: guaranteed events carry 0 bits, while rare events carry massive information.",
            "analogy": "Hearing 'The sun rose today' (P = 1.0) gives 0 bits of information. Hearing 'A massive blizzard just hit the Sahara Desert' (P ≈ 0.00001) gives immense surprise and high information.",
            "why_it_matters": "Explains why rare events (like edge cases, anomalies, or fraud) carry far higher diagnostic value in machine learning than routine data."
        },
        {
            "term": "Information Gain (Entropy Reduction)",
            "what_is_it": "• The reduction in entropy achieved by partitioning data according to a specific feature: IG = H(Parent) - H(Children).\n• Measures how much cleaner, purer, and more predictable a dataset becomes after asking a question.",
            "analogy": "In 20 Questions: Asking 'Is it living?' cuts uncertainty in half (high Information Gain), whereas asking 'Is its name Bob?' gives near-zero Information Gain.",
            "why_it_matters": "The core splitting criterion used by Decision Trees, Random Forests, and XGBoost to build optimal decision paths."
        }
    ],
    "types_header": "Entropy Properties & Information Bounds",
    "types_badge": "Information Limits",
    "quick_types": [
        {
            "type": "Maximum Entropy (Uniform)",
            "definition": "Occurs when all outcomes are equally likely (e.g. fair 6-sided die, H = log₂(6) ≈ 2.58 bits). Maximum unpredictability.",
            "looks_like": "P(x₁) = P(x₂) = ... = 1/n → H(X) = log₂(n)"
        },
        {
            "type": "Minimum Entropy (Deterministic)",
            "definition": "Occurs when one outcome has probability 1.0 and all others 0. Pure certainty yields zero surprise and zero information.",
            "looks_like": "P(x₁) = 1.0, Others = 0 → H(X) = 0 bits"
        },
        {
            "type": "Bits vs. Nats",
            "definition": "Base-2 log (log₂) measures information in bits (Information Theory); natural log (ln) measures information in nats (used in PyTorch/Deep Learning).",
            "looks_like": "1 nat = 1 / ln(2) ≈ 1.443 bits"
        },
        {
            "type": "Shannon Compression Limit",
            "definition": "Entropy is the absolute physical lower bound on lossless data compression (Huffman, GZIP cannot beat H bits/char on average).",
            "looks_like": "Average Code Length L ≥ H(X) bits/symbol"
        },
        {
            "type": "Why the Logarithm? (Additivity)",
            "definition": "Independent events multiply in probability P(A ∩ B) = P(A)P(B), but taking logs makes information additive: I(A ∩ B) = I(A) + I(B).",
            "looks_like": "-log₂(P₁ · P₂) = -log₂(P₁) - log₂(P₂)"
        }
    ],
    "symbol_guide": [
        {
            "symbol": "H(X)",
            "meaning": "Shannon Entropy",
            "plain_english": "Average uncertainty or expected surprise across the full distribution"
        },
        {
            "symbol": "I(xᵢ)",
            "meaning": "Surprisal (Self-Information)",
            "plain_english": "Information in bits yielded by observing single outcome xᵢ"
        },
        {
            "symbol": "P(xᵢ)",
            "meaning": "Outcome Probability",
            "plain_english": "Likelihood of outcome xᵢ occurring, bounded between 0 and 1"
        },
        {
            "symbol": "log₂",
            "meaning": "Base-2 Logarithm",
            "plain_english": "Logarithm measuring information in binary digits (bits)"
        },
        {
            "symbol": "∑ (Sigma)",
            "meaning": "Summation",
            "plain_english": "Adds up the probability-weighted surprise across all n outcomes"
        },
        {
            "symbol": "n",
            "meaning": "Number of Outcomes",
            "plain_english": "Total distinct possible classes or states in the probability distribution"
        }
    ],
    "numerical_example": "Fair Coin vs. Biased Coin Calculation:\n1. Fair Coin (P(H) = 0.5, P(T) = 0.5):\n   • Surprisal per flip: I(H) = -log₂(0.5) = 1 bit\n   • Entropy: H(X) = -[0.5 log₂(0.5) + 0.5 log₂(0.5)] = -[0.5(-1) + 0.5(-1)] = 1.0 bit (Maximum uncertainty).\n\n2. Biased Coin (P(H) = 0.9, P(T) = 0.1):\n   • Surprisal: I(H) = -log₂(0.9) ≈ 0.152 bits (common, low surprise); I(T) = -log₂(0.1) ≈ 3.322 bits (rare, high surprise)\n   • Entropy: H(X) = -[0.9(-0.152) + 0.1(-3.322)] = 0.137 + 0.332 = 0.469 bits.\n\n3. Guaranteed Event (P(H) = 1.0, P(T) = 0):\n   • Entropy: H(X) = -[1.0 log₂(1.0) + 0] = 0 bits (Complete certainty, zero information gained).",
    "pitfalls": "Common Pitfall: Confusing high entropy with high information quality. High entropy means high disorder, chaos, or uncertainty—not 'useful' data. In classification, our goal is to drive entropy toward 0 (pure, confident predictions).",
    "core_logic": "Why this matters: Information is the resolution of uncertainty. A guaranteed message gives zero bits, while rare events carry maximum signal. Shannon Entropy defines the mathematical floor for data compression and the exact objective for training classifiers.",
    "architectural_logic": "In deep learning architectures, Shannon Entropy grounds Cross-Entropy loss by measuring target uncertainty H(P). In Reinforcement Learning, adding a policy entropy bonus β · H(π) prevents policy collapse, ensuring agents continuously explore diverse, creative actions.",
    "connected_logic": [
        {
            "title": "Decision Trees & Random Forests: Information Gain",
            "content": "• Decision trees evaluate splits by computing label entropy in candidate subsets, choosing the split that maximizes Information Gain = H(Parent) - H(Children).\n• High entropy indicates a chaotic mix of classes; maximizing Information Gain purifies nodes into crisp, homogeneous classification buckets."
        },
        {
            "title": "The Bridge to Deep Learning: Cross-Entropy Loss",
            "content": "• Cross-entropy between true labels P and network predictions Q decomposes as H(P, Q) = H(P) + D_KL(P || Q), where H(P) is the irreducible ground-truth entropy.\n• Minimizing Cross-Entropy loss directly minimizes the KL divergence, driving the model's predicted probability distribution Q to match reality P."
        },
        {
            "title": "Reinforcement Learning: The Policy Entropy Bonus",
            "content": "• RL agents often fall into local optima by repeatedly choosing the first rewarding action they discover (premature policy collapse).\n• Modern algorithms (PPO, Soft Actor-Critic) add an Entropy Bonus β · H(π) to the reward, penalizing overconfidence and forcing agents to actively explore diverse policies."
        },
        {
            "title": "Shannon's Source Coding Theorem: The Physical Limit of Compression",
            "content": "• Shannon proved that entropy is the fundamental limit of lossless data compression: no algorithm (ZIP, GZIP, Huffman) can compress a file below its entropy rate.\n• Formats like MP3 and JPEG assign short bit sequences to frequent symbols (low surprisal) and longer sequences to rare symbols (high surprisal), operating directly on Shannon's limit."
        }
    ],
    "key_takeaways": [
        "Core Principle: Shannon Entropy H(X) measures the expected surprise or uncertainty in a probability distribution.",
        "Surprisal & Additivity: Single event surprise I(x) = -log₂ P(x); taking logarithms makes information additive across independent events.",
        "Boundaries: Maximum entropy occurs when outcomes are uniformly flat; minimum entropy (0 bits) occurs with complete certainty.",
        "AI Pillars: Governs Information Gain in Decision Trees, Cross-Entropy loss in Deep Learning, and policy exploration in Reinforcement Learning."
    ],
    "definition_bullets": [
        "Shannon Entropy: The mathematical measure of average uncertainty or surprise across all outcomes of a random variable, maximized when outcomes are uniformly unpredictable.",
        "Surprisal (Self-Information): The amount of information yielded by observing a single event, inversely proportional to its probability."
    ]
}

def update_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    found = False
    for item in data:
        if item.get('id') == 'concept_shannon_entropy':
            item.update(SHANNON_ENTROPY_UPDATE)
            found = True
            break
            
    if not found:
        print(f"Warning: concept_shannon_entropy not found in {filepath}")
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
        if item.get('id') == 'concept_shannon_entropy':
            item.update(SHANNON_ENTROPY_UPDATE)
            break
            
    new_content = '"""\nConcepts Database: Mathematical Foundations (19 Concepts)\n"""\n\nMATH_CONCEPTS = ' + json.dumps(mod.MATH_CONCEPTS, indent=4, ensure_ascii=False) + '\n'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Successfully updated {filepath}")

update_concepts_math()
