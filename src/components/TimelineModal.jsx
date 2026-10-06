import React, { useState, useMemo } from 'react';
import { 
  X, 
  History, 
  Calendar, 
  Sparkles, 
  ExternalLink, 
  Search, 
  Filter, 
  ChevronRight, 
  BookOpen, 
  Award, 
  Cpu, 
  Layers, 
  Zap, 
  ArrowRight,
  TrendingUp
} from 'lucide-react';
import KaTeXRenderer from './KaTeXRenderer';
import AudioExplainerButton from './AudioExplainerButton';

export const AI_MILESTONES = [
  // Era 1: The Dawn (1950–1969)
  {
    id: 'turing-1950',
    year: 1950,
    era: 'dawn',
    eraLabel: 'Dawn of Machine Intelligence (1950–1969)',
    title: 'The Turing Test & Imitation Game',
    pioneers: 'Alan Turing',
    category: 'Foundational Theory',
    badgeColor: 'bg-blue-500/15 text-blue-300 border-blue-500/30',
    summary: 'Alan Turing published "Computing Machinery and Intelligence" proposing the operational question: Can machines think? Introduced the Imitation Game benchmark.',
    formula: '\\text{Turing Criterion}: \\ P(\\text{Judge identifies Human}) \\approx P(\\text{Judge identifies Machine}) \\approx 0.5',
    impact: 'Defined the philosophical and functional foundation of artificial intelligence for the next seven decades.',
    paperLink: 'https://academic.oup.com/mind/article/LIX/236/433/986238'
  },
  {
    id: 'dartmouth-1956',
    year: 1956,
    era: 'dawn',
    eraLabel: 'Dawn of Machine Intelligence (1950–1969)',
    title: 'Dartmouth Workshop: Coining "Artificial Intelligence"',
    pioneers: 'John McCarthy, Marvin Minsky, Nathaniel Rochester, Claude Shannon',
    category: 'Field Inception',
    badgeColor: 'bg-indigo-500/15 text-indigo-300 border-indigo-500/30',
    summary: 'The landmark summer research conference where the discipline of Artificial Intelligence was formally founded as an academic field.',
    formula: '\\text{Conjecture}: \\text{ Every aspect of learning can be described so precisely a machine can simulate it.}',
    impact: 'Catalyzed initial public and governmental research funding across symbolic reasoning and automata theory.'
  },
  {
    id: 'perceptron-1957',
    year: 1957,
    era: 'dawn',
    eraLabel: 'Dawn of Machine Intelligence (1950–1969)',
    title: 'The Perceptron & Hardware Neural Classifier',
    pioneers: 'Frank Rosenblatt (Cornell Aeronautical Laboratory)',
    category: 'Neural Architecture',
    badgeColor: 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30',
    summary: 'Built the Mark I Perceptron hardware computer for visual pattern recognition. Established the mathematical threshold neuron model.',
    formula: 'y = f\\left(\\sum_{i=1}^d w_i x_i + b\\right), \\quad f(z) = \\begin{cases} 1 & \\text{if } z \\geq 0 \\\\ 0 & \\text{otherwise} \\end{cases}',
    impact: 'First biologically-inspired trainable artificial neuron algorithm with formal convergence guarantee on linearly separable data.'
  },
  {
    id: 'minsky-xor-1969',
    year: 1969,
    era: 'dawn',
    eraLabel: 'Dawn of Machine Intelligence (1950–1969)',
    title: 'Minsky & Papert: The XOR Limitation & 1st AI Winter',
    pioneers: 'Marvin Minsky & Seymour Papert',
    category: 'Theoretical Limits',
    badgeColor: 'bg-rose-500/15 text-rose-300 border-rose-500/30',
    summary: 'Published "Perceptrons", mathematically proving single-layer linear models cannot compute the non-linearly separable XOR boolean logic function.',
    formula: '\\text{XOR}(0,1)=\\text{XOR}(1,0)=1, \\ \\text{XOR}(0,0)=\\text{XOR}(1,1)=0 \\implies \\nexists \\ (w_1, w_2, b) \\text{ separating classes}',
    impact: 'Severely dampened funding for neural network research for over a decade, precipitating the first "AI Winter".'
  },

  // Era 2: Connectionist Revival & ML Emergence (1970–1999)
  {
    id: 'backprop-1986',
    year: 1986,
    era: 'revival',
    eraLabel: 'Connectionist Revival & Statistical ML (1970–1999)',
    title: 'Backpropagation Through Multi-Layer Networks',
    pioneers: 'David Rumelhart, Geoffrey Hinton, Ronald Williams',
    category: 'Algorithmic Breakthrough',
    badgeColor: 'bg-purple-500/15 text-purple-300 border-purple-500/30',
    summary: 'Popularized the application of generalized reverse-mode automatic differentiation (chain rule) for training multi-layer hidden representations in neural networks.',
    formula: '\\frac{\\partial \\mathcal{L}}{\\partial w_{ij}^{(l)}} = \\delta_i^{(l)} a_j^{(l-1)}, \\quad \\delta_i^{(l)} = \\left(\\sum_k \\delta_k^{(l+1)} w_{ki}^{(l+1)}\\right) \\sigma\'\\left(z_i^{(l)}\\right)',
    impact: 'Shattered the XOR limitation and established the universal optimization method for all modern deep learning.'
  },
  {
    id: 'lenet-1989',
    year: 1989,
    era: 'revival',
    eraLabel: 'Connectionist Revival & Statistical ML (1970–1999)',
    title: 'LeNet-1 & Convolutional Weight Sharing',
    pioneers: 'Yann LeCun et al. (Bell Labs)',
    category: 'Computer Vision',
    badgeColor: 'bg-cyan-500/15 text-cyan-300 border-cyan-500/30',
    summary: 'Trained a Convolutional Neural Network with spatial weight-sharing kernels directly on handwritten ZIP codes for the US Postal Service.',
    formula: 'y_{i,j} = \\sigma\\left(\\sum_{m} \\sum_{n} w_{m,n} x_{i+m, j+n} + b\\right)',
    impact: 'Proved translational invariance and parameter efficiency over fully connected layers for visual grids.'
  },
  {
    id: 'lstm-1997',
    year: 1997,
    era: 'revival',
    eraLabel: 'Connectionist Revival & Statistical ML (1970–1999)',
    title: 'Long Short-Term Memory (LSTM) Networks',
    pioneers: 'Sepp Hochreiter & Jürgen Schmidhuber',
    category: 'Sequence Modeling',
    badgeColor: 'bg-amber-500/15 text-amber-300 border-amber-500/30',
    summary: 'Introduced memory cells with input, forget, and output gating mechanisms that provide an additive gradient highway, solving vanishing gradients in RNNs.',
    formula: 'c_t = f_t \\odot c_{t-1} + i_t \\odot \\tilde{c}_t, \\quad h_t = o_t \\odot \\tanh(c_t)',
    impact: 'Dominated speech recognition, machine translation, and text modeling until the Transformer era.'
  },

  // Era 3: The Deep Learning Revolution (2000–2016)
  {
    id: 'alexnet-2012',
    year: 2012,
    era: 'revolution',
    eraLabel: 'The Deep Learning Revolution (2000–2016)',
    title: 'AlexNet: GPU Acceleration & ImageNet Victory',
    pioneers: 'Alex Krizhevsky, Ilya Sutskever, Geoffrey Hinton',
    category: 'Hardware & Architecture',
    badgeColor: 'bg-rose-500/15 text-rose-300 border-rose-500/30',
    summary: 'Trained an 8-layer deep CNN on dual NVIDIA GTX 580 GPUs with ReLU and Dropout, slashing ImageNet top-5 classification error from 26% to 15.3%.',
    formula: '\\text{ReLU}(z) = \\max(0, z) \\implies \\frac{\\partial}{\\partial z} = 1 \\text{ for } z > 0 \\text{ (prevents gradient vanishing)}',
    impact: 'The defining catalyst of modern AI. Convinced the computer vision and machine learning community that deep learning with GPU compute was the future.'
  },
  {
    id: 'gan-2014',
    year: 2014,
    era: 'revolution',
    eraLabel: 'The Deep Learning Revolution (2000–2016)',
    title: 'Generative Adversarial Networks (GANs)',
    pioneers: 'Ian Goodfellow et al. (Univ. of Montreal)',
    category: 'Generative Models',
    badgeColor: 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30',
    summary: 'Formulated generative modeling as a two-player zero-sum minimax game between a Generator producing synthetic samples and a Discriminator.',
    formula: '\\min_G \\max_D V(D, G) = \\mathbb{E}_{x \\sim p_{\\text{data}}}[\\log D(x)] + \\mathbb{E}_{z \\sim p_z}[\\log(1 - D(G(z)))]',
    impact: 'Ignited a tidal wave of photorealistic image synthesis, deepfakes, and adversarial game theory in machine learning.'
  },
  {
    id: 'resnet-2015',
    year: 2015,
    era: 'revolution',
    eraLabel: 'The Deep Learning Revolution (2000–2016)',
    title: 'ResNet: Deep Residual Learning & Identity Shortcuts',
    pioneers: 'Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun (MSRA)',
    category: 'Deep Architecture',
    badgeColor: 'bg-purple-500/15 text-purple-300 border-purple-500/30',
    summary: 'Introduced residual identity skip connections $y = \\mathcal{F}(x) + x$, allowing networks with over 152 layers to train stably and win ImageNet 2015.',
    formula: 'y = \\mathcal{F}(x, \\{W_i\\}) + x \\implies \\frac{\\partial \\mathcal{L}}{\\partial x} = \\frac{\\partial \\mathcal{L}}{\\partial y} \\left(\\frac{\\partial \\mathcal{F}}{\\partial x} + 1\\right)',
    impact: 'Solved optimization degradation in ultra-deep networks; identity skip connections are standard in every modern Transformer block.'
  },
  {
    id: 'alphago-2016',
    year: 2016,
    era: 'revolution',
    eraLabel: 'The Deep Learning Revolution (2000–2016)',
    title: 'AlphaGo Defeats 18-Time World Go Champion',
    pioneers: 'David Silver, Demis Hassabis et al. (Google DeepMind)',
    category: 'Deep RL & Search',
    badgeColor: 'bg-cyan-500/15 text-cyan-300 border-cyan-500/30',
    summary: 'Combined Monte Carlo Tree Search (MCTS) with deep policy and value neural networks to defeat Lee Sedol 4-1 in Go, an ancient game with $10^{170}$ board states.',
    formula: 'Q(s, a) = \\frac{1}{N(s, a)} \\sum_{i=1}^N V(s_i), \\quad a^* = \\arg\\max_a \\left(Q(s, a) + c_{\\text{puct}} P(s, a) \\frac{\\sqrt{\\sum_b N(s, b)}}{1 + N(s, a)}\\right)',
    impact: 'A watershed demonstration that AI could master intuitive human strategy and creativity (Move 37).'
  },

  // Era 4: The Transformer Epoch (2017–2022)
  {
    id: 'transformer-2017',
    year: 2017,
    era: 'transformer',
    eraLabel: 'The Transformer & Foundation Model Epoch (2017–2022)',
    title: 'Attention Is All You Need (The Transformer)',
    pioneers: 'Vaswani, Shazeer, Parmar, Uszkoreit, Jones, Gomez, Kaiser, Polosukhin (Google Brain / Research)',
    category: 'Paradigm Shift',
    badgeColor: 'bg-amber-500/15 text-amber-300 border-amber-500/30',
    summary: 'Replaced recurrence and convolutions entirely with Scaled Dot-Product Multi-Head Self-Attention, unlocking massive GPU training parallelism.',
    formula: '\\text{Attention}(Q, K, V) = \\text{softmax}\\left(\\frac{QK^T}{\\sqrt{d_k}}\\right)V',
    impact: 'The foundational architectural backbone of GPT-4, Gemini, Claude, LLaMA, AlphaFold 2, Stable Diffusion, and all modern foundation models.'
  },
  {
    id: 'bert-gpt-2018',
    year: 2018,
    era: 'transformer',
    eraLabel: 'The Transformer & Foundation Model Epoch (2017–2022)',
    title: 'BERT & GPT-1: Pre-training + Fine-Tuning Era',
    pioneers: 'Jacob Devlin (BERT @ Google) & Alec Radford (GPT-1 @ OpenAI)',
    category: 'Self-Supervised Learning',
    badgeColor: 'bg-blue-500/15 text-blue-300 border-blue-500/30',
    summary: 'Shifted NLP from task-specific feature engineering to large-scale self-supervised pre-training (Masked LM & Causal LM) followed by downstream transfer fine-tuning.',
    formula: '\\mathcal{L}_{\\text{BERT}} = -\\sum_{i \\in M} \\log P(x_i \\mid \\tilde{x}), \\quad \\mathcal{L}_{\\text{GPT}} = -\\sum_{t=1}^T \\log P(x_t \\mid x_{<t})',
    impact: 'Unified Natural Language Processing under pre-trained foundation models.'
  },
  {
    id: 'gpt3-2020',
    year: 2020,
    era: 'transformer',
    eraLabel: 'The Transformer & Foundation Model Epoch (2017–2022)',
    title: 'GPT-3 & Emergent Few-Shot In-Context Learning',
    pioneers: 'Tom Brown, Benjamin Mann, Dario Amodei et al. (OpenAI)',
    category: 'Scaling Laws',
    badgeColor: 'bg-purple-500/15 text-purple-300 border-purple-500/30',
    summary: 'Demonstrated that scaling autoregressive transformers to 175 billion parameters unlocks in-context learning without gradient weight updates.',
    formula: 'P(y \\mid x, \\text{prompt}) = \\prod_{i=1}^m P(y_i \\mid [x_1, y_1, \\dots, x_k, y_k, x, y_{<i}])',
    impact: 'Ignited the commercial Generative AI era and prompted the discovery of empirical scaling laws.'
  },
  {
    id: 'chatgpt-diffusion-2022',
    year: 2022,
    era: 'transformer',
    eraLabel: 'The Transformer & Foundation Model Epoch (2017–2022)',
    title: 'ChatGPT (RLHF) & Latent Diffusion (Stable Diffusion)',
    pioneers: 'OpenAI (ChatGPT) & Rombach, Blattmann et al. (CompVis / Stability)',
    category: 'Mainstream Adoption',
    badgeColor: 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30',
    summary: 'Reinforcement Learning from Human Feedback (RLHF) aligned LLMs into conversational assistants (100M users in 2 months). Latent diffusion democratized image generation on consumer GPUs.',
    formula: '\\max_\\theta \\mathbb{E}_{(x, y) \\sim D}\\left[r_\\psi(x, y) - \\beta \\mathbb{D}_{\\text{KL}}(\\pi_\\theta(y|x) \\parallel \\pi_{\\text{ref}}(y|x))\\right]',
    impact: 'Made artificial intelligence a global cultural and economic phenomenon.'
  },

  // Era 5: Frontier Reasoning, Open Weights & Agents (2023–2026)
  {
    id: 'llama-open-2023',
    year: 2023,
    era: 'frontier',
    eraLabel: 'Frontier Reasoning & Open Weights (2023–2026)',
    title: 'LLaMA & The Open-Weight Ecosystem Revolution',
    pioneers: 'Meta AI (Touvron et al.) & Open-Source Community',
    category: 'Open Source Ecosystem',
    badgeColor: 'bg-cyan-500/15 text-cyan-300 border-cyan-500/30',
    summary: 'Meta open-sourced LLaMA (7B–65B) under research license, sparking an explosion of efficient fine-tuning (LoRA, QLoRA), local quantization (llama.cpp, Ollama), and open models (Mistral, Gemma).',
    formula: 'W = W_0 + \\frac{\\alpha}{r} B A, \\quad B \\in \\mathbb{R}^{d \\times r}, A \\in \\mathbb{R}^{r \\times k}',
    impact: 'Democratized frontier LLM research away from closed corporate APIs to local laptops and global open communities.'
  },
  {
    id: 'reasoning-o1-2024',
    year: 2024,
    era: 'frontier',
    eraLabel: 'Frontier Reasoning & Open Weights (2023–2026)',
    title: 'Test-Time Compute Scaling & Reasoning Models (o1)',
    pioneers: 'OpenAI (o1 / Strawberry Architecture)',
    category: 'Reasoning Scaling',
    badgeColor: 'bg-indigo-500/15 text-indigo-300 border-indigo-500/30',
    summary: 'Introduced inference-time compute scaling: models generate internal chain-of-thought tokens, self-correct, and evaluate search trees prior to responding, drastically outperforming standard LLMs on competitive math and code.',
    formula: '\\text{Accuracy} \\propto f(\\text{Test-Time Compute}) \\approx f(\\text{Number of Hidden Reasoning Tokens})',
    impact: 'Unlocked a second scaling dimension: spending more compute at inference time instead of only pre-training.'
  },
  {
    id: 'deepseek-r1-2025',
    year: 2025,
    era: 'frontier',
    eraLabel: 'Frontier Reasoning & Open Weights (2023–2026)',
    title: 'DeepSeek-R1: Pure RL Reasoning Emergence',
    pioneers: 'DeepSeek-AI Team',
    category: 'Pure RL & Cost Efficiency',
    badgeColor: 'bg-rose-500/15 text-rose-300 border-rose-500/30',
    summary: 'Demonstrated that complex mathematical reasoning behaviors (self-reflection, backtracking, verification) emerge purely through Large-Scale Reinforcement Learning (GRPO) without cold-start human SFT, at a fraction of Western frontier cluster budgets.',
    formula: '\\text{Objective}_{\\text{GRPO}} = \\mathbb{E}\\left[\\frac{\\pi_\\theta(a_t|s_t)}{\\pi_{\\text{old}}(a_t|s_t)} A_i - \\beta \\mathbb{D}_{\\text{KL}}(\\pi_\\theta \\parallel \\pi_{\\text{ref}})\\right]',
    impact: 'Proved reasoning can be unlocked openly and cost-effectively, shifting global AI geopolitics and open-source foundation model research.'
  }
];

