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

print("Loading existing dataset...")
with open('src/data/concepts.json', 'r', encoding='utf-8') as f:
    concepts = json.load(f)
with open('src/data/topics.json', 'r', encoding='utf-8') as f:
    topics = json.load(f)
with open('src/data/allNodes.json', 'r', encoding='utf-8') as f:
    nodes = json.load(f)
with open('src/data/interviewQuestions.json', 'r', encoding='utf-8') as f:
    interviews = json.load(f)

existing_c_ids = set(c['id'] for c in concepts)
existing_t_ids = set(t['id'] for t in topics)
existing_n_ids = set(n['id'] for n in nodes)

new_concepts = []

# ==========================================
# 1. TOPIC: ml_svm_ensembles (Category: ml)
# ==========================================
t_svm_id = "ml_svm_ensembles"
t_svm_label = "Support Vector Machines & Production Ensembles"

new_concepts.append(create_concept_obj(
    "concept_svm_max_margin",
    "Support Vector Machines (SVM & Maximum Margin Hyperplanes)",
    t_svm_id, t_svm_label, "ml", "Classical Machine Learning",
    "Support Vector Machines find the optimal hyperplane that separates classes with the maximum possible margin, relying only on critical boundary instances called support vectors.",
    r"\max_{w, b} \frac{2}{\|w\|} \quad \text{s.t.} \quad y_i(w^T x_i + b) \ge 1 \quad \forall i",
    "By maximizing the geometric margin (2/||w||), SVM minimizes the structural risk rather than empirical risk, drastically preventing overfitting on small-to-medium sized datasets.",
    "Used in multi-tenant financial fraud detection to cleanly separate fraudulent credit transfers from authentic customer behaviors.",
    [
        {"term": "Support Vector", "what_is_it": "The data points that lie closest to the decision boundary and determine the position and orientation of the separating hyperplane.", "analogy": "The fence posts that directly define the boundary line between two properties.", "why_it_matters": "All other training points can be removed without altering the final decision boundary."},
        {"term": "Margin", "what_is_it": "The perpendicular distance between the separating hyperplane and the closest data points from either class.", "analogy": "A wide median strip on a highway separating oncoming traffic lanes.", "why_it_matters": "Wider margins guarantee greater tolerance to future measurement noise and variance."}
    ],
    [
        {"symbol": "w", "meaning": "Weight vector orthogonal to the separating hyperplane", "plain_english": "Direction vector pointing perpendicular to the decision boundary."},
        {"symbol": "b", "meaning": "Bias term / intercept", "plain_english": "Shifts the hyperplane offset from the coordinate origin."},
        {"symbol": "y_i", "meaning": "Binary class label in {-1, +1}", "plain_english": "Ground truth classification sign for training sample i."}
    ],
    "Given weight vector w = [3, 4] with norm ||w|| = 5:\nGeometric margin = 2 / ||w|| = 2 / 5 = 0.4 units on either side of the separating hyperplane w^T x + b = 0.",
    "Do not train linear SVMs without standardizing feature scales; unscaled features cause the optimizer to bias the margin orientation toward high-magnitude features.",
    ["SVM", "Maximum Margin", "Support Vectors", "Convex Optimization"],
    [
        "SVM solves a convex quadratic programming problem with a guaranteed global optimum (no local minima).",
        "Only support vectors determine the decision boundary; removing non-support vectors leaves the model unchanged.",
        "Feature scaling (StandardScaler) is strictly mandatory before fitting an SVM."
    ]
))

new_concepts.append(create_concept_obj(
    "concept_kernel_trick_rbf",
    "The Kernel Trick & RBF Kernels (Non-Linear Mapping)",
    t_svm_id, t_svm_label, "ml", "Classical Machine Learning",
    "The Kernel Trick implicitly projects non-linearly separable data into an infinite-dimensional Hilbert space by computing dot products via kernel functions without ever explicitly calculating high-dimensional coordinates.",
    r"K(x_i, x_j) = \exp\left(-\gamma \|x_i - x_j\|^2\right) = \langle \phi(x_i), \phi(x_j) \rangle",
    "Enables linear decision boundaries in latent high-dimensional spaces to act as intricate, non-linear contour boundaries in the original feature space with O(N) computational complexity.",
    "Classifying genomic sequences and protein folding structures where biological interactions represent complex non-linear combinations.",
    [
        {"term": "RBF Kernel (Radial Basis Function)", "what_is_it": "A stationary kernel whose value depends only on the Euclidean distance between two feature vectors.", "analogy": "A localized spotlight centered on each training point that dims smoothly with distance.", "why_it_matters": "Can model arbitrarily complex non-linear decision boundaries with a single smoothness parameter gamma."},
        {"term": "Gamma Parameter", "what_is_it": "Controls the radius of influence of each support vector in the feature space.", "analogy": "How focused or wide a flashlight beam is.", "why_it_matters": "High gamma leads to tight localized islands (overfitting); low gamma creates overly smooth boundaries (underfitting)."}
    ],
    [
        {"symbol": "K(x_i, x_j)", "meaning": "Kernel evaluation between two input vectors", "plain_english": "Implicit inner product in higher-dimensional transformed space."},
        {"symbol": "\\gamma", "meaning": "Kernel scale parameter (1 / (2*sigma^2))", "plain_english": "Determines how fast similarity drops to zero with Euclidean distance."}
    ],
    "For x1 = [1, 2], x2 = [2, 3] with gamma = 0.5:\nSquared Euclidean distance ||x1 - x2||^2 = (1-2)^2 + (2-3)^2 = 1 + 1 = 2.\nKernel similarity K(x1, x2) = exp(-0.5 * 2) = exp(-1.0) ≈ 0.3678.",
    "Setting gamma too high turns the SVM into a lookup table where each training point forms an isolated circular decision island, completely ruining test generalization.",
    ["Kernel Trick", "RBF Kernel", "Hilbert Space", "Non-linear Separation"],
    [
        "The kernel trick avoids computing expensive or infinite-dimensional coordinate mappings phi(x).",
        "Mercer's Theorem guarantees that any positive semi-definite kernel corresponds to an inner product in some space.",
        "Always tune C and gamma jointly via grid search or Bayesian optimization."
    ]
))

