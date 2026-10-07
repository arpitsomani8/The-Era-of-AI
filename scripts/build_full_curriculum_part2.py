import json

def create_concept_obj(
    cid, title, tid, tlabel, cat, cat_label, definition, formula, logic, example,
    core_terms, symbol_guide, numerical_example, pitfalls, tags, takeaways
):
    return {
        "id": cid,
        "title": title,
        "topic_id": tid,
        "topic_label": tlabel,
        "category": cat,
        "category_label": cat_label,
        "raw_subtopic": title,
        "def": definition,
        "formula": formula,
        "logic": logic,
        "example": example,
        "tags": tags,
        "raw_sub": title,
        "definition": definition,
        "formula_explanation": f"Mathematical formulation and loss objective for {title}.",
        "simple_summary": definition.split('.')[0] + '.',
        "core_terms": core_terms,
        "symbol_guide": symbol_guide,
        "numerical_example": numerical_example,
        "pitfalls": pitfalls,
        "core_logic": logic,
        "architectural_logic": f"{title} integrates into production machine learning pipelines by establishing mathematically sound boundaries and optimal computational resource utilization.",
        "key_takeaways": takeaways,
        "definition_bullets": [
            f"**Core Purpose:** {definition}",
            f"**Operational Role:** {logic}",
            f"**Production Significance:** {example}"
        ]
    }

with open('src/data/concepts.json', 'r', encoding='utf-8') as f:
    concepts = json.load(f)

new_concepts = []

# ==============================================================
# 4. TOPIC: genai_vector_db_pinecone (Category: genai)
# ==============================================================
t_vdb_id = "genai_vector_db_pinecone"
t_vdb_label = "Vector Databases, Pinecone & Enterprise Hybrid Retrieval"

new_concepts.append(create_concept_obj(
    "concept_hnsw_ivfpq_indexing",
    "Vector Database Internals: HNSW, IVF-PQ & High-Dimensional Indexing",
    t_vdb_id, t_vdb_label, "genai", "Transformers & Generative AI",
    "High-dimensional approximate nearest neighbor (ANN) search algorithms that trade exact distance precision for logarithmic query time, primarily Hierarchical Navigable Small World (HNSW) graphs and Inverted File with Product Quantization (IVF-PQ).",
    r"\text{Complexity}_{\text{HNSW}} = \mathcal{O}(\log N), \quad d(q, x) \approx \sum_{m=1}^M d(q^{(m)}, c_{k_m}^{(m)})",
    "Navigable Small World multi-layer skip-list graphs provide sub-5ms similarity retrieval across millions of 1536-dimensional vectors by traversing coarse long-distance links at upper layers before zooming into dense lower layers.",
    "Powering real-time semantic document retrieval across 50 million patents where exact linear scanning would take seconds per query.",
    [
        {"term": "HNSW (Hierarchical Navigable Small World)", "what_is_it": "A multi-layered graph data structure where upper layers contain sparse long-range connections and lower layers contain dense local neighbor clusters.", "analogy": "Navigating a country by taking international airports first, regional highways second, and local city streets last.", "why_it_matters": "The fastest, most accurate vector search index in modern production databases (Pinecone, Qdrant, Milvus)."},
        {"term": "Product Quantization (PQ)", "what_is_it": "Decomposing high-dimensional vectors into smaller sub-vectors and quantizing each sub-vector into centroid cluster IDs.", "analogy": "Summarizing a 1,000-page book into 8 key bullet codes to store on a tiny index card.", "why_it_matters": "Compresses vector memory footprints by 95%, allowing billion-scale vector indexes to fit in RAM."}
    ],
    [
        {"symbol": "M", "meaning": "Maximum number of bidirectional links per node in HNSW", "plain_english": "Controls graph density and memory usage (typically 16–64)."},
        {"symbol": "\\text{efSearch}", "meaning": "Size of dynamic candidate list during query search", "plain_english": "Higher values increase recall accuracy at the cost of slight query latency."}
    ],
    "Querying 10,000,000 vectors of dimension 1536:\nExact Flat L2 search = 15.36 billion float operations (Latency: 850 ms).\nHNSW index (M=32, ef=64) = ~12,000 float operations (Latency: 3.2 ms, 98.5% recall).",
    "Building HNSW graphs with tiny M and efSearch parameters to save RAM; this causes the search to get trapped in local graph minima, tanking recall below 70%.",
    ["HNSW", "IVF-PQ", "Vector Indexing", "ANN Search", "High-Dimensional Geometry"],
    [
        "HNSW delivers state-of-the-art recall vs speed tradeoff but consumes significant memory.",
        "Product Quantization (IVF-PQ) is optimal when memory budgets are tight and vector counts exceed 100M+.",
        "Always benchmark Recall@10 against an exact flat index before choosing production HNSW hyperparameters."
    ]
))

