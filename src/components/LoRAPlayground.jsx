import React, { useState, useMemo } from 'react';
import { 
  Sliders, 
  Layers, 
  Cpu, 
  Sparkles, 
  HardDrive, 
  Zap, 
  ArrowRight, 
  CheckCircle2, 
  Calculator, 
  RotateCcw,
  BarChart3,
  Shield,
  Minimize2,
  Server
} from 'lucide-react';
import KaTeXRenderer from './KaTeXRenderer';

// PRESET FOUNDATION MODEL ARCHITECTURES
const MODEL_CONFIGS = [
  {
    id: 'llama3_8b',
    name: 'LLaMA-3 / Mistral (8B)',
    d: 4096,
    k: 4096,
    layers: 32,
    totalParams: '8.0 Billion',
    baseWeightsGB: 16.0 // FP16 (2 bytes per param)
  },
  {
    id: 'llama2_13b',
    name: 'LLaMA-2 (13B)',
    d: 5120,
    k: 5120,
    layers: 40,
    totalParams: '13.0 Billion',
    baseWeightsGB: 26.0
  },
  {
    id: 'llama3_70b',
    name: 'LLaMA-3 (70B)',
    d: 8192,
    k: 8192,
    layers: 80,
    totalParams: '70.0 Billion',
    baseWeightsGB: 140.0
  }
];

