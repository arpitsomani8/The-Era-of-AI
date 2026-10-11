import json
import re

def update_all():
    with open("src/data/concepts.json", "r", encoding="utf-8") as f:
        concepts = json.load(f)

    with open("scripts/data_sources/all_concepts.json", "r", encoding="utf-8") as f:
        all_concepts = json.load(f)

    with open("scripts/data_sources/concepts_ml.py", "r", encoding="utf-8") as f:
        py_content = f.read()

    # 1. CLEAN LEARNING RATE
    lr_data = {
        "id": "concept_learning_rate",
        "title": "Learning Rate & Step Size",
        "topic_id": "ml_opt",
        "topic_label": "Gradient Descent & Hyperparameters",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "raw_subtopic": "Learning Rate (Step size taken per iteration)",
        "def": "Learning rate (η) is the hyperparameter that controls how large of a step a model takes when updating its weights to reduce prediction loss.",
        "formula": "$$w_{\\text{new}} = w_{\\text{old}} - \\eta \\cdot \\nabla L(w)$$",
        "logic": "The parameter update balances two forces: the gradient (∇L) gives the direction (downhill), while the learning rate (η) sets the magnitude (how far to step). Because the actual step taken is η × slope, the model automatically takes bigger strides on steep slopes and gentler steps as it nears the valley.",
        "example": "If η = 10.0, the model violently overshoots the valley and crashes with NaN loss. If η = 0.000001, the weights barely move after 50 epochs. With a tuned rate like η = 0.001, the model steadily glides down to the minimum.",
        "tags": [
            "Learning Rate",
            "Step Size",
            "Gradient Descent",
            "Hyperparameters",
            "Optimization",
            "LR Finder",
            "Warmup"
        ],
        "definition": "Learning rate (η) is the hyperparameter that controls how large of a step a model takes when updating its weights to reduce prediction loss.",
        "formula_explanation": "",
        "simple_summary": "Think of learning rate (η) as the stride length of a hiker walking down a mountain into a valley. If your steps are microscopic, you will take forever to reach the bottom and might get stuck on flat plateaus. If your steps are giant leaps, you will overshoot the valley and crash into the opposite cliff wall. A 'Goldilocks' rate lets you walk fast at the start and smoothly settle right at the lowest point.",
        "core_terms": [
            {
                "term": "Learning Rate (η)",
                "what_is_it": "• The primary scaling factor chosen before training that determines the pace of weight updates.\n• Common starting values are 0.1 for basic SGD, or 0.001 for adaptive optimizers like Adam.",
                "analogy": "The gas pedal on a car: pressing it gently moves you safely forward, but stomping on it causes you to spin out.",
                "why_it_matters": "It is widely considered the single most important hyperparameter—get it wrong, and the model cannot learn anything."
            },
            {
                "term": "Actual Step Size (η × Slope)",
                "what_is_it": "• A common beginner misconception is that fixed η means identical steps throughout training.\n• The actual step taken equals η × ||∇L||. As the model nears the bottom, the slope flattens, so step sizes naturally shrink on their own!",
                "analogy": "Rolling downhill on a skateboard: even without touching the brakes, you naturally slow down as the steep hill levels out into a flat driveway.",
                "why_it_matters": "Explains why models can decelerate smoothly into the minimum without having to manually tweak η at every iteration."
            },
            {
                "term": "Gradient Direction (-∇L)",
                "what_is_it": "• The gradient points in the steepest uphill direction where loss increases most.\n• By placing a minus sign in front (-η · ∇L), we force the weights to step downhill toward lower error.",
                "analogy": "A marble released on a curved bowl: gravity naturally pulls it straight down the steepest slope toward the center.",
                "why_it_matters": "Provides the mathematical compass so the optimizer always knows which way is downhill."
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
                "plain_english": "The scaling multiplier controlling step magnitude"
            },
            {
                "symbol": "∇L(w)",
                "meaning": "Gradient / Slope",
                "plain_english": "The directional slope telling us which way is steepest uphill"
            },
            {
                "symbol": "η · ∇L(w)",
                "meaning": "Actual Step Taken",
                "plain_english": "The exact numerical distance the weight moves in parameter space"
            }
        ],
        "numerical_example": "Step-by-Step Weight Update:\nFormula: w_new = w_old - η · (Slope)\n\nSuppose Current Weight w_old = 5.0, Slope (Gradient) = 4.0\n\n1. Goldilocks Rate (η = 0.1):\n• Step Taken = 0.1 × 4.0 = 0.4\n• w_new = 5.0 - 0.4 = 4.6 (Smooth, steady downhill progress toward 0!)\n\n2. Too Small (η = 0.001):\n• Step Taken = 0.001 × 4.0 = 0.004\n• w_new = 5.0 - 0.004 = 4.996 (Barely moved; requires thousands of epochs)\n\n3. Too Large (η = 2.0):\n• Step Taken = 2.0 × 4.0 = 8.0\n• w_new = 5.0 - 8.0 = -3.0 (Overshot the valley floor at 0 and landed on the opposing wall with a steeper slope!)",
        "pitfalls": "Common Mistakes to Avoid:\n1. Setting η too high: Causes violent oscillations and divergence, printing 'Loss: NaN' or 'Loss: Inf' in your terminal.\n2. Setting η too low: Training takes days instead of hours, and the model easily gets trapped in flat saddle points.\n3. Assuming step size is fixed: Forgetting that step size = η × slope, so steep initial gradients cause big jumps even with small η.\n4. Skipping Warmup on Transformers: Billions of random weights at step 0 cause chaotic gradient spikes; always use a linear warmup over the first 2,000 steps.\n5. Guessing randomly: Instead of guessing numbers, use the Learning Rate Range Test (LR Finder) to spot the steepest loss drop on a log plot.",
        "core_logic": "Why this matters: Gradient descent relies on a local linear approximation. If your step size is small, the linear approximation holds true and loss is guaranteed to decrease. But if your step is too large, the loss surface curves away beneath you, violating the linear assumption and launching weights into runaway divergence.",
        "architectural_logic": "In deep learning frameworks, schedulers like torch.optim.lr_scheduler.CosineAnnealingLR wrap around optimizers. For Transformers and LLMs, a Linear Warmup over 2,000 steps followed by Cosine Decay to 10% of peak η is the standard recipe across state-of-the-art foundation models.",
        "key_takeaways": [
            "Controls Step Magnitude: Learning rate (η) scales how far parameters move per iteration.",
            "Step Size = η × Slope: The actual distance moved naturally shrinks as the loss curve flattens near the minimum.",
            "Avoid The Extremes: Too small crawls into saddle points; too large violently overshoots and explodes into NaNs.",
            "Use Schedulers & LR Finder: Employ Linear Warmup for deep networks, Cosine Decay, and the LR Finder to locate the optimal rate."
        ],
        "definition_bullets": [
            "Learning Rate (η): The foundational scalar hyperparameter that controls the step magnitude per iteration during gradient descent.",
            "Step Size: The actual numerical change applied to a parameter (η · ||∇L||), combining learning rate and gradient steepness."
        ],
        "types_header": "Learning Rate Schedulers in Practice",
        "types_badge": "Dynamic Training Strategies",
        "quick_types": [
            {
                "type": "Constant Learning Rate",
                "definition": "Keeps η fixed from the first step to the last; simple and reliable for linear regression and shallow models.",
                "looks_like": "optimizer = Adam(lr=0.001)"
            },
            {
                "type": "Step Decay (ReduceLROnPlateau)",
                "definition": "Divides η by 10 (e.g. 0.1 → 0.01) whenever validation loss stops improving for a set patience window (e.g. 3 epochs).",
                "looks_like": "ReduceLROnPlateau(patience=3, factor=0.1)"
            },
            {
                "type": "Cosine Annealing",
                "definition": "Lowers η following a smooth cosine curve, gently guiding the learning rate down to near zero by the final epoch.",
                "looks_like": "CosineAnnealingLR(T_max=epochs)"
            },
            {
                "type": "Linear Warmup + Cosine Decay",
                "definition": "Ramps η up from near zero over early warmup steps to protect random weights, then smoothly decays; standard for Transformers.",
                "looks_like": "get_cosine_schedule_with_warmup()"
            }
        ],
        "connected_logic": [
            {
                "title": "Leslie Smith's LR Range Test (The LR Finder)",
                "content": "• Instead of guessing blindly, train the model for 1 single epoch while exponentially increasing η from 10⁻⁷ to 10.0 on each batch.\n• Plot Loss vs. Learning Rate on a log scale.\n• The Golden Rule: Select the learning rate at the steepest downward slope—typically one order of magnitude before the minimum point."
            },
            {
                "title": "Loss Explosion & Debugging NaNs",
                "content": "• When learning rate is too large, weight updates take giant jumps that land in steep loss regions, causing gradients to double on each step.\n• Eventually numbers exceed 32-bit floating point limits (~3.4 × 10³⁸), printing 'Loss: NaN'.\n• Solution: Lower η and add Gradient Clipping (torch.nn.utils.clip_grad_norm_) to cap maximum gradient norms."
            },
            {
                "title": "Learning Rate in Adaptive Optimizers (Adam vs. SGD)",
                "content": "• In standard SGD, all weights share the exact same global learning rate η.\n• In Adam and RMSProp, the optimizer maintains running averages of past gradients (moments) to give frequently updated weights smaller steps and rarely updated weights larger steps.\n• Because of this automatic scaling, Adam's default rate of 0.001 works well across a wide variety of tasks."
            },
            {
                "title": "The Linear Scaling Rule for Multi-GPU Training",
                "content": "• When scaling training from 1 GPU to 8 GPUs with an 8x larger total batch size, the number of updates per epoch decreases by 8x.\n• To compensate, the Linear Scaling Rule recommends multiplying the learning rate by 8 (η_new = k × η_old).\n• This ensures weights traverse the same total distance per epoch as single-GPU training."
            }
        ]
    }

    # 2. CLEAN BATCH SIZES
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
                "term": "Batch Size (B)",
                "what_is_it": "• The number of training samples grouped together in a single forward and backward pass.\n• Directly dictates how many weight updates occur per epoch (N / B).",
                "analogy": "A chef cooking meals in small batches of 4 to 8 dishes instead of cooking 1 French fry at a time or preparing 500 meals simultaneously.",
                "why_it_matters": "Determines GPU memory consumption, training speed, and generalization accuracy."
            },
            {
                "term": "Gradient Noise & Stochasticity",
                "what_is_it": "• Because a mini-batch is only a small slice of the full dataset, its gradient has slight random fluctuation.\n• This beneficial noise acts like tiny tremors that shake weights out of narrow, fragile pits and guide them into wide valleys.",
                "analogy": "Gently shaking a jar of marbles: the rattling causes them to settle neatly into the widest, most stable gaps at the bottom.",
                "why_it_matters": "The key reason mini-batches generalize better to unseen test data than gigantic full-dataset batches."
            },
            {
                "term": "Hardware Warp Alignment (Powers of 2)",
                "what_is_it": "• Modern GPU architectures (like NVIDIA Tensor Cores) execute instructions in groups of 32 parallel threads (warps).\n• Setting batch size to powers of 2 (32, 64, 128, 256) aligns memory access perfectly with GPU hardware, running significantly faster than odd numbers like 61.",
                "analogy": "Packing rectangular boxes into a shipping container: standard shapes fill the space with zero wasted volume, whereas irregular boxes leave empty gaps.",
                "why_it_matters": "Maximizes memory bus bandwidth and prevents idle GPU processor cores during matrix operations."
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
        "pitfalls": "Common Mistakes to Avoid:\n1. Assuming larger batches always make better models: Gigantic batches (B = 10,000+) overfit to razor-sharp minima and degrade test accuracy.\n2. Causing Out-Of-Memory (OOM) crashes: Pushing batch size beyond GPU VRAM limits causes instant fatal crashes; use Gradient Accumulation to simulate large batches instead.\n3. Using non-binary batch sizes: Setting B = 61 or 100 underutilizes GPU warps; always choose powers of 2 (32, 64, 128, 256) for top hardware throughput.\n4. Forgetting shuffle=True in DataLoader: Without randomizing sample order every epoch, cyclical order patterns bias the gradients and cause loss oscillations.\n5. Confusing optimizer name with batch size: Calling an algorithm 'SGD' in PyTorch refers to the update rule, even when running with mini-batches of 64 or 128.",
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
                "title": "Sharp Minima vs. Flat Minima (The Generalization Secret)",
                "content": "• Huge batches (B = 10,000+) compute ultra-precise gradients that drop models into narrow, steep crevices (Sharp Minima).\n• When real-world test distributions shift slightly, loss on sharp minima explodes!\n• Mini-batches (B = 32 to 256) generate mild stochastic noise that bumps weights into wide, flat basins (Flat Minima), ensuring robust real-world performance."
            },
            {
                "title": "GPU Memory Sizing & Fixing Out-Of-Memory (OOM)",
                "content": "• During the forward pass, intermediate activations for all B samples must be stored in GPU VRAM for the backward pass.\n• If batch size is too large, the GPU runs out of memory (CUDA OOM crash).\n• Solution: Halve the batch size or enable mixed precision (torch.cuda.amp.autocast()) to cut activation memory in half."
            },
            {
                "title": "The PyTorch DataLoader Pipeline",
                "content": "• In code: DataLoader(dataset, batch_size=64, shuffle=True, pin_memory=True, num_workers=4).\n• shuffle=True randomizes row order every epoch to prevent cyclical gradient resonance.\n• num_workers=4 uses background CPU processes to load and preprocess batch N+1 while the GPU trains on batch N."
            },
            {
                "title": "The SGD Optimizer vs. Batch Size Confusion",
                "content": "• In textbooks, 'Pure SGD' strictly means batch_size=1.\n• In production code, torch.optim.SGD is simply the name of the mathematical update rule (w = w - η · ∇L), which is almost always executed with mini-batches of 64 or 128.\n• The optimizer algorithm and the batch size are two completely separate settings."
            }
        ]
    }

    # 3. CLEAN EPOCHS
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
                "term": "The Forward and Backward Pass",
                "what_is_it": "• Forward Pass: Input (X) flows through layers to generate predictions (ŷ) and compute the loss penalty.\n• Backward Pass: Backpropagation computes gradients (loss.backward()) and updates weights (optimizer.step()).\n• Repeating these two passes across all batches in the dataset completes one epoch.",
                "analogy": "A student taking a practice quiz (forward pass), grading the mistakes with the answer key (backward pass), and studying the corrections.",
                "why_it_matters": "The core mechanical cycle executed inside every deep learning training loop."
            },
            {
                "term": "The Training vs. Validation Loss Gap",
                "what_is_it": "• Training loss measures errors on examples the model is actively learning from.\n• Validation loss measures errors on hold-out examples the model has never seen before.\n• When training loss continues falling but validation loss starts rising, the generalization gap has widened into overfitting.",
                "analogy": "A student who scores 100% on homework by memorizing questions, but scores 60% on the final exam with slightly altered numbers.",
                "why_it_matters": "The primary diagnostic tool used to know exactly when to stop training."
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
                "type": "Web-Scale LLM Regime (1 to 2 Epochs)",
                "definition": "Trained across massive web-scale corpora (trillions of tokens); 1 to 2 passes prevent verbatim memorization and maximize knowledge breadth.",
                "looks_like": "GPT-4 / LLaMA Pretraining"
            }
        ],
        "connected_logic": [
            {
                "title": "Early Stopping & Patience in Production",
                "content": "• Rather than guessing how many epochs to train for, Early Stopping monitors validation loss at the end of each epoch.\n• Patience defines the tolerance window (e.g., 5 epochs) to wait without validation improvement before terminating training.\n• This prevents wasted GPU hours and eliminates manual guesswork on training duration."
            },
            {
                "title": "Model Checkpointing (Saving the Best Epoch)",
                "content": "• Even with early stopping, the weights at the final epoch are already slightly overfitted.\n• Model Checkpointing (e.g. ModelCheckpoint(save_best_only=True)) saves the weights to disk every time validation loss hits a new all-time low.\n• When training completes, the pipeline automatically reloads this optimal checkpoint for deployment."
            },
            {
                "title": "Data Shuffling Between Epochs",
                "content": "• In PyTorch, DataLoader(shuffle=True) reshuffles the sequence of examples at the start of every new epoch.\n• Without shuffling, the model sees identical batches in identical order, causing it to memorize sequence correlations and oscillate along cyclical gradient paths."
            },
            {
                "title": "Why Vision Models Need 100+ Epochs but LLMs Use 1-2",
                "content": "• Vision datasets (like ImageNet with ~1.2M images) are relatively small, requiring 90 to 300 epochs for convolutional or attention filters to converge on visual features.\n• LLMs are trained on trillions of tokens (the entire web). At that immense scale, 1 to 2 passes provide enough gradient steps, while repeating text tokens causes verbatim memorization and hallucinations."
            }
        ]
    }

    # UPDATE concepts.json
    for c in concepts:
        if c.get("id") == "concept_learning_rate":
            c.update(lr_data)
        elif c.get("id") == "concept_batch_sizes":
            c.update(batch_data)
        elif c.get("id") == "concept_epochs":
            c.update(epoch_data)

    with open("src/data/concepts.json", "w", encoding="utf-8") as f:
        json.dump(concepts, f, indent=2, ensure_ascii=False)
    print("Updated concepts.json")

    # UPDATE all_concepts.json
    for c in all_concepts:
        if c.get("id") == "concept_learning_rate":
            c.update(lr_data)
        elif c.get("id") == "concept_batch_sizes":
            c.update(batch_data)
        elif c.get("id") == "concept_epochs":
            c.update(epoch_data)

    with open("scripts/data_sources/all_concepts.json", "w", encoding="utf-8") as f:
        json.dump(all_concepts, f, indent=2, ensure_ascii=False)
    print("Updated all_concepts.json")

    # UPDATE concepts_ml.py
    # Replace lr
    pattern_lr = r'\{\s*"id":\s*"concept_learning_rate".*?\},(?=\s*\{\s*"id":\s*"concept_batch_sizes")'
    match_lr = re.search(pattern_lr, py_content, re.DOTALL)
    if match_lr:
        lines_lr = json.dumps(lr_data, indent=4, ensure_ascii=False).splitlines()
        indented_lr = "\n".join("    " + line for line in lines_lr) + ","
        py_content = py_content[:match_lr.start()] + indented_lr + py_content[match_lr.end():]
        print("Updated concept_learning_rate in concepts_ml.py")

    # Replace batch
    pattern_batch = r'\{\s*"id":\s*"concept_batch_sizes".*?\},(?=\s*\{\s*"id":\s*"concept_epochs")'
    match_batch = re.search(pattern_batch, py_content, re.DOTALL)
    if match_batch:
        lines_batch = json.dumps(batch_data, indent=4, ensure_ascii=False).splitlines()
        indented_batch = "\n".join("    " + line for line in lines_batch) + ","
        py_content = py_content[:match_batch.start()] + indented_batch + py_content[match_batch.end():]
        print("Updated concept_batch_sizes in concepts_ml.py")

    # Replace epochs
    pattern_epochs = r'\{\s*"id":\s*"concept_epochs".*?\},(?=\s*\{\s*"id":\s*"concept_convergence")'
    match_epochs = re.search(pattern_epochs, py_content, re.DOTALL)
    if match_epochs:
        lines_epochs = json.dumps(epoch_data, indent=4, ensure_ascii=False).splitlines()
        indented_epochs = "\n".join("    " + line for line in lines_epochs) + ","
        py_content = py_content[:match_epochs.start()] + indented_epochs + py_content[match_epochs.end():]
        print("Updated concept_epochs in concepts_ml.py")

    with open("scripts/data_sources/concepts_ml.py", "w", encoding="utf-8") as f:
        f.write(py_content)
    print("Wrote concepts_ml.py")

if __name__ == "__main__":
    update_all()
