import React, { useState, useRef, useEffect, useMemo, useCallback } from 'react';
import { useSearchParams } from 'react-router-dom';
import { 
  ZoomIn, 
  ZoomOut, 
  RotateCcw, 
  Share2, 
  Search, 
  Filter, 
  Info,
  Layers,
  ChevronRight,
  ChevronLeft,
  Download,
  Route,
  Sparkles,
  X
} from 'lucide-react';
import { useTheme } from '../context/ThemeContext';
import allNodesData from '../data/allNodes.json';
import crossLinksData from '../data/crossLinks.json';
import NodeInspector from '../components/NodeInspector';

export const CAREER_TRACKS = {
  genai_engineer: {
    id: 'genai_engineer',
    title: 'GenAI & LLM Engineer',
    icon: '🤖',
    badge: 'Trending #1',
    color: '#06b6d4',
    bg: 'rgba(6, 182, 212, 0.15)',
    border: 'rgba(6, 182, 212, 0.4)',
    summary: 'Master Transformers, Attention mechanisms, Vector RAG pipelines, LoRA fine-tuning, and Agentic workflows.',
    path: [
      'root',
      'genai_root',
      'genai_embed',
      'genai_attention',
      'genai_rag',
      'genai_train',
      'genai_align',
      'genai_prompt_agents',
      'dl_root',
      'dl_neurons',
      'dl_opt',
      'mlops_root'
    ]
  },
  research_scientist: {
    id: 'research_scientist',
    title: 'AI Research Scientist',
    icon: '🔬',
    badge: 'Deep Theory',
    color: '#a855f7',
    bg: 'rgba(168, 85, 247, 0.15)',
    border: 'rgba(168, 85, 247, 0.4)',
    summary: 'Vector spaces, optimization calculus, backpropagation proofs, generative diffusion mathematics, and alignment.',
    path: [
      'root',
      'math_root',
      'math_linalg',
      'math_calc',
      'math_prob',
      'math_info',
      'dl_root',
      'dl_backprop',
      'dl_norm',
      'dl_generative',
      'genai_root',
      'genai_attention',
      'genai_align',
      'eval_root',
      'eval_tradeoff'
    ]
  },
  mlops_engineer: {
    id: 'mlops_engineer',
    title: 'MLOps & Systems Engineer',
    icon: '⚙️',
    badge: 'Production & Infra',
    color: '#10b981',
    bg: 'rgba(16, 185, 129, 0.15)',
    border: 'rgba(16, 185, 129, 0.4)',
    summary: 'Data scrub pipelines, model evaluation curves, drift detection, inference serving, and vector DB infrastructure.',
    path: [
      'root',
      'mlops_root',
      'data_root',
      'data_scrub',
      'data_scale',
      'data_split',
      'eval_root',
      'eval_matrix',
      'eval_curves',
      'genai_train',
      'genai_rag',
      'dl_opt'
    ]
  },
  data_scientist: {
    id: 'data_scientist',
    title: 'Classical ML & Data Scientist',
    icon: '📊',
    badge: 'Statistical Modeling',
    color: '#f59e0b',
    bg: 'rgba(245, 158, 11, 0.15)',
    border: 'rgba(245, 158, 11, 0.4)',
    summary: 'Feature engineering, tabular predictive modeling, tree ensembles (XGBoost/LightGBM), and ROC/PR metric validation.',
    path: [
      'root',
      'data_root',
      'data_scrub',
      'data_impute',
      'data_scale',
      'data_fe',
      'data_split',
      'ml_root',
      'ml_linear',
      'ml_loss',
      'ml_opt',
      'ml_logistic',
      'ml_reg',
      'ml_trees',
      'ml_unsupervised',
      'eval_root',
      'eval_matrix',
      'eval_curves',
      'eval_tradeoff'
    ]
  }
};

