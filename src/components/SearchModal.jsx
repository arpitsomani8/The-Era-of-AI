import React, { useState, useEffect, useMemo, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, X, BookOpen, FileText, Briefcase, HelpCircle, Layers, ArrowRight } from 'lucide-react';
import conceptsData from '../data/concepts.json';
import papersData from '../data/papers.json';
import projectsData from '../data/projects.json';
import interviewData from '../data/interviewQuestions.json';
import topicsData from '../data/topics.json';

export default function SearchModal({ isOpen, onClose }) {
  const [query, setQuery] = useState('');
  const inputRef = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (isOpen) {
      setTimeout(() => inputRef.current?.focus(), 50);
    } else {
      setQuery('');
    }
  }, [isOpen]);

  useEffect(() => {
    const handleKeyDown = (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        if (isOpen) onClose();
        else onClose(false); // will be handled by parent toggle
      }
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  const searchResults = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return [];

    const results = [];

    // Search Concepts (274)
    for (const c of conceptsData) {
      if (
        c.title?.toLowerCase().includes(q) ||
        c.def?.toLowerCase().includes(q) ||
        c.logic?.toLowerCase().includes(q) ||
        c.category_label?.toLowerCase().includes(q)
      ) {
        results.push({
          type: 'concept',
          title: c.title,
          subtitle: c.category_label || c.category,
          desc: c.def,
          target: `/concepts?id=${encodeURIComponent(c.id)}`,
          icon: Layers,
          color: 'text-rose-400 bg-rose-500/10'
        });
        if (results.length >= 25) break;
      }
    }

    // Search Papers (22)
    for (const p of papersData) {
      if (
        p.title?.toLowerCase().includes(q) ||
        p.authors?.toLowerCase().includes(q) ||
        p.breakthrough?.toLowerCase().includes(q) ||
        p.category?.toLowerCase().includes(q)
      ) {
        results.push({
          type: 'paper',
          title: p.title,
          subtitle: `${p.year} • ${p.authors}`,
          desc: p.breakthrough,
          target: `/papers?search=${encodeURIComponent(p.title)}`,
          icon: FileText,
          color: 'text-amber-400 bg-amber-500/10'
        });
        if (results.length >= 25) break;
      }
    }

    // Search Interview Questions (150)
    for (const i of interviewData) {
      if (
        i.question?.toLowerCase().includes(q) ||
        i.category?.toLowerCase().includes(q) ||
        i.short_answer?.toLowerCase().includes(q)
      ) {
        results.push({
          type: 'interview',
          title: i.question,
          subtitle: `${i.category} • ${i.difficulty}`,
          desc: i.short_answer,
          target: `/interview?search=${encodeURIComponent(i.question.slice(0, 30))}`,
          icon: HelpCircle,
          color: 'text-purple-400 bg-purple-500/10'
        });
        if (results.length >= 35) break;
      }
    }

    // Search Case Studies (5)
    for (const proj of projectsData) {
      if (
        proj.title?.toLowerCase().includes(q) ||
        proj.company?.toLowerCase().includes(q) ||
        proj.architecture?.toLowerCase().includes(q)
      ) {
        results.push({
          type: 'project',
          title: proj.title,
          subtitle: proj.company,
          desc: proj.business_problem || proj.impact,
          target: `/projects?search=${encodeURIComponent(proj.company || proj.title)}`,
          icon: Briefcase,
          color: 'text-emerald-400 bg-emerald-500/10'
        });
      }
    }

    // Search Topics (34)
    for (const t of topicsData) {
      if (
        t.label?.toLowerCase().includes(q) ||
        t.def?.toLowerCase().includes(q)
      ) {
        results.push({
          type: 'syllabus',
          title: t.label,
          subtitle: `Domain: ${t.category}`,
          desc: t.def,
          target: `/syllabus?topic=${t.id}`,
          icon: BookOpen,
          color: 'text-indigo-400 bg-indigo-500/10'
        });
      }
    }

    return results.slice(0, 30);
  }, [query]);

  if (!isOpen) return null;

  const handleSelect = (target) => {
    navigate(target);
    onClose();
  };

  return (
    <div 
      className="fixed inset-0 z-50 flex items-start justify-center pt-16 sm:pt-24 px-4 bg-slate-950/80 backdrop-blur-md cursor-pointer animate-in fade-in duration-150"
      onClick={onClose}
    >
      <div 
        className="w-full max-w-2xl bg-slate-900 border border-slate-700/80 rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[80vh] animate-in fade-in zoom-in-95 duration-150 cursor-default"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Search Input Bar */}
        <div className="flex items-center px-4 py-3.5 border-b border-slate-800 bg-slate-950/50">
          <Search className="w-5 h-5 text-indigo-400 shrink-0 mr-3" />
          <input
            ref={inputRef}
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder={`Search all ${conceptsData.length} concepts, ${interviewData.length}+ questions, ${papersData.length} papers, architectures...`}
            className="flex-1 bg-transparent text-sm sm:text-base text-white placeholder-slate-500 focus:outline-none"
          />
          {query && (
            <button
              onClick={() => {
                setQuery('');
                inputRef.current?.focus();
              }}
              className="p-1 rounded-full text-slate-400 hover:text-white hover:bg-slate-800 transition mr-1.5"
              title="Clear search text"
            >
              <X className="w-3.5 h-3.5" />
            </button>
          )}
          <button
            onClick={onClose}
            className="p-1.5 rounded-xl text-slate-400 hover:text-white hover:bg-slate-800 transition border border-slate-700/70 ml-1 flex items-center justify-center cursor-pointer shadow-sm active:scale-95"
            title="Close Search (Escape)"
            aria-label="Close search"
          >
            <X className="w-4 h-4 text-slate-300" />
          </button>
        </div>

        {/* Results List */}
        <div className="flex-1 overflow-y-auto p-2 divide-y divide-slate-800/40">
          {query && searchResults.length === 0 && (
            <div className="p-8 text-center text-slate-400 text-sm">
              No results found for &ldquo;<span className="text-white font-medium">{query}</span>&rdquo;.
              <p className="text-xs text-slate-500 mt-1">
                Try searching for concepts like <em>Backpropagation</em>, <em>LoRA</em>, <em>Attention</em>, <em>Eigenvalues</em>, or <em>XGBoost</em>.
              </p>
            </div>
          )}

          {!query && (
            <div className="p-6 text-center text-slate-400 text-xs">
              <p className="font-semibold text-slate-300 text-sm mb-2">Universal AI Knowledge Search</p>
              <div className="flex flex-wrap items-center justify-center gap-2 mt-3">
                {['LoRA', 'AdamW', 'Attention', 'Diffusion', 'Transformer', 'ROC-AUC', 'Cross-Entropy', 'Vector DB', 'SMOTE', 'RLHF'].map((tag) => (
                  <button
                    key={tag}
                    onClick={() => setQuery(tag)}
                    className="px-2.5 py-1 rounded-lg bg-slate-800/80 hover:bg-indigo-600/30 text-slate-300 hover:text-indigo-200 border border-slate-700/60 transition text-xs"
                  >
                    {tag}
                  </button>
                ))}
              </div>
            </div>
          )}

          {searchResults.map((item, idx) => {
            const Icon = item.icon;
            return (
              <div
                key={idx}
                onClick={() => handleSelect(item.target)}
                className="p-3 rounded-xl hover:bg-slate-800/70 cursor-pointer transition flex items-center justify-between gap-3 group"
              >
                <div className="flex items-start gap-3 min-w-0">
                  <div className={`p-2 rounded-lg shrink-0 mt-0.5 ${item.color}`}>
                    <Icon className="w-4 h-4" />
                  </div>
                  <div className="min-w-0">
                    <div className="flex items-center gap-2">
                      <span className="font-semibold text-sm text-slate-100 group-hover:text-indigo-300 transition-colors truncate">
                        {item.title}
                      </span>
                      <span className="text-[10px] px-2 py-0.5 rounded-full bg-slate-800 text-slate-400 border border-slate-700 shrink-0">
                        {item.subtitle}
                      </span>
                    </div>
                    {item.desc && (
                      <p className="text-xs text-slate-400 line-clamp-1 mt-0.5">
                        {item.desc}
                      </p>
                    )}
                  </div>
                </div>
                <ArrowRight className="w-4 h-4 text-slate-500 group-hover:text-indigo-400 group-hover:translate-x-0.5 transition-all shrink-0" />
              </div>
            );
          })}
        </div>

        {/* Footer */}
        <div className="px-4 py-2 border-t border-slate-800 bg-slate-950/70 text-[11px] text-slate-500 flex items-center justify-between">
          <span>{searchResults.length} results matching</span>
          <span>Navigation: Click to jump directly</span>
        </div>
      </div>
    </div>
  );
}
