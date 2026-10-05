import json
import os

from build_encyclopedia import TOPICS
from papers_data import PAPERS
from projects_data import PROJECTS
from interview_questions_data import INTERVIEW_QUESTIONS
from all_concepts import ALL_CONCEPTS

HUB_NODES = [
    {
        "id": "root", "label": "AI & Machine Learning Universe", "category": "center", "x": 0, "y": 0, "level": 0,
        "def": "The unified superset of artificial intelligence, statistical learning, deep representations, and automated reasoning.",
        "formula": "$$f: \\mathcal{X} \\to \\mathcal{Y}, \\quad \\min_\\theta \\mathcal{L}(f(X; \\theta), Y) + \\lambda \\Omega(\\theta)$$",
        "logic": "All AI/ML algorithms learn an approximating function f(X; θ) mapping inputs X to targets Y while penalizing complexity Ω(θ) to ensure generalization.",
        "example": "Predicting house price Y given features X, or predicting the next token in a conversational prompt.",
        "subtopics": ["Mathematical Foundations", "Data Engineering & Preprocessing", "Classical ML", "Model Evaluation", "Deep Learning", "Generative AI & LLMs", "MLOps & Production"],
        "connections": ["math_root", "data_root", "ml_root", "eval_root", "dl_root", "genai_root", "mlops_root"]
    },
    {
        "id": "math_root", "label": "1. Mathematical Foundations", "category": "math", "x": -500, "y": -450, "level": 1,
        "def": "The theoretical backbone of all ML algorithms: vector spaces, optimization calculus, and statistical inference.",
        "formula": "$$\\mathcal{L}(\\theta) = \\mathbb{E}_{(x, y)} [\\text{loss}(y, f(x; \\theta))]$$",
        "logic": "Provides the formal language to define loss surfaces, calculate gradients, compute probabilities, and prove convergence bounds.",
        "example": "Understanding why high-dimensional embeddings suffer from the curse of dimensionality and how cosine distance remedies it.",
        "subtopics": ["Linear Algebra", "Calculus & Optimization", "Probability & Statistics", "Information Theory"],
        "connections": ["root"]
    },
    {
        "id": "data_root", "label": "2. Data Preprocessing & EDA", "category": "data", "x": -550, "y": 150, "level": 1,
        "def": "The end-to-end pipeline of cleaning, transforming, imputing, scaling, and partitioning raw real-world data for robust modeling.",
        "formula": "$$\\mathcal{D}_{\\text{clean}} = \\text{Pipeline}(\\text{Scrub}(\\mathcal{D}_{\\text{raw}})) \\implies X_{\\text{train}}, X_{\\text{val}}, X_{\\text{test}}$$",
        "logic": "Raw data contains sensor noise, missing entries, extreme outliers, and skewed distributions that destabilize optimization without proper preprocessing.",
        "example": "Transforming messy CSV transaction logs into normalized numerical feature matrices ready for model training.",
        "subtopics": ["Scrubbing & Outliers", "Imputation Strategies", "Feature Scaling", "Feature Engineering", "Data Partitioning & SMOTE"],
        "connections": ["root"]
    },
    {
        "id": "ml_root", "label": "3. Classical Machine Learning", "category": "ml", "x": -100, "y": -450, "level": 1,
        "def": "Supervised and unsupervised statistical learning algorithms, loss formulations, gradient descent optimization, and regularization.",
        "formula": "$$\\hat{y} = f(X; W, b) = \\sigma(W^T X + b)$$",
        "logic": "Establishes foundational concepts of feature weights, loss minimization, decision boundaries, tree-based partitioning, and clustering.",
        "example": "Training an XGBoost model on structured tabular customer records to predict churn with high explainability.",
        "subtopics": ["Linear Regression", "Loss Functions", "Gradient Descent", "Classification & Sigmoid", "Regularization", "Trees & Boosting", "Unsupervised & Clustering"],
        "connections": ["root"]
    },
    {
        "id": "eval_root", "label": "4. Model Evaluation & Generalization", "category": "eval", "x": -100, "y": 350, "level": 1,
        "def": "Rigorous quantitative frameworks to test accuracy, calibration, trade-offs, and generalization performance on unseen data.",
        "formula": "$$\\mathbb{E}[(y - \\hat{f})^2] = \\text{Bias}^2 + \\text{Variance} + \\sigma^2$$",
        "logic": "Prevents deploying models with false confidence caused by data leakage, class imbalance skew, or memorization of training noise.",
        "example": "Using PR-AUC and Recall instead of raw Accuracy to evaluate an automated credit card fraud detector.",
        "subtopics": ["Confusion Matrix", "ROC & PR Curves", "Bias-Variance Tradeoff", "Cross-Validation"],
        "connections": ["root"]
    },
    {
        "id": "dl_root", "label": "5. Deep Learning Foundations", "category": "dl", "x": 450, "y": -200, "level": 1,
        "def": "Hierarchical representation learning through layered computational graphs, non-linear activations, backpropagation, and specialized architectures.",
        "formula": "$$a^{[l]} = g\\left(W^{[l]} a^{[l-1]} + b^{[l]}\\right)$$",
        "logic": "Replaces manual feature engineering with learned feature hierarchies (e.g. pixels -> edges -> textures -> objects).",
        "example": "Deep convolutional networks classifying 1,000 distinct object classes from raw ImageNet pixel matrices.",
        "subtopics": ["Neurons & Perceptrons", "Activation Functions", "Backpropagation", "Optimizers (Adam, AdamW)", "Normalization (BatchNorm, LayerNorm)", "Vision (CNN, ViT)", "Sequence Models (LSTM)", "Diffusion Models"],
        "connections": ["root"]
    },
    {
        "id": "genai_root", "label": "6. Transformers & Generative AI", "category": "genai", "x": 450, "y": 250, "level": 1,
        "def": "Modern foundation models, self-attention architectures, next-token prediction, parameter-efficient fine-tuning (PEFT), and autonomous agent frameworks.",
        "formula": "$$\\text{Attention}(Q, K, V) = \\text{softmax}\\left(\\frac{Q K^T}{\\sqrt{d_k}}\\right) V$$",
        "logic": "Self-attention enables dynamic routing of semantic information between all pairs of tokens in parallel, scaling pre-training to trillions of tokens.",
        "example": "Large Language Models generating code, summarizing legal documents, reasoning step-by-step, and calling external APIs autonomously.",
        "subtopics": ["Tokenization & Embeddings", "Self-Attention Mechanism", "Pre-training, SFT & LoRA", "Alignment (RLHF, DPO)", "RAG Ecosystem", "Prompt Engineering & Agents"],
        "connections": ["root"]
    }
]

ALL_NODES = HUB_NODES + TOPICS