new_concepts.append(create_concept_obj(
    "concept_pinecone_architecture_namespaces",
    "Pinecone Architecture: Namespaces, Metadata Filtering & Pods/Serverless",
    t_vdb_id, t_vdb_label, "genai", "Transformers & Generative AI",
    "Cloud-native managed vector database architecture utilizing isolated partition namespaces, single-stage metadata filtering, and decoupled serverless storage-compute separation.",
    r"\text{FilterQuery} = \{v \in \text{Namespace}(T) \mid \text{CosineSim}(q, v) \ge \tau \land \text{metadata.tenant\_id} = t\}",
    "Namespaces provide strict data partitioning within a single index, eliminating multi-tenant cross-talk and metadata filter overhead while guaranteeing sub-50ms P99 SLA.",
    "A multi-tenant SaaS application storing legal contracts for 800 enterprise clients, where each client's documents reside in an isolated Pinecone namespace.",
    [
        {"term": "Pinecone Namespace", "what_is_it": "A logical partition inside a Pinecone vector index that confines queries strictly to a designated subset of vectors.", "analogy": "Separate locked safe-deposit drawers inside a single bank vault.", "why_it_matters": "Enables multi-tenancy with zero risk of cross-tenant vector leakage and zero performance degradation."},
        {"term": "Single-Stage Metadata Filtering", "what_is_it": "Evaluating metadata boolean constraints concurrently during graph traversal rather than pre-filtering or post-filtering.", "analogy": "A security scanner that checks your ticket and your luggage simultaneously at the gate.", "why_it_matters": "Prevents catastrophic recall loss caused by naive post-filtering."}
    ],
    [
        {"symbol": "\\text{Namespace}", "meaning": "Logical tenant identifier string", "plain_english": "Directs index routing to tenant-isolated data blocks."},
        {"symbol": "\\text{Serverless}", "meaning": "Decoupled compute-storage vector architecture", "plain_english": "Automatically scales up during high-traffic spikes and scales to zero when idle."}
    ],
    "Post-filtering vs Single-stage filtering: With 1M vectors where 1% belong to tenant A. Post-filtering top 100 ANN returns only 1 tenant document. Single-stage filtering evaluates metadata during graph traversal, returning 100% relevant tenant documents.",
    "Attempting to create a separate Pinecone index for every tenant instead of using namespaces; indexes have minimum billing costs and slow provisioning, while namespaces are free and instantaneous.",
    ["Pinecone", "Vector Database", "Namespaces", "Metadata Filtering", "Multi-Tenancy"],
    [
        "Namespaces are the recommended best practice for multi-tenant SaaS architectures in vector databases.",
        "Pinecone Serverless separates blob storage from stateless vector search pods, cutting costs by up to 70%.",
        "Always pass metadata filters alongside vector embeddings to restrict search to relevant document categories."
    ]
))

