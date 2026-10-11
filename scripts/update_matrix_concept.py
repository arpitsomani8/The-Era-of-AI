import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
CONCEPTS_PATH = os.path.join(ROOT_DIR, "src", "data", "concepts.json")
ALL_CONCEPTS_PATH = os.path.join(SCRIPT_DIR, "data_sources", "all_concepts.json")
MATH_PY = os.path.join(SCRIPT_DIR, "data_sources", "concepts_math.py")

matrix_concept = {
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
}

# 1. Update src/data/concepts.json
with open(CONCEPTS_PATH, 'r', encoding='utf-8') as f:
    concepts = json.load(f)

for idx, c in enumerate(concepts):
    if c['id'] == 'concept_matrix_mult_inverses':
        concepts[idx] = matrix_concept
        break

with open(CONCEPTS_PATH, 'w', encoding='utf-8') as f:
    json.dump(concepts, f, indent=2, ensure_ascii=False)
print("Updated src/data/concepts.json for concept_matrix_mult_inverses successfully!")

# 2. Update scripts/data_sources/all_concepts.json
if os.path.exists(ALL_CONCEPTS_PATH):
    with open(ALL_CONCEPTS_PATH, 'r', encoding='utf-8') as f:
        all_concepts = json.load(f)
    for idx, c in enumerate(all_concepts):
        if c['id'] == 'concept_matrix_mult_inverses':
            all_concepts[idx] = matrix_concept
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
        if c['id'] == 'concept_matrix_mult_inverses':
            math_concepts[idx] = matrix_concept
            break
    with open(MATH_PY, "w", encoding="utf-8") as f:
        f.write('"""\nConcepts Database: Mathematical Foundations (19 Concepts)\n"""\n\nMATH_CONCEPTS = ' + json.dumps(math_concepts, indent=4, ensure_ascii=False) + '\n')
    print("Updated concepts_math.py successfully!")
