"""
Deep Learning Architectures Core Concepts (15 concepts):
- Computer Vision: CNNs & Vision Transformers (ViT)
- Sequence Models: RNNs, LSTMs & GRUs
- Generative Models & Diffusion (DDPM, Latent Diffusion, CFG)
"""

DL_ARCH_CONCEPTS = [
    # dl_vision
    {
        "id": "convolutions-kernels-stride-padding",
        "topic_id": "dl_vision",
        "topic_label": "Computer Vision: CNNs & Vision Transformers",
        "category": "dl",
        "category_label": "Deep Learning",
        "title": "Convolutions (Kernels, Stride & Padding)",
        "raw_sub": "Convolutions (Kernels, Filters, Stride, Padding)",
        "definition": "Convolution is a specialized linear operation where small learnable weight matrices (kernels/filters) slide across an input feature grid to compute dot products, creating spatially shift-invariant feature maps that detect local patterns regardless of position.",
        "formula": "$$S(i, j) = (I * K)(i, j) = \\sum_{m} \\sum_{n} I(i-m, j-n) K(m, n)$$ $$W_{out} = \\left\\lfloor \\frac{W_{in} - K + 2P}{S} \\right\\rfloor + 1$$",
        "formula_explanation": "$I$ is the input image tensor, $K$ is kernel size (e.g. $3 \\times 3$), $P$ is zero-padding count, and $S$ is stride step size.",
        "logic": "Convolutions enforce two critical visual inductive biases: local spatial connectivity (nearby pixels correlate strongly) and translation invariance (a cat in the corner has the same visual features as a cat in the center).",
        "example": "A $3 \\times 3$ Sobel edge-detection filter sliding over a $256 \\times 256$ photo highlights vertical sharp edges by taking positive weights on the right column and negative on the left."
    },
    {
        "id": "pooling-max-pooling",
        "topic_id": "dl_vision",
        "topic_label": "Computer Vision: CNNs & Vision Transformers",
        "category": "dl",
        "category_label": "Deep Learning",
        "title": "Pooling & Max Pooling",
        "raw_sub": "Pooling (Max Pooling to downsample spatial dimensions)",
        "definition": "Pooling downsamples spatial dimensions (height and width) of feature tensors independently across channels, reducing computational parameters for subsequent layers and providing slight translational distortion invariance.",
        "formula": "$$y_{i, j, c} = \\max_{(m, n) \\in \\Omega(i, j)} x_{m, n, c}$$",
        "formula_explanation": "$\\Omega(i, j)$ defines the local spatial pooling window (commonly $2 \\times 2$ with stride 2), which cuts spatial resolution in half while preserving the strongest activation feature in each quadrant.",
        "logic": "Max pooling extracts dominant activation presence regardless of sub-pixel positional shifts. Average pooling can also be used, particularly as Global Average Pooling (GAP) before final classification heads.",
        "example": "A $2 \\times 2$ max pooling window over $\\begin{bmatrix} 1 & 7 \\\\ 3 & 4 \\end{bmatrix}$ extracts $\\max(1, 7, 3, 4) = 7$."
    },
    {
        "id": "resnet-residual-connections",
        "topic_id": "dl_vision",
        "topic_label": "Computer Vision: CNNs & Vision Transformers",
        "category": "dl",
        "category_label": "Deep Learning",
        "title": "ResNet Skip & Residual Connections",
        "raw_sub": "ResNet Skip / Residual Connections (F(x) + x)",
        "definition": "Residual connections (He et al., 2015) introduce identity shortcut paths that bypass one or more transformation layers, reforming the layer task to learn a residual delta function $\\mathcal{F}(\\mathbf{x})$ instead of the full target function.",
        "formula": "$$\\mathbf{y} = \\mathcal{F}(\\mathbf{x}, \\{\\mathbf{W}_i\\}) + \\mathbf{x}, \\quad \\frac{\\partial \\mathcal{L}}{\\partial \\mathbf{x}} = \\frac{\\partial \\mathcal{L}}{\\partial \\mathbf{y}} \\left( \\frac{\\partial \\mathcal{F}}{\\partial \\mathbf{x}} + \\mathbf{I} \\right)$$",
        "formula_explanation": "$\\mathbf{x}$ is the unperturbed input tensor, $\\mathcal{F}$ is the learned residual sub-network, and $\\mathbf{I}$ is the identity matrix.",
        "logic": "The additive identity term $+ \\mathbf{I}$ guarantees an unimpeded gradient superhighway directly back through hundreds of layers, eradicating the vanishing gradient barrier and enabling networks with 100+ to 1,000+ layers.",
        "example": "If a layer needs to do nothing to preserve optimal features, it simply drives weights toward zero ($\\mathcal{F}(\\mathbf{x}) \\to 0$), trivially yielding the identity mapping $\\mathbf{y} = \\mathbf{x}$."
    },
    {
        "id": "object-detection-yolo",
        "topic_id": "dl_vision",
        "topic_label": "Computer Vision: CNNs & Vision Transformers",
        "category": "dl",
        "category_label": "Deep Learning",
        "title": "Object Detection & YOLO Architecture",
        "raw_sub": "Object Detection (YOLO bounding boxes and anchors)",
        "definition": "You Only Look Once (YOLO - Redmon et al., 2016) frames object detection as a single unified regression problem directly from full image pixels to bounding box coordinates $[x, y, w, h]$ and class probabilities across a spatial grid.",
        "formula": "$$\\text{IoU} = \\frac{\\text{Area of Overlap}}{\\text{Area of Union}} = \\frac{|B_{pred} \\cap B_{gt}|}{|B_{pred} \\cup B_{gt}|}, \\quad \\mathcal{L}_{box} = \\text{GIoU} \\text{ or } \\text{CIoU}$$",
        "formula_explanation": "Intersection over Union (IoU) measures bounding box overlap accuracy. Complete IoU (CIoU) loss penalizes centroid distance and aspect ratio discrepancy simultaneously.",
        "logic": "Prior region-proposal networks (like Faster R-CNN) ran two decoupled stages (propose candidate crops, then classify). YOLO processes the entire image in a single fast forward pass, achieving real-time 60+ FPS inference.",
        "example": "Autonomous driving video: YOLO detects pedestrian at $(x=340, y=210)$ with width 40, height 120 and 0.96 confidence, simultaneously tagging 15 other vehicles in 12ms."
    },
    {
        "id": "vision-transformers-vit",
        "topic_id": "dl_vision",
        "topic_label": "Computer Vision: CNNs & Vision Transformers",
        "category": "dl",
        "category_label": "Deep Learning",
        "title": "Vision Transformers (ViT)",
        "raw_sub": "Vision Transformers (ViT: Splitting images into visual token patches)",
        "definition": "Vision Transformer (Dosovitskiy et al., 2020) applies standard Transformer encoders directly to computer vision by chopping a 2D image into a sequence of non-overlapping $16 \\times 16$ pixel patches, linearly projecting each into a token vector, and processing them with global self-attention.",
        "formula": "$$\\mathbf{z}_0 = [\\mathbf{x}_{class}; \\mathbf{x}_p^1 \\mathbf{E}; \\mathbf{x}_p^2 \\mathbf{E}; \\dots; \\mathbf{x}_p^N \\mathbf{E}] + \\mathbf{E}_{pos}, \\quad \\mathbf{E} \\in \\mathbb{R}^{(P^2 \\cdot C) \\times D}$$",
        "formula_explanation": "$P=16$ is patch size, $N = \\frac{H \\cdot W}{P^2}$ is sequence length, $\\mathbf{E}$ is the linear patch projection matrix, and $\\mathbf{x}_{class}$ is a prepended learnable `[CLS]` token.",
        "logic": "ViT discards translation invariance and local inductive bias in favor of universal global attention. When pre-trained on massive datasets (JFT-300M, LAION), ViT significantly outperforms CNNs.",
        "example": "A $224 \\times 224$ image splits into $14 \\times 14 = 196$ patches of $16 \\times 16 \\times 3 = 768$ numbers each, which are treated exactly like a sentence of 196 words."
    },

    # dl_seq
    {
        "id": "recurrent-neural-networks-rnn",
        "topic_id": "dl_seq",
        "topic_label": "Sequence Models: RNNs, LSTMs & GRUs",
        "category": "dl",
        "category_label": "Deep Learning",
        "title": "Recurrent Neural Networks (RNN)",
        "raw_sub": "Recurrent Neural Networks (RNN & Hidden States)",
        "definition": "Recurrent Neural Networks process sequential inputs by maintaining an internal hidden state vector $\\mathbf{h}_t$ that acts as a recurrent memory buffer, updated at each time step based on current input $\\mathbf{x}_t$ and previous state $\\mathbf{h}_{t-1}$.",
        "formula": "$$\\mathbf{h}_t = \\tanh(\\mathbf{W}_{hh} \\mathbf{h}_{t-1} + \\mathbf{W}_{xh} \\mathbf{x}_t + \\mathbf{b}_h), \\quad \\mathbf{y}_t = \\text{Softmax}(\\mathbf{W}_{hy} \\mathbf{h}_t + \\mathbf{b}_y)$$",
        "formula_explanation": "$\\mathbf{W}_{hh}$ is the recurrent transition weight matrix shared across all time steps, and $\\mathbf{W}_{xh}$ projects the current time step's input.",
        "logic": "Parameter sharing across time allows RNNs to process arbitrary-length sequence inputs with a fixed parameter count, unlike feedforward networks.",
        "example": "Predicting the next character in a word: when processing character 'l' after seeing 'h', 'e', the hidden state holds context that 'l' should likely be followed by another 'l' (for 'hello')."
    },
    {
        "id": "vanishing-gradients-bptt",
        "topic_id": "dl_seq",
        "topic_label": "Sequence Models: RNNs, LSTMs & GRUs",
        "category": "dl",
        "category_label": "Deep Learning",
        "title": "Vanishing Gradients in BPTT",
        "raw_sub": "Vanishing Gradients across Long Time Horizons (BPTT)",
        "definition": "Backpropagation Through Time (BPTT) unrolls the recurrent network across $T$ chronological steps. Because the recurrent weight matrix $\\mathbf{W}_{hh}$ is repeatedly multiplied at every step, gradients vanish exponentially for dependencies longer than 10-20 steps.",
        "formula": "$$\\frac{\\partial \\mathcal{L}_T}{\\partial \\mathbf{h}_1} = \\frac{\\partial \\mathcal{L}_T}{\\partial \\mathbf{h}_T} \\prod_{t=2}^{T} \\frac{\\partial \\mathbf{h}_t}{\\partial \\mathbf{h}_{t-1}} = \\frac{\\partial \\mathcal{L}_T}{\\partial \\mathbf{h}_T} \\prod_{t=2}^{T} \\text{diag}(1 - \\tanh^2(\\mathbf{z}_t)) \\mathbf{W}_{hh}^T$$",
        "formula_explanation": "The product of $T-1$ matrices decays as $O(\\lambda_{max}^{T-1})$, where $\\lambda_{max} < 1$ causes signals from step 1 to completely vanish by step $T$.",
        "logic": "Standard RNNs cannot connect information separated by more than a few words (e.g. subject-verb agreement across long relative clauses), necessitating gated architectures like LSTM.",
        "example": "In sentence: 'The *clouds* in the dark overcast sky ... *were* pouring rain': plain RNN forgets that 'clouds' was plural by the time it reaches the verb 25 tokens later."
    },
    {
        "id": "lstm-architecture",
        "topic_id": "dl_seq",
        "topic_label": "Sequence Models: RNNs, LSTMs & GRUs",
        "category": "dl",
        "category_label": "Deep Learning",
        "title": "LSTM (Long Short-Term Memory)",
        "raw_sub": "LSTM (Forget, Input, and Output Gates + Cell State)",
        "definition": "LSTM (Hochreiter & Schmidhuber, 1997) introduces a dedicated linear Cell State $\\mathbf{c}_t$ regulated by three multiplicative gates: Forget Gate (what to discard), Input Gate (what new info to store), and Output Gate (what to expose to hidden state $\\mathbf{h}_t$).",
        "formula": "$$\\mathbf{f}_t = \\sigma(\\mathbf{W}_f [\\mathbf{h}_{t-1}, \\mathbf{x}_t] + \\mathbf{b}_f), \\quad \\mathbf{i}_t = \\sigma(\\mathbf{W}_i [\\mathbf{h}_{t-1}, \\mathbf{x}_t] + \\mathbf{b}_i)$$ $$\\tilde{\\mathbf{c}}_t = \\tanh(\\mathbf{W}_c [\\mathbf{h}_{t-1}, \\mathbf{x}_t] + \\mathbf{b}_c), \\quad \\mathbf{c}_t = \\mathbf{f}_t \\odot \\mathbf{c}_{t-1} + \\mathbf{i}_t \\odot \\tilde{\\mathbf{c}}_t, \\quad \\mathbf{h}_t = \\mathbf{o}_t \\odot \\tanh(\\mathbf{c}_t)$$",
        "formula_explanation": "$\\mathbf{f}_t \\odot \\mathbf{c}_{t-1}$ is an additive linear update where gradients can flow through time with derivative 1 when forget gate $\\mathbf{f}_t \\approx 1$.",
        "logic": "By relying on additive updates rather than continuous matrix multiplications, LSTM creates a constant error carousel that preserves long-term temporal dependencies across hundreds of steps.",
        "example": "Sentiment analysis of movie reviews: LSTM remembers early mentions of 'disappointing acting' through hundreds of intermediate plot descriptions to correctly classify the overall review as negative."
    },
    {
        "id": "gru-gated-recurrent-unit",
        "topic_id": "dl_seq",
        "topic_label": "Sequence Models: RNNs, LSTMs & GRUs",
        "category": "dl",
        "category_label": "Deep Learning",
        "title": "GRU (Gated Recurrent Unit)",
        "raw_sub": "GRU (Gated Recurrent Unit: Reset and Update Gates)",
        "definition": "GRU (Cho et al., 2014) is a streamlined variant of LSTM that merges the cell state and hidden state into a single vector, using only two gates: a Reset Gate (how to combine new input with past memory) and an Update Gate (how much past state to retain).",
        "formula": "$$\\mathbf{z}_t = \\sigma(\\mathbf{W}_z [\\mathbf{h}_{t-1}, \\mathbf{x}_t]), \\quad \\mathbf{r}_t = \\sigma(\\mathbf{W}_r [\\mathbf{h}_{t-1}, \\mathbf{x}_t])$$ $$\\tilde{\\mathbf{h}}_t = \\tanh(\\mathbf{W} [\\mathbf{r}_t \\odot \\mathbf{h}_{t-1}, \\mathbf{x}_t]), \\quad \\mathbf{h}_t = (1 - \\mathbf{z}_t) \\odot \\mathbf{h}_{t-1} + \\mathbf{z}_t \\odot \\tilde{\\mathbf{h}}_t$$",
        "formula_explanation": "$\\mathbf{z}_t$ acts simultaneously as forget and input gate: retaining $(1 - \\mathbf{z}_t)$ of old state and $\\mathbf{z}_t$ of candidate state $\\tilde{\\mathbf{h}}_t$.",
        "logic": "GRU has ~25% fewer parameters and trains faster than standard LSTM while delivering comparable performance, making it popular for mobile edge devices and lightweight time-series forecasting.",
        "example": "Stock price or weather sensor telemetry forecasting where sequence lengths are moderate and fast low-latency inference on edge microcontrollers is required."
    },
    {
        "id": "bidirectional-sequence-encoding",
        "topic_id": "dl_seq",
        "topic_label": "Sequence Models: RNNs, LSTMs & GRUs",
        "category": "dl",
        "category_label": "Deep Learning",
        "title": "Bidirectional Sequence Encoding (BiLSTM / BERT)",
        "raw_sub": "Bidirectional Sequence Encoding",
        "definition": "Bidirectional encoding processes a sequence from both directions simultaneously: a forward pass from left-to-right ($t=1 \\to T$) and a backward pass from right-to-left ($t=T \\to 1$), concatenating both representations at each step so each token has complete past and future context.",
        "formula": "$$\\overrightarrow{\\mathbf{h}}_t = \\text{RNN}_{fwd}(\\mathbf{x}_t, \\overrightarrow{\\mathbf{h}}_{t-1}), \\quad \\overleftarrow{\\mathbf{h}}_t = \\text{RNN}_{bwd}(\\mathbf{x}_t, \\overleftarrow{\\mathbf{h}}_{t+1}), \\quad \\mathbf{h}_t = [\\overrightarrow{\\mathbf{h}}_t; \\overleftarrow{\\mathbf{h}}_t]$$",
        "formula_explanation": "The concatenated output $\\mathbf{h}_t \\in \\mathbb{R}^{2d}$ fuses context from both the start and end of the document.",
        "logic": "In comprehension tasks like Named Entity Recognition or BERT question answering, knowing words that follow a token is as crucial as words preceding it.",
        "example": "Disambiguating homonyms: In 'Apple announced a new phone', seeing 'phone' later clarifies that 'Apple' is a corporation, not an edible fruit."
    },

    # dl_generative
    {
        "id": "variational-autoencoders-vae",
        "topic_id": "dl_generative",
        "topic_label": "Generative Models & Diffusion (DDPM)",
        "category": "dl",
        "category_label": "Deep Learning",
        "title": "Variational Autoencoders (VAEs)",
        "raw_sub": "Variational Autoencoders (VAEs & Reparameterization Trick)",
        "definition": "A VAE (Kingma & Welling, 2013) is a directed probabilistic generative model that encodes input $\\mathbf{x}$ into mean $\\boldsymbol{\\mu}$ and variance $\\log\\boldsymbol{\\sigma}^2$ parameters of a continuous Gaussian latent distribution, trained using the Evidence Lower Bound (ELBO) and Reparameterization Trick.",
        "formula": "$$\\mathcal{L}_{ELBO} = \\mathbb{E}_{q_\\phi(\\mathbf{z}|\\mathbf{x})}[\\log p_\\theta(\\mathbf{x}|\\mathbf{z})] - D_{KL}(q_\\phi(\\mathbf{z}|\\mathbf{x}) \\parallel p(\\mathbf{z}))$$ $$\\mathbf{z} = \\boldsymbol{\\mu} + \\boldsymbol{\\sigma} \\odot \\boldsymbol{\\epsilon}, \\quad \\boldsymbol{\\epsilon} \\sim \\mathcal{N}(\\mathbf{0}, \\mathbf{I})$$",
        "formula_explanation": "The reparameterization trick moves the stochastic random sampling $\\boldsymbol{\\epsilon}$ outside the backpropagation graph, allowing deterministic gradients to flow back into encoder parameters $\\boldsymbol{\\mu}$ and $\\boldsymbol{\\sigma}$.",
        "logic": "The KL divergence regularizer forces the latent space to be dense, continuous, and centered at the unit Gaussian, allowing smooth interpolation between points to generate novel samples.",
        "example": "Latent face interpolation: moving smoothly along a vector between 'smiling face' and 'neutral face' in latent space generates natural gradual transitions."
    },
    {
        "id": "generative-adversarial-networks-gan",
        "topic_id": "dl_generative",
        "topic_label": "Generative Models & Diffusion (DDPM)",
        "category": "dl",
        "category_label": "Deep Learning",
        "title": "Generative Adversarial Networks (GANs)",
        "raw_sub": "Generative Adversarial Networks (GANs: Generator vs Discriminator)",
        "definition": "GANs (Goodfellow et al., 2014) frame generation as a two-player zero-sum minimax game between a Generator $G$ (which tries to produce realistic synthetic data from noise) and a Discriminator $D$ (which tries to distinguish real training samples from fake generated ones).",
        "formula": "$$\\min_{G} \\max_{D} V(D, G) = \\mathbb{E}_{\\mathbf{x} \\sim p_{data}}[\\log D(\\mathbf{x})] + \\mathbb{E}_{\\mathbf{z} \\sim p_{\\mathbf{z}}}[\\log(1 - D(G(\\mathbf{z})))]$$",
        "formula_explanation": "$D(\\mathbf{x}) \\in [0, 1]$ outputs probability that $\\mathbf{x}$ is real. $G(\\mathbf{z})$ maps Gaussian noise $\\mathbf{z}$ to realistic synthetic data.",
        "logic": "At Nash equilibrium, the generator captures the true data distribution $p_g = p_{data}$, and the discriminator is unable to tell real from synthetic data ($D(\\mathbf{x}) = 0.5$).",
        "example": "StyleGAN2 generating photorealistic 1024x1024 synthetic human faces that are indistinguishable from real photographs."
    },
    {
        "id": "denoising-diffusion-ddpm",
        "topic_id": "dl_generative",
        "topic_label": "Generative Models & Diffusion (DDPM)",
        "category": "dl",
        "category_label": "Deep Learning",
        "title": "Denoising Diffusion Probabilistic Models (DDPM)",
        "raw_sub": "Denoising Diffusion Probabilistic Models (DDPM)",
        "definition": "DDPM (Sohl-Dickstein 2015, Ho et al. 2020) generates high-fidelity data through a two-phase Markov process: a Forward Process that systematically destroys an image by adding Gaussian noise over $T$ steps, and a learned Reverse Process (a U-Net) that predicts and subtracts that noise step-by-step.",
        "formula": "$$q(\\mathbf{x}_t | \\mathbf{x}_0) = \\mathcal{N}(\\mathbf{x}_t; \\sqrt{\\bar{\\alpha}_t}\\mathbf{x}_0, (1 - \\bar{\\alpha}_t)\\mathbf{I}), \\quad \\mathcal{L}_{simple} = \\mathbb{E}_{t, \\mathbf{x}_0, \\boldsymbol{\\epsilon}} \\left[ \\| \\boldsymbol{\\epsilon} - \\boldsymbol{\\epsilon}_\\theta(\\mathbf{x}_t, t) \\|^2 \\right]$$",
        "formula_explanation": "$\\boldsymbol{\\epsilon} \\sim \\mathcal{N}(\\mathbf{0}, \\mathbf{I})$ is the actual added Gaussian noise, and $\\boldsymbol{\\epsilon}_\\theta(\\mathbf{x}_t, t)$ is the U-Net's estimate of the noise present at timestep $t$.",
        "logic": "Unlike GANs which suffer from mode collapse and training instability, diffusion models have stable convex-like regression objectives and cover the full multimodal distribution.",
        "example": "Starting with pure TV static white noise $\\mathbf{x}_{1000}$, running 50 reverse denoising steps with a trained U-Net reconstructs a crystal-clear photorealistic landscape image."
    },
    {
        "id": "classifier-free-guidance-cfg",
        "topic_id": "dl_generative",
        "topic_label": "Generative Models & Diffusion (DDPM)",
        "category": "dl",
        "category_label": "Deep Learning",
        "title": "Classifier-Free Guidance (CFG)",
        "raw_sub": "Classifier-Free Guidance (Balancing prompt adherence vs diversity)",
        "definition": "Classifier-Free Guidance (Ho & Salimans, 2021) controls how strictly a generative diffusion model adheres to a text prompt versus sample diversity by interpolating between conditional noise predictions and unconditional (empty prompt) noise predictions.",
        "formula": "$$\\tilde{\\boldsymbol{\\epsilon}}_\\theta(\\mathbf{x}_t, c) = \\boldsymbol{\\epsilon}_\\theta(\\mathbf{x}_t, \\emptyset) + s \\cdot \\left( \\boldsymbol{\\epsilon}_\\theta(\\mathbf{x}_t, c) - \\boldsymbol{\\epsilon}_\\theta(\\mathbf{x}_t, \\emptyset) \\right)$$",
        "formula_explanation": "$c$ is the text prompt conditioning embedding, $\\emptyset$ is the unconditional null token, and $s \\ge 1.0$ is the guidance scale hyperparameter.",
        "logic": "Setting $s = 1.0$ yields standard conditioning. Raising $s$ to $7.0$ amplifies the direction where prompt features are strongest, dramatically boosting prompt faithfulness and image sharpness at the cost of diversity.",
        "example": "In Stable Diffusion or Midjourney: CFG scale $s = 7.5$ ensures an astronaut helmet prompt strictly renders a helmet instead of blending into general space backgrounds."
    },
    {
        "id": "latent-diffusion-models",
        "topic_id": "dl_generative",
        "topic_label": "Generative Models & Diffusion (DDPM)",
        "category": "dl",
        "category_label": "Deep Learning",
        "title": "Latent Diffusion Models (LDM / Stable Diffusion)",
        "raw_sub": "Latent Diffusion Models (Running diffusion inside compressed latent space)",
        "definition": "Latent Diffusion Models (Rombach et al., 2022) train and execute the denoising diffusion process within a low-dimensional compressed latent space $\\mathbf{z} = \\mathcal{E}(\\mathbf{x})$ learned by a pre-trained VAE, rather than directly on high-dimensional raw pixel space.",
        "formula": "$$\\mathbf{z} = \\mathcal{E}(\\mathbf{x}) \\in \\mathbb{R}^{\\frac{H}{8} \\times \\frac{W}{8} \\times 4}, \\quad \\hat{\\mathbf{x}} = \\mathcal{D}(\\mathbf{z})$$",
        "formula_explanation": "For a $512 \\times 512 \\times 3$ image (786,432 numbers), compression factor $f=8$ yields a compact latent tensor of $64 \\times 64 \\times 4$ (16,384 numbers), an exact $48\\times$ reduction in computational complexity.",
        "logic": "High-frequency imperceptible pixel noise is abstracted away by the VAE autoencoder, allowing the diffusion U-Net to concentrate its parameter capacity solely on semantic composition and geometry.",
        "example": "Stable Diffusion v1.5, SDXL, and Flux run diffusion on latents in seconds on consumer GPUs with 8GB VRAM, whereas pixel-space diffusion (Imagen) requires server clusters."
    }
]

if __name__ == "__main__":
    print(f"Loaded {len(DL_ARCH_CONCEPTS)} Deep Learning Architecture concepts successfully.")