new_concepts.append(create_concept_obj(
    "concept_svm_slack_soft_margin",
    "Soft-Margin Optimization & Slack Variables (C-Hyperparameter)",
    t_svm_id, t_svm_label, "ml", "Classical Machine Learning",
    "Soft-margin SVM introduces non-negative slack variables that permit controlled margin violations and misclassifications to handle overlapping distributions and noisy real-world data.",
    r"\min_{w, b, \xi} \frac{1}{2}\|w\|^2 + C \sum_{i=1}^n \xi_i \quad \text{s.t.} \quad y_i(w^T x_i + b) \ge 1 - \xi_i, \quad \xi_i \ge 0",
    "The C hyperparameter governs the bias-variance tradeoff: large C strictly penalizes slack (narrow margin, low bias, high variance), while small C tolerates violations (wide margin, high bias, low variance).",
    "Multi-tenant customer churn prediction where customer behavioral noise creates overlapping feature boundaries.",
    [
        {"term": "Slack Variable (xi_i)", "what_is_it": "A measurement of how far a training sample violates the canonical margin boundary.", "analogy": "A hall pass permitting students a specific margin of lateness without failing.", "why_it_matters": "Allows linear classifiers to remain stable when datasets contain overlapping outliers."},
        {"term": "C Parameter", "what_is_it": "The regularization constant governing the penalty weight assigned to slack violations.", "analogy": "A strict judge (high C) versus a lenient mediator (low C).", "why_it_matters": "Directly controls whether the model favors boundary simplicity or training sample accuracy."}
    ],
    [
        {"symbol": "\\xi_i", "meaning": "Slack variable for sample i", "plain_english": "0 if strictly correct; between 0 and 1 if inside margin; > 1 if misclassified."},
        {"symbol": "C", "meaning": "Slack penalty tradeoff multiplier", "plain_english": "Higher C penalizes mistakes aggressively; lower C tolerates margin intruders."}
    ],
    "Sample i has margin distance y_i(w^T x_i + b) = 0.6.\nSince the margin target is 1.0, slack xi_i = 1.0 - 0.6 = 0.4.\nWith penalty C = 10, this sample adds 10 * 0.4 = 4.0 to the overall optimization loss.",
    "Assuming C acts like an L2 penalty weight lambda: in SVM, C is inversely proportional to regularization (High C = Less Regularization, Low C = Strong Regularization).",
    ["Slack Variables", "Soft Margin", "C Hyperparameter", "Optimization"],
    [
        "Hard-margin SVM fails entirely if data is not linearly separable; soft-margin is universally used in production.",
        "Samples with xi_i > 0 are margin violators; samples with xi_i > 1 are misclassified training samples.",
        "Low C creates a wider highway that ignores small outlier rocks; High C swerves around every single pebble."
    ]
))

new_concepts.append(create_concept_obj(
    "concept_ensemble_architectures",
    "Ensemble Architectures (Voting, Bagging, Boosting & Stacking)",
    t_svm_id, t_svm_label, "ml", "Classical Machine Learning",
    "Ensemble techniques combine predictions from multiple base learners to reduce variance (Bagging), reduce bias (Boosting), or optimize diverse algorithmic hypotheses (Stacking / Voting).",
    r"\hat{y}_{\text{voting}} = \arg\max_c \sum_{m=1}^M w_m \cdot P_m(y=c|x), \quad \hat{y}_{\text{stacking}} = g\left(f_1(x), f_2(x), \dots, f_M(x)\right)",
    "Uncorrelated errors from diverse models cancel out mathematically, driving ensemble error significantly below that of any individual constituent model.",
    "Winning Kaggle competition solutions and enterprise loan approval engines combining LightGBM, CatBoost, and Logistic Regression.",
    [
        {"term": "Bagging (Bootstrap Aggregating)", "what_is_it": "Training multiple instances of the same model on random bootstrap samples with replacement and averaging predictions.", "analogy": "Asking 100 independent doctors for a diagnosis and taking the majority consensus.", "why_it_matters": "Reduces variance without increasing bias (e.g. Random Forest)."},
        {"term": "Stacking (Stacked Generalization)", "what_is_it": "Training a meta-learner (e.g., Logistic Regression) on the out-of-fold predictions of multiple base models.", "analogy": "A chief executive who weighs the recommendations of specialized department heads.", "why_it_matters": "Blends completely different model families (trees, linear, neural nets) into a unified predictor."}
    ],
    [
        {"symbol": "f_m(x)", "meaning": "Prediction of m-th base model", "plain_english": "Output generated by an individual estimator."},
        {"symbol": "g(\\cdot)", "meaning": "Meta-model combiner", "plain_english": "Higher-level model trained to combine base model outputs."},
        {"symbol": "w_m", "meaning": "Weight assigned to model m", "plain_english": "Confidence multiplier in weighted soft voting."}
    ],
    "Three models predict fraud probability: Model 1 = 0.85, Model 2 = 0.90, Model 3 = 0.40.\nSoft Voting average = (0.85 + 0.90 + 0.40) / 3 = 2.15 / 3 = 0.7167 (Final decision: Fraudulent).",
    "Stacking base model predictions on the training set directly causes massive data leakage; out-of-fold cross-validation predictions must be used to train meta-learners.",
    ["Ensembles", "Bagging", "Boosting", "Stacking", "Soft Voting"],
    [
        "Ensemble diversity is essential: combining 10 identical models yields zero variance reduction.",
        "Bagging reduces variance; Boosting reduces bias; Stacking optimizes multi-model cooperation.",
        "Soft voting (averaging probabilities) consistently outperforms hard voting (majority rule on class labels)."
    ]
))

