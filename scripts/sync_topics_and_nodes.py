import json

# 1. Load concepts
with open('src/data/concepts.json', 'r', encoding='utf-8') as f:
    concepts = json.load(f)

# Group concepts by topic_id
concepts_by_topic = {}
for c in concepts:
    tid = c['topic_id']
    concepts_by_topic.setdefault(tid, []).append(c)

print(f"Total concepts: {len(concepts)} across {len(concepts_by_topic)} distinct topics.")

# 2. Load topics.json
with open('src/data/topics.json', 'r', encoding='utf-8') as f:
    topics = json.load(f)

existing_t_ids = set(t['id'] for t in topics)

new_topic_defs = [
    {
        "id": "ml_svm_ensembles",
        "category": "ml",
        "label": "Support Vector Machines & Production Ensembles",
        "level": 2,
        "x": 680,
        "y": 1400,
        "def": "Maximum-margin hyperplane classification using convex quadratic optimization, kernel trick projections for non-linear decision boundaries, and production model ensembles (voting, stacking, bagging).",
        "formula": r"\min_{w, b, \xi} \frac{1}{2}\|w\|^2 + C \sum_{i=1}^n \xi_i \quad \text{s.t.} \quad y_i(w^T \phi(x_i) + b) \ge 1 - \xi_i",
        "logic": "Maximizing the margin between support vectors maximizes generalization robustness against unseen noise.",
        "example": "Multi-tenant fraud classification using scikit-learn pipelines serialized with Joblib for sub-millisecond scoring.",
        "connections": ["ml_linear", "ml_trees", "eval_tradeoff"]
    },
    {
        "id": "dl_frameworks_cv_inference",
        "category": "dl",
        "label": "Deep Learning Framework Internals & Real-Time CV Inference",
        "level": 2,
        "x": 1380,
        "y": 1900,
        "def": "Execution graph internals in PyTorch vs TensorFlow, computer vision object detection evaluation metrics (mAP, IoU), YOLO real-time architectures, and high-performance inference acceleration via ONNX and DeepSparse.",
        "formula": r"\text{IoU} = \frac{\text{Area}(B_p \cap B_{gt})}{\text{Area}(B_p \cup B_{gt})}, \quad \text{mAP} = \frac{1}{N}\sum_{k=1}^N \text{AP}_k",
        "logic": "Separating model graph compilation from execution and quantizing weights to INT8 enables ultra-low latency inference on edge and server hardware.",
        "example": "Real-time industrial defect anomaly detection running a YOLOv8 model optimized via ONNX Runtime on edge cameras at 120 FPS.",
        "connections": ["dl_vision", "dl_backprop", "mlops_root"]
    },
    {
        "id": "genai_decoding_architectures",
        "category": "genai",
        "label": "LLM Decoding Dynamics & GPT vs Llama Architecture",
        "level": 2,
        "x": 2050,
        "y": 1800,
        "def": "Token generation sampling strategies (temperature, top-k, top-p nucleus), architectural divergences between GPT and open-weight Llama ecosystems (RoPE, SwiGLU, RMSNorm, GQA), structured output guarantees via Pydantic/JSON schemas, and classical NLP tool bridging.",
        "formula": r"P(w_i) = \frac{\exp(z_i / T)}{\sum_j \exp(z_j / T)}, \quad \sum_{i \in V^{(p)}} P(w_i) \ge p",
        "logic": "Temperature controls the entropy of the softmax distribution while nucleus sampling dynamically truncates improbable long-tail hallucinations.",
        "example": "Generating strict JSON API payloads for automated booking systems using Pydantic schema validation and constrained grammar decoding.",
        "connections": ["genai_attention", "genai_prompt_agents", "genai_transformer_deep_dive"]
    },
    {
        "id": "genai_vector_db_pinecone",
        "category": "genai",
        "label": "Vector Databases, Pinecone & Enterprise Hybrid Retrieval",
        "level": 2,
        "x": 2180,
        "y": 1950,
        "def": "High-dimensional vector indexing (HNSW graphs, IVF-PQ), cloud vector database infrastructure (Pinecone namespaces, metadata filtering, serverless index scaling), and hybrid dense-sparse search evaluation.",
        "formula": r"\text{RRF\_Score}(d) = \sum_{m \in \{\text{dense}, \text{sparse}\}} \frac{1}{k + r_m(d)}",
        "logic": "Combining dense semantic embeddings with sparse keyword BM25 rankings guarantees high recall for rare acronyms and entity lookups.",
        "example": "Multi-tenant enterprise knowledge base indexing 10 million technical PDFs with customer-isolated Pinecone namespaces and sub-50ms hybrid retrieval.",
        "connections": ["genai_rag", "genai_embed", "mlops_root"]
    },
    {
        "id": "genai_multimodal_agents",
        "category": "genai",
        "label": "Multimodal Foundation Models & Advanced Agentic Workflows",
        "level": 2,
        "x": 2250,
        "y": 2150,
        "def": "Joint text-vision contrastive embeddings (CLIP), diffusion generation processes (DDPM forward/reverse Gaussian transitions), sketch-to-image and style transfer, stateful agent graphs (LangGraph cyclical execution, checkpoints), and multi-agent supervisor swarms.",
        "formula": r"\mathcal{L}_{\text{CLIP}} = -\frac{1}{2N}\sum_{i=1}^N \left(\log \frac{\exp(\langle u_i, v_i \rangle/\tau)}{\sum_j \exp(\langle u_i, v_j \rangle/\tau)} + \log \frac{\exp(\langle u_i, v_i \rangle/\tau)}{\sum_j \exp(\langle u_j, v_i \rangle/\tau)}\right)",
        "logic": "Mapping disparate modalities into a shared latent metric space enables cross-modal similarity search, zero-shot image classification, and visual reasoning.",
        "example": "Fashion AI Copilot analyzing hand-drawn clothing sketches and generating production fabric textures with multi-agent trend intelligence.",
        "connections": ["genai_agentic_stack", "dl_generative", "genai_rag"]
    },
    {
        "id": "mlops_llmops_system_design",
        "category": "mlops",
        "label": "LLMOps, Multi-Tenancy & AI System Design",
        "level": 2,
        "x": 2350,
        "y": 1250,
        "def": "Productionizing generative AI at scale: semantic response caching (Redis, GPTCache), safety guardrails, token budget rate limiting, multi-tenant resource isolation, and complete architectural system design patterns for enterprise AI platforms.",
        "formula": r"\text{CacheHit}(q) = \mathbb{I}\left(\max_{k \in \mathcal{K}} \cos(\mathbf{e}_q, \mathbf{e}_k) \ge \tau_{\text{sim}}\right)",
        "logic": "Semantic vector caching bypasses costly foundation model API roundtrips for repeated intent queries, slashing latency and inference bills by 60%+.",
        "example": "Architecture of a multi-tenant enterprise LLM gateway serving 50,000 queries per minute with tenant quota enforcement, PII scrubbing, and fallback routing.",
        "connections": ["mlops_root", "genai_rag", "mlops_hygiene"]
    },
    {
        "id": "swe_patterns_architecture",
        "category": "swe_cloud",
        "label": "Software Engineering Patterns & Clean Architecture for AI",
        "level": 2,
        "x": 2480,
        "y": 1450,
        "def": "Software engineering principles tailored for AI engineers: creational and structural design patterns (Singleton, Factory, Strategy), Onion / Clean architecture with dependency inversion, high-throughput asynchronous REST APIs (FastAPI vs Flask), and automated PyTest testing suites.",
        "formula": r"\text{DIP}: \quad \text{High-Level Policy} \longrightarrow \text{Abstract Interface} \longleftarrow \text{Low-Level Infra}",
        "logic": "Decoupling machine learning core logic from external databases, GPU runners, and API frameworks ensures models can be updated and unit-tested without external dependencies.",
        "example": "Refactoring an inference pipeline using the Strategy pattern to seamlessly swap between local PyTorch, ONNX Runtime, and AWS SageMaker endpoints.",
        "connections": ["mlops_root", "swe_cloud_infra"]
    },
    {
        "id": "swe_cloud_infra",
        "category": "swe_cloud",
        "label": "Cloud Infrastructure, Containerization & Production Tooling",
        "level": 2,
        "x": 2550,
        "y": 1600,
        "def": "Industrial cloud ML deployment infrastructure: AWS vs Azure ecosystem tradeoffs, Docker containerization with NVIDIA CUDA runtime acceleration, ONNX model serialization, Postman API contract verification, and automated Git CI/CD deployment pipelines.",
        "formula": r"\text{Latency}_{\text{P99}} = T_{\text{network}} + T_{\text{queue}} + T_{\text{CUDA\_inference}} + T_{\text{deserialization}}",
        "logic": "Immutable multi-stage Docker builds ensure deterministic Python dependencies, preventing 'works on my machine' drift between dev environments and production GPU clusters.",
        "example": "Packaging a PyTorch sentiment analysis microservice into a multi-stage Docker container with CUDA base images deployed to AWS ECS with automatic scaling.",
        "connections": ["swe_patterns_architecture", "mlops_root"]
    }
]

