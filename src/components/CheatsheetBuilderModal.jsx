import React, { useState, useMemo, useRef } from 'react';
import { 
  X, 
  Printer, 
  Download, 
  Copy, 
  Check, 
  FileText, 
  Sparkles, 
  Layers, 
  Plus, 
  Trash2, 
  Search, 
  Sun, 
  Moon, 
  BookOpen, 
  HelpCircle, 
  Zap,
  Columns2,
  Columns3,
  Bookmark
} from 'lucide-react';
import KaTeXRenderer from './KaTeXRenderer';
import conceptsData from '../data/concepts.json';
import interviewData from '../data/interviewQuestions.json';
import { useProgress } from '../context/ProgressContext';

// Pre-curated high-yield packs
const PRESET_PACKS = [
  {
    id: 'transformers',
    title: '⚡ Transformers & Attention',
    description: 'Scaled Dot-Product, Multi-Head, KV Cache sizing, RoPE & FlashAttention',
    items: [
      {
        id: 'cs-attn',
        title: 'Scaled Dot-Product Attention',
        category: 'Deep Learning',
        formula: '\\text{Attention}(Q,K,V) = \\text{softmax}\\left(\\frac{QK^T}{\\sqrt{d_k}}\\right)V',
        definition: 'Measures pairwise token relevance. The scaling factor 1/sqrt(d_k) prevents dot products from growing excessively large in high dimensions, preventing softmax gradient saturation.',
        takeaway: 'Time & memory complexity: O(N^2) where N is sequence length. Query (Q) and Key (K) have dimension d_k; Value (V) has dimension d_v.'
      },
      {
        id: 'cs-mha',
        title: 'Multi-Head Attention (MHA)',
        category: 'Deep Learning',
        formula: '\\text{MHA}(Q,K,V) = \\text{Concat}(\\text{head}_1, \\dots, \\text{head}_h)W^O, \\quad \\text{where } \\text{head}_i = \\text{Attention}(QW_i^Q, KW_i^K, VW_i^V)',
        definition: 'Projects Q, K, V into h distinct representation subspaces simultaneously, enabling the model to jointly attend to syntactic, semantic, and positional contexts.',
        takeaway: 'Standard config: d_model = 4096, h = 32 heads, d_k = d_v = 128.'
      },
      {
        id: 'cs-kvcache',
        title: 'KV Cache VRAM Footprint',
        category: 'GenAI & Systems',
        formula: '\\text{Memory (bytes)} = 2 \\times 2 \\times b \\times s \\times n_{\\text{layers}} \\times d_{\\text{model}}',
        definition: 'In autoregressive generation, keys and values of previous tokens are cached to avoid redundant O(N^2) recomputation during decoding.',
        takeaway: 'For Llama-3-8B (32 layers, d=4096) with batch=1 and seq_len=4096 in FP16: ~2.15 GB VRAM solely for KV Cache!'
      },
      {
        id: 'cs-rope',
        title: 'Rotary Position Embedding (RoPE)',
        category: 'Deep Learning',
        formula: 'R_{\\Theta, m}^d x_m = \\begin{pmatrix} x_m^{(1)} \\cos m\\theta_1 - x_m^{(2)} \\sin m\\theta_1 \\\\ x_m^{(1)} \\sin m\\theta_1 + x_m^{(2)} \\cos m\\theta_1 \\end{pmatrix}',
        definition: 'Encodes positional information by multiplying representations with orthogonal 2D rotation matrices. The inner product <R_m q, R_n k> depends purely on relative distance (m - n).',
        takeaway: 'Used by modern LLMs (Llama, Mistral, Gemma, Qwen) for superior context extrapolation over absolute positional embeddings.'
      },
      {
        id: 'cs-flashattn',
        title: 'FlashAttention Tiling',
        category: 'MLOps & Systems',
        formula: '\\text{HBM IO Speedup} = O(N^2) \\longrightarrow O(N) \\text{ via SRAM Online Softmax Tiling}',
        definition: 'Fuses softmax and matrix multiplication into GPU SRAM blocks using online softmax rescaling (Milakov & Gimelshein algorithm), eliminating expensive HBM roundtrips.',
        takeaway: 'Yields 2x-4x wall-clock training speedup and 10x-20x memory reduction for long contexts.'
      }
    ]
  },
  {
    id: 'finetuning',
    title: '🔬 Fine-Tuning & Quantization',
    description: 'LoRA decomposition, QLoRA NF4, Chinchilla scaling, and memory budgeting',
    items: [
      {
        id: 'cs-lora',
        title: 'Low-Rank Adaptation (LoRA)',
        category: 'GenAI & LLMs',
        formula: 'W = W_0 + \\Delta W = W_0 + \\frac{\\alpha}{r} B \\cdot A, \\quad B \\in \\mathbb{R}^{d \\times r}, A \\in \\mathbb{R}^{r \\times k}, \\ r \\ll \\min(d, k)',
        definition: 'Freezes pre-trained weight matrix W_0 and injects trainable low-rank decomposition matrices. A is initialized randomly from N(0, sigma^2), B is initialized to 0 so delta W starts at zero.',
        takeaway: 'Zero inference latency overhead: merge W = W_0 + (alpha/r)*BA directly into base weights prior to deployment.'
      },
      {
        id: 'cs-qlora',
        title: 'QLoRA 4-bit NormalFloat (NF4)',
        category: 'GenAI & LLMs',
        formula: 'W_{\\text{NF4}} = q_{\\text{NF4}}(W_0) + \\text{Dequant}(c_1, c_2) \\times \\text{FP16}(B A)',
        definition: 'Quantizes base LLM weights to an information-theoretically optimal 4-bit NormalFloat distribution with Double Quantization of quantization constants and Paged Optimizers.',
        takeaway: 'Enables fine-tuning a 70B parameter model on a single 48GB GPU (or 7B on a 16GB consumer RTX 4080) with zero performance degradation.'
      },
      {
        id: 'cs-chinchilla',
        title: 'Chinchilla Compute-Optimal Scaling',
        category: 'Foundations',
        formula: 'C \\approx 6 N D, \\quad N_{\\text{opt}} \\propto C^{0.5}, \\quad D_{\\text{opt}} \\approx 20 \\times N',
        definition: 'For compute-optimal pre-training, parameter count (N) and training tokens (D) should be scaled in equal proportion. Training tokens should be roughly 20x the parameter count.',
        takeaway: 'Demonstrated that LLaMA (7B trained on 1T+ tokens) drastically outperforms undertrained 175B models for inference economics.'
      },
      {
        id: 'cs-perplexity',
        title: 'Perplexity & Cross-Entropy',
        category: 'Metrics & Evaluation',
        formula: '\\text{PPL}(X) = \\exp\\left(-\\frac{1}{T}\\sum_{t=1}^T \\log P(x_t \\mid x_{<t})\\right) = \\exp(\\mathcal{L}_{\\text{CE}})',
        definition: 'The exponentiated cross-entropy loss over tokens. Represents the effective branching factor: how many tokens the model is equally uncertain between at each step.',
        takeaway: 'Lower is better. A perplexity of 10 means the model is as confused as if it were choosing uniformly among 10 options.'
      }
    ]
  },
  {
    id: 'rag',
    title: '🔍 Production RAG & Vector Search',
    description: 'Cosine distance, Reciprocal Rank Fusion, HNSW graph index, and HyDE',
    items: [
      {
        id: 'cs-cosine',
        title: 'Cosine Similarity & Normalization',
        category: 'Vector DBs',
        formula: '\\cos(\\theta) = \\frac{u \\cdot v}{\\|u\\|_2 \\|v\\|_2} = \\frac{\\sum u_i v_i}{\\sqrt{\\sum u_i^2}\\sqrt{\\sum v_i^2}}',
        definition: 'Measures directional alignment independent of vector magnitudes. In L2-normalized vector spaces, cosine similarity is identical to the inner product dot product u . v.',
        takeaway: 'Normalizing embeddings during indexing reduces nearest neighbor search from expensive Euclidean square roots to fast BLAS GEMM matrix multiplications.'
      },
      {
        id: 'cs-rrf',
        title: 'Reciprocal Rank Fusion (RRF)',
        category: 'RAG & Retrieval',
        formula: '\\text{RRF\\_Score}(d \\in D) = \\sum_{m \\in M} \\frac{1}{k + r_m(d)}, \\quad k \\approx 60',
        definition: 'Hybrid search fusion algorithm combining dense vector rankings and BM25 sparse keyword rankings without requiring calibrated score normalization.',
        takeaway: 'Solves dense retrieval "blind spots" on exact serial numbers, product codes, or acronyms.'
      },
      {
        id: 'cs-hnsw',
        title: 'HNSW Graph Index Complexity',
        category: 'Vector Search',
        formula: '\\text{Search Complexity} = O(\\log N), \\quad \\text{Layer Prob} = p^l',
        definition: 'Hierarchical Navigable Small World graphs organize vectors across multi-layer geometric skip-lists. Top layers execute long-distance jumps; bottom layer conducts fine local greedy search.',
        takeaway: 'Industry standard for Milvus, Pinecone, Qdrant, Weaviate, and pgvector.'
      },
      {
        id: 'cs-chunking',
        title: 'Semantic Chunking & Overlap',
        category: 'RAG Pipeline',
        formula: '\\text{Overlap} \\approx 10\\% - 20\\% \\text{ of Chunk Size } (\\sim 50-100 \\text{ tokens})',
        definition: 'Sliding window token partitioning preserving semantic boundary context across adjacent text chunks.',
        takeaway: 'Prevents sentences containing crucial causal relationships or coreferences from being cleaved apart.'
      }
    ]
  },
  {
    id: 'optimization',
    title: '🧠 Loss Functions & Optimization',
    description: 'Cross-Entropy, AdamW weight decay, InfoNCE contrastive, and learning rate warmup',
    items: [
      {
        id: 'cs-adamw',
        title: 'AdamW (Decoupled Weight Decay)',
        category: 'Optimization',
        formula: '\\theta_{t+1} = \\theta_t - \\eta \\lambda \\theta_t - \\eta \\frac{m_t}{\\sqrt{v_t} + \\epsilon}',
        definition: 'Loshchilov & Hutter showed standard Adam with L2 regularization is broken because weight decay is scaled by 1/sqrt(v_t), penalizing frequent gradients less. AdamW decouples weight decay directly.',
        takeaway: 'Standard optimizer for virtually all modern foundation models.'
      },
      {
        id: 'cs-infonce',
        title: 'InfoNCE Contrastive Loss',
        category: 'Representation Learning',
        formula: '\\mathcal{L}_{\\text{InfoNCE}} = -\\log \\frac{\\exp(\\text{sim}(q, k^+) / \\tau)}{\\exp(\\text{sim}(q, k^+) / \\tau) + \\sum_{j=1}^K \\exp(\\text{sim}(q, k_j^-) / \\tau)}',
        definition: 'Pulls positive representation pairs (q, k^+) closer together while pushing K negative pairs apart in hyperspherical embedding space, scaled by temperature tau.',
        takeaway: 'Core training objective for CLIP (OpenAI), SimCLR, and dense embedding models (e.g. text-embedding-3).'
      },
      {
        id: 'cs-ce',
        title: 'Categorical Cross-Entropy Loss',
        category: 'Foundations',
        formula: '\\mathcal{L}_{\\text{CE}} = -\\sum_{c=1}^C y_c \\log \\hat{y}_c = -\\log \\hat{y}_{\\text{target}}',
        definition: 'Measures divergence between true one-hot distribution y and predicted softmax probabilities. Minimizing cross-entropy is mathematically equivalent to minimizing KL divergence.',
        takeaway: 'Combined with label smoothing epsilon: y_c = (1-eps)*y_c + eps/C to prevent overconfident logits.'
      },
      {
        id: 'cs-warmup',
        title: 'Cosine Learning Rate Schedule with Warmup',
        category: 'Optimization',
        formula: '\\eta_t = \\eta_{\\min} + \\frac{1}{2}(\\eta_{\\max} - \\eta_{\\min})\\left(1 + \\cos\\left(\\frac{t - T_{\\text{warm}}}{T_{\\text{total}} - T_{\\text{warm}}} \\pi\\right)\\right)',
        definition: 'Linearly warms up learning rate from 0 to eta_max over early steps to stabilize initial random variance, then smoothly decays following a half cosine wave.',
        takeaway: 'Prevents catastrophic early gradient explosions in deep transformer architectures.'
      }
    ]
  }
];

