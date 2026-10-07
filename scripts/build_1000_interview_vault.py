# scripts/build_1000_interview_vault.py
import json
import random
import os

random.seed(42)

def get_interview_category(concept):
    cat = concept.get('category', 'ml')
    tid = concept.get('topic_id', '')

    if cat == 'math':
        return 'logic_prob', 'Logic & Quant'
    elif cat in ('data', 'eval'):
        return 'metrics_data', 'Metrics & Data'
    elif cat == 'ml':
        return 'ml', 'Classical ML'
    elif cat == 'dl':
        return 'dl', 'Deep Learning'
    elif cat == 'genai':
        if any(k in tid for k in ['rag', 'vector_db', 'embed', 'retriev']):
            return 'rag', 'RAG & Vector DB'
        return 'genai_llm', 'GenAI & LLMs'
    elif cat == 'mlops':
        return 'system_mlops', 'System & MLOps'
    elif cat == 'swe_cloud':
        return 'swe_cloud', 'SWE & Cloud Infra'
    return 'ml', 'Classical ML'

COMPANY_POOLS = {
    'junior': [
        ["Google", "Amazon", "Microsoft", "TCS", "Infosys"],
        ["Meta", "Apple", "Adobe", "Accenture", "Cognizant"],
        ["Bloomberg", "Cisco", "IBM", "Oracle", "Wipro"],
        ["Uber", "LinkedIn", "Salesforce", "Capgemini", "Deloitte"],
        ["Amazon", "Walmart Global Tech", "PayPal", "Intuit", "EY"],
        ["Spotify", "Stripe", "Goldman Sachs", "JPMorgan", "Morgan Stanley"]
    ],
    'mid': [
        ["Google", "Meta", "Amazon", "Apple", "Netflix"],
        ["OpenAI", "Microsoft", "NVIDIA", "Databricks", "Stripe"],
        ["Uber", "DoorDash", "Airbnb", "Snowflake", "Pinterest"],
        ["Palantir", "Scale AI", "Anthropic", "Cohere", "ByteDance"],
        ["LinkedIn", "Roblox", "Instacart", "Coinbase", "Spotify"],
        ["Atlassian", "Figma", "Canva", "Shopify", "Twilio"]
    ],
    'senior': [
        ["Google DeepMind", "OpenAI", "Anthropic", "Meta FAIR", "NVIDIA"],
        ["Apple AI/ML", "Microsoft Research", "Amazon AWS AI", "Databricks", "Stripe"],
        ["Netflix Algorithms", "Uber Michelangelo", "ByteDance AI Lab", "Palantir Foundry", "Snowflake"],
        ["Waymo", "Tesla Autopilot", "Scale AI", "Cruise", "Mistral AI"],
        ["Two Sigma", "Jane Street", "Citadel Securities", "DE Shaw", "Jump Trading"],
        ["Hudson River Trading", "Optiver", "Point72", "Millennium", "Renaissance Technologies"]
    ]
}