export default function MindMapPage() {
  const { theme } = useTheme();
  const [searchParams, setSearchParams] = useSearchParams();
  const [selectedNodeId, setSelectedNodeId] = useState(() => searchParams.get('node') || null);
  const [searchQuery, setSearchQuery] = useState('');
  const [activeDomain, setActiveDomain] = useState('all');
  const [showInterlinks, setShowInterlinks] = useState(true);
  const [selectedTrackId, setSelectedTrackId] = useState(null);
  const [currentTrackStep, setCurrentTrackStep] = useState(0);

  const activeTrack = selectedTrackId ? CAREER_TRACKS[selectedTrackId] : null;
  const trackNodeSet = useMemo(() => {
    return activeTrack ? new Set(activeTrack.path) : null;
  }, [activeTrack]);

  // SVG Pan & Zoom Transform State: Initialized with window center so nodes are never off-screen
  const [transform, setTransform] = useState(() => {
    const w = typeof window !== 'undefined' ? window.innerWidth : 1200;
    const h = typeof window !== 'undefined' ? window.innerHeight : 800;
    return {
      x: Math.round(w / 2),
      y: Math.round(h / 2),
      k: 0.8
    };
  });
  const [isDragging, setIsDragging] = useState(false);
  const dragStartRef = useRef({ x: 0, y: 0 });
  const svgRef = useRef(null);

  const focusNode = useCallback((nodeId) => {
    const node = allNodesData.find((n) => n.id === nodeId);
    if (!node) return;
    setSelectedNodeId(nodeId);
    setSearchParams({ node: nodeId });
    const rect = svgRef.current ? svgRef.current.getBoundingClientRect() : null;
    const w = rect && rect.width > 50 ? rect.width : (typeof window !== 'undefined' ? window.innerWidth : 1200);
    const h = rect && rect.height > 50 ? rect.height : (typeof window !== 'undefined' ? window.innerHeight : 800);
    setTransform({
      x: Math.round(w / 2 - (node.x || 0) * 0.85),
      y: Math.round(h / 2 - (node.y || 0) * 0.85),
      k: 0.85
    });
  }, [setSearchParams]);

  const handleNextTrackStep = () => {
    if (!activeTrack) return;
    const nextIdx = Math.min(currentTrackStep + 1, activeTrack.path.length - 1);
    setCurrentTrackStep(nextIdx);
    focusNode(activeTrack.path[nextIdx]);
  };

  const handlePrevTrackStep = () => {
    if (!activeTrack) return;
    const prevIdx = Math.max(currentTrackStep - 1, 0);
    setCurrentTrackStep(prevIdx);
    focusNode(activeTrack.path[prevIdx]);
  };

  // Export as SVG
  const handleExportSVG = () => {
    if (!svgRef.current) return;
    const serializer = new XMLSerializer();
    const svgString = serializer.serializeToString(svgRef.current);
    const blob = new Blob([svgString], { type: 'image/svg+xml;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `The-Era-of-AI-Knowledge-Graph-${new Date().toISOString().slice(0, 10)}.svg`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  // Export as PNG
  const handleExportPNG = () => {
    if (!svgRef.current) return;
    const serializer = new XMLSerializer();
    const svgString = serializer.serializeToString(svgRef.current);
    const img = new Image();
    const svgBlob = new Blob([svgString], { type: 'image/svg+xml;charset=utf-8' });
    const url = URL.createObjectURL(svgBlob);

    img.onload = () => {
      const canvas = document.createElement('canvas');
      canvas.width = 2400;
      canvas.height = 1400;
      const ctx = canvas.getContext('2d');
      ctx.fillStyle = theme === 'bright' ? '#f8fafc' : theme === 'metallic-green' ? '#041d13' : '#020617';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
      URL.revokeObjectURL(url);

      const pngUrl = canvas.toDataURL('image/png');
      const downloadLink = document.createElement('a');
      downloadLink.href = pngUrl;
      downloadLink.download = `The-Era-of-AI-Knowledge-Graph-${new Date().toISOString().slice(0, 10)}.png`;
      document.body.appendChild(downloadLink);
      downloadLink.click();
      document.body.removeChild(downloadLink);
    };
    img.src = url;
  };

  // Sync selected node with URL parameter
  useEffect(() => {
    const nodeFromParam = searchParams.get('node');
    if (nodeFromParam) {
      setSelectedNodeId(nodeFromParam);
    }
  }, [searchParams]);

  const handleSelectNode = (id) => {
    setSelectedNodeId(id);
    if (id) {
      setSearchParams({ node: id });
    } else {
      setSearchParams({});
    }
  };

  const selectedNode = useMemo(() => {
    return allNodesData.find((n) => n.id === selectedNodeId) || null;
  }, [selectedNodeId]);

  // Color scheme by category
  const categoryConfig = {
    center: { fill: '#4f46e5', stroke: '#818cf8', text: '#ffffff', label: 'Universe' },
    math: { fill: '#1e3a8a', stroke: '#3b82f6', text: '#93c5fd', label: 'Math' },
    data: { fill: '#064e3b', stroke: '#10b981', text: '#6ee7b7', label: 'Data Preprocessing' },
    ml: { fill: '#581c87', stroke: '#a855f7', text: '#d8b4fe', label: 'Classical ML' },
    eval: { fill: '#78350f', stroke: '#f59e0b', text: '#fcd34d', label: 'Evaluation' },
    dl: { fill: '#831843', stroke: '#ec4899', text: '#fbcfe8', label: 'Deep Learning' },
    genai: { fill: '#312e81', stroke: '#6366f1', text: '#c7d2fe', label: 'GenAI & LLMs' },
    mlops: { fill: '#134e4a', stroke: '#14b8a6', text: '#99f6e4', label: 'MLOps' },
    swe_cloud: { fill: '#0f172a', stroke: '#38bdf8', text: '#bae6fd', label: 'SWE & Cloud Infra' }
  };

  const getThemeCanvasColors = () => {
    switch (theme) {
      case 'bright':
        return {
          gridPath: '#cbd5e1',
          gridDot: '#94a3b8',
          lineNormal: '#94a3b8',
          lineSelected: '#4f46e5',
          nodeBg: '#ffffff',
          nodeBgSelected: '#e0e7ff',
          nodeRootBg: '#4f46e5',
          nodeText: '#0f172a',
          nodeRootText: '#ffffff',
        };
      case 'metallic-green':
        return {
          gridPath: '#064e3b',
          gridDot: '#059669',
          lineNormal: '#064e3b',
          lineSelected: '#34d399',
          nodeBg: '#042115',
          nodeBgSelected: '#065f46',
          nodeRootBg: '#047857',
          nodeText: '#ecfdf5',
          nodeRootText: '#ffffff',
        };
      case 'dark':
        return {
          gridPath: '#27272a',
          gridDot: '#3f3f46',
          lineNormal: '#27272a',
          lineSelected: '#ffffff',
          nodeBg: '#09090b',
          nodeBgSelected: '#27272a',
          nodeRootBg: '#18181b',
          nodeText: '#ffffff',
          nodeRootText: '#ffffff',
        };
      default:
        return {
          gridPath: '#334155',
          gridDot: '#475569',
          lineNormal: '#334155',
          lineSelected: '#818cf8',
          nodeBg: '#0f172a',
          nodeBgSelected: '#1e1b4b',
          nodeRootBg: '#312e81',
          nodeText: '#f8fafc',
          nodeRootText: '#ffffff',
        };
    }
  };
  const themeColors = getThemeCanvasColors();

  // Center the view on initial mount and re-center on layout stabilization
  useEffect(() => {
    const centerGraph = () => {
      if (!svgRef.current) return;
      const rect = svgRef.current.getBoundingClientRect();
      const w = rect.width > 50 ? rect.width : (typeof window !== 'undefined' ? window.innerWidth : 1200);
      const h = rect.height > 50 ? rect.height : (typeof window !== 'undefined' ? window.innerHeight : 800);

      const nodeFromParam = searchParams.get('node');
      const targetNode = nodeFromParam ? allNodesData.find((n) => n.id === nodeFromParam) : null;

      if (targetNode) {
        setTransform({
          x: Math.round(w / 2 - (targetNode.x || 0) * 0.85),
          y: Math.round(h / 2 - (targetNode.y || 0) * 0.85),
          k: 0.85
        });
      } else {
        setTransform({
          x: Math.round(w / 2),
          y: Math.round(h / 2),
          k: 0.8
        });
      }
    };

    centerGraph();
    const raf = requestAnimationFrame(centerGraph);
    const t1 = setTimeout(centerGraph, 60);
    const t2 = setTimeout(centerGraph, 200);

    let observer;
    if (typeof ResizeObserver !== 'undefined' && svgRef.current) {
      observer = new ResizeObserver(() => {
        centerGraph();
      });
      observer.observe(svgRef.current);
    }

    return () => {
      cancelAnimationFrame(raf);
      clearTimeout(t1);
      clearTimeout(t2);
      if (observer) observer.disconnect();
    };
  }, [searchParams]);

  // Filtered nodes
  const filteredNodes = useMemo(() => {
    return allNodesData.filter((node) => {
      // Domain filter
      if (activeDomain !== 'all') {
        if (node.id !== 'root' && node.category !== activeDomain) {
          return false;
        }
      }
      // Search query
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase();
        const matchLabel = node.label?.toLowerCase().includes(q);
        const matchDef = node.def?.toLowerCase().includes(q);
        const matchSub = node.subtopics?.some((s) => s.toLowerCase().includes(q));
        if (!matchLabel && !matchDef && !matchSub) return false;
      }
      return true;
    });
  }, [activeDomain, searchQuery]);

  // Hierarchy lines calculation
  const hierarchyLinks = useMemo(() => {
    const links = [];
    const nodeMap = new Map(allNodesData.map((n) => [n.id, n]));

    for (const node of allNodesData) {
      if (node.connections) {
        for (const targetId of node.connections) {
          const target = nodeMap.get(targetId);
          if (target) {
            links.push({
              source: node,
              target: target,
              id: `${node.id}-${target.id}`
            });
          }
        }
      }
    }
    return links;
  }, []);

  // Pan handlers
  const handleMouseDown = (e) => {
    if (e.button !== 0) return; // Only left click
    setIsDragging(true);
    dragStartRef.current = {
      x: e.clientX - transform.x,
      y: e.clientY - transform.y
    };
  };

  const handleMouseMove = (e) => {
    if (!isDragging) return;
    setTransform((prev) => ({
      ...prev,
      x: e.clientX - dragStartRef.current.x,
      y: e.clientY - dragStartRef.current.y
    }));
  };

  const handleMouseUp = () => {
    setIsDragging(false);
  };

  const handleWheel = (e) => {
    e.preventDefault();
    const zoomFactor = e.deltaY < 0 ? 1.12 : 0.88;
    setTransform((prev) => {
      const newScale = Math.min(Math.max(prev.k * zoomFactor, 0.2), 3.0);
      return {
        ...prev,
        k: newScale
      };
    });
  };

  const zoom = (direction) => {
    const factor = direction > 0 ? 1.25 : 0.8;
    setTransform((prev) => ({
      ...prev,
      k: Math.min(Math.max(prev.k * factor, 0.2), 3.0)
    }));
  };

  const resetView = () => {
    if (svgRef.current) {
      const rect = svgRef.current.getBoundingClientRect();
      setTransform({
        x: rect.width / 2,
        y: rect.height / 2,
        k: 0.8
      });
    }
  };

  return (
    <div className="relative flex-1 w-full h-full overflow-hidden flex flex-col bg-slate-950 select-none">
      {/* Semantic H1 for SEO */}
      <h1 className="sr-only">Interactive Machine Learning & AI Knowledge Graph Mind Map — The Era of AI</h1>

      {/* Mindmap Toolbar */}
      <div className="bg-slate-900/90 backdrop-blur-md border-b border-slate-800 px-3 sm:px-4 py-2 flex flex-col md:flex-row md:items-center justify-between gap-2 z-10 shrink-0">
        <div className="flex items-center gap-2 flex-wrap sm:flex-nowrap">
          {/* Search Box */}
          <div className="relative flex-1 sm:flex-none">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search 34+ modules (AdamW, LoRA)..."
              className="bg-slate-950 border border-slate-800 text-xs text-white rounded-lg pl-8 pr-4 py-1.5 focus:outline-none focus:ring-2 focus:ring-indigo-500 w-full sm:w-52 md:w-64 placeholder-slate-500"
            />
            <Search className="w-3.5 h-3.5 absolute left-2.5 top-2.5 text-slate-500" />
            {searchQuery && (
              <button 
                onClick={() => setSearchQuery('')}
                className="absolute right-2 top-2 text-slate-500 hover:text-white text-xs"
              >
                &times;
              </button>
            )}
          </div>

          {/* Domain Filter Pills */}
          <div className="hidden 2xl:flex items-center space-x-1 text-xs">
            {[
              { id: 'all', label: 'All' },
              { id: 'math', label: 'Math' },
              { id: 'data', label: 'Data' },
              { id: 'ml', label: 'Classical ML' },
              { id: 'eval', label: 'Evaluation' },
              { id: 'dl', label: 'Deep Learning' },
              { id: 'genai', label: 'GenAI & LLM' },
              { id: 'mlops', label: 'MLOps' },
              { id: 'swe_cloud', label: 'SWE & Cloud' }
            ].map((dom) => (
              <button
                key={dom.id}
                onClick={() => setActiveDomain(dom.id)}
                className={`px-2.5 py-1 rounded-md text-xs font-medium transition ${
                  activeDomain === dom.id
                    ? 'bg-indigo-600 text-white shadow'
                    : 'bg-slate-950 text-slate-400 hover:text-white border border-slate-800'
                }`}
              >
                {dom.label}
              </button>
            ))}
          </div>

          {/* Career Track Pathways Selector */}
          <div className="flex items-center gap-1.5 bg-slate-950/90 border border-slate-800 rounded-lg p-1 text-xs shrink-0 max-w-full">
            <span className="text-slate-400 font-semibold flex items-center gap-1 pl-1">
              <Route className="w-3.5 h-3.5 text-cyan-400 shrink-0" />
              <span className="hidden sm:inline">Track:</span>
            </span>
            <select
              value={selectedTrackId || 'none'}
              onChange={(e) => {
                const val = e.target.value === 'none' ? null : e.target.value;
                setSelectedTrackId(val);
                setCurrentTrackStep(0);
                if (val && CAREER_TRACKS[val]) {
                  const firstNodeId = CAREER_TRACKS[val].path[1] || CAREER_TRACKS[val].path[0];
                  focusNode(firstNodeId);
                }
              }}
              className="bg-slate-900 border border-slate-700/80 rounded-md text-xs font-semibold text-white px-2 py-1 focus:outline-none focus:border-cyan-500 cursor-pointer max-w-[190px] sm:max-w-none truncate"
            >
              <option value="none">🌐 All Domains</option>
              <option value="genai_engineer">🤖 GenAI & LLM</option>
              <option value="research_scientist">🔬 AI Research</option>
              <option value="mlops_engineer">⚙️ MLOps & Systems</option>
              <option value="data_scientist">📊 Data Scientist</option>
            </select>
          </div>
        </div>

        {/* Zoom & View Controls */}
        <div className="flex items-center justify-between sm:justify-end space-x-1.5 text-xs overflow-x-auto scrollbar-none py-0.5">
          <button
            onClick={() => zoom(1)}
            title="Zoom In"
            className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white border border-slate-700/60 transition"
          >
            <ZoomIn className="w-4 h-4" />
          </button>
          <button
            onClick={() => zoom(-1)}
            title="Zoom Out"
            className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white border border-slate-700/60 transition"
          >
            <ZoomOut className="w-4 h-4" />
          </button>
          <button
            onClick={resetView}
            title="Reset View to Center"
            className="p-1.5 px-2.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white border border-slate-700/60 transition flex items-center gap-1 font-medium"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>Reset</span>
          </button>

          <button
            onClick={() => setShowInterlinks(!showInterlinks)}
            title="Toggle Inter-Domain Cross-Links"
            className={`p-1.5 px-2.5 rounded-lg border transition text-xs font-semibold flex items-center gap-1.5 ${
              showInterlinks
                ? 'bg-indigo-600/20 text-indigo-300 border-indigo-500/40 hover:bg-indigo-600/30'
                : 'bg-slate-800 text-slate-400 border-slate-700 hover:text-white'
            }`}
          >
            <Share2 className="w-3.5 h-3.5" />
            <span>Links: {showInterlinks ? 'ON' : 'OFF'}</span>
          </button>

          {/* Export PNG Dropdown */}
          <button
            onClick={handleExportPNG}
            title="Export High-Resolution Mind Map (PNG)"
            className="p-1.5 px-2.5 rounded-lg bg-slate-800 hover:bg-indigo-600/30 text-slate-300 hover:text-white border border-slate-700/60 hover:border-indigo-500/50 transition flex items-center gap-1.5 font-medium"
          >
            <Download className="w-3.5 h-3.5 text-indigo-400" />
            <span className="hidden sm:inline">Export PNG</span>
          </button>
        </div>
      </div>

      {/* SVG Canvas Area */}
      <div
        className={`relative flex-1 w-full h-full overflow-hidden ${
          isDragging ? 'grabbing-cursor' : 'grab-cursor'
        }`}
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
        onWheel={handleWheel}
      >
        {/* Subtle Background Grid Pattern */}
        <svg className="absolute inset-0 w-full h-full pointer-events-none opacity-20">
          <defs>
            <pattern id="gridPattern" width="40" height="40" patternUnits="userSpaceOnUse">
              <path d="M 40 0 L 0 0 0 40" fill="none" stroke={themeColors.gridPath} strokeWidth="0.8" />
              <circle cx="0" cy="0" r="1.2" fill={themeColors.gridDot} />
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#gridPattern)" />
        </svg>

        {/* Dynamic Zoomable Graph SVG */}
        <svg ref={svgRef} className="w-full h-full overflow-visible">
          <defs>
            {/* Arrowhead marker for cross links */}
            <marker
              id="arrowhead-cross"
              markerWidth="8"
              markerHeight="6"
              refX="7"
              refY="3"
              orient="auto"
            >
              <polygon points="0 0, 8 3, 0 6" fill="#f59e0b" />
            </marker>
          </defs>

          <g transform={`translate(${transform.x}, ${transform.y}) scale(${transform.k})`}>
            {/* 1. Hierarchy Lines (Root -> Hubs -> Topics) */}
            <g id="hierarchyLines">
              {hierarchyLinks.map((link) => {
                const isSelected = selectedNodeId === link.source.id || selectedNodeId === link.target.id;
                const isTrackLink = trackNodeSet && trackNodeSet.has(link.source.id) && trackNodeSet.has(link.target.id);
                const isDimmed = trackNodeSet && !isTrackLink;

                return (
                  <line
                    key={link.id}
                    x1={link.source.x || 0}
                    y1={link.source.y || 0}
                    x2={link.target.x || 0}
                    y2={link.target.y || 0}
                    stroke={isTrackLink ? activeTrack.color : isSelected ? themeColors.lineSelected : themeColors.lineNormal}
                    strokeWidth={isTrackLink ? 3.5 : isSelected ? 2.5 : 1.5}
                    strokeDasharray={isTrackLink ? '6 3' : link.source.level === 0 ? '4 4' : 'none'}
                    strokeOpacity={isDimmed ? 0.12 : 1}
                    className="transition-colors duration-200"
                  />
                );
              })}
            </g>

            {/* 2. Cross-Domain Links */}
            {showInterlinks && (
              <g id="crossLinks">
                {crossLinksData.map((link, idx) => {
                  const nodeMap = new Map(allNodesData.map((n) => [n.id, n]));
                  const fromNode = nodeMap.get(link.from);
                  const toNode = nodeMap.get(link.to);
                  if (!fromNode || !toNode) return null;

                  const isLinkedToSelected = selectedNodeId === link.from || selectedNodeId === link.to;
                  const isTrackCrossLink = trackNodeSet && trackNodeSet.has(link.from) && trackNodeSet.has(link.to);
                  const isDimmed = trackNodeSet && !isTrackCrossLink;

                  // Curved path calculation
                  const dx = (toNode.x || 0) - (fromNode.x || 0);
                  const dy = (toNode.y || 0) - (fromNode.y || 0);
                  const cx = (fromNode.x || 0) + dx * 0.5 - dy * 0.2;
                  const cy = (fromNode.y || 0) + dy * 0.5 + dx * 0.2;

                  return (
                    <g key={idx} className="cursor-pointer group">
                      <path
                        d={`M ${fromNode.x || 0} ${fromNode.y || 0} Q ${cx} ${cy} ${toNode.x || 0} ${toNode.y || 0}`}
                        fill="none"
                        stroke={isTrackCrossLink ? activeTrack.color : isLinkedToSelected ? '#fbbf24' : '#f59e0b'}
                        strokeWidth={isTrackCrossLink ? 3.5 : isLinkedToSelected ? 2.5 : 1.2}
                        strokeDasharray="5,5"
                        strokeOpacity={isDimmed ? 0.08 : isTrackCrossLink ? 1 : isLinkedToSelected ? 0.95 : 0.45}
                        markerEnd="url(#arrowhead-cross)"
                      />
                    </g>
                  );
                })}
              </g>
            )}

            {/* 3. Node Elements */}
            <g id="nodesGroup">
              {filteredNodes.map((node) => {
                const isSelected = selectedNodeId === node.id;
                const cfg = categoryConfig[node.category] || categoryConfig.ml;
                const isRoot = node.level === 0;
                const isHub = node.level === 1;

                // Career track highlights
                const isTrackNode = trackNodeSet ? trackNodeSet.has(node.id) : false;
                const isDimmed = trackNodeSet ? !isTrackNode : false;
                const stepIndex = isTrackNode ? activeTrack.path.indexOf(node.id) + 1 : null;
                const isCurrentTrackStep = isTrackNode && activeTrack.path[currentTrackStep] === node.id;

                // Dynamically calculate node width based on character count so text never spills out of the box
                const labelLen = (node.label || '').length;
                const charWidth = isRoot ? 8.6 : isHub ? 7.6 : 6.8;
                const textWidth = Math.round(labelLen * charWidth);
                const leftOffset = isRoot ? 36 : isHub ? 30 : 28;
                const rightPadding = 18;
                const minWidth = isRoot ? 260 : isHub ? 210 : 180;
                const nodeWidth = Math.max(minWidth, textWidth + leftOffset + rightPadding);
                const nodeHeight = isRoot ? 54 : isHub ? 46 : 40;
                const rx = isRoot ? 16 : 10;

                return (
                  <g
                    key={node.id}
                    transform={`translate(${node.x || 0}, ${node.y || 0})`}
                    opacity={isDimmed ? 0.2 : 1}
                    onClick={(e) => {
                      e.stopPropagation();
                      handleSelectNode(node.id);
                      if (isTrackNode) {
                        const idx = activeTrack.path.indexOf(node.id);
                        if (idx !== -1) setCurrentTrackStep(idx);
                      }
                    }}
                    className="cursor-pointer group transition-opacity duration-300"
                  >
                    {/* Pulsing ring for current career track step */}
                    {isCurrentTrackStep && (
                      <rect
                        x={-nodeWidth / 2 - 6}
                        y={-nodeHeight / 2 - 6}
                        width={nodeWidth + 12}
                        height={nodeHeight + 12}
                        rx={rx + 4}
                        fill="none"
                        stroke={activeTrack.color}
                        strokeWidth="2.5"
                        strokeDasharray="6,4"
                        className="animate-pulse"
                      />
                    )}

                    {/* Node background pill */}
                    <rect
                      x={-nodeWidth / 2}
                      y={-nodeHeight / 2}
                      width={nodeWidth}
                      height={nodeHeight}
                      rx={rx}
                      fill={isSelected ? themeColors.nodeBgSelected : isRoot ? themeColors.nodeRootBg : themeColors.nodeBg}
                      stroke={isTrackNode ? activeTrack.color : isSelected ? themeColors.lineSelected : cfg.stroke}
                      strokeWidth={isCurrentTrackStep ? 3.5 : isTrackNode ? 2.5 : isSelected ? 3 : isHub ? 2 : 1.5}
                      filter="drop-shadow(0 4px 6px rgba(0,0,0,0.3))"
                      className="transition-all duration-200 group-hover:scale-105"
                    />

                    {/* Small category indicator dot */}
                    <circle
                      cx={-nodeWidth / 2 + 14}
                      cy={0}
                      r={isRoot ? 5.5 : 4}
                      fill={isTrackNode ? activeTrack.color : cfg.stroke}
                    />

                    {/* Node text label */}
                    <text
                      x={-nodeWidth / 2 + leftOffset}
                      y={4}
                      fill={isSelected ? '#ffffff' : isRoot ? themeColors.nodeRootText : themeColors.nodeText}
                      fontSize={isRoot ? 14 : isHub ? 12 : 11}
                      fontWeight={isRoot ? '700' : isHub ? '600' : '500'}
                      fontFamily="Inter, system-ui, sans-serif"
                      style={{ pointerEvents: 'none', userSelect: 'none' }}
                    >
                      {node.label}
                    </text>

                    {/* Milestone Sequence Badge on Track Nodes */}
                    {isTrackNode && (
                      <g transform={`translate(${nodeWidth / 2 - 14}, ${-nodeHeight / 2 - 5})`}>
                        <rect
                          x="-14"
                          y="-8"
                          width="28"
                          height="16"
                          rx="8"
                          fill={activeTrack.color}
                          stroke="#ffffff"
                          strokeWidth="1.2"
                          filter="drop-shadow(0 2px 4px rgba(0,0,0,0.4))"
                        />
                        <text
                          x="0"
                          y="3.5"
                          fill="#ffffff"
                          fontSize="9"
                          fontWeight="800"
                          textAnchor="middle"
                          fontFamily="ui-monospace, monospace"
                        >
                          #{stepIndex}
                        </text>
                      </g>
                    )}
                  </g>
                );
              })}
            </g>
          </g>
        </svg>

        {/* Legend Overlay at bottom-left */}
        <div className="absolute bottom-4 left-4 bg-slate-900/95 backdrop-blur-md border border-slate-800 rounded-xl px-4 py-2 text-xs text-slate-300 shadow-xl pointer-events-none hidden md:flex items-center space-x-3.5">
          <div className="flex items-center space-x-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-blue-500 shadow-sm shadow-blue-500/50"></span>
            <span>Math</span>
          </div>
          <div className="flex items-center space-x-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 shadow-sm shadow-emerald-500/50"></span>
            <span>Data</span>
          </div>
          <div className="flex items-center space-x-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-purple-500 shadow-sm shadow-purple-500/50"></span>
            <span>Classical ML</span>
          </div>
          <div className="flex items-center space-x-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-amber-500 shadow-sm shadow-amber-500/50"></span>
            <span>Evaluation</span>
          </div>
          <div className="flex items-center space-x-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-pink-500 shadow-sm shadow-pink-500/50"></span>
            <span>Deep Learning</span>
          </div>
          <div className="flex items-center space-x-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-indigo-500 shadow-sm shadow-indigo-500/50"></span>
            <span>GenAI & LLMs</span>
          </div>
          <div className="flex items-center space-x-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-teal-500 shadow-sm shadow-teal-500/50"></span>
            <span>MLOps</span>
          </div>
          <div className="flex items-center space-x-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-sky-400 shadow-sm shadow-sky-400/50"></span>
            <span>SWE &amp; Cloud</span>
          </div>
          <div className="text-slate-500 border-l border-slate-700 pl-3 hidden lg:block">
            Drag to pan &bull; Scroll to zoom &bull; Click node to inspect details
          </div>
        </div>

        {/* Floating Career Track HUD (When a track is active) */}
        {activeTrack && (
          <div className="absolute bottom-4 sm:bottom-6 left-1/2 -translate-x-1/2 z-20 flex items-center gap-3 bg-slate-900/95 backdrop-blur-md border border-slate-700/80 rounded-2xl px-4 py-2.5 shadow-2xl animate-in slide-in-from-bottom-4 duration-200 max-w-[94vw]">
            <div className="flex items-center gap-2.5 min-w-0">
              <span className="text-xl shrink-0">{activeTrack.icon}</span>
              <div className="min-w-0">
                <div className="flex items-center gap-2">
                  <span className="text-xs font-bold text-white tracking-wide truncate">{activeTrack.title}</span>
                  <span 
                    className="text-[10px] font-mono px-2 py-0.2 rounded-full font-bold shrink-0" 
                    style={{ backgroundColor: activeTrack.bg, color: activeTrack.color, border: `1px solid ${activeTrack.border}` }}
                  >
                    Step {currentTrackStep + 1} / {activeTrack.path.length}
                  </span>
                </div>
                <p className="text-[11px] text-slate-300 truncate max-w-[200px] sm:max-w-xs md:max-w-md">
                  Target: <span className="font-semibold text-white">{allNodesData.find(n => n.id === activeTrack.path[currentTrackStep])?.label || 'Milestone'}</span>
                </p>
              </div>
            </div>

            <div className="flex items-center gap-1.5 ml-2 pl-2 border-l border-slate-800 shrink-0">
              <button
                onClick={handlePrevTrackStep}
                disabled={currentTrackStep === 0}
                className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 disabled:opacity-30 text-slate-200 transition"
                title="Previous Milestone in Track"
              >
                <ChevronLeft className="w-4 h-4" />
              </button>
              <button
                onClick={handleNextTrackStep}
                disabled={currentTrackStep === activeTrack.path.length - 1}
                className="p-1.5 px-2.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 disabled:opacity-30 text-white font-medium text-xs flex items-center gap-1 transition shadow-md shadow-indigo-600/30"
                title="Next Milestone in Track"
              >
                <span>Next</span>
                <ChevronRight className="w-4 h-4" />
              </button>
              <button
                onClick={() => setSelectedTrackId(null)}
                className="p-1.5 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-white transition ml-1"
                title="Exit Career Track View"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Slide-over Inspector Drawer for Node Details */}
      <NodeInspector
        node={selectedNode}
        crossLinks={crossLinksData}
        onClose={() => handleSelectNode(null)}
        onSelectNode={handleSelectNode}
      />
    </div>
  );
}