for item in new_topic_defs:
    if item['id'] not in existing_t_ids:
        topics.append(item)
        existing_t_ids.add(item['id'])

# Ensure subtopics match concepts.json 1-to-1
for t in topics:
    tid = t['id']
    if tid in concepts_by_topic:
        t['subtopics'] = [c['title'] for c in concepts_by_topic[tid]]

with open('src/data/topics.json', 'w', encoding='utf-8') as f:
    json.dump(topics, f, indent=2, ensure_ascii=False)

print(f"Updated topics.json: now has {len(topics)} topics.")

# 3. Update allNodes.json
with open('src/data/allNodes.json', 'r', encoding='utf-8') as f:
    nodes = json.load(f)

existing_n_ids = set(n['id'] for n in nodes)

# Add hub_swe_cloud if not present
if "hub_swe_cloud" not in existing_n_ids:
    nodes.append({
        "id": "hub_swe_cloud",
        "category": "swe_cloud",
        "label": "Software Engineering & Cloud Infrastructure",
        "level": 1,
        "x": 2400,
        "y": 1500,
        "def": "Engineering depth, design patterns (Singleton, Factory), Onion architecture, cloud ecosystems (AWS, Azure), Docker containerization, and automated CI/CD release pipelines for AI systems.",
        "formula": r"\text{Enterprise AI} = \text{Model} + \text{Clean Architecture} + \text{Cloud Infrastructure}",
        "logic": "World-class AI systems require hardened software engineering standards, modular dependency inversion, and rock-solid cloud deployment hygiene.",
        "example": "Production microservice architectures deploying resilient, audited machine learning services at scale.",
        "subtopics": [
            "Software Engineering Patterns & Clean Architecture for AI",
            "Cloud Infrastructure, Containerization & Production Tooling"
        ],
        "connections": ["root", "swe_patterns_architecture", "swe_cloud_infra", "mlops_root"]
    })
    existing_n_ids.add("hub_swe_cloud")
    # Also ensure root has connection to hub_swe_cloud
    for n in nodes:
        if n['id'] == 'root':
            if 'hub_swe_cloud' not in n.get('connections', []):
                n.setdefault('connections', []).append('hub_swe_cloud')
            if 'Software Engineering & Cloud Infrastructure' not in n.get('subtopics', []):
                n.setdefault('subtopics', []).append('Software Engineering & Cloud Infrastructure')

