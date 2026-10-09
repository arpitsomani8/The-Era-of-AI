import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
CONCEPTS_PATH = os.path.join(ROOT_DIR, "src", "data", "concepts.json")
ALL_CONCEPTS_PATH = os.path.join(SCRIPT_DIR, "data_sources", "all_concepts.json")
MATH_PY = os.path.join(SCRIPT_DIR, "data_sources", "concepts_math.py")

svd_concept = {
    "id": "concept_svd",
    "title": "Singular Value Decomposition (SVD)",
    "topic_id": "math_linalg",
    "topic_label": "Linear Algebra & Vector Spaces",
    "category": "math",
    "category_label": "Mathematical Foundations",
    "raw_subtopic": "Singular Value Decomposition (SVD for compression)",
    "def": "A fundamental matrix factorization theorem stating that any arbitrary real matrix can be factored into rotation, scaling, and second rotation matrices: A = U Σ Vᵀ.",
    "formula": "$$A = U \\Sigma V^T = \\sum_{i=1}^r \\sigma_i u_i v_i^T, \\quad \\sigma_i = \\sqrt{\\lambda_i(A^T A)}$$",
    "logic": "Eckart-Young Theorem proves that truncated SVD provides the provably optimal rank-k approximation of any matrix under the Frobenius norm, maximizing preserved information while compressing storage.",
    "example": "Netflix Prize collaborative filtering: A massive user-movie rating matrix [500,000 users × 20,000 movies] is decomposed via truncated SVD to rank 50, revealing latent movie genres and user taste archetypes.",
    "tags": [
        "SVD",
        "Matrix Factorization",
        "Dimensionality Reduction",
        "Recommender Systems",
        "LoRA",
        "Linear Algebra"
    ],
    "raw_sub": "Singular Value Decomposition (SVD for compression)",
    "definition": "A fundamental matrix factorization theorem stating that any arbitrary real matrix can be factored into three matrices: A = U Σ Vᵀ (Left singular vectors, Singular values, and Right singular vectors).",
    "formula_explanation": "A = U Σ Vᵀ factors any m × n matrix into orthogonal matrix U (m × m), diagonal matrix Σ (m × n) with non-negative singular values σᵢ, and orthogonal matrix Vᵀ (n × n). Each singular value σᵢ = √(λᵢ(AᵀA)).",
    "simple_summary": "SVD is the universal decomposition of linear algebra: it breaks any rectangular spreadsheet of data into row concepts (U), column concepts (V), and concept importance dials (Σ). Truncating the smallest dials removes noise and compresses massive AI models.",
    "core_terms": [
        {
            "term": "Singular Value Decomposition (SVD)",
            "what_is_it": "• A mathematical theorem stating that ANY matrix of ANY shape can be cleanly factored into three sub-matrices: A = U Σ Vᵀ.\n• While eigenvalue decomposition only works on square matrices (n × n), SVD works universally on rectangular real-world datasets (e.g., 100,000 users × 50 features).",
            "analogy": "MIT mathematician Gilbert Strang called SVD 'the pinnacle of linear algebra'—it acts like a master prism, splitting messy mixed white light (raw data) into pure, independent color beams (latent concepts).",
            "why_it_matters": "It is the mathematical backbone of PCA, collaborative recommendation engines, data compression, and modern LLM parameter-efficient fine-tuning (LoRA)."
        },
        {
            "term": "Singular Values (Σ / Sigma)",
            "what_is_it": "• A diagonal matrix containing numbers (σ₁, σ₂, σ₃, ...) that measure how strong or important each hidden concept is.\n• They are always real numbers, non-negative, and sorted from largest to smallest (σ₁ ≥ σ₂ ≥ σ₃ ≥ ... ≥ 0).",
            "analogy": "Think of volume sliders on an audio mixing board: slider 1 plays 80% of the music, slider 2 plays 15%, while sliders 50 to 100 are just quiet background hiss that you can safely turn off.",
            "why_it_matters": "They quantify exactly how much information each dimension holds, and relate directly to eigenvalues via σᵢ = √(λᵢ) of AᵀA."
        },
        {
            "term": "Truncated SVD (Low-Rank Approximation)",
            "what_is_it": "• Keeping only the top k largest singular values and discarding the tiny tail values to compress data and remove noise.\n• By the Eckart–Young Theorem, this truncated matrix is mathematically the single best possible rank-k approximation of your original matrix.",
            "analogy": "Converting an uncompressed 50MB raw photo into a crisp 1MB JPEG—human eyes see the exact same image, but noise is gone and 98% storage is saved.",
            "why_it_matters": "Enables machines to store massive datasets efficiently, speed up matrix computations, and fine-tune billion-parameter LLMs using low-rank updates (LoRA)."
        }
    ],
    "types_header": "Comparison: Eigenvalue Decomposition vs. SVD",
    "types_badge": "Decomposition Differences",
    "quick_types": [
        {
            "type": "Matrix Shape Required",
            "definition": "Eigendecomposition requires square matrices (n × n). SVD works on any shape (m × n).",
            "looks_like": "Users × Items (100k × 5k) works natively"
        },
        {
            "type": "Universal Existence",
            "definition": "Eigendecomposition may fail to exist. SVD always exists for every matrix.",
            "looks_like": "Guaranteed for any real or complex matrix"
        },
        {
            "type": "Vector Orthogonality",
            "definition": "Eigenvectors are orthogonal only if symmetric. SVD vectors (U and V) are always orthogonal.",
            "looks_like": "Independent, perpendicular direction vectors"
        },
        {
            "type": "Values Type & Signs",
            "definition": "Eigenvalues can be negative or complex. Singular values are always real and non-negative (σᵢ ≥ 0).",
            "looks_like": "Always positive & sorted: σ₁ ≥ σ₂ ≥ ... ≥ 0"
        },
        {
            "type": "Primary AI / ML Use",
            "definition": "Eigenvalues: Spectral theory & loss landscapes. SVD: Compression, PCA, recommenders, and LoRA.",
            "looks_like": "Data compression, PCA, Recommenders, LoRA"
        }
    ],
    "symbol_guide": [
        {
            "symbol": "A",
            "meaning": "Original data matrix",
            "plain_english": "The m × n data table (e.g., m users × n products)"
        },
        {
            "symbol": "U",
            "meaning": "Left singular vectors",
            "plain_english": "m × m matrix linking rows (users) to hidden concepts"
        },
        {
            "symbol": "Σ (Sigma)",
            "meaning": "Singular values matrix",
            "plain_english": "m × n diagonal matrix measuring concept strengths (σ₁ ≥ σ₂ ≥ ...)"
        },
        {
            "symbol": "Vᵀ",
            "meaning": "Right singular vectors",
            "plain_english": "n × n matrix linking columns (products) to hidden concepts"
        },
        {
            "symbol": "σᵢ (sigma)",
            "meaning": "Singular value",
            "plain_english": "Strength of concept i; σᵢ = √(λᵢ(AᵀA))"
        },
        {
            "symbol": "Aₖ",
            "meaning": "Truncated rank-k matrix",
            "plain_english": "Optimal compressed approximation keeping only the top k concepts"
        }
    ],
    "numerical_example": "Connecting SVD with Eigenvalues using A = [[3, 0], [0, -2]]:\n\n1. Compute AᵀA:\n   AᵀA = [[3, 0], [0, -2]] × [[3, 0], [0, -2]] = [[9, 0], [0, 4]].\n\n2. Find Eigenvalues of AᵀA:\n   det(AᵀA - λI) = (9 - λ)(4 - λ) = 0  ==>  λ₁ = 9,  λ₂ = 4.\n\n3. Calculate Singular Values (σᵢ = √λᵢ):\n   σ₁ = √9 = 3\n   σ₂ = √4 = 2\n\nNotice:\n• Even though entry -2 was negative in matrix A, its singular value σ₂ = +2 is strictly positive!\n• SVD decomposes A into A = U Σ Vᵀ where Σ = [[3, 0], [0, 2]].\n• The first singular value σ₁ = 3 captures 3 / (3 + 2) = 60% of the total scale of the transformation!",
    "pitfalls": "Common Trap: Confusing SVD with Eigenvalue Decomposition. Eigendecomposition only works on square matrices and can produce complex/negative eigenvalues. SVD works on ANY rectangular matrix, and singular values are always real, non-negative, and sorted.",
    "core_logic": "Eckart-Young Theorem proves that truncated SVD provides the provably optimal rank-k approximation of any matrix under the Frobenius norm, maximizing preserved information while compressing storage.",
    "architectural_logic": "In deep learning and LLMs, weight updates are compressed using low-rank decomposition. LoRA (Low-Rank Adaptation) decomposes large fine-tuning weight matrices into rank-r products ΔW = A × B, directly utilizing SVD principles to reduce trainable parameters by over 99%.",
    "connected_logic": [
        {
            "title": "Core Intuition: Uncovering Hidden Concepts",
            "content": "• Real-world data (like 1M users × 5k products) is sparse, noisy, and unwieldy.\n• SVD uncovers latent themes (e.g. Action, Romance, Tech): U maps users to concepts, Σ ranks concept importance, and Vᵀ maps products to concepts."
        },
        {
            "title": "Geometric Meaning: Rotation → Stretch → Rotation",
            "content": "• Any linear transformation breaks down into three clean geometric steps:\n  1. Vᵀ: Pure rotation in the input space.\n  2. Σ: Pure stretching or squishing along coordinate axes (by factors σᵢ).\n  3. U: Pure rotation in the output space.\n• No skewing or distortion—just two rotations with an axis stretch in between."
        },
        {
            "title": "Truncated SVD: Optimal Noise Filtering",
            "content": "• Singular values decay rapidly (e.g. [100, 80, 60, 40, 20, ..., 0.1]). Keeping only the top k values preserves 95%+ of information while discarding noise.\n• By the Eckart–Young Theorem, this truncated matrix (Aₖ) is mathematically the single best possible rank-k approximation of the original data."
        },
        {
            "title": "Modern LLMs: Low-Rank Adaptation (LoRA)",
            "content": "• Fine-tuning billion-parameter models is too costly to update all weights W.\n• LoRA applies SVD's low-rank principle: since the weight update ΔW has a very low intrinsic rank, it decomposes ΔW = A × B (r ≪ d), saving 99% GPU VRAM."
        }
    ],
    "key_takeaways": [
        "SVD factors ANY matrix of ANY shape (m × n) into three matrices: A = U Σ Vᵀ.",
        "Gilbert Strang called SVD 'the pinnacle of linear algebra' because it works universally where eigendecomposition fails.",
        "U captures row concepts (users), V captures column concepts (products), and Σ measures concept strengths.",
        "Singular values are always real, non-negative, and sorted in descending order: σ₁ ≥ σ₂ ≥ σ₃ ≥ ... ≥ 0.",
        "Singular values relate directly to eigenvalues of AᵀA via σᵢ = √(λᵢ).",
        "Truncated SVD discards noisy tail dimensions (Eckart–Young Theorem) and powers modern LLM fine-tuning via LoRA."
    ],
    "definition_bullets": [
        "SVD (A = U Σ Vᵀ): Universal factorization breaking any matrix into row concepts (U), concept strengths (Σ), and column concepts (Vᵀ).",
        "Singular Values (Σ): Real, non-negative scaling factors (σᵢ = √(λᵢ)) sorted by descending importance.",
        "Truncated SVD & LoRA: Discarding tail singular values for optimal low-rank compression and parameter-efficient LLM tuning."
    ]
}

