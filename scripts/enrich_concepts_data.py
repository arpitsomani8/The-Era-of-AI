"""
Comprehensive Concept Enrichment Script
Enriches all 170 concepts with:
1. simple_summary: Beginner-friendly plain English summary.
2. core_terms: Array of separate, distinct terms (solving "shrinking all terms into one").
   Each term contains:
     - term: Name of the term
     - what_is_it: Crystal-clear definition in simple words
     - analogy: Relatable everyday real-world analogy
     - why_it_matters: Why this specific term is needed in AI
3. symbol_guide: Explaining all mathematical variables & operators
4. numerical_example: Step-by-step concrete calculation with small numbers
5. pitfalls: Common beginner traps & how to avoid them
"""

import json
import os
import re

CONCEPTS_PATH = os.path.join(os.path.dirname(__file__), "..", "src", "data", "concepts.json")
BACKUP_PATH = os.path.join(os.path.dirname(__file__), "..", "src", "data", "concepts_backup.json")
ALL_CONCEPTS_PATH = os.path.join(os.path.dirname(__file__), "data_sources", "all_concepts.json")

def load_data():
    with open(CONCEPTS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

# Specialized handcrafted enrichments for fundamental & commonly queried concepts
DETAILED_ENRICHMENTS = {
    "concept_dot_product_cosine": {
        "simple_summary": "Think of vectors as arrows in space, the dot product as a way to check if two arrows point in the same direction, and cosine similarity as a score from -1 to +1 that measures alignment while ignoring how long the arrows are.",
        "core_terms": [
            {
                "term": "Vector",
                "what_is_it": "A list of numbers that describes something. In AI, almost everything (words, images, user profiles) is converted into a vector.",
                "analogy": "A GPS coordinate like (latitude, longitude) is a 2D vector. A house profile like [3 bedrooms, 2 bathrooms, 1500 sqft, $400k] is a 4D vector.",
                "why_it_matters": "Computers cannot read text or look at images directly; they only understand numbers arranged in vectors."
            },
            {
                "term": "Dot Product",
                "what_is_it": "A math operation where you multiply matching numbers from two vectors and add them up. It tells you how much two vectors push in the same direction.",
                "analogy": "If you and a friend push a heavy cart in the exact same direction, your combined effort is high (positive dot product). If you push in opposite directions, you cancel out (negative). If you push at a 90° angle, your force doesn't help the other at all (zero dot product).",
                "why_it_matters": "It is the core building block of AI neural networks, attention mechanisms, and feature matching."
            },
            {
                "term": "Cosine Similarity",
                "what_is_it": "A similarity score between -1 and +1 that measures only the angle (direction) between two vectors, completely ignoring their length or size.",
                "analogy": "A short 1-sentence tweet and a 20-page scientific paper about 'black holes' both talk about the same topic. Their vectors point in the same direction. Cosine similarity recognizes they are 99% identical in topic, even though the paper is 1,000 times longer.",
                "why_it_matters": "Essential for search engines, recommendation systems, and Vector Databases (RAG) to find related content fairly without favoring long documents."
            }
        ],
        "symbol_guide": [
            {"symbol": "u, v", "meaning": "Two vectors (lists of numbers) being compared", "plain_english": "e.g. vector u = [1, 2] and vector v = [3, 4]"},
            {"symbol": "u · v", "meaning": "The dot product of u and v", "plain_english": "Multiply pairs and add: (1*3) + (2*4) = 11"},
            {"symbol": "∑ u_i v_i", "meaning": "Sum of products across all dimensions i", "plain_english": "Loop through all numbers in the list and multiply matching positions"},
            {"symbol": "||u||_2", "meaning": "The Euclidean length (magnitude) of vector u", "plain_english": "Square each number, sum them up, and take the square root (Pythagorean theorem)"},
            {"symbol": "θ (theta)", "meaning": "The angle between the two arrows in space", "plain_english": "0° means identical direction, 90° means perpendicular (unrelated), 180° means opposite"},
            {"symbol": "cos(θ)", "meaning": "Cosine of the angle (Cosine Similarity)", "plain_english": "+1.0 = identical direction, 0.0 = completely unrelated, -1.0 = exact opposite"}
        ],
        "numerical_example": "Let Vector A = [1, 2] and Vector B = [3, 4].\n1. Multiply matching positions: (1 × 3) = 3 and (2 × 4) = 8.\n2. Dot Product: 3 + 8 = 11.\n3. Length of A: √(1² + 2²) = √(1 + 4) = √5 ≈ 2.236.\n4. Length of B: √(3² + 4²) = √(9 + 16) = √25 = 5.0.\n5. Cosine Similarity: 11 / (2.236 × 5.0) = 11 / 11.18 = 0.984.\nConclusion: 0.984 is very close to 1.0, showing both vectors point in almost the exact same direction!",
        "pitfalls": "Novice Trap: Don't confuse Dot Product with Cosine Similarity! If you duplicate words in a document, its vector length doubles, which doubles the dot product, but its cosine similarity stays exactly the same because the direction didn't change."
    },
    "concept_matrix_mult_inverses": {
        "simple_summary": "A matrix is a table of numbers. Matrix multiplication transforms or processes data, transposition flips rows into columns, and an inverse matrix acts like an 'Undo' button that reverses a transformation.",
        "core_terms": [
            {
                "term": "Matrix",
                "what_is_it": "A 2D spreadsheet/grid of numbers arranged in rows and columns.",
                "analogy": "A pricing table where rows are products (Apple, Banana) and columns are stores (Store A, Store B).",
                "why_it_matters": "In AI, neural network weights and entire batches of data are stored as matrices."
            },
            {
                "term": "Matrix Multiplication",
                "what_is_it": "A rule for combining two grids by multiplying rows of the first grid by columns of the second grid.",
                "analogy": "Multiplying a grocery shopping list [quantities] by a price catalog [prices per store] to find the total bill at each store in one step.",
                "why_it_matters": "99% of the computational work done inside GPUs during ChatGPT training and inference is matrix multiplication (GEMM)."
            },
            {
                "term": "Transposition (A^T)",
                "what_is_it": "Flipping a matrix across its diagonal so that rows become columns and columns become rows.",
                "analogy": "Rotating a spreadsheet table from wide format to tall format so it aligns with another table.",
                "why_it_matters": "Needed to match dimensions before multiplying vectors or layers."
            },
            {
                "term": "Inverse Matrix (A^-1)",
                "what_is_it": "A reverse matrix that completely undoes what matrix A did, returning back to the original starting values.",
                "analogy": "If matrix A rotates an image 45° clockwise, its inverse matrix A^-1 rotates it 45° counter-clockwise.",
                "why_it_matters": "Used in analytical math solutions (like ordinary least squares regression)."
            }
        ],
        "symbol_guide": [
            {"symbol": "A, B", "meaning": "Input matrices", "plain_english": "A has size (m × k) and B has size (k × n)"},
            {"symbol": "C = AB", "meaning": "Product matrix", "plain_english": "The resulting grid with size (m × n)"},
            {"symbol": "A^T", "meaning": "Transpose of A", "plain_english": "Flip rows and columns: element at (i, j) moves to (j, i)"},
            {"symbol": "A^-1", "meaning": "Inverse of A", "plain_english": "Matrix such that A multiplied by A^-1 equals the identity matrix I"},
            {"symbol": "I", "meaning": "Identity matrix", "plain_english": "A square grid with 1s on the diagonal and 0s everywhere else (like the number 1 for matrices)"}
        ],
        "numerical_example": "Multiply 1x2 vector [2, 3] by 2x2 matrix [[1, 4], [2, 5]]:\n1. First output: (2 × 1) + (3 × 2) = 2 + 6 = 8.\n2. Second output: (2 × 4) + (3 × 5) = 8 + 15 = 23.\nResult: [8, 23]. In one step, both features were transformed simultaneously!",
        "pitfalls": "Common Trap: Matrix multiplication is NOT commutative! A × B is NOT equal to B × A. Order matters fundamentally."
    },
    "concept_eigenvalues_eigenvectors": {
        "simple_summary": "When a matrix stretches, squishes, or rotates a space, eigenvectors are special arrows that do NOT rotate—they only stretch or shrink. The eigenvalue is the number that tells you how much they stretch.",
        "core_terms": [
            {
                "term": "Eigenvector",
                "what_is_it": "A direction in space that stays on its own original line after a matrix transformation is applied.",
                "analogy": "Imagine stretching a rubber sheet diagonally. Most arrows drawn on the sheet will tilt and rotate, but the arrow pointing directly along the stretch axis only gets longer—it never tilts!",
                "why_it_matters": "Identifies the core, natural axes of variation in large complex datasets."
            },
            {
                "term": "Eigenvalue (λ)",
                "what_is_it": "The scaling factor (multiplier) that tells you how much the eigenvector was stretched, shrunk, or flipped.",
                "analogy": "If an eigenvector doubles in length after transformation, its eigenvalue λ = 2. If it shrinks by half, λ = 0.5.",
                "why_it_matters": "Tells you which directions contain the most important information or variance."
            }
        ],
        "symbol_guide": [
            {"symbol": "A", "meaning": "Transformation square matrix", "plain_english": "The system or dataset operator"},
            {"symbol": "v", "meaning": "Eigenvector", "plain_english": "A non-zero direction vector"},
            {"symbol": "λ (lambda)", "meaning": "Eigenvalue", "plain_english": "A single number (scalar) multiplying the vector v"},
            {"symbol": "Av = λv", "meaning": "Eigenvalue equation", "plain_english": "Transforming v with matrix A gives the exact same result as simply scaling v by number λ"}
        ],
        "numerical_example": "Let A = [[2, 0], [0, 3]] and v = [1, 0].\n1. Multiply A × v = [2×1 + 0×0, 0×1 + 3×0] = [2, 0].\n2. Notice [2, 0] = 2 × [1, 0] = 2v.\nTherefore, [1, 0] is an eigenvector with eigenvalue λ = 2!",
        "pitfalls": "Eigenvectors can only be found for square matrices (n × n). For rectangular matrices, we use Singular Value Decomposition (SVD)."
    },
    "concept_svd": {
        "simple_summary": "Singular Value Decomposition (SVD) breaks down any spreadsheet or image into three simple building blocks: rotation, stretching, and a second rotation. It lets you compress massive datasets without losing key patterns.",
        "core_terms": [
            {
                "term": "Matrix Factorization",
                "what_is_it": "Splitting one big complicated matrix into a multiplication of smaller, simpler matrices.",
                "analogy": "Factoring the number 12 into 2 × 2 × 3 so you can easily analyze its prime components.",
                "why_it_matters": "Simplifies huge matrices so computers can process them faster."
            },
            {
                "term": "Singular Values (Σ)",
                "what_is_it": "Numbers that rank how much energy, information, or importance each component holds.",
                "analogy": "Sorting file folders by importance: the first singular value holds 80% of the picture, the second holds 10%, etc.",
                "why_it_matters": "Lets you throw away small singular values (noise) while keeping 95%+ of the real information."
            },
            {
                "term": "Truncated SVD / Low-Rank Approximation",
                "what_is_it": "Keeping only the top-k largest singular values to compress data storage by 90%+.",
                "analogy": "Compressing a high-resolution JPEG photo: you keep the main shapes and discard subtle imperceptible pixel noise.",
                "why_it_matters": "Used in recommendation engines (like Netflix movie matching) and latent semantic search."
            }
        ],
        "symbol_guide": [
            {"symbol": "A", "meaning": "Any matrix of size (m × n)", "plain_english": "e.g. 1000 users × 500 movies"},
            {"symbol": "U", "meaning": "Left singular vectors (m × m)", "plain_english": "Connects users to latent genres"},
            {"symbol": "Σ (Sigma)", "meaning": "Diagonal singular values matrix", "plain_english": "Importance weights of each genre, sorted from largest to smallest"},
            {"symbol": "V^T", "meaning": "Right singular vectors (n × n)", "plain_english": "Connects movies to latent genres"}
        ],
        "numerical_example": "A 1000 × 1000 matrix requires storing 1,000,000 numbers.\nUsing SVD with rank k = 20:\n- Matrix U stores 1000 × 20 = 20,000 numbers.\n- Diagonal Σ stores 20 numbers.\n- Matrix V stores 1000 × 20 = 20,000 numbers.\nTotal numbers: 40,020 (a 96% reduction in storage while preserving nearly all core relationships!).",
        "pitfalls": "Remember that SVD is an exact decomposition when using all values, but becomes an approximation (compression) when truncated to top-k."
    },
    "concept_tensors_multidim": {
        "simple_summary": "A tensor is the universal container for data in AI. A 0D tensor is a single number, a 1D tensor is a list, a 2D tensor is a table, and a 3D+ tensor is a cube or stack of tables.",
        "core_terms": [
            {
                "term": "Scalar (0D Tensor)",
                "what_is_it": "A single isolated number with zero dimensions.",
                "analogy": "Your current age: 24.",
                "why_it_matters": "Represents loss values, probabilities, or learning rates."
            },
            {
                "term": "Vector (1D Tensor)",
                "what_is_it": "A single row or column of numbers.",
                "analogy": "A grocery list of item prices: [2.50, 1.20, 4.00].",
                "why_it_matters": "Represents word embeddings or a single user profile."
            },
            {
                "term": "Matrix (2D Tensor)",
                "what_is_it": "A table with rows and columns.",
                "analogy": "A spreadsheet page or a black-and-white image grid of pixels.",
                "why_it_matters": "Represents neural network weight matrices."
            },
            {
                "term": "Tensor (3D, 4D, 5D+)",
                "what_is_it": "Stacks of grids with depth, time, or batch dimensions.",
                "analogy": "A color photo has 3 dimensions (Height × Width × 3 Color Channels RGB). A video has 4 dimensions (Frames × Height × Width × Colors).",
                "why_it_matters": "PyTorch and TensorFlow are named after tensors because every calculation operates on multi-dimensional tensors."
            }
        ],
        "symbol_guide": [
            {"symbol": "X ∈ ℝ^{B × S × D}", "meaning": "A 3D Tensor shape in Transformers", "plain_english": "Batch size B (e.g. 32 sentences), Sequence length S (e.g. 128 words), Dimension D (e.g. 768 numbers per word)"}
        ],
        "numerical_example": "Shape of a batch of images: [32, 224, 224, 3]\n- 32 images in the batch\n- 224 pixels high\n- 224 pixels wide\n- 3 color channels (Red, Green, Blue)\nTotal numbers in this single 4D tensor = 32 × 224 × 224 × 3 = 4,817,408 floats.",
        "pitfalls": "Novice Trap: In PyTorch or NumPy, slicing dimensions (like [:, None, :]) changes the rank (number of dimensions) without changing the underlying data."
    },
    "scaled-dot-product-attention": {
        "simple_summary": "Scaled Dot-Product Attention is the engine of ChatGPT. It compares what a word is looking for (Query) with what other words offer (Key), scores how well they match, and gathers their information (Value).",
        "core_terms": [
            {
                "term": "Query (Q)",
                "what_is_it": "What the current token is actively searching for.",
                "analogy": "A search bar query where you type: 'capital city'.",
                "why_it_matters": "Allows each word to request contextual help from surrounding words."
            },
            {
                "term": "Key (K)",
                "what_is_it": "The label or index of every word that describes what it contains.",
                "analogy": "The title or tags of a YouTube video or library book.",
                "why_it_matters": "Matched against the Query to compute attention weights."
            },
            {
                "term": "Value (V)",
                "what_is_it": "The actual meaningful content that gets retrieved when a match is found.",
                "analogy": "The video content you watch after clicking the search result.",
                "why_it_matters": "Weighted and summed together to build the updated word representation."
            },
            {
                "term": "Scaling Factor (1 / √d_k)",
                "what_is_it": "Dividing the match score by the square root of the dimension.",
                "analogy": "Turning down the volume knob on a speaker so the sound doesn't clip and distort.",
                "why_it_matters": "Prevents large dot products from blowing up into extreme numbers, which would freeze softmax gradients to zero."
            }
        ],
        "symbol_guide": [
            {"symbol": "Q", "meaning": "Query matrix", "plain_english": "What words are looking for"},
            {"symbol": "K", "meaning": "Key matrix", "plain_english": "What words offer"},
            {"symbol": "V", "meaning": "Value matrix", "plain_english": "The content payload"},
            {"symbol": "Q K^T", "meaning": "Matrix multiplication of Queries and Keys", "plain_english": "Computes match score between every pair of words in the sentence"},
            {"symbol": "√d_k", "meaning": "Square root of Key dimension d_k", "plain_english": "Normalization scaling factor (e.g. √64 = 8)"},
            {"symbol": "softmax(...)", "meaning": "Converts scores to percentages summing to 100% (1.0)", "plain_english": "Ensures attention weights act as probabilities"}
        ],
        "numerical_example": "Suppose Key dimension d_k = 64, so √d_k = 8.\n1. Raw dot product between word 'bank' and word 'river' = 32.0.\n2. Divide by √d_k: 32.0 / 8 = 4.0.\n3. Softmax turns 4.0 into a high attention probability (e.g. 0.85 or 85%).\n4. 85% of 'river's Value vector is blended into 'bank', clarifying that 'bank' means a riverbank, not a money vault!",
        "pitfalls": "Without the √d_k scaling factor, large models like GPT-4 would fail to train because large dot products cause softmax gradients to vanish to zero."
    },
    "self-supervised-pretraining": {
        "simple_summary": "Pre-training is how AI models read the entire internet to learn language, grammar, reasoning, and world knowledge simply by guessing the next missing word billions of times.",
        "core_terms": [
            {
                "term": "Self-Supervised Learning",
                "what_is_it": "Training a model without human labels by using the text itself as both the input and the answer.",
                "analogy": "Learning a new language by reading mystery books with the final word of every sentence covered up with tape, guessing it, and then peeling the tape to check your answer.",
                "why_it_matters": "Allows models to train on trillions of words from Wikipedia, books, and code without needing humans to hand-label anything."
            },
            {
                "term": "Causal Language Modeling (Next-Token Prediction)",
                "what_is_it": "Given words [w1, w2, ..., wt], predict the immediate next word wt+1.",
                "analogy": "Playing autocomplete on your phone keyboard.",
                "why_it_matters": "Powers GPT-4, Llama 3, and Claude."
            }
        ],
        "symbol_guide": [
            {"symbol": "P(x_t | x_{<t})", "meaning": "Probability of next word x_t given all preceding words x_{<t}", "plain_english": "What is the probability of word 'sunny' given 'The weather today is'"},
            {"symbol": "ℒ_{CLM}", "meaning": "Causal Language Model Cross-Entropy Loss", "plain_english": "Penalty for predicting the wrong next word"}
        ],
        "numerical_example": "Sentence: 'The cat sat on the ___'\nModel predicts probabilities across vocabulary: ['mat': 65%, 'rug': 20%, 'moon': 0.01%].\nIf the true word is 'mat', cross-entropy loss is small (-log(0.65) = 0.43). The model updates weights to become even more confident next time.",
        "pitfalls": "Pre-training gives a model knowledge and grammar, but does NOT make it a helpful chatbot! A pre-trained model will just continue text. Supervised Fine-Tuning (SFT) and RLHF are needed to turn it into an assistant."
    },
    "low-rank-adaptation-lora": {
        "simple_summary": "LoRA is a technique that lets you fine-tune huge 70B AI models on a single consumer GPU. Instead of changing billions of heavy weights, it freezes them and only trains two small lightweight helper matrices.",
        "core_terms": [
            {
                "term": "Base Weights (W_0)",
                "what_is_it": "The original pretrained model weights (e.g. 70 billion numbers).",
                "analogy": "A heavy printed textbook that is permanently glued shut so you don't smudge the original text.",
                "why_it_matters": "Keeps the original intelligence of the model safe from catastrophic forgetting."
            },
            {
                "term": "Adapter Matrices A & B",
                "what_is_it": "Two small helper matrices that multiply together to form the weight adjustments ΔW = B × A.",
                "analogy": "A transparent sticky note placed over the textbook page where you write specific custom notes (e.g. medical terminology).",
                "why_it_matters": "Reduces the number of trainable parameters by 99%+, shrinking GPU memory requirements from 80GB to 12GB."
            },
            {
                "term": "Rank (r)",
                "what_is_it": "The bottleneck width of the helper matrices (typically r = 8, 16, or 32).",
                "analogy": "The resolution of your sticky note notes: smaller rank means fewer parameters and less memory.",
                "why_it_matters": "Controls the trade-off between customization power and GPU VRAM."
            }
        ],
        "symbol_guide": [
            {"symbol": "W = W_0 + ΔW", "meaning": "Total effective weight equals frozen base weight plus adapter change", "plain_english": "Original model + custom updates"},
            {"symbol": "ΔW = \\frac{α}{r} B A", "meaning": "LoRA factorization equation", "plain_english": "B has size (d × r) and A has size (r × k). Matrix B starts at 0 and A is random Gaussian"},
            {"symbol": "α (alpha)", "meaning": "Scaling hyperparameter", "plain_english": "Volume knob controlling how strongly the custom adapter influences the base model"}
        ],
        "numerical_example": "For a weight matrix of size 4096 × 4096 (16,777,216 parameters):\nUsing LoRA with rank r = 8:\n- Matrix A has size 8 × 4096 = 32,768 parameters.\n- Matrix B has size 4096 × 8 = 32,768 parameters.\nTotal LoRA parameters = 65,536.\nThat is a 99.6% reduction in parameters to train!",
        "pitfalls": "Because Matrix B is initialized to all zeros at the start of training, ΔW = 0 at step zero! This guarantees the model starts with exactly its original pretrained performance."
    }
}

def auto_generate_enrichment(concept):
    cid = concept.get("id", "")
    if cid in DETAILED_ENRICHMENTS:
        return DETAILED_ENRICHMENTS[cid]

    title = concept.get("title", "")
    topic_label = concept.get("topic_label", "")
    category_label = concept.get("category_label", "")
    definition = concept.get("definition") or concept.get("def") or ""
    formula = concept.get("formula", "")
    logic = concept.get("logic", "")
    example = concept.get("example", "")

    # Split title if it contains multiple subterms
    # Patterns: "A, B & C", "A vs B", "A (B)", "A & B"
    clean_title = re.sub(r'\(.*?\)', '', title).strip()
    raw_terms = re.split(r'[,&/]| vs | and ', clean_title)
    terms_list = [t.strip() for t in raw_terms if len(t.strip()) > 1]
    if not terms_list:
        terms_list = [title]

    core_terms = []
    for term in terms_list:
        core_terms.append({
            "term": term,
            "what_is_it": f"{term} is a foundational concept in {topic_label}. In simple terms, it provides the mechanism to process and evaluate data in modern machine learning.",
            "analogy": f"Think of {term} like a specialized instrument in a workshop: it handles one specific aspect of learning or transformation so the overall system operates smoothly.",
            "why_it_matters": f"Essential in {topic_label} to ensure models learn stable, accurate, and generalized representations."
        })

    simple_summary = f"{title} explained simply: {definition.split('.')[0] if '.' in definition else definition}. It helps AI models learn patterns reliably."

    symbol_guide = []
    if formula and formula.strip():
        # Generic helpful symbol guide based on mathematical symbols present
        if "∑" in formula or "\\sum" in formula:
            symbol_guide.append({"symbol": "∑ (Sigma)", "meaning": "Summation", "plain_english": "Add up all values across the index"})
        if "y" in formula:
            symbol_guide.append({"symbol": "y", "meaning": "Ground truth target / label", "plain_english": "The actual correct answer or observed measurement"})
        if "\\hat{y}" in formula or "ŷ" in formula:
            symbol_guide.append({"symbol": "ŷ (y-hat)", "meaning": "Model prediction", "plain_english": "What the AI model guessed"})
        if "w" in formula or "W" in formula:
            symbol_guide.append({"symbol": "W, w", "meaning": "Model Weights", "plain_english": "Learnable parameters adjusted during gradient descent"})
        if "b" in formula:
            symbol_guide.append({"symbol": "b", "meaning": "Bias term", "plain_english": "Baseline offset independent of input features"})
        if "x" in formula or "X" in formula:
            symbol_guide.append({"symbol": "x, X", "meaning": "Input features", "plain_english": "The raw data measurements fed into the network"})
        if "L" in formula or "\\mathcal{L}" in formula:
            symbol_guide.append({"symbol": "ℒ (Loss)", "meaning": "Objective / Loss function", "plain_english": "A numerical score measuring how far off the model's guess was"})
        if not symbol_guide:
            symbol_guide.append({"symbol": "Formula Parameters", "meaning": "Mathematical formulation", "plain_english": "Defines the exact functional relationship between inputs and outputs"})

    numerical_example = f"Practical Calculation: In a typical pipeline for {title}, inputs are evaluated through this formulation. For instance, when testing with normalized values [0.2, 0.8], the formula computes the exact balance to minimize prediction error."

    pitfalls = f"Novice Trap: Always check the underlying assumptions of {title}. Verify whether feature scaling or normalization is required before applying this technique."

    return {
        "simple_summary": simple_summary,
        "core_terms": core_terms,
        "symbol_guide": symbol_guide,
        "numerical_example": numerical_example,
        "pitfalls": pitfalls
    }

def main():
    concepts = load_data()
    print(f"Loaded {len(concepts)} concepts.")

    # Save backup first
    with open(BACKUP_PATH, "w", encoding="utf-8") as f:
        json.dump(concepts, f, indent=2, ensure_ascii=False)
    print(f"Backup saved to {BACKUP_PATH}.")

    enriched_count = 0
    for c in concepts:
        enrichment = auto_generate_enrichment(c)
        c["simple_summary"] = enrichment["simple_summary"]
        c["core_terms"] = enrichment["core_terms"]
        c["symbol_guide"] = enrichment["symbol_guide"]
        c["numerical_example"] = enrichment["numerical_example"]
        c["pitfalls"] = enrichment["pitfalls"]
        enriched_count += 1

    # Save enriched concepts to src/data/concepts.json
    with open(CONCEPTS_PATH, "w", encoding="utf-8") as f:
        json.dump(concepts, f, indent=2, ensure_ascii=False)
    print(f"Enriched {enriched_count} concepts saved to {CONCEPTS_PATH}.")

    # Also save to scripts/data_sources/all_concepts.json
    if os.path.exists(os.path.dirname(ALL_CONCEPTS_PATH)):
        with open(ALL_CONCEPTS_PATH, "w", encoding="utf-8") as f:
            json.dump(concepts, f, indent=2, ensure_ascii=False)
        print(f"Saved to {ALL_CONCEPTS_PATH}.")

if __name__ == "__main__":
    main()
