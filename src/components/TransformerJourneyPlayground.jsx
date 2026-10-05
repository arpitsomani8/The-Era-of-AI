import React, { useState, useMemo, useEffect, useRef } from 'react';
import { 
  Cpu, 
  Sparkles, 
  Play, 
  Pause, 
  RotateCcw, 
  ChevronRight, 
  ChevronLeft, 
  Layers, 
  Sliders, 
  Calculator, 
  Binary, 
  Activity, 
  ArrowRight, 
  CheckCircle2, 
  HelpCircle, 
  Maximize2,
  Zap,
  Info,
  Compass,
  CornerDownRight,
  TrendingUp,
  Award
} from 'lucide-react';
import KaTeXRenderer from './KaTeXRenderer';

// Preset Prompts for Token Tracing
const PROMPT_PRESETS = [
  {
    id: 'ai_future',
    label: 'AI & Cognition',
    text: 'The secret to artificial intelligence is deep neural learning',
    targetIndex: 4 // "intelligence"
  },
  {
    id: 'attention',
    label: 'Transformers Paper',
    text: 'Attention is all you need for sequence modeling',
    targetIndex: 0 // "Attention"
  },
  {
    id: 'reasoning',
    label: 'Mathematical Reasoning',
    text: 'Large language models compute tokens through residual stream layers',
    targetIndex: 5 // "tokens"
  }
];

// Architecture Configurations
const ARCHITECTURES = {
  llama3: {
    name: 'Llama 3 8B',
    dModel: 4096,
    nHeads: 32,
    nKVHeads: 8,
    headDim: 128,
    dFFN: 14336,
    vocabSize: 128256,
    norm: 'RMSNorm',
    activation: 'SwiGLU',
    posEncoding: 'RoPE (Rotary, base=500k)',
    color: 'from-cyan-500 to-blue-600'
  },
  mistral: {
    name: 'Mistral 7B v0.3',
    dModel: 4096,
    nHeads: 32,
    nKVHeads: 8,
    headDim: 128,
    dFFN: 14336,
    vocabSize: 32768,
    norm: 'RMSNorm',
    activation: 'SwiGLU',
    posEncoding: 'RoPE (base=10k)',
    color: 'from-amber-500 to-orange-600'
  },
  gemma2: {
    name: 'Gemma 2 9B',
    dModel: 3584,
    nHeads: 16,
    nKVHeads: 8,
    headDim: 256,
    dFFN: 14336,
    vocabSize: 256000,
    norm: 'RMSNorm (Pre & Post)',
    activation: 'GeGLU',
    posEncoding: 'RoPE',
    color: 'from-emerald-500 to-teal-600'
  },
  deepseek: {
    name: 'DeepSeek V3 (MLA)',
    dModel: 7168,
    nHeads: 128,
    nKVHeads: 128,
    headDim: 128,
    dFFN: 18432,
    vocabSize: 102400,
    norm: 'RMSNorm',
    activation: 'SwiGLU (MoE active)',
    posEncoding: 'Decoupled RoPE',
    color: 'from-indigo-500 to-purple-600'
  }
};

// 8 STAGES OF THE TOKEN JOURNEY
const PIPELINE_STAGES = [
  {
    id: 1,
    name: 'Token ID & Embedding Lookup',
    badge: 'Stage 1 / 8',
    short: 'Embedding',
    shapeIn: '[B, 1]',
    shapeOut: '[B, 1, d_model]',
    color: 'border-cyan-500 text-cyan-400',
    summary: 'The raw text token is mapped to a discrete vocabulary ID and translated into a dense high-dimensional latent vector via an embedding lookup matrix.'
  },
  {
    id: 2,
    name: 'Rotary Position Embedding (RoPE)',
    badge: 'Stage 2 / 8',
    short: 'RoPE',
    shapeIn: '[B, 1, d_model]',
    shapeOut: '[B, 1, d_model]',
    color: 'border-indigo-500 text-indigo-400',
    summary: 'Injects sequence position by rotating 2D adjacent coordinate pairs in the complex plane. Allows relative token distance to be naturally computed via inner products.'
  },
  {
    id: 3,
    name: 'Pre-Attention RMSNorm',
    badge: 'Stage 3 / 8',
    short: 'RMSNorm #1',
    shapeIn: '[B, 1, d_model]',
    shapeOut: '[B, 1, d_model]',
    color: 'border-purple-500 text-purple-400',
    summary: 'Root Mean Square Normalization scales the vector across its hidden features to unit variance, preventing activation explosions without expensive mean subtraction.'
  },
  {
    id: 4,
    name: 'Grouped-Query Attention (GQA)',
    badge: 'Stage 4 / 8',
    short: 'GQA Attention',
    shapeIn: '[B, 1, d_model]',
    shapeOut: '[B, 1, d_model]',
    color: 'border-pink-500 text-pink-400',
    summary: 'Projects Query, Key, and Value vectors. Multiple Query heads share a smaller set of Key/Value heads to compress KV cache memory by 75% while maintaining full expressivity.'
  },
  {
    id: 5,
    name: 'Residual Connection #1',
    badge: 'Stage 5 / 8',
    short: 'Add & Skip',
    shapeIn: '[B, 1, d_model]',
    shapeOut: '[B, 1, d_model]',
    color: 'border-emerald-500 text-emerald-400',
    summary: 'Adds the attention output directly back to the pre-norm input. This creates an uninterrupted residual gradient highway allowing 80+ stacked layers to train stably.'
  },
  {
    id: 6,
    name: 'SwiGLU Gated Feedforward Network',
    badge: 'Stage 6 / 8',
    short: 'SwiGLU FFN',
    shapeIn: '[B, 1, d_model]',
    shapeOut: '[B, 1, d_model]',
    color: 'border-amber-500 text-amber-400',
    summary: 'Expands the token vector to d_ffn (~14,336) through parallel Gate and Up projections, gated by the SiLU/Swish activation function, before down-projecting back.'
  },
  {
    id: 7,
    name: 'Residual Connection #2 & Final Norm',
    badge: 'Stage 7 / 8',
    short: 'Residual #2',
    shapeIn: '[B, 1, d_model]',
    shapeOut: '[B, 1, d_model]',
    color: 'border-teal-500 text-teal-400',
    summary: 'Merges the FFN knowledge update back into the residual stream and performs the final RMSNorm pass to stabilize outputs before vocabulary projection.'
  },
  {
    id: 8,
    name: 'LM Head Un-Embedding & Logits',
    badge: 'Stage 8 / 8',
    short: 'LM Head Logits',
    shapeIn: '[B, 1, d_model]',
    shapeOut: '[B, 1, Vocab]',
    color: 'border-rose-500 text-rose-400',
    summary: 'Projects the 4096-dim vector into vocabulary space (128k logits), applies temperature scaling and softmax to generate next-token prediction probability distribution.'
  }
];

