import React from 'react';
import { Link } from 'react-router-dom';
import { X, ExternalLink, Lightbulb, Calculator, Sparkles, BookOpen, Layers, ArrowUpRight } from 'lucide-react';
import KaTeXRenderer, { MathText } from './KaTeXRenderer';
import { findConceptForSubtopic } from '../utils/conceptLookup';

export default function NodeInspector({ node, crossLinks = [], onClose, onSelectNode }) {
  if (!node) return null;

  const relevantLinks = crossLinks.filter(
    (l) => l.from === node.id || l.to === node.id
  );

  const getCategoryColor = (cat) => {
    switch (cat) {
      case 'math': return 'text-blue-400 bg-blue-500/10 border-blue-500/30';
      case 'data': return 'text-emerald-400 bg-emerald-500/10 border-emerald-500/30';
      case 'ml': return 'text-purple-400 bg-purple-500/10 border-purple-500/30';
      case 'eval': return 'text-amber-400 bg-amber-500/10 border-amber-500/30';
      case 'dl': return 'text-pink-400 bg-pink-500/10 border-pink-500/30';
      case 'genai': return 'text-indigo-400 bg-indigo-500/10 border-indigo-500/30';
      case 'mlops': return 'text-cyan-400 bg-cyan-500/10 border-cyan-500/30';
      default: return 'text-slate-300 bg-slate-800 border-slate-700';
    }
  };

  return (
    <aside
      className="fixed inset-y-0 right-0 z-40 w-full sm:w-[460px] md:w-[520px] bg-slate-900/95 backdrop-blur-xl border-l border-slate-800 shadow-2xl flex flex-col transform transition-transform duration-300 ease-in-out"
      aria-label="Node Inspector"
    >
      {/* Header */}
      <div className="p-4 sm:p-5 border-b border-slate-800 flex items-start justify-between gap-3 bg-slate-950/40">
        <div>
          <span
            className={`inline-block px-2.5 py-0.5 rounded-full text-[11px] font-semibold tracking-wider uppercase border mb-2 ${getCategoryColor(
              node.category
            )}`}
          >
            {node.category?.toUpperCase() || 'TOPIC'}
          </span>
          <h2 className="text-lg sm:text-xl font-bold text-white tracking-tight leading-snug">
            {node.label}
          </h2>
        </div>
        <button
          onClick={onClose}
          className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition"
          title="Close Inspector"
        >
          <X className="w-5 h-5" />
        </button>
      </div>

      {/* Body Content */}
      <div className="flex-1 overflow-y-auto p-4 sm:p-5 space-y-5 text-sm">
        {/* 1. Formal Definition */}
        {node.def && (
          <div className="bg-slate-950/60 rounded-xl p-4 border border-slate-800/80">
            <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1.5 flex items-center gap-1.5">
              <BookOpen className="w-3.5 h-3.5 text-indigo-400" />
              1. Formal Definition
            </h3>
            <p className="text-slate-200 leading-relaxed">
              <MathText text={node.def} />
            </p>
          </div>
        )}

        {/* 2. Mathematical Formula */}
        {node.formula && (
          <div className="bg-slate-950/80 rounded-xl p-4 border border-indigo-500/25">
            <h3 className="text-xs font-semibold text-indigo-300 uppercase tracking-wider mb-2 flex items-center gap-1.5">
              <Calculator className="w-3.5 h-3.5 text-indigo-400" />
              2. Core Mathematical Formulation
            </h3>
            <div className="py-2 px-1 overflow-x-auto bg-slate-900/90 rounded-lg border border-slate-800">
              <KaTeXRenderer math={node.formula} block={true} />
            </div>
          </div>
        )}

        {/* 3. Intuition & Logic */}
        {node.logic && (
          <div className="bg-amber-950/20 rounded-xl p-4 border border-amber-500/25">
            <h3 className="text-xs font-semibold text-amber-400 uppercase tracking-wider mb-1.5 flex items-center gap-1.5">
              <Lightbulb className="w-3.5 h-3.5 text-amber-400" />
              3. Intuition & When to Use
            </h3>
            <p className="text-amber-100/90 leading-relaxed">
              <MathText text={node.logic} />
            </p>
          </div>
        )}

        {/* 4. Real-World Practical Example */}
        {node.example && (
          <div className="bg-emerald-950/20 rounded-xl p-4 border border-emerald-500/25">
            <h3 className="text-xs font-semibold text-emerald-400 uppercase tracking-wider mb-1.5 flex items-center gap-1.5">
              <Sparkles className="w-3.5 h-3.5 text-emerald-400" />
              4. Real-World Practical Example
            </h3>
            <p className="text-emerald-100/90 leading-relaxed">
              <MathText text={node.example} />
            </p>
          </div>
        )}

        {/* 5. Subtopics Breakdown */}
        {node.subtopics && node.subtopics.length > 0 && (
          <div>
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
                <Layers className="w-3.5 h-3.5 text-slate-400" />
                Key Subtopics & Architectural Components ({node.subtopics.length})
              </h3>
              <span className="text-[11px] text-indigo-400 font-medium hidden sm:inline">
                Click to explore &rarr;
              </span>
            </div>
            <div className="flex flex-wrap gap-2">
              {node.subtopics.map((sub, idx) => {
                const concept = findConceptForSubtopic(sub, node.id);
                const targetUrl = concept
                  ? `/concepts?id=${encodeURIComponent(concept.id)}`
                  : `/concepts?search=${encodeURIComponent(sub)}`;

                return (
                  <Link
                    key={idx}
                    to={targetUrl}
                    className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-800/80 hover:bg-indigo-600/20 text-slate-200 hover:text-indigo-300 border border-slate-700/60 hover:border-indigo-500/50 transition-all duration-150 group shadow-sm"
                    title={`View full explanation, formulas & examples for "${sub}"`}
                  >
                    <span>{sub}</span>
                    <ArrowUpRight className="w-3 h-3 text-slate-400 group-hover:text-indigo-300 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform shrink-0" />
                  </Link>
                );
              })}
            </div>
          </div>
        )}

        {/* 6. Inter-domain Connections */}
        {relevantLinks.length > 0 && (
          <div>
            <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2 flex items-center gap-1.5">
              <ExternalLink className="w-3.5 h-3.5 text-slate-400" />
              Cross-Domain Knowledge Links ({relevantLinks.length})
            </h3>
            <div className="space-y-2">
              {relevantLinks.map((link, idx) => {
                const targetId = link.from === node.id ? link.to : link.from;
                const direction = link.from === node.id ? 'Outgoing' : 'Incoming';

                return (
                  <div
                    key={idx}
                    onClick={() => onSelectNode && onSelectNode(targetId)}
                    className="p-2.5 rounded-lg bg-slate-950/60 hover:bg-indigo-950/30 border border-slate-800 hover:border-indigo-500/40 cursor-pointer transition flex items-center justify-between group"
                  >
                    <div>
                      <span className="text-[10px] font-semibold uppercase text-slate-400 tracking-wider">
                        {direction}: {link.label}
                      </span>
                      <p className="text-xs font-medium text-slate-200 group-hover:text-indigo-300 transition-colors">
                        &rarr; {targetId}
                      </p>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="p-3 border-t border-slate-800 bg-slate-950/60 text-center">
        <p className="text-[11px] text-slate-400">
          Tip: Click any linked node or drag & zoom the mind map canvas anytime.
        </p>
      </div>
    </aside>
  );
}
