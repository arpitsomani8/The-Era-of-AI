import React, { useState, useEffect, useRef, useMemo } from 'react';
import { 
  PlayCircle, 
  RotateCcw, 
  Play, 
  Pause, 
  StepForward, 
  Sparkles, 
  Flame, 
  Sliders, 
  Eye, 
  Calculator, 
  HelpCircle,
  Activity,
  Layers,
  ArrowRight,
  Cpu,
  Binary,
  Database,
  Minimize2
} from 'lucide-react';
import KaTeXRenderer from '../components/KaTeXRenderer';
import NeuralNetworkPlayground from '../components/NeuralNetworkPlayground';
import TokenizerPlayground from '../components/TokenizerPlayground';
import RAGPipelinePlayground from '../components/RAGPipelinePlayground';
import LoRAPlayground from '../components/LoRAPlayground';

// PRESET SENTENCES FOR ATTENTION VISUALIZER
const ATTENTION_PRESETS = [
  {
    id: 'coref',
    label: 'Coreference Resolution',
    text: "The animal didn't cross the street because it was too tired",
    highlightPair: [7, 1] // "it" -> "animal"
  },
  {
    id: 'transformer',
    label: 'Transformer Breakthrough',
    text: "Attention mechanisms allow models to focus on relevant context words",
    highlightPair: [0, 8] // "Attention" -> "context"
  },
  {
    id: 'reasoning',
    label: 'Modern LLM Reasoning',
    text: "Deep learning models compute representations through layered neural networks",
    highlightPair: [5, 0] // "representations" -> "Deep"
  }
];

// LOSS LANDSCAPES FOR GRADIENT DESCENT
const LOSS_LANDSCAPES = {
  paraboloid: {
    name: 'Convex Paraboloid (Ill-conditioned)',
    desc: 'Steep along Y axis, shallow along X axis. Highlights why plain SGD oscillates and zig-zags.',
    f: (x, y) => 0.5 * (x * x + 10 * y * y),
    grad: (x, y) => [x, 10 * y],
    minima: [0, 0],
    range: [-3, 3]
  },
  saddle: {
    name: 'Saddle Point Landscape',
    desc: 'Slopes down in one direction and up in another. SGD stalls at zero gradient while Momentum escapes.',
    f: (x, y) => (x * x - y * y) * 0.5,
    grad: (x, y) => [x, -y],
    minima: [0, 0],
    range: [-3, 3]
  },
  rosenbrock: {
    name: 'Rosenbrock Banana Valley',
    desc: 'Narrow parabolic valley. Finding the valley is easy, but converging to the global minimum (1,1) is notoriously tricky.',
    f: (x, y) => (1 - x) ** 2 + 10 * (y - x * x) ** 2,
    grad: (x, y) => [
      -2 * (1 - x) - 40 * x * (y - x * x),
      20 * (y - x * x)
    ],
    minima: [1, 1],
    range: [-2, 2.5]
  }
};

