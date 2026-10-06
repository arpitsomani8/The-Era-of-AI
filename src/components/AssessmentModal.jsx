import React, { useState, useMemo, useEffect } from 'react';
import { 
  X, 
  Sparkles, 
  Award, 
  Clock, 
  RotateCcw, 
  CheckCircle2, 
  AlertCircle, 
  ArrowRight, 
  Compass, 
  BookOpen, 
  FileText, 
  Layers, 
  TrendingUp, 
  BrainCircuit, 
  HelpCircle,
  Share2,
  Check
} from 'lucide-react';
import { MathText } from './KaTeXRenderer';

// 3 TARGETED EXPERIENCE TRACKS (10 QUESTIONS EACH)
export const ASSESSMENT_TRACKS = {
  '0-2': {
    id: '0-2',
    name: '0–2 Years (Freshers & Novices)',
    badge: '🌱 Novice & Fresher Track',
    badgeCls: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40',
    description: '100% intuitive, conceptual questions. Zero complex math, Hessian matrices, or calculus proofs.',
    pillars: {
      math: { label: 'Foundations & Concepts', total: 2 },
      ml: { label: 'Classical ML', total: 2 },
      dl: { label: 'Deep Learning', total: 2 },
      genai: { label: 'GenAI & LLMs', total: 4 }
    },
    questions: [
      // Pillar 1: Core Foundations (Non-Math)
      {
        id: 'b1',
        pillar: 'math',
        pillarLabel: 'Foundations & Concepts',
        question: 'What is an "Embedding" in Machine Learning and AI in simple terms?',
        options: [
          'A list of numbers (vector) that captures the semantic meaning of text or images so similar items are located close together',
          'A compressed zip archive file that stores pre-trained neural network weights on local disk',
          'An encrypted cryptographic password token used to authenticate API requests to OpenAI',
          'A specialized physical cooling chip installed inside modern GPU servers'
        ],
        correctIndex: 0,
        explanation: 'An embedding represents unstructured data (like words, sentences, or images) as a list of numbers (a vector). Items with similar meanings (such as "king" and "queen", or "cat" and "dog") end up with coordinates close to each other in vector space.'
      },
      {
        id: 'b2',
        pillar: 'math',
        pillarLabel: 'Foundations & Concepts',
        question: 'In machine learning model training, what is the fundamental purpose of a "Loss Function"?',
        options: [
          'It measures how wrong or far off the model prediction is from the actual target answer, guiding the optimizer on how to adjust weights',
          'It calculates how much computer RAM memory is lost or leaked during Python model execution',
          'It randomly discards 10% of the training dataset to prevent hard disk drives from filling up',
          'It calculates the monthly financial cloud subscription bill for GPU compute clusters'
        ],
        correctIndex: 0,
        explanation: 'The loss function acts like a scorekeeper or grading test. It calculates the error between the model prediction and the real ground-truth label. During training, the optimizer tweaks the model weights to make this loss score as small as possible.'
      },

      // Pillar 2: Classical Machine Learning
      {
        id: 'b3',
        pillar: 'ml',
        pillarLabel: 'Classical ML',
        question: 'What is the primary difference between Supervised Learning and Unsupervised Learning?',
        options: [
          'Supervised learning trains on labeled data with known correct answers, while unsupervised learning discovers patterns and groupings in unlabeled data',
          'Supervised learning requires a human data scientist to sit and observe the computer continuously while it trains',
          'Unsupervised learning can only be run on quantum supercomputers and cannot run on ordinary GPUs',
          'Supervised learning models never make mistakes or classification errors on test data'
        ],
        correctIndex: 0,
        explanation: 'In supervised learning, the model is trained with an answer key (e.g. house features paired with actual selling prices). In unsupervised learning, the algorithm is given raw data without answer labels and must discover natural clusters or patterns on its own (like customer segmentation).'
      },
      {
        id: 'b4',
        pillar: 'ml',
        pillarLabel: 'Classical ML',
        question: 'What is "Overfitting" in machine learning, and how can a developer detect it?',
        options: [
          'The model memorizes training data almost perfectly (e.g. 99% accuracy) but performs poorly on new, unseen test data',
          'The trained model weight file is too large to fit inside the computer hard drive storage',
          'The Python training script takes longer than 24 hours to finish execution',
          'The dataset contains too many duplicate columns and redundant features'
        ],
        correctIndex: 0,
        explanation: 'Overfitting happens when a model learns the random noise and specific quirks of the training data instead of general patterns. Like a student who memorizes exact practice exam answers, it scores high on training data but fails on real-world tests. A large gap between training and validation scores is the classic symptom.'
      },

      // Pillar 3: Deep Learning
      {
        id: 'b5',
        pillar: 'dl',
        pillarLabel: 'Deep Learning',
        question: 'Why is a dataset commonly split into separate Training, Validation, and Test sets?',
        options: [
          'To learn patterns on the training set, tune model hyperparameters on validation, and evaluate true real-world generalization on the unseen test set',
          'Because Python and PyTorch cannot load data files larger than 1 Gigabyte into memory at one time',
          'To ensure all customer data is permanently encrypted before feeding it to GPU workers',
          'To train three completely different models simultaneously and average their predictions together'
        ],
        correctIndex: 0,
        explanation: 'If you evaluate your model on the same data it learned from, you cannot tell if it truly learned the concept or simply memorized the answers. Keeping the test set pristine and untouched ensures an honest, unbiased evaluation of how the model will perform on future data.'
      },
      {
        id: 'b6',
        pillar: 'dl',
        pillarLabel: 'Deep Learning',
        question: 'In medical disease screening (such as cancer detection), why is a False Negative usually considered much worse than a False Positive?',
        options: [
          'A False Negative tells a sick patient they are healthy, delaying life-saving treatment, whereas a False Positive is a false alarm that can be resolved by follow-up tests',
          'A False Negative consumes double the amount of GPU electricity to calculate in software',
          'A False Positive corrupts the database tables and causes the server operating system to crash',
          'False Negatives cannot be measured or plotted on standard confusion matrix charts'
        ],
        correctIndex: 0,
        explanation: 'In medical diagnostics, missing a true positive case (a False Negative) means a patient life-threatening illness goes undetected and untreated. High Recall is prioritized here to catch as many true cases as possible, accepting a few harmless false alarms (False Positives) that can be verified later.'
      },

      // Pillar 4: GenAI & LLMs
      {
        id: 'b7',
        pillar: 'genai',
        pillarLabel: 'GenAI & LLMs',
        question: 'What is a "Token" in Large Language Models (LLMs) like ChatGPT or Claude?',
        options: [
          'A chunk of characters or word piece (roughly ~4 characters in English) that the language model reads and generates',
          'A cryptocurrency token required to pay Ethereum transaction fees for running AI queries',
          'A secret user authentication password cookie stored in the client web browser',
          'A physical networking cable connecting multiple graphics cards in an AI data center'
        ],
        correctIndex: 0,
        explanation: 'LLMs do not process text word-by-word or character-by-character; they break text into "tokens" (word pieces or subwords). In English, 1,000 tokens corresponds to roughly 750 words.'
      },
      {
        id: 'b8',
        pillar: 'genai',
        pillarLabel: 'GenAI & LLMs',
        question: 'What does "Hallucination" mean in the context of Generative AI and LLMs?',
        options: [
          'When an AI model confidently generates plausible-sounding statements that are factually incorrect or completely fabricated',
          'When a diffusion model generates colorful optical illusions and surreal psychedelic pictures',
          'When GPU hardware runs too hot and causes floating-point calculation errors',
          'When the training dataset contains voice recordings of multiple human speakers'
        ],
        correctIndex: 0,
        explanation: 'Because LLMs generate text by predicting which words are statistically likely to come next, they can produce articulate, convincing explanations that contain completely invented facts, nonexistent citations, or fake quotes.'
      },
      {
        id: 'b9',
        pillar: 'genai',
        pillarLabel: 'GenAI & LLMs',
        question: 'What is Retrieval-Augmented Generation (RAG) and why is it so widely adopted in AI products?',
        options: [
          'It searches and retrieves relevant facts from external documents and feeds them to the LLM so it answers with accurate, verified information',
          'It retrains the entire foundation model from scratch every time a user submits a prompt',
          'It automatically translates English user prompts into Python programming code',
          'It compresses large image and video files into tiny text files to save storage bandwidth'
        ],
        correctIndex: 0,
        explanation: 'RAG connects an LLM to external knowledge (such as company PDFs, docs, or databases). When a user asks a question, the system retrieves relevant snippets and includes them in the prompt. This prevents hallucinations and keeps the AI up-to-date without costly model retraining.'
      },
      {
        id: 'b10',
        pillar: 'genai',
        pillarLabel: 'GenAI & LLMs',
        question: 'What is the main difference between Prompt Engineering and Fine-Tuning an AI model?',
        options: [
          'Prompt Engineering guides the model using instructions and examples in the prompt without modifying weights, while Fine-Tuning trains and updates the model internal weights on specialized datasets',
          'Prompt Engineering requires modifying the PyTorch C++ engine, while Fine-Tuning is performed in spreadsheets',
          'Fine-Tuning is completely free and instant, while Prompt Engineering costs millions of dollars in compute',
          'There is no difference; they are two marketing terms for the exact same technical procedure'
        ],
        correctIndex: 0,
        explanation: 'Prompt Engineering directs the existing model through clever instructions, system personas, and few-shot formatting within the context window. Fine-Tuning takes an existing model and runs gradient descent on thousands of labeled domain examples to permanently change its internal parameters.'
      }
    ]
  },

  '2-4': {
    id: '2-4',
    name: '2–4 Years (Mid-Level Engineers)',
    badge: '🚀 Mid-Level Track',
    badgeCls: 'bg-blue-500/20 text-blue-300 border-blue-500/40',
    description: 'Applied machine learning, transformer mechanics, vector search, and production tradeoffs.',
    pillars: {
      math: { label: 'Loss & Optimization', total: 2 },
      ml: { label: 'Applied ML & Ensembles', total: 2 },
      dl: { label: 'Deep Learning & Normalization', total: 2 },
      genai: { label: 'GenAI, KV-Cache & RAG', total: 4 }
    },
    questions: [
      {
        id: 'm1',
        pillar: 'math',
        pillarLabel: 'Loss & Optimization',
        question: 'Why is Cross-Entropy loss preferred over Mean Squared Error (MSE) for multi-class classification with Softmax outputs?',
        options: [
          'Cross-Entropy avoids vanishing gradients when softmax predictions are confidently wrong, whereas MSE gradients saturate near zero',
          'Cross-Entropy is computationally faster because it never calculates logarithms',
          'MSE produces unbounded negative infinite loss values for probabilities between 0 and 1',
          'Softmax outputs cannot mathematically be evaluated with Euclidean distance'
        ],
        correctIndex: 0,
        explanation: 'When using MSE with Softmax, if the model predicts near 0 for the correct class, the derivative of Softmax approaches 0, causing the gradient to vanish and halting learning. Cross-Entropy derivative cancels this saturation factor, producing a gradient directly proportional to prediction error (p - y).'
      },
      {
        id: 'm2',
        pillar: 'math',
        pillarLabel: 'Loss & Optimization',
        question: 'Why is Learning Rate Warm-Up used when training Transformer architectures with AdamW?',
        options: [
          'Early in training, random weights produce erratic gradients that would cause Adam second-moment estimates to diverge without a gradual ramp-up',
          'To give GPU cooling systems enough time to reach steady operating temperatures',
          'Because weight decay cannot be applied during the first 1,000 steps of training',
          'To prevent input embedding lookup tables from overflowing integer limits'
        ],
        correctIndex: 0,
        explanation: 'At the start of training, model weights are random and gradients have high variance. If high learning rates are used immediately, Adam running variance estimates get corrupted by early outliers. Warming up the learning rate from 0 allows the moving averages to stabilize before taking large optimizer steps.'
      },
      {
        id: 'm3',
        pillar: 'ml',
        pillarLabel: 'Applied ML & Ensembles',
        question: 'How does a Random Forest reduce model error compared to an individual Decision Tree?',
        options: [
          'It trains multiple deep, high-variance trees on bootstrap samples with random feature subsets, reducing variance through ensemble averaging without increasing bias',
          'It forces all individual trees to have identical split decisions across all nodes',
          'It applies second-order gradient descent to iteratively reweight misclassified training rows',
          'It eliminates the need for any cross-validation or hyperparameter tuning'
        ],
        correctIndex: 0,
        explanation: 'An individual decision tree is prone to high variance (overfitting). Random Forest uses Bagging (Bootstrap Aggregation) + feature sub-sampling to build decorrelated trees. Averaging N decorrelated models reduces variance by approximately 1/N while preserving the low bias of deep trees.'
      },
      {
        id: 'm4',
        pillar: 'ml',
        pillarLabel: 'Applied ML & Ensembles',
        question: 'On an imbalanced fraud detection dataset (99.9% legit, 0.1% fraud), why is raw Accuracy a misleading evaluation metric?',
        options: [
          'A trivial baseline model that classifies every transaction as "legit" achieves 99.9% accuracy while detecting 0 fraud cases',
          'Accuracy cannot be calculated when the number of samples exceeds 10,000',
          'Accuracy is mathematically undefined whenever any class has less than 1% representation',
          'Accuracy gives equal weight to false alarms and undetected frauds'
        ],
        correctIndex: 0,
        explanation: 'With severe class imbalance, high accuracy is trivially obtained by predicting the majority class for everything. In fraud detection, catching the positive cases (Recall) and minimizing false accusations (Precision) are what matter, making PR-AUC and F1-score far more meaningful.'
      },
      {
        id: 'm5',
        pillar: 'dl',
        pillarLabel: 'Deep Learning & Normalization',
        question: 'Why is Layer Normalization (LayerNorm) universally preferred over Batch Normalization in autoregressive Transformers?',
        options: [
          'LayerNorm normalizes across the feature dimension independently per token, avoiding cross-batch dependencies that fail on variable-length sequences and batch size 1 inference',
          'Batch Normalization requires twice as many trainable floating-point parameters as LayerNorm',
          'LayerNorm converts all negative activation values into exact zeros like ReLU',
          'Batch Normalization cannot be computed on modern NVIDIA GPU architectures'
        ],
        correctIndex: 0,
        explanation: 'Batch Normalization calculates statistics across the batch dimension, which causes severe issues when sentence lengths vary, when sequences are generated autoregressively one token at a time, or during distributed training with small mini-batches. LayerNorm computes mean and variance across the hidden features of each individual token.'
      },
      {
        id: 'm6',
        pillar: 'dl',
        pillarLabel: 'Deep Learning & Normalization',
        question: 'What is "Teacher Forcing" during recurrent/autoregressive sequence model training?',
        options: [
          'Feeding the true ground-truth previous token as input to the next step during training, rather than the model own sampled output',
          'Distilling knowledge from a larger teacher model (e.g. 70B) into a smaller student model (e.g. 7B)',
          'Freezing all hidden layers and only updating the final linear classification head',
          'Forcing the learning rate to decay whenever validation loss plateaus'
        ],
        correctIndex: 0,
        explanation: 'In Teacher Forcing, during training the model is fed the actual ground truth previous token from the training text, rather than its own prediction. This prevents early prediction errors from compounding down the sequence, stabilizing and speeding up training convergence.'
      },
      {
        id: 'm7',
        pillar: 'genai',
        pillarLabel: 'GenAI, KV-Cache & RAG',
        question: 'In Vector Databases, why do production search engines use Approximate Nearest Neighbors (ANN, like HNSW) instead of Exact kNN search?',
        options: [
          'HNSW provides sub-linear O(log N) query search time by sacrificing 1–2% recall compared to exhaustive O(N) brute-force distance calculations across millions of vectors',
          'Exact kNN cannot measure cosine similarity or dot product distances between float vectors',
          'HNSW stores vector data on CPU RAM instead of GPU VRAM',
          'ANN algorithms eliminate the need for embedding dimension reduction'
        ],
        correctIndex: 0,
        explanation: 'Exhaustive exact kNN compares the query vector to every single document vector in the database (O(N)). When scaling to tens of millions of documents, this takes hundreds of milliseconds. Hierarchical Navigable Small World (HNSW) graphs navigate a multi-layer index in O(log N) time with >98% recall accuracy.'
      },
      {
        id: 'm8',
        pillar: 'genai',
        pillarLabel: 'GenAI, KV-Cache & RAG',
        question: 'What is the primary function of the KV-Cache in LLM autoregressive inference?',
        options: [
          'It caches the computed Key and Value projection vectors of previous tokens so they do not need to be recomputed at every newly generated token step',
          'It stores popular user prompts in Redis to serve identical answers instantly',
          'It quantizes 16-bit floating point model weights down to 4-bit integers',
          'It prevents prompt injection attacks by filtering malicious input tokens'
        ],
        correctIndex: 0,
        explanation: 'During autoregressive text generation, predicting each new token requires attending to all prior tokens. Without KV caching, the model would re-evaluate the full attention matrix for the entire prompt on every single token (O(N^2) FLOPs). KV-Cache retains prior Key and Value vectors, reducing each step to an O(N) vector-matrix multiplication.'
      },
      {
        id: 'm9',
        pillar: 'genai',
        pillarLabel: 'GenAI, KV-Cache & RAG',
        question: 'Why does weight quantization (e.g. FP16 to INT8 or INT4) significantly speed up LLM token generation throughput?',
        options: [
          'Autoregressive generation is memory-bandwidth bound; smaller weights cut the gigabytes of data transferred from GPU VRAM to compute cores per token in half',
          'Integer arithmetic eliminates the need for positional encodings and layer normalization',
          'INT4 weights automatically compress context window lengths by 4x',
          'Quantization removes all multi-head attention layers and replaces them with feedforward nets'
        ],
        correctIndex: 0,
        explanation: 'Generating text one token at a time requires loading all model parameters from High Bandwidth Memory (HBM) into SRAM for every single token. The GPU compute cores sit idle waiting for memory transfer. Reducing weights from 16-bit to 4-bit cuts memory transfer requirements by 4x, directly speeding up generation.'
      },
      {
        id: 'm10',
        pillar: 'genai',
        pillarLabel: 'GenAI, KV-Cache & RAG',
        question: 'In production RAG systems, why is Semantic Chunking often preferred over naive fixed-character chunking (e.g. 500 characters)?',
        options: [
          'It splits documents at natural semantic boundaries (paragraphs, headings, complete thoughts), preventing context fragmentation and split sentences',
          'It reduces vector embedding dimensions from 1536 to 384 automatically',
          'It encrypts private company data before it is ingested into the vector database',
          'Naive fixed-character chunking cannot be processed by OpenAI embedding models'
        ],
        correctIndex: 0,
        explanation: 'Naive chunking slices text strictly by character or word count, frequently severing sentences, code snippets, or coherent arguments in half. Semantic chunking evaluates sentence transitions, paragraph breaks, or markdown headers to ensure each retrieved chunk is a self-contained, semantically complete unit.'
      }
    ]
  },

  '5+': {
    id: '5+',
    name: '5+ Years (Senior / Staff / Quant)',
    badge: '🏛️ Senior & Staff Track',
    badgeCls: 'bg-purple-500/20 text-purple-300 border-purple-500/40',
    description: 'Rigorous optimization, GPU memory bandwidth, mathematical derivations, and architecture proofs.',
    pillars: {
      math: { label: 'Math & Optimization', total: 2 },
      ml: { label: 'Classical ML & Bounds', total: 2 },
      dl: { label: 'Deep Learning & IO', total: 2 },
      genai: { label: 'GenAI, LoRA & Scaling', total: 4 }
    },
    questions: [
      {
        id: 's1',
        pillar: 'math',
        pillarLabel: 'Math & Optimization',
        question: 'Why does Scaled Dot-Product Attention divide the query-key dot product by $\\sqrt{d_k}$?',
        options: [
          'To ensure the attention matrix has zero mean and unit variance',
          'To prevent the dot products from growing excessively large, which pushes softmax into regions with vanishing gradients',
          'To enforce symmetric attention weights between query and key tokens',
          'To reduce memory footprint in GPU High Bandwidth Memory'
        ],
        correctIndex: 1,
        explanation: 'If components of $q$ and $k$ are independent variables with mean 0 and variance 1, their dot product has mean 0 and variance $d_k$. For large dimensions (e.g. $d_k = 128$), magnitudes grow into hundreds, saturating softmax into a one-hot distribution where gradients vanish. Dividing by $\\sqrt{d_k}$ stabilizes variance to 1.0.'
      },
      {
        id: 's2',
        pillar: 'math',
        pillarLabel: 'Math & Optimization',
        question: 'In L1 regularization (Lasso), why does the penalty produce sparse parameter weights (exact zeros), whereas L2 (Ridge) does not?',
        options: [
          'L1 penalty has a constant non-zero subgradient at the origin, creating sharp diamond-shaped contour corners on coordinate axes',
          'L1 regularization penalizes large weights with squared exponential force',
          'L1 penalty introduces momentum that forces oscillating parameters to zero',
          'L1 loss is strictly non-convex, leading to multiple saddle points'
        ],
        correctIndex: 0,
        explanation: 'L1 regularization penalty $\\lambda \\sum |w_i|$ has a constant derivative $\\pm \\lambda$ regardless of how small $|w_i|$ is. Geometrically, its diamond constraint boundary has sharp corners on the coordinate axes where the loss contours intersect, setting coefficients to exact zero.'
      },
      {
        id: 's3',
        pillar: 'ml',
        pillarLabel: 'Classical ML & Bounds',
        question: 'When evaluating a model on an imbalanced dataset (e.g., 99% negative, 1% positive), why is the Precision-Recall (PR) AUC preferred over ROC AUC?',
        options: [
          'PR AUC evaluates True Positives against False Negatives rather than True Negatives, avoiding distortion from massive True Negative counts',
          'ROC AUC cannot be computed when the class imbalance ratio exceeds 10:1',
          'PR AUC is insensitive to probability threshold calibration',
          'Precision and Recall are always monotonic functions of one another'
        ],
        correctIndex: 0,
        explanation: 'The False Positive Rate in ROC is $\\text{FPR} = \\frac{\\text{FP}}{\\text{FP} + \\text{TN}}$. With a massive number of negative samples, large absolute False Positives still produce a tiny FPR, creating an illusion of high performance. PR curves omit True Negatives entirely.'
      },
      {
        id: 's4',
        pillar: 'ml',
        pillarLabel: 'Classical ML & Bounds',
        question: 'How does XGBoost prevent overfitting in deep gradient boosted decision trees compared to standard Gradient Boosting Machines (GBM)?',
        options: [
          'Uses second-order Taylor expansion (Hessian) and explicit L1/L2 leaf weight regularization penalty',
          'Eliminates all negative leaf weights via ReLU post-processing',
          'Replaces decision trees with randomized linear perceptrons',
          'Forces all boosting iterations to have equal learning rate weights'
        ],
        correctIndex: 0,
        explanation: 'XGBoost uses a 2nd-order Taylor expansion of the loss function incorporating both gradients $g_i$ and Hessians $h_i$, plus an objective penalty $\\gamma T + \\frac{1}{2}\\lambda \\sum w_j^2$ on leaf counts and weights.'
      },
      {
        id: 's5',
        pillar: 'dl',
        pillarLabel: 'Deep Learning & IO',
        question: 'Why do modern LLM architectures (e.g., LLaMA, GPT-4) use RMSNorm or Pre-LayerNorm instead of Post-LayerNorm?',
        options: [
          'Pre-LayerNorm maintains an uncorrupted residual identity path, enabling stable gradient backpropagation without warm-up instability',
          'Post-LayerNorm requires twice as many trainable affine scale parameters',
          'RMSNorm computes covariance matrices across channels, improving spatial invariance',
          'Pre-LayerNorm eliminates the need for non-linear activation functions'
        ],
        correctIndex: 0,
        explanation: 'In Pre-LN ($x + F(\\text{Norm}(x))$), the clean skip connection $x$ is preserved end-to-end, preventing gradients from decaying or exploding through layer norms during early training iterations.'
      },
      {
        id: 's6',
        pillar: 'dl',
        pillarLabel: 'Deep Learning & IO',
        question: 'What is the primary computational bottleneck of standard self-attention on modern GPU hardware (e.g., A100 / H100)?',
        options: [
          'Memory bandwidth bound: transferring $O(N^2)$ attention matrices between slow HBM and fast SRAM',
          'Compute bound: floating-point matrix multiplications (FLOPs) exceed Tensor Core throughput',
          'Cache thrashing in L2 CPU cache during PyTorch autograd tracing',
          'PCIe bus transfer latency between CPU host and GPU device'
        ],
        correctIndex: 0,
        explanation: 'Standard attention is memory-bandwidth bound. GPUs spend over 80% of time waiting for High Bandwidth Memory (HBM, 2 TB/s) reads/writes of the $N \\times N$ matrix, while SRAM (19 TB/s) compute units sit idle. FlashAttention resolves this via block tiling.'
      },
      {
        id: 's7',
        pillar: 'genai',
        pillarLabel: 'GenAI, LoRA & Scaling',
        question: 'In LoRA (Low-Rank Adaptation), how does rank decomposition parameterize the weight update $\\Delta W$?',
        options: [
          '$\\Delta W = \\frac{\\alpha}{r} (B \\times A)$ where $B \\in \\mathbb{R}^{d \\times r}$ and $A \\in \\mathbb{R}^{r \\times k}$ with $r \\ll \\min(d, k)$',
          '$\\Delta W = W_0 \\odot \\text{Dropout}(p)$',
          '$\\Delta W = \\text{SVD}(W_0)$ retaining top $r$ singular values',
          '$\\Delta W = B + A$ where $B$ is sparse and $A$ is dense'
        ],
        correctIndex: 0,
        explanation: 'LoRA freezes $W_0$ and trains two low-rank matrices $B$ and $A$. With $r = 8$ or $16$, trainable parameters drop by $10,000\\times$, and during inference, $\\Delta W$ can be pre-merged directly into $W_0 = W_0 + \\Delta W$ with 0 extra latency.'
      },
      {
        id: 's8',
        pillar: 'genai',
        pillarLabel: 'GenAI, LoRA & Scaling',
        question: 'What is the function of the auxiliary load balancing loss in Mixture-of-Experts (MoE) models (e.g. Mixtral 8x7B)?',
        options: [
          'Prevents router collapse by encouraging uniform token distribution across all $N$ expert networks',
          'Minimizes floating-point quantization errors in 4-bit weights',
          'Enforces orthogonality between expert attention matrices',
          'Aligns model outputs with human preference feedback (RLHF)'
        ],
        correctIndex: 0,
        explanation: 'Without load balancing loss ($\\alpha N \\sum f_i P_i$), the gating router quickly develops a self-reinforcing bias toward a few popular experts, starving other experts of gradient updates and causing severe distributed pipeline bottlenecks.'
      },
      {
        id: 's9',
        pillar: 'genai',
        pillarLabel: 'GenAI, LoRA & Scaling',
        question: 'Why does RoPE (Rotary Position Embedding) outperform absolute sinusoidal position embeddings for long-context extrapolation?',
        options: [
          'It encodes relative token distances purely as complex planar rotations ($q_m^T k_n = g(x_m, x_n, m-n)$) via inner products',
          'It eliminates positional information from value vectors $V$',
          'It multiplies attention weights by static exponential decay masks',
          'It stores a discrete lookup table for every possible context length'
        ],
        correctIndex: 0,
        explanation: 'RoPE applies an orthogonal rotation matrix $R_{\\Theta, m}^d$ to queries and keys. The inner product $(R_m q)^T (R_n k)$ depends exclusively on relative distance $(m - n)$, preserving shift invariance and enabling context extension methods like YaRN.'
      },
      {
        id: 's10',
        pillar: 'genai',
        pillarLabel: 'GenAI, LoRA & Scaling',
        question: 'In Retrieval-Augmented Generation (RAG), what is the primary role of a Cross-Encoder Re-ranker following dense vector search?',
        options: [
          'Jointly attends to Query and Candidate Document tokens simultaneously, capturing deep cross-attention semantics that bi-encoder cosine search misses',
          'Compresses retrieved passage tokens into 8-bit quantized embeddings',
          'Generates synthetic hypothetical documents to augment query vectors (HyDE)',
          'Computes sparse BM25 inverted indexes in local cache'
        ],
        correctIndex: 0,
        explanation: 'Bi-encoders embed query and document independently, missing rich token-to-token cross-attention interactions. A cross-encoder takes $(Query, Document)$ into a single self-attention sequence, dramatically boosting top-1 accuracy.'
      }
    ]
  }
};