# Add the new topic nodes to allNodes
for item in new_topic_defs:
    if item['id'] not in existing_n_ids:
        nodes.append({
            "id": item['id'],
            "category": item['category'],
            "label": item['label'],
            "level": 2,
            "x": item['x'],
            "y": item['y'],
            "def": item['def'],
            "formula": item['formula'],
            "logic": item['logic'],
            "example": item['example'],
            "subtopics": [c['title'] for c in concepts_by_topic[item['id']]],
            "connections": item['connections']
        })
        existing_n_ids.add(item['id'])

# Sync all node subtopics with concepts.json
for n in nodes:
    nid = n['id']
    if nid in concepts_by_topic and n.get('level') in (1, 2) and nid not in ('math_root', 'data_root', 'ml_root', 'eval_root', 'dl_root', 'genai_root', 'root', 'hub_swe_cloud'):
        n['subtopics'] = [c['title'] for c in concepts_by_topic[nid]]

with open('src/data/allNodes.json', 'w', encoding='utf-8') as f:
    json.dump(nodes, f, indent=2, ensure_ascii=False)

print(f"Updated allNodes.json: now has {len(nodes)} nodes.")

# 4. Add Phase 13 Mock Interview Questions
with open('src/data/interviewQuestions.json', 'r', encoding='utf-8') as f:
    interviews = json.load(f)

existing_q_ids = set(q['id'] for q in interviews)

