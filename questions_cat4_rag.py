"""Category 4: RAG, Embeddings & Vector Search (Questions 76-95)"""

CAT4_QUESTIONS = [
    {
        "id": "rag_76",
        "category": "rag",
        "category_label": "RAG, Embeddings & Vector Search",
        "difficulty": "Mid / Senior",
        "company_tags": ["Google", "Pinecone", "Elasticsearch"],
        "question": "Compare Bi-Encoder and Cross-Encoder architectures for retrieval. Why are bi-encoders used for initial search while cross-encoders are reserved for re-ranking?",
        "answer": """**1. Bi-Encoder Architecture (Two-Tower):**
- Encodes Query $q$ and Document $d$ completely independently:
  $$u = E(q), \\quad v = E(d)$$
- Similarity is computed via a fast vector dot product: $\\text{sim}(q, d) = u^T v$.
- **Computational Benefit:** All $N$ documents in the corpus can be embedded and indexed **offline** into a vector database. At query time, we only embed the query once ($O(1)$) and perform fast MIPS/ANN vector search ($O(\\log N)$).
- **Drawback:** Zero cross-attention between query tokens and document tokens. Lower semantic precision.

**2. Cross-Encoder Architecture (Joint Encoding):**
- Concatenates Query and Document into a single sequence separated by `[SEP]`:
  $$\\text{Input} = [\\text{CLS}], q_1, \\dots, q_m, [\\text{SEP}], d_1, \\dots, d_n, [\\text{SEP}]$$
- Evaluates full bidirectional cross-attention between every query token and every document token across all Transformer layers.
- **Benefit:** Superb ranking precision; captures intricate syntactic and contextual nuances.
- **Drawback:** Cannot precompute document representations offline! Running a cross-encoder on a 10-million document corpus would take hours per query.

**3. Standard Two-Stage Production Architecture:**
1. **Stage 1 (Bi-Encoder):** Rapidly retrieves top 50-100 candidates from millions of documents in $< 10\\text{ms}$.
2. **Stage 2 (Cross-Encoder Re-ranker):** Evaluates cross-attention on only the top 50 candidates, re-ranking them to select the top 3-5 high-precision chunks for the LLM prompt in $\\approx 20\\text{ms}$.""",
        "tip": "Explain that the bi-encoder trades token-to-token interaction for offline precomputability, while the cross-encoder is an online reranker."
    },
    {
        "id": "rag_77",
        "category": "rag",
        "category_label": "RAG, Embeddings & Vector Search",
        "difficulty": "Mid / Senior",
        "company_tags": ["Cohere", "Qdrant", "Microsoft"],
        "question": "Compare BM25 (Sparse) and Dense Vector Retrieval. What are the failure modes of each, and how does Reciprocal Rank Fusion (RRF) combine them?",
        "answer": """**1. BM25 (Sparse Lexical Retrieval):**
- Based on term frequency (TF) and inverse document frequency (IDF) with saturation parameter $k_1$ and document length normalization $b$:
  $$\\text{BM25}(D, Q) = \\sum_{q \\in Q} \\text{IDF}(q) \\cdot \\frac{f(q, D)(k_1 + 1)}{f(q, D) + k_1(1 - b + b \\frac{|D|}{\\text{avgdl}})}$$
- **Strength:** Unbeatable for exact keyword matches, serial numbers, rare medical terms (ICD-10), and code identifiers (`ValueError: 404`).
- **Failure Mode (Vocabulary Mismatch):** Fails on synonyms, paraphrasing, or conceptual queries (e.g. querying *'automobile'* will never match a document about *'sedans'* unless the exact word is present).

**2. Dense Embeddings (Semantic Retrieval):**
- Maps text into continuous vectors ($d=768, 1536$) where semantic distance reflects conceptual similarity.
- **Strength:** Handles synonyms, multilingual queries, and intent matching.
- **Failure Mode:** Struggles with rare product IDs, alphanumeric codes, exact part numbers, and short keyword searches.

**3. Reciprocal Rank Fusion (RRF - Cormack et al.):**
A robust, score-agnostic rank combination formula:
$$\\text{RRF\\_Score}(d) = \\sum_{m \\in M} \\frac{1}{k + r_m(d)}$$
where $r_m(d)$ is the rank of document $d$ in system $m$ (1-indexed), and $k$ is a constant (typically $k=60$).
- Bypasses raw score calibration issues (BM25 $[0, 30]$ vs cosine similarity $[0, 1]$).
- If a document appears in the top 3 of either retriever, it is strongly elevated to the final context.""",
        "tip": "State clearly why RRF is favored over score addition: raw BM25 scores are unbounded, while cosine scores are bounded, making raw score normalization fragile."
    },
    {
        "id": "rag_78",
        "category": "rag",
        "category_label": "RAG, Embeddings & Vector Search",
        "difficulty": "Junior / Mid",
        "company_tags": ["Pinecone", "Milvus", "Weaviate"],
        "question": "When are Cosine Similarity, Dot Product, and Euclidean Distance mathematically identical for vector retrieval? Which is fastest on modern GPU/CPU hardware?",
        "answer": """**1. Mathematical Equivalence Under L2 Normalization:**
Let $u$ and $v$ be unit-normalized vectors: $\\|u\\|_2 = \\|v\\|_2 = 1$.
- **Cosine Similarity:**
  $$\\cos(u, v) = \\frac{u \\cdot v}{\\|u\\| \\|v\\|} = u \\cdot v$$
  For unit vectors, Cosine Similarity is **strictly identical to the Dot Product**!
- **Squared Euclidean Distance:**
  $$\\|u - v\\|_2^2 = \\|u\\|_2^2 + \\|v\\|_2^2 - 2 (u \\cdot v) = 1 + 1 - 2 (u \\cdot v) = 2 - 2 \\cos(u, v)$$
  Maximizing Cosine Similarity is strictly equivalent to minimizing Euclidean Distance!

**2. Hardware Execution Speed:**
- Calculating raw cosine similarity requires computing $\\sqrt{\\sum u_i^2}$ and dividing at query time ($O(d)$ square root + division).
- If embeddings are pre-normalized to unit length ($\\|v\\|=1$) at index time, retrieval reduces to a pure **matrix-vector dot product**: $Q \\cdot V^T$.
- Dot products map directly to highly optimized GEMM (General Matrix Multiply) operations on GPU Tensor Cores and CPU AVX-512 instructions, executing **$3-5\\times$ faster** than distance metrics with normalization or square roots.""",
        "tip": "Always advise pre-normalizing all vectors to unit norm so production databases can run blazing-fast dot products."
    },
    {
        "id": "rag_79",
        "category": "rag",
        "category_label": "RAG, Embeddings & Vector Search",
        "difficulty": "Senior / Staff",
        "company_tags": ["Meta", "Pinecone", "Google"],
        "question": "How does the Hierarchical Navigable Small World (HNSW) index work for Approximate Nearest Neighbor (ANN) search? What are the roles of parameters $M$, $efConstruction$, and $efSearch$?",
        "answer": """**1. HNSW Architecture (Malkov & Yashunin, 2018):**
Combines the multi-layer skip-list concept with Navigable Small World (NSW) proximity graphs:
- **Hierarchical Layers:** Organizes points into layers $l = 0, \\dots, L_{\\max}$.
  - Top layer $L_{\\max}$: Contains very few, widely spaced nodes with long-range links (express highway).
  - Bottom layer $0$: Contains all $N$ data points with dense local clustering.
- **Search Process:**
  1. Starts at the top entry point.
  2. Performs greedy search across long-distance links to quickly home in on the local neighborhood.
  3. Drops down to the next denser layer and resumes local search, terminating at layer 0.
  4. Achieves logarithmic search complexity: $O(\\log N)$.

**2. Core Hyperparameters & Trade-offs:**
- **$M$ (Max Connections per Node):** Number of bidirectional edges per node (typically $16-64$).
  - Higher $M$: Higher recall on complex manifolds, but higher RAM memory consumption and slower index build.
- **$efConstruction$ (Exploration Factor during Build):** Size of the dynamic candidate list evaluated during index construction (typically $100-200$).
  - Higher $efConstruction$: Slower indexing time, but superior graph quality and higher retrieval recall.
- **$efSearch$ (Exploration Factor during Query):** Size of the priority queue maintained during live search (typically $32-128$).
  - Higher $efSearch$: Increases query recall at the expense of higher query latency (ms). Can be tuned dynamically at runtime without rebuilding the index!""",
        "tip": "Explain that HNSW maintains the entire graph in RAM, making it blisteringly fast (<2ms) but memory-intensive."
    },
    {
        "id": "rag_80",
        "category": "rag",
        "category_label": "RAG, Embeddings & Vector Search",
        "difficulty": "Senior / Staff",
        "company_tags": ["Meta (FAISS)", "Qdrant", "Milvus"],
        "question": "What is Inverted File with Product Quantization (IVF-PQ)? How does it achieve 10x-50x compression of billion-scale vector datasets?",
        "answer": """**1. Inverted File (IVF - Coarse Quantization):**
- Clusters the vector space into $K$ Voronoi cells using K-Means (e.g. $K = 4096$).
- An inverted list stores which vectors belong to which centroid.
- At query time, only the $nprobe$ closest centroids (e.g. $nprobe = 16$) are searched, instantly pruning $99\\%$ of the dataset!

**2. Product Quantization (PQ - Fine Compression):**
A 1536-dimensional FP32 vector consumes $1536 \\times 4 = 6144\\text{ bytes}$.
PQ compresses this vector down to 64 bytes via decomposition:
1. Split 1536-dim vector into $M=64$ equal sub-vectors of dimension $d^* = 24$.
2. Run K-Means on each sub-space independently to find $K^* = 256$ sub-centroids.
3. Replace each 24-dim continuous sub-vector with an **8-bit integer index (0-255)** pointing to its nearest sub-centroid.
- **Memory:** $64\\text{ bytes}$ per vector instead of $6144\\text{ bytes}$! An astounding **$96\\times$ memory reduction**.

**3. Asymmetric Distance Computation (ADC):**
During query search, the query vector is kept unquantized. Distances between query sub-vectors and all 256 precomputed sub-centroids are stored in a lookup table. Distance evaluation requires only table lookups and integer additions, executing at billions of vectors per second!""",
        "tip": "Mention FAISS as the canonical library implementing IVF-PQ and powering Meta's billion-scale similarity search."
    },
    {
        "id": "rag_81",
        "category": "rag",
        "category_label": "RAG, Embeddings & Vector Search",
        "difficulty": "Mid",
        "company_tags": ["Anthropic", "Cohere", "Pinecone"],
        "question": "Compare RAG Chunking Strategies: Fixed-size chunking, Sentence-window chunking, Semantic chunking, and Parent-Document retrieval.",
        "answer": """- **Fixed-Size Chunking (with overlap):** E.g. 500 tokens with 50-token overlap.
  - *Pros:* Simple, fast, deterministic.
  - *Cons:* Frequently splits sentences or code blocks mid-thought, destroying semantic coherence.
- **Sentence-Window Chunking:** Embeds individual sentences for high-precision vector retrieval, but when a sentence matches, returns a surrounding window of $\\pm 3$ sentences to the LLM prompt.
  - *Pros:* Embeddings are hyper-focused, while LLM receives full conversational context.
- **Semantic Chunking:** Computes cosine distance between consecutive sentence embeddings; inserts a chunk break whenever similarity drops below a threshold percentile (signaling a topic shift).
  - *Pros:* Naturally preserves coherent thoughts.
- **Parent-Document Retrieval (Hierarchical):**
  - Chunks document into small sub-chunks (100 tokens) for dense vector search.
  - Links each sub-chunk to its larger **Parent Document** (1000 tokens).
  - Search hits small granular chunks, but injects the complete parent context into the LLM prompt, resolving the context vs precision dilemma.""",
        "tip": "Parent-Document Retrieval is widely regarded as the most robust architecture for complex technical PDFs and documentation."
    },
    {
        "id": "rag_82",
        "category": "rag",
        "category_label": "RAG, Embeddings & Vector Search",
        "difficulty": "Mid / Senior",
        "company_tags": ["Stanford", "Google", "OpenAI"],
        "question": "What is the 'Lost in the Middle' phenomenon (Liu et al., 2023) in long context LLMs? How should retrieved chunks be ordered in the prompt?",
        "answer": """**1. The Phenomenon:**
When an LLM is provided with a long context prompt containing multiple retrieved document chunks, its retrieval and reasoning accuracy follows a distinct **U-shaped curve**:
- **Primacy Bias:** Chunks placed at the very **beginning** of the prompt are recalled with high fidelity.
- **Recency Bias:** Chunks placed at the very **end** of the prompt (right before the user question) are recalled with high fidelity.
- **Lost in the Middle:** Performance plummets by up to $30-50\\%$ when critical facts are placed in the **middle** of a long context window.

**2. Prompt Engineering & Reranker Mitigation:**
Instead of sorting retrieved chunks in descending order of relevance ($1, 2, 3, 4, 5$), order them so the most critical chunks sit at the extremes:
- Slot 1 (Start of context): #1 Most Relevant Chunk.
- Slot 2 (End of context, right before question): #2 Most Relevant Chunk.
- Slot 3, 4: #3, #4 Chunks placed in the middle.
This ensures critical grounding evidence is placed in the model's highest-attention regions.""",
        "tip": "Explain that causal attention masks and RoPE frequency decay naturally bias attention toward initial system instructions and recent tokens."
    },
    {
        "id": "rag_83",
        "category": "rag",
        "category_label": "RAG, Embeddings & Vector Search",
        "difficulty": "Mid",
        "company_tags": ["Microsoft", "Elasticsearch"],
        "question": "What is Hypothetical Document Embeddings (HyDE - Gao et al., 2022)? When does it dramatically improve retrieval, and when does it fail?",
        "answer": """**1. Mechanism:**
1. Given a short or ambiguous user query $q$ (e.g. *'How to fix error 0x80070005?'*), ask an LLM to generate a **hypothetical ideal answer** document $\\hat{d}$ (even if it contains hallucinated details!).
2. Embed the hypothetical document: $v = \\text{Embed}(\\hat{d})$.
3. Use $v$ to search the vector database for real documents.

**2. Why It Works (Document-to-Document Similarity):**
User queries are often short (5-10 words) and phrased as questions, whereas target knowledge chunks are long (300 words) and phrased as authoritative explanations.
- Query-to-document vector search suffers from cross-modal asymmetry.
- HyDE converts query search into **document-to-document search**, matching stylistic and lexical structures in latent space.

**3. When It Fails:**
- Open-ended, highly unfamiliar, or cutting-edge proprietary domains where the LLM's hallucination is completely untethered from reality, pulling vector search into completely wrong neighborhoods.""",
        "tip": "Mention HyDE as an effective zero-shot retrieval technique when fine-tuning dense embedders is not possible."
    },
    {
        "id": "rag_84",
        "category": "rag",
        "category_label": "RAG, Embeddings & Vector Search",
        "difficulty": "Senior / Staff",
        "company_tags": ["Stanford", "Databricks", "Cohere"],
        "question": "Explain ColBERT (Late Interaction - Khattab & Zaharia). How does MaxSim achieve token-level interaction speed comparable to dense bi-encoders?",
        "answer": """**1. Limitation of Standard Bi-Encoders:**
Compresses an entire 500-word document into a single fixed-size 768-dim vector (Sentence-BERT). Compressing complex multi-topic documents into one vector causes severe information loss.

**2. ColBERT Late Interaction Architecture:**
- Keeps token-level embeddings for all query tokens ($E_q \\in \\mathbb{R}^{|Q| \\times d}$) and all document tokens ($E_d \\in \\mathbb{R}^{|D| \\times d}$).
- Computes similarity using the **MaxSim operator**:
  $$\\text{Score}(Q, D) = \\sum_{i \\in |Q|} \\max_{j \\in |D|} (E_{q, i} \\cdot E_{d, j}^T)$$
- For every token in the query, find the single most similar token in the document, and sum these maximal alignment scores!

**3. Computational Efficiency:**
- Token embeddings for all documents are precomputed and indexed offline using vector quantization (ColBERTv2 PLAID).
- At query time, MaxSim requires only fast matrix dot products and max operations across token lists, evaluating thousands of candidates in $< 15\\text{ms}$ while preserving token-level alignment precision of a cross-encoder.""",
        "tip": "ColBERT is considered the state-of-the-art retrieval paradigm bridging bi-encoders and cross-encoders."
    },
    {
        "id": "rag_85",
        "category": "rag",
        "category_label": "RAG, Embeddings & Vector Search",
        "difficulty": "Senior / Staff",
        "company_tags": ["Microsoft Research", "Neo4j", "Palantir"],
        "question": "What is GraphRAG (Edge et al., Microsoft, 2024)? When does combining Knowledge Graphs with Vector RAG outperform standard Vector RAG?",
        "answer": """**1. The Failure Mode of Standard Vector RAG:**
Standard vector RAG excels at local entity lookup queries (*'What was Company X's revenue in Q2?'*).
However, it fails catastrophically on **global, holistic, or multi-hop aggregation queries**:
*Example:* *'What are the main corruption themes across all 10,000 court case transcripts?'*
Vector similarity cannot retrieve 1,000 disparate chunks at once without overflowing context limits.

**2. GraphRAG Architecture:**
1. **Extraction:** An LLM parses the entire text corpus to extract Knowledge Graph Entities, Relationships, and Claims.
2. **Hierarchical Community Detection (Leiden Algorithm):** Partitions the knowledge graph into hierarchical clusters of closely related entities.
3. **Community Summarization:** An LLM generates pre-computed summaries for each entity community at multiple levels of granularity.
4. **Global Query Answering:** When a macro question is asked, GraphRAG evaluates summaries across communities, synthesizes partial answers, and aggregates them into a comprehensive global overview.
- Outperforms standard vector RAG by $>70\\%$ on comprehensive synthesis and complex relational reasoning.""",
        "tip": "Position GraphRAG as the solution for 'sensemaking' across entire corpora, whereas vector RAG is for specific needle-in-a-haystack retrieval."
    },
    {
        "id": "rag_86",
        "category": "rag",
        "category_label": "RAG, Embeddings & Vector Search",
        "difficulty": "Mid",
        "company_tags": ["LangChain", "Amazon"],
        "question": "Explain Multi-Query Expansion and RAG-Fusion. How does generating multiple query variants reduce lexical and conceptual retrieval mismatch?",
        "answer": """**1. Problem:**
User search queries are frequently noisy, incomplete, or use phrasing distinct from how knowledge is structured in documents. A single vector search can miss critical chunks due to distance thresholds.

**2. Multi-Query Expansion:**
Given user prompt $q$, an LLM generates 3-5 alternative query phrasings from different perspectives:
- Query 1: Synonym expansion.
- Query 2: Technical/formal rephrasing.
- Query 3: Decomposed sub-question.

**3. RAG-Fusion Pipeline:**
1. Execute parallel vector searches for all 5 generated query variants against the vector database.
2. Collect the top $K$ retrieved document lists from each search.
3. Apply **Reciprocal Rank Fusion (RRF)** to combine and de-duplicate the multiple result sets into a single unified ranking.
- Documents that appear consistently across multiple query variations are strongly promoted to the final prompt.
- Dramatically increases recall on ambiguous or complex multi-intent questions.""",
        "tip": "Explain that RAG-Fusion acts as an ensemble method for information retrieval."
    },
    {
        "id": "rag_87",
        "category": "rag",
        "category_label": "RAG, Embeddings & Vector Search",
        "difficulty": "Senior",
        "company_tags": ["OpenAI", "Meta", "Google"],
        "question": "What is Self-RAG (Asai et al., 2023)? How do reflection tokens allow an LLM to dynamically retrieve, critique, and ground its own responses?",
        "answer": """**1. The Flaw of Naive RAG:**
Naive RAG retrieves chunks indiscriminately for every query (even when retrieval is unnecessary, such as *'What is 2+2?'*) and assumes all retrieved chunks are relevant and factual.

**2. Self-RAG Architecture:**
Trains an LLM to emit special **Reflection Tokens** on-the-fly during generation:
1. `[Retrieve]`: Predicts whether external knowledge is needed (`yes`, `no`, `continue`). If `no`, generates from parametric memory.
2. `[IsRel]` (Is Relevant): Evaluates whether retrieved document chunks actually contain information relevant to the user query. Prunes irrelevant noise chunks.
3. `[IsSup]` (Is Supported): Verifies whether the drafted generation sentence is **fully grounded** in the retrieved context (detects hallucinations step-by-step).
4. `[IsUse]` (Is Useful): Rates the overall usefulness of the response (1 to 5).
- Achieves self-governing, adaptive retrieval with automated self-critique and factuality filtering.""",
        "tip": "Cite Self-RAG as the precursor to modern agentic self-correcting RAG loops."
    },
    {
        "id": "rag_88",
        "category": "rag",
        "category_label": "RAG, Embeddings & Vector Search",
        "difficulty": "Mid / Senior",
        "company_tags": ["Weights & Biases", "Arize AI", "Databricks"],
        "question": "How do you evaluate a production RAG pipeline quantitatively without human labels? Explain the 4 Ragas metrics: Faithfulness, Answer Relevance, Context Precision, and Context Recall.",
        "answer": """**1. Ragas Evaluation Framework (Es et al., 2023):**
Evaluates RAG via LLM-as-a-judge across two axes: **Retrieval Quality** and **Generation Quality**.

**2. Generation Metrics:**
- **Faithfulness (Groundedness):** Measures factual consistency:
  $$\\text{Faithfulness} = \\frac{\\text{Number of claims in answer supported by context}}{\\text{Total claims made in answer}}$$
  - Prevents hallucinations. Evaluates whether the LLM invented facts not present in retrieved context.
- **Answer Relevance:** Evaluates whether the generated response directly addresses the user query (penalizes redundant or evasive answers). Computed by generating hypothetical questions from the answer and measuring semantic similarity to original query.

**3. Retrieval Metrics:**
- **Context Precision:** Measures the signal-to-noise ratio in retrieved chunks. Verifies that ground-truth relevant chunks are ranked at the top of the context list (Mean Average Precision).
- **Context Recall:** Measures whether the retrieved chunks contained all the necessary information required to answer the question.""",
        "tip": "In production: Context Precision/Recall benchmark the retrieval engine; Faithfulness/Relevance benchmark the generation LLM."
    },
    {
        "id": "rag_89",
        "category": "rag",
        "category_label": "RAG, Embeddings & Vector Search",
        "difficulty": "Mid / Senior",
        "company_tags": ["Pinecone", "Elasticsearch", "Amazon"],
        "question": "Compare Metadata Filtering strategies in Vector Databases: Post-Filtering, Pre-Filtering, and Single-Stage Filtered HNSW.",
        "answer": """**1. Post-Filtering:**
1. Execute pure vector ANN search to retrieve top 1000 nearest neighbors.
2. Discard all returned documents that fail metadata filter (e.g. `user_id == '123'` or `year >= 2024`).
- **Fatal Flaw:** If the metadata condition is selective (e.g. only 0.1% of documents match), all 1000 vector neighbors will be filtered out, returning **zero results**!

**2. Pre-Filtering:**
1. Filter the entire dataset by metadata first, creating a temporary subset.
2. Perform brute-force vector search over the filtered subset.
- **Flaw:** Bypasses fast HNSW indexing; slow and memory-intensive if the filtered subset is large.

**3. Single-Stage Filtered HNSW (Iterative Graph Traversal):**
Applies metadata filter **during the HNSW graph traversal**:
- Explores graph edges through both matching and non-matching nodes to preserve connectivity, but only adds nodes that satisfy metadata filters to the candidate nearest-neighbor result set.
- Guaranteed to return $K$ relevant, filtered results in logarithmic time.""",
        "tip": "Explain that modern enterprise vector databases (Pinecone, Qdrant) use single-stage filtered HNSW to prevent empty search results."
    },
    {
        "id": "rag_90",
        "category": "rag",
        "category_label": "RAG, Embeddings & Vector Search",
        "difficulty": "Senior",
        "company_tags": ["Stripe", "Uber", "Palantir"],
        "question": "What is the Hubness Problem in high-dimensional vector spaces, and how does it distort nearest-neighbor retrieval?",
        "answer": """**1. The Hubness Phenomenon (Radovanović et al., 2010):**
In high-dimensional spaces ($d > 500$), data points do not share equal probabilities of being nearest neighbors.
A tiny fraction of data points—called **Hubs**—emerge as nearest neighbors to an absurdly disproportionate number of query points across the dataset, regardless of semantic relevance! Conversely, many points are **Anti-hubs** that are never retrieved by any query.

**2. Mathematical Cause:**
Caused by distance concentration and boundary variance in high dimensions. Points located slightly closer to the global centroid or in dense subspace clusters have smaller distances to randomly distributed points on the hypersphere shell.

**3. Impact on RAG & Search:**
- Popular hub documents keep getting erroneously retrieved for queries they know nothing about, polluting context prompts.
- Can be detected by plotting the $k$-occurrence distribution (number of times point $x$ appears in top-$k$ lists).
- **Remediation:** Cosine centering (subtracting mean embedding vector), Local Scaling, or Mutual Proximity normalization.""",
        "tip": "Hubness is an advanced topic that deeply impresses vector search and embedding researchers."
    },
    {
        "id": "rag_91",
        "category": "rag",
        "category_label": "RAG, Embeddings & Vector Search",
        "difficulty": "Mid / Senior",
        "company_tags": ["Anthropic", "Cohere"],
        "question": "What is Retrieval Poisoning (Context Window Contamination) in RAG, and how do cross-encoder rerankers defend against it?",
        "answer": """**1. The Threat:**
An attacker uploads a document crafted to achieve high cosine similarity with sensitive queries (e.g. contains repeated keywords or semantic triggers).
When a user asks a related question, the malicious document is retrieved and injected into the LLM context prompt, misleading the model into generating false instructions or executing indirect prompt injection.

**2. Why Bi-Encoders are Vulnerable:**
Bi-encoders evaluate queries and documents via separate vector towers. Attackers can optimize adversarial text strings that align with target query embeddings without actually answering the question.

**3. Cross-Encoder Defense:**
Cross-encoders evaluate full bidirectional token cross-attention across Query and Document jointly.
- Detects that although document has overlapping keywords, its grammatical and semantic relationship to the query is adversarial or incoherent.
- Assigns near-zero reranking scores, pushing the poisoned chunk completely out of the top 3-5 prompt context window.""",
        "tip": "Highlight that rerankers act as a robust semantic firewall in production RAG architectures."
    },
    {
        "id": "rag_92",
        "category": "rag",
        "category_label": "RAG, Embeddings & Vector Search",
        "difficulty": "Senior",
        "company_tags": ["LangChain", "Amazon", "Google"],
        "question": "What is Adaptive RAG? How does a query router decide dynamically between No Retrieval, Web Search, and Multi-Hop Vector Retrieval?",
        "answer": """**1. The Problem with One-Size-Fits-All RAG:**
- Simple conversational queries (*'Hello, how are you?'*) waste latency and cost if passed to vector retrieval.
- Factual queries on recent events require live Web Search.
- Complex queries (*'Compare revenue growth of Apple vs Microsoft over 5 years'*) require multi-step query decomposition and multiple retrieval hops.

**2. Adaptive RAG Architecture:**
Employs an upfront **Query Classifier / Router** (fine-tuned small LLM or fast classifier):
1. **Direct Generation (No Retrieval):** For conversational, creative, or common sense queries. Latency: $< 500\\text{ms}$.
2. **Single-Hop Vector RAG:** For specific internal knowledge lookups.
3. **Web Search API (Brave/Tavily/Google):** When query involves real-time sports, news, or post-cutoff world knowledge.
4. **Agentic Multi-Hop RAG (LangGraph / ReAct):** Decomposes complex comparative queries into sequential sub-queries, iteratively querying vector DB, synthesizing partial answers, and refining until complete.""",
        "tip": "Emphasize that Adaptive RAG cuts average latency and vector database costs by 40-60% in production."
    },
    {
        "id": "rag_93",
        "category": "rag",
        "category_label": "RAG, Embeddings & Vector Search",
        "difficulty": "Mid / Senior",
        "company_tags": ["Databricks", "Pinecone"],
        "question": "What is Corrective RAG (CRAG - Yan et al., 2024)? How does it trigger automated fallback when retrieval confidence is low?",
        "answer": """**1. Concept:**
Standard RAG fails whenever retrieval pulls low-quality or irrelevant chunks, forcing the LLM to hallucinate or regurgitate irrelevant context.
CRAG introduces a lightweight **Retrieval Evaluator** that scores the confidence of retrieved documents before prompt generation.

**2. Three Action Branches:**
- **Correct (Confidence $\\ge \\tau_{high}$):** Retrieved context is high quality. Chunks are stripped of irrelevant sentences via knowledge refinement and passed to LLM.
- **Incorrect (Confidence $\\le \\tau_{low}$):** Retrieved context is completely irrelevant. CRAG discards all retrieved chunks and triggers an automated fallback to **Web Search API** to gather fresh evidence.
- **Ambiguous ($\\tau_{low} < \\text{Score} < \\tau_{high}$):** Blends filtered internal chunks with web search results to ensure comprehensive coverage.
- Guarantees that the generator is never poisoned with low-confidence garbage context.""",
        "tip": "Cite CRAG as an essential self-healing pattern for enterprise RAG platforms."
    },
    {
        "id": "rag_94",
        "category": "rag",
        "category_label": "RAG, Embeddings & Vector Search",
        "difficulty": "Mid",
        "company_tags": ["Anthropic", "Cohere"],
        "question": "How does contextual chunking (Contextual Retrieval - Anthropic, 2024) solve the problem of missing context in RAG?",
        "answer": """**1. The Missing Context Dilemma:**
Consider a financial report chunk:
*Chunk:* 'Operating income grew by 18% in the third quarter.'
If a user asks *'What was Tesla's 2024 operating income?'*, the vector embedder has no idea which company or year this chunk belongs to, because the company name was mentioned 5 pages earlier in the document! The chunk is never retrieved.

**2. Anthropic Contextual Retrieval Solution:**
During indexing, prepend a short, 50-token **contextual summary** generated by an LLM to every chunk before embedding it:
*Contextual Chunk:*
`[Document: Tesla 2024 Annual 10-K Report, Section: Automotive Earnings] Operating income grew by 18% in the third quarter.`
- When embedded, the chunk vector contains both the specific financial metrics AND the global document metadata (Tesla, 2024, Automotive).
- Anthropic demonstrated that combining contextual embeddings with contextual BM25 reduces retrieval failure rate by **$49\\%$**!""",
        "tip": "Cite Anthropic's September 2024 Contextual Retrieval research paper."
    },
    {
        "id": "rag_95",
        "category": "rag",
        "category_label": "RAG, Embeddings & Vector Search",
        "difficulty": "Senior / Staff",
        "company_tags": ["OpenAI", "Meta", "Google"],
        "question": "Explain the trade-offs of embedding dimensions: Why did OpenAI introduce Matryoshka Representation Learning (MRL) in text-embedding-3?",
        "answer": """**1. The Storage & Compute Dilemma:**
High-dimensional embeddings ($d=3072$) provide rich semantic representation, but storing 100M 3072-dim vectors consumes **$1.2\\text{ TB}$ of costly GPU/RAM** with slower vector search.

**2. Matryoshka Representation Learning (MRL - Kusupati et al., 2022):**
Inspired by Russian nesting dolls:
- Trains the model such that the **first $k$ dimensions** ($k \\in \\{64, 128, 256, 512, 1536, 3072\\}$) form a fully functional, high-quality embedding vector on their own!
- The loss function is a multi-task sum of InfoNCE losses evaluated simultaneously across multiple truncated prefix dimensions:
  $$\\mathcal{L}_{MRL} = \\sum_{m \\in \\mathcal{M}} \\mathcal{L}_{InfoNCE}(v_{1:m})$$

**3. Production Benefit:**
- Allows engineers to truncate 3072-dim embeddings down to 512 dimensions at zero retraining cost, achieving a **$6\\times$ reduction in storage and search latency** while retaining $>98\\%$ of full retrieval accuracy.
- Enables two-stage search: fast 128-dim rough filter followed by 3072-dim full precision rerank on top 100 candidates.""",
        "tip": "MRL is the exact technology behind OpenAI's `dimensions` parameter in `text-embedding-3-small` and `text-embedding-3-large`."
    }
]
