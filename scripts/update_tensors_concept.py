import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
CONCEPTS_PATH = os.path.join(ROOT_DIR, "src", "data", "concepts.json")
ALL_CONCEPTS_PATH = os.path.join(SCRIPT_DIR, "data_sources", "all_concepts.json")
MATH_PY = os.path.join(SCRIPT_DIR, "data_sources", "concepts_math.py")

tensors_concept = {
    "id": "concept_tensors",
    "title": "Tensors & Multidimensional Arrays",
    "topic_id": "math_linalg",
    "topic_label": "Linear Algebra & Vector Spaces",
    "category": "math",
    "category_label": "Mathematical Foundations",
    "raw_subtopic": "Tensors (Multidimensional arrays for batches and images)",
    "def": "A tensor is the mathematical generalization of scalars, vectors, and matrices to any number of dimensions, serving as the universal data structure of deep learning.",
    "formula": "$$\\mathcal{T} \\in \\mathbb{R}^{B \\times C \\times H \\times W}, \\quad \\text{Total Elements} = \\prod_{i=1}^R d_i$$",
    "logic": "In modern AI, neural networks are pipelines that take in tensors, transform and reshape them across layers, and output new tensors. All inputs, model weights, and gradients are represented as tensors.",
    "example": "A batch of RGB images stored as a 4D tensor with shape (64, 3, 224, 224) representing 64 images, 3 color channels, 224px height, and 224px width.",
    "tags": [
        "Tensors",
        "PyTorch",
        "Broadcasting",
        "Deep Learning Data",
        "GPU Acceleration",
        "Linear Algebra"
    ],
    "raw_sub": "Tensors (Multidimensional arrays for batches and images)",
    "definition": "A tensor is the generalization of scalars, vectors, and matrices to any number of dimensions. A matrix is simply a 2D tensor, and every neural network is a tensor transformation pipeline.",
    "formula_explanation": "A tensor of rank R has a shape tuple (d₁, d₂, ..., d_R). Total elements stored equals d₁ × d₂ × ... × d_R. Tensor operations execute in parallel across GPU threads.",
    "simple_summary": "Tensors are the universal currency of AI. From a single number (0D scalar) to video batches (5D cubes of cubes), all data, model weights, and gradients are stored and multiplied as tensors on GPUs.",
    "core_terms": [
        {
            "term": "Tensor (The Universal Container)",
            "what_is_it": "• The mathematical generalization of scalars, vectors, and matrices to any number of dimensions.\n• A matrix is simply a 2D tensor—a tensor is not necessarily 3D or higher, but can span 0, 1, 2, 3, or N dimensions.",
            "analogy": "0D is a single point (scalar), 1D is a line of points (vector), 2D is a flat sheet of paper (matrix), 3D is a cube of numbers, and 4D/5D are albums or videos of cubes.",
            "why_it_matters": "Every modern neural network is a pipeline that ingests tensors, reshapes and multiplies them, and outputs predictions."
        },
        {
            "term": "Tensor Attributes (Rank, Shape, dtype)",
            "what_is_it": "• Rank (ndim): The number of dimensions or axes (e.g., scalar = 0, vector = 1, matrix = 2).\n• Shape: A tuple showing the size along each axis (e.g., (32, 3, 224, 224)).\n• Data Type (dtype): The numerical format stored inside (e.g., float32, bfloat16, int64).",
            "analogy": "Think of a shipping crate: Rank is whether it's a line, shelf, or grid of boxes; Shape is the exact count (depth × height × width); dtype is what's inside (glass, wood, or steel).",
            "why_it_matters": "Shape mismatches cause over 90% of all deep learning bugs; mastering tensor dimensions prevents pipeline errors."
        },
        {
            "term": "PyTorch Tensors vs. NumPy Arrays",
            "what_is_it": "• GPU/TPU Acceleration: NumPy runs only on CPUs, while PyTorch tensors can run directly on GPUs for 100x–1,000x faster matrix math.\n• Autograd (Automatic Differentiation): Tensors track every mathematical operation in a computational graph, enabling automatic gradient calculation via loss.backward().",
            "analogy": "NumPy is a reliable bicycle on a dirt road (CPU); PyTorch is a supersonic jet (GPU) with autopilot tracking every maneuver (Autograd).",
            "why_it_matters": "Enables training massive multi-billion parameter neural networks that would take decades on traditional CPU arrays."
        }
    ],
    "types_header": "How Real-World Data is Stored as Tensors",
    "types_badge": "Standard AI Shapes",
    "quick_types": [
        {
            "type": "Tabular Data (2D)",
            "definition": "Shape: (Batch_Size, Features) — rows of independent data records.",
            "looks_like": "64 patients, 10 medical tests each: (64, 10)"
        },
        {
            "type": "Text / NLP (3D)",
            "definition": "Shape: (Batch_Size, Sequence_Length, Embedding_Dim) — sequences of word vectors.",
            "looks_like": "32 sentences, 128 tokens, 768-dim embeddings: (32, 128, 768)"
        },
        {
            "type": "Audio & Sensors (3D)",
            "definition": "Shape: (Batch_Size, Time_Steps, Channels) — continuous audio or sensor readings.",
            "looks_like": "16 audio clips, 44,100 samples, 2 channels (stereo): (16, 44100, 2)"
        },
        {
            "type": "Color Images (4D)",
            "definition": "Shape: (Batch_Size, Channels, Height, Width) — batch of RGB image grids (NCHW).",
            "looks_like": "64 images, 3 RGB channels, 224×224 pixels: (64, 3, 224, 224)"
        },
        {
            "type": "Video Clips (5D)",
            "definition": "Shape: (Batch_Size, Frames, Channels, Height, Width) — temporal image sequences.",
            "looks_like": "8 clips, 30 frames, 3 RGB channels, 128×128: (8, 30, 3, 128, 128)"
        }
    ],
    "symbol_guide": [
        {
            "symbol": "T (𝒯)",
            "meaning": "Multidimensional Tensor",
            "plain_english": "The N-dimensional data container holding numerical values"
        },
        {
            "symbol": "B, C, H, W",
            "meaning": "4D Tensor Axes (Batch, Channels, Height, Width)",
            "plain_english": "Standard CV layout: B images, C color channels, H pixels high, W pixels wide"
        },
        {
            "symbol": "R",
            "meaning": "Rank of the tensor",
            "plain_english": "Total number of axes or dimensions (e.g., R = 4 for a batch of images)"
        },
        {
            "symbol": "dᵢ",
            "meaning": "Axis dimension size",
            "plain_english": "The size or count along the i-th axis (e.g., d₁ = B, d₂ = C, etc.)"
        },
        {
            "symbol": "∏ (Capital Pi)",
            "meaning": "Product over all dimensions",
            "plain_english": "Multiplies all axis sizes together (d₁ × d₂ × ... × d_R) to get total elements in memory"
        }
    ],
    "numerical_example": "Understanding Tensor Shapes & Broadcasting:\n\n1. Mini-Batch Matrix (4 samples, 3 features):\n   X = [[ 1,  2,  3],\n        [ 4,  5,  6],\n        [ 7,  8,  9],\n        [10, 11, 12]]   --> Shape: (4, 3)\n\n2. Bias Vector (3 features):\n   b = [10, 20, 30]     --> Shape: (3,)\n\n3. Broadcasting in Action (X + b):\n   Vector b automatically stretches across all 4 sample rows without allocating extra memory:\n   Result = [[ 1+10,  2+20,  3+30],   =  [[11, 22, 33],\n             [ 4+10,  5+20,  6+30],       [14, 25, 36],\n             [ 7+10,  8+20,  9+30],       [17, 28, 39],\n             [10+10, 11+20, 12+30]]       [20, 31, 42]]\n   --> Final Shape: (4, 3)",
    "pitfalls": "Common Trap: Dimension mismatches when multiplying or passing tensors into linear layers. Remember: Conv2D outputs 4D tensors (B, C, H, W) which must be flattened (or pooled) to 2D (B, Features) before entering Dense/Linear layers.",
    "core_logic": "Deep learning models compute on contiguous multi-dimensional memory blocks. Tensor broadcasting allows operations across tensors of mismatched shapes without redundant memory allocations.",
    "architectural_logic": "Modern deep learning architectures (Transformers, CNNs) are built around tensor shape contracts. Attention mechanisms perform batched matrix multiplications across (Batch, Heads, Seq_Len, Head_Dim) 4D tensors, requiring strict dimensional alignment at every step.",
    "connected_logic": [
        {
            "title": "The Universal Batch Dimension (GPU Parallelism)",
            "content": "• The first dimension in AI tensors is almost always Batch_Size (e.g., 32, 64, 128).\n• Neural networks rarely process single items—they bundle samples so Nvidia GPU tensor cores can execute thousands of multiplications in parallel."
        },
        {
            "title": "Tensor Surgery: Reshape, Squeeze & Permute",
            "content": "• reshape / view: Alters dimension layout without copying memory (e.g. flattening (28, 28) image to (784,)).\n• squeeze / unsqueeze: Removes or adds dummy dimensions of size 1 (e.g., (10,) → unsqueeze(0) → (1, 10)).\n• permute: Rearranges axis ordering (e.g. swapping OpenCV (H, W, C) to PyTorch (C, H, W))."
        },
        {
            "title": "Broadcasting: Zero-Copy Mathematical Magic",
            "content": "• Operates seamlessly between tensors of different ranks (e.g. adding a (3,) bias vector to a (4, 3) matrix).\n• Stretches the smaller tensor along missing dimensions without allocating extra RAM, allowing fast batch arithmetic."
        },
        {
            "title": "Why Deep Learning Demands Tensors Over NumPy",
            "content": "• GPU Acceleration: Tensors reside in GPU VRAM, multiplying billions of parameters at teraflop speeds.\n• Autograd: Tensors record every forward operation in a computational graph so loss.backward() automatically calculates weight gradients."
        }
    ],
    "key_takeaways": [
        "A tensor is an N-dimensional array: 0D = scalar, 1D = vector, 2D = matrix, 3D+ = higher tensors.",
        "Every tensor has 3 core attributes: Rank (axes count), Shape (sizes tuple), and dtype (numerical format).",
        "The first dimension is almost always Batch_Size to maximize GPU parallel execution.",
        "Broadcasting allows math between different shapes without copying data in memory.",
        "PyTorch Tensors = NumPy arrays + GPU hardware acceleration + Automatic differentiation (Autograd)."
    ],
    "definition_bullets": [
        "Tensor: Multi-dimensional array generalizing scalars, vectors, and matrices to any rank.",
        "Rank & Shape: Rank is axis count; Shape specifies size along each axis (e.g. (B, C, H, W)).",
        "PyTorch vs NumPy: GPU parallel processing and automatic gradient tracking (Autograd)."
    ]
}