SPECIALIZED_SCENARIOS = [
    {
        "category": "genai_llm",
        "category_label": "GenAI & LLMs",
        "experience_level": "5+",
        "difficulty": "Senior / Staff",
        "companies": ["OpenAI", "Anthropic", "Google DeepMind"],
        "question": "How does Multi-Head Latent Attention (MLA) in DeepSeek-V2/V3 reduce KV cache memory footprint compared to Multi-Query (MQA) and Grouped-Query Attention (GQA)?",
        "answer": "**Core Architectural Innovation:**\nMLA compresses Key and Value projections into low-rank latent spaces ($d_c \\ll d_h \\cdot n_h$) prior to caching.\n\n**1. Low-Rank Key-Value Compression:**\n- Traditional MHA stores $2 \\times L \\times n_h \\times d_h \\times B \\times T$ KV states in GPU High Bandwidth Memory (HBM).\n- MLA projects the hidden state $h_t$ into compressed latent vector $c_t^{KV} = W^{DKV} h_t$.\n- During decoding, only $c_t^{KV}$ and a decoupled rotary positional embedding vector $k_t^{R}$ are stored in the KV cache.\n- Upon query computation, projection weights are absorbed via matrix associative property: $q_t^T (W^{UK} c_t^{KV}) = (q_t^T W^{UK}) c_t^{KV}$, eliminating decompression overhead in memory.\n\n**2. Quantitative Impact on Memory:**\n- Cache compression ratio reaches $5\\times$ to $7\\times$ relative to standard MHA, allowing up to $4\\times$ larger batch sizes with equivalent HBM utilization.\n\n**3. Production Trade-offs:**\n- **Pros:** Massive inference throughput boost, drastically reduced memory bandwidth bottlenecks during auto-regressive generation.\n- **Cons:** Additional linear projection computations during prefill phase; requires custom CUDA kernel fusing.",
        "tip": "Draw the matrix absorption trick on the whiteboard to demonstrate you understand hardware memory bandwidth vs compute bound operations."
    },
    {
        "category": "genai_llm",
        "category_label": "GenAI & LLMs",
        "experience_level": "5+",
        "difficulty": "Senior / Staff",
        "companies": ["Meta", "OpenAI", "NVIDIA"],
        "question": "Derive the mathematical mechanics of Direct Preference Optimization (DPO) and explain how it bypasses PPO's reward model training.",
        "answer": "**Mathematical Foundation:**\nPPO optimizes policy $\\pi_\\theta$ against reward model $r_\\phi(x, y)$ with KL penalty:\n$$\\max_{\\pi} \\mathbb{E}_{x, y \\sim \\pi} [r_\\phi(x, y)] - \\beta D_{KL}(\\pi(y|x) \\parallel \\pi_{\\text{ref}}(y|x))$$\n\n**The Closed-Form Analytic Inversion:**\nThe optimal policy satisfies:\n$$\\pi^*(y|x) = \\frac{1}{Z(x)} \\pi_{\\text{ref}}(y|x) \\exp\\left(\\frac{1}{\\beta} r(x, y)\\right)$$\nRearranging for ground-truth implicit reward:\n$$r(x, y) = \\beta \\log \\frac{\\pi^*(y|x)}{\\pi_{\\text{ref}}(y|x)} + \\beta \\log Z(x)$$\n\n**Substitution into Bradley-Terry Preference Objective:**\nUnder Bradley-Terry, $P(y_w \\succ y_l | x) = \\sigma(r(x, y_w) - r(x, y_l))$. Substituting the implicit reward cancels the partition function $Z(x)$:\n$$\\mathcal{L}_{\\text{DPO}}(\\theta) = -\\mathbb{E}_{(x, y_w, y_l)} \\left[ \\log \\sigma \\left( \\beta \\log \\frac{\\pi_\\theta(y_w|x)}{\\pi_{\\text{ref}}(y_w|x)} - \\beta \\log \\frac{\\pi_\\theta(y_l|x)}{\\pi_{\\text{ref}}(y_l|x)} \\right) \\right]$$\n\n**Engineering Implications:**\n- **Stability:** Eliminates 4-model actor-critic-reference-reward memory overhead; reduces training to a simple binary cross-entropy classification on model logits.",
        "tip": "Highlight that DPO is prone to distribution drift if chosen and rejected completions are too similar or if $\\beta$ is set too small, causing policy collapse."
    },
    {
        "category": "system_mlops",
        "category_label": "System & MLOps",
        "experience_level": "5+",
        "difficulty": "Senior / Staff",
        "companies": ["NVIDIA", "Google DeepMind", "Amazon AWS AI"],
        "question": "How does FlashAttention (v1, v2, v3) optimize GPU SRAM vs HBM memory hierarchy to achieve sub-quadratic I/O complexity?",
        "answer": "**GPU Architecture Bottleneck:**\nModern GPUs (A100, H100) are compute-rich (hundreds of TFLOPS) but memory-bandwidth limited (1.5-3.3 TB/s HBM vs ~19 TB/s SRAM).\nStandard attention materializes $S = QK^T / \\sqrt{d} \\in \\mathbb{R}^{N \\times N}$ in HBM, requiring $O(N^2)$ memory reads/writes.\n\n**FlashAttention Innovations:**\n**1. Tiling:**\n- Loads blocks of $Q, K, V$ into high-speed on-chip SRAM ($192$ KB per Streaming Multiprocessor).\n- Computes partial attention locally without writing intermediate $N \\times N$ attention matrix to DRAM/HBM.\n\n**2. Online Softmax Computation:**\n- Tracks running normalization statistics $m(x) = \\max(m_{\\text{prev}}, m_{\\text{block}})$ and scale factors $l(x) = \\sum e^{x_i - m(x)}$.\n- Combines block outputs via dynamic rescaling: $O_{\\text{new}} = \\frac{l_1 e^{m_1 - m} O_1 + l_2 e^{m_2 - m} O_2}{l_1 e^{m_1 - m} + l_2 e^{m_2 - m}}$.\n\n**3. Recomputation in Backward Pass:**\n- Instead of storing intermediate activations, FlashAttention recomputes them on-the-fly in SRAM during backprop, reducing backward memory from $O(N^2)$ to $O(N)$.\n\n**FlashAttention-2 vs FA-3 Enhancements:**\n- FA-2 optimizes work partitioning across thread blocks and warps, reducing non-matmul FLOPs.\n- FA-3 leverages Hopper H100 asynchronous Tensor Memory Accelerator (TMA) and FP8 gemm pipelining.",
        "tip": "Distinguish compute complexity ($O(N^2 d)$ FLOPs, which does not change) from IO complexity ($O(N^2)$ reduced to $O(N d / M)$ HBM transfers), which provides the speedup."
    },
    {
        "category": "rag",
        "category_label": "RAG & Vector DB",
        "experience_level": "5+",
        "difficulty": "Senior / Staff",
        "companies": ["Databricks", "Pinecone", "Elastic"],
        "question": "Compare Hierarchical Navigable Small World (HNSW) and Inverted File Product Quantization (IVF-PQ) for 100M+ vector search. When would you use each?",
        "answer": "**Comparative Architecture Breakdown:**\n\n**1. HNSW (Graph-Based):**\n- Multi-layer proximity graph where top layers have long-range skip links and bottom layer contains all vectors with short-range Delaunay-like connections.\n- **Search Latency:** Microsecond scale ($< 2$ ms p99 for 10M vectors).\n- **Recall@K:** Extremely high ($95-99%+$).\n- **Memory Footprint:** Very High ($1.5-2.5\\times$ vector size due to adjacency lists in RAM). 100M 1536-dim FP32 vectors require ~600 GB to 1 TB RAM.\n\n**2. IVF-PQ (Quantization + Inverted Index):**\n- Partitions vector space into Voronoi cells via $k$-means centroids (`nlist`).\n- Vectors within cells are decomposed into sub-vectors and quantized to centroids (`codebook`), compressing vectors from 1536 floats to 64 bytes.\n- **Search Latency:** 5-15 ms.\n- **Recall@K:** Lower ($80-92%$), requires re-ranking step.\n- **Memory Footprint:** 90-95% reduction (~16-32 GB RAM for 100M vectors).\n\n**Production Recommendation:**\n- Use **HNSW** when memory is secondary to strict $<5$ ms latency SLAs and maximum recall (e.g. conversational search, legal e-discovery).\n- Use **IVF-PQ with FP16 Re-ranking** when indexing $100M+$ vectors on cost-constrained instances or hybrid disk/RAM architectures.",
        "tip": "Always mention 'Two-stage retrieval': IVF-PQ to fetch top-200 candidates followed by exact cosine re-ranking of the uncompressed vectors."
    },
    {
        "category": "system_mlops",
        "category_label": "System & MLOps",
        "experience_level": "2-4",
        "difficulty": "Mid / Senior",
        "companies": ["Stripe", "Uber", "DoorDash"],
        "question": "How do you detect and mitigate Data Drift and Concept Drift in a real-time production fraud detection pipeline?",
        "answer": "**Definitions & Differences:**\n- **Data Drift (Covariate Shift):** Distribution of input features $P(X)$ changes while ground-truth relationship $P(Y|X)$ remains constant (e.g. users shopping later at night during holidays).\n- **Concept Drift:** Relationship between inputs and targets $P(Y|X)$ changes (e.g. fraudsters changing tactics to mimic normal transactions).\n\n**Monitoring & Detection Architecture:**\n1. **Continuous Statistical Tests:**\n   - **Kolmogorov-Smirnov (KS) Test:** Non-parametric test for continuous univariate features comparing reference window against rolling 24h window.\n   - **Population Stability Index (PSI):** Quantifies distribution divergence across buckets (PSI $<0.1$: stable, $0.1-0.2$: moderate shift, $>0.2$: severe drift).\n   - **Maximum Mean Discrepancy (MMD) / Adversarial Validation:** Train a discriminator model to predict whether a sample is from the training set or production set; ROC-AUC $>0.65$ signals drift.\n\n2. **Mitigation Playbook:**\n   - Trigger automated retrain pipelines on sliding temporal windows.\n   - Use dynamic threshold calibration (adjust decision boundary percentile to maintain false positive rate SLA).\n   - Fall back to rules-based risk engine if model uncertainty variance spikes.",
        "tip": "Emphasize ground truth label delay: In fraud, labels take 30-90 days (chargebacks). Thus, monitoring $P(X)$ drift is your only early warning signal before $P(Y|X)$ is observable."
    },
    {
        "category": "dl",
        "category_label": "Deep Learning",
        "experience_level": "5+",
        "difficulty": "Senior / Staff",
        "companies": ["OpenAI", "Meta FAIR", "Google DeepMind"],
        "question": "What is Speculative Decoding in LLMs, and how does it achieve $2-3\\times$ speedup without degrading model quality?",
        "answer": "**The Autoregressive Latency Dilemma:**\nLLM token generation is memory-bandwidth bound: generating 1 token requires loading all 70B parameters ($140$ GB) from GPU HBM into compute cores for just 1 matrix-vector multiplication.\n\n**Speculative Decoding Protocol:**\n1. **Draft Generation:** A small, fast draft model (e.g. LLaMA-3-8B) autoregressively drafts $K$ candidate tokens ($x_1, \\dots, x_K$) cheaply.\n2. **Target Verification:** The large target model (e.g. LLaMA-3-70B) runs a single forward pass over all $K$ tokens in parallel (matrix-matrix multiplication, compute-bound rather than memory-bandwidth bound).\n3. **Rejection Sampling / Acceptance Criterion:**\n   For each token $i$, accept with probability:\n   $$P(\\text{accept}) = \\min\\left(1, \\frac{P_{\\text{target}}(x_i | x_{<i})}{P_{\\text{draft}}(x_i | x_{<i})}\\right)$$\n   If rejected, resample from corrected distribution $\\max(0, P_{\\text{target}} - P_{\\text{draft}})$ and discard remaining draft tokens.\n\n**Guarantees & Metrics:**\n- **Exact Equivalence:** Mathematically provable that output distribution is identical to target model standalone.\n- **Acceptance Rate $\\alpha$:** Typically $60-80%$ on code and structured text, yielding $2.0\\times$ to $2.8\\times$ end-to-end wall-clock speedup.",
        "tip": "Explain that speculative decoding converts memory-bound latency into parallel compute-bound throughput without altering the model weights or perplexity."
    }
]