new_concepts.append(create_concept_obj(
    "concept_hybrid_search_rrf",
    "Hybrid Search Fusion: Reciprocal Rank Fusion (RRF) & BM25 + Dense",
    t_vdb_id, t_vdb_label, "genai", "Transformers & Generative AI",
    "Hybrid retrieval architectures combining sparse lexical inverted indexes (BM25 for exact keyword/part-number matching) and dense semantic vector embeddings via Reciprocal Rank Fusion (RRF).",
    r"\text{RRF}(d) = \sum_{m \in \{\text{dense}, \text{sparse}\}} \frac{1}{k + r_m(d)}, \quad k \approx 60",
    "Dense embeddings capture abstract semantic conceptual similarity but struggle with rare domain codes (e.g. 'ERR_404_AUTH'); sparse BM25 guarantees exact keyword hits, and RRF seamlessly merges their rankings without score normalization issues.",
    "Enterprise IT support search where users query both vague symptoms ('my screen looks blurry') and exact error codes ('DRIVER_IRQL_NOT_LESS_OR_EQUAL').",
    [
        {"term": "Reciprocal Rank Fusion (RRF)", "what_is_it": "A rank aggregation algorithm that sums the reciprocals of document ranks across multiple independent retrieval methods.", "analogy": "Combining movie rankings from two critics by rewarding films that appear near the top of both lists, regardless of the critics' scoring scales.", "why_it_matters": "Solves the score calibration problem between unbounded BM25 scores and cosine similarities."},
        {"term": "Sparse Lexical Search (BM25)", "what_is_it": "An information retrieval ranking function based on Term Frequency (TF) and Inverse Document Frequency (IDF).", "analogy": "A traditional library index card catalogue matching exact book title words.", "why_it_matters": "Unbeatable for exact model numbers, acronyms, and rare entity lookups."}
    ],
    [
        {"symbol": "r_m(d)", "meaning": "Rank of document d in retrieval system m", "plain_english": "Ordinal position (1st, 2nd, 3rd) in the specific search result list."},
        {"symbol": "k", "meaning": "Smoothing constant (typically 60)", "plain_english": "Prevents top-ranked items from dominating the reciprocal score excessively."}
    ],
    "Document A is Rank 1 in Dense search (r_dense=1) and Rank 5 in BM25 (r_sparse=5). Constant k=60.\nRRF score = 1/(60+1) + 1/(60+5) = 1/61 + 1/65 = 0.01639 + 0.01538 = 0.03177 (Dominates Document B with rank 20 and 30).",
    "Simply adding raw BM25 scores (which range from 0 to 45) to Cosine similarity scores (which range from -1 to +1); this causes BM25 to completely drown out the vector search. Use RRF instead.",
    ["Hybrid Search", "RRF", "BM25", "Dense Retrieval", "Rank Fusion"],
    [
        "Hybrid search consistently outperforms dense-only search across all enterprise benchmarks (BEIR).",
        "RRF requires zero training and zero hyperparameter tuning, making it robust against distribution shift.",
        "Pinecone, Weaviate, and ElasticSearch offer native hybrid sparse-dense vector indexing."
    ]
))

new_concepts.append(create_concept_obj(
    "concept_rag_retrieval_evaluation",
    "Retrieval Evaluation Metrics: Hit Rate, MRR & Context Relevance",
    t_vdb_id, t_vdb_label, "genai", "Transformers & Generative AI",
    "Quantitative evaluation methodologies for assessing the retrieval stage of RAG systems independent of generator hallucinations, utilizing Mean Reciprocal Rank (MRR), Hit Rate@K, and Ragas Context Relevance.",
    r"\text{HitRate@K} = \frac{1}{|Q|}\sum_{q=1}^{|Q|} \mathbb{I}(\text{rank}_q \le K), \quad \text{MRR} = \frac{1}{|Q|}\sum_{q=1}^{|Q|} \frac{1}{\text{rank}_q}",
    "If the retriever fails to retrieve the correct source chunk within the top K, the generator model has zero probability of providing a factually grounded answer.",
    "Evaluating an internal HR policy chatbot across 500 test questions to verify that the correct employee benefits clause is present in the top-3 retrieved chunks.",
    [
        {"term": "Hit Rate @ K", "what_is_it": "The percentage of test queries for which the correct ground-truth chunk appears somewhere within the top K retrieved results.", "analogy": "Checking whether your lost keys are anywhere inside the top 3 drawers you opened.", "why_it_matters": "Measures basic retrieval coverage before feeding context to the LLM."},
        {"term": "Mean Reciprocal Rank (MRR)", "what_is_it": "The average of the reciprocal ranks of the first relevant document across all queries.", "analogy": "Rewarding a search engine heavily when the right answer is in the 1st position rather than the 5th position.", "why_it_matters": "Directly measures how well the retriever prioritizes the most crucial context at the top of the prompt."}
    ],
    [
        {"symbol": "\\text{rank}_q", "meaning": "Rank position of the first ground-truth document for query q", "plain_english": "1 if at top; 2 if second; infinity if not retrieved."},
        {"symbol": "K", "meaning": "Retrieved context chunk window cutoff", "plain_english": "Usually 3, 5, or 10 chunks passed to the LLM context."}
    ],
    "Across 3 test queries: Query 1 finds target at rank 1 (1/1 = 1.0); Query 2 finds target at rank 2 (1/2 = 0.5); Query 3 finds target at rank 4 (1/4 = 0.25).\nMRR = (1.0 + 0.5 + 0.25) / 3 = 1.75 / 3 = 0.5833.\nHitRate@3 = 2 / 3 = 66.7% (Query 3 missed the top 3 cutoff).",
    "Evaluating entire RAG pipelines with end-to-end BLEU or ROUGE scores; this conflates generator phrasing with retrieval quality. Always evaluate retrieval metrics separately.",
    ["RAG Evaluation", "MRR", "Hit Rate", "Ragas", "Context Relevance"],
    [
        "Never optimize the generator prompt until your retrieval HitRate@5 exceeds 90%.",
        "Ragas framework evaluates the RAG Triad: Context Relevance, Groundedness, and Answer Relevance.",
        "Higher MRR places key facts at the beginning of the context window, combating 'Lost in the Middle' attention degradation."
    ]
))

