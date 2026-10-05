"""Category 2: Deep Learning Foundations & Training Dynamics (Questions 26-50)"""

CAT2_QUESTIONS = [
    {
        "id": "dl_26",
        "category": "dl",
        "category_label": "Deep Learning & Optimization",
        "difficulty": "Mid / Senior",
        "company_tags": ["Google", "Meta", "OpenAI"],
        "question": "Why do gradients vanish or explode in deep feedforward networks, and how do Residual Connections (ResNets) mathematically solve the vanishing gradient problem?",
        "answer": """**1. Vanishing Gradients via Chain Rule:**
In an $L$-layer network, the gradient of loss with respect to early layer activations $a^{[1]}$ is:
$$\\frac{\\partial \\mathcal{L}}{\\partial a^{[1]}} = \\frac{\\partial \\mathcal{L}}{\\partial a^{[L]}} \\prod_{l=2}^L W^{[l] T} \\cdot \\text{diag}(\\sigma'(z^{[l]}))$$
If the spectral norm of weights $\\|W\\| < 1$ or activation derivatives $\\sigma'(z) < 1$ (e.g. sigmoid $\\le 0.25$, tanh $\\le 1.0$), the product of $L$ small fractions decays exponentially to zero ($0.25^{20} \\approx 10^{-12}$). Early layers receive zero gradient updates.

**2. ResNet Mathematical Solution:**
A residual block defines: $y = x + F(x, W)$.
Taking the derivative of loss $\\mathcal{L}$ with respect to input $x$:
$$\\frac{\\partial \\mathcal{L}}{\\partial x} = \\frac{\\partial \\mathcal{L}}{\\partial y} \\cdot \\frac{\\partial y}{\\partial x} = \\frac{\\partial \\mathcal{L}}{\\partial y} \\left( I + \\frac{\\partial F}{\\partial x} \\right) = \\frac{\\partial \\mathcal{L}}{\\partial y} + \\frac{\\partial \\mathcal{L}}{\\partial y} \\frac{\\partial F}{\\partial x}$$
- Notice the **identity term $+ I$**!
- Even if the gradient through the non-linear residual branch $\\frac{\\partial F}{\\partial x} \\approx 0$, the gradient directly backpropagates unimpeded through the skip connection: $\\frac{\\partial \\mathcal{L}}{\\partial x} = \\frac{\\partial \\mathcal{L}}{\\partial y}$.
- Gradients flow back from layer $L$ to layer $1$ without exponential decay, enabling networks with 100+ layers.""",
        "tip": "Write out $\\frac{\\partial y}{\\partial x} = I + \\frac{\\partial F}{\\partial x}$ explicitly. That $+I$ term is what earned ResNet 180,000+ citations."
    },
    {
        "id": "dl_27",
        "category": "dl",
        "category_label": "Deep Learning & Optimization",
        "difficulty": "Mid / Senior",
        "company_tags": ["Apple", "Tesla", "Microsoft"],
        "question": "Compare Batch Normalization, Layer Normalization, and Group Normalization. Why does BatchNorm fail on small batch sizes, and why do Transformers use LayerNorm?",
        "answer": """**1. Dimensional Normalization Slices (Tensor shape $[N, C, H, W]$ or $[B, S, D]$):**
- **Batch Normalization (BN):** Normalizes across the **batch dimension $N$** for each channel independently: $\\mu_c = \\frac{1}{N \\cdot H \\cdot W} \\sum x$.
- **Layer Normalization (LN):** Normalizes across the **channel / feature dimension $C$** for each sample independently: $\\mu_n = \\frac{1}{C} \\sum x$.
- **Group Normalization (GN):** Divides channels into $G$ groups and normalizes within each group per sample.

**2. Why BatchNorm Fails on Small Batches:**
BN computes empirical mini-batch mean and variance. When batch size $N \\le 4$, the sample variance is noisy and inaccurate, causing training instability and huge discrepancy with inference running statistics.

**3. Why Transformers Use LayerNorm:**
- In NLP, sequences vary in length across batches. BN requires padding masks and struggles with variable length sequences.
- In distributed LLM training, batch size per GPU is often tiny (1 to 4) due to memory constraints, where BN completely breaks down.
- LayerNorm computes statistics independently per token vector across embedding dimensions $D$, with zero dependence on other samples in the batch.""",
        "tip": "Mention that BatchNorm requires tracking running mean and variance during training for inference, whereas LayerNorm uses the exact same computation in training and inference."
    },
    {
        "id": "dl_28",
        "category": "dl",
        "category_label": "Deep Learning & Optimization",
        "difficulty": "Senior",
        "company_tags": ["Meta", "OpenAI", "Anthropic"],
        "question": "What is the difference between Post-LayerNorm and Pre-LayerNorm in Transformers? Why did modern LLMs (LLaMA, GPT-3, Mistral) switch to Pre-LN / RMSNorm?",
        "answer": """**1. Formulations:**
- **Post-LN (Original Attention is All You Need):**
  $$x_{t+1} = \\text{LayerNorm}(x_t + \\text{Sublayer}(x_t))$$
- **Pre-LN (Modern LLMs):**
  $$x_{t+1} = x_t + \\text{Sublayer}(\\text{LayerNorm}(x_t))$$

**2. The Post-LN Vanishing/Exploding Gradient Problem:**
In Post-LN, the residual stream passes through LayerNorm at every block.
As depth increases, gradients passing through the normalization scale inversely with depth ($O(1/\\sqrt{L})$), causing severe gradient vanishing or explosion during the initial training steps.
- Post-LN strictly requires a delicate **learning rate warmup** to avoid divergence.

**3. Pre-LN Advantages:**
In Pre-LN, the identity skip connection $x_{t+1} = x_t + \\dots$ remains completely unperturbed. Gradients flow directly through the residual backbone without attenuation.
- Models train reliably without fragile warmup schedules and scale smoothly to 100B+ parameters.

**4. RMSNorm (Root Mean Square Normalization):**
Modern LLMs replace Pre-LN with RMSNorm:
$$\\bar{x}_i = \\frac{x_i}{\\sqrt{\\frac{1}{d}\\sum_{j=1}^d x_j^2 + \\epsilon}} \\cdot \\gamma_i$$
Omits mean centering $\\mu$, reducing GPU memory access overhead by 10-25% without sacrificing perplexity.""",
        "tip": "Explain that RMSNorm's speedup comes from eliminating the need to compute and subtract the mean $\\mu$."
    },
    {
        "id": "dl_29",
        "category": "dl",
        "category_label": "Deep Learning & Optimization",
        "difficulty": "Mid / Senior",
        "company_tags": ["Google", "NVIDIA", "Amazon"],
        "question": "Why does zero-initialization fail for hidden neural network layers? Derive the intuition behind Xavier/Glorot and He/Kaiming initialization.",
        "answer": """**1. Why Zero-Initialization Fails (Symmetry Problem):**
If all weights $W_{ij} = 0$, every neuron in layer $l$ computes the exact same activation: $a_j^{[1]} = \\sigma(0)$.
During backpropagation, all neurons receive identical gradients: $\\frac{\\partial \\mathcal{L}}{\\partial w_{ij}} = \\frac{\\partial \\mathcal{L}}{\\partial a_j} \\sigma'(0) x_i$.
All hidden neurons evolve identically throughout training, reducing an $N$-neuron layer to a single effective neuron.

**2. Xavier / Glorot Initialization (For Tanh / Sigmoid):**
Goal: Keep variance of activations and gradients constant across layers: $\\text{Var}(y) = \\text{Var}(x)$.
For linear layer $y = \\sum_{i=1}^{n_{in}} w_i x_i$:
$$\\text{Var}(y) = n_{in} \\cdot \\text{Var}(w) \\cdot \\text{Var}(x)$$
To enforce $\\text{Var}(y) = \\text{Var}(x)$, we need $\\text{Var}(w) = \\frac{1}{n_{in}}$.
Balancing forward and backward pass ($n_{out}$):
$$\\text{Var}(w) = \\frac{2}{n_{in} + n_{out}}, \\quad W \\sim \\mathcal{N}\\left(0, \\frac{2}{n_{in} + n_{out}}\\right)$$

**3. He / Kaiming Initialization (For ReLU):**
ReLU sets negative values to zero, halving the variance: $\\mathbb{E}[\\text{ReLU}(z)^2] = \\frac{1}{2} \\text{Var}(z)$.
To counteract this $50\\%$ variance loss, weights must have twice the variance:
$$\\text{Var}(w) = \\frac{2}{n_{in}}, \\quad W \\sim \\mathcal{N}\\left(0, \\frac{2}{n_{in}}\\right)$$""",
        "tip": "State clearly: Use Xavier for Sigmoid/Tanh, and He/Kaiming for ReLU/GELU."
    },
    {
        "id": "dl_30",
        "category": "dl",
        "category_label": "Deep Learning & Optimization",
        "difficulty": "Senior / Staff",
        "company_tags": ["OpenAI", "Meta", "Google DeepMind"],
        "question": "What was the fundamental bug in the original Adam optimizer when using L2 Regularization, and how did AdamW resolve it via Decoupled Weight Decay?",
        "answer": """**1. The Original Adam L2 Flaw:**
In standard SGD, adding L2 regularization $\\frac{1}{2}\\lambda w^2$ is mathematically equivalent to weight decay:
$$\\nabla \\tilde{\\mathcal{L}} = \\nabla \\mathcal{L} + \\lambda w \\implies w_{t+1} = w_t - \\eta (\\nabla \\mathcal{L} + \\lambda w_t) = (1 - \\eta \\lambda)w_t - \\eta \\nabla \\mathcal{L}$$
However, in **Adam**, L2 penalty was added directly to the gradient before computing adaptive moments:
$$g_t = \\nabla \\mathcal{L} + \\lambda w_t, \\quad v_t = \\beta_2 v_{t-1} + (1 - \\beta_2) g_t^2, \\quad w_{t+1} = w_t - \\frac{\\eta}{\\sqrt{v_t} + \\epsilon} m_t$$
- When a parameter has large historical gradients, $v_t$ is large. The effective weight decay becomes $\\frac{\\eta \\lambda}{\\sqrt{v_t}}$, so its weights are **barely decayed**!
- When a parameter has small or sparse gradients, $v_t$ is tiny, meaning it receives an **enormously strong weight decay penalty**.
- L2 regularization became coupled to gradient scales, ruining generalization.

**2. AdamW Solution (Loshchilov & Hutter, 2017):**
Decouple weight decay from the gradient updates entirely:
1. Compute gradient $g_t = \\nabla \\mathcal{L}$ (pure loss, no $\\lambda$).
2. Compute moments $m_t$ and $v_t$ using only $g_t$.
3. Update parameter by subtracting adaptive gradient AND direct proportional weight decay:
$$w_{t+1} = w_t - \\eta \\lambda w_t - \\frac{\\eta}{\\sqrt{\\hat{v}_t} + \\epsilon} \\hat{m}_t$$
Every weight decays uniformly at rate $\\eta \\lambda$ regardless of its gradient magnitude.""",
        "tip": "Explain that AdamW is why modern Transformers generalize as effectively as SGD with momentum."
    },
    {
        "id": "dl_31",
        "category": "dl",
        "category_label": "Deep Learning & Optimization",
        "difficulty": "Junior / Mid",
        "company_tags": ["Amazon", "Meta", "Apple"],
        "question": "How does Dropout work during training versus inference? What is Inverted Dropout, and why is it standard?",
        "answer": """**1. Dropout Mechanism:**
During training, each neuron is independently zeroed out with probability $p$ (or kept with probability $q = 1-p$) by applying a Bernoulli mask: $a_{drop} = a \\odot m$, where $m_j \\sim \\text{Bernoulli}(1-p)$.
- Prevents co-adaptation of features; forces the network to learn redundant, robust representations.

**2. Standard Dropout at Test Time:**
At test time, all neurons are active. To match the expected activation magnitude during training ($\\mathbb{E}[a_{drop}] = (1-p)a$), the output must be scaled by $(1-p)$ at inference: $a_{test} = (1-p) a$.

**3. Inverted Dropout (Modern Standard):**
Instead of scaling at test time, we scale activations **during training** by $\\frac{1}{1-p}$:
$$a_{train} = \\frac{a \\odot m}{1 - p}$$
- **Advantage:** At inference time, Dropout becomes an absolute no-op ($a_{test} = a$). Zero additional multiplications or inference latency overhead.""",
        "tip": "Highlight that Inverted Dropout eliminates all test-time code modifications, saving inference FLOPs."
    },
    {
        "id": "dl_32",
        "category": "dl",
        "category_label": "Deep Learning & Optimization",
        "difficulty": "Mid",
        "company_tags": ["Anthropic", "OpenAI", "Google"],
        "question": "What is the mathematical formulation of Softmax with Temperature $T$? What happens to the output distribution as $T \\to 0$ and $T \\to \\infty$?",
        "answer": """**1. Mathematical Formula:**
$$P(y = i | z) = \\frac{\\exp(z_i / T)}{\\sum_{j=1}^K \\exp(z_j / T)}$$
where $z_i$ are raw model logits and $T > 0$ is the temperature scalar.

**2. As $T \\to 0$ (Argmax / Greedy Sampling):**
As $T \\to 0^+$, the difference between the maximum logit and all other logits is scaled to infinity:
$$\\lim_{T \\to 0} P(y=i | z) = \\begin{cases} 1 & \\text{if } z_i = \\max_j(z_j) \\\\ 0 & \\text{otherwise} \\end{cases}$$
The distribution collapses into a deterministic one-hot vector (pure greedy argmax).

**3. As $T \\to \\infty$ (Uniform Random Sampling):**
As $T \\to \\infty$, $z_i / T \\to 0$, so $\\exp(z_i / T) \\to 1$:
$$\\lim_{T \\to \\infty} P(y=i | z) = \\frac{1}{K}$$
The distribution becomes completely flat (maximum entropy uniform distribution). Every token has equal probability.""",
        "tip": "In LLM generation: lower temperature ($0.1-0.3$) for factual/code tasks; higher temperature ($0.7-1.0$) for creative tasks."
    },
    {
        "id": "dl_33",
        "category": "dl",
        "category_label": "Deep Learning & Optimization",
        "difficulty": "Mid / Senior",
        "company_tags": ["Tesla", "Waymo", "Apple"],
        "question": "How do you calculate the Receptive Field of a Convolutional Neural Network? How do kernel size, stride, and dilation affect it?",
        "answer": """**1. Receptive Field Formula (Recursive):**
Let $RF_{l-1}$ be the receptive field of layer $l-1$. The receptive field of layer $l$ is:
$$RF_l = RF_{l-1} + (k_l - 1) \\cdot J_{l-1}$$
where $k_l$ is the kernel size, and $J_{l-1}$ is the cumulative **jump** (effective stride product of all prior layers):
$$J_l = J_{l-1} \\cdot s_l, \\quad J_0 = 1$$

**2. Effect of Parameters:**
- **Kernel Size ($k$):** Larger kernels expand RF linearly by $(k - 1) \\cdot J$.
- **Stride ($s$):** Stride $>1$ doubles or triples the jump $J_l$, causing all subsequent layers to expand RF exponentially faster.
- **Dilated (Atrous) Convolutions:** Inserts $d - 1$ spaces between kernel elements. Effective kernel size becomes:
  $$k' = k + (k - 1)(d - 1)$$
  Allows exponential expansion of receptive field with **zero increase in parameter count or FLOPs**.""",
        "tip": "Explain that dilated convolutions are standard in segmentation (DeepLab) and audio generation (WaveNet) for broad context without downsampling."
    },
    {
        "id": "dl_34",
        "category": "dl",
        "category_label": "Deep Learning & Optimization",
        "difficulty": "Mid",
        "company_tags": ["Amazon", "Bloomberg", "Google"],
        "question": "Why do standard Recurrent Neural Networks (RNNs) suffer from vanishing/exploding gradients, and how do LSTM gates regulate information flow?",
        "answer": """**1. Standard RNN Instability:**
Hidden state: $h_t = \\tanh(W_{hh} h_{t-1} + W_{xh} x_t)$.
Gradient over $T$ timesteps involves $\\prod_{t=1}^T W_{hh}^T \\text{diag}(1 - h_t^2)$. Repeated multiplication by $W_{hh}$ causes exponential decay (vanishing) or exponential growth (explosion) over long sequences.

**2. LSTM Architecture:**
Maintains an uninterrupted **Cell State highway ($C_t$)** governed by additive updates:
1. **Forget Gate:** $f_t = \\sigma(W_f [h_{t-1}, x_t] + b_f)$ (What fraction of old memory to discard, $0$ to $1$).
2. **Input Gate:** $i_t = \\sigma(W_i [h_{t-1}, x_t] + b_i)$ and candidate memory $\\tilde{C}_t = \\tanh(W_c [h_{t-1}, x_t] + b_c)$.
3. **Cell State Update:** $C_t = f_t \\odot C_{t-1} + i_t \\odot \\tilde{C}_t$ (Additive linear update prevents vanishing gradients!).
4. **Output Gate:** $o_t = \\sigma(W_o [h_{t-1}, x_t] + b_o)$, $h_t = o_t \\odot \\tanh(C_t)$.""",
        "tip": "Emphasize that the cell state update is linear and additive ($C_t = f_t C_{t-1} + \\dots$), allowing gradients to backpropagate across hundreds of timesteps without multiplicative decay."
    },
    {
        "id": "dl_35",
        "category": "dl",
        "category_label": "Deep Learning & Optimization",
        "difficulty": "Junior / Mid",
        "company_tags": ["OpenAI", "Meta"],
        "question": "What is Gradient Clipping, how is it computed, and why is it essential when training Transformers or RNNs?",
        "answer": """**1. The Exploding Gradient Hazard:**
In deep networks, sharp loss cliffs or recurrent unrolling can produce massive gradient norms ($\\|g\\| > 1000$). Taking a gradient descent step with such a vector shoots parameters far into high-loss regimes, causing `NaN` weights.

**2. Gradient Norm Clipping Formula (Pascanu et al., 2013):**
Compute total L2 norm of all gradients across all parameters:
$$\\|g\\|_2 = \\sqrt{\\sum_{p} \\|g_p\\|_2^2}$$
If $\\|g\\|_2 > \\text{threshold}$, scale all gradients proportionally:
$$g \\leftarrow g \\cdot \\frac{\\text{threshold}}{\\|g\\|_2}$$
- **Key Property:** Preserves the exact **directional angle** of the gradient vector while strictly bounding its maximum step length to `threshold` (typically 1.0).""",
        "tip": "Distinguish between clipping by norm (standard) and clipping by value ($\text{clamp}(g, -c, c)$), which distorts the gradient direction."
    },
    {
        "id": "dl_36",
        "category": "dl",
        "category_label": "Deep Learning & Optimization",
        "difficulty": "Mid",
        "company_tags": ["Google", "Anthropic"],
        "question": "Compare the vanishing gradient characteristics of Sigmoid, Tanh, ReLU, and GELU activation functions.",
        "answer": """- **Sigmoid:** $\\sigma(z) = \\frac{1}{1 + e^{-z}}$. Derivative $\\sigma'(z) = \\sigma(z)(1 - \\sigma(z)) \\le 0.25$. Max gradient is 0.25! Severe vanishing gradient in networks $>3$ layers. Not zero-centered.
- **Tanh:** $\\tanh(z) = \\frac{e^z - e^{-z}}{e^z + e^{-z}}$. Derivative $\\tanh'(z) = 1 - \\tanh^2(z) \\le 1.0$. Zero-centered, but still saturates at $\\pm 1$, causing vanishing gradients when $|z| > 3$.
- **ReLU:** $\\max(0, z)$. Derivative is $1$ for $z > 0$, and $0$ for $z < 0$. Eliminates vanishing gradients in positive regime; but suffers from the **Dead ReLU** problem if weights push inputs permanently negative.
- **GELU (Gaussian Error Linear Unit):** $x \\cdot \\Phi(x) = x P(X \\le x)$ where $X \\sim \\mathcal{N}(0, 1)$. Smooth, non-monotonic curve with negative curvature that permits small gradients for negative inputs, preventing dead neurons. Standard in modern LLMs.""",
        "tip": "Mention that Hendrycks & Gimpel (2016) motivated GELU as a stochastic regularization where inputs are randomly dropped depending on magnitude."
    },
    {
        "id": "dl_37",
        "category": "dl",
        "category_label": "Deep Learning & Optimization",
        "difficulty": "Senior / Staff",
        "company_tags": ["OpenAI", "Meta", "NVIDIA"],
        "question": "Explain the differences between Data Parallelism (DDP), Pipeline Parallelism (PP), and Tensor Parallelism (TP) for distributed LLM training.",
        "answer": """**1. Distributed Data Parallelism (DDP):**
- Replicates entire model on every GPU.
- Each GPU processes a distinct data shard; gradients are synchronized using `AllReduce`.
- Fails when model weights + optimizer states exceed single GPU VRAM.

**2. Tensor Parallelism (TP - Megatron-LM):**
- Splits individual weight matrices **within a layer** across GPUs.
- Linear layer $Y = X W$: split $W$ column-wise ($W = [W_1, W_2]$) in MLP layer 1, and row-wise in MLP layer 2 with `AllReduce`.
- Operates inside a single node across ultra-high-bandwidth NVLink ($900\\text{ GB/s}$) due to frequent per-layer communication.

**3. Pipeline Parallelism (PP - GPipe / Megatron):**
- Partitions layers **across nodes** (e.g. Layers 1-8 on Node 1, 9-16 on Node 2).
- Divides mini-batch into micro-batches to minimize pipeline bubbles. Lower communication frequency (only activation handoffs).""",
        "tip": "In 3D parallelism: TP within NVLink node, PP across nodes, and DP across pipeline replicas."
    },
    {
        "id": "dl_38",
        "category": "dl",
        "category_label": "Deep Learning & Optimization",
        "difficulty": "Senior / Staff",
        "company_tags": ["Microsoft", "NVIDIA", "Meta"],
        "question": "What is ZeRO (Zero Redundancy Optimizer) in DeepSpeed? Explain the memory reduction across Stage 1, Stage 2, and Stage 3.",
        "answer": """In mixed precision training, a 16-bit model with $\\Psi$ parameters requires:
- 16-bit weights ($2\\Psi$ bytes) + 16-bit gradients ($2\\Psi$ bytes) + FP32 master weights ($4\\Psi$ bytes) + Adam FP32 moments ($8\\Psi$ bytes) = **$16\\Psi$ bytes**.
For a 70B model, optimizer states alone take $16 \\times 70\\text{B} = 1.12\\text{ TB}$!

**ZeRO Memory Elimination Stages (across $N_d$ data parallel devices):**
- **ZeRO-1 (Optimizer State Partitioning):**
  Partitions the FP32 Adam states ($12\\Psi$ bytes) across $N_d$ GPUs.
  Memory: $4\\Psi + \\frac{12\\Psi}{N_d}$. (4x memory reduction with zero extra communication).
- **ZeRO-2 (Gradient Partitioning):**
  Partitions gradients ($2\\Psi$ bytes) as they are computed.
  Memory: $2\\Psi + \\frac{14\\Psi}{N_d}$. (8x reduction).
- **ZeRO-3 (Parameter Partitioning):**
  Partitions model parameters ($2\\Psi$ bytes) across all GPUs. Each GPU only holds its slice of weights, fetching other weights via `AllGather` on-demand just before the forward/backward pass.
  Memory: $\\frac{16\\Psi}{N_d}$ (Linear memory reduction). Allows training massive models without Tensor Parallelism.""",
        "tip": "Memorize the state memory distribution: Parameters (2B), Gradients (2B), Optimizer States (12B)."
    },
    {
        "id": "dl_39",
        "category": "dl",
        "category_label": "Deep Learning & Optimization",
        "difficulty": "Mid / Senior",
        "company_tags": ["NVIDIA", "Google", "OpenAI"],
        "question": "What is the difference between FP16 and BF16 in deep learning? Why did the industry transition from FP16 to BF16 for large model training?",
        "answer": """**1. Bit Formats:**
- **FP32:** 1 sign bit, 8 exponent bits, 23 mantissa (fraction) bits. Range $\\approx 10^{\\pm 38}$.
- **FP16 (IEEE Half):** 1 sign bit, 5 exponent bits, 10 mantissa bits. Range: $[6 \\times 10^{-5}, 65504]$.
- **BF16 (Bfloat16 - Brain Floating Point):** 1 sign bit, **8 exponent bits**, 7 mantissa bits. Range $\\approx 10^{\\pm 38}$ (same as FP32!).

**2. The FP16 Flaw (Underflow & Overflow):**
With only 5 exponent bits, FP16 has an extremely narrow dynamic range. In deep networks, gradients frequently underflow to zero ($< 6 \\times 10^{-5}$) or overflow to `NaN` ($> 65,504$).
- FP16 strictly requires dynamic loss scaling to shift gradients into range, which often destabilizes training.

**3. Why BF16 Dominated:**
BF16 preserves all 8 exponent bits of FP32. It matches FP32's dynamic range perfectly.
- Gradients never underflow or overflow.
- **Zero loss scaling required.** Plug-and-play stability for 100B+ LLM training on NVIDIA A100/H100 and Google TPUs.""",
        "tip": "State clearly that BF16 sacrifices precision (7 bits vs 10 bits) for dynamic range, which neural networks tolerate remarkably well."
    },
    {
        "id": "dl_40",
        "category": "dl",
        "category_label": "Deep Learning & Optimization",
        "difficulty": "Mid",
        "company_tags": ["Apple", "Amazon"],
        "question": "What is the difference between Polyak Momentum and Nesterov Accelerated Gradient (NAG)?",
        "answer": """**1. Classical Polyak Momentum:**
$$v_t = \\beta v_{t-1} + \\eta \\nabla f(\\theta_t), \\quad \\theta_{t+1} = \\theta_t - v_t$$
Computes gradient at current position $\\theta_t$, then steps in direction of accumulated velocity. Can overshoot minima on steep slopes.

**2. Nesterov Accelerated Gradient (Look-Ahead):**
$$v_t = \\beta v_{t-1} + \\eta \\nabla f(\\theta_t - \\beta v_{t-1}), \\quad \\theta_{t+1} = \\theta_t - v_t$$
- Evaluates the gradient not at the current position, but at the **predicted future position** $(\\theta_t - \\beta v_{t-1})$ after momentum is applied.
- Acts as a smart braking mechanism: if momentum is about to carry the model up a steep slope, the look-ahead gradient detects this in advance and applies corrective deceleration.
- Improves theoretical convergence rate on convex functions from $O(1/k)$ to $O(1/k^2)$.""",
        "tip": "Explain NAG using the analogy of a ball rolling down a hill looking ahead to slow down before an upward slope."
    },
    {
        "id": "dl_41",
        "category": "dl",
        "category_label": "Deep Learning & Optimization",
        "difficulty": "Junior / Mid",
        "company_tags": ["Meta", "Google"],
        "question": "What is the 'Dying ReLU' problem, what causes it, and how do Leaky ReLU, PReLU, and ELU prevent it?",
        "answer": """**1. The Dying ReLU Problem:**
ReLU is $f(z) = \\max(0, z)$. If a neuron receives an update with a large negative bias or massive gradient such that $w^T x + b < 0$ for all samples in the training set:
- Its output is permanently $0$.
- Its gradient is permanently $0$ ($\\frac{\\partial f}{\\partial z} = 0$).
The neuron enters an unrecoverable state where it can never update its weights again. Up to 20-50% of network capacity can silently die.

**2. Solutions:**
- **Leaky ReLU:** $f(z) = \\max(\\alpha z, z)$ with fixed slope $\\alpha = 0.01$. Keeps a small gradient in negative territory.
- **PReLU (Parametric ReLU):** $\\alpha$ is a learnable parameter optimized via backpropagation.
- **ELU (Exponential Linear Unit):** $f(z) = z$ if $z > 0$, else $\\alpha (e^z - 1)$. Smooth negative saturation brings mean activation closer to zero.""",
        "tip": "Mention lower learning rates and Xavier/He initialization as effective operational defenses against dying ReLUs."
    },
    {
        "id": "dl_42",
        "category": "dl",
        "category_label": "Deep Learning & Optimization",
        "difficulty": "Junior / Mid",
        "company_tags": ["Amazon", "Microsoft"],
        "question": "Why do deep neural networks require non-linear activation functions? What happens if you stack 100 linear layers without activations?",
        "answer": """**Proof by Matrix Composition:**
A linear layer computes $y = W x + b$.
Stacking two linear layers:
$$y = W_2 (W_1 x + b_1) + b_2 = (W_2 W_1) x + (W_2 b_1 + b_2) = W' x + b'$$
The product of two linear transformations $W_2 W_1$ is simply another linear transformation $W'$.
- Stacking 100 linear layers is mathematically identical to a **single linear regression layer**.
- The model can only draw linear decision boundaries (hyperplanes). It cannot solve XOR or model non-linear manifolds.
Non-linear activation functions break linearity, allowing neural networks to become Universal Function Approximators.""",
        "tip": "Cite the Cybenko Universal Approximation Theorem: non-linear activations allow 2-layer nets to approximate any continuous function."
    },
    {
        "id": "dl_43",
        "category": "dl",
        "category_label": "Deep Learning & Optimization",
        "difficulty": "Senior",
        "company_tags": ["Meta", "Google", "OpenAI"],
        "question": "What is Contrastive Learning? Explain the mathematical formulation of InfoNCE loss used in SimCLR and CLIP.",
        "answer": """**1. Concept:**
Self-supervised representation learning that pulls positive pairs (augmented views of same image, or paired image-text) close together in latent space while pushing negative pairs apart.

**2. InfoNCE Loss Formulation:**
For query representation $q$, positive match $k_+$, and $K$ negative samples $\\{k_i\\}$:
$$\\mathcal{L}_{q} = -\\log \\frac{\\exp(\\text{sim}(q, k_+) / \\tau)}{\\exp(\\text{sim}(q, k_+) / \\tau) + \\sum_{i=1}^K \\exp(\\text{sim}(q, k_i) / \\tau)}$$
where $\\text{sim}(u, v) = \\frac{u^T v}{\\|u\\| \\|v\\|}$ (cosine similarity) and $\\tau$ is the temperature parameter.

**3. Connection to Mutual Information:**
InfoNCE provides a lower bound on the mutual information $I(X; Y)$ between representations:
$$I(X; Y) \\ge \\log(K) - \\mathcal{L}_{InfoNCE}$$
Minimizing InfoNCE maximizes mutual information between paired views.""",
        "tip": "Highlight that CLIP uses a symmetric InfoNCE loss (cross-entropy across rows and columns of the $N \\times N$ batch similarity matrix)."
    },
    {
        "id": "dl_44",
        "category": "dl",
        "category_label": "Deep Learning & Optimization",
        "difficulty": "Mid / Senior",
        "company_tags": ["Apple", "Google", "Tesla"],
        "question": "How does Knowledge Distillation work? What is the mathematical difference between Soft Targets and Hard Targets?",
        "answer": """**1. Principle (Hinton et al., 2015):**
Transfers dark knowledge from a large, high-capacity Teacher network $T$ into a lightweight, fast Student network $S$.

**2. Loss Formulation:**
$$\\mathcal{L}_{KD} = (1 - \\alpha) \\mathcal{L}_{CE}(y, \\sigma(z_S)) + \\alpha T^2 \\cdot D_{KL}\\left(\\sigma(z_T / T) \\, \\Vert \\, \\sigma(z_S / T)\\right)$$
where $z_T, z_S$ are teacher/student logits, $T$ is temperature, and $\\alpha$ is blending weight.

**3. Soft Targets vs Hard Targets:**
- **Hard Targets:** One-hot vector $[0, 0, 1, 0]$ (e.g. BMW). Contains zero information about semantic similarity to other classes.
- **Soft Targets ($T > 1$):** Smoothed distribution $[0.001, 0.08, 0.85, 0.069]$ indicating that a BMW looks somewhat like an Audi (0.08) but nothing like a Garbage Truck ($10^{-5}$).
These dark knowledge inter-class probability ratios guide the student to generalize far better than ground truth labels alone.""",
        "tip": "Explain why the KL divergence is multiplied by $T^2$: as $T$ increases, gradient magnitudes scale as $1/T^2$; multiplying by $T^2$ balances loss contributions."
    },
    {
        "id": "dl_45",
        "category": "dl",
        "category_label": "Deep Learning & Optimization",
        "difficulty": "Mid / Senior",
        "company_tags": ["Google Research", "Apple", "Meta"],
        "question": "What is the architectural difference between Vision Transformers (ViT) and CNNs? Why does ViT perform worse than CNNs on small datasets, but outperforms them on massive datasets?",
        "answer": """**1. Architectural Differences:**
- **CNNs:** Process images via local receptive field sliding kernels. Hardwired inductive biases: **translation equivariance** and **spatial locality**.
- **ViT (Dosovitskiy et al., 2020):** Flattens images into $16 \\times 16$ non-overlapping patches, projects them into linear embeddings, adds position embeddings, and processes them with standard Transformer self-attention.

**2. Inductive Bias vs Dataset Scale:**
- **On Small Datasets (< 1M images):** CNNs outperform ViT. CNN's strong inductive biases guide optimization with minimal data. ViT has almost zero spatial inductive bias and overfits, wasting capacity learning basic pixel adjacencies.
- **On Massive Datasets (JFT-300M, ImageNet-21k):** ViT significantly outperforms CNNs. CNN's fixed local kernels cap model capacity. ViT's global self-attention learns complex long-range semantic patterns that transcend local convolutions.""",
        "tip": "Cite the classic quote: 'Transformers trade inductive bias for scalability when massive data is available.'"
    },
    {
        "id": "dl_46",
        "category": "dl",
        "category_label": "Deep Learning & Optimization",
        "difficulty": "Senior",
        "company_tags": ["DeepMind", "OpenAI"],
        "question": "What is Catastrophic Forgetting in continual learning? Explain 3 architectural or rehearsal techniques to mitigate it.",
        "answer": """**1. Catastrophic Forgetting (Stability-Plasticity Dilemma):**
When a neural network trained on Task A is subsequently trained on Task B, backpropagation updates weights to minimize Task B loss, overwriting the weight configurations critical for Task A. Performance on Task A collapses to near zero.

**2. Mitigation Strategies:**
1. **Replay Buffers / Experience Replay:** Store a small exemplar set of Task A data and interleave it into Task B training batches.
2. **Elastic Weight Consolidation (EWC):** Adds a quadratic penalty constraining parameters from moving away from Task A optimal weights $\\theta_A^*$, weighted by parameter importance via the **Fisher Information Matrix $F$**:
   $$\\mathcal{L}(\\theta) = \\mathcal{L}_B(\\theta) + \\sum_i \\frac{\\lambda}{2} F_i (\\theta_i - \\theta_{A, i}^*)^2$$
3. **Parameter Isolation / LoRA Adapters:** Freeze base model weights and train task-specific low-rank parameter adapters for each task.""",
        "tip": "Mention that human brains avoid catastrophic forgetting through hippocampal replay and complementary learning systems."
    },
    {
        "id": "dl_47",
        "category": "dl",
        "category_label": "Deep Learning & Optimization",
        "difficulty": "Mid / Senior",
        "company_tags": ["OpenAI", "Meta", "Google"],
        "question": "Why is Learning Rate Warmup critical when training deep Transformers with adaptive optimizers (Adam / AdamW)?",
        "answer": """**1. Instability at Step 0:**
At the start of training, model weights are randomly initialized.
In Adam:
$$v_t = \\beta_2 v_{t-1} + (1 - \\beta_2) g_t^2$$
During the first few steps, the second moment estimate $v_t$ is based on noisy, random gradients.
- Because $v_t$ is uncalibrated and tiny, the parameter update $\\frac{\\eta}{\\sqrt{v_t} + \\epsilon} m_t$ produces **excessively large, erratic weight updates**.
- This can knock the model out of good initialization basins and destroy the initial layer alignments.

**2. Learning Rate Warmup Remedy:**
Linearly ramps learning rate from $0$ to $\\eta_{\\max}$ over the first $k$ steps (e.g. 2,000 steps):
$$\\eta_t = \\eta_{\\max} \\cdot \\frac{t}{k}$$
Allows $v_t$ and $m_t$ to build stable, accurate running statistics using tiny steps before unleashing full gradient magnitudes.""",
        "tip": "Cite the RAdam (Rectified Adam) paper which analyzed how warmup stabilizes the variance of the adaptive learning rate."
    },
    {
        "id": "dl_48",
        "category": "dl",
        "category_label": "Deep Learning & Optimization",
        "difficulty": "Mid",
        "company_tags": ["Amazon", "Uber"],
        "question": "What is Truncated Backpropagation Through Time (TBPTT), and why is it required for long sequence training in RNNs?",
        "answer": """**1. Full BPTT Limitations:**
In a sequence of length $T=10,000$, standard BPTT unrolls the computation graph across all $10,000$ steps before backpropagating.
- Memory: Requires saving hidden states for all $10,000$ timesteps in GPU VRAM ($O(T)$ memory).
- Compute: Gradients vanish or explode over such extreme temporal horizons.

**2. Truncated BPTT:**
Divides sequence into chunks of length $k_1$ (forward pass) and backpropagates for $k_2$ steps:
1. Run forward pass through $k_1$ steps, carrying forward hidden state $h_t$.
2. Backpropagate error through only the last $k_2$ steps.
3. Decouples memory consumption from total sequence length to $O(k_2)$, allowing infinite streaming training.""",
        "tip": "Explain that TBPTT trades the ability to capture dependencies longer than $k_2$ steps for constant memory usage."
    },
    {
        "id": "dl_49",
        "category": "dl",
        "category_label": "Deep Learning & Optimization",
        "difficulty": "Senior / Staff",
        "company_tags": ["Google DeepMind", "OpenAI"],
        "question": "What is the Double Descent phenomenon in deep learning? How does it challenge the classical U-shaped Bias-Variance tradeoff curve?",
        "answer": """**1. Classical U-Shaped Trade-Off:**
Classical statistical theory states that as model capacity increases, test error decreases to an optimal point, then increases monotonically due to overfitting (U-curve).

**2. Double Descent (Belkin et al., 2019):**
As capacity increases past the **interpolation threshold** (where number of parameters equals number of training points and training error reaches 0):
1. **Under-parameterized regime:** Standard U-curve. Peak test error occurs right at the interpolation boundary where model fits training noise with extreme weight variance.
2. **Over-parameterized regime:** Past the threshold, test error **decreases again**, often achieving lower test error than the classical optimum!

**3. Why it happens:**
In highly overparameterized models, there are infinitely many interpolating solutions. Gradient descent acts as an implicit regularizer, selecting the interpolator with the **minimal L2 norm**, resulting in smooth function fits that generalize well.""",
        "tip": "Mention Epoch Double Descent (Nakkiran et al., 2019): double descent occurs across training epochs as well as model parameter counts."
    },
    {
        "id": "dl_50",
        "category": "dl",
        "category_label": "Deep Learning & Optimization",
        "difficulty": "Mid / Senior",
        "company_tags": ["NVIDIA", "Qualcomm", "Apple"],
        "question": "Compare Post-Training Quantization (PTQ) and Quantization-Aware Training (QAT). How does the Straight-Through Estimator (STE) make QAT differentiable?",
        "answer": """**1. Post-Training Quantization (PTQ):**
- Quantizes an already-trained FP32/FP16 model down to INT8/INT4 using a small calibration dataset.
- Extremely fast (minutes, no training required).
- Can cause noticeable perplexity/accuracy drops on aggressive 4-bit quantization.

**2. Quantization-Aware Training (QAT):**
- Simulates quantization noise **during training/fine-tuning**.
- Weights and activations are clamped and rounded in the forward pass to simulate integer precision, forcing the model to adapt and remain robust.

**3. Straight-Through Estimator (STE):**
The rounding operation $q = \\text{round}(x)$ is a step function with derivative $\\frac{dq}{dx} = 0$ almost everywhere, which blocks backpropagation gradients completely.
- **STE Solution:**
  - Forward pass: uses quantized values $q = \\text{round}(x)$.
  - Backward pass: pretends rounding was the identity function: $\\frac{\\partial \\mathcal{L}}{\\partial x} = \\frac{\\partial \\mathcal{L}}{\\partial q}$.
Allows gradients to flow through non-differentiable quantization operations.""",
        "tip": "Explain that QAT almost completely closes the accuracy gap between FP16 and INT4."
    }
]
