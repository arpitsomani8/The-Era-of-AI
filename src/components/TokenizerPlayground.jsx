import React, { useState, useMemo, useRef, useEffect } from 'react';
import { 
  Binary, 
  Sparkles, 
  Play, 
  RotateCcw, 
  StepForward, 
  Compass, 
  Layers, 
  Sliders, 
  Calculator, 
  ArrowRight,
  Hash,
  Search,
  CheckCircle2
} from 'lucide-react';
import KaTeXRenderer from './KaTeXRenderer';

// PRESET TEXTS FOR BPE
const BPE_PRESETS = [
  {
    id: 'morphology',
    label: 'Morphological Roots',
    text: 'low lower lowest newer newest widest wider'
  },
  {
    id: 'ai_sentence',
    label: 'Modern AI Domain',
    text: 'Transformers revolutionize generative artificial intelligence across tokenized language models'
  },
  {
    id: 'long_words',
    label: 'Compound & Rare Words',
    text: 'unbelievable counterproductive multilingual hyperparameterization'
  },
  {
    id: 'code',
    label: 'Programming Code',
    text: 'def attention_mechanism(query, key, value): return softmax(query @ key.T)'
  }
];

// EMBEDDING WORDS FOR 2D VECTOR SPACE EXPLORATION
const EMBEDDING_VOCAB = [
  // Royalty / Gender
  { word: 'king', x: 0.65, y: 0.60, category: 'royalty' },
  { word: 'queen', x: 0.70, y: 0.25, category: 'royalty' },
  { word: 'man', x: 0.20, y: 0.62, category: 'gender' },
  { word: 'woman', x: 0.25, y: 0.27, category: 'gender' },
  { word: 'prince', x: 0.55, y: 0.70, category: 'royalty' },
  { word: 'princess', x: 0.60, y: 0.35, category: 'royalty' },

  // Geography / Capital
  { word: 'paris', x: -0.55, y: 0.65, category: 'capital' },
  { word: 'france', x: -0.60, y: 0.30, category: 'country' },
  { word: 'tokyo', x: -0.15, y: 0.70, category: 'capital' },
  { word: 'japan', x: -0.20, y: 0.35, category: 'country' },
  { word: 'london', x: -0.70, y: 0.55, category: 'capital' },
  { word: 'england', x: -0.75, y: 0.20, category: 'country' },

  // Verbs / Tenses
  { word: 'walk', x: -0.30, y: -0.45, category: 'verb' },
  { word: 'walking', x: -0.35, y: -0.75, category: 'verb_ing' },
  { word: 'swim', x: 0.15, y: -0.42, category: 'verb' },
  { word: 'swimming', x: 0.10, y: -0.72, category: 'verb_ing' },

  // Tech / AI
  { word: 'neural', x: 0.50, y: -0.30, category: 'tech' },
  { word: 'network', x: 0.58, y: -0.45, category: 'tech' },
  { word: 'tensor', x: 0.75, y: -0.35, category: 'tech' }
];

const ANALOGY_PRESETS = [
  {
    label: 'King - Man + Woman = Queen',
    pos1: 'king',
    neg: 'man',
    pos2: 'woman',
    target: 'queen',
    desc: 'Gender direction vector addition across semantic manifold.'
  },
  {
    label: 'Paris - France + Japan = Tokyo',
    pos1: 'paris',
    neg: 'france',
    pos2: 'japan',
    target: 'tokyo',
    desc: 'Capital-city relation vector projection.'
  },
  {
    label: 'Walking - Walk + Swim = Swimming',
    pos1: 'walking',
    neg: 'walk',
    pos2: 'swim',
    target: 'swimming',
    desc: 'Grammatical tense transformation vector offset.'
  }
];