CROSS_LINKS = [
    {"from": "math_calc", "to": "ml_opt", "label": "Supplies ∇ Gradients"},
    {"from": "math_linalg", "to": "genai_embed", "label": "Powers Vector Spaces"},
    {"from": "math_prob", "to": "ml_logistic", "label": "Likelihood & Probabilities"},
    {"from": "math_info", "to": "ml_loss", "label": "Derives Cross-Entropy"},
    {"from": "data_scale", "to": "ml_opt", "label": "Enables Gradient Stability"},
    {"from": "data_fe", "to": "ml_linear", "label": "Supplies Feature Matrix X"},
    {"from": "data_split", "to": "eval_tradeoff", "label": "Measures Generalization"},
    {"from": "ml_loss", "to": "dl_backprop", "label": "Seed of Chain Rule"},
    {"from": "ml_opt", "to": "dl_opt", "label": "Evolves to Adam / AdamW"},
    {"from": "ml_reg", "to": "dl_norm", "label": "Controls Overfitting"},
    {"from": "ml_logistic", "to": "dl_activations", "label": "Sigmoid becomes Activation"},
    {"from": "dl_neurons", "to": "genai_attention", "label": "Layered Linear Projections"},
    {"from": "genai_embed", "to": "genai_rag", "label": "Generates Vector Chunks"},
    {"from": "dl_opt", "to": "genai_train", "label": "Drives LoRA / Pre-training"},
    {"from": "eval_matrix", "to": "genai_align", "label": "Evaluates Alignment Quality"}
]

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Master AI / ML / DL / Data Mind Map & Research Papers Hub</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>

  <!-- KaTeX for High-Fidelity Mathematical Typesetting (Local + CDN Fallback) -->
  <link rel="stylesheet" href="katex/katex.min.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
  <script src="katex/katex.min.js"></script>
  <script src="katex/auto-render.min.js"></script>
  <script>
    if (typeof katex === 'undefined') {
      document.write('<script src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"><\\/script>');
      document.write('<script src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"><\\/script>');
    }
  </script>

  <style>
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: var(--card, #1e293b); }
    ::-webkit-scrollbar-thumb { background: var(--border, #475569); border-radius: 3px; }
    .grab-cursor { cursor: grab; }
    .grabbing-cursor { cursor: grabbing; }
    .badge {
      font-size: 11px;
      padding: 2px 8px;
      border-radius: 9999px;
      font-weight: 500;
    }

    /* KaTeX equation display enhancements */
    .katex {
      font-size: 1.05em !important;
      text-rendering: geometricPrecision;
      color: #f1f5f9;
    }
    .katex-display {
      margin: 0.6em 0 !important;
      overflow-x: auto !important;
      overflow-y: hidden !important;
      padding: 0.4rem 0.25rem;
      scrollbar-width: thin;
      text-align: center;
    }
    .katex-display::-webkit-scrollbar {
      height: 4px;
    }
    .katex-display::-webkit-scrollbar-thumb {
      background: #6366f1;
      border-radius: 2px;
    }
    .katex .mord, .katex .mbin, .katex .mrel, .katex .mopen, .katex .mclose, .katex .mpunct {
      color: #f8fafc;
    }
    .katex .frac-line {
      border-bottom-width: 1.5px !important;
      border-color: #a5b4fc !important;
    }
    .katex-inline-formula {
      display: inline-block;
      padding: 0 1px;
      vertical-align: middle;
    }
    .formula-box {
      background: rgba(15, 23, 42, 0.7);
      border: 1px solid rgba(99, 102, 241, 0.25);
      border-radius: 0.6rem;
      padding: 0.6rem 0.8rem;
      margin: 0.4rem 0;
      overflow-x: auto;
    }

    @media print {
      @page {
        margin: 1.2cm;
        size: A4 portrait;
      }
      body {
        overflow: visible !important;
        height: auto !important;
        background: #ffffff !important;
        color: #0f172a !important;
      }
      header, #mindmapViewport, #inspectorPanel, .quick-legend, .grid-overlay, .no-print, #navTabs {
        display: none !important;
      }
      #printableDocContainer, #papersContainer {
        position: static !important;
        width: 100% !important;
        height: auto !important;
        overflow: visible !important;
        background: #ffffff !important;
        color: #0f172a !important;
        padding: 0 !important;
      }
      .print-card {
        page-break-inside: avoid !important;
        break-inside: avoid !important;
        border: 1px solid #cbd5e1 !important;
        background: #ffffff !important;
        color: #0f172a !important;
        margin-bottom: 1.25rem !important;
        padding: 1.2rem !important;
        border-radius: 0.5rem !important;
        box-shadow: none !important;
      }
      .print-domain-header {
        page-break-before: auto !important;
        break-before: auto !important;
        color: #1e1b4b !important;
        border-bottom: 2px solid #4f46e5 !important;
        padding-bottom: 0.5rem !important;
        margin-top: 1.5rem !important;
        margin-bottom: 1rem !important;
      }
      .print-formula {
        background: #f8fafc !important;
        color: #0f172a !important;
        border: 1px solid #cbd5e1 !important;
      }
      .print-logic {
        background: #fffbeb !important;
        color: #78350f !important;
        border: 1px solid #fef3c7 !important;
      }
      .print-example {
        background: #ecfdf5 !important;
        color: #064e3b !important;
        border: 1px solid #a7f3d0 !important;
      }
      .print-badge {
        border: 1px solid #94a3b8 !important;
        color: #334155 !important;
        background: #f1f5f9 !important;
      }
      .print-subtopic-bullet {
        color: #4338ca !important;
      }
    }
  
    /* Mobile Responsive Optimizations */
    .no-scrollbar::-webkit-scrollbar {
      display: none;
    }
    .no-scrollbar {
      -ms-overflow-style: none;
      scrollbar-width: none;
    }
    @media (max-width: 640px) {
      .mobile-bottom-sheet {
        position: fixed !important;
        bottom: 0 !important;
        top: auto !important;
        left: 0 !important;
        right: 0 !important;
        width: 100% !important;
        max-width: 100% !important;
        max-height: 85vh !important;
        border-radius: 1.5rem 1.5rem 0 0 !important;
        transform: translateY(100%) !important;
      }
      .mobile-bottom-sheet.inspector-open {
        transform: translateY(0) !important;
      }
      .mobile-tab-text {
        font-size: 11px !important;
      }
    }
    @media (min-width: 641px) {
      .inspector-open {
        transform: translateX(0) !important;
      }
    }
    </style>
  <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
  <script>mermaid.initialize({ startOnLoad: false, theme: 'dark' });</script>
</head>
<body class="bg-[var(--background,#0f172a)] text-[var(--foreground,#f8fafc)] font-sans antialiased overflow-hidden h-screen w-screen flex flex-col select-none">

  <!-- Header & Toolbar -->
  <header class="bg-[var(--card,#1e293b)] border-b border-[var(--border,#334155)] px-4 py-2.5 flex flex-wrap items-center justify-between gap-3 z-20 shadow-md">
    <div class="flex items-center space-x-3">
      <div class="p-2 rounded-lg bg-indigo-600 text-white font-bold flex items-center justify-center shadow-lg shadow-indigo-500/30">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
      </div>
      <div>
        <h1 class="font-bold text-base md:text-lg tracking-tight text-[var(--foreground,#f8fafc)] flex items-center gap-2">
          Master AI & Machine Learning Knowledge Graph
        </h1>
        <p class="text-xs text-[var(--muted-foreground,#94a3b8)]">Interactive Mind Map &bull; Complete Syllabus &bull; Landmark Research Papers Hub</p>
      </div>
    </div>

    <!-- Navigation Tabs -->
    <div id="navTabs" class="flex items-center overflow-x-auto no-scrollbar max-w-full space-x-1 bg-slate-900/80 p-1 rounded-xl border border-slate-700/60 shadow-inner flex-nowrap shrink-0">
      <button onclick="switchMainTab('mindmap')" id="tabBtn-mindmap" class="px-3 py-1.5 rounded-lg text-xs font-semibold transition flex items-center gap-1.5 bg-indigo-600 text-white shadow whitespace-nowrap shrink-0">
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7"/></svg>
        <span>Mind Map</span>
      </button>

      <button onclick="switchMainTab('syllabus')" id="tabBtn-syllabus" class="px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-300 hover:text-white transition flex items-center gap-1.5 whitespace-nowrap shrink-0">
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h7"/></svg>
        <span>Line-wise Syllabus</span>
      </button>

      <button onclick="switchMainTab('papers')" id="tabBtn-papers" class="px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-300 hover:text-white transition flex items-center gap-1.5 relative whitespace-nowrap shrink-0">
        <svg class="w-3.5 h-3.5 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/></svg>
        <span>Landmark Papers</span>
        <span class="w-2 h-2 rounded-full bg-amber-400 animate-pulse"></span>
      </button>

      <button onclick="switchMainTab('projects')" id="tabBtn-projects" class="px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-300 hover:text-white transition flex items-center gap-1.5 relative whitespace-nowrap shrink-0">
        <svg class="w-3.5 h-3.5 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/></svg>
        <span>Production Case Studies</span>
        <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
      </button>

      <button onclick="switchMainTab('interview')" id="tabBtn-interview" class="px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-300 hover:text-white transition flex items-center gap-1.5 relative whitespace-nowrap shrink-0">
        <svg class="w-3.5 h-3.5 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
        <span>Interview Vault (150+)</span>
        <span class="w-2 h-2 rounded-full bg-purple-400 animate-pulse"></span>
      </button>
    </div>

    <!-- Right Controls: Download Syllabus PDF (Only visible on Line-wise Syllabus) -->
    <div class="flex items-center space-x-2">
      <button onclick="downloadActiveViewPDF()" id="pdfBtn" title="Download Syllabus PDF" class="hidden p-1.5 rounded-lg bg-gradient-to-r from-red-600 to-rose-600 hover:from-red-500 hover:to-rose-500 text-white font-semibold text-xs px-3 shadow-md shadow-red-500/20 transition flex items-center gap-1.5">
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
        <span>Download Syllabus PDF</span>
      </button>
    </div>
  </header>

  <!-- Sub-header Toolbar (Mind Map controls) -->
  <div id="mindmapToolbar" class="bg-slate-900/90 border-b border-slate-800 px-4 py-2 flex flex-wrap items-center justify-between gap-2 z-10">
    <div class="flex items-center space-x-2">
      <div class="relative">
        <input id="searchInput" type="text" placeholder="Search 34+ modules (e.g. AdamW, ROC, LoRA, L2)..."
               class="bg-[var(--background,#0f172a)] border border-[var(--border,#334155)] text-xs text-[var(--foreground,#f8fafc)] rounded-lg pl-8 pr-4 py-1 focus:outline-none focus:ring-2 focus:ring-indigo-500 w-52 md:w-72 placeholder-[var(--muted-foreground,#64748b)]">
        <svg class="w-3.5 h-3.5 absolute left-2.5 top-2 text-[var(--muted-foreground,#64748b)]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
      </div>

      <div class="hidden xl:flex items-center space-x-1 text-xs" id="domainFilterGroup">
        <button onclick="filterDomain('all')" class="px-2.5 py-0.5 rounded text-xs font-medium bg-indigo-600 text-white domain-btn active" data-domain="all">All</button>
        <button onclick="filterDomain('math')" class="px-2.5 py-0.5 rounded text-xs font-medium bg-[var(--background,#0f172a)] text-[var(--muted-foreground,#94a3b8)] hover:text-white border border-[var(--border,#334155)] domain-btn" data-domain="math">Math</button>
        <button onclick="filterDomain('data')" class="px-2.5 py-0.5 rounded text-xs font-medium bg-[var(--background,#0f172a)] text-[var(--muted-foreground,#94a3b8)] hover:text-white border border-[var(--border,#334155)] domain-btn" data-domain="data">Data</button>
        <button onclick="filterDomain('ml')" class="px-2.5 py-0.5 rounded text-xs font-medium bg-[var(--background,#0f172a)] text-[var(--muted-foreground,#94a3b8)] hover:text-white border border-[var(--border,#334155)] domain-btn" data-domain="ml">Classical ML</button>
        <button onclick="filterDomain('eval')" class="px-2.5 py-0.5 rounded text-xs font-medium bg-[var(--background,#0f172a)] text-[var(--muted-foreground,#94a3b8)] hover:text-white border border-[var(--border,#334155)] domain-btn" data-domain="eval">Evaluation</button>
        <button onclick="filterDomain('dl')" class="px-2.5 py-0.5 rounded text-xs font-medium bg-[var(--background,#0f172a)] text-[var(--muted-foreground,#94a3b8)] hover:text-white border border-[var(--border,#334155)] domain-btn" data-domain="dl">Deep Learning</button>
        <button onclick="filterDomain('genai')" class="px-2.5 py-0.5 rounded text-xs font-medium bg-[var(--background,#0f172a)] text-[var(--muted-foreground,#94a3b8)] hover:text-white border border-[var(--border,#334155)] domain-btn" data-domain="genai">GenAI & LLM</button>
      </div>
    </div>

    <div class="flex items-center space-x-1.5 text-xs">
      <button onclick="zoom(0.15)" title="Zoom In" class="p-1 rounded hover:bg-[var(--border,#334155)] text-[var(--foreground,#f8fafc)] transition">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
      </button>
      <button onclick="zoom(-0.15)" title="Zoom Out" class="p-1 rounded hover:bg-[var(--border,#334155)] text-[var(--foreground,#f8fafc)] transition">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4"/></svg>
      </button>
      <button onclick="resetZoom()" title="Reset View" class="p-1 rounded hover:bg-[var(--border,#334155)] text-[var(--foreground,#f8fafc)] transition px-2 font-semibold">
        Reset
      </button>
      <button onclick="toggleInterlinks()" id="interlinksBtn" title="Toggle Cross-links" class="p-1 rounded bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 px-2 font-medium hover:bg-indigo-500/30 transition">
        Links: ON
      </button>
    </div>
  </div>

  <!-- Main Viewport -->
  <main class="relative flex-1 w-full h-full overflow-hidden bg-[var(--background,#0b0f19)]">
    <!-- TAB 1: 2D Mind Map Canvas -->
    <div id="mindmapTabContainer" class="absolute inset-0">
      <svg class="grid-overlay absolute inset-0 w-full h-full pointer-events-none opacity-20">
        <defs>
          <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
            <path d="M 40 0 L 0 0 0 40" fill="none" stroke="currentColor" stroke-width="0.8" class="text-slate-600"/>
            <circle cx="0" cy="0" r="1.5" fill="currentColor" class="text-slate-500"/>
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill="url(#grid)" />
      </svg>

      <div id="mindmapViewport" class="absolute inset-0 grab-cursor overflow-hidden">
        <svg id="mindmapSvg" class="w-full h-full overflow-visible">
          <defs>
            <marker id="arrowhead-cross" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
              <polygon points="0 0, 8 3, 0 6" fill="#f59e0b" />
            </marker>
          </defs>
          <g id="worldGroup">
            <g id="linksHierarchyGroup"></g>
            <g id="linksCrossGroup"></g>
            <g id="nodesGroup"></g>
          </g>
        </svg>
      </div>

      <!-- Quick Legend -->
      <div class="quick-legend absolute bottom-4 left-4 bg-[var(--card,#1e293b)]/90 backdrop-blur-md border border-[var(--border,#334155)] rounded-xl px-4 py-2 text-xs text-slate-300 shadow-lg pointer-events-none hidden md:flex items-center space-x-4">
        <div class="flex items-center space-x-1.5"><span class="w-2.5 h-2.5 rounded-full bg-blue-500"></span><span>Math</span></div>
        <div class="flex items-center space-x-1.5"><span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span><span>Data</span></div>
        <div class="flex items-center space-x-1.5"><span class="w-2.5 h-2.5 rounded-full bg-purple-500"></span><span>Classical ML</span></div>
        <div class="flex items-center space-x-1.5"><span class="w-2.5 h-2.5 rounded-full bg-pink-500"></span><span>Deep Learning</span></div>
        <div class="flex items-center space-x-1.5"><span class="w-2.5 h-2.5 rounded-full bg-amber-500"></span><span>Transformers</span></div>
        <div class="text-slate-400 border-l border-slate-700 pl-3">Drag to Pan &bull; Scroll to Zoom &bull; Click Node for 4-Part Details</div>
      </div>
    </div>

    <!-- TAB 2: Line-Wise Syllabus Document -->
    <div id="printableDocContainer" class="hidden absolute inset-0 overflow-y-auto p-6 md:p-12 z-10 bg-[var(--background,#0b0f19)] text-[var(--foreground,#f8fafc)]"></div>

    <!-- TAB 3: Landmark Research Papers Hub -->
    <div id="papersTabContainer" class="hidden absolute inset-0 overflow-y-auto p-6 md:p-12 z-10 bg-[var(--background,#0b0f19)] text-[var(--foreground,#f8fafc)]">
      <div class="max-w-5xl mx-auto space-y-6 pb-20">
        <!-- Papers Header -->
        <div class="border-b border-slate-700 pb-5 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-500/20 text-amber-300 border border-amber-500/30 text-xs font-semibold uppercase tracking-wider mb-2">
              Landmark Research Papers
            </div>
            <h2 class="text-2xl md:text-3xl font-extrabold tracking-tight text-white">
              Game-Changing AI & Machine Learning Research Papers
            </h2>
            <p class="text-xs md:text-sm text-slate-400 mt-1">
              Publicly Available Seminal Papers (From "Attention Is All You Need" to ResNet, LoRA, DPO, and Diffusion) with Direct Links, Core Innovations, and Historical Legacy.
            </p>
          </div>
        </div>

        <!-- Papers Search & Filter -->
        <div class="flex flex-wrap items-center justify-between gap-3 no-print">
          <div class="relative flex-1 min-w-[240px] max-w-md">
            <input id="paperSearchInput" type="text" placeholder="Search papers by title, author, breakthrough (e.g. Vaswani, Attention, LoRA, ResNet)..."
                   class="w-full bg-slate-900 border border-slate-700 text-xs text-white rounded-lg pl-8 pr-4 py-2 focus:outline-none focus:ring-2 focus:ring-amber-500 placeholder-slate-500">
            <svg class="w-4 h-4 absolute left-2.5 top-2.5 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
          </div>

          <div class="flex items-center overflow-x-auto no-scrollbar max-w-full space-x-1.5 pb-1 text-xs flex-nowrap">
            <button onclick="filterPapers('all')" class="px-2.5 py-1 rounded-md font-medium bg-amber-600 text-white paper-btn active" data-cat="all">All (22)</button>
            <button onclick="filterPapers('transformer')" class="px-2.5 py-1 rounded-md font-medium bg-slate-900 text-slate-400 hover:text-white border border-slate-700 paper-btn" data-cat="transformer">Transformers & Attention</button>
            <button onclick="filterPapers('llm')" class="px-2.5 py-1 rounded-md font-medium bg-slate-900 text-slate-400 hover:text-white border border-slate-700 paper-btn" data-cat="llm">LLMs & Scaling</button>
            <button onclick="filterPapers('vision_dl')" class="px-2.5 py-1 rounded-md font-medium bg-slate-900 text-slate-400 hover:text-white border border-slate-700 paper-btn" data-cat="vision_dl">Vision & Foundations</button>
            <button onclick="filterPapers('generative')" class="px-2.5 py-1 rounded-md font-medium bg-slate-900 text-slate-400 hover:text-white border border-slate-700 paper-btn" data-cat="generative">Diffusion & GANs</button>
            <button onclick="filterPapers('alignment')" class="px-2.5 py-1 rounded-md font-medium bg-slate-900 text-slate-400 hover:text-white border border-slate-700 paper-btn" data-cat="alignment">Alignment & RLHF</button>
          </div>
        </div>

        <!-- Papers List Container -->
        <div id="papersList" class="space-y-4"></div>
      </div>
    </div>

    <!-- TAB 4: Production AI Case Studies & Real-World Projects Hub -->
    <div id="projectsTabContainer" class="hidden absolute inset-0 overflow-y-auto p-6 md:p-12 z-10 bg-[var(--background,#0b0f19)] text-[var(--foreground,#f8fafc)]">
      <div class="max-w-6xl mx-auto space-y-6 pb-20">
        <!-- Projects Header -->
        <div class="border-b border-slate-700 pb-5 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-xs font-semibold uppercase tracking-wider mb-2">
              Enterprise Case Studies
            </div>
            <h2 class="text-2xl md:text-3xl font-extrabold tracking-tight text-white">
              Full-Scale Production Implementations & Zero-to-One Architectures
            </h2>
            <p class="text-xs md:text-sm text-slate-400 mt-1">
              End-to-End System Designs, Interactive Flowcharts, Dynamic Schema Engines, Hybrid ML/RAG, Agentic Multimodal Studios & Copy-Pasteable Code.
            </p>
          </div>
        </div>

        <!-- Projects Search & Filter -->
        <div class="flex flex-wrap items-center justify-between gap-3 no-print">
          <div class="relative flex-1 min-w-[240px] max-w-md">
            <input id="projectSearchInput" type="text" placeholder="Search projects by title, tech stack (LightGBM, Pinecone, CLIP, SDXL, Kafka)..."
                   class="w-full bg-slate-900 border border-slate-700 text-xs text-white rounded-lg pl-8 pr-4 py-2 focus:outline-none focus:ring-2 focus:ring-emerald-500 placeholder-slate-500">
            <svg class="w-4 h-4 absolute left-2.5 top-2.5 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
          </div>

          <div class="flex items-center overflow-x-auto no-scrollbar max-w-full space-x-1.5 pb-1 text-xs flex-nowrap">
            <button onclick="filterProjects('all')" class="px-2.5 py-1 rounded-md font-medium bg-emerald-600 text-white proj-btn active" data-cat="all">All (5)</button>
            <button onclick="filterProjects('hybrid_rag_ml')" class="px-2.5 py-1 rounded-md font-medium bg-slate-900 text-slate-400 hover:text-white border border-slate-700 proj-btn" data-cat="hybrid_rag_ml">Multi-Tenant & RAG</button>
            <button onclick="filterProjects('agentic_multimodal')" class="px-2.5 py-1 rounded-md font-medium bg-slate-900 text-slate-400 hover:text-white border border-slate-700 proj-btn" data-cat="agentic_multimodal">Agentic & Multimodal</button>
            <button onclick="filterProjects('streaming_graph')" class="px-2.5 py-1 rounded-md font-medium bg-slate-900 text-slate-400 hover:text-white border border-slate-700 proj-btn" data-cat="streaming_graph">Streaming & Graph ML</button>
          </div>
        </div>

        <!-- Projects List Container -->
        <div id="projectsList" class="space-y-8"></div>
      </div>
    </div>

    <!-- TAB 5: Technical Interview Question & Answer Bank (150 Questions) -->
    <div id="interviewTabContainer" class="hidden absolute inset-0 overflow-y-auto p-6 md:p-12 z-10 bg-[var(--background,#0b0f19)] text-[var(--foreground,#f8fafc)]">
      <div class="max-w-6xl mx-auto space-y-6 pb-20">
        <!-- Header -->
        <div class="border-b border-slate-700 pb-5 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-purple-500/20 text-purple-300 border border-purple-500/30 text-xs font-semibold uppercase tracking-wider mb-2">
              🎯 150 Technical Interview Questions & Answers
            </div>
            <h2 class="text-2xl md:text-3xl font-extrabold tracking-tight text-white">
              AI, Machine Learning, LLMs & Quant Interview Master Vault
            </h2>
            <p class="text-xs md:text-sm text-slate-400 mt-1">
              Top-Tier Questions from FAANG/MAANG, Frontier AI Labs (OpenAI, DeepMind), and Quant Funds (Jane Street, Citadel). Answers are hidden by default for active recall testing.
            </p>
          </div>

          <div class="flex items-center space-x-2 text-xs no-print">
            <button onclick="revealAllInterviewAnswers()" class="px-3 py-1.5 rounded-lg bg-purple-600/30 hover:bg-purple-600 text-purple-300 hover:text-white border border-purple-500/40 font-semibold transition flex items-center gap-1.5">
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
              <span>Reveal All</span>
            </button>
            <button onclick="hideAllInterviewAnswers()" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold border border-slate-700 transition flex items-center gap-1.5">
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l18 18"/></svg>
              <span>Hide All</span>
            </button>
          </div>
        </div>

        <!-- Search & Filter Controls -->
        <div class="space-y-3 no-print">
          <div class="relative max-w-md">
            <input id="qSearchInput" type="text" placeholder="Search 150 questions (e.g. RoPE, AdamW, KV-cache, Monty Hall, L1)..."
                   class="w-full bg-slate-900 border border-slate-700 text-xs text-white rounded-lg pl-8 pr-4 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500 placeholder-slate-500">
            <svg class="w-4 h-4 absolute left-2.5 top-2.5 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
          </div>

          <div class="flex items-center overflow-x-auto no-scrollbar max-w-full space-x-1.5 pb-1 text-xs flex-nowrap">
            <button onclick="filterInterviewCategory('all')" class="px-2.5 py-1 rounded-md font-medium bg-purple-600 text-white q-cat-btn active" data-cat="all">All (150)</button>
            <button onclick="filterInterviewCategory('ml')" class="px-2.5 py-1 rounded-md font-medium bg-slate-900 text-slate-400 hover:text-white border border-slate-700 q-cat-btn" data-cat="ml">Classical ML (25)</button>
            <button onclick="filterInterviewCategory('dl')" class="px-2.5 py-1 rounded-md font-medium bg-slate-900 text-slate-400 hover:text-white border border-slate-700 q-cat-btn" data-cat="dl">Deep Learning (25)</button>
            <button onclick="filterInterviewCategory('genai_llm')" class="px-2.5 py-1 rounded-md font-medium bg-slate-900 text-slate-400 hover:text-white border border-slate-700 q-cat-btn" data-cat="genai_llm">Transformers & LLMs (25)</button>
            <button onclick="filterInterviewCategory('rag')" class="px-2.5 py-1 rounded-md font-medium bg-slate-900 text-slate-400 hover:text-white border border-slate-700 q-cat-btn" data-cat="rag">RAG & Vector Search (20)</button>
            <button onclick="filterInterviewCategory('metrics_data')" class="px-2.5 py-1 rounded-md font-medium bg-slate-900 text-slate-400 hover:text-white border border-slate-700 q-cat-btn" data-cat="metrics_data">Metrics & Preprocessing (20)</button>
            <button onclick="filterInterviewCategory('system_mlops')" class="px-2.5 py-1 rounded-md font-medium bg-slate-900 text-slate-400 hover:text-white border border-slate-700 q-cat-btn" data-cat="system_mlops">MLOps & System Design (20)</button>
            <button onclick="filterInterviewCategory('logic_prob')" class="px-2.5 py-1 rounded-md font-medium bg-slate-900 text-slate-400 hover:text-white border border-slate-700 q-cat-btn" data-cat="logic_prob">Logic & Probability (15)</button>
          </div>
        </div>

        <!-- Questions List Container -->
        <div id="questionsContainer" class="space-y-4"></div>
      </div>
    </div>

    <!-- Inspector Drawer -->
    <div id="inspectorPanel" class="mobile-bottom-sheet absolute top-4 right-4 w-96 max-w-[calc(100vw-2rem)] max-h-[calc(100%-2rem)] bg-[var(--card,#1e293b)] border border-[var(--border,#334155)] rounded-2xl shadow-2xl p-5 overflow-y-auto flex flex-col gap-4 transform translate-x-full transition-transform duration-300 ease-out z-30">
      <div class="w-12 h-1.5 bg-slate-700 rounded-full mx-auto sm:hidden -mt-1 mb-1"></div>
      <div class="flex items-start justify-between">
        <div>
          <span id="inspBadge" class="badge bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">Machine Learning</span>
          <h2 id="inspTitle" class="text-lg font-bold text-white mt-1">Linear Regression</h2>
        </div>
        <button onclick="closeInspector()" class="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-700/50 transition">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
        </button>
      </div>

      <div class="text-xs text-slate-300 leading-relaxed space-y-3">
        <div>
          <h4 class="text-[11px] uppercase tracking-wider font-semibold text-slate-400 mb-1">📖 Simple Definition</h4>
          <p id="inspDefinition" class="bg-slate-900/60 p-3 rounded-lg border border-slate-800 text-slate-200">
            Definition goes here...
          </p>
        </div>

        <div id="inspMathSection">
          <h4 class="text-[11px] uppercase tracking-wider font-semibold text-indigo-400 mb-1">🔢 Mathematical Formula</h4>
          <div id="inspFormula" class="bg-indigo-950/40 p-3 rounded-lg border border-indigo-800/40 text-indigo-200 text-xs overflow-x-auto">
            Formula goes here...
          </div>
        </div>

        <div id="inspLogicSection">
          <h4 class="text-[11px] uppercase tracking-wider font-semibold text-amber-400 mb-1">💡 Important Logic & When to Use</h4>
          <div id="inspLogic" class="bg-amber-950/20 p-3 rounded-lg border border-amber-800/40 text-amber-200 text-xs leading-relaxed">
            Key intuition goes here...
          </div>
        </div>

        <div id="inspExampleSection">
          <h4 class="text-[11px] uppercase tracking-wider font-semibold text-emerald-400 mb-1">🎯 Simple Real-World Example</h4>
          <div id="inspExample" class="bg-emerald-950/20 p-3 rounded-lg border border-emerald-800/40 text-emerald-200 text-xs leading-relaxed">
            Concrete example goes here...
          </div>
        </div>

        <div id="inspSubtopicsSection">
          <h4 class="text-[11px] uppercase tracking-wider font-semibold text-blue-400 mb-1">📋 Key Components & Sub-topics</h4>
          <ul id="inspSubtopics" class="list-disc list-inside space-y-1 text-slate-300 pl-1 text-[12px]">
          </ul>
        </div>

        <div>
          <h4 class="text-[11px] uppercase tracking-wider font-semibold text-purple-400 mb-1">🔗 Interlinked Concepts</h4>
          <div id="inspCrossLinks" class="flex flex-wrap gap-1.5 pt-1">
          </div>
        </div>
      </div>
  <!-- Dedicated Concept Modal -->
  <div id="conceptModal" class="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-md hidden flex items-center justify-center p-3 md:p-6 transition-all duration-200">
    <div class="bg-slate-900 border border-slate-700/80 rounded-2xl w-full max-w-3xl max-h-[90vh] flex flex-col shadow-2xl overflow-hidden">
      <!-- Modal Header -->
      <div class="p-4 md:p-5 border-b border-slate-800 bg-slate-900/95 flex items-start justify-between gap-4">
        <div>
          <div class="flex items-center gap-2 text-xs mb-1">
            <span id="modalCategoryBadge" class="px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 font-semibold uppercase">Category</span>
            <span class="text-slate-500">›</span>
            <span id="modalTopicBadge" class="text-slate-400 font-medium">Topic</span>
          </div>
          <h2 id="modalConceptTitle" class="text-xl md:text-2xl font-bold text-white tracking-tight">Concept Title</h2>
          <p id="modalSubtext" class="text-xs text-slate-400 font-mono mt-0.5">Subtopic Terminology</p>
        </div>
        <div class="flex items-center gap-2 shrink-0">
          <a id="modalStandaloneLink" href="#" target="_blank" class="px-3 py-1.5 rounded-lg bg-indigo-600/30 hover:bg-indigo-600 text-indigo-300 hover:text-white border border-indigo-500/40 text-xs font-semibold flex items-center gap-1 transition">
            <span>Dedicated Page</span>
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg>
          </a>
          <button onclick="closeConceptModal()" class="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
          </button>
        </div>
      </div>

      <!-- Modal Body -->
      <div class="p-4 md:p-6 overflow-y-auto space-y-4 text-xs md:text-sm">
        <!-- 1. Definition -->
        <div class="space-y-1">
          <div class="text-[11px] font-bold text-blue-400 uppercase tracking-wider">📖 Simple Definition</div>
          <p id="modalDef" class="bg-slate-950/70 p-3.5 rounded-xl border border-slate-800/80 text-slate-200 leading-relaxed font-normal">
          </p>
        </div>

        <!-- 2. Formula -->
        <div id="modalFormulaSection" class="space-y-1">
          <div class="text-[11px] font-bold text-indigo-400 uppercase tracking-wider flex items-center justify-between">
            <span>🔢 Mathematical Formula</span>
            <span class="text-[10px] lowercase font-normal px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-300 border border-indigo-500/20">KaTeX</span>
          </div>
          <div class="formula-box bg-slate-950/90 p-4 rounded-xl border border-indigo-900/40 text-center overflow-x-auto">
            <div id="modalFormula" class="text-sm md:text-base text-indigo-100"></div>
            <div id="modalFormulaExpl" class="text-xs text-slate-400 mt-2 text-left pt-2 border-t border-slate-800/60"></div>
          </div>
        </div>

        <!-- 3. Logic -->
        <div id="modalLogicSection" class="space-y-1">
          <div class="text-[11px] font-bold text-amber-400 uppercase tracking-wider">💡 Important Logic & Intuition (When to Use)</div>
          <div id="modalLogic" class="bg-amber-950/20 p-3.5 rounded-xl border border-amber-800/40 text-amber-200/90 leading-relaxed font-normal">
          </div>
        </div>

        <!-- 4. Example -->
        <div id="modalExampleSection" class="space-y-1">
          <div class="text-[11px] font-bold text-emerald-400 uppercase tracking-wider">🎯 Simple Real-World Example</div>
          <div id="modalExample" class="bg-emerald-950/20 p-3.5 rounded-xl border border-emerald-800/40 text-emerald-200/90 leading-relaxed font-normal">
          </div>
        </div>
      </div>

      <!-- Modal Footer -->
      <div class="p-3 md:p-4 border-t border-slate-800 bg-slate-900/80 flex items-center justify-between">
        <button onclick="copyConceptModalLink()" id="modalCopyBtn" class="text-xs px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition flex items-center gap-1.5">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/></svg>
          <span>Copy Direct Link</span>
        </button>
        <button onclick="closeConceptModal()" class="text-xs px-4 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-white font-medium transition">
          Close
        </button>
      </div>
    </div>
  </div>

  <script>
    const GRAPH_DATA = {
      nodes: __NODES_JSON__,
      crossLinks: __LINKS_JSON__
    };

    const PAPERS_DATA = __PAPERS_JSON__;
    const PROJECTS_DATA = __PROJECTS_JSON__;
    const QUESTIONS_DATA = __QUESTIONS_JSON__;
    const CONCEPTS_DATA = __CONCEPTS_JSON__;

    const CONCEPTS_MAP = {};
    CONCEPTS_DATA.forEach(c => {
      CONCEPTS_MAP[c.id] = c;
      if (c.raw_sub) CONCEPTS_MAP[c.raw_sub] = c;
      if (c.title) CONCEPTS_MAP[c.title] = c;
    });

    function normStr(s) {
      return (s || '').toLowerCase().replace(/[^a-z0-9]/g, '');
    }

    function findConcept(query) {
      if (!query) return null;
      if (CONCEPTS_MAP[query]) return CONCEPTS_MAP[query];
      const q = normStr(query);
      return CONCEPTS_DATA.find(c => {
        const idN = normStr(c.id);
        const titleN = normStr(c.title);
        const subN = normStr(c.raw_sub);
        return idN === q || titleN === q || subN === q || subN.includes(q) || q.includes(subN) || titleN.includes(q) || q.includes(titleN);
      });
    }

    function openConceptModal(idOrQuery) {
      const c = findConcept(idOrQuery);
      if (!c) {
        window.location.href = `concept.html?id=${encodeURIComponent(idOrQuery)}`;
        return;
      }

      document.getElementById("modalConceptTitle").textContent = c.title;
      document.getElementById("modalSubtext").textContent = c.raw_sub || c.title;
      document.getElementById("modalCategoryBadge").textContent = c.category_label || "AI Core Concept";
      document.getElementById("modalTopicBadge").textContent = c.topic_label || "Topic";
      document.getElementById("modalDef").textContent = c.definition || c.def || "Core theoretical definition.";

      const fSec = document.getElementById("modalFormulaSection");
      const fEl = document.getElementById("modalFormula");
      const fExpl = document.getElementById("modalFormulaExpl");
      if (c.formula && c.formula.trim()) {
        fSec.style.display = "block";
        fEl.innerHTML = formatFormulaDisplay(c.formula);
        fExpl.textContent = c.formula_explanation || "";
        fExpl.style.display = c.formula_explanation ? "block" : "none";
        triggerMathRender(fSec);
      } else {
        fSec.style.display = "none";
      }

      document.getElementById("modalLogic").textContent = c.logic || "";
      document.getElementById("modalExample").textContent = c.example || "";

      const standLink = document.getElementById("modalStandaloneLink");
      standLink.href = `concept.html?id=${c.id}`;

      const modal = document.getElementById("conceptModal");
      modal.classList.remove("hidden");
      modal.dataset.currentId = c.id;

      history.replaceState({ tab: currentMainTab, concept: c.id }, "", `#concept/${c.id}`);
    }

    function closeConceptModal() {
      const modal = document.getElementById("conceptModal");
      modal.classList.add("hidden");
      if (window.location.hash.startsWith("#concept/")) {
        history.replaceState({ tab: currentMainTab }, "", `#${currentMainTab}`);
      }
    }

    function copyConceptModalLink() {
      const modal = document.getElementById("conceptModal");
      const id = modal.dataset.currentId || "";
      const url = `${window.location.origin}${window.location.pathname.replace(/index\\.html$/, '')}concept.html?id=${id}`;
      navigator.clipboard.writeText(url).then(() => {
        const btn = document.getElementById("modalCopyBtn");
        const orig = btn.innerHTML;
        btn.innerHTML = `<span class="text-emerald-400 font-bold">✓ Copied Direct Link!</span>`;
        setTimeout(() => { btn.innerHTML = orig; }, 1800);
      });
    }

    window.addEventListener("keydown", (e) => {
      if (e.key === "Escape") {
        closeConceptModal();
        closeInspector();
      }
    });

    let projectFilterCategory = "all";
    let projectSearchQuery = "";

    let interviewFilterCategory = "all";
    let interviewSearchQuery = "";
    let openQuestionsSet = new Set();
    let solvedQuestionsSet = new Set();

    const CATEGORY_COLORS = {
      center: { border: "#6366f1", bg: "#312e81", text: "#ffffff", stroke: "#818cf8" },
      math: { border: "#3b82f6", bg: "#1e3a8a", text: "#bfdbfe", stroke: "#60a5fa" },
      data: { border: "#10b981", bg: "#064e3b", text: "#a7f3d0", stroke: "#34d399" },
      ml: { border: "#8b5cf6", bg: "#4c1d95", text: "#ddd6fe", stroke: "#a78bfa" },
      eval: { border: "#06b6d4", bg: "#164e63", text: "#cffafe", stroke: "#22d3ee" },
      dl: { border: "#ec4899", bg: "#831843", text: "#fbcfe8", stroke: "#f472b6" },
      genai: { border: "#f59e0b", bg: "#78350f", text: "#fde68a", stroke: "#fbbf24" },
      mlops: { border: "#14b8a6", bg: "#134e4a", text: "#99f6e4", stroke: "#2dd4bf" }
    };

    let currentMainTab = "mindmap";
    let paperFilterCategory = "all";
    let paperSearchQuery = "";

    // Tab switcher & URL Router
    const TAB_METADATA = {
      mindmap: { title: "AI & ML Universe | Interactive Mind Map Explorer", bgClass: "bg-indigo-600 text-white" },
      syllabus: { title: "AI & ML Universe | Line-wise Master Syllabus", bgClass: "bg-blue-600 text-white" },
      papers: { title: "AI & ML Universe | Landmark Research Papers Hub", bgClass: "bg-amber-600 text-white" },
      projects: { title: "AI & ML Universe | Production AI Architectures & Case Studies", bgClass: "bg-emerald-600 text-white" },
      interview: { title: "AI & ML Universe | 150+ Technical Interview Questions Vault", bgClass: "bg-purple-600 text-white" }
    };

    function switchMainTab(tab, updateHistory = true, deepTarget = null) {
      if (!TAB_METADATA[tab]) tab = "mindmap";
      currentMainTab = tab;

      // Update Page Title
      if (TAB_METADATA[tab]) {
        document.title = TAB_METADATA[tab].title;
      }

      // Update URL route in address bar
      if (updateHistory) {
        const targetHash = deepTarget ? `#${tab}/${deepTarget}` : `#${tab}`;
        if (window.location.hash !== targetHash) {
          history.pushState({ tab: tab, deepTarget: deepTarget }, "", targetHash);
        }
      }

      const mindmapTab = document.getElementById("mindmapTabContainer");
      const syllabusTab = document.getElementById("printableDocContainer");
      const papersTab = document.getElementById("papersTabContainer");
      const projectsTab = document.getElementById("projectsTabContainer");
      const interviewTab = document.getElementById("interviewTabContainer");
      const mindmapToolbar = document.getElementById("mindmapToolbar");

      // Reset tab button states
      document.querySelectorAll("#navTabs button").forEach(btn => {
        btn.className = "px-3.5 py-1.5 rounded-lg text-xs font-semibold text-slate-300 hover:text-white transition flex items-center gap-1.5 whitespace-nowrap shrink-0";
      });

      const activeBtn = document.getElementById(`tabBtn-${tab}`);
      if (activeBtn) {
        activeBtn.className = `px-3.5 py-1.5 rounded-lg text-xs font-semibold transition flex items-center gap-1.5 ${TAB_METADATA[tab].bgClass} shadow whitespace-nowrap shrink-0`;
      }

      // Keep Download PDF button on Line-wise Syllabus page only
      const pdfBtn = document.getElementById("pdfBtn");
      if (pdfBtn) {
        if (tab === "syllabus") {
          pdfBtn.classList.remove("hidden");
        } else {
          pdfBtn.classList.add("hidden");
        }
      }

      if (tab === "mindmap") {
        mindmapTab.classList.remove("hidden");
        syllabusTab.classList.add("hidden");
        papersTab.classList.add("hidden");
        projectsTab.classList.add("hidden");
        if (interviewTab) interviewTab.classList.add("hidden");
        mindmapToolbar.classList.remove("hidden");
        if (deepTarget) {
          const matchNode = GRAPH_DATA.nodes.find(n => n.id === deepTarget);
          if (matchNode) {
            selectNode(matchNode);
            focusOnNode(matchNode);
          }
        }
      } else if (tab === "syllabus") {
        mindmapTab.classList.add("hidden");
        syllabusTab.classList.remove("hidden");
        papersTab.classList.add("hidden");
        projectsTab.classList.add("hidden");
        if (interviewTab) interviewTab.classList.add("hidden");
        mindmapToolbar.classList.add("hidden");
        buildLineWiseDocument();
        if (deepTarget) {
          setTimeout(() => {
            const el = document.getElementById(`syllabus-node-${deepTarget}`);
            if (el) el.scrollIntoView({ behavior: "smooth", block: "center" });
          }, 150);
        }
      } else if (tab === "papers") {
        mindmapTab.classList.add("hidden");
        syllabusTab.classList.add("hidden");
        papersTab.classList.remove("hidden");
        projectsTab.classList.add("hidden");
        if (interviewTab) interviewTab.classList.add("hidden");
        mindmapToolbar.classList.add("hidden");
        renderPapersList();
        if (deepTarget) {
          setTimeout(() => {
            const el = document.getElementById(`paper-card-${deepTarget}`);
            if (el) el.scrollIntoView({ behavior: "smooth", block: "center" });
          }, 150);
        }
      } else if (tab === "projects") {
        mindmapTab.classList.add("hidden");
        syllabusTab.classList.add("hidden");
        papersTab.classList.add("hidden");
        projectsTab.classList.remove("hidden");
        if (interviewTab) interviewTab.classList.add("hidden");
        mindmapToolbar.classList.add("hidden");
        renderProjectsList();
        if (deepTarget) {
          setTimeout(() => {
            const el = document.getElementById(`project-card-${deepTarget}`);
            if (el) el.scrollIntoView({ behavior: "smooth", block: "center" });
          }, 150);
        }
      } else if (tab === "interview") {
        mindmapTab.classList.add("hidden");
        syllabusTab.classList.add("hidden");
        papersTab.classList.add("hidden");
        projectsTab.classList.add("hidden");
        if (interviewTab) interviewTab.classList.remove("hidden");
        mindmapToolbar.classList.add("hidden");
        if (deepTarget) {
          const rawId = deepTarget.replace(/^q-?/, "");
          const found = QUESTIONS_DATA.find((q, idx) => q.id === rawId || String(idx + 1) === rawId || q.id === `ml_${rawId.padStart(2, '0')}`);
          if (found) {
            openQuestionsSet.add(found.id);
          }
        }
        renderQuestionsList();
        if (deepTarget) {
          setTimeout(() => {
            const rawId = deepTarget.replace(/^q-?/, "");
            const found = QUESTIONS_DATA.find((q, idx) => q.id === rawId || String(idx + 1) === rawId || q.id === `ml_${rawId.padStart(2, '0')}`);
            const targetId = found ? found.id : deepTarget;
            const el = document.getElementById(`q-card-${targetId}`) || document.getElementById(`q-card-${deepTarget}`);
            if (el) {
              el.scrollIntoView({ behavior: "smooth", block: "center" });
              el.classList.add("ring-2", "ring-purple-500");
              setTimeout(() => el.classList.remove("ring-2", "ring-purple-500"), 3000);
            }
          }, 200);
        }
      }
      setTimeout(() => { triggerMathRender(); }, 50);
    }

    function handleUrlRouting(isInitialLoad = false) {
      const urlParams = new URLSearchParams(window.location.search);
      let tab = urlParams.get("tab");
      let deepTarget = urlParams.get("id") || urlParams.get("q");

      const hash = window.location.hash.replace(/^#[/]?/, "");
      if (!tab && hash) {
        const parts = hash.split("/").map(p => p.trim()).filter(Boolean);
        if (parts.length > 0) {
          const first = parts[0].toLowerCase();
          if (first === "concept" && parts[1]) {
            switchMainTab("syllabus", false);
            setTimeout(() => openConceptModal(parts[1]), 100);
            return;
          } else if (["mindmap", "syllabus", "papers", "projects", "interview"].includes(first)) {
            tab = first;
            deepTarget = parts[1] || deepTarget;
          } else if (first.startsWith("q-") || (first.startsWith("q") && !isNaN(first.slice(1)))) {
            tab = "interview";
            deepTarget = first;
          } else {
            const matchConcept = findConcept(first);
            if (matchConcept) {
              switchMainTab("syllabus", false);
              setTimeout(() => openConceptModal(matchConcept.id), 100);
              return;
            }
            const matchNode = GRAPH_DATA.nodes.find(n => n.id === first);
            if (matchNode) {
              tab = "mindmap";
              deepTarget = first;
            }
          }
        }
      }

      if (!tab || !["mindmap", "syllabus", "papers", "projects", "interview"].includes(tab)) {
        tab = "mindmap";
      }

      if (isInitialLoad && !window.location.hash) {
        history.replaceState({ tab: tab }, "", `#${tab}`);
      }

      switchMainTab(tab, false, deepTarget);
    }

    function downloadActiveViewPDF() {
      if (currentMainTab === "mindmap") {
        switchMainTab("syllabus");
      }
      setTimeout(() => {
        window.print();
      }, 200);
    }

    // ----------------------------------------------------
    // LANDMARK PAPERS RENDERER
    // ----------------------------------------------------
    function renderPapersList() {
      const container = document.getElementById("papersList");
      if (!container) return;

      const filtered = PAPERS_DATA.filter(p => {
        if (paperFilterCategory !== "all" && p.category !== paperFilterCategory) {
          return false;
        }
        if (paperSearchQuery.trim()) {
          const q = paperSearchQuery.toLowerCase();
          const matchTitle = p.title.toLowerCase().includes(q);
          const matchAuthors = p.authors.toLowerCase().includes(q);
          const matchOneLiner = p.one_liner.toLowerCase().includes(q);
          const matchBreakthrough = p.breakthrough.toLowerCase().includes(q);
          return matchTitle || matchAuthors || matchOneLiner || matchBreakthrough;
        }
        return true;
      });

      if (filtered.length === 0) {
        container.innerHTML = `<div class="p-8 text-center text-slate-500 bg-slate-900/50 rounded-xl border border-slate-800">No matching research papers found. Try adjusting your search query.</div>`;
        return;
      }

      let html = "";
      filtered.forEach((p, idx) => {
        const paperId = p.id || ('paper-' + (idx + 1));
        html += `
          <div id="paper-card-${paperId}" class="print-card bg-slate-900/80 border border-slate-800 rounded-2xl p-5 shadow-lg space-y-3 transition hover:border-slate-700 scroll-mt-20">
            <div class="flex items-start justify-between flex-wrap gap-2">
              <div class="space-y-1">
                <div class="flex items-center flex-wrap gap-2">
                  <span class="px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 border border-amber-500/30 text-[11px] font-bold">
                    ${p.year}
                  </span>
                  <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700 text-[11px] font-medium">
                    ${p.institution}
                  </span>
                  <span class="text-xs text-slate-400 italic">
                    ${p.authors}
                  </span>
                </div>
                <h3 class="text-base md:text-lg font-bold text-white hover:text-indigo-300 transition flex items-center gap-2">
                  <a href="${p.url}" target="_blank" rel="noopener noreferrer" class="hover:underline flex items-center gap-1.5">
                    <span>${p.title}</span>
                    <svg class="w-4 h-4 text-slate-400 hover:text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg>
                  </a>
                </h3>
              </div>
              <a href="${p.url}" target="_blank" rel="noopener noreferrer" class="no-print px-3 py-1.5 rounded-lg bg-indigo-600/30 hover:bg-indigo-600 text-indigo-300 hover:text-white border border-indigo-500/40 text-xs font-semibold flex items-center gap-1 transition">
                <span>Read on arXiv</span>
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
              </a>
            </div>

            <!-- One-liner intuition -->
            <div class="p-2.5 rounded-lg bg-amber-950/30 border border-amber-800/40 text-amber-200 text-xs font-medium">
              💡 <span class="font-semibold text-amber-100">Key Takeaway:</span> ${p.one_liner}
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
              <div class="bg-slate-950/40 p-3 rounded-lg border border-slate-800/80">
                <span class="font-semibold text-rose-400 uppercase text-[10px] tracking-wider block mb-1">The Problem It Solved</span>
                <p class="text-slate-300 leading-relaxed">${p.problem}</p>
              </div>

              <div class="bg-slate-950/40 p-3 rounded-lg border border-slate-800/80">
                <span class="font-semibold text-emerald-400 uppercase text-[10px] tracking-wider block mb-1">The Game-Changing Breakthrough</span>
                <p class="text-slate-300 leading-relaxed">${p.breakthrough}</p>
              </div>
            </div>

            <!-- Formula -->
            <div class="bg-slate-950/60 p-2.5 rounded-lg border border-slate-800 text-xs text-indigo-200 overflow-x-auto">
              <span class="text-indigo-400 font-sans font-semibold text-[10px] uppercase tracking-wider block mb-0.5">Core Mathematical Formulation / Mechanism:</span>
              <div class="my-1">${p.formula}</div>
            </div>

            <!-- Historical Impact -->
            <div class="text-xs text-slate-300 pt-1 border-t border-slate-800/80 flex items-start gap-2">
              <span class="text-purple-400 font-semibold flex-shrink-0">🚀 Modern Legacy:</span>
              <span class="text-slate-300">${p.impact}</span>
            </div>
          </div>
        `;
      });

      container.innerHTML = html;
      triggerMathRender(container);
    }

    function filterPapers(cat) {
      paperFilterCategory = cat;
      document.querySelectorAll(".paper-btn").forEach(btn => {
        if (btn.dataset.cat === cat) {
          btn.className = "px-2.5 py-1 rounded-md font-medium bg-amber-600 text-white paper-btn active";
        } else {
          btn.className = "px-2.5 py-1 rounded-md font-medium bg-slate-900 text-slate-400 hover:text-white border border-slate-700 paper-btn";
        }
      });
      renderPapersList();
    }


    // ----------------------------------------------------
    // ENTERPRISE PRODUCTION PROJECTS RENDERER
    // ----------------------------------------------------
    function escapeHtml(str) {
      if (!str) return "";
      return str
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
    }

    function renderProjectsList() {
      const container = document.getElementById("projectsList");
      if (!container) return;

      const filtered = PROJECTS_DATA.filter(p => {
        if (projectFilterCategory !== "all" && p.category !== projectFilterCategory) {
          return false;
        }
        if (projectSearchQuery.trim()) {
          const q = projectSearchQuery.toLowerCase();
          const matchTitle = p.title.toLowerCase().includes(q);
          const matchSub = p.subtitle.toLowerCase().includes(q);
          const matchTech = p.tech_stack.some(t => t.toLowerCase().includes(q));
          return matchTitle || matchSub || matchTech;
        }
        return true;
      });

      if (filtered.length === 0) {
        container.innerHTML = `<div class="p-8 text-center text-slate-500 bg-slate-900/50 rounded-xl border border-slate-800">No matching projects found. Try searching for LightGBM, Pinecone, or CLIP.</div>`;
        return;
      }

      let html = "";
      filtered.forEach((p, idx) => {
        const techChips = p.tech_stack.map(t => 
          `<span class="px-2 py-0.5 rounded-md bg-slate-800/90 text-slate-300 border border-slate-700 text-[11px] font-mono font-medium">${t}</span>`
        ).join("");

        const highlights = p.key_highlights.map(h => 
          `<li class="flex items-start gap-2 text-xs text-slate-300 leading-relaxed">
            <span class="text-emerald-400 mt-0.5 font-bold">✔</span>
            <span>${h}</span>
          </li>`
        ).join("");

        const components = p.system_components.map(c => 
          `<div class="bg-slate-950/60 p-3 rounded-xl border border-slate-800/80">
            <h5 class="text-xs font-bold text-indigo-300">${c.name}</h5>
            <p class="text-[11px] text-slate-400 mt-1 leading-relaxed">${c.desc}</p>
          </div>`
        ).join("");

        const projId = p.id || ('proj-' + (idx + 1));
        html += `
          <div id="project-card-${projId}" class="print-card bg-slate-900/90 border border-slate-800 rounded-2xl p-6 md:p-8 space-y-6 shadow-xl transition hover:border-slate-700 scroll-mt-20">
            <!-- Header -->
            <div class="space-y-3">
              <div class="flex flex-wrap items-center justify-between gap-3">
                <span class="px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-xs font-bold uppercase tracking-wider">
                  ${p.badge}
                </span>
                <div class="flex flex-wrap gap-1.5">
                  ${techChips}
                </div>
              </div>

              <div>
                <h3 class="text-xl md:text-2xl font-extrabold text-white tracking-tight">${p.title}</h3>
                <p class="text-xs md:text-sm text-slate-300 mt-1.5 leading-relaxed">${p.subtitle}</p>
              </div>
            </div>

            <!-- Highlights & Components -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-5">
              <div class="bg-slate-950/40 p-4 rounded-xl border border-slate-800/60 space-y-3">
                <h4 class="text-xs uppercase tracking-wider font-bold text-emerald-400 flex items-center gap-1.5">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                  Architectural Highlights & Capabilities
                </h4>
                <ul class="space-y-2">
                  ${highlights}
                </ul>
              </div>

              <div class="bg-slate-950/40 p-4 rounded-xl border border-slate-800/60 space-y-3">
                <h4 class="text-xs uppercase tracking-wider font-bold text-indigo-400 flex items-center gap-1.5">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/></svg>
                  Core System Components
                </h4>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                  ${components}
                </div>
              </div>
            </div>

            <!-- Architecture Diagram -->
            <div class="bg-slate-950/70 p-5 rounded-xl border border-slate-800/80 space-y-3">
              <div class="flex items-center justify-between">
                <h4 class="text-xs uppercase tracking-wider font-bold text-amber-400 flex items-center gap-1.5">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4"/></svg>
                  End-to-End System Architecture Flow
                </h4>
                <span class="text-[11px] text-slate-500 font-mono">Mermaid Flowchart</span>
              </div>
              <div class="mermaid bg-[#090d16] p-4 rounded-lg border border-slate-800 overflow-x-auto text-center text-xs">
${p.mermaid_diagram}
              </div>
            </div>

            <!-- Code Section -->
            <div class="space-y-2">
              <div class="flex flex-wrap items-center justify-between gap-3 bg-slate-950 px-4 py-2.5 rounded-t-xl border-t border-x border-slate-800">
                <div class="flex items-center space-x-2">
                  <span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span>
                  <span class="text-xs font-mono font-bold text-emerald-400">${p.id}.py</span>
                  <span class="text-[11px] text-slate-400 hidden sm:inline">&bull; Complete & Copy-Pasteable Implementation</span>
                </div>
                <div class="flex items-center space-x-2">
                  <button onclick="toggleProjectCode('${p.id}')" id="toggleProjBtn-${p.id}" class="px-2.5 py-1 text-slate-400 hover:text-white text-xs font-semibold rounded bg-slate-800/60 hover:bg-slate-800 transition">
                    Collapse Code
                  </button>
                  <button onclick="copyProjectCode('${p.id}')" id="copyProjBtn-${p.id}" class="px-3.5 py-1 text-xs font-semibold rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white flex items-center gap-1.5 shadow transition">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"/></svg>
                    <span>Copy Full Code</span>
                  </button>
                </div>
              </div>

              <div id="codeWrapper-${p.id}" class="relative">
                <pre class="bg-[#050811] p-4 rounded-b-xl border border-slate-800 text-[11px] font-mono text-emerald-300/90 overflow-x-auto max-h-[500px] leading-relaxed"><code id="codeBlock-${p.id}">${escapeHtml(p.code_snippet)}</code></pre>
              </div>
            </div>
          </div>
        `;
      });

      container.innerHTML = html;

      // Render mermaid diagrams
      setTimeout(() => {
        try {
          if (window.mermaid) {
            window.mermaid.run();
          }
        } catch (e) {
          console.warn("Mermaid error:", e);
        }
      }, 50);
    }

    function filterProjects(cat) {
      projectFilterCategory = cat;
      document.querySelectorAll(".proj-btn").forEach(btn => {
        if (btn.dataset.cat === cat) {
          btn.className = "px-2.5 py-1 rounded-md font-medium bg-emerald-600 text-white proj-btn active";
        } else {
          btn.className = "px-2.5 py-1 rounded-md font-medium bg-slate-900 text-slate-400 hover:text-white border border-slate-700 proj-btn";
        }
      });
      renderProjectsList();
    }

    function copyProjectCode(projId) {
      const codeElem = document.getElementById(`codeBlock-${projId}`);
      const btn = document.getElementById(`copyProjBtn-${projId}`);
      if (!codeElem || !btn) return;

      navigator.clipboard.writeText(codeElem.innerText).then(() => {
        const origHTML = btn.innerHTML;
        btn.innerHTML = `
          <svg class="w-3.5 h-3.5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
          <span>Copied!</span>
        `;
        btn.classList.remove("bg-emerald-600", "hover:bg-emerald-500");
        btn.classList.add("bg-teal-500");

        setTimeout(() => {
          btn.innerHTML = origHTML;
          btn.classList.remove("bg-teal-500");
          btn.classList.add("bg-emerald-600", "hover:bg-emerald-500");
        }, 2200);
      });
    }

    function toggleProjectCode(projId) {
      const wrapper = document.getElementById(`codeWrapper-${projId}`);
      const btn = document.getElementById(`toggleProjBtn-${projId}`);
      if (!wrapper || !btn) return;

      if (wrapper.classList.contains("hidden")) {
        wrapper.classList.remove("hidden");
        btn.innerText = "Collapse Code";
      } else {
        wrapper.classList.add("hidden");
        btn.innerText = "Expand Code";
      }
    }


    // ----------------------------------------------------
    // MATHEMATICAL TYPESETTING ENGINE (KaTeX + Offline Fallback)
    // ----------------------------------------------------
    function triggerMathRender(rootElement) {
      const target = rootElement || document.body;
      if (typeof renderMathInElement === 'function') {
        try {
          renderMathInElement(target, {
            delimiters: [
              { left: '$$', right: '$$', display: true },
              { left: '$', right: '$', display: false },
              { left: '\\(', right: '\\)', display: false },
              { left: '\\[', right: '\\]', display: true }
            ],
            throwOnError: false,
            errorColor: '#f43f5e'
          });
        } catch (e) {
          console.warn('KaTeX rendering error:', e);
        }
      } else {
        fallbackFormatFormulas(target);
      }
    }

    function fallbackFormatFormulas(target) {
      if (!target) return;
      const walker = document.createTreeWalker(target, NodeFilter.SHOW_TEXT, null, false);
      const nodesToReplace = [];
      let n;
      while (n = walker.nextNode()) {
        if (n.nodeValue && n.nodeValue.includes('$')) {
          nodesToReplace.push(n);
        }
      }
      nodesToReplace.forEach(node => {
        const parent = node.parentNode;
        if (!parent || parent.tagName === 'SCRIPT' || parent.tagName === 'STYLE') return;
        const original = node.nodeValue;
        const replaced = original.replace(/\\$([^\\$\\n]+?)\\$/g, function(_, eq) {
          let clean = eq
            .replace(/\\\\frac\\{([^}]+)\\}\\{([^}]+)\\}/g, '<span style="display:inline-flex;flex-direction:column;vertical-align:middle;text-align:center;font-size:0.9em;padding:0 2px;"><span style="border-bottom:1.5px solid #818cf8;padding:0 2px;">$1</span><span style="padding:0 2px;">$2</span></span>')
            .replace(/\\\\lambda/g, 'λ')
            .replace(/\\\\theta/g, 'θ')
            .replace(/\\\\sigma/g, 'σ')
            .replace(/\\\\mu/g, 'μ')
            .replace(/\\\\pi/g, 'π')
            .replace(/\\\\eta/g, 'η')
            .replace(/\\\\beta/g, 'β')
            .replace(/\\\\gamma/g, 'γ')
            .replace(/\\\\Omega/g, 'Ω')
            .replace(/\\\\min/g, 'min')
            .replace(/\\\\max/g, 'max')
            .replace(/\\\\sum/g, '∑')
            .replace(/\\\\partial/g, '∂')
            .replace(/\\\\le|\\\\leq/g, '≤')
            .replace(/\\\\ge|\\\\geq/g, '≥')
            .replace(/\\\\to/g, '→')
            .replace(/\\\\pm/g, '±')
            .replace(/\\\\neq/g, '≠')
            .replace(/\\\\cdot/g, '·')
            .replace(/\\\\in/g, '∈')
            .replace(/\\\\approx/g, '≈')
            .replace(/\\\\sqrt\\{([^}]+)\\}/g, '√($1)')
            .replace(/\\\\|/g, '‖')
            .replace(/\\^2/g, '²')
            .replace(/_\\{([^}]+)\\}/g, '<sub>$1</sub>')
            .replace(/_([a-zA-Z0-9])/g, '<sub>$1</sub>');
          return `<span class="math-fallback font-serif text-indigo-200">${clean}</span>`;
        });
        if (replaced !== original) {
          const span = document.createElement('span');
          span.innerHTML = replaced;
          parent.replaceChild(span, node);
        }
      });
    }

    function formatFormulaDisplay(rawFormula) {
      if (!rawFormula) return "";
      if (rawFormula.includes("$$")) {
        return rawFormula;
      }
      if (rawFormula.includes("$")) {
        return rawFormula;
      }

      const parts = rawFormula.split(" | ");
      return parts.map(p => {
        let text = p.trim();
        let label = "";
        const colonIdx = text.indexOf(": ");
        if (colonIdx > 0 && colonIdx < 30) {
          label = `<span class="text-indigo-400 font-semibold font-sans text-[11px] block mb-0.5">${text.substring(0, colonIdx + 1)}</span>`;
          text = text.substring(colonIdx + 2).trim();
        }

        let latex = text
          .replace(/λ/g, "\\lambda ")
          .replace(/θ/g, "\\theta ")
          .replace(/σ\\^2|σ²/g, "\\\\sigma^2 ")
          .replace(/σ/g, "\\sigma ")
          .replace(/μ/g, "\\mu ")
          .replace(/π/g, "\\pi ")
          .replace(/η/g, "\\eta ")
          .replace(/β_1/g, "\\beta_1 ")
          .replace(/β_2/g, "\\beta_2 ")
          .replace(/β_t/g, "\\beta_t ")
          .replace(/β/g, "\\beta ")
          .replace(/γ/g, "\\gamma ")
          .replace(/Ω/g, "\\Omega ")
          .replace(/∇_w/g, "\\nabla_w ")
          .replace(/∇/g, "\\nabla ")
          .replace(/∈/g, "\\in ")
          .replace(/≈/g, "\\approx ")
          .replace(/≠/g, "\\neq ")
          .replace(/≤|<=/g, "\\le ")
          .replace(/≥|>=/g, "\\ge ")
          .replace(/->/g, "\\to ")
          .replace(/·/g, "\\cdot ")
          .replace(/∑/g, "\\sum ")
          .replace(/√([a-zA-Z0-9_]+)/g, "\\sqrt{$1}")
          .replace(/√\\((.*?)\\)/g, "\\\\sqrt{$1}")
          .replace(/\\|\\|/g, "\\\\|")
          .replace(/:=/g, "\\leftarrow ");

        latex = latex.replace(/\\[([^\\]]+)\\]\\s*\\/\\s*([a-zA-Z0-9_\\(\\)]+)/g, "\\\\frac{$1}{$2}");
        latex = latex.replace(/\\(([^)]+)\\)\\s*\\/\\s*([a-zA-Z0-9_\\(\\)]+)/g, "\\\\frac{$1}{$2}");

        return `${label}<div class="katex-display-box my-1">$$${latex}$$</div>`;
      }).join("");
    }

    // ----------------------------------------------------
    // 150 INTERVIEW QUESTIONS & ANSWERS RENDERER
    // ----------------------------------------------------
    function formatAnswerMarkdown(text) {
      if (!text) return "";

      // 1. Protect display math $$ ... $$ and inline math $ ... $
      const mathTokens = [];
      
      let tokenized = text.replace(/\\$\\$([\\s\\S]*?)\\$\\$/g, function(_, math) {
        const key = `@@@MATH_DISP_${mathTokens.length}@@@`;
        mathTokens.push({ type: 'display', code: math });
        return key;
      });

      tokenized = tokenized.replace(/\\$([^\\$\\n]+?)\\$/g, function(_, math) {
        const key = `@@@MATH_INL_${mathTokens.length}@@@`;
        mathTokens.push({ type: 'inline', code: math });
        return key;
      });

      // 2. Format standard Markdown safely
      let html = tokenized
        .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
        .replace(/\\*\\*(.*?)\\*\\*/g, '<strong class="text-white font-bold">$1</strong>')
        .replace(/\\*(.*?)\\*/g, '<em class="text-slate-300 italic">$1</em>')
        .replace(/`([^`]+)`/g, '<code class="px-1.5 py-0.5 rounded bg-slate-800 text-purple-300 text-xs font-mono">$1</code>')
        .replace(/\\n\\n/g, '<div class="my-2.5"></div>')
        .replace(/\\n- /g, '<br>&bull; ')
        .replace(/\\n/g, '<br>');

      // 3. Restore math expressions with renderable KaTeX delimiters
      html = html.replace(/@@@MATH_DISP_(\\d+)@@@/g, function(_, id) {
        const item = mathTokens[parseInt(id, 10)];
        return `<div class="katex-display-box formula-box text-center">$$${item.code}$$</div>`;
      });

      html = html.replace(/@@@MATH_INL_(\\d+)@@@/g, function(_, id) {
        const item = mathTokens[parseInt(id, 10)];
        return `<span class="katex-inline-formula">$${item.code}$</span>`;
      });

      return html;
    }

    function renderQuestionsList() {
      const container = document.getElementById("questionsContainer");
      if (!container) return;

      const filtered = QUESTIONS_DATA.filter(q => {
        if (interviewFilterCategory !== "all" && q.category !== interviewFilterCategory) {
          return false;
        }
        if (interviewSearchQuery.trim()) {
          const term = interviewSearchQuery.toLowerCase();
          const matchQ = q.question.toLowerCase().includes(term);
          const matchA = q.answer.toLowerCase().includes(term);
          const matchCat = q.category_label.toLowerCase().includes(term);
          const matchCompany = q.company_tags.some(c => c.toLowerCase().includes(term));
          return matchQ || matchA || matchCat || matchCompany;
        }
        return true;
      });

      if (filtered.length === 0) {
        container.innerHTML = `<div class="p-8 text-center text-slate-500 bg-slate-900/50 rounded-xl border border-slate-800">No matching questions found. Try searching for 'RoPE', 'AdamW', 'L1', or 'Monty Hall'.</div>`;
        return;
      }

      let html = "";
      filtered.forEach((q, idx) => {
        const isOpen = openQuestionsSet.has(q.id);
        const isSolved = solvedQuestionsSet.has(q.id);
        const companyChips = q.company_tags.map(c => 
          `<span class="px-2 py-0.5 rounded-md bg-slate-800/80 text-slate-300 border border-slate-700 text-[10px] font-medium">${c}</span>`
        ).join("");

        const diffColors = {
          "Junior / Mid": "bg-blue-500/20 text-blue-300 border-blue-500/30",
          "Mid / Senior": "bg-indigo-500/20 text-indigo-300 border-indigo-500/30",
          "Senior": "bg-purple-500/20 text-purple-300 border-purple-500/30",
          "Senior / Staff": "bg-pink-500/20 text-pink-300 border-pink-500/30",
          "Quant / Research": "bg-amber-500/20 text-amber-300 border-amber-500/30"
        };
        const diffClass = diffColors[q.difficulty] || "bg-slate-800 text-slate-300 border-slate-700";

        html += `
          <div id="q-card-${q.id}" data-qid="${q.id}" class="print-card bg-slate-900/90 border ${isSolved ? 'border-emerald-600/40' : 'border-slate-800'} rounded-2xl p-5 md:p-6 space-y-4 shadow-lg transition hover:border-slate-700 scroll-mt-20">
            <!-- Header Row -->
            <div class="flex items-start justify-between flex-wrap gap-2">
              <div class="flex items-center flex-wrap gap-2">
                <span class="px-2.5 py-0.5 rounded-full text-[11px] font-bold border ${diffClass}">
                  ${q.difficulty}
                </span>
                <span class="px-2.5 py-0.5 rounded-full bg-slate-800 text-slate-300 border border-slate-700 text-[11px] font-semibold">
                  ${q.category_label}
                </span>
                <div class="flex items-center gap-1">
                  ${companyChips}
                </div>
              </div>

              <div class="flex items-center space-x-2 no-print">
                <label class="flex items-center space-x-1.5 cursor-pointer text-xs text-slate-400 hover:text-white">
                  <input type="checkbox" onchange="toggleInterviewSolved('${q.id}')" ${isSolved ? 'checked' : ''}
                         class="rounded border-slate-700 text-emerald-500 focus:ring-emerald-500">
                  <span class="${isSolved ? 'text-emerald-400 font-semibold' : ''}">${isSolved ? 'Mastered' : 'Mark Solved'}</span>
                </label>
              </div>
            </div>

            <!-- Question Title -->
            <h3 class="text-base md:text-lg font-bold text-white leading-snug">
              <span class="text-purple-400 font-mono mr-1.5">Q${idx + 1}.</span> ${q.question}
            </h3>

            <!-- Toggle Answer Button -->
            <div class="pt-1 no-print">
              <button onclick="toggleInterviewAnswer('${q.id}')" id="btn-ans-${q.id}"
                      class="px-4 py-2 rounded-xl text-xs font-semibold flex items-center gap-2 transition ${isOpen ? 'bg-slate-800 text-slate-300 hover:text-white' : 'bg-purple-600 hover:bg-purple-500 text-white shadow-lg shadow-purple-600/20'}">
                <svg class="w-4 h-4 transform transition-transform ${isOpen ? 'rotate-180' : ''}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                </svg>
                <span>${isOpen ? 'Hide Detailed Answer' : '💡 Reveal Answer & Explanation'}</span>
              </button>
            </div>

            <!-- Answer Section (Hidden Initially) -->
            <div id="ans-box-${q.id}" class="${isOpen ? '' : 'hidden'} print:block pt-2 space-y-4 border-t border-slate-800/80">
              <div class="bg-slate-950/80 p-5 rounded-xl border border-slate-800 text-slate-200 text-xs md:text-sm leading-relaxed space-y-2">
                ${formatAnswerMarkdown(q.answer)}
              </div>

              ${q.tip ? `
                <div class="p-3.5 rounded-xl bg-amber-950/30 border border-amber-800/40 text-amber-200 text-xs flex items-start gap-2.5">
                  <span class="text-base flex-shrink-0">⭐</span>
                  <div>
                    <strong class="text-amber-100 font-semibold block mb-0.5">Interviewer Evaluation Tip:</strong>
                    <span>${q.tip}</span>
                  </div>
                </div>
              ` : ''}
            </div>
          </div>
        `;
      });

      container.innerHTML = html;
      triggerMathRender(container);
    }

    function toggleInterviewAnswer(id) {
      if (openQuestionsSet.has(id)) {
        openQuestionsSet.delete(id);
      } else {
        openQuestionsSet.add(id);
        if (currentMainTab === "interview") {
          history.replaceState({ tab: 'interview', deepTarget: id }, "", `#interview/q-${id}`);
        }
      }
      renderQuestionsList();
    }

    function revealAllInterviewAnswers() {
      QUESTIONS_DATA.forEach(q => openQuestionsSet.add(q.id));
      renderQuestionsList();
    }

    function hideAllInterviewAnswers() {
      openQuestionsSet.clear();
      renderQuestionsList();
    }

    function toggleInterviewSolved(id) {
      if (solvedQuestionsSet.has(id)) {
        solvedQuestionsSet.delete(id);
      } else {
        solvedQuestionsSet.add(id);
      }
      renderQuestionsList();
    }

    function filterInterviewCategory(cat) {
      interviewFilterCategory = cat;
      document.querySelectorAll(".q-cat-btn").forEach(btn => {
        if (btn.dataset.cat === cat) {
          btn.className = "px-2.5 py-1 rounded-md font-medium bg-purple-600 text-white q-cat-btn active";
        } else {
          btn.className = "px-2.5 py-1 rounded-md font-medium bg-slate-900 text-slate-400 hover:text-white border border-slate-700 q-cat-btn";
        }
      });
      renderQuestionsList();
    }

    // Mind Map Canvas Engine
    let state = {
      zoom: 0.85,
      panX: window.innerWidth / 2,
      panY: window.innerHeight / 2,
      isDragging: false,
      startX: 0,
      startY: 0,
      activeDomain: "all",
      searchQuery: "",
      showCrossLinks: true,
      selectedNodeId: null
    };

    const worldGroup = document.getElementById("worldGroup");
    const viewport = document.getElementById("mindmapViewport");
    const linksHierarchyGroup = document.getElementById("linksHierarchyGroup");
    const linksCrossGroup = document.getElementById("linksCrossGroup");
    const nodesGroup = document.getElementById("nodesGroup");

    function updateTransform() {
      worldGroup.setAttribute("transform", `translate(${state.panX}, ${state.panY}) scale(${state.zoom})`);
    }

    
    // Mobile Touch Gesture Support (Single-finger Pan & Two-finger Pinch Zoom)
    let lastTouchDist = 0;
    viewport.addEventListener("touchstart", (e) => {
      if (e.target.closest(".node-group")) return;
      if (e.touches.length === 1) {
        state.isDragging = true;
        state.startX = e.touches[0].clientX - state.panX;
        state.startY = e.touches[0].clientY - state.panY;
      } else if (e.touches.length === 2) {
        lastTouchDist = Math.hypot(
          e.touches[0].clientX - e.touches[1].clientX,
          e.touches[0].clientY - e.touches[1].clientY
        );
      }
    }, { passive: true });

    window.addEventListener("touchmove", (e) => {
      if (currentMainTab !== "mindmap") return;
      if (e.touches.length === 1 && state.isDragging) {
        state.panX = e.touches[0].clientX - state.startX;
        state.panY = e.touches[0].clientY - state.startY;
        updateTransform();
      } else if (e.touches.length === 2) {
        const dist = Math.hypot(
          e.touches[0].clientX - e.touches[1].clientX,
          e.touches[0].clientY - e.touches[1].clientY
        );
        if (lastTouchDist > 0) {
          const delta = (dist - lastTouchDist) * 0.006;
          zoom(delta);
        }
        lastTouchDist = dist;
      }
    }, { passive: true });

    window.addEventListener("touchend", () => {
      state.isDragging = false;
      lastTouchDist = 0;
    });
    
    viewport.addEventListener("mousedown", (e) => {
      if (e.target.closest(".node-group")) return;
      state.isDragging = true;
      state.startX = e.clientX - state.panX;
      state.startY = e.clientY - state.panY;
      viewport.classList.remove("grab-cursor");
      viewport.classList.add("grabbing-cursor");
    });

    window.addEventListener("mousemove", (e) => {
      if (!state.isDragging) return;
      state.panX = e.clientX - state.startX;
      state.panY = e.clientY - state.startY;
      updateTransform();
    });

    window.addEventListener("mouseup", () => {
      state.isDragging = false;
      viewport.classList.remove("grabbing-cursor");
      viewport.classList.add("grab-cursor");
    });

    viewport.addEventListener("wheel", (e) => {
      e.preventDefault();
      const zoomFactor = e.deltaY < 0 ? 1.1 : 0.9;
      const mouseX = e.clientX;
      const mouseY = e.clientY;

      const newZoom = Math.min(Math.max(state.zoom * zoomFactor, 0.25), 2.5);
      state.panX = mouseX - (mouseX - state.panX) * (newZoom / state.zoom);
      state.panY = mouseY - (mouseY - state.panY) * (newZoom / state.zoom);
      state.zoom = newZoom;
      updateTransform();
    }, { passive: false });

    function zoom(delta) {
      const newZoom = Math.min(Math.max(state.zoom + delta, 0.25), 2.5);
      const centerX = window.innerWidth / 2;
      const centerY = window.innerHeight / 2;
      state.panX = centerX - (centerX - state.panX) * (newZoom / state.zoom);
      state.panY = centerY - (centerY - state.panY) * (newZoom / state.zoom);
      state.zoom = newZoom;
      updateTransform();
    }

    function resetZoom() {
      state.zoom = 0.85;
      state.panX = window.innerWidth / 2;
      state.panY = window.innerHeight / 2;
      updateTransform();
    }

    function toggleInterlinks() {
      state.showCrossLinks = !state.showCrossLinks;
      document.getElementById("interlinksBtn").innerText = `Links: ${state.showCrossLinks ? 'ON' : 'OFF'}`;
      document.getElementById("interlinksBtn").className = state.showCrossLinks
        ? "p-1 rounded bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 px-2 font-medium hover:bg-indigo-500/30 transition"
        : "p-1 rounded bg-slate-800 text-slate-400 border border-slate-700 px-2 font-medium hover:bg-slate-700 transition";
      renderLinks();
    }

    function render() {
      renderNodes();
      renderLinks();
      updateTransform();
    }

    function renderNodes() {
      nodesGroup.innerHTML = "";
      const filtered = GRAPH_DATA.nodes.filter(n => {
        if (state.activeDomain !== "all" && n.category !== "center" && n.category !== state.activeDomain) {
          return false;
        }
        if (state.searchQuery.trim()) {
          const q = state.searchQuery.toLowerCase();
          const matchLabel = n.label.toLowerCase().includes(q);
          const matchDef = n.def && n.def.toLowerCase().includes(q);
          const matchSub = n.subtopics && n.subtopics.some(s => s.toLowerCase().includes(q));
          return matchLabel || matchDef || matchSub;
        }
        return true;
      });

      filtered.forEach(node => {
        const theme = CATEGORY_COLORS[node.category] || CATEGORY_COLORS.center;
        const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
        g.setAttribute("class", "node-group cursor-pointer transition-all duration-200");
        g.setAttribute("transform", `translate(${node.x}, ${node.y})`);
        g.setAttribute("id", `node-${node.id}`);

        const isCenter = node.level === 0;
        const isL1 = node.level === 1;
        const width = isCenter ? 260 : isL1 ? 240 : 210;
        const height = isCenter ? 75 : isL1 ? 65 : 55;

        const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
        rect.setAttribute("x", -width / 2);
        rect.setAttribute("y", -height / 2);
        rect.setAttribute("width", width);
        rect.setAttribute("height", height);
        rect.setAttribute("rx", isCenter ? "16" : "12");
        rect.setAttribute("fill", theme.bg);
        rect.setAttribute("stroke", theme.border);
        rect.setAttribute("stroke-width", isCenter ? "3" : isL1 ? "2.5" : "1.5");
        rect.setAttribute("filter", "drop-shadow(0 4px 6px rgba(0,0,0,0.3))");

        const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
        text.setAttribute("x", "0");
        text.setAttribute("y", isCenter ? "-4" : isL1 ? "-6" : "-4");
        text.setAttribute("text-anchor", "middle");
        text.setAttribute("fill", "#ffffff");
        text.setAttribute("font-size", isCenter ? "14" : isL1 ? "12.5" : "11");
        text.setAttribute("font-weight", "600");
        text.textContent = node.label;

        const subtext = document.createElementNS("http://www.w3.org/2000/svg", "text");
        subtext.setAttribute("x", "0");
        subtext.setAttribute("y", isCenter ? "18" : isL1 ? "16" : "14");
        subtext.setAttribute("text-anchor", "middle");
        subtext.setAttribute("fill", theme.text);
        subtext.setAttribute("font-size", "9.5");
        subtext.setAttribute("font-weight", "400");
        subtext.textContent = isCenter ? "Root Architecture" : `${node.subtopics ? node.subtopics.length : 0} Topics • Click for 4-Part Guide`;

        g.appendChild(rect);
        g.appendChild(text);
        g.appendChild(subtext);

        g.addEventListener("click", (e) => {
          e.stopPropagation();
          selectNode(node);
        });

        nodesGroup.appendChild(g);
      });
    }

    function renderLinks() {
      linksHierarchyGroup.innerHTML = "";
      linksCrossGroup.innerHTML = "";

      const nodeMap = new Map();
      GRAPH_DATA.nodes.forEach(n => nodeMap.set(n.id, n));

      GRAPH_DATA.nodes.forEach(node => {
        if (!node.connections) return;
        node.connections.forEach(targetId => {
          const target = nodeMap.get(targetId);
          if (!target) return;

          if (state.activeDomain !== "all" &&
              node.category !== "center" && target.category !== "center" &&
              node.category !== state.activeDomain && target.category !== state.activeDomain) {
            return;
          }

          const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
          const dx = target.x - node.x;
          const dy = target.y - node.y;
          const cx1 = node.x + dx * 0.4;
          const cy1 = node.y;
          const cx2 = node.x + dx * 0.6;
          const cy2 = target.y;

          path.setAttribute("d", `M ${node.x} ${node.y} C ${cx1} ${cy1}, ${cx2} ${cy2}, ${target.x} ${target.y}`);
          path.setAttribute("fill", "none");
          path.setAttribute("stroke", "#475569");
          path.setAttribute("stroke-width", "1.5");
          path.setAttribute("stroke-dasharray", "4,4");
          path.setAttribute("opacity", "0.7");
          linksHierarchyGroup.appendChild(path);
        });
      });

      if (state.showCrossLinks) {
        GRAPH_DATA.crossLinks.forEach(link => {
          const from = nodeMap.get(link.from);
          const to = nodeMap.get(link.to);
          if (!from || !to) return;

          if (state.activeDomain !== "all" &&
              from.category !== state.activeDomain && to.category !== state.activeDomain) {
            return;
          }

          const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
          const midX = (from.x + to.x) / 2;
          const midY = (from.y + to.y) / 2 - 40;

          path.setAttribute("d", `M ${from.x} ${from.y} Q ${midX} ${midY} ${to.x} ${to.y}`);
          path.setAttribute("fill", "none");
          path.setAttribute("stroke", "#f59e0b");
          path.setAttribute("stroke-width", "2");
          path.setAttribute("marker-end", "url(#arrowhead-cross)");
          path.setAttribute("opacity", "0.85");

          const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
          text.setAttribute("x", midX);
          text.setAttribute("y", midY - 6);
          text.setAttribute("text-anchor", "middle");
          text.setAttribute("fill", "#fbbf24");
          text.setAttribute("font-size", "9.5");
          text.setAttribute("font-weight", "500");
          text.textContent = link.label;

          linksCrossGroup.appendChild(path);
          linksCrossGroup.appendChild(text);
        });
      }
    }

    function selectNode(node) {
      state.selectedNodeId = node.id;
      const panel = document.getElementById("inspectorPanel");

      const badge = document.getElementById("inspBadge");
      badge.textContent = node.category.toUpperCase();
      badge.className = `badge bg-${node.category === 'math' ? 'blue' : node.category === 'data' ? 'emerald' : node.category === 'ml' ? 'purple' : node.category === 'dl' ? 'pink' : node.category === 'genai' ? 'amber' : 'indigo'}-500/20 text-${node.category === 'math' ? 'blue' : node.category === 'data' ? 'emerald' : node.category === 'ml' ? 'purple' : node.category === 'dl' ? 'pink' : node.category === 'genai' ? 'amber' : 'indigo'}-300 border border-slate-700`;

      document.getElementById("inspTitle").textContent = node.label;
      document.getElementById("inspDefinition").textContent = node.def || "Core theoretical definition.";

      const formulaEl = document.getElementById("inspFormula");
      if (node.formula) {
        document.getElementById("inspMathSection").style.display = "block";
        formulaEl.innerHTML = formatFormulaDisplay(node.formula);
        triggerMathRender(formulaEl);
      } else {
        document.getElementById("inspMathSection").style.display = "none";
      }

      const logicEl = document.getElementById("inspLogic");
      if (node.logic) {
        document.getElementById("inspLogicSection").style.display = "block";
        logicEl.textContent = node.logic;
      } else {
        document.getElementById("inspLogicSection").style.display = "none";
      }

      const exampleEl = document.getElementById("inspExample");
      if (node.example) {
        document.getElementById("inspExampleSection").style.display = "block";
        exampleEl.textContent = node.example;
      } else {
        document.getElementById("inspExampleSection").style.display = "none";
      }

      const subList = document.getElementById("inspSubtopics");
      subList.innerHTML = "";
      if (node.subtopics && node.subtopics.length > 0) {
        node.subtopics.forEach(sub => {
          const match = findConcept(sub);
          const cId = match ? match.id : sub;
          const btn = document.createElement("button");
          btn.className = "w-full text-left p-2 rounded-lg bg-slate-800/80 hover:bg-indigo-950/60 border border-slate-700/80 hover:border-indigo-500/50 transition flex items-center justify-between group";
          btn.innerHTML = `<span class="text-xs text-slate-200 group-hover:text-indigo-200 font-medium">${sub}</span>
                           <span class="text-[10px] text-indigo-400 group-hover:text-indigo-300 transition shrink-0 ml-1.5 flex items-center gap-1 font-semibold">Open ➔</span>`;
          btn.onclick = (e) => {
            e.stopPropagation();
            openConceptModal(cId);
          };
          subList.appendChild(btn);
        });
        document.getElementById("inspSubtopicsSection").style.display = "block";
      } else {
        document.getElementById("inspSubtopicsSection").style.display = "none";
      }

      const linksContainer = document.getElementById("inspCrossLinks");
      linksContainer.innerHTML = "";
      const related = GRAPH_DATA.crossLinks.filter(l => l.from === node.id || l.to === node.id);
      if (related.length > 0) {
        related.forEach(link => {
          const targetId = link.from === node.id ? link.to : link.from;
          const targetNode = GRAPH_DATA.nodes.find(n => n.id === targetId);
          if (targetNode) {
            const btn = document.createElement("button");
            btn.className = "text-[11px] px-2.5 py-1 rounded bg-amber-500/10 text-amber-300 border border-amber-500/30 hover:bg-amber-500/20 transition flex items-center gap-1";
            btn.innerHTML = `<span>${link.from === node.id ? '➔' : '⬅'} ${targetNode.label}</span> <span class="text-[9px] text-slate-400">(${link.label})</span>`;
            btn.onclick = () => {
              selectNode(targetNode);
              focusOnNode(targetNode);
            };
            linksContainer.appendChild(btn);
          }
        });
      } else {
        linksContainer.innerHTML = "<span class='text-slate-500 italic text-[11px]'>Hierarchical branch connections</span>";
      }

      panel.classList.remove("translate-x-full");
      if (currentMainTab === "mindmap") {
        history.replaceState({ tab: 'mindmap', deepTarget: node.id }, "", `#mindmap/${node.id}`);
      }
    }

    function closeInspector() {
      document.getElementById("inspectorPanel").classList.add("translate-x-full");
      state.selectedNodeId = null;
      if (currentMainTab === "mindmap") {
        history.replaceState({ tab: 'mindmap' }, "", `#mindmap`);
      }
    }

    function focusOnNode(node) {
      const centerX = window.innerWidth / 2;
      const centerY = window.innerHeight / 2;
      state.panX = centerX - node.x * state.zoom;
      state.panY = centerY - node.y * state.zoom;
      updateTransform();
    }

    function filterDomain(domain) {
      state.activeDomain = domain;
      document.querySelectorAll(".domain-btn").forEach(btn => {
        if (btn.dataset.domain === domain) {
          btn.className = "px-2.5 py-0.5 rounded text-xs font-medium bg-indigo-600 text-white domain-btn active";
        } else {
          btn.className = "px-2.5 py-0.5 rounded text-xs font-medium bg-[var(--background,#0f172a)] text-[var(--muted-foreground,#94a3b8)] hover:text-white border border-[var(--border,#334155)] domain-btn";
        }
      });
      render();
    }

    const DOMAIN_SECTIONS = [
      { id: "math", title: "1. Mathematical & Theoretical Foundations", desc: "Linear algebra, multivariate optimization calculus, probability distributions, and information theory.", filter: n => n.category === "math" && n.level > 1 },
      { id: "data", title: "2. Data Preprocessing, Scrubbing & Feature Engineering", desc: "Outlier management, imputation, scaling, polynomial transforms, feature crosses, and class imbalance mitigation.", filter: n => n.category === "data" && n.level > 1 },
      { id: "ml", title: "3. Classical Machine Learning & Optimization", desc: "Supervised and unsupervised models, loss formulations, gradient descent mechanics, and regularization.", filter: n => n.category === "ml" && n.level > 1 },
      { id: "eval", title: "4. Model Evaluation & Generalization", desc: "Confusion matrix metrics, ROC/PR curves, operating thresholds, and bias-variance tradeoff.", filter: n => n.category === "eval" && n.level > 1 },
      { id: "dl", title: "5. Deep Learning Foundations", desc: "Artificial neurons, activation functions, backpropagation, Adam/AdamW optimizers, and normalization.", filter: n => n.category === "dl" && !["dl_vision", "dl_seq", "dl_generative"].includes(n.id) && n.level > 1 },
      { id: "dl_arch", title: "6. Specialized Deep Architectures", desc: "Convolutional neural networks (CNNs), residual connections, sequence models (LSTM), and diffusion models (DDPM).", filter: n => ["dl_vision", "dl_seq", "dl_generative"].includes(n.id) },
      { id: "genai", title: "7. Generative AI, Transformers & Large Language Models", desc: "Tokenization, embeddings, self-attention, pre-training, SFT, PEFT (LoRA/QLoRA), alignment (RLHF/DPO), and RAG.", filter: n => n.category === "genai" && n.level > 1 },
      { id: "mlops", title: "8. MLOps & Production Systems", desc: "Model registry, serving engines (vLLM), data/concept drift detection, and automated monitoring.", filter: n => n.category === "mlops" }
    ];

    function buildLineWiseDocument() {
      const container = document.getElementById("printableDocContainer");
      if (!container) return;

      let html = `
        <div class="max-w-5xl mx-auto space-y-8 pb-16">
          <div class="border-b border-slate-700 pb-6 mb-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 text-xs font-semibold uppercase tracking-wider mb-2 print-badge">
                Master Curriculum & Syllabus Index
              </div>
              <h1 class="text-2xl md:text-3xl font-extrabold tracking-tight text-white print:text-black">
                Master AI, Machine Learning & Deep Learning Syllabus
              </h1>
              <p class="text-xs md:text-sm text-slate-400 mt-1 print:text-slate-600">
                Complete structured index of all 8 Domains, 34 Topics, and 170 Core Concepts. Click any concept to view its dedicated page with definition, mathematical formula, intuition, and real-world example.
              </p>
            </div>
            <div class="no-print flex items-center gap-2 shrink-0">
              <a href="concept.html" target="_blank" class="px-3.5 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white border border-slate-700 text-xs font-semibold flex items-center gap-1.5 transition">
                <span>All Concepts Encyclopedia</span>
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg>
              </a>
              <button onclick="downloadActiveViewPDF()" class="bg-red-600 hover:bg-red-500 text-white font-semibold text-xs px-4 py-2 rounded-lg shadow-lg shadow-red-600/30 flex items-center gap-1.5 transition">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
                <span>Print / Save as PDF</span>
              </button>
            </div>
          </div>
      `;

      DOMAIN_SECTIONS.forEach(domain => {
        const domainNodes = GRAPH_DATA.nodes.filter(domain.filter);
        if (domainNodes.length === 0) return;

        let totalDomainConcepts = 0;
        domainNodes.forEach(n => totalDomainConcepts += (n.subtopics ? n.subtopics.length : 0));

        html += `
          <section class="space-y-4 pt-2">
            <div class="print-domain-header border-b-2 border-indigo-500/40 pb-2 flex items-baseline justify-between flex-wrap gap-2">
              <h2 class="text-lg md:text-xl font-bold text-white print:text-indigo-950 flex items-center gap-2">
                <span>${domain.title}</span>
              </h2>
              <div class="flex items-center gap-2">
                <span class="text-[11px] font-semibold px-2 py-0.5 rounded bg-slate-800 text-indigo-300 border border-slate-700 print-badge">
                  ${domainNodes.length} Topics
                </span>
                <span class="text-[11px] font-semibold px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 print-badge">
                  ${totalDomainConcepts} Core Concepts
                </span>
              </div>
            </div>
            <p class="text-xs text-slate-400 print:text-slate-600 italic mb-3">${domain.desc}</p>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        `;

        domainNodes.forEach(node => {
          const subtopics = node.subtopics || [];

          html += `
            <div id="syllabus-node-${node.id}" class="print-card bg-slate-900/80 border border-slate-800 rounded-xl p-4 md:p-5 shadow-sm space-y-3 transition hover:border-slate-700">
              <div class="flex items-start justify-between gap-2 border-b border-slate-800/80 pb-2.5">
                <div>
                  <h3 class="text-sm md:text-base font-bold text-white print:text-indigo-950 flex items-center gap-2">
                    <span class="w-2.5 h-2.5 rounded-full bg-indigo-500"></span>
                    <span>${node.label}</span>
                  </h3>
                </div>
                <span class="text-[10px] font-medium px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-300 border border-indigo-500/20 print-badge shrink-0">
                  Level ${node.level}
                </span>
              </div>

              <div class="space-y-1.5">
                <div class="text-[10.5px] uppercase tracking-wider font-semibold text-slate-400 flex items-center justify-between">
                  <span>Subtopics & Core Concepts:</span>
                  <span class="text-[10px] text-slate-500 font-mono">${subtopics.length} items</span>
                </div>
                <div class="flex flex-col space-y-1.5 pt-1">
                  ${subtopics.map(sub => {
                    const match = findConcept(sub);
                    const cId = match ? match.id : sub;
                    return `
                      <button onclick="openConceptModal('${cId}')" class="w-full text-left p-2 rounded-lg bg-slate-950/70 hover:bg-indigo-950/50 border border-slate-800/80 hover:border-indigo-500/50 transition flex items-center justify-between group cursor-pointer">
                        <span class="text-xs text-slate-200 group-hover:text-indigo-200 font-medium leading-snug">${sub}</span>
                        <span class="text-[10px] text-indigo-400 group-hover:text-indigo-300 transition shrink-0 ml-2 font-semibold flex items-center gap-1">
                          <span>View</span> ➔
                        </span>
                      </button>
                    `;
                  }).join('')}
                </div>
              </div>
            </div>
          `;
        });

        html += `
            </div>
          </section>
        `;
      });

      html += `</div>`;
      container.innerHTML = html;
    }

    // Search listeners
    document.getElementById("searchInput").addEventListener("input", (e) => {
      state.searchQuery = e.target.value;
      render();
    });

    document.getElementById("paperSearchInput").addEventListener("input", (e) => {
      paperSearchQuery = e.target.value;
      renderPapersList();
    });

    document.getElementById("projectSearchInput").addEventListener("input", (e) => {
      projectSearchQuery = e.target.value;
      renderProjectsList();
    });

    window.addEventListener("resize", () => {
      render();
    });

    document.getElementById("qSearchInput").addEventListener("input", (e) => {
      interviewSearchQuery = e.target.value;
      renderQuestionsList();
    });

    render();
    buildLineWiseDocument();
    renderPapersList();
    renderProjectsList();
    renderQuestionsList();

    // Initial URL Routing based on window.location
    handleUrlRouting(true);

    window.addEventListener("DOMContentLoaded", () => {
      handleUrlRouting(true);
      triggerMathRender(document.body);
    });

    window.addEventListener("popstate", () => {
      handleUrlRouting(false);
    });

    window.addEventListener("hashchange", () => {
      handleUrlRouting(false);
    });

    setTimeout(() => {
      triggerMathRender(document.body);
    }, 120);
  </script>
