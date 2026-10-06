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
# 5. TOPIC: genai_multimodal_agents (Category: genai)
# ==============================================================
t_mma_id = "genai_multimodal_agents"
t_mma_label = "Multimodal Foundation Models & Advanced Agentic Workflows"

new_concepts.append(create_concept_obj(
    "concept_clip_contrastive_multimodal",
    "CLIP Multimodal Embeddings & Contrastive Vision-Language Alignment",
    t_mma_id, t_mma_label, "genai", "Transformers & Generative AI",
    "Contrastive Language-Image Pre-training (CLIP) maps images and natural language sentences into a joint shared embedding space by maximizing cosine similarity for matching pairs while minimizing similarity for mismatched pairs via InfoNCE symmetric cross-entropy loss.",
    r"\mathcal{L}_{\text{CLIP}} = -\frac{1}{2N}\sum_{i=1}^N \left(\log \frac{\exp(\langle u_i, v_i \rangle/\tau)}{\sum_j \exp(\langle u_i, v_j \rangle/\tau)} + \log \frac{\exp(\langle u_i, v_i \rangle/\tau)}{\sum_j \exp(\langle u_j, v_i \rangle/\tau)}\right)",
    "Joint multimodal metric geometry enables zero-shot image classification and cross-modal semantic search without training task-specific classifier heads.",
    "Fashion e-commerce search allowing users to type 'bohemian floral maxi dress' and instantly retrieve matching product catalog photos with zero manual image tagging.",
    [
        {"term": "Dual-Encoder Architecture", "what_is_it": "Separate image (Vision Transformer/ResNet) and text (Transformer) encoders that project both modalities into a normalized D-dimensional space.", "analogy": "Two bilingual translators translating English and visual photographs into the exact same universal coordinate system.", "why_it_matters": "Enables pre-computing and caching millions of image embeddings in a vector database for millisecond querying."},
        {"term": "Zero-Shot Classification", "what_is_it": "Classifying an image by computing cosine similarity against prompt embeddings like 'a photo of a {class_name}' without fine-tuning weights.", "analogy": "Looking up matching descriptions in an encyclopedia to identify an unfamiliar bird species.", "why_it_matters": "Eliminates the expensive requirement for hundreds of labeled training examples per visual category."}
    ],
    [
        {"symbol": "u_i, v_i", "meaning": "Normalized text embedding and image embedding", "plain_english": "Unit vectors in shared latent metric space (||u|| = ||v|| = 1)."},
        {"symbol": "\\tau", "meaning": "Learnable temperature parameter", "plain_english": "Controls the sharpness of the contrastive probability distribution."}
    ],
    "Given prompt embedding u and two image candidate embeddings v1, v2:\nCosineSim(u, v1) = 0.88; CosineSim(u, v2) = 0.32.\nSoftmax probability for Image 1 with tau = 0.07: P(v1) = exp(0.88/0.07) / [exp(0.88/0.07) + exp(0.32/0.07)] = 0.9997 (Confirmed match).",
    "Attempting to use CLIP for dense spatial localization (e.g. object bounding boxes); CLIP is trained on global image-level contrastive loss and lacks pixel-level bounding coordinates.",
    ["CLIP", "Multimodal AI", "Contrastive Learning", "Zero-Shot Classification", "Vision-Language"],
    [
        "CLIP projects text and images into an identical normalized latent vector space.",
        "Prompt engineering matters in CLIP: using 'a photo of a {label}' boosts accuracy by 5–10% over the raw word alone.",
        "CLIP embeddings form the visual conditioning backbone for modern diffusion models (Stable Diffusion, Midjourney)."
    ]
))