new_concepts.append(create_concept_obj(
    "concept_scikit_joblib_multitenant",
    "Scikit-Learn, Joblib Model Serialization & Multi-Tenant Classifiers",
    t_svm_id, t_svm_label, "ml", "Classical Machine Learning",
    "Serializing fitted scikit-learn estimators and preprocessing pipelines using Joblib/pickle, and structuring multi-tenant ML inference architectures where tenant models are dynamically routed or partitioned.",
    r"\text{Latency}_{\text{infer}} = T_{\text{deserialize}} + T_{\text{pipeline\_transform}} + T_{\text{predict}} < 5\,\text{ms}",
    "Joblib employs efficient disk-to-memory memory mapping (mmap) for large NumPy weight arrays, enabling sub-millisecond model loading and zero-copy shared memory access across multi-worker server processes.",
    "A multi-tenant SaaS CRM platform maintaining 1,200 tenant-specific lead scoring models loaded on-demand via LRU memory cache.",
    [
        {"term": "Joblib Serialization", "what_is_it": "Python serialization optimized for objects containing large internal NumPy arrays.", "analogy": "Packing precision machine parts into custom pre-formed foam cases rather than generic bubble wrap.", "why_it_matters": "Loads large weight matrices up to 10x faster than standard Python pickle."},
        {"term": "Multi-Tenant Model Partitioning", "what_is_it": "Architectural strategy of training customer-specific models or prepending tenant ID embeddings to guarantee data isolation.", "analogy": "Safe deposit boxes inside a bank vault where each client has their own key and compartment.", "why_it_matters": "Prevents data leakage across enterprise clients while tailoring models to tenant-specific distributions."}
    ],
    [
        {"symbol": "\\text{dump}(model, path)", "meaning": "Joblib disk serialization", "plain_english": "Saves trained weights and preprocessors to binary storage."},
        {"symbol": "\\text{load}(path, mmap)", "meaning": "Memory-mapped loading", "plain_english": "Reads model weights into process memory with zero copy overhead."}
    ],
    "Joblib mmap benchmark: A 450 MB ensemble model loads in 18 ms via memory mapping versus 420 ms via standard uncompressed pickle deserialization.",
    "Deserializing untrusted Joblib files via joblib.load opens severe remote code execution vulnerabilities; only deserialize files signed with trusted cryptographic hashes.",
    ["Joblib", "Scikit-Learn", "Multi-Tenant", "Serialization", "Inference Latency"],
    [
        "Always serialize the complete Pipeline (imputer, scaler, encoder, classifier) together, never the classifier alone.",
        "Multi-tenant architectures should keep an LRU cache of recently queried tenant models in Redis or local RAM.",
        "Pin exact scikit-learn and NumPy versions in requirements.txt to prevent silent deserialization crashes."
    ]
))

# ==============================================================
# 2. TOPIC: dl_frameworks_cv_inference (Category: dl)
# ==============================================================
t_dlf_id = "dl_frameworks_cv_inference"
t_dlf_label = "Deep Learning Framework Internals & Real-Time CV Inference"

new_concepts.append(create_concept_obj(
    "concept_pytorch_tensorflow_internals",
    "PyTorch vs TensorFlow Execution Internals (Autograd & Dynamic Graphs)",
    t_dlf_id, t_dlf_label, "dl", "Deep Learning",
    "PyTorch operates an eager execution paradigm with reverse-mode automatic differentiation (Autograd) constructing dynamic Directed Acyclic Graphs (DAG) on the fly, contrasted with TensorFlow GraphDef static compilation and XLA kernel fusion.",
    r"y = f(x), \quad \frac{\partial \mathcal{L}}{\partial x} = \sum_{p \in \text{parents}(x)} \frac{\partial \mathcal{L}}{\partial p} \frac{\partial p}{\partial x}",
    "Dynamic tape-based computational graphs allow arbitrary Python control flow (loops, conditionals) inside neural forward passes, facilitating dynamic sequence models and fast debugging.",
    "Training generative language models and dynamic visual tree decoders where sequence lengths vary dynamically per batch element.",
    [
        {"term": "Autograd Engine", "what_is_it": "PyTorch's automatic differentiation system that records tensor operations on an execution tape to automatically backpropagate gradients.", "analogy": "A flight data recorder tracking every steering maneuver to retrace the journey backwards.", "why_it_matters": "Eliminates manual gradient calculus derivations for arbitrary multi-layer neural architectures."},
        {"term": "XLA (Accelerated Linear Algebra)", "what_is_it": "A domain-specific compiler for linear algebra that fuses consecutive operators into single GPU kernel calls.", "analogy": "Combining three separate stops at the grocery, pharmacy, and post office into one master errands drive.", "why_it_matters": "Eliminates high-overhead GPU memory read/write roundtrips, boosting throughput by 20–40%."}
    ],
    [
        {"symbol": "x.\\text{grad}", "meaning": "Accumulated gradient buffer", "plain_english": "Tensor storing the derivative dL/dx after calling .backward()."},
        {"symbol": "\\text{requires\\_grad}", "meaning": "Autograd tracking flag", "plain_english": "Boolean flag indicating whether operations on this tensor should be recorded."}
    ],
    "Forward pass: a = tensor([2.0], requires_grad=True); b = a**3 + 5.\nBackward pass: b.backward() calculates db/da = 3*a^2 = 3*(2.0^2) = 12.0.\na.grad now contains tensor([12.0]).",
    "Forgetting to call optimizer.zero_grad() causes gradients to accumulate additively across mini-batches, resulting in exploding updates.",
    ["PyTorch", "TensorFlow", "Autograd", "Dynamic Computation Graph", "XLA"],
    [
        "PyTorch constructs dynamic DAGs per iteration; TensorFlow historically used static graphs, though TF 2.x defaults to eager execution.",
        "Always call optimizer.zero_grad() before loss.backward() in standard PyTorch training loops.",
        "Wrap evaluation and inference code in with torch.no_grad(): to prevent memory leaks from unused graph allocations."
    ]
))

