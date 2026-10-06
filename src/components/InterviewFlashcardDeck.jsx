import React, { useState, useEffect, useCallback } from 'react';
import { 
  RotateCw, 
  ChevronLeft, 
  ChevronRight, 
  Shuffle, 
  CheckCircle2, 
  Bookmark, 
  Sparkles, 
  Lightbulb, 
  Layers, 
  Flame, 
  Check, 
  HelpCircle,
  Keyboard,
  Award
} from 'lucide-react';
import { MathText } from './KaTeXRenderer';
import { useProgress } from '../context/ProgressContext';
import AudioExplainerButton from './AudioExplainerButton';

export default function InterviewFlashcardDeck({ 
  questions = [], 
  onClose,
  getDifficultyBadge
}) {
  const { toggleCompleted, isCompleted, toggleBookmark, isBookmarked } = useProgress();
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);
  const [sessionReviewed, setSessionReviewed] = useState(new Set());
  const [sessionMastered, setSessionMastered] = useState(new Set());

  const total = questions.length;
  const currentCard = questions[currentIndex] || questions[0];
  const qKey = currentCard ? `interview-${currentCard.id}` : '';
  const isCardDone = currentCard ? isCompleted(qKey) : false;
  const isCardSaved = currentCard ? isBookmarked(qKey) : false;

  // Navigation handlers
  const handleNext = useCallback(() => {
    setIsFlipped(false);
    if (total > 0) {
      setCurrentIndex(prev => (prev + 1) % total);
    }
  }, [total]);

  const handlePrev = useCallback(() => {
    setIsFlipped(false);
    if (total > 0) {
      setCurrentIndex(prev => (prev - 1 + total) % total);
    }
  }, [total]);

  const handleShuffle = useCallback(() => {
    setIsFlipped(false);
    if (total > 0) {
      setCurrentIndex(Math.floor(Math.random() * total));
    }
  }, [total]);

  // Active Recall Spaced Repetition Grading
  const handleGrade = useCallback((grade) => {
    if (!currentCard) return;

    setSessionReviewed(prev => new Set(prev).add(currentCard.id));

    if (grade === 'easy') {
      if (!isCardDone) toggleCompleted(qKey);
      setSessionMastered(prev => new Set(prev).add(currentCard.id));
      handleNext();
    } else if (grade === 'medium') {
      handleNext();
    } else if (grade === 'hard') {
      // Keep in queue or notify
      handleNext();
    }
  }, [currentCard, isCardDone, toggleCompleted, qKey, handleNext]);

  // Global Keyboard Navigation
  useEffect(() => {
    const handleKeyDown = (e) => {
      // Ignore if typing in an input
      if (['INPUT', 'TEXTAREA'].includes(e.target.tagName)) return;

      if (e.code === 'Space' || e.key === 'Enter') {
        e.preventDefault();
        setIsFlipped(prev => !prev);
      } else if (e.key === 'ArrowRight' || e.key === 'j') {
        e.preventDefault();
        handleNext();
      } else if (e.key === 'ArrowLeft' || e.key === 'k') {
        e.preventDefault();
        handlePrev();
      } else if (e.key === 's' || e.key === 'S') {
        e.preventDefault();
        handleShuffle();
      } else if (e.key === '1') {
        handleGrade('hard');
      } else if (e.key === '2') {
        handleGrade('medium');
      } else if (e.key === '3') {
        handleGrade('easy');
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [handleNext, handlePrev, handleShuffle, handleGrade]);

  if (!currentCard || total === 0) {
    return (
      <div className="p-8 text-center bg-slate-900/80 rounded-2xl border border-slate-800 text-slate-400">
        No questions match the current filter selection. Adjust filters to practice flashcards!
      </div>
    );
  }

  const qLen = currentCard?.question?.length || 0;
  const questionSizeClass = qLen > 280 
    ? 'text-sm sm:text-base md:text-lg' 
    : qLen > 140 
    ? 'text-base sm:text-lg md:text-xl' 
    : 'text-lg sm:text-xl md:text-2xl';

  return (
    <div className="space-y-4">
      {/* Session Progress & Controls Bar */}
      <div className="flex flex-wrap items-center justify-between gap-3 bg-slate-900/80 border border-slate-800 rounded-2xl px-5 py-3 text-xs">
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-1.5 text-purple-300 font-semibold font-mono">
            <Layers className="w-4 h-4 text-purple-400" />
            <span>Card {currentIndex + 1} of {total}</span>
          </div>
          <div className="hidden sm:flex items-center gap-2 text-slate-400">
            <span>Reviewed: <strong className="text-white font-mono">{sessionReviewed.size}</strong></span>
            <span>&bull;</span>
            <span>Mastered: <strong className="text-emerald-400 font-mono">{sessionMastered.size}</strong></span>
          </div>
        </div>

        {/* Shuffle & Quick Action Buttons */}
        <div className="flex items-center gap-2">
          <button
            onClick={handleShuffle}
            className="p-1.5 px-2.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white border border-slate-700 transition flex items-center gap-1.5 text-[11px] font-medium"
            title="Shuffle deck randomly (Shortcut: S)"
          >
            <Shuffle className="w-3.5 h-3.5 text-indigo-400" />
            <span className="hidden sm:inline">Shuffle</span>
          </button>

          {/* Audio Flashcard Explainer with Male / Female Voices */}
          {currentCard && (
            <AudioExplainerButton
              title={`Question ${currentIndex + 1}`}
              text={isFlipped
                ? `Question: ${currentCard.question}. Answer: ${currentCard.answer}. ${currentCard.tip ? 'Tip: ' + currentCard.tip : ''}`
                : `Question: ${currentCard.question}. Flip card to reveal and listen to the complete answer.`
              }
              label={isFlipped ? "Listen Answer" : "Listen Question"}
              variant="compact"
            />
          )}

          <button
            onClick={() => toggleBookmark({
              id: qKey,
              type: 'interview',
              title: currentCard.question,
              subtitle: `${currentCard.category} • ${currentCard.difficulty}`,
              link: `/interview?search=${encodeURIComponent(currentCard.question.slice(0, 30))}`
            })}
            className={`p-1.5 px-2.5 rounded-lg border transition flex items-center gap-1.5 text-[11px] font-medium ${
              isCardSaved
                ? 'bg-amber-500/20 text-amber-300 border-amber-500/40'
                : 'bg-slate-800 text-slate-400 hover:text-white border-slate-700'
            }`}
            title="Bookmark card"
          >
            <Bookmark className={`w-3.5 h-3.5 ${isCardSaved ? 'fill-amber-400 text-amber-400' : ''}`} />
            <span className="hidden sm:inline">{isCardSaved ? 'Saved' : 'Save'}</span>
          </button>

          <button
            onClick={() => toggleCompleted(qKey)}
            className={`p-1.5 px-2.5 rounded-lg border transition flex items-center gap-1.5 text-[11px] font-medium ${
              isCardDone
                ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40'
                : 'bg-slate-800 text-slate-400 hover:text-white border-slate-700'
            }`}
            title="Mark question mastered"
          >
            <CheckCircle2 className={`w-3.5 h-3.5 ${isCardDone ? 'text-emerald-400' : ''}`} />
            <span className="hidden sm:inline">{isCardDone ? 'Mastered' : 'Mark Done'}</span>
          </button>
        </div>
      </div>

      {/* 3D FLIP CONTAINER */}
      <div className="perspective-1200 w-full min-h-[480px] sm:min-h-[520px]">
        <div 
          onClick={() => setIsFlipped(!isFlipped)}
          className={`relative w-full min-h-[480px] sm:min-h-[520px] transform-style-3d transition-transform duration-500 cursor-pointer rounded-3xl ${
            isFlipped ? 'rotate-y-180' : ''
          }`}
        >
          {/* ========================================================= */}
          {/* FRONT FACE: QUESTION */}
          {/* ========================================================= */}
          <div className="absolute inset-0 backface-hidden bg-slate-900 border border-purple-500/30 hover:border-purple-500/60 rounded-3xl p-5 sm:p-7 shadow-2xl flex flex-col justify-between select-none transition-all overflow-hidden">
            {/* Front Header */}
            <div className="flex items-center justify-between border-b border-slate-800 pb-3 shrink-0">
              <div className="flex items-center gap-2 flex-wrap">
                <span className="px-2 py-0.5 rounded-md bg-purple-500/20 text-purple-300 border border-purple-500/30 text-xs font-mono font-bold">
                  #{currentIndex + 1}
                </span>
                <span className="px-2.5 py-0.5 rounded-full bg-slate-800 text-slate-300 text-xs font-semibold uppercase tracking-wider">
                  {currentCard.category_label || currentCard.category}
                </span>
                <span className={`text-[11px] px-2.5 py-0.5 rounded-full border ${getDifficultyBadge(currentCard.difficulty)}`}>
                  {currentCard.difficulty}
                </span>
                {currentCard.experience_level && (
                  <span className={`text-[11px] px-2.5 py-0.5 rounded-full border ${
                    currentCard.experience_level === '0-2'
                      ? 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30'
                      : currentCard.experience_level === '2-5'
                      ? 'bg-blue-500/15 text-blue-300 border-blue-500/30'
                      : 'bg-purple-500/15 text-purple-300 border-purple-500/30'
                  }`}>
                    {currentCard.experience_level === '0-2' ? '🌱 0–2 Yrs' : currentCard.experience_level === '2-5' ? '🚀 2–5 Yrs' : '🏛️ 6+ Yrs'}
                  </span>
                )}
              </div>

              {isCardDone && (
                <span className="px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-[11px] font-semibold flex items-center gap-1 font-mono">
                  <Check className="w-3 h-3 text-emerald-400" />
                  Mastered
                </span>
              )}
            </div>

            {/* Front Question Body */}
            <div 
              onClick={(e) => {
                if (window.getSelection()?.toString()?.length > 0) {
                  e.stopPropagation();
                }
              }}
              className="flex-1 overflow-y-auto my-2 py-3 text-center flex flex-col items-center justify-center space-y-3.5 max-w-4xl w-full mx-auto scrollbar-thin px-2"
            >
              <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-purple-500/10 text-purple-400 border border-purple-500/20 text-[11px] font-semibold uppercase tracking-wider shrink-0">
                <HelpCircle className="w-3.5 h-3.5" />
                Technical Interview Question
              </span>

              <h2 className={`${questionSizeClass} font-bold text-white leading-relaxed tracking-normal max-w-3xl`}>
                <MathText text={currentCard.question} />
              </h2>

              {/* Company Tags */}
              {currentCard.company_tags && currentCard.company_tags.length > 0 && (
                <div className="flex flex-wrap justify-center gap-1.5 pt-1 shrink-0">
                  {currentCard.company_tags.map((comp, idx) => (
                    <span 
                      key={idx}
                      className="px-2 py-0.5 rounded-md bg-slate-950 text-indigo-300 border border-slate-800 text-[10px] font-mono"
                    >
                      {comp}
                    </span>
                  ))}
                </div>
              )}
            </div>

            {/* Front Footer Prompt */}
            <div className="flex items-center justify-between border-t border-slate-800/80 pt-3 text-slate-400 text-xs shrink-0">
              <span className="flex items-center gap-1.5 text-purple-400 font-medium">
                <RotateCw className="w-3.5 h-3.5 animate-spin-slow" />
                Click card or press [Space] to flip
              </span>
              <span className="hidden sm:inline-block font-mono text-[11px] text-slate-500">
                Shortcuts: [←] Prev &bull; [→] Next
              </span>
            </div>
          </div>

          {/* ========================================================= */}
          {/* BACK FACE: TECHNICAL ANSWER & PROOFS */}
          {/* ========================================================= */}
          <div className="absolute inset-0 backface-hidden rotate-y-180 bg-slate-900 border border-emerald-500/40 rounded-3xl p-5 sm:p-7 shadow-2xl flex flex-col justify-between transition-all overflow-hidden">
            {/* Back Header */}
            <div className="flex items-center justify-between border-b border-slate-800 pb-3 shrink-0">
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                <span className="text-xs font-bold text-emerald-400 uppercase tracking-wider">
                  Technical Answer & Mathematical Derivation
                </span>
              </div>
              <span className="text-[11px] text-slate-400 font-mono">
                Click to flip back [Space]
              </span>
            </div>

            {/* Back Answer Body */}
            <div 
              onClick={(e) => e.stopPropagation()} 
              className="flex-1 overflow-y-auto my-2 py-2 pr-2 space-y-3 cursor-text text-slate-200 text-xs sm:text-sm leading-relaxed scrollbar-thin"
            >
              <div className="whitespace-pre-line">
                <MathText text={currentCard.answer} />
              </div>

              {currentCard.tip && (
                <div className="p-3 rounded-xl bg-amber-950/20 border border-amber-500/30 text-xs text-amber-200/90 flex items-start gap-2.5 mt-2">
                  <Lightbulb className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
                  <div>
                    <strong className="block text-amber-300 font-semibold mb-0.5">Interviewer Tip:</strong>
                    <span>{currentCard.tip}</span>
                  </div>
                </div>
              )}
            </div>

            {/* Back Active Recall Grading Bar */}
            <div 
              onClick={(e) => e.stopPropagation()} 
              className="border-t border-slate-800/80 pt-3 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs shrink-0"
            >
              <span className="font-semibold text-slate-400 text-[11px] uppercase tracking-wider">
                Rate Your Recall:
              </span>

              <div className="flex items-center gap-2 w-full sm:w-auto">
                <button
                  onClick={() => handleGrade('hard')}
                  className="flex-1 sm:flex-initial px-3.5 py-1.5 rounded-xl bg-rose-500/15 hover:bg-rose-500/25 text-rose-300 border border-rose-500/40 font-semibold transition flex items-center justify-center gap-1.5"
                  title="Needs more practice (Press 1)"
                >
                  <span>Hard [1]</span>
                </button>

                <button
                  onClick={() => handleGrade('medium')}
                  className="flex-1 sm:flex-initial px-3.5 py-1.5 rounded-xl bg-amber-500/15 hover:bg-amber-500/25 text-amber-300 border border-amber-500/40 font-semibold transition flex items-center justify-center gap-1.5"
                  title="Understood moderately (Press 2)"
                >
                  <span>Good [2]</span>
                </button>

                <button
                  onClick={() => handleGrade('easy')}
                  className="flex-1 sm:flex-initial px-3.5 py-1.5 rounded-xl bg-emerald-500/20 hover:bg-emerald-500/30 text-emerald-300 border border-emerald-500/40 font-semibold transition flex items-center justify-center gap-1.5 shadow-sm"
                  title="Mastered! (Press 3)"
                >
                  <Award className="w-3.5 h-3.5 text-emerald-400" />
                  <span>Mastered [3]</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Navigation Controls Below Card */}
      <div className="flex items-center justify-between pt-1">
        <button
          onClick={handlePrev}
          className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-medium text-xs flex items-center gap-1.5 border border-slate-700 transition"
        >
          <ChevronLeft className="w-4 h-4" />
          <span>Previous</span>
        </button>

        <div className="flex items-center gap-1.5 text-[11px] text-slate-500 font-mono">
          <Keyboard className="w-3.5 h-3.5 text-slate-400" />
          <span className="hidden sm:inline">Use Arrow keys &bull; Space to Flip &bull; 1/2/3 to Grade</span>
        </div>

        <button
          onClick={handleNext}
          className="px-5 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-semibold text-xs flex items-center gap-1.5 shadow-lg shadow-purple-600/25 transition"
        >
          <span>Next Card</span>
          <ChevronRight className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}
