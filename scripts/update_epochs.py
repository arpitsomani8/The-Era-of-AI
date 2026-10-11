import json
import re

def main():
    # 1. Load concepts.json
    with open("src/data/concepts.json", "r", encoding="utf-8") as f:
        concepts = json.load(f)

    # 2. Load all_concepts.json
    with open("scripts/data_sources/all_concepts.json", "r", encoding="utf-8") as f:
        all_concepts = json.load(f)

    epoch_data = {
        "id": "concept_epochs",
        "title": "Epochs & Training Passes",
        "topic_id": "ml_opt",
        "topic_label": "Gradient Descent & Hyperparameters",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "raw_subtopic": "Epochs (Full passes over the entire training set)",
        "def": "An epoch is one complete pass through the entire training dataset during model training.",
        "formula": "$$\\text{Updates per Epoch} = \\left\\lceil \\frac{N}{B} \\right\\rceil, \\quad \\text{Total Updates} = E \\times \\left\\lceil \\frac{N}{B} \\right\\rceil$$",
        "logic": "A model rarely learns complex relationships in a single pass because small learning rates nudge weights only a fraction of the distance per step. Multiple epochs let the optimizer repeatedly refine its parameters. However, training for too many epochs causes overfitting, where the model starts memorizing noise instead of learning general rules.",
        "example": "A dataset of 1,000 examples trained with batch size 100 executes 10 iterations per epoch. Training for 30 epochs yields 300 total gradient updates. At epoch 30, validation loss reaches its lowest point; pushing to epoch 100 reduces training loss to near zero but causes validation loss to curve upward into overfitting.",
        "tags": [
            "Epochs",
            "Training Passes",
            "Forward Pass",
            "Backward Pass",
            "Early Stopping",
            "Underfitting",
            "Overfitting"
        ],
        "definition": "An epoch is one complete pass through the entire training dataset during model training.",
        "formula_explanation": "",
        "simple_summary": "Think of an epoch as reading a textbook from cover to cover once. Reading only 2 chapters (underfitting) means you fail the test because you haven't learned enough. Reading the textbook 20 to 30 times (the sweet spot) helps you understand the core concepts so you can answer brand-new questions. But memorizing the book 100 times (overfitting) means you can recite page numbers and typos word-for-word, but stumble on real-world exams because you memorized the noise.",
        "core_terms": [
            {
                "term": "Epoch vs. Batch vs. Iteration (Step)",
                "what_is_it": "• Epoch: One complete pass through all N examples in the training dataset.\n• Batch: A group of B examples processed together in one step (e.g., 64 rows).\n• Iteration (Step): One single parameter update where the optimizer calculates gradients on a batch and updates weights.",
                "analogy": "Reading a 10-chapter book: the whole book is an Epoch, one chapter is a Batch, and turning each page to study it is an Iteration.",
                "why_it_matters": "Fundamental machine learning vocabulary; confusing iterations with epochs causes severe sizing and scheduling bugs in training scripts."
            },
            {
                "term": "The 3 Types of Passes (Forward, Backward, Epoch)",
                "what_is_it": "• Forward Pass: Input (X) flows through layers to make predictions (ŷ) and compute the loss.\n• Backward Pass: loss.backward() calculates gradients, and optimizer.step() updates weights.\n• Epoch Pass: The complete loop of forward and backward passes until every single sample in the dataset has been processed.",
                "analogy": "A golf swing: swinging forward (Forward Pass), checking how far off the ball landed (Backward Pass), and repeating across all 18 holes of the course (Epoch Pass).",
                "why_it_matters": "Clarifies the exact sequence running inside every deep learning training loop across PyTorch and TensorFlow."
            },
            {
                "term": "Early Stopping & Patience",
                "what_is_it": "• An automated guardrail that monitors validation loss after every epoch.\n• If validation loss fails to improve for a set number of consecutive epochs (patience, e.g., 5 epochs), training halts automatically and restores the best checkpoint.",
                "analogy": "An oven thermometer that automatically turns off the heat when the cake is perfectly baked, instead of letting it burn on a rigid timer.",
                "why_it_matters": "Saves massive amounts of GPU compute time and permanently prevents models from drifting into severe overfitting."
            }
        ],
        "symbol_guide": [
            {
                "symbol": "E",
                "meaning": "Number of Epochs",
                "plain_english": "The total count of full passes through the training dataset"
            },
            {
                "symbol": "N",
                "meaning": "Training Dataset Size",
                "plain_english": "The total number of available training samples"
            },
            {
                "symbol": "B",
                "meaning": "Batch Size",
                "plain_english": "The number of examples grouped into each training update step"
            },
            {
                "symbol": "⌈N / B⌉",
                "meaning": "Iterations per Epoch",
                "plain_english": "The number of batch updates needed to complete one full epoch"
            },
            {
                "symbol": "Total Updates",
                "meaning": "Lifetime Updates",
                "plain_english": "E × ⌈N / B⌉: The total count of optimizer weight adjustments during training"
            }
        ],
        "numerical_example": "Step-by-Step Training Updates & Loss Curve Tracking:\n\nDataset: N = 10,000 images | Batch Size: B = 64 | Epochs: E = 20\n• Updates per Epoch = ⌈10,000 / 64⌉ = 157 iterations\n• Total Training Updates = 20 × 157 = 3,140 optimizer steps\n\nHow the Model Evolves Over 20 Epochs:\n• Epochs 1 to 5 (Zone 1 - Underfitting): Train Loss = 2.45 ➔ 1.10, Val Loss = 2.50 ➔ 1.15. Both dropping fast; keep training!\n• Epoch 14 (Zone 2 - The Optimal Sweet Spot): Train Loss = 0.35, Val Loss hits lowest minimum at 0.38. (Best model checkpoint saved here!)\n• Epochs 15 to 20 (Zone 3 - Overfitting): Train Loss drops to 0.12, but Val Loss climbs upward to 0.52! Early stopping halts training with patience = 5.",
        "pitfalls": "Common Mistakes to Avoid:\n1. Assuming more epochs always mean higher accuracy: Beyond the sweet spot, training loss continues dropping toward 0 while validation loss turns upward, ruining real-world generalization.\n2. Thinking the model resets after every epoch: Parameters carry forward continuously; an epoch is just another loop over the data, not a fresh start.\n3. Monitoring only training loss: Never decide training length based solely on training loss; always track validation loss on a separate validation set.\n4. Using the test set for early stopping: Never touch the test set during training or early stopping decisions! Reserve the test set strictly for final reporting.\n5. Training LLMs like vision models: Traditional vision models train for 100+ epochs, but modern LLMs (like GPT-4) train for only 1 to 2 epochs over trillions of tokens to avoid memorization.",
        "core_logic": "Why this matters: Training loss measures errors on examples the model has already memorized. Validation loss measures errors on unseen examples to test true generalization. Tracking both across epochs reveals the exact moment a model transitions from learning real patterns to memorizing training noise.",
        "architectural_logic": "In PyTorch Lightning and Hugging Face Transformers, early stopping is configured as a callback: EarlyStopping(monitor='val_loss', patience=5, mode='min'). ModelCheckpoint(save_best_only=True) automatically serializes the optimal weights when val_loss hits its lowest point, discarding later overfitted states.",
        "key_takeaways": [
            "One Epoch = Full Pass: One epoch means every training example has been evaluated exactly once.",
            "The 3 Curve Zones: Underfitting (Zone 1), Optimal Sweet Spot (Zone 2), and Overfitting (Zone 3).",
            "Early Stopping Saves Compute: Monitor validation loss with patience to stop automatically and restore the best weights.",
            "Vision vs. LLMs: Vision models train for 100+ epochs, while LLMs train for only 1 to 2 epochs over trillions of tokens."
        ],
        "definition_bullets": [
            "Epoch: One complete pass through the entire training dataset during which every example is processed.",
            "Early Stopping: An optimization technique that halts training when validation loss stops improving for a specified patience window."
        ],
        "types_header": "The 3 Zones of the Epoch Loss Curve",
        "types_badge": "Training Trajectory & Generalization",
        "quick_types": [
            {
                "type": "Zone 1: Underfitting (Early Epochs)",
                "definition": "Both training loss and validation loss are high and falling rapidly; the model hasn't had enough iterations to discover underlying patterns.",
                "looks_like": "Epochs 0 to 10 (Keep training!)"
            },
            {
                "type": "Zone 2: The Optimal Sweet Spot",
                "definition": "Validation loss reaches its global minimum; the model has learned true generalizable features before memorizing training set noise.",
                "looks_like": "Epoch ~30 (Best Checkpoint!)"
            },
            {
                "type": "Zone 3: Overfitting (Late Epochs)",
                "definition": "Training loss continues plunging toward zero, but validation loss curves upward; the model is memorizing training quirks and losing real-world accuracy.",
                "looks_like": "Epochs 40 to 100+ (Halt training!)"
            },
            {
                "type": "Modern LLM Regime (1 to 2 Epochs)",
                "definition": "Trained across massive web-scale corpora (trillions of tokens); 1 to 2 passes prevent verbatim memorization and maximize knowledge breadth.",
                "looks_like": "GPT-4 / LLaMA Pretraining"
            }
        ],
        "connected_logic": [
            {
                "title": "The 3 Types of Passes (Forward, Backward, Epoch)",
                "content": "• Forward Pass: Input (X) flows through layers to predict ŷ and calculate loss.\n• Backward Pass: Backpropagation computes gradients (loss.backward()) and updates weights (optimizer.step()).\n• Epoch Pass: The complete loop of forward and backward passes until all N samples in the dataset have been processed."
            },
            {
                "title": "The 3 Zones of the Loss Curve",
                "content": "• Zone 1 (Underfitting): Both train and val loss drop rapidly; keep training.\n• Zone 2 (Sweet Spot): Val loss reaches its lowest point; save model checkpoint.\n• Zone 3 (Overfitting): Train loss drops to near zero, but val loss curves upward; model is memorizing noise."
            },
            {
                "title": "Early Stopping & Model Checkpointing",
                "content": "• Monitors validation loss at the end of each epoch.\n• Patience: Number of epochs to wait without improvement before stopping (e.g. 5 epochs).\n• Best Checkpoint: Automatically restores the weights from the epoch with lowest validation loss, throwing away later overfitted epochs."
            },
            {
                "title": "Why Vision Models Need 100+ Epochs but LLMs Use 1-2",
                "content": "• Vision datasets (ImageNet with ~1.2M images) are relatively small, requiring 90 to 300 epochs for convolutional filters to converge.\n• LLMs are trained on trillions of tokens (entire internet). At that scale, 1 to 2 epochs provide enough gradient steps, while repeating text tokens causes verbatim memorization and hallucinations."
            }
        ]
    }

    # Update in concepts.json
    for c in concepts:
        if c.get("id") == "concept_epochs":
            c.update(epoch_data)
            print("Updated concept_epochs in concepts.json")
            break

    with open("src/data/concepts.json", "w", encoding="utf-8") as f:
        json.dump(concepts, f, indent=2, ensure_ascii=False)

    # Update in all_concepts.json
    for c in all_concepts:
        if c.get("id") == "concept_epochs":
            c.update(epoch_data)
            print("Updated concept_epochs in all_concepts.json")
            break

    with open("scripts/data_sources/all_concepts.json", "w", encoding="utf-8") as f:
        json.dump(all_concepts, f, indent=2, ensure_ascii=False)

    # Update in concepts_ml.py
    with open("scripts/data_sources/concepts_ml.py", "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r'\{\s*"id":\s*"concept_epochs".*?\},(?=\s*\{\s*"id":\s*"concept_convergence")'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        lines = json.dumps(epoch_data, indent=4, ensure_ascii=False).splitlines()
        indented_replacement = "\n".join("    " + line for line in lines) + ","
        new_content = content[:match.start()] + indented_replacement + content[match.end():]
        with open("scripts/data_sources/concepts_ml.py", "w", encoding="utf-8") as f:
            f.write(new_content)
        print("Updated concept_epochs in concepts_ml.py")
    else:
        print("Could not find regex match in concepts_ml.py")

if __name__ == "__main__":
    main()
