import conceptsData from '../data/concepts.json';

// Group concepts by topic_id for topic-scoped fallbacks
const topicToConcepts = new Map();
const conceptIdMap = new Map();
const conceptTitleMap = new Map();

for (const c of conceptsData) {
  conceptIdMap.set(c.id, c);
  conceptTitleMap.set((c.title || '').toLowerCase().trim(), c);
  if (c.raw_subtopic) conceptTitleMap.set(c.raw_subtopic.toLowerCase().trim(), c);
  if (c.raw_sub) conceptTitleMap.set(c.raw_sub.toLowerCase().trim(), c);

  const tid = c.topic_id;
  if (tid) {
    if (!topicToConcepts.has(tid)) {
      topicToConcepts.set(tid, []);
    }
    topicToConcepts.get(tid).push(c);
  }
}

// Explicit mappings for Hub nodes (Level 1) and Root (Level 0) subtopics
const hubSubtopicToConceptId = {
  // 1. Math Root
  "linear algebra": "concept_dot_product_cosine",
  "calculus & optimization": "concept_partial_derivatives",
  "probability & statistics": "concept_random_variables_variance",
  "information theory": "concept_shannon_entropy",

  // 2. Data Root
  "scrubbing & outliers": "concept_outlier_detection",
  "data scrubbing & outliers": "concept_outlier_detection",
  "data scrubbing & cleaning": "concept_deduplication",
  "scrubbing": "concept_deduplication",
  "outliers": "concept_outlier_detection",
  "imputation strategies": "concept_mean_median_impute",
  "missing value imputation": "concept_mean_median_impute",
  "feature scaling": "concept_min_max_scaling",
  "feature scaling & transformations": "concept_min_max_scaling",
  "feature engineering": "concept_feature_crosses",
  "categorical data & feature crosses": "concept_one_hot_encoding",
  "data partitioning & smote": "concept_smote_oversampling",
  "datasets, splitting & class imbalance": "concept_data_leakage_hygiene",

  // 3. Classical ML Root
  "linear regression": "concept_features_labels",
  "linear regression & core ml concepts": "concept_features_labels",
  "loss functions": "concept_squared_loss",
  "loss functions (l1, l2, mse, mae, log loss)": "concept_squared_loss",
  "gradient descent": "concept_learning_rate",
  "gradient descent & hyperparameters": "concept_learning_rate",
  "classification & sigmoid": "concept_sigmoid",
  "logistic regression & sigmoid": "concept_sigmoid",
  "regularization": "concept_l2_ridge",
  "regularization (l1 lasso & l2 ridge)": "concept_l2_ridge",
  "trees & boosting": "concept_decision_trees_splitting",
  "decision trees, random forests & xgboost": "concept_decision_trees_splitting",
  "unsupervised & clustering": "concept_k_means",
  "unsupervised learning & clustering": "concept_k_means",

  // 4. Evaluation Root
  "confusion matrix": "concept_tp_tn",
  "confusion matrix & classification metrics": "concept_tp_tn",
  "roc & pr curves": "concept_roc_curve",
  "evaluation curves: roc & pr": "concept_roc_curve",
  "bias-variance tradeoff": "concept_underfitting_bias",
  "generalization, overfitting & complexity": "concept_underfitting_bias",
  "cross-validation": "concept_stratified_kfold",

  // 5. Deep Learning Root
  "neurons & perceptrons": "artificial-neurons-perceptrons",
  "neural networks & hidden layers": "artificial-neurons-perceptrons",
  "activation functions": "relu-activation",
  "activation functions (relu, gelu, softmax)": "relu-activation",
  "backpropagation": "computational-graph",
  "backpropagation & autodiff": "computational-graph",
  "optimizers (adam, adamw)": "sgd-momentum",
  "deep learning optimizers (adam, adamw)": "sgd-momentum",
  "normalization (batchnorm, layernorm)": "dropout-regularization",
  "normalization & regularization (dropout, layernorm)": "dropout-regularization",
  "vision (cnn, vit)": "convolutions-kernels-stride-padding",
  "computer vision: cnns & vision transformers": "convolutions-kernels-stride-padding",
  "sequence models (lstm)": "recurrent-neural-networks-rnn",
  "sequence models: rnns, lstms & grus": "recurrent-neural-networks-rnn",
  "diffusion models": "variational-autoencoders-vae",
  "generative models & diffusion (ddpm)": "variational-autoencoders-vae",

  // 6. GenAI Root
  "tokenization & embeddings": "tokenizers-bpe-wordpiece-sentencepiece",
  "tokenization & vector embeddings": "tokenizers-bpe-wordpiece-sentencepiece",
  "self-attention mechanism": "query-key-value-projections",
  "self-attention & transformer core": "query-key-value-projections",
  "pre-training, sft & lora": "self-supervised-pre-training",
  "pre-training, sft & peft (lora/qlora)": "self-supervised-pre-training",
  "alignment (rlhf, dpo)": "rlhf-reinforcement-learning-human-feedback",
  "alignment: rlhf, dpo & distillation": "rlhf-reinforcement-learning-human-feedback",
  "rag ecosystem": "document-parsing-chunking",
  "retrieval-augmented generation (rag)": "document-parsing-chunking",
  "prompt engineering & agents": "in-context-learning-few-shot",
  "prompt engineering & autonomous agents": "in-context-learning-few-shot",

  // Fairness & Bias
  "fairness, types of bias & mitigation": "concept_human_cognitive_biases",
  "human & cognitive biases (reporting, historical, automation & confirmation bias)": "concept_human_cognitive_biases",
  "selection bias (coverage, non-response & sampling bias)": "concept_selection_biases",
  "group attribution bias (in-group bias & out-group homogeneity)": "concept_group_attribution_bias",
  "fairness metrics (demographic parity, equality of opportunity & counterfactual fairness)": "concept_fairness_metrics_parity",
  "algorithmic bias mitigation (mindiff & counterfactual logit pairing)": "concept_bias_mitigation_mindiff",

  // Production Data Hygiene
  "production data hygiene & engineering pitfalls": "concept_training_serving_skew_leakage",
  "training-serving skew & label leakage": "concept_training_serving_skew_leakage",
  "data slices, sliced metrics & the unicorn model antipattern": "concept_data_slices_unicorn_model",
  "static vs dynamic training & static vs dynamic inference": "concept_static_vs_dynamic_training_inference",
  "production ml pipelines, randomization & automl": "concept_production_ml_pipelines_automl",
  "big data infrastructure & distributed feature stores": "concept_big_data_feature_stores",

  // NLP Foundations
  "nlp foundations: n-grams, tokens & word2vec": "concept_tokens_tokenization",
  "tokens, tokenization (bpe, wordpiece) & vocabulary bounds": "concept_tokens_tokenization",
  "n-grams, bigrams & statistical language modeling": "concept_ngrams_language_models",
  "sparse vs dense representations & word2vec (skip-gram & cbow)": "concept_word2vec_embeddings",
  "contextual embeddings (bert, elmo) vs static word vectors": "concept_contextual_embeddings",
  "positional encodings (sinusoidal, rope & alibi)": "concept_positional_encoding_rope",

  // Transformers & Attention Deep Dive
  "transformers, attention & llm lifecycle": "concept_multihead_self_attention",
  "multi-head, multi-layer self-attention dynamics": "concept_multihead_self_attention",
  "bidirectional encoders (bert) vs unidirectional decoders (gpt)": "concept_bidirectional_vs_unidirectional",
  "the llm training lifecycle (pretraining, sft, rlhf) & local training feasibility": "concept_llm_training_lifecycle",
  "problems & failure modes with llms (hallucinations, sycophancy & prompt injection)": "concept_llm_problems_failures",
  "prompt engineering (zero-shot, one-shot, few-shot & chain-of-thought)": "concept_prompt_engineering_shots",

  // Agentic AI & Fine-Tuning
  "agentic ai, fine-tuning & application infrastructure": "concept_lora_qlora",
  "lora, qlora & parameter-efficient fine-tuning": "concept_lora_qlora",
  "model quantization dynamics (fp16, int8, int4, awq & gguf)": "concept_model_quantization",
  "fastapi production serving & streaming llm endpoints": "concept_fastapi_llm_serving",
  "langchain, langgraph (cyclical state machines) & llamaindex rag": "concept_langchain_langgraph_llamaindex",
  "agentic ai: react loops, tool calling & autonomous agent swarms": "concept_agentic_ai_react",

  // Deep Learning Foundations & Limits
  "feed forward, sequence limits & gradient dynamics": "concept_feed_forward_mlp",
  "feed forward neural networks (multilayer perceptrons & dense layers)": "concept_feed_forward_mlp",
  "recurrent neural networks (rnns) & hidden state recurrence": "concept_rnns_sequence_recurrence",
  "vanishing gradient & exploding gradient dynamics": "concept_vanishing_exploding_gradients",
  "principal component analysis (pca & dimensionality reduction)": "concept_pca_dimensionality_reduction",

  // MLOps Root
  "production ml systems & mlops": "model-registry-experiment-tracking",
  "model registry & experiment tracking (mlflow, weights & biases)": "model-registry-experiment-tracking",
  "high-throughput serving (vllm pagedattention, tensorrt-llm, onnx)": "high-throughput-serving-vllm",
  "data drift vs concept drift monitoring (psi, ks-test)": "data-drift-concept-drift-monitoring",
  "feature stores & continuous training ci/cd pipelines": "feature-stores-cicd-pipelines",
  "fairness, accountability & responsible ai auditing": "fairness-accountability-auditing",

  // Root Level 0
  "ai & machine learning universe": "concept_dot_product_cosine",
  "mathematical foundations": "concept_dot_product_cosine",
  "data engineering & preprocessing": "concept_deduplication",
  "classical ml": "concept_features_labels",
  "classical machine learning": "concept_features_labels",
  "model evaluation": "concept_tp_tn",
  "model evaluation & generalization": "concept_tp_tn",
  "deep learning": "artificial-neurons-perceptrons",
  "deep learning foundations": "artificial-neurons-perceptrons",
  "generative ai & llms": "tokenizers-bpe-wordpiece-sentencepiece",
  "transformers & generative ai": "tokenizers-bpe-wordpiece-sentencepiece",
  "mlops & production": "model-registry-experiment-tracking"
};

