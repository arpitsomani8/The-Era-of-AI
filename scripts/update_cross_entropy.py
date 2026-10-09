import json

CROSS_ENTROPY_UPDATE = {
    "def": "Cross-Entropy Loss measures how well a model's predicted probabilities match actual outcomes. It is the fundamental loss function for training classification models, neural networks, and Large Language Models.",
    "definition": "Cross-Entropy Loss measures how well a model's predicted probabilities match actual outcomes. It is the fundamental loss function for training classification models, neural networks, and Large Language Models.",
    "formula": "$$\\mathcal{L}_{\\text{BCE}} = -[y \\log(\\hat{y}) + (1 - y) \\log(1 - \\hat{y})], \\quad \\mathcal{L}_{\\text{CCE}} = -\\sum_{i=1}^C y_i \\log(\\hat{y}_i) = -\\log(\\hat{y}_{\\text{correct}})$$",
    "formula_explanation": "",
    "logic": "The loss approaches infinity as the model predicts zero probability for the correct true class. This creates steep, aggressive corrective gradients (ŷ - y) when a model makes confident errors.",
    "example": "3-class classifier (True label: Cat [1, 0, 0]): If the model predicts Cat with probability 0.90, loss is -log(0.90) = 0.105. If it predicts Cat with probability 0.001, loss explodes to -log(0.001) = 6.908.",
    "simple_summary": "Cross-Entropy Loss measures how well predicted probabilities match reality. If the model is confident and correct, loss is near zero; if it is confident and wrong, loss explodes toward infinity. It avoids vanishing gradients and trains all modern LLMs.",
    "core_terms": [
        {
            "term": "Cross-Entropy Loss (Log Loss)",
            "what_is_it": "• A loss function that measures how closely a model's predicted probability distribution Q matches the true distribution P.\n• Quantifies the penalty for wrong predictions: loss is near zero when confident and correct, but explodes toward infinity if confident and wrong.",
            "analogy": "A lie detector test: if you speak the truth confidently, there is zero penalty; if you assert a falsehood with complete certainty, the alarm rings at deafening volume.",
            "why_it_matters": "The universal loss function powering image classification, speech recognition, and next-token prediction in Large Language Models (LLMs)."
        },
        {
            "term": "Binary Cross-Entropy (BCE)",
            "what_is_it": "• The 2-class specialization of cross-entropy for Yes/No decisions: L_BCE = -[y log(ŷ) + (1 - y) log(1 - ŷ)].\n• Paired with a Sigmoid activation function to output a single probability ŷ ∈ [0, 1].",
            "analogy": "A medical diagnostic test (Disease vs. Healthy) or an email filter (Spam vs. Inbox)—only two mutually exclusive possibilities exist.",
            "why_it_matters": "Standard objective for binary classification, multi-label tagging, and discriminator training in Generative Adversarial Networks (GANs)."
        },
        {
            "term": "Categorical Cross-Entropy (CCE)",
            "what_is_it": "• The multi-class specialization for picking one class out of C choices: L_CCE = -∑ yᵢ log(ŷᵢ) = -log(ŷ_correct).\n• Paired with a Softmax activation function to convert raw unbounded logits into a normalized probability distribution.",
            "analogy": "A multiple-choice exam where exactly one option is right—you distribute your confidence percentages across all options, and get scored solely on -log(confidence) for the correct answer.",
            "why_it_matters": "Directly trains vision models on ImageNet (1,000 classes) and LLMs (predicting the next token out of 100,000 vocabulary words)."
        }
    ],
    "types_header": "Cross-Entropy Flavors & Gradient Mechanics",
    "types_badge": "Loss Comparison",
    "quick_types": [
        {
            "type": "Binary Cross-Entropy (BCE)",
            "definition": "Used for binary classification (2 classes). Paired with Sigmoid activation. L = -[y log ŷ + (1 - y) log(1 - ŷ)].",
            "looks_like": "Sigmoid + BCE: Spam Detection, Medical Diagnosis"
        },
        {
            "type": "Categorical Cross-Entropy (CCE)",
            "definition": "Used for multi-class classification (C > 2). Paired with Softmax activation. L = -log(ŷ_correct).",
            "looks_like": "Softmax + CCE: ImageNet, Next-Token Prediction in LLMs"
        },
        {
            "type": "Cross-Entropy vs. MSE",
            "definition": "MSE suffers from vanishing gradients when wrong predictions saturate Sigmoid; Cross-Entropy produces clean linear gradients (ŷ - y).",
            "looks_like": "MSE Gradient: (ŷ - y)σ'(z) ≈ 0 vs. CE Gradient: ŷ - y"
        },
        {
            "type": "Information Theory Duality",
            "definition": "Cross-Entropy equals True Entropy plus KL Divergence: H(P, Q) = H(P) + D_KL(P || Q). Minimizing loss minimizes divergence.",
            "looks_like": "Loss = Irreducible Truth Entropy + Model Divergence"
        },
        {
            "type": "Logits vs. Probabilities",
            "definition": "Raw model outputs z are unconstrained numbers (-∞ to +∞). Softmax normalizes them into probabilities summing to 1.0 before Cross-Entropy.",
            "looks_like": "z → Softmax(z) → ŷ → -log(ŷ_correct)"
        }
    ],
    "symbol_guide": [
        {
            "symbol": "L_BCE",
            "meaning": "Binary Cross-Entropy Loss",
            "plain_english": "Loss penalty computed for 2-class binary prediction tasks"
        },
        {
            "symbol": "L_CCE",
            "meaning": "Categorical Cross-Entropy Loss",
            "plain_english": "Loss penalty computed across C mutually exclusive classes"
        },
        {
            "symbol": "y",
            "meaning": "True Label (Ground Truth)",
            "plain_english": "Binary indicator (1 for positive class, 0 for negative)"
        },
        {
            "symbol": "ŷ (y-hat)",
            "meaning": "Predicted Probability",
            "plain_english": "Probability output by the model after Sigmoid or Softmax (between 0 and 1)"
        },
        {
            "symbol": "C",
            "meaning": "Number of Classes",
            "plain_english": "Total number of candidate target categories in the classification task"
        },
        {
            "symbol": "ŷ_correct",
            "meaning": "Target Class Probability",
            "plain_english": "The model's predicted confidence assigned to the single true class"
        }
    ],
    "numerical_example": "Cat, Dog, Bird 3-Class Classifier (True Label = Cat, One-Hot: [1, 0, 0]):\n1. Model A (Confident & Correct): Predicts [0.90, 0.08, 0.02]\n   • Loss = -[1 · log(0.90) + 0 · log(0.08) + 0 · log(0.02)] = -log(0.90) ≈ 0.105 (Very low loss).\n2. Model B (Uncertain): Predicts [0.34, 0.33, 0.33]\n   • Loss = -log(0.34) ≈ 1.079 (Moderate loss penalty for lack of confidence).\n3. Model C (Confident & Disastrously Wrong): Predicts [0.001, 0.998, 0.001] (claims 99.8% Dog)\n   • Loss = -log(0.001) ≈ 6.908 (Exploding loss penalty providing an aggressive gradient kick).",
    "pitfalls": "Common Pitfall: Applying Mean Squared Error (MSE) to classification networks. When an initial prediction is severely wrong, Sigmoid and Softmax gradients saturate to 0, permanently stalling training. Cross-Entropy completely eliminates this failure mode.",
    "core_logic": "Why this matters: Cross-Entropy (H(P, Q)) is the total average bits needed to describe reality (P) using model predictions (Q). The log cancels the exponential in Sigmoid/Softmax, ensuring gradient updates are directly proportional to error: ∂L/∂z = ŷ - y.",
    "architectural_logic": "In modern Large Language Models (LLMs) and vision architectures, Cross-Entropy loss is paired directly with Softmax in logit space via PyTorch's nn.CrossEntropyLoss for numerical stability (LogSumExp trick), preventing underflow on 100k+ token vocabularies.",
    "connected_logic": [
        {
            "title": "Why Not MSE? The Vanishing Gradient Proof",
            "content": "• If a model predicts ŷ = 0.0001 for true class y = 1, MSE gradient (ŷ - y)σ'(z) collapses to zero because Sigmoid's derivative σ'(z) is flat at extremes.\n• Cross-Entropy's logarithm directly cancels the exponential in Softmax/Sigmoid, producing an uncluttered gradient ∂L/∂z = ŷ - y = -0.9999 that forcefully corrects errors."
        },
        {
            "title": "Next-Token Prediction: The Engine of Large Language Models",
            "content": "• LLMs like GPT-4 and Gemini predict the next token across vocabularies of ~100,000 candidate words, outputting a probability distribution via Softmax.\n• Training minimizes -log P(next_token); if the model predicts 90% for the ground truth word, loss is 0.10, but if it predicts 0.01%, loss explodes to 9.21."
        },
        {
            "title": "Label Smoothing: Preventing Overconfident Overfitting",
            "content": "• Hard one-hot targets [1, 0, 0] force logits toward infinity to achieve ŷ = 1.0, making neural networks dangerously overconfident.\n• Label smoothing replaces hard targets with soft distributions [0.9, 0.05, 0.05], bounding logit magnitudes and boosting generalization."
        },
        {
            "title": "The KL Divergence Connection: Matching Model to Reality",
            "content": "• Because the true label entropy H(P) is constant and determined by the dataset, minimizing Cross-Entropy H(P, Q) is mathematically identical to minimizing D_KL(P || Q).\n• This guarantees that training a neural network with Cross-Entropy is mathematically equivalent to Maximum Likelihood Estimation (MLE) under a categorical distribution."
        }
    ],
    "key_takeaways": [
        "Core Principle: Cross-Entropy measures how well model probabilities Q describe ground-truth distribution P.",
        "One-Hot Simplicity: For single-label classification, multi-class loss simplifies to -log(ŷ_correct).",
        "Gradient Dynamics: Eliminates vanishing gradients by canceling Sigmoid/Softmax exponentials, yielding linear error ∂L/∂z = ŷ - y.",
        "Modern AI Engine: The loss function used to train all modern LLMs on next-token prediction across 100k+ vocabulary tokens."
    ],
    "definition_bullets": [
        "Binary Cross-Entropy (BCE): Loss function for binary 2-class tasks paired with Sigmoid, penalizing divergence from 0 or 1 labels.",
        "Categorical Cross-Entropy (CCE): Loss function for multi-class classification paired with Softmax, penalizing low confidence on the correct class."
    ]
}

def update_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    found = False
    for item in data:
        if item.get('id') == 'concept_cross_entropy':
            item.update(CROSS_ENTROPY_UPDATE)
            found = True
            break
            
    if not found:
        print(f"Warning: concept_cross_entropy not found in {filepath}")
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
        if item.get('id') == 'concept_cross_entropy':
            item.update(CROSS_ENTROPY_UPDATE)
            break
            
    new_content = '"""\nConcepts Database: Mathematical Foundations (19 Concepts)\n"""\n\nMATH_CONCEPTS = ' + json.dumps(mod.MATH_CONCEPTS, indent=4, ensure_ascii=False) + '\n'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Successfully updated {filepath}")

update_concepts_math()
