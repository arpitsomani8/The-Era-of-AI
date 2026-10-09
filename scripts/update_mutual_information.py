import json

MUTUAL_INFO_UPDATE = {
    "def": "Mutual Information measures the shared information between two random variables. It quantifies how much uncertainty about one variable is wiped away when you observe the other.",
    "definition": "Mutual Information measures the shared information between two random variables. It quantifies how much uncertainty about one variable is wiped away when you observe the other.",
    "formula": "$$I(X; Y) = \\sum_{x, y} P(x, y) \\log\\left( \\frac{P(x, y)}{P(x)P(y)} \\right) = H(X) - H(X \\mid Y) = H(X) + H(Y) - H(X, Y)$$",
    "formula_explanation": "",
    "logic": "Unlike linear correlation (Pearson r) which only captures straight-line associations, Mutual Information captures arbitrary non-linear and non-monotonic relationships between features and labels.",
    "example": "Customer churn dataset: A feature like 'Age' may have Pearson r ≈ 0 due to a U-shaped risk curve (very young and very old churn more). Mutual Information readily captures this strong non-linear predictive value.",
    "simple_summary": "Mutual Information measures how much knowing X tells you about Y. Unlike correlation which only catches straight lines, Mutual Information detects ANY relationship (curves, chaos). It is symmetric, equals 0 for independent variables, and powers feature selection and contrastive learning (CLIP).",
    "core_terms": [
        {
            "term": "Mutual Information I(X; Y)",
            "what_is_it": "• A measure of the shared information between two random variables, answering: 'How much does knowing X tell me about Y?'\n• Quantifies the reduction in uncertainty: I(X; Y) = H(X) - H(X | Y), equaling 0 if and only if X and Y are completely independent.",
            "analogy": "Looking at wet asphalt on the street: observing wet pavement (X) wipes away your uncertainty about whether it rained recently (Y).",
            "why_it_matters": "Universal dependence measure that detects arbitrary non-linear patterns, driving feature selection and representation learning."
        },
        {
            "term": "Mutual Information vs. Correlation",
            "what_is_it": "• Pearson correlation (r) only detects straight-line relationships (y = mx + b) and yields r ≈ 0 on parabolic curves (y = x²).\n• Mutual Information detects ANY relationship—linear, quadratic, cyclic, or chaotic—and handles both discrete classes and continuous values.",
            "analogy": "A metal detector that only beeps on straight copper pipes (Pearson) versus an X-ray scanner that reveals objects of any shape or material (Mutual Information).",
            "why_it_matters": "Prevents machine learning engineers from discarding powerful non-linear predictive features during data preprocessing."
        },
        {
            "term": "The Information Bottleneck Principle",
            "what_is_it": "• A foundational theory explaining how deep neural networks learn: min [I(X; T) - β · I(T; Y)].\n• Hidden layers T act as a bottleneck that compresses away irrelevant input noise I(X; T) while maximizing predictive mutual information I(T; Y).",
            "analogy": "An executive summary: a great assistant discards 90% of raw email clutter (compression) while retaining the 10% essential facts needed to make decisions (prediction).",
            "why_it_matters": "Provides the theoretical framework for why deep networks generalize rather than simply memorizing training data."
        }
    ],
    "types_header": "Mutual Information Properties & Contrast",
    "types_badge": "Information Dynamics",
    "quick_types": [
        {
            "type": "High Mutual Information",
            "definition": "Knowing X dramatically reduces uncertainty about Y (e.g. transaction velocity predicting credit card fraud).",
            "looks_like": "Strong predictive power: I(X; Y) >> 0"
        },
        {
            "type": "Zero Mutual Information (Independence)",
            "definition": "X and Y are statistically independent (P(X, Y) = P(X)P(Y)). Knowing X provides zero insight into Y.",
            "looks_like": "I(X; Y) = 0 ⟺ P(X, Y) = P(X)P(Y)"
        },
        {
            "type": "Low Mutual Information",
            "definition": "Knowing X gives trivial or negligible insight into Y (e.g. customer shoe size predicting cloud software purchase).",
            "looks_like": "Uninformative feature: I(X; Y) ≈ 0"
        },
        {
            "type": "Symmetry Guarantee",
            "definition": "Mutual Information is strictly symmetric: I(X; Y) = I(Y; X). Variable X reveals as much about Y as Y reveals about X.",
            "looks_like": "I(X; Y) = I(Y; X) always"
        },
        {
            "type": "Non-Linear Detection",
            "definition": "Unlike Pearson correlation which scores 0 on U-shaped curves (y = x²), Mutual Information readily detects any functional dependence.",
            "looks_like": "Detects curves, circles, & complex manifolds"
        }
    ],
    "symbol_guide": [
        {
            "symbol": "I(X; Y)",
            "meaning": "Mutual Information",
            "plain_english": "Shared information between random variables X and Y (in bits or nats)"
        },
        {
            "symbol": "P(x, y)",
            "meaning": "Joint Probability",
            "plain_english": "Probability that variable X takes value x AND variable Y takes value y"
        },
        {
            "symbol": "P(x), P(y)",
            "meaning": "Marginal Probabilities",
            "plain_english": "Individual probabilities of observing outcome x and outcome y independently"
        },
        {
            "symbol": "H(X)",
            "meaning": "Marginal Entropy",
            "plain_english": "Baseline uncertainty in variable X before observing variable Y"
        },
        {
            "symbol": "H(X | Y)",
            "meaning": "Conditional Entropy",
            "plain_english": "Remaining uncertainty in variable X after variable Y is revealed"
        },
        {
            "symbol": "H(X, Y)",
            "meaning": "Joint Entropy",
            "plain_english": "Total uncertainty across both variables X and Y combined"
        }
    ],
    "numerical_example": "Weather vs. Umbrella Usage (Discrete Binary Variables):\n• States: Rain (R ∈ {0, 1}), Umbrella (U ∈ {0, 1})\n• Probabilities: P(No Rain, No Umbrella) = 0.70, P(Rain, Umbrella) = 0.20, P(Rain, No Umbrella) = 0.05, P(No Rain, Umbrella) = 0.05.\n\n1. Marginals: P(Rain=1) = 0.25, P(Umbrella=1) = 0.25.\n2. Entropy of Rain: H(R) = -[0.25 log₂(0.25) + 0.75 log₂(0.75)] ≈ 0.811 bits.\n3. Conditional Entropy H(R | U):\n   • If Umbrella=1: P(Rain=1 | U=1) = 0.20 / 0.25 = 0.80 --> H(R | U=1) ≈ 0.722 bits.\n   • If Umbrella=0: P(Rain=1 | U=0) = 0.05 / 0.75 = 0.067 --> H(R | U=0) ≈ 0.354 bits.\n   • H(R | U) = 0.25(0.722) + 0.75(0.354) ≈ 0.446 bits.\n4. Mutual Information: I(R; U) = H(R) - H(R | U) = 0.811 - 0.446 = 0.365 bits.\nObserving whether someone carries an umbrella wipes away ~45% of our uncertainty about rain!",
    "pitfalls": "Common Pitfall: Using Pearson correlation to eliminate 'useless' features during preprocessing. Features with zero linear correlation can possess near-perfect mutual information with the target label (e.g. concentric circles or quadratic patterns). Always verify with mutual_info_classif before dropping non-linear signals.",
    "core_logic": "Why this matters: Mutual Information measures the statistical dependence between variables without assuming linearity or monotonicity. It equals the KL divergence between the joint distribution and product of marginals: I(X; Y) = D_KL(P(X, Y) || P(X)P(Y)).",
    "architectural_logic": "In modern multi-modal AI (CLIP) and contrastive learning (SimCLR), models maximize a variational lower bound on Mutual Information via the InfoNCE objective: max I(Image; Text). In deep learning theory, the Information Bottleneck principle balances compression against target mutual information.",
    "connected_logic": [
        {
            "title": "Feature Selection in Machine Learning: Beyond Linear Correlation",
            "content": "• Tabular models often discard high-value features because Pearson correlation fails on non-monotonic or U-shaped curves (e.g. credit default risk vs. age).\n• Using mutual_info_classif ranks features by pure shared entropy I(X; Y), preserving complex non-linear predictors and eliminating pure noise columns."
        },
        {
            "title": "Contrastive Learning & CLIP: Maximizing Cross-Modal Mutual Information",
            "content": "• Vision-language models like OpenAI's CLIP align images and text without labels by optimizing InfoNCE (Noise-Contrastive Estimation) loss.\n• Mathematically, minimizing InfoNCE maximizes a variational lower bound on I(Image; Text), forcing encoders to capture the shared semantic concepts between modalities."
        },
        {
            "title": "The Information Bottleneck: Why Deep Networks Generalize",
            "content": "• Tishby's Information Bottleneck principle models training as min [I(X; T) - β · I(T; Y)], balancing compression against target preservation.\n• During gradient descent, representations T compress away nuisance pixel variations (low I(X; T)) while keeping high predictive mutual information with the label (high I(T; Y))."
        },
        {
            "title": "Pointwise Mutual Information (PMI) in NLP & Word Embeddings",
            "content": "• In NLP, Pointwise Mutual Information measures whether words appear together more often than expected by chance: PMI(w₁, w₂) = log [P(w₁, w₂) / (P(w₁)P(w₂))].\n• Factorizing the PMI co-occurrence matrix is mathematically equivalent to training skip-gram word embeddings (Word2Vec), grounding lexical semantics in shared information."
        }
    ],
    "key_takeaways": [
        "Core Principle: Mutual Information I(X; Y) measures uncertainty reduction: I(X; Y) = H(X) - H(X | Y).",
        "Non-Linear Superiority: Captures ANY functional relationship (curves, U-shapes), whereas Pearson correlation only detects straight lines.",
        "Symmetry & Independence: I(X; Y) = I(Y; X), and equals 0 if and only if X and Y are statistically independent.",
        "Modern AI Role: Drives feature selection in tabular ML, InfoNCE contrastive learning in CLIP, and the Information Bottleneck theory of deep learning."
    ],
    "definition_bullets": [
        "Mutual Information: The amount of information shared between two random variables, measuring how much uncertainty in one is eliminated by observing the other.",
        "Information Bottleneck: The deep learning principle where internal network layers compress input noise while preserving target mutual information."
    ]
}

def update_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    found = False
    for item in data:
        if item.get('id') == 'concept_mutual_information':
            item.update(MUTUAL_INFO_UPDATE)
            found = True
            break
            
    if not found:
        print(f"Warning: concept_mutual_information not found in {filepath}")
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
        if item.get('id') == 'concept_mutual_information':
            item.update(MUTUAL_INFO_UPDATE)
            break
            
    new_content = '"""\nConcepts Database: Mathematical Foundations (19 Concepts)\n"""\n\nMATH_CONCEPTS = ' + json.dumps(mod.MATH_CONCEPTS, indent=4, ensure_ascii=False) + '\n'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Successfully updated {filepath}")

update_concepts_math()
