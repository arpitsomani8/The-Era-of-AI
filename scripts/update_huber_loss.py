import json
import re

def main():
    # 1. Load concepts.json
    with open("src/data/concepts.json", "r", encoding="utf-8") as f:
        concepts = json.load(f)

    # 2. Load all_concepts.json
    with open("scripts/data_sources/all_concepts.json", "r", encoding="utf-8") as f:
        all_concepts = json.load(f)

    huber_data = {
        "id": "concept_huber_loss",
        "title": "Huber Loss (Smooth Robust Loss)",
        "topic_id": "ml_loss",
        "topic_label": "Loss Functions (L1, L2, MSE, MAE, Log Loss)",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "raw_subtopic": "Huber Loss (Smooth piecewise hybrid of L1 and L2)",
        "def": "Huber Loss is a hybrid loss function that acts like squared error (MSE) for small mistakes and acts like absolute error (MAE) for large mistakes.",
        "formula": "$$L_\\delta(e) = \\begin{cases} \\frac{1}{2} e^2 & \\text{if } |e| \\le \\delta \\\\ \\delta (|e| - \\frac{1}{2} \\delta) & \\text{if } |e| > \\delta \\end{cases}$$",
        "logic": "MSE gives smooth gradients for small errors but explodes on outliers, while MAE resists outliers but has a sharp, jagged corner at zero. Huber Loss combines the best of both: it gives smooth math near zero, and caps the penalty for wild outliers into a straight, gentle line.",
        "example": "Self-driving car steering: Small tracking errors (off by a few centimeters) use squared loss to make smooth, steady steering corrections. If a sensor glitch reports an impossible 500-meter jump (outlier), Huber loss switches to linear loss so the car doesn't jerk the wheel violently.",
        "tags": [
            "Huber Loss",
            "Robust Regression",
            "Smooth L1 Loss",
            "Loss Functions",
            "Outliers"
        ],
        "definition": "Huber Loss is a hybrid loss function that acts like squared error (MSE) for small mistakes and acts like absolute error (MAE) for large mistakes.",
        "formula_explanation": "",
        "simple_summary": "Huber Loss gives you the best of MSE and MAE. It uses a cutoff value called delta (δ). If your prediction error is smaller than delta, it squares the error so gradient descent glides smoothly to the bottom. If the error is larger than delta, it switches to a straight line so crazy outliers cannot explode your gradients or break your model.",
        "core_terms": [
            {
                "term": "Huber Loss (Smooth Robust Hybrid)",
                "what_is_it": "• A loss function that seamlessly merges MSE for small errors and MAE for large errors.\n• Formula switches based on threshold δ: ½e² when |e| ≤ δ, and δ(|e| - ½δ) when |e| > δ.",
                "analogy": "A speed bump with gentle rounded slopes at the bottom so you can roll smoothly, but a flat top so cars don't scrape.",
                "why_it_matters": "Provides smooth, stable convergence near zero without letting massive outliers derail your model."
            },
            {
                "term": "The Delta Threshold (δ)",
                "what_is_it": "• The boundary parameter that decides when an error stops being 'small' and becomes 'large'.\n• A smaller δ makes the loss act more like MAE (outlier-proof); a larger δ makes it act more like MSE.",
                "analogy": "The sensitivity knob on a microphone: setting the volume level where background whispers are picked up smoothly, but sudden loud shouts are clipped.",
                "why_it_matters": "Must be tuned to match the scale and units of your target variable so the switch happens at the right error size."
            },
            {
                "term": "The Capped Gradient Superpower",
                "what_is_it": "• In neural networks, the gradient of Huber Loss can never exceed ±δ, no matter how huge the error is.\n• If an outlier has an error of 10,000, MSE sends a 10,000 gradient step that breaks the network, while Huber Loss caps the step at exactly δ.",
                "analogy": "A circuit breaker in your house: if a massive power surge hits, it caps the current so your appliances don't explode.",
                "why_it_matters": "Prevents exploding gradients and NaN weight errors during deep learning training."
            }
        ],
        "types_header": "MSE vs MAE vs Huber Loss",
        "types_badge": "Loss Function Comparison",
        "quick_types": [
            {
                "type": "MSE (Squared Error)",
                "definition": "Quadratic everywhere; smooth at zero, but easily derailed by extreme outliers.",
                "looks_like": "L = (y - y_hat)**2"
            },
            {
                "type": "MAE (Absolute Error)",
                "definition": "Linear everywhere; robust to outliers, but has an awkward sharp V-corner at zero.",
                "looks_like": "L = abs(y - y_hat)"
            },
            {
                "type": "Huber Loss (Hybrid)",
                "definition": "Quadratic for small errors and linear for large errors; smooth at zero and robust to outliers.",
                "looks_like": "torch.nn.HuberLoss(delta=1.0)"
            },
            {
                "type": "Smooth L1 Loss (PyTorch)",
                "definition": "A popular implementation of Huber Loss widely used in object detection bounding-box regression.",
                "looks_like": "torch.nn.SmoothL1Loss(beta=1.0)"
            }
        ],
        "symbol_guide": [
            {
                "symbol": "e",
                "meaning": "Prediction Error",
                "plain_english": "The difference between actual value and prediction (y - ŷ)"
            },
            {
                "symbol": "δ (delta)",
                "meaning": "Transition Threshold",
                "plain_english": "The error size where the loss switches from quadratic to linear"
            },
            {
                "symbol": "|e| ≤ δ",
                "meaning": "Small Error Zone",
                "plain_english": "Errors inside this range are squared (behaving like MSE)"
            },
            {
                "symbol": "|e| > δ",
                "meaning": "Large Error Zone",
                "plain_english": "Errors outside this range are treated linearly (behaving like MAE)"
            }
        ],
        "numerical_example": "Calculating Huber Loss with δ = 2.0:\n\nCase A: Small Error (Inside the Quadratic Zone)\n• Actual y = 10, Predicted ŷ = 9 → Error e = 1.0\n• Since |1.0| ≤ 2.0 (small error), use ½ e²:\n• Loss = 0.5 × (1.0)² = 0.5\n\nCase B: Large Outlier Error (Inside the Linear Zone)\n• Actual y = 10, Predicted ŷ = 20 → Error e = 10.0\n• Since |10.0| > 2.0 (large error), use δ(|e| - ½δ):\n• Loss = 2.0 × (10.0 - 0.5 × 2.0) = 2.0 × (10.0 - 1.0) = 18.0\n\nCompare with MSE for Case B:\n• MSE penalty would be ½ × (10.0)² = 50.0!\n• Huber loss kept the penalty at 18.0 instead of 50.0, protecting the model from overreacting.",
        "pitfalls": "Common Pitfall: Leaving delta at the default value of 1.0 without checking data scale. If your target variable is house prices in hundreds of thousands of dollars, an error of $5,000 will be treated as an extreme outlier if delta is 1.0! The loss would become almost 100% linear everywhere. Always scale your features and targets (e.g. using StandardScaler) so that delta=1.0 aligns with a standard deviation of 1, or adjust delta to match your target units.",
        "core_logic": "Why this matters: In calculus, connecting a parabola y = ½x² with a line y = x at point x = 1 creates a curve where both the value and the derivative match up seamlessly (derivative is x for x ≤ 1, and 1 for x > 1). This mathematical continuity ensures gradient descent transitions from big errors to fine-tuning without sudden jumps or oscillations.",
        "architectural_logic": "In object detection architectures like Faster R-CNN and YOLO, bounding box coordinate regression uses Smooth L1 Loss (Huber Loss). Because initial box proposals can be wildly off target, Huber's capped gradients prevent gradient explosion during early training epochs.",
        "connected_logic": [
            {
                "title": "Why the Derivative Matches at Delta",
                "content": "• The slope of ½e² at e = δ is exactly δ.\n• The slope of the linear part δ(|e| - ½δ) is also δ.\n• Because the two slopes match perfectly, the gradient transitions smoothly with zero mathematical bumps."
            },
            {
                "title": "Capping the Gradient to Prevent NaNs",
                "content": "• Under MSE, if an outlier error is 1,000, the gradient is 1,000, which can push weights out of bounds.\n• Under Huber loss with δ = 1, the gradient is capped at 1.0, shielding the neural network from explosive updates."
            },
            {
                "title": "Smooth L1 Loss in Computer Vision",
                "content": "• Used in Fast R-CNN and RetinaNet for predicting [x, y, width, height] of bounding boxes.\n• Replaced pure L2 loss because it made training dramatically more stable against initial random box proposals."
            },
            {
                "title": "How to Choose Delta",
                "content": "• In scikit-learn's HuberRegressor, epsilon is set by default to 1.35, which achieves 95% statistical efficiency on normal data.\n• If you normalize targets to mean 0 and standard deviation 1, δ = 1.0 is almost always a reliable default."
            }
        ],
        "key_takeaways": [
            "Best of Both: Quadratic like MSE for small errors; linear like MAE for large errors.",
            "Smooth at Zero: Derivative gently approaches zero, unlike MAE's sharp corner.",
            "Gradient Cap: Gradient never exceeds ±δ, preventing exploding gradients from extreme outliers.",
            "Tune Delta to Units: Adjust δ based on target scale, or standardize targets to mean 0 and std 1."
        ],
        "definition_bullets": [
            "Huber Loss: A smooth, robust piecewise loss function that transitions from squared error to linear error at a threshold delta.",
            "Smooth L1 Loss: A variant of Huber Loss commonly used in deep learning and computer vision bounding-box regression."
        ]
    }

    # Update in concepts.json
    for c in concepts:
        if c.get("id") == "concept_huber_loss":
            c.update(huber_data)
            print("Updated concept_huber_loss in concepts.json")
            break

    with open("src/data/concepts.json", "w", encoding="utf-8") as f:
        json.dump(concepts, f, indent=2, ensure_ascii=False)

    # Update in all_concepts.json
    for c in all_concepts:
        if c.get("id") == "concept_huber_loss":
            c.update(huber_data)
            print("Updated concept_huber_loss in all_concepts.json")
            break

    with open("scripts/data_sources/all_concepts.json", "w", encoding="utf-8") as f:
        json.dump(all_concepts, f, indent=2, ensure_ascii=False)

    # Update in concepts_ml.py
    with open("scripts/data_sources/concepts_ml.py", "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r'\{\s*"id":\s*"concept_huber_loss".*?\},(?=\s*\{\s*"id":\s*"concept_binary_cross_entropy")'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        lines = json.dumps(huber_data, indent=4, ensure_ascii=False).splitlines()
        indented_replacement = "\n".join("    " + line for line in lines) + ","
        new_content = content[:match.start()] + indented_replacement + content[match.end():]
        with open("scripts/data_sources/concepts_ml.py", "w", encoding="utf-8") as f:
            f.write(new_content)
        print("Updated concept_huber_loss in concepts_ml.py")
    else:
        print("Could not find regex match in concepts_ml.py")

if __name__ == "__main__":
    main()
