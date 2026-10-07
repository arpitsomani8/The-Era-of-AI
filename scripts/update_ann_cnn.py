import json

# 1. Update concepts.json
with open('src/data/concepts.json', 'r', encoding='utf-8') as f:
    concepts = json.load(f)

for c in concepts:
    if c['id'] == 'artificial-neurons-perceptrons':
        c['title'] = 'Artificial Neural Networks (ANN & Perceptrons)'
        c['raw_subtopic'] = 'Artificial Neural Networks (ANN & Perceptrons)'
        c['raw_sub'] = 'Artificial Neural Networks (ANN & Perceptrons)'
        c['topic_label'] = 'Artificial Neural Networks (ANN) & Hidden Layers'
        c['def'] = 'An Artificial Neural Network (ANN) is a computational model inspired by biological brains, structured as interconnected layers of artificial neurons (perceptrons) that map inputs to outputs via weighted sums and non-linear activations.'
        c['formula'] = r"z = \sum_{j=1}^d w_j x_j + b = \mathbf{w}^T \mathbf{x} + b, \quad a = \sigma(z)"
        c['logic'] = 'Biological brains learn by adjusting synaptic connection strengths between neurons. In an ANN, learnable numerical weights (w) and biases (b) replace biological synapses, while non-linear activation functions (sigma) decide whether and how strongly each artificial neuron fires.'
        c['example'] = 'Multi-tenant credit scoring and loan risk assessment where an ANN processes hundreds of customer financial indicators simultaneously to predict default probability.'
        c['tags'] = ['ANN', 'Artificial Neural Network', 'Deep Learning', 'Perceptron', 'Multi-Layer Perceptron', 'Hidden Layers']
        c['core_terms'] = [
            {
                "term": "Artificial Neural Network (ANN)",
                "what_is_it": "A multi-layered network of artificial processing nodes that learns complex patterns and non-linear functions from data through training.",
                "analogy": "An interconnected team of analysts where entry-level staff process raw facts and pass summary insights to senior managers for final decisions.",
                "why_it_matters": "The foundational bedrock of all modern deep learning, computer vision, and generative foundation models."
            },
            {
                "term": "Artificial Neuron (Perceptron)",
                "what_is_it": "The basic computational building block that takes inputs, multiplies them by weights, adds a bias offset, and applies an activation function.",
                "analogy": "A decision maker weighing multiple pros and cons before deciding whether to take an umbrella.",
                "why_it_matters": "Enables computing linear decision boundaries in feature space."
            },
            {
                "term": "Synaptic Weights & Bias",
                "what_is_it": "Weights (w) represent the strength/importance of an input connection; bias (b) is an adjustable threshold offset independent of inputs.",
                "analogy": "The volume knob on individual instruments (weights) and the master baseline volume setting (bias).",
                "why_it_matters": "The actual parameters adjusted during backpropagation via gradient descent to train the model."
            },
            {
                "term": "Non-Linear Activation Function",
                "what_is_it": "A mathematical curve (e.g. ReLU, GELU, Sigmoid) applied to the neuron's weighted sum to introduce non-linearity.",
                "analogy": "An on/off trigger switch that only fires once a certain threshold of electrical current is reached.",
                "why_it_matters": "Without non-linear activations, stacking 100 neural layers mathematically collapses into a single boring linear equation."
            }
        ]
        c['key_takeaways'] = [
            "An Artificial Neural Network (ANN) consists of input, hidden, and output layers of interconnected neurons.",
            "Each neuron computes z = w^T x + b, followed by a non-linear activation a = sigma(z).",
            "Non-linear activation functions are mandatory; otherwise, multi-layer networks collapse into simple linear regression."
        ]
        c['definition_bullets'] = [
            "**Core Architecture:** Layered graph of mathematical neurons connected by adjustable synaptic weights.",
            "**Forward Equation:** Computes linear combination z = w^T x + b, then applies non-linear activation a = sigma(z).",
            "**Foundation of AI:** Forms the core substrate upon which CNNs, RNNs, and Transformers are constructed."
        ]

    elif c['id'] == 'convolutions-kernels-stride-padding':
        c['title'] = 'Convolutional Neural Networks (CNN & Feature Extraction)'
        c['raw_subtopic'] = 'Convolutional Neural Networks (CNN & Feature Extraction)'
        c['raw_sub'] = 'Convolutional Neural Networks (CNN & Feature Extraction)'
        c['topic_label'] = 'Convolutional Neural Networks (CNN) & Vision Transformers'
        c['def'] = 'A Convolutional Neural Network (CNN) is a deep neural network tailored for grid-like data (images, video, spectrograms) that uses learnable spatial filters (kernels) to automatically detect visual hierarchies from simple edges to complex objects.'
        c['formula'] = r"S(i, j) = (I * K)(i, j) = \sum_{m} \sum_{n} I(i - m, j - n) K(m, n)"
        c['logic'] = 'Fully connected ANNs fail on high-resolution images because a 1000x1000 pixel image creates millions of weights, causing massive overfitting. CNNs solve this via local receptive fields and parameter sharing (the exact same 3x3 filter slides across the entire image).'
        c['example'] = 'Automated medical diagnosis detecting micro-fractures in high-resolution digital X-rays with millimeter precision.'
        c['tags'] = ['CNN', 'Convolutional Neural Network', 'Computer Vision', 'Kernels', 'Filters', 'Feature Maps', 'Deep Learning']
        c['core_terms'] = [
            {
                "term": "Convolutional Neural Network (CNN)",
                "what_is_it": "A specialized neural network architecture that extracts hierarchical spatial patterns from images using convolutional sliding filters.",
                "analogy": "A detective scanning a crime scene with a magnifying glass, noting clues box by box.",
                "why_it_matters": "Dominates computer vision, medical imaging, autonomous vehicle perception, and visual quality inspection."
            },
            {
                "term": "Convolutional Kernel / Filter",
                "what_is_it": "A small learnable matrix of weights (typically 3x3 or 5x5) that slides over the image computing element-wise dot products.",
                "analogy": "A stencil or magnifying stamp designed to glow whenever it slides over a specific shape like a vertical edge or diagonal line.",
                "why_it_matters": "Extracts low-level textures, horizontal edges, circular curves, and high-level visual features."
            },
            {
                "term": "Parameter Sharing",
                "what_is_it": "The engineering principle where the same filter weights are reused across every single spatial position of the input grid.",
                "analogy": "Using one metal coin detector to scan an entire beach rather than burying 10,000 separate sensors.",
                "why_it_matters": "Drastically slashes the parameter count from billions down to thousands, eliminating overfitting."
            },
            {
                "term": "Translation Invariance",
                "what_is_it": "The property that a visual feature (e.g. an eye, a wheel, or a crack) is recognized regardless of where it appears in the frame.",
                "analogy": "Recognizing a stop sign whether it stands on the left sidewalk or the right shoulder of the road.",
                "why_it_matters": "Allows models to generalize to objects positioned anywhere in the camera field of view."
            }
        ]
        c['key_takeaways'] = [
            "CNNs use learnable sliding kernels to extract spatial feature maps from 2D and 3D grid data.",
            "Parameter sharing and local receptive fields reduce parameter counts by 99.9% compared to dense ANNs.",
            "Hierarchical feature representation: early layers detect edges; middle layers detect textures; deep layers recognize full objects."
        ]
        c['definition_bullets'] = [
            "**Core Architecture:** Spatial filter convolutions combined with activation and pooling layers.",
            "**Convolution Operation:** (I * K)(i, j) computes sliding inner products across the image plane.",
            "**Visual Inductive Bias:** Translation invariance and local spatial connectivity make CNNs the premier visual architecture."
        ]