export default function TransformerJourneyPlayground() {
  const [selectedArchKey, setSelectedArchKey] = useState('llama3');
  const [promptPreset, setPromptPreset] = useState(PROMPT_PRESETS[0]);
  const [inputText, setInputText] = useState(PROMPT_PRESETS[0].text);
  const [targetTokenIndex, setTargetTokenIndex] = useState(PROMPT_PRESETS[0].targetIndex);
  
  // Pipeline Step (1 to 8)
  const [currentStep, setCurrentStep] = useState(1);
  const [isPlaying, setIsPlaying] = useState(false);
  const [playbackSpeed, setPlaybackSpeed] = useState(2500); // ms per step

  // Interactive Sub-Controls per Stage
  const [embeddingDimWindow, setEmbeddingDimWindow] = useState(0); // 0 to 4080 (in steps of 16)
  const [ropePositionAngle, setRopePositionAngle] = useState(targetTokenIndex);
  const [ropePairIndex, setRopePairIndex] = useState(0); // Which 2D pair (0..7)
  const [selectedQueryHead, setSelectedQueryHead] = useState(0); // 0 to 31
  const [enableResidualAblation, setEnableResidualAblation] = useState(false); // Toggle skip connection
  const [swigluGateModulation, setSwigluGateModulation] = useState(1.0); // 0.0 to 2.0
  const [samplingTemperature, setSamplingTemperature] = useState(0.7); // 0.1 to 2.0
  const [topKFilter, setTopKFilter] = useState(5);

  const arch = ARCHITECTURES[selectedArchKey];

  // Tokenize input string
  const tokens = useMemo(() => {
    const splitTokens = inputText.trim().split(/\s+/).filter(Boolean);
    return splitTokens.length > 0 ? splitTokens : ['AI'];
  }, [inputText]);

  // Keep targetTokenIndex within bounds
  const safeTargetIndex = Math.min(targetTokenIndex, Math.max(0, tokens.length - 1));
  const activeToken = tokens[safeTargetIndex] || 'token';

  // Seeded mock token ID and pseudo-embedding values based on string hash
  const tokenHash = useMemo(() => {
    let hash = 0;
    for (let i = 0; i < activeToken.length; i++) {
      hash = (hash << 5) - hash + activeToken.charCodeAt(i);
      hash |= 0;
    }
    return Math.abs(hash);
  }, [activeToken]);

  const simulatedTokenId = (tokenHash % (arch.vocabSize - 1000)) + 1000;

  // Generate 16 continuous pseudo-random vector dimensions for visual inspection
  const vectorSlice = useMemo(() => {
    const values = [];
    for (let i = 0; i < 16; i++) {
      const idx = embeddingDimWindow + i;
      const seed = Math.sin(tokenHash * 0.17 + idx * 0.43) * 1.5;
      values.push({
        dim: idx,
        val: parseFloat(seed.toFixed(4)),
        normVal: Math.max(-1, Math.min(1, seed))
      });
    }
    return values;
  }, [embeddingDimWindow, tokenHash]);

  // RoPE rotation calculation
  const ropeBase = selectedArchKey === 'llama3' ? 500000 : 10000;
  const ropeTheta = Math.pow(ropeBase, -2 * ropePairIndex / arch.dModel);
  const ropeAngleRadians = (ropePositionAngle * ropeTheta * 15) % (2 * Math.PI); // Scaled for visible UI rotation
  const xOriginal = Math.cos(tokenHash + ropePairIndex) * 0.8;
  const yOriginal = Math.sin(tokenHash + ropePairIndex * 2) * 0.8;
  const xRotated = xOriginal * Math.cos(ropeAngleRadians) - yOriginal * Math.sin(ropeAngleRadians);
  const yRotated = xOriginal * Math.sin(ropeAngleRadians) + yOriginal * Math.cos(ropeAngleRadians);

  // Grouped-Query Attention (GQA) mapping
  // e.g. 32 Query heads, 8 KV heads -> 4 query heads per KV head
  const qPerKV = arch.nHeads / arch.nKVHeads;
  const mappedKVHead = Math.floor(selectedQueryHead / qPerKV);

  // Next Token Logits simulation based on active token and prompt context
  const candidateNextTokens = useMemo(() => {
    const candidatesMap = {
      intelligence: [
        { word: 'is', baseLogit: 6.2 },
        { word: 'requires', baseLogit: 5.1 },
        { word: 'involves', baseLogit: 4.8 },
        { word: 'breakthroughs', baseLogit: 4.3 },
        { word: 'systems', baseLogit: 3.9 }
      ],
      Attention: [
        { word: 'is', baseLogit: 7.4 },
        { word: 'mechanisms', baseLogit: 5.8 },
        { word: 'layers', baseLogit: 4.6 },
        { word: 'scores', baseLogit: 4.1 },
        { word: 'heads', baseLogit: 3.8 }
      ],
      tokens: [
        { word: 'through', baseLogit: 6.5 },
        { word: 'into', baseLogit: 5.3 },
        { word: 'sequentially', baseLogit: 4.9 },
        { word: 'embeddings', baseLogit: 4.2 },
        { word: 'representations', baseLogit: 3.7 }
      ]
    };

    const defaultList = [
      { word: 'learning', baseLogit: 5.8 },
      { word: 'computation', baseLogit: 5.2 },
      { word: 'context', baseLogit: 4.7 },
      { word: 'architecture', baseLogit: 4.1 },
      { word: 'neural', baseLogit: 3.6 }
    ];

    const rawList = candidatesMap[activeToken] || defaultList;

    // Apply temperature scaling: z_i / T
    const scaled = rawList.map(item => ({
      word: item.word,
      scaledLogit: item.baseLogit / Math.max(0.1, samplingTemperature)
    }));

    // Softmax
    const maxVal = Math.max(...scaled.map(s => s.scaledLogit));
    const expVals = scaled.map(s => Math.exp(s.scaledLogit - maxVal));
    const sumExp = expVals.reduce((a, b) => a + b, 0);

    return scaled.map((s, idx) => ({
      word: s.word,
      prob: parseFloat((expVals[idx] / sumExp).toFixed(4)),
      percentage: (expVals[idx] / sumExp * 100).toFixed(1)
    }));
  }, [activeToken, samplingTemperature]);

  // Auto-play timer
  useEffect(() => {
    let interval = null;
    if (isPlaying) {
      interval = setInterval(() => {
        setCurrentStep((prev) => (prev < 8 ? prev + 1 : 1));
      }, playbackSpeed);
    }
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isPlaying, playbackSpeed]);

  const activeStage = PIPELINE_STAGES[currentStep - 1];

  return (
    <div className="space-y-6">
      {/* ========================================================= */}
      {/* TOP HEADER & ARCHITECTURE SPEC SELECTOR */}
      {/* ========================================================= */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 shadow-sm space-y-4">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold tracking-wider uppercase bg-gradient-to-r from-cyan-500/20 to-indigo-500/20 text-cyan-300 border border-cyan-500/40">
                Interactive Architectural Flow
              </span>
              <span className="text-xs text-slate-400 font-mono">Modern Decoder-Only Block</span>
            </div>
            <h2 className="text-xl sm:text-2xl font-bold text-white flex items-center gap-2">
              <Cpu className="w-6 h-6 text-cyan-400" />
              <span>The Transformer Token Journey</span>
            </h2>
            <p className="text-xs text-slate-400 mt-1 max-w-2xl">
              Trace a single token step-by-step through an entire modern LLM Transformer layer — from discrete Token ID and RoPE frequency rotation to GQA Attention, SwiGLU FFN gating, and next-token Softmax logits.
            </p>
          </div>

          {/* Model Architecture Selector */}
          <div className="flex flex-col sm:flex-row items-start sm:items-center gap-2">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider font-mono">
              Architecture:
            </span>
            <div className="flex flex-wrap gap-1.5 bg-slate-950 p-1 rounded-xl border border-slate-800">
              {Object.entries(ARCHITECTURES).map(([key, spec]) => (
                <button
                  key={key}
                  onClick={() => setSelectedArchKey(key)}
                  className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition ${
                    selectedArchKey === key
                      ? 'bg-gradient-to-r text-white shadow-sm ' + spec.color
                      : 'text-slate-400 hover:text-slate-200'
                  }`}
                >
                  {spec.name}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Live Architecture Parameters Strip */}
        <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-2 pt-3 border-t border-slate-800/80 text-[11px] font-mono">
          <div className="bg-slate-950/80 p-2 rounded-xl border border-slate-800">
            <span className="text-slate-500 block text-[9px] uppercase">Hidden Dimension</span>
            <span className="text-cyan-300 font-bold">d_model = {arch.dModel}</span>
          </div>
          <div className="bg-slate-950/80 p-2 rounded-xl border border-slate-800">
            <span className="text-slate-500 block text-[9px] uppercase">Query Heads</span>
            <span className="text-indigo-300 font-bold">H_q = {arch.nHeads} heads</span>
          </div>
          <div className="bg-slate-950/80 p-2 rounded-xl border border-slate-800">
            <span className="text-slate-500 block text-[9px] uppercase">KV Heads (GQA)</span>
            <span className="text-pink-300 font-bold">H_kv = {arch.nKVHeads} (ratio {arch.nHeads / arch.nKVHeads}:1)</span>
          </div>
          <div className="bg-slate-950/80 p-2 rounded-xl border border-slate-800">
            <span className="text-slate-500 block text-[9px] uppercase">Head Dimension</span>
            <span className="text-emerald-300 font-bold">d_k = {arch.headDim}</span>
          </div>
          <div className="bg-slate-950/80 p-2 rounded-xl border border-slate-800">
            <span className="text-slate-500 block text-[9px] uppercase">FFN Expansion</span>
            <span className="text-amber-300 font-bold">d_ffn = {arch.dFFN}</span>
          </div>
          <div className="bg-slate-950/80 p-2 rounded-xl border border-slate-800">
            <span className="text-slate-500 block text-[9px] uppercase">Vocabulary Size</span>
            <span className="text-purple-300 font-bold">|V| = {arch.vocabSize.toLocaleString()}</span>
          </div>
          <div className="bg-slate-950/80 p-2 rounded-xl border border-slate-800">
            <span className="text-slate-500 block text-[9px] uppercase">Non-Linearity</span>
            <span className="text-teal-300 font-bold">{arch.activation}</span>
          </div>
        </div>
      </div>

      {/* ========================================================= */}
      {/* INPUT PROMPT & TOKEN PICKER */}
      {/* ========================================================= */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 space-y-4 shadow-sm">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-3">
          <div>
            <label className="text-xs font-bold text-slate-300 uppercase tracking-wider block">
              Choose or Type Prompt Scenario:
            </label>
            <p className="text-[11px] text-slate-400">
              Click any token below to designate it as the active token to accompany through the Transformer block.
            </p>
          </div>
          <div className="flex flex-wrap gap-1.5">
            {PROMPT_PRESETS.map((p) => (
              <button
                key={p.id}
                onClick={() => {
                  setPromptPreset(p);
                  setInputText(p.text);
                  setTargetTokenIndex(p.targetIndex);
                  setRopePositionAngle(p.targetIndex);
                }}
                className={`px-3 py-1 rounded-lg text-xs font-medium transition ${
                  promptPreset.id === p.id && inputText === p.text
                    ? 'bg-cyan-600 text-white shadow-sm'
                    : 'bg-slate-950 text-slate-400 hover:text-white border border-slate-800'
                }`}
              >
                {p.label}
              </button>
            ))}
          </div>
        </div>

        {/* Text Input Field */}
        <input
          type="text"
          value={inputText}
          onChange={(e) => {
            setInputText(e.target.value);
            setTargetTokenIndex(0);
          }}
          className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-xs sm:text-sm text-white focus:outline-none focus:ring-2 focus:ring-cyan-500 font-mono"
          placeholder="Type any sentence to tokenize..."
        />

        {/* Interactive Token Sequence Chips */}
        <div className="space-y-1.5 pt-1">
          <div className="flex items-center justify-between text-[11px] font-mono text-slate-400">
            <span>Tokenized Sequence ({tokens.length} tokens):</span>
            <span className="text-cyan-400">
              Selected Token: <span className="font-bold underline">"{activeToken}"</span> (Position #{safeTargetIndex})
            </span>
          </div>

          <div className="flex flex-wrap gap-2 p-2 bg-slate-950/70 border border-slate-800 rounded-xl">
            {tokens.map((token, idx) => {
              const isSelected = idx === safeTargetIndex;
              return (
                <button
                  key={`${token}-${idx}`}
                  onClick={() => {
                    setTargetTokenIndex(idx);
                    setRopePositionAngle(idx);
                  }}
                  className={`px-3 py-1.5 rounded-lg text-xs font-mono font-medium transition flex items-center gap-1.5 ${
                    isSelected
                      ? 'bg-cyan-600 text-white shadow-md shadow-cyan-600/30 ring-2 ring-cyan-400'
                      : 'bg-slate-900 text-slate-300 hover:bg-slate-800 hover:text-white border border-slate-700/60'
                  }`}
                >
                  <span className={`text-[10px] ${isSelected ? 'text-cyan-200' : 'text-slate-500'}`}>
                    #{idx}
                  </span>
                  <span>{token}</span>
                  {isSelected && <Sparkles className="w-3 h-3 text-cyan-200 animate-pulse" />}
                </button>
              );
            })}
          </div>
        </div>
      </div>

      {/* ========================================================= */}
      {/* 8-STAGE INTERACTIVE PROGRESS PIPELINE BREADCRUMB */}
      {/* ========================================================= */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-4 shadow-sm space-y-3">
        {/* Stepper Navigation Bar */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <button
              onClick={() => setCurrentStep((prev) => Math.max(1, prev - 1))}
              disabled={currentStep === 1}
              className="p-1.5 px-3 rounded-lg bg-slate-800 hover:bg-slate-700 disabled:opacity-40 disabled:cursor-not-allowed text-xs font-semibold text-slate-200 transition flex items-center gap-1"
            >
              <ChevronLeft className="w-4 h-4" />
              <span>Previous</span>
            </button>

            <button
              onClick={() => setIsPlaying(!isPlaying)}
              className={`p-1.5 px-3 rounded-lg text-xs font-semibold transition flex items-center gap-1.5 shadow-sm ${
                isPlaying 
                  ? 'bg-amber-600 hover:bg-amber-500 text-white' 
                  : 'bg-cyan-600 hover:bg-cyan-500 text-white'
              }`}
            >
              {isPlaying ? <Pause className="w-3.5 h-3.5" /> : <Play className="w-3.5 h-3.5" />}
              <span>{isPlaying ? 'Pause Auto-Run' : 'Auto Step-Through'}</span>
            </button>

            <button
              onClick={() => setCurrentStep((prev) => Math.min(8, prev + 1))}
              disabled={currentStep === 8}
              className="p-1.5 px-3 rounded-lg bg-slate-800 hover:bg-slate-700 disabled:opacity-40 disabled:cursor-not-allowed text-xs font-semibold text-slate-200 transition flex items-center gap-1"
            >
              <span>Next</span>
              <ChevronRight className="w-4 h-4" />
            </button>

            <button
              onClick={() => { setCurrentStep(1); setIsPlaying(false); }}
              className="p-1.5 px-2.5 rounded-lg bg-slate-950 hover:bg-slate-800 text-slate-400 hover:text-slate-200 border border-slate-800 text-xs transition"
              title="Reset to Stage 1"
            >
              <RotateCcw className="w-3.5 h-3.5" />
            </button>
          </div>

          {/* Current Stage Indicator */}
          <div className="flex items-center gap-2 text-xs font-mono">
            <span className="text-slate-400">Pipeline Progress:</span>
            <span className="px-2 py-0.5 rounded-md bg-cyan-500/20 text-cyan-300 font-bold border border-cyan-500/30">
              Stage {currentStep} of 8
            </span>
          </div>
        </div>

        {/* 8 Stage Clickable Cards Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-8 gap-1.5 pt-1">
          {PIPELINE_STAGES.map((stage) => {
            const isCurrent = stage.id === currentStep;
            const isCompleted = stage.id < currentStep;

            return (
              <button
                key={stage.id}
                onClick={() => {
                  setCurrentStep(stage.id);
                  setIsPlaying(false);
                }}
                className={`p-2 rounded-xl text-left transition border flex flex-col justify-between min-h-[72px] ${
                  isCurrent
                    ? 'bg-slate-800/90 border-cyan-400 shadow-lg shadow-cyan-500/20 ring-1 ring-cyan-400'
                    : isCompleted
                    ? 'bg-slate-950/90 border-emerald-500/40 hover:border-emerald-400 text-slate-300'
                    : 'bg-slate-950/40 border-slate-800/80 hover:border-slate-700 text-slate-500'
                }`}
              >
                <div className="flex items-center justify-between w-full mb-1">
                  <span className={`text-[10px] font-mono font-bold ${isCurrent ? 'text-cyan-300' : isCompleted ? 'text-emerald-400' : 'text-slate-500'}`}>
                    0{stage.id}
                  </span>
                  {isCompleted ? (
                    <CheckCircle2 className="w-3 h-3 text-emerald-400 shrink-0" />
                  ) : isCurrent ? (
                    <span className="w-2 h-2 rounded-full bg-cyan-400 animate-ping" />
                  ) : null}
                </div>
                <span className={`text-xs font-semibold leading-tight line-clamp-2 ${isCurrent ? 'text-white' : ''}`}>
                  {stage.short}
                </span>
                <span className="text-[9px] font-mono text-slate-500 mt-1 truncate">
                  {stage.shapeOut}
                </span>
              </button>
            );
          })}
        </div>
      </div>

      {/* ========================================================= */}
      {/* ACTIVE STAGE DEEP DIVE & INTERACTIVE DEMO */}
      {/* ========================================================= */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 shadow-sm space-y-6">
        {/* Stage Header & Tensor Shape Banner */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-4">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold tracking-wider uppercase border ${activeStage.color} bg-slate-950`}>
                {activeStage.badge}
              </span>
              <span className="text-xs text-slate-400 font-mono">
                Tracking Token: <span className="text-white font-bold font-mono">"{activeToken}"</span> (ID: {simulatedTokenId})
              </span>
            </div>
            <h3 className="text-lg sm:text-xl font-bold text-white">
              {activeStage.name}
            </h3>
            <p className="text-xs text-slate-400 mt-1 max-w-3xl leading-relaxed">
              {activeStage.summary}
            </p>
          </div>

          {/* Tensor Dimensions Inspector */}
          <div className="bg-slate-950 p-3 rounded-xl border border-slate-800/80 font-mono text-xs space-y-1 shrink-0">
            <span className="text-[10px] text-slate-500 block uppercase font-bold">Tensor Transformation</span>
            <div className="flex items-center gap-2">
              <span className="text-slate-400">{activeStage.shapeIn}</span>
              <ArrowRight className="w-3.5 h-3.5 text-cyan-400" />
              <span className="text-cyan-300 font-bold">{activeStage.shapeOut}</span>
            </div>
          </div>
        </div>

        {/* ========================================================= */}
        {/* STAGE 1: TOKEN ID & EMBEDDING LOOKUP */}
        {/* ========================================================= */}
        {currentStep === 1 && (
          <div className="space-y-6 animate-fadeIn">
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
              {/* Left Column: Mathematical Formulation & Explanation */}
              <div className="lg:col-span-5 space-y-4">
                <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-2">
                  <h4 className="text-xs font-bold text-cyan-400 uppercase tracking-wider font-mono flex items-center gap-1.5">
                    <Calculator className="w-3.5 h-3.5" />
                    <span>Embedding Lookup Formulation</span>
                  </h4>
                  <div className="py-1">
                    <KaTeXRenderer math="x_0 = \text{EmbeddingLookup}(t_{\text{token}}) = W_E[t_{\text{token}}, :] \in \mathbb{R}^{d_{\text{model}}}" />
                  </div>
                  <p className="text-xs text-slate-400 leading-relaxed">
                    The token ID indexes row <span className="text-cyan-300 font-mono">{simulatedTokenId}</span> of the weight matrix <KaTeXRenderer math="W_E \in \mathbb{R}^{|V| \times d_{\text{model}}}" inline={true} />. In <span className="text-white font-semibold">{arch.name}</span>, this projects our 1D token into a <span className="text-cyan-300 font-mono">{arch.dModel}</span>-dimensional continuous semantic space.
                  </p>
                </div>

                <div className="bg-slate-950/60 p-4 rounded-xl border border-slate-800 space-y-2 text-xs">
                  <span className="font-bold text-slate-300 uppercase tracking-wider block text-[11px]">
                    Why High Hidden Dimensions? ({arch.dModel})
                  </span>
                  <p className="text-slate-400 leading-relaxed">
                    A vector with 4,096 continuous dimensions can simultaneously encode thousands of orthogonal concepts: grammatical syntax, sentiment, world knowledge facts, tense, and contextual relationships without semantic collisions.
                  </p>
                </div>
              </div>

              {/* Right Column: Interactive Vector Slice Explorer */}
              <div className="lg:col-span-7 bg-slate-950 p-5 rounded-xl border border-slate-800 space-y-4">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800/80 pb-3">
                  <div className="flex items-center gap-2">
                    <Binary className="w-4 h-4 text-cyan-400" />
                    <span className="text-xs font-bold text-white font-mono uppercase">
                      Embedding Vector Window: d[{embeddingDimWindow} .. {embeddingDimWindow + 15}]
                    </span>
                  </div>
                  <span className="text-[11px] font-mono text-cyan-300">
                    Total: {arch.dModel} continuous floats
                  </span>
                </div>

                {/* Slider to shift window across 4096 dimensions */}
                <div className="space-y-1.5">
                  <div className="flex justify-between text-xs text-slate-400 font-mono">
                    <span>Inspect Dimension Offset:</span>
                    <span className="text-white font-bold">{embeddingDimWindow} / {arch.dModel - 16}</span>
                  </div>
                  <input
                    type="range"
                    min="0"
                    max={arch.dModel - 16}
                    step="16"
                    value={embeddingDimWindow}
                    onChange={(e) => setEmbeddingDimWindow(parseInt(e.target.value))}
                    className="w-full accent-cyan-500 h-1.5 bg-slate-800 rounded-lg cursor-pointer"
                  />
                </div>

                {/* Vector Bar Visualizer */}
                <div className="grid grid-cols-4 sm:grid-cols-8 gap-2 pt-2">
                  {vectorSlice.map((slot) => {
                    const isPositive = slot.val >= 0;
                    return (
                      <div
                        key={slot.dim}
                        className="bg-slate-900 border border-slate-800 rounded-lg p-2 text-center space-y-1.5 hover:border-cyan-500/60 transition group"
                      >
                        <span className="text-[10px] font-mono text-slate-500 block">
                          d_{slot.dim}
                        </span>
                        {/* Vertical mini bar */}
                        <div className="h-14 w-full bg-slate-950 rounded flex items-center justify-center p-1 relative overflow-hidden">
                          <div
                            className={`w-full rounded transition-all duration-300 ${
                              isPositive ? 'bg-cyan-500' : 'bg-rose-500'
                            }`}
                            style={{
                              height: `${Math.min(100, Math.abs(slot.normVal) * 80 + 20)}%`,
                              opacity: Math.max(0.4, Math.abs(slot.normVal))
                            }}
                          />
                        </div>
                        <span className={`text-[10px] font-mono font-bold block ${isPositive ? 'text-cyan-300' : 'text-rose-400'}`}>
                          {slot.val > 0 ? `+${slot.val}` : slot.val}
                        </span>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* STAGE 2: ROTARY POSITION EMBEDDING (ROPE) */}
        {/* ========================================================= */}
        {currentStep === 2 && (
          <div className="space-y-6 animate-fadeIn">
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
              {/* Left Column: RoPE Math & Theory */}
              <div className="lg:col-span-5 space-y-4">
                <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-2">
                  <h4 className="text-xs font-bold text-indigo-400 uppercase tracking-wider font-mono flex items-center gap-1.5">
                    <Compass className="w-3.5 h-3.5" />
                    <span>Rotary Embedding Equation</span>
                  </h4>
                  <div className="py-1">
                    <KaTeXRenderer math="\begin{pmatrix} x'_{2i} \\ x'_{2i+1} \end{pmatrix} = \begin{pmatrix} \cos(m\theta_i) & -\sin(m\theta_i) \\ \sin(m\theta_i) & \cos(m\theta_i) \end{pmatrix} \begin{pmatrix} x_{2i} \\ x_{2i+1} \end{pmatrix}" />
                  </div>
                  <div className="py-0.5">
                    <KaTeXRenderer math="\theta_i = b^{-2i/d}, \quad b = 500{,}000 \text{ (Llama 3)}" />
                  </div>
                  <p className="text-xs text-slate-400 leading-relaxed">
                    Instead of adding static positional vectors, RoPE treats adjacent coordinate pairs as 2D complex numbers and rotates them by angle <KaTeXRenderer math="m \theta_i" inline={true} /> proportional to sequence position <KaTeXRenderer math="m" inline={true} />.
                  </p>
                </div>

                <div className="bg-slate-950/60 p-4 rounded-xl border border-slate-800 space-y-2 text-xs">
                  <span className="font-bold text-indigo-300 uppercase tracking-wider block text-[11px]">
                    The Inner Product Invariance Property:
                  </span>
                  <KaTeXRenderer math="\langle R_m q, R_n k \rangle = q^T R_{n-m} k" />
                  <p className="text-slate-400 leading-relaxed mt-1">
                    When Query at position <KaTeXRenderer math="m" inline={true} /> and Key at position <KaTeXRenderer math="n" inline={true} /> multiply in Attention, their dot product depends solely on their relative distance <KaTeXRenderer math="(n - m)" inline={true} />, allowing natural generalization across long contexts.
                  </p>
                </div>
              </div>

              {/* Right Column: Interactive 2D Complex Rotation Visualizer */}
              <div className="lg:col-span-7 bg-slate-950 p-5 rounded-xl border border-slate-800 space-y-4">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800/80 pb-3">
                  <span className="text-xs font-bold text-white font-mono uppercase flex items-center gap-1.5">
                    <Compass className="w-4 h-4 text-indigo-400" />
                    <span>2D Subspace Rotation: Pair (x_{2 * ropePairIndex}, x_{2 * ropePairIndex + 1})</span>
                  </span>
                  <span className="text-xs font-mono text-indigo-300">
                    Pos m = {ropePositionAngle} &bull; θ = {(ropeAngleRadians * 180 / Math.PI).toFixed(1)}°
                  </span>
                </div>

                {/* Subspace Controls */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                  <div className="space-y-1">
                    <div className="flex justify-between text-slate-400 font-mono">
                      <span>Token Position (m):</span>
                      <span className="text-white font-bold">{ropePositionAngle}</span>
                    </div>
                    <input
                      type="range"
                      min="0"
                      max={Math.max(10, tokens.length + 5)}
                      value={ropePositionAngle}
                      onChange={(e) => setRopePositionAngle(parseInt(e.target.value))}
                      className="w-full accent-indigo-500 h-1.5 bg-slate-800 rounded-lg cursor-pointer"
                    />
                  </div>

                  <div className="space-y-1">
                    <div className="flex justify-between text-slate-400 font-mono">
                      <span>Frequency Channel (i):</span>
                      <span className="text-white font-bold">Pair #{ropePairIndex} ({ropePairIndex === 0 ? 'Highest Freq' : 'Lower Freq'})</span>
                    </div>
                    <input
                      type="range"
                      min="0"
                      max="7"
                      value={ropePairIndex}
                      onChange={(e) => setRopePairIndex(parseInt(e.target.value))}
                      className="w-full accent-indigo-500 h-1.5 bg-slate-800 rounded-lg cursor-pointer"
                    />
                  </div>
                </div>

                {/* Interactive SVG Unit Circle Rotation */}
                <div className="flex items-center justify-center p-3 bg-slate-900/60 rounded-xl border border-slate-800">
                  <svg width="240" height="240" viewBox="-120 -120 240 240" className="overflow-visible">
                    {/* Circle Axis */}
                    <circle cx="0" cy="0" r="90" fill="none" stroke="#334155" strokeWidth="1" strokeDasharray="4 4" />
                    <line x1="-110" y1="0" x2="110" y2="0" stroke="#475569" strokeWidth="1" />
                    <line x1="0" y1="-110" x2="0" y2="110" stroke="#475569" strokeWidth="1" />

                    {/* Original Vector (Position 0 baseline) */}
                    <line
                      x1="0"
                      y1="0"
                      x2={xOriginal * 90}
                      y2={-yOriginal * 90}
                      stroke="#64748b"
                      strokeWidth="2"
                      strokeDasharray="3 3"
                    />
                    <circle cx={xOriginal * 90} cy={-yOriginal * 90} r="4" fill="#64748b" />
                    <text x={xOriginal * 90 + 8} y={-yOriginal * 90} fill="#94a3b8" fontSize="10" fontFamily="monospace">
                      Base (m=0)
                    </text>

                    {/* Rotated Vector */}
                    <line
                      x1="0"
                      y1="0"
                      x2={xRotated * 90}
                      y2={-yRotated * 90}
                      stroke="#818cf8"
                      strokeWidth="3"
                    />
                    <circle cx={xRotated * 90} cy={-yRotated * 90} r="5" fill="#a5b4fc" />
                    <text x={xRotated * 90 + 8} y={-yRotated * 90} fill="#c7d2fe" fontSize="11" fontWeight="bold" fontFamily="monospace">
                      RoPE(m={ropePositionAngle})
                    </text>

                    {/* Angle arc */}
                    <path
                      d={`M ${xOriginal * 30} ${-yOriginal * 30} A 30 30 0 0 1 ${xRotated * 30} ${-yRotated * 30}`}
                      fill="none"
                      stroke="#a855f7"
                      strokeWidth="2"
                    />
                  </svg>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* STAGE 3: PRE-ATTENTION RMSNORM */}
        {/* ========================================================= */}
        {currentStep === 3 && (
          <div className="space-y-6 animate-fadeIn">
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
              <div className="lg:col-span-5 space-y-4">
                <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-2">
                  <h4 className="text-xs font-bold text-purple-400 uppercase tracking-wider font-mono flex items-center gap-1.5">
                    <Activity className="w-3.5 h-3.5" />
                    <span>RMSNorm vs LayerNorm</span>
                  </h4>
                  <div className="py-1">
                    <KaTeXRenderer math="\text{RMSNorm}(x) = \frac{x}{\text{RMS}(x)} \odot \gamma" />
                  </div>
                  <div className="py-0.5">
                    <KaTeXRenderer math="\text{RMS}(x) = \sqrt{\frac{1}{d} \sum_{i=1}^d x_i^2 + \epsilon}" />
                  </div>
                  <p className="text-xs text-slate-400 leading-relaxed">
                    Standard LayerNorm computes both the mean <KaTeXRenderer math="\mu" inline={true} /> and variance <KaTeXRenderer math="\sigma^2" inline={true} />. RMSNorm assumes mean activation is approximately 0, eliminating the mean computation pass and saving <span className="text-purple-300 font-semibold">7% to 12% GPU memory bandwidth</span>.
                  </p>
                </div>

                <div className="bg-slate-950/60 p-4 rounded-xl border border-slate-800 space-y-2 text-xs">
                  <span className="font-bold text-purple-300 uppercase tracking-wider block text-[11px]">
                    Pre-Norm vs Post-Norm Stability:
                  </span>
                  <p className="text-slate-400 leading-relaxed">
                    Original 2017 Transformers used Post-Norm (<KaTeXRenderer math="x + \text{Norm}(\dots)" inline={true} />), which suffered from unstable initial gradient spikes. All modern LLMs use <span className="text-white font-semibold">Pre-Norm</span> (<KaTeXRenderer math="x + \text{Attn}(\text{RMSNorm}(x))" inline={true} />) where the main highway remains untouched.
                  </p>
                </div>
              </div>

              {/* Right Column: Numerical Variance Rescaling Simulator */}
              <div className="lg:col-span-7 bg-slate-950 p-5 rounded-xl border border-slate-800 space-y-4">
                <div className="flex items-center justify-between border-b border-slate-800/80 pb-3">
                  <span className="text-xs font-bold text-white font-mono uppercase">
                    Variance Scaling Comparison
                  </span>
                  <span className="text-xs font-mono text-purple-300">
                    ε = 1e-6 &bull; Gain γ ≈ 1.0
                  </span>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  {/* Before RMSNorm */}
                  <div className="bg-slate-900/80 p-3.5 rounded-xl border border-slate-800 space-y-2">
                    <span className="text-xs font-bold text-rose-400 block font-mono">
                      Raw Vector (Pre-Norm)
                    </span>
                    <p className="text-[11px] text-slate-400">
                      Activations can have wildly varying magnitudes across tokens:
                    </p>
                    <div className="font-mono text-xs text-slate-300 bg-slate-950 p-2.5 rounded-lg border border-slate-800 space-y-1">
                      <div>RMS Magnitude: <span className="text-rose-400 font-bold">2.418</span></div>
                      <div>Max Component: <span className="text-rose-400 font-bold">+5.89</span></div>
                      <div>Min Component: <span className="text-rose-400 font-bold">-4.72</span></div>
                    </div>
                  </div>

                  {/* After RMSNorm */}
                  <div className="bg-slate-900/80 p-3.5 rounded-xl border border-purple-500/40 space-y-2">
                    <span className="text-xs font-bold text-purple-300 block font-mono">
                      Normalized Output Vector
                    </span>
                    <p className="text-[11px] text-slate-400">
                      Rescaled to exact unit variance across hidden channels:
                    </p>
                    <div className="font-mono text-xs text-slate-300 bg-slate-950 p-2.5 rounded-lg border border-slate-800 space-y-1">
                      <div>RMS Magnitude: <span className="text-purple-300 font-bold">1.000</span></div>
                      <div>Max Component: <span className="text-purple-300 font-bold">+2.43</span></div>
                      <div>Min Component: <span className="text-purple-300 font-bold">-1.95</span></div>
                    </div>
                  </div>
                </div>

                <div className="p-3 bg-purple-500/10 border border-purple-500/20 rounded-xl text-xs text-purple-200">
                  <span className="font-bold">Key Insight:</span> By scaling by <KaTeXRenderer math="1/\text{RMS}" inline={true} />, the subsequent dot products in Self-Attention remain well-behaved without pushing softmax into saturated flat zero-gradient regions.
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* STAGE 4: GROUPED-QUERY ATTENTION (GQA) */}
        {/* ========================================================= */}
        {currentStep === 4 && (
          <div className="space-y-6 animate-fadeIn">
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
              <div className="lg:col-span-5 space-y-4">
                <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-2">
                  <h4 className="text-xs font-bold text-pink-400 uppercase tracking-wider font-mono flex items-center gap-1.5">
                    <Layers className="w-3.5 h-3.5" />
                    <span>GQA Attention Formulation</span>
                  </h4>
                  <div className="py-1">
                    <KaTeXRenderer math="\text{Attention}(Q_h, K_g, V_g) = \text{softmax}\left(\frac{Q_h K_g^T}{\sqrt{d_k}} + M\right) V_g" />
                  </div>
                  <div className="py-0.5">
                    <KaTeXRenderer math="g = \lfloor h / 4 \rfloor, \quad h \in [0..31], \quad g \in [0..7]" />
                  </div>
                  <p className="text-xs text-slate-400 leading-relaxed">
                    Standard Multi-Head Attention (MHA) pairs 1 Key/Value head per Query head (32:32). Grouped-Query Attention assigns <span className="text-pink-300 font-semibold">{arch.nHeads / arch.nKVHeads} Query heads to share 1 KV head</span>, saving 75% memory footprint in the KV-cache during inference generation.
                  </p>
                </div>

                <div className="bg-slate-950/60 p-4 rounded-xl border border-slate-800 space-y-2 text-xs">
                  <span className="font-bold text-pink-300 uppercase tracking-wider block text-[11px]">
                    KV Cache Compression Impact:
                  </span>
                  <p className="text-slate-400 leading-relaxed">
                    For a batch size of 16 and 8,192 tokens in FP16, MHA KV cache consumes <span className="text-rose-400 font-semibold">16.4 GB</span> VRAM. GQA 4:1 reduces this to just <span className="text-emerald-400 font-semibold">4.1 GB</span> with negligible 0.2% perplexity change.
                  </p>
                </div>
              </div>

              {/* Right Column: Interactive GQA Head Mapping Explorer */}
              <div className="lg:col-span-7 bg-slate-950 p-5 rounded-xl border border-slate-800 space-y-4">
                <div className="flex items-center justify-between border-b border-slate-800/80 pb-3">
                  <span className="text-xs font-bold text-white font-mono uppercase">
                    Interactive GQA Head Routing
                  </span>
                  <span className="text-xs font-mono text-pink-300">
                    Query Head #{selectedQueryHead} → Shared KV Head #{mappedKVHead}
                  </span>
                </div>

                {/* Query Head Selector Grid */}
                <div className="space-y-1.5">
                  <label className="text-xs text-slate-400 font-mono block">
                    Select Query Head ({arch.nHeads} heads total):
                  </label>
                  <div className="grid grid-cols-8 sm:grid-cols-16 gap-1">
                    {Array.from({ length: arch.nHeads }).map((_, idx) => (
                      <button
                        key={idx}
                        onClick={() => setSelectedQueryHead(idx)}
                        className={`p-1 rounded text-[10px] font-mono font-bold transition text-center ${
                          selectedQueryHead === idx
                            ? 'bg-pink-600 text-white shadow-sm ring-1 ring-pink-400'
                            : Math.floor(idx / qPerKV) === mappedKVHead
                            ? 'bg-pink-500/20 text-pink-300 border border-pink-500/30'
                            : 'bg-slate-900 text-slate-400 hover:text-white'
                        }`}
                      >
                        Q{idx}
                      </button>
                    ))}
                  </div>
                </div>

                {/* Visual GQA Grouping Diagram */}
                <div className="p-4 bg-slate-900/70 rounded-xl border border-slate-800 space-y-3">
                  <span className="text-[11px] font-mono text-slate-400 uppercase font-bold block">
                    Shared KV Group #{mappedKVHead} Mapping:
                  </span>
                  <div className="flex flex-wrap items-center gap-2 text-xs font-mono">
                    <div className="flex items-center gap-1.5 p-2 bg-pink-500/10 border border-pink-500/30 rounded-lg">
                      <span className="text-pink-300 font-bold">Query Heads:</span>
                      <span className="text-white">
                        [Q{mappedKVHead * 4}, Q{mappedKVHead * 4 + 1}, Q{mappedKVHead * 4 + 2}, Q{mappedKVHead * 4 + 3}]
                      </span>
                    </div>
                    <ArrowRight className="w-4 h-4 text-slate-500" />
                    <div className="p-2 bg-indigo-500/10 border border-indigo-500/30 rounded-lg">
                      <span className="text-indigo-300 font-bold">Shared Key/Value:</span>
                      <span className="text-white ml-1">KV_{mappedKVHead}</span>
                    </div>
                  </div>
                  <p className="text-[11px] text-slate-400">
                    All 4 Query heads project their distinct questions, but look up into the exact same Key/Value memory buffer.
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* STAGE 5: RESIDUAL CONNECTION #1 */}
        {/* ========================================================= */}
        {currentStep === 5 && (
          <div className="space-y-6 animate-fadeIn">
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
              <div className="lg:col-span-5 space-y-4">
                <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-2">
                  <h4 className="text-xs font-bold text-emerald-400 uppercase tracking-wider font-mono flex items-center gap-1.5">
                    <Zap className="w-3.5 h-3.5" />
                    <span>Residual Gradient Highway</span>
                  </h4>
                  <div className="py-1">
                    <KaTeXRenderer math="x_{\text{post-attn}} = x_0 + \text{Dropout}(\text{GQA}(\text{RMSNorm}(x_0)))" />
                  </div>
                  <p className="text-xs text-slate-400 leading-relaxed">
                    The token representation doesn't get completely overwritten by Attention. Instead, the Attention mechanism computes a <span className="text-emerald-300 font-semibold">delta update</span> that is element-wise added onto the original token vector.
                  </p>
                </div>

                <div className="bg-slate-950/60 p-4 rounded-xl border border-slate-800 space-y-2 text-xs">
                  <span className="font-bold text-emerald-300 uppercase tracking-wider block text-[11px]">
                    The Backpropagation Identity Rule:
                  </span>
                  <KaTeXRenderer math="\frac{\partial \mathcal{L}}{\partial x_0} = \frac{\partial \mathcal{L}}{\partial x_{\text{post}}} \left( \mathbf{I} + \frac{\partial \text{Attn}}{\partial x_0} \right)" />
                  <p className="text-slate-400 leading-relaxed mt-1">
                    The identity matrix <KaTeXRenderer math="\mathbf{I}" inline={true} /> ensures gradients can backpropagate directly across 80+ layers without decaying to zero.
                  </p>
                </div>
              </div>

              {/* Right Column: Skip Connection Ablation Test */}
              <div className="lg:col-span-7 bg-slate-950 p-5 rounded-xl border border-slate-800 space-y-4">
                <div className="flex items-center justify-between border-b border-slate-800/80 pb-3">
                  <span className="text-xs font-bold text-white font-mono uppercase">
                    Interactive Skip Connection Ablation Test
                  </span>
                  <button
                    onClick={() => setEnableResidualAblation(!enableResidualAblation)}
                    className={`px-3 py-1 rounded-lg text-xs font-mono font-semibold transition ${
                      enableResidualAblation
                        ? 'bg-rose-600 text-white shadow-sm'
                        : 'bg-emerald-600 text-white shadow-sm'
                    }`}
                  >
                    {enableResidualAblation ? 'Ablated (Skip Cut OFF)' : 'Normal (Highway Active)'}
                  </button>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className={`p-4 rounded-xl border space-y-2 transition ${
                    !enableResidualAblation ? 'bg-emerald-500/10 border-emerald-500/30' : 'bg-slate-900 border-slate-800 opacity-60'
                  }`}>
                    <span className="text-xs font-bold text-emerald-300 font-mono block">
                      With Residual Highway (Standard)
                    </span>
                    <p className="text-[11px] text-slate-300 leading-relaxed">
                      Token retains its original grammatical identity and semantic embedding while smoothly incorporating contextual information from neighboring tokens.
                    </p>
                    <span className="text-[10px] font-mono text-emerald-400 font-bold block pt-1">
                      Gradient Flow: 100% Unattenuated
                    </span>
                  </div>

                  <div className={`p-4 rounded-xl border space-y-2 transition ${
                    enableResidualAblation ? 'bg-rose-500/10 border-rose-500/30' : 'bg-slate-900 border-slate-800 opacity-60'
                  }`}>
                    <span className="text-xs font-bold text-rose-300 font-mono block">
                      Without Residual Highway (Ablated)
                    </span>
                    <p className="text-[11px] text-slate-300 leading-relaxed">
                      Token vector is violently warped. Deep networks suffer gradient collapse and cannot train past layer 8.
                    </p>
                    <span className="text-[10px] font-mono text-rose-400 font-bold block pt-1">
                      Gradient Flow: Vanishes exponentially (0.01%)
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* STAGE 6: SWIGLU GATED FEEDFORWARD NETWORK */}
        {/* ========================================================= */}
        {currentStep === 6 && (
          <div className="space-y-6 animate-fadeIn">
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
              <div className="lg:col-span-5 space-y-4">
                <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-2">
                  <h4 className="text-xs font-bold text-amber-400 uppercase tracking-wider font-mono flex items-center gap-1.5">
                    <Sliders className="w-3.5 h-3.5" />
                    <span>SwiGLU Gated Activation</span>
                  </h4>
                  <div className="py-1">
                    <KaTeXRenderer math="\text{FFN}_{\text{SwiGLU}}(x) = \left( \text{Swish}(x W_{\text{gate}}) \otimes x W_{\text{up}} \right) W_{\text{down}}" />
                  </div>
                  <div className="py-0.5">
                    <KaTeXRenderer math="\text{Swish}(z) = z \cdot \sigma(z) = \frac{z}{1 + e^{-z}}" />
                  </div>
                  <p className="text-xs text-slate-400 leading-relaxed">
                    Instead of a single linear layer with ReLU or GELU, SwiGLU projects the input through two parallel matrices (<KaTeXRenderer math="W_{\text{gate}}" inline={true} /> and <KaTeXRenderer math="W_{\text{up}}" inline={true} />) of dimension <span className="text-amber-300 font-mono">{arch.dFFN}</span>, element-wise multiplying them before down-projecting.
                  </p>
                </div>

                <div className="bg-slate-950/60 p-4 rounded-xl border border-slate-800 space-y-2 text-xs">
                  <span className="font-bold text-amber-300 uppercase tracking-wider block text-[11px]">
                    Why FFN Stores Factual Knowledge:
                  </span>
                  <p className="text-slate-400 leading-relaxed">
                    Attention routes information <span className="italic">between</span> tokens in the context, while the Feedforward Network acts as an associative key-value memory retrieving world facts stored during pre-training.
                  </p>
                </div>
              </div>

              {/* Right Column: SwiGLU Gate Modulator Simulator */}
              <div className="lg:col-span-7 bg-slate-950 p-5 rounded-xl border border-slate-800 space-y-4">
                <div className="flex items-center justify-between border-b border-slate-800/80 pb-3">
                  <span className="text-xs font-bold text-white font-mono uppercase">
                    Interactive SwiGLU Gating Modulation
                  </span>
                  <span className="text-xs font-mono text-amber-300">
                    Dimension: {arch.dModel} → {arch.dFFN} → {arch.dModel}
                  </span>
                </div>

                {/* Slider for gate activation level */}
                <div className="space-y-1.5">
                  <div className="flex justify-between text-xs text-slate-400 font-mono">
                    <span>Gate Linear Activation (z):</span>
                    <span className="text-amber-300 font-bold">{swigluGateModulation.toFixed(2)}</span>
                  </div>
                  <input
                    type="range"
                    min="-3.0"
                    max="3.0"
                    step="0.1"
                    value={swigluGateModulation}
                    onChange={(e) => setSwigluGateModulation(parseFloat(e.target.value))}
                    className="w-full accent-amber-500 h-1.5 bg-slate-800 rounded-lg cursor-pointer"
                  />
                </div>

                {/* Live Output Calculator */}
                {(() => {
                  const z = swigluGateModulation;
                  const sigmoid = 1 / (1 + Math.exp(-z));
                  const swish = z * sigmoid;
                  const upVal = 1.25;
                  const gatedProduct = swish * upVal;

                  return (
                    <div className="grid grid-cols-3 gap-3 text-center text-xs font-mono pt-2">
                      <div className="bg-slate-900 p-3 rounded-xl border border-slate-800">
                        <span className="text-slate-500 block text-[10px] uppercase">Swish Gate (z · σ(z))</span>
                        <span className="text-amber-400 text-sm font-bold">{swish.toFixed(3)}</span>
                      </div>
                      <div className="bg-slate-900 p-3 rounded-xl border border-slate-800">
                        <span className="text-slate-500 block text-[10px] uppercase">Up Projection (x W_up)</span>
                        <span className="text-cyan-400 text-sm font-bold">+{upVal.toFixed(2)}</span>
                      </div>
                      <div className="bg-slate-900 p-3 rounded-xl border border-amber-500/40">
                        <span className="text-slate-400 block text-[10px] uppercase">Gated Product (⊗)</span>
                        <span className="text-emerald-400 text-sm font-bold">{gatedProduct.toFixed(3)}</span>
                      </div>
                    </div>
                  );
                })()}

                <div className="p-3 bg-amber-500/10 border border-amber-500/20 rounded-xl text-xs text-amber-200">
                  <span className="font-bold">Gating Mechanism:</span> When <KaTeXRenderer math="z \ll 0" inline={true} />, the gate completely suppresses feature transmission (output = 0). When <KaTeXRenderer math="z > 0" inline={true} />, it allows non-linear feature amplifying through the Up stream.
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* STAGE 7: RESIDUAL CONNECTION #2 & FINAL RMSNORM */}
        {/* ========================================================= */}
        {currentStep === 7 && (
          <div className="space-y-6 animate-fadeIn">
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
              <div className="lg:col-span-5 space-y-4">
                <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-2">
                  <h4 className="text-xs font-bold text-teal-400 uppercase tracking-wider font-mono flex items-center gap-1.5">
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    <span>Second Residual Addition & Final Norm</span>
                  </h4>
                  <div className="py-1">
                    <KaTeXRenderer math="x_{\text{post-ffn}} = x_{\text{post-attn}} + \text{FFN}_{\text{SwiGLU}}(\text{RMSNorm}(x_{\text{post-attn}}))" />
                  </div>
                  <div className="py-0.5">
                    <KaTeXRenderer math="h_{\text{final}} = \text{RMSNorm}_{\text{final}}(x_{\text{post-ffn}}) \in \mathbb{R}^{d_{\text{model}}}" />
                  </div>
                  <p className="text-xs text-slate-400 leading-relaxed">
                    The token vector now carries the accumulated contributions of both Self-Attention (relational context) and the Feedforward network (factual knowledge). The final RMSNorm pass prepares the vector for vocabulary logit decoding.
                  </p>
                </div>
              </div>

              <div className="lg:col-span-7 bg-slate-950 p-5 rounded-xl border border-slate-800 space-y-4">
                <span className="text-xs font-bold text-white font-mono uppercase block border-b border-slate-800/80 pb-3">
                  Layer Completion Summary
                </span>
                <div className="space-y-3 text-xs">
                  <div className="p-3 bg-slate-900 rounded-xl border border-slate-800 flex items-center justify-between font-mono">
                    <span className="text-slate-400">Total Hidden Dimension Preserved:</span>
                    <span className="text-cyan-300 font-bold">{arch.dModel} channels</span>
                  </div>
                  <div className="p-3 bg-slate-900 rounded-xl border border-slate-800 flex items-center justify-between font-mono">
                    <span className="text-slate-400">Number of Layers Stacked (e.g. Llama 3 8B):</span>
                    <span className="text-indigo-300 font-bold">32 Transformer Blocks</span>
                  </div>
                  <div className="p-3 bg-slate-900 rounded-xl border border-slate-800 flex items-center justify-between font-mono">
                    <span className="text-slate-400">Final Norm Variance:</span>
                    <span className="text-teal-300 font-bold">Exact Unit Variance (σ = 1.000)</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* STAGE 8: LM HEAD UN-EMBEDDING & LOGITS */}
        {/* ========================================================= */}
        {currentStep === 8 && (
          <div className="space-y-6 animate-fadeIn">
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
              <div className="lg:col-span-5 space-y-4">
                <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-2">
                  <h4 className="text-xs font-bold text-rose-400 uppercase tracking-wider font-mono flex items-center gap-1.5">
                    <TrendingUp className="w-3.5 h-3.5" />
                    <span>LM Head & Softmax Sampling</span>
                  </h4>
                  <div className="py-1">
                    <KaTeXRenderer math="z = h_{\text{final}} W_{\text{vocab}}^T \in \mathbb{R}^{|V|}, \quad |V| = 128{,}256" />
                  </div>
                  <div className="py-0.5">
                    <KaTeXRenderer math="P(w_i | \text{context}) = \frac{\exp(z_i / T)}{\sum_{j=1}^{|V|} \exp(z_j / T)}" />
                  </div>
                  <p className="text-xs text-slate-400 leading-relaxed">
                    The final 4096-dim vector is projected across all {arch.vocabSize.toLocaleString()} vocabulary candidates. Dividing by temperature <KaTeXRenderer math="T" inline={true} /> tunes the sharpness of next-token sampling.
                  </p>
                </div>

                {/* Temperature Slider */}
                <div className="bg-slate-950/80 p-4 rounded-xl border border-slate-800 space-y-2">
                  <div className="flex justify-between text-xs font-mono text-slate-300">
                    <span>Softmax Temperature (T):</span>
                    <span className="text-rose-400 font-bold">{samplingTemperature.toFixed(2)}</span>
                  </div>
                  <input
                    type="range"
                    min="0.1"
                    max="2.0"
                    step="0.05"
                    value={samplingTemperature}
                    onChange={(e) => setSamplingTemperature(parseFloat(e.target.value))}
                    className="w-full accent-rose-500 h-1.5 bg-slate-800 rounded-lg cursor-pointer"
                  />
                  <div className="flex justify-between text-[10px] text-slate-500 font-mono">
                    <span>0.1 (Greedy / Argmax)</span>
                    <span>0.7 (Balanced)</span>
                    <span>2.0 (High Entropy / Creative)</span>
                  </div>
                </div>
              </div>

              {/* Right Column: Top Candidate Next Tokens Probability Bars */}
              <div className="lg:col-span-7 bg-slate-950 p-5 rounded-xl border border-slate-800 space-y-4">
                <div className="flex items-center justify-between border-b border-slate-800/80 pb-3">
                  <span className="text-xs font-bold text-white font-mono uppercase">
                    Top Next-Token Candidates Distribution
                  </span>
                  <span className="text-xs font-mono text-rose-300">
                    Following "{activeToken}"
                  </span>
                </div>

                <div className="space-y-3">
                  {candidateNextTokens.map((candidate, idx) => (
                    <div key={candidate.word} className="space-y-1">
                      <div className="flex justify-between text-xs font-mono">
                        <span className="text-white font-semibold">
                          #{idx + 1} <span className="text-cyan-300">"{candidate.word}"</span>
                        </span>
                        <span className="text-rose-300 font-bold">{candidate.percentage}%</span>
                      </div>
                      <div className="h-2.5 w-full bg-slate-900 rounded-full overflow-hidden border border-slate-800">
                        <div
                          className="h-full bg-gradient-to-r from-rose-500 to-pink-500 rounded-full transition-all duration-300"
                          style={{ width: `${candidate.percentage}%` }}
                        />
                      </div>
                    </div>
                  ))}
                </div>

                <div className="p-3 bg-slate-900/80 border border-slate-800 rounded-xl text-xs text-slate-400">
                  <span className="text-white font-bold">Conclusion of Journey:</span> The highest probability token (or top-p sampled candidate) is emitted to the output buffer, appended to the sequence, and looped back to Stage 1 for autoregressive generation of the following token!
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