new_concepts.append(create_concept_obj(
    "concept_diffusion_models_math",
    "Diffusion Models from Scratch: Forward & Reverse Gaussian Markov Processes",
    t_mma_id, t_mma_label, "genai", "Transformers & Generative AI",
    "Denoising Diffusion Probabilistic Models (DDPM) generate high-fidelity synthetic data by modeling a forward Markov process that incrementally corrupts data into isotropic Gaussian noise, and training a neural UNet/DiT to reverse this process via noise prediction.",
    r"q(x_t \mid x_0) = \mathcal{N}\left(x_t; \sqrt{\bar{\alpha}_t}x_0, (1 - \bar{\alpha}_t)\mathbf{I}\right), \quad \mathcal{L}_{\text{simple}} = \mathbb{E}_{t, x_0, \epsilon}\left[\|\epsilon - \epsilon_\theta(x_t, t)\|^2\right]",
    "Reversing the thermodynamic degradation allows generating complex data distributions by iteratively subtracting predicted noise, bypassing GAN mode collapse and VAE blurriness.",
    "Generating photorealistic textile patterns, interior architectural renderings, and synthetic medical CT training scans.",
    [
        {"term": "Forward Process (Noising)", "what_is_it": "A parameter-free Markov chain that adds small Gaussian noise at each step t until the image becomes pure white noise at T=1000.", "analogy": "Dissolving a drop of food coloring in a glass of water until the water is completely uniform and cloudy.", "why_it_matters": "Enables closed-form sampling of any corrupted state x_t directly from x_0 without running t iterations."},
        {"term": "Reverse Process (Denoising)", "what_is_it": "A trained neural network (UNet or Diffusion Transformer) that estimates and subtracts the exact noise epsilon added at step t.", "analogy": "A digital artist carefully removing grain and scratches from an old photograph frame by frame.", "why_it_matters": "Transforms random Gaussian static into crisp, highly detailed images conditioned on text embeddings."}
    ],
    [
        {"symbol": "\\alpha_t, \\bar{\\alpha}_t", "meaning": "Variance schedule coefficients", "plain_english": "Fractions determining signal retention vs noise injection at step t."},
        {"symbol": "\\epsilon_\\theta(x_t, t)", "meaning": "Neural noise predictor", "plain_english": "Model output predicting the random noise vector present in x_t."}
    ],
    "At step t=500 with alpha_bar = 0.5:\nNoisy image x_500 = sqrt(0.5)*x_0 + sqrt(0.5)*noise.\nNeural network receives x_500 and t=500, predicts the noise vector, and subtracts it to reconstruct the cleaner x_499.",
    "Sampling diffusion models with full 1000 DDPM steps in real-time APIs; modern production deployments use accelerated non-Markovian solvers (DDIM, DPM-Solver++, LCM) that require only 15–25 sampling steps.",
    ["Diffusion Models", "DDPM", "Generative AI", "Markov Process", "UNet"],
    [
        "Diffusion models avoid the adversarial training instability of GANs and produce higher diversity.",
        "Classifier-Free Guidance (CFG) balances image realism against strict adherence to the conditioning text prompt.",
        "Latent Diffusion (Stable Diffusion) applies diffusion in a compressed latent space, cutting GPU VRAM requirements by 16x."
    ]
))

