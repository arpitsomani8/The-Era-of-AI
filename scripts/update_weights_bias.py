import json
import re

def main():
    # 1. Load concepts.json
    with open("src/data/concepts.json", "r", encoding="utf-8") as f:
        concepts = json.load(f)

    # 2. Load all_concepts.json
    with open("scripts/data_sources/all_concepts.json", "r", encoding="utf-8") as f:
        all_concepts = json.load(f)

    weights_bias_data = {
        "id": "concept_weights_bias",
        "title": "Weights (Slopes) & Bias (Intercept)",
        "topic_id": "ml_linear",
        "topic_label": "Linear Regression & Core ML Concepts",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "raw_subtopic": "Weights (Slopes w) & Bias (Intercept b)",
        "def": "Weights are multipliers that control how strongly each input feature influences the prediction, while bias is the baseline value added when all inputs are zero.",
        "formula": "$$\\hat{y} = \\mathbf{w}^T \\mathbf{x} + b = w_1 x_1 + w_2 x_2 + \\dots + w_d x_d + b$$",
        "logic": "In a linear model, the weight acts as the slope (telling the model how steep the line is and which way it tilts), while the bias acts as the intercept (allowing the line to slide up or down so it doesn't get stuck at the origin (0, 0)).",
        "example": "Predicting house prices: Price = (200 × Area) + (-5,000 × Distance to City) + 50,000. Here, 200 and -5,000 are the weights (area increases price, distance decreases it), and $50,000 is the bias (baseline price).",
        "tags": [
            "Weights",
            "Bias",
            "Slopes",
            "Intercept",
            "Linear Model",
            "Parameters"
        ],
        "definition": "Weights are multipliers that control how strongly each input feature influences the prediction, while bias is the baseline value added when all inputs are zero.",
        "formula_explanation": "",
        "simple_summary": "Think of a line equation: ŷ = w · x + b. The weight (w) is the slope—it decides how much the prediction changes when a feature goes up or down. The bias (b) is the starting point—it shifts the line up or down so the model isn't forced to pass through zero. During training, the model uses gradient descent to adjust both numbers until its predictions are as close to real answers as possible.",
        "core_terms": [
            {
                "term": "Weight (Slope w)",
                "what_is_it": "• A multiplier attached to an input feature that controls its influence and direction.\n• Positive weight means the prediction goes up with the feature; negative weight means it goes down.",
                "analogy": "A volume knob on a stereo: turning it up gives that specific instrument more power in the final song.",
                "why_it_matters": "Tells you how sensitive the model is to each feature; larger magnitude means a bigger change in prediction."
            },
            {
                "term": "Bias (Intercept b)",
                "what_is_it": "• A constant added to the prediction that sets the baseline output when all inputs equal zero.\n• Without bias (b = 0), the model is locked to the origin (0, 0), which ruins its ability to fit real data.",
                "analogy": "The base fare of a taxi ride: you pay $5 just for getting into the car, even before the taxi moves a single mile.",
                "why_it_matters": "Gives the model the freedom to shift its line up or down to fit where the actual data points sit."
            },
            {
                "term": "Neuron Firing Threshold (Deep Learning)",
                "what_is_it": "• In neural networks, bias shifts the activation curve left or right to set how easily a neuron fires.\n• A negative bias makes a neuron harder to activate, while a positive bias makes it fire easily.",
                "analogy": "The sensitivity setting on a smoke detector: adjust it so it triggers only for real smoke and ignores steam.",
                "why_it_matters": "Allows individual artificial neurons in deep networks to remain inactive until strong signals arrive."
            }
        ],
        "types_header": "How Weights & Bias Shape Predictions",
        "types_badge": "Parameter Dynamics",
        "quick_types": [
            {
                "type": "Positive Weight (w > 0)",
                "definition": "The prediction increases as the feature increases (e.g., more square footage leads to higher house price).",
                "looks_like": "Slope tilts upward (/)"
            },
            {
                "type": "Negative Weight (w < 0)",
                "definition": "The prediction decreases as the feature increases (e.g., greater distance from city center leads to lower price).",
                "looks_like": "Slope tilts downward (\\)"
            },
            {
                "type": "Near-Zero Weight (w ≈ 0)",
                "definition": "The feature has very little effect on the prediction (e.g., paint color code having almost no impact on house price).",
                "looks_like": "Flat horizontal line (—)"
            },
            {
                "type": "Scikit-Learn Extraction",
                "definition": "Accessing the learned parameters directly after calling model.fit().",
                "looks_like": "weights = model.coef_, bias = model.intercept_"
            },
            {
                "type": "Deep Learning Neuron",
                "definition": "Passing weighted inputs plus bias through an activation function like ReLU or Sigmoid.",
                "looks_like": "output = torch.relu(torch.matmul(x, w) + b)"
            }
        ],
        "symbol_guide": [
            {
                "symbol": "w",
                "meaning": "Weight (Slope)",
                "plain_english": "The learned multiplier for a single feature"
            },
            {
                "symbol": "b",
                "meaning": "Bias (Intercept)",
                "plain_english": "The learned baseline constant added to the prediction"
            },
            {
                "symbol": "w^T x",
                "meaning": "Dot Product",
                "plain_english": "Multiplying each feature by its weight and adding them all together"
            },
            {
                "symbol": "ŷ (y-hat)",
                "meaning": "Predicted Output",
                "plain_english": "The final value calculated by the model"
            }
        ],
        "numerical_example": "Predicting a Taxi Fare Step-by-Step:\nEquation: Fare = (Weight × Distance in Miles) + Bias\n\nGiven learned parameters:\n• Learned Weight w = $2.50 (cost per mile)\n• Learned Bias b = $3.00 (base pickup fee)\n\nRide 1: Distance x = 0 miles (just got into the cab)\n• Fare = (2.50 × 0) + 3.00 = $3.00 (the bias sets the starting baseline!)\n\nRide 2: Distance x = 10 miles\n• Fare = (2.50 × 10) + 3.00 = 25.00 + 3.00 = $28.00\n\nWhat happens if weight changes?\n• If w increases to $4.00, the line becomes steeper and every mile adds more cost.\n• If b increases to $5.00, the entire line shifts up by $2.00 for every trip.",
        "pitfalls": "Common Pitfall: Comparing weights before scaling features. If Feature A is measured in centimeters (values like 180) and Feature B is measured in meters (values like 1.8), their weights will have completely different sizes even if both features are equally important! Always standardize or scale features before using weight sizes to judge feature importance. Also, remember that negative weights are completely normal and simply mean an inverse relationship.",
        "core_logic": "Why this matters: Weights and biases are the actual 'knowledge' stored inside a trained machine learning model. When a model trains, it isn't memorizing your data; it is tuning these numbers so that multiplying inputs by weights and adding bias produces the closest possible guesses to the real targets.",
        "architectural_logic": "In modern neural networks, a linear layer (like nn.Linear(in_features, out_features)) stores weights as a matrix of shape (out_features, in_features) and bias as a vector of shape (out_features). Setting bias=False is only done when an immediate subsequent Batch Normalization layer would cancel the bias out anyway.",
        "connected_logic": [
            {
                "title": "Why Forcing Bias to Zero Hurts Models",
                "content": "• If you set bias to 0, the prediction line must pass through (0, 0).\n• If the true data has a non-zero baseline (like house prices never starting at $0), forcing b = 0 creates huge errors across all predictions."
            },
            {
                "title": "Feature Scaling Before Weight Comparison",
                "content": "• A large weight does not automatically mean a more important feature if features use different units.\n• Standardizing all features to mean 0 and variance 1 puts all weights on an equal scale so you can compare their magnitudes fairly."
            },
            {
                "title": "How Gradient Descent Updates Parameters",
                "content": "• The optimizer calculates the slope of the error for both w and b.\n• It subtracts a fraction of that gradient: w_new = w - (learning_rate × dLoss/dw), adjusting both numbers slightly on every step."
            },
            {
                "title": "From Single Lines to Deep Neural Networks",
                "content": "• A single linear regression has one weight per feature and one bias.\n• Deep neural networks stack dozens of layers of weights and biases separated by nonlinear activations, allowing them to learn complex curves and patterns."
            }
        ],
        "key_takeaways": [
            "Weights are Slopes: Control how strongly each feature changes the prediction and in what direction.",
            "Bias is the Intercept: Sets the baseline prediction when all inputs equal zero.",
            "Scale Before Comparing: Never judge feature importance by weight size without standardizing features first.",
            "Neuron Thresholds: In neural networks, bias sets how easily an artificial neuron fires."
        ],
        "definition_bullets": [
            "Weight: The learned coefficient multiplied by an input feature to determine its effect on the prediction.",
            "Bias: The learned constant added to a prediction to set the baseline starting value."
        ]
    }

    # Update in concepts.json
    for c in concepts:
        if c.get("id") == "concept_weights_bias":
            c.update(weights_bias_data)
            print("Updated concept_weights_bias in concepts.json")
            break

    with open("src/data/concepts.json", "w", encoding="utf-8") as f:
        json.dump(concepts, f, indent=2, ensure_ascii=False)

    # Update in all_concepts.json
    for c in all_concepts:
        if c.get("id") == "concept_weights_bias":
            c.update(weights_bias_data)
            print("Updated concept_weights_bias in all_concepts.json")
            break

    with open("scripts/data_sources/all_concepts.json", "w", encoding="utf-8") as f:
        json.dump(all_concepts, f, indent=2, ensure_ascii=False)

    # Update in concepts_ml.py
    with open("scripts/data_sources/concepts_ml.py", "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r'\{\s*"id":\s*"concept_weights_bias".*?\},(?=\s*\{\s*"id":\s*"concept_labeled_unlabeled")'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        lines = json.dumps(weights_bias_data, indent=4, ensure_ascii=False).splitlines()
        indented_replacement = "\n".join("    " + line for line in lines) + ","
        new_content = content[:match.start()] + indented_replacement + content[match.end():]
        with open("scripts/data_sources/concepts_ml.py", "w", encoding="utf-8") as f:
            f.write(new_content)
        print("Updated concept_weights_bias in concepts_ml.py")
    else:
        print("Could not find regex match in concepts_ml.py")

if __name__ == "__main__":
    main()
