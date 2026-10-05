import React, { useState, useMemo } from 'react';
import { 
  Database, 
  FileText, 
  Search, 
  Layers, 
  Cpu, 
  Sparkles, 
  ArrowRight, 
  CheckCircle2, 
  Sliders, 
  Calculator, 
  RotateCcw, 
  Zap, 
  Scissors, 
  Filter, 
  MessageSquare,
  ChevronRight,
  ShieldCheck
} from 'lucide-react';
import KaTeXRenderer from './KaTeXRenderer';

// PRESET KNOWLEDGE BASES
const KNOWLEDGE_DOCS = [
  {
    id: 'flash_attention',
    title: 'FlashAttention: Fast and Memory-Efficient Exact Attention',
    source: 'Dao et al., NeurIPS 2022',
    rawText: `Standard attention in transformers has O(N^2) memory footprint because it materializes the full N x N attention matrix into slow GPU High Bandwidth Memory (HBM). FlashAttention solves this memory-bandwidth bottleneck by using IO-awareness and tiling. The input matrices Q, K, and V are loaded into ultra-fast on-chip SRAM in blocks of size B_r and B_c. FlashAttention computes attention incrementally using online softmax scaling (Milakov and Gimelshein), avoiding ever writing the full N x N matrix to HBM. In the backward pass, it recomputes attention on-the-fly rather than storing it, delivering a 2x-4x wall-clock speedup without any mathematical approximation.`
  },
  {
    id: 'lora',
    title: 'LoRA: Low-Rank Adaptation of Large Language Models',
    source: 'Hu et al., ICLR 2022',
    rawText: `Fine-tuning large language models by updating all parameters is computationally prohibitive. LoRA freezes pre-trained model weights W_0 and injects trainable rank decomposition matrices into each transformer layer. The weight update is parameterized as Delta W = B * A, where B is in R^(d x r) and A is in R^(r x k), with rank r << min(d, k). This reduces trainable parameter counts by 10,000x and GPU VRAM requirements by 3x. During inference, Delta W can be directly merged back into W_0 = W_0 + B * A, introducing exactly zero additional inference latency.`
  },
  {
    id: 'mixture_of_experts',
    title: 'Mixture of Experts & Sparse Gating Networks',
    source: 'Shazeer et al., 2017 & Mixtral 8x7B',
    rawText: `Sparse Mixture-of-Experts (MoE) replaces dense feed-forward layers with N independent expert subnetworks. A learned router or gating network computes a softmax probability distribution over all experts for each token. In Top-2 routing, only the two highest-scoring experts are activated per token, multiplying total model capacity while keeping inference FLOPs constant. Auxiliary load balancing loss is applied during pre-training to prevent expert collapse and ensure uniform workload distribution across GPU hardware clusters.`
  }
];

const PRESET_QUERIES = [
  {
    text: 'How does FlashAttention avoid writing the N x N matrix to HBM?',
    docId: 'flash_attention'
  },
  {
    text: 'What rank parameter r does LoRA use and how does it achieve zero inference latency?',
    docId: 'lora'
  },
  {
    text: 'Why is auxiliary load balancing loss required in Mixture of Experts?',
    docId: 'mixture_of_experts'
  }
];