export default function AssessmentModal({ isOpen, onClose }) {
  const [activeTrack, setActiveTrack] = useState('0-2'); // '0-2', '2-4', '5+'
  const [currentIdx, setCurrentIdx] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState({}); // { [questionId]: optionIndex }
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [timeLeft, setTimeLeft] = useState(600); // 10 minutes (600s)
  const [copiedResult, setCopiedResult] = useState(false);

  const currentTrackConfig = ASSESSMENT_TRACKS[activeTrack] || ASSESSMENT_TRACKS['0-2'];
  const questions = currentTrackConfig.questions;

  // Timer countdown
  useEffect(() => {
    if (!isOpen || isSubmitted) return;
    const timer = setInterval(() => {
      setTimeLeft(prev => {
        if (prev <= 1) {
          setIsSubmitted(true);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
    return () => clearInterval(timer);
  }, [isOpen, isSubmitted]);

  // Handle Track Switching
  const handleSwitchTrack = (trackId) => {
    if (trackId === activeTrack) return;
    setActiveTrack(trackId);
    setSelectedAnswers({});
    setCurrentIdx(0);
    setIsSubmitted(false);
    setTimeLeft(600);
  };

  // Pillar Scores Breakdown
  const scores = useMemo(() => {
    const trackPillars = currentTrackConfig.pillars;
    const pillars = {
      math: { label: trackPillars.math.label, correct: 0, total: trackPillars.math.total },
      ml: { label: trackPillars.ml.label, correct: 0, total: trackPillars.ml.total },
      dl: { label: trackPillars.dl.label, correct: 0, total: trackPillars.dl.total },
      genai: { label: trackPillars.genai.label, correct: 0, total: trackPillars.genai.total }
    };

    let totalCorrect = 0;
    questions.forEach(q => {
      if (selectedAnswers[q.id] === q.correctIndex) {
        totalCorrect++;
        if (pillars[q.pillar]) pillars[q.pillar].correct++;
      }
    });

    const percent = Math.round((totalCorrect / questions.length) * 100);

    let tier = 'Aspiring AI Builder';
    let tierColor = 'text-cyan-400';
    let tierBadge = 'bg-cyan-500/20 text-cyan-300 border-cyan-500/40';

    if (activeTrack === '0-2') {
      if (percent >= 90) {
        tier = 'Interview Ready (Entry-Level AI / Data)';
        tierColor = 'text-emerald-400';
        tierBadge = 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40';
      } else if (percent >= 70) {
        tier = 'Promising Novice (Strong Core Intuition)';
        tierColor = 'text-teal-400';
        tierBadge = 'bg-teal-500/20 text-teal-300 border-teal-500/40';
      } else if (percent >= 50) {
        tier = 'Developing Beginner (Review Core Concepts)';
        tierColor = 'text-amber-400';
        tierBadge = 'bg-amber-500/20 text-amber-300 border-amber-500/40';
      } else {
        tier = 'Foundations In Progress';
        tierColor = 'text-rose-400';
        tierBadge = 'bg-rose-500/20 text-rose-300 border-rose-500/40';
      }
    } else if (activeTrack === '2-4') {
      if (percent >= 90) {
        tier = 'Production-Ready Applied ML Engineer';
        tierColor = 'text-blue-400';
        tierBadge = 'bg-blue-500/20 text-blue-300 border-blue-500/40';
      } else if (percent >= 70) {
        tier = 'Solid Mid-Level Systems Practitioner';
        tierColor = 'text-indigo-400';
        tierBadge = 'bg-indigo-500/20 text-indigo-300 border-indigo-500/40';
      } else if (percent >= 50) {
        tier = 'Emerging Systems Builder';
        tierColor = 'text-amber-400';
        tierBadge = 'bg-amber-500/20 text-amber-300 border-amber-500/40';
      } else {
        tier = 'Applied Foundations Review Needed';
        tierColor = 'text-rose-400';
        tierBadge = 'bg-rose-500/20 text-rose-300 border-rose-500/40';
      }
    } else {
      if (percent >= 90) {
        tier = 'Principal Research / Staff AI Engineer';
        tierColor = 'text-purple-400';
        tierBadge = 'bg-purple-500/20 text-purple-300 border-purple-500/40';
      } else if (percent >= 70) {
        tier = 'Senior AI / Machine Learning Engineer';
        tierColor = 'text-emerald-400';
        tierBadge = 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40';
      } else if (percent >= 50) {
        tier = 'Core ML Practitioner & Systems Architect';
        tierColor = 'text-amber-400';
        tierBadge = 'bg-amber-500/20 text-amber-300 border-amber-500/40';
      } else {
        tier = 'Theoretical Deep Dive Recommended';
        tierColor = 'text-rose-400';
        tierBadge = 'bg-rose-500/20 text-rose-300 border-rose-500/40';
      }
    }

    return {
      pillars,
      totalCorrect,
      totalQuestions: questions.length,
      percent,
      tier,
      tierColor,
      tierBadge
    };
  }, [selectedAnswers, questions, currentTrackConfig, activeTrack]);

  const currentQ = questions[currentIdx] || questions[0];

  const handleSelectOption = (qId, optionIdx) => {
    if (isSubmitted) return;
    setSelectedAnswers(prev => ({
      ...prev,
      [qId]: optionIdx
    }));
  };

  const handleReset = () => {
    setSelectedAnswers({});
    setIsSubmitted(false);
    setCurrentIdx(0);
    setTimeLeft(600);
  };

  const handleCopyReport = () => {
    const report = `🏆 The Era of AI — Technical Diagnostic Assessment Report\nTrack: ${currentTrackConfig.name}\nScore: ${scores.totalCorrect}/10 (${scores.percent}%)\nReadiness Tier: ${scores.tier}\n- ${scores.pillars.math.label}: ${scores.pillars.math.correct}/${scores.pillars.math.total}\n- ${scores.pillars.ml.label}: ${scores.pillars.ml.correct}/${scores.pillars.ml.total}\n- ${scores.pillars.dl.label}: ${scores.pillars.dl.correct}/${scores.pillars.dl.total}\n- ${scores.pillars.genai.label}: ${scores.pillars.genai.correct}/${scores.pillars.genai.total}\nTested at: http://localhost:3000/`;
    navigator.clipboard.writeText(report);
    setCopiedResult(true);
    setTimeout(() => setCopiedResult(false), 2000);
  };

  if (!isOpen) return null;

  // Format time MM:SS
  const formatTime = (secs) => {
    const m = Math.floor(secs / 60);
    const s = secs % 60;
    return `${m}:${s < 10 ? '0' : ''}${s}`;
  };

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-slate-950/85 backdrop-blur-md flex items-center justify-center p-3 sm:p-6 animate-fadeIn">
      <div className="bg-slate-900 border border-slate-700/80 rounded-3xl w-full max-w-4xl shadow-2xl overflow-hidden flex flex-col max-h-[92vh]">
        {/* Header Bar */}
        <div className="p-4 sm:p-5 border-b border-slate-800 flex items-center justify-between bg-slate-900/90 shrink-0">
          <div className="flex items-center gap-3">
            <div className={`w-9 h-9 rounded-xl border flex items-center justify-center shrink-0 ${
              activeTrack === '0-2'
                ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
                : activeTrack === '2-4'
                ? 'bg-blue-500/10 text-blue-400 border-blue-500/30'
                : 'bg-purple-500/10 text-purple-400 border-purple-500/30'
            }`}>
              <BrainCircuit className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2 flex-wrap">
                <h2 className="text-sm sm:text-base font-bold text-white tracking-wide">
                  AI Technical Readiness Diagnostic
                </h2>
                <span className={`text-[10px] px-2 py-0.5 rounded-full border font-mono font-semibold ${currentTrackConfig.badgeCls}`}>
                  {currentTrackConfig.badge}
                </span>
              </div>
              <p className="text-[11px] text-slate-400 hidden sm:block">
                {currentTrackConfig.description}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            {/* Timer Badge */}
            {!isSubmitted && (
              <div className="flex items-center gap-1.5 px-3 py-1 rounded-xl bg-slate-950 border border-slate-800 text-xs font-mono text-cyan-300">
                <Clock className="w-3.5 h-3.5 text-cyan-400" />
                <span>{formatTime(timeLeft)}</span>
              </div>
            )}

            <button
              onClick={onClose}
              className="p-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white border border-slate-700 transition"
              title="Close modal"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Content Body: Assessment Questions OR Results Report */}
        <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-5">
          {/* Experience Track Tabs Selector */}
          <div className="bg-slate-950 p-1.5 rounded-2xl border border-slate-800 flex items-center gap-2 overflow-x-auto no-scrollbar">
            {[
              { id: '0-2', label: '0–2 Years', sub: 'Freshers & Novices (Zero-Math)', icon: '🌱' },
              { id: '2-4', label: '2–4 Years', sub: 'Mid-Level Applied Engineers', icon: '🚀' },
              { id: '5+', label: '5+ Years', sub: 'Senior / Staff / Quant', icon: '🏛️' },
            ].map((track) => (
              <button
                key={track.id}
                onClick={() => handleSwitchTrack(track.id)}
                className={`flex-1 min-w-[170px] p-2.5 rounded-xl border text-left transition flex items-center gap-2.5 ${
                  activeTrack === track.id
                    ? track.id === '0-2'
                      ? 'bg-emerald-950/60 border-emerald-500/60 ring-1 ring-emerald-500/40 text-emerald-200'
                      : track.id === '2-4'
                      ? 'bg-blue-950/60 border-blue-500/60 ring-1 ring-blue-500/40 text-blue-200'
                      : 'bg-purple-950/60 border-purple-500/60 ring-1 ring-purple-500/40 text-purple-200'
                    : 'bg-slate-900/60 border-slate-800 text-slate-400 hover:text-slate-200 hover:bg-slate-900'
                }`}
              >
                <span className="text-base">{track.icon}</span>
                <div className="min-w-0">
                  <div className="text-xs font-bold leading-tight">{track.label}</div>
                  <div className="text-[10px] opacity-75 truncate">{track.sub}</div>
                </div>
              </button>
            ))}
          </div>

          {!isSubmitted ? (
            /* ========================================================= */
            /* QUESTION TAKING VIEW */
            /* ========================================================= */
            <div className="space-y-5">
              {/* Novice Track Callout */}
              {activeTrack === '0-2' && (
                <div className="bg-emerald-950/30 border border-emerald-500/30 rounded-2xl p-3 sm:p-4 flex items-center gap-3">
                  <span className="text-lg">🌱</span>
                  <div className="text-xs text-emerald-300/90 leading-relaxed">
                    <strong className="text-emerald-200 font-bold block">Novice & Fresher Track Active:</strong>
                    Questions focus on fundamental intuition and real-world scenarios. No scary calculus or LaTeX formulas!
                  </div>
                </div>
              )}

              {/* Stepper Dots Bar */}
              <div className="flex items-center justify-between gap-1 pb-1">
                {questions.map((q, idx) => {
                  const isAnswered = selectedAnswers[q.id] !== undefined;
                  const isCurrent = idx === currentIdx;

                  return (
                    <button
                      key={q.id}
                      onClick={() => setCurrentIdx(idx)}
                      className={`flex-1 h-2 rounded-full transition-all ${
                        isCurrent
                          ? activeTrack === '0-2' ? 'bg-emerald-500 ring-2 ring-emerald-400/40' : activeTrack === '2-4' ? 'bg-blue-500 ring-2 ring-blue-400/40' : 'bg-purple-500 ring-2 ring-purple-400/40'
                          : isAnswered
                          ? 'bg-teal-500'
                          : 'bg-slate-800'
                      }`}
                      title={`Question ${idx + 1} (${q.pillarLabel})`}
                    />
                  );
                })}
              </div>

              {/* Question Card */}
              <div className="bg-slate-950 rounded-2xl p-5 sm:p-6 border border-slate-800 space-y-4">
                <div className="flex items-center justify-between text-xs">
                  <span className={`px-2.5 py-1 rounded-full font-semibold font-mono ${
                    activeTrack === '0-2'
                      ? 'bg-emerald-950 text-emerald-300 border border-emerald-500/30'
                      : activeTrack === '2-4'
                      ? 'bg-blue-950 text-blue-300 border border-blue-500/30'
                      : 'bg-purple-950 text-purple-300 border border-purple-500/30'
                  }`}>
                    Question {currentIdx + 1} of 10 &bull; {currentQ.pillarLabel}
                  </span>
                  <span className="text-slate-500 font-mono text-[11px]">
                    {Object.keys(selectedAnswers).length} / 10 Answered
                  </span>
                </div>

                <h3 className="text-base sm:text-xl font-bold text-white leading-relaxed">
                  <MathText text={currentQ.question} />
                </h3>

                {/* Multiple Choice Options */}
                <div className="space-y-2.5 pt-2">
                  {currentQ.options.map((opt, optIdx) => {
                    const isSelected = selectedAnswers[currentQ.id] === optIdx;

                    return (
                      <button
                        key={optIdx}
                        onClick={() => handleSelectOption(currentQ.id, optIdx)}
                        className={`w-full p-3.5 rounded-xl border text-left transition flex items-start gap-3 ${
                          isSelected
                            ? activeTrack === '0-2'
                              ? 'bg-emerald-600/20 text-white border-emerald-500 shadow-md shadow-emerald-600/10'
                              : activeTrack === '2-4'
                              ? 'bg-blue-600/20 text-white border-blue-500 shadow-md shadow-blue-600/10'
                              : 'bg-purple-600/20 text-white border-purple-500 shadow-md shadow-purple-600/10'
                            : 'bg-slate-900 hover:bg-slate-850 text-slate-300 border-slate-800 hover:border-slate-700'
                        }`}
                      >
                        <span className={`w-6 h-6 rounded-lg text-xs font-mono font-bold flex items-center justify-center shrink-0 mt-0.5 ${
                          isSelected 
                            ? activeTrack === '0-2' ? 'bg-emerald-600 text-white' : activeTrack === '2-4' ? 'bg-blue-600 text-white' : 'bg-purple-600 text-white'
                            : 'bg-slate-800 text-slate-400'
                        }`}>
                          {String.fromCharCode(65 + optIdx)}
                        </span>
                        <div className="text-xs sm:text-sm leading-relaxed">
                          <MathText text={opt} />
                        </div>
                      </button>
                    );
                  })}
                </div>
              </div>

              {/* Bottom Question Navigation Controls */}
              <div className="flex items-center justify-between pt-2">
                <button
                  onClick={() => setCurrentIdx(prev => Math.max(0, prev - 1))}
                  disabled={currentIdx === 0}
                  className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 disabled:opacity-30 text-white text-xs font-medium transition"
                >
                  Previous
                </button>

                {currentIdx < questions.length - 1 ? (
                  <button
                    onClick={() => setCurrentIdx(prev => Math.min(questions.length - 1, prev + 1))}
                    className={`px-5 py-2 rounded-xl text-white text-xs font-semibold shadow-md transition flex items-center gap-1.5 ${
                      activeTrack === '0-2'
                        ? 'bg-emerald-600 hover:bg-emerald-500 shadow-emerald-600/25'
                        : activeTrack === '2-4'
                        ? 'bg-blue-600 hover:bg-blue-500 shadow-blue-600/25'
                        : 'bg-purple-600 hover:bg-purple-500 shadow-purple-600/25'
                    }`}
                  >
                    <span>Next</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </button>
                ) : (
                  <button
                    onClick={() => setIsSubmitted(true)}
                    className="px-6 py-2 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white text-xs font-bold shadow-lg shadow-emerald-600/25 transition flex items-center gap-2"
                  >
                    <Award className="w-4 h-4" />
                    <span>Submit & Generate Diagnostic Report</span>
                  </button>
                )}
              </div>
            </div>
          ) : (
            /* ========================================================= */
            /* RESULTS & RADAR SKILL REPORT VIEW */
            /* ========================================================= */
            <div className="space-y-6 animate-fadeIn">
              {/* Score & Tier Banner */}
              <div className="bg-gradient-to-br from-slate-900 to-slate-950 p-6 rounded-3xl border border-slate-800 flex flex-col sm:flex-row items-center justify-between gap-6 shadow-xl">
                <div className="flex items-center gap-4">
                  <div className={`w-16 h-16 rounded-2xl border flex items-center justify-center shrink-0 ${
                    activeTrack === '0-2'
                      ? 'bg-emerald-500/10 border-emerald-500/30'
                      : activeTrack === '2-4'
                      ? 'bg-blue-500/10 border-blue-500/30'
                      : 'bg-purple-500/10 border-purple-500/30'
                  }`}>
                    <Award className={`w-8 h-8 ${
                      activeTrack === '0-2' ? 'text-emerald-400' : activeTrack === '2-4' ? 'text-blue-400' : 'text-purple-400'
                    }`} />
                  </div>
                  <div className="space-y-1">
                    <span className={`text-[11px] font-bold uppercase tracking-wider px-3 py-0.5 rounded-full border ${scores.tierBadge}`}>
                      {scores.tier}
                    </span>
                    <h3 className="text-2xl sm:text-3xl font-black text-white">
                      {scores.totalCorrect} / 10 Correct ({scores.percent}%)
                    </h3>
                    <p className="text-xs text-slate-400">
                      Track: {currentTrackConfig.name} &bull; Completed in {formatTime(600 - timeLeft)}
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-2 shrink-0">
                  <button
                    onClick={handleCopyReport}
                    className="px-3.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 text-xs font-medium transition flex items-center gap-1.5"
                  >
                    {copiedResult ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Share2 className="w-3.5 h-3.5" />}
                    <span>{copiedResult ? 'Report Copied!' : 'Share Score'}</span>
                  </button>

                  <button
                    onClick={handleReset}
                    className="px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-white text-xs font-semibold transition flex items-center gap-1.5 shadow-md shadow-purple-600/25"
                  >
                    <RotateCcw className="w-3.5 h-3.5" />
                    <span>Retake Diagnostic</span>
                  </button>
                </div>
              </div>

              {/* 4 Pillars Breakdown & Visual SVG Radar / Bar Graphic */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* Visual SVG Radar Web */}
                <div className="bg-slate-950 p-5 rounded-2xl border border-slate-800 flex flex-col items-center justify-center space-y-2">
                  <span className="text-xs font-bold text-slate-300 uppercase tracking-wider self-start flex items-center gap-1.5">
                    <Compass className="w-3.5 h-3.5 text-purple-400" />
                    AI Knowledge Radar Profile
                  </span>

                  <svg className="w-60 h-60" viewBox="-120 -120 240 240">
                    {/* Concentric Radar Rings */}
                    {[0.25, 0.5, 0.75, 1.0].map(r => (
                      <circle
                        key={`ring-${r}`}
                        cx="0"
                        cy="0"
                        r={r * 80}
                        fill="none"
                        stroke="rgba(255, 255, 255, 0.08)"
                        strokeDasharray="3,3"
                      />
                    ))}

                    {/* Radar Cross Axes */}
                    <line x1="0" y1="-85" x2="0" y2="85" stroke="rgba(255, 255, 255, 0.1)" />
                    <line x1="-85" y1="0" x2="85" y2="0" stroke="rgba(255, 255, 255, 0.1)" />

                    {/* Axis Labels */}
                    <text x="0" y="-92" textAnchor="middle" fill="#c084fc" fontSize="9" fontWeight="bold">Foundations</text>
                    <text x="96" y="3" textAnchor="start" fill="#38bdf8" fontSize="9" fontWeight="bold">ML</text>
                    <text x="0" y="100" textAnchor="middle" fill="#fb7185" fontSize="9" fontWeight="bold">Deep Learning</text>
                    <text x="-96" y="3" textAnchor="end" fill="#34d399" fontSize="9" fontWeight="bold">GenAI</text>

                    {/* Computed User Polygon */}
                    {(() => {
                      const pMath = scores.pillars.math.total ? scores.pillars.math.correct / scores.pillars.math.total : 0;
                      const pML = scores.pillars.ml.total ? scores.pillars.ml.correct / scores.pillars.ml.total : 0;
                      const pDL = scores.pillars.dl.total ? scores.pillars.dl.correct / scores.pillars.dl.total : 0;
                      const pGenAI = scores.pillars.genai.total ? scores.pillars.genai.correct / scores.pillars.genai.total : 0;

                      const ptMath = [0, -Math.max(10, pMath * 80)];
                      const ptML = [Math.max(10, pML * 80), 0];
                      const ptDL = [0, Math.max(10, pDL * 80)];
                      const ptGenAI = [-Math.max(10, pGenAI * 80), 0];

                      const pointsStr = `${ptMath[0]},${ptMath[1]} ${ptML[0]},${ptML[1]} ${ptDL[0]},${ptDL[1]} ${ptGenAI[0]},${ptGenAI[1]}`;

                      return (
                        <>
                          <polygon
                            points={pointsStr}
                            fill={activeTrack === '0-2' ? 'rgba(16, 185, 129, 0.25)' : activeTrack === '2-4' ? 'rgba(59, 130, 246, 0.25)' : 'rgba(168, 85, 247, 0.25)'}
                            stroke={activeTrack === '0-2' ? '#34d399' : activeTrack === '2-4' ? '#60a5fa' : '#c084fc'}
                            strokeWidth="2.5"
                          />
                          {[ptMath, ptML, ptDL, ptGenAI].map((pt, i) => (
                            <circle key={i} cx={pt[0]} cy={pt[1]} r="4" fill="#ffffff" stroke="#c084fc" strokeWidth="2" />
                          ))}
                        </>
                      );
                    })()}
                  </svg>
                </div>

                {/* Pillar Score Bars */}
                <div className="bg-slate-950 p-5 rounded-2xl border border-slate-800 space-y-4 flex flex-col justify-center">
                  <span className="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
                    <TrendingUp className="w-3.5 h-3.5 text-emerald-400" />
                    Pillar Mastery Percentages
                  </span>

                  {Object.entries(scores.pillars).map(([k, p]) => {
                    const pct = p.total ? Math.round((p.correct / p.total) * 100) : 0;

                    return (
                      <div key={k} className="space-y-1">
                        <div className="flex justify-between text-xs">
                          <span className="text-slate-300 font-medium">{p.label}</span>
                          <span className="font-mono text-purple-300 font-bold">{p.correct}/{p.total} ({pct}%)</span>
                        </div>
                        <div className="h-2 w-full bg-slate-900 rounded-full overflow-hidden">
                          <div 
                            className={`h-full rounded-full transition-all duration-500 ${
                              activeTrack === '0-2'
                                ? 'bg-gradient-to-r from-emerald-500 to-teal-400'
                                : activeTrack === '2-4'
                                ? 'bg-gradient-to-r from-blue-500 to-indigo-400'
                                : 'bg-gradient-to-r from-purple-500 to-pink-400'
                            }`}
                            style={{ width: `${pct}%` }}
                          />
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Detailed Question Review List */}
              <div className="space-y-3">
                <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
                  <BookOpen className="w-3.5 h-3.5 text-cyan-400" />
                  Detailed Question Explanations & Answers:
                </h4>

                <div className="space-y-3">
                  {questions.map((q, idx) => {
                    const userAns = selectedAnswers[q.id];
                    const isCorrect = userAns === q.correctIndex;

                    return (
                      <div 
                        key={q.id}
                        className={`p-4 rounded-2xl border text-xs space-y-2 ${
                          isCorrect 
                            ? 'bg-slate-950/70 border-emerald-500/30' 
                            : 'bg-slate-950/70 border-rose-500/30'
                        }`}
                      >
                        <div className="flex items-center justify-between">
                          <span className="font-mono text-slate-400 font-bold">
                            Question #{idx + 1} &bull; {q.pillarLabel}
                          </span>
                          <span className={`px-2 py-0.5 rounded-full font-mono font-bold text-[10px] ${
                            isCorrect ? 'bg-emerald-500/20 text-emerald-300' : 'bg-rose-500/20 text-rose-300'
                          }`}>
                            {isCorrect ? 'Correct' : 'Needs Review'}
                          </span>
                        </div>

                        <p className="font-semibold text-white text-xs sm:text-sm">
                          <MathText text={q.question} />
                        </p>

                        <div className="text-slate-300 space-y-1 pt-1 border-t border-slate-800/80">
                          <div>
                            <span className="text-slate-500">Correct Answer: </span>
                            <strong className="text-emerald-400">
                              <MathText text={q.options[q.correctIndex]} />
                            </strong>
                          </div>
                          {!isCorrect && userAns !== undefined && (
                            <div>
                              <span className="text-slate-500">Your Choice: </span>
                              <span className="text-rose-400">
                                <MathText text={q.options[userAns]} />
                              </span>
                            </div>
                          )}
                        </div>

                        <div className="p-3 bg-slate-900 rounded-xl border border-slate-800 text-[11px] text-slate-400 leading-relaxed">
                          <strong className="text-purple-300 block mb-0.5">Explanation:</strong>
                          <MathText text={q.explanation} />
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
