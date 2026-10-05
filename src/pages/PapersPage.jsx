import React, { useState, useMemo } from 'react';
import { useSearchParams } from 'react-router-dom';
import { 
  FileText, 
  Search, 
  ExternalLink, 
  Sparkles, 
  Calendar, 
  Building, 
  Users, 
  AlertCircle,
  Calculator,
  Award
} from 'lucide-react';
import papersData from '../data/papers.json';
import KaTeXRenderer from '../components/KaTeXRenderer';

export default function PapersPage() {
  const [searchParams] = useSearchParams();
  const initialSearch = searchParams.get('search') || '';
  const [searchQuery, setSearchQuery] = useState(initialSearch);
  const [activeCategory, setActiveCategory] = useState('all');

  const categories = [
    { id: 'all', label: 'All Papers (22)' },
    { id: 'transformer', label: 'Transformers' },
    { id: 'llm', label: 'LLMs & Scaling' },
    { id: 'vision_dl', label: 'Vision & DL' },
    { id: 'generative', label: 'Diffusion & GANs' },
    { id: 'alignment', label: 'Alignment & RLHF' },
    { id: 'rag', label: 'RAG & Retrieval' },
    { id: 'efficient_llm', label: 'PEFT & LoRA' },
  ];

  const filteredPapers = useMemo(() => {
    return papersData.filter((paper) => {
      if (activeCategory !== 'all' && paper.category !== activeCategory) {
        return false;
      }
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase();
        const matchTitle = paper.title?.toLowerCase().includes(q);
        const matchAuthors = paper.authors?.toLowerCase().includes(q);
        const matchInst = paper.institution?.toLowerCase().includes(q);
        const matchBreak = paper.breakthrough?.toLowerCase().includes(q);
        const matchProb = paper.problem?.toLowerCase().includes(q);
        if (!matchTitle && !matchAuthors && !matchInst && !matchBreak && !matchProb) {
          return false;
        }
      }
      return true;
    });
  }, [activeCategory, searchQuery]);

  return (
    <div className="flex-1 w-full h-full overflow-y-auto bg-slate-950 text-slate-100 p-4 sm:p-6 md:p-10">
      <div className="max-w-5xl mx-auto space-y-6 pb-20">
        {/* Header */}
        <div className="border-b border-slate-800 pb-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-500/10 text-amber-300 border border-amber-500/30 text-xs font-semibold uppercase tracking-wider mb-2">
              <FileText className="w-3.5 h-3.5" />
              Landmark Research Papers
            </div>
            <h1 className="text-2xl sm:text-3xl md:text-4xl font-extrabold text-white tracking-tight">
              Seminal AI & Machine Learning Research Compendium
            </h1>
            <p className="text-xs sm:text-sm text-slate-400 mt-1 max-w-3xl">
              22 game-changing papers that defined the modern artificial intelligence era. Complete with the exact problem tackled, mathematical breakthroughs, historical legacy, and direct arXiv access.
            </p>
          </div>
        </div>

        {/* Search & Category Filter */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div className="relative flex-1 max-w-md">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search by title, author, breakthrough (e.g. Vaswani, ResNet, LoRA)..."
              className="w-full bg-slate-900 border border-slate-800 text-xs sm:text-sm text-white rounded-xl pl-9 pr-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-amber-500 placeholder-slate-500"
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

          <div className="flex items-center overflow-x-auto no-scrollbar space-x-1.5 pb-1">
            {categories.map((cat) => (
              <button
                key={cat.id}
                onClick={() => setActiveCategory(cat.id)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition ${
                  activeCategory === cat.id
                    ? 'bg-amber-600 text-white shadow-md shadow-amber-600/30'
                    : 'bg-slate-900 text-slate-400 hover:text-white border border-slate-800'
                }`}
              >
                {cat.label}
              </button>
            ))}
          </div>
        </div>

        {/* Counter */}
        <div className="text-xs text-slate-400">
          Showing {filteredPapers.length} of {papersData.length} landmark publications
        </div>

        {/* Papers Grid */}
        <div className="grid grid-cols-1 gap-6">
          {filteredPapers.map((paper) => (
            <article
              key={paper.id}
              className="bg-slate-900/90 border border-slate-800 hover:border-amber-500/40 rounded-2xl p-5 sm:p-6 shadow-md transition-all duration-200 space-y-4"
            >
              {/* Paper Top Meta */}
              <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-3">
                <div className="space-y-1">
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider bg-amber-500/10 text-amber-300 border border-amber-500/30">
                      {paper.category}
                    </span>
                    <span className="flex items-center gap-1 text-xs text-slate-400">
                      <Calendar className="w-3.5 h-3.5" />
                      {paper.year}
                    </span>
                    {paper.institution && (
                      <span className="flex items-center gap-1 text-xs text-slate-400">
                        <Building className="w-3.5 h-3.5" />
                        {paper.institution}
                      </span>
                    )}
                  </div>
                  <h2 className="text-lg sm:text-xl font-bold text-white tracking-tight leading-snug">
                    {paper.title}
                  </h2>
                  <p className="text-xs text-slate-400 flex items-center gap-1.5">
                    <Users className="w-3.5 h-3.5 text-slate-500 shrink-0" />
                    {paper.authors}
                  </p>
                </div>

                {paper.url && (
                  <a
                    href={paper.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-amber-500/10 hover:bg-amber-500/20 text-amber-300 border border-amber-500/30 text-xs font-semibold transition shrink-0 self-start"
                  >
                    <span>Read arXiv PDF</span>
                    <ExternalLink className="w-3.5 h-3.5" />
                  </a>
                )}
              </div>

              {/* One Liner Summary */}
              {paper.one_liner && (
                <p className="text-xs sm:text-sm font-medium text-amber-200/90 italic bg-amber-950/20 p-3 rounded-xl border border-amber-500/20">
                  &ldquo;{paper.one_liner}&rdquo;
                </p>
              )}

              {/* Problem vs Breakthrough Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs sm:text-sm">
                {paper.problem && (
                  <div className="bg-slate-950/60 p-4 rounded-xl border border-slate-800/80">
                    <h3 className="text-xs font-bold text-red-400 uppercase tracking-wider mb-1.5 flex items-center gap-1.5">
                      <AlertCircle className="w-3.5 h-3.5 text-red-400" />
                      The Problem & Bottleneck
                    </h3>
                    <p className="text-slate-300 leading-relaxed">{paper.problem}</p>
                  </div>
                )}

                {paper.breakthrough && (
                  <div className="bg-slate-950/60 p-4 rounded-xl border border-slate-800/80">
                    <h3 className="text-xs font-bold text-emerald-400 uppercase tracking-wider mb-1.5 flex items-center gap-1.5">
                      <Sparkles className="w-3.5 h-3.5 text-emerald-400" />
                      Core Breakthrough Innovation
                    </h3>
                    <p className="text-slate-300 leading-relaxed">{paper.breakthrough}</p>
                  </div>
                )}
              </div>

              {/* Mathematical Formula */}
              {paper.formula && (
                <div className="bg-slate-950/80 p-4 rounded-xl border border-amber-500/20">
                  <h3 className="text-xs font-bold text-amber-300 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                    <Calculator className="w-3.5 h-3.5 text-amber-400" />
                    Key Mathematical Equation
                  </h3>
                  <div className="p-3 bg-slate-900/90 rounded-lg border border-slate-800 overflow-x-auto">
                    <KaTeXRenderer math={paper.formula} block={true} />
                  </div>
                </div>
              )}

              {/* Impact / Legacy */}
              {paper.impact && (
                <div className="p-3.5 rounded-xl bg-slate-950/40 border border-slate-800/60 flex items-start gap-2.5 text-xs">
                  <Award className="w-4 h-4 text-indigo-400 shrink-0 mt-0.5" />
                  <div>
                    <span className="font-semibold text-slate-300 uppercase tracking-wider text-[11px] block">
                      Historical Legacy & Industry Impact:
                    </span>
                    <p className="text-slate-400 mt-0.5 leading-relaxed">{paper.impact}</p>
                  </div>
                </div>
              )}
            </article>
          ))}
        </div>
      </div>
    </div>
  );
}