export default function CheatsheetBuilderModal({ isOpen, onClose }) {
  const { bookmarkedItems } = useProgress();
  const printRef = useRef(null);

  // Selected pack or custom
  const [activePackId, setActivePackId] = useState('transformers');
  const [customItems, setCustomItems] = useState(PRESET_PACKS[0].items);
  const [layoutColumns, setLayoutColumns] = useState(2); // 2 or 3
  const [printTheme, setPrintTheme] = useState('light'); // 'light' or 'dark'
  const [searchQuery, setSearchQuery] = useState('');
  const [isCopied, setIsCopied] = useState(false);
  const [showAddDrawer, setShowAddDrawer] = useState(false);

  // When active pack changes
  const handleSelectPack = (packId) => {
    setActivePackId(packId);
    if (packId === 'bookmarks') {
      // Build items from bookmarks
      const bookmarkedConcepts = bookmarkedItems.map((b, idx) => ({
        id: `bm-${b.id || idx}`,
        title: b.title || 'Bookmarked Item',
        category: b.type ? b.type.toUpperCase() : 'Saved Item',
        formula: '',
        definition: b.subtitle || 'Saved for rapid revision and study notes.',
        takeaway: `Type: ${b.type || 'Custom'} | Saved to personal vault.`
      }));
      setCustomItems(bookmarkedConcepts.length > 0 ? bookmarkedConcepts : [
        {
          id: 'bm-empty',
          title: 'No Bookmarks Yet',
          category: 'Quick Tip',
          formula: '',
          definition: 'Click the Bookmark icon on any concept, paper, or interview question across the site to build your personal cheat sheet.',
          takeaway: 'Bookmark high-priority topics to auto-generate custom PDF study guides.'
        }
      ]);
      return;
    }

    const pack = PRESET_PACKS.find(p => p.id === packId);
    if (pack) {
      setCustomItems([...pack.items]);
    }
  };

  // Remove an item
  const handleRemoveItem = (id) => {
    setCustomItems(prev => prev.filter(item => item.id !== id));
  };

  // Add an item from concepts data
  const handleAddConcept = (concept) => {
    if (customItems.some(i => i.id === concept.id)) return;
    const newItem = {
      id: concept.id,
      title: concept.title,
      category: concept.category_label || concept.topic_label || 'Concept',
      formula: concept.formula ? concept.formula.replace(/^\$\$/,'').replace(/\$\$$/,'') : '',
      definition: concept.def || concept.definition || '',
      takeaway: concept.logic || concept.example || ''
    };
    setCustomItems(prev => [...prev, newItem]);
  };

  // Printable action
  const handlePrint = () => {
    window.print();
  };

  // Markdown export action
  const generateMarkdown = () => {
    let md = `# The Era of AI — Quick Revision Cheatsheet\n`;
    md += `*Generated on ${new Date().toLocaleDateString()} | Total Items: ${customItems.length}*\n\n`;
    md += `---\n\n`;

    customItems.forEach((item, index) => {
      md += `### ${index + 1}. ${item.title} \`[${item.category}]\`\n\n`;
      if (item.formula) {
        md += `$$\n${item.formula}\n$$\n\n`;
      }
      if (item.definition) {
        md += `**Definition & Mechanics:**\n${item.definition}\n\n`;
      }
      if (item.takeaway) {
        md += `> **Key Takeaway / Intuition:** ${item.takeaway}\n\n`;
      }
      md += `---\n\n`;
    });

    return md;
  };

  const handleDownloadMarkdown = () => {
    const md = generateMarkdown();
    const blob = new Blob([md], { type: 'text/markdown;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `Era_of_AI_Cheatsheet_${activePackId}.md`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const handleCopyMarkdown = () => {
    const md = generateMarkdown();
    navigator.clipboard.writeText(md);
    setIsCopied(true);
    setTimeout(() => setIsCopied(false), 2000);
  };

  // Filtered concepts for quick add drawer
  const availableConcepts = useMemo(() => {
    if (!searchQuery.trim()) return conceptsData.slice(0, 30);
    const q = searchQuery.toLowerCase();
    return conceptsData.filter(c => 
      c.title.toLowerCase().includes(q) || 
      (c.def && c.def.toLowerCase().includes(q)) ||
      (c.tags && c.tags.some(t => t.toLowerCase().includes(q)))
    ).slice(0, 30);
  }, [searchQuery]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-5 bg-slate-950/80 backdrop-blur-md overflow-hidden">
      {/* Print Stylesheet Hook */}
      <style>{`
        @media print {
          body * {
            visibility: hidden !important;
          }
          #cheatsheet-print-area, #cheatsheet-print-area * {
            visibility: visible !important;
          }
          #cheatsheet-print-area {
            position: absolute !important;
            left: 0 !important;
            top: 0 !important;
            width: 100% !important;
            margin: 0 !important;
            padding: 12px !important;
            background: white !important;
            color: black !important;
            box-shadow: none !important;
            border: none !important;
          }
          .no-print {
            display: none !important;
          }
          .print-card {
            break-inside: avoid !important;
            page-break-inside: avoid !important;
            border: 1px solid #cbd5e1 !important;
            background: #ffffff !important;
            color: #0f172a !important;
            box-shadow: none !important;
          }
          .print-text-dark {
            color: #0f172a !important;
          }
          .print-text-muted {
            color: #475569 !important;
          }
        }
      `}</style>

      <div className="relative w-full max-w-6xl max-h-[92vh] flex flex-col bg-slate-900 border border-slate-700/80 rounded-2xl shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-200">
        
        {/* Header */}
        <div className="px-5 py-3.5 border-b border-slate-800 bg-slate-950/60 flex items-center justify-between gap-4 shrink-0">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-500/20 to-indigo-500/20 border border-cyan-500/30 flex items-center justify-center text-cyan-300 shadow-sm">
              <FileText className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-base sm:text-lg font-bold text-white tracking-tight">
                  High-Yield Cheatsheet Builder & PDF Exporter
                </h2>
                <span className="text-[11px] font-mono bg-cyan-500/15 text-cyan-300 border border-cyan-500/30 px-2 py-0.5 rounded-full">
                  {customItems.length} Formulas & Concepts
                </span>
              </div>
              <p className="text-xs text-slate-400">
                Curate formulas, equations & intuitions. Print as 1-page PDF or export clean Markdown.
              </p>
            </div>
          </div>

          {/* Action buttons */}
          <div className="flex items-center gap-2">
            <button
              onClick={handlePrint}
              id="cheatsheet-print-btn"
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold shadow-md shadow-indigo-600/30 transition active:scale-95"
              title="Print / Save to PDF"
            >
              <Printer className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">Print / Save PDF</span>
            </button>

            <button
              onClick={handleDownloadMarkdown}
              id="cheatsheet-download-md-btn"
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold border border-slate-700 transition"
              title="Download Markdown (.md)"
            >
              <Download className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">Download .md</span>
            </button>

            <button
              onClick={handleCopyMarkdown}
              id="cheatsheet-copy-md-btn"
              className="p-1.5 px-2.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white border border-slate-700 text-xs font-medium transition flex items-center gap-1"
              title="Copy Markdown"
            >
              {isCopied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
              <span className="hidden md:inline">{isCopied ? 'Copied!' : 'Copy'}</span>
            </button>

            <button
              onClick={onClose}
              className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Toolbar: Preset Packs + View Options */}
        <div className="px-5 py-2.5 bg-slate-950/40 border-b border-slate-800 flex flex-wrap items-center justify-between gap-3 text-xs shrink-0">
          {/* Quick Packs */}
          <div className="flex items-center gap-1.5 overflow-x-auto pb-1 sm:pb-0 max-w-full">
            <span className="text-slate-400 font-medium whitespace-nowrap mr-1 flex items-center gap-1">
              <Zap className="w-3.5 h-3.5 text-amber-400" />
              Packs:
            </span>
            {PRESET_PACKS.map(pack => (
              <button
                key={pack.id}
                onClick={() => handleSelectPack(pack.id)}
                className={`px-2.5 py-1 rounded-md text-xs font-medium whitespace-nowrap transition border ${
                  activePackId === pack.id
                    ? 'bg-cyan-500/20 text-cyan-300 border-cyan-500/50 shadow-sm'
                    : 'bg-slate-800/80 text-slate-400 border-slate-700/60 hover:text-slate-200 hover:bg-slate-800'
                }`}
              >
                {pack.title}
              </button>
            ))}
            
            {/* Bookmarks pack */}
            <button
              onClick={() => handleSelectPack('bookmarks')}
              className={`px-2.5 py-1 rounded-md text-xs font-medium whitespace-nowrap transition border flex items-center gap-1 ${
                activePackId === 'bookmarks'
                  ? 'bg-amber-500/20 text-amber-300 border-amber-500/50 shadow-sm'
                  : 'bg-slate-800/80 text-slate-400 border-slate-700/60 hover:text-slate-200 hover:bg-slate-800'
              }`}
            >
              <Bookmark className="w-3 h-3 text-amber-400" />
              <span>My Bookmarks ({bookmarkedItems.length})</span>
            </button>
          </div>

          {/* Controls: Columns, Theme, Add Concept */}
          <div className="flex items-center gap-2 shrink-0">
            {/* Column switch */}
            <div className="flex items-center bg-slate-900 border border-slate-800 rounded-lg p-0.5">
              <button
                onClick={() => setLayoutColumns(2)}
                className={`p-1 px-1.5 rounded text-xs flex items-center gap-1 ${layoutColumns === 2 ? 'bg-slate-800 text-white shadow-sm' : 'text-slate-400 hover:text-slate-200'}`}
                title="2-Column Layout"
              >
                <Columns2 className="w-3.5 h-3.5" />
                <span className="hidden sm:inline">2-Col</span>
              </button>
              <button
                onClick={() => setLayoutColumns(3)}
                className={`p-1 px-1.5 rounded text-xs flex items-center gap-1 ${layoutColumns === 3 ? 'bg-slate-800 text-white shadow-sm' : 'text-slate-400 hover:text-slate-200'}`}
                title="3-Column Compact"
              >
                <Columns3 className="w-3.5 h-3.5" />
                <span className="hidden sm:inline">3-Col</span>
              </button>
            </div>

            {/* Print Theme */}
            <div className="flex items-center bg-slate-900 border border-slate-800 rounded-lg p-0.5">
              <button
                onClick={() => setPrintTheme('light')}
                className={`p-1 px-2 rounded text-xs flex items-center gap-1 ${printTheme === 'light' ? 'bg-slate-800 text-amber-300' : 'text-slate-400'}`}
                title="Clean Print White Mode"
              >
                <Sun className="w-3 h-3" />
                <span className="hidden sm:inline">Print Light</span>
              </button>
              <button
                onClick={() => setPrintTheme('dark')}
                className={`p-1 px-2 rounded text-xs flex items-center gap-1 ${printTheme === 'dark' ? 'bg-slate-800 text-cyan-300' : 'text-slate-400'}`}
                title="Dark Studio Mode"
              >
                <Moon className="w-3 h-3" />
                <span className="hidden sm:inline">Dark</span>
              </button>
            </div>

            {/* Add Custom Items button */}
            <button
              onClick={() => setShowAddDrawer(!showAddDrawer)}
              className="px-2.5 py-1 rounded-lg bg-emerald-600/20 hover:bg-emerald-600/30 text-emerald-300 border border-emerald-500/40 font-semibold text-xs transition flex items-center gap-1"
            >
              <Plus className="w-3.5 h-3.5" />
              <span>{showAddDrawer ? 'Done Adding' : 'Add Formula'}</span>
            </button>
          </div>
        </div>

        {/* Main Body */}
        <div className="flex-1 overflow-hidden flex flex-col md:flex-row">

          {/* Optional Add Concepts Drawer */}
          {showAddDrawer && (
            <div className="w-full md:w-80 border-b md:border-b-0 md:border-r border-slate-800 bg-slate-950/70 p-3.5 flex flex-col gap-2.5 overflow-hidden shrink-0">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-white flex items-center gap-1.5">
                  <BookOpen className="w-3.5 h-3.5 text-emerald-400" />
                  Add Concepts & Formulas
                </span>
                <span className="text-[10px] text-slate-400">Click to add</span>
              </div>
              <div className="relative">
                <Search className="w-3.5 h-3.5 absolute left-2.5 top-2.5 text-slate-400" />
                <input
                  type="text"
                  placeholder="Search 170+ concepts..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-8 pr-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500"
                />
              </div>

              <div className="flex-1 overflow-y-auto space-y-1.5 pr-1">
                {availableConcepts.map((c) => {
                  const isAdded = customItems.some(item => item.id === c.id);
                  return (
                    <div
                      key={c.id}
                      onClick={() => !isAdded && handleAddConcept(c)}
                      className={`p-2 rounded-lg border text-left text-xs transition cursor-pointer flex items-center justify-between gap-2 ${
                        isAdded
                          ? 'bg-slate-900/40 border-slate-800/40 text-slate-500 cursor-default'
                          : 'bg-slate-900/90 border-slate-800 hover:border-emerald-500/50 text-slate-300 hover:text-white'
                      }`}
                    >
                      <div className="overflow-hidden">
                        <div className="font-semibold truncate">{c.title}</div>
                        <div className="text-[10px] text-slate-500 truncate">{c.category_label || c.topic_label}</div>
                      </div>
                      <button
                        disabled={isAdded}
                        className={`p-1 rounded shrink-0 ${isAdded ? 'text-slate-600' : 'text-emerald-400 hover:bg-emerald-500/20'}`}
                      >
                        {isAdded ? <Check className="w-3.5 h-3.5" /> : <Plus className="w-3.5 h-3.5" />}
                      </button>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* Printable Cheatsheet Canvas */}
          <div className="flex-1 overflow-y-auto p-4 sm:p-6 bg-slate-950/20">
            <div 
              ref={printRef}
              id="cheatsheet-print-area"
              className={`rounded-xl p-5 sm:p-7 shadow-lg border transition-colors ${
                printTheme === 'light' 
                  ? 'bg-white text-slate-900 border-slate-300' 
                  : 'bg-slate-900/95 text-slate-100 border-slate-800'
              }`}
            >
              {/* Sheet Header */}
              <div className="border-b pb-4 mb-5 flex items-center justify-between flex-wrap gap-2 border-slate-200 dark:border-slate-800">
                <div>
                  <div className="text-xl font-extrabold tracking-tight flex items-center gap-2">
                    <span className={printTheme === 'light' ? 'text-indigo-600' : 'text-cyan-400'}>
                      THE ERA OF AI
                    </span>
                    <span className={printTheme === 'light' ? 'text-slate-900' : 'text-white'}>
                      — Technical Quick Revision Cheatsheet
                    </span>
                  </div>
                  <p className={`text-xs mt-0.5 ${printTheme === 'light' ? 'text-slate-600' : 'text-slate-400'}`}>
                    Active study guide • {customItems.length} High-Yield Modules • {new Date().toLocaleDateString()}
                  </p>
                </div>
                <div className={`text-right text-[11px] font-mono ${printTheme === 'light' ? 'text-slate-500' : 'text-slate-500'}`}>
                  portal: the-era-of-ai.dev
                </div>
              </div>

              {/* Grid of Cards */}
              <div className={`grid gap-3.5 ${layoutColumns === 3 ? 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3' : 'grid-cols-1 md:grid-cols-2'}`}>
                {customItems.map((item, idx) => (
                  <div
                    key={item.id || idx}
                    className={`print-card rounded-lg p-3.5 border relative group transition ${
                      printTheme === 'light'
                        ? 'bg-slate-50/70 border-slate-200 text-slate-900'
                        : 'bg-slate-950/60 border-slate-800/90 text-slate-200 hover:border-slate-700'
                    }`}
                  >
                    {/* Delete item button (hidden on print) */}
                    <button
                      onClick={() => handleRemoveItem(item.id)}
                      className="no-print absolute top-2 right-2 p-1 rounded hover:bg-rose-500/20 text-slate-400 hover:text-rose-400 opacity-0 group-hover:opacity-100 transition"
                      title="Remove from Cheatsheet"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>

                    {/* Card Header */}
                    <div className="flex items-start justify-between gap-2 mb-1.5 pr-5">
                      <h4 className={`text-xs font-bold leading-snug ${printTheme === 'light' ? 'text-slate-950' : 'text-white'}`}>
                        {idx + 1}. {item.title}
                      </h4>
                      <span className={`text-[10px] font-mono font-semibold px-1.5 py-0.2 rounded shrink-0 border ${
                        printTheme === 'light' 
                          ? 'bg-indigo-50 text-indigo-700 border-indigo-200' 
                          : 'bg-cyan-500/10 text-cyan-300 border-cyan-500/30'
                      }`}>
                        {item.category}
                      </span>
                    </div>

                    {/* LaTeX Formula */}
                    {item.formula && (
                      <div className={`my-2 p-2 rounded border overflow-x-auto text-center ${
                        printTheme === 'light'
                          ? 'bg-white border-slate-200 text-slate-900 shadow-none'
                          : 'bg-slate-900/90 border-slate-800 text-cyan-300'
                      }`}>
                        <KaTeXRenderer math={item.formula} block={true} />
                      </div>
                    )}

                    {/* Definition */}
                    {item.definition && (
                      <p className={`text-[11px] leading-relaxed mb-2 ${printTheme === 'light' ? 'text-slate-700' : 'text-slate-300'}`}>
                        {item.definition}
                      </p>
                    )}

                    {/* Key Intuition / Takeaway */}
                    {item.takeaway && (
                      <div className={`text-[10.5px] leading-snug p-2 rounded border font-sans ${
                        printTheme === 'light'
                          ? 'bg-amber-50/60 border-amber-200/80 text-amber-950'
                          : 'bg-amber-500/10 border-amber-500/25 text-amber-200'
                      }`}>
                        <span className="font-bold">⚡ Key Insight: </span>
                        {item.takeaway}
                      </div>
                    )}
                  </div>
                ))}
              </div>

              {/* Sheet Footer */}
              <div className={`mt-6 pt-3 border-t text-center text-[10px] font-mono flex items-center justify-between ${
                printTheme === 'light' ? 'border-slate-200 text-slate-500' : 'border-slate-800 text-slate-500'
              }`}>
                <span>The Era of AI — Interactive Deep Tech Learning Platform</span>
                <span>Page 1 of 1 • Prepared for Technical Interviews & Model Architecture Reviews</span>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}
