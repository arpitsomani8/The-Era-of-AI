import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { 
  Sparkles, 
  ArrowRight, 
  Network, 
  BookOpen, 
  FileText, 
  Briefcase, 
  HelpCircle, 
  Layers,
  PlayCircle,
  Zap,
  CheckCircle2,
  Compass
} from 'lucide-react';

export default function LandingHeroPage() {
  const navigate = useNavigate();

  const portalCards = [
    {
      to: '/mindmap',
      title: 'Interactive Mind Map',
      subtitle: '41 domain nodes & cross-domain links',
      icon: Network,
      color: 'from-indigo-500/20 to-indigo-600/10 border-indigo-500/30 text-indigo-400',
      badge: 'Interactive 2D Graph'
    },
    {
      to: '/syllabus',
      title: 'Line-Wise Syllabus',
      subtitle: '34 modules from linear algebra to GenAI',
      icon: BookOpen,
      color: 'from-blue-500/20 to-blue-600/10 border-blue-500/30 text-blue-400',
      badge: 'Core Curriculum'
    },
    {
      to: '/papers',
      title: 'Landmark Research Papers',
      subtitle: '22+ milestone papers with arXiv feeds',
      icon: FileText,
      color: 'from-amber-500/20 to-amber-600/10 border-amber-500/30 text-amber-400',
      badge: 'Daily arXiv'
    },
    {
      to: '/concepts',
      title: 'Core Concepts & Math',
      subtitle: '170+ in-depth technical breakdowns',
      icon: Layers,
      color: 'from-rose-500/20 to-rose-600/10 border-rose-500/30 text-rose-400',
      badge: 'Deep Derivations'
    },
    {
      to: '/interview',
      title: 'Interview Vault',
      subtitle: '150+ math, coding & design questions',
      icon: HelpCircle,
      color: 'from-purple-500/20 to-purple-600/10 border-purple-500/30 text-purple-400',
      badge: '150+ QA Vault'
    },
    {
      to: '/playgrounds',
      title: 'ML Playgrounds & Labs',
      subtitle: 'Attention heatmaps & Python sandbox',
      icon: PlayCircle,
      color: 'from-cyan-500/20 to-cyan-600/10 border-cyan-500/30 text-cyan-400',
      badge: 'WebAssembly Pyodide'
    }
  ];

  return (
    <div className="relative flex-1 w-full h-full overflow-y-auto bg-slate-950 text-slate-100 flex flex-col items-center justify-start select-none">
      {/* Background Ambient Glow & Blurred Thumbnail Atmosphere */}
      <div 
        className="fixed inset-0 pointer-events-none opacity-25 filter blur-3xl scale-110 bg-cover bg-center transition-opacity duration-1000"
        style={{ backgroundImage: `url(${import.meta.env.BASE_URL}thumbnail.jpg)` }}
      />
      <div className="fixed inset-0 pointer-events-none bg-gradient-to-b from-slate-950/80 via-slate-950/90 to-slate-950" />
      <div className="fixed inset-0 pointer-events-none bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(120,119,198,0.25),rgba(255,255,255,0))]" />

      {/* Main Hero Container */}
      <div className="relative z-10 w-full max-w-5xl mx-auto px-4 sm:px-6 py-8 sm:py-12 md:py-16 flex flex-col items-center text-center space-y-8">
        
        {/* Top Announcement Badge */}
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-indigo-500/10 border border-indigo-500/30 text-indigo-300 text-xs sm:text-sm font-semibold shadow-lg shadow-indigo-500/10 animate-fadeIn">
          <Sparkles className="w-4 h-4 text-amber-300 animate-pulse" />
          <span>The Era of AI — Master Knowledge Universe</span>
          <span className="hidden sm:inline text-indigo-400/60">•</span>
          <span className="hidden sm:inline text-[11px] text-indigo-300 font-mono">React 2026 Edition</span>
        </div>

        {/* Hero Title */}
        <div className="space-y-3 max-w-3xl">
          <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-black tracking-tight text-white leading-tight">
            The Era of <span className="bg-gradient-to-r from-indigo-400 via-purple-300 to-teal-300 bg-clip-text text-transparent">AI</span>
          </h1>
          <p className="text-base sm:text-lg md:text-xl text-slate-300 font-normal leading-relaxed max-w-2xl mx-auto">
            From foundational vector calculus to modern LLMs, diffusion mechanisms, and industrial production pipelines.
          </p>
        </div>

        {/* Thumbnail Showcase Frame */}
        <div className="relative w-full max-w-3xl rounded-2xl sm:rounded-3xl overflow-hidden border border-slate-700/80 shadow-2xl shadow-indigo-500/20 group transition-all duration-300 hover:border-indigo-500/50 bg-slate-900/80">
          <div className="relative aspect-[16/9] w-full overflow-hidden">
            <img 
              src={`${import.meta.env.BASE_URL}thumbnail.jpg`} 
              alt="The Era of AI Official Thumbnail"
              className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700 ease-out"
            />
            {/* Subtle Gradient Overlay */}
            <div className="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-950/20 to-transparent" />

            {/* Corner Badge */}
            <div className="absolute top-3 left-3 sm:top-4 sm:left-4 flex items-center gap-2 px-3 py-1 rounded-xl bg-slate-950/80 backdrop-blur-md border border-slate-700/60 text-xs font-semibold text-slate-200 shadow-md">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
              <span>Knowledge Portal</span>
            </div>

            {/* In-Card Center Enter Button Overlay */}
            <div className="absolute inset-0 flex items-center justify-center p-4">
              <button
                onClick={() => navigate('/mindmap')}
                id="hero-center-enter-btn"
                className="group/btn relative inline-flex items-center gap-3.5 px-7 sm:px-10 py-3.5 sm:py-5 rounded-2xl bg-gradient-to-r from-indigo-600 via-indigo-500 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-extrabold text-base sm:text-xl shadow-2xl shadow-indigo-600/70 hover:shadow-indigo-500/90 ring-4 ring-indigo-400/40 hover:ring-indigo-400/80 hover:scale-105 active:scale-95 transition-all duration-200 cursor-pointer"
              >
                <Sparkles className="w-5 h-5 sm:w-6 sm:h-6 text-amber-300 animate-bounce shrink-0" />
                <span className="tracking-wide drop-shadow-md">Enter the World of AI</span>
                <ArrowRight className="w-5 h-5 sm:w-6 sm:h-6 group-hover/btn:translate-x-1.5 transition-transform shrink-0 text-white" />
              </button>
            </div>

            {/* Bottom Caption inside Card */}
            <div className="absolute bottom-3 sm:bottom-4 inset-x-4 flex items-center justify-between text-[11px] sm:text-xs text-slate-300/80">
              <span className="hidden sm:inline">Explore 41 interactive nodes & line-wise curriculum</span>
              <span className="font-mono text-indigo-300">Click button above to enter &rarr;</span>
            </div>
          </div>
        </div>

        {/* Prominent Center Standalone Call to Action (Accessible below thumbnail) */}
        <div className="pt-2 flex flex-col items-center gap-3">
          <Link
            to="/mindmap"
            className="inline-flex items-center gap-3 px-8 py-4 rounded-2xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-base sm:text-lg shadow-xl shadow-indigo-600/40 hover:scale-105 active:scale-95 transition-all duration-200 border border-indigo-400/40"
          >
            <span>Launch Interactive Mind Map</span>
            <ArrowRight className="w-5 h-5" />
          </Link>
          <p className="text-xs text-slate-400">
            Or jump directly into any section below
          </p>
        </div>

        {/* Portal Quick Links Grid */}
        <div className="w-full max-w-4xl grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3.5 pt-4">
          {portalCards.map((portal, idx) => {
            const Icon = portal.icon;
            return (
              <Link
                key={idx}
                to={portal.to}
                className={`p-4 rounded-2xl bg-slate-900/70 hover:bg-slate-900 border transition-all duration-200 text-left flex flex-col justify-between group shadow-sm hover:shadow-md hover:scale-[1.02] ${portal.color}`}
              >
                <div>
                  <div className="flex items-center justify-between gap-2 mb-2">
                    <div className="w-8 h-8 rounded-lg bg-slate-800/80 flex items-center justify-center">
                      <Icon className="w-4 h-4" />
                    </div>
                    <span className="text-[10px] px-2 py-0.5 rounded-full font-semibold border bg-slate-800/90 text-slate-300 border-slate-700/60">
                      {portal.badge}
                    </span>
                  </div>
                  <h3 className="text-sm font-bold text-white group-hover:text-indigo-300 transition-colors">
                    {portal.title}
                  </h3>
                  <p className="text-xs text-slate-400 mt-1 leading-snug">
                    {portal.subtitle}
                  </p>
                </div>
                <div className="mt-3 pt-2 border-t border-slate-800/60 flex items-center justify-between text-[11px] font-medium text-slate-400 group-hover:text-white">
                  <span>Explore Section</span>
                  <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
                </div>
              </Link>
            );
          })}
        </div>

        {/* Key Curriculum Metrics Bar */}
        <div className="w-full max-w-3xl pt-6 border-t border-slate-800/80 flex items-center justify-around flex-wrap gap-4 text-center">
          <div>
            <div className="text-xl sm:text-2xl font-black text-white font-mono">41</div>
            <div className="text-[11px] text-slate-400 uppercase tracking-wider font-semibold">Graph Nodes</div>
          </div>
          <div className="w-px h-8 bg-slate-800 hidden sm:block" />
          <div>
            <div className="text-xl sm:text-2xl font-black text-white font-mono">34</div>
            <div className="text-[11px] text-slate-400 uppercase tracking-wider font-semibold">Syllabus Modules</div>
          </div>
          <div className="w-px h-8 bg-slate-800 hidden sm:block" />
          <div>
            <div className="text-xl sm:text-2xl font-black text-white font-mono">170+</div>
            <div className="text-[11px] text-slate-400 uppercase tracking-wider font-semibold">Core Concepts</div>
          </div>
          <div className="w-px h-8 bg-slate-800 hidden sm:block" />
          <div>
            <div className="text-xl sm:text-2xl font-black text-white font-mono">150+</div>
            <div className="text-[11px] text-slate-400 uppercase tracking-wider font-semibold">Interview Q&A</div>
          </div>
          <div className="w-px h-8 bg-slate-800 hidden sm:block" />
          <div>
            <div className="text-xl sm:text-2xl font-black text-white font-mono">22+</div>
            <div className="text-[11px] text-slate-400 uppercase tracking-wider font-semibold">Landmark Papers</div>
          </div>
        </div>

      </div>
    </div>
  );
}