new_concepts.append(create_concept_obj(
    "concept_iou_map_metrics",
    "Object Detection Metrics: Intersection over Union (IoU) & mAP",
    t_dlf_id, t_dlf_label, "dl", "Deep Learning",
    "Intersection over Union (IoU) measures spatial bounding box overlap, while mean Average Precision (mAP) integrates precision-recall curves across multiple IoU thresholds (e.g. mAP@0.5, mAP@0.5:0.95) to quantify detection precision and localization accuracy.",
    r"\text{IoU} = \frac{\text{Area}(B_p \cap B_{gt})}{\text{Area}(B_p \cup B_{gt})}, \quad \text{AP} = \int_0^1 p(r) \, dr, \quad \text{mAP} = \frac{1}{C}\sum_{c=1}^C \text{AP}_c",
    "Bounding box detection requires evaluating both label classification correctness and coordinate spatial alignment simultaneously; mAP penalizes hallucinations and duplicate boxes via Non-Maximum Suppression (NMS).",
    "Evaluating autonomous driving pedestrian detectors where an IoU > 0.5 determines whether a safety collision warning is triggered.",
    [
        {"term": "Intersection over Union (IoU)", "what_is_it": "The ratio of the overlapping area between predicted and ground-truth bounding boxes to their combined union area.", "analogy": "The overlapping lens area of two pairs of spectacles held against each other.", "why_it_matters": "Determines whether an object prediction is officially categorized as a True Positive or False Positive."},
        {"term": "mAP@[.5:.95] (COCO Metric)", "what_is_it": "The average AP across 10 IoU thresholds from 0.50 to 0.95 with step size 0.05.", "analogy": "Grading an archer not just on hitting the broad target, but averaging scores across progressively tighter bullseyes.", "why_it_matters": "The gold-standard benchmark in modern computer vision competitions and industry models."}
    ],
    [
        {"symbol": "B_p, B_{gt}", "meaning": "Predicted and Ground Truth bounding boxes", "plain_english": "Coordinate rectangles [x_min, y_min, x_max, y_max]."},
        {"symbol": "\\text{AP}", "meaning": "Average Precision", "plain_english": "Area under the precision-recall curve for a specific class."}
    ],
    "Predicted box area = 100 px^2, Ground truth box area = 100 px^2, Overlapping intersection area = 60 px^2.\nUnion area = 100 + 100 - 60 = 140 px^2.\nIoU = 60 / 140 = 0.4286 (Below standard 0.5 threshold -> Classified as False Positive).",
    "Do not confuse image-level classification accuracy with object detection mAP; a model can detect all objects but suffer terrible mAP due to loose bounding box coordinates.",
    ["IoU", "mAP", "COCO Metrics", "Object Detection", "Precision-Recall"],
    [
        "IoU = 1.0 represents a perfect pixel-for-pixel bounding box alignment.",
        "Non-Maximum Suppression (NMS) removes redundant overlapping predicted boxes with IoU above a suppression threshold.",
        "COCO mAP@[.50:.95] heavily rewards models with millimeter-precise object localization."
    ]
))

new_concepts.append(create_concept_obj(
    "concept_yolo_realtime_detection",
    "YOLO Architectural Evolution & Real-Time Object Detection",
    t_dlf_id, t_dlf_label, "dl", "Deep Learning",
    "You Only Look Once (YOLO) reframes object detection as a single-stage regression problem directly from full image pixels to bounding box coordinates and class probabilities, bypassing two-stage region proposal networks (Faster R-CNN).",
    r"\mathcal{L}_{\text{YOLO}} = \lambda_{\text{coord}}\mathcal{L}_{\text{box}} + \mathcal{L}_{\text{obj}} + \lambda_{\text{noobj}}\mathcal{L}_{\text{noobj}} + \mathcal{L}_{\text{class}}",
    "By predicting detection grids and anchor-free coordinate offsets in a single forward pass, YOLO achieves ultra-fast inference speeds exceeding 100+ frames per second on commodity GPUs.",
    "Real-time retail security monitoring and inventory checkout tracking thousands of consumer goods concurrently.",
    [
        {"term": "Single-Stage Detector", "what_is_it": "An architecture that predicts object bounding boxes and category classes in a single unified neural forward pass.", "analogy": "A seasoned radar operator who spots targets instantly in a glance without taking multiple binoculars readings.", "why_it_matters": "Enables 10x higher frame rates compared to two-stage Region Proposal Networks (RPNs)."},
        {"term": "Path Aggregation Network (PANet)", "what_is_it": "A feature pyramid neck architecture that routes fine-grained low-level visual textures up to semantic high-level layers.", "analogy": "An express elevator allowing ground-floor security to send detailed visual alerts directly to top-floor command.", "why_it_matters": "Drastically improves detection accuracy for small objects and dense overlapping groups."}
    ],
    [
        {"symbol": "\\lambda_{\\text{coord}}", "meaning": "Localization loss weight multiplier", "plain_english": "Puts heavier penalty on bounding box coordinate errors than class errors."},
        {"symbol": "\\mathcal{L}_{\\text{box}}", "meaning": "Bounding box loss (CIoU / GIoU)", "plain_english": "Measures center offset, aspect ratio, and box shape alignment."}
    ],
    "YOLOv8s benchmark on NVIDIA T4 GPU: Inference latency = 8.2 ms per 640x640 frame (122 FPS) with 44.9 mAP, compared to Faster R-CNN at 65 ms (15 FPS).",
    "Training YOLO on custom datasets with small objects without adjusting the anchor strides or input resolution (640 vs 1280) causes catastrophic miss rates.",
    ["YOLO", "Single-Stage Detector", "Real-Time CV", "PANet", "CIoU Loss"],
    [
        "YOLO trades minor precision at ultra-high IoU thresholds for 10x faster real-time throughput.",
        "Modern YOLO versions (v8, v9, v10) are anchor-free, directly regressing distances from grid cells to box boundaries.",
        "Single-stage architectures are mandatory for edge robotics and video stream analytics."
    ]
))