export default function TimelineModal({ isOpen, onClose }) {
  const [selectedEra, setSelectedEra] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedMilestoneId, setSelectedMilestoneId] = useState(AI_MILESTONES[0].id);

  const eras = [
    { id: 'all', label: 'All Eras (1950–2026)', count: AI_MILESTONES.length },
    { id: 'dawn', label: 'Dawn (1950–69)', count: AI_MILESTONES.filter(m => m.era === 'dawn').length },
    { id: 'revival', label: 'Revival (1970–99)', count: AI_MILESTONES.filter(m => m.era === 'revival').length },
    { id: 'revolution', label: 'Deep Learning (2000–16)', count: AI_MILESTONES.filter(m => m.era === 'revolution').length },
    { id: 'transformer', label: 'Transformer (2017–22)', count: AI_MILESTONES.filter(m => m.era === 'transformer').length },
    { id: 'frontier', label: 'Reasoning (2023–26)', count: AI_MILESTONES.filter(m => m.era === 'frontier').length },
  ];

  const filteredMilestones = useMemo(() => {
    return AI_MILESTONES.filter((m) => {
      if (selectedEra !== 'all' && m.era !== selectedEra) return false;
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase();
        const matchTitle = m.title.toLowerCase().includes(q);
        const matchPioneers = m.pioneers.toLowerCase().includes(q);
        const matchSummary = m.summary.toLowerCase().includes(q);
        const matchYear = String(m.year).includes(q);
        if (!matchTitle && !matchPioneers && !matchSummary && !matchYear) return false;
      }
      return true;
    });
  }, [selectedEra, searchQuery]);

  const selectedMilestone = useMemo(() => {
    return AI_MILESTONES.find(m => m.id === selectedMilestoneId) || filteredMilestones[0] || AI_MILESTONES[0];
  }, [selectedMilestoneId, filteredMilestones]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-5 bg-slate-950/80 backdrop-blur-md overflow-hidden">
      <div className="relative w-full max-w-6xl max-h-[92vh] flex flex-col bg-slate-900 border border-slate-700/80 rounded-2xl shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-200 text-slate-100">
        
        {/* Header */}
        <div className="px-5 py-4 border-b border-slate-800 bg-slate-950/60 flex items-center justify-between gap-4 shrink-0">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-amber-500/20 to-indigo-500/20 border border-amber-500/30 flex items-center justify-center text-amber-300 shadow-sm">
              <History className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-base sm:text-lg font-bold text-white tracking-tight">
                  Interactive AI History Timeline (1950 – 2026)
                </h2>
                <span className="text-[11px] font-mono bg-amber-500/15 text-amber-300 border border-amber-500/30 px-2 py-0.5 rounded-full">
                  76 Years of Breakthroughs
                </span>
              </div>
              <p className="text-xs text-slate-400">
                From the Turing Test and the Perceptron to Transformers, Reasoning Models & DeepSeek-R1.
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Toolbar: Eras & Search */}
        <div className="px-5 py-2.5 bg-slate-950/40 border-b border-slate-800 flex flex-wrap items-center justify-between gap-3 text-xs shrink-0">
          {/* Era Pills */}
          <div className="flex items-center gap-1.5 overflow-x-auto pb-1 sm:pb-0 max-w-full">
            <span className="text-slate-400 font-semibold whitespace-nowrap mr-1 flex items-center gap-1">
              <Calendar className="w-3.5 h-3.5 text-amber-400" />
              Era:
            </span>
            {eras.map(era => (
              <button
                key={era.id}
                onClick={() => setSelectedEra(era.id)}
                className={`px-2.5 py-1 rounded-md text-xs font-medium whitespace-nowrap transition border ${
                  selectedEra === era.id
                    ? 'bg-amber-500/20 text-amber-300 border-amber-500/50 shadow-sm'
                    : 'bg-slate-800/80 text-slate-400 border-slate-700/60 hover:text-slate-200 hover:bg-slate-800'
                }`}
              >
                {era.label}
              </button>
            ))}
          </div>

          {/* Search box */}
          <div className="relative w-full sm:w-56 shrink-0">
            <Search className="w-3.5 h-3.5 absolute left-2.5 top-2.5 text-slate-400" />
            <input
              type="text"
              placeholder="Search milestone or pioneer..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-8 pr-3 py-1 rounded-lg bg-slate-900 border border-slate-700/80 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-amber-500"
            />
          </div>
        </div>

        {/* Main 2-Column Split: Timeline Track List (Left) + Milestone Deep Dive (Right) */}
        <div className="flex-1 overflow-hidden flex flex-col md:flex-row">
          
          {/* Left Column: Chronological Milestone Track */}
          <div className="w-full md:w-96 border-b md:border-b-0 md:border-r border-slate-800 bg-slate-950/50 overflow-y-auto p-3 space-y-2 shrink-0">
            <div className="text-[11px] font-bold text-slate-400 uppercase tracking-wider px-2 py-1 flex items-center justify-between">
              <span>Timeline Milestones</span>
              <span>{filteredMilestones.length} items</span>
            </div>

            {filteredMilestones.map((m) => {
              const isSelected = selectedMilestone?.id === m.id;
              return (
                <div
                  key={m.id}
                  onClick={() => setSelectedMilestoneId(m.id)}
                  className={`p-3 rounded-xl border text-left cursor-pointer transition flex items-start gap-3 relative group ${
                    isSelected
                      ? 'bg-gradient-to-r from-amber-500/15 to-indigo-500/15 border-amber-500/50 shadow-md text-white'
                      : 'bg-slate-900/80 border-slate-800 hover:border-slate-700 text-slate-300 hover:text-white'
                  }`}
                >
                  {/* Year Tag */}
                  <div className={`px-2 py-1 rounded-lg text-xs font-mono font-bold shrink-0 border ${
                    isSelected 
                      ? 'bg-amber-500 text-slate-950 border-amber-400 shadow-sm' 
                      : 'bg-slate-800 text-amber-300 border-slate-700'
                  }`}>
                    {m.year}
                  </div>

                  <div className="min-w-0 flex-1">
                    <div className="text-xs font-bold leading-snug truncate">
                      {m.title}
                    </div>
                    <div className="text-[11px] text-slate-400 truncate mt-0.5">
                      {m.pioneers}
                    </div>
                    <div className="mt-1 flex items-center gap-1.5">
                      <span className={`text-[10px] font-mono px-1.5 py-0.2 rounded border ${m.badgeColor}`}>
                        {m.category}
                      </span>
                    </div>
                  </div>

                  <ChevronRight className={`w-4 h-4 shrink-0 transition-transform ${isSelected ? 'text-amber-400 translate-x-0.5' : 'text-slate-600'}`} />
                </div>
              );
            })}
          </div>

          {/* Right Column: Active Milestone Deep Dive View */}
          <div className="flex-1 overflow-y-auto p-5 sm:p-7 bg-slate-950/20">
            {selectedMilestone && (
              <div className="max-w-3xl mx-auto space-y-6">
                
                {/* Milestone Header */}
                <div className="border-b border-slate-800 pb-5 space-y-3">
                  <div className="flex flex-wrap items-center justify-between gap-3">
                    <div className="flex items-center gap-2">
                      <span className="text-2xl sm:text-3xl font-black font-mono text-amber-400 tracking-tight">
                        {selectedMilestone.year}
                      </span>
                      <span className={`text-xs font-mono font-semibold px-2.5 py-0.5 rounded-full border ${selectedMilestone.badgeColor}`}>
                        {selectedMilestone.category}
                      </span>
                    </div>

                    {/* Audio Explainer for the Milestone */}
                    <AudioExplainerButton
                      title={`${selectedMilestone.year}: ${selectedMilestone.title}`}
                      text={`Milestone ${selectedMilestone.year}: ${selectedMilestone.title}. Pioneers and contributors: ${selectedMilestone.pioneers}. Summary: ${selectedMilestone.summary}. Industry Impact: ${selectedMilestone.impact}`}
                    />
                  </div>

                  <h3 className="text-xl sm:text-2xl font-black text-white tracking-tight leading-snug">
                    {selectedMilestone.title}
                  </h3>

                  <div className="flex items-center gap-2 text-xs text-slate-400">
                    <Award className="w-3.5 h-3.5 text-indigo-400" />
                    <span>Pioneers & Contributors: <strong className="text-slate-200">{selectedMilestone.pioneers}</strong></span>
                  </div>
                </div>

                {/* Technical Overview & Summary */}
                <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-4 sm:p-5 space-y-2">
                  <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
                    <BookOpen className="w-3.5 h-3.5 text-amber-400" />
                    Historical Summary & Mechanics
                  </h4>
                  <p className="text-xs sm:text-sm text-slate-200 leading-relaxed">
                    {selectedMilestone.summary}
                  </p>
                </div>

                {/* Mathematical Formulation */}
                {selectedMilestone.formula && (
                  <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-4 sm:p-5 space-y-2">
                    <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
                      <Cpu className="w-3.5 h-3.5 text-cyan-400" />
                      Core Mathematical Formulation
                    </h4>
                    <div className="py-2 px-3 rounded-lg bg-slate-950 border border-slate-800 overflow-x-auto text-center">
                      <KaTeXRenderer math={selectedMilestone.formula} block={true} />
                    </div>
                  </div>
                )}

                {/* Historical Impact & Legacy */}
                <div className="bg-amber-500/10 border border-amber-500/25 rounded-xl p-4 sm:p-5 space-y-2">
                  <h4 className="text-xs font-bold text-amber-300 uppercase tracking-wider flex items-center gap-1.5">
                    <TrendingUp className="w-3.5 h-3.5 text-amber-400" />
                    Long-Term Industry & Scientific Impact
                  </h4>
                  <p className="text-xs sm:text-sm text-amber-100/90 leading-relaxed">
                    {selectedMilestone.impact}
                  </p>
                </div>

                {/* Links if available */}
                {selectedMilestone.paperLink && (
                  <div className="pt-2">
                    <a
                      href={selectedMilestone.paperLink}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-2 text-xs font-semibold text-cyan-400 hover:text-cyan-300 hover:underline"
                    >
                      <span>Read Original Landmark Publication</span>
                      <ExternalLink className="w-3.5 h-3.5" />
                    </a>
                  </div>
                )}

              </div>
            )}
          </div>

        </div>

      </div>
    </div>
  );
}