mock_interview_questions = [
    {
        "id": "mock_coding_01",
        "category": "swe_cloud",
        "category_label": "Software Engineering & Cloud",
        "interview_round": "round_coding",
        "round_label": "Coding Round (Python / DSA)",
        "experience_level": "2-4",
        "experience_label": "2–4 Yrs (Mid-Level)",
        "difficulty": "Mid / Senior",
        "company_tags": ["Google", "Meta", "Amazon", "Databricks"],
        "question": "Phase 13 Coding Round: Implement a thread-safe Least Recently Used (LRU) Cache in Python supporting O(1) time complexity for get(key) and put(key, value) operations.",
        "answer": "**Problem Breakdown & Algorithmic Strategy:**\nTo achieve strictly O(1) time complexity for both `get` and `put`, we combine two classic data structures:\n1. **Hash Map (`dict`):** Provides instantaneous O(1) key-to-node lookup.\n2. **Doubly Linked List (DLL):** Enables O(1) node deletion and insertion at the head (Most Recently Used - MRU) and tail (Least Recently Used - LRU) without shifting contiguous memory arrays.\n\n```python\nfrom threading import Lock\n\nclass Node:\n    def __init__(self, key=0, val=0):\n        self.key, self.val = key, val\n        self.prev = self.next = None\n\nclass LRUCache:\n    def __init__(self, capacity: int):\n        self.capacity = capacity\n        self.cache = {}  # key -> Node\n        self.lock = Lock()\n        # Dummy sentinel head and tail nodes\n        self.head, self.tail = Node(), Node()\n        self.head.next = self.tail\n        self.tail.prev = self.head\n\n    def _remove(self, node: Node):\n        prev_node, next_node = node.prev, node.next\n        prev_node.next = next_node\n        next_node.prev = prev_node\n\n    def _insert_at_head(self, node: Node):\n        node.next = self.head.next\n        node.prev = self.head\n        self.head.next.prev = node\n        self.head.next = node\n\n    def get(self, key: int) -> int:\n        with self.lock:\n            if key not in self.cache:\n                return -1\n            node = self.cache[key]\n            self._remove(node)\n            self._insert_at_head(node)  # Mark as MRU\n            return node.val\n\n    def put(self, key: int, value: int) -> None:\n        with self.lock:\n            if key in self.cache:\n                self._remove(self.cache[key])\n            node = Node(key, value)\n            self.cache[key] = node\n            self._insert_at_head(node)\n            if len(self.cache) > self.capacity:\n                # Evict least recently used (node right before tail)\n                lru = self.tail.prev\n                self._remove(lru)\n                del self.cache[lru.key]\n```\n\n**Complexity Analysis:**\n- **Time Complexity:** `get`: O(1), `put`: O(1).\n- **Space Complexity:** O(capacity) to store elements in memory.\n- **Production Extension:** In Python production code, `collections.OrderedDict` provides the exact same behavior with C-level optimizations.",
        "tip": "Interviewers specifically test whether you use dummy head and tail sentinel nodes. Sentinels eliminate edge-case `if self.head is None` checks, demonstrating senior coding maturity."
    },
    {
        "id": "mock_coding_02",
        "category": "dl",
        "category_label": "Deep Learning",
        "interview_round": "round_coding",
        "round_label": "Coding Round (Python / DSA)",
        "experience_level": "2-4",
        "experience_label": "2–4 Yrs (Mid-Level)",
        "difficulty": "Mid / Senior",
        "company_tags": ["OpenAI", "Anthropic", "Apple", "NVIDIA"],
        "question": "Phase 13 Coding Round: Write a clean, vectorized implementation of Scaled Dot-Product Self-Attention with causal masking in NumPy or PyTorch from scratch without using torch.nn.MultiheadAttention.",
        "answer": "**Vectorized Self-Attention Implementation:**\n\n$$\\text{Attention}(Q, K, V) = \\text{softmax}\\left(\\frac{Q K^T}{\\sqrt{d_k}} + M\\right) V$$\n\n```python\nimport torch\nimport torch.nn.functional as F\n\ndef scaled_dot_product_attention(Q, K, V, mask=None):\n    \"\"\"\n    Q, K, V: [batch_size, num_heads, seq_len, head_dim]\n    mask: Optional [seq_len, seq_len] causal mask\n    \"\"\"\n    d_k = Q.size(-1)\n    \n    # 1. Batched matrix multiplication: Q @ K^T\n    # Shape: [batch, heads, seq_len, seq_len]\n    scores = torch.matmul(Q, K.transpose(-2, -1)) / (d_k ** 0.5)\n    \n    # 2. Apply causal mask (set upper triangle above diagonal to -inf)\n    if mask is not None:\n        scores = scores.masked_fill(mask == 0, float('-inf'))\n        \n    # 3. Softmax across last dimension (key sequence dimension)\n    attention_weights = F.softmax(scores, dim=-1)\n    \n    # 4. Context aggregation: Weights @ V\n    output = torch.matmul(attention_weights, V)\n    return output, attention_weights\n```\n\n**Numerical Stability Nuance:**\nDividing by $\\sqrt{d_k}$ prevents dot product scores from growing excessively large for high-dimensional vectors ($d_k=64, 128$), which would push softmax into flat saturation zones with near-zero gradients during backpropagation.",
        "tip": "Explain to the interviewer why we use `-inf` before softmax: $\\exp(-\\infty) = 0$, which ensures future tokens receive strictly zero attention weight during autoregressive text generation."
    },
    {
        "id": "mock_ml_theory_01",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "interview_round": "round_ml_theory",
        "round_label": "ML Theory Rapid-Fire",
        "experience_level": "0-2",
        "experience_label": "0–2 Yrs (Junior / Fresher)",
        "difficulty": "Junior / Mid",
        "company_tags": ["Stripe", "Visa", "PayPal", "Amazon"],
        "question": "Phase 13 ML Theory Rapid-Fire: When tuning classification decision thresholds on an extremely imbalanced credit card fraud dataset (0.01% fraud rate), should you optimize for Precision, Recall, or F1, and why?",
        "answer": "**Structured Answer:**\n\n1. **Business Cost Asymmetry:**\nIn fraud detection, the business cost of a **False Negative** (allowing a $10,000 fraudulent transaction to pass through unchecked) is vastly greater than the cost of a **False Positive** (sending an automated 2-second SMS confirmation alert to a legitimate customer).\n\n2. **Target Metric Priority:**\n- **Primary Metric: High Recall (Sensitivity):** We want to catch $\\ge 98\\%$ of all fraudulent transactions: $\\text{Recall} = \\frac{\\text{TP}}{\\text{TP} + \\text{FN}}$.\n- **Secondary Constraint: Precision Budget:** While maximizing recall, we maintain a minimum acceptable Precision (e.g. $\\ge 15\\%$) so customer support agents aren't overwhelmed investigating false alarms.\n\n3. **Decision Threshold Tuning:**\nInstead of the default `0.50` probability cutoff, we calibrate the threshold downwards (e.g. to `0.08` or `0.12`) based on the empirical Precision-Recall (PR) curve or custom financial loss matrix:\n$$\\text{Total Cost} = C_{\\text{FN}} \\cdot \\text{FN} + C_{\\text{FP}} \\cdot \\text{FP}$$",
        "tip": "Never say 'Accuracy' in an imbalanced classification interview! A naive model predicting 100% legitimate transactions gets 99.99% accuracy while letting all fraud through."
    },
    {
        "id": "mock_ml_theory_02",
        "category": "dl",
        "category_label": "Deep Learning",
        "interview_round": "round_ml_theory",
        "round_label": "ML Theory Rapid-Fire",
        "experience_level": "2-4",
        "experience_label": "2–4 Yrs (Mid-Level)",
        "difficulty": "Mid / Senior",
        "company_tags": ["Meta", "Google DeepMind", "Anthropic"],
        "question": "Phase 13 ML Theory Rapid-Fire: Why did Loshchilov & Hutter create AdamW, and how does decoupling weight decay from the moving average gradients fundamentally fix L2 regularization in adaptive optimizers?",
        "answer": "**The AdamW Breakthrough:**\n\n1. **The Flaw in Standard Adam:**\nIn standard SGD, L2 weight decay and gradient penalties are mathematically identical. However, in Adam, L2 regularization was historically implemented by adding $\\lambda \\theta$ directly to the gradient $g_t$.\nBecause Adam divides gradients by $\\sqrt{v_t}$ (the moving average of squared gradients), weights with large historical gradients had their regularization penalties **divided and shrunk**, while weights with tiny historical gradients had their regularization **amplified**.\n\n2. **The AdamW Solution (Decoupled Weight Decay):**\nAdamW subtracts weight decay directly from the weights at the final step, completely bypassing the first and second moment running averages:\n$$\\theta_{t+1} = \\theta_t - \\eta_t \\left( \\frac{\\hat{m}_t}{\\sqrt{\\hat{v}_t} + \\epsilon} + \\lambda \\theta_t \\right)$$\n\n3. **Empirical Impact:**\nDecoupling weight decay restored true exponential weight shrinkage across all parameters, drastically improving test generalization and becoming the universal optimizer for BERT, GPT-3/4, and Llama.",
        "tip": "Draw the equation or write it out clearly. Explaining that standard Adam scales down L2 decay on high-frequency weights shows you have deep mathematical mastery of optimizer internals."
    },
    {
        "id": "mock_sys_design_01",
        "category": "mlops",
        "category_label": "System Design",
        "interview_round": "round_system_design",
        "round_label": "System Design (AI / LLM Systems)",
        "experience_level": "5+",
        "experience_label": "5+ Yrs (Senior / Lead)",
        "difficulty": "Senior / Staff",
        "company_tags": ["Microsoft", "Google", "Amazon", "OpenAI"],
        "question": "Phase 13 System Design: Design an Enterprise Hybrid RAG System for 10 Million Internal Technical Documents with sub-200ms P95 latency and Role-Based Access Control (RBAC).",
        "answer": "**Comprehensive System Design Blueprint:**\n\n**1. High-Level Requirements:**\n- 10M documents (PDF, Markdown, Confluence, Word), average 5 pages.\n- P95 query latency < 200 ms; availability 99.9%.\n- Strict RBAC: Users only see documents permitted by their active directory security groups.\n\n**2. Architecture Components:**\n- **Asynchronous Ingestion Service:** Kafka queue receives document update webhooks. Celery worker fleet parses text, creates semantic chunks (512 tokens with 50-token overlap), and extracts document ACL metadata tags (e.g. `allowed_groups: ['eng', 'finance']`).\n- **Storage Layer:** Dual-Index Strategy:\n  * Dense Vectors: Pinecone Serverless (HNSW, 1536-dim) with namespace separation.\n  * Sparse Lexical: Elasticsearch / OpenSearch BM25 inverted index for exact error codes.\n- **Query Gateway (FastAPI ASGI):**\n  * Step 1: Redis Semantic Cache lookup (sub-10ms hit for frequent questions).\n  * Step 2: Extract User JWT token -> Inject user group claims into Pinecone metadata query filter: `{'groups': {'$in': user.groups}}`.\n  * Step 3: Run parallel Dense Vector + Sparse BM25 retrieval.\n  * Step 4: Reciprocal Rank Fusion (RRF) combines top 50 dense and top 50 sparse hits.\n  * Step 5: Lightweight Cross-Encoder Reranker (BGE-Reranker-Large on GPU) narrows top 100 down to the top 4 most relevant chunks.\n  * Step 6: vLLM engine generates streamed response using Llama-3-70B.\n\n**3. Bottlenecks & Mitigations:**\n- *Cold Start / Cache misses:* Pre-warm Redis cache with top 10,000 frequently asked employee queries.\n- *Context Window Bloat:* Limit generator context strictly to 4 reranked chunks (< 2k tokens) to prevent 'Lost in the Middle' degradation.",
        "tip": "Start your system design by clarifying functional requirements (RPS, doc size) and non-functional requirements (latency, RBAC security) before drawing boxes."
    },
    {
        "id": "mock_sys_design_02",
        "category": "mlops",
        "category_label": "System Design",
        "interview_round": "round_system_design",
        "round_label": "System Design (AI / LLM Systems)",
        "experience_level": "5+",
        "experience_label": "5+ Yrs (Senior / Lead)",
        "difficulty": "Senior / Staff",
        "company_tags": ["Uber", "Stripe", "Snowflake", "Databricks"],
        "question": "Phase 13 System Design: Design a High-Throughput Multi-Tenant Machine Learning Classification Platform serving 5,000 enterprise tenants with sub-15ms P99 latency and strict data isolation.",
        "answer": "**Multi-Tenant ML Platform Architecture:**\n\n**1. Key Challenges:**\n- 5,000 distinct enterprise models; cannot load all into GPU RAM simultaneously.\n- P99 latency < 15 ms; tenant data must never leak across customer boundaries.\n\n**2. Core Architecture:**\n- **API Gateway & Rate Limiter:** Envoy / FastAPI gateway enforcing Token Bucket rate limiting per tenant ID. Authenticates tenant API keys and extracts tenant model routing IDs.\n- **Tiered Model Serving Layer (Triton Inference Server):**\n  * Tier 1 (Hot Models - Top 200 active tenants): Kept pinned in GPU VRAM with Dynamic Batching (max_batch_size=32, max_queue_delay=2ms).\n  * Tier 2 (Warm Models - Next 1,000 tenants): Cached in Host System RAM (pinned memory); loaded to GPU in < 5 ms via CUDA streams.\n  * Tier 3 (Cold Models - Remaining 3,800 tenants): Serialized ONNX / Joblib artifacts stored in Amazon S3; fetched on-demand and cached via LRU eviction policy.\n- **Feature Store Integration:** Low-latency online feature store (Redis / Feast) providing pre-computed real-time entity features in < 2 ms via primary key lookups.\n- **Automated Retraining & Canary Pipeline:** Airflow / Kubeflow jobs train models weekly on tenant-isolated S3 buckets. New models deploy to a 2% traffic canary slice; if drift or error rates exceed 0.5%, traffic rolls back automatically.\n\n**3. Security & Disaster Recovery:**\nTenant-isolated encryption keys (AWS KMS BYOK) ensure that even at the storage layer, one tenant's raw model weights cannot be decrypted by unauthorized processes.",
        "tip": "Highlight the Hot/Warm/Cold tiered memory model! Interviewers love seeing practical awareness of GPU VRAM hardware cost constraints."
    },
    {
        "id": "mock_behavioral_01",
        "category": "system_mlops",
        "category_label": "System & MLOps",
        "interview_round": "round_behavioral",
        "round_label": "Behavioral & Experience",
        "experience_level": "2-4",
        "experience_label": "2–4 Yrs (Mid-Level)",
        "difficulty": "Mid / Senior",
        "company_tags": ["Amazon", "Google", "Airbnb", "Netflix"],
        "question": "Phase 13 Behavioral Round: Tell me about a time your production machine learning model suffered from Training-Serving Skew or Label Leakage. How did you identify the root cause and resolve it?",
        "answer": "**STAR Method Response Framework:**\n\n- **Situation:** At our previous e-commerce analytics company, we deployed a customer conversion prediction model that achieved an astounding 99.4% ROC-AUC in offline cross-validation notebooks. However, within 48 hours of production deployment, real-world conversion precision plummeted to 32%.\n\n- **Task:** As lead ML engineer, I had to identify why the offline validation failed to predict production reality, stop inaccurate customer targeting, and fix the feature pipeline without disrupting marketing campaigns.\n\n- **Action:**\n  1. I immediately audited the feature generation SQL queries and compared production log timestamps against database transaction timestamps.\n  2. I discovered **Label Leakage (Future Data Leakage)**: A feature called `last_checkout_session_id` was being populated by the payment processor webhook *during* the transaction. In offline historical dumps, this column was non-empty for all successful checkouts, giving the model a backdoor cheat code into the target label.\n  3. In live production, however, this field was still `NULL` when the model was queried before payment completion.\n  4. I purged the leaking feature, introduced **point-in-time joins** in our feature store (Feast), and implemented automated data validation tests in CI that assert all feature timestamps precede the prediction event timestamp strictly by $\\ge 1$ second.\n\n- **Result:** Offline validation ROC-AUC re-normalized to a realistic 83.2%, which matched production performance within 0.8% variance over the subsequent 6 months, saving $45,000 in wasted ad spend.",
        "tip": "Own the problem honestly! Interviewers respect engineers who understand subtle real-world gotchas like future timestamp leakage over candidates who claim their models never fail."
    },
    {
        "id": "mock_behavioral_02",
        "category": "system_mlops",
        "category_label": "System & MLOps",
        "interview_round": "round_behavioral",
        "round_label": "Behavioral & Experience",
        "experience_level": "5+",
        "experience_label": "5+ Yrs (Senior / Lead)",
        "difficulty": "Senior / Staff",
        "company_tags": ["LinkedIn", "Meta", "Uber", "Microsoft"],
        "question": "Phase 13 Behavioral Round: How do you balance trade-offs between model accuracy, inference latency, and cloud infrastructure costs when shipping an enterprise AI solution?",
        "answer": "**Senior Engineering Philosophy:**\n\n1. **Business-First SLA Definition:**\nBefore choosing an architecture, I define the hard non-negotiable boundaries: What is the maximum acceptable latency for the user experience? (e.g. < 250 ms for interactive autocomplete vs < 5 seconds for batch reporting) and what is the unit economics budget per query? (e.g. $0.001 per call).\n\n2. **The 80/20 Accuracy vs Cost Curve:**\nA frontier 70B parameter model might achieve 92% benchmark accuracy at $0.04 per query and 1,800 ms latency. A fine-tuned 8B model might achieve 89% accuracy at $0.001 per query and 80 ms latency.\nFor 95% of customer interactions, the 3% accuracy difference is completely unnoticeable, while the 40x cost reduction and 20x latency boost make the product commercially viable.\n\n3. **Practical Hybrid Compromise:**\nI implement **Cascaded / Tiered Model Routing**:\n- Route all queries to a fast, cheap quantized model (e.g. Llama-3-8B INT8 via vLLM) with a confidence scoring head.\n- If confidence is $\\ge 0.85$, return the answer immediately.\n- Only escalate the remaining 15% of ambiguous or complex queries to frontier models (GPT-4o / Claude 3.5 Sonnet).\nThis delivers 99th percentile quality while slashing 80%+ off cloud compute bills.",
        "tip": "Frame model selection as an engineering ROI decision rather than a pure academic pursuit of decimal points on leaderboards."
    },
    {
        "id": "mock_terminology_01",
        "category": "genai_llm",
        "category_label": "GenAI & LLMs",
        "interview_round": "round_terminology",
        "round_label": "Rapid-Fire Terminology Blitz",
        "experience_level": "2-4",
        "experience_label": "2–4 Yrs (Mid-Level)",
        "difficulty": "Mid / Senior",
        "company_tags": ["OpenAI", "Anthropic", "Google", "Mistral"],
        "question": "Phase 13 Terminology Blitz: In under 30 seconds each, contrast: 1) GQA vs MHA vs MQA, 2) SwiGLU vs GeLU, and 3) RoPE vs Absolute Positional Encoding.",
        "answer": "**Rapid-Fire Flashcard Answers:**\n\n**1. Attention Variants (MHA vs MQA vs GQA):**\n- **MHA (Multi-Head Attention):** Every query head has its own private key and value head. Highest representational capacity, but massive KV-cache memory footprint.\n- **MQA (Multi-Query Attention):** All query heads share a single key and single value head. Slashes KV-cache by 95%, but causes noticeable quality degradation in reasoning.\n- **GQA (Grouped-Query Attention):** The sweet-spot compromise where subsets of query heads (e.g. 8 Q heads) share one KV head pair. Used in Llama 3, Mistral, and Gemma.\n\n**2. Activation Functions (GeLU vs SwiGLU):**\n- **GeLU (Gaussian Error Linear Unit):** Multiplies input by the standard Gaussian cumulative distribution; standard in original BERT and GPT-2.\n- **SwiGLU (Swish Gated Linear Unit):** A bilinear gating mechanism: $\\text{Swish}(x W_1) \\otimes (x W_2)$. Requires three weight matrices instead of two in the feed-forward layer, but converges significantly faster with lower final validation perplexity.\n\n**3. Positional Embeddings (Absolute vs RoPE):**\n- **Absolute Positional Embeddings:** Add fixed lookup vectors to token embeddings at input layer. Cannot generalize beyond the pre-training context length.\n- **RoPE (Rotary Position Embeddings):** Multiplies query and key vectors by 2D rotation matrices based on token position index. Mathematically ensures that the inner product depends strictly on relative distance $(m - n)$, enabling seamless context window extrapolation.",
        "tip": "Keep each definition under 3 crisp sentences. Rapid-fire rounds reward precision, confident terminology, and zero waffle."
    },
    {
        "id": "mock_terminology_02",
        "category": "genai_llm",
        "category_label": "GenAI & LLMs",
        "interview_round": "round_terminology",
        "round_label": "Rapid-Fire Terminology Blitz",
        "experience_level": "0-2",
        "experience_label": "0–2 Yrs (Junior / Fresher)",
        "difficulty": "Junior / Mid",
        "company_tags": ["Google", "Meta", "Amazon", "Microsoft"],
        "question": "Phase 13 Terminology Blitz: In under 30 seconds each, contrast: 1) Temperature vs Top-P vs Top-K, 2) Precision vs Recall, and 3) L1 Lasso vs L2 Ridge regularization.",
        "answer": "**Rapid-Fire Flashcard Answers:**\n\n**1. Decoding Parameters (Temperature vs Top-P vs Top-K):**\n- **Temperature:** Divides raw logits before softmax; scales the sharpness of the distribution ($T \\to 0$ is deterministic greedy; $T > 1$ is creative randomness).\n- **Top-K:** Truncates candidate pool to the fixed top $K$ most probable tokens before sampling.\n- **Top-P (Nucleus):** Dynamically sums token probabilities until reaching cumulative threshold $p$ (e.g. 90%), expanding for diverse contexts and contracting for obvious next tokens.\n\n**2. Evaluation Metrics (Precision vs Recall):**\n- **Precision:** $\\frac{\\text{TP}}{\\text{TP} + \\text{FP}}$ — Out of everything the model predicted as positive, how many were actually correct? (Focuses on minimizing false alarms).\n- **Recall:** $\\frac{\\text{TP}}{\\text{TP} + \\text{FN}}$ — Out of all real positive instances in the world, how many did the model successfully find? (Focuses on avoiding missed detections).\n\n**3. Regularization (L1 Lasso vs L2 Ridge):**\n- **L1 Lasso:** Adds sum of absolute weights $\\lambda \\sum |w_i|$. Produces sparse models by driving uninformative feature weights strictly to zero (automatic feature selection).\n- **L2 Ridge:** Adds sum of squared weights $\\lambda \\sum w_i^2$. Shrinks weights smoothly toward zero without zeroing them out completely, handling collinear features gracefully.",
        "tip": "Deliver with energetic, confident pacing. Nailing these basic foundational distinctions in 60 seconds immediately establishes candidate credibility."
    }
]

for q in mock_interview_questions:
    if q['id'] not in existing_q_ids:
        interviews.append(q)
        existing_q_ids.add(q['id'])

with open('src/data/interviewQuestions.json', 'w', encoding='utf-8') as f:
    json.dump(interviews, f, indent=2, ensure_ascii=False)

print(f"Updated interviewQuestions.json: now has {len(interviews)} questions (including Phase 13 Mock Interview Rounds).")