# Also update topic_label on any sibling concepts in those two topics
for c in concepts:
    if c['topic_id'] == 'dl_neurons':
        c['topic_label'] = 'Artificial Neural Networks (ANN) & Hidden Layers'
    elif c['topic_id'] == 'dl_vision':
        c['topic_label'] = 'Convolutional Neural Networks (CNN) & Vision Transformers'

with open('src/data/concepts.json', 'w', encoding='utf-8') as f:
    json.dump(concepts, f, indent=2, ensure_ascii=False)

print("Updated concepts.json for ANN and CNN!")

# 2. Update topics.json
with open('src/data/topics.json', 'r', encoding='utf-8') as f:
    topics = json.load(f)

for t in topics:
    if t['id'] == 'dl_neurons':
        t['label'] = 'Artificial Neural Networks (ANN) & Hidden Layers'
        t['subtopics'] = [c['title'] for c in concepts if c['topic_id'] == 'dl_neurons']
    elif t['id'] == 'dl_vision':
        t['label'] = 'Convolutional Neural Networks (CNN) & Vision Transformers'
        t['subtopics'] = [c['title'] for c in concepts if c['topic_id'] == 'dl_vision']

with open('src/data/topics.json', 'w', encoding='utf-8') as f:
    json.dump(topics, f, indent=2, ensure_ascii=False)

print("Updated topics.json for ANN and CNN!")

# 3. Update allNodes.json
with open('src/data/allNodes.json', 'r', encoding='utf-8') as f:
    nodes = json.load(f)

for n in nodes:
    if n['id'] == 'dl_neurons':
        n['label'] = 'Artificial Neural Networks (ANN) & Hidden Layers'
        n['subtopics'] = [c['title'] for c in concepts if c['topic_id'] == 'dl_neurons']
    elif n['id'] == 'dl_vision':
        n['label'] = 'Convolutional Neural Networks (CNN) & Vision Transformers'
        n['subtopics'] = [c['title'] for c in concepts if c['topic_id'] == 'dl_vision']

with open('src/data/allNodes.json', 'w', encoding='utf-8') as f:
    json.dump(nodes, f, indent=2, ensure_ascii=False)

print("Updated allNodes.json for ANN and CNN!")