export default function TokenizerPlayground() {
  const [activeSubTab, setActiveSubTab] = useState('bpe'); // 'bpe' | 'embeddings'

  // --- BPE STATE ---
  const [bpeInput, setBpeInput] = useState(BPE_PRESETS[0].text);
  const [mergeSteps, setMergeSteps] = useState([]);
  const [vocabSize, setVocabSize] = useState(30);

  // Initialize initial character split with word-boundary marker '•'
  const initialWordTokens = useMemo(() => {
    return bpeInput
      .trim()
      .split(/\s+/)
      .filter(Boolean)
      .map(word => word.split('').concat(['</w>']));
  }, [bpeInput]);

  // Compute Current Words Tokenization based on executed merge steps
  const currentTokens = useMemo(() => {
    let words = initialWordTokens.map(w => [...w]);

    for (const [t1, t2] of mergeSteps) {
      const merged = t1 + t2;
      words = words.map(w => {
        const next = [];
        let i = 0;
        while (i < w.length) {
          if (i < w.length - 1 && w[i] === t1 && w[i + 1] === t2) {
            next.push(merged);
            i += 2;
          } else {
            next.push(w[i]);
            i += 1;
          }
        }
        return next;
      });
    }

    return words;
  }, [initialWordTokens, mergeSteps]);

  // Find all candidate bigram pairs and their counts
  const bigramCounts = useMemo(() => {
    const counts = {};
    for (const w of currentTokens) {
      for (let i = 0; i < w.length - 1; i++) {
        const pair = `${w[i]}|||${w[i + 1]}`;
        counts[pair] = (counts[pair] || 0) + 1;
      }
    }

    return Object.entries(counts)
      .map(([pair, freq]) => {
        const [t1, t2] = pair.split('|||');
        return { t1, t2, pair: `${t1} + ${t2}`, freq };
      })
      .sort((a, b) => b.freq - a.freq);
  }, [currentTokens]);

  const topPair = bigramCounts[0] || null;

  // Single Merge Step
  const handleMergeStep = () => {
    if (!topPair || topPair.freq <= 1) return;
    setMergeSteps(prev => [...prev, [topPair.t1, topPair.t2]]);
  };

  // Reset BPE
  const handleResetBpe = () => {
    setMergeSteps([]);
  };

  // Run full BPE merges automatically
  const handleRunAllMerges = () => {
    let current = currentTokens;
    const newSteps = [...mergeSteps];

    for (let s = 0; s < 15; s++) {
      const counts = {};
      for (const w of current) {
        for (let i = 0; i < w.length - 1; i++) {
          const pair = `${w[i]}|||${w[i + 1]}`;
          counts[pair] = (counts[pair] || 0) + 1;
        }
      }
      const sorted = Object.entries(counts).sort((a, b) => b[1] - a[1]);
      if (sorted.length === 0 || sorted[0][1] <= 1) break;

      const [t1, t2] = sorted[0][0].split('|||');
      newSteps.push([t1, t2]);

      const merged = t1 + t2;
      current = current.map(w => {
        const next = [];
        let i = 0;
        while (i < w.length) {
          if (i < w.length - 1 && w[i] === t1 && w[i + 1] === t2) {
            next.push(merged);
            i += 2;
          } else {
            next.push(w[i]);
            i += 1;
          }
        }
        return next;
      });
    }

    setMergeSteps(newSteps);
  };

  // Flattened token list for display
  const flattenedTokens = useMemo(() => {
    const list = [];
    currentTokens.forEach((wordTokens, wIdx) => {
      wordTokens.forEach((tok, tIdx) => {
        list.push({
          id: `${wIdx}-${tIdx}`,
          token: tok,
          isEnd: tok.includes('</w>')
        });
      });
    });
    return list;
  }, [currentTokens]);

  // Tokenization metrics
  const totalCharacters = bpeInput.length;
  const totalTokenCount = flattenedTokens.length;
  const compressionRatio = totalCharacters > 0 ? (totalCharacters / totalTokenCount).toFixed(2) : 1;

  // --- EMBEDDING SPACE STATE ---
  const [selectedWord, setSelectedWord] = useState('king');
  const [activeAnalogy, setActiveAnalogy] = useState(ANALOGY_PRESETS[0]);
  const canvasRef = useRef(null);

  // Compute Cosine Similarity between word A and all other words
  const similarities = useMemo(() => {
    const base = EMBEDDING_VOCAB.find(w => w.word === selectedWord);
    if (!base) return [];

    return EMBEDDING_VOCAB
      .filter(w => w.word !== selectedWord)
      .map(w => {
        // Dot product and magnitude
        const dot = base.x * w.x + base.y * w.y;
        const mag1 = Math.sqrt(base.x * base.x + base.y * base.y);
        const mag2 = Math.sqrt(w.x * w.x + w.y * w.y);
        const sim = dot / (mag1 * mag2);
        return {
          word: w.word,
          similarity: sim,
          category: w.category
        };
      })
      .sort((a, b) => b.similarity - a.similarity);
  }, [selectedWord]);

  // Compute Analogy Result Vector (vA - vB + vC)
  const analogyVector = useMemo(() => {
    const vPos1 = EMBEDDING_VOCAB.find(w => w.word === activeAnalogy.pos1);
    const vNeg = EMBEDDING_VOCAB.find(w => w.word === activeAnalogy.neg);
    const vPos2 = EMBEDDING_VOCAB.find(w => w.word === activeAnalogy.pos2);
    if (!vPos1 || !vNeg || !vPos2) return null;

    return {
      x: vPos1.x - vNeg.x + vPos2.x,
      y: vPos1.y - vNeg.y + vPos2.y
    };
  }, [activeAnalogy]);

  // Render 2D Vector Projection Canvas
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas || activeSubTab !== 'embeddings') return;
    const ctx = canvas.getContext('2d');

    const width = (canvas.width = 460);
    const height = (canvas.height = 360);

    const toCanvasX = (val) => width / 2 + val * (width * 0.42);
    const toCanvasY = (val) => height / 2 - val * (height * 0.42);

    // Clear background
    ctx.fillStyle = '#090d16';
    ctx.fillRect(0, 0, width, height);

    // Grid lines & Axis
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.08)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(0, height / 2);
    ctx.lineTo(width, height / 2);
    ctx.moveTo(width / 2, 0);
    ctx.lineTo(width / 2, height);
    ctx.stroke();

    // Concentric coordinate rings
    [0.3, 0.6, 0.9].forEach(r => {
      ctx.beginPath();
      ctx.arc(width / 2, height / 2, r * (width * 0.42), 0, Math.PI * 2);
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.04)';
      ctx.stroke();
    });

    // Draw Vector Analogy Parallelogram & Arrows
    if (analogyVector) {
      const vA = EMBEDDING_VOCAB.find(w => w.word === activeAnalogy.pos1);
      const vB = EMBEDDING_VOCAB.find(w => w.word === activeAnalogy.neg);
      const vC = EMBEDDING_VOCAB.find(w => w.word === activeAnalogy.pos2);

      if (vA && vB && vC) {
        // Draw difference vector from B to A
        ctx.beginPath();
        ctx.moveTo(toCanvasX(vB.x), toCanvasY(vB.y));
        ctx.lineTo(toCanvasX(vA.x), toCanvasY(vA.y));
        ctx.strokeStyle = '#f59e0b';
        ctx.lineWidth = 2;
        ctx.setLineDash([4, 4]);
        ctx.stroke();
        ctx.setLineDash([]);

        // Shift difference vector to C -> Result
        ctx.beginPath();
        ctx.moveTo(toCanvasX(vC.x), toCanvasY(vC.y));
        ctx.lineTo(toCanvasX(analogyVector.x), toCanvasY(analogyVector.y));
        ctx.strokeStyle = '#38bdf8';
        ctx.lineWidth = 2;
        ctx.stroke();

        // Target Predicted Point
        ctx.beginPath();
        ctx.arc(toCanvasX(analogyVector.x), toCanvasY(analogyVector.y), 7, 0, Math.PI * 2);
        ctx.fillStyle = '#38bdf8';
        ctx.fill();
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 2;
        ctx.stroke();

        ctx.fillStyle = '#38bdf8';
        ctx.font = 'bold 10px monospace';
        ctx.fillText('Computed Vector', toCanvasX(analogyVector.x) + 10, toCanvasY(analogyVector.y) + 4);
      }
    }

    // Draw All Vocabulary Words
    EMBEDDING_VOCAB.forEach(w => {
      const cx = toCanvasX(w.x);
      const cy = toCanvasY(w.y);
      const isSelected = w.word === selectedWord;

      // Draw vector line from origin
      ctx.beginPath();
      ctx.moveTo(width / 2, height / 2);
      ctx.lineTo(cx, cy);
      ctx.strokeStyle = isSelected ? 'rgba(56, 189, 248, 0.45)' : 'rgba(255, 255, 255, 0.08)';
      ctx.lineWidth = isSelected ? 2 : 1;
      ctx.stroke();

      // Word Point Circle
      ctx.beginPath();
      ctx.arc(cx, cy, isSelected ? 6.5 : 4.5, 0, Math.PI * 2);
      ctx.fillStyle = isSelected 
        ? '#38bdf8' 
        : w.category === 'royalty' 
        ? '#ec4899' 
        : w.category === 'gender' 
        ? '#c084fc' 
        : w.category === 'capital' 
        ? '#10b981' 
        : '#f59e0b';
      ctx.fill();

      if (isSelected) {
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 2;
        ctx.stroke();
      }

      // Word Label
      ctx.font = isSelected ? 'bold 11px sans-serif' : '10px sans-serif';
      ctx.fillStyle = isSelected ? '#ffffff' : '#cbd5e1';
      ctx.fillText(w.word, cx + 8, cy + 3);
    });
  }, [activeSubTab, selectedWord, activeAnalogy, analogyVector]);

  return (
    <div className="space-y-6 animate-fadeIn">
      {/* Top Header Card */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 shadow-sm space-y-4">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="p-1.5 rounded-lg bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
                <Binary className="w-4 h-4" />
              </span>
              <h2 className="text-base font-bold text-white tracking-wide">
                BPE Tokenizer & Embedding Space Explorer
              </h2>
              <span className="text-[10px] px-2 py-0.5 rounded-full bg-cyan-500/20 text-cyan-300 border border-cyan-500/30 font-mono">
                Interactive NLP
              </span>
            </div>
            <p className="text-xs text-slate-400 mt-1 max-w-2xl">
              Inspect how modern Large Language Models compress human language into subword token vocabularies with Byte-Pair Encoding (BPE), and explore high-dimensional semantic vector arithmetic.
            </p>
          </div>

          {/* Sub-Tab Selector */}
          <div className="flex items-center bg-slate-950 border border-slate-800 rounded-xl p-1 shrink-0 self-start md:self-auto">
            <button
              onClick={() => setActiveSubTab('bpe')}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition flex items-center gap-1.5 ${
                activeSubTab === 'bpe'
                  ? 'bg-cyan-600 text-white shadow-md shadow-cyan-600/30'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              <Hash className="w-3.5 h-3.5" />
              <span>BPE Tokenizer</span>
            </button>
            <button
              onClick={() => setActiveSubTab('embeddings')}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition flex items-center gap-1.5 ${
                activeSubTab === 'embeddings'
                  ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              <Compass className="w-3.5 h-3.5" />
              <span>Vector Arithmetic (King - Man + Woman)</span>
            </button>
          </div>
        </div>
      </div>

      {/* ========================================================= */}
      {/* VIEW A: BYTE-PAIR ENCODING (BPE) INTERACTIVE TOKENIZER */}
      {/* ========================================================= */}
      {activeSubTab === 'bpe' && (
        <div className="space-y-6">
          {/* Controls & Input Panel */}
          <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 space-y-4 shadow-sm">
            <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
              {/* Presets */}
              <div className="space-y-1">
                <label className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">
                  Curated Tokenization Scenarios:
                </label>
                <div className="flex flex-wrap gap-2">
                  {BPE_PRESETS.map((p) => (
                    <button
                      key={p.id}
                      onClick={() => {
                        setBpeInput(p.text);
                        setMergeSteps([]);
                      }}
                      className={`px-3 py-1.5 rounded-lg text-xs font-medium transition ${
                        bpeInput === p.text
                          ? 'bg-cyan-600 text-white shadow-sm'
                          : 'bg-slate-950 text-slate-400 hover:text-white border border-slate-800'
                      }`}
                    >
                      {p.label}
                    </button>
                  ))}
                </div>
              </div>

              {/* Compression Stats */}
              <div className="flex items-center gap-3 bg-slate-950 p-2.5 px-4 rounded-xl border border-slate-800 text-xs shrink-0">
                <div>
                  <span className="text-[10px] text-slate-500 block uppercase font-mono">Input Length</span>
                  <span className="font-mono font-bold text-white">{totalCharacters} chars</span>
                </div>
                <div className="w-[1px] h-6 bg-slate-800" />
                <div>
                  <span className="text-[10px] text-slate-500 block uppercase font-mono">Tokens</span>
                  <span className="font-mono font-bold text-cyan-400">{totalTokenCount} tokens</span>
                </div>
                <div className="w-[1px] h-6 bg-slate-800" />
                <div>
                  <span className="text-[10px] text-slate-500 block uppercase font-mono">Compression</span>
                  <span className="font-mono font-bold text-emerald-400">{compressionRatio}x</span>
                </div>
              </div>
            </div>

            {/* Editable Text Area */}
            <div className="space-y-1 pt-2 border-t border-slate-800/80">
              <label className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">
                Input Text to Tokenize:
              </label>
              <textarea
                rows={2}
                value={bpeInput}
                onChange={(e) => {
                  setBpeInput(e.target.value);
                  setMergeSteps([]);
                }}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-xs sm:text-sm text-white focus:outline-none focus:ring-2 focus:ring-cyan-500"
                placeholder="Type or paste any sentence to observe subword tokenization..."
              />
            </div>

            {/* Merge Action Stepper Bar */}
            <div className="flex flex-wrap items-center justify-between gap-3 pt-2 border-t border-slate-800/80">
              <div className="flex items-center gap-2">
                <button
                  onClick={handleMergeStep}
                  disabled={!topPair || topPair.freq <= 1}
                  className="px-4 py-2 rounded-xl bg-cyan-600 hover:bg-cyan-500 disabled:opacity-40 text-white text-xs font-semibold shadow-md shadow-cyan-600/25 transition flex items-center gap-2"
                >
                  <StepForward className="w-3.5 h-3.5" />
                  <span>
                    Merge Next Top Bigram {topPair && topPair.freq > 1 ? `("${topPair.t1}" + "${topPair.t2}")` : '(No pairs)'}
                  </span>
                </button>

                <button
                  onClick={handleRunAllMerges}
                  disabled={!topPair || topPair.freq <= 1}
                  className="px-3.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 disabled:opacity-40 text-slate-200 text-xs font-medium border border-slate-700 transition flex items-center gap-1.5"
                >
                  <Play className="w-3.5 h-3.5 text-cyan-400" />
                  <span>Auto Merge (15 Steps)</span>
                </button>

                <button
                  onClick={handleResetBpe}
                  className="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white border border-slate-700 transition"
                  title="Reset to Initial Characters"
                >
                  <RotateCcw className="w-4 h-4" />
                </button>
              </div>

              <div className="text-[11px] font-mono text-slate-400">
                <span>{mergeSteps.length} merges executed</span>
                <span> &bull; </span>
                <span className="text-cyan-400">{bigramCounts.length} candidate pairs remaining</span>
              </div>
            </div>
          </div>

          {/* Interactive Token Grid & Bigram Ranking Table */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
            {/* Left: Live Visual Token Chips */}
            <div className="lg:col-span-8 bg-slate-900/90 border border-slate-800 rounded-2xl p-5 space-y-4 shadow-sm">
              <div className="flex items-center justify-between border-b border-slate-800/80 pb-3">
                <h3 className="text-xs font-bold text-white uppercase tracking-wider flex items-center gap-1.5">
                  <Hash className="w-3.5 h-3.5 text-cyan-400" />
                  Resulting Subword Token Sequence ({flattenedTokens.length} Tokens)
                </h3>
                <span className="text-[10px] text-slate-500 font-mono">
                  Word end = &lt;/w&gt;
                </span>
              </div>

              {/* Token Chips Canvas Grid */}
              <div className="p-4 bg-slate-950 rounded-2xl border border-slate-800 min-h-[140px] flex flex-wrap gap-2 items-center content-start">
                {currentTokens.map((wordTokens, wIdx) => (
                  <div 
                    key={`word-${wIdx}`} 
                    className="p-1.5 bg-slate-900/90 rounded-xl border border-slate-800/90 flex flex-wrap gap-1 items-center"
                  >
                    {wordTokens.map((tok, tIdx) => {
                      // Distinct color hue based on token length & merge status
                      const isMerged = tok.length > 1 && !tok.includes('</w>');
                      const cleanLabel = tok.replace('</w>', '•');

                      return (
                        <div
                          key={`tok-${wIdx}-${tIdx}`}
                          className={`px-2 py-1 rounded-lg text-xs font-mono font-medium transition-all shadow-sm flex items-center gap-1 ${
                            isMerged
                              ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 ring-1 ring-cyan-500/20'
                              : tok.includes('</w>')
                              ? 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/30'
                              : 'bg-slate-800 text-slate-300 border border-slate-700/80'
                          }`}
                          title={`Token: "${tok}" | Length: ${tok.length}`}
                        >
                          <span>{cleanLabel}</span>
                          <span className="text-[9px] text-slate-500 font-mono">
                            #{tIdx + 1}
                          </span>
                        </div>
                      );
                    })}
                  </div>
                ))}
              </div>

              {/* Educational Explanation Box */}
              <div className="p-3.5 bg-slate-950 rounded-xl border border-slate-800 text-xs text-slate-400 space-y-2">
                <div className="font-semibold text-slate-300 flex items-center gap-1.5">
                  <Calculator className="w-3.5 h-3.5 text-cyan-400" />
                  <span>How Byte-Pair Encoding (BPE) Works in GPT & LLaMA:</span>
                </div>
                <p className="text-[11px] leading-relaxed">
                  BPE (Sennrich et al., 2016) iteratively searches the training corpus for the most frequent adjacent character or subword pair:
                </p>
                <div className="py-1 text-center font-mono">
                  <KaTeXRenderer math="\text{Best Pair} = \arg\max_{(t_1, t_2)} \text{Frequency}(t_1, t_2)" block={true} />
                </div>
                <p className="text-[11px] leading-relaxed">
                  The selected pair is merged into a single new subword token. Common roots like <code className="text-cyan-300 font-mono">"low"</code> remain atomic, while rare words are broken into understandable syllables, eliminating out-of-vocabulary (OOV) tokens completely.
                </p>
              </div>
            </div>

            {/* Right: Bigram Frequency Ranking Table */}
            <div className="lg:col-span-4 bg-slate-900/90 border border-slate-800 rounded-2xl p-5 space-y-3 shadow-sm">
              <div className="flex items-center justify-between border-b border-slate-800/80 pb-3">
                <h3 className="text-xs font-bold text-white uppercase tracking-wider flex items-center gap-1.5">
                  <Layers className="w-3.5 h-3.5 text-cyan-400" />
                  Top Bigram Frequencies
                </h3>
                <span className="text-[10px] text-slate-400 font-mono">{bigramCounts.length} Pairs</span>
              </div>

              <div className="space-y-1.5 max-h-[380px] overflow-y-auto pr-1">
                {bigramCounts.length === 0 && (
                  <div className="p-4 text-center text-xs text-slate-500">
                    No adjacent pairs available to merge.
                  </div>
                )}

                {bigramCounts.slice(0, 10).map((bg, idx) => (
                  <div
                    key={`bg-${idx}`}
                    className={`p-2 rounded-xl text-xs flex items-center justify-between transition ${
                      idx === 0
                        ? 'bg-cyan-500/15 border border-cyan-500/40 text-cyan-200'
                        : 'bg-slate-950 border border-slate-800/80 text-slate-300'
                    }`}
                  >
                    <div className="flex items-center gap-2">
                      <span className="w-4 text-[10px] font-mono text-slate-500 text-center">
                        #{idx + 1}
                      </span>
                      <span className="font-mono font-medium">
                        "{bg.t1}" + "{bg.t2}"
                      </span>
                    </div>
                    <span className="px-2 py-0.5 rounded-full bg-slate-800 text-[10px] font-mono font-bold text-cyan-300">
                      {bg.freq}x
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ========================================================= */}
      {/* VIEW B: WORD EMBEDDINGS & VECTOR ARITHMETIC SANDBOX */}
      {/* ========================================================= */}
      {activeSubTab === 'embeddings' && (
        <div className="space-y-6">
          {/* Analogy Presets Bar */}
          <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 space-y-4 shadow-sm">
            <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
              <div className="space-y-1">
                <label className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">
                  Famous Vector Space Analogies:
                </label>
                <div className="flex flex-wrap gap-2">
                  {ANALOGY_PRESETS.map((a, idx) => (
                    <button
                      key={`analogy-${idx}`}
                      onClick={() => {
                        setActiveAnalogy(a);
                        setSelectedWord(a.target);
                      }}
                      className={`px-3 py-1.5 rounded-lg text-xs font-medium transition ${
                        activeAnalogy.label === a.label
                          ? 'bg-indigo-600 text-white shadow-sm'
                          : 'bg-slate-950 text-slate-400 hover:text-white border border-slate-800'
                      }`}
                    >
                      {a.label}
                    </button>
                  ))}
                </div>
              </div>

              {/* Math Formulation */}
              <div className="p-2.5 px-4 bg-slate-950 rounded-xl border border-slate-800 text-center shrink-0">
                <span className="text-[10px] text-slate-500 uppercase tracking-wider block font-mono">
                  Parallelogram Arithmetic
                </span>
                <div className="text-xs text-indigo-300 font-mono mt-0.5">
                  <KaTeXRenderer math="\vec{v}_{\text{A}} - \vec{v}_{\text{B}} + \vec{v}_{\text{C}} \approx \vec{v}_{\text{Target}}" inline={true} />
                </div>
              </div>
            </div>

            <p className="text-xs text-slate-400 pt-2 border-t border-slate-800/80">
              {activeAnalogy.desc} Word embeddings map discrete words into continuous dense vector spaces (<KaTeXRenderer math="\mathbb{R}^d" inline={true} />) where semantic and syntactic relationships correspond to spatial directional offsets.
            </p>
          </div>

          {/* Interactive 2D Vector Space Canvas + Nearest Neighbors List */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
            {/* 2D Projection Canvas */}
            <div className="lg:col-span-7 bg-slate-900/90 border border-slate-800 rounded-2xl p-5 space-y-4 shadow-sm">
              <div className="flex items-center justify-between border-b border-slate-800/80 pb-3">
                <h3 className="text-xs font-bold text-white uppercase tracking-wider flex items-center gap-1.5">
                  <Compass className="w-3.5 h-3.5 text-indigo-400" />
                  2D Semantic Vector Space (PCA Projection)
                </h3>
                <span className="text-[10px] text-slate-500 font-mono">
                  Click any word to inspect neighbors
                </span>
              </div>

              {/* Canvas Container */}
              <div className="flex justify-center p-3 bg-slate-950 rounded-2xl border border-slate-800 shadow-inner">
                <canvas
                  ref={canvasRef}
                  className="w-full max-w-[460px] aspect-[4/3] rounded-xl shadow-lg cursor-pointer"
                  onClick={(e) => {
                    const canvas = canvasRef.current;
                    if (!canvas) return;
                    const rect = canvas.getBoundingClientRect();
                    const scaleX = canvas.width / rect.width;
                    const scaleY = canvas.height / rect.height;
                    const clickX = (e.clientX - rect.left) * scaleX;
                    const clickY = (e.clientY - rect.top) * scaleY;

                    // Find nearest word point
                    let closest = null;
                    let minDist = 30;
                    EMBEDDING_VOCAB.forEach(w => {
                      const cx = canvas.width / 2 + w.x * (canvas.width * 0.42);
                      const cy = canvas.height / 2 - w.y * (canvas.height * 0.42);
                      const dist = Math.hypot(clickX - cx, clickY - cy);
                      if (dist < minDist) {
                        minDist = dist;
                        closest = w.word;
                      }
                    });
                    if (closest) setSelectedWord(closest);
                  }}
                />
              </div>

              {/* Category Dot Legend */}
              <div className="flex flex-wrap items-center justify-center gap-4 text-[11px] text-slate-400 pt-1">
                <span className="flex items-center gap-1.5">
                  <span className="w-2.5 h-2.5 rounded-full bg-pink-500" />
                  Royalty
                </span>
                <span className="flex items-center gap-1.5">
                  <span className="w-2.5 h-2.5 rounded-full bg-purple-400" />
                  Gender
                </span>
                <span className="flex items-center gap-1.5">
                  <span className="w-2.5 h-2.5 rounded-full bg-emerald-400" />
                  Geography
                </span>
                <span className="flex items-center gap-1.5">
                  <span className="w-2.5 h-2.5 rounded-full bg-amber-400" />
                  Verbs & Actions
                </span>
              </div>
            </div>

            {/* Right: Cosine Similarity Ranked Nearest Neighbors */}
            <div className="lg:col-span-5 bg-slate-900/90 border border-slate-800 rounded-2xl p-5 space-y-4 shadow-sm">
              <div className="flex items-center justify-between border-b border-slate-800/80 pb-3">
                <h3 className="text-xs font-bold text-white uppercase tracking-wider flex items-center gap-1.5">
                  <Calculator className="w-3.5 h-3.5 text-indigo-400" />
                  Nearest Semantic Neighbors to "{selectedWord}"
                </h3>
                <span className="text-[10px] text-indigo-400 font-mono">Cosine Sim</span>
              </div>

              {/* Cosine Formulation Header */}
              <div className="p-3 bg-slate-950 rounded-xl border border-slate-800 text-[11px] text-slate-400 space-y-1">
                <span className="text-[10px] font-mono text-slate-500 uppercase block">Metric Definition:</span>
                <KaTeXRenderer math="\text{Cosine Similarity}(u, v) = \frac{u \cdot v}{\|u\|_2 \|v\|_2} = \cos(\theta)" block={true} />
              </div>

              {/* Ranked Neighbor Cards */}
              <div className="space-y-2 max-h-[340px] overflow-y-auto pr-1">
                {similarities.map((item, idx) => {
                  const percent = Math.max(0, Math.round(((item.similarity + 1) / 2) * 100));
                  const isTop = idx === 0;

                  return (
                    <div
                      key={`sim-${item.word}`}
                      onClick={() => setSelectedWord(item.word)}
                      className={`p-2.5 rounded-xl border transition cursor-pointer flex items-center justify-between ${
                        isTop
                          ? 'bg-indigo-500/15 border-indigo-500/40 text-white shadow-sm'
                          : 'bg-slate-950 border-slate-800/80 text-slate-300 hover:border-slate-700'
                      }`}
                    >
                      <div className="flex items-center gap-2.5">
                        <span className="w-4 text-[10px] font-mono text-slate-500 text-center">
                          #{idx + 1}
                        </span>
                        <span className="font-semibold text-xs capitalize">
                          {item.word}
                        </span>
                        <span className="text-[9px] px-1.5 py-0.2 rounded-full bg-slate-800 text-slate-400 font-mono capitalize">
                          {item.category}
                        </span>
                      </div>

                      <div className="flex items-center gap-2">
                        <div className="w-16 h-1.5 bg-slate-800 rounded-full overflow-hidden">
                          <div 
                            className="h-full bg-indigo-500 rounded-full"
                            style={{ width: `${percent}%` }}
                          />
                        </div>
                        <span className="font-mono text-xs font-bold text-indigo-300 w-12 text-right">
                          {item.similarity.toFixed(3)}
                        </span>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
