# scripts/build_full_updated_dataset.py
import json

def get_realigned_concepts():
    return [
        {
            "id": "concept_autoencoders_latent_bottlenecks",
            "title": "Autoencoders & Latent Bottlenecks",
            "topic_id": "dl_foundations_limits",
            "topic_label": "Feed Forward, Sequence Limits & Gradient Dynamics",
            "category": "dl",
            "category_label": "Deep Learning Foundations",
            "raw_subtopic": "Autoencoders & Latent Bottlenecks",
            "raw_sub": "Autoencoders & Latent Bottlenecks",
            "def": "An unsupervised neural network architecture comprising an encoder that compresses high-dimensional inputs into a lower-dimensional latent bottleneck and a decoder that reconstructs the original input, forcing the network to discover compact non-linear manifold geometry.",
            "definition": "An unsupervised neural network architecture comprising an encoder that compresses high-dimensional inputs into a lower-dimensional latent bottleneck and a decoder that reconstructs the original input, forcing the network to discover compact non-linear manifold geometry.",
            "formula": "$$z = f_\\theta(x) = \\sigma(W_e x + b_e), \\quad \\hat{x} = g_\\phi(z) = \\sigma(W_d z + b_d), \\quad \\mathcal{L}(x, \\hat{x}) = \\frac{1}{2} \\|x - \\hat{x}\\|_2^2$$",
            "formula_explanation": "",
            "logic": "Unlike linear PCA which is constrained to orthogonal hyperplanes, autoencoders use non-linear activations to learn curved, complex topological manifolds in latent space.",
            "core_logic": "Unlike linear PCA which is constrained to orthogonal hyperplanes, autoencoders use non-linear activations to learn curved, complex topological manifolds in latent space.",
            "architectural_logic": "",
            "example": "Industrial anomaly detection in wafer manufacturing: An autoencoder trained solely on flawless semiconductor images yields high reconstruction error when encountering microscopic surface scratches.",
            "tags": ["Autoencoders", "Latent Space", "Dimensionality Reduction", "Unsupervised Learning"],
            "simple_summary": "An autoencoder acts like an extreme summarizer: it compresses an image or vector down through an hourglass bottleneck, then forces a decoder to reconstruct the original perfectly from that tiny summary.",
            "core_terms": [
                {
                    "term": "Encoder",
                    "what_is_it": "The contracting half of the network that maps high-dimensional input $x$ down into latent code $z$.",
                    "analogy": "A book editor condensing a 500-page manuscript into a 1-page executive summary.",
                    "why_it_matters": "Discards superficial noise and isolates the core underlying generative factors."
                },
                {
                    "term": "Latent Bottleneck",
                    "what_is_it": "The narrow central hidden layer with significantly fewer dimensions than the input.",
                    "analogy": "An hourglass neck that forces sand grains to pass in single file.",
                    "why_it_matters": "Prevents the network from simply learning an identity memorization function."
                },
                {
                    "term": "Decoder",
                    "what_is_it": "The expanding half of the network that reconstructs the input from the latent code.",
                    "analogy": "An architect sketching a complete 3D house using only the 1-page executive summary.",
                    "why_it_matters": "Verifies that the bottleneck preserved enough information to reconstruct the real data."
                },
                {
                    "term": "Reconstruction Loss",
                    "what_is_it": "The squared difference or cross-entropy between original input $x$ and reconstruction $\\hat{x}$.",
                    "analogy": "The difference score between an original painting and an apprentice's copy.",
                    "why_it_matters": "Drives backpropagation gradients without needing any human-labeled target tags."
                }
            ],
            "symbol_guide": [
                {"symbol": "x", "meaning": "High-dimensional input sample", "plain_english": "e.g. 784-pixel image"},
                {"symbol": "z", "meaning": "Compressed latent vector", "plain_english": "e.g. 16-dimensional bottleneck vector"},
                {"symbol": "\\hat{x}", "meaning": "Reconstructed output", "plain_english": "The decoder's best estimate of original x"},
                {"symbol": "W_e, W_d", "meaning": "Encoder and decoder weight matrices", "plain_english": "The learned parameters that compress and decompress"}
            ],
            "numerical_example": "Input dimension = 1,024 features. Bottleneck dimension = 32 features (96.8% compression). Encoder computes z = W_e x (size 32). Decoder computes x_hat = W_d z (size 1024). If reconstruction MSE is 0.002, the 32 numbers retained 99.8% of the information.",
            "pitfalls": "Novice Trap: If the bottleneck dimension is too large or the network has too much capacity without regularization, the autoencoder will learn the identity function (memorization) instead of meaningful feature representations.",
            "key_takeaways": [],
            "definition_bullets": [
                "Encoder: The contracting half of the network that maps high-dimensional input x down into latent code z.",
                "Latent Bottleneck: The narrow central hidden layer with significantly fewer dimensions than the input.",
                "Decoder: The expanding half of the network that reconstructs the input from the latent code.",
                "Reconstruction Loss: The squared difference or cross-entropy between original input x and reconstruction."
            ]
        },
        {
            "id": "concept_inference_acceleration_tensorrt_onnx",
            "title": "Real-Time Inference Acceleration (TensorRT, ONNX Runtime & CUDA Graphs)",
            "topic_id": "dl_frameworks_cv_inference",
            "topic_label": "Deep Learning Framework Internals & Real-Time CV Inference",
            "category": "dl",
            "category_label": "Deep Learning Foundations",
            "raw_subtopic": "Real-Time Inference Acceleration (TensorRT, ONNX Runtime & CUDA Graphs)",
            "raw_sub": "Real-Time Inference Acceleration (TensorRT, ONNX Runtime & CUDA Graphs)",
            "def": "Production optimization frameworks that lower deep learning computational graphs into target-hardware-specific execution kernels through operator fusion, dynamic INT8/FP16 quantization, memory arena reuse, and CUDA graph stream replay.",
            "definition": "Production optimization frameworks that lower deep learning computational graphs into target-hardware-specific execution kernels through operator fusion, dynamic INT8/FP16 quantization, memory arena reuse, and CUDA graph stream replay.",
            "formula": "$$\\text{Latency} = \\sum_{k=1}^K T_{\\text{fused\\_kernel}}(k) + T_{\\text{copy}} - T_{\\text{CUDA\\_graph\\_overhead}}$$",
            "formula_explanation": "",
            "logic": "Python runtime overhead and un-fused PyTorch kernel dispatches incur significant latency penalties per layer. ONNX Runtime and TensorRT fuse convolution, batchnorm, and activation into single fused GPU kernel passes.",
            "core_logic": "Python runtime overhead and un-fused PyTorch kernel dispatches incur significant latency penalties per layer. ONNX Runtime and TensorRT fuse convolution, batchnorm, and activation into single fused GPU kernel passes.",
            "architectural_logic": "",
            "example": "Autonomous driving camera perception: Lowering a 30-layer YOLO backbone from 42ms Python latency to 4.2ms GPU execution using TensorRT INT8 calibration, enabling 120 FPS real-time processing.",
            "tags": ["TensorRT", "ONNX Runtime", "CUDA Graphs", "Inference Optimization"],
            "simple_summary": "Think of PyTorch as a chef preparing each ingredient one step at a time with pauses, while TensorRT pre-bakes all operations into an ultra-fast automated assembly line that runs at maximum hardware speed.",
            "core_terms": [
                {
                    "term": "Operator Fusion",
                    "what_is_it": "Combining multiple adjacent operations (e.g. Conv + BatchNorm + ReLU) into a single GPU kernel execution.",
                    "analogy": "Drinking tea with milk and sugar mixed together instead of swallowing tea, then milk, then sugar in 3 separate trips.",
                    "why_it_matters": "Eliminates high-latency roundtrips to GPU global memory (VRAM) by keeping data in high-speed registers/SRAM."
                },
                {
                    "term": "ONNX Runtime",
                    "what_is_it": "A cross-platform inference engine that executes standard ONNX graphs with hardware execution providers (CPU, CUDA, DirectML).",
                    "analogy": "A universal video player that plays any video codec smoothly on Windows, Mac, Linux, or embedded devices.",
                    "why_it_matters": "Decouples models from PyTorch/TensorFlow, enabling lightweight production microservices without huge framework binaries."
                },
                {
                    "term": "TensorRT",
                    "what_is_it": "NVIDIA's proprietary hardware-tailored optimizer that profiles specific GPU architectures to generate optimal execution plans.",
                    "analogy": "A Formula 1 pit crew fine-tuning an engine specifically for the Monaco race track.",
                    "why_it_matters": "Achieves up to 5x-10x latency speedups on NVIDIA Tensor Cores."
                },
                {
                    "term": "CUDA Graphs",
                    "what_is_it": "A mechanism to record an entire sequence of GPU kernel launches once and replay the graph with zero CPU driver launch overhead.",
                    "analogy": "Recording a macro script on your keyboard so a 50-step sequence replays with 1 keypress.",
                    "why_it_matters": "Cuts CPU dispatch bottleneck for small models where CPU launch time exceeds actual GPU compute time."
                }
            ],
            "symbol_guide": [
                {"symbol": "T_{fused}", "meaning": "Execution time of fused kernel", "plain_english": "Time spent doing math in GPU cores"},
                {"symbol": "T_{copy}", "meaning": "Host-to-device memory transfer time", "plain_english": "PCIe bus transfer duration"},
                {"symbol": "INT8 / FP16", "meaning": "Reduced numerical precision formats", "plain_english": "8-bit integer or 16-bit float math instead of 32-bit float"}
            ],
            "numerical_example": "Standard PyTorch model: 120 separate GPU kernels taking 0.15ms each + 0.05ms CPU launch overhead each = (0.15 + 0.05) × 120 = 24.0ms. TensorRT fused engine: 18 fused kernels + CUDA Graph single replay launch = 18 × 0.18ms + 0.02ms = 3.26ms (7.3x speedup).",
            "pitfalls": "Novice Trap: Dynamic batch sizes or dynamic sequence lengths can break CUDA Graphs unless memory shapes are bounded or multiple graph instances are captured for common bucket sizes.",
            "key_takeaways": [],
            "definition_bullets": [
                "Operator Fusion: Combining multiple adjacent operations into a single GPU kernel execution.",
                "ONNX Runtime: A cross-platform inference engine that executes standard ONNX graphs with hardware execution providers.",
                "TensorRT: NVIDIA's proprietary hardware-tailored optimizer that profiles specific GPU architectures.",
                "CUDA Graphs: A mechanism to record an entire sequence of GPU kernel launches once and replay with zero CPU overhead."
            ]
        },
        {
            "id": "concept_text_preprocessing_normalization",
            "title": "Text Preprocessing, Lemmatization, Stopwords & Linguistic Normalization",
            "topic_id": "genai_nlp_foundations",
            "topic_label": "NLP Foundations: N-Grams, Tokens & Word2Vec",
            "category": "genai",
            "category_label": "Transformers & Generative AI",
            "raw_subtopic": "Text Preprocessing, Lemmatization, Stopwords & Linguistic Normalization",
            "raw_sub": "Text Preprocessing, Lemmatization, Stopwords & Linguistic Normalization",
            "def": "The foundational pipeline of transforming raw unstructured text strings into standardized linguistic units through case folding, Unicode normalization (NFC/NFKD), regex cleaning, morphological lemmatization, and selective stopword removal.",
            "definition": "The foundational pipeline of transforming raw unstructured text strings into standardized linguistic units through case folding, Unicode normalization (NFC/NFKD), regex cleaning, morphological lemmatization, and selective stopword removal.",
            "formula": "$$\\text{Doc}_{\\text{clean}} = \\text{Lemmatize}\\left(\\text{RegexFilter}\\left(\\text{UnicodeNFKD}(\\text{Doc}_{\\text{raw}})\\right)\\right) \\setminus \\mathcal{V}_{\\text{stopwords}}$$",
            "formula_explanation": "",
            "logic": "Raw text contains noise, dialectal variants, and inflectional inflections ('running', 'runs', 'ran'). Normalization collapses inflectional redundancy to a canonical vocabulary base.",
            "core_logic": "Raw text contains noise, dialectal variants, and inflectional inflections ('running', 'runs', 'ran'). Normalization collapses inflectional redundancy to a canonical vocabulary base.",
            "architectural_logic": "",
            "example": "Legal discovery search: Mapping 'contractual obligations', 'contracted', and 'contracting' to the common lemma 'contract' so semantic search surfaces all relevant clauses regardless of grammatical tense.",
            "tags": ["NLP", "Preprocessing", "Lemmatization", "Stopwords"],
            "simple_summary": "Before feeding human writing into NLP models, text preprocessing strips out weird formatting, turns words into their dictionary root forms (like turning 'mice' into 'mouse'), and cleans away filler words.",
            "core_terms": [
                {
                    "term": "Lemmatization",
                    "what_is_it": "Using linguistic vocabulary and morphological analysis to return words to their canonical dictionary lemma (e.g. 'better' -> 'good', 'was' -> 'be').",
                    "analogy": "Tracing branches of a family tree back to the common grandparent root.",
                    "why_it_matters": "Unlike crude suffix-chopping stemming (which turns 'universe' into 'univers'), lemmatization always produces real, valid root words."
                },
                {
                    "term": "Stemming",
                    "what_is_it": "Rule-based heuristic chopping of word endings (Porter/Snowball stemmers) to approximate root form.",
                    "analogy": "Using hedge clippers to cut the ends off hedges without checking the botany.",
                    "why_it_matters": "Extremely fast, but produces non-words like 'organ' from 'organization' and 'organism'."
                },
                {
                    "term": "Stopwords",
                    "what_is_it": "High-frequency syntactic glue words ('the', 'is', 'at', 'which') that carry little topical information in classic search.",
                    "analogy": "The filler words ('um', 'uh', 'like') in everyday spoken conversation.",
                    "why_it_matters": "Removing them reduces index size by 30-40% in BM25/TF-IDF (though modern LLMs keep them for full syntax)."
                },
                {
                    "term": "Unicode Normalization (NFKD)",
                    "what_is_it": "Decomposing ligature glyphs, accents, and special symbols into standard compatible ASCII/Unicode code points.",
                    "analogy": "Converting fancy calligraphy curly letters into plain typewriter alphabet.",
                    "why_it_matters": "Prevents 'café' (composed) and 'cafe\\u0301' (decomposed) from being treated as two totally different words."
                }
            ],
            "symbol_guide": [
                {"symbol": "\\mathcal{V}_{stopwords}", "meaning": "Set of stopword tokens to exclude", "plain_english": "e.g. {'the', 'a', 'in', 'on'}"},
                {"symbol": "NFKD", "meaning": "Compatibility Decomposition Normalization", "plain_english": "Standardizes accented characters and symbols"}
            ],
            "numerical_example": "Raw: 'The CEO's 3 cafes were thriving!'. Unicode/Regex: 'the ceos 3 cafes were thriving'. Stopwords removed: 'ceos 3 cafes thriving'. Lemmatized: 'ceo 3 cafe thrive'. Vocabulary size for this phrase drops from 7 tokens to 4 canonical root concepts.",
            "pitfalls": "Novice Trap: Blindly removing stopwords when training sentiment analysis models or modern LLMs. The word 'not' is on standard stopword lists, but removing it flips 'not good' into 'good', completely reversing the sentiment!",
            "key_takeaways": [],
            "definition_bullets": [
                "Lemmatization: Using linguistic vocabulary to return words to their canonical dictionary lemma.",
                "Stemming: Rule-based heuristic chopping of word endings to approximate root form.",
                "Stopwords: High-frequency syntactic glue words that carry little topical information in search.",
                "Unicode Normalization: Decomposing ligature glyphs and accents into standard compatible code points."
            ]
        },
        {
            "id": "concept_context_window_scaling_yarn",
            "title": "Context Window Scaling (YaRN, LongLoRA & StreamingLLM)",
            "topic_id": "genai_embed",
            "topic_label": "Tokenization & Vector Embeddings",
            "category": "genai",
            "category_label": "Transformers & Generative AI",
            "raw_subtopic": "Context Window Scaling (YaRN, LongLoRA & StreamingLLM)",
            "raw_sub": "Context Window Scaling (YaRN, LongLoRA & StreamingLLM)",
            "def": "Architectures and mathematical interpolation strategies that extrapolate the effective context horizon of Transformer models beyond their initial pre-training window (e.g. 4k to 128k+) through RoPE frequency scaling, shifted sparse attention, and initial token attention sinks.",
            "definition": "Architectures and mathematical interpolation strategies that extrapolate the effective context horizon of Transformer models beyond their initial pre-training window (e.g. 4k to 128k+) through RoPE frequency scaling, shifted sparse attention, and initial token attention sinks.",
            "formula": "$$\\theta_i' = \\theta_i \\cdot s^{-\\frac{2(i-1)}{d}}, \\quad \\text{YaRN: } \\lambda_i = (1 - \\alpha_i) \\frac{\\theta_i}{s} + \\alpha_i \\theta_i, \\quad \\text{Entropy Scale } t = 0.1 \\ln(s) + 1$$",
            "formula_explanation": "",
            "logic": "Direct positional extrapolation causes attention logits to explode because novel relative distances were never observed during training. YaRN interpolates high-frequency dimensions while extrapolating low frequencies to preserve local sharpness and global distance awareness.",
            "core_logic": "Direct positional extrapolation causes attention logits to explode because novel relative distances were never observed during training. YaRN interpolates high-frequency dimensions while extrapolating low frequencies to preserve local sharpness and global distance awareness.",
            "architectural_logic": "",
            "example": "Processing entire codebases: Extending a Llama-3 8B model's context from 8,192 tokens to 131,072 tokens to ingest complete git repositories and multi-file dependencies in a single inference call.",
            "tags": ["Context Window", "YaRN", "RoPE", "Long Context"],
            "simple_summary": "Transformers originally forget or break if you give them prompts longer than their training limit. Context scaling techniques gently stretch their position numbers so they can read entire books and giant codebases without retraining from scratch.",
            "core_terms": [
                {
                    "term": "RoPE Interpolation vs Extrapolation",
                    "what_is_it": "Interpolation compresses position numbers into the known training range [0, L]; extrapolation assigns brand new unobserved numbers > L.",
                    "analogy": "Fitting 100 people into an 80-seat auditorium by asking people to sit closer together (interpolation) vs making people sit outside in the rain (extrapolation).",
                    "why_it_matters": "Interpolation prevents catastrophic perplexity spikes when prompt length exceeds pre-training bounds."
                },
                {
                    "term": "YaRN (Yet another RoPE extensioN)",
                    "what_is_it": "A method that splits RoPE dimensions: high frequencies (local token grammar) stay untouched, while low frequencies (long-range topic order) are interpolated.",
                    "analogy": "Keeping the high-detail text on a road map crystal sharp, but zooming out the regional boundary scale.",
                    "why_it_matters": "Enables 128k context extension with only 400 steps of fine-tuning."
                },
                {
                    "term": "Attention Sink (StreamingLLM)",
                    "what_is_it": "The discovery that the first 4 tokens in any sequence absorb huge attention weight regardless of their semantics.",
                    "analogy": "A lightning rod on a roof that safely grounds excess electrical charge.",
                    "why_it_matters": "Keeping just the first 4 initial tokens in KV cache allows infinite-length streaming generation without memory blowup or model collapse."
                },
                {
                    "term": "LongLoRA",
                    "what_is_it": "Shifted short attention that divides long sequences into local groups and shifts them across half the heads to enable efficient fine-tuning.",
                    "analogy": "Relay race runners who only talk to their immediate handoff partners instead of yelling across the entire stadium.",
                    "why_it_matters": "Saves 70% GPU VRAM during long-context fine-tuning."
                }
            ],
            "symbol_guide": [
                {"symbol": "s", "meaning": "Context scale expansion factor", "plain_english": "e.g. s = 16 for expanding 8k to 128k context"},
                {"symbol": "\\theta_i", "meaning": "RoPE rotational frequency", "plain_english": "The angle speed for coordinate dimension i"},
                {"symbol": "t", "meaning": "Temperature entropy correction factor", "plain_english": "Calibrates softmax sharpness as context grows"}
            ],
            "numerical_example": "Original model trained on 4,096 tokens. We want to process a 65,536 token financial prospectus (scale factor s = 16). With YaRN, position 65,536 is mathematically mapped through frequency modulation back into the dynamic attention manifold, maintaining perplexity at 4.12 vs 100,000+ for raw extrapolation.",
            "pitfalls": "Novice Trap: Assuming that expanding the context window to 128k means the model will perfectly find information in the middle. Models suffer from the 'Lost in the Middle' phenomenon unless specifically fine-tuned with needle-in-a-haystack retrieval tasks.",
            "key_takeaways": [],
            "definition_bullets": [
                "RoPE Interpolation: Compresses position numbers into known training range rather than extrapolating beyond it.",
                "YaRN: Splits frequencies so local grammar stays sharp while long-range distances are smoothly scaled.",
                "Attention Sink: The initial 4 tokens absorb excess attention softmax mass, stabilizing streaming inference.",
                "LongLoRA: Shifted sparse group attention enabling long-context fine-tuning with modest GPU VRAM."
            ]
        },
        {
            "id": "concept_multimodal_tool_calling_agents",
            "title": "Multimodal Tool Calling & Vision-Language Agents",
            "topic_id": "genai_multimodal_agents",
            "topic_label": "Multimodal Foundation Models & Advanced Agentic Workflows",
            "category": "genai",
            "category_label": "Transformers & Generative AI",
            "raw_subtopic": "Multimodal Tool Calling & Vision-Language Agents",
            "raw_sub": "Multimodal Tool Calling & Vision-Language Agents",
            "def": "Autonomous agents powered by Vision-Language Models (VLMs) that perceive multi-sensory inputs (images, diagrams, video frames, audio) and dynamically generate structured API tool calls with spatial bounding coordinates to execute real-world tasks.",
            "definition": "Autonomous agents powered by Vision-Language Models (VLMs) that perceive multi-sensory inputs (images, diagrams, video frames, audio) and dynamically generate structured API tool calls with spatial bounding coordinates to execute real-world tasks.",
            "formula": "$$\\mathcal{A}_t = \\text{VLM}(\\mathcal{H}_{1:t-1}, I_{\\text{frame}}, \\Omega_{\\text{tools}}) \\implies \\text{ToolCall}(\\text{name}=\\text{\"click\"}, \\text{args}=\\{\\text{coords}: [x, y], \\text{bbox}: [y_1, x_1, y_2, x_2]\\})$$",
            "formula_explanation": "",
            "logic": "Unlike purely text-based agents, multimodal agents must ground spatial, temporal, and sensory evidence into symbolic function arguments (e.g. clicking a button at [x=450, y=720] on a browser screen).",
            "core_logic": "Unlike purely text-based agents, multimodal agents must ground spatial, temporal, and sensory evidence into symbolic function arguments (e.g. clicking a button at [x=450, y=720] on a browser screen).",
            "architectural_logic": "",
            "example": "Autonomous UI testing: An agent visually inspects a checkout webpage screenshot, detects a broken payment modal via coordinate grounding, and invokes the bug-tracker API with the exact error crop.",
            "tags": ["VLM", "Multimodal Agents", "Tool Calling", "Grounding"],
            "simple_summary": "Vision agents don't just chat about pictures—they can look at computer screens, read diagrams, find buttons by their exact pixel coordinates, and trigger real software tools and APIs to get work done.",
            "core_terms": [
                {
                    "term": "Visual Grounding",
                    "what_is_it": "The ability of a model to link specific linguistic words or user commands to precise pixel bounding box coordinates in an image.",
                    "analogy": "A person pointing their index finger directly at a specific sign on a crowded street map.",
                    "why_it_matters": "Enables the agent to know exactly where to click, tap, crop, or highlight."
                },
                {
                    "term": "Structured Multimodal Tool Calling",
                    "what_is_it": "Emitting valid JSON or Python function calls with parameters derived directly from visual perception.",
                    "analogy": "A pilot looking out the cockpit window and entering exact GPS coordinates into the autopilot computer.",
                    "why_it_matters": "Allows models to act as autonomous computer operators and robotic assistants."
                },
                {
                    "term": "Set-of-Mark (SoM) Prompting",
                    "what_is_it": "Overlaying alphanumeric labels or colored tags onto detected UI objects before feeding the image to the model.",
                    "analogy": "Numbering players on a football jersey so the coach can say 'pass to #7' instead of describing 'the guy on the left'.",
                    "why_it_matters": "Drastically boosts agent accuracy when navigating dense websites and desktop operating systems."
                },
                {
                    "term": "Sensory Feedback Loop",
                    "what_is_it": "Executing a tool action, taking a new screenshot or audio snippet of the environment, and validating if the action succeeded.",
                    "analogy": "Opening a door and looking to see if the room opened before taking a step forward.",
                    "why_it_matters": "Enables self-correction when web popups, captcha blocks, or dynamic animations alter the screen."
                }
            ],
            "symbol_guide": [
                {"symbol": "I_{frame}", "meaning": "Visual input frame/screenshot", "plain_english": "e.g. 1920x1080 screenshot image"},
                {"symbol": "\\Omega_{tools}", "meaning": "Available tool API schemas", "plain_english": "Definitions of tools the agent can invoke"},
                {"symbol": "[y_1, x_1, y_2, x_2]", "meaning": "Normalized bounding box coordinates", "plain_english": "Values from 0 to 1000 representing box corners"}
            ],
            "numerical_example": "User prompt: 'Click the checkout button'. VLM processes 1080p image with SoM. Bounding box for green button is [720, 840, 760, 960]. Center coordinate = [x=900, y=740]. Agent produces tool call: `mouse_click(x=900, y=740)`. Environment responds with confirmation screen.",
            "pitfalls": "Novice Trap: Passing huge 4K uncompressed screenshots without tiling or downsampling, which blows through model token limits and exceeds attention budget. Standard systems tile images into 336x336 patches with a downscaled global thumbnail.",
            "key_takeaways": [],
            "definition_bullets": [
                "Visual Grounding: Linking linguistic commands to precise pixel bounding box coordinates.",
                "Structured Tool Calling: Emitting valid JSON/Python function calls with visual parameter inputs.",
                "Set-of-Mark Prompting: Numbering screen elements to give the model unambiguous targeting IDs.",
                "Sensory Feedback Loop: Evaluating new screen state after tool execution to confirm success."
            ]
        },
        {
            "id": "concept_hyperparameter_tuning_bayesian",
            "title": "Hyperparameter Tuning (Grid Search, Random Search & Bayesian Optuna)",
            "topic_id": "ml_opt",
            "topic_label": "Gradient Descent & Hyperparameters",
            "category": "ml",
            "category_label": "Classical Machine Learning",
            "raw_subtopic": "Hyperparameter Tuning (Grid Search, Random Search & Bayesian Optuna)",
            "raw_sub": "Hyperparameter Tuning (Grid Search, Random Search & Bayesian Optuna)",
            "def": "Systematic algorithms for finding the optimal hyperparameter configuration $\\theta^* \\in \\Theta$ that maximizes cross-validated model performance using exhaustive grid search, probabilistic random search, or Sequential Model-Based Optimization (Bayesian TPE).",
            "definition": "Systematic algorithms for finding the optimal hyperparameter configuration $\\theta^* \\in \\Theta$ that maximizes cross-validated model performance using exhaustive grid search, probabilistic random search, or Sequential Model-Based Optimization (Bayesian TPE).",
            "formula": "$$\\theta^* = \\arg\\max_{\\theta \\in \\Theta} f(\\theta), \\quad \\text{EI}(\\theta) = \\mathbb{E}[\\max(0, f(\\theta) - f(\\theta^+))], \\quad \\text{TPE: } \\frac{p(\\theta | y < y^*)}{p(\\theta | y \\ge y^*)}$$",
            "formula_explanation": "",
            "logic": "Exhaustive grid search suffers from exponential complexity $O(k^d)$. Bayesian optimization constructs a probabilistic surrogate model of the objective function, balancing exploration of uncertain parameter spaces with exploitation of known high-reward configurations.",
            "core_logic": "Exhaustive grid search suffers from exponential complexity $O(k^d)$. Bayesian optimization constructs a probabilistic surrogate model of the objective function, balancing exploration of uncertain parameter spaces with exploitation of known high-reward configurations.",
            "architectural_logic": "",
            "example": "Tuning an XGBoost fraud pipeline: Using Optuna Tree-structured Parzen Estimator (TPE) with ASHA early stopping to discover the optimal learning rate, max_depth, and subsample in 50 trials instead of 2,000 grid iterations.",
            "tags": ["Hyperparameters", "Bayesian Optimization", "Optuna", "Model Tuning"],
            "simple_summary": "Tuning hyperparameters is like finding the perfect temperature, baking time, and flour ratio for a cake. Grid search tries every combination blindly, random search tries random guesses, and Bayesian optimization intelligently learns from each trial to guess smarter next time.",
            "core_terms": [
                {
                    "term": "Grid Search",
                    "what_is_it": "Exhaustively testing every single combination across predefined lists of hyperparameter values.",
                    "analogy": "Systematically checking every square on a chessboard one by one.",
                    "why_it_matters": "Simple and reproducible, but suffers from exponential explosion in high dimensions."
                },
                {
                    "term": "Random Search",
                    "what_is_it": "Sampling hyperparameter combinations randomly from continuous probability distributions.",
                    "analogy": "Throwing darts randomly across a target board.",
                    "why_it_matters": "Far more efficient than grid search when only a subset of hyperparameters actually impacts performance (Bengio & Bergstra, 2012)."
                },
                {
                    "term": "Bayesian Optimization (TPE)",
                    "what_is_it": "Building a probabilistic model of past trial results to calculate which unexamined configuration has the highest Expected Improvement (EI).",
                    "analogy": "A treasure hunter using metal detector readings from previous holes to decide where to dig next.",
                    "why_it_matters": "Finds near-optimal hyperparameters in 10x-50x fewer trial iterations."
                },
                {
                    "term": "Hyperband / ASHA Pruning",
                    "what_is_it": "An early-stopping algorithm that terminates unpromising trials after a few training epochs, reallocating compute to top performers.",
                    "analogy": "A talent audition where judges buzz off unconvincing singers after 10 seconds to spend more time on potential finalists.",
                    "why_it_matters": "Prevents wasting expensive GPU hours on terrible hyperparameter runs."
                }
            ],
            "symbol_guide": [
                {"symbol": "\\theta", "meaning": "Hyperparameter configuration vector", "plain_english": "e.g. {lr: 0.01, depth: 6, l2: 0.001}"},
                {"symbol": "f(\\theta)", "meaning": "Objective validation score", "plain_english": "e.g. 5-fold cross-validation ROC-AUC"},
                {"symbol": "EI(\\theta)", "meaning": "Expected Improvement", "plain_english": "How much better we expect this new guess to be"}
            ],
            "numerical_example": "Grid search over 4 learning rates, 5 tree depths, and 5 regularization values = 4 × 5 × 5 = 100 trials × 5 folds = 500 model fits (took 4.2 hours). Optuna Bayesian TPE reached a higher F1 score (0.914 vs 0.902) in only 32 trials (took 25 minutes) using ASHA early stopping.",
            "pitfalls": "Novice Trap: Tuning hyperparameters on the test set! This causes subtle data leakage and optimistic bias. Hyperparameters must strictly be evaluated using K-fold Cross-Validation or a dedicated validation split, keeping the test set locked until the very end.",
            "key_takeaways": [],
            "definition_bullets": [
                "Grid Search: Exhaustively testing every single predefined hyperparameter combination.",
                "Random Search: Sampling configurations randomly from continuous probability distributions.",
                "Bayesian Optimization: Modeling past trial history to choose parameters with highest expected improvement.",
                "Hyperband Pruning: Terminating unpromising trials early to save compute resources."
            ]
        }
    ]

print("Realigned concepts function ready.")