new_concepts.append(create_concept_obj(
    "concept_onnx_runtime_quantization",
    "Real-Time Inference Optimization: ONNX Runtime & Model Quantization",
    t_dlf_id, t_dlf_label, "dl", "Deep Learning",
    "Open Neural Network Exchange (ONNX) provides an open intermediate representation format that decouples neural architectures from training frameworks, enabling graph optimization, operator fusion, and INT8/FP16 quantization.",
    r"q = \text{round}\left(\frac{r}{S}\right) + Z, \quad r \approx S \cdot (q - Z)",
    "Converting 32-bit floating point weights (FP32) to 8-bit integers (INT8) reduces memory bandwidth by 75% and utilizes specialized CPU AVX-512 / GPU Tensor Core INT8 matrix multiplication units for 3–5x speedups.",
    "Deploying visual inspection neural models on industrial edge cameras with constrained 15W TDP power budgets.",
    [
        {"term": "ONNX Runtime", "what_is_it": "A cross-platform high-performance accelerator engine that executes ONNX models using specialized hardware Execution Providers (CUDA, TensorRT, DirectML).", "analogy": "A universal high-speed train engine that runs seamlessly across any country's railway gauge.", "why_it_matters": "Delivers up to 3x lower latency compared to native PyTorch Python runtime engines."},
        {"term": "Post-Training Quantization (PTQ)", "what_is_it": "Quantizing pre-trained FP32 neural weights into INT8 using a small calibration dataset without retraining.", "analogy": "Compressing an uncompressed WAV audio file into high-bitrate MP3 with undetectable loss in audio fidelity.", "why_it_matters": "Shrinks model size by 4x instantly with under 1% drop in accuracy."}
    ],
    [
        {"symbol": "S", "meaning": "Quantization scale factor", "plain_english": "Multiplier mapping integer values back to the real floating point range."},
        {"symbol": "Z", "meaning": "Zero-point integer offset", "plain_english": "Integer representing real-number zero (handles asymmetric distributions)."}
    ],
    "FP32 ResNet-50 model size = 102 MB, P99 Latency = 32 ms.\nAfter ONNX INT8 Quantization: Model size = 26 MB (74.5% reduction), P99 Latency = 8.5 ms (3.7x faster) with 0.3% mAP variation.",
    "Quantizing sensitive attention projection layers in small LLMs without proper calibration causes severe output perplexity degradation; use mixed precision (FP16 weights + INT8 activations).",
    ["ONNX", "Quantization", "Model Compression", "Edge Inference", "TensorRT"],
    [
        "ONNX decouples model training (PyTorch) from production runtime serving (C++ ONNX Runtime).",
        "Quantization reduces memory bandwidth bottlenecks, which dominate deep learning inference latency.",
        "Static quantization calibrates scale and zero-point offline; dynamic quantization calculates scale on the fly."
    ]
))

new_concepts.append(create_concept_obj(
    "concept_deepsparse_anomaly_detection",
    "DeepSparse, Neural Sparsification & Computer Vision Anomaly Detection",
    t_dlf_id, t_dlf_label, "dl", "Deep Learning",
    "DeepSparse leverages weight pruning (sparsity) and CPU instruction sets (AVX-512 VNNI) to achieve GPU-level inference speeds on commodity x86 CPUs, combined with unsupervised visual anomaly detection (Autoencoders, PatchCore).",
    r"\text{Sparsity} = \frac{|\{w_{ij} = 0\}|}{|\{w_{ij}\}|} \ge 80\%, \quad \text{AnomalyScore}(x) = \|x - \hat{x}\|^2",
    "Unstructured and structured pruning zeroes out 75–90% of redundant neural connections; sparse computation engines bypass zero-multiply operations completely, slashing floating point FLOPs.",
    "Semiconductor wafer surface defect inspection identifying micro-scratches on high-speed factory lines without expensive industrial GPUs.",
    [
        {"term": "Neural Sparsification (Pruning)", "what_is_it": "The process of systematically setting near-zero weights in a trained neural network to zero without sacrificing task accuracy.", "analogy": "Pruning dead and non-fruitful branches from a tree to channel nutrients to the most productive limbs.", "why_it_matters": "Enables 4x–10x acceleration on specialized sparse compute engines like Neural Magic DeepSparse."},
        {"term": "PatchCore Anomaly Detection", "what_is_it": "An unsupervised visual anomaly algorithm that extracts patch-level feature memory banks to flag deviations from pristine baseline products.", "analogy": "A quality inspector who memorizes what a flawless Rolex watch looks like and immediately spots an irregular gear tooth.", "why_it_matters": "Detects novel, never-before-seen manufacturing defects with zero defect training samples."}
    ],
    [
        {"symbol": "\\text{FLOPs}", "meaning": "Floating Point Operations", "plain_english": "Total arithmetic operations executed in a single forward pass."},
        {"symbol": "\\|x - \\hat{x}\\|^2", "meaning": "Reconstruction error", "plain_english": "Pixel difference between input image and autoencoder reconstruction."}
    ],
    "Dense YOLOv8 model: 100% weights = 18 million parameters, Latency on 4-core Intel CPU = 75 ms.\n85% Sparse Pruned + DeepSparse engine: 2.7 million active weights, Latency on same 4-core CPU = 12 ms (6.2x speedup).",
    "Attempting to run sparse models on standard PyTorch runtimes yields zero speedup because standard BLAS libraries compute zero-multiplications anyway; a sparse execution engine like DeepSparse is required.",
    ["DeepSparse", "Sparsity", "Model Pruning", "Anomaly Detection", "PatchCore"],
    [
        "DeepSparse delivers GPU-class inference speeds on standard enterprise CPUs via sparse tensor execution.",
        "PatchCore achieves 99%+ Image-level AUROC on MVTec anomaly detection benchmarks using memory banks.",
        "Unsupervised anomaly detection eliminates the need for thousands of manually labeled defect examples."
    ]
))

