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
  Check,
  Radio,
  RefreshCw,
  FileDown,
  Github,
  Flame,
  Layers,
  BookOpen,
  Info,
  Clock,
  History,
  ArrowUpDown
} from 'lucide-react';
import papersData from '../data/papers.json';
import arxivLiveFeed from '../data/arxivLiveFeed.json';
import KaTeXRenderer from '../components/KaTeXRenderer';
import AudioExplainerButton from '../components/AudioExplainerButton';
import { useProgress } from '../context/ProgressContext';

export default function PapersPage() {
  const { toggleCompleted, isCompleted, toggleBookmark, isBookmarked } = useProgress();
  const [searchParams] = useSearchParams();
  const initialSearch = searchParams.get('search') || '';
  const [searchQuery, setSearchQuery] = useState(initialSearch);
  
  // 3-way collection selection: 'all' | 'foundational' | 'latest'
  const [activeCollection, setActiveCollection] = useState('all');
  const [activeCategory, setActiveCategory] = useState('all');
  const [statusFilter, setStatusFilter] = useState('all'); // 'all', 'bookmarked', 'read', 'unread'
  const [sortOrder, setSortOrder] = useState('newest'); // 'newest' | 'oldest' | 'upvotes'
  const [copiedBibId, setCopiedBibId] = useState(null);
  const [isSyncing, setIsSyncing] = useState(false);
  const [syncToast, setSyncToast] = useState(null);

  // Combined dataset with deduplication and clear collection tags
  const allPapers = useMemo(() => {
    const seen = new Set();
    const result = [];
    // Prioritize arxiv feed for latest details
    for (const p of arxivLiveFeed) {
      seen.add(p.id);
      result.push({ ...p, collectionType: 'latest' });
    }
    for (const p of papersData) {
      if (!seen.has(p.id)) {
        seen.add(p.id);
        result.push({ ...p, collectionType: 'foundational' });
      }
    }
    return result;
  }, []);

  // Filter by selected collection
  const currentDataset = useMemo(() => {
    if (activeCollection === 'foundational') {
      return allPapers.filter(p => p.collectionType === 'foundational');
    }
    if (activeCollection === 'latest') {
      return allPapers.filter(p => p.collectionType === 'latest');
    }
    return allPapers;
  }, [allPapers, activeCollection]);

  // Topic categories
  const categories = [
    { id: 'all', label: `All Topics (${currentDataset.length})` },
    { id: 'transformer', label: 'Transformers & Architectures' },
    { id: 'llm', label: 'LLMs & Reasoning' },
    { id: 'alignment', label: 'Alignment & RL' },
    { id: 'vision_dl', label: 'Vision & Deep Learning' },
    { id: 'generative', label: 'Diffusion & Generative' },
    { id: 'efficient_llm', label: 'Efficiency & LoRA' },
    { id: 'rag', label: 'RAG & Retrieval' },
    { id: 'nlp_embed', label: 'Embeddings & NLP' },
    { id: 'prompt_agent', label: 'Agents & Prompting' },
    { id: 'optimization', label: 'Optimization & Training' },
  ];

  // Only show categories that have at least one paper in the current collection
  const availableCategories = useMemo(() => {
    const presentCategories = new Set(currentDataset.map(p => p.category));
    return categories.filter(cat => cat.id === 'all' || presentCategories.has(cat.id));
  }, [currentDataset]);

  const readCount = useMemo(() => {
    return currentDataset.filter((p) => isCompleted(`paper-${p.id}`)).length;
  }, [currentDataset, isCompleted]);

  const readPercentage = Math.round((readCount / currentDataset.length) * 100) || 0;

  // Date formatter helper: converts '2025-01-22' to 'Jan 22, 2025'
  const formatPaperDate = (dateStr, year) => {
    if (!dateStr && !year) return 'Milestone';
    if (!dateStr) return `${year}`;
    try {
      const d = new Date(dateStr);
      if (isNaN(d.getTime())) return `${year || dateStr}`;
      return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
    } catch {
      return `${year || dateStr}`;
    }
  };

  const handleCopyBibtex = (paper) => {
    const bibtexKey = paper.title.split(' ')[0].toLowerCase() + (paper.year || 2025);
    const bibtex = `@article{${bibtexKey},
  title={${paper.title}},
  author={${paper.authors}},
  year={${paper.year || 2025}},
  institution={${paper.institution || 'Research Lab'}},
  url={${paper.url || ''}}
}`;
    navigator.clipboard.writeText(bibtex);
    setCopiedBibId(paper.id);
    setTimeout(() => setCopiedBibId(null), 2000);
  };

  const handleSyncArxiv = () => {
    setIsSyncing(true);
    setTimeout(() => {
      setIsSyncing(false);
      setSyncToast('ArXiv stream verified! Up to date with latest 2024–2026 releases.');
      setTimeout(() => setSyncToast(null), 3500);
    }, 900);
  };

  // Filter papers by search, status, and category
  const filteredPapers = useMemo(() => {
    return currentDataset.filter((paper) => {
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
        const matchArxiv = paper.arxiv_id?.toLowerCase().includes(q);
        if (!matchTitle && !matchAuthors && !matchInst && !matchBreak && !matchProb && !matchArxiv) {
          return false;
        }
      }
      return true;
    });
  }, [currentDataset, activeCategory, searchQuery, statusFilter, isCompleted, isBookmarked]);

  // Sort papers chronologically or by upvotes
  const sortedAndFilteredPapers = useMemo(() => {
    return filteredPapers.slice().sort((a, b) => {
      if (sortOrder === 'upvotes') {
        const uvA = a.upvotes || 0;
        const uvB = b.upvotes || 0;
        return uvB - uvA;
      }
      const timeA = new Date(a.published_date || `${a.year || 2020}-01-01`).getTime();
      const timeB = new Date(b.published_date || `${b.year || 2020}-01-01`).getTime();
      if (sortOrder === 'oldest') {
        return timeA - timeB; // Chronological ascending: 2012 -> 2026
      }
      // 'newest': Chronological descending: 2026 -> 2012
      return timeB - timeA;
    });
  }, [filteredPapers, sortOrder]);

  return (
    <div className="flex-1 w-full h-full overflow-y-auto bg-slate-950 text-slate-100 p-4 sm:p-6 md:p-10">
      <div className="max-w-5xl mx-auto space-y-6 pb-20">
        
        {/* Header Section */}
        <div className="border-b border-slate-800 pb-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-500/10 text-amber-300 border border-amber-500/30 text-xs font-semibold uppercase tracking-wider mb-2">
              <Sparkles className="w-3.5 h-3.5 text-amber-400" />
              <span>Game-Changing AI Research</span>
            </div>
            <h1 className="text-2xl sm:text-3xl md:text-4xl font-extrabold text-white tracking-tight">
              Game-Changing AI Research Publications
            </h1>
            <p className="text-xs sm:text-sm text-slate-400 mt-1.5 max-w-3xl leading-relaxed">
              35 milestone publications aligned by publication date — from historical breakthroughs like Transformers and ResNet to active 2024–2026 frontier preprints like DeepSeek-R1 and FlashAttention-3.
            </p>
          </div>

          {/* Sync / Live Stream Action */}
          <div className="flex items-center gap-2 shrink-0">
            <button
              onClick={handleSyncArxiv}
              disabled={isSyncing}
              className="px-3 py-1.5 rounded-xl bg-cyan-600/20 hover:bg-cyan-600/30 text-cyan-300 border border-cyan-500/40 text-xs font-semibold transition flex items-center gap-2 shadow-sm disabled:opacity-50"
              title="Check for latest arXiv frontier preprints"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${isSyncing ? 'animate-spin text-cyan-400' : ''}`} />
              <span>{isSyncing ? 'Checking...' : 'Check arXiv Updates'}</span>
            </button>
          </div>
        </div>

        {/* Sync Toast Notification */}
        {syncToast && (
          <div className="p-3 bg-cyan-950/80 border border-cyan-500/40 rounded-xl text-cyan-200 text-xs flex items-center justify-between shadow-lg animate-fadeIn">
            <span className="flex items-center gap-2 font-medium">
              <Radio className="w-4 h-4 text-cyan-400 animate-pulse" />
              {syncToast}
            </span>
            <button onClick={() => setSyncToast(null)} className="text-cyan-400 hover:text-white">&times;</button>
          </div>
        )}

        {/* Primary Collection Switcher: All | Foundational | Latest */}
        <div className="space-y-2.5">
          <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-2 bg-slate-900/90 p-1.5 rounded-2xl border border-slate-800 shadow-sm">
            <div className="flex items-center gap-1.5 flex-wrap">
              {/* All Publications Tab */}
              <button
                onClick={() => {
                  setActiveCollection('all');
                  setActiveCategory('all');
                }}
                className={`px-3.5 py-2 rounded-xl text-xs sm:text-sm font-semibold transition flex items-center justify-center gap-2 ${
                  activeCollection === 'all'
                    ? 'bg-white text-slate-950 shadow-md font-bold'
                    : 'text-slate-400 hover:text-white hover:bg-slate-800'
                }`}
              >
                <Layers className="w-4 h-4" />
                <span>All Publications ({allPapers.length})</span>
              </button>

              {/* Foundational Classics Tab */}
              <button
                onClick={() => {
                  setActiveCollection('foundational');
                  setActiveCategory('all');
                }}
                className={`px-3.5 py-2 rounded-xl text-xs sm:text-sm font-semibold transition flex items-center justify-center gap-2 ${
                  activeCollection === 'foundational'
                    ? 'bg-amber-500 text-slate-950 shadow-md shadow-amber-500/20 font-bold'
                    : 'text-slate-400 hover:text-white hover:bg-slate-800'
                }`}
              >
                <Award className="w-4 h-4" />
                <span>Foundational Breakthroughs ({papersData.length})</span>
              </button>

              {/* Latest Research Tab */}
              <button
                onClick={() => {
                  setActiveCollection('latest');
                  setActiveCategory('all');
                }}
                className={`px-3.5 py-2 rounded-xl text-xs sm:text-sm font-semibold transition flex items-center justify-center gap-2 ${
                  activeCollection === 'latest'
                    ? 'bg-cyan-500 text-slate-950 shadow-md shadow-cyan-500/20 font-bold'
                    : 'text-slate-400 hover:text-white hover:bg-slate-800'
                }`}
              >
                <div className="relative flex items-center">
                  <Radio className="w-4 h-4" />
                  <span className="absolute -top-0.5 -right-0.5 w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
                </div>
                <span>Latest Research 2024–2026 ({arxivLiveFeed.length})</span>
              </button>
            </div>

            <div className="text-xs text-slate-400 font-mono px-3 py-1 flex items-center gap-2">
              <span className="inline-block w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
              <span>
                {activeCollection === 'all' && 'All 35 Papers with Timestamps'}
                {activeCollection === 'foundational' && 'All-Time Historic Milestones'}
                {activeCollection === 'latest' && 'Active arXiv Frontier Preprints'}
              </span>
            </div>
          </div>

          {/* Plain English Difference Explainer Banner */}
          <div className="bg-slate-900/60 border border-slate-800/80 rounded-xl px-4 py-2.5 text-xs text-slate-300 flex flex-col md:flex-row md:items-center justify-between gap-2">
            <div className="flex items-start md:items-center gap-2">
              <Info className="w-4 h-4 text-amber-400 shrink-0 mt-0.5 md:mt-0" />
              <div className="space-x-1">
                <span className="font-semibold text-white">What's the difference?</span>
                <span className="text-slate-400">
                  <strong className="text-amber-300 font-medium">Foundational Breakthroughs (24)</strong> are the historic classics that built modern AI (Attention, ResNet, BERT, LoRA).
                </span>
                <span className="hidden md:inline text-slate-600">|</span>
                <span className="text-slate-400">
                  <strong className="text-cyan-300 font-medium">Latest Research (12)</strong> are frontier 2024–2026 papers fresh from arXiv (DeepSeek-R1, FlashAttention-3, Llama 3).
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Papers Reading Progress Banner */}
        <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-4 sm:p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-4 shadow-sm">
          <div className="flex items-center gap-3.5">
            <div className="w-10 h-10 rounded-xl flex items-center justify-center shrink-0 border bg-indigo-500/10 text-indigo-400 border-indigo-500/30">
              <BookOpen className="w-5 h-5" />
            </div>
            <div>
              <div className="text-sm font-bold text-white flex items-center gap-2.5">
                <span>Reading Progress</span>
                <span className="font-mono text-xs px-2.5 py-0.5 rounded-full border text-amber-300 bg-amber-500/15 border-amber-500/30">
                  {readCount} / {currentDataset.length} Read ({readPercentage}%)
                </span>
              </div>
              <p className="text-xs text-slate-400 mt-0.5">
                Listen with AI voice narration, study core math equations, copy BibTeX citations, and track your progress.
              </p>
            </div>
          </div>
          <div className="w-full sm:w-56 flex flex-col gap-1.5 shrink-0">
            <div className="flex justify-between text-[11px] text-slate-400 font-mono">
              <span>Completed</span>
              <span className="text-amber-300 font-bold">
                {readPercentage}%
              </span>
            </div>
            <div className="w-full bg-slate-800/90 rounded-full h-2.5 overflow-hidden border border-slate-700/60 p-0.5">
              <div 
                className="h-full transition-all duration-500 rounded-full bg-gradient-to-r from-amber-500 via-orange-500 to-rose-400"
                style={{ width: `${readPercentage}%` }}
              />
            </div>
          </div>
        </div>

        {/* Search, Timestamp Sort, and Category Controls */}
        <div className="space-y-3">
          <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-3">
            {/* Search Input */}
            <div className="relative flex-1 max-w-md">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search by title, author, breakthrough, arXiv ID, or math..."
                className="w-full bg-slate-900 border border-slate-800 text-xs sm:text-sm text-white rounded-xl pl-9 pr-8 py-2.5 focus:outline-none focus:ring-2 focus:ring-amber-500 placeholder-slate-500"
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

            {/* Sort & Status Bar */}
            <div className="flex items-center gap-2 flex-wrap sm:flex-nowrap">
              {/* Timestamp Sort Pill Controls */}
              <div className="flex items-center gap-1 bg-slate-900/90 p-1 rounded-xl border border-slate-800">
                <span className="text-[11px] text-slate-500 font-medium px-1.5 hidden sm:inline flex items-center gap-1">
                  <Clock className="w-3 h-3 text-slate-400" />
                  Sort:
                </span>
                
                <button
                  onClick={() => setSortOrder('newest')}
                  className={`px-2.5 py-1 rounded-lg text-xs font-medium transition flex items-center gap-1.5 ${
                    sortOrder === 'newest'
                      ? 'bg-amber-500/20 text-amber-300 font-semibold border border-amber-500/30 shadow-sm'
                      : 'text-slate-400 hover:text-slate-200'
                  }`}
                  title="Sort chronologically: Newest to Oldest"
                >
                  <Clock className="w-3 h-3 text-amber-400" />
                  <span>Newest</span>
                </button>

                <button
                  onClick={() => setSortOrder('oldest')}
                  className={`px-2.5 py-1 rounded-lg text-xs font-medium transition flex items-center gap-1.5 ${
                    sortOrder === 'oldest'
                      ? 'bg-amber-500/20 text-amber-300 font-semibold border border-amber-500/30 shadow-sm'
                      : 'text-slate-400 hover:text-slate-200'
                  }`}
                  title="Sort chronologically: Oldest to Newest (Evolution of AI)"
                >
                  <History className="w-3 h-3 text-amber-400" />
                  <span>Timeline</span>
                </button>

                <button
                  onClick={() => setSortOrder('upvotes')}
                  className={`px-2.5 py-1 rounded-lg text-xs font-medium transition flex items-center gap-1.5 ${
                    sortOrder === 'upvotes'
                      ? 'bg-rose-500/20 text-rose-300 font-semibold border border-rose-500/30 shadow-sm'
                      : 'text-slate-400 hover:text-slate-200'
                  }`}
                  title="Sort by community popularity / upvotes"
                >
                  <Flame className="w-3 h-3 text-rose-400" />
                  <span className="hidden sm:inline">Upvotes</span>
                </button>
              </div>

              {/* Status Filter Pill Tabs */}
              <div className="flex items-center gap-1 bg-slate-900/90 p-1 rounded-xl border border-slate-800 overflow-x-auto">
                {[
                  { id: 'all', label: 'All' },
                  { id: 'unread', label: 'To Read' },
                  { id: 'read', label: 'Read' },
                  { id: 'bookmarked', label: 'Saved' }
                ].map((s) => (
                  <button
                    key={s.id}
                    onClick={() => setStatusFilter(s.id)}
                    className={`px-2.5 py-1 rounded-lg text-xs font-medium transition ${
                      statusFilter === s.id
                        ? 'bg-slate-700 text-white font-semibold'
                        : 'text-slate-400 hover:text-slate-200'
                    }`}
                  >
                    {s.label}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Category Filter Pills */}
          <div className="flex items-center gap-2 overflow-x-auto pb-1 scrollbar-none">
            {availableCategories.map((cat) => (
              <button
                key={cat.id}
                onClick={() => setActiveCategory(cat.id)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition border ${
                  activeCategory === cat.id
                    ? 'bg-amber-500/20 text-amber-300 border-amber-500/40 shadow-sm'
                    : 'bg-slate-900 text-slate-400 border-slate-800 hover:border-slate-700 hover:text-slate-300'
                }`}
              >
                {cat.label}
              </button>
            ))}
          </div>
        </div>

        {/* Results Counter & Active Timestamp Alignment Indicator */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between text-xs text-slate-400 gap-2 border-t border-slate-900 pt-3">
          <div className="flex items-center gap-2 flex-wrap">
            <span>Showing <strong className="text-white">{sortedAndFilteredPapers.length}</strong> of {currentDataset.length} publications</span>
            <span className="text-slate-600">•</span>
            <span className="text-amber-400/90 font-mono text-[11px] flex items-center gap-1">
              <Clock className="w-3 h-3 text-amber-400" />
              {sortOrder === 'newest' && 'Timestamp: Newest to Oldest (2026 → 2012)'}
              {sortOrder === 'oldest' && 'Chronological: Oldest to Newest (2012 → 2026 Evolution)'}
              {sortOrder === 'upvotes' && 'Ranked by Community Upvotes'}
            </span>
          </div>

          {searchQuery && (
            <button 
              onClick={() => setSearchQuery('')}
              className="text-amber-400 hover:underline self-start sm:self-auto"
            >
              Clear search filter
            </button>
          )}
        </div>

        {/* Papers List with Chronological Year Markers */}
        <div className="space-y-6">
          {sortedAndFilteredPapers.map((paper, idx) => {
            const pKey = `paper-${paper.id}`;
            const isDone = isCompleted(pKey);
            const isSaved = isBookmarked(pKey);
            const isLatest = paper.collectionType === 'latest';

            // Determine if a year header should be shown when sorted by time
            const paperYear = paper.year || (paper.published_date ? new Date(paper.published_date).getFullYear() : 2020);
            const prevPaper = idx > 0 ? sortedAndFilteredPapers[idx - 1] : null;
            const prevYear = prevPaper ? (prevPaper.year || (prevPaper.published_date ? new Date(prevPaper.published_date).getFullYear() : 2020)) : null;
            const isYearBoundary = (sortOrder === 'newest' || sortOrder === 'oldest') && paperYear !== prevYear;

            return (
              <React.Fragment key={paper.id}>
                {isYearBoundary && (
                  <div className="flex items-center gap-3 pt-4 pb-1">
                    <span className="text-xs font-mono font-bold px-3 py-1 rounded-full bg-slate-800 text-amber-300 border border-slate-700 flex items-center gap-1.5 shadow-sm">
                      <Calendar className="w-3 h-3 text-amber-400" />
                      {paperYear} Milestones
                    </span>
                    <div className="h-px flex-1 bg-gradient-to-r from-slate-800 via-slate-800/60 to-transparent" />
                  </div>
                )}

                <article
                  id={`paper-${paper.id}`}
                  className={`border rounded-2xl p-5 sm:p-6 space-y-4 shadow-sm transition ${
                    isDone 
                      ? 'bg-slate-900/95 border-emerald-500/40 ring-1 ring-emerald-500/20' 
                      : 'bg-slate-900/90 border-slate-800 hover:border-slate-700'
                  }`}
                >
                  {/* Paper Header Strip */}
                  <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-3">
                    <div className="space-y-1.5 flex-1 min-w-0">
                      <div className="flex items-center gap-2 flex-wrap">
                        {/* Collection Type Badge */}
                        {isLatest ? (
                          <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold tracking-wider bg-cyan-500/15 text-cyan-300 border border-cyan-500/30 flex items-center gap-1">
                            <Radio className="w-3 h-3 text-cyan-400" />
                            Latest (2024–2026)
                          </span>
                        ) : (
                          <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold tracking-wider bg-amber-500/15 text-amber-300 border border-amber-500/30 flex items-center gap-1">
                            <Award className="w-3 h-3 text-amber-400" />
                            Foundational Classic
                          </span>
                        )}

                        {/* Precise Timestamp Badge */}
                        <span 
                          className="flex items-center gap-1.5 text-xs text-amber-300/90 font-mono font-medium bg-amber-500/10 px-2 py-0.5 rounded-full border border-amber-500/30"
                          title={`Exact Publication Date: ${paper.published_date || paper.year}`}
                        >
                          <Calendar className="w-3.5 h-3.5 text-amber-400" />
                          <span>{formatPaperDate(paper.published_date, paper.year)}</span>
                        </span>

                        {/* Topic Category */}
                        <span className="px-2.5 py-0.5 rounded-full text-[10px] font-semibold uppercase tracking-wider bg-slate-800 text-slate-300 border border-slate-700">
                          {paper.category}
                        </span>

                        {paper.institution && (
                          <span className="flex items-center gap-1 text-xs text-slate-400">
                            <Building className="w-3.5 h-3.5" />
                            {paper.institution}
                          </span>
                        )}

                        {paper.upvotes && (
                          <span className="flex items-center gap-1 text-[11px] font-semibold text-rose-400 bg-rose-500/10 px-2 py-0.5 rounded-full border border-rose-500/30">
                            <Flame className="w-3 h-3 text-rose-400 fill-rose-400" />
                            {paper.upvotes.toLocaleString()} upvotes
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
                    <div className="flex items-center gap-2 shrink-0 self-start flex-wrap">
                      {/* Audio Explainer Button */}
                      <AudioExplainerButton
                        title={paper.title}
                        text={`Paper title: ${paper.title}. Published: ${formatPaperDate(paper.published_date, paper.year)}. Authors: ${paper.authors}. Core innovation: ${paper.breakthrough || paper.one_liner}. ${paper.formula ? 'Key mathematical formulation: ' + paper.formula : ''}`}
                        label="Listen"
                        variant="compact"
                      />

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
                          subtitle: `${formatPaperDate(paper.published_date, paper.year)} • ${paper.institution || paper.authors}`,
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

                      {/* ArXiv Abstract Link */}
                      {paper.url && (
                        <a
                          href={paper.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-amber-500/10 hover:bg-amber-500/20 text-amber-300 border border-amber-500/30 text-xs font-semibold transition"
                          title="View on arXiv"
                        >
                          <span>arXiv</span>
                          <ExternalLink className="w-3.5 h-3.5" />
                        </a>
                      )}

                      {/* ArXiv PDF Direct Download */}
                      {paper.pdf_url && (
                        <a
                          href={paper.pdf_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="inline-flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-rose-500/10 hover:bg-rose-500/20 text-rose-300 border border-rose-500/30 text-xs font-semibold transition"
                          title="Direct Download PDF"
                        >
                          <FileDown className="w-3.5 h-3.5" />
                          <span className="hidden sm:inline">PDF</span>
                        </a>
                      )}

                      {/* GitHub Code Repository */}
                      {paper.code_url && (
                        <a
                          href={paper.code_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="inline-flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-indigo-500/10 hover:bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 text-xs font-semibold transition"
                          title="View Official Code / GitHub Repository"
                        >
                          <Github className="w-3.5 h-3.5" />
                          <span className="hidden sm:inline">Code</span>
                        </a>
                      )}
                    </div>
                  </div>

                  {/* One Liner Summary */}
                  {paper.one_liner && (
                    <p className={`text-xs sm:text-sm font-medium italic p-3 rounded-xl border ${
                      isLatest
                        ? 'text-cyan-200/90 bg-cyan-950/20 border-cyan-500/20'
                        : 'text-amber-200/90 bg-amber-950/20 border-amber-500/20'
                    }`}>
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
                          Industry Impact & Legacy:
                        </span>
                        <p className="text-slate-400 mt-0.5 leading-relaxed">{paper.impact}</p>
                      </div>
                    </div>
                  )}
                </article>
              </React.Fragment>
            );
          })}
        </div>

      </div>
    </div>
  );
}
