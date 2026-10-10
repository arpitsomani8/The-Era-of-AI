import json
import re

def main():
    # 1. Load concepts.json
    with open("src/data/concepts.json", "r", encoding="utf-8") as f:
        concepts = json.load(f)

    # 2. Load all_concepts.json
    with open("scripts/data_sources/all_concepts.json", "r", encoding="utf-8") as f:
        all_concepts = json.load(f)

    features_labels_data = {
        "id": "concept_features_labels",
        "title": "Features (Inputs) & Labels (Targets)",
        "topic_id": "ml_linear",
        "topic_label": "Linear Regression & Core ML Concepts",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "raw_subtopic": "Features (Input attributes x) & Labels (Target outcome y)",
        "def": "Features are the input variables used to make a prediction, while a label (or target) is the actual answer the model learns to predict.",
        "formula": "$$\\mathbf{X} \\in \\mathbb{R}^{N \\times D} \\quad \\xrightarrow{\\text{Model } f(\\mathbf{X})} \\quad \\hat{\\mathbf{y}} \\approx \\mathbf{y} \\in \\mathbb{R}^N$$",
        "logic": "Machine learning learns the relationship between input clues (features X) and known answers (labels y). Once trained, the model takes new features it has never seen before and predicts their missing label.",
        "example": "Predicting house prices: The features are square footage, number of bedrooms, and location. The label is the actual selling price (like $350,000) that the model tries to predict.",
        "tags": [
            "Features",
            "Labels",
            "Targets",
            "Supervised Learning",
            "Data Types"
        ],
        "definition": "Features are the input variables used to make a prediction, while a label (or target) is the actual answer the model learns to predict.",
        "formula_explanation": "",
        "simple_summary": "Features (X) are the input clues you feed into a model, and the label (y) is the answer you want the model to guess. Features are stored as a 2D table of rows and columns, while labels are stored as a single list of answers. During training, the model studies both so it can accurately predict answers for brand-new examples.",
        "core_terms": [
            {
                "term": "Features (Inputs X)",
                "what_is_it": "• The measurable properties or clues describing each example in your dataset.\n• For example, a house's area, number of bedrooms, and zip code.",
                "analogy": "The clues in a detective mystery: fingerprints, footprints, and witness statements that help you solve the case.",
                "why_it_matters": "Without informative, relevant features that connect to the outcome, no machine learning model can make accurate predictions."
            },
            {
                "term": "Label (Target y)",
                "what_is_it": "• The ground-truth answer or outcome that the model is trying to learn and predict.\n• For example, whether an email is spam (1) or not spam (0), or the final sale price of a house.",
                "analogy": "The answer key on the back of a textbook that you use to grade your practice homework.",
                "why_it_matters": "Defines what problem you are solving—continuous numbers mean regression, while discrete categories mean classification."
            },
            {
                "term": "The Missing Label Golden Rule",
                "what_is_it": "• If a training row is missing its label (y), delete that row immediately.\n• You can fill in missing features (X) using mean or median, but you must never guess or invent the true answer you are trying to teach the model.",
                "analogy": "Studying for a test with flashcards where someone guessed the answers on the back: you will memorize wrong facts.",
                "why_it_matters": "Training on fabricated labels corrupts the entire learning process and ruins real-world model accuracy."
            }
        ],
        "types_header": "The 4 Roles of the Label (y)",
        "types_badge": "Learning Paradigms",
        "quick_types": [
            {
                "type": "Continuous Label (Regression)",
                "definition": "The target is a continuous number, such as predicting house price, temperature, or stock price.",
                "looks_like": "y = [350000.0, 420000.0, 195000.0]"
            },
            {
                "type": "Discrete Label (Classification)",
                "definition": "The target belongs to distinct categories, such as spam vs legitimate, or cat vs dog vs car.",
                "looks_like": "y = ['Spam', 'Ham'] or y = [0, 1, 2]"
            },
            {
                "type": "No Label At All (Unsupervised)",
                "definition": "There is no target column; the model discovers natural clusters or patterns using only features X.",
                "looks_like": "model = KMeans(n_clusters=3).fit(X)"
            },
            {
                "type": "Self-Supervised (Next-Token / LLMs)",
                "definition": "The label is generated automatically from raw text by using the very next word as the target answer.",
                "looks_like": "Input: 'The cat sat on the' -> Label: 'mat'"
            }
        ],
        "symbol_guide": [
            {
                "symbol": "X (Capital X)",
                "meaning": "Feature Matrix (2D)",
                "plain_english": "The 2D table of input data where each row is an example and each column is a feature"
            },
            {
                "symbol": "y (Lowercase y)",
                "meaning": "Target Vector (1D)",
                "plain_english": "The 1D column containing the true answer for each example"
            },
            {
                "symbol": "ŷ (y-hat)",
                "meaning": "Model Prediction",
                "plain_english": "The answer guessed by the model after looking at features X"
            },
            {
                "symbol": "N × D",
                "meaning": "Dataset Dimensions",
                "plain_english": "N is the number of samples (rows) and D is the number of features (columns)"
            }
        ],
        "numerical_example": "Features and Labels in a Small House-Price Table:\n\nFeatures Matrix X (3 Houses, 2 Features):\n  House 1: [1,800 sq ft, 3 Bedrooms]\n  House 2: [2,400 sq ft, 4 Bedrooms]\n  House 3: [1,200 sq ft, 2 Bedrooms]\n\nTarget Label Vector y (Actual Selling Prices):\n  House 1: $320,000\n  House 2: $450,000\n  House 3: $210,000\n\nHow Training Works:\n1. The model inspects X and compares its guesses with y.\n2. When given a brand-new unlabeled House 4 [2,000 sq ft, 3 Bedrooms], the model uses what it learned to predict: ŷ = $365,000.",
        "pitfalls": "Common Pitfall: Target Leakage. Never include a feature that contains information about the label that wouldn't be available at prediction time. For example, using 'cancellation date' to predict customer churn leaks the answer, because you only know the cancellation date after a customer has already canceled! Also, keep feature names, column order, and preprocessing strictly identical between training and live inference.",
        "core_logic": "Why this matters: Supervised machine learning is fundamentally about finding a mathematical function that maps input features X to output labels y. If your features have no real connection to the label, no algorithm in the world can learn to predict the answer.",
        "architectural_logic": "In code, features X are stored as a 2D NumPy array or Pandas DataFrame of shape (N, D), while labels y are stored as a 1D array of shape (N,). When deploying models, the serving pipeline receives only features X and outputs predictions ŷ.",
        "connected_logic": [
            {
                "title": "Supervised vs Unsupervised Data Shapes",
                "content": "• Supervised learning requires pairs of (X, y) so the model has correct answers to learn from.\n• Unsupervised learning takes only X, discovering groups (clustering) or reducing dimensions without any labels."
            },
            {
                "title": "Target Leakage vs Normal Features",
                "content": "• A valid feature is information you legitimately know before the event happens (e.g., past purchases).\n• A leaked feature uses future knowledge (e.g., refund transaction ID), creating fake 100% accuracy that crashes in production."
            },
            {
                "title": "Self-Supervised Labels in Modern LLMs",
                "content": "• Large language models don't need human-labeled data for pre-training.\n• They turn raw text into supervised pairs automatically by using the preceding words as X and the next word as y."
            },
            {
                "title": "Training-Serving Feature Consistency",
                "content": "• If a model trains on features named [Age, Income, City], the live production API must receive those exact same features in the exact same format.\n• Missing or misordered features at inference time lead to silent calculation errors."
            }
        ],
        "key_takeaways": [
            "Features are Inputs (X): Stored as a 2D table of clues describing each example.",
            "Labels are Outputs (y): Stored as a 1D list of ground-truth answers to predict.",
            "Label Dictates Task: Continuous labels mean regression; categorical labels mean classification.",
            "Never Impute Labels: Drop training rows missing their label; only impute missing features."
        ],
        "definition_bullets": [
            "Features: The input variables or attributes fed into a model to make a prediction.",
            "Labels: The ground-truth answers that a supervised model learns to predict."
        ]
    }

    # Update in concepts.json
    for c in concepts:
        if c.get("id") == "concept_features_labels":
            c.update(features_labels_data)
            print("Updated concept_features_labels in concepts.json")
            break

    with open("src/data/concepts.json", "w", encoding="utf-8") as f:
        json.dump(concepts, f, indent=2, ensure_ascii=False)

    # Update in all_concepts.json
    for c in all_concepts:
        if c.get("id") == "concept_features_labels":
            c.update(features_labels_data)
            print("Updated concept_features_labels in all_concepts.json")
            break

    with open("scripts/data_sources/all_concepts.json", "w", encoding="utf-8") as f:
        json.dump(all_concepts, f, indent=2, ensure_ascii=False)

    # Update in concepts_ml.py
    with open("scripts/data_sources/concepts_ml.py", "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r'\{\s*"id":\s*"concept_features_labels".*?\},(?=\s*\{\s*"id":\s*"concept_weights_bias")'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        lines = json.dumps(features_labels_data, indent=4, ensure_ascii=False).splitlines()
        indented_replacement = "\n".join("    " + line for line in lines) + ","
        new_content = content[:match.start()] + indented_replacement + content[match.end():]
        with open("scripts/data_sources/concepts_ml.py", "w", encoding="utf-8") as f:
            f.write(new_content)
        print("Updated concept_features_labels in concepts_ml.py")
    else:
        print("Could not find regex match in concepts_ml.py")

if __name__ == "__main__":
    main()