new_concepts.append(create_concept_obj(
    "concept_imagetoimage_fabric_transfer",
    "Image-to-Image Pipelines, Sketch-to-Image & Fabric Style Transfer",
    t_mma_id, t_mma_label, "genai", "Transformers & Generative AI",
    "Conditional generative computer vision pipelines utilizing ControlNet spatial conditioning, IP-Adapter cross-attention visual prompts, and latent neural style transfer to convert structural hand sketches into textured textile prototypes.",
    r"z_t = \text{ForwardDiffuse}(\text{VAE\_Encode}(x_{\text{init}}), t), \quad \epsilon_\theta(z_t, t, c_{\text{text}}, c_{\text{spatial}})",
    "Freezing base diffusion model weights and training zero-initialized convolution layers (ControlNet) allows incorporating explicit edge maps (Canny, HED, Depth, Pose) to lock spatial composition during generative rendering.",
    "Fashion AI Copilot allowing apparel designers to sketch a garment silhouette and generate realistic silk, denim, or tweed textile texture variations.",
    [
        {"term": "ControlNet", "what_is_it": "A neural architecture that adds spatial condition controls (sketches, depth maps, wireframes) to pre-trained text-to-image diffusion models.", "analogy": "A physical coloring book outline that dictates exactly where the artist can paint colors and textures.", "why_it_matters": "Eliminates random compositional hallucination, giving enterprise designers pixel-precise geometric control."},
        {"term": "IP-Adapter (Image Prompt Adapter)", "what_is_it": "A decoupled cross-attention mechanism that conditions diffusion models using image reference prompts rather than text.", "analogy": "Handing an interior designer a swatch of velvet fabric and saying 'Make the whole room feel like this'.", "why_it_matters": "Enables 1-shot visual style and fabric texture transfer without expensive model fine-tuning."}
    ],
    [
        {"symbol": "c_{\\text{spatial}}", "meaning": "Spatial condition conditioning tensor (Canny edges/Depth)", "plain_english": "Structural guide map extracted from designer sketch."},
        {"symbol": "\\text{DenoisingStrength}", "meaning": "Initial noise injection factor (0.0 to 1.0)", "plain_english": "Controls how much of the original sketch is preserved versus regenerated."}
    ],
    "Designer uploads hand-drawn jacket sketch. Canny edge detector extracts line contour (c_spatial). Denoising strength set to 0.75 with prompt 'vintage Italian corduroy jacket'. Model renders realistic corduroy wales matching the exact sketched seams.",
    "Setting DenoisingStrength too low (< 0.2) in Image-to-Image creates muddy noise artifacts; setting it too high (> 0.9) obliterates the original sketch geometry entirely. Optimal balance is 0.60–0.75.",
    ["ControlNet", "Image-to-Image", "Style Transfer", "Fashion AI", "Diffusion Conditioning"],
    [
        "ControlNet preserves structural line art, garment seams, and human poses with zero drift.",
        "IP-Adapter extracts visual style features from reference texture swatches and injects them via dedicated cross-attention layers.",
        "Zero-convolutions in ControlNet guarantee that initialized training starts from pristine base model capabilities."
    ]
))

new_concepts.append(create_concept_obj(
    "concept_langgraph_cyclical_state_machines",
    "LangGraph vs LangChain: State Machines, Cyclical Graphs & Checkpointing",
    t_mma_id, t_mma_label, "genai", "Transformers & Generative AI",
    "Orchestration framework comparison between classical Directed Acyclic Graph (DAG) pipelines (LangChain) and cyclical, stateful graph execution engines (LangGraph) featuring first-class multi-agent state management, checkpoint persistence, and human-in-the-loop interruptions.",
    r"\text{State}_{t+1} = \text{Node}_i(\text{State}_t), \quad \text{Branch} = \text{ConditionalEdge}(\text{State}_{t+1}) \longrightarrow \text{Node}_j \lor \text{END}",
    "Real-world agentic intelligence requires cyclical looping (reflection, self-correction, tool retries) and durable state persistence across asynchronous user approvals, which acyclic DAG chains cannot natively execute.",
    "An autonomous coding agent that writes code, runs unit tests, reads the error traceback, cyclically loops back to edit the file, and pauses for human security approval before merging to GitHub.",
    [
        {"term": "Cyclical Graph Execution", "what_is_it": "A computational architecture where nodes can route back to previously executed nodes in iterative while-loops.", "analogy": "An editor rejecting a writer's draft and sending it back for round 2 of revisions until it meets quality standards.", "why_it_matters": "Enables true self-correction, code refactoring loops, and autonomous agent reflection."},
        {"term": "State Checkpointing", "what_is_it": "Automatically saving the entire execution graph memory state to a persistent database (Postgres, Redis) at every step.", "analogy": "A video game save-point right before a dangerous boss battle.", "why_it_matters": "Enables rollbacks, multi-day long-running workflows, and human-in-the-loop pauses without in-memory state loss."}
    ],
    [
        {"symbol": "\\text{TypedDict State}", "meaning": "Shared agent memory structure", "plain_english": "Schema defining all messages, tool outputs, and execution variables accessible by graph nodes."},
        {"symbol": "\\text{interrupt\\_before}", "meaning": "Human-in-the-loop checkpoint pause", "plain_english": "Halts execution and awaits external human review before executing dangerous tools (e.g. database write)."}
    ],
    "Agent execution loop in LangGraph: Node 'GenerateSQL' produces query -> Node 'ExecuteSQL' fails with 'Table not found' -> Conditional edge routes state back to 'GenerateSQL' with error trace -> Node 'GenerateSQL' self-corrects column name -> Success -> END.",
    "Using LangChain LCEL (LangChain Expression Language) for complex autonomous agents; LCEL is strictly acyclic (DAG). Trying to build cyclical feedback loops in LCEL results in awkward recursion recursion errors.",
    ["LangGraph", "LangChain", "State Machines", "Agentic AI", "Human-in-the-Loop"],
    [
        "LangChain is ideal for linear RAG and simple chains; LangGraph is the standard for production agentic state machines.",
        "Checkpointers in LangGraph store thread states in Redis or Postgres, enabling enterprise disaster recovery.",
        "Conditional edges in LangGraph route execution dynamically based on tool output validation."
    ]
))