new_concepts.append(create_concept_obj(
    "concept_rag_failure_modes_lost_middle",
    "RAG Failure Modes: Context Overflow, Retrieval Misses & Lost in the Middle",
    t_vdb_id, t_vdb_label, "genai", "Transformers & Generative AI",
    "Systematic analysis of the five primary architectural failure modes in enterprise RAG pipelines: retrieval misses, context window overflow, 'Lost in the Middle' attention degradation, noisy chunk distraction, and generator sycophancy.",
    r"P(\text{Recall} \mid \text{Position}) \approx \begin{cases} \text{High} & \text{at beginning of prompt} \\ \text{Low} & \text{in middle of prompt} \\ \text{High} & \text{at end of prompt (recency)} \end{cases}",
    "Transformer attention mechanisms inherently suffer from U-shaped attention curves, excelling at recalling tokens near the beginning and end of long prompts while consistently overlooking crucial facts buried in the middle.",
    "A financial compliance bot failing to flag an illegal transaction because the governing clause was placed in chunk 12 of a 20-chunk injected context.",
    [
        {"term": "Lost in the Middle Phenomenon", "what_is_it": "The empirical observation that LLMs retrieve and utilize facts placed in the middle of long contexts significantly worse than facts at the start or end.", "analogy": "Reading a 500-page book and vividly remembering the prologue and epilogue while forgetting chapter 15.", "why_it_matters": "Requires re-ranking algorithms to deliberately place the highest-confidence chunk at the very beginning of the prompt."},
        {"term": "Chunk Fragmentation", "what_is_it": "Splitting text at arbitrary character boundaries that cut sentences or critical tables in half, destroying semantic coherence.", "analogy": "Tearing a photograph down the center of someone's face.", "why_it_matters": "Causes embedding models to encode incomplete fragments that fail retrieval similarity."}
    ],
    [
        {"symbol": "\\text{U-Curve}", "meaning": "Attention weight distribution across sequence tokens", "plain_english": "Token attention dips significantly in the middle 60% of the context."},
        {"symbol": "\\text{ChunkOverlap}", "meaning": "Sliding window overlap between consecutive chunks", "plain_english": "Typically 10–20% of chunk size to preserve cross-boundary semantics."}
    ],
    "Stanford study benchmark: LLM query accuracy on 20 retrieved documents drops from 85% (when key fact is at document 1) down to 52% (when key fact is placed at document 10). Re-ordering chunks restores accuracy to 84%.",
    "Stuffing 30 retrieved chunks into context just because the model supports 128k tokens; injecting noisy, low-relevance chunks dilutes attention and increases hallucination probability by 3x.",
    ["RAG Failures", "Lost in the Middle", "Chunk Fragmentation", "Attention Degradation", "Reranking"],
    [
        "Apply a Cross-Encoder Reranker (e.g. Cohere Rerank, BGE-Reranker) to select the top 3–5 most relevant chunks.",
        "Sort retrieved chunks so the highest-scoring chunk is placed first and second highest is placed last (sandwich strategy).",
        "Use semantic chunking (splitting at markdown headers or sentence boundaries) rather than fixed character chunking."
    ]
))

# Save concepts so far
with open('src/data/concepts.json', 'w', encoding='utf-8') as f:
    json.dump(concepts + new_concepts, f, indent=2, ensure_ascii=False)

print(f"Total concepts written so far: {len(concepts) + len(new_concepts)}")
