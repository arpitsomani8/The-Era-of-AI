import React, { useState, useMemo } from 'react';
import { useSearchParams } from 'react-router-dom';
import { 
  HelpCircle, 
  Search, 
  ChevronDown, 
  ChevronUp, 
  Check, 
  Copy, 
  Sparkles, 
  Lightbulb, 
  Bookmark,
  CheckCircle2,
  Layers,
  RotateCw,
  ChevronLeft,
  ChevronRight,
  Shuffle,
  Award
} from 'lucide-react';
import interviewData from '../data/interviewQuestions.json';
import KaTeXRenderer, { MathText } from '../components/KaTeXRenderer';
import { useProgress } from '../context/ProgressContext';
import InterviewFlashcardDeck from '../components/InterviewFlashcardDeck';

export default function InterviewPage({ onOpenAssessment }) {
  const { toggleCompleted, isCompleted, toggleBookmark, isBookmarked } = useProgress();
  const [searchParams] = useSearchParams();
  const initialSearch = searchParams.get('search') || '';
  const [searchQuery, setSearchQuery] = useState(initialSearch);
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedDifficulty, setSelectedDifficulty] = useState('all');
  const [statusFilter, setStatusFilter] = useState('all'); // 'all', 'bookmarked', 'mastered', 'unmastered'
  const [openIds, setOpenIds] = useState(new Set());
  const [copiedId, setCopiedId] = useState(null);
  const [visibleCount, setVisibleCount] = useState(50);

  // Flashcard mode state
  const [isFlashcardMode, setIsFlashcardMode] = useState(false);
  const [cardIndex, setCardIndex] = useState(0);
  const [isCardFlipped, setIsCardFlipped] = useState(false);
  const [selectedExperience, setSelectedExperience] = useState('0-2'); // '0-2', '2-5', '6+', 'all'
  const [selectedRound, setSelectedRound] = useState('all'); // 'all', 'round_coding', 'round_ml_theory', 'round_system_design', 'round_behavioral', 'round_terminology'

  const experienceCounts = useMemo(() => {
    const counts = { all: interviewData.length, '0-2': 0, '2-5': 0, '6+': 0 };
    interviewData.forEach((q) => {
      const exp = q.experience_level || '6+';
      if (counts[exp] !== undefined) counts[exp]++;
    });
    return counts;
  }, []);

  const categoryCounts = useMemo(() => {
    const counts = { all: interviewData.length };
    interviewData.forEach((q) => {
      if (q.category) {
        counts[q.category] = (counts[q.category] || 0) + 1;
      }
    });
    return counts;
  }, []);

  const categories = [
    { id: 'all', label: `All (${categoryCounts.all})` },
    { id: 'ml', label: `Classical ML (${categoryCounts.ml || 0})` },
    { id: 'dl', label: `Deep Learning (${categoryCounts.dl || 0})` },
    { id: 'genai_llm', label: `GenAI & LLMs (${categoryCounts.genai_llm || 0})` },
    { id: 'rag', label: `RAG & Vector DB (${categoryCounts.rag || 0})` },
    { id: 'metrics_data', label: `Metrics & Data (${categoryCounts.metrics_data || 0})` },
    { id: 'system_mlops', label: `System & MLOps (${categoryCounts.system_mlops || 0})` },
    { id: 'swe_cloud', label: `SWE & Cloud Infra (${categoryCounts.swe_cloud || 0})` },
    { id: 'logic_prob', label: `Logic & Quant (${categoryCounts.logic_prob || 0})` }
  ];

  const difficulties = [
    'all',
    'Junior / Fresher',
    'Junior / Mid',
    'Mid',
    'Mid / Senior',
    'Senior',
    'Senior / Staff',
    'Quant / Research'
  ];

  const masteredCount = useMemo(() => {
    return interviewData.filter((q) => isCompleted(`interview-${q.id}`)).length;
  }, [isCompleted]);

  const masteredPercentage = Math.round((masteredCount / interviewData.length) * 100);

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
      setVisibleCount(filteredQuestions.length);
      setOpenIds(new Set(filteredQuestions.map((q) => q.id)));
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
      const qKey = `interview-${item.id}`;
      const isDone = isCompleted(qKey);
      const isSaved = isBookmarked(qKey);

      if (statusFilter === 'bookmarked' && !isSaved) return false;
      if (statusFilter === 'mastered' && !isDone) return false;
      if (statusFilter === 'unmastered' && isDone) return false;

      // Filter by Phase 13 Mock Interview Round
      if (selectedRound !== 'all' && item.interview_round !== selectedRound) {
        return false;
      }

      // Filter by Experience Tier
      if (selectedExperience !== 'all') {
        const itemExp = item.experience_level || '6+';
        if (itemExp !== selectedExperience) return false;
      }

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
  }, [selectedExperience, selectedCategory, selectedDifficulty, searchQuery, statusFilter, selectedRound, isCompleted, isBookmarked]);

  React.useEffect(() => {
    setVisibleCount(50);
  }, [selectedExperience, selectedCategory, selectedDifficulty, searchQuery, statusFilter, selectedRound]);

  const displayedQuestions = useMemo(() => {
    return filteredQuestions.slice(0, visibleCount);
  }, [filteredQuestions, visibleCount]);

  const getExperienceBadge = (level) => {
    if (level === '0-2') {
      return {
        label: '🌱 0–2 Yrs (Freshers)',
        cls: 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30'
      };
    }
    if (level === '2-5') {
      return {
        label: '🚀 2–5 Yrs (Mid-Level)',
        cls: 'bg-blue-500/15 text-blue-300 border-blue-500/30'
      };
    }
    return {
      label: '🏛️ 6+ Yrs (Senior / Lead)',
      cls: 'bg-purple-500/15 text-purple-300 border-purple-500/30'
    };
  };

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

  // Flashcard controls
  const currentCard = filteredQuestions[cardIndex] || filteredQuestions[0];

  const handleNextCard = () => {
    setIsCardFlipped(false);
    setCardIndex((prev) => (prev + 1) % (filteredQuestions.length || 1));
  };

  const handlePrevCard = () => {
    setIsCardFlipped(false);
    setCardIndex((prev) => (prev - 1 + filteredQuestions.length) % (filteredQuestions.length || 1));
  };

  const handleShuffleCards = () => {
    setIsCardFlipped(false);
    setCardIndex(Math.floor(Math.random() * (filteredQuestions.length || 1)));
  };

  return (
    <div className="flex-1 w-full h-full overflow-y-auto bg-slate-950 text-slate-100 p-4 sm:p-6 md:p-10">
      <div className="max-w-5xl mx-auto space-y-6 pb-20">
        {/* Header */}
        <div className="border-b border-slate-800 pb-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-purple-500/10 text-purple-300 border border-purple-500/30 text-xs font-semibold uppercase tracking-wider mb-2">
              <HelpCircle className="w-3.5 h-3.5" />
              Technical Interview Question Vault
            </div>
            <h1 className="text-2xl sm:text-3xl md:text-4xl font-extrabold text-white tracking-tight">
              Master AI & Machine Learning Interview Vault
            </h1>
            <p className="text-xs sm:text-sm text-slate-400 mt-1 max-w-3xl">
              {interviewData.length.toLocaleString()}+ curated technical questions tailored for all career stages: <span className="text-emerald-400 font-semibold">🌱 0–2 Yrs (Freshers)</span>, <span className="text-blue-400 font-semibold">🚀 2–5 Yrs (Mid-Level)</span>, and <span className="text-purple-400 font-semibold">🏛️ 6+ Yrs (Senior / Staff / Lead)</span>.
            </p>
          </div>

          <div className="flex items-center gap-2 shrink-0">
            {/* Flashcard Mode Toggle */}
            <button
              onClick={() => {
                setIsFlashcardMode(!isFlashcardMode);
                setIsCardFlipped(false);
              }}
              className={`px-3 py-1.5 rounded-lg border text-xs font-semibold transition flex items-center gap-1.5 ${
                isFlashcardMode 
                  ? 'bg-purple-600 text-white border-purple-500 shadow-md shadow-purple-600/30' 
                  : 'bg-slate-900 border-slate-700 hover:bg-slate-800 text-slate-300'
              }`}
            >
              <Layers className="w-3.5 h-3.5" />
              <span>{isFlashcardMode ? 'Standard List' : 'Flashcard Mode'}</span>
            </button>

            {!isFlashcardMode && (
              <>
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
              </>
            )}
          </div>
        </div>

        {/* Interview Mastery Progress Banner */}
        <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-4 sm:p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-4 shadow-sm">
          <div className="flex items-center gap-3.5">
            <div className="w-10 h-10 rounded-xl bg-purple-500/10 text-purple-400 border border-purple-500/30 flex items-center justify-center shrink-0">
              <CheckCircle2 className="w-5 h-5" />
            </div>
            <div>
              <div className="text-sm font-bold text-white flex items-center gap-2.5">
                <span>Interview Readiness Score</span>
                <span className="text-purple-300 font-mono text-xs bg-purple-500/15 px-2.5 py-0.5 rounded-full border border-purple-500/30">
                  {masteredCount} / {interviewData.length} Mastered ({masteredPercentage}%)
                </span>
              </div>
              <p className="text-xs text-slate-400 mt-0.5">
                Practice each question, flip cards for active recall, and mark items mastered as you prepare for interviews.
              </p>
            </div>
          </div>
          <div className="w-full sm:w-60 flex flex-col gap-2 shrink-0">
            <div className="flex justify-between text-[11px] text-slate-400 font-mono">
              <span>Readiness</span>
              <span className="text-purple-300 font-bold">{masteredPercentage}%</span>
            </div>
            <div className="w-full bg-slate-800/90 rounded-full h-2.5 overflow-hidden border border-slate-700/60 p-0.5">
              <div 
                className="bg-gradient-to-r from-purple-500 via-indigo-500 to-cyan-400 h-full transition-all duration-500 rounded-full"
                style={{ width: `${masteredPercentage}%` }}
              />
            </div>
            {onOpenAssessment && (
              <button
                onClick={onOpenAssessment}
                className="mt-0.5 flex items-center justify-center gap-1.5 px-3 py-1.5 rounded-lg bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white text-xs font-semibold shadow-md shadow-purple-600/25 transition active:scale-95"
              >
                <Award className="w-3.5 h-3.5" />
                <span>Take Diagnostic Test</span>
              </button>
            )}
          </div>
        </div>

        {/* Phase 13: Mock Interview Simulator Rounds */}
        <div className="bg-gradient-to-r from-purple-950/40 via-slate-900 to-indigo-950/40 border border-purple-500/35 rounded-2xl p-4 space-y-3 shadow-md">
          <div className="flex items-center justify-between flex-wrap gap-2">
            <div className="flex items-center gap-2">
              <span className="text-lg">🎯</span>
              <h3 className="text-xs sm:text-sm font-bold text-white uppercase tracking-wider">
                Phase 13 &bull; Mock Interview Simulator Rounds
              </h3>
            </div>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-purple-500/20 text-purple-300 border border-purple-500/40 font-semibold">
              5 Specialized Tracks
            </span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2">
            {[
              { id: 'all', label: 'All Questions', icon: '📋' },
              { id: 'round_coding', label: '1. Coding (DSA)', icon: '💻' },
              { id: 'round_ml_theory', label: '2. ML Theory', icon: '🧠' },
              { id: 'round_system_design', label: '3. System Design', icon: '🏗️' },
              { id: 'round_behavioral', label: '4. Behavioral', icon: '🤝' },
              { id: 'round_terminology', label: '5. Terminology Blitz', icon: '⚡' }
            ].map((round) => {
              const isActive = selectedRound === round.id;
              return (
                <button
                  key={round.id}
                  onClick={() => {
                    setSelectedRound(round.id);
                    if (round.id !== 'all') setSelectedExperience('all');
                  }}
                  className={`p-2.5 rounded-xl border text-xs font-semibold transition flex flex-col items-center justify-center text-center gap-1 ${
                    isActive
                      ? 'bg-purple-600 text-white border-purple-400 shadow-md shadow-purple-600/30 ring-1 ring-purple-400'
                      : 'bg-slate-950/80 hover:bg-slate-800 text-slate-300 border-slate-800'
                  }`}
                >
                  <span className="text-base">{round.icon}</span>
                  <span className="text-[11px] leading-tight">{round.label}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Experience Tier Selector */}
        <div className="space-y-3">
          <div className="flex items-center justify-between text-xs">
            <span className="text-slate-400 font-medium">Select Experience Level:</span>
            <span className="text-purple-300 font-mono text-[11px]">
              Active: {selectedExperience === '0-2' ? '🌱 0–2 Years' : selectedExperience === '2-5' ? '🚀 2–5 Years' : selectedExperience === '6+' ? '🏛️ 6+ Years' : 'All Levels'}
            </span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
            {[
              { id: '0-2', label: '0–2 Years', sub: 'Freshers & Entry-Level', icon: '🌱', count: experienceCounts['0-2'], color: 'emerald' },
              { id: '2-5', label: '2–5 Years', sub: 'Mid-Level Engineers', icon: '🚀', count: experienceCounts['2-5'], color: 'blue' },
              { id: '6+', label: '6+ Years', sub: 'Senior / Staff / Lead', icon: '🏛️', count: experienceCounts['6+'], color: 'purple' },
              { id: 'all', label: 'All Levels', sub: 'Complete Question Bank', icon: '🌐', count: experienceCounts.all, color: 'slate' },
            ].map((tier) => {
              const isActive = selectedExperience === tier.id;
              return (
                <button
                  key={tier.id}
                  onClick={() => setSelectedExperience(tier.id)}
                  className={`p-3 rounded-2xl border text-left transition flex flex-col justify-between gap-1.5 cursor-pointer ${
                    isActive
                      ? tier.id === '0-2'
                        ? 'bg-emerald-950/50 border-emerald-500/60 ring-1 ring-emerald-500/40 text-emerald-200'
                        : tier.id === '2-5'
                        ? 'bg-blue-950/50 border-blue-500/60 ring-1 ring-blue-500/40 text-blue-200'
                        : tier.id === '6+'
                        ? 'bg-purple-950/50 border-purple-500/60 ring-1 ring-purple-500/40 text-purple-200'
                        : 'bg-slate-850 border-slate-700 ring-1 ring-slate-600 text-white'
                      : 'bg-slate-900/90 border-slate-800 hover:border-slate-700 text-slate-300 hover:bg-slate-850'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="text-base">{tier.icon}</span>
                    <span className={`text-[10px] px-2 py-0.5 rounded-full font-mono font-bold ${
                      isActive ? 'bg-black/30' : 'bg-slate-800 text-slate-400'
                    }`}>
                      {tier.count} Qs
                    </span>
                  </div>
                  <div>
                    <div className="text-xs font-bold leading-tight">{tier.label}</div>
                    <div className="text-[10px] text-slate-400 leading-tight mt-0.5">{tier.sub}</div>
                  </div>
                </button>
              );
            })}
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
                placeholder={`Search ${interviewData.length.toLocaleString()}+ questions (e.g. Overfitting, RAG, Embeddings, LoRA)...`}
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

            {/* Quick Status and Difficulty Dropdown */}
            <div className="flex items-center gap-2 text-xs flex-wrap">
              {/* Status Filter */}
              <div className="flex items-center bg-slate-900 border border-slate-800 rounded-lg p-0.5">
                {[
                  { id: 'all', label: 'All' },
                  { id: 'bookmarked', label: 'Saved' },
                  { id: 'mastered', label: 'Mastered' },
                  { id: 'unmastered', label: 'To Review' },
                ].map((s) => (
                  <button
                    key={s.id}
                    onClick={() => setStatusFilter(s.id)}
                    className={`px-2.5 py-1 rounded-md text-[11px] font-medium transition ${
                      statusFilter === s.id
                        ? 'bg-purple-600 text-white shadow-sm'
                        : 'text-slate-400 hover:text-slate-200'
                    }`}
                  >
                    {s.label}
                  </button>
                ))}
              </div>

              {/* Difficulty Dropdown */}
              <select
                value={selectedDifficulty}
                onChange={(e) => setSelectedDifficulty(e.target.value)}
                className="bg-slate-900 border border-slate-800 text-slate-200 rounded-lg px-3 py-1.5 text-xs focus:outline-none focus:ring-2 focus:ring-purple-500"
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
                    ? 'bg-purple-600 text-white shadow'
                    : 'bg-slate-900 text-slate-400 hover:text-white border border-slate-800'
                }`}
              >
                {cat.label}
              </button>
            ))}
          </div>
        </div>

        {/* Results Count & Quick Actions */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2.5 text-xs text-slate-400 pb-1">
          <div className="flex items-center gap-2 flex-wrap">
            <span className="font-semibold text-slate-200">
              Showing {displayedQuestions.length < filteredQuestions.length ? `${displayedQuestions.length} of ${filteredQuestions.length}` : filteredQuestions.length}
            </span>
            <span className="text-slate-500 font-normal">
              of {interviewData.length.toLocaleString()} technical questions
            </span>
            <span className="text-slate-700 hidden sm:inline">&bull;</span>
            <span className="text-purple-400/90 font-mono text-[11px]">
              {openIds.size > 0 ? `${openIds.size} answers expanded` : 'All answers collapsed'}
            </span>
          </div>

          {!isFlashcardMode && (
            <div className="flex items-center gap-2 shrink-0">
              <button
                onClick={() => toggleAll(true)}
                className="px-3 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-700/80 hover:border-purple-500/50 text-slate-200 hover:text-white text-xs font-medium transition flex items-center gap-1.5 cursor-pointer shadow-sm active:scale-95"
                title="Expand answers for all displayed questions"
              >
                <ChevronDown className="w-3.5 h-3.5 text-purple-400" />
                <span>Expand All</span>
              </button>
              <button
                onClick={() => toggleAll(false)}
                className="px-3 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-700/80 hover:border-purple-500/50 text-slate-200 hover:text-white text-xs font-medium transition flex items-center gap-1.5 cursor-pointer shadow-sm active:scale-95"
                title="Collapse all expanded answers"
              >
                <ChevronUp className="w-3.5 h-3.5 text-purple-400" />
                <span>Collapse All</span>
              </button>
            </div>
          )}
        </div>

        {/* 3D ACTIVE RECALL FLASHCARD STUDY DECK */}
        {isFlashcardMode && (
          <InterviewFlashcardDeck
            questions={filteredQuestions}
            onClose={() => setIsFlashcardMode(false)}
            getDifficultyBadge={getDifficultyBadge}
          />
        )}

        {/* STANDARD LIST OF QUESTIONS */}
        {!isFlashcardMode && (
          <div className="space-y-4">
            {displayedQuestions.map((item, idx) => {
              const isOpen = openIds.has(item.id);
              const qKey = `interview-${item.id}`;
              const isDone = isCompleted(qKey);
              const isSaved = isBookmarked(qKey);

              return (
                <div
                  key={item.id}
                  id={`q-${item.id}`}
                  className={`border rounded-2xl overflow-hidden shadow-sm transition ${
                    isDone 
                      ? 'bg-slate-900/95 border-emerald-500/40 ring-1 ring-emerald-500/20' 
                      : 'bg-slate-900/90 border-slate-800 hover:border-slate-700'
                  }`}
                >
                  {/* Question Header Card */}
                  <div
                    onClick={() => toggleAnswer(item.id)}
                    className="p-4 sm:p-5 flex items-start justify-between cursor-pointer hover:bg-slate-800/40 select-none transition gap-3"
                  >
                    <div className="space-y-2 flex-1 min-w-0">
                      <div className="flex items-center gap-2 flex-wrap">
                        <span className={`px-2 h-6 min-w-[2.25rem] rounded-md font-mono text-[11px] font-bold flex items-center justify-center shrink-0 border ${
                          isDone 
                            ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40' 
                            : 'bg-purple-500/10 text-purple-400 border border-purple-500/30'
                        }`}>
                          #{idx + 1}
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
                        {item.experience_level && (
                          <span
                            className={`px-2 py-0.5 rounded-full text-[10px] font-semibold border ${getExperienceBadge(
                              item.experience_level
                            ).cls}`}
                          >
                            {getExperienceBadge(item.experience_level).label}
                          </span>
                        )}
                        {item.company_tags?.map((comp, cIdx) => (
                          <span
                            key={cIdx}
                            className="px-2 py-0.5 rounded-md text-[10px] font-mono bg-slate-950 text-indigo-300 border border-slate-800"
                          >
                            {comp}
                          </span>
                        ))}
                        {isDone && (
                          <span className="text-[10px] px-2 py-0.5 rounded-full font-semibold bg-emerald-500/15 text-emerald-300 border border-emerald-500/30 flex items-center gap-1">
                            <CheckCircle2 className="w-3 h-3 text-emerald-400" />
                            Mastered
                          </span>
                        )}
                      </div>

                      <h2 className={`text-base sm:text-lg font-bold tracking-tight leading-snug ${
                        isDone ? 'text-emerald-100' : 'text-white'
                      }`}>
                        <MathText text={item.question} />
                      </h2>
                    </div>

                    <div className="flex items-center space-x-2 shrink-0 pt-1">
                      {/* Mark as Mastered button */}
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          toggleCompleted(qKey);
                        }}
                        className={`p-1.5 rounded-lg border transition ${
                          isDone 
                            ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40' 
                            : 'bg-slate-800 text-slate-400 hover:text-slate-200 border-slate-700'
                        }`}
                        title={isDone ? 'Mark as Incomplete' : 'Mark question as Mastered'}
                      >
                        <CheckCircle2 className={`w-4 h-4 ${isDone ? 'fill-emerald-400/20 text-emerald-400' : ''}`} />
                      </button>

                      {/* Bookmark button */}
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          toggleBookmark({
                            id: qKey,
                            type: 'interview',
                            title: item.question,
                            subtitle: `${item.category} • ${item.difficulty}`,
                            link: `/interview?search=${encodeURIComponent(item.question.slice(0, 30))}`
                          });
                        }}
                        className={`p-1.5 rounded-lg border transition ${
                          isSaved 
                            ? 'bg-amber-500/20 text-amber-300 border-amber-500/40' 
                            : 'bg-slate-800 text-slate-400 hover:text-slate-200 border-slate-700'
                        }`}
                        title={isSaved ? 'Remove Bookmark' : 'Bookmark question'}
                      >
                        <Bookmark className={`w-4 h-4 ${isSaved ? 'fill-amber-400 text-amber-400' : ''}`} />
                      </button>

                      {/* Copy Question & Answer */}
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          handleCopy(item);
                        }}
                        title="Copy Question & Answer"
                        className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 border border-slate-700 transition"
                      >
                        {copiedId === item.id ? (
                          <Check className="w-4 h-4 text-emerald-400" />
                        ) : (
                          <Copy className="w-4 h-4" />
                        )}
                      </button>

                      <div className="text-slate-400 pl-1">
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
                          <MathText text={item.answer} />
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

            {/* Load More Pagination */}
            {visibleCount < filteredQuestions.length && (
              <div className="flex flex-col sm:flex-row items-center justify-center gap-3 pt-6 pb-4">
                <button
                  onClick={() => setVisibleCount((prev) => Math.min(prev + 50, filteredQuestions.length))}
                  className="px-6 py-2.5 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-semibold text-xs sm:text-sm shadow-lg shadow-purple-600/30 transition flex items-center gap-2 cursor-pointer"
                >
                  <span>Load More Questions (Showing {displayedQuestions.length} of {filteredQuestions.length})</span>
                  <ChevronDown className="w-4 h-4" />
                </button>
                <button
                  onClick={() => setVisibleCount(filteredQuestions.length)}
                  className="px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-medium text-xs border border-slate-700 transition cursor-pointer"
                >
                  Show All ({filteredQuestions.length})
                </button>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
