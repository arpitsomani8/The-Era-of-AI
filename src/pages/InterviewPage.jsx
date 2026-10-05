import React, { useState, useMemo } from 'react';
import { useSearchParams } from 'react-router-dom';
import { 
  HelpCircle, 
  Search, 
  ChevronDown, 
  ChevronUp, 
  Check, 
  Copy, 
  Tag, 
  Sparkles, 
  Lightbulb, 
  Award,
  Filter
} from 'lucide-react';
import interviewData from '../data/interviewQuestions.json';
import KaTeXRenderer from '../components/KaTeXRenderer';

export default function InterviewPage() {
  const [searchParams] = useSearchParams();
  const initialSearch = searchParams.get('search') || '';
  const [searchQuery, setSearchQuery] = useState(initialSearch);
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedDifficulty, setSelectedDifficulty] = useState('all');
  const [openIds, setOpenIds] = useState(new Set());
  const [copiedId, setCopiedId] = useState(null);

  const categories = [
    { id: 'all', label: 'All (150)' },
    { id: 'ml', label: 'Classical ML' },
    { id: 'dl', label: 'Deep Learning' },
    { id: 'genai_llm', label: 'GenAI & LLMs' },
    { id: 'rag', label: 'RAG & Vector DB' },
    { id: 'metrics_data', label: 'Metrics & Data' },
    { id: 'system_mlops', label: 'System & MLOps' },
    { id: 'logic_prob', label: 'Logic & Quant' }
  ];

  const difficulties = [
    'all',
    'Junior / Mid',
    'Mid',
    'Mid / Senior',
    'Senior',
    'Senior / Staff',
    'Quant / Research'
  ];

  const toggleAnswer = (id) => {
    setOpenIds((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  const toggleAll = (expand) => {
    if (expand) {
      setOpenIds(new Set(interviewData.map((q) => q.id)));
    } else {
      setOpenIds(new Set());
    }
  };

  const handleCopy = (item) => {
    const text = `Q: ${item.question}\n\nA: ${item.answer}\n\nTip: ${item.tip || ''}`;
    navigator.clipboard.writeText(text);
    setCopiedId(item.id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const filteredQuestions = useMemo(() => {
    return interviewData.filter((item) => {
      if (selectedCategory !== 'all' && item.category !== selectedCategory) {
        return false;
      }
      if (selectedDifficulty !== 'all' && item.difficulty !== selectedDifficulty) {
        return false;
      }
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase();
        const matchQ = item.question?.toLowerCase().includes(q);
        const matchA = item.answer?.toLowerCase().includes(q);
        const matchTip = item.tip?.toLowerCase().includes(q);
        const matchCompany = item.company_tags?.some((c) => c.toLowerCase().includes(q));
        if (!matchQ && !matchA && !matchTip && !matchCompany) return false;
      }
      return true;
    });
  }, [selectedCategory, selectedDifficulty, searchQuery]);

  const getDifficultyBadge = (diff) => {
    if (diff?.includes('Staff') || diff?.includes('Quant')) {
      return 'bg-purple-500/10 text-purple-300 border-purple-500/30';
    }
    if (diff?.includes('Senior')) {
      return 'bg-amber-500/10 text-amber-300 border-amber-500/30';
    }
    if (diff?.includes('Mid')) {
      return 'bg-blue-500/10 text-blue-300 border-blue-500/30';
    }
    return 'bg-emerald-500/10 text-emerald-300 border-emerald-500/30';
  };

  return (
    <div className="flex-1 w-full h-full overflow-y-auto bg-slate-950 text-slate-100 p-4 sm:p-6 md:p-10">
      <div className="max-w-5xl mx-auto space-y-6 pb-20">
        {/* Header */}
        <div className="border-b border-slate-800 pb-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-purple-500/10 text-purple-300 border border-purple-500/30 text-xs font-semibold uppercase tracking-wider mb-2">
              <HelpCircle className="w-3.5 h-3.5" />
              Technical Interview Question Bank
            </div>
            <h1 className="text-2xl sm:text-3xl md:text-4xl font-extrabold text-white tracking-tight">
              Master AI & Machine Learning Interview Vault
            </h1>
            <p className="text-xs sm:text-sm text-slate-400 mt-1 max-w-3xl">
              150+ rigorously curated technical interview questions asked at Google, Meta, OpenAI, Anthropic, and top hedge funds. Includes mathematical explanations, code walkthroughs, and practical insider tips.
            </p>
          </div>

          <div className="flex items-center gap-2 shrink-0">
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

        {/* Filters */}
        <div className="space-y-3">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            {/* Search Input */}
            <div className="relative flex-1 max-w-md">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search 150 questions (e.g. FlashAttention, LoRA, ROC-AUC)..."
                className="w-full bg-slate-900 border border-slate-800 text-xs sm:text-sm text-white rounded-xl pl-9 pr-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-purple-500 placeholder-slate-500"
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

            {/* Difficulty Dropdown */}
            <div className="flex items-center gap-2 text-xs">
              <span className="text-slate-400 hidden sm:inline">Difficulty:</span>
              <select
                value={selectedDifficulty}
                onChange={(e) => setSelectedDifficulty(e.target.value)}
                className="bg-slate-900 border border-slate-800 text-slate-200 rounded-lg px-3 py-2 text-xs focus:outline-none focus:ring-2 focus:ring-purple-500"
              >
                {difficulties.map((diff) => (
                  <option key={diff} value={diff}>
                    {diff === 'all' ? 'All Difficulties' : diff}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Category Tabs */}
          <div className="flex items-center overflow-x-auto no-scrollbar space-x-1.5 pb-1">
            {categories.map((cat) => (
              <button
                key={cat.id}
                onClick={() => setSelectedCategory(cat.id)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition ${
                  selectedCategory === cat.id
                    ? 'bg-purple-600 text-white shadow-md shadow-purple-600/30'
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
          Showing {filteredQuestions.length} of {interviewData.length} interview questions
        </div>

        {/* Question Cards List */}
        <div className="space-y-4">
          {filteredQuestions.map((item, idx) => {
            const isOpen = openIds.has(item.id);

            return (
              <div
                key={item.id || idx}
                className="bg-slate-900/90 border border-slate-800 rounded-2xl overflow-hidden shadow-sm transition hover:border-slate-700"
              >
                {/* Question Header Card */}
                <div
                  onClick={() => toggleAnswer(item.id)}
                  className="p-4 sm:p-5 flex items-start justify-between gap-4 cursor-pointer hover:bg-slate-800/40 select-none transition"
                >
                  <div className="space-y-2 flex-1 min-w-0">
                    <div className="flex items-center gap-2 flex-wrap">
                      <span className="w-6 h-6 rounded-md bg-purple-500/10 text-purple-400 border border-purple-500/30 font-mono text-xs font-bold flex items-center justify-center shrink-0">
                        {item.id}
                      </span>
                      <span className="px-2 py-0.5 rounded-full text-[10px] font-semibold uppercase tracking-wider bg-slate-800 text-slate-300 border border-slate-700">
                        {item.category_label || item.category}
                      </span>
                      <span
                        className={`px-2 py-0.5 rounded-full text-[10px] font-semibold border ${getDifficultyBadge(
                          item.difficulty
                        )}`}
                      >
                        {item.difficulty}
                      </span>
                      {item.company_tags?.map((comp, cIdx) => (
                        <span
                          key={cIdx}
                          className="px-2 py-0.5 rounded-md text-[10px] font-mono bg-slate-950 text-indigo-300 border border-slate-800"
                        >
                          {comp}
                        </span>
                      ))}
                    </div>

                    <h2 className="text-base sm:text-lg font-bold text-white tracking-tight leading-snug">
                      {item.question}
                    </h2>
                  </div>

                  <div className="flex items-center space-x-2 shrink-0 pt-1">
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleCopy(item);
                      }}
                      title="Copy Question & Answer"
                      className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition"
                    >
                      {copiedId === item.id ? (
                        <Check className="w-4 h-4 text-emerald-400" />
                      ) : (
                        <Copy className="w-4 h-4" />
                      )}
                    </button>
                    <div className="text-slate-400">
                      {isOpen ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
                    </div>
                  </div>
                </div>

                {/* Expanded Answer Body */}
                {isOpen && (
                  <div className="p-4 sm:p-6 border-t border-slate-800/80 bg-slate-950/60 space-y-4 text-xs sm:text-sm">
                    {/* Detailed Answer */}
                    <div className="bg-slate-900/80 rounded-xl p-4 sm:p-5 border border-slate-800 space-y-3">
                      <h3 className="text-xs font-bold text-purple-300 uppercase tracking-wider flex items-center gap-1.5">
                        <Sparkles className="w-3.5 h-3.5 text-purple-400" />
                        Comprehensive Technical Answer:
                      </h3>
                      <div className="text-slate-200 leading-relaxed whitespace-pre-line">
                        {item.answer}
                      </div>
                    </div>

                    {/* Interviewer Tip / Gotcha */}
                    {item.tip && (
                      <div className="bg-amber-950/20 rounded-xl p-4 border border-amber-500/25 flex items-start gap-2.5">
                        <Lightbulb className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
                        <div>
                          <span className="text-xs font-bold text-amber-400 uppercase tracking-wider block mb-0.5">
                            Interviewer Tip & Gotcha:
                          </span>
                          <p className="text-amber-100/90 leading-relaxed text-xs sm:text-sm">
                            {item.tip}
                          </p>
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