# 1. Update src/data/concepts.json
with open(CONCEPTS_PATH, 'r', encoding='utf-8') as f:
    concepts = json.load(f)

for idx, c in enumerate(concepts):
    if c['id'] == 'concept_svd':
        concepts[idx] = svd_concept
        break

with open(CONCEPTS_PATH, 'w', encoding='utf-8') as f:
    json.dump(concepts, f, indent=2, ensure_ascii=False)
print("Updated src/data/concepts.json for concept_svd successfully!")

# 2. Update scripts/data_sources/all_concepts.json
if os.path.exists(ALL_CONCEPTS_PATH):
    with open(ALL_CONCEPTS_PATH, 'r', encoding='utf-8') as f:
        all_concepts = json.load(f)
    for idx, c in enumerate(all_concepts):
        if c['id'] == 'concept_svd':
            all_concepts[idx] = svd_concept
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
        if c['id'] == 'concept_svd':
            math_concepts[idx] = svd_concept
            break
    with open(MATH_PY, "w", encoding="utf-8") as f:
        f.write('"""\nConcepts Database: Mathematical Foundations (19 Concepts)\n"""\n\nMATH_CONCEPTS = ' + json.dumps(math_concepts, indent=4, ensure_ascii=False) + '\n')
    print("Updated concepts_math.py successfully!")
