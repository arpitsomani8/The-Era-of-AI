import React, { useState, useMemo } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { 
  Search, 
  BookOpen, 
  Layers, 
  ChevronDown, 
  ChevronUp, 
  ArrowUpRight,
  Bookmark,
  CheckCircle2,
  Network,
  GitBranch,
  ExternalLink,
  Compass
} from 'lucide-react';
import topicsData from '../data/topics.json';
import allNodesData from '../data/allNodes.json';
import { findConceptForSubtopic } from '../utils/conceptLookup';
import { useProgress } from '../context/ProgressContext';

// Curated inter-topic relationships across the curriculum
const CURATED_TOPIC_CONNECTIONS = {
  math_linalg: [
    { id: 'genai_embed', relation: 'Powers Vector Spaces' },
    { id: 'ml_unsupervised', relation: 'Matrix Decomposition (SVD & PCA)' }
  ],
  math_calc: [
    { id: 'ml_opt', relation: 'Supplies ∇ Gradients' },
    { id: 'dl_backprop', relation: 'Multivariate Chain Rule' }
  ],
  math_prob: [
    { id: 'ml_logistic', relation: 'Likelihood & Probabilities' },
    { id: 'dl_generative', relation: 'Prior Distributions & Latent SDEs' }
  ],
  math_info: [
    { id: 'ml_loss', relation: 'Derives Cross-Entropy' },
    { id: 'ml_trees', relation: 'Information Gain & Entropy' }
  ],
  data_scrub: [
    { id: 'data_impute', relation: 'Pipeline Next: Missing Value Imputation' },
    { id: 'data_scale', relation: 'Pipeline Follow-up: Outlier Cleansing' }
  ],
  data_impute: [
    { id: 'data_scrub', relation: 'Prerequisite: Anomaly Detection' },
    { id: 'data_scale', relation: 'Pipeline Next: Feature Standardization' }
  ],
  data_scale: [
    { id: 'ml_opt', relation: 'Enables Gradient Stability' },
    { id: 'math_linalg', relation: 'Distance Metric Normalization' }
  ],
  data_fe: [
    { id: 'ml_linear', relation: 'Supplies Feature Matrix X' },
    { id: 'genai_embed', relation: 'Dense Embeddings vs Sparse Crosses' }
  ],
  data_split: [
    { id: 'eval_tradeoff', relation: 'Measures Generalization & Leakage' },
    { id: 'eval_matrix', relation: 'Independent Validation Folds' }
  ],
  ml_linear: [
    { id: 'data_fe', relation: 'Feature Engineering Inputs' },
    { id: 'ml_loss', relation: 'Mean Squared Error Optimization' }
  ],
  ml_loss: [
    { id: 'dl_backprop', relation: 'Seed of Chain Rule' },
    { id: 'math_info', relation: 'Information Theoretic Loss' }
  ],
  ml_opt: [
    { id: 'dl_opt', relation: 'Evolves to Adam / AdamW' },
    { id: 'math_calc', relation: 'Supplied by ∇ Gradients' },
    { id: 'data_scale', relation: 'Enables Gradient Stability' }
  ],
  ml_logistic: [
    { id: 'dl_activations', relation: 'Sigmoid becomes Activation' },
    { id: 'math_prob', relation: 'Likelihood & Probabilities' }
  ],
  ml_reg: [
    { id: 'dl_norm', relation: 'Controls Overfitting' },
    { id: 'eval_tradeoff', relation: 'Bias-Variance Regularization' }
  ],
  ml_trees: [
    { id: 'math_info', relation: 'Information Gain & Entropy' },
    { id: 'eval_matrix', relation: 'Classification & Split Evaluation' }
  ],
  ml_unsupervised: [
    { id: 'math_linalg', relation: 'Eigenvalue Decomposition for PCA' },
    { id: 'genai_embed', relation: 'Cluster Analysis in Vector Space' }
  ],
  eval_matrix: [
    { id: 'genai_align', relation: 'Evaluates Alignment Quality' },
    { id: 'eval_curves', relation: 'Precision, Recall & F1 Boundaries' }
  ],
  eval_curves: [
    { id: 'eval_matrix', relation: 'Derives ROC-AUC & PR Curves' },
    { id: 'eval_tradeoff', relation: 'Threshold Tuning for Class Imbalance' }
  ],
  eval_tradeoff: [
    { id: 'data_split', relation: 'Measures Generalization' },
    { id: 'ml_reg', relation: 'Regularization to Prevent Overfitting' }
  ],
  dl_neurons: [
    { id: 'genai_attention', relation: 'Layered Linear Projections' },
    { id: 'dl_activations', relation: 'Non-linear Transformation of Latents' }
  ],
  dl_activations: [
    { id: 'ml_logistic', relation: 'Sigmoid becomes Activation' },
    { id: 'dl_backprop', relation: 'Non-vanishing Derivative Gradients' }
  ],
  dl_backprop: [
    { id: 'ml_loss', relation: 'Seed of Chain Rule' },
    { id: 'math_calc', relation: 'Multivariate Chain Rule' }
  ],
  dl_opt: [
    { id: 'genai_train', relation: 'Drives LoRA / Pre-training' },
    { id: 'ml_opt', relation: 'Evolves from Classical Optimization' }
  ],
  dl_norm: [
    { id: 'ml_reg', relation: 'Controls Overfitting' },
    { id: 'genai_attention', relation: 'Pre-LayerNorm in Transformers' }
  ],
  dl_vision: [
    { id: 'dl_neurons', relation: '2D Convolutional Receptive Fields' },
    { id: 'genai_embed', relation: 'Vision Transformers & Patch Embeddings' }
  ],
  dl_seq: [
    { id: 'genai_attention', relation: 'Evolution: Recurrence to Self-Attention' },
    { id: 'dl_backprop', relation: 'Backpropagation Through Time (BPTT)' }
  ],
  dl_generative: [
    { id: 'math_prob', relation: 'Diffusion SDEs & Latent Gaussian Priors' },
    { id: 'genai_train', relation: 'Score Matching & Denoiser Architectures' }
  ],
  genai_embed: [
    { id: 'genai_rag', relation: 'Generates Vector Chunks' },
    { id: 'math_linalg', relation: 'Vector Space Dot Products' }
  ],
  genai_attention: [
    { id: 'dl_neurons', relation: 'Layered Linear Projections' },
    { id: 'genai_train', relation: 'FlashAttention & KV-Cache Execution' }
  ],
  genai_train: [
    { id: 'dl_opt', relation: 'Drives LoRA / Pre-training' },
    { id: 'genai_align', relation: 'Base Model to Instruct Alignment' }
  ],
  genai_align: [
    { id: 'eval_matrix', relation: 'Evaluates Alignment Quality' },
    { id: 'genai_prompt_agents', relation: 'System Prompts & Safety Guardrails' }
  ],
  genai_rag: [
    { id: 'genai_embed', relation: 'Generates Vector Chunks' },
    { id: 'genai_prompt_agents', relation: 'Retrieval Augmentation for Agents' }
  ],
  genai_prompt_agents: [
    { id: 'genai_rag', relation: 'Tool Use & Vector DB Retrieval' },
    { id: 'genai_align', relation: 'Safety Guardrails & Constitutional AI' }
  ],
  mlops_root: [
    { id: 'eval_matrix', relation: 'Continuous Drift & Quality Monitoring' },
    { id: 'genai_rag', relation: 'Vector DB & Production Serving Pipelines' }
  ]
};