new_concepts.append(create_concept_obj(
    "concept_multiagent_swarms_fashion_copilot",
    "Multi-Agent Orchestration, Supervisor Swarms & Fashion AI Copilot Architecture",
    t_mma_id, t_mma_label, "genai", "Transformers & Generative AI",
    "Hierarchical multi-agent swarm architecture where a central supervisor agent coordinates specialized autonomous sub-agents (Trend Intelligence, Image Generation, Inventory Pricing) with scoped tool privileges and peer-to-peer handoffs.",
    r"\text{Decision} = \text{Supervisor}(\text{UserIntent}) \longrightarrow \{\text{Agent}_{\text{Trend}}, \text{Agent}_{\text{Design}}, \text{Agent}_{\text{Cost}}\} \longrightarrow \text{Consensus}",
    "Partitioning complex enterprise workflows across focused micro-agents with small system prompts prevents prompt bloat, eliminates context distraction, and enforces strict operational guardrails per domain.",
    "Fashion AI Copilot where a Creative Agent renders apparel designs, a Costing Agent queries ERP fabric pricing, and a Compliance Agent verifies copyright infringement.",
    [
        {"term": "Supervisor Agent Pattern", "what_is_it": "A master orchestration node that analyzes user requests, routes tasks to specialized worker agents, and synthesizes final answers.", "analogy": "A general contractor on a house build who coordinates electricians, plumbers, and carpenters.", "why_it_matters": "Prevents individual agents from drifting off-task and provides a single deterministic point of executive control."},
        {"term": "Agent Hand-off Protocol", "what_is_it": "Structured transfer of conversation control and memory context from one agent directly to another specialized agent.", "analogy": "Transferring a customer phone call from Tier 1 technical support directly to billing with the full incident file attached.", "why_it_matters": "Allows specialized models (e.g. Claude 3.5 Sonnet for code, Midjourney for design) to handle their ideal subtasks."}
    ],
    [
        {"symbol": "\\text{WorkerAgent}", "meaning": "Domain-scoped LLM instance with dedicated tools", "plain_english": "Agent restricted to specific tasks (e.g. TrendAnalysisAgent only reads social trend data)."},
        {"symbol": "\\text{Router}", "meaning": "LLM classification function", "plain_english": "Determines which worker agent should execute next based on conversation state."}
    ],
    "User prompt: 'Design a sustainable summer linen collection and calculate bill of materials cost'.\nSupervisor routes to TrendAgent (selects Mediterranean olive tones) -> routes output to DesignAgent (generates ControlNet sketches) -> routes sketches to CostingAgent (calculates $18.40/yard from ERP DB) -> Supervisor outputs unified executive summary.",
    "Creating unconstrained peer-to-peer swarms where agents converse endlessly in infinite circular arguments with no supervisor to enforce termination criteria, racking up huge API bills.",
    ["Multi-Agent Systems", "Supervisor Pattern", "Swarm Architecture", "Fashion AI", "Autonomous Agents"],
    [
        "Always implement a hard maximum recursion limit (e.g. max_iterations=15) to prevent infinite agent chatter.",
        "Give worker agents narrow, specialized tool sets to avoid tool-calling confusion and hallucinations.",
        "Log full agent execution traces to OpenTelemetry or LangSmith for enterprise auditing and failure debugging."
    ]
))

# Save concepts so far
with open('src/data/concepts.json', 'w', encoding='utf-8') as f:
    json.dump(concepts + new_concepts, f, indent=2, ensure_ascii=False)

print(f"Total concepts written so far: {len(concepts) + len(new_concepts)}")