# ==============================================================
# 3. TOPIC: genai_decoding_architectures (Category: genai)
# ==============================================================
t_gda_id = "genai_decoding_architectures"
t_gda_label = "LLM Decoding Dynamics & GPT vs Llama Architecture"

new_concepts.append(create_concept_obj(
    "concept_llm_decoding_strategies",
    "LLM Generation Decoding: Temperature, Top-K, Top-P & Repetition Penalty",
    t_gda_id, t_gda_label, "genai", "Transformers & Generative AI",
    "Autoregressive decoding strategies govern how language models sample next-token probabilities from the final vocabulary logit distribution, balancing creativity, determinism, and hallucination suppression.",
    r"P(w_i) = \frac{\exp(z_i / T)}{\sum_j \exp(z_j / T)}, \quad V^{(p)} = \left\{w \in V \mid \sum_{i=1}^k P(w_i) \le p\right\}",
    "Temperature scales the logit distribution sharpness (T->0 yields greedy argmax; T>1 flattens toward uniform randomness), while Top-P (nucleus sampling) dynamically adjusts the token pool based on cumulative probability mass.",
    "Configuring customer support chatbots at Temperature = 0.1 for deterministic policy adherence vs creative copywriting assistants at Temperature = 0.8.",
    [
        {"term": "Temperature (T)", "what_is_it": "A hyperparameter dividing logits before softmax that controls the entropy of the resulting probability distribution.", "analogy": "Thermal agitation of gas molecules: near 0°K everything freezes into a single state; at high temperatures molecules bounce everywhere.", "why_it_matters": "T=0 ensures reproducible code generation; T=0.7 fosters natural, engaging dialogue."},
        {"term": "Top-P (Nucleus Sampling)", "what_is_it": "Restricting next-token sampling to the smallest candidate set whose cumulative probability exceeds threshold p (e.g. 0.90).", "analogy": "Only inviting candidates who represent the top 90% of the applicant pool, whether that is 2 candidates or 20.", "why_it_matters": "Eliminates low-probability tail tokens that cause bizarre gibberish or hallucinations."}
    ],
    [
        {"symbol": "z_i", "meaning": "Unnormalized logit score for token i", "plain_english": "Raw linear output from the language model's final language modeling head."},
        {"symbol": "T", "meaning": "Sampling temperature", "plain_english": "Values < 1 sharpen the distribution; values > 1 flatten it."},
        {"symbol": "p", "meaning": "Nucleus probability cutoff", "plain_english": "Target cumulative probability mass threshold (typically 0.85–0.95)."}
    ],
    "Given raw logits z = [10.0, 8.0, 2.0].\nAt T = 1.0: Softmax probs = [0.875, 0.118, 0.007].\nAt T = 0.5: Logits / 0.5 = [20.0, 16.0, 4.0] -> Softmax probs = [0.982, 0.018, 0.0000003] (Greedy determinism).",
    "Setting Temperature to 0 while specifying Top-P or Top-K is redundant; Temperature = 0 forces greedy argmax selection where only the top 1 token is ever picked.",
    ["Decoding", "Temperature", "Top-P Nucleus", "Top-K", "Repetition Penalty"],
    [
        "Greedy decoding picks the single highest probability token at every step but often gets trapped in repetitive loops.",
        "Top-P dynamically expands its candidate pool for open-ended queries and narrows to 1 token when certainty is high.",
        "Repetition penalties divide logits of previously generated tokens to prevent infinite degenerative looping."
    ]
))

