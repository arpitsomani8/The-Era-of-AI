import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
CONCEPTS_PATH = os.path.join(ROOT_DIR, "src", "data", "concepts.json")
ALL_CONCEPTS_PATH = os.path.join(SCRIPT_DIR, "data_sources", "all_concepts.json")
MATH_PY = os.path.join(SCRIPT_DIR, "data_sources", "concepts_math.py")

enriched_concept = {
    "id": "concept_dot_product_cosine",
    "title": "Vectors, Dot Products & Cosine Similarity",
    "topic_id": "math_linalg",
    "topic_label": "Linear Algebra & Vector Spaces",
    "category": "math",
    "category_label": "Mathematical Foundations",
    "raw_subtopic": "Vectors, Dot Products & Geometric Cosine Similarity",
    "def": "A vector is an ordered list of numbers representing a point or direction in multi-dimensional space. The dot product sums the products of corresponding elements, and cosine similarity measures the directional alignment between two vectors regardless of magnitude.",
    "formula": "$$u \\cdot v = \\sum_{i=1}^d u_i v_i = \\|u\\| \\|v\\| \\cos(\\theta), \\quad \\text{Cosine Similarity} = \\frac{u \\cdot v}{\\|u\\|_2 \\|v\\|_2} = \\frac{\\sum u_i v_i}{\\sqrt{\\sum u_i^2} \\sqrt{\\sum v_i^2}}$$",
    "logic": "When comparing high-dimensional embeddings (e.g., text, images), Euclidean distance is heavily sensitive to document length or feature magnitude. Cosine similarity normalizes length away, isolating pure semantic orientation.",
    "example": "Comparing search queries: Query vector for 'electric car' [0.9, 0.1, 0.8] and document vector for 'Tesla EV vehicle' [0.85, 0.05, 0.75] produce a cosine similarity of 0.998, indicating near-perfect topical alignment.",
    "tags": [
        "Vectors",
        "Linear Algebra",
        "Cosine Similarity",
        "Embeddings",
        "Dot Product",
        "Vector Space"
    ],
    "raw_sub": "Vectors, Dot Products & Geometric Cosine Similarity",
    "definition": "A vector is an ordered list of numbers representing a point or direction in multi-dimensional space. The dot product sums the products of corresponding elements, and cosine similarity measures the directional alignment between two vectors regardless of magnitude.",
    "formula_explanation": "",
    "simple_summary": "Think of vectors as arrows pointing in space, the dot product as a tool to measure how much two arrows point in the same direction, and cosine similarity as a score from -1 to +1 that measures alignment while ignoring arrow length.",
    "core_terms": [
        {
            "term": "Vector",
            "what_is_it": "• A list of numbers that describes something. In AI, every piece of data (words, images, house prices, audio) is converted into a vector (a numerical representation that an ML model can process and compare).\n• In AI, when text or concepts are converted into vectors in continuous space, that vector representation is called an embedding.",
            "analogy": "A GPS coordinate (latitude, longitude) is a 2D vector. A house profile [3 bedrooms, 2 bathrooms, 1500 sqft, $350k] is a 4D vector.",
            "why_it_matters": "Computers cannot read text or look at images directly; they only understand numbers arranged in vectors."
        },
        {
            "term": "Dot Product",
            "what_is_it": "• A math operation where you multiply matching numbers from two vectors and add them up.\n• It tells you whether two vectors push in the same direction, push against each other, or are completely unrelated.",
            "analogy": "If you and a friend push a heavy cart in the exact same direction, your combined effort is high (positive dot product). If you push in opposite directions, you cancel out (negative). If you push at a 90° right angle, your push doesn't help your friend at all (zero dot product).",
            "why_it_matters": "It is the core building block of AI neural networks, attention mechanisms, and feature matching."
        },
        {
            "term": "Cosine Similarity",
            "what_is_it": "• A similarity score between -1 and +1 that measures only the angle (direction) between two vectors.\n• It completely ignores vector length or size, evaluating pure directional alignment.",
            "analogy": "A short 1-sentence tweet and a 20-page article about 'quantum computing' both talk about the same topic. Their vectors point in the same direction. Cosine similarity recognizes they are 99% identical in topic, even though the 20-page article has much larger numbers because it has more words.",
            "why_it_matters": "Essential for search engines, recommendation systems, and Vector Databases (RAG) to find related content fairly without favoring long documents."
        }
    ],
    "types_of_vectors": [
        {
            "type": "Row Vector",
            "definition": "A 1D vector written horizontally as a single row.",
            "looks_like": "[x₁, x₂, x₃] (shape: 1 × 3, e.g. [2, 5, 8])"
        },
        {
            "type": "Column Vector",
            "definition": "A 1D vector written vertically (the standard default in AI math & neural networks).",
            "looks_like": "[[x₁], [x₂], [x₃]] (shape: 3 × 1)"
        },
        {
            "type": "Dense Vector",
            "definition": "Most or all numbers are non-zero real values; stores rich meaning in compact size.",
            "looks_like": "[0.42, -0.89, 0.15, 0.77] (e.g. 1536-dim embedding)"
        },
        {
            "type": "Sparse Vector",
            "definition": "Most numbers are zeros; only a few positions have values.",
            "looks_like": "[0, 0, 1, 0, 0, 0, 0] (e.g. One-Hot, TF-IDF)"
        },
        {
            "type": "Zero Vector",
            "definition": "All elements are zero; represents the center origin with zero magnitude.",
            "looks_like": "[0, 0, 0, 0]"
        },
        {
            "type": "Unit Vector",
            "definition": "A vector normalized so its total length/magnitude is exactly 1 (pure direction).",
            "looks_like": "||v|| = 1.0 (e.g. [0.6, 0.8])"
        },
        {
            "type": "Orthogonal Vectors",
            "definition": "Two vectors meeting at a 90° angle whose dot product is exactly 0 (completely unrelated).",
            "looks_like": "[1, 0] · [0, 1] = 0 (perpendicular)"
        },
        {
            "type": "Feature Vector vs. Embedding Vector",
            "definition": "Feature vectors are raw measured attributes; Embeddings are learned by neural nets to capture conceptual meaning.",
            "looks_like": "[age=28, salary=65k] vs. [0.21, -0.45, 0.82]"
        }
    ],
    "symbol_guide": [
        {
            "symbol": "u, v",
            "meaning": "Two vectors (lists of numbers) being compared",
            "plain_english": "e.g. vector u = [1, 2] and vector v = [3, 4]"
        },
        {
            "symbol": "u · v",
            "meaning": "The dot product of u and v",
            "plain_english": "Multiply pairs and add: (1×3) + (2×4) = 11"
        },
        {
            "symbol": "∑ u_i v_i",
            "meaning": "Sum of products across all dimensions i",
            "plain_english": "Loop through all numbers in the list and multiply matching positions"
        },
        {
            "symbol": "||u||_2",
            "meaning": "The Euclidean length (magnitude) of vector u",
            "plain_english": "Square each number, sum them up, and take the square root (Pythagorean theorem)"
        },
        {
            "symbol": "θ (theta)",
            "meaning": "The angle between the two arrows in space",
            "plain_english": "0° means identical direction, 90° means perpendicular (unrelated), 180° means opposite"
        },
        {
            "symbol": "cos(θ)",
            "meaning": "Cosine of the angle (Cosine Similarity)",
            "plain_english": "+1.0 = identical direction, 0.0 = completely unrelated, -1.0 = exact opposite"
        }
    ],
    "numerical_example": "Let Vector A = [1, 2] and Vector B = [3, 4].\n1. Multiply matching positions: (1 × 3) = 3 and (2 × 4) = 8.\n2. Dot Product: 3 + 8 = 11.\n3. Length of A: √(1² + 2²) = √(1 + 4) = √5 ≈ 2.236.\n4. Length of B: √(3² + 4²) = √(9 + 16) = √25 = 5.0.\n5. Cosine Similarity: 11 / (2.236 × 5.0) = 11 / 11.18 = 0.984.\nConclusion: 0.984 is very close to 1.0, showing both vectors point in almost the exact same direction!",
    "pitfalls": "Common Pitfall: Don't confuse Dot Product with Cosine Similarity! If you duplicate words in a document, its vector length doubles, which doubles the dot product, but its cosine similarity stays exactly the same because the direction didn't change.",
    "core_logic": "When comparing high-dimensional embeddings (e.g., text, images), Euclidean distance is heavily sensitive to document length or feature magnitude. Cosine similarity normalizes length away, isolating pure semantic orientation.",
    "architectural_logic": "When comparing high-dimensional embeddings (e.g., text, images), Euclidean distance is heavily sensitive to document length or feature magnitude. Cosine similarity normalizes length away, isolating pure semantic orientation.",
    "connected_logic": [
        {
            "title": "Scalar vs. Vector vs. Matrix vs. Tensor (The Hierarchy)",
            "content": "• Scalar (0D): A single isolated number.\n   Example: Learning rate η = 0.001, loss = 0.42, temperature = 0.7\n• Vector (1D): A 1D list of numbers.\n   Example: Word embedding vector of shape [768]\n• Matrix (2D): A 2D table/grid with rows and columns.\n   Example: Neural layer weight matrix W of shape [128, 64]\n• Tensor (ND, N ≥ 3): A multi-dimensional array.\n   Example: A batch of 32 images [32, 3, 224, 224] (Batch × Channels × Height × Width)"
        },
        {
            "title": "Dense Vector vs. Sparse Vector (Key Difference)",
            "content": "• Sparse Vector: Huge dimension (e.g., 50,000 words in a dictionary), but 99.9% of entries are zeros. Great for exact keyword search (TF-IDF, BM25, SPLADE), but wastes memory if stored naively and doesn't understand synonyms.\n• Dense Vector: Compact dimension (e.g., 768 or 1536 numbers), almost all non-zero floats. Learned by neural nets to capture semantic meaning (e.g., understands 'king' is related to 'queen' even if the words look different)."
        },
        {
            "title": "Vector Norm / Magnitude & Distance Metrics",
            "content": "• Vector Norm / Magnitude (Length from origin):\n   ├── Euclidean Norm (L₂): Straight-line length: ||v||₂ = √(v₁² + v₂² + ...)\n   └── Manhattan Norm (L₁): Sum of absolute values: ||v||₁ = |v₁| + |v₂| + ...\n• Distance (Dissimilarity between two points):\n   ├── Euclidean Distance (L₂): Direct straight-line distance: d(u, v) = √(∑(u_i - v_i)²). Highly sensitive to vector length.\n   └── Manhattan Distance (L₁): Grid / taxicab distance along streets: d(u, v) = ∑|u_i - v_i|."
        },
        {
            "title": "Vector Space & Vector Databases",
            "content": "• Vector Space: The multi-dimensional coordinate space ℝᵈ where all these vectors live and can be compared geometrically.\n• Vector Databases (Pinecone, Milvus, Qdrant, Chroma): Specialized databases engineered to store millions of dense embeddings and find the most similar items in milliseconds using Approximate Nearest Neighbor (ANN) search for RAG systems."
        },
        {
            "title": "Neuron as a Dot Product & Directional Meaning",
            "content": "• An artificial neuron is primarily a dot product of inputs and weights: z = w · x + b = ∑ w_i x_i + b.\n• Dot product formula: A · B = |A| |B| cos(θ), where |A| = length of A, |B| = length of B, and θ = angle between them.\n• The dot product depends on BOTH: (1) The angle/direction between vectors, and (2) Their magnitudes/lengths.\n• When vectors have the same length (or are unit vectors):\n   - Positive and large: Similar direction (θ < 90°, neuron fires strongly)\n   - Around 0: Little/no alignment, orthogonal (θ ≈ 90°, neuron output near bias)\n   - Negative: Opposite direction (θ > 90°, neuron is inhibited)"
        }
    ],
    "key_takeaways": [
        "A vector is a numerical representation of data that an ML model can process and compare; learned representations are called embeddings.",
        "Data hierarchy: Scalar (0D) → Vector (1D) → Matrix (2D) → Tensor (ND).",
        "Dense vectors hold compact semantic meaning; sparse vectors hold mostly zeros for keyword counts.",
        "An artificial neuron is primarily a dot product of inputs and weights: z = w · x + b.",
        "The dot product depends on both angle and magnitude: A · B = |A| |B| cos(θ).",
        "Cosine similarity divides out magnitude to measure pure directional alignment between -1 and +1.",
        "Vector databases index vector spaces to power instant semantic search in RAG."
    ],
    "definition_bullets": [
        "Vector: A list of numbers that describes something. In AI, every piece of data is converted into a vector.",
        "Dot Product: A math operation multiplying matching numbers from two vectors and add them up.",
        "Cosine Similarity: A similarity score between -1 and +1 measuring directional angle while ignoring length."
    ]
}

# 1. Update src/data/concepts.json
with open(CONCEPTS_PATH, 'r', encoding='utf-8') as f:
    concepts = json.load(f)

for idx, c in enumerate(concepts):
    if c['id'] == 'concept_dot_product_cosine':
        concepts[idx] = enriched_concept
        break

with open(CONCEPTS_PATH, 'w', encoding='utf-8') as f:
    json.dump(concepts, f, indent=2, ensure_ascii=False)
print("Updated src/data/concepts.json successfully!")

# 2. Update scripts/data_sources/all_concepts.json
if os.path.exists(ALL_CONCEPTS_PATH):
    with open(ALL_CONCEPTS_PATH, 'r', encoding='utf-8') as f:
        all_concepts = json.load(f)
    for idx, c in enumerate(all_concepts):
        if c['id'] == 'concept_dot_product_cosine':
            all_concepts[idx] = enriched_concept
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
    math_concepts[0] = enriched_concept
    with open(MATH_PY, "w", encoding="utf-8") as f:
        f.write('"""\nConcepts Database: Mathematical Foundations (19 Concepts)\n"""\n\nMATH_CONCEPTS = ' + json.dumps(math_concepts, indent=4, ensure_ascii=False) + '\n')
    print("Updated concepts_math.py successfully!")
