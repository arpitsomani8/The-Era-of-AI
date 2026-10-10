import json
import re

def main():
    # 1. Load concepts.json
    with open("src/data/concepts.json", "r", encoding="utf-8") as f:
        concepts = json.load(f)

    # 2. Load all_concepts.json
    with open("scripts/data_sources/all_concepts.json", "r", encoding="utf-8") as f:
        all_concepts = json.load(f)

    labeled_unlabeled_data = {
        "id": "concept_labeled_unlabeled",
        "title": "Labeled vs Unlabeled Examples",
        "topic_id": "ml_linear",
        "topic_label": "Linear Regression & Core ML Concepts",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "raw_subtopic": "Labeled vs Unlabeled Examples",
        "def": "A labeled example includes both input features and the correct answer (x, y), while an unlabeled example includes only the features (x) without any target answer.",
        "formula": "$$\\mathcal{D}_{\\text{labeled}} = \\{(x_i, y_i)\\}_{i=1}^N, \\quad \\mathcal{D}_{\\text{unlabeled}} = \\{x_j\\}_{j=1}^M \\implies \\hat{y}_j = f(x_j)$$",
        "logic": "Labeled data is used during training so the model can check its mistakes and adjust its weights. Unlabeled data represents new real-world inputs where the answer is unknown, and the trained model must predict it.",
        "example": "Spam filter: 10,000 emails already marked by humans as 'Spam' or 'Inbox' are labeled examples used to train the model. A brand-new email arriving in your inbox right now is an unlabeled example that the model needs to classify.",
        "tags": [
            "Labeled Data",
            "Unlabeled Data",
            "Supervised Learning",
            "Semi-Supervised",
            "Self-Supervised"
        ],
        "definition": "A labeled example includes both input features and the correct answer (x, y), while an unlabeled example includes only the features (x) without any target answer.",
        "formula_explanation": "",
        "simple_summary": "Labeled examples have the answers included (features + target); models use them during training to learn. Unlabeled examples have no answers; they are what your model sees in the real world when making predictions. Unlabeled data is cheap and abundant, while labeled data is expensive because it usually requires humans to review and tag it.",
        "core_terms": [
            {
                "term": "Labeled Example (x, y)",
                "what_is_it": "• A data row containing both the input features (x) and the confirmed correct answer (y).\n• Used during model training so the algorithm can calculate its error and update its parameters.",
                "analogy": "A practice math worksheet that includes the full answer key printed at the bottom of the page.",
                "why_it_matters": "Supervised machine learning cannot train without labeled examples to guide its loss function."
            },
            {
                "term": "Unlabeled Example (x)",
                "what_is_it": "• A data row containing only the input features (x) with no target answer provided.\n• Used in production inference where the model must guess the missing answer, or in unsupervised clustering.",
                "analogy": "The final exam handed to a student: all the questions are there, but the student must fill in the answers.",
                "why_it_matters": "Real-world data is almost always unlabeled when it arrives; the entire purpose of deploying an AI model is to label it."
            },
            {
                "term": "Self-Supervised Learning (LLMs)",
                "what_is_it": "• A modern training technique that automatically creates its own labels from raw, unlabeled text.\n• For example, hiding the next word in a sentence and training the model to predict it without human labeling.",
                "analogy": "A student reading a book and testing themselves by covering up the last word of every sentence with their thumb.",
                "why_it_matters": "Enables training massive models (like ChatGPT and Claude) on billions of web pages without paying humans to label them."
            }
        ],
        "types_header": "How Machine Learning Uses Labeled & Unlabeled Data",
        "types_badge": "Data Paradigms",
        "quick_types": [
            {
                "type": "Supervised Learning",
                "definition": "Trains exclusively on labeled pairs (x, y) to predict continuous values or categories.",
                "looks_like": "model.fit(X_train, y_train)"
            },
            {
                "type": "Unsupervised Learning",
                "definition": "Finds hidden patterns or groups using only unlabeled features (x) with no answers.",
                "looks_like": "KMeans(n_clusters=4).fit(X_unlabeled)"
            },
            {
                "type": "Semi-Supervised Learning",
                "definition": "Combines a small set of labeled data with a large collection of unlabeled data to improve accuracy.",
                "looks_like": "LabelPropagation().fit(X_mixed, y_partially_known)"
            },
            {
                "type": "Self-Supervised (Next-Token)",
                "definition": "Generates labels automatically from the sequence itself, powering modern language models.",
                "looks_like": "Input: 'Artificial intelligence is' -> Target: 'transforming'"
            },
            {
                "type": "Pseudo-Labeling",
                "definition": "Uses a trained model to predict labels on unlabeled data, then trains again on the confident predictions.",
                "looks_like": "y_pseudo = model.predict(X_unlabeled); filter high confidence"
            }
        ],
        "symbol_guide": [
            {
                "symbol": "(x, y)",
                "meaning": "Labeled Observation",
                "plain_english": "A complete training pair containing inputs x and true target y"
            },
            {
                "symbol": "(x)",
                "meaning": "Unlabeled Observation",
                "plain_english": "Input features only, with no target answer provided"
            },
            {
                "symbol": "ŷ (y-hat)",
                "meaning": "Predicted Label",
                "plain_english": "The output guess produced by the model for an unlabeled input"
            },
            {
                "symbol": "D_train",
                "meaning": "Training Dataset",
                "plain_english": "The collection of labeled rows used to fit the model parameters"
            }
        ],
        "numerical_example": "Tracking Data in a Real-World Machine Learning Pipeline:\n\nStep 1: Training Phase (Labeled Data)\n• Row 1: [Age: 45, Cholesterol: 240] -> Heart Disease: YES (y=1)\n• Row 2: [Age: 25, Cholesterol: 160] -> Heart Disease: NO (y=0)\n• Row 3: [Age: 52, Cholesterol: 210] -> Heart Disease: YES (y=1)\nThe model trains on these 3 labeled rows and learns the risk formula.\n\nStep 2: Production Phase (Unlabeled Data)\n• Patient 4 walks in: [Age: 48, Cholesterol: 230] -> Disease: ???\nThis is an unlabeled example (x). The model uses its learned weights to output: ŷ = YES (88% probability).\n\nStep 3: Delayed Feedback (Converting Unlabeled to Labeled)\n• Six months later, medical tests confirm Patient 4 actually developed heart disease (y=1).\n• This row now becomes a new labeled example and gets added to the training set for the next model update!",
        "pitfalls": "Common Pitfall: Training on missing labels or pseudo-label feedback loops. If a row is missing its target in your training dataset, never try to guess or impute it—filter it out with df[df['target'].notna()]. When using pseudo-labeling, be extremely careful: if your model makes a mistake and you accept it as a true label, the model will reinforce its own error during retraining. Also watch out for label noise, where humans accidentally assigned wrong tags during manual review.",
        "core_logic": "Why this matters: Getting labeled data is usually the biggest bottleneck in machine learning. While collecting raw text, images, or click logs is cheap and automated, having domain experts label them costs time and money. Modern AI strategies focus on maximizing what can be learned from vast unlabeled pools before spending money on human labels.",
        "architectural_logic": "In production data pipelines, incoming live inference requests (unlabeled x) and their model predictions (ŷ) are logged to a message queue like Kafka. When ground-truth outcomes arrive later (e.g., chargeback notices or loan defaults), they are joined by record ID to create fresh labeled training records.",
        "connected_logic": [
            {
                "title": "The Data Economics Bottleneck",
                "content": "• Unlabeled data is everywhere: millions of unread forum posts, hospital scans, and sensor logs.\n• Labeled data requires paid human review, making high-quality labeled datasets scarce and valuable."
            },
            {
                "title": "Semi-Supervised Label Propagation",
                "content": "• When you only have 50 labeled examples and 10,000 unlabeled ones, label propagation connects similar rows in feature space.\n• It spreads the known labels to their nearest neighbors, expanding your training set without manual work."
            },
            {
                "title": "Self-Supervised Learning in Foundation Models",
                "content": "• Large language models removed the need for manual human labeling by predicting the next word in massive text dumps.\n• This allowed models to scale from thousands of training samples to trillions of tokens."
            },
            {
                "title": "Label Noise and Quality Auditing",
                "content": "• Having a label doesn't mean it's 100% correct; human annotators frequently disagree or make mistakes.\n• Auditing label quality using consensus voting or confident learning prevents noisy labels from degrading model accuracy."
            }
        ],
        "key_takeaways": [
            "Labeled (x, y): Has features and confirmed answers; used to train supervised models.",
            "Unlabeled (x): Has features only; used during live inference and unsupervised clustering.",
            "Cost Difference: Unlabeled data is cheap and abundant; labeled data is scarce and expensive.",
            "Delayed Feedback: Live unlabeled predictions eventually become tomorrow's labeled training data."
        ],
        "definition_bullets": [
            "Labeled Example: A data sample that contains both input features and the true ground-truth outcome.",
            "Unlabeled Example: A data sample that contains only input features without any target answer."
        ]
    }

    # Update in concepts.json
    for c in concepts:
        if c.get("id") == "concept_labeled_unlabeled":
            c.update(labeled_unlabeled_data)
            print("Updated concept_labeled_unlabeled in concepts.json")
            break

    with open("src/data/concepts.json", "w", encoding="utf-8") as f:
        json.dump(concepts, f, indent=2, ensure_ascii=False)

    # Update in all_concepts.json
    for c in all_concepts:
        if c.get("id") == "concept_labeled_unlabeled":
            c.update(labeled_unlabeled_data)
            print("Updated concept_labeled_unlabeled in all_concepts.json")
            break

    with open("scripts/data_sources/all_concepts.json", "w", encoding="utf-8") as f:
        json.dump(all_concepts, f, indent=2, ensure_ascii=False)

    # Update in concepts_ml.py
    with open("scripts/data_sources/concepts_ml.py", "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r'\{\s*"id":\s*"concept_labeled_unlabeled".*?\},(?=\s*\{\s*"id":\s*"concept_normal_equation")'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        lines = json.dumps(labeled_unlabeled_data, indent=4, ensure_ascii=False).splitlines()
        indented_replacement = "\n".join("    " + line for line in lines) + ","
        new_content = content[:match.start()] + indented_replacement + content[match.end():]
        with open("scripts/data_sources/concepts_ml.py", "w", encoding="utf-8") as f:
            f.write(new_content)
        print("Updated concept_labeled_unlabeled in concepts_ml.py")
    else:
        print("Could not find regex match in concepts_ml.py")

if __name__ == "__main__":
    main()