</body>
</html>
"""

def build_html():
    nodes_json = json.dumps(ALL_NODES, indent=2)
    links_json = json.dumps(CROSS_LINKS, indent=2)
    papers_json = json.dumps(PAPERS, indent=2)
    projects_json = json.dumps(PROJECTS, indent=2)
    questions_json = json.dumps(INTERVIEW_QUESTIONS, indent=2)
    concepts_json = json.dumps(ALL_CONCEPTS, indent=2)
    html = (HTML_TEMPLATE
            .replace("__NODES_JSON__", nodes_json)
            .replace("__LINKS_JSON__", links_json)
            .replace("__PAPERS_JSON__", papers_json)
            .replace("__PROJECTS_JSON__", projects_json)
            .replace("__QUESTIONS_JSON__", questions_json)
            .replace("__CONCEPTS_JSON__", concepts_json))
    with open("ai_ml_dl_master_mindmap.html", "w", encoding="utf-8") as f:
        f.write(html)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated ai_ml_dl_master_mindmap.html & index.html with KaTeX support successfully!")


def build_markdown_encyclopedia():
    md = "# Master AI, Machine Learning, Deep Learning & Data Science Encyclopedia\n\n"
    md += "Complete theoretical reference guide covering **Definition**, **Mathematical Formula**, **Important Logic**, and **Simple Real-World Example** for every single topic and subtopic across Data Science, Machine Learning, Deep Learning, and Generative AI.\n\n"
    md += "---\n\n"

    categories = [
        ("1. Mathematical & Theoretical Foundations", "math"),
        ("2. Data Preprocessing, Scrubbing & Feature Engineering", "data"),
        ("3. Classical Machine Learning & Optimization", "ml"),
        ("4. Model Evaluation & Generalization", "eval"),
        ("5. Deep Learning Foundations", "dl"),
        ("6. Specialized Deep Architectures", "dl_arch"),
        ("7. Generative AI, Transformers & Large Language Models", "genai"),
        ("8. MLOps & Production Systems", "mlops")
    ]

    for title, cat_id in categories:
        md += f"## {title}\n\n"
        if cat_id == "dl_arch":
            cat_nodes = [n for n in TOPICS if n["id"] in ["dl_vision", "dl_seq", "dl_generative"]]
        elif cat_id == "dl":
            cat_nodes = [n for n in TOPICS if n["category"] == "dl" and n["id"] not in ["dl_vision", "dl_seq", "dl_generative"]]
        else:
            cat_nodes = [n for n in TOPICS if n["category"] == cat_id]

        for node in cat_nodes:
            md += f"### {node['label']}\n\n"
            md += f"- **📖 Simple Definition**: {node.get('def', '')}\n"
            md += f"- **🔢 Mathematical Formula**: `{node.get('formula', 'N/A')}`\n"
            md += f"- **💡 Important Logic & Intuition**: {node.get('logic', '')}\n"
            md += f"- **🎯 Simple Real-World Example**: {node.get('example', '')}\n\n"
            
            md += "**📋 Subtopics & Core Mechanics**:\n"
            for sub in node.get("subtopics", []):
                md += f"- {sub}\n"
            md += "\n"

            related = [l for l in CROSS_LINKS if l["from"] == node["id"] or l["to"] == node["id"]]
            if related:
                md += "**🔗 Key Interconnections**:\n"
                for l in related:
                    target_id = l["to"] if l["from"] == node["id"] else l["from"]
                    target_node = next((n for n in ALL_NODES if n["id"] == target_id), None)
                    target_name = target_node["label"] if target_node else target_id
                    arrow = "➔" if l["from"] == node["id"] else "⬅"
                    md += f"- {arrow} **{target_name}**: {l['label']}\n"
                md += "\n"
            md += "---\n\n"

    with open("ai_ml_dl_master_mindmap.md", "w", encoding="utf-8") as f:
        f.write(md)
    print("Generated ai_ml_dl_master_mindmap.md successfully!")


def build_markdown_papers():
    md = "# Landmark & Game-Changing AI Research Papers Compendium\n\n"
    md += "A curated archive of the seminal, revolutionary research papers that transformed Machine Learning, Deep Learning, Computer Vision, Transformers, and Generative AI — with direct public arXiv links, the core problem each paper solved, their mathematical breakthroughs, and modern legacy.\n\n"
    md += "---\n\n"

    for p in PAPERS:
        md += f"## [{p['title']}]({p['url']})\n\n"
        md += f"- **📅 Year**: `{p['year']}` | **🏢 Institution**: `{p['institution']}`\n"
        md += f"- **👥 Authors**: {p['authors']}\n"
        md += f"- **🔗 Public Paper Link**: [{p['url']}]({p['url']})\n"
        md += f"- **💡 Key Takeaway**: *{p['one_liner']}*\n\n"
        md += f"### ❌ The Core Problem It Solved\n{p['problem']}\n\n"
        md += f"### 🚀 The Game-Changing Breakthrough\n{p['breakthrough']}\n\n"
        md += f"### 🔢 Core Mathematical Formulation / Mechanism\n```text\n{p['formula']}\n```\n\n"
        md += f"### 🌟 Modern Legacy & Impact\n{p['impact']}\n\n"
        md += "---\n\n"

    with open("ai_ml_dl_master_research_papers.md", "w", encoding="utf-8") as f:
        f.write(md)
    print("Generated ai_ml_dl_master_research_papers.md successfully!")


if __name__ == "__main__":
    build_html()
    build_markdown_encyclopedia()
    build_markdown_papers()
    try:
        from build_standalone_concept import build_standalone_concept_pages
        build_standalone_concept_pages()
    except Exception as e:
        print("Note: build_standalone_concept_pages:", e)
