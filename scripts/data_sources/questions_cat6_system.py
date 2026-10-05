"""Category 6: Production MLOps, System Design & Latency Optimization (Questions 116-135)"""

CAT6_QUESTIONS = [
    {
        "id": "sys_116",
        "category": "system_mlops",
        "category_label": "MLOps & System Design",
        "difficulty": "Mid / Senior",
        "company_tags": ["Amazon", "Uber", "Google", "Stripe"],
        "question": "Why does optimizing average (mean) latency hide severe tail-latency bottlenecks in real-time ML systems? Why do SLA contracts mandate P95 and P99 latency guarantees?",
        "answer": """**1. The Flaw of Mean (Average) Latency:**
Average latency divides total time by request count. A small fraction of severe outliers (e.g. Garbage Collection pauses, network retries, cache misses, GPU cold starts) are completely diluted by the massive volume of fast requests.
- *Example:* 99 requests take $10\\text{ms}$, but 1 request hangs for $10,000\\text{ms}$ (10 seconds).
  $$\\text{Average Latency} = \\frac{99 \\times 10 + 10,000}{100} = 109.9\\text{ms}$$
  The average looks acceptable (~110ms), but 1% of users experienced an unbearable 10-second freeze!

**2. The Microservice Fanout Multiplier (Tail Latency Amplification):**
In modern enterprise architectures, loading a single user webpage triggers **fan-out requests to 50 downstream microservices** in parallel (Recommendation model, Fraud scorer, Ad ranker, User profile):
$$P(\\text{User experiences slow page}) = 1 - (1 - 0.01)^{50} = 1 - 0.605 = \\mathbf{39.5\\%!}$$
Even if each individual ML model has only a **1% tail spike (P99)**, nearly **40% of all real-world customer requests** suffer agonizing latency delays!

**3. Why SLAs Require P95/P99/P99.9:**
Percentiles strictly bound user experience:
- **P95:** 95% of all requests complete faster than this threshold.
- **P99:** The worst 1% of user interactions are guaranteed to finish within this limit, protecting conversion rates and preventing cascading queue pileups.""",
        "tip": "Dean & Barroso's famous paper 'The Tail at Scale' (Google, 2013) is the foundational citation for this question."
    },
    {
        "id": "sys_117",
        "category": "system_mlops",
        "category_label": "MLOps & System Design",
        "difficulty": "Junior / Mid",
        "company_tags": ["Netflix", "Amazon", "Databricks"],
        "question": "Compare Batch (Offline) Inference and Online (Real-Time) Inference. What are the architectural trade-offs in throughput, latency, cost, and freshness?",
        "answer": """- **Batch (Offline) Inference:**
  - *Architecture:* Scheduled batch pipelines (Apache Spark, Ray, Airflow) process millions of records periodically (e.g. nightly) and pre-compute predictions into a key-value store (DynamoDB / Redis).
  - *Throughput:* Extremely high (maximizes GPU/CPU saturation with massive batch sizes).
  - *Latency:* Milliseconds at query time (pure key-value lookup: `GET user_123_recommendations`).
  - *Cost:* Low (uses cheap spot instances during off-peak hours).
  - *Limitation (Stale Freshness):* Cannot react to real-time user context (e.g. user's last 3 clicks in the current session).
- **Online (Real-Time) Inference:**
  - *Architecture:* Real-time microservices (FastAPI, Triton Inference Server, TorchServe, vLLM) receive HTTP/gRPC requests, fetch online features, and run forward passes on-demand.
  - *Throughput:* Lower per dollar (must handle variable traffic spikes and low batch sizes).
  - *Latency:* 10ms - 500ms depending on model size.
  - *Freshness:* Zero latency drift; incorporates instant in-session behavior.""",
        "tip": "Explain hybrid architectures: pre-compute slow candidate embeddings offline, and re-rank with a fast real-time model online."
    },
    {
        "id": "sys_118",
        "category": "system_mlops",
        "category_label": "MLOps & System Design",
        "difficulty": "Mid / Senior",
        "company_tags": ["DoorDash", "Uber (Michelangelo)", "Feast"],
        "question": "What is Training-Serving Skew in machine learning? How does a Feature Store (e.g. Feast / Hopsworks) prevent it?",
        "answer": """**1. The Training-Serving Skew Catastrophe:**
Occurs when the feature values seen by a model during production inference differ systematically from the features it learned on during offline training.
- *Root Cause:* Data science teams write offline feature pipelines in SQL / Snowflake / Spark for training, while backend software engineers re-implement the 'same' features in Java / Go / Python for low-latency live APIs.
- Differences in timezone parsing, floating-point rounding, window definitions (e.g. last 7 days vs last 168 hours), or lookahead leakage lead to silent performance degradation.

**2. How a Feature Store Solves It (Dual Storage Engine):**
Maintains a **single unified feature definition** that serves two distinct storage backends:
1. **Offline Store (Snowflake / BigQuery / Parquet):**
   Stores historical time-stamped feature logs. Performs point-in-time correct **time-travel joins** to build training datasets with zero future data leakage.
2. **Online Store (Redis / DynamoDB / Cassandra):**
   Stores only the latest feature snapshot per entity for sub-2ms point lookups during live HTTP inference requests.
Guarantees $100\\%$ feature parity across training and serving.""",
        "tip": "Mention Uber's Michelangelo platform as the pioneer of the feature store paradigm in production ML."
    },
    {
        "id": "sys_119",
        "category": "system_mlops",
        "category_label": "MLOps & System Design",
        "difficulty": "Mid / Senior",
        "company_tags": ["Netflix", "Meta", "Google"],
        "question": "Compare Model Deployment Strategies: Canary Deployment, Blue/Green Deployment, and Shadow (Dark) Launching.",
        "answer": """- **Blue/Green Deployment:**
  - Maintains two identical production environments: *Blue* (active live model) and *Green* (idle new candidate model).
  - Deploy new model to Green, run integration tests, then flip router traffic $100\\%$ from Blue to Green.
  - *Benefit:* Instant rollback (flip router back to Blue if errors occur).
  - *Drawback:* Expensive ($2\\times$ infrastructure), and bugs hit all users at once if not caught.
- **Canary Deployment:**
  - Gradually shifts live user traffic from old model to new model in increments: $1\\% \\to 5\\% \\to 25\\% \\to 100\\%$.
  - Monitors error rates, latency P99, and business metrics continuously.
  - *Benefit:* Minimizes blast radius. If candidate model has a memory leak, only 1% of users are impacted.
- **Shadow (Dark) Launching:**
  - Ingress router duplicates live production requests: the primary model answers the user, while an asynchronous copy of the request is sent to the candidate model in the background.
  - Candidate model predictions are logged and evaluated against ground truth, but **never returned to the user**.
  - *Benefit:* Validates real-world latency, throughput, and accuracy under 100% live production load with **zero risk to users**.""",
        "tip": "Recommend Shadow Launching as the prerequisite step before initiating a Canary rollout for mission-critical ML systems."
    },
    {
        "id": "sys_120",
        "category": "system_mlops",
        "category_label": "MLOps & System Design",
        "difficulty": "Senior",
        "company_tags": ["NVIDIA", "Tesla", "Apple"],
        "question": "How do inference compilation engines like NVIDIA TensorRT and ONNX Runtime optimize deep learning models for production serving?",
        "answer": """**1. Graph Surgery & Layer Fusion:**
Standard PyTorch executes each layer as a separate CUDA kernel call:
$$\\text{Conv} \\xrightarrow{\\text{VRAM write}} \\text{BatchNorm} \\xrightarrow{\\text{VRAM write}} \\text{ReLU}$$
TensorRT fuses these sequential operations into a **single unified kernel**:
$$[\\text{Conv} + \\text{BatchNorm} + \\text{ReLU}]_{\\text{Fused Kernel}}$$
Eliminates intermediate round-trips to GPU memory, reducing memory bandwidth pressure.

**2. Kernel Auto-Tuning:**
Profiles multiple candidate CUDA kernel implementations for the specific target GPU architecture (e.g. Hopper H100 vs Ada Lovelace L40S) to select the exact block and thread tile dimensions that maximize Tensor Core saturation.

**3. Precision Calibration & Quantization:**
Fuses FP16 and INT8 quantization with dynamic per-tensor scaling factors, reducing memory footprint by $2-4\\times$ and doubling throughput on Tensor Cores.

**4. Dynamic Memory Management:**
Pre-allocates unified execution scratchpad buffers, eliminating runtime `cudaMalloc` overhead.""",
        "tip": "State that layer fusion and memory bandwidth reduction are where 60-80% of TensorRT speedups originate."
    },
    {
        "id": "sys_121",
        "category": "system_mlops",
        "category_label": "MLOps & System Design",
        "difficulty": "Senior / Staff",
        "company_tags": ["vLLM", "OpenAI", "Together AI"],
        "question": "What are the two distinct phases of LLM inference? Why is the Prefill Phase compute-bound while the Decoding Phase is memory-bandwidth bound?",
        "answer": """**1. Prefill Phase (Prompt Ingestion):**
- Ingests the entire user prompt of $N$ tokens simultaneously.
- Attention and MLP calculations execute large, parallel General Matrix Multiplies (GEMM) across all prompt tokens ($N \\times d$).
- High Arithmetic Intensity (FLOPs / Byte). GPU Tensor Cores are fully saturated.
- **Compute-Bound:** Performance is limited by GPU TFLOPs capacity.

**2. Decoding Phase (Autoregressive Generation):**
- Generates text token-by-token. Each step computes forward pass for only a **single token** ($1 \\times d$).
- At each step, all model parameters (e.g. 140GB for a 70B FP16 model) and past KV-cache tokens must be loaded from GPU VRAM into on-chip cache just to process that single token!
- Low Arithmetic Intensity. GPU compute cores sit idle waiting for weights to stream across memory buses.
- **Memory-Bandwidth Bound:** Generation speed is capped by GPU VRAM bandwidth ($TB/s$), not compute FLOPs!

**3. Architectural Mitigation (Chunked Prefill & Continuous Batching):**
Systems like vLLM and TensorRT-LLM co-schedule compute-heavy prefill chunks with memory-heavy decoding steps in the same batch to maximize overall GPU hardware saturation.""",
        "tip": "Explaining the Arithmetic Intensity transition between prefill and decoding is the hallmark of a staff-level AI systems engineer."
    },
    {
        "id": "sys_122",
        "category": "system_mlops",
        "category_label": "MLOps & System Design",
        "difficulty": "Senior / Staff",
        "company_tags": ["Stripe", "Visa", "PayPal", "Uber"],
        "question": "Design a real-time Fraud Detection system serving predictions in $< 15\\text{ms}$ while handling 100,000 transactions/second. Detail the data flow and latency budget.",
        "answer": """**1. Latency Budget Allocation ($15\\text{ms}$ total):**
- Ingress API Gateway & Authentication: $2\\text{ms}$
- Online Feature Store Retrieval (Redis): $3\\text{ms}$
- Model Inference Scoring (Quantized LightGBM on ONNX / C++): $5\\text{ms}$
- Business Policy Rules Engine & Decision Logging: $2\\text{ms}$
- Network Roundtrip & Safety Buffer: $3\\text{ms}$

**2. Architectural Blueprint:**
1. **Streaming Ingestion:** Transaction hits API Gateway $\\to$ pushes event to Apache Kafka / Redpanda partitioned by `user_id`.
2. **Dual-Path Architecture:**
   - **Path A (Real-Time Synchronous Scoring):**
     - Fetch pre-aggregated historical features (e.g. `spend_velocity_1h`, `failed_logins_24h`) from Redis Cluster in parallel via pipeline MGET ($< 2\\text{ms}$).
     - Feed features into a quantized LightGBM model executed in C++ via ONNX Runtime ($< 4\\text{ms}$).
     - If risk score $> 0.85 \\implies$ Decline; if $> 0.50 \\implies$ Step-up 2FA; else Approve.
   - **Path B (Asynchronous Graph & Streaming Analytics):**
     - Flink consumes Kafka stream to update rolling velocity counters in Redis.
     - Graph Neural Network / Tarjan's cycle algorithm runs asynchronously to detect multi-account laundering syndicate rings without blocking payment authorization.
3. **Automated Fallback:** If latency exceeds $12\\text{ms}$, trigger circuit breaker fallback to deterministic heuristic rules (e.g. approve transactions under 50 USD for low-risk merchants).""",
        "tip": "Interviewers want to see concrete millisecond budgets and an asynchronous split between point-in-time scoring and heavy graph analytics."
    },
    {
        "id": "sys_123",
        "category": "system_mlops",
        "category_label": "MLOps & System Design",
        "difficulty": "Mid / Senior",
        "company_tags": ["Capital One", "Zillow", "Upstart"],
        "question": "How do you monitor a machine learning model in production when ground truth labels are delayed by months (e.g. 90-day loan default prediction)?",
        "answer": """**1. The Delayed Feedback Dilemma:**
In credit underwriting, insurance claims, or customer lifetime value, whether a customer defaults ($y=1$) is not known for 3 to 12 months. Accuracy, Precision, and Recall cannot be computed in real-time.

**2. Proxy Monitoring Strategy (Input & Output Drift):**
Instead of waiting for ground truth labels, monitor distributions that are available immediately:
1. **Feature Distribution Drift (Covariate Shift):**
   - Monitor Population Stability Index (PSI) and Kolmogorov-Smirnov (KS) tests daily across incoming features (e.g. credit score, income, debt ratio) against training baselines.
2. **Model Prediction Drift (Output Shift):**
   - Monitor the distribution of predicted default probabilities $\\hat{p}$. If the fraction of high-risk predictions surges from $5\\%$ to $25\\%$, either the macro environment shifted or upstream data ingestion corrupted a feature.
3. **Upstream Data Integrity / Schema Violations:**
   - Monitor percentage of missing values, null rates, and type mismatches via Great Expectations.
4. **Short-Term Leading Indicator Proxies:**
   - Use early surrogate signals: 15-day missed payment, debit card overdraft, or customer service inquiries as immediate leading indicators of future 90-day defaults.""",
        "tip": "Explain that monitoring feature PSI and prediction score distribution is the primary defense when label latency is high."
    },
    {
        "id": "sys_124",
        "category": "system_mlops",
        "category_label": "MLOps & System Design",
        "difficulty": "Mid / Senior",
        "company_tags": ["DoorDash", "Uber", "Etsy"],
        "question": "Explain Continuous Training (CT) in MLOps. What automated triggers should initiate model retraining?",
        "answer": """**1. Concept:**
Continuous Training is an automated pipeline that ingests fresh data, retrains model architectures, runs automated validation gates, and registers candidate models without manual human intervention.

**2. 4 Automated Retraining Triggers:**
1. **Performance Degradation Trigger:** Live monitored business metrics (e.g. CTR, conversion rate) or ground-truth evaluation metrics (PR-AUC, RMSE) drop below a pre-defined SLA threshold.
2. **Data / Concept Drift Trigger:** Feature or prediction drift metric exceeds tolerance (e.g. feature $\\text{PSI} \\ge 0.20$ or KS-test $p < 0.01$).
3. **Data Volume Threshold Trigger:** Retrain automatically every time $N$ new labeled samples (e.g. 500,000 new verified purchases) are ingested.
4. **Scheduled Cadence (Periodic):** Time-based retraining (e.g. daily for volatile stock/ad models; weekly for recommendation feeds) to adapt to seasonality.

**3. Automated Safety Gate Before Deployment:**
Retrained candidate models must pass automated validation:
- Must outperform currently deployed production champion model on an out-of-time holdout test split.
- Must satisfy strict latency P99 benchmarks and zero-regression slice tests on critical customer subgroups.""",
        "tip": "Always mention automated Champion-Challenger evaluation gates before any retrained model touches production traffic."
    },
    {
        "id": "sys_125",
        "category": "system_mlops",
        "category_label": "MLOps & System Design",
        "difficulty": "Junior / Mid",
        "company_tags": ["MLflow", "Weights & Biases", "Amazon"],
        "question": "What is a Model Registry? What exact metadata must be tracked to guarantee 100% reproducibility in production AI systems?",
        "answer": """**1. Definition:**
A centralized repository and governance hub that tracks model artifacts throughout their entire lifecycle (Development $\\to$ Staging $\\to$ Production $\\to$ Archived). Examples: MLflow, AWS SageMaker Model Registry.

**2. Mandatory Reproducibility Metadata:**
1. **Code Versioning:** Exact Git commit hash of the training repository and pipeline scripts.
2. **Data Versioning:** Precise dataset snapshot hash or DVC / Delta Lake time-travel commit hash ($V_{train}$).
3. **Environment & Dependencies:** Complete Docker container image URI (with CUDA drivers and operating system libraries) and exact frozen package lockfile (`requirements.txt` / poetry lock).
4. **Hyperparameters & Configuration:** Full JSON config (learning rate, batch size, seed, tree depth, optimizer).
5. **Evaluation Metrics & Validation Gates:** Holdout performance (AUC, F1, latency, slice tests).
6. **Artifact Storage Pointer:** Secure S3/GCS URI to serialized model weights (`model.onnx`, `state_dict.pt`).
7. **Model Lineage & Sign-off:** Engineer identity, date, and governance approval signatures for compliance (EU AI Act / HIPAA).""",
        "tip": "Explain that model reproducibility requires locking the Trinity of ML: Code + Data + Environment."
    },
    {
        "id": "sys_126",
        "category": "system_mlops",
        "category_label": "MLOps & System Design",
        "difficulty": "Senior / Staff",
        "company_tags": ["AWS", "Microsoft Azure", "Salesforce"],
        "question": "How do you architect Multi-Tenant isolation in a shared enterprise LLM serving cluster? Address security, resource quotas, and tenant noisy-neighbor issues.",
        "answer": """**1. Compute & GPU Resource Isolation (Noisy-Neighbor Prevention):**
- **Dynamic Capacity Quotas:** Assign token-bucket rate limiters per tenant (Requests per Minute and Tokens per Minute).
- **Priority Queuing:** When GPU cluster is congested, high-tier enterprise tenants jump to priority queues, while free-tier requests are throttled or spilled over to slower spot instances.
- **Fair-Share Continuous Batching:** vLLM scheduler ensures a single tenant submitting 100 long prompt requests cannot starve other tenants' single-token chat queries.

**2. Data & Memory Isolation:**
- **Vector DB Namespaces:** Partition Pinecone / Qdrant indices using strict metadata namespace filters (`tenant_id == 'corp_a'`). Enforce database-level encryption with Customer-Managed Keys (AWS KMS).
- **Prompt Isolation:** Strict sandbox execution ensuring dynamic prompt templates cannot bleed cross-tenant data.

**3. Model Weight Multi-Tenancy (LoRA Adapters):**
Instead of spinning up separate 70B parameter base models for every enterprise client:
- Host a single shared base model in GPU VRAM.
- Load dynamic, client-specific **LoRA adapter weights (S-LoRA / Punica)** on-the-fly per request. Swapping tiny 50MB LoRA weights takes $< 5\\text{ms}$, serving 1,000 customized tenants from a single GPU cluster!""",
        "tip": "Cite S-LoRA (Sheng et al., 2023) or Punica for serving thousands of fine-tuned LoRA adapters concurrently on a shared base model."
    },
    {
        "id": "sys_127",
        "category": "system_mlops",
        "category_label": "MLOps & System Design",
        "difficulty": "Senior",
        "company_tags": ["Apple", "Google", "Meta"],
        "question": "How does Knowledge Distillation compress a 70B parameter LLM down to an 8B model for low-cost on-device or edge deployment?",
        "answer": """**1. The Compression Objective:**
A 70B model requires 140GB VRAM (2x A100 GPUs) and high inference costs. An 8B model requires only 16GB VRAM (runs on consumer GPUs or mobile devices).

**2. Distillation Pipeline:**
1. **Teacher Logit Distillation (White-Box):**
   - Forward pass input through 70B Teacher to obtain output probability distribution over vocabulary: $P_T = \\text{softmax}(z_T / T)$.
   - Train 8B Student to minimize Kullback-Leibler (KL) divergence between student logits and teacher logits:
     $$\\mathcal{L} = D_{KL}(P_T \\Vert P_S) + \\mathcal{L}_{CE}(y, P_S)$$
   - The student learns the rich probability distribution (dark knowledge) across candidate tokens rather than simple binary next-token targets.
2. **Synthetic Data Distillation (Black-Box):**
   - Prompt the 70B model with complex prompts to generate high-quality synthetic instruction-response pairs (CoT reasoning traces, code solutions, explanations).
   - Filter responses with automated verifiers/compilers.
   - Fine-tune the 8B model on the synthetic curriculum (e.g. Phi-3, Gemma-2, LLaMA-3-8B).
- Enables the 8B student model to achieve $>85\\%$ of the 70B teacher's benchmark capabilities.""",
        "tip": "Explain that synthetic data distillation (black-box) is now widely favored over raw logit distillation due to compute efficiency."
    },
    {
        "id": "sys_128",
        "category": "system_mlops",
        "category_label": "MLOps & System Design",
        "difficulty": "Mid / Senior",
        "company_tags": ["Pinterest", "Netflix", "Spotify", "YouTube"],
        "question": "Design a two-tower candidate generation and ranking architecture for YouTube/Netflix recommendation systems processing 1 billion items.",
        "answer": """**1. The Scale Challenge:**
Ranking 1 billion candidate videos through a complex deep neural network in $< 50\\text{ms}$ is computationally impossible ($10^9 \\times \\text{deep net} = \\text{hours}$).

**2. Two-Stage Industrial Funnel Architecture:**
- **Stage 1: Candidate Generation (Nomination / Retrieval - Two-Tower):**
  - Filters 1,000,000,000 items down to **Top 1,000 candidates** in $< 10\\text{ms}$.
  - **User Tower:** Encodes user history, demographics, device, search context $\\to u(x) \\in \\mathbb{R}^{128}$.
  - **Item Tower:** Encodes video tags, creator, audio/visual features $\\to v(y) \\in \\mathbb{R}^{128}$.
  - Item embeddings are precomputed and indexed in a vector search engine (ScaNN / HNSW).
  - Retrieval is a single fast Maximum Inner Product Search (MIPS): $\\arg\\max_{y} u(x)^T v(y)$.
- **Stage 2: Scoring & Heavy Ranking:**
  - Evaluates only the top 1,000 candidates from Stage 1 using a complex, feature-rich model (Deep & Cross Network, Transformer, or LightGBM).
  - Uses real-time features: user-item interactions, exact position bias, context time, freshness.
  - Computes expected engagement: $P(\\text{Click}) \\times \\mathbb{E}[\\text{Watch Time}]$.
- **Stage 3: Re-ranking & Diversity:**
  - Filters seen items, applies diversity constraints (not all videos from same creator), and injects exploration/freshness slots.""",
        "tip": "Cite the seminal Google paper 'Deep Neural Networks for YouTube Recommendations' (Covington et al., 2016)."
    },
    {
        "id": "sys_129",
        "category": "system_mlops",
        "category_label": "MLOps & System Design",
        "difficulty": "Mid / Senior",
        "company_tags": ["Netflix", "Amazon", "Uber"],
        "question": "What is the Circuit Breaker pattern in ML microservices? How does it prevent cascading failures when an upstream model times out?",
        "answer": """**1. The Cascading Failure Threat:**
If a downstream ML service (e.g. real-time personalization model) experiences high latency or crashes, upstream client requests queue up waiting for responses.
Worker threads block, connection pools exhaust, and the entire parent API crashes, causing a total site outage.

**2. Circuit Breaker States (Martin Fowler):**
- **CLOSED (Normal Operation):** All requests pass to the ML service. If failure rate exceeds threshold (e.g. $>50\\%$ timeouts over 10 seconds), the circuit **TRIPS to OPEN**.
- **OPEN (Failing Fast):** All incoming requests **immediately fail fast** or divert to fallback without calling the broken ML service. Prevents overloading the failing model and preserves upstream thread pools.
- **HALF-OPEN (Recovery Probe):** After a cooldown period (e.g. 30 seconds), allows a small percentage of test canary requests through. If they succeed, circuit resets to **CLOSED**; if they fail, circuit flips back to **OPEN**.

**3. Graceful Fallback Strategies:**
- Fall back to cached historical predictions.
- Fall back to a fast, static popularity baseline (e.g. top 10 trending items).
- Fall back to a lightweight, deterministic heuristic rule.""",
        "tip": "Emphasize that an ML system must always have a graceful deterministic fallback when its neural network times out."
    },
    {
        "id": "sys_130",
        "category": "system_mlops",
        "category_label": "MLOps & System Design",
        "difficulty": "Senior / Staff",
        "company_tags": ["vLLM", "OpenAI", "Anyscale"],
        "question": "How does Continuous Batching (Iteration-Level Scheduling - Orca, 2022) differ from traditional Static Batching in LLM serving?",
        "answer": """**1. The Flaw of Traditional Static Batching:**
In standard batching, $B$ requests are grouped together.
Because different requests generate varying output lengths (e.g. Request 1 generates 10 tokens, Request 2 generates 500 tokens):
- Request 1 finishes in 10 steps, but its GPU memory and thread slot **must sit idle as wasted padding** for the remaining 490 steps until Request 2 finishes!
- New incoming requests cannot enter the batch until the entire static batch completes.
- Wasteful and causes catastrophic queuing delays.

**2. Continuous Batching (Iteration-Level Batching):**
Operates at the granularity of a **single token iteration step**:
1. At every iteration step, the scheduler inspects the batch.
2. The instant Request 1 emits its `<EOS>` token at step 10, it is immediately evicted and its output returned to the user.
3. A newly arrived Request 3 is inserted into the empty slot in the very next step!
- GPUs run at continuous $100\\%$ operational saturation.
- Increases serving throughput by **$2-4\\times$** and slashes average queue latency by $>80\\%$.""",
        "tip": "Explain that continuous batching was introduced by the Orca paper (OSDI 2022) and popularized globally by vLLM."
    },
    {
        "id": "sys_131",
        "category": "system_mlops",
        "category_label": "MLOps & System Design",
        "difficulty": "Junior / Mid",
        "company_tags": ["Databricks", "Amazon"],
        "question": "What is Automated Data Validation in production ML pipelines? What automated assertions should tools like Great Expectations enforce?",
        "answer": """**1. Purpose:**
Silent data corruption (e.g. missing columns, null spikes, shifted schemas) is the #1 cause of catastrophic model failures. Automated data validation acts as a circuit breaker at the front door of the training and inference pipeline.

**2. Key Automated Assertions (Great Expectations / TFDV):**
1. **Schema & Type Integrity:** Assert column names, data types (float vs int vs string), and structural dimensions.
2. **Null / Completeness Check:** `expect_column_values_to_not_be_null(column='user_id')`. Flag if missing percentage exceeds 0.1%.
3. **Range & Boundary Checks:** `expect_column_values_to_be_between(column='age', min=18, max=120)`. Catch sensor errors (e.g. negative prices, temperature of 9999).
4. **Categorical Set Validation:** `expect_column_values_to_be_in_set(column='country', allowed_set=['US', 'CA', 'UK'])`. Detect unhandled new categories that would crash encoders.
5. **Distributional Checks:** Assert that feature mean and variance fall within historical statistical bounds.""",
        "tip": "Highlight that failing data validation must halt downstream model training and alert engineers before corrupted models are deployed."
    },
    {
        "id": "sys_132",
        "category": "system_mlops",
        "category_label": "MLOps & System Design",
        "difficulty": "Mid / Senior",
        "company_tags": ["Cloudflare", "OpenAI", "AWS"],
        "question": "How do you defend an enterprise LLM API against Denial of Service (DoS) via Token Exhaustion and Model Extraction attacks?",
        "answer": """**1. Defense Against Token Exhaustion (DoS):**
- **Strict `max_tokens` Bounding:** Clamp maximum generation tokens and reject unbounded input contexts.
- **Cost-Weighted Rate Limiting:** Enforce token-bucket algorithms based on estimated computational cost (Input Tokens + Max Output Tokens) rather than raw request counts.
- **Streaming Response Timeouts:** Terminate generation if client throttles consumption or drops connection.

**2. Defense Against Model Extraction (Distillation Scraping):**
Attackers query the API with millions of diverse prompts to steal model weights via knowledge distillation.
- **Query Pattern & Entropy Anomaly Detection:** Flag user accounts making programmatic high-volume queries spanning broad, out-of-distribution synthetic vocabularies.
- **Logit Obfuscation:** Never return full logit probabilities or top-5 alternative tokens to public API users; return only the sampled text.
- **Watermarking (Kirchenbauer et al.):** Embed imperceptible statistical green/red list token biases into outputs to legally prove intellectual property theft if competitor trains on the scraped data.""",
        "tip": "Mention Kirchenbauer's statistical watermarking method as the state-of-the-art IP defense against model extraction."
    },
    {
        "id": "sys_133",
        "category": "system_mlops",
        "category_label": "MLOps & System Design",
        "difficulty": "Mid",
        "company_tags": ["AWS", "Google Cloud", "Netflix"],
        "question": "Compare Horizontal Pod Autoscaling (HPA) and Vertical Pod Autoscaling (VPA) for ML inference clusters in Kubernetes. What metrics should trigger scaling?",
        "answer": """- **Horizontal Pod Autoscaling (HPA):**
  - Dynamically adds or removes replicas (pods/containers) across nodes.
  - Standard for stateless inference microservices.
  - Fast, zero downtime.
- **Vertical Pod Autoscaling (VPA):**
  - Increases CPU, RAM, or GPU allocation of existing pods.
  - Requires restarting the container; causes downtime or connection drops. Unsuitable for fast real-time scaling.

**Optimal Autoscaling Triggers for ML Inference:**
- **Do NOT rely exclusively on CPU/GPU utilization!**
  - Neural network servers (Triton / TorchServe) often pre-allocate GPU memory and keep threads spinning, reporting misleadingly high utilization.
- **Use Concurrency & Queue Depth:**
  - Scale on **Queue Latency** or **Concurrent Request Queue Length** (e.g. scale out when request queue depth $> 10$ requests per replica).
  - Use custom metrics from Prometheus / Envoy to scale ahead of latency SLA breaches.""",
        "tip": "Explain why queue depth is far superior to GPU utilization as an autoscaling metric for LLM and deep learning workloads."
    },
    {
        "id": "sys_134",
        "category": "system_mlops",
        "category_label": "MLOps & System Design",
        "difficulty": "Mid",
        "company_tags": ["Stripe", "Airbnb", "Celery"],
        "question": "What is the role of Asynchronous Task Queues (Celery, Kafka, Redis Queue) in decoupling long-running AI pipelines from user-facing HTTP endpoints?",
        "answer": """**1. The HTTP Timeout Problem:**
Generative AI tasks (video generation, multi-hop RAG, document parsing, fine-tuning) take seconds to minutes.
Holding an open HTTP request for 60 seconds ties up server connection threads, causes gateway timeouts (504 Gateway Timeout), and fails on unstable mobile networks.

**2. Asynchronous Queue Architecture:**
1. Client submits task via `POST /api/v1/generate-report`.
2. HTTP server validates request, pushes task payload to queue (Redis / RabbitMQ / Kafka), and **instantly returns HTTP 202 Accepted** with a unique `task_id` in $< 10\\text{ms}$.
3. Background worker pool (Celery / Ray workers) pulls jobs from queue, executes heavy GPU pipeline, and writes results to database/S3.
4. Client checks status via:
   - Polling: `GET /api/v1/tasks/{task_id}`.
   - WebSockets or Server-Sent Events (SSE) for live streaming progress updates.
   - Webhook callback URL once complete.
Ensures web tier remains 100% responsive and resilient to traffic spikes.""",
        "tip": "Mention that HTTP 202 Accepted + Webhook/WebSocket is the universal enterprise design pattern for long-running AI jobs."
    },
    {
        "id": "sys_135",
        "category": "system_mlops",
        "category_label": "MLOps & System Design",
        "difficulty": "Senior / Staff",
        "company_tags": ["Google", "DeepMind", "Meta"],
        "question": "What is Data Parallelism vs Model Parallelism communication overhead? Explain the ring-AllReduce algorithm.",
        "answer": """**1. Communication Bottleneck:**
In Distributed Data Parallelism across $N$ GPUs, each GPU computes local parameter gradients $\\nabla W_i$. All GPUs must synchronize gradients before taking an optimization step: $\\bar{g} = \\frac{1}{N} \\sum g_i$.
- Naive master-worker synchronization creates a severe network bandwidth bottleneck at the master node ($O(N \\times \\text{size})$).

**2. Ring-AllReduce Algorithm (Patarasuk & Yuan, 2009):**
Organizes the $N$ GPUs into a logical circular ring.
Grades are split into $N$ equal chunks. The algorithm executes in two phases:
1. **Scatter-Reduce Phase ($N-1$ steps):**
   - Each GPU sends chunk $k$ to its right neighbor and receives chunk $k-1$ from its left neighbor, summing received gradients.
   - After $N-1$ steps, each GPU holds the complete global sum for one unique chunk of the gradient vector.
2. **Allgather Phase ($N-1$ steps):**
   - Each GPU sends its fully summed chunk around the ring until all GPUs hold the complete synchronized gradient vector.

**3. Communication Volume:**
Total data transferred per GPU is:
$$\\text{Total Sent} = 2 \\left( \\frac{N-1}{N} \\right) \\times \\text{Model Size}$$
- **Key Insight:** As $N$ grows large, $\\frac{N-1}{N} \\to 1$. Communication volume is **completely independent of the number of GPUs $N$**! It depends solely on model size, allowing linear scaling to thousands of GPUs.""",
        "tip": "Highlight that Ring-AllReduce bandwidth independence is the mathematical foundation of NCCL (NVIDIA Collective Communications Library)."
    }
]