new_concepts.append(create_concept_obj(
    "concept_gpt_vs_llama_architecture",
    "GPT-Family vs Llama-Family Architecture (RoPE, GQA, SwiGLU & RMSNorm)",
    t_gda_id, t_gda_label, "genai", "Transformers & Generative AI",
    "Modern open-weight foundation models (Llama 2/3, Mistral) introduce four transformative architectural enhancements over classical GPT-3/4: Rotary Position Embeddings (RoPE), Grouped-Query Attention (GQA), SwiGLU activation functions, and Root Mean Square Normalization (RMSNorm).",
    r"\text{SwiGLU}(x) = \text{Swish}_\beta(x W_1) \otimes (x W_2), \quad \text{RMSNorm}(x) = \frac{x}{\sqrt{\frac{1}{d}\sum_{i=1}^d x_i^2 + \epsilon}} \odot \gamma",
    "Replacing standard Multi-Head Attention with Grouped-Query Attention reduces KV-cache memory footprints by 8x, while RMSNorm eliminates mean calculation overhead, accelerating forward pass speed by 7%.",
    "Serving 128k long-context documents using Llama-3-70B on 8x H100 GPUs with GQA enabling 4x larger batch sizes before GPU Out-of-Memory (OOM).",
    [
        {"term": "Grouped-Query Attention (GQA)", "what_is_it": "An attention design where multiple query heads share a single key-value head pair.", "analogy": "Eight project managers sharing one lead architect rather than each hiring their own duplicate architect.", "why_it_matters": "Slashes KV-cache memory consumption drastically while retaining 99% of MHA reasoning quality."},
        {"term": "RMSNorm", "what_is_it": "A simplified LayerNorm variant that scales activations purely by their root mean square without subtracting the mean.", "analogy": "Leveling the volume on a speaker by measuring overall energy without computing the baseline silence offset.", "why_it_matters": "Saves memory bandwidth and accelerates backward pass computation."}
    ],
    [
        {"symbol": "GQA", "meaning": "Grouped-Query Attention", "plain_english": "Intermediary between full MHA (high memory) and Multi-Query Attention MQA (low quality)."},
        {"symbol": "\\text{SwiGLU}", "meaning": "Swish Gated Linear Unit", "plain_english": "Non-linear feedforward activation providing smoother gradient flow."}
    ],
    "Memory comparison for 128k context on 70B model:\nFull Multi-Head Attention KV-Cache = 64 GB per sequence.\nGrouped-Query Attention (8 KV heads vs 64 Q heads) = 8 GB per sequence (87.5% memory reduction).",
    "Assuming Llama architecture supports standard sinusoidal positional embeddings; Llama requires complex complex-number rotation matrices (RoPE) to compute relative attention.",
    ["Llama Architecture", "GQA", "RoPE", "SwiGLU", "RMSNorm"],
    [
        "RoPE encodes relative position directly into key and query vectors via orthogonal 2D rotation matrices.",
        "GQA is the industry standard for foundation models in 2024–2026 (Llama-3, Mistral, Gemma, Claude 3.5).",
        "SwiGLU replaces ReLU/GELU in the MLP block, requiring 3 weight matrices instead of 2 but delivering higher accuracy per parameter."
    ]
))

new_concepts.append(create_concept_obj(
    "concept_prompting_vs_finetuning_vs_rag",
    "Decision Matrix: Prompting vs Fine-Tuning vs RAG (When to Use Which)",
    t_gda_id, t_gda_label, "genai", "Transformers & Generative AI",
    "The foundational decision framework determining whether an enterprise problem requires In-Context Prompt Engineering, Retrieval-Augmented Generation (RAG), or Parameter-Efficient Fine-Tuning (PEFT/LoRA).",
    r"\text{Total Cost} = C_{\text{precompute}} + C_{\text{storage}} + N_{\text{queries}} \cdot (C_{\text{retrieval}} + C_{\text{tokens}} + C_{\text{GPU}})",
    "RAG provides dynamic external factual grounding and source attribution; Fine-Tuning adapts linguistic style, tone, format, and vocabulary; Prompting offers zero-latency proof-of-concept iteration.",
    "An enterprise legal contract platform: using RAG to retrieve active clause precedents and a LoRA fine-tuned model to output strict legal formatting.",
    [
        {"term": "Prompt Engineering", "what_is_it": "Optimizing natural language instructions and in-context examples within the context window without updating model weights.", "analogy": "Briefing a freelance consultant with a 2-page project requirements memo.", "why_it_matters": "Zero training cost, instantaneous deployment, easiest to test and iterate."},
        {"term": "Retrieval-Augmented Generation (RAG)", "what_is_it": "Injecting relevant external factual documents dynamically into the prompt at runtime.", "analogy": "An open-book exam where the student can look up facts in the library before answering.", "why_it_matters": "The definitive solution for private, rapidly changing, or proprietary corporate facts."},
        {"term": "Fine-Tuning (SFT / LoRA)", "what_is_it": "Updating model weights on task-specific paired input-output examples.", "analogy": "Sending an employee to a 6-month specialized professional trade school.", "why_it_matters": "Teaches nuanced behavioral style, specialized domain syntax, or structured formatting."}
    ],
    [
        {"symbol": "\\text{Dynamic Knowledge}", "meaning": "Frequently updated facts", "plain_english": "RAG is mandatory; Fine-Tuning is terrible because weights become outdated instantly."},
        {"symbol": "\\text{Style / Formatting}", "meaning": "Strict output syntax constraints", "plain_english": "Fine-Tuning excels; saves prompt tokens and guarantees deterministic JSON/SQL."}
    ],
    "Enterprise Decision Matrix:\n- Need latest company facts? -> RAG (Accuracy: 95%, Up-to-date: Real-time).\n- Need model to mimic senior radiologist report tone? -> LoRA Fine-Tuning.\n- Testing a new feature idea this afternoon? -> Prompting (Cost: $0.05).",
    "Fine-tuning a base model on factual textbooks in an attempt to teach it new knowledge; foundation models hallucinate facts during fine-tuning. Use RAG for knowledge, Fine-Tuning for style.",
    ["Decision Matrix", "RAG vs Fine-Tuning", "Prompt Engineering", "Enterprise AI Strategy"],
    [
        "Rule of Thumb: Teach behavior and style with Fine-Tuning; provide facts and evidence with RAG.",
        "Combining RAG and Fine-Tuning (RAFT: Retrieval-Augmented Fine-Tuning) yields state-of-the-art enterprise results.",
        "Always prototype with prompt engineering first before investing thousands of dollars in fine-tuning."
    ]
))

