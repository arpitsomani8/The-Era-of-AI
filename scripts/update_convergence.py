import json
import re

def main():
    # 1. Load concepts.json
    with open("src/data/concepts.json", "r", encoding="utf-8") as f:
        concepts = json.load(f)

    # 2. Load all_concepts.json
    with open("scripts/data_sources/all_concepts.json", "r", encoding="utf-8") as f:
        all_concepts = json.load(f)

    conv_data = {
        "id": "concept_convergence",
        "title": "Loss Convergence & Stopping Criteria",
        "topic_id": "ml_opt",
        "topic_label": "Gradient Descent & Hyperparameters",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "raw_subtopic": "Convergence (When loss plateaus and stops decreasing)",
        "def": "Loss convergence is the state where a model's loss plateaus and stops decreasing, while stopping criteria are the explicit rules used to decide when training should halt.",
        "formula": "$$\\Delta L_t = |L_{t-1} - L_t| < \\epsilon \\quad \\text{or} \\quad \\|\\nabla_\\theta L\\| < \\epsilon$$",
        "logic": "Training is not about running for as many epochs as possible. The goal is to reach a stable minimum and stop before wasting cloud computing or memorizing noise. Stopping criteria automate this decision by monitoring loss improvements, gradient magnitudes, and validation scores.",
        "example": "Training a neural net: At epoch 1, loss is 2.5; by epoch 15, loss is 0.35. Between epochs 15 and 20, loss changes by less than 0.0001 (convergence). An early stopping rule detects this plateau and halts training at epoch 20 instead of running to 1,000, saving 980 epochs of GPU compute.",
        "tags": [
            "Convergence",
            "Stopping Criteria",
            "Early Stopping",
            "Patience",
            "Tolerance",
            "Loss Curve",
            "Gradient Norm"
        ],
        "definition": "Loss convergence is the state where a model's loss plateaus and stops decreasing, while stopping criteria are the explicit rules used to decide when training should halt.",
        "formula_explanation": "",
        "simple_summary": "Think of loss convergence like boiling a pot of soup until it reaches the right temperature. At first, the temperature rises rapidly (fast learning). Eventually, it levels off at boiling point and stops rising (convergence). Stopping criteria act like an automatic kitchen timer or thermostat: they turn off the stove so your soup doesn't boil dry (wasting power) or burn to the bottom of the pot (overfitting).",
        "core_terms": [
            {
                "term": "Loss Convergence",
                "what_is_it": "• The state in optimization where loss changes very little from iteration to iteration.\n• Indicates that parameter updates have settled into a local or global minimum on the loss surface.",
                "analogy": "A rolling marble finally settling into the center curve of a bowl after slowing down.",
                "why_it_matters": "Tells you that the model has learned the main patterns from the data and further iterations yield diminishing returns."
            },
            {
                "term": "Stopping Criteria",
                "what_is_it": "• Predefined rules or thresholds programmed into the training loop that tell the computer when to halt.\n• Prevents infinite loops, runaway cloud compute costs, and overtraining.",
                "analogy": "The automatic shut-off click on a gas station nozzle that stops pumping fuel the instant your tank is full.",
                "why_it_matters": "Without stopping criteria, training either terminates too early (underfitting) or wastes hours burning cloud GPUs."
            },
            {
                "term": "The Tolerance Threshold (tol / ε)",
                "what_is_it": "• A minimum improvement value (e.g. 0.001) required between consecutive steps to count as real progress.\n• If the drop in loss is smaller than this threshold (ΔL < ε), training is considered converged.",
                "analogy": "A bathroom scale that ignores a 2-gram crumb on your shirt because it is below the scale's sensitivity threshold.",
                "why_it_matters": "Built directly into Scikit-Learn algorithms (as the tol parameter) so models stop automatically when changes become negligible."
            }
        ],
        "symbol_guide": [
            {
                "symbol": "L_t",
                "meaning": "Current Loss",
                "plain_english": "The error score measured at the current step or epoch t"
            },
            {
                "symbol": "ΔL_t",
                "meaning": "Loss Delta",
                "plain_english": "|L_(t-1) - L_t|: The improvement in loss from the previous epoch"
            },
            {
                "symbol": "ε (epsilon) / tol",
                "meaning": "Tolerance Threshold",
                "plain_english": "The minimum improvement required to consider training productive"
            },
            {
                "symbol": "||∇L||",
                "meaning": "Gradient Norm",
                "plain_english": "The total magnitude/steepness of the gradient vector across all parameters"
            },
            {
                "symbol": "Patience (p)",
                "meaning": "Epoch Grace Period",
                "plain_english": "The number of consecutive epochs without improvement allowed before halting"
            }
        ],
        "numerical_example": "Step-by-Step Stopping Threshold in Action:\n\nSetup: Logistic Regression with Tolerance tol = 0.001 and max_iter = 100\nFormula: Stop when ΔL = |L_(t-1) - L_t| < 0.001\n\n• Epoch 1: Loss = 0.850\n• Epoch 2: Loss = 0.420 ➔ ΔL = |0.850 - 0.420| = 0.430 (Much bigger than 0.001; keep training!)\n• Epoch 3: Loss = 0.210 ➔ ΔL = |0.420 - 0.210| = 0.210 (Good progress; keep training!)\n• Epoch 4: Loss = 0.152 ➔ ΔL = |0.210 - 0.152| = 0.058 (Making progress; keep training!)\n• Epoch 5: Loss = 0.1512 ➔ ΔL = |0.152 - 0.1512| = 0.0008 (Smaller than tol = 0.001!)\n\nResult: The stopping condition triggers at Epoch 5. Training halts immediately, saving 95 unnecessary epochs of compute!",
        "pitfalls": "Common Mistakes to Avoid:\n1. Setting tolerance or patience too small: If patience is only 1 epoch, random mini-batch noise can cause a temporary flat spot that triggers a premature stop.\n2. Stopping based only on Training Loss: Training loss can keep dropping forever while validation loss gets worse (overfitting); always evaluate generalization.\n3. Assuming zero gradient always means a great model: A tiny gradient norm (||∇L|| < ε) can occur at flat saddle points or poor local plateaus, not just global minima.\n4. Relying on max_epochs alone: Training for a fixed 500 epochs might run for 10 hours when the model already converged in 20 minutes.\n5. Forgetting to restore best weights: When patience expires at epoch 30, the weights at epoch 30 are slightly overfitted; always ensure your code restores the best checkpoint (e.g. from epoch 25).",
        "core_logic": "Why this matters: Convergence represents the point where optimization transitions from learning signals to fitting noise. Continuing to optimize past the validation convergence point forces weights to memorize individual sample coordinates, inflating generalization error.",
        "architectural_logic": "In Scikit-Learn, stopping is configured via tol=1e-4 and n_iter_no_change=5. In PyTorch Lightning, early stopping is added as a callback: EarlyStopping(monitor='val_loss', min_delta=1e-3, patience=5, mode='min', restore_best_weights=True).",
        "key_takeaways": [
            "Signals Optimal Training: Convergence indicates loss has stabilized and further training yields diminishing returns.",
            "Automates Stop Decisions: Stopping criteria prevent both underfitting (stopping too early) and overfitting (running too long).",
            "The 5 Core Rules: Max epochs, loss delta (tol), validation early stopping with patience, gradient norm, and compute budget.",
            "Saves Cloud Budget: Automated stopping eliminates wasted GPU hours and restores the best performing model checkpoint."
        ],
        "definition_bullets": [
            "Loss Convergence: The state where optimization reaches a plateau and further parameter updates produce negligible loss reduction.",
            "Stopping Criteria: Predefined mathematical conditions or resource limits that automatically terminate a model's training loop."
        ],
        "types_header": "The 5 Common Stopping Criteria",
        "types_badge": "Optimization Termination Rules",
        "quick_types": [
            {
                "type": "Early Stopping on Validation Loss",
                "definition": "Monitors holdout validation error; stops when validation loss fails to improve for a set number of consecutive epochs (patience).",
                "looks_like": "EarlyStopping(patience=5)"
            },
            {
                "type": "Loss Improvement Threshold (tol)",
                "definition": "Stops when the drop in loss between successive epochs is smaller than epsilon (|ΔL| < tol).",
                "looks_like": "SGDClassifier(tol=1e-3)"
            },
            {
                "type": "Gradient Norm Threshold (||∇L|| < ε)",
                "definition": "Stops when the magnitude of the parameter gradient vector drops near zero, indicating a flat stationary region.",
                "looks_like": "scipy.optimize(gtol=1e-5)"
            },
            {
                "type": "Maximum Number of Epochs (max_iter)",
                "definition": "A hard-coded safety upper bound that guarantees training will not run indefinitely regardless of loss.",
                "looks_like": "max_epochs = 100"
            },
            {
                "type": "Compute & Time Budget",
                "definition": "Stops when GPU cloud budget, job timeout limits, or wall-clock deadlines are reached.",
                "looks_like": "Trainer(max_time='12:00:00')"
            }
        ],
        "connected_logic": [
            {
                "title": "Diagnosing the 3 Loss Trajectory Patterns",
                "content": "• Loss is Decreasing: Model is making healthy progress; keep training as long as validation metrics improve.\n• Loss has Plateaued: Model has reached convergence, or learning rate is too small to make further progress.\n• Loss is Increasing or Unstable: Learning rate is too large or gradients are exploding; investigate hyperparameters before stopping."
            },
            {
                "title": "Scikit-Learn vs. PyTorch Stopping Syntax",
                "content": "• Scikit-Learn: Uses tol=1e-4 and n_iter_no_change=5 across LogisticRegression, SGDClassifier, and MLPClassifier.\n• PyTorch: Training loops evaluate val_loss at each epoch end, incrementing a patience_counter and triggering break when patience is exceeded."
            },
            {
                "title": "Mini-Batch Noise & Patience Smoothing",
                "content": "• In mini-batch gradient descent, random batch sampling causes natural loss fluctuations.\n• A strict rule of stopping after one flat step would quit prematurely on harmless batch noise.\n• A patience window of 3 to 10 epochs acts as a moving average filter, ensuring training only stops on genuine plateaus."
            },
            {
                "title": "The Compute Cost Trade-Off (Diminishing Returns)",
                "content": "• Reaching 90% accuracy often takes 10 epochs, but squeezing out the last 0.2% can take 100 more epochs.\n• In production engineering, cloud GPU hours cost money. Setting reasonable stopping criteria prevents spending 80% of your budget for a 0.1% accuracy gain."
            }
        ]
    }

    # Update in concepts.json
    for c in concepts:
        if c.get("id") == "concept_convergence":
            c.update(conv_data)
            print("Updated concept_convergence in concepts.json")
            break

    with open("src/data/concepts.json", "w", encoding="utf-8") as f:
        json.dump(concepts, f, indent=2, ensure_ascii=False)

    # Update in all_concepts.json
    for c in all_concepts:
        if c.get("id") == "concept_convergence":
            c.update(conv_data)
            print("Updated concept_convergence in all_concepts.json")
            break

    with open("scripts/data_sources/all_concepts.json", "w", encoding="utf-8") as f:
        json.dump(all_concepts, f, indent=2, ensure_ascii=False)

    # Update in concepts_ml.py
    with open("scripts/data_sources/concepts_ml.py", "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r'\{\s*"id":\s*"concept_convergence".*?\},(?=\s*\{\s*"id":\s*"concept_lr_schedules")'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        lines = json.dumps(conv_data, indent=4, ensure_ascii=False).splitlines()
        indented_replacement = "\n".join("    " + line for line in lines) + ","
        new_content = content[:match.start()] + indented_replacement + content[match.end():]
        with open("scripts/data_sources/concepts_ml.py", "w", encoding="utf-8") as f:
            f.write(new_content)
        print("Updated concept_convergence in concepts_ml.py")
    else:
        print("Could not find regex match in concepts_ml.py")

if __name__ == "__main__":
    main()
