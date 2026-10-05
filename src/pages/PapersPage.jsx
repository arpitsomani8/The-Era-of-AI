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
  Award,
  Bookmark,
  CheckCircle2,
  Quote,
  Check
} from 'lucide-react';
import papersData from '../data/papers.json';
import KaTeXRenderer from '../components/KaTeXRenderer';
import { useProgress } from '../context/ProgressContext';

export default function PapersPage() {
  const { toggleCompleted, isCompleted, toggleBookmark, isBookmarked } = useProgress();
  const [searchParams] = useSearchParams();
  const initialSearch = searchParams.get('search') || '';
  const [searchQuery, setSearchQuery] = useState(initialSearch);
  const [activeCategory, setActiveCategory] = useState('all');
  const [statusFilter, setStatusFilter] = useState('all'); // 'all', 'bookmarked', 'read'
  const [copiedBibId, setCopiedBibId] = useState(null);

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

  const readCount = useMemo(() => {
    return papersData.filter((p) => isCompleted(`paper-${p.id}`)).length;
  }, [isCompleted]);

  const readPercentage = Math.round((readCount / papersData.length) * 100);

  const handleCopyBibtex = (paper) => {
    const bibtexKey = paper.title.split(' ')[0].toLowerCase() + paper.year;
    const bibtex = `@article{${bibtexKey},
  title={${paper.title}},
  author={${paper.authors}},
  year={${paper.year}},
  institution={${paper.institution || 'Research Lab'}},
  url={${paper.url || ''}}
}`;
    navigator.clipboard.writeText(bibtex);
    setCopiedBibId(paper.id);
    setTimeout(() => setCopiedBibId(null), 2000);
  };

  const filteredPapers = useMemo(() => {
    return papersData.filter((paper) => {
      const pKey = `paper-${paper.id}`;
      const isDone = isCompleted(pKey);
      const isSaved = isBookmarked(pKey);

      if (statusFilter === 'bookmarked' && !isSaved) return false;
      if (statusFilter === 'read' && !isDone) return false;
      if (statusFilter === 'unread' && isDone) return false;

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
  }, [activeCategory, searchQuery, statusFilter, isCompleted, isBookmarked]);

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
              22 milestone papers that defined modern artificial intelligence. Complete with historical legacy, mathematical formulations, breakthrough innovations, one-click BibTeX citations, and direct arXiv access.
            </p>
          </div>
        </div>

        {/* Papers Reading Progress Banner */}
        <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-4 sm:p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-4 shadow-sm">
          <div className="flex items-center gap-3.5">
            <div className="w-10 h-10 rounded-xl bg-amber-500/10 text-amber-400 border border-amber-500/30 flex items-center justify-center shrink-0">
              <CheckCircle2 className="w-5 h-5" />
            </div>
            <div>
              <div className="text-sm font-bold text-white flex items-center gap-2.5">
                <span>Research Literature Progress</span>
                <span className="text-amber-300 font-mono text-xs bg-amber-500/15 px-2.5 py-0.5 rounded-full border border-amber-500/30">
                  {readCount} / {papersData.length} Papers Read ({readPercentage}%)
                </span>
              </div>
              <p className="text-xs text-slate-400 mt-0.5">
                Track papers you've digested, copy academic citations, and bookmark foundational milestones.
              </p>
            </div>
          </div>
          <div className="w-full sm:w-56 flex flex-col gap-1.5 shrink-0">
            <div className="flex justify-between text-[11px] text-slate-400 font-mono">
              <span>Literature Read</span>
              <span className="text-amber-300 font-bold">{readPercentage}%</span>
            </div>
            <div className="w-full bg-slate-800/90 rounded-full h-2.5 overflow-hidden border border-slate-700/60 p-0.5">
              <div 
                className="bg-gradient-to-r from-amber-500 via-orange-500 to-rose-400 h-full transition-all duration-500 rounded-full"
                style={{ width: `${readPercentage}%` }}
              />
            </div>
          </div>
        </div>

        {/* Search & Category Filter */}
        <div className="space-y-3">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            {/* Search Input */}
            <div className="relative flex-1 max-w-md">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search papers by title, author, breakthrough, or math..."
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

            {/* Quick Status Filter Tabs */}
            <div className="flex items-center bg-slate-900 border border-slate-800 rounded-lg p-0.5 text-xs">
              {[
                { id: 'all', label: 'All' },
                { id: 'bookmarked', label: 'Saved' },
                { id: 'read', label: 'Read' },
                { id: 'unread', label: 'To Read' },
              ].map((s) => (
                <button
                  key={s.id}
                  onClick={() => setStatusFilter(s.id)}
                  className={`px-3 py-1 rounded-md text-[11px] font-medium transition ${
                    statusFilter === s.id
                      ? 'bg-amber-600 text-white shadow-sm'
                      : 'text-slate-400 hover:text-slate-200'
                  }`}
                >
                  {s.label}
                </button>
              ))}
            </div>
          </div>

          {/* Category Tabs */}
          <div className="flex items-center overflow-x-auto no-scrollbar space-x-1.5 pb-1">
            {categories.map((cat) => (
              <button
                key={cat.id}
                onClick={() => setActiveCategory(cat.id)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition ${
                  activeCategory === cat.id
                    ? 'bg-amber-600 text-white shadow'
                    : 'bg-slate-900 text-slate-400 hover:text-white border border-slate-800'
                }`}
              >
                {cat.label}
              </button>
            ))}
          </div>
        </div>

        {/* Results Counter */}
        <div className="flex items-center justify-between text-xs text-slate-400">
          <span>Showing {filteredPapers.length} of {papersData.length} seminal papers</span>
        </div>

        {/* Papers List */}
        <div className="space-y-6">
          {filteredPapers.map((paper) => {
            const pKey = `paper-${paper.id}`;
            const isDone = isCompleted(pKey);
            const isSaved = isBookmarked(pKey);

            return (
              <article
                key={paper.id}
                id={`paper-${paper.id}`}
                className={`border rounded-2xl p-5 sm:p-6 space-y-4 shadow-sm transition ${
                  isDone 
                    ? 'bg-slate-900/95 border-emerald-500/40 ring-1 ring-emerald-500/20' 
                    : 'bg-slate-900/90 border-slate-800 hover:border-slate-700'
                }`}
              >
                {/* Paper Header */}
                <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-3">
                  <div className="space-y-1.5 flex-1 min-w-0">
                    <div className="flex items-center gap-2 flex-wrap">
                      <span className="px-2.5 py-0.5 rounded-full bg-amber-500/10 text-amber-300 border border-amber-500/30 text-[10px] font-bold uppercase tracking-wider">
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
                      {isDone && (
                        <span className="text-[10px] px-2 py-0.5 rounded-full font-semibold bg-emerald-500/15 text-emerald-300 border border-emerald-500/30 flex items-center gap-1">
                          <CheckCircle2 className="w-3 h-3 text-emerald-400" />
                          Read
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

                  {/* Actions Strip */}
                  <div className="flex items-center gap-2 shrink-0 self-start">
                    {/* Mark as Read */}
                    <button
                      onClick={() => toggleCompleted(pKey)}
                      className={`p-1.5 rounded-lg border transition ${
                        isDone 
                          ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40' 
                          : 'bg-slate-800 text-slate-400 hover:text-slate-200 border-slate-700'
                      }`}
                      title={isDone ? 'Mark as Unread' : 'Mark paper as Read'}
                    >
                      <CheckCircle2 className={`w-4 h-4 ${isDone ? 'fill-emerald-400/20 text-emerald-400' : ''}`} />
                    </button>

                    {/* Bookmark Paper */}
                    <button
                      onClick={() => toggleBookmark({
                        id: pKey,
                        type: 'paper',
                        title: paper.title,
                        subtitle: `${paper.year} • ${paper.institution || paper.authors}`,
                        link: `/papers?search=${encodeURIComponent(paper.title.slice(0, 30))}`
                      })}
                      className={`p-1.5 rounded-lg border transition ${
                        isSaved 
                          ? 'bg-amber-500/20 text-amber-300 border-amber-500/40' 
                          : 'bg-slate-800 text-slate-400 hover:text-slate-200 border-slate-700'
                      }`}
                      title={isSaved ? 'Remove Bookmark' : 'Bookmark paper'}
                    >
                      <Bookmark className={`w-4 h-4 ${isSaved ? 'fill-amber-400 text-amber-400' : ''}`} />
                    </button>

                    {/* Copy BibTeX */}
                    <button
                      onClick={() => handleCopyBibtex(paper)}
                      className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white border border-slate-700 transition"
                      title="Copy BibTeX Citation"
                    >
                      {copiedBibId === paper.id ? (
                        <Check className="w-4 h-4 text-emerald-400" />
                      ) : (
                        <Quote className="w-4 h-4" />
                      )}
                    </button>

                    {/* Read arXiv PDF */}
                    {paper.url && (
                      <a
                        href={paper.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-amber-500/10 hover:bg-amber-500/20 text-amber-300 border border-amber-500/30 text-xs font-semibold transition"
                      >
                        <span>arXiv</span>
                        <ExternalLink className="w-3.5 h-3.5" />
                      </a>
                    )}
                  </div>
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
            );
          })}
        </div>
      </div>
    </div>
  );
}
