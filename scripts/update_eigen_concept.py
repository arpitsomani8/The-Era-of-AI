import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
CONCEPTS_PATH = os.path.join(ROOT_DIR, "src", "data", "concepts.json")
ALL_CONCEPTS_PATH = os.path.join(SCRIPT_DIR, "data_sources", "all_concepts.json")
MATH_PY = os.path.join(SCRIPT_DIR, "data_sources", "concepts_math.py")

eigen_concept = {
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
}

# 1. Update src/data/concepts.json
with open(CONCEPTS_PATH, 'r', encoding='utf-8') as f:
    concepts = json.load(f)

for idx, c in enumerate(concepts):
    if c['id'] == 'concept_eigenvalues_eigenvectors':
        concepts[idx] = eigen_concept
        break

with open(CONCEPTS_PATH, 'w', encoding='utf-8') as f:
    json.dump(concepts, f, indent=2, ensure_ascii=False)
print("Updated src/data/concepts.json for concept_eigenvalues_eigenvectors successfully!")

# 2. Update scripts/data_sources/all_concepts.json
if os.path.exists(ALL_CONCEPTS_PATH):
    with open(ALL_CONCEPTS_PATH, 'r', encoding='utf-8') as f:
        all_concepts = json.load(f)
    for idx, c in enumerate(all_concepts):
        if c['id'] == 'concept_eigenvalues_eigenvectors':
            all_concepts[idx] = eigen_concept
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
        if c['id'] == 'concept_eigenvalues_eigenvectors':
            math_concepts[idx] = eigen_concept
            break
    with open(MATH_PY, "w", encoding="utf-8") as f:
        f.write('"""\nConcepts Database: Mathematical Foundations (19 Concepts)\n"""\n\nMATH_CONCEPTS = ' + json.dumps(math_concepts, indent=4, ensure_ascii=False) + '\n')
    print("Updated concepts_math.py successfully!")
