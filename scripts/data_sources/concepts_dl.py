"""
Deep Learning Core Concepts (25 concepts):
- Neurons & Hidden Layers
- Activation Functions (ReLU, GELU, Softmax, etc.)
- Backpropagation & AutoDiff
- Optimizers (Adam, AdamW, Momentum, Cosine Decay)
- Normalization & Regularization (Dropout, LayerNorm, RMSNorm, Weight Decay)
"""

DL_CONCEPTS = [
    # dl_neurons
    {
        "id": "artificial-neurons-perceptrons",
        "topic_id": "dl_neurons",
        "topic_label": "Neural Networks & Hidden Layers",
        "category": "dl",
        "category_label": "Deep Learning",
        "title": "Artificial Neurons & Perceptrons",
        "raw_sub": "Artificial Neurons / Perceptrons (Linear sum + activation)",
        "definition": "An artificial neuron (perceptron) is the fundamental computational cell of a neural network. It takes multiple numerical inputs, computes a weighted sum plus an adjustable bias, and passes that scalar through a non-linear activation function to produce an output signal.",
        "formula": "$$z = \\sum_{i=1}^{n} w_i x_i + b = \\mathbf{w}^T \\mathbf{x} + b, \\quad a = \\sigma(z)$$",
        "formula_explanation": "$\\mathbf{x}$ is the input feature vector, $\\mathbf{w}$ is the learned weight vector, $b$ is the scalar bias (allowing the decision boundary to shift away from the origin), and $\\sigma(\\cdot)$ is a non-linear activation function producing final activation $a$.",
        "logic": "A single linear combination $\\mathbf{w}^T\\mathbf{x} + b$ can only construct flat linear hyperplanes. By feeding the linear combination into a non-linear activation $\\sigma(z)$, the neuron gains the ability to fire selectively, creating non-linear decision boundaries when chained in networks.",
        "example": "A loan approval neuron: inputs are income $x_1$ and credit score $x_2$. If $w_1 \\cdot x_1 + w_2 \\cdot x_2 + b > 0$, the activation outputs close to 1 (approved); otherwise close to 0 (rejected)."
    },
    {
        "id": "input-hidden-output-layers",
        "topic_id": "dl_neurons",
        "topic_label": "Neural Networks & Hidden Layers",
        "category": "dl",
        "category_label": "Deep Learning",
        "title": "Input, Hidden, and Output Layers",
        "raw_sub": "Input, Hidden, and Output Layers",
        "definition": "A multilayer perceptron (MLP) organizes neurons into sequential stages: the Input Layer receives raw feature dimensions, Hidden Layers extract progressively abstract internal representations, and the Output Layer delivers task predictions (logits, probabilities, or continuous targets).",
        "formula": "$$\\mathbf{h}^{[1]} = \\sigma(\\mathbf{W}^{[1]}\\mathbf{x} + \\mathbf{b}^{[1]}), \\quad \\mathbf{h}^{[l]} = \\sigma(\\mathbf{W}^{[l]}\\mathbf{h}^{[l-1]} + \\mathbf{b}^{[l]}), \\quad \\hat{\\mathbf{y}} = g(\\mathbf{W}^{[L]}\\mathbf{h}^{[L-1]} + \\mathbf{b}^{[L]})$$",
        "formula_explanation": "$\\mathbf{h}^{[l]}$ represents the activation tensor of layer $l$, $\\mathbf{W}^{[l]}$ is the parameter weight matrix mapping from dimension $d_{l-1}$ to $d_l$, and $g(\\cdot)$ is the output layer transformation (e.g. Softmax for multi-class classification or identity for regression).",
        "logic": "Lower hidden layers detect primitive patterns (edges, frequency blips), middle hidden layers assemble textures and motifs, and higher hidden layers capture semantic object identities. Deep hierarchical structure allows exponential representational capacity relative to parameter count.",
        "example": "In image recognition: Input layer takes $28 \\times 28 = 784$ pixel grayscale intensities; Hidden Layer 1 (128 neurons) extracts strokes; Hidden Layer 2 (64 neurons) extracts loops and corners; Output Layer (10 neurons) predicts digits 0 to 9."
    },
    {
        "id": "non-linear-separability",
        "topic_id": "dl_neurons",
        "topic_label": "Neural Networks & Hidden Layers",
        "category": "dl",
        "category_label": "Deep Learning",
        "title": "Non-linear Separability (XOR Problem)",
        "raw_sub": "Non-linear Separability (Solving XOR and concentric circles)",
        "definition": "A dataset is non-linearly separable when no single straight line or flat hyperplane can partition positive and negative classes without error. Classic examples include the XOR boolean logic gate and concentric rings of data points.",
        "formula": "$$\\text{XOR}(x_1, x_2) = (x_1 \\lor x_2) \\land \\neg(x_1 \\land x_2)$$",
        "formula_explanation": "A single linear perceptron fails on XOR because $(0,1)$ and $(1,0)$ output 1, while $(0,0)$ and $(1,1)$ output 0, requiring two intersecting decision lines rather than one.",
        "logic": "Without hidden layers and non-linear activations, stacking multiple linear layers simply collapses into a single matrix multiplication: $\\mathbf{W}_2(\\mathbf{W}_1 \\mathbf{x}) = (\\mathbf{W}_2 \\mathbf{W}_1) \\mathbf{x} = \\mathbf{W}_{net} \\mathbf{x}$. Non-linear activations warp the coordinate space, making classes linearly separable in the transformed hidden space.",
        "example": "Predicting disease risk when either low sugar or very high sugar is safe, but moderate abnormal spikes cause complications. A straight line cannot isolate the two ends simultaneously; a hidden layer bends the geometry to enclose the region."
    },
    {
        "id": "forward-propagation-matrix-arithmetic",
        "topic_id": "dl_neurons",
        "topic_label": "Neural Networks & Hidden Layers",
        "category": "dl",
        "category_label": "Deep Learning",
        "title": "Forward Propagation Matrix Arithmetic",
        "raw_sub": "Forward Propagation Matrix Arithmetic",
        "definition": "Forward propagation is the directional execution pass that computes layer activations from input to output across a batch of samples simultaneously using vectorized matrix-matrix multiplications (GEMM) on GPUs.",
        "formula": "$$\\mathbf{Z}^{[l]} = \\mathbf{A}^{[l-1]} (\\mathbf{W}^{[l]})^T + \\mathbf{b}^{[l]}, \\quad \\mathbf{A}^{[l]} = \\sigma(\\mathbf{Z}^{[l]})$$",
        "formula_explanation": "For a mini-batch of $B$ samples with input dimension $d_{in}$ and output dimension $d_{out}$, $\\mathbf{A}^{[l-1]} \\in \\mathbb{R}^{B \\times d_{in}}$ and $\\mathbf{W}^{[l]} \\in \\mathbb{R}^{d_{out} \\times d_{in}}$, yielding pre-activation batch tensor $\\mathbf{Z}^{[l]} \\in \\mathbb{R}^{B \\times d_{out}}$.",
        "logic": "Batching samples into 2D/3D matrices maximizes parallel CUDA core saturation and memory bandwidth efficiency compared to serial element-by-element loops.",
        "example": "Passing a batch of $B=64$ token vectors of dimension 768 through a linear projection layer of dimension 3072: computed via a single cuBLAS matrix multiplication $(64 \\times 768) \\times (768 \\times 3072) \\to (64 \\times 3072)$ in microseconds."
    },
    {
        "id": "universal-approximation-theorem",
        "topic_id": "dl_neurons",
        "topic_label": "Neural Networks & Hidden Layers",
        "category": "dl",
        "category_label": "Deep Learning",
        "title": "Universal Approximation Theorem",
        "raw_sub": "Universal Approximation Theorem",
        "definition": "A foundational theorem (Cybenko, 1989; Hornik, 1991) stating that a feedforward network with a single hidden layer containing a finite number of non-linear neurons can approximate any continuous function on compact subsets of $\\mathbb{R}^n$ to arbitrary precision $\\epsilon > 0$.",
        "formula": "$$\\forall f \\in C(K), \\epsilon > 0, \\quad \\exists F(x) = \\sum_{i=1}^{N} v_i \\sigma(\\mathbf{w}_i^T \\mathbf{x} + b_i) \\quad \\text{such that} \\quad \\sup_{x \\in K} |F(x) - f(x)| < \\epsilon$$",
        "formula_explanation": "$K \\subset \\mathbb{R}^n$ is a compact input set, $N$ is the number of hidden units, $\\sigma$ is any continuous non-polynomial activation function, and $F(x)$ is the network approximation.",
        "logic": "While a single wide layer can theoretically approximate any function, the required width $N$ scales exponentially with dimension. Deep networks (many narrow layers) achieve the same approximation power with exponentially fewer parameters by reusing compositional features.",
        "example": "Approximating a complex aerodynamic drag curve: a network can fit any bumpy non-linear curve as closely as needed by adding enough hidden neurons."
    },

    # dl_activations
    {
        "id": "relu-activation",
        "topic_id": "dl_activations",
        "topic_label": "Activation Functions (ReLU, GELU, Softmax)",
        "category": "dl",
        "category_label": "Deep Learning",
        "title": "ReLU (Rectified Linear Unit)",
        "raw_sub": "ReLU (Rectified Linear Unit - default for hidden layers)",
        "definition": "ReLU is the most widely adopted piecewise linear activation function for hidden layers in modern deep learning. It passes positive values unchanged and zeros out all negative inputs, providing computational simplicity and constant derivative.",
        "formula": "$$\\text{ReLU}(z) = \\max(0, z), \\quad \\frac{d}{dz}\\text{ReLU}(z) = \\begin{cases} 1 & \\text{if } z > 0 \\\\ 0 & \\text{if } z < 0 \\end{cases}$$",
        "formula_explanation": "For $z > 0$, the gradient is exactly 1, completely preventing gradient attenuation or saturation during backpropagation across dozens of layers.",
        "logic": "Unlike Sigmoid or Tanh whose gradients approach 0 when $|z|$ is large, ReLU never saturates in the positive regime. Furthermore, evaluating $\\max(0, z)$ requires just a single CPU/GPU hardware instruction (conditional thresholding), dramatically speeding up training.",
        "example": "If pre-activation $z = 4.2$, $\\text{ReLU}(4.2) = 4.2$. If $z = -3.8$, $\\text{ReLU}(-3.8) = 0$."
    },
    {
        "id": "dying-relu-leaky-relu",
        "topic_id": "dl_activations",
        "topic_label": "Activation Functions (ReLU, GELU, Softmax)",
        "category": "dl",
        "category_label": "Deep Learning",
        "title": "Dying ReLU & Leaky ReLU / PReLU",
        "raw_sub": "Dying ReLU Problem & Leaky ReLU / PReLU",
        "definition": "The 'Dying ReLU' problem occurs when a neuron's weights update such that its input is negative for all training samples; its gradient becomes permanently 0 and the neuron never fires or learns again. Leaky ReLU prevents this by introducing a small non-zero slope $\\alpha$ for negative values.",
        "formula": "$$\\text{LeakyReLU}(z) = \\begin{cases} z & \\text{if } z \\ge 0 \\\\ \\alpha z & \\text{if } z < 0 \\end{cases} \\quad (\\text{typically } \\alpha = 0.01)$$",
        "formula_explanation": "When $z < 0$, the gradient is $\\alpha = 0.01$ rather than 0, allowing backpropagated error gradients to reach weights and revive inactive neurons.",
        "logic": "In Parametric ReLU (PReLU), $\\alpha$ is treated as a learnable parameter trained via backprop. In ELU (Exponential Linear Unit), negative values smoothly asymptote to $-\\alpha$, bringing mean activation closer to zero.",
        "example": "If a neuron receives $z = -5.0$, standard ReLU outputs 0 with 0 gradient (dead). Leaky ReLU outputs $-0.05$ with gradient $0.01$, keeping the neuron alive to learn."
    },
    {
        "id": "gelu-activation",
        "topic_id": "dl_activations",
        "topic_label": "Activation Functions (ReLU, GELU, Softmax)",
        "category": "dl",
        "category_label": "Deep Learning",
        "title": "GELU (Gaussian Error Linear Unit)",
        "raw_sub": "GELU (Gaussian Error Linear Unit - standard in modern LLMs)",
        "definition": "GELU is a smooth, non-monotonic activation function that weights inputs by their probability under a Gaussian normal distribution. It is the gold standard activation in Transformer architectures including BERT, GPT-3, LLaMA, and ViT.",
        "formula": "$$\\text{GELU}(z) = z \\cdot \\Phi(z) = z \\cdot P(X \\le z) \\approx 0.5z \\left(1 + \\tanh\\left(\\sqrt{\\frac{2}{\\pi}} \\left(z + 0.044715 z^3\\right)\\right)\\right)$$",
        "formula_explanation": "$\\Phi(z)$ is the standard normal cumulative distribution function (CDF). For high positive $z$, $\\Phi(z) \\approx 1 \\implies \\text{GELU}(z) \\approx z$. For high negative $z$, $\\Phi(z) \\approx 0 \\implies \\text{GELU}(z) \\approx 0$.",
        "logic": "Unlike ReLU which has a hard sharp kink at $z=0$, GELU is smoothly differentiable everywhere and allows a small negative trough near $z \\approx -0.75$, enabling richer gradient flow and probabilistic gating.",
        "example": "In GPT-4 feedforward layers: each hidden activation passes through GELU (or SwiGLU), ensuring smooth non-zero gradient transmission even for slightly negative token representations."
    },
    {
        "id": "softmax-activation",
        "topic_id": "dl_activations",
        "topic_label": "Activation Functions (ReLU, GELU, Softmax)",
        "category": "dl",
        "category_label": "Deep Learning",
        "title": "Softmax Activation Function",
        "raw_sub": "Softmax (For multi-class probability outputs)",
        "definition": "Softmax normalizes an arbitrary $K$-dimensional vector of real-valued unnormalized logits into a valid categorical probability distribution where each probability lies in $(0, 1)$ and all values sum strictly to 1.",
        "formula": "$$\\sigma(\\mathbf{z})_i = \\frac{e^{z_i - \\max(\\mathbf{z})}}{\\sum_{j=1}^{K} e^{z_j - \\max(\\mathbf{z})}}, \\quad \\sum_{i=1}^{K} \\sigma(\\mathbf{z})_i = 1$$",
        "formula_explanation": "$z_i$ is the logit for class $i$. Subtracting $\\max(\\mathbf{z})$ from each logit is a mathematically identical numerical stability trick that prevents floating-point overflow ($e^{1000} = \\infty$).",
        "logic": "The exponential function ensures all output values are strictly positive ($e^z > 0$), and dividing by the sum of exponentials guarantees normalization to a true discrete probability distribution.",
        "example": "Image classifier outputting logits $[2.0, 1.0, 0.1]$: Softmax computes $e^{2.0} \\approx 7.39$, $e^{1.0} \\approx 2.72$, $e^{0.1} \\approx 1.11$ (sum $= 11.22$), yielding probabilities $[0.659, 0.242, 0.099]$."
    },
    {
        "id": "sigmoid-tanh-activations",
        "topic_id": "dl_activations",
        "topic_label": "Activation Functions (ReLU, GELU, Softmax)",
        "category": "dl",
        "category_label": "Deep Learning",
        "title": "Sigmoid & Tanh Saturated Activations",
        "raw_sub": "Sigmoid & Tanh (Historical activations prone to saturation)",
        "definition": "Sigmoid maps $(-\\infty, \\infty)$ into $(0, 1)$, while Hyperbolic Tangent (Tanh) maps into $(-1, 1)$. While historically popular, both suffer from severe gradient saturation (vanishing gradients) in deep networks when inputs move away from 0.",
        "formula": "$$\\sigma(z) = \\frac{1}{1 + e^{-z}}, \\quad \\tanh(z) = \\frac{e^z - e^{-z}}{e^z + e^{-z}} = 2\\sigma(2z) - 1$$",
        "formula_explanation": "Derivative peaks are small: $\\max(\\sigma'(z)) = 0.25$ at $z=0$, and $\\max(\\tanh'(z)) = 1.0$ at $z=0$. For $|z| > 4$, the derivatives are virtually zero.",
        "logic": "Tanh is preferred over Sigmoid in recurrent cells (LSTMs/GRUs) because its output is zero-centered (mean near 0), which prevents zig-zagging gradient dynamics during backpropagation.",
        "example": "Binary logistic regression uses Sigmoid at the output layer to predict probability of customer churn. LSTM memory cells use Tanh to regulate hidden candidate state updates between $-1$ and $+1$."
    },

    # dl_backprop
    {
        "id": "computational-graph",
        "topic_id": "dl_backprop",
        "topic_label": "Backpropagation & AutoDiff",
        "category": "dl",
        "category_label": "Deep Learning",
        "title": "Computational Graph (DAG)",
        "raw_sub": "Computational Graph (DAG of tensor operations)",
        "definition": "A computational graph is a directed acyclic graph (DAG) where nodes represent mathematical tensor operations (addition, matrix multiplication, activation) or variables (weights, inputs, biases), and edges represent data tensors flowing between them.",
        "formula": "$$G = (V, E), \\quad v_i = f_i(\\text{Parents}(v_i)), \\quad \\mathcal{L} = v_{output}$$",
        "formula_explanation": "During forward execution, operations are evaluated in topological order. During backward execution, gradients flow in reverse topological order from scalar loss node $\\mathcal{L}$ back to leaf parameter nodes.",
        "logic": "Frameworks like PyTorch construct dynamic computational graphs on-the-fly (eager execution) during each forward pass, recording which operation created each tensor to enable automatic reverse-mode backpropagation.",
        "example": "Computing $z = (w \\cdot x + b)^2$: Graph has leaf nodes $w, x, b \\to$ node `mul` $\\to$ node `add` $\\to$ node `pow(2)`. The gradient of $z$ with respect to $w$ is automatically evaluated by walking backwards through each node."
    },
    {
        "id": "reverse-mode-autodiff",
        "topic_id": "dl_backprop",
        "topic_label": "Backpropagation & AutoDiff",
        "category": "dl",
        "category_label": "Deep Learning",
        "title": "Reverse-Mode Automatic Differentiation",
        "raw_sub": "Reverse-Mode Automatic Differentiation",
        "definition": "Reverse-mode automatic differentiation (backpropagation) applies the multivariate calculus Chain Rule recursively from the scalar loss function backwards to all internal parameters in a single reverse sweep.",
        "formula": "$$\\frac{\\partial \\mathcal{L}}{\\partial x_j} = \\sum_{i \\in \\text{Children}(j)} \\frac{\\partial \\mathcal{L}}{\\partial y_i} \\cdot \\frac{\\partial y_i}{\\partial x_j}$$",
        "formula_explanation": "$\\frac{\\partial \\mathcal{L}}{\\partial y_i}$ is the adjoint (incoming gradient) from downstream nodes, multiplied by the local Jacobian $\\frac{\\partial y_i}{\\partial x_j}$ of the operation connecting them.",
        "logic": "In machine learning, models have billions of inputs/weights ($N \\gg 1$) but only a single scalar loss value ($M = 1$). Reverse-mode autodiff computes all $N$ partial derivatives in $O(1)$ passes, whereas forward-mode would require $N$ separate forward passes.",
        "example": "For a 7-billion parameter LLM, reverse-mode autodiff computes gradients for all 7,000,000,000 parameters simultaneously in approximately $2\\times$ the runtime of a single forward pass."
    },
    {
        "id": "vanishing-gradient-problem",
        "topic_id": "dl_backprop",
        "topic_label": "Backpropagation & AutoDiff",
        "category": "dl",
        "category_label": "Deep Learning",
        "title": "Vanishing Gradient Problem",
        "raw_sub": "Vanishing Gradient Problem (Gradients shrinking exponentially)",
        "definition": "The vanishing gradient problem occurs when backpropagated error gradients shrink exponentially as they multiply across many successive layers, causing early layers near the input to receive virtually zero gradient updates and stall learning.",
        "formula": "$$\\frac{\\partial \\mathcal{L}}{\\partial \\mathbf{h}^{[1]}} = \\frac{\\partial \\mathcal{L}}{\\partial \\mathbf{h}^{[L]}} \\prod_{l=2}^{L} \\left( \\mathbf{W}^{[l]T} \\cdot \\text{diag}(\\sigma'(\\mathbf{z}^{[l]})) \\right)$$",
        "formula_explanation": "If the eigenvalues of weight matrices $\\mathbf{W}^{[l]}$ or activation derivatives $\\sigma'$ are $< 1$ (e.g. $\\sigma' \\le 0.25$ for Sigmoid), multiplying $L$ such terms causes the gradient magnitude to decay as $O(\\gamma^L) \\to 0$.",
        "logic": "Modern deep architectures solve vanishing gradients through three breakthroughs: non-saturating activations (ReLU/GELU), residual skip connections ($F(x) + x$), and normalization layers (BatchNorm/LayerNorm).",
        "example": "A 50-layer deep network using Sigmoids: gradient at layer 1 is multiplied by $(0.25)^{50} \\approx 10^{-30}$, effectively freezing all initial convolutional feature extractors."
    },
    {
        "id": "exploding-gradient-clipping",
        "topic_id": "dl_backprop",
        "topic_label": "Backpropagation & AutoDiff",
        "category": "dl",
        "category_label": "Deep Learning",
        "title": "Exploding Gradients & Gradient Clipping",
        "raw_sub": "Exploding Gradient Problem & Gradient Clipping",
        "definition": "The exploding gradient problem occurs when accumulated gradient products exceed 1 repeatedly, causing gradients to blow up to infinity (producing `NaN` loss or destabilizing weights). Gradient clipping rescales the gradient vector if its L2 norm exceeds a maximum threshold $c$.",
        "formula": "$$\\mathbf{g} \\leftarrow \\begin{cases} \\mathbf{g} & \\text{if } \\|\\mathbf{g}\\|_2 \\le c \\\\ c \\cdot \\frac{\\mathbf{g}}{\\|\\mathbf{g}\\|_2} & \\text{if } \\|\\mathbf{g}\\|_2 > c \\end{cases}$$",
        "formula_explanation": "$\\|\\mathbf{g}\\|_2 = \\sqrt{\\sum_i g_i^2}$ is the total Euclidean norm across all model parameters, and $c$ is the maximum permitted clip threshold (typically $1.0$).",
        "logic": "Gradient clipping preserves the exact geometric direction of the gradient vector while capping its maximum step magnitude, preventing catastrophic weight divergence during sudden loss spikes.",
        "example": "In recurrent networks or Transformer pre-training: an unexpected noisy batch produces $\\|\\mathbf{g}\\| = 85.0$. With clip value $c = 1.0$, all gradients are rescaled by $\\frac{1.0}{85.0} \\approx 0.0117$, keeping training smooth and stable."
    },
    {
        "id": "jacobian-hessian-matrices",
        "topic_id": "dl_backprop",
        "topic_label": "Backpropagation & AutoDiff",
        "category": "dl",
        "category_label": "Deep Learning",
        "title": "Jacobian & Hessian Matrices",
        "raw_sub": "Jacobian & Hessian Matrix Multiplications",
        "definition": "The Jacobian matrix stores all first-order partial derivatives of a vector-valued function with respect to a vector input. The Hessian matrix stores all second-order partial derivatives of a scalar function, describing local curvature and loss landscape geometry.",
        "formula": "$$\\mathbf{J}_{ij} = \\frac{\\partial f_i}{\\partial x_j}, \\quad \\mathbf{H}_{ij} = \\frac{\\partial^2 \\mathcal{L}}{\\partial x_i \\partial x_j}$$",
        "formula_explanation": "For a vector output $\\mathbf{f} \\in \\mathbb{R}^m$ and input $\\mathbf{x} \\in \\mathbb{R}^n$, $\\mathbf{J} \\in \\mathbb{R}^{m \\times n}$. For a scalar loss $\\mathcal{L}$ with parameter vector $\\boldsymbol{\\theta} \\in \\mathbb{R}^P$, the Hessian is symmetric $\\mathbf{H} \\in \\mathbb{R}^{P \\times P}$.",
        "logic": "Exact second-order Newton-Raphson optimization uses $\\mathbf{H}^{-1}\\nabla \\mathcal{L}$, which converges in very few steps but requires $O(P^2)$ memory and $O(P^3)$ computation. In deep learning ($P = 10^9$), full Hessian inversion is impossible, so first-order methods (Adam) or Hessian-free approximations are used.",
        "example": "Analyzing loss landscape sharpness: the maximum eigenvalue $\\lambda_{max}(\\mathbf{H})$ indicates curvature sharpness. Flatter minima (lower eigenvalues) correlate with superior real-world test generalization."
    },

    # dl_opt
    {
        "id": "sgd-momentum",
        "topic_id": "dl_opt",
        "topic_label": "Deep Learning Optimizers (Adam, AdamW)",
        "category": "dl",
        "category_label": "Deep Learning",
        "title": "SGD with Momentum",
        "raw_sub": "SGD with Momentum (Building velocity to escape local minima)",
        "definition": "Stochastic Gradient Descent with Momentum accelerates optimization by accumulating an exponentially decaying moving average of past gradients (like a heavy ball rolling down a hilly landscape), smoothing oscillations across ravines and speeding progress along flat slopes.",
        "formula": "$$\\mathbf{v}_t = \\beta \\mathbf{v}_{t-1} + (1 - \\beta) \\nabla_{\\boldsymbol{\\theta}} \\mathcal{L}_t, \\quad \\boldsymbol{\\theta}_{t+1} = \\boldsymbol{\\theta}_t - \\eta \\mathbf{v}_t$$",
        "formula_explanation": "$\\mathbf{v}_t$ is the velocity vector, $\\beta \\in [0.9, 0.99]$ is the momentum friction coefficient, and $\\eta$ is the learning rate.",
        "logic": "In ravine valleys where gradients oscillate violently side-to-side, perpendicular oscillations cancel out across successive steps, while forward velocity along the canyon floor steadily compounds.",
        "example": "Training ResNet-50: SGD with momentum $\\beta = 0.9$ and learning rate $0.1$ is standard, consistently achieving superior test generalization accuracy over un-regularized adaptive methods."
    },
    {
        "id": "rmsprop-optimizer",
        "topic_id": "dl_opt",
        "topic_label": "Deep Learning Optimizers (Adam, AdamW)",
        "category": "dl",
        "category_label": "Deep Learning",
        "title": "RMSprop (Root Mean Square Propagation)",
        "raw_sub": "RMSprop (Scaling steps by root mean square of gradients)",
        "definition": "RMSprop (Hinton, 2012) is an adaptive learning rate optimizer that divides parameter updates by the running square root of exponentially decaying squared gradients, dampening updates for frequent large-gradient parameters and amplifying updates for sparse gradients.",
        "formula": "$$\\mathbf{s}_t = \\beta_2 \\mathbf{s}_{t-1} + (1 - \\beta_2) \\mathbf{g}_t^2, \\quad \\boldsymbol{\\theta}_{t+1} = \\boldsymbol{\\theta}_t - \\frac{\\eta}{\\sqrt{\\mathbf{s}_t} + \\epsilon} \\odot \\mathbf{g}_t$$",
        "formula_explanation": "$\\mathbf{s}_t$ tracks the second raw moment (variance) of gradient $\\mathbf{g}_t$, $\\beta_2 \\approx 0.99$ is the discount factor, and $\\epsilon = 10^{-8}$ prevents division by zero.",
        "logic": "AdaGrad accumulated all historical squared gradients without decay, causing steps to shrink to zero prematurely. RMSprop uses an exponential window, allowing continuous adaptation during non-stationary mini-batch training.",
        "example": "Popular in training Recurrent Neural Networks (RNNs) and deep reinforcement learning (DQN) where gradient magnitudes fluctuate unpredictably."
    },
    {
        "id": "adam-optimizer",
        "topic_id": "dl_opt",
        "topic_label": "Deep Learning Optimizers (Adam, AdamW)",
        "category": "dl",
        "category_label": "Deep Learning",
        "title": "Adam (Adaptive Moment Estimation)",
        "raw_sub": "Adam (Combining momentum and adaptive variance scaling)",
        "definition": "Adam (Kingma & Ba, 2014) combines the advantages of Momentum (first moment: running mean) and RMSprop (second moment: uncentered running variance), along with analytical bias-correction factors to compensate for initialization at zero.",
        "formula": "$$\\mathbf{m}_t = \\beta_1 \\mathbf{m}_{t-1} + (1-\\beta_1)\\mathbf{g}_t, \\quad \\mathbf{v}_t = \\beta_2 \\mathbf{v}_{t-1} + (1-\\beta_2)\\mathbf{g}_t^2$$ $$\\hat{\\mathbf{m}}_t = \\frac{\\mathbf{m}_t}{1 - \\beta_1^t}, \\quad \\hat{\\mathbf{v}}_t = \\frac{\\mathbf{v}_t}{1 - \\beta_2^t}, \\quad \\boldsymbol{\\theta}_{t+1} = \\boldsymbol{\\theta}_t - \\frac{\\eta}{\\sqrt{\\hat{\\mathbf{v}}_t} + \\epsilon} \\hat{\\mathbf{m}}_t$$",
        "formula_explanation": "$\\beta_1 = 0.9$, $\\beta_2 = 0.999$, $\\epsilon = 10^{-8}$. Dividing by $1 - \\beta^t$ corrects the initial zero-bias of the moving averages during early optimization steps.",
        "logic": "Adam is robust to hyperparameter tuning and scales gradient steps invariant to the scale of the gradients, making it the default optimizer across computer vision, NLP, and reinforcement learning.",
        "example": "Default starting optimizer for virtually all deep learning prototypes: setting `optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)` guarantees rapid, stable convergence."
    },
    {
        "id": "adamw-optimizer",
        "topic_id": "dl_opt",
        "topic_label": "Deep Learning Optimizers (Adam, AdamW)",
        "category": "dl",
        "category_label": "Deep Learning",
        "title": "AdamW (Decoupled Weight Decay)",
        "raw_sub": "AdamW (Decoupling weight decay from gradient updates)",
        "definition": "AdamW (Loshchilov & Hutter, 2017) fixes a major flaw in how standard Adam implements L2 regularization. Instead of adding L2 gradient penalty into the adaptive gradient moments (which distorts weight decay for large gradients), AdamW decouples weight decay and subtracts it directly from weights.",
        "formula": "$$\\boldsymbol{\\theta}_{t+1} = \\boldsymbol{\\theta}_t - \\eta \\cdot \\lambda \\boldsymbol{\\theta}_t - \\frac{\\eta}{\\sqrt{\\hat{\\mathbf{v}}_t} + \\epsilon} \\hat{\\mathbf{m}}_t$$",
        "formula_explanation": "$\\eta \\cdot \\lambda \\boldsymbol{\\theta}_t$ is the decoupled weight decay step, where $\\lambda$ is the true decay coefficient, applied completely independently of the adaptive denominator $\\sqrt{\\hat{\\mathbf{v}}_t}$.",
        "logic": "In standard Adam with L2, weights with large historical gradients had their weight decay divided by a large variance estimate, weakening the regularization effect. AdamW restores true proportional weight decay across all parameters.",
        "example": "Universal standard for modern Large Language Models: GPT-3, LLaMA-3, Mistral, and BERT are all trained with `torch.optim.AdamW(lr=3e-4, weight_decay=0.1)`."
    },
    {
        "id": "learning-rate-schedules",
        "topic_id": "dl_opt",
        "topic_label": "Deep Learning Optimizers (Adam, AdamW)",
        "category": "dl",
        "category_label": "Deep Learning",
        "title": "Learning Rate Warmup & Cosine Decay",
        "raw_sub": "Learning Rate Warmup & Cosine Decay Schedules",
        "definition": "Learning rate scheduling dynamically varies step size $\\eta$ over training: Warmup linearly ramps $\\eta$ from 0 to $\\eta_{max}$ in early iterations to stabilize initial weights, followed by Cosine Annealing which smoothly reduces $\\eta$ along a cosine curve down to a small floor.",
        "formula": "$$\\eta_t = \\eta_{min} + \\frac{1}{2}(\\eta_{max} - \\eta_{min}) \\left(1 + \\cos\\left(\\frac{t - T_{warm}}{T_{max} - T_{warm}} \\pi\\right)\\right)$$",
        "formula_explanation": "$T_{warm}$ is the warmup step budget (typically first $1\\%$ to $5\\%$ of training), $T_{max}$ is total training steps, and $\\eta_{min} \\approx 0.1 \\cdot \\eta_{max}$.",
        "logic": "Early randomly initialized weights produce violent, noisy gradients; low warmup learning rate prevents disruptive initial parameter updates. Later cosine decay allows weights to settle gently into deep, flat local minima without overshooting.",
        "example": "LLaMA-3 training schedule: linearly warms up from 0 to $3 \\times 10^{-4}$ over the first 2,000 steps, then follows cosine decay down to $3 \\times 10^{-5}$ across the remaining 15 trillion tokens."
    },

    # dl_norm
    {
        "id": "dropout-regularization",
        "topic_id": "dl_norm",
        "topic_label": "Normalization & Regularization (Dropout, LayerNorm)",
        "category": "dl",
        "category_label": "Deep Learning",
        "title": "Dropout Regularization",
        "raw_sub": "Dropout (Randomly dropping activations to prevent co-adaptation)",
        "definition": "Dropout (Srivastava et al., 2014) is an extreme ensemble regularization technique that randomly zeros out a fraction $p$ of hidden neuron activations during each forward training step, forcing the network to learn redundant, robust internal representations.",
        "formula": "$$\\mathbf{r} \\sim \\text{Bernoulli}(1 - p), \\quad \\mathbf{h}_{train} = \\frac{1}{1 - p} (\\mathbf{r} \\odot \\mathbf{h}), \\quad \\mathbf{h}_{eval} = \\mathbf{h}$$",
        "formula_explanation": "Multiplying by inverted scaling factor $\\frac{1}{1-p}$ during training (Inverted Dropout) keeps expected activation magnitude identical, eliminating any need to rescale weights at test inference time.",
        "logic": "When neurons cannot rely on specific neighboring neurons to always be present, they cannot form fragile co-adaptations. Training a network with dropout approximates training an ensemble of $2^N$ sub-networks sharing weights.",
        "example": "Applying `Dropout(p=0.5)` to a dense 1024-unit classifier: on each training batch, approximately 512 randomly chosen neurons are silenced. At test time, all 1024 neurons participate."
    },
    {
        "id": "batch-normalization",
        "topic_id": "dl_norm",
        "topic_label": "Normalization & Regularization (Dropout, LayerNorm)",
        "category": "dl",
        "category_label": "Deep Learning",
        "title": "Batch Normalization (BatchNorm)",
        "raw_sub": "Batch Normalization (Normalizing across mini-batch samples)",
        "definition": "Batch Normalization (Ioffe & Szegedy, 2015) normalizes layer inputs across all samples in the current mini-batch to zero mean and unit variance, followed by learned affine scaling $\\gamma$ and shifting $\\beta$.",
        "formula": "$$\\hat{x}_i = \\frac{x_i - \\mu_B}{\\sqrt{\\sigma_B^2 + \\epsilon}}, \\quad y_i = \\gamma \\hat{x}_i + \\beta$$",
        "formula_explanation": "$\\mu_B$ and $\\sigma_B^2$ are computed across the mini-batch dimension $B$. $\\gamma$ and $\\beta$ are learnable parameters that allow the network to recover the original representation if optimal.",
        "logic": "BatchNorm smoothens the loss optimization landscape and reduces internal covariate shift, allowing significantly higher learning rates and acting as a mild regularizer in Convolutional Neural Networks.",
        "example": "Used extensively in CNN vision backbones (ResNet, EfficientNet). However, BatchNorm degrades if batch sizes are very small ($B < 8$) and is unsuitable for autoregressive sequence models."
    },
    {
        "id": "layer-normalization",
        "topic_id": "dl_norm",
        "topic_label": "Normalization & Regularization (Dropout, LayerNorm)",
        "category": "dl",
        "category_label": "Deep Learning",
        "title": "Layer Normalization (LayerNorm)",
        "raw_sub": "Layer Normalization (Normalizing across feature dimensions per token)",
        "definition": "Layer Normalization (Ba, Kiros & Hinton, 2016) computes mean and variance statistics across all feature/channel dimensions of a single sample or token independently, making it completely independent of mini-batch size.",
        "formula": "$$\\mu_L = \\frac{1}{D}\\sum_{k=1}^{D} x_k, \\quad \\sigma_L^2 = \\frac{1}{D}\\sum_{k=1}^{D} (x_k - \\mu_L)^2, \\quad \\hat{x}_k = \\frac{x_k - \\mu_L}{\\sqrt{\\sigma_L^2 + \\epsilon}}, \\quad y_k = \\gamma_k \\hat{x}_k + \\beta_k$$",
        "formula_explanation": "$D$ is the embedding dimension (e.g. 4096), and $\\gamma, \\beta \\in \\mathbb{R}^D$ are learnable scale and bias vectors.",
        "logic": "Because statistics are calculated independently for each sequence token, LayerNorm functions identically during training and single-token autoregressive generation, making it the foundational norm for Transformers.",
        "example": "Every Transformer sub-block (Multi-Head Attention and MLP) wraps around LayerNorm in pre-norm configuration: $x_{out} = x + \\text{SubBlock}(\\text{LayerNorm}(x))$."
    },
    {
        "id": "rmsnorm",
        "topic_id": "dl_norm",
        "topic_label": "Normalization & Regularization (Dropout, LayerNorm)",
        "category": "dl",
        "category_label": "Deep Learning",
        "title": "RMSNorm (Root Mean Square Normalization)",
        "raw_sub": "RMSNorm (Lightweight LayerNorm used in Llama models)",
        "definition": "RMSNorm (Zhang & Sennrich, 2019) simplifies LayerNorm by enforcing root mean square scaling without centering inputs to zero mean. It eliminates mean calculation and bias addition, saving 10% to 50% GPU memory overhead.",
        "formula": "$$\\text{RMS}(\\mathbf{x}) = \\sqrt{\\frac{1}{D} \\sum_{i=1}^{D} x_i^2 + \\epsilon}, \\quad \\bar{x}_i = \\frac{x_i}{\\text{RMS}(\\mathbf{x})}, \\quad y_i = \\gamma_i \\bar{x}_i$$",
        "formula_explanation": "No $\\mu$ computation and no subtractive offset. Scaling vector $\\boldsymbol{\\gamma}$ is the only learned parameter.",
        "logic": "Ablation studies proved that the primary regularizing benefit of LayerNorm comes from scaling invariance rather than mean-shifting. Dropping mean re-centering saves two reduction kernel passes in CUDA.",
        "example": "Adopted by modern open-source foundation models including Meta's LLaMA 1/2/3, Mistral 7B, Gemma, and DeepSeek for optimal token throughput."
    },
    {
        "id": "weight-decay-regularization",
        "topic_id": "dl_norm",
        "topic_label": "Normalization & Regularization (Dropout, LayerNorm)",
        "category": "dl",
        "category_label": "Deep Learning",
        "title": "Weight Decay in Deep Learning",
        "raw_sub": "Weight Decay (L2 penalty directly integrated into parameter updates)",
        "definition": "Weight decay is a parameter shrinkage technique that subtracts a small fixed percentage of each weight during every gradient update, preventing weights from growing excessively large and encouraging smooth decision surfaces.",
        "formula": "$$\\mathbf{w}_{t+1} = (1 - \\eta \\lambda) \\mathbf{w}_t - \\eta \\nabla_{\\mathbf{w}} \\mathcal{L}$$",
        "formula_explanation": "$\\eta$ is the learning rate and $\\lambda$ is the weight decay coefficient (commonly $0.01$ to $0.1$). $(1 - \\eta \\lambda)$ causes idle weights with zero gradients to decay exponentially toward zero.",
        "logic": "Under standard SGD, weight decay is mathematically equivalent to L2 penalty on loss $\\mathcal{L} + \\frac{\\lambda}{2}\\|\\mathbf{w}\\|^2$. Under adaptive optimizers like Adam, they diverge; true weight decay must be applied directly as in AdamW.",
        "example": "Training an image vision backbone: setting `weight_decay = 1e-4` prevents convolutional filters from blowing up on rare training artifacts, improving out-of-distribution test accuracy."
    }
]

if __name__ == "__main__":
    print(f"Loaded {len(DL_CONCEPTS)} Deep Learning concepts successfully.")