def generate_questions():
    # 1. Load concepts
    concepts_path = os.path.join("src", "data", "concepts.json")
    with open(concepts_path, "r", encoding="utf-8") as f:
        concepts = json.load(f)
    print(f"Loaded {len(concepts)} concepts from concepts.json")

    # 2. Load existing 190 questions
    iv_path = os.path.join("src", "data", "interviewQuestions.json")
    with open(iv_path, "r", encoding="utf-8") as f:
        existing_questions = json.load(f)
    print(f"Loaded {len(existing_questions)} existing questions.")

    # Normalize existing question categories
    for q in existing_questions:
        if q.get('category') == 'mlops':
            q['category'] = 'system_mlops'
            q['category_label'] = 'System & MLOps'

    combined_questions = []

    # Keep all existing questions
    for q in existing_questions:
        combined_questions.append(q)

    # 3. Generate 3 questions per concept
    count_generated = 0
    for idx, c in enumerate(concepts):
        title = c.get('title', 'Concept')
        defn = c.get('def', c.get('definition', ''))
        formula = c.get('formula', '')
        logic = c.get('logic', c.get('core_logic', ''))
        example = c.get('example', '')
        pitfalls = c.get('pitfalls', '')
        core_terms = c.get('core_terms', [])
        simple_summary = c.get('simple_summary', '')
        num_ex = c.get('numerical_example', '')
        cat_id, cat_label = get_interview_category(c)

        terms_summary = ""
        if core_terms and isinstance(core_terms, list):
            bullet_items = []
            for t in core_terms[:4]:
                if isinstance(t, dict):
                    tname = t.get('term', '')
                    twhat = t.get('what_is_it', t.get('desc', ''))
                    bullet_items.append(f"- **{tname}:** {twhat}")
            if bullet_items:
                terms_summary = "\n" + "\n".join(bullet_items) + "\n"

        base_id_num = len(combined_questions) + 1

        # Question 1: Junior / Fresher (0-2 Yrs)
        q1 = {
            "id": f"q_{base_id_num:04d}",
            "category": cat_id,
            "category_label": cat_label,
            "experience_level": "0-2",
            "experience_label": "0–2 Yrs (Junior / Fresher)",
            "difficulty": "Junior / Fresher",
            "company_tags": random.choice(COMPANY_POOLS['junior']),
            "question": f"What is {title}, and how does it function intuitively?",
            "answer": (
                f"**Executive Intuition:**\n"
                f"{simple_summary or defn}\n\n"
                f"**Core Mechanics:**\n"
                f"{defn}\n"
                f"{terms_summary}\n"
                f"**Practical Example:**\n"
                f"{example or 'Used extensively across ML workflows to guarantee stability and prevent predictive degeneration.'}\n\n"
                f"**Common Beginner Misconception:**\n"
                f"{pitfalls or 'Assuming theoretical optimality holds without verifying underlying data distribution assumptions.'}"
            ),
            "tip": f"When asked about {title}, begin with a clean high-level analogy before jumping into implementation or terminology."
        }
        combined_questions.append(q1)

        # Question 2: Mid-Level (2-4 Yrs)
        formula_sec = f"**Mathematical Formulation:**\n{formula}\n\n" if formula else ""
        num_sec = f"**Numerical Walkthrough:**\n{num_ex}\n\n" if num_ex else ""
        q2 = {
            "id": f"q_{base_id_num + 1:04d}",
            "category": cat_id,
            "category_label": cat_label,
            "experience_level": "2-4",
            "experience_label": "2–4 Yrs (Mid-Level)",
            "difficulty": "Mid / Senior",
            "company_tags": random.choice(COMPANY_POOLS['mid']),
            "question": f"How do you mathematically formulate and evaluate {title}, and what are its production trade-offs?",
            "answer": (
                f"**Mathematical & Technical Breakdown:**\n"
                f"{logic or defn}\n\n"
                f"{formula_sec}"
                f"{num_sec}"
                f"**Engineering Pros & Cons:**\n"
                f"- **Pros:** High predictive utility, mathematically bounded behavior, robust generalization when tuned.\n"
                f"- **Cons:** Sensitive to edge cases, hyperparameter calibration overhead, and computational constraints.\n\n"
                f"**Production Debugging Strategy:**\n"
                f"{pitfalls or 'Monitor loss divergence, gradient norms, and slice-level validation metrics to catch edge failures early.'}"
            ),
            "tip": f"For mid-level roles, explain both the mathematical foundation and the practical engineering trade-offs of {title}."
        }
        combined_questions.append(q2)

        # Question 3: Senior / Staff (5+ Yrs)
        q3 = {
            "id": f"q_{base_id_num + 2:04d}",
            "category": cat_id,
            "category_label": cat_label,
            "experience_level": "5+",
            "experience_label": "5+ Yrs (Senior / Staff)",
            "difficulty": "Senior / Staff",
            "company_tags": random.choice(COMPANY_POOLS['senior']),
            "question": f"How would you architect, scale, and monitor {title} in a high-throughput, mission-critical distributed production environment?",
            "answer": (
                f"**Production Architectural Blueprint:**\n"
                f"Deploying {title} at web scale (tens of thousands of QPS with strict $<20$ ms p99 latency SLAs) requires isolating online compute paths from offline batch operations.\n\n"
                f"**1. Distributed Serving & Acceleration:**\n"
                f"- Compile computation graphs using TensorRT, TorchDynamo, or ONNX Runtime to minimize operator launch overhead.\n"
                f"- Utilize thread-safe connection pooling, worker concurrency, and asynchronous batching.\n\n"
                f"**2. Mathematical Invariants & Health Checks:**\n"
                f"{logic}\n\n"
                f"**3. Observability & Failure Recovery:**\n"
                f"- **Drift & Degradation:** Emit Prometheus metrics for feature distribution divergence, latency percentiles, and inference error rates.\n"
                f"- **Graceful Degradation:** Implement circuit breakers to route to fallback heuristics if latency exceeds strict budget boundaries.\n\n"
                f"**Real-World Impact:**\n"
                f"{example or 'Ensures resilient 99.99% uptime with predictable resource utilization across cloud clusters.'}"
            ),
            "tip": f"Frame your response around latency budgets (p95/p99), memory boundaries, failure recovery, and observability rather than textbook theory."
        }
        combined_questions.append(q3)
        count_generated += 3

    print(f"Generated {count_generated} concept-aligned questions.")

    # 4. Add specialized real-world scenarios to exceed 1,020+
    for s in SPECIALIZED_SCENARIOS:
        spec_id = f"q_{len(combined_questions) + 1:04d}"
        combined_questions.append({
            "id": spec_id,
            "category": s["category"],
            "category_label": s["category_label"],
            "experience_level": s["experience_level"],
            "experience_label": f"{s['experience_level']} Yrs (Senior / Staff)",
            "difficulty": s["difficulty"],
            "company_tags": s["companies"],
            "question": s["question"],
            "answer": s["answer"],
            "tip": s["tip"]
        })

    # Re-index all question IDs cleanly so they are sequential and consistent if needed,
    # or preserve existing IDs while indexing new ones
    print(f"Total Combined Questions: {len(combined_questions)}")

    # Write out to src/data/interviewQuestions.json
    with open(iv_path, "w", encoding="utf-8") as f:
        json.dump(combined_questions, f, indent=2, ensure_ascii=False)

    print(f"Successfully saved {len(combined_questions)} questions to {iv_path}!")

if __name__ == "__main__":
    generate_questions()
