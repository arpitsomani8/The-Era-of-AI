import React, { useState, useMemo, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { 
  Layers, 
  Search, 
  BookOpen, 
  Calculator, 
  Lightbulb, 
  Sparkles, 
  Tag, 
  ChevronRight,
  Share2,
  Check,
  Bookmark,
  CheckCircle2,
  Copy
} from 'lucide-react';
import conceptsData from '../data/concepts.json';
import KaTeXRenderer, { MathText } from '../components/KaTeXRenderer';
import { useProgress } from '../context/ProgressContext';

export default function ConceptsPage() {
  const { toggleCompleted, isCompleted, toggleBookmark, isBookmarked } = useProgress();
  const [searchParams, setSearchParams] = useSearchParams();
  const conceptIdParam = searchParams.get('id');
  const searchParam = searchParams.get('search');
  const topicParam = searchParams.get('topic');
  const categoryParam = searchParams.get('category');

  const [selectedConceptId, setSelectedConceptId] = useState(
    () => conceptIdParam || (conceptsData[0] ? conceptsData[0].id : null)
  );
  const [searchQuery, setSearchQuery] = useState(() => searchParam || '');
  const [activeCategory, setActiveCategory] = useState(() => categoryParam || 'all');
  const [copiedLink, setCopiedLink] = useState(false);
  const [copiedFormula, setCopiedFormula] = useState(false);

  // Sync state with URL search params whenever they change
  useEffect(() => {
    // 1. Direct Concept ID
    if (conceptIdParam) {
      const match = conceptsData.find((c) => c.id === conceptIdParam);
      if (match) {
        setSelectedConceptId(match.id);
        if (match.category) {
          setActiveCategory(match.category);
        }
        setSearchQuery('');
        return;
      }
    }

    // 2. Topic ID scoped
    if (topicParam) {
      const topicMatches = conceptsData.filter((c) => c.topic_id === topicParam);
      if (topicMatches.length > 0) {
        setSelectedConceptId(topicMatches[0].id);
        if (topicMatches[0].category) {
          setActiveCategory(topicMatches[0].category);
        }
        setSearchQuery('');
        return;
      }
    }

    // 3. Category scoped
    if (categoryParam) {
      setActiveCategory(categoryParam);
      const catMatches = conceptsData.filter((c) => c.category === categoryParam);
      if (catMatches.length > 0) {
        setSelectedConceptId(catMatches[0].id);
      }
      return;
    }

    // 4. Search query
    if (searchParam) {
      setSearchQuery(searchParam);
      setActiveCategory('all');
    }
  }, [conceptIdParam, topicParam, categoryParam, searchParam]);

  const categories = [
    { id: 'all', label: 'All (170)' },
    { id: 'math', label: 'Math' },
    { id: 'data', label: 'Data' },
    { id: 'ml', label: 'Classical ML' },
    { id: 'eval', label: 'Evaluation' },
    { id: 'dl', label: 'Deep Learning' },
    { id: 'genai', label: 'GenAI & LLMs' },
    { id: 'mlops', label: 'MLOps' }
  ];

  const filteredConcepts = useMemo(() => {
    return conceptsData.filter((c) => {
      if (activeCategory !== 'all' && c.category !== activeCategory) {
        return false;
      }
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase().trim();
        const tokens = q.split(/[\s,&]+/).filter((t) => t.length > 1);
        
        const title = (c.title || '').toLowerCase();
        const def = (c.def || '').toLowerCase();
        const topic = (c.topic_label || '').toLowerCase();
        const tags = (c.tags || []).join(' ').toLowerCase();
        const combined = `${title} ${def} ${topic} ${tags}`;

        if (title.includes(q) || combined.includes(q)) return true;
        if (tokens.length > 0 && tokens.some((t) => combined.includes(t))) return true;
        return false;
      }
      return true;
    });
  }, [activeCategory, searchQuery]);

  // Selected Concept resolution: prioritize match in filteredConcepts
  const selectedConcept = useMemo(() => {
    const foundInFiltered = filteredConcepts.find((c) => c.id === selectedConceptId);
    if (foundInFiltered) return foundInFiltered;

    if (filteredConcepts.length > 0) {
      return filteredConcepts[0];
    }

    return conceptsData.find((c) => c.id === selectedConceptId) || conceptsData[0];
  }, [selectedConceptId, filteredConcepts]);

  // Auto-scroll sidebar list to the selected concept
  useEffect(() => {
    if (selectedConcept?.id) {
      const el = document.getElementById(`concept-item-${selectedConcept.id}`);
      if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }
    }
  }, [selectedConcept?.id]);

  const handleSelect = (id) => {
    setSelectedConceptId(id);
    setSearchParams({ id });
  };

  const handleCopyLink = () => {
    navigator.clipboard.writeText(window.location.href);
    setCopiedLink(true);
    setTimeout(() => setCopiedLink(false), 2000);
  };

  return (
    <div className="flex-1 w-full h-full flex flex-col md:flex-row overflow-hidden bg-slate-950 text-slate-100">
      {/* Left Sidebar: 170 Concepts Directory */}
      <aside className="w-full md:w-80 lg:w-96 border-r border-slate-800 bg-slate-900/60 flex flex-col shrink-0 h-1/3 md:h-full">
        {/* Sidebar Header & Search */}
        <div className="p-4 border-b border-slate-800 space-y-3 bg-slate-950/40">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Layers className="w-4 h-4 text-rose-400" />
              <h2 className="text-sm font-bold text-white uppercase tracking-wider">
                Concept Encyclopedia
              </h2>
            </div>
            <span className="text-xs px-2 py-0.5 rounded-full bg-slate-800 text-slate-400 border border-slate-700 font-mono">
              {filteredConcepts.length}
            </span>
          </div>

          {/* Search Box */}
          <div className="relative">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Filter 170 concepts..."
              className="w-full bg-slate-900 border border-slate-800 text-xs text-white rounded-lg pl-8 pr-3 py-1.5 focus:outline-none focus:ring-2 focus:ring-rose-500 placeholder-slate-500"
            />
            <Search className="w-3.5 h-3.5 absolute left-2.5 top-2.5 text-slate-500" />
            {searchQuery && (
              <button
                onClick={() => setSearchQuery('')}
                className="absolute right-2.5 top-1.5 text-slate-500 hover:text-white text-xs"
              >
                &times;
              </button>
            )}
          </div>

          {/* Category Filter Pills */}
          <div className="flex items-center overflow-x-auto no-scrollbar space-x-1 pt-1 pb-0.5">
            {categories.map((cat) => (
              <button
                key={cat.id}
                onClick={() => setActiveCategory(cat.id)}
                className={`px-2 py-1 rounded-md text-[11px] font-medium whitespace-nowrap transition ${
                  activeCategory === cat.id
                    ? 'bg-rose-600 text-white shadow'
                    : 'bg-slate-900 text-slate-400 hover:text-white border border-slate-800'
                }`}
              >
                {cat.label}
              </button>
            ))}
          </div>
        </div>

        {/* Concept Items Scrollable List */}
        <div className="flex-1 overflow-y-auto p-2 space-y-1">
          {filteredConcepts.map((concept) => {
            const isSelected = selectedConcept?.id === concept.id;
            const isDone = isCompleted(`concept-${concept.id}`);

            return (
              <div
                key={concept.id}
                id={`concept-item-${concept.id}`}
                onClick={() => handleSelect(concept.id)}
                className={`p-2.5 rounded-xl cursor-pointer transition flex items-center justify-between gap-2 text-xs ${
                  isSelected
                    ? 'bg-rose-600/20 text-white border border-rose-500/40 shadow-sm font-semibold'
                    : 'text-slate-300 hover:bg-slate-800/60 hover:text-white border border-transparent'
                }`}
              >
                <div className="min-w-0 flex items-center gap-2">
                  {isDone && (
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 shrink-0" title="Mastered" />
                  )}
                  <div className="min-w-0">
                    <div className="truncate text-xs font-medium">
                      {concept.title}
                    </div>
                    <div className="text-[10px] text-slate-400 truncate mt-0.5">
                      {concept.topic_label}
                    </div>
                  </div>
                </div>
                <ChevronRight
                  className={`w-3.5 h-3.5 shrink-0 transition-transform ${
                    isSelected ? 'text-rose-400 translate-x-0.5' : 'text-slate-600'
                  }`}
                />
              </div>
            );
          })}
        </div>
      </aside>

      {/* Main Content Area: Selected Concept Detail View */}
      <main className="flex-1 h-2/3 md:h-full overflow-y-auto p-4 sm:p-6 md:p-10">
        {selectedConcept ? (
          <div className="max-w-4xl mx-auto space-y-6 pb-20">
            {/* Concept Header */}
            <div className="border-b border-slate-800 pb-5 space-y-2">
              <div className="flex flex-wrap items-center justify-between gap-3">
                <div className="flex items-center gap-2 flex-wrap">
                  <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider bg-rose-500/10 text-rose-300 border border-rose-500/30">
                    {selectedConcept.category_label || selectedConcept.category}
                  </span>
                  <span className="text-xs text-slate-400">
                    Module: <strong className="text-slate-200">{selectedConcept.topic_label}</strong>
                  </span>
                  {isCompleted(`concept-${selectedConcept.id}`) && (
                    <span className="text-[10px] px-2 py-0.5 rounded-full font-semibold bg-emerald-500/15 text-emerald-300 border border-emerald-500/30 flex items-center gap-1">
                      <CheckCircle2 className="w-3 h-3 text-emerald-400" />
                      Mastered
                    </span>
                  )}
                </div>

                <div className="flex items-center gap-2">
                  {/* Mark as Mastered button */}
                  <button
                    onClick={() => toggleCompleted(`concept-${selectedConcept.id}`)}
                    className={`px-2.5 py-1 rounded-lg border text-xs font-medium transition flex items-center gap-1.5 ${
                      isCompleted(`concept-${selectedConcept.id}`)
                        ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40'
                        : 'bg-slate-900 border-slate-800 text-slate-300 hover:text-white hover:bg-slate-800'
                    }`}
                    title={isCompleted(`concept-${selectedConcept.id}`) ? 'Mark Incomplete' : 'Mark as Mastered'}
                  >
                    <CheckCircle2 className={`w-3.5 h-3.5 ${isCompleted(`concept-${selectedConcept.id}`) ? 'text-emerald-400' : ''}`} />
                    <span>{isCompleted(`concept-${selectedConcept.id}`) ? 'Mastered' : 'Mark Done'}</span>
                  </button>

                  {/* Bookmark button */}
                  <button
                    onClick={() => toggleBookmark({
                      id: `concept-${selectedConcept.id}`,
                      type: 'concept',
                      title: selectedConcept.title,
                      subtitle: `${selectedConcept.topic_label} (${selectedConcept.category})`,
                      link: `/concepts?id=${selectedConcept.id}`
                    })}
                    className={`px-2.5 py-1 rounded-lg border text-xs font-medium transition flex items-center gap-1.5 ${
                      isBookmarked(`concept-${selectedConcept.id}`)
                        ? 'bg-amber-500/20 text-amber-300 border-amber-500/40'
                        : 'bg-slate-900 border-slate-800 text-slate-300 hover:text-white hover:bg-slate-800'
                    }`}
                    title={isBookmarked(`concept-${selectedConcept.id}`) ? 'Remove Bookmark' : 'Bookmark Concept'}
                  >
                    <Bookmark className={`w-3.5 h-3.5 ${isBookmarked(`concept-${selectedConcept.id}`) ? 'fill-amber-400 text-amber-400' : ''}`} />
                    <span>{isBookmarked(`concept-${selectedConcept.id}`) ? 'Saved' : 'Save'}</span>
                  </button>

                  {/* Share button */}
                  <button
                    onClick={handleCopyLink}
                    className="px-2.5 py-1 rounded-lg bg-slate-900 border border-slate-800 hover:bg-slate-800 text-xs text-slate-300 hover:text-white transition flex items-center gap-1.5"
                    title="Copy direct link to this concept"
                  >
                    {copiedLink ? (
                      <>
                        <Check className="w-3.5 h-3.5 text-emerald-400" />
                        <span className="text-emerald-400">Link Copied!</span>
                      </>
                    ) : (
                      <>
                        <Share2 className="w-3.5 h-3.5 text-slate-400" />
                        <span>Share</span>
                      </>
                    )}
                  </button>
                </div>
              </div>

              <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight leading-snug">
                {selectedConcept.title}
              </h1>
            </div>

            {/* 1. Definition */}
            {selectedConcept.def && (
              <div className="bg-slate-900/90 rounded-2xl p-5 sm:p-6 border border-slate-800 space-y-2">
                <h3 className="text-xs font-bold text-rose-300 uppercase tracking-wider flex items-center gap-1.5">
                  <BookOpen className="w-3.5 h-3.5 text-rose-400" />
                  1. Formal Definition & Role
                </h3>
                <p className="text-slate-200 leading-relaxed text-sm sm:text-base">
                  <MathText text={selectedConcept.def} />
                </p>
              </div>
            )}

            {/* 2. Mathematical Formulation */}
            {selectedConcept.formula && (
              <div className="bg-slate-900/90 rounded-2xl p-5 sm:p-6 border border-indigo-500/25 space-y-3">
                <div className="flex items-center justify-between">
                  <h3 className="text-xs font-bold text-indigo-300 uppercase tracking-wider flex items-center gap-1.5">
                    <Calculator className="w-3.5 h-3.5 text-indigo-400" />
                    2. Core Mathematical Formulation
                  </h3>

                  <button
                    onClick={() => {
                      navigator.clipboard.writeText(selectedConcept.formula);
                      setCopiedFormula(true);
                      setTimeout(() => setCopiedFormula(false), 2000);
                    }}
                    className="p-1 px-2 rounded-lg bg-slate-950 hover:bg-slate-800 border border-slate-800 text-[11px] text-slate-400 hover:text-white transition flex items-center gap-1"
                    title="Copy raw LaTeX equation"
                  >
                    {copiedFormula ? (
                      <>
                        <Check className="w-3 h-3 text-emerald-400" />
                        <span className="text-emerald-400">LaTeX Copied!</span>
                      </>
                    ) : (
                      <>
                        <Copy className="w-3 h-3" />
                        <span>Copy LaTeX</span>
                      </>
                    )}
                  </button>
                </div>

                <div className="p-4 bg-slate-950 rounded-xl border border-slate-800 overflow-x-auto text-center">
                  <KaTeXRenderer math={selectedConcept.formula} block={true} />
                </div>
              </div>
            )}

            {/* 3. Intuition & When to Use */}
            {selectedConcept.logic && (
              <div className="bg-amber-950/20 rounded-2xl p-5 sm:p-6 border border-amber-500/25 space-y-2">
                <h3 className="text-xs font-bold text-amber-400 uppercase tracking-wider flex items-center gap-1.5">
                  <Lightbulb className="w-3.5 h-3.5 text-amber-400" />
                  3. Intuition & When to Use
                </h3>
                <p className="text-amber-100/90 leading-relaxed text-sm sm:text-base">
                  <MathText text={selectedConcept.logic} />
                </p>
              </div>
            )}

            {/* 4. Real-World Practical Example */}
            {selectedConcept.example && (
              <div className="bg-emerald-950/20 rounded-2xl p-5 sm:p-6 border border-emerald-500/25 space-y-2">
                <h3 className="text-xs font-bold text-emerald-400 uppercase tracking-wider flex items-center gap-1.5">
                  <Sparkles className="w-3.5 h-3.5 text-emerald-400" />
                  4. Real-World Practical Example
                </h3>
                <p className="text-emerald-100/90 leading-relaxed text-sm sm:text-base">
                  <MathText text={selectedConcept.example} />
                </p>
              </div>
            )}

            {/* Tags */}
            {selectedConcept.tags && selectedConcept.tags.length > 0 && (
              <div className="pt-2">
                <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                  <Tag className="w-3.5 h-3.5 text-slate-400" />
                  Related Keywords:
                </h4>
                <div className="flex flex-wrap gap-1.5">
                  {selectedConcept.tags.map((t, idx) => (
                    <span
                      key={idx}
                      className="px-2.5 py-1 rounded-lg text-xs bg-slate-900 text-slate-300 border border-slate-800"
                    >
                      #{t}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        ) : (
          <div className="h-full flex items-center justify-center text-slate-500 text-sm">
            Select a concept from the sidebar to inspect details.
          </div>
        )}
      </main>
    </div>
  );
}