export default function PlaygroundsPage() {
  const [activeTab, setActiveTab] = useState('attention'); // 'attention' | 'gradient'

  // --- ATTENTION SIMULATOR STATE ---
  const [selectedPreset, setSelectedPreset] = useState(ATTENTION_PRESETS[0]);
  const [customText, setCustomText] = useState(ATTENTION_PRESETS[0].text);
  const [temperature, setTemperature] = useState(1.0);
  const [activeHead, setActiveHead] = useState(0); // 0, 1, 2, 3
  const [hoveredSourceIdx, setHoveredSourceIdx] = useState(null);
  const [hoveredTargetIdx, setHoveredTargetIdx] = useState(null);

  // Tokenize text into words
  const tokens = useMemo(() => {
    return customText
      .trim()
      .split(/\s+/)
      .filter(Boolean)
      .slice(0, 12); // Limit to 12 tokens for pristine visual grid
  }, [customText]);

  // Compute simulated multi-head attention matrix based on token affinities & head type
  const attentionMatrix = useMemo(() => {
    const N = tokens.length;
    if (N === 0) return [];

    // Pre-calculate raw scores
    const rawScores = Array.from({ length: N }, () => Array(N).fill(0));

    for (let i = 0; i < N; i++) {
      for (let j = 0; j < N; j++) {
        let score = 0;
        const w1 = tokens[i].toLowerCase();
        const w2 = tokens[j].toLowerCase();

        if (activeHead === 0) {
          // Coreference & Long-range Head
          if (w1 === 'it' && (w2 === 'animal' || w2 === 'street')) {
            score = 5.2;
          } else if (Math.abs(i - j) > 3) {
            score = 1.8 + Math.sin(i * 3 + j) * 0.8;
          } else {
            score = 0.5;
          }
        } else if (activeHead === 1) {
          // Syntactic & Adjacent Dependency Head
          if (Math.abs(i - j) === 1) {
            score = 4.5;
          } else if (Math.abs(i - j) === 2) {
            score = 2.0;
          } else {
            score = 0.2;
          }
        } else if (activeHead === 2) {
          // Semantic Content Similarity Head
          const common = ['attention', 'models', 'focus', 'context', 'neural', 'representations', 'tired', 'cross'];
          if (common.includes(w1) && common.includes(w2)) {
            score = 4.2;
          } else {
            score = Math.cos(i * 1.5 + j * 2.2) * 1.5 + 1.2;
          }
        } else {
          // Self / Diagonal Focus Head
          if (i === j) {
            score = 5.0;
          } else {
            score = 0.4 / (Math.abs(i - j) + 1);
          }
        }

        rawScores[i][j] = score / Math.max(0.2, temperature);
      }
    }

    // Apply Softmax per row
    return rawScores.map((row) => {
      const maxVal = Math.max(...row);
      const exps = row.map((val) => Math.exp(val - maxVal));
      const sum = exps.reduce((acc, curr) => acc + curr, 0);
      return exps.map((val) => val / sum);
    });
  }, [tokens, activeHead, temperature]);

  // --- GRADIENT DESCENT SIMULATOR STATE ---
  const [selectedLandscapeKey, setSelectedLandscapeKey] = useState('paraboloid');
  const [optimizer, setOptimizer] = useState('adamw'); // 'sgd', 'momentum', 'rmsprop', 'adamw'
  const [learningRate, setLearningRate] = useState(0.08);
  const [momentumBeta, setMomentumBeta] = useState(0.9);
  const [isRunning, setIsRunning] = useState(false);
  const [trajectory, setTrajectory] = useState([{ x: -2.2, y: 1.8 }]);
  const [stepCount, setStepCount] = useState(0);

  const optStateRef = useRef({
    vx: 0,
    vy: 0,
    sx: 0,
    sy: 0,
    t: 0
  });

  const landscape = LOSS_LANDSCAPES[selectedLandscapeKey];
  const currentPos = trajectory[trajectory.length - 1] || { x: -2.0, y: 1.5 };
  const currentLoss = landscape.f(currentPos.x, currentPos.y);

  // Single step of optimization
  const stepOptimizer = () => {
    setTrajectory((prev) => {
      const last = prev[prev.length - 1];
      if (!last) return prev;

      // Check for divergence
      if (Math.abs(last.x) > 10 || Math.abs(last.y) > 10 || isNaN(last.x) || isNaN(last.y)) {
        setIsRunning(false);
        return prev;
      }

      const [gx, gy] = landscape.grad(last.x, last.y);
      let nx = last.x;
      let ny = last.y;
      const st = optStateRef.current;
      st.t += 1;

      if (optimizer === 'sgd') {
        nx -= learningRate * gx;
        ny -= learningRate * gy;
      } else if (optimizer === 'momentum') {
        st.vx = momentumBeta * st.vx + learningRate * gx;
        st.vy = momentumBeta * st.vy + learningRate * gy;
        nx -= st.vx;
        ny -= st.vy;
      } else if (optimizer === 'rmsprop') {
        st.sx = 0.9 * st.sx + 0.1 * gx * gx;
        st.sy = 0.9 * st.sy + 0.1 * gy * gy;
        nx -= (learningRate / (Math.sqrt(st.sx) + 1e-8)) * gx;
        ny -= (learningRate / (Math.sqrt(st.sy) + 1e-8)) * gy;
      } else if (optimizer === 'adamw') {
        const beta1 = 0.9;
        const beta2 = 0.999;
        st.vx = beta1 * st.vx + (1 - beta1) * gx;
        st.vy = beta1 * st.vy + (1 - beta1) * gy;
        st.sx = beta2 * st.sx + (1 - beta2) * (gx * gx);
        st.sy = beta2 * st.sy + (1 - beta2) * (gy * gy);

        const mHatX = st.vx / (1 - Math.pow(beta1, st.t));
        const mHatY = st.vy / (1 - Math.pow(beta1, st.t));
        const vHatX = st.sx / (1 - Math.pow(beta2, st.t));
        const vHatY = st.sy / (1 - Math.pow(beta2, st.t));

        // Decoupled weight decay
        const weightDecay = 0.01;
        nx = nx * (1 - learningRate * weightDecay) - (learningRate / (Math.sqrt(vHatX) + 1e-8)) * mHatX;
        ny = ny * (1 - learningRate * weightDecay) - (learningRate / (Math.sqrt(vHatY) + 1e-8)) * mHatY;
      }

      setStepCount((c) => c + 1);
      return [...prev.slice(-150), { x: nx, y: ny }];
    });
  };

  // Run loop for Gradient Descent
  useEffect(() => {
    if (!isRunning) return;
    const interval = setInterval(() => {
      stepOptimizer();
    }, 60);
    return () => clearInterval(interval);
  }, [isRunning, optimizer, learningRate, momentumBeta, selectedLandscapeKey]);

  const resetOptimization = (startPos = { x: -2.2, y: 1.8 }) => {
    setIsRunning(false);
    setTrajectory([startPos]);
    setStepCount(0);
    optStateRef.current = { vx: 0, vy: 0, sx: 0, sy: 0, t: 0 };
  };

  return (
    <div className="flex-1 w-full h-full overflow-y-auto bg-slate-950 text-slate-100 p-4 sm:p-6 md:p-10">
      <div className="max-w-6xl mx-auto space-y-6 pb-20">
        {/* Page Header */}
        <div className="border-b border-slate-800 pb-5 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-500/10 text-cyan-300 border border-cyan-500/30 text-xs font-semibold uppercase tracking-wider mb-2">
              <PlayCircle className="w-3.5 h-3.5" />
              Interactive AI Sandboxes
            </div>
            <h1 className="text-2xl sm:text-3xl md:text-4xl font-extrabold text-white tracking-tight">
              Interactive Machine Learning Playgrounds
            </h1>
            <p className="text-xs sm:text-sm text-slate-400 mt-1 max-w-3xl">
              Real-time mathematical simulations. Test how attention heads dynamically weight semantic connections and explore optimizer ball physics across non-convex loss valleys.
            </p>
          </div>

          {/* Tab Selector */}
          <div className="flex items-center bg-slate-900 border border-slate-800 rounded-xl p-1 shrink-0 self-start md:self-auto">
            <button
              onClick={() => setActiveTab('attention')}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition flex items-center gap-1.5 ${
                activeTab === 'attention'
                  ? 'bg-cyan-600 text-white shadow-md shadow-cyan-600/30'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              <Eye className="w-3.5 h-3.5" />
              <span>Attention Heatmap</span>
            </button>
            <button
              onClick={() => setActiveTab('gradient')}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition flex items-center gap-1.5 ${
                activeTab === 'gradient'
                  ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              <Activity className="w-3.5 h-3.5" />
              <span>Gradient Descent Physics</span>
            </button>
            <button
              onClick={() => setActiveTab('neural')}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition flex items-center gap-1.5 ${
                activeTab === 'neural'
                  ? 'bg-emerald-600 text-white shadow-md shadow-emerald-600/30'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              <Cpu className="w-3.5 h-3.5" />
              <span>Neural Net & Backprop</span>
            </button>
            <button
              onClick={() => setActiveTab('tokenizer')}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition flex items-center gap-1.5 ${
                activeTab === 'tokenizer'
                  ? 'bg-cyan-600 text-white shadow-md shadow-cyan-600/30'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              <Binary className="w-3.5 h-3.5" />
              <span>BPE & Embeddings</span>
            </button>
            <button
              onClick={() => setActiveTab('rag')}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition flex items-center gap-1.5 ${
                activeTab === 'rag'
                  ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              <Database className="w-3.5 h-3.5" />
              <span>RAG Pipeline</span>
            </button>
            <button
              onClick={() => setActiveTab('lora')}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition flex items-center gap-1.5 ${
                activeTab === 'lora'
                  ? 'bg-pink-600 text-white shadow-md shadow-pink-600/30'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              <Minimize2 className="w-3.5 h-3.5" />
              <span>LoRA Rank Explorer</span>
            </button>
          </div>
        </div>

        {/* ========================================================= */}
        {/* TAB 1: MULTI-HEAD ATTENTION MATRIX SIMULATOR */}
        {/* ========================================================= */}
        {activeTab === 'attention' && (
          <div className="space-y-6 animate-fadeIn">
            {/* Control Panel */}
            <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 space-y-4 shadow-sm">
              <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
                {/* Sentence Presets */}
                <div className="space-y-1.5">
                  <label className="text-xs font-bold text-slate-300 uppercase tracking-wider block">
                    Choose Sentence Scenario:
                  </label>
                  <div className="flex flex-wrap gap-2">
                    {ATTENTION_PRESETS.map((p) => (
                      <button
                        key={p.id}
                        onClick={() => {
                          setSelectedPreset(p);
                          setCustomText(p.text);
                        }}
                        className={`px-3 py-1.5 rounded-lg text-xs font-medium transition ${
                          selectedPreset.id === p.id && customText === p.text
                            ? 'bg-cyan-600 text-white shadow-sm'
                            : 'bg-slate-950 text-slate-400 hover:text-white border border-slate-800'
                        }`}
                      >
                        {p.label}
                      </button>
                    ))}
                  </div>
                </div>

                {/* Head Selector */}
                <div className="space-y-1.5">
                  <label className="text-xs font-bold text-slate-300 uppercase tracking-wider block">
                    Select Attention Head:
                  </label>
                  <div className="flex items-center gap-1.5 bg-slate-950 p-1 rounded-xl border border-slate-800">
                    {[
                      { id: 0, label: 'Head 1: Coreference' },
                      { id: 1, label: 'Head 2: Syntactic' },
                      { id: 2, label: 'Head 3: Semantic' },
                      { id: 3, label: 'Head 4: Self/Local' },
                    ].map((head) => (
                      <button
                        key={head.id}
                        onClick={() => setActiveHead(head.id)}
                        className={`px-2.5 py-1 rounded-lg text-xs font-medium transition ${
                          activeHead === head.id
                            ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 shadow-sm'
                            : 'text-slate-400 hover:text-slate-200'
                        }`}
                      >
                        {head.label}
                      </button>
                    ))}
                  </div>
                </div>
              </div>

              {/* Editable Input and Temperature */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2 border-t border-slate-800/80">
                <div className="md:col-span-2 space-y-1">
                  <label className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">
                    Input Text (Live Tokenizer):
                  </label>
                  <input
                    type="text"
                    value={customText}
                    onChange={(e) => setCustomText(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2 text-xs sm:text-sm text-white focus:outline-none focus:ring-2 focus:ring-cyan-500"
                    placeholder="Type any sentence to inspect attention..."
                  />
                </div>

                <div className="space-y-1">
                  <div className="flex justify-between text-[11px] font-semibold text-slate-400 uppercase tracking-wider items-center">
                    <span className="flex items-center gap-1">Softmax Temp (<KaTeXRenderer math="\tau" inline={true} />):</span>
                    <span className="text-cyan-400 font-mono">{temperature.toFixed(2)}</span>
                  </div>
                  <input
                    type="range"
                    min="0.2"
                    max="2.5"
                    step="0.05"
                    value={temperature}
                    onChange={(e) => setTemperature(parseFloat(e.target.value))}
                    className="w-full accent-cyan-500 cursor-pointer"
                  />
                  <div className="flex justify-between text-[10px] text-slate-500 font-mono">
                    <span>0.2 (Sharp)</span>
                    <span>1.0 (Standard)</span>
                    <span>2.5 (Diffused)</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Interactive Attention Visualization Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
              {/* Token Bipartite Ribbon View */}
              <div className="lg:col-span-5 bg-slate-900/90 border border-slate-800 rounded-2xl p-5 space-y-4">
                <div className="flex items-center justify-between border-b border-slate-800/80 pb-3">
                  <h3 className="text-xs font-bold text-white uppercase tracking-wider flex items-center gap-1.5">
                    <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
                    Bipartite Token Flow
                  </h3>
                  <span className="text-[11px] text-slate-400">Hover a word to view attention weights</span>
                </div>

                <div className="relative flex justify-between items-start pt-2 min-h-[340px]">
                  {/* Source Tokens Column */}
                  <div className="space-y-2 z-10 w-36">
                    <span className="text-[10px] uppercase font-bold text-cyan-400 tracking-wider block mb-1">
                      Query (From):
                    </span>
                    {tokens.map((token, idx) => (
                      <div
                        key={`src-${idx}`}
                        onMouseEnter={() => setHoveredSourceIdx(idx)}
                        onMouseLeave={() => setHoveredSourceIdx(null)}
                        className={`p-1.5 px-2.5 rounded-lg border text-xs font-mono transition cursor-pointer flex items-center justify-between ${
                          hoveredSourceIdx === idx
                            ? 'bg-cyan-500 text-white border-cyan-400 shadow-md shadow-cyan-500/30'
                            : 'bg-slate-950 border-slate-800 text-slate-300 hover:border-cyan-500/50'
                        }`}
                      >
                        <span className="truncate">{token}</span>
                        <span className="text-[10px] text-slate-500">{idx}</span>
                      </div>
                    ))}
                  </div>

                  {/* SVG Bezier Ribbons between Source and Target */}
                  <svg className="absolute inset-0 w-full h-full pointer-events-none overflow-visible">
                    {tokens.map((_, sIdx) => {
                      return tokens.map((_, tIdx) => {
                        const weight = attentionMatrix[sIdx]?.[tIdx] || 0;
                        const isHovered = hoveredSourceIdx === sIdx || hoveredTargetIdx === tIdx;
                        const isSelectedRow = hoveredSourceIdx === sIdx;
                        const opacity = hoveredSourceIdx !== null ? (isSelectedRow ? Math.max(weight, 0.15) : 0.05) : weight * 0.7;

                        // Source Y and Target Y approximations based on standard 34px step
                        const y1 = 40 + sIdx * 34;
                        const y2 = 40 + tIdx * 34;

                        if (opacity < 0.08) return null;

                        return (
                          <path
                            key={`path-${sIdx}-${tIdx}`}
                            d={`M 140 ${y1} C 210 ${y1}, 230 ${y2}, 300 ${y2}`}
                            fill="none"
                            stroke={isHovered ? '#38bdf8' : '#818cf8'}
                            strokeWidth={Math.max(1, weight * 8)}
                            opacity={opacity}
                            className="transition-all duration-150"
                          />
                        );
                      });
                    })}
                  </svg>

                  {/* Target Tokens Column */}
                  <div className="space-y-2 z-10 w-36 ml-auto">
                    <span className="text-[10px] uppercase font-bold text-indigo-400 tracking-wider block mb-1 text-right">
                      Key (To):
                    </span>
                    {tokens.map((token, idx) => (
                      <div
                        key={`tgt-${idx}`}
                        onMouseEnter={() => setHoveredTargetIdx(idx)}
                        onMouseLeave={() => setHoveredTargetIdx(null)}
                        className={`p-1.5 px-2.5 rounded-lg border text-xs font-mono transition cursor-pointer flex items-center justify-between ${
                          hoveredTargetIdx === idx
                            ? 'bg-indigo-600 text-white border-indigo-400 shadow-md shadow-indigo-500/30'
                            : 'bg-slate-950 border-slate-800 text-slate-300 hover:border-indigo-500/50'
                        }`}
                      >
                        <span className="text-[10px] text-slate-500">{idx}</span>
                        <span className="truncate">{token}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* Full Matrix Heatmap View */}
              <div className="lg:col-span-7 bg-slate-900/90 border border-slate-800 rounded-2xl p-5 space-y-4">
                <div className="flex items-center justify-between border-b border-slate-800/80 pb-3">
                  <h3 className="text-xs font-bold text-white uppercase tracking-wider flex items-center gap-1.5 flex-wrap">
                    <Calculator className="w-3.5 h-3.5 text-cyan-400 shrink-0" />
                    <span>Attention Weight Matrix</span>
                    <span className="text-slate-400 font-normal">
                      (<KaTeXRenderer math="A = \text{softmax}(QK^T / \sqrt{d_k})" inline={true} />)
                    </span>
                  </h3>
                  <div className="flex items-center gap-1 text-[10px] font-mono text-slate-400">
                    <span>Head {activeHead + 1}</span>
                    <span>&bull;</span>
                    <span>{tokens.length}x{tokens.length} matrix</span>
                  </div>
                </div>

                {/* Heatmap Grid */}
                <div className="overflow-x-auto pb-2">
                  <table className="w-full border-collapse">
                    <thead>
                      <tr>
                        <th className="p-1 text-[10px] font-mono text-slate-500">Q \ K</th>
                        {tokens.map((t, idx) => (
                          <th
                            key={`th-${idx}`}
                            className={`p-1.5 text-[10px] font-mono font-medium max-w-[50px] truncate text-center transition ${
                              hoveredTargetIdx === idx ? 'text-indigo-300 font-bold bg-indigo-500/10 rounded-t' : 'text-slate-400'
                            }`}
                            title={t}
                          >
                            {t}
                          </th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {tokens.map((rowToken, rIdx) => (
                        <tr key={`tr-${rIdx}`}>
                          <td
                            className={`p-1.5 text-[10px] font-mono font-medium max-w-[60px] truncate text-right pr-2 transition ${
                              hoveredSourceIdx === rIdx ? 'text-cyan-300 font-bold bg-cyan-500/10 rounded-l' : 'text-slate-400'
                            }`}
                            title={rowToken}
                          >
                            {rowToken}
                          </td>
                          {tokens.map((_, cIdx) => {
                            const val = attentionMatrix[rIdx]?.[cIdx] || 0;
                            const isCellHovered = hoveredSourceIdx === rIdx && hoveredTargetIdx === cIdx;
                            // Color intensity from 0 to 1
                            const bgAlpha = Math.min(1, Math.max(0.08, val * 1.2));

                            return (
                              <td
                                key={`cell-${rIdx}-${cIdx}`}
                                onMouseEnter={() => {
                                  setHoveredSourceIdx(rIdx);
                                  setHoveredTargetIdx(cIdx);
                                }}
                                onMouseLeave={() => {
                                  setHoveredSourceIdx(null);
                                  setHoveredTargetIdx(null);
                                }}
                                style={{
                                  backgroundColor: `rgba(6, 182, 212, ${bgAlpha})`
                                }}
                                className={`p-2 text-center text-[10px] font-mono cursor-pointer transition border border-slate-900/60 ${
                                  isCellHovered
                                    ? 'ring-2 ring-white z-10 font-bold text-white scale-110 shadow-lg'
                                    : val > 0.4
                                    ? 'text-white font-semibold'
                                    : 'text-slate-200'
                                }`}
                                title={`Attention("${rowToken}" -> "${tokens[cIdx]}") = ${(val * 100).toFixed(1)}%`}
                              >
                                {val.toFixed(2)}
                              </td>
                            );
                          })}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>

                {/* Mathematical Insight Note */}
                <div className="p-3 bg-slate-950/80 rounded-xl border border-slate-800 text-xs text-slate-300 flex items-start gap-2.5">
                  <HelpCircle className="w-4 h-4 text-cyan-400 shrink-0 mt-0.5" />
                  <div className="space-y-1">
                    <p className="leading-relaxed">
                      <strong>How Multi-Head Attention Works:</strong> Each attention head maps tokens into separate Query ($Q$), Key ($K$), and Value ($V$) subspaces of dimension $d_k$. Head 1 specializes in grammatical coreference, while others specialize in syntactic parsing or direct semantic similarity.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* TAB 2: GRADIENT DESCENT & OPTIMIZER PHYSICS SIMULATOR */}
        {/* ========================================================= */}
        {activeTab === 'gradient' && (
          <div className="space-y-6 animate-fadeIn">
            {/* Control Panel */}
            <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 space-y-4 shadow-sm">
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                {/* Landscape Selector */}
                <div className="space-y-1.5 md:col-span-2">
                  <label className="text-xs font-bold text-slate-300 uppercase tracking-wider block">
                    Optimization Loss Landscape:
                  </label>
                  <div className="flex flex-wrap gap-2">
                    {Object.entries(LOSS_LANDSCAPES).map(([key, l]) => (
                      <button
                        key={key}
                        onClick={() => {
                          setSelectedLandscapeKey(key);
                          resetOptimization();
                        }}
                        className={`px-3 py-1.5 rounded-lg text-xs font-medium transition ${
                          selectedLandscapeKey === key
                            ? 'bg-indigo-600 text-white shadow-sm'
                            : 'bg-slate-950 text-slate-400 hover:text-white border border-slate-800'
                        }`}
                      >
                        {l.name.split(' (')[0]}
                      </button>
                    ))}
                  </div>
                </div>

                {/* Optimizer Algorithm */}
                <div className="space-y-1.5 md:col-span-2">
                  <label className="text-xs font-bold text-slate-300 uppercase tracking-wider block">
                    Optimizer Algorithm:
                  </label>
                  <div className="flex items-center gap-1.5 bg-slate-950 p-1 rounded-xl border border-slate-800">
                    {[
                      { id: 'sgd', label: 'Vanilla SGD' },
                      { id: 'momentum', label: 'Momentum' },
                      { id: 'rmsprop', label: 'RMSprop' },
                      { id: 'adamw', label: 'AdamW' },
                    ].map((opt) => (
                      <button
                        key={opt.id}
                        onClick={() => {
                          setOptimizer(opt.id);
                          resetOptimization();
                        }}
                        className={`flex-1 py-1 rounded-lg text-xs font-medium transition ${
                          optimizer === opt.id
                            ? 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/40 shadow-sm'
                            : 'text-slate-400 hover:text-slate-200'
                        }`}
                      >
                        {opt.label}
                      </button>
                    ))}
                  </div>
                </div>
              </div>

              {/* Sliders and Play/Pause Bar */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-3 border-t border-slate-800/80 items-center">
                {/* Learning Rate Slider */}
                <div className="space-y-1">
                  <div className="flex justify-between text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
                    <span>Learning Rate ($\alpha$):</span>
                    <span className="text-indigo-400 font-mono">{learningRate.toFixed(3)}</span>
                  </div>
                  <input
                    type="range"
                    min="0.005"
                    max="0.35"
                    step="0.005"
                    value={learningRate}
                    onChange={(e) => setLearningRate(parseFloat(e.target.value))}
                    className="w-full accent-indigo-500 cursor-pointer"
                  />
                  <div className="flex justify-between text-[10px] text-slate-500 font-mono">
                    <span>0.005 (Slow)</span>
                    <span>0.1 (Optimal)</span>
                    <span>0.35 (Divergent)</span>
                  </div>
                </div>

                {/* Momentum Beta Slider */}
                <div className="space-y-1">
                  <div className="flex justify-between text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
                    <span>Momentum ($\beta$):</span>
                    <span className="text-indigo-400 font-mono">{momentumBeta.toFixed(2)}</span>
                  </div>
                  <input
                    type="range"
                    min="0.5"
                    max="0.98"
                    step="0.02"
                    value={momentumBeta}
                    onChange={(e) => setMomentumBeta(parseFloat(e.target.value))}
                    className="w-full accent-indigo-500 cursor-pointer"
                    disabled={optimizer === 'sgd'}
                  />
                  <div className="flex justify-between text-[10px] text-slate-500 font-mono">
                    <span>0.50</span>
                    <span>0.90 (Standard)</span>
                    <span>0.98</span>
                  </div>
                </div>

                {/* Play, Step, Reset Buttons */}
                <div className="flex items-center gap-2 justify-end pt-2 md:pt-0">
                  <button
                    onClick={() => setIsRunning(!isRunning)}
                    className={`px-4 py-2 rounded-xl font-bold text-xs flex items-center gap-2 transition shadow-sm ${
                      isRunning
                        ? 'bg-amber-600 hover:bg-amber-500 text-white'
                        : 'bg-indigo-600 hover:bg-indigo-500 text-white shadow-indigo-600/30'
                    }`}
                  >
                    {isRunning ? (
                      <>
                        <Pause className="w-4 h-4" />
                        <span>Pause</span>
                      </>
                    ) : (
                      <>
                        <Play className="w-4 h-4" />
                        <span>Run Optimization</span>
                      </>
                    )}
                  </button>

                  <button
                    onClick={stepOptimizer}
                    disabled={isRunning}
                    className="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white border border-slate-700 disabled:opacity-40 transition"
                    title="Take single gradient step"
                  >
                    <StepForward className="w-4 h-4" />
                  </button>

                  <button
                    onClick={() => resetOptimization()}
                    className="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white border border-slate-700 transition"
                    title="Reset simulation"
                  >
                    <RotateCcw className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>

            {/* 2D Contour Canvas & Metrics Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
              {/* Canvas Contour Map */}
              <div className="lg:col-span-8 bg-slate-900/90 border border-slate-800 rounded-2xl p-5 space-y-3 relative overflow-hidden">
                <div className="flex items-center justify-between border-b border-slate-800/80 pb-3">
                  <div>
                    <h3 className="text-xs font-bold text-white uppercase tracking-wider">
                      2D Loss Contour Map & Trajectory Tracing
                    </h3>
                    <p className="text-[11px] text-slate-400 mt-0.5">
                      Click anywhere on the landscape to reposition the starting particle!
                    </p>
                  </div>
                  <span className="text-[11px] font-mono px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                    Step {stepCount}
                  </span>
                </div>

                {/* SVG Contour Simulation Canvas */}
                <div 
                  className="relative w-full aspect-[16/10] bg-slate-950 rounded-xl border border-slate-800 overflow-hidden cursor-crosshair"
                  onClick={(e) => {
                    const rect = e.currentTarget.getBoundingClientRect();
                    const px = (e.clientX - rect.left) / rect.width;
                    const py = (e.clientY - rect.top) / rect.height;
                    const range = landscape.range;
                    const spanX = range[1] - range[0];
                    const spanY = range[1] - range[0];
                    const newX = range[0] + px * spanX;
                    const newY = range[1] - py * spanY; // Invert Y
                    resetOptimization({ x: newX, y: newY });
                  }}
                >
                  <svg className="w-full h-full" viewBox="0 0 600 375">
                    {/* Concentric Iso-Loss Contour Ellipses */}
                    {[1, 2, 4, 8, 16, 28, 45, 70].map((level, idx) => {
                      const rx = idx * 36 + 25;
                      const ry = selectedLandscapeKey === 'paraboloid' ? rx * 0.35 : rx * 0.7;
                      return (
                        <ellipse
                          key={`contour-${idx}`}
                          cx="300"
                          cy="187"
                          rx={rx}
                          ry={ry}
                          fill="none"
                          stroke={idx % 2 === 0 ? '#4f46e5' : '#1e1b4b'}
                          strokeWidth="1"
                          strokeDasharray="4,4"
                          opacity={0.35 + idx * 0.05}
                        />
                      );
                    })}

                    {/* Global Minima Star / Target */}
                    <g transform="translate(300, 187)">
                      <circle cx="0" cy="0" r="6" fill="#10b981" />
                      <circle cx="0" cy="0" r="14" fill="none" stroke="#10b981" strokeWidth="1" strokeDasharray="3,3" />
                      <text x="10" y="4" fill="#6ee7b7" fontSize="10" fontFamily="monospace">
                        Minima
                      </text>
                    </g>

                    {/* Tracing Trajectory Polyline */}
                    {trajectory.length > 1 && (
                      <polyline
                        points={trajectory
                          .map((pt) => {
                            const range = landscape.range;
                            const spanX = range[1] - range[0];
                            const spanY = range[1] - range[0];
                            const cx = ((pt.x - range[0]) / spanX) * 600;
                            const cy = ((range[1] - pt.y) / spanY) * 375;
                            return `${cx},${cy}`;
                          })
                          .join(' ')}
                        fill="none"
                        stroke="#38bdf8"
                        strokeWidth="2.5"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        filter="drop-shadow(0 0 6px #0284c7)"
                      />
                    )}

                    {/* Historical Dots */}
                    {trajectory.slice(-30).map((pt, idx) => {
                      const range = landscape.range;
                      const spanX = range[1] - range[0];
                      const spanY = range[1] - range[0];
                      const cx = ((pt.x - range[0]) / spanX) * 600;
                      const cy = ((range[1] - pt.y) / spanY) * 375;
                      return (
                        <circle
                          key={`pt-${idx}`}
                          cx={cx}
                          cy={cy}
                          r={2}
                          fill="#818cf8"
                          opacity={idx / 30}
                        />
                      );
                    })}

                    {/* Current Position Particle */}
                    {(() => {
                      const range = landscape.range;
                      const spanX = range[1] - range[0];
                      const spanY = range[1] - range[0];
                      const cx = ((currentPos.x - range[0]) / spanX) * 600;
                      const cy = ((range[1] - currentPos.y) / spanY) * 375;

                      return (
                        <g transform={`translate(${cx}, ${cy})`}>
                          <circle cx="0" cy="0" r="8" fill="#f43f5e" className="animate-ping opacity-60" />
                          <circle cx="0" cy="0" r="7" fill="#f43f5e" stroke="#ffffff" strokeWidth="2" />
                          <circle cx="0" cy="0" r="2.5" fill="#ffffff" />
                        </g>
                      );
                    })()}
                  </svg>
                </div>
              </div>

              {/* Real-time Optimizer Metrics & Math Formulation */}
              <div className="lg:col-span-4 space-y-4">
                {/* Live Metrics Card */}
                <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 space-y-3.5 shadow-sm">
                  <h3 className="text-xs font-bold text-white uppercase tracking-wider border-b border-slate-800/80 pb-2 flex items-center justify-between">
                    <span>Telemetry Metrics</span>
                    <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
                  </h3>

                  <div className="grid grid-cols-2 gap-3 text-xs">
                    <div className="p-3 rounded-xl bg-slate-950 border border-slate-800">
                      <span className="text-[10px] text-slate-500 uppercase block font-mono">Current Loss (L):</span>
                      <span className="text-base font-bold text-emerald-400 font-mono">
                        {isNaN(currentLoss) ? 'DIVERGED' : currentLoss.toFixed(4)}
                      </span>
                    </div>

                    <div className="p-3 rounded-xl bg-slate-950 border border-slate-800">
                      <span className="text-[10px] text-slate-500 uppercase block font-mono">Coordinates (X, Y):</span>
                      <span className="text-xs font-bold text-indigo-300 font-mono">
                        ({currentPos.x.toFixed(2)}, {currentPos.y.toFixed(2)})
                      </span>
                    </div>

                    <div className="p-3 rounded-xl bg-slate-950 border border-slate-800">
                      <span className="text-[10px] text-slate-500 uppercase block font-mono">Iterations Taken:</span>
                      <span className="text-base font-bold text-slate-200 font-mono">{stepCount}</span>
                    </div>

                    <div className="p-3 rounded-xl bg-slate-950 border border-slate-800">
                      <span className="text-[10px] text-slate-500 uppercase block font-mono">Optimizer Mode:</span>
                      <span className="text-xs font-bold text-cyan-300 uppercase font-mono">{optimizer}</span>
                    </div>
                  </div>

                  {currentLoss < 0.05 && (
                    <div className="p-2.5 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs flex items-center gap-2">
                      <Sparkles className="w-4 h-4 text-emerald-400 shrink-0" />
                      <span><strong>Converged!</strong> Minimum point reached successfully.</span>
                    </div>
                  )}

                  {Math.abs(currentPos.x) > 6 && (
                    <div className="p-2.5 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs flex items-center gap-2">
                      <Flame className="w-4 h-4 text-rose-400 shrink-0" />
                      <span className="inline-flex items-center gap-1"><strong>Exploding Gradient!</strong> Lower learning rate (<KaTeXRenderer math="\alpha" inline={true} />) to avoid divergence.</span>
                    </div>
                  )}
                </div>

                {/* Mathematical Optimizer Formula Card */}
                <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 space-y-2.5 shadow-sm text-xs">
                  <h4 className="font-bold text-indigo-300 uppercase tracking-wider flex items-center gap-1.5">
                    <Calculator className="w-3.5 h-3.5 text-indigo-400" />
                    Optimizer Formulation
                  </h4>
                  <div className="p-3 bg-slate-950 rounded-xl border border-slate-800 overflow-x-auto text-center">
                    {optimizer === 'sgd' && (
                      <KaTeXRenderer math="\theta_{t+1} = \theta_t - \alpha \nabla L(\theta_t)" block={true} />
                    )}
                    {optimizer === 'momentum' && (
                      <KaTeXRenderer math="v_{t+1} = \beta v_t + \alpha \nabla L(\theta_t), \quad \theta_{t+1} = \theta_t - v_{t+1}" block={true} />
                    )}
                    {optimizer === 'rmsprop' && (
                      <KaTeXRenderer math="s_t = \gamma s_{t-1} + (1-\gamma)g_t^2, \quad \theta_{t+1} = \theta_t - \frac{\alpha}{\sqrt{s_t + \epsilon}} g_t" block={true} />
                    )}
                    {optimizer === 'adamw' && (
                      <KaTeXRenderer math="\theta_{t+1} = \theta_t(1 - \alpha \lambda) - \frac{\alpha}{\sqrt{\hat{v}_t} + \epsilon} \hat{m}_t" block={true} />
                    )}
                  </div>
                  <p className="text-[11px] text-slate-400 leading-relaxed">
                    {optimizer === 'adamw'
                      ? 'AdamW couples adaptive first/second moments with decoupled weight decay for state-of-the-art LLM training stability.'
                      : optimizer === 'momentum'
                      ? 'Momentum accelerates gradient vectors in the right direction, dampening oscillations across ravines.'
                      : 'Vanilla SGD takes direct steps along the steepest slope, susceptible to zig-zagging in ill-conditioned valleys.'}
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* TAB 3: NEURAL NETWORK & BACKPROP PLAYGROUND */}
        {/* ========================================================= */}
        {activeTab === 'neural' && (
          <NeuralNetworkPlayground />
        )}

        {/* ========================================================= */}
        {/* TAB 4: BPE TOKENIZER & EMBEDDING SPACE PLAYGROUND */}
        {/* ========================================================= */}
        {activeTab === 'tokenizer' && (
          <TokenizerPlayground />
        )}

        {/* ========================================================= */}
        {/* TAB 5: RAG ARCHITECTURE PIPELINE PLAYGROUND */}
        {/* ========================================================= */}
        {activeTab === 'rag' && (
          <RAGPipelinePlayground />
        )}

        {/* ========================================================= */}
        {/* TAB 6: LORA RANK DECOMPOSITION PLAYGROUND */}
        {/* ========================================================= */}
        {activeTab === 'lora' && (
          <LoRAPlayground />
        )}
      </div>
    </div>
  );
}