# 1. Update src/data/concepts.json
with open(CONCEPTS_PATH, 'r', encoding='utf-8') as f:
    concepts = json.load(f)

for idx, c in enumerate(concepts):
    if c['id'] == 'concept_tensors':
        concepts[idx] = tensors_concept
        break

with open(CONCEPTS_PATH, 'w', encoding='utf-8') as f:
    json.dump(concepts, f, indent=2, ensure_ascii=False)
print("Updated src/data/concepts.json for concept_tensors successfully!")

# 2. Update scripts/data_sources/all_concepts.json
if os.path.exists(ALL_CONCEPTS_PATH):
    with open(ALL_CONCEPTS_PATH, 'r', encoding='utf-8') as f:
        all_concepts = json.load(f)
    for idx, c in enumerate(all_concepts):
        if c['id'] == 'concept_tensors':
            all_concepts[idx] = tensors_concept
            break
    with open(ALL_CONCEPTS_PATH, 'w', encoding='utf-8') as f:
        json.dump(all_concepts, f, indent=2, ensure_ascii=False)
    print("Updated scripts/data_sources/all_concepts.json successfully!")

# 3. Update concepts_math.py
if os.path.exists(MATH_PY):
    import importlib.util
    spec = importlib.util.spec_from_file_location("concepts_math", MATH_PY)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    math_concepts = mod.MATH_CONCEPTS
    for idx, c in enumerate(math_concepts):
        if c['id'] == 'concept_tensors':
            math_concepts[idx] = tensors_concept
            break
    with open(MATH_PY, "w", encoding="utf-8") as f:
        f.write('"""\nConcepts Database: Mathematical Foundations (19 Concepts)\n"""\n\nMATH_CONCEPTS = ' + json.dumps(math_concepts, indent=4, ensure_ascii=False) + '\n')
    print("Updated concepts_math.py successfully!")
