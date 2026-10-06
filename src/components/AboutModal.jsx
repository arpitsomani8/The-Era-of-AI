import React, { useEffect } from 'react';
import { X, Sparkles, Network, BookOpen, FileText, Briefcase, HelpCircle, Layers, ExternalLink, Github, Heart } from 'lucide-react';
import allNodesData from '../data/allNodes.json';
import topicsData from '../data/topics.json';
import conceptsData from '../data/concepts.json';
import papersData from '../data/papers.json';
import interviewData from '../data/interviewQuestions.json';
import projectsData from '../data/projects.json';
import AudioExplainerButton from './AudioExplainerButton';

export default function AboutModal({ isOpen, onClose }) {
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div 
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md animate-fadeIn"
      onClick={onClose}
    >
      <div 
        className="relative w-full max-w-2xl bg-slate-900 border border-slate-700/80 rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh] animate-scaleUp text-slate-100"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Hero Thumbnail Banner */}
        <div className="relative w-full h-48 sm:h-56 bg-slate-950 overflow-hidden shrink-0">
          <img 
            src={`${import.meta.env.BASE_URL}thumbnail.jpg`} 
            alt="The Era of AI Thumbnail Banner" 
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-slate-900 via-slate-900/40 to-transparent" />
          
          {/* Close button */}
          <button 
            onClick={onClose}
            aria-label="Close About Modal"
            className="absolute top-3 right-3 p-1.5 rounded-full bg-slate-900/80 hover:bg-slate-800 text-slate-300 hover:text-white border border-slate-700/60 transition shadow-lg"
          >
            <X className="w-5 h-5" />
          </button>

          {/* Floating Logo Badge */}
          <div className="absolute bottom-3 left-4 flex items-center gap-3">
            <div className="w-12 h-12 rounded-xl overflow-hidden shadow-xl ring-2 ring-indigo-500/40 bg-slate-950 shrink-0">
              <img 
                src={`${import.meta.env.BASE_URL}logo.png`} 
                alt="The Era of AI Logo" 
                className="w-full h-full object-cover"
              />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-extrabold text-lg text-white tracking-tight drop-shadow-md">
                  The Era of AI
                </span>
              </div>
              <p className="text-xs text-slate-300 drop-shadow">
                Master Knowledge Graph, Curriculum &amp; Research Portal
              </p>
            </div>
          </div>
        </div>

        {/* Modal Content Body */}
        <div className="p-6 overflow-y-auto space-y-6">
          {/* Description */}
          <div>
            <div className="flex items-center justify-between gap-2 mb-1 flex-wrap">
              <h3 className="text-sm font-semibold uppercase tracking-wider text-indigo-400">
                About The Project
              </h3>
              <AudioExplainerButton
                variant="compact"
                title="About The Era of AI"
                text={`About The Era of AI. The Era of AI is an open-source, production-grade knowledge architecture designed to bridge the gap between theoretical machine learning foundations and state-of-the-art modern generative AI systems. Featuring an interconnected graph of ${allNodesData.length} domain nodes, ${topicsData.length} structured syllabus modules, ${conceptsData.length} mathematical concept breakdowns, ${interviewData.length} interview questions, ${papersData.length} milestone research papers, and ${projectsData.length} production case studies.`}
              />
            </div>
            <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
              <strong>The Era of AI</strong> is an open-source, production-grade knowledge architecture designed to bridge the gap between theoretical machine learning foundations and state-of-the-art modern generative AI systems.
            </p>
          </div>

          {/* Stats Grid */}
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
            <div className="p-3 rounded-xl bg-slate-800/60 border border-slate-700/50 flex items-center gap-3">
              <div className="p-2 rounded-lg bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                <Network className="w-4 h-4" />
              </div>
              <div>
                <div className="text-base font-bold text-white">{allNodesData.length}</div>
                <div className="text-[11px] text-slate-400">Graph Nodes</div>
              </div>
            </div>

            <div className="p-3 rounded-xl bg-slate-800/60 border border-slate-700/50 flex items-center gap-3">
              <div className="p-2 rounded-lg bg-blue-500/10 text-blue-400 border border-blue-500/20">
                <BookOpen className="w-4 h-4" />
              </div>
              <div>
                <div className="text-base font-bold text-white">{topicsData.length}</div>
                <div className="text-[11px] text-slate-400">Syllabus Modules</div>
              </div>
            </div>

            <div className="p-3 rounded-xl bg-slate-800/60 border border-slate-700/50 flex items-center gap-3">
              <div className="p-2 rounded-lg bg-rose-500/10 text-rose-400 border border-rose-500/20">
                <Layers className="w-4 h-4" />
              </div>
              <div>
                <div className="text-base font-bold text-white">{conceptsData.length}</div>
                <div className="text-[11px] text-slate-400">Core Concepts</div>
              </div>
            </div>

            <div className="p-3 rounded-xl bg-slate-800/60 border border-slate-700/50 flex items-center gap-3">
              <div className="p-2 rounded-lg bg-purple-500/10 text-purple-400 border border-purple-500/20">
                <HelpCircle className="w-4 h-4" />
              </div>
              <div>
                <div className="text-base font-bold text-white">{interviewData.length}+</div>
                <div className="text-[11px] text-slate-400">Interview Vault</div>
              </div>
            </div>

            <div className="p-3 rounded-xl bg-slate-800/60 border border-slate-700/50 flex items-center gap-3">
              <div className="p-2 rounded-lg bg-amber-500/10 text-amber-400 border border-amber-500/20">
                <FileText className="w-4 h-4" />
              </div>
              <div>
                <div className="text-base font-bold text-white">{papersData.length}</div>
                <div className="text-[11px] text-slate-400">Landmark Papers</div>
              </div>
            </div>

            <div className="p-3 rounded-xl bg-slate-800/60 border border-slate-700/50 flex items-center gap-3">
              <div className="p-2 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                <Briefcase className="w-4 h-4" />
              </div>
              <div>
                <div className="text-base font-bold text-white">{projectsData.length}</div>
                <div className="text-[11px] text-slate-400">Case Studies</div>
              </div>
            </div>
          </div>

          {/* Key Features List */}
          <div className="space-y-2">
            <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400">
              Core Capabilities
            </h4>
            <ul className="text-xs text-slate-300 space-y-1.5 list-disc list-inside">
              <li>Interactive SVG Mind Map with physics-inspired hierarchy and cross-domain links</li>
              <li>Multi-Theme Support: Default Theme, OLED Dark, Bright Day &amp; Metallic Green</li>
              <li>KaTeX Math Engine rendering inline and block mathematical formulas</li>
              <li>Curated library of breakthrough AI publications and frontier research</li>
            </ul>
          </div>
        </div>

        {/* Modal Footer */}
        <div className="px-6 py-3 bg-slate-950/80 border-t border-slate-800 flex flex-wrap items-center justify-between gap-3 text-xs text-slate-400">
          <div className="flex items-center gap-1.5">
            <span>Built with passion by</span>
            <span className="font-semibold text-slate-200">Arpit Somani</span>
          </div>

          <a
            href="https://github.com/arpitsomani8/The-Era-of-AI"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-medium transition shadow-sm"
          >
            <Github className="w-3.5 h-3.5" />
            <span>GitHub Repository</span>
            <ExternalLink className="w-3 h-3 ml-0.5" />
          </a>
        </div>
      </div>
    </div>
  );
}
