import json
import re

def main():
    # 1. Load concepts.json
    with open("src/data/concepts.json", "r", encoding="utf-8") as f:
        concepts = json.load(f)

    # 2. Load all_concepts.json
    with open("scripts/data_sources/all_concepts.json", "r", encoding="utf-8") as f:
        all_concepts = json.load(f)

    batch_data = {
        "id": "concept_batch_sizes",
        "title": "Batch Size (Full Batch vs Mini-Batch vs SGD)",
        "topic_id": "ml_opt",
        "topic_label": "Gradient Descent & Hyperparameters",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "raw_subtopic": "Batch Size (Full Batch vs Mini-Batch vs Single-Sample SGD)",
        "def": "Batch size determines how many training examples a model evaluates to calculate the gradient before updating its parameters.",
        "formula": "$$\\nabla L_{\\text{batch}} = \\frac{1}{B} \\sum_{i=1}^B \\nabla L_i(w), \\quad B \\in \\{1, 32, 64, 128, \\dots, N\\}$$",
        "logic": "Gradient descent can process all data at once (Full Batch), one sample at a time (Pure SGD), or in small groups (Mini-Batch). Mini-batch is the undisputed industry standard because it maximizes GPU parallel computing while introducing healthy gradient noise that helps models settle into broad, generalizable valleys.",
        "example": "Training on 100,000 images: Full batch tries to load all 100,000 images at once and crashes GPU memory (OOM). Pure SGD updates 100,000 times on 1 image each, leaving 99.9% of GPU cores idle. Mini-batch size 128 computes 128 images simultaneously across GPU Tensor Cores, performing ~781 fast, well-vectorized updates per epoch.",
        "tags": [
            "Batch Size",
            "Mini-Batch",
            "SGD",
            "Full Batch",
            "GPU Optimization",
            "Flat Minima",
            "DataLoader"
        ],
        "definition": "Batch size determines how many training examples a model evaluates to calculate the gradient before updating its parameters.",
        "formula_explanation": "",
        "simple_summary": "Think of batch size as how many practice questions a student reviews before checking the answer key and correcting mistakes. Full-batch studies the entire textbook before checking answers once (accurate but causes memory overload). Pure SGD checks answers after every single question (constant frantic zig-zag corrections). Mini-batch (groups of 32, 64, or 128) is the sweet spot: fast group processing that unlocks full GPU power and produces models that generalize best to the real world.",
        "core_terms": [
            {
                "term": "Mini-Batch Gradient Descent (The Industry Standard)",
                "what_is_it": "• Groups examples into small slices (typically 32, 64, 128, or 256) per parameter update.\n• Strikes the optimal balance: frequent updates per epoch, efficient memory use, and full GPU tensor core utilization.",
                "analogy": "A restaurant chef cooking dishes in small batches of 4 to 8 meals instead of one single fry at a time or making 500 meals simultaneously.",
                "why_it_matters": "The universal backbone for training modern computer vision, NLP, and large language models (LLMs)."
            },
            {
                "term": "Flat Minima vs. Sharp Minima (Generalization)",
                "what_is_it": "• Massive batches (B = 10,000+) compute ultra-precise gradients that drop models into narrow, fragile pits (sharp minima), which fail when test data shifts.\n• Mini-batches (B = 32 to 256) introduce subtle sampling noise like tiny earthquakes, shaking weights out of narrow pits into wide, robust valleys (flat minima).",
                "analogy": "A wide valley vs a tight crack: if you stand in a wide valley and the wind shifts (real-world data), you stay balanced; if you stand on a needle crack, you immediately stumble.",
                "why_it_matters": "Explains why smaller/medium mini-batches almost always generalize better to unseen test data than gigantic batches."
            },
            {
                "term": "Hardware Alignment (Why Powers of 2: 32, 64, 128)",
                "what_is_it": "• Computer hardware (GPU VRAM memory buses, Tensor Cores, and warp sizes of 32 threads) is organized in binary powers.\n• Setting batch size to 32, 64, or 128 aligns perfectly with GPU thread blocks, running much faster than an odd number like 61.",
                "analogy": "Packing cargo into rectangular shipping containers: standard box sizes pack tightly with zero wasted space, while odd-shaped boxes leave empty gaps.",
                "why_it_matters": "Maximizes GPU memory bandwidth and prevents idle CUDA cores during matrix multiplication."
            }
        ],
        "symbol_guide": [
            {
                "symbol": "B",
                "meaning": "Batch Size",
                "plain_english": "The number of training examples processed together in one forward/backward pass"
            },
            {
                "symbol": "N",
                "meaning": "Total Dataset Size",
                "plain_english": "The total number of available training samples"
            },
            {
                "symbol": "∇L_i(w)",
                "meaning": "Sample Gradient",
                "plain_english": "The gradient slope calculated for a single individual example i"
            },
            {
                "symbol": "(1/B) ∑ ∇L_i",
                "meaning": "Batch Average Gradient",
                "plain_english": "The mean gradient across all B examples in the batch used to update weights"
            },
            {
                "symbol": "N / B",
                "meaning": "Steps per Epoch",
                "plain_english": "The number of parameter update iterations completed during one full pass through the dataset"
            }
        ],
        "numerical_example": "Comparison of 3 Batch Regimes on a Dataset of N = 10,000 Examples:\n\n1. Full-Batch Gradient Descent (B = 10,000):\n• Updates per Epoch: 10,000 / 10,000 = 1 update per epoch\n• Trajectory: Perfectly smooth, deterministic glide down the average slope\n• Risk: Enormous memory footprint; risks Out-Of-Memory (OOM) on large datasets\n\n2. Pure Stochastic Gradient Descent (SGD) (B = 1):\n• Updates per Epoch: 10,000 / 1 = 10,000 updates per epoch\n• Trajectory: The 'Drunk Sailor' path—wild zig-zag oscillations driven by individual sample noise\n• Inefficiency: Evaluates 1 row at a time, leaving 99.9% of GPU parallel cores completely idle\n\n3. Mini-Batch Gradient Descent (B = 64):\n• Updates per Epoch: 10,000 / 64 ≈ 157 updates per epoch\n• Trajectory: Semi-smooth descent with gentle, beneficial stochastic noise\n• Benefit: Fully saturates GPU Tensor Cores, trains fast, and discovers robust flat minima!",
        "pitfalls": "Common Mistakes & Traps:\n1. Assuming larger batches always make better models: Gigantic batches (B = 10,000+) yield very low training loss but overfit to sharp minima, degrading test accuracy.\n2. Causing Out-Of-Memory (OOM) crashes: Pushing batch size beyond GPU VRAM limits causes instant fatal crashes. If you need a larger effective batch, use Gradient Accumulation instead of raising physical batch size.\n3. Using non-binary batch sizes: Setting B = 61 or 100 underutilizes GPU warps; always prefer powers of 2 (32, 64, 128, 256) for optimal hardware throughput.\n4. Forgetting shuffle=True in DataLoader: Without randomizing sample order every epoch, cyclical order patterns bias the gradients and cause loss oscillations.\n5. Confusing the optimizer name with batch size: Strictly speaking, pure SGD means B = 1. However, ML frameworks (e.g. PyTorch's torch.optim.SGD) use the name SGD for the mathematical update algorithm, which is routinely run with mini-batches of 32 or 64.",
        "core_logic": "Why this matters: Mini-batch gradient descent is the ideal compromise between the law of large numbers and compute hardware architecture. A full-batch gradient accurately reflects the true dataset expectation E[∇L], but computing it requires loading all N rows simultaneously. A mini-batch gradient provides an unbiased estimator with low variance that fits comfortably in GPU caches and Tensor Cores.",
        "architectural_logic": "In PyTorch, data streaming is managed via torch.utils.data.DataLoader(dataset, batch_size=64, shuffle=True, pin_memory=True, num_workers=4). Setting pin_memory=True and num_workers enables asynchronous CPU-to-GPU memory transfer, ensuring GPU cores are never starved waiting for the next mini-batch.",
        "key_takeaways": [
            "Balances Speed & Updates: Mini-batch blends GPU matrix parallelism with frequent weight updates.",
            "Discovers Flat Minima: Natural mini-batch noise shakes optimization out of narrow pits into robust valleys.",
            "Hardware Optimized: Powers of 2 (32, 64, 128) maximize GPU memory bandwidth and warp occupancy.",
            "Optimizer vs Batch Size: 'SGD' in PyTorch refers to the update algorithm, even when paired with mini-batches."
        ],
        "definition_bullets": [
            "Batch Size: The number of training examples processed together in one forward and backward pass before updating model parameters.",
            "Flat Minima: Broad, stable valleys in the loss landscape found by mini-batch optimization that generalize well when real-world test data shifts."
        ],
        "types_header": "The 3 Core Batch Regimes",
        "types_badge": "Compute & Convergence Trade-offs",
        "quick_types": [
            {
                "type": "Mini-Batch Gradient Descent (B = 32 to 512)",
                "definition": "The undisputed industry standard: groups samples to maximize GPU Tensor Core parallelism while retaining beneficial gradient noise.",
                "looks_like": "DataLoader(batch_size=64)"
            },
            {
                "type": "Full-Batch Gradient Descent (B = N)",
                "definition": "Processes the entire dataset for each single update; deterministic and stable, but computationally slow and prone to GPU Out-of-Memory (OOM) crashes.",
                "looks_like": "Batch Size = len(train_dataset)"
            },
            {
                "type": "Pure Stochastic Gradient Descent (B = 1)",
                "definition": "Updates weights after each individual example; very cheap per step, but follows a noisy 'Drunk Sailor' path and severely underutilizes GPU hardware.",
                "looks_like": "DataLoader(batch_size=1)"
            },
            {
                "type": "Gradient Accumulation",
                "definition": "Simulates large batch training on small GPUs by summing gradients across multiple mini-batches before calling optimizer.step().",
                "looks_like": "loss.backward() x N steps then step()"
            }
        ],
        "connected_logic": [
            {
                "title": "Full Batch vs Mini-Batch vs Pure SGD",
                "content": "• Full Batch (B = N): All examples processed together ➔ 1 update per epoch. Deterministic and smooth, but suffers from high memory use and OOM risk.\n• Mini-Batch (B = 32 to 256): Small groups processed together ➔ frequent updates, high GPU throughput, and superior generalization.\n• Pure SGD (B = 1): One example processed at a time ➔ fast individual steps, but erratic zig-zag path that wastes 99.9% of GPU cores."
            },
            {
                "title": "Sharp vs Flat Minima (The Secret to Generalization)",
                "content": "• Huge batches (B = 10,000+) calculate exact gradients that guide the model into narrow, steep crevices (Sharp Minima).\n• When real-world test distributions shift slightly, loss on sharp minima explodes!\n• Mini-batches (B = 32 to 256) generate mild stochastic noise like tiny tremors that bump the model into wide, flat basins (Flat Minima), ensuring robust real-world performance."
            },
            {
                "title": "Why GPUs Love Powers of 2 (32, 64, 128, 256)",
                "content": "• GPU hardware architectures are built around binary units: NVIDIA warps contain exactly 32 threads, and Tensor Cores process matrix tiles in multiples of 16 and 32.\n• A batch size of 64 or 128 aligns perfectly with GPU memory buses and cache lines, running substantially faster than odd numbers like 61."
            },
            {
                "title": "PyTorch DataLoader & The SGD Terminology Disconnect",
                "content": "• In code, torch.utils.data.DataLoader(dataset, batch_size=64, shuffle=True) loads samples in randomized groups of 64.\n• Setting shuffle=True prevents cyclical batch ordering that could cause gradient resonance.\n• Terminology note: While 'pure SGD' means batch_size=1, deep learning practitioners use torch.optim.SGD with mini-batches of 64 or 128 every day."
            }
        ]
    }

    # Update in concepts.json
    for c in concepts:
        if c.get("id") == "concept_batch_sizes":
            c.update(batch_data)
            print("Updated concept_batch_sizes in concepts.json")
            break

    with open("src/data/concepts.json", "w", encoding="utf-8") as f:
        json.dump(concepts, f, indent=2, ensure_ascii=False)

    # Update in all_concepts.json
    for c in all_concepts:
        if c.get("id") == "concept_batch_sizes":
            c.update(batch_data)
            print("Updated concept_batch_sizes in all_concepts.json")
            break

    with open("scripts/data_sources/all_concepts.json", "w", encoding="utf-8") as f:
        json.dump(all_concepts, f, indent=2, ensure_ascii=False)

    # Update in concepts_ml.py
    with open("scripts/data_sources/concepts_ml.py", "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r'\{\s*"id":\s*"concept_batch_sizes".*?\},(?=\s*\{\s*"id":\s*"concept_epochs")'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        lines = json.dumps(batch_data, indent=4, ensure_ascii=False).splitlines()
        indented_replacement = "\n".join("    " + line for line in lines) + ","
        new_content = content[:match.start()] + indented_replacement + content[match.end():]
        with open("scripts/data_sources/concepts_ml.py", "w", encoding="utf-8") as f:
            f.write(new_content)
        print("Updated concept_batch_sizes in concepts_ml.py")
    else:
        print("Could not find regex match in concepts_ml.py")

if __name__ == "__main__":
    main()
