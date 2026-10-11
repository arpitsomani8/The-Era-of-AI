import json
import re

def main():
    # 1. Load concepts.json
    with open("src/data/concepts.json", "r", encoding="utf-8") as f:
        concepts = json.load(f)

    # 2. Load all_concepts.json
    with open("scripts/data_sources/all_concepts.json", "r", encoding="utf-8") as f:
        all_concepts = json.load(f)

    lr_data = {
        "id": "concept_learning_rate",
        "title": "Learning Rate & Step Size",
        "topic_id": "ml_opt",
        "topic_label": "Gradient Descent & Hyperparameters",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "raw_subtopic": "Learning Rate (Step size taken per iteration)",
        "def": "Learning rate is a crucial hyperparameter (written as η) that controls how big of a step a model takes when updating its parameters to reduce loss.",
        "formula": "$$w_{\\text{new}} = w_{\\text{old}} - \\eta \\cdot \\nabla L(w)$$",
        "logic": "The parameter update balances two key pieces: the gradient (∇L) gives the direction (uphill vs downhill), while the learning rate (η) controls the magnitude (how far to step). Because the actual step taken is η × Slope, the model naturally takes bigger steps on steep slopes and gentler steps as it nears the valley.",
        "example": "Training a neural net: With η = 10.0, the loss explodes to NaN as steps violently overshoot the valley. With η = 0.000001, the loss barely moves after 50 epochs. With a Goldilocks rate of η = 0.001, the weights smoothly glide to the minimum.",
        "tags": [
            "Learning Rate",
            "Step Size",
            "Gradient Descent",
            "Hyperparameters",
            "Optimization",
            "LR Finder",
            "Warmup"
        ],
        "definition": "Learning rate is a crucial hyperparameter (written as η) that controls how big of a step a model takes when updating its parameters to reduce loss.",
        "formula_explanation": "",
        "simple_summary": "Think of learning rate (η) as the stride length of a hiker walking down a foggy mountain to find the valley bottom. If your steps are microscopic, you will take forever to reach the bottom and might get stuck on flat plateaus. If your steps are giant leaps, you will overshoot the valley and crash into the opposite mountain wall. A 'Goldilocks' rate lets you walk fast at the start and smoothly settle right into the lowest point.",
        "core_terms": [
            {
                "term": "The Learning Rate (η)",
                "what_is_it": "• A hyperparameter chosen before training that scales the magnitude of parameter updates.\n• Common starting values are 0.1 for basic SGD, or 0.01 / 0.001 for adaptive optimizers like Adam.",
                "analogy": "The gas pedal on a car: pressing it gently moves you safely forward, but stomping on it causes you to spin out of control.",
                "why_it_matters": "Often considered the single most critical hyperparameter—an improper learning rate prevents models from learning anything at all."
            },
            {
                "term": "Step Size vs. Learning Rate",
                "what_is_it": "• A common beginner myth is that a fixed η means identical step sizes throughout training.\n• In reality, Step Size = η × Slope (||∇L||). As the model gets closer to the minimum, the slope flattens, so step sizes naturally shrink on their own!",
                "analogy": "Walking downhill on a skateboard: even with a fixed brake setting, your speed naturally slows down as the steep hill levels into a flat driveway.",
                "why_it_matters": "Explains why models naturally decelerate near the optimal solution without having to manually tweak η on every iteration."
            },
            {
                "term": "Learning Rate Schedulers (Warmup & Decay)",
                "what_is_it": "• Dynamic schedules that adjust η during training: Step Decay (cut η by 10x on plateaus), Cosine Annealing (smooth decay to 0), and Linear Warmup.\n• Transformers & LLMs (like GPT-4) use linear warmup for the first 2,000 steps to protect freshly randomized weights from shattering.",
                "analogy": "An airplane flight: gentle takeoff during warmup, cruising speed across training, and a smooth glide down for landing.",
                "why_it_matters": "Modern deep learning and LLMs never use a flat constant learning rate; dynamic schedules are required for top-tier stability and accuracy."
            }
        ],
        "symbol_guide": [
            {
                "symbol": "w_new",
                "meaning": "Updated Weight",
                "plain_english": "The new parameter value calculated after taking a step"
            },
            {
                "symbol": "w_old",
                "meaning": "Current Weight",
                "plain_english": "The weight's current value before the update"
            },
            {
                "symbol": "η (eta)",
                "meaning": "Learning Rate",
                "plain_english": "The hyperparameter scaling how far you jump (Magnitude)"
            },
            {
                "symbol": "∇L(w)",
                "meaning": "Gradient / Slope",
                "plain_english": "Points in the steepest uphill direction; we subtract it to move downhill (Direction)"
            },
            {
                "symbol": "η · ∇L(w)",
                "meaning": "Actual Step Taken",
                "plain_english": "The exact distance the weight moves: Learning Rate multiplied by the slope"
            }
        ],
        "numerical_example": "Step-by-Step Weight Update:\nFormula: w_new = w_old - η · (Slope)\n\nSuppose Current Weight w_old = 5.0, Slope (Gradient) = 4.0\n\nScenario 1: Goldilocks Rate (η = 0.1)\n• Actual Step Taken = 0.1 × 4.0 = 0.4\n• w_new = 5.0 - 0.4 = 4.6 (Smooth, steady progress downhill toward minimum at 0!)\n\nScenario 2: Too Small (η = 0.001)\n• Actual Step Taken = 0.001 × 4.0 = 0.004\n• w_new = 5.0 - 0.004 = 4.996 (Hardly moved; would need thousands of epochs to reach 0)\n\nScenario 3: Too Large (η = 2.0)\n• Actual Step Taken = 2.0 × 4.0 = 8.0\n• w_new = 5.0 - 8.0 = -3.0 (Overshot the minimum at 0, landing on the opposite canyon wall with a steeper slope!)\n\nTakeaway: The product of learning rate and slope determines whether you converge cleanly or explode into divergence.",
        "pitfalls": "Common Mistakes to Avoid:\n1. Setting η too large: Causes severe oscillations and divergence, printing 'Loss: NaN' or 'Loss: Inf' in your terminal as weights blow up to infinity.\n2. Setting η too small: Training takes forever (days instead of hours) and falls into the Saddle Point Trap—getting permanently trapped on flat plateaus.\n3. Assuming step size is fixed: Forgetting that Step Size = η · ||∇L||, so steep gradients cause big leaps even with a modest η.\n4. Skipping Warmup on Transformers: Bilions of random weights at Step 0 produce chaotic gradient spikes. Taking a normal step shatters attention layers; always use a linear warmup over the first 2,000 steps.\n5. Blind guessing: Instead of guessing random numbers, use Leslie Smith's LR Range Test (LR Finder) to inspect loss on a log scale and find the steepest downward slope.",
        "core_logic": "Why this matters: Gradient descent relies on a local linear approximation of the loss surface. If the step size is small, the linear approximation holds true and loss is guaranteed to decrease. But if the step size is too large, the surface curves away beneath the model, violating the linear assumption and launching weights out of the valley into runaway divergence.",
        "architectural_logic": "In PyTorch and TensorFlow, optimizers (SGD, AdamW) are combined with lr_scheduler modules. For Transformers, a Linear Warmup over 2,000 steps followed by Cosine Decay to 10% of peak η is the standard recipe across modern LLMs and foundation vision models.",
        "key_takeaways": [
            "Controls Update Magnitude: Learning rate (η) scales parameter changes along the negative gradient direction.",
            "Actual Step = η × Slope: Step size naturally shrinks as gradients flatten near the bottom of the valley.",
            "Avoid The Extremes: Too small crawls into saddle point traps; too large violently overshoots and explodes into NaNs.",
            "Use Modern Schedulers: Combine Linear Warmup with Cosine Decay for deep models, and use the LR Finder to locate the optimal rate."
        ],
        "definition_bullets": [
            "Learning Rate (η): The hyperparameter that sets the scale of parameter updates per training iteration.",
            "Step Size: The actual numerical shift applied to a weight (η · ||∇L||), combining learning rate and gradient steepness."
        ],
        "types_header": "Learning Rate Behaviors & Dynamic Schedulers",
        "types_badge": "Optimization Strategies",
        "quick_types": [
            {
                "type": "The Goldilocks Rate (η*)",
                "definition": "Fast enough to cover ground rapidly early on, yet small enough to smoothly settle into the optimal minimum without overshooting.",
                "looks_like": "η = 0.001 (standard starting default for Adam)"
            },
            {
                "type": "Step Decay (ReduceLROnPlateau)",
                "definition": "Divides the learning rate by 10 (e.g. 0.1 → 0.01) whenever validation loss stops improving for a set patience window (e.g. 3 epochs).",
                "looks_like": "torch.optim.lr_scheduler.ReduceLROnPlateau()"
            },
            {
                "type": "Cosine Annealing",
                "definition": "Lowers η following a smooth cosine curve, gently guiding the learning rate down to near zero at the final training epoch.",
                "looks_like": "torch.optim.lr_scheduler.CosineAnnealingLR()"
            },
            {
                "type": "Linear Warmup + Cosine Decay",
                "definition": "Starts η near zero and ramps up over the first 2,000 steps to protect random weights, then decays smoothly; universal standard for LLMs.",
                "looks_like": "get_cosine_schedule_with_warmup()"
            }
        ],
        "connected_logic": [
            {
                "title": "The 3 Components of the Update Rule",
                "content": "• w_new = w_old - [η] × [∇L(w)]\n• Current Weight (w_old): Where the parameter currently sits on the loss landscape.\n• Learning Rate (η): The hyperparameter scaling how far you jump (the magnitude).\n• Gradient (∇L): The local slope providing the uphill direction (subtracted to go downhill)."
            },
            {
                "title": "Too Small vs Too Large vs Goldilocks",
                "content": "• Too Small (η → 0): Takes microscopic baby steps; training takes days; gets trapped on flat saddle points.\n• Too Large (η ≫ 0): Overshoots canyon walls, oscillates wildly, and diverges until terminal prints 'Loss: NaN'.\n• Goldilocks (η*): Rapid early progress that cleanly settles into the global valley."
            },
            {
                "title": "Why Transformers & LLMs Require Warmup",
                "content": "• At Step 0, all billions of Transformer weights are random noise, creating chaotic initial gradients.\n• A normal step at Step 1 would permanently shatter the sensitive attention and layer norm projections.\n• Linear warmup gradually ramps η up over 2,000 steps, letting weights organize before taking full-sized steps."
            },
            {
                "title": "Leslie Smith's LR Range Test (The LR Finder)",
                "content": "• Popularized by Fast.ai: trains the model for just one single epoch from η = 10⁻⁷ exponentially up to 10.0.\n• Plots Loss vs Learning Rate on a log scale.\n• The Golden Rule: Choose the learning rate located at the steepest downward slope (typically one order of magnitude before the minimum point)."
            }
        ]
    }

    # Update in concepts.json
    for c in concepts:
        if c.get("id") == "concept_learning_rate":
            c.update(lr_data)
            print("Updated concept_learning_rate in concepts.json")
            break

    with open("src/data/concepts.json", "w", encoding="utf-8") as f:
        json.dump(concepts, f, indent=2, ensure_ascii=False)

    # Update in all_concepts.json
    for c in all_concepts:
        if c.get("id") == "concept_learning_rate":
            c.update(lr_data)
            print("Updated concept_learning_rate in all_concepts.json")
            break

    with open("scripts/data_sources/all_concepts.json", "w", encoding="utf-8") as f:
        json.dump(all_concepts, f, indent=2, ensure_ascii=False)

    # Update in concepts_ml.py
    with open("scripts/data_sources/concepts_ml.py", "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r'\{\s*"id":\s*"concept_learning_rate".*?\},(?=\s*\{\s*"id":\s*"concept_batch_sizes")'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        lines = json.dumps(lr_data, indent=4, ensure_ascii=False).splitlines()
        indented_replacement = "\n".join("    " + line for line in lines) + ","
        new_content = content[:match.start()] + indented_replacement + content[match.end():]
        with open("scripts/data_sources/concepts_ml.py", "w", encoding="utf-8") as f:
            f.write(new_content)
        print("Updated concept_learning_rate in concepts_ml.py")
    else:
        print("Could not find regex match in concepts_ml.py")

if __name__ == "__main__":
    main()