new_concepts.append(create_concept_obj(
    "concept_structured_output_pydantic",
    "Structured Output Prompting: Pydantic, JSON Schema & Function Calling",
    t_gda_id, t_gda_label, "genai", "Transformers & Generative AI",
    "Constrained generation techniques that force autoregressive models to strictly adhere to formal schemas (Pydantic models, JSON Schema) using context-free grammar masking (Outlines, vLLM, Instructor) during decoding.",
    r"P(w_i) = 0 \quad \text{if } w_i \notin \text{ValidTokens}(\text{GrammarState})",
    "By masking out vocabulary logits that violate grammar syntax at every decoding step, the model mathematically cannot produce invalid commas, unclosed brackets, or invalid JSON.",
    "Automating database record insertion where LLM outputs must cleanly serialize into Pydantic models before triggering SQL executions.",
    [
        {"term": "Grammar-Constrained Decoding", "what_is_it": "Enforcing a Context-Free Grammar (CFG) at runtime by zeroing out logits of tokens that would produce invalid syntax.", "analogy": "A keyboard that physically locks all letter keys and only lets you press numbers when typing a postal code.", "why_it_matters": "Guarantees 100% syntactically valid JSON and eliminates regex parsing crashes in production."},
        {"term": "Pydantic Schema Validation", "what_is_it": "Python type-hinting library that enforces runtime data validation and parses LLM outputs into structured objects.", "analogy": "A strict bouncer checking age and dress code before allowing guests through the club door.", "why_it_matters": "Catches hallucinated fields and missing values before they reach downstream backend code."}
    ],
    [
        {"symbol": "\\text{ValidTokens}", "meaning": "Subset of vocabulary matching grammar", "plain_english": "Only tokens permitted by the current JSON syntax state."},
        {"symbol": "\\text{LogitMask}", "meaning": "Setting forbidden token logits to -inf", "plain_english": "Guarantees probability of forbidden tokens is exactly 0.0."}
    ],
    "When model outputs '{\"age\": ', the grammar engine masks out all characters except digits [0-9]. The model is physically incapable of outputting 'twenty-five' or unquoted text.",
    "Relying solely on system prompts like 'Please output valid JSON' without grammar masking; models under high load or temperature will eventually emit unparseable text.",
    ["Structured Output", "Pydantic", "JSON Schema", "Constrained Decoding", "Instructor"],
    [
        "Structured outputs transform LLMs from unpredictable text generators into deterministic enterprise microservices.",
        "Libraries like Outlines, Instructor, and guidance enforce schemas at the engine level with zero latency penalty.",
        "Always define Pydantic Field(description=...) to guide model reasoning for individual JSON attributes."
    ]
))

new_concepts.append(create_concept_obj(
    "concept_spacy_nltk_nlp_pipelines",
    "NLP Industrial Pipelines: spaCy, NLTK & Contextual Embedding Bridges",
    t_gda_id, t_gda_label, "genai", "Transformers & Generative AI",
    "Classical and hybrid natural language processing pipelines combining rule-based tokenizers, part-of-speech taggers, and Named Entity Recognition (spaCy, NLTK) with contextual neural transformer embeddings.",
    r"\text{Pipeline}(doc) = \text{ner}(\text{parser}(\text{tagger}(\text{tokenizer}(text))))",
    "Lightweight CPU-based rule pipelines execute in microseconds, providing fast PII redaction, entity chunking, and pre-filtering before invoking expensive transformer attention layers.",
    "Redacting social security numbers and customer names from healthcare support transcripts via spaCy NER before sending text to OpenAI APIs.",
    [
        {"term": "spaCy Pipeline", "what_is_it": "An industrial-grade, Cython-optimized NLP engine designed for fast production text processing and entity extraction.", "analogy": "An automated assembly line where a raw car frame passes through sequential robotic welding stations.", "why_it_matters": "Processes hundreds of thousands of words per second on single CPU cores."},
        {"term": "Named Entity Recognition (NER)", "what_is_it": "Locating and classifying named entities in unstructured text into predefined categories (Person, Organization, Date).", "analogy": "A highlighter pen that automatically marks every company name in yellow and every person in blue.", "why_it_matters": "Essential for privacy compliance (GDPR/HIPAA PII masking) and knowledge graph construction."}
    ],
    [
        {"symbol": "\\text{doc.ents}", "meaning": "Recognized entity spans in document", "plain_english": "Array of entity tokens with label annotations."},
        {"symbol": "\\text{pos\\_}", "meaning": "Part-of-speech tag", "plain_english": "Grammatical syntactic role (Noun, Verb, Adjective)."}
    ],
    "spaCy vs Transformer latency: spaCy en_core_web_sm parses 1,000 sentences in 42 ms on CPU; RoBERTa takes 1,800 ms on GPU. spaCy is 40x faster for basic entity filtering.",
    "Using heavy LLMs for simple tasks like regex phone number extraction or POS tagging; simple tasks should be routed to spaCy or regex to save thousands in cloud costs.",
    ["spaCy", "NLTK", "NER", "NLP Pipelines", "PII Redaction"],
    [
        "Use spaCy for industrial text preprocessing and privacy scrubbing; use NLTK for linguistic research and education.",
        "Combining spaCy entity extraction with Vector DB metadata filtering boosts RAG retrieval accuracy.",
        "Pre-filtering queries with classical NLP saves substantial LLM GPU inference expenditures."
    ]
))

# Save concepts so far
with open('src/data/concepts.json', 'w', encoding='utf-8') as f:
    json.dump(concepts + new_concepts, f, indent=2, ensure_ascii=False)

print(f"Total concepts written so far: {len(concepts) + len(new_concepts)}")
