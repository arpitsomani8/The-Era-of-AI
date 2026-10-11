# -*- coding: utf-8 -*-
"""
Script to modernize dense-vector-embeddings in
src/data/concepts.json and scripts/data_sources/all_concepts.json.
"""

import json

new_concept = {
    "id": "dense-vector-embeddings",
    "topic_id": "genai_embed",
    "topic_label": "Tokenization & Vector Embeddings",
    "category": "genai",
    "category_label": "Generative AI & LLMs",
    "title": "Dense Vector Embeddings & Semantic Geometry",
    "raw_subtopic": "Dense Vector Embeddings & Semantic Geometry",
    "raw_sub": "Dense Vector Embeddings (Semantic clustering)",
    "def": "Dense vector embeddings map discrete text, multimodal entities, or documents into continuous, real-valued geometric vector spaces R^d where geometric proximity (cosine similarity, inner product, Euclidean distance) encodes latent semantic relationships, analogies, and functional equivalence.",
    "definition": "Dense vector embeddings form the mathematical bedrock of modern Natural Language Processing, semantic search engines, recommendation algorithms, and Retrieval-Augmented Generation (RAG). In traditional sparse representations (such as one-hot encodings, bag-of-words, or TF-IDF), text is represented by high-dimensional vectors with thousands of dimensions where almost all entries are zero. In these sparse spaces, distinct words are strictly orthogonal: 'heart attack' and 'cardiac arrest' share zero overlapping features, rendering their inner product zero despite identical medical meaning. In contrast, a dense vector embedding maps an entity into a continuous d-dimensional vector space R^d (typically d in [384, 1536]) where every entry is a learned, informative real-valued number. The geometric relationships between vectors—known as semantic geometry—reflect learned patterns of meaning: vectors pointing in similar directions denote semantic affinity, while orthogonal or opposing vectors denote distinct or contrasting concepts. The paradigm evolved from static word embeddings (Word2Vec, GloVe), which suffered from polysemy conflation (assigning the exact same vector to 'bank' for both riverbanks and financial institutions), to contextual Transformer hidden states (BERT), and finally to specialized pooled sentence/passage representations (Sentence-BERT, ColBERT, OpenAI text-embedding-3). Comparing embeddings relies on three foundational metrics: Dot Product (sensitive to both angle and length), Cosine Similarity (directional angle independent of length), and Euclidean Distance (straight-line spatial gap). When vectors are L2-normalized to unit length, cosine similarity simplifies to the dot product, and squared Euclidean distance reduces directly to 2 - 2*cos(theta), enabling ultra-fast Approximate Nearest Neighbor (ANN) vector retrieval across millions of documents.",
    "simple_summary": "Think of a dense vector embedding like a set of GPS coordinates for human meaning. If you only used traditional keyword search, computers would treat words like blind file names: 'dog' and 'puppy' would look completely unrelated because they don't share the same letters. Dense vector embeddings solve this by giving every concept an address in a 768-dimensional 'map of ideas'. On this semantic map, 'dog' and 'puppy' are located on the same street, 'cat' is located one block over in the pet neighborhood, and 'stock market crash' is located thousands of miles away on a financial island. When you search for 'How do I recover my locked account?', the search engine doesn't just look for matching letters; it finds the document whose GPS coordinate points in the exact same direction ('Steps to reset your forgotten password'). By measuring the angle (cosine similarity) between your question and millions of documents, AI models find the right answer in milliseconds even when using totally different words.",
    "definition_bullets": [
        "Dense vs. Sparse Duality: Replaces high-dimensional, orthogonal sparse vectors (TF-IDF, one-hot) with dense, continuous vectors e in R^d capturing semantic synonymy and contextual nuance.",
        "The Three Geometric Metrics: Compares representations via Dot Product (a . b), Cosine Similarity (a . b / (||a|| ||b||)), and Euclidean Distance (||a - b||_2).",
        "Unit Hypersphere Equivalence: For L2-normalized embeddings (||a|| = 1), the dot product equals cosine similarity, and squared Euclidean distance simplifies to 2 - 2*cos(theta).",
        "Evolution of Embedding Models: Progressed from static word vectors (Word2Vec, GloVe) to contextual token states (BERT) to specialized pooled sentence/passage embeddings (Sentence-BERT, OpenAI text-embedding-3).",
        "Foundation of Modern RAG & Search: Powers vector databases, Approximate Nearest Neighbor (ANN) indexing (HNSW, IVF), and semantic retrieval engines."
    ],
    "core_terms": [
        {
            "term": "Dense Vector Embedding",
            "what_is_it": "An ordered list of real-valued numbers where most or all entries are non-zero, encoding semantic properties of text or data.",
            "definition": "A continuous vector e in R^d (commonly d=384, 768, 1024, or 1536) learned through self-supervised or contrastive neural network training, where coordinates represent latent distributed features rather than human-assigned labels.",
            "analogy": "A detailed 50-point sensory tasting profile of a wine (acidity, sweetness, oakiness, body) where every measurement has a subtle value, rather than a single coarse sticker that just says 'red' or 'white'.",
            "why_it_matters": "Enables neural networks and search engines to compare the semantic similarity of text, images, or audio mathematically through linear algebra."
        },
        {
            "term": "Embedding Space & Semantic Geometry",
            "what_is_it": "The continuous high-dimensional coordinate space where vectors reside, and the geometric relationships governing them.",
            "definition": "The metric space R^d endowed with a distance metric (cosine, Euclidean) such that semantic relationships between entities correspond to geometric distances and directional alignments between their vector points.",
            "analogy": "A giant 3D celestial star chart where stars representing similar constellations cluster together in distinct galaxies.",
            "why_it_matters": "Governs how vector databases (Pinecone, Qdrant, Milvus) index and cluster data for instant semantic retrieval in LLM pipelines."
        },
        {
            "term": "Cosine Similarity",
            "what_is_it": "A metric that measures the cosine of the angle between two vectors, completely independent of their lengths.",
            "definition": "A similarity measure cos(theta) = (a . b) / (||a|| ||b||) ranging from -1 to 1 for non-zero vectors, where 1 indicates identical direction, 0 indicates orthogonality (unrelated), and -1 indicates opposite orientation.",
            "analogy": "Checking if two compass needles point in the same direction, regardless of whether one needle is 2 inches long and the other is 10 feet long.",
            "why_it_matters": "The standard metric for text and document comparison because document length (which scales vector magnitude) should not distort topical similarity."
        },
        {
            "term": "Unit Hypersphere Normalization (L2 Normalization)",
            "what_is_it": "Dividing a vector by its Euclidean length so that its magnitude becomes exactly 1.0.",
            "definition": "The transformation v_hat = v / ||v||_2 projecting any non-zero vector onto the surface of a unit hypersphere S^{d-1}, ensuring ||v_hat||_2 = 1.",
            "analogy": "Standardizing all recipe ingredients into percentages of the whole dish, so a recipe for 2 people can be directly compared to a recipe for 200 people.",
            "why_it_matters": "Turns expensive cosine similarity calculations into simple matrix multiplications (dot products) and establishes exact equivalence with Euclidean distance."
        },
        {
            "term": "Static vs. Contextual Embeddings",
            "what_is_it": "The distinction between fixed per-word vectors versus dynamic representations that change with surrounding context.",
            "definition": "Static embeddings (Word2Vec, GloVe) assign a single immutable vector to each vocabulary word regardless of context. Contextual embeddings (BERT, RoBERTa, GPT) dynamically compute different vectors for the same token depending on its surrounding sentence (e.g. 'river bank' vs 'investment bank').",
            "analogy": "An actor reading lines with identical flat monotone in every scene (static) versus adapting their tone, emotion, and meaning to the specific dialogue (contextual).",
            "why_it_matters": "Resolves polysemy and homonymy, dramatically improving search accuracy and language understanding."
        },
        {
            "term": "Approximate Nearest Neighbors (ANN & Vector DBs)",
            "what_is_it": "Algorithmic data structures that find the most similar vectors in sub-linear time without checking every item.",
            "definition": "Indexing techniques (such as Hierarchical Navigable Small World graphs [HNSW] or Inverted File with Product Quantization [IVF-PQ]) that trade a tiny fraction of recall accuracy for logarithmic O(log N) search latency across billions of vectors.",
            "analogy": "Using a well-organized library card catalog to find a relevant book in seconds rather than walking down every aisle reading the title of every single book.",
            "why_it_matters": "Allows real-world RAG systems and search engines to retrieve relevant document chunks from millions of candidates in under 15 milliseconds."
        }
    ],
    "symbol_guide": [
        {
            "symbol": "e in R^d",
            "name": "Dense Embedding Vector",
            "meaning": "An ordered list of d real-valued numbers representing a text, document, or entity (commonly d=384, 768, 1024, or 1536).",
            "plain_english": "The numerical profile vector representing the meaning of a piece of text."
        },
        {
            "symbol": "a . b",
            "name": "Inner Dot Product",
            "meaning": "The sum of the products of corresponding elements: sum_{i=1}^d a_i b_i; combines directional alignment and magnitude.",
            "plain_english": "Multiplying matching numbers in two vectors and adding up the total."
        },
        {
            "symbol": "||a||_2",
            "name": "Euclidean Norm (L2 Norm)",
            "meaning": "The geometric length or magnitude of vector a: sqrt(sum_{i=1}^d a_i^2).",
            "plain_english": "The straight-line length of the vector from the origin."
        },
        {
            "symbol": "cos(theta)",
            "name": "Cosine Similarity",
            "meaning": "The cosine of the angle theta between two vectors: (a . b) / (||a||_2 ||b||_2), bounded in [-1, 1].",
            "plain_english": "A score from -1 to +1 showing how closely two vectors point in the same direction."
        },
        {
            "symbol": "d(a, b)",
            "name": "Euclidean Distance",
            "meaning": "The straight-line spatial distance between two vectors: sqrt(sum_{i=1}^d (a_i - b_i)^2).",
            "plain_english": "The physical distance between two points in high-dimensional space."
        },
        {
            "symbol": "v_hat = v / ||v||",
            "name": "Normalized Unit Vector",
            "meaning": "Vector scaled to have Euclidean length exactly equal to 1.0.",
            "plain_english": "A vector reshaped so its length is 1, keeping only its direction."
        },
        {
            "symbol": "E in R^{V x d}",
            "name": "Embedding Table Matrix",
            "meaning": "Matrix storing dense vectors for all V vocabulary tokens in an LLM.",
            "plain_english": "The giant spreadsheet storing a vector for every token in the model's vocabulary."
        }
    ],
    "formula": "$$\\text{Dot Product: } \\mathbf{a} \\cdot \\mathbf{b} = \\sum_{i=1}^d a_i b_i$$\n\n$$\\text{Cosine Similarity: } \\cos(\\theta) = \\frac{\\mathbf{a} \\cdot \\mathbf{b}}{\\|\\mathbf{a}\\|_2 \\|\\mathbf{b}\\|_2} = \\frac{\\sum_{i=1}^d a_i b_i}{\\sqrt{\\sum_{i=1}^d a_i^2} \\sqrt{\\sum_{i=1}^d b_i^2}}$$\n\n$$\\text{Euclidean Distance: } d(\\mathbf{a}, \\mathbf{b}) = \\|\\mathbf{a} - \\mathbf{b}\\|_2 = \\sqrt{\\sum_{i=1}^d (a_i - b_i)^2}$$\n\n$$\\text{Unit Hypersphere Equivalence (when } \\|\\mathbf{a}\\| = \\|\\mathbf{b}\\| = 1\\text{): } \\|\\mathbf{a} - \\mathbf{b}\\|_2^2 = 2 - 2\\cos(\\theta), \\quad \\mathbf{a} \\cdot \\mathbf{b} = \\cos(\\theta)$$\n\n$$\\text{Semantic Vector Arithmetic: } \\mathbf{v}_{\\text{king}} - \\mathbf{v}_{\\text{man}} + \\mathbf{v}_{\\text{woman}} \\approx \\mathbf{v}_{\\text{queen}}$$\n\n$$\\text{Sentence Pooling (Mean-Pooling): } \\mathbf{e}_{\\text{sent}} = \\frac{\\sum_{t=1}^T m_t \\mathbf{h}_t}{\\sum_{t=1}^T m_t}, \\quad m_t = \\text{attention\\_mask}$$\n\n$$\\text{Contrastive InfoNCE Objective: } \\mathcal{L} = -\\log \\frac{\\exp(\\text{sim}(\\mathbf{q}, \\mathbf{d}^+) / \\tau)}{\\exp(\\text{sim}(\\mathbf{q}, \\mathbf{d}^+) / \\tau) + \\sum_{j} \\exp(\\text{sim}(\\mathbf{q}, \\mathbf{d}_j^-) / \\tau)}$$",
    "logic": "The power of dense vector embeddings stems from their continuous geometric representation of semantic meaning. In traditional sparse vector spaces (like one-hot or TF-IDF), every distinct word is assigned an independent orthogonal axis. Because orthogonal axes have zero inner product, sparse spaces suffer from the 'vocabulary mismatch problem': they cannot recognize that 'heart attack' and 'cardiac arrest' mean the same thing, or that 'automobile' is a synonym for 'car'.\n\nDense embeddings resolve this by mapping tokens or full sentences into a shared, continuous vector space R^d where semantic relatedness corresponds to directional alignment and spatial closeness:\n\n1. Angle vs. Magnitude: The raw dot product a . b is sensitive to both the angle between vectors and their lengths. In text embeddings, longer documents or frequent tokens can develop larger vector magnitudes simply because they accumulate more activation energy. Cosine similarity normalizes by vector length, ensuring that document length does not distort semantic affinity. For unit-normalized vectors (||a|| = 1), dot product and cosine similarity become mathematically identical.\n\n2. Metric Equivalence on Unit Spheres: In production vector search, computing Euclidean distance or cosine similarity is equivalent once vectors are L2-normalized: ||a - b||^2 = ||a||^2 + ||b||^2 - 2(a . b) = 1 + 1 - 2*cos(theta) = 2 - 2*cos(theta). Thus, maximizing cosine similarity is mathematically identical to minimizing Euclidean distance.\n\n3. The Polysemy Problem: Static word embeddings (Word2Vec, GloVe) assign one fixed vector to each vocabulary token, conflating multiple meanings of polysemous words (such as 'apple' the fruit vs. 'Apple' the tech company). Modern embedding systems resolve this via Contextual Pooling: a Transformer encoder (like BERT or MiniLM) first contextualizes each token via multi-head self-attention, and then a pooling operator (mean pooling across non-padding tokens) collapses the contextual sequence into a single dense sentence embedding that captures the holistic nuance of the passage.",
    "example": "Consider a customer service RAG assistant for an e-commerce platform. A user submits the query: 'How can I get my money back for a broken item?'\n\n1. Keyword Search (Sparse BM25): Fails to match a policy document titled 'Initiating a refund request for damaged merchandise' because zero keywords overlap ('money back' vs 'refund', 'broken' vs 'damaged').\n\n2. Dense Semantic Search (Sentence-BERT / text-embedding-3-small):\n   - Query Vector: e_query in R^1536\n   - Document A Vector ('Initiating a refund request for damaged merchandise'): Cosine Similarity = 0.91 (Retrieved #1)\n   - Document B Vector ('Steps to return an unwanted gift'): Cosine Similarity = 0.74 (Retrieved #2)\n   - Document C Vector ('Track your delivery status'): Cosine Similarity = 0.42\n   - Document D Vector ('Chocolate cake recipe'): Cosine Similarity = 0.08\n\nThe dense embedding system correctly connects the query to the refund document despite zero verbatim keyword overlap.",
    "numerical_example": "Step 1: Worked Numerical Comparison of Toy Vectors (Matching Lesson Walkthrough)\nConsider three illustrative 2D vectors:\n  a = [1, 2]  (e.g., 'dog')\n  b = [2, 4]  (e.g., 'puppy' - exact same direction, doubled magnitude)\n  c = [2, -1] (e.g., 'stock market' - orthogonal / unrelated)\n\nStep 1a: Compare vector a and vector b:\n  - Dot Product: a . b = (1 * 2) + (2 * 4) = 2 + 8 = 10.0\n  - Magnitude of a: ||a|| = sqrt(1^2 + 2^2) = sqrt(1 + 4) = sqrt(5) approx 2.236\n  - Magnitude of b: ||b|| = sqrt(2^2 + 4^2) = sqrt(4 + 16) = sqrt(20) = 2*sqrt(5) approx 4.472\n  - Cosine Similarity:\n    cos(theta) = (a . b) / (||a|| * ||b||) = 10.0 / (sqrt(5) * sqrt(20)) = 10.0 / sqrt(100) = 10.0 / 10.0 = 1.0\n  -> Both vectors point in the EXACT same direction (angle theta = 0 degrees), yielding maximum similarity 1.0!\n\nStep 1b: Compare vector a and vector c:\n  - Dot Product: a . c = (1 * 2) + (2 * -1) = 2 - 2 = 0.0\n  - Magnitude of c: ||c|| = sqrt(2^2 + (-1)^2) = sqrt(4 + 1) = sqrt(5) approx 2.236\n  - Cosine Similarity:\n    cos(theta) = 0.0 / (sqrt(5) * sqrt(5)) = 0.0 / 5.0 = 0.0\n  -> Vectors a and c are perpendicular (angle theta = 90 degrees), indicating completely unrelated concepts!\n\nStep 1c: Verify Euclidean Distance on L2-Normalized Vectors:\n  - Normalized a: a_hat = [1/sqrt(5), 2/sqrt(5)] = [0.4472, 0.8944]\n  - Normalized b: b_hat = [2/sqrt(20), 4/sqrt(20)] = [1/sqrt(5), 2/sqrt(5)] = [0.4472, 0.8944]\n  - Euclidean Distance: ||a_hat - b_hat||_2 = sqrt((0.4472 - 0.4472)^2 + (0.8944 - 0.8944)^2) = 0.0\n  - Using Formula: ||a_hat - b_hat||^2 = 2 - 2*cos(theta) = 2 - 2(1.0) = 0.0 (exact match!).\n\nStep 2: Practical Python Semantic Search Implementation\n```python\nimport numpy as np\nfrom sentence_transformers import SentenceTransformer\n\n# Load pretrained sentence embedding model (384 dimensions)\nmodel = SentenceTransformer('all-MiniLM-L6-v2')\n\ndocuments = [\n    'Reset your password from the account settings page.',\n    'Learn how to bake a chocolate cake.',\n    'Recover access to your account if you forgot your login.',\n    'Today\\'s weather forecast predicts heavy rain.'\n]\n\n# Encode documents with L2 unit normalization\ndocument_embeddings = model.encode(documents, normalize_embeddings=True)\nprint('Document embeddings shape:', document_embeddings.shape)  # (4, 384)\n\nquery = 'How can I recover my account?'\nquery_embedding = model.encode(query, normalize_embeddings=True)  # (384,)\n\n# Dot product equals cosine similarity for normalized unit vectors!\nscores = document_embeddings @ query_embedding\n\n# Rank documents by highest similarity\nranked_indices = np.argsort(scores)[::-1]\n\nprint('\\n--- Semantic Search Results for:', query, '---')\nfor rank, idx in enumerate(ranked_indices, start=1):\n    print(f'{rank}. Score: {scores[idx]:.4f} | {documents[idx]}')\n```",
    "types_header": "Vector Embedding Architectures & Similarity Metrics",
    "types_badge": "Semantic Foundations",
    "quick_types": [
        {
            "type": "Dense Sentence / Passage Embedding",
            "name": "Dense Sentence / Passage Embedding",
            "definition": "A fixed-size dense vector (e.g. 384-d MiniLM, 1536-d OpenAI) generated by pooling transformer states to represent the holistic semantic meaning of a complete passage.",
            "description": "A fixed-size dense vector (e.g. 384-d MiniLM, 1536-d OpenAI) generated by pooling transformer states to represent the holistic semantic meaning of a complete passage.",
            "looks_like": "[0.024, -0.089, 0.152, ..., -0.041] in R^768"
        },
        {
            "type": "Static Word Embedding (Word2Vec / GloVe)",
            "name": "Static Word Embedding (Word2Vec / GloVe)",
            "definition": "A single fixed vector assigned to each vocabulary word regardless of context, learned via word co-occurrence statistics. Fails on polysemy and homonyms.",
            "description": "A single fixed vector assigned to each vocabulary word regardless of context, learned via word co-occurrence statistics. Fails on polysemy and homonyms.",
            "looks_like": "E['bank'] -> fixed vector in R^300"
        },
        {
            "type": "Contextual Token State (Transformer Hidden State)",
            "name": "Contextual Token State (Transformer Hidden State)",
            "definition": "Dynamic representations computed by transformer self-attention where each token's vector reflects surrounding context (e.g. BERT hidden states).",
            "description": "Dynamic representations computed by transformer self-attention where each token's vector reflects surrounding context (e.g. BERT hidden states).",
            "looks_like": "H in R^{T x d_model} (one vector per sequence token)"
        },
        {
            "type": "Sparse Lexical Representation (BM25 / SPLADE)",
            "name": "Sparse Lexical Representation (BM25 / SPLADE)",
            "definition": "High-dimensional sparse vectors indexed by vocabulary terms where values denote term frequency or learned lexical importance. Strong on exact keyword matching.",
            "description": "High-dimensional sparse vectors indexed by vocabulary terms where values denote term frequency or learned lexical importance. Strong on exact keyword matching.",
            "looks_like": "{token_4895: 1.84, token_2244: 0.92} (99.9% zeros)"
        }
    ],
    "connected_logic": [
        {
            "title": "Dense Semantic Alignment vs. Sparse Exact Keyword Matching",
            "description": "Why modern search architectures pair dense embeddings with sparse lexical retrieval (Hybrid Search).",
            "content": "• Sparse retrieval (BM25, TF-IDF) excels at exact matches for rare identifiers, acronyms, and product IDs (e.g. 'SKU-89412B') where synonymy is irrelevant.\n• Dense embeddings excel at conceptual synonymy, semantic paraphrases, and multi-language queries where exact keywords differ.\n• Production search systems (Hybrid Search) fuse both signals using Reciprocal Rank Fusion (RRF) to achieve the best of both worlds.",
            "points": [
                "Sparse retrieval (BM25, TF-IDF) excels at exact matches for rare identifiers, acronyms, and product IDs (e.g. 'SKU-89412B') where synonymy is irrelevant.",
                "Dense embeddings excel at conceptual synonymy, semantic paraphrases, and multi-language queries where exact keywords differ.",
                "Production search systems (Hybrid Search) fuse both signals using Reciprocal Rank Fusion (RRF) to achieve the best of both worlds."
            ]
        },
        {
            "title": "The Geometry of Unit Hyperspheres & Metric Equivalence",
            "description": "How L2 normalization simplifies distance computation in high-dimensional spaces.",
            "content": "• Unnormalized dot product a . b combines directional angle and vector magnitudes, which can unfairly favor long passages with larger norms.\n• Cosine similarity cos(theta) = (a . b) / (||a|| ||b||) normalizes by length, isolating pure directional alignment.\n• By explicitly pre-normalizing all vectors to unit length (||v||_2 = 1), dot product becomes identical to cosine similarity: a_hat . b_hat = cos(theta), and squared Euclidean distance reduces to 2 - 2*cos(theta), enabling massive hardware SIMD speedups.",
            "points": [
                "Unnormalized dot product a . b combines directional angle and vector magnitudes, which can unfairly favor long passages with larger norms.",
                "Cosine similarity cos(theta) = (a . b) / (||a|| ||b||) normalizes by length, isolating pure directional alignment.",
                "By explicitly pre-normalizing all vectors to unit length (||v||_2 = 1), dot product becomes identical to cosine similarity: a_hat . b_hat = cos(theta), and squared Euclidean distance reduces to 2 - 2*cos(theta), enabling massive hardware SIMD speedups."
            ]
        },
        {
            "title": "Static Polysemy vs. Dynamic Contextual Pooling",
            "description": "Why sentence-level pooling of contextual transformer representations outperforms word-level averages.",
            "content": "• In static word embeddings (Word2Vec, GloVe), averaging word vectors wipes out word order and grammatical negation ('not guilty' averages into 'guilty').\n• Contextual models (BERT, RoBERTa) use bidirectional self-attention so that token vectors encode contextual qualifiers before pooling.\n• Mean pooling across non-padding contextual token vectors produces robust sentence representations that distinguish nuanced semantic conditions.",
            "points": [
                "In static word embeddings (Word2Vec, GloVe), averaging word vectors wipes out word order and grammatical negation ('not guilty' averages into 'guilty').",
                "Contextual models (BERT, RoBERTa) use bidirectional self-attention so that token vectors encode contextual qualifiers before pooling.",
                "Mean pooling across non-padding contextual token vectors produces robust sentence representations that distinguish nuanced semantic conditions."
            ]
        },
        {
            "title": "Scaling Semantic Search: Vector Databases & HNSW Indexing",
            "description": "How Approximate Nearest Neighbor (ANN) graphs solve the linear-scan bottleneck at web scale.",
            "content": "• Exhaustive brute-force search compares a query against all N stored vectors in O(N * d) time, which is too slow for millions of documents.\n• Hierarchical Navigable Small World (HNSW) indexes vectors into multi-layer proximity skip-graphs, navigating from coarse clusters to fine neighbors in O(log N) time.\n• Product Quantization (PQ) compresses 1536-d float32 vectors (6 KB each) into compact 64-byte codes, reducing RAM requirements by 90% while preserving high retrieval recall.",
            "points": [
                "Exhaustive brute-force search compares a query against all N stored vectors in O(N * d) time, which is too slow for millions of documents.",
                "Hierarchical Navigable Small World (HNSW) indexes vectors into multi-layer proximity skip-graphs, navigating from coarse clusters to fine neighbors in O(log N) time.",
                "Product Quantization (PQ) compresses 1536-d float32 vectors (6 KB each) into compact 64-byte codes, reducing RAM requirements by 90% while preserving high retrieval recall."
            ]
        }
    ],
    "pitfalls": [
        "Assuming Every Dimension Has a Human-Readable Meaning: Embedding dimensions are learned distributed representations; individual coordinate axes rarely correspond to clean isolated semantic labels.",
        "Confusing Embeddings with Token IDs: A token ID is a discrete scalar integer; an embedding is a continuous real-valued vector in R^d representing semantic position.",
        "Assuming High Similarity Guarantees Identical Meaning: Dense models can stumble on negation ('customer approved' vs 'customer did not approve') or subtle domain edge cases.",
        "Comparing Vectors Across Incompatible Models: Embeddings produced by different models (e.g. MiniLM vs OpenAI text-embedding-3) live in distinct coordinate spaces and cannot be compared directly.",
        "Using Cosine Similarity When Inner Product is Expected: Some models encode significance into vector magnitude; stripping magnitude via normalization alters scoring dynamics if the model was trained for inner product.",
        "Treating Similarity Scores as Calibrated Probabilities: A cosine similarity score of 0.82 reflects geometric directional alignment, not an 82% statistical probability of relevance.",
        "Relying on Cherry-Picked Query Evaluations: Production retrieval quality must be measured on real user query distributions using Mean Reciprocal Rank (MRR@K) and nDCG@K."
    ],
    "key_takeaways": [
        "Dense vector embeddings map discrete entities into continuous real-valued spaces R^d where geometric proximity encodes semantic relatedness.",
        "Cosine similarity measures the angle between vectors, normalizing for length and preventing document length from distorting semantic matching.",
        "For L2-normalized unit vectors, dot product equals cosine similarity, and squared Euclidean distance simplifies to 2 - 2*cos(theta).",
        "Dense embeddings form the foundation of modern search, recommendation, and RAG architectures, scaled via Approximate Nearest Neighbor (ANN) vector databases."
    ],
    "tags": [
        "Embeddings",
        "Semantic Search",
        "Cosine Similarity",
        "Vector Database",
        "RAG",
        "Sentence-BERT",
        "NLP",
        "LLMs",
        "Generative AI & LLMs"
    ]
}

def update_concepts_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        concepts = json.load(f)
    found = False
    for i, c in enumerate(concepts):
        if c.get('id') == new_concept['id']:
            concepts[i] = new_concept
            found = True
            break
    if not found:
        concepts.append(new_concept)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(concepts, f, indent=2, ensure_ascii=False)
        f.write('\n')
    print(f"Updated {filepath} successfully (found={found}, total={len(concepts)})")

if __name__ == '__main__':
    update_concepts_file('src/data/concepts.json')
    update_concepts_file('scripts/data_sources/all_concepts.json')