const getCategoryBadgeClass = (cat) => {
  switch (cat) {
    case 'math': return 'text-blue-400 bg-blue-500/10 border-blue-500/30';
    case 'data': return 'text-emerald-400 bg-emerald-500/10 border-emerald-500/30';
    case 'ml': return 'text-purple-400 bg-purple-500/10 border-purple-500/30';
    case 'eval': return 'text-amber-400 bg-amber-500/10 border-amber-500/30';
    case 'dl': return 'text-pink-400 bg-pink-500/10 border-pink-500/30';
    case 'genai': return 'text-indigo-400 bg-indigo-500/10 border-indigo-500/30';
    case 'mlops': return 'text-cyan-400 bg-cyan-500/10 border-cyan-500/30';
    default: return 'text-slate-300 bg-slate-800 border-slate-700';
  }
};

export default function SyllabusPage() {
  const { toggleCompleted, isCompleted, toggleBookmark, isBookmarked } = useProgress();
  const [searchParams] = useSearchParams();
  const initialTopic = searchParams.get('topic') || '';
  const [searchQuery, setSearchQuery] = useState(initialTopic);
  const [activeCategory, setActiveCategory] = useState('all');
  const [expandedTopics, setExpandedTopics] = useState(() => {
    // Default expand all to easily scan subtopics & connections
    return new Set(topicsData.map((t) => t.id));
  });

  const nodeMap = useMemo(() => {
    return new Map(allNodesData.map((n) => [n.id, n]));
  }, []);

  const categories = [
    { id: 'all', label: 'All Modules (34)' },
    { id: 'math', label: '1. Math Foundations' },
    { id: 'data', label: '2. Data Preprocessing' },
    { id: 'ml', label: '3. Classical ML' },
    { id: 'eval', label: '4. Model Evaluation' },
    { id: 'dl', label: '5. Deep Learning' },
    { id: 'genai', label: '6. Transformers & GenAI' },
  ];

  const toggleTopic = (id) => {
    setExpandedTopics((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  const toggleAll = (expand) => {
    if (expand) {
      setExpandedTopics(new Set(topicsData.map((t) => t.id)));
    } else {
      setExpandedTopics(new Set());
    }
  };

  const filteredTopics = useMemo(() => {
    return topicsData.filter((topic) => {
      if (activeCategory !== 'all' && topic.category !== activeCategory) {
        return false;
      }
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase();
        const matchTitle = topic.label?.toLowerCase().includes(q);
        const matchSub = topic.subtopics?.some((s) => s.toLowerCase().includes(q));
        const conns = CURATED_TOPIC_CONNECTIONS[topic.id] || [];
        const matchConn = conns.some((c) => {
          const targetNode = nodeMap.get(c.id);
          return targetNode?.label?.toLowerCase().includes(q) || c.relation?.toLowerCase().includes(q);
        });
        if (!matchTitle && !matchSub && !matchConn) return false;
      }
      return true;
    });
  }, [activeCategory, searchQuery, nodeMap]);

  return (
    <div className="flex-1 w-full h-full overflow-y-auto bg-slate-950 text-slate-100 p-4 sm:p-6 md:p-10">
      <div className="max-w-5xl mx-auto space-y-6 pb-20 print-container">
        {/* Header Section */}
        <div className="border-b border-slate-800 pb-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 text-indigo-300 border border-indigo-500/30 text-xs font-semibold uppercase tracking-wider mb-2">
              <BookOpen className="w-3.5 h-3.5" />
              Curriculum Roadmap
            </div>
            <h1 className="text-2xl sm:text-3xl md:text-4xl font-extrabold text-white tracking-tight">
              Line-wise Master AI & Machine Learning Syllabus
            </h1>
            <p className="text-xs sm:text-sm text-slate-400 mt-1 max-w-3xl">
              Clean curriculum index: explore core topics, line-wise subtopics, and inter-domain connected pathways with direct redirect links to their in-depth breakdowns.
            </p>
          </div>

          <div className="flex items-center gap-2 no-print shrink-0">
            <button
              onClick={() => toggleAll(true)}
              className="px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-700 hover:bg-slate-800 text-xs text-slate-300 font-medium transition"
            >
              Expand All
            </button>
            <button
              onClick={() => toggleAll(false)}
              className="px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-700 hover:bg-slate-800 text-xs text-slate-300 font-medium transition"
            >
              Collapse All
            </button>
          </div>
        </div>

        {/* Filter & Search Bar */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 no-print">
          {/* Search Box */}
          <div className="relative flex-1 max-w-md">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search syllabus by topic, subtopic, or connected concept..."
              className="w-full bg-slate-900 border border-slate-800 text-xs sm:text-sm text-white rounded-xl pl-9 pr-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-indigo-500 placeholder-slate-500"
            />
            <Search className="w-4 h-4 absolute left-3 top-3 text-slate-500" />
            {searchQuery && (
              <button
                onClick={() => setSearchQuery('')}
                className="absolute right-3 top-2.5 text-slate-500 hover:text-white text-xs"
              >
                &times;
              </button>
            )}
          </div>

          {/* Category Filter Buttons */}
          <div className="flex items-center overflow-x-auto no-scrollbar space-x-1.5 pb-1">
            {categories.map((cat) => (
              <button
                key={cat.id}
                onClick={() => setActiveCategory(cat.id)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition ${
                  activeCategory === cat.id
                    ? 'bg-indigo-600 text-white shadow'
                    : 'bg-slate-900 text-slate-400 hover:text-white border border-slate-800'
                }`}
              >
                {cat.label}
              </button>
            ))}
          </div>
        </div>

        {/* Results Counter */}
        <div className="flex items-center justify-between text-xs text-slate-400 no-print">
          <span>Showing {filteredTopics.length} of {topicsData.length} core syllabus modules</span>
        </div>

        {/* Topics List */}
        <div className="space-y-4">
          {filteredTopics.map((topic, index) => {
            const isExpanded = expandedTopics.has(topic.id);
            const isDone = isCompleted(topic.id);
            const bookmarked = isBookmarked(topic.id);
            const connectedTopics = CURATED_TOPIC_CONNECTIONS[topic.id] || [];

            return (
              <div
                key={topic.id}
                id={`topic-${topic.id}`}
                className={`border rounded-2xl overflow-hidden shadow-sm transition ${
                  isDone 
                    ? 'bg-slate-900/95 border-emerald-500/40 ring-1 ring-emerald-500/20' 
                    : 'bg-slate-900/90 border-slate-800 hover:border-slate-700'
                }`}
              >
                {/* Topic Header Card */}
                <div
                  onClick={() => toggleTopic(topic.id)}
                  className="p-4 sm:p-5 flex items-center justify-between cursor-pointer hover:bg-slate-800/40 select-none transition gap-3"
                >
                  <div className="flex items-center gap-3 min-w-0">
                    <span className={`w-7 h-7 rounded-lg font-mono text-xs font-bold flex items-center justify-center shrink-0 border ${
                      isDone 
                        ? 'bg-emerald-500/20 border-emerald-500/40 text-emerald-300' 
                        : 'bg-indigo-500/10 border-indigo-500/30 text-indigo-400'
                    }`}>
                      {index + 1}
                    </span>
                    <div className="min-w-0">
                      <div className="flex items-center gap-2 flex-wrap">
                        <h2 className={`text-base sm:text-lg font-bold tracking-tight ${
                          isDone ? 'text-emerald-100 line-through decoration-emerald-500/40' : 'text-white'
                        }`}>
                          {topic.label}
                        </h2>
                        <span className={`text-[10px] px-2 py-0.5 rounded-full uppercase font-semibold border ${getCategoryBadgeClass(topic.category)}`}>
                          {topic.category}
                        </span>
                        {isDone && (
                          <span className="text-[10px] px-2 py-0.5 rounded-full font-semibold bg-emerald-500/15 text-emerald-300 border border-emerald-500/30 flex items-center gap-1">
                            <CheckCircle2 className="w-3 h-3 text-emerald-400" />
                            Mastered
                          </span>
                        )}
                      </div>
                      <div className="flex items-center gap-2 mt-1 text-xs text-slate-400 flex-wrap">
                        <span>{topic.subtopics?.length || 0} Subtopics</span>
                        <span>•</span>
                        <span>{connectedTopics.length} Connected Topics</span>
                      </div>
                    </div>
                  </div>

                  <div className="no-print flex items-center gap-2 shrink-0">
                    {/* Direct redirect to Core Concepts topic view */}
                    <Link
                      to={`/concepts?topic=${encodeURIComponent(topic.id)}`}
                      onClick={(e) => e.stopPropagation()}
                      className="hidden sm:inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg text-xs font-medium bg-indigo-500/10 text-indigo-300 hover:bg-indigo-500/20 border border-indigo-500/30 hover:border-indigo-500/50 transition"
                      title={`Open detailed study breakdown for "${topic.label}" in Core Concepts`}
                    >
                      <span>Explore Detail</span>
                      <ArrowUpRight className="w-3.5 h-3.5" />
                    </Link>

                    {/* Direct redirect to Mind Map node */}
                    <Link
                      to={`/mindmap?node=${encodeURIComponent(topic.id)}`}
                      onClick={(e) => e.stopPropagation()}
                      className="hidden md:inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg text-xs font-medium bg-slate-800 text-slate-300 hover:text-white hover:bg-slate-700 border border-slate-700 transition"
                      title={`View "${topic.label}" on 2D Knowledge Graph`}
                    >
                      <Network className="w-3.5 h-3.5 text-cyan-400" />
                      <span>Mind Map</span>
                    </Link>

                    {/* Mark as Mastered button */}
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        toggleCompleted(topic.id);
                      }}
                      className={`p-1.5 rounded-lg border transition ${
                        isDone 
                          ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40' 
                          : 'bg-slate-800 text-slate-400 hover:text-slate-200 border-slate-700'
                      }`}
                      title={isDone ? 'Mark as Incomplete' : 'Mark module as Mastered'}
                    >
                      <CheckCircle2 className={`w-4 h-4 ${isDone ? 'fill-emerald-400/20 text-emerald-400' : ''}`} />
                    </button>

                    {/* Bookmark button */}
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        toggleBookmark({
                          id: topic.id,
                          type: 'syllabus',
                          title: topic.label,
                          subtitle: topic.subtopics?.slice(0, 3).join(', '),
                          link: `/syllabus?topic=${encodeURIComponent(topic.label)}`
                        });
                      }}
                      className={`p-1.5 rounded-lg border transition ${
                        bookmarked 
                          ? 'bg-amber-500/20 text-amber-300 border-amber-500/40' 
                          : 'bg-slate-800 text-slate-400 hover:text-slate-200 border-slate-700'
                      }`}
                      title={bookmarked ? 'Remove Bookmark' : 'Bookmark to Study Vault'}
                    >
                      <Bookmark className={`w-4 h-4 ${bookmarked ? 'fill-amber-400 text-amber-400' : ''}`} />
                    </button>

                    <div className="text-slate-400 pl-1">
                      {isExpanded ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
                    </div>
                  </div>
                </div>

                {/* Expanded Body: ONLY Subtopics and Connected Topics with Redirect Links */}
                {isExpanded && (
                  <div className="p-4 sm:p-5 border-t border-slate-800/80 bg-slate-950/40 space-y-5 text-xs sm:text-sm">
                    {/* 1. Subtopics Section */}
                    {topic.subtopics && topic.subtopics.length > 0 && (
                      <div>
                        <div className="flex items-center justify-between mb-2.5">
                          <h3 className="text-xs font-bold text-indigo-300 uppercase tracking-wider flex items-center gap-1.5">
                            <Layers className="w-3.5 h-3.5 text-indigo-400" />
                            Subtopics ({topic.subtopics.length})
                          </h3>
                          <Link 
                            to={`/concepts?topic=${encodeURIComponent(topic.id)}`}
                            className="text-[11px] text-indigo-400 hover:text-indigo-300 font-medium flex items-center gap-1 group transition"
                          >
                            <span>Explore all in Core Concepts</span>
                            <ArrowUpRight className="w-3 h-3 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform" />
                          </Link>
                        </div>

                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                          {topic.subtopics.map((sub, sIdx) => {
                            const concept = findConceptForSubtopic(sub, topic.id);
                            const targetUrl = concept
                              ? `/concepts?id=${encodeURIComponent(concept.id)}`
                              : `/concepts?search=${encodeURIComponent(sub)}`;

                            return (
                              <Link
                                key={sIdx}
                                to={targetUrl}
                                className="p-2.5 rounded-xl bg-slate-900/80 hover:bg-indigo-600/15 text-slate-200 hover:text-white border border-slate-800 hover:border-indigo-500/40 transition-all flex items-start justify-between gap-2.5 group shadow-sm"
                                title={`Open detailed breakdown, math formulas, and code sandbox for "${sub}" in Core Concepts`}
                              >
                                <div className="flex items-start gap-2.5 min-w-0">
                                  <span className="w-2 h-2 rounded-full bg-indigo-400 mt-1.5 shrink-0 group-hover:scale-125 transition-transform"></span>
                                  <div className="min-w-0">
                                    <p className="text-xs font-medium text-slate-200 group-hover:text-indigo-200 leading-snug">
                                      {sub}
                                    </p>
                                    <span className="text-[10px] text-slate-500 group-hover:text-indigo-400/80">
                                      Open detail section &rarr;
                                    </span>
                                  </div>
                                </div>
                                <ArrowUpRight className="w-3.5 h-3.5 text-slate-500 group-hover:text-indigo-300 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform shrink-0 mt-0.5" />
                              </Link>
                            );
                          })}
                        </div>
                      </div>
                    )}

                    {/* 2. Connected Topics Section */}
                    {connectedTopics.length > 0 && (
                      <div className="pt-2 border-t border-slate-800/60">
                        <div className="flex items-center justify-between mb-2.5">
                          <h3 className="text-xs font-bold text-cyan-300 uppercase tracking-wider flex items-center gap-1.5">
                            <GitBranch className="w-3.5 h-3.5 text-cyan-400" />
                            Connected Topics ({connectedTopics.length})
                          </h3>
                          <Link 
                            to={`/mindmap?node=${encodeURIComponent(topic.id)}`}
                            className="text-[11px] text-cyan-400 hover:text-cyan-300 font-medium flex items-center gap-1 group transition"
                          >
                            <span>Inspect node connections in Mind Map</span>
                            <Network className="w-3 h-3 group-hover:scale-110 transition-transform" />
                          </Link>
                        </div>

                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                          {connectedTopics.map((conn, cIdx) => {
                            const targetNode = nodeMap.get(conn.id);
                            if (!targetNode) return null;
                            const targetConceptUrl = `/concepts?topic=${encodeURIComponent(conn.id)}`;
                            const targetMapUrl = `/mindmap?node=${encodeURIComponent(conn.id)}`;

                            return (
                              <div
                                key={cIdx}
                                className="p-2.5 rounded-xl bg-slate-900/60 hover:bg-slate-900 border border-slate-800/90 hover:border-cyan-500/40 transition-all flex flex-col justify-between gap-2 shadow-sm"
                              >
                                <div className="flex items-start justify-between gap-2">
                                  <div className="min-w-0">
                                    <div className="flex items-center gap-1.5 mb-1">
                                      <span className="text-[10px] px-2 py-0.5 rounded-full font-semibold bg-cyan-500/10 text-cyan-300 border border-cyan-500/25">
                                        {conn.relation}
                                      </span>
                                      <span className={`text-[9px] px-1.5 py-0.2 rounded uppercase font-bold border ${getCategoryBadgeClass(targetNode.category)}`}>
                                        {targetNode.category}
                                      </span>
                                    </div>
                                    <h4 className="text-xs font-bold text-slate-100">
                                      {targetNode.label}
                                    </h4>
                                  </div>
                                </div>

                                <div className="flex items-center gap-2 pt-1 border-t border-slate-800/40">
                                  <Link
                                    to={targetConceptUrl}
                                    className="inline-flex items-center gap-1 text-[11px] font-medium text-indigo-400 hover:text-indigo-300 transition"
                                    title={`Go to detail page for ${targetNode.label}`}
                                  >
                                    <span>Detail section</span>
                                    <ArrowUpRight className="w-3 h-3" />
                                  </Link>
                                  <span className="text-slate-700">•</span>
                                  <Link
                                    to={targetMapUrl}
                                    className="inline-flex items-center gap-1 text-[11px] font-medium text-cyan-400 hover:text-cyan-300 transition"
                                    title={`View ${targetNode.label} on Mind Map`}
                                  >
                                    <Network className="w-3 h-3" />
                                    <span>Mind Map</span>
                                  </Link>
                                </div>
                              </div>
                            );
                          })}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