/**
 * Finds the corresponding concept object for a given subtopic string and optional parent topic ID.
 */
export function findConceptForSubtopic(subtopicName, parentId = null) {
  if (!subtopicName) return null;
  const sClean = subtopicName.trim().toLowerCase();

  // 1. Direct ID match
  if (conceptIdMap.has(subtopicName.trim())) {
    return conceptIdMap.get(subtopicName.trim());
  }

  // 2. Hub / Root explicit map
  if (hubSubtopicToConceptId[sClean]) {
    const cid = hubSubtopicToConceptId[sClean];
    if (conceptIdMap.has(cid)) return conceptIdMap.get(cid);
  }

  // 3. Exact title / raw_sub match
  if (conceptTitleMap.has(sClean)) {
    return conceptTitleMap.get(sClean);
  }

  // 4. Scoped to parent topic
  if (parentId && topicToConcepts.has(parentId)) {
    const list = topicToConcepts.get(parentId);
    // Substring in title
    for (const c of list) {
      const ct = (c.title || '').toLowerCase();
      if (ct.includes(sClean) || sClean.includes(ct)) {
        return c;
      }
    }
    // Word overlap in title
    const words = sClean.split(/[\s,()&]+/).filter(w => w.length > 2);
    for (const c of list) {
      const ct = (c.title || '').toLowerCase();
      for (const w of words) {
        if (ct.includes(w)) return c;
      }
    }
    if (list.length > 0) return list[0];
  }

  // 5. Global fuzzy word match across all concepts
  const words = sClean.split(/[\s,()&]+/).filter(w => w.length > 3);
  let bestConcept = null;
  let maxMatches = 0;

  for (const c of conceptsData) {
    const ct = (c.title || '').toLowerCase();
    const cdef = (c.def || '').toLowerCase();
    let matches = 0;
    for (const w of words) {
      if (ct.includes(w)) matches += 2;
      else if (cdef.includes(w)) matches += 1;
    }
    if (matches > maxMatches) {
      maxMatches = matches;
      bestConcept = c;
    }
  }

  if (bestConcept && maxMatches > 0) {
    return bestConcept;
  }

  // 6. Global fallback
  return conceptsData[0];
}

/**
 * Returns the exact target URL to redirect to the concept's full explanation page.
 */
export function getConceptRedirectUrl(subtopicName, parentId = null) {
  const concept = findConceptForSubtopic(subtopicName, parentId);
  if (concept && concept.id) {
    return `/concepts?id=${encodeURIComponent(concept.id)}`;
  }
  return `/concepts?search=${encodeURIComponent(subtopicName || '')}`;
}