export default function RAGPipelinePlayground() {
  const [selectedDocId, setSelectedDocId] = useState('flash_attention');
  const [queryText, setQueryText] = useState(PRESET_QUERIES[0].text);
  const [chunkSize, setChunkSize] = useState(120); // characters per chunk
  const [chunkOverlap, setChunkOverlap] = useState(25); // characters overlap
  const [topK, setTopK] = useState(2);
  const [activeStep, setActiveStep] = useState(1); // 1: Chunking, 2: Embedding, 3: Vector Search, 4: Reranking, 5: Synthesis

  const activeDoc = useMemo(() => {
    return KNOWLEDGE_DOCS.find(d => d.id === selectedDocId) || KNOWLEDGE_DOCS[0];
  }, [selectedDocId]);

  // STAGE 1: CHUNKING ENGINE
  const chunks = useMemo(() => {
    const text = activeDoc.rawText;
    const result = [];
    let start = 0;
    let chunkIndex = 1;

    while (start < text.length) {
      const end = Math.min(start + chunkSize, text.length);
      const chunkStr = text.slice(start, end).trim();
      if (chunkStr.length > 0) {
        result.push({
          id: `chunk-${chunkIndex}`,
          index: chunkIndex,
          start,
          end,
          text: chunkStr,
          tokenEstimate: Math.round(chunkStr.split(/\s+/).length * 1.3)
        });
        chunkIndex++;
      }
      if (end >= text.length) break;
      start += (chunkSize - chunkOverlap);
    }
    return result;
  }, [activeDoc, chunkSize, chunkOverlap]);

  // STAGE 2 & 3: SIMULATED DENSE EMBEDDING & COSINE SIMILARITY
  const scoredChunks = useMemo(() => {
    const qWords = queryText.toLowerCase().split(/\s+/).filter(w => w.length > 2);

    return chunks.map(chunk => {
      const chunkWords = chunk.text.toLowerCase().split(/\s+/);
      
      // Keyword overlap + semantic boost simulation
      let matchCount = 0;
      qWords.forEach(qw => {
        if (chunkWords.some(cw => cw.includes(qw) || qw.includes(cw))) {
          matchCount += 1.5;
        }
      });

      // Semantic proximity score based on document relevance
      const baseScore = activeDoc.id === selectedDocId ? 0.65 : 0.20;
      const termDensity = matchCount / (qWords.length || 1);
      const rawSim = Math.min(0.97, Math.max(0.18, baseScore + termDensity * 0.35 + (Math.sin(chunk.index * 7) * 0.05)));

      // Generate a mock 6-dimensional dense embedding snippet
      const mockVector = Array.from({ length: 6 }, (_, i) => 
        (Math.sin(chunk.index * (i + 1)) * 0.8).toFixed(3)
      );

      return {
        ...chunk,
        similarity: parseFloat(rawSim.toFixed(3)),
        embedding: mockVector,
        rerankScore: parseFloat((rawSim * 1.02 - 0.01).toFixed(3))
      };
    }).sort((a, b) => b.similarity - a.similarity);
  }, [chunks, queryText, activeDoc, selectedDocId]);

  // STAGE 4: TOP-K RETRIEVED CHUNKS
  const retrievedChunks = useMemo(() => {
    return scoredChunks.slice(0, topK);
  }, [scoredChunks, topK]);

  // STAGE 5: SYNTHESIZED ANSWER & PROMPT TOKENS
  const synthesis = useMemo(() => {
    const contextPrompt = retrievedChunks.map((c, i) => `[Source ${i + 1} (${c.id})]: "${c.text}"`).join('\n\n');
    const totalPromptTokens = Math.round((contextPrompt.length + queryText.length) / 3.8);

    let answer = '';
    if (selectedDocId === 'flash_attention') {
      answer = `Based on Dao et al. (NeurIPS 2022), FlashAttention eliminates the memory-bandwidth bottleneck by loading Q, K, and V matrices in tiled blocks directly into fast GPU SRAM. It computes exact attention incrementally via online softmax scaling without ever materializing the full N × N attention matrix in slow High Bandwidth Memory (HBM). During backpropagation, it recomputes intermediate attention on-the-fly, achieving a 2x–4x wall-clock speedup with zero approximation error.`;
    } else if (selectedDocId === 'lora') {
      answer = `According to Hu et al. (ICLR 2022), LoRA freezes the pre-trained weights W_0 and injects low-rank decomposition matrices ΔW = B × A (where rank r << min(d, k)). This reduces trainable parameters by 10,000x and GPU VRAM by 3x. Zero inference latency is achieved by directly folding the learned ΔW weights into W_0 at deployment (W_merged = W_0 + B × A).`;
    } else {
      answer = `In Mixture of Experts (MoE) architectures, sparse Top-2 gating routes tokens exclusively to the two highest-scoring expert subnetworks. An auxiliary load balancing loss (L_aux = α * N * Σ f_i * P_i) is strictly enforced during pre-training to penalize routing imbalance, preventing expert collapse and ensuring all distributed GPU hardware compute units are uniformly utilized.`;
    }

    return {
      contextPrompt,
      answer,
      tokens: totalPromptTokens,
      estCost: `$${((totalPromptTokens / 1000) * 0.0015).toFixed(5)}`
    };
  }, [retrievedChunks, queryText, selectedDocId]);

  const stages = [
    { num: 1, title: 'Document Chunking', icon: Scissors, desc: 'Splitting text into overlapping token windows' },
    { num: 2, title: 'Dense Embeddings', icon: Layers, desc: 'Projecting chunks into continuous vector space' },
    { num: 3, title: 'Vector Search', icon: Search, desc: 'Cosine similarity ranking against query vector' },
    { num: 4, title: 'Top-K & Reranking', icon: Filter, desc: 'Selecting highest scoring context passages' },
    { num: 5, title: 'Augmented Synthesis', icon: Sparkles, desc: 'Injecting grounded context into LLM prompt' }
  ];

  return (
    <div className="space-y-6 animate-fadeIn">
      {/* Top Header Card */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 shadow-sm space-y-4">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="p-1.5 rounded-lg bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                <Database className="w-4 h-4" />
              </span>
              <h2 className="text-base font-bold text-white tracking-wide">
                Interactive RAG Architecture Pipeline Visualizer
              </h2>
              <span className="text-[10px] px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 font-mono">
                5-Stage Pipeline
              </span>
            </div>
            <p className="text-xs text-slate-400 mt-1 max-w-2xl">
              Inspect the end-to-end lifecycle of Retrieval-Augmented Generation: from document chunking and dense embeddings to vector cosine similarity search and grounded LLM generation.
            </p>
          </div>

          {/* Quick Metrics */}
          <div className="flex items-center gap-3 bg-slate-950 p-2.5 px-4 rounded-xl border border-slate-800 text-xs shrink-0">
            <div>
              <span className="text-[10px] text-slate-500 block uppercase font-mono">Chunks</span>
              <span className="font-mono font-bold text-white">{chunks.length}</span>
            </div>
            <div className="w-[1px] h-6 bg-slate-800" />
            <div>
              <span className="text-[10px] text-slate-500 block uppercase font-mono">Top-K</span>
              <span className="font-mono font-bold text-indigo-400">{topK}</span>
            </div>
            <div className="w-[1px] h-6 bg-slate-800" />
            <div>
              <span className="text-[10px] text-slate-500 block uppercase font-mono">Top Sim</span>
              <span className="font-mono font-bold text-emerald-400">
                {scoredChunks[0] ? scoredChunks[0].similarity.toFixed(3) : '0.000'}
              </span>
            </div>
          </div>
        </div>

        {/* 5-Stage Step Navigation Progress Bar */}
        <div className="pt-3 border-t border-slate-800/80">
          <div className="grid grid-cols-2 sm:grid-cols-5 gap-2">
            {stages.map((st) => {
              const Icon = st.icon;
              const isActive = activeStep === st.num;
              const isPast = activeStep > st.num;

              return (
                <button
                  key={`stage-${st.num}`}
                  onClick={() => setActiveStep(st.num)}
                  className={`p-2.5 rounded-xl border text-left transition flex items-start gap-2.5 ${
                    isActive
                      ? 'bg-indigo-600/20 text-white border-indigo-500/50 shadow-md shadow-indigo-600/10'
                      : isPast
                      ? 'bg-slate-950 text-slate-300 border-slate-800 hover:border-slate-700'
                      : 'bg-slate-950/60 text-slate-500 border-slate-800/60 hover:text-slate-400'
                  }`}
                >
                  <div className={`w-6 h-6 rounded-lg flex items-center justify-center shrink-0 ${
                    isActive ? 'bg-indigo-600 text-white' : isPast ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' : 'bg-slate-800 text-slate-400'
                  }`}>
                    {isPast ? <CheckCircle2 className="w-3.5 h-3.5" /> : <Icon className="w-3.5 h-3.5" />}
                  </div>
                  <div className="truncate">
                    <span className="text-[10px] block font-mono text-slate-400 uppercase">
                      Stage {st.num}
                    </span>
                    <span className="text-xs font-semibold block truncate">
                      {st.title}
                    </span>
                  </div>
                </button>
              );
            })}
          </div>
        </div>
      </div>

      {/* Control Panel: Knowledge Document & Query Selector */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 space-y-4 shadow-sm">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Document Ingestion Selector */}
          <div className="space-y-1.5">
            <label className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">
              1. Ingest Knowledge Document:
            </label>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
              {KNOWLEDGE_DOCS.map(d => (
                <button
                  key={d.id}
                  onClick={() => {
                    setSelectedDocId(d.id);
                    const matchingPreset = PRESET_QUERIES.find(p => p.docId === d.id);
                    if (matchingPreset) setQueryText(matchingPreset.text);
                  }}
                  className={`p-2.5 rounded-xl border text-left transition ${
                    selectedDocId === d.id
                      ? 'bg-indigo-500/20 text-indigo-300 border-indigo-500/40 shadow-sm'
                      : 'bg-slate-950 text-slate-400 hover:text-white border border-slate-800'
                  }`}
                >
                  <div className="text-xs font-semibold truncate">{d.title.split(':')[0]}</div>
                  <div className="text-[10px] text-slate-500 truncate mt-0.5">{d.source}</div>
                </button>
              ))}
            </div>
          </div>

          {/* User Query Input */}
          <div className="space-y-1.5">
            <label className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">
              2. User Prompt / Query Vector:
            </label>
            <div className="relative">
              <input
                type="text"
                value={queryText}
                onChange={(e) => setQueryText(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-xs sm:text-sm text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 pr-10"
                placeholder="Ask any technical question to evaluate RAG retrieval..."
              />
              <Search className="w-4 h-4 text-slate-400 absolute right-3 top-3" />
            </div>
          </div>
        </div>

        {/* Hyperparameter Sliders */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-3 border-t border-slate-800/80">
          <div className="space-y-1">
            <div className="flex justify-between text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
              <span>Chunk Size:</span>
              <span className="text-indigo-400 font-mono">{chunkSize} chars</span>
            </div>
            <input
              type="range"
              min="80"
              max="240"
              step="20"
              value={chunkSize}
              onChange={(e) => setChunkSize(parseInt(e.target.value))}
              className="w-full accent-indigo-500 cursor-pointer"
            />
          </div>

          <div className="space-y-1">
            <div className="flex justify-between text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
              <span>Chunk Overlap:</span>
              <span className="text-indigo-400 font-mono">{chunkOverlap} chars</span>
            </div>
            <input
              type="range"
              min="10"
              max="50"
              step="5"
              value={chunkOverlap}
              onChange={(e) => setChunkOverlap(parseInt(e.target.value))}
              className="w-full accent-indigo-500 cursor-pointer"
            />
          </div>

          <div className="space-y-1">
            <div className="flex justify-between text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
              <span>Top-K Retrieval:</span>
              <span className="text-emerald-400 font-mono">{topK} Chunks</span>
            </div>
            <input
              type="range"
              min="1"
              max="4"
              step="1"
              value={topK}
              onChange={(e) => setTopK(parseInt(e.target.value))}
              className="w-full accent-emerald-500 cursor-pointer"
            />
          </div>
        </div>
      </div>

      {/* STAGE-SPECIFIC INTERACTIVE VISUALIZATION */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Left Side: Pipeline Work Area */}
        <div className="lg:col-span-7 space-y-4">
          {/* STAGE 1: Chunking Visualizer */}
          {activeStep === 1 && (
            <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 space-y-4 shadow-sm animate-fadeIn">
              <div className="flex items-center justify-between border-b border-slate-800/80 pb-3">
                <h3 className="text-xs font-bold text-white uppercase tracking-wider flex items-center gap-1.5">
                  <Scissors className="w-3.5 h-3.5 text-indigo-400" />
                  Stage 1: Document Sliding Window Chunking ({chunks.length} Chunks)
                </h3>
                <span className="text-[10px] text-slate-400 font-mono">Overlap: {chunkOverlap} chars</span>
              </div>

              <div className="space-y-2 max-h-[420px] overflow-y-auto pr-1">
                {chunks.map((c) => (
                  <div 
                    key={c.id}
                    className="p-3 bg-slate-950 rounded-xl border border-slate-800 text-xs space-y-1.5"
                  >
                    <div className="flex items-center justify-between text-[10px] font-mono text-slate-400">
                      <span className="px-1.5 py-0.5 rounded bg-indigo-500/20 text-indigo-300 font-bold">
                        {c.id}
                      </span>
                      <span>Chars {c.start}–{c.end} &bull; ~{c.tokenEstimate} tokens</span>
                    </div>
                    <p className="text-slate-300 leading-relaxed font-sans">
                      {c.text}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* STAGE 2: Dense Embeddings */}
          {activeStep === 2 && (
            <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 space-y-4 shadow-sm animate-fadeIn">
              <div className="flex items-center justify-between border-b border-slate-800/80 pb-3">
                <h3 className="text-xs font-bold text-white uppercase tracking-wider flex items-center gap-1.5">
                  <Layers className="w-3.5 h-3.5 text-indigo-400" />
                  Stage 2: Dense Embedding Vectors (Projection to Vector Space)
                </h3>
                <span className="text-[10px] text-slate-400 font-mono">Embedding Dim d = 1536</span>
              </div>

              <div className="space-y-3 max-h-[420px] overflow-y-auto pr-1">
                {scoredChunks.map((c) => (
                  <div key={c.id} className="p-3 bg-slate-950 rounded-xl border border-slate-800 text-xs space-y-2">
                    <div className="flex items-center justify-between text-[10px] font-mono">
                      <span className="text-indigo-400 font-bold">{c.id}</span>
                      <span className="text-slate-400">Model: text-embedding-3-small</span>
                    </div>
                    <p className="text-slate-400 text-[11px] truncate">
                      "{c.text}"
                    </p>
                    {/* Visual Vector Array */}
                    <div className="p-2 bg-slate-900 rounded-lg border border-slate-800/80 font-mono text-[11px] text-cyan-300 flex items-center gap-2 overflow-x-auto">
                      <span className="text-slate-500">E({c.id}) = [</span>
                      {c.embedding.map((val, i) => (
                        <span key={i} className="px-1.5 py-0.5 rounded bg-slate-800 text-indigo-200">
                          {val}
                        </span>
                      ))}
                      <span className="text-slate-500">... +1530 dims]</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* STAGE 3 & 4: Vector Similarity Search & Reranking */}
          {(activeStep === 3 || activeStep === 4) && (
            <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 space-y-4 shadow-sm animate-fadeIn">
              <div className="flex items-center justify-between border-b border-slate-800/80 pb-3">
                <h3 className="text-xs font-bold text-white uppercase tracking-wider flex items-center gap-1.5">
                  <Filter className="w-3.5 h-3.5 text-indigo-400" />
                  {activeStep === 3 ? 'Stage 3: Vector Database Cosine Search' : 'Stage 4: Top-K Context Selection & Reranking'}
                </h3>
                <span className="text-[10px] text-emerald-400 font-mono">Top {topK} Injected</span>
              </div>

              <div className="space-y-2.5 max-h-[420px] overflow-y-auto pr-1">
                {scoredChunks.map((c, idx) => {
                  const isRetrieved = idx < topK;

                  return (
                    <div
                      key={c.id}
                      className={`p-3.5 rounded-xl border transition space-y-2 ${
                        isRetrieved
                          ? 'bg-indigo-500/10 border-indigo-500/40 text-white shadow-sm'
                          : 'bg-slate-950/60 border-slate-800/60 text-slate-400 opacity-60'
                      }`}
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <span className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold ${
                            isRetrieved ? 'bg-indigo-600 text-white' : 'bg-slate-800 text-slate-400'
                          }`}>
                            Rank #{idx + 1}
                          </span>
                          <span className="text-xs font-semibold font-mono">{c.id}</span>
                          {isRetrieved && (
                            <span className="text-[10px] px-2 py-0.2 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 flex items-center gap-1 font-mono">
                              <CheckCircle2 className="w-3 h-3" />
                              Retrieved
                            </span>
                          )}
                        </div>

                        <div className="flex items-center gap-2">
                          <div className="w-20 h-2 bg-slate-800 rounded-full overflow-hidden">
                            <div 
                              className={`h-full rounded-full ${isRetrieved ? 'bg-emerald-400' : 'bg-slate-600'}`}
                              style={{ width: `${c.similarity * 100}%` }}
                            />
                          </div>
                          <span className="text-xs font-mono font-bold text-emerald-400">
                            {c.similarity.toFixed(3)}
                          </span>
                        </div>
                      </div>

                      <p className="text-xs leading-relaxed">
                        {c.text}
                      </p>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* STAGE 5: Grounded LLM Generation */}
          {activeStep === 5 && (
            <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 space-y-4 shadow-sm animate-fadeIn">
              <div className="flex items-center justify-between border-b border-slate-800/80 pb-3">
                <h3 className="text-xs font-bold text-white uppercase tracking-wider flex items-center gap-1.5">
                  <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
                  Stage 5: Grounded LLM Response with Verified Citations
                </h3>
                <span className="text-[10px] text-emerald-400 font-mono">100% Factually Grounded</span>
              </div>

              {/* Synthesized Answer Box */}
              <div className="p-4 bg-slate-950 rounded-xl border border-emerald-500/30 space-y-3 shadow-inner">
                <div className="flex items-center gap-2 text-xs font-semibold text-emerald-300">
                  <Sparkles className="w-4 h-4 text-emerald-400" />
                  <span>LLM Synthesized Answer (Zero Hallucination):</span>
                </div>
                <p className="text-xs sm:text-sm text-slate-200 leading-relaxed">
                  {synthesis.answer}
                </p>

                {/* Grounded Citation Badges */}
                <div className="pt-2 border-t border-slate-800 flex flex-wrap gap-2 text-[10px] font-mono">
                  {retrievedChunks.map((c, i) => (
                    <span 
                      key={c.id}
                      className="px-2 py-1 rounded bg-slate-900 text-indigo-300 border border-slate-800"
                    >
                      [Source {i + 1}]: {c.id} (Sim: {c.similarity.toFixed(3)})
                    </span>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Step Progression Buttons */}
          <div className="flex items-center justify-between pt-2">
            <button
              onClick={() => setActiveStep(prev => Math.max(1, prev - 1))}
              disabled={activeStep === 1}
              className="px-3.5 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 disabled:opacity-30 text-xs font-medium text-slate-300 transition"
            >
              Previous Stage
            </button>
            <button
              onClick={() => setActiveStep(prev => Math.min(5, prev + 1))}
              disabled={activeStep === 5}
              className="px-4 py-1.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 disabled:opacity-30 text-xs font-semibold text-white transition flex items-center gap-1.5 shadow-md shadow-indigo-600/25"
            >
              <span>Next Stage</span>
              <ChevronRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        {/* Right Side: Augmented Prompt Assembly & Formula Card */}
        <div className="lg:col-span-5 space-y-4">
          {/* Augmented Prompt Inspection Card */}
          <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 space-y-3 shadow-sm text-xs">
            <div className="flex items-center justify-between border-b border-slate-800/80 pb-3">
              <h4 className="font-bold text-indigo-300 uppercase tracking-wider flex items-center gap-1.5">
                <MessageSquare className="w-3.5 h-3.5 text-indigo-400" />
                Assembled Context Prompt
              </h4>
              <span className="text-[10px] font-mono text-slate-400">{synthesis.tokens} tokens</span>
            </div>

            <div className="p-3 bg-slate-950 rounded-xl border border-slate-800 font-mono text-[11px] text-slate-300 space-y-2 max-h-[220px] overflow-y-auto">
              <div className="text-slate-500 font-semibold">[SYSTEM PROMPT]</div>
              <div className="text-indigo-300">
                You are a faithful AI technical assistant. Answer the user prompt using ONLY the provided verified context passages.
              </div>
              <div className="text-slate-500 font-semibold pt-1">[RETRIEVED CONTEXT]</div>
              <div className="text-slate-300 text-[10px] leading-relaxed whitespace-pre-wrap">
                {synthesis.contextPrompt}
              </div>
              <div className="text-slate-500 font-semibold pt-1">[USER QUERY]</div>
              <div className="text-cyan-300 font-bold">
                "{queryText}"
              </div>
            </div>

            <div className="flex items-center justify-between text-[11px] text-slate-400 pt-1">
              <span>Estimated Cost (GPT-4o mini):</span>
              <span className="font-mono text-emerald-400 font-bold">{synthesis.estCost}</span>
            </div>
          </div>

          {/* Mathematical Formulations Card */}
          <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 space-y-3 shadow-sm text-xs">
            <h4 className="font-bold text-white uppercase tracking-wider flex items-center gap-1.5">
              <Calculator className="w-3.5 h-3.5 text-cyan-400" />
              Mathematical Formulations in RAG
            </h4>

            <div className="space-y-2 text-[11px] text-slate-400">
              <div className="p-2.5 bg-slate-950 rounded-xl border border-slate-800 text-center font-mono">
                <KaTeXRenderer math="\text{Cosine Sim}(\vec{q}, \vec{c}_i) = \frac{\vec{q} \cdot \vec{c}_i}{\|\vec{q}\|_2 \|\vec{c}_i\|_2}" block={true} />
              </div>
              <p className="leading-relaxed">
                Dense retrieval encodes both query <KaTeXRenderer math="\vec{q} = \text{Encoder}(Q)" inline={true} /> and chunks <KaTeXRenderer math="\vec{c} = \text{Encoder}(C)" inline={true} /> into normalized vector embeddings. Maximum inner-product search (MIPS) rapidly indexes top-<KaTeXRenderer math="K" inline={true} /> nearest neighbors in sub-millisecond latency.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
