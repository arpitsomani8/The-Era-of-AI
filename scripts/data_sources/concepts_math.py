"""
Concepts Database: Mathematical Foundations (19 Concepts)
"""

MATH_CONCEPTS = [
    {
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
    },
    {
        "id": "concept_matrix_mult_inverses",
        "title": "Matrix Multiplication, Transposition & Inverses",
        "topic_id": "math_linalg",
        "topic_label": "Linear Algebra & Vector Spaces",
        "category": "math",
        "category_label": "Mathematical Foundations",
        "raw_subtopic": "Matrix Multiplication, Transposition & Inverses",
        "def": "A matrix is a 2D grid of numbers representing linear transformations or entire datasets. Matrix multiplication composes transformations row-by-column, transposition flips rows and columns across the diagonal, and an inverse matrix undoes a transformation.",
        "formula": "$$C = A B \\implies C_{ij} = \\sum_{k=1}^p A_{ik} B_{kj}, \\quad (A B)^T = B^T A^T, \\quad A A^{-1} = A^{-1} A = I$$",
        "logic": "Every feedforward layer in a neural network is a matrix multiplication y = WX + b. Matrix division does not exist in linear algebra; solving Ax = b is performed by multiplying by the inverse matrix x = A⁻¹b.",
        "example": "Batch Forward Pass & Self-Attention: In modern LLMs (e.g. LLaMA), a batch of 64 tokens with embedding dimension 4096 is projected through a weight matrix of shape [4096, 4096] in a single GPU matrix multiplication taking microseconds.",
        "tags": [
            "Matrices",
            "Matrix Multiplication",
            "Transposition",
            "Matrix Inverses",
            "Identity Matrix",
            "Hadamard Product",
            "Linear Algebra",
            "Deep Learning"
        ],
        "raw_sub": "Matrix Multiplication, Transposition & Inverses",
        "definition": "A matrix is a 2D grid of numbers representing linear transformations or entire datasets. Matrix multiplication composes transformations row-by-column, transposition flips rows and columns across the diagonal, and an inverse matrix undoes a transformation.",
        "formula_explanation": "Matrix multiplication combines rows of A with columns of B (inner dimensions must match). Transposition flips rows to columns with the reverse order rule (AB)ᵀ = BᵀAᵀ. An inverse matrix A⁻¹ acts as an undo operator such that A A⁻¹ = I.",
        "simple_summary": "A matrix is a 2D table of numbers. Matrix multiplication transforms data, transposition flips rows into columns, and an inverse matrix acts like an 'Undo' button that reverses a transformation.",
        "core_terms": [
            {
                "term": "Matrix",
                "what_is_it": "• A 2D spreadsheet or grid of numbers arranged in rows and columns.\n• In AI, neural network weights, feature tables, and batches of data are represented as matrices.",
                "analogy": "A pricing table where rows are products (Apple, Banana) and columns are stores (Store A, Store B).",
                "why_it_matters": "Virtually all neural network weights and data batches are stored and processed as matrices in GPU memory."
            },
            {
                "term": "Matrix Multiplication",
                "what_is_it": "• A mathematical operation combining two grids by calculating the dot product of rows from the first matrix with columns of the second matrix.\n• The inner dimensions must match: A(m × k) × B(k × n) = C(m × n).",
                "analogy": "Multiplying a grocery shopping list [quantities] by a store price catalog [prices per item] to compute total bills in a single step.",
                "why_it_matters": "Over 99% of compute cycles during LLM training and inference (ChatGPT) are matrix multiplications (GEMM) running on GPUs."
            },
            {
                "term": "Transposition (A^T)",
                "what_is_it": "• Flipping a matrix across its main diagonal so that rows become columns and columns become rows.\n• A matrix of shape (m × n) becomes shape (n × m), satisfying the identity (Aᵀ)ᵀ = A.",
                "analogy": "Rotating a spreadsheet table from wide format to tall format so its headers align with another dataset.",
                "why_it_matters": "Essential in AI for fixing dimension mismatches before multiplication, computing Attention scores (Q Kᵀ), and calculating covariance matrices."
            },
            {
                "term": "Inverse Matrix (A^-1)",
                "what_is_it": "• A unique matrix that reverses the effect of matrix A, satisfying A A⁻¹ = A⁻¹ A = I (Identity Matrix).\n• In matrix algebra there is no division; instead of dividing by A, we multiply by its inverse A⁻¹.",
                "analogy": "If matrix A rotates a 3D model 45° clockwise, its inverse matrix A⁻¹ rotates it 45° counter-clockwise back to its original position.",
                "why_it_matters": "Used to solve linear equation systems (Ax = b ⟹ x = A⁻¹b) and in analytical optimization methods like Ordinary Least Squares (OLS)."
            }
        ],
        "types_header": "Matrix Operations & Types at a Glance",
        "types_badge": "Operations & Types",
        "quick_types": [
            {
                "type": "Identity Matrix (I)",
                "definition": "Square matrix with 1s on the main diagonal and 0s elsewhere; acts like the number 1.",
                "looks_like": "[[1, 0], [0, 1]] (A · I = A)"
            },
            {
                "type": "Matrix Multiplication (@)",
                "definition": "Transforms shapes by taking row-by-column combinations. Inner dimensions must match.",
                "looks_like": "A(m×k) @ B(k×n) = C(m×n)"
            },
            {
                "type": "Element-wise Product (*)",
                "definition": "Hadamard product; matrices must have identical shape and multiply matching positions.",
                "looks_like": "A(m×n) * B(m×n) = C(m×n) (Gated LSTMs)"
            },
            {
                "type": "Transposition (A^T)",
                "definition": "Swaps rows with columns, flipping shape across the diagonal.",
                "looks_like": "[[1, 2], [3, 4]]ᵀ = [[1, 3], [2, 4]]"
            },
            {
                "type": "Square Matrix",
                "definition": "A matrix with equal rows and columns (n × n); mandatory prerequisite for inverses.",
                "looks_like": "shape: (3 × 3) or (n × n)"
            },
            {
                "type": "Invertible Matrix",
                "definition": "A non-singular square matrix with non-zero determinant (det(A) ≠ 0).",
                "looks_like": "A A⁻¹ = I (det(A) ≠ 0)"
            },
            {
                "type": "Singular Matrix",
                "definition": "A matrix with determinant equal to zero (det(A) = 0); cannot be inverted.",
                "looks_like": "det(A) = 0 (no inverse exists)"
            },
            {
                "type": "Symmetric Matrix",
                "definition": "A square matrix that equals its own transpose (A = Aᵀ).",
                "looks_like": "Aᵀ = A (e.g. Covariance Matrix XᵀX)"
            }
        ],
        "symbol_guide": [
            {
                "symbol": "A, B",
                "meaning": "Input matrices",
                "plain_english": "A has size (m × k) and B has size (k × n)"
            },
            {
                "symbol": "C = A B or A @ B",
                "meaning": "Matrix multiplication product",
                "plain_english": "The resulting matrix with size (m × n)"
            },
            {
                "symbol": "A ⊙ B or A * B",
                "meaning": "Hadamard / Element-wise product",
                "plain_english": "Multiply entries at the exact same position (shapes must match)"
            },
            {
                "symbol": "A^T",
                "meaning": "Transpose of A",
                "plain_english": "Flip rows and columns: element at (i, j) moves to (j, i)"
            },
            {
                "symbol": "A^-1",
                "meaning": "Inverse of A",
                "plain_english": "Matrix such that A multiplied by A⁻¹ equals the identity matrix I"
            },
            {
                "symbol": "I",
                "meaning": "Identity matrix",
                "plain_english": "Square grid with 1s on diagonal and 0s elsewhere (like number 1)"
            },
            {
                "symbol": "det(A)",
                "meaning": "Determinant of matrix A",
                "plain_english": "Scaling factor of transformation; if det(A) = 0, no inverse exists"
            }
        ],
        "numerical_example": "1. Matrix Multiplication (2×2 by 2×2):\nLet A = [[1, 2], [3, 4]] and B = [[2, 0], [1, 2]].\n• Top-left: (1 × 2) + (2 × 1) = 2 + 2 = 4\n• Top-right: (1 × 0) + (2 × 2) = 0 + 4 = 4\n• Bottom-left: (3 × 2) + (4 × 1) = 6 + 4 = 10\n• Bottom-right: (3 × 0) + (4 × 2) = 0 + 8 = 8\nResult C = [[4, 4], [10, 8]] with shape (2 × 2).\n\n2. Transposition (Aᵀ):\nLet A = [[1, 2], [3, 4]].\n• Flip rows into columns: Row 1 [1, 2] becomes Column 1; Row 2 [3, 4] becomes Column 2.\nResult Aᵀ = [[1, 3], [2, 4]].\n\n3. Matrix Inverse (2×2 Formula):\nLet M = [[2, 1], [5, 3]].\nFormula: M⁻¹ = (1 / det(M)) × [[d, -b], [-c, a]]\n• Step 1: Compute Determinant: det(M) = (2 × 3) - (1 × 5) = 6 - 5 = 1 (det ≠ 0, invertible!)\n• Step 2: Swap diagonal elements (2 & 3) and negate off-diagonals (1 & 5): [[3, -1], [-5, 2]]\n• Step 3: Divide by det(M) = 1:\nResult M⁻¹ = [[3, -1], [-5, 2]].\n\nVerification: M × M⁻¹ = [[(2×3 + 1×-5), (2×-1 + 1×2)], [(5×3 + 3×-5), (5×-1 + 3×2)]] = [[1, 0], [0, 1]] = I!",
        "pitfalls": "• Common Trap 1: Matrix multiplication is NOT commutative! A × B is almost never equal to B × A. Order matters fundamentally.\n• Common Trap 2: The Reverse Order Transpose rule: (A B)ᵀ = Bᵀ Aᵀ (notice the order flips; writing Aᵀ Bᵀ is incorrect!).\n• Common Trap 3: Dividing matrices: Matrix division does not exist (A / B is mathematically invalid); you must multiply by the inverse (A B⁻¹).\n• Common Trap 4: Inverting singular matrices: Attempting to invert a matrix with determinant = 0 will crash your program because it is equivalent to dividing by zero.",
        "core_logic": "Every feedforward layer in a neural network is a matrix multiplication y = WX + b. Computing matrix inverses directly is O(d³) and numerically unstable; modern deep learning solvers use iterative gradient descent or matrix decompositions (QR, Cholesky, LU).",
        "architectural_logic": "Every feedforward layer in a neural network is a matrix multiplication y = WX + b. In Transformer architectures, queries and keys are multiplied via matrix multiplication with a transpose: Score = Q Kᵀ. Modern GPU Tensor Cores are hardware-specialized to execute matrix multiplications in parallel hardware cycles.",
        "connected_logic": [
            {
                "title": "Inner Dimension Rule & Multiplication Types (@ vs. *)",
                "content": "• The Inner Dimension Rule: A(m × k) × B(k × n) = C(m × n). The inner dimensions (k and k) must match and collapse; outer dimensions (m and n) define the output shape.\n• Matrix Multiplication (@ in Python): Combines rows and columns, transforming shapes and mixing features.\n• Element-wise Product (* in Python / Hadamard): Matrices must have the exact same shape. Used in Deep Learning gated mechanisms (LSTM forget gates, attention masks) to selectively filter information."
            },
            {
                "title": "Transposition in AI & The Reverse Order Rule",
                "content": "• The Reverse Order Rule: (A B)ᵀ = Bᵀ Aᵀ. Notice that the multiplication order flips (a very common interview question!).\n• Why We Transpose in AI:\n  - Fixing Dimension Mismatches: Passing batch X [B, D_in] into weights W [D_out, D_in] via X Wᵀ.\n  - Transformer Self-Attention: Computing query-key similarity Q Kᵀ gives the [T, T] attention score matrix.\n  - Feature Covariance: Calculating Xᵀ X to measure cross-feature correlation."
            },
            {
                "title": "Why There's No Matrix Division: Inverses & Solving Ax = b",
                "content": "• In scalar math: 5x = 20 ⟹ x = 20 / 5 = 5⁻¹ × 20 = 4.\n• In matrix algebra: Division does not exist (writing B / A is mathematically invalid).\n• Instead, we multiply by the inverse: A x = b ⟹ x = A⁻¹ b.\n• Multiplying by A⁻¹ acts like an 'Undo' button that reverses the transformation done by A."
            },
            {
                "title": "When Inverses Fail: Singular Matrices & Zero Determinant",
                "content": "• A matrix has an inverse ONLY IF it is square (n × n) and its determinant is not zero (det(A) ≠ 0).\n• If det(A) ≠ 0: The matrix is invertible (non-singular).\n• If det(A) = 0: The matrix is singular and has NO inverse (analogous to dividing by zero).\n• Intuition: A determinant of zero means the matrix flattens space (e.g., squashing a 2D plane into a 1D line), permanently destroying information so it can never be reversed."
            }
        ],
        "key_takeaways": [
            "A matrix is a 2D grid representing linear transformations and dataset batches.",
            "Matrix multiplication requires matching inner dimensions: A(m×k) × B(k×n) = C(m×n).",
            "Matrix multiplication (@) combines rows and columns, while Element-wise multiplication (*) multiplies identical positions (used in LSTM gates).",
            "Transposition flips rows and columns: (Aᵀ)ᵀ = A and (AB)ᵀ = Bᵀ Aᵀ (Reverse Order Rule).",
            "Matrix division does not exist; we solve Ax = b by multiplying by the inverse: x = A⁻¹b.",
            "An inverse exists only for square matrices with non-zero determinant (det(A) ≠ 0); matrices with det(A) = 0 are singular and cannot be inverted.",
            "The Identity Matrix I has 1s on the diagonal and acts like the number 1 (A I = A)."
        ],
        "definition_bullets": [
            "Matrix: A 2D grid of numbers representing linear transformations or batches of data.",
            "Matrix Multiplication: Inner dimensions must match; computes row-by-column combinations.",
            "Transposition: Swaps rows and columns; satisfies the Reverse Order Rule (AB)ᵀ = Bᵀ Aᵀ.",
            "Inverse Matrix: Reverses a transformation; exists only when det(A) ≠ 0."
        ]
    },
    {
        "id": "concept_eigenvalues_eigenvectors",
        "title": "Eigenvalues & Eigenvectors",
        "topic_id": "math_linalg",
        "topic_label": "Linear Algebra & Vector Spaces",
        "category": "math",
        "category_label": "Mathematical Foundations",
        "raw_subtopic": "Eigenvalues & Eigenvectors (Directions of invariant stretch)",
        "def": "Eigenvectors are special non-zero vectors that do not rotate when transformed by a square matrix; they only stretch or shrink by a scalar factor called the eigenvalue.",
        "formula": "$$A v = \\lambda v, \\quad \\det(A - \\lambda I) = 0$$",
        "logic": "Eigenvectors reveal the fundamental internal axes of a dataset or physical system. In PCA, the eigenvectors of the data covariance matrix identify the orthogonal directions of maximum data spread and variance.",
        "example": "Google PageRank algorithm: The web is modeled as a massive transition matrix $M$. The steady-state importance of every webpage is the principal eigenvector corresponding to eigenvalue $\\lambda = 1$.",
        "tags": [
            "Eigenvalues",
            "Eigenvectors",
            "Spectral Theory",
            "PCA",
            "PageRank",
            "Linear Algebra"
        ],
        "raw_sub": "Eigenvalues & Eigenvectors (Directions of invariant stretch)",
        "definition": "Eigenvectors are special non-zero vectors that do not rotate when transformed by a square matrix; they only stretch or shrink by a scalar factor called the eigenvalue.",
        "formula_explanation": "Av = λv states that transforming vector v by matrix A produces the exact same result as simply scaling v by scalar λ. The characteristic equation det(A - λI) = 0 is solved to find all eigenvalues λ.",
        "simple_summary": "When a matrix stretches, squishes, or rotates space, eigenvectors are special arrows that do NOT rotate—they only stretch or shrink. The eigenvalue is the number that tells you how much they stretch.",
        "core_terms": [
            {
                "term": "Eigenvector",
                "what_is_it": "• A direction in space that stays on its own original line after a matrix transformation is applied (the word 'Eigen' is German for 'own', 'peculiar', or 'characteristic').\n• Instead of rotating when multiplied by matrix A, the vector only stretches or shrinks along its original line.",
                "analogy": "Imagine stretching a rubber sheet diagonally. Most arrows drawn on the sheet will tilt and rotate, but the arrow pointing directly along the stretch axis only gets longer—it never tilts!",
                "why_it_matters": "They form the backbone of Dimensionality Reduction (PCA), Google's PageRank algorithm, and understanding how deep neural networks train."
            },
            {
                "term": "Eigenvalue (λ)",
                "what_is_it": "• The scaling factor (multiplier) that tells you how much the eigenvector was stretched, shrunk, or flipped.\n• It turns an expensive matrix-vector multiplication (Av) into a simple scalar multiplication (λv).",
                "analogy": "If an eigenvector doubles in length after transformation, its eigenvalue λ = 2. If it shrinks by half, λ = 0.5.",
                "why_it_matters": "In PCA, eigenvalues tell you how much information (variance) exists along that principal axis."
            }
        ],
        "types_header": "What Different Eigenvalue (λ) Values Mean",
        "types_badge": "Eigenvalue Behaviors",
        "quick_types": [
            {
                "type": "λ > 1 (Stretching)",
                "definition": "The vector is stretched longer in the exact same direction.",
                "looks_like": "e.g. λ = 2.0 (doubles length along axis)"
            },
            {
                "type": "0 < λ < 1 (Compression)",
                "definition": "The vector is shrunk / compressed along its axis without flipping.",
                "looks_like": "e.g. λ = 0.5 (halves length along axis)"
            },
            {
                "type": "λ = 1 (Stationary / Invariant)",
                "definition": "The vector remains completely unchanged in length and direction.",
                "looks_like": "Av = 1v = v (PageRank steady state)"
            },
            {
                "type": "λ < 0 (Reflection / 180° Flip)",
                "definition": "The vector is flipped 180° to point in the exact opposite direction.",
                "looks_like": "e.g. λ = -1.0 (exact direction reversal)"
            },
            {
                "type": "λ = 0 (Dimensional Collapse)",
                "definition": "The vector is squashed to zero; the matrix completely collapsed this dimension.",
                "looks_like": "Av = 0v = 0 (singular matrix)"
            }
        ],
        "symbol_guide": [
            {
                "symbol": "A",
                "meaning": "Transformation square matrix",
                "plain_english": "The system or dataset operator"
            },
            {
                "symbol": "v",
                "meaning": "Eigenvector",
                "plain_english": "A non-zero direction vector that doesn't rotate"
            },
            {
                "symbol": "λ (lambda)",
                "meaning": "Eigenvalue",
                "plain_english": "A single number (scalar) scaling vector v"
            },
            {
                "symbol": "Av = λv",
                "meaning": "Eigenvalue equation",
                "plain_english": "Transforming v with matrix A equals simply scaling v by number λ"
            },
            {
                "symbol": "det(A - λI) = 0",
                "meaning": "Characteristic equation",
                "plain_english": "Equation solved to compute all eigenvalues λ of matrix A"
            }
        ],
        "numerical_example": "Let A = [[2, 0], [0, 3]] and v = [1, 0].\n1. Multiply A × v = [2×1 + 0×0, 0×1 + 3×0] = [2, 0].\n2. Notice [2, 0] = 2 × [1, 0] = 2v.\nTherefore, [1, 0] is an eigenvector with eigenvalue λ = 2!\n\nSimilarly, for v₂ = [0, 1]:\nA × v₂ = [2×0 + 0×1, 0×0 + 3×1] = [0, 3] = 3 × [0, 1] = 3v₂.\nHere v₂ is an eigenvector with eigenvalue λ = 3 (stretched by 3x)!",
        "pitfalls": "Common Trap: Eigenvectors can only be found for square matrices (n × n). For rectangular matrices (where row and column counts differ), we use Singular Value Decomposition (SVD).",
        "core_logic": "Eigenvectors reveal the fundamental internal axes of a dataset or physical system. In PCA, the eigenvectors of the data covariance matrix identify the orthogonal directions of maximum data spread and variance.",
        "architectural_logic": "In deep neural networks, the eigenvalues of weight matrices govern stability during training. If eigenvalues of weight matrices exceed 1 (spectral radius > 1), gradients can explode during backpropagation across many layers. If eigenvalues are below 1, gradients rapidly vanish. Techniques like Spectral Normalization constrain the maximum eigenvalue to stabilize GANs and deep Transformers.",
        "connected_logic": [
            {
                "title": "Av vs. λv: Matrix Transformation vs. Simple Scalar Scaling",
                "content": "• Av is normally an expensive matrix-vector multiplication that rotates and skews space.\n• For an eigenvector, this complex transformation collapses into a simple scalar multiplication: λv.\n• Transforming v with matrix A simply stretches, compresses, or flips it along its own original line without any rotation."
            },
            {
                "title": "The Backbone of PCA & Dimensionality Reduction",
                "content": "• The Eigenvectors of a dataset's covariance matrix point in the directions of maximum spread (variance) in the data—these directions are called the Principal Components.\n• The Eigenvalues tell you exactly how much information (variance) exists along that axis!\n• By keeping only the eigenvectors with the largest eigenvalues, PCA compresses high-dimensional data while preserving 95%+ of the original information."
            },
            {
                "title": "The Spectral Theorem for Symmetric Matrices (A = Aᵀ)",
                "content": "• For symmetric matrices (where A = Aᵀ, such as data covariance matrices XᵀX), the Spectral Theorem guarantees two critical properties:\n  1. All eigenvalues are real numbers (no imaginary or complex numbers).\n  2. All eigenvectors are strictly perpendicular (orthogonal) to each other.\n• This ensures that Principal Components form an ideal, non-overlapping coordinate grid."
            },
            {
                "title": "Real-World Impact: Google PageRank & Deep Learning",
                "content": "• Google PageRank: The entire internet is modeled as a giant transition probability matrix M. The steady-state ranking and authority score of every webpage is the principal eigenvector corresponding to eigenvalue λ = 1.\n• Deep Learning Stability: The eigenvalues of neural weight matrices determine gradient flow—preventing exploding gradients (when λ > 1) or vanishing gradients (when λ < 1) through Spectral Normalization."
            }
        ],
        "key_takeaways": [
            "The word 'Eigen' is German for 'own' or 'characteristic'; eigenvectors keep their direction under matrix transformation.",
            "Equation Av = λv: expensive matrix-vector multiplication Av collapses into simple scalar scaling λv.",
            "Eigenvalue values: λ > 1 stretches, 0 < λ < 1 shrinks, λ = 1 remains unchanged, λ < 0 flips 180°, and λ = 0 collapses.",
            "In PCA, eigenvectors are the Principal Components (directions of max variance); eigenvalues quantify the variance along each axis.",
            "Spectral Theorem: for symmetric matrices (A = Aᵀ), all eigenvalues are real and all eigenvectors are mutually orthogonal.",
            "Google's PageRank computes the principal eigenvector with λ = 1 to find steady-state web page authority."
        ],
        "definition_bullets": [
            "Eigenvector: A direction that does not rotate under matrix transformation; only stretches or shrinks.",
            "Eigenvalue (λ): The scalar factor by which the eigenvector stretches (λ > 1), shrinks (0 < λ < 1), or flips (λ < 0).",
            "PCA & Spectral Theorem: Eigenvectors identify principal axes of variance; for symmetric matrices, all eigenvectors are orthogonal."
        ]
    },
    {
        "id": "concept_svd",
        "title": "Singular Value Decomposition (SVD)",
        "topic_id": "math_linalg",
        "topic_label": "Linear Algebra & Vector Spaces",
        "category": "math",
        "category_label": "Mathematical Foundations",
        "raw_subtopic": "Singular Value Decomposition (SVD for compression)",
        "def": "A fundamental matrix factorization theorem stating that any arbitrary real matrix can be factored into rotation, scaling, and second rotation matrices.",
        "formula": "$$A = U \\Sigma V^T, \\quad A \\approx U_k \\Sigma_k V_k^T = \\sum_{i=1}^k \\sigma_i u_i v_i^T$$",
        "logic": "Eckart-Young Theorem proves that truncated SVD provides the provably optimal rank-$k$ approximation of any matrix under the Frobenius norm, maximizing preserved information while compressing storage.",
        "example": "Netflix Prize collaborative filtering: A massive user-movie rating matrix [500,000 users × 20,000 movies] is decomposed via truncated SVD to rank 50, revealing latent movie genres and user taste archetypes.",
        "tags": [
            "SVD",
            "Matrix Factorization",
            "Dimensionality Reduction",
            "Recommender Systems"
        ]
    },
    {
        "id": "concept_tensors",
        "title": "Tensors & Multidimensional Arrays",
        "topic_id": "math_linalg",
        "topic_label": "Linear Algebra & Vector Spaces",
        "category": "math",
        "category_label": "Mathematical Foundations",
        "raw_subtopic": "Tensors (Multidimensional arrays for batches and images)",
        "def": "A generalized mathematical array of numbers spanning arbitrary dimensions (rank 0 = scalar, rank 1 = vector, rank 2 = matrix, rank 3+ = tensor).",
        "formula": "$$\\mathcal{T} \\in \\mathbb{R}^{B \\times S \\times D} \\quad (\\text{Batch} \\times \\text{Sequence Length} \\times \\text{Embedding Dimension})$$",
        "logic": "Deep learning models compute on contiguous multi-dimensional memory blocks. Tensor broadcasting allows operations across tensors of mismatched shapes without redundant memory allocations.",
        "example": "A mini-batch of video clips: Stored as a 5D tensor of shape `[Batch_Size=16, Frames=30, Channels=3, Height=224, Width=224]`.",
        "tags": [
            "Tensors",
            "PyTorch",
            "Array Programming",
            "Deep Learning Data"
        ]
    },
    {
        "id": "concept_partial_derivatives",
        "title": "Partial Derivatives & Slopes",
        "topic_id": "math_calc",
        "topic_label": "Calculus & Optimization Dynamics",
        "category": "math",
        "category_label": "Mathematical Foundations",
        "raw_subtopic": "Partial Derivatives & Univariate Slopes",
        "def": "The rate of change of a multivariable function with respect to one single variable while holding all other variables constant as fixed values.",
        "formula": "$$\\frac{\\partial f}{\\partial x_i} = \\lim_{h \\to 0} \\frac{f(x_1, \\dots, x_i + h, \\dots, x_d) - f(x_1, \\dots, x_i, \\dots, x_d)}{h}$$",
        "logic": "Neural networks possess millions or billions of parameters. Partial derivatives isolate the individual sensitivity of the total loss to small perturbations of each specific weight.",
        "example": "Predicting car price from house age and square footage: $\\frac{\\partial \\text{Price}}{\\partial \\text{SqFt}}$ tells you how much the price rises per extra square foot, keeping house age strictly fixed.",
        "tags": [
            "Calculus",
            "Derivatives",
            "Sensitivity",
            "Optimization"
        ]
    },
    {
        "id": "concept_chain_rule",
        "title": "The Chain Rule of Calculus",
        "topic_id": "math_calc",
        "topic_label": "Calculus & Optimization Dynamics",
        "category": "math",
        "category_label": "Mathematical Foundations",
        "raw_subtopic": "The Chain Rule of Calculus (Nested functions f(g(x)))",
        "def": "The mathematical formula for computing the derivative of composite, nested functions by multiplying the derivatives of each intermediate sub-function.",
        "formula": "$$\\frac{d}{dx} [f(g(x))] = f'(g(x)) \\cdot g'(x), \\quad \\frac{\\partial z}{\\partial x} = \\sum_k \\frac{\\partial z}{\\partial u_k} \\frac{\\partial u_k}{\\partial x}$$",
        "logic": "The chain rule is the mathematical bedrock of backpropagation. A neural network is simply a chain of composite functions $y = f_L(f_{L-1}(\\dots f_1(x)))$; gradients propagate backward layer by layer via sequential chain rule multiplications.",
        "example": "If your speed affects fuel consumption ($d\\text{Fuel}/d\\text{Speed}$), and pedal pressure affects speed ($d\\text{Speed}/d\\text{Pedal}$), the chain rule gives the direct impact of pedal pressure on fuel usage ($d\\text{Fuel}/d\\text{Pedal}$).",
        "tags": [
            "Chain Rule",
            "Calculus",
            "Backpropagation",
            "Deep Learning Foundations"
        ]
    },
    {
        "id": "concept_gradient_vector",
        "title": "Gradient Vector & Steepest Ascent",
        "topic_id": "math_calc",
        "topic_label": "Calculus & Optimization Dynamics",
        "category": "math",
        "category_label": "Mathematical Foundations",
        "raw_subtopic": "Gradient Vector (Direction of steepest increase)",
        "def": "A multi-dimensional vector collecting all partial derivatives of a scalar function, pointing directly in the compass direction of greatest rate of increase.",
        "formula": "$$\\nabla f(w) = \\left[ \\frac{\\partial f}{\\partial w_1}, \\frac{\\partial f}{\\partial w_2}, \\dots, \\frac{\\partial f}{\\partial w_d} \\right]^T, \\quad w^{(t+1)} = w^{(t)} - \\eta \\nabla f(w^{(t)})$$",
        "logic": "Because the gradient vector points in the direction of steepest increase, stepping in the negative gradient direction ($-\\nabla f$) guarantees the fastest local decrease in loss.",
        "example": "Hiking on a foggy hill (Google ML Crash Course analogy): You cannot see the valley floor, so you feel the ground tilt under your boots and step in the exact opposite direction of the upward slope.",
        "tags": [
            "Gradient",
            "Gradient Descent",
            "Optimization",
            "Vector Calculus"
        ]
    },
    {
        "id": "concept_hessian_matrix",
        "title": "Hessian Matrix & 2nd Order Curvature",
        "topic_id": "math_calc",
        "topic_label": "Calculus & Optimization Dynamics",
        "category": "math",
        "category_label": "Mathematical Foundations",
        "raw_subtopic": "Hessian Matrix (2nd order curvature & saddle points)",
        "def": "The square matrix of second-order partial derivatives describing the local curvature and bending of a multi-variable loss surface.",
        "formula": "$$H_{ij} = \\frac{\\partial^2 f}{\\partial w_i \\partial w_j}, \\quad H = \\begin{bmatrix} \\frac{\\partial^2 f}{\\partial w_1^2} & \\cdots & \\frac{\\partial^2 f}{\\partial w_1 \\partial w_d} \\\\ \\vdots & \\ddots & \\vdots \\\\ \\frac{\\partial^2 f}{\\partial w_d \\partial w_1} & \\cdots & \\frac{\\partial^2 f}{\\partial w_d^2} \\end{bmatrix}$$",
        "logic": "First-order gradients only tell you slope; second-order Hessians tell you if the slope is getting steeper or flatter. If eigenvalues of $H$ have mixed positive and negative signs, the point is a saddle point rather than an extremum.",
        "example": "XGBoost optimization: Taylor series expansion of loss uses the first derivative $g_i$ (gradient) and second derivative $h_i$ (Hessian diagonal) to calculate the exact optimal leaf weight analytically.",
        "tags": [
            "Hessian",
            "Second Order",
            "Curvature",
            "Newton Method",
            "XGBoost"
        ]
    },
    {
        "id": "concept_convex_optimization",
        "title": "Convex vs Non-Convex Loss Landscapes",
        "topic_id": "math_calc",
        "topic_label": "Calculus & Optimization Dynamics",
        "category": "math",
        "category_label": "Mathematical Foundations",
        "raw_subtopic": "Convex vs Non-Convex Loss Landscapes",
        "def": "A function is convex if a line segment drawn between any two points on the graph never lies below the graph itself. A convex function has exactly one unique global minimum and zero sub-optimal local minima.",
        "formula": "$$f(\\alpha x + (1-\\alpha)y) \\le \\alpha f(x) + (1-\\alpha)f(y) \\quad \\forall \\alpha \\in [0, 1], \\quad H(x) \\succeq 0$$",
        "logic": "Linear Regression and Logistic Regression are convex (guaranteed global optimum with standard gradient descent). Deep Neural Networks are non-convex with countless saddle points, requiring momentum, adaptive learning rates, and overparameterization to escape plateaus.",
        "example": "Convex bowl: A marble dropped into a soup bowl always rolls to the exact center bottom. Non-convex mountain range: A marble can get stuck in countless small puddles and ravines.",
        "tags": [
            "Convexity",
            "Optimization",
            "Global Minimum",
            "Loss Landscapes"
        ]
    },
    {
        "id": "concept_random_variables_variance",
        "title": "Random Variables, Expectation & Variance",
        "topic_id": "math_prob",
        "topic_label": "Probability & Statistical Inference",
        "category": "math",
        "category_label": "Mathematical Foundations",
        "raw_subtopic": "Random Variables, Expectation (Mean μ) & Variance (σ²)",
        "def": "A random variable maps random real-world outcomes to numerical values. Expectation is the probability-weighted average (mean), and variance measures how widely values spread around that mean.",
        "formula": "$$\\mathbb{E}[X] = \\mu = \\sum x_i P(x_i), \\quad \\text{Var}(X) = \\sigma^2 = \\mathbb{E}[(X - \\mu)^2] = \\mathbb{E}[X^2] - (\\mathbb{E}[X])^2$$",
        "logic": "Machine learning models are function approximators trained over empirical samples drawn from an underlying random distribution. Optimizing loss is equivalent to minimizing expected risk $\\mathbb{E}[\\mathcal{L}(y, \\hat{y})]$.",
        "example": "Fair die roll: Values 1 through 6 each with probability 1/6. Expected value is $\\mu = 3.5$, and variance is $\\sigma^2 = 2.92$.",
        "tags": [
            "Probability",
            "Expectation",
            "Variance",
            "Statistics"
        ]
    },
    {
        "id": "concept_prob_distributions",
        "title": "Distributions: Gaussian, Bernoulli & Poisson",
        "topic_id": "math_prob",
        "topic_label": "Probability & Statistical Inference",
        "category": "math",
        "category_label": "Mathematical Foundations",
        "raw_subtopic": "Distributions: Gaussian (Bell Curve), Bernoulli, Poisson",
        "def": "Mathematical functions that specify the probabilities of occurrence of different possible outcomes in an experiment.",
        "formula": "$$\\text{Gaussian: } p(x) = \\frac{1}{\\sqrt{2\\pi\\sigma^2}} e^{-\\frac{(x-\\mu)^2}{2\\sigma^2}}, \\quad \\text{Bernoulli: } P(y) = p^y (1-p)^{1-y}$$",
        "logic": "Selecting loss functions depends on the assumed output distribution: Gaussian assumption leads to Mean Squared Error; Bernoulli assumption leads to Binary Cross-Entropy; Poisson assumption leads to Poisson deviance loss.",
        "example": "Bernoulli models whether an ad is clicked (0 or 1); Gaussian models the continuous price of a used house; Poisson models the number of website visits per minute.",
        "tags": [
            "Distributions",
            "Gaussian",
            "Bernoulli",
            "Loss Foundations"
        ]
    },
    {
        "id": "concept_bayes_theorem",
        "title": "Bayes' Theorem: Prior, Likelihood & Posterior",
        "topic_id": "math_prob",
        "topic_label": "Probability & Statistical Inference",
        "category": "math",
        "category_label": "Mathematical Foundations",
        "raw_subtopic": "Bayes' Theorem: Prior, Likelihood, Evidence & Posterior",
        "def": "A mathematical formula that describes how to update the probability of a hypothesis as new evidence or data is observed.",
        "formula": "$$P(\\theta | \\mathcal{D}) = \\frac{P(\\mathcal{D} | \\theta) \\cdot P(\\theta)}{P(\\mathcal{D})} = \\frac{\\text{Likelihood} \\times \\text{Prior}}{\\text{Evidence}}$$",
        "logic": "Provides a formal mechanism to integrate domain knowledge (the Prior) with real observed data (the Likelihood) to reach a statistically sound revised conclusion (the Posterior).",
        "example": "Spam filtering: If 20% of all emails are spam (Prior $P(S)=0.2$), and the word 'lottery' appears in 80% of spam but only 1% of ham, Bayes' theorem computes the revised probability that an incoming email with 'lottery' is spam as ~95.2%.",
        "tags": [
            "Bayes Rule",
            "Probability",
            "Inference",
            "Naive Bayes"
        ]
    },
    {
        "id": "concept_mle_map",
        "title": "Maximum Likelihood (MLE) vs MAP Estimation",
        "topic_id": "math_prob",
        "topic_label": "Probability & Statistical Inference",
        "category": "math",
        "category_label": "Mathematical Foundations",
        "raw_subtopic": "Maximum Likelihood Estimation (MLE) vs MAP Estimation",
        "def": "MLE finds parameters that maximize the probability of observed data without any priors. MAP finds parameters that maximize the posterior, incorporating prior beliefs.",
        "formula": "$$\\hat{\\theta}_{\\text{MLE}} = \\arg\\max_\\theta \\sum_{i=1}^n \\log P(x_i | \\theta), \\quad \\hat{\\theta}_{\\text{MAP}} = \\arg\\max_\\theta \\left[ \\sum_{i=1}^n \\log P(x_i | \\theta) + \\log P(\\theta) \\right]$$",
        "logic": "Ridge regression is mathematically identical to MAP estimation assuming a zero-mean Gaussian prior on weights; Lasso regression is MAP with a zero-mean Laplace prior on weights.",
        "example": "Coin flip: If you flip a coin 3 times and get 3 heads, MLE concludes $P(\\text{Heads}) = 1.0$ (ridiculous). MAP with a prior centered at 0.5 concludes $P(\\text{Heads}) \\approx 0.625$.",
        "tags": [
            "MLE",
            "MAP",
            "Bayesian",
            "Regularization Duality"
        ]
    },
    {
        "id": "concept_clt_lln",
        "title": "Law of Large Numbers & Central Limit Theorem",
        "topic_id": "math_prob",
        "topic_label": "Probability & Statistical Inference",
        "category": "math",
        "category_label": "Mathematical Foundations",
        "raw_subtopic": "Law of Large Numbers & Central Limit Theorem",
        "def": "The Law of Large Numbers (LLN) states that sample averages converge to expected values as sample size grows. The Central Limit Theorem (CLT) states that the sum or average of independent random variables approaches a normal distribution, regardless of the original distribution shape.",
        "formula": "$$\\lim_{n \\to \\infty} \\bar{X}_n = \\mu, \\quad \\sqrt{n}\\left(\\bar{X}_n - \\mu\\right) \\xrightarrow{d} \\mathcal{N}(0, \\sigma^2)$$",
        "logic": "Allows data scientists to compute confidence intervals and conduct valid hypothesis tests (e.g. A/B testing z-tests) on arbitrary metrics because sample means are guaranteed to be normally distributed.",
        "example": "Rolling 100 dice: Individual dice outcomes are uniform flat [1, 2, 3, 4, 5, 6]. But if you roll 100 dice and sum them, the resulting sum across thousands of trials forms an exquisite bell curve centered at 350.",
        "tags": [
            "CLT",
            "Statistics",
            "A/B Testing",
            "Confidence Intervals"
        ]
    },
    {
        "id": "concept_shannon_entropy",
        "title": "Shannon Entropy",
        "topic_id": "math_info",
        "topic_label": "Information Theory & Cross-Entropy",
        "category": "math",
        "category_label": "Mathematical Foundations",
        "raw_subtopic": "Shannon Entropy (Measure of inherent uncertainty)",
        "def": "The average amount of information, surprise, or uncertainty inherent in the possible outcomes of a random variable.",
        "formula": "$$H(X) = -\\sum_{i=1}^n P(x_i) \\log_2 P(x_i)$$",
        "logic": "A deterministic event with probability 1.0 contains 0 bits of information (0 entropy, no surprises). Maximum entropy occurs when all outcomes are equally likely (maximum unpredictability).",
        "example": "A fair coin has $H = -(0.5 \\log_2 0.5 + 0.5 \\log_2 0.5) = 1.0$ bit of entropy. A rigged coin that lands on heads 99% of the time has $H = 0.08$ bits (almost no surprise).",
        "tags": [
            "Entropy",
            "Information Theory",
            "Uncertainty",
            "Decision Trees"
        ]
    },
    {
        "id": "concept_cross_entropy",
        "title": "Cross-Entropy Loss",
        "topic_id": "math_info",
        "topic_label": "Information Theory & Cross-Entropy",
        "category": "math",
        "category_label": "Mathematical Foundations",
        "raw_subtopic": "Cross-Entropy Loss (Standard classification objective)",
        "def": "A loss metric quantifying the difference between two probability distributions: the true distribution $P$ and the predicted distribution $Q$.",
        "formula": "$$H(P, Q) = -\\sum_{x} P(x) \\log Q(x) = -\\sum_{k=1}^K y_k \\log(\\hat{y}_k)$$",
        "logic": "The loss approaches infinity as the model predicts zero probability for the correct true class. This creates steep, aggressive corrective gradients when a model is confidently wrong.",
        "example": "Dog vs Cat classifier: True label is Dog [1, 0]. If the model predicts Dog with probability 0.99, loss is $-\\log(0.99) = 0.01$. If it foolishly predicts Dog with probability 0.01, loss is $-\\log(0.01) = 4.60$.",
        "tags": [
            "Cross Entropy",
            "Loss Functions",
            "Classification",
            "Log Loss"
        ]
    },
    {
        "id": "concept_kl_divergence",
        "title": "Kullback-Leibler (KL) Divergence",
        "topic_id": "math_info",
        "topic_label": "Information Theory & Cross-Entropy",
        "category": "math",
        "category_label": "Mathematical Foundations",
        "raw_subtopic": "Kullback-Leibler (KL) Divergence (Distribution distance)",
        "def": "An asymmetric measure of the statistical distance or information lost when an approximating distribution $Q$ is used to represent a true distribution $P$.",
        "formula": "$$D_{\\text{KL}}(P \\parallel Q) = \\sum_{x} P(x) \\log\\left( \\frac{P(x)}{Q(x)} \\right) = H(P, Q) - H(P)$$",
        "logic": "Always non-negative ($D_{\\text{KL}} \\ge 0$) via Gibbs' inequality, and zero if and only if $P = Q$. Used in Variational Autoencoders (VAEs) and RLHF / DPO to prevent fine-tuned models from drifting too far from their base pre-trained models.",
        "example": "LLM Alignment: In RLHF, a KL-penalty term $-\\beta D_{\\text{KL}}(\\pi_\\theta \\parallel \\pi_{\\text{ref}})$ prevents the agent from hacking the reward model by deviating into gibberish.",
        "tags": [
            "KL Divergence",
            "Information Distance",
            "VAE",
            "RLHF Alignment"
        ]
    },
    {
        "id": "concept_mutual_information",
        "title": "Mutual Information",
        "topic_id": "math_info",
        "topic_label": "Information Theory & Cross-Entropy",
        "category": "math",
        "category_label": "Mathematical Foundations",
        "raw_subtopic": "Mutual Information (Shared dependency between features)",
        "def": "A measure of the mutual dependence between two random variables; it quantifies how much knowing the value of one variable reduces uncertainty about the other.",
        "formula": "$$I(X; Y) = \\sum_{x, y} P(x, y) \\log\\left( \\frac{P(x, y)}{P(x) P(y)} \\right) = H(X) - H(X | Y)$$",
        "logic": "Unlike linear correlation (Pearson $r$) which only captures straight-line associations, Mutual Information captures arbitrary non-linear and non-monotonic relationships between features and labels.",
        "example": "Feature selection for credit default: A feature 'Age' and label 'Default' may have Pearson $r \\approx 0$ due to a U-shaped risk curve (very young and very old default more). Mutual Information easily captures this high predictive value.",
        "tags": [
            "Mutual Information",
            "Feature Selection",
            "Non-linear Dependence"
        ]
    }
]