export default function LoRAPlayground() {
  const [selectedModelId, setSelectedModelId] = useState('llama3_8b');
  const [rank, setRank] = useState(8); // r in [1, 2, 4, 8, 16, 32, 64]
  const [alpha, setAlpha] = useState(16); // LoRA alpha
  const [targetModules, setTargetModules] = useState('qv'); // 'qv' (Q, V only) | 'all' (All 7 linear matrices)
  const [isMerged, setIsMerged] = useState(false);

  const activeModel = useMemo(() => {
    return MODEL_CONFIGS.find(m => m.id === selectedModelId) || MODEL_CONFIGS[0];
  }, [selectedModelId]);

  // Compute LoRA vs Full Fine-Tuning Parameters & VRAM
  const stats = useMemo(() => {
    const { d, k, layers } = activeModel;
    const numTargetMatrices = targetModules === 'qv' ? 2 : 7; // Q, V vs Q, K, V, O, Gate, Up, Down

    // Full Fine-Tuning: Every target matrix is fully updated
    const fullParamsPerLayer = numTargetMatrices * (d * k);
    const fullTrainableParams = fullParamsPerLayer * layers;

    // LoRA: Update is decomposed into B (d x r) + A (r x k)
    const loraParamsPerMatrix = d * rank + rank * k;
    const loraParamsPerLayer = numTargetMatrices * loraParamsPerMatrix;
    const loraTrainableParams = loraParamsPerLayer * layers;

    // Parameter Reduction Percentage
    const paramSavingsPct = ((1 - loraTrainableParams / fullTrainableParams) * 100).toFixed(2);
    const reductionFactor = Math.round(fullTrainableParams / loraTrainableParams);

    // VRAM Calculations (FP16 / BF16 mixed precision training):
    // 1. Model Weights: 2 bytes per param
    // 2. Gradients: 2 bytes per trainable param
    // 3. AdamW Optimizer states: 8 bytes per trainable param (first moment 4B + second moment 4B)
    // 4. Activations & Overhead: ~6GB estimated for standard batch size 2, seq len 2048

    // Full Fine-Tuning VRAM
    const fullWeightsVRAM = activeModel.baseWeightsGB;
    const fullGradsVRAM = (fullTrainableParams * 2) / (1024 ** 3);
    const fullOptVRAM = (fullTrainableParams * 8) / (1024 ** 3);
    const fullTotalVRAM = (fullWeightsVRAM + fullGradsVRAM + fullOptVRAM + 8).toFixed(1);

    // LoRA VRAM (Base weights frozen, gradients + AdamW only for LoRA params)
    const loraWeightsVRAM = activeModel.baseWeightsGB;
    const loraGradsVRAM = (loraTrainableParams * 2) / (1024 ** 3);
    const loraOptVRAM = (loraTrainableParams * 8) / (1024 ** 3);
    const loraTotalVRAM = (loraWeightsVRAM + loraGradsVRAM + loraOptVRAM + 4).toFixed(1);

    return {
      fullTrainableParams: (fullTrainableParams / 1e6).toFixed(1) + 'M',
      loraTrainableParams: (loraTrainableParams / 1e6).toFixed(2) + 'M',
      paramSavingsPct,
      reductionFactor,
      fullTotalVRAM,
      loraTotalVRAM,
      fullOptVRAM: fullOptVRAM.toFixed(1),
      loraOptVRAM: (loraOptVRAM * 1024).toFixed(1) + ' MB',
      scalingFactor: (alpha / rank).toFixed(2)
    };
  }, [activeModel, rank, alpha, targetModules]);

  return (
    <div className="space-y-6 animate-fadeIn">
      {/* Top Header Card */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 shadow-sm space-y-4">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="p-1.5 rounded-lg bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                <Minimize2 className="w-4 h-4" />
              </span>
              <h2 className="text-base font-bold text-white tracking-wide">
                LoRA vs Full Fine-Tuning Rank Explorer
              </h2>
              <span className="text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 font-mono">
                {stats.paramSavingsPct}% Parameter Reduction
              </span>
            </div>
            <p className="text-xs text-slate-400 mt-1 max-w-2xl">
              Decompose dense weight updates <KaTeXRenderer math="W = W_0 + \frac{\alpha}{r} (B \times A)" inline={true} /> into low-rank matrices. Inspect real-time parameter reduction, GPU VRAM savings, and zero-latency inference weight merging.
            </p>
          </div>

          {/* Quick Reduction Callout */}
          <div className="flex items-center gap-3 bg-slate-950 p-2.5 px-4 rounded-xl border border-slate-800 text-xs shrink-0">
            <div>
              <span className="text-[10px] text-slate-500 block uppercase font-mono">Rank r</span>
              <span className="font-mono font-bold text-cyan-400">{rank}</span>
            </div>
            <div className="w-[1px] h-6 bg-slate-800" />
            <div>
              <span className="text-[10px] text-slate-500 block uppercase font-mono">Reduction</span>
              <span className="font-mono font-bold text-emerald-400">{stats.reductionFactor}x</span>
            </div>
            <div className="w-[1px] h-6 bg-slate-800" />
            <div>
              <span className="text-[10px] text-slate-500 block uppercase font-mono">LoRA VRAM</span>
              <span className="font-mono font-bold text-indigo-300">{stats.loraTotalVRAM} GB</span>
            </div>
          </div>
        </div>

        {/* Global Controls: Model Preset & Target Modules */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-3 border-t border-slate-800/80">
          {/* Model Selector */}
          <div className="space-y-1.5">
            <label className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">
              1. Foundation Architecture:
            </label>
            <div className="grid grid-cols-3 gap-2">
              {MODEL_CONFIGS.map(m => (
                <button
                  key={m.id}
                  onClick={() => setSelectedModelId(m.id)}
                  className={`p-2.5 rounded-xl border text-left transition ${
                    selectedModelId === m.id
                      ? 'bg-indigo-500/20 text-indigo-300 border-indigo-500/40 shadow-sm'
                      : 'bg-slate-950 text-slate-400 hover:text-white border border-slate-800'
                  }`}
                >
                  <div className="text-xs font-semibold truncate">{m.name}</div>
                  <div className="text-[10px] text-slate-500 truncate mt-0.5">{m.d}x{m.k} &bull; {m.layers}L</div>
                </button>
              ))}
            </div>
          </div>

          {/* Target Modules Selector */}
          <div className="space-y-1.5">
            <label className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">
              2. Target Linear Layers:
            </label>
            <div className="grid grid-cols-2 gap-2">
              <button
                onClick={() => setTargetModules('qv')}
                className={`p-2.5 rounded-xl border text-left transition ${
                  targetModules === 'qv'
                    ? 'bg-indigo-500/20 text-indigo-300 border-indigo-500/40 shadow-sm'
                    : 'bg-slate-950 text-slate-400 hover:text-white border border-slate-800'
                }`}
              >
                <div className="text-xs font-semibold">Q, V Attention Projections</div>
                <div className="text-[10px] text-slate-500 mt-0.5">Original LoRA paper standard</div>
              </button>
              <button
                onClick={() => setTargetModules('all')}
                className={`p-2.5 rounded-xl border text-left transition ${
                  targetModules === 'all'
                    ? 'bg-indigo-500/20 text-indigo-300 border-indigo-500/40 shadow-sm'
                    : 'bg-slate-950 text-slate-400 hover:text-white border border-slate-800'
                }`}
              >
                <div className="text-xs font-semibold">All Linear Modules (Q, K, V, O, MLP)</div>
                <div className="text-[10px] text-slate-500 mt-0.5">Highest benchmark quality</div>
              </button>
            </div>
          </div>
        </div>

        {/* Hyperparameter Sliders: Rank r and Alpha */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 pt-3 border-t border-slate-800/80">
          <div className="space-y-1.5">
            <div className="flex justify-between text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
              <span>Intrinsic Rank (<KaTeXRenderer math="r" inline={true} />):</span>
              <span className="text-cyan-400 font-mono font-bold text-xs">{rank}</span>
            </div>
            <div className="flex items-center gap-1.5">
              {[1, 2, 4, 8, 16, 32, 64].map((rVal) => (
                <button
                  key={`r-${rVal}`}
                  onClick={() => setRank(rVal)}
                  className={`flex-1 py-1.5 rounded-lg text-xs font-mono font-semibold transition ${
                    rank === rVal
                      ? 'bg-cyan-500 text-slate-950 shadow-md shadow-cyan-500/30'
                      : 'bg-slate-950 text-slate-400 hover:text-white border border-slate-800'
                  }`}
                >
                  {rVal}
                </button>
              ))}
            </div>
          </div>

          <div className="space-y-1.5">
            <div className="flex justify-between text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
              <span>Scaling Alpha (<KaTeXRenderer math="\alpha" inline={true} />) & Multiplier (<KaTeXRenderer math="\frac{\alpha}{r}" inline={true} />):</span>
              <span className="text-emerald-400 font-mono font-bold text-xs">
                α = {alpha} ({stats.scalingFactor}x scale)
              </span>
            </div>
            <div className="flex items-center gap-1.5">
              {[8, 16, 32, 64].map((aVal) => (
                <button
                  key={`a-${aVal}`}
                  onClick={() => setAlpha(aVal)}
                  className={`flex-1 py-1.5 rounded-lg text-xs font-mono font-semibold transition ${
                    alpha === aVal
                      ? 'bg-emerald-500 text-slate-950 shadow-md shadow-emerald-500/30'
                      : 'bg-slate-950 text-slate-400 hover:text-white border border-slate-800'
                  }`}
                >
                  {aVal}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Main Grid: Visual Matrix Decomposition + VRAM Comparison */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Left Side: Physical Matrix Architecture Visualizer */}
        <div className="lg:col-span-7 bg-slate-900/90 border border-slate-800 rounded-2xl p-5 space-y-4 shadow-sm">
          <div className="flex items-center justify-between border-b border-slate-800/80 pb-3">
            <h3 className="text-xs font-bold text-white uppercase tracking-wider flex items-center gap-1.5">
              <Layers className="w-3.5 h-3.5 text-cyan-400" />
              Weight Matrix Decomposition: <KaTeXRenderer math="W = W_0 + \frac{\alpha}{r} (B \times A)" inline={true} />
            </h3>
            <button
              onClick={() => setIsMerged(!isMerged)}
              className={`px-3 py-1 rounded-lg text-xs font-semibold transition flex items-center gap-1.5 ${
                isMerged 
                  ? 'bg-emerald-600 text-white shadow-sm'
                  : 'bg-slate-800 hover:bg-slate-700 text-slate-300'
              }`}
            >
              <Zap className="w-3.5 h-3.5 text-amber-400" />
              <span>{isMerged ? 'Merged (0 Latency)' : 'Merge for Inference'}</span>
            </button>
          </div>

          {/* Interactive SVG Matrix Decomposition Diagram */}
          <div className="p-4 bg-slate-950 rounded-2xl border border-slate-800 flex items-center justify-center overflow-x-auto min-h-[220px]">
            {!isMerged ? (
              <svg className="w-full max-w-[500px] h-48" viewBox="0 0 520 180">
                {/* W0 Box (Frozen Pretrained Weights) */}
                <rect 
                  x="20" 
                  y="20" 
                  width="130" 
                  height="130" 
                  rx="10" 
                  fill="#1e293b" 
                  stroke="#475569" 
                  strokeWidth="2" 
                />
                <text x="85" y="75" textAnchor="middle" fill="#ffffff" fontWeight="bold" fontSize="13">W₀</text>
                <text x="85" y="95" textAnchor="middle" fill="#94a3b8" fontSize="10" fontFamily="monospace">
                  {activeModel.d} × {activeModel.k}
                </text>
                <text x="85" y="115" textAnchor="middle" fill="#38bdf8" fontSize="9" fontWeight="bold">
                  [FROZEN]
                </text>

                {/* Plus Sign */}
                <text x="180" y="90" textAnchor="middle" fill="#ffffff" fontSize="22" fontWeight="bold">+</text>

                {/* Matrix B (d x r) - Tall & Thin */}
                <g>
                  {/* Dynamic width based on rank */}
                  {(() => {
                    const bWidth = Math.max(16, Math.min(48, rank * 0.7 + 14));
                    const aHeight = bWidth;
                    return (
                      <>
                        <rect 
                          x="215" 
                          y="20" 
                          width={bWidth} 
                          height="130" 
                          rx="6" 
                          fill="rgba(56, 189, 248, 0.2)" 
                          stroke="#38bdf8" 
                          strokeWidth="2" 
                        />
                        <text x={215 + bWidth / 2} y="75" textAnchor="middle" fill="#38bdf8" fontWeight="bold" fontSize="12">B</text>
                        <text x={215 + bWidth / 2} y="95" textAnchor="middle" fill="#cbd5e1" fontSize="9" fontFamily="monospace">
                          {activeModel.d}×{rank}
                        </text>

                        {/* Multiplication Cross */}
                        <text x="300" y="90" textAnchor="middle" fill="#ffffff" fontSize="18" fontWeight="bold">×</text>

                        {/* Matrix A (r x k) - Wide & Flat */}
                        <rect 
                          x="330" 
                          y={85 - aHeight / 2} 
                          width="130" 
                          height={aHeight} 
                          rx="6" 
                          fill="rgba(244, 63, 94, 0.2)" 
                          stroke="#f43f5e" 
                          strokeWidth="2" 
                        />
                        <text x="395" y="85" textAnchor="middle" fill="#f43f5e" fontWeight="bold" fontSize="12">A</text>
                        <text x="395" y="103" textAnchor="middle" fill="#cbd5e1" fontSize="9" fontFamily="monospace">
                          {rank}×{activeModel.k}
                        </text>
                      </>
                    );
                  })()}
                </g>

                {/* Bottom Legend */}
                <text x="260" y="170" textAnchor="middle" fill="#94a3b8" fontSize="10">
                  Inner bottleneck rank r = {rank} carries high-gradient intrinsic updates
                </text>
              </svg>
            ) : (
              /* Merged State Diagram */
              <div className="py-6 text-center space-y-2 animate-fadeIn">
                <div className="inline-flex items-center gap-2 p-3 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-300">
                  <CheckCircle2 className="w-5 h-5 text-emerald-400" />
                  <span className="font-bold text-sm">Weights Successfully Merged for Inference</span>
                </div>
                <div className="font-mono text-xs text-white">
                  <KaTeXRenderer math="W_{\text{deploy}} = W_0 + \frac{\alpha}{r} (B \times A) \in \mathbb{R}^{d \times k}" block={true} />
                </div>
                <p className="text-[11px] text-slate-400 max-w-md mx-auto">
                  During production serving, the delta weights are directly added to the original weights. Exactly <strong>0 additional matrix multiplications</strong> and <strong>0 extra milliseconds</strong> of latency are introduced!
                </p>
              </div>
            )}
          </div>

          {/* Educational Insights Box */}
          <div className="p-3.5 bg-slate-950 rounded-xl border border-slate-800 text-xs text-slate-400 space-y-2">
            <div className="font-semibold text-slate-300 flex items-center gap-1.5">
              <Calculator className="w-3.5 h-3.5 text-cyan-400" />
              <span>Why Low-Rank Adaptation Works (Intrinsic Rank Hypothesis):</span>
            </div>
            <p className="text-[11px] leading-relaxed">
              Aghajanyan et al. (2020) demonstrated that pre-trained language models have an extremely low <em>intrinsic dimension</em>. Although the weight matrix contains millions of parameters ($d \times k$), the manifold of gradient updates required to adapt to a downstream task resides in a subspace of rank as small as <KaTeXRenderer math="r = 4" inline={true} /> or <KaTeXRenderer math="r = 8" inline={true} />.
            </p>
          </div>
        </div>

        {/* Right Side: VRAM & Parameter Comparison Cards */}
        <div className="lg:col-span-5 space-y-4">
          {/* Trainable Parameters Card */}
          <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 space-y-3 shadow-sm text-xs">
            <h4 className="font-bold text-white uppercase tracking-wider flex items-center justify-between border-b border-slate-800/80 pb-3">
              <span className="flex items-center gap-1.5">
                <BarChart3 className="w-3.5 h-3.5 text-emerald-400" />
                Trainable Parameter Count
              </span>
              <span className="text-[10px] text-emerald-400 font-mono font-bold">
                {stats.reductionFactor}x Less
              </span>
            </h4>

            <div className="space-y-3 pt-1">
              <div>
                <div className="flex justify-between text-slate-400 mb-1">
                  <span>Full Fine-Tuning:</span>
                  <span className="font-mono text-rose-400 font-bold">{stats.fullTrainableParams}</span>
                </div>
                <div className="h-2 w-full bg-slate-950 rounded-full overflow-hidden">
                  <div className="h-full bg-rose-500 rounded-full w-full" />
                </div>
              </div>

              <div>
                <div className="flex justify-between text-slate-400 mb-1">
                  <span>LoRA (r = {rank}):</span>
                  <span className="font-mono text-emerald-400 font-bold">{stats.loraTrainableParams}</span>
                </div>
                <div className="h-2 w-full bg-slate-950 rounded-full overflow-hidden">
                  <div 
                    className="h-full bg-emerald-400 rounded-full transition-all duration-300"
                    style={{ width: `${Math.max(2, (100 / stats.reductionFactor))}%` }}
                  />
                </div>
              </div>
            </div>
          </div>

          {/* GPU VRAM Hardware Requirement Card */}
          <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 space-y-3 shadow-sm text-xs">
            <h4 className="font-bold text-white uppercase tracking-wider flex items-center justify-between border-b border-slate-800/80 pb-3">
              <span className="flex items-center gap-1.5">
                <Server className="w-3.5 h-3.5 text-indigo-400" />
                GPU VRAM Hardware Requirements
              </span>
              <span className="text-[10px] text-indigo-300 font-mono">FP16 Training</span>
            </h4>

            <div className="space-y-3 pt-1">
              <div className="p-3 bg-slate-950 rounded-xl border border-rose-500/20 space-y-1">
                <div className="flex justify-between items-center">
                  <span className="font-semibold text-rose-300">Full Fine-Tuning:</span>
                  <span className="text-sm font-mono font-bold text-rose-400">{stats.fullTotalVRAM} GB</span>
                </div>
                <div className="text-[10px] text-slate-500">
                  Requires <strong>2x–4x NVIDIA A100 (80GB)</strong> enterprise clusters.
                </div>
              </div>

              <div className="p-3 bg-slate-950 rounded-xl border border-emerald-500/30 space-y-1">
                <div className="flex justify-between items-center">
                  <span className="font-semibold text-emerald-300">LoRA (r = {rank}):</span>
                  <span className="text-sm font-mono font-bold text-emerald-400">{stats.loraTotalVRAM} GB</span>
                </div>
                <div className="text-[10px] text-emerald-400/90">
                  Fits on a single <strong>NVIDIA RTX 4090 (24GB)</strong> consumer workstation!
                </div>
              </div>
            </div>

            <div className="pt-2 border-t border-slate-800/80 text-[10px] text-slate-500 flex justify-between">
              <span>AdamW Optimizer State:</span>
              <span className="font-mono text-slate-400">{stats.loraOptVRAM} (vs. {stats.fullOptVRAM} GB full)</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
