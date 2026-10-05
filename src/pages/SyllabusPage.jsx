import React, { useState, useMemo } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { 
  Search, 
  BookOpen, 
  Calculator, 
  Lightbulb, 
  Sparkles, 
  Layers, 
  ChevronDown, 
  ChevronUp, 
  Printer,
  ArrowUpRight,
  Bookmark,
  CheckCircle2
} from 'lucide-react';
import topicsData from '../data/topics.json';
import hubNodesData from '../data/hubNodes.json';
import KaTeXRenderer, { MathText } from '../components/KaTeXRenderer';
import { findConceptForSubtopic } from '../utils/conceptLookup';
import { useProgress } from '../context/ProgressContext';

export default function SyllabusPage() {
  const { toggleCompleted, isCompleted, toggleBookmark, isBookmarked } = useProgress();
  const [searchParams] = useSearchParams();
  const initialTopic = searchParams.get('topic') || '';
  const [searchQuery, setSearchQuery] = useState(initialTopic);
  const [activeCategory, setActiveCategory] = useState('all');
  const [expandedTopics, setExpandedTopics] = useState(() => {
    // Default expand all
    return new Set(topicsData.map((t) => t.id));
  });

  const completedSyllabusCount = useMemo(() => {
    return topicsData.filter((t) => isCompleted(t.id)).length;
  }, [isCompleted]);

  const completionPercentage = Math.round((completedSyllabusCount / topicsData.length) * 100);

  const categories = [
    { id: 'all', label: 'All Modules (34)' },
    { id: 'math', label: '1. Math Foundations' },
    { id: 'data', label: '2. Data Preprocessing' },
    { id: 'ml', label: '3. Classical ML' },
    { id: 'eval', label: '4. Model Evaluation' },
    { id: 'dl', label: '5. Deep Learning' },
    { id: 'genai', label: '6. Transformers & GenAI' },
  ];

  const toggleTopic = (id) => {
    setExpandedTopics((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  const toggleAll = (expand) => {
    if (expand) {
      setExpandedTopics(new Set(topicsData.map((t) => t.id)));
    } else {
      setExpandedTopics(new Set());
    }
  };

  const filteredTopics = useMemo(() => {
    return topicsData.filter((topic) => {
      if (activeCategory !== 'all' && topic.category !== activeCategory) {
        return false;
      }
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase();
        const matchTitle = topic.label?.toLowerCase().includes(q);
        const matchDef = topic.def?.toLowerCase().includes(q);
        const matchLogic = topic.logic?.toLowerCase().includes(q);
        const matchSub = topic.subtopics?.some((s) => s.toLowerCase().includes(q));
        if (!matchTitle && !matchDef && !matchLogic && !matchSub) return false;
      }
      return true;
    });
  }, [activeCategory, searchQuery]);

  return (
    <div className="flex-1 w-full h-full overflow-y-auto bg-slate-950 text-slate-100 p-4 sm:p-6 md:p-10">
      <div className="max-w-5xl mx-auto space-y-6 pb-20 print-container">
        {/* Header Section */}
        <div className="border-b border-slate-800 pb-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 text-indigo-300 border border-indigo-500/30 text-xs font-semibold uppercase tracking-wider mb-2">
              <BookOpen className="w-3.5 h-3.5" />
              Complete Curriculum
            </div>
            <h1 className="text-2xl sm:text-3xl md:text-4xl font-extrabold text-white tracking-tight">
              Line-wise Master AI & Machine Learning Syllabus
            </h1>
            <p className="text-xs sm:text-sm text-slate-400 mt-1 max-w-3xl">
              From vector calculus and classical optimization to modern LLMs, diffusion mechanisms, and production evaluation. Every single topic broken down with definition, mathematical formulas, intuitive logic, and real-world scenarios.
            </p>
          </div>

          <div className="flex items-center gap-2 no-print shrink-0">
            <button
              onClick={() => toggleAll(true)}
              className="px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-700 hover:bg-slate-800 text-xs text-slate-300 font-medium transition"
            >
              Expand All
            </button>
            <button
              onClick={() => toggleAll(false)}
              className="px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-700 hover:bg-slate-800 text-xs text-slate-300 font-medium transition"
            >
              Collapse All
            </button>
          </div>
        </div>

        {/* Curriculum Mastery Progress Banner */}
        <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-4 sm:p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-4 no-print shadow-sm">
          <div className="flex items-center gap-3.5">
            <div className="w-10 h-10 rounded-xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 flex items-center justify-center shrink-0">
              <CheckCircle2 className="w-5 h-5" />
            </div>
            <div>
              <div className="text-sm font-bold text-white flex items-center gap-2.5">
                <span>Curriculum Mastery Progress</span>
                <span className="text-emerald-400 font-mono text-xs bg-emerald-500/15 px-2.5 py-0.5 rounded-full border border-emerald-500/30">
                  {completedSyllabusCount} / {topicsData.length} Modules ({completionPercentage}%)
                </span>
              </div>
              <p className="text-xs text-slate-400 mt-0.5">
                Mark modules as mastered to track your study roadmap and export personalized revision guides.
              </p>
            </div>
          </div>
          <div className="w-full sm:w-56 flex flex-col gap-1.5 shrink-0">
            <div className="flex justify-between text-[11px] text-slate-400 font-mono">
              <span>Progress</span>
              <span className="text-emerald-300 font-bold">{completionPercentage}%</span>
            </div>
            <div className="w-full bg-slate-800/90 rounded-full h-2.5 overflow-hidden border border-slate-700/60 p-0.5">
              <div 
                className="bg-gradient-to-r from-indigo-500 via-emerald-500 to-teal-400 h-full transition-all duration-500 rounded-full"
                style={{ width: `${completionPercentage}%` }}
              />
            </div>
          </div>
        </div>

        {/* Filter & Search Bar */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 no-print">
          {/* Search Box */}
          <div className="relative flex-1 max-w-md">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search syllabus by topic, formula, or keyword..."
              className="w-full bg-slate-900 border border-slate-800 text-xs sm:text-sm text-white rounded-xl pl-9 pr-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-indigo-500 placeholder-slate-500"
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

          {/* Category Filter Buttons */}
          <div className="flex items-center overflow-x-auto no-scrollbar space-x-1.5 pb-1">
            {categories.map((cat) => (
              <button
                key={cat.id}
                onClick={() => setActiveCategory(cat.id)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition ${
                  activeCategory === cat.id
                    ? 'bg-indigo-600 text-white shadow'
                    : 'bg-slate-900 text-slate-400 hover:text-white border border-slate-800'
                }`}
              >
                {cat.label}
              </button>
            ))}
          </div>
        </div>

        {/* Results Counter */}
        <div className="flex items-center justify-between text-xs text-slate-400 no-print">
          <span>Showing {filteredTopics.length} of {topicsData.length} core syllabus modules</span>
        </div>

        {/* Topics List */}
        <div className="space-y-4">
          {filteredTopics.map((topic, index) => {
            const isExpanded = expandedTopics.has(topic.id);
            const isDone = isCompleted(topic.id);
            const bookmarked = isBookmarked(topic.id);

            return (
              <div
                key={topic.id}
                id={`topic-${topic.id}`}
                className={`border rounded-2xl overflow-hidden shadow-sm transition ${
                  isDone 
                    ? 'bg-slate-900/95 border-emerald-500/40 ring-1 ring-emerald-500/20' 
                    : 'bg-slate-900/90 border-slate-800 hover:border-slate-700'
                }`}
              >
                {/* Topic Header Card */}
                <div
                  onClick={() => toggleTopic(topic.id)}
                  className="p-4 sm:p-5 flex items-center justify-between cursor-pointer hover:bg-slate-800/40 select-none transition gap-3"
                >
                  <div className="flex items-center gap-3 min-w-0">
                    <span className={`w-7 h-7 rounded-lg font-mono text-xs font-bold flex items-center justify-center shrink-0 border ${
                      isDone 
                        ? 'bg-emerald-500/20 border-emerald-500/40 text-emerald-300' 
                        : 'bg-indigo-500/10 border-indigo-500/30 text-indigo-400'
                    }`}>
                      {index + 1}
                    </span>
                    <div className="min-w-0">
                      <div className="flex items-center gap-2 flex-wrap">
                        <h2 className={`text-base sm:text-lg font-bold tracking-tight ${
                          isDone ? 'text-emerald-100 line-through decoration-emerald-500/40' : 'text-white'
                        }`}>
                          {topic.label}
                        </h2>
                        <span className="text-[10px] px-2 py-0.5 rounded-full uppercase font-semibold bg-slate-800 text-slate-400 border border-slate-700">
                          {topic.category}
                        </span>
                        {isDone && (
                          <span className="text-[10px] px-2 py-0.5 rounded-full font-semibold bg-emerald-500/15 text-emerald-300 border border-emerald-500/30 flex items-center gap-1">
                            <CheckCircle2 className="w-3 h-3 text-emerald-400" />
                            Mastered
                          </span>
                        )}
                      </div>
                      <p className="text-xs text-slate-400 mt-0.5 line-clamp-1">
                        {topic.subtopics?.join(' • ')}
                      </p>
                    </div>
                  </div>

                  <div className="no-print flex items-center gap-2 shrink-0">
                    {/* Mark as Mastered button */}
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        toggleCompleted(topic.id);
                      }}
                      className={`p-1.5 rounded-lg border transition ${
                        isDone 
                          ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40' 
                          : 'bg-slate-800 text-slate-400 hover:text-slate-200 border-slate-700'
                      }`}
                      title={isDone ? 'Mark as Incomplete' : 'Mark module as Mastered'}
                    >
                      <CheckCircle2 className={`w-4 h-4 ${isDone ? 'fill-emerald-400/20 text-emerald-400' : ''}`} />
                    </button>

                    {/* Bookmark button */}
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        toggleBookmark({
                          id: topic.id,
                          type: 'syllabus',
                          title: topic.label,
                          subtitle: topic.subtopics?.slice(0, 3).join(', '),
                          link: `/syllabus?topic=${encodeURIComponent(topic.label)}`
                        });
                      }}
                      className={`p-1.5 rounded-lg border transition ${
                        bookmarked 
                          ? 'bg-amber-500/20 text-amber-300 border-amber-500/40' 
                          : 'bg-slate-800 text-slate-400 hover:text-slate-200 border-slate-700'
                      }`}
                      title={bookmarked ? 'Remove Bookmark' : 'Bookmark to Study Vault'}
                    >
                      <Bookmark className={`w-4 h-4 ${bookmarked ? 'fill-amber-400 text-amber-400' : ''}`} />
                    </button>

                    <div className="text-slate-400 pl-1">
                      {isExpanded ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
                    </div>
                  </div>
                </div>

                {/* Expanded Details Body */}
                {isExpanded && (
                  <div className="p-4 sm:p-6 border-t border-slate-800/80 bg-slate-950/40 space-y-4 text-xs sm:text-sm">
                    {/* Definition */}
                    {topic.def && (
                      <div className="bg-slate-900/60 rounded-xl p-4 border border-slate-800">
                        <h3 className="text-xs font-bold text-indigo-300 uppercase tracking-wider mb-1 flex items-center gap-1.5">
                          <BookOpen className="w-3.5 h-3.5" />
                          1. Core Definition & Role
                        </h3>
                        <p className="text-slate-300 leading-relaxed">
                          <MathText text={topic.def} />
                        </p>
                      </div>
                    )}

                    {/* Formula */}
                    {topic.formula && (
                      <div className="bg-slate-900/80 rounded-xl p-4 border border-indigo-500/20">
                        <h3 className="text-xs font-bold text-indigo-300 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                          <Calculator className="w-3.5 h-3.5" />
                          2. Mathematical Formulation
                        </h3>
                        <div className="p-3 bg-slate-950 rounded-lg border border-slate-800 overflow-x-auto">
                          <KaTeXRenderer math={topic.formula} block={true} />
                        </div>
                      </div>
                    )}

                    {/* Grid of Logic & Real-World Scenario */}
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {topic.logic && (
                        <div className="bg-amber-950/20 rounded-xl p-4 border border-amber-500/25">
                          <h3 className="text-xs font-bold text-amber-400 uppercase tracking-wider mb-1.5 flex items-center gap-1.5">
                            <Lightbulb className="w-3.5 h-3.5" />
                            3. Intuition & When to Use
                          </h3>
                          <p className="text-amber-100/90 leading-relaxed text-xs sm:text-sm">
                            <MathText text={topic.logic} />
                          </p>
                        </div>
                      )}

                      {topic.example && (
                        <div className="bg-emerald-950/20 rounded-xl p-4 border border-emerald-500/25">
                          <h3 className="text-xs font-bold text-emerald-400 uppercase tracking-wider mb-1.5 flex items-center gap-1.5">
                            <Sparkles className="w-3.5 h-3.5" />
                            4. Real-World Practical Example
                          </h3>
                          <p className="text-emerald-100/90 leading-relaxed text-xs sm:text-sm">
                            <MathText text={topic.example} />
                          </p>
                        </div>
                      )}
                    </div>

                    {/* Subtopics Checklist */}
                    {topic.subtopics && topic.subtopics.length > 0 && (
                      <div className="pt-2">
                        <div className="flex items-center justify-between mb-2">
                          <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
                            <Layers className="w-3.5 h-3.5 text-indigo-400" />
                            Line-Wise Syllabus Modules ({topic.subtopics.length}):
                          </h3>
                          <span className="text-[11px] text-indigo-400 font-medium hidden sm:inline">
                            Click to explore in Core Concepts &rarr;
                          </span>
                        </div>
                        <div className="flex flex-wrap gap-2">
                          {topic.subtopics.map((sub, sIdx) => {
                            const concept = findConceptForSubtopic(sub, topic.id);
                            const targetUrl = concept
                              ? `/concepts?id=${encodeURIComponent(concept.id)}`
                              : `/concepts?search=${encodeURIComponent(sub)}`;

                            return (
                              <Link
                                key={sIdx}
                                to={targetUrl}
                                className="px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-900 hover:bg-indigo-600/20 text-slate-200 hover:text-indigo-300 border border-slate-800 hover:border-indigo-500/40 transition-all flex items-center gap-2 group shadow-sm"
                                title={`Read full mathematical breakdown and real-world examples for "${sub}" in Core Concepts`}
                              >
                                <span className="w-1.5 h-1.5 rounded-full bg-indigo-400 group-hover:scale-125 transition-transform shrink-0"></span>
                                <span>{sub}</span>
                                <ArrowUpRight className="w-3 h-3 text-slate-500 group-hover:text-indigo-300 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform shrink-0" />
                              </Link>
                            );
                          })}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
