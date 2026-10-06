import React, { useState, useEffect, useRef } from 'react';
import { NavLink, useLocation, useNavigate } from 'react-router-dom';
import { 
  Network, 
  BookOpen, 
  FileText, 
  Briefcase, 
  HelpCircle, 
  Layers, 
  Search, 
  Printer, 
  Sparkles,
  ExternalLink,
  Info,
  Zap,
  Bookmark,
  CheckCircle2,
  PlayCircle,
  Award,
  History,
  Download,
  Menu,
  X,
  Code2,
  ChevronDown
} from 'lucide-react';
import ThemeSwitcher from './ThemeSwitcher';
import { useProgress } from '../context/ProgressContext';
import papersData from '../data/papers.json';
import conceptsData from '../data/concepts.json';
import projectsData from '../data/projects.json';
import interviewData from '../data/interviewQuestions.json';

export default function Navbar({ 
  onOpenSearch, 
  onOpenAbout, 
  onOpenKinetic, 
  onOpenBookmarks, 
  onOpenAssessment, 
  onOpenTimeline,
  onOpenPythonLab
}) {
  const location = useLocation();
  const navigate = useNavigate();
  const [logoError, setLogoError] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [toolsDropdownOpen, setToolsDropdownOpen] = useState(false);
  const toolsDropdownRef = useRef(null);
  const { bookmarkCount, completedCount } = useProgress();
  const [deferredPrompt, setDeferredPrompt] = useState(null);
  const [isInstallable, setIsInstallable] = useState(false);

  // Close menus on route change
  useEffect(() => {
    setMobileMenuOpen(false);
    setToolsDropdownOpen(false);
  }, [location.pathname]);

  // Click outside to close tools dropdown
  useEffect(() => {
    const handleOutsideClick = (e) => {
      if (toolsDropdownRef.current && !toolsDropdownRef.current.contains(e.target)) {
        setToolsDropdownOpen(false);
      }
    };
    document.addEventListener('mousedown', handleOutsideClick);
    return () => document.removeEventListener('mousedown', handleOutsideClick);
  }, []);

  // PWA install prompt handler
  useEffect(() => {
    const handler = (e) => {
      e.preventDefault();
      setDeferredPrompt(e);
      setIsInstallable(true);
    };
    window.addEventListener('beforeinstallprompt', handler);
    return () => window.removeEventListener('beforeinstallprompt', handler);
  }, []);

  const handleInstallClick = async () => {
    if (!deferredPrompt) return;
    deferredPrompt.prompt();
    const { outcome } = await deferredPrompt.userChoice;
    if (outcome === 'accepted') {
      setIsInstallable(false);
      setDeferredPrompt(null);
    }
  };

  const navItems = [
    {
      to: '/concepts',
      label: 'Core Concepts',
      icon: Layers,
      color: 'rose',
      badge: String(conceptsData.length),
      badgeColor: 'bg-rose-500/20 text-rose-300 border-rose-500/30',
    },
    {
      to: '/interview',
      label: 'Interview Vault',
      icon: HelpCircle,
      color: 'purple',
      badge: '1000+',
      badgeColor: 'bg-purple-500/20 text-purple-300 border-purple-500/30',
    },
    {
      to: '/projects',
      label: 'Case Studies',
      icon: Briefcase,
      color: 'emerald',
      badge: String(projectsData.length),
      badgeColor: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30',
    },
    {
      to: '/papers',
      label: 'Landmark Papers',
      icon: FileText,
      color: 'amber',
      badge: String(papersData.length),
      badgeColor: 'bg-amber-500/20 text-amber-300 border-amber-500/30',
    },
    {
      to: '/playgrounds',
      label: 'ML Playgrounds',
      icon: PlayCircle,
      color: 'cyan',
      badge: 'Live',
      badgeColor: 'bg-cyan-500/20 text-cyan-300 border-cyan-500/30',
    }
  ];

  const handlePrint = () => {
    window.print();
  };

  return (
    <header className="bg-slate-900/95 backdrop-blur-md border-b border-slate-800 px-3 sm:px-4 py-2 z-30 shadow-lg shrink-0 sticky top-0">
      {/* Top Single Row Bar */}
      <div className="flex items-center justify-between gap-2.5 w-full">
        {/* Brand & Logo */}
        <div className="flex items-center space-x-2.5 shrink-0">
          <NavLink 
            to="/" 
            id="navbar-brand-logo"
            className="group flex items-center space-x-2.5 text-left focus:outline-none"
            title="Return to The Era of AI Home Portal"
          >
            <div className="relative w-8 h-8 sm:w-9 sm:h-9 rounded-xl overflow-hidden shadow-lg shadow-indigo-500/25 ring-1 ring-white/10 group-hover:scale-105 group-hover:ring-indigo-400/40 transition-all duration-200 shrink-0 bg-slate-900 flex items-center justify-center">
              {!logoError ? (
                <img 
                  src={`${import.meta.env.BASE_URL}logo.png`} 
                  alt="The Era of AI Logo" 
                  className="w-full h-full object-cover"
                  onError={() => setLogoError(true)}
                />
              ) : (
                <div className="w-full h-full flex items-center justify-center bg-gradient-to-tr from-indigo-600 via-indigo-500 to-purple-500 text-white">
                  <Sparkles className="w-5 h-5" />
                </div>
              )}
            </div>
            <div>
              <span className="font-bold text-sm sm:text-base tracking-tight text-white flex items-center gap-1.5 group-hover:text-indigo-300 transition-colors">
                <span>The Era of AI</span>
                <span className="hidden md:inline-block text-[10px] font-semibold uppercase px-1.5 py-0.2 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 tracking-wider">
                  React Edition
                </span>
              </span>
              <p className="text-[10px] text-slate-400 hidden 2xl:block">
                Interactive Knowledge Universe &bull; Syllabus &bull; Papers &bull; 1000+ Questions
              </p>
            </div>
          </NavLink>
        </div>

        {/* Center Desktop Nav Tabs (Visible on xl+ screens) */}
        <nav className="hidden xl:flex items-center space-x-1 2xl:space-x-1.5 bg-slate-950/80 p-1 rounded-xl border border-slate-800 shadow-inner flex-nowrap shrink-0">
          {/* Merged Segmented Toggle: Mind Map & Line-wise Syllabus */}
          <div className="flex items-center p-0.5 bg-slate-900 rounded-lg border border-slate-800 shadow-sm shrink-0">
            <button
              onClick={() => navigate('/mindmap')}
              id="navbar-toggle-mindmap-btn"
              className={`px-2.5 py-1.5 rounded-md text-[11px] 2xl:text-xs font-semibold transition-all duration-150 flex items-center gap-1.5 whitespace-nowrap shrink-0 ${
                location.pathname === '/mindmap'
                  ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                  : 'text-slate-400 hover:text-white hover:bg-slate-800/60'
              }`}
            >
              <Network className="w-3.5 h-3.5 shrink-0" />
              <span>Mind Map</span>
            </button>
            <button
              onClick={() => navigate('/syllabus')}
              id="navbar-toggle-syllabus-btn"
              className={`px-2.5 py-1.5 rounded-md text-[11px] 2xl:text-xs font-semibold transition-all duration-150 flex items-center gap-1.5 whitespace-nowrap shrink-0 ${
                location.pathname === '/syllabus'
                  ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                  : 'text-slate-400 hover:text-white hover:bg-slate-800/60'
              }`}
            >
              <BookOpen className="w-3.5 h-3.5 shrink-0" />
              <span>Line-wise Syllabus</span>
            </button>
          </div>

          {/* Remaining 5 Core Specialized Hubs */}
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.to;

            return (
              <NavLink
                key={item.to}
                to={item.to}
                className={`px-2 2xl:px-2.5 py-1.5 rounded-lg text-[11px] 2xl:text-xs font-semibold transition-all duration-150 flex items-center gap-1 whitespace-nowrap shrink-0 ${
                  isActive
                    ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                    : 'text-slate-300 hover:text-white hover:bg-slate-800/60'
                }`}
              >
                <Icon className={`w-3.5 h-3.5 shrink-0 ${isActive ? 'text-white' : 'text-slate-400'}`} />
                <span>{item.label}</span>
                {item.badge && (
                  <span className={`text-[9px] px-1.5 py-0.2 rounded-full border ${item.badgeColor} font-mono ml-0.5`}>
                    {item.badge}
                  </span>
                )}
              </NavLink>
            );
          })}
        </nav>

        {/* Right Controls Container */}
        <div className="flex items-center space-x-1.5 sm:space-x-2 shrink-0">
          <ThemeSwitcher />

          {/* Global Search Button */}
          <button
            onClick={onOpenSearch}
            id="navbar-search-btn"
            className="p-1.5 sm:px-2.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white border border-slate-700/60 transition flex items-center gap-1.5 text-xs font-medium shadow-sm"
            title="Universal Search (Ctrl+K / Cmd+K)"
          >
            <Search className="w-3.5 h-3.5 text-slate-400" />
            <span className="hidden md:inline">Search</span>
            <kbd className="hidden 2xl:inline-block px-1 py-0.2 text-[9px] font-mono bg-slate-900 border border-slate-700 rounded text-slate-400">
              ⌘K
            </kbd>
          </button>

          {/* Bookmarks Toggle (Desktop & Tablet) */}
          <button
            onClick={onOpenBookmarks}
            id="navbar-bookmarks-btn"
            className="relative p-1.5 px-2 sm:px-2.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white border border-slate-700/60 transition flex items-center gap-1.5 text-xs font-medium shadow-sm group"
            title="Open Saved Bookmarks"
          >
            <Bookmark className={`w-3.5 h-3.5 transition-transform group-hover:scale-110 ${bookmarkCount > 0 ? 'text-amber-400 fill-amber-400' : 'text-slate-400'}`} />
            <span className="hidden sm:inline">Bookmarks</span>
            {bookmarkCount > 0 && (
              <span className="px-1.5 py-0.2 rounded-full bg-amber-500/20 text-amber-300 border border-amber-500/40 text-[10px] font-bold">
                {bookmarkCount}
              </span>
            )}
          </button>

          {/* Direct About Modal Button (Features Project Overview, Stats & Author Arpit Somani) */}
          <button
            onClick={onOpenAbout}
            id="navbar-about-btn"
            className="p-1.5 px-2 sm:px-2.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white border border-slate-700/60 transition flex items-center gap-1.5 text-xs font-medium shadow-sm group"
            title="About The Era of AI (Project Overview, Stats & Author)"
          >
            <Info className="w-3.5 h-3.5 text-indigo-400 group-hover:scale-110 transition-transform" />
            <span className="hidden sm:inline">About</span>
          </button>

          {/* Interactive Tools & Labs Dropdown (Prevents navbar overflow on all screen sizes) */}
          <div className="relative hidden sm:block" ref={toolsDropdownRef}>
            <button
              onClick={() => setToolsDropdownOpen(!toolsDropdownOpen)}
              id="navbar-tools-dropdown-btn"
              className={`p-1.5 px-2.5 rounded-lg border transition flex items-center gap-1.5 text-xs font-semibold shadow-sm ${
                toolsDropdownOpen 
                  ? 'bg-indigo-600 text-white border-indigo-400 shadow-indigo-600/30 ring-1 ring-indigo-400' 
                  : 'bg-indigo-500/10 hover:bg-indigo-500/20 text-indigo-300 hover:text-white border-indigo-500/30'
              }`}
              title="Interactive Tools, Sandboxes & Diagnostics"
            >
              <Sparkles className="w-3.5 h-3.5 text-indigo-400 shrink-0" />
              <span>Tools &amp; Labs</span>
              <span className="text-[10px] px-1 rounded-full bg-indigo-500/20 text-indigo-200 border border-indigo-500/30 font-mono">
                6
              </span>
              <ChevronDown className={`w-3 h-3 text-indigo-300 transition-transform duration-200 ${toolsDropdownOpen ? 'rotate-180' : ''}`} />
            </button>

            {/* Glassmorphic Dropdown Menu */}
            {toolsDropdownOpen && (
              <div className="absolute right-0 mt-2 w-72 sm:w-80 bg-slate-900/98 backdrop-blur-xl border border-slate-700/80 rounded-2xl shadow-2xl p-2 z-50 animate-fadeIn space-y-1 divide-y divide-slate-800/80">
                {/* Section: Interactive Sandboxes */}
                <div className="space-y-1 pb-1">
                  <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 px-2 py-1 block font-mono">
                    Interactive Sandboxes
                  </span>
                  
                  <button
                    onClick={() => { onOpenPythonLab(); setToolsDropdownOpen(false); }}
                    id="tools-dropdown-python-btn"
                    className="w-full p-2 rounded-xl hover:bg-emerald-500/10 hover:border-emerald-500/30 border border-transparent text-left flex items-start gap-2.5 transition group"
                  >
                    <div className="w-8 h-8 rounded-lg bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 flex items-center justify-center shrink-0 group-hover:scale-105 transition-transform mt-0.5">
                      <Code2 className="w-4 h-4" />
                    </div>
                    <div>
                      <div className="text-xs font-semibold text-white group-hover:text-emerald-300 flex items-center gap-1.5">
                        <span>Python Lab</span>
                        <span className="text-[9px] px-1 py-0.2 rounded bg-emerald-500/20 text-emerald-300 font-mono">Wasm</span>
                      </div>
                      <p className="text-[11px] text-slate-400 leading-tight mt-0.5">
                        Run Attention, RoPE &amp; LoRA in WebAssembly Pyodide
                      </p>
                    </div>
                  </button>

                  <button
                    onClick={() => { onOpenKinetic(); setToolsDropdownOpen(false); }}
                    id="tools-dropdown-kinetic-btn"
                    className="w-full p-2 rounded-xl hover:bg-indigo-500/10 hover:border-indigo-500/30 border border-transparent text-left flex items-start gap-2.5 transition group"
                  >
                    <div className="w-8 h-8 rounded-lg bg-indigo-500/20 text-cyan-400 border border-indigo-500/30 flex items-center justify-center shrink-0 group-hover:scale-105 transition-transform mt-0.5">
                      <Zap className="w-4 h-4" />
                    </div>
                    <div>
                      <div className="text-xs font-semibold text-white group-hover:text-cyan-300">
                        Kinetic Universe
                      </div>
                      <p className="text-[11px] text-slate-400 leading-tight mt-0.5">
                        Interactive neural canvas physics &amp; gravitation
                      </p>
                    </div>
                  </button>
                </div>

                {/* Section: Study & Diagnostics */}
                <div className="space-y-1 pt-1.5 pb-1">
                  <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 px-2 py-1 block font-mono">
                    Diagnostics &amp; Study Tools
                  </span>

                  <button
                    onClick={() => { onOpenAssessment(); setToolsDropdownOpen(false); }}
                    id="tools-dropdown-diagnostic-btn"
                    className="w-full p-2 rounded-xl hover:bg-purple-500/10 hover:border-purple-500/30 border border-transparent text-left flex items-start gap-2.5 transition group"
                  >
                    <div className="w-8 h-8 rounded-lg bg-purple-500/20 text-purple-400 border border-purple-500/30 flex items-center justify-center shrink-0 group-hover:scale-105 transition-transform mt-0.5">
                      <Award className="w-4 h-4" />
                    </div>
                    <div>
                      <div className="text-xs font-semibold text-white group-hover:text-purple-300">
                        AI Readiness Diagnostic
                      </div>
                      <p className="text-[11px] text-slate-400 leading-tight mt-0.5">
                        15-min knowledge evaluation &amp; personalized score
                      </p>
                    </div>
                  </button>

                  <button
                    onClick={() => { onOpenTimeline(); setToolsDropdownOpen(false); }}
                    id="tools-dropdown-timeline-btn"
                    className="w-full p-2 rounded-xl hover:bg-amber-500/10 hover:border-amber-500/30 border border-transparent text-left flex items-start gap-2.5 transition group"
                  >
                    <div className="w-8 h-8 rounded-lg bg-amber-500/20 text-amber-400 border border-amber-500/30 flex items-center justify-center shrink-0 group-hover:scale-105 transition-transform mt-0.5">
                      <History className="w-4 h-4" />
                    </div>
                    <div>
                      <div className="text-xs font-semibold text-white group-hover:text-amber-300">
                        AI History Timeline
                      </div>
                      <p className="text-[11px] text-slate-400 leading-tight mt-0.5">
                        1950–2026 landmark paradigms &amp; discoveries
                      </p>
                    </div>
                  </button>
                </div>

                {/* Section: Platform Info & Actions */}
                <div className="space-y-1 pt-1.5">
                  <button
                    onClick={() => { onOpenAbout(); setToolsDropdownOpen(false); }}
                    id="tools-dropdown-about-btn"
                    className="w-full p-2 rounded-xl hover:bg-slate-800 text-left flex items-center gap-2.5 transition text-slate-300 hover:text-white"
                  >
                    <Info className="w-4 h-4 text-indigo-400 shrink-0 ml-1" />
                    <span className="text-xs font-medium">About The Era of AI</span>
                  </button>

                  {isInstallable && (
                    <button
                      onClick={() => { handleInstallClick(); setToolsDropdownOpen(false); }}
                      className="w-full p-2 rounded-xl bg-cyan-500/20 hover:bg-cyan-500/30 text-cyan-300 border border-cyan-500/40 text-left flex items-center gap-2.5 transition text-xs font-semibold"
                    >
                      <Download className="w-4 h-4 text-cyan-300 shrink-0 ml-1" />
                      <span>Install App (PWA)</span>
                    </button>
                  )}

                  {(location.pathname === '/syllabus' || location.pathname === '/papers') && (
                    <button
                      onClick={() => { handlePrint(); setToolsDropdownOpen(false); }}
                      className="w-full p-2 rounded-xl bg-gradient-to-r from-red-600 to-rose-600 hover:from-red-500 hover:to-rose-500 text-white text-left flex items-center gap-2.5 transition text-xs font-semibold shadow-md shadow-red-500/20"
                    >
                      <Printer className="w-4 h-4 shrink-0 ml-1" />
                      <span>Print or Save PDF</span>
                    </button>
                  )}
                </div>
              </div>
            )}
          </div>

          {/* Mobile & Tablet Hamburger Menu Toggle Button (Visible on screens < xl) */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            id="navbar-mobile-toggle-btn"
            aria-label="Toggle navigation menu"
            className={`p-1.5 sm:p-2 rounded-xl transition flex items-center justify-center border xl:hidden ${
              mobileMenuOpen
                ? 'bg-indigo-600 text-white border-indigo-500 shadow-md shadow-indigo-600/30'
                : 'bg-slate-800 hover:bg-slate-700 text-slate-200 border-slate-700'
            }`}
          >
            {mobileMenuOpen ? (
              <X className="w-4 h-4 sm:w-5 sm:h-5 text-white" />
            ) : (
              <div className="relative">
                <Menu className="w-4 h-4 sm:w-5 sm:h-5 text-slate-200" />
                {bookmarkCount > 0 && (
                  <span className="w-2 h-2 rounded-full bg-amber-400 absolute -top-0.5 -right-0.5" />
                )}
              </div>
            )}
          </button>
        </div>
      </div>

      {/* Mobile Drawer Dropdown Menu (Clean, organized, responsive) */}
      {mobileMenuOpen && (
        <div className="xl:hidden mt-2.5 pt-3 pb-2 border-t border-slate-800 space-y-3.5 animate-fadeIn">
          {/* Section 1: Main Platform Routes */}
          <div className="space-y-2">
            <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 px-1 font-mono flex items-center justify-between">
              <span>Core Curriculum</span>
              <span className="text-slate-500 font-normal">Toggle View</span>
            </span>

            {/* Merged Segmented Toggle in Mobile */}
            <div className="p-1 bg-slate-950 rounded-xl border border-slate-800 flex items-center gap-1">
              <button
                onClick={() => { navigate('/mindmap'); setMobileMenuOpen(false); }}
                id="mobile-toggle-mindmap-btn"
                className={`flex-1 p-2 rounded-lg text-xs font-semibold transition flex items-center justify-center gap-2 ${
                  location.pathname === '/mindmap'
                    ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                    : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
                }`}
              >
                <Network className="w-4 h-4 shrink-0" />
                <span>Mind Map</span>
              </button>
              <button
                onClick={() => { navigate('/syllabus'); setMobileMenuOpen(false); }}
                id="mobile-toggle-syllabus-btn"
                className={`flex-1 p-2 rounded-lg text-xs font-semibold transition flex items-center justify-center gap-2 ${
                  location.pathname === '/syllabus'
                    ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                    : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
                }`}
              >
                <BookOpen className="w-4 h-4 shrink-0" />
                <span>Line-wise Syllabus</span>
              </button>
            </div>

            <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 px-1 font-mono flex items-center justify-between pt-1">
              <span>Navigation Pages</span>
              <span className="text-slate-500 font-normal">5 Specialized Hubs</span>
            </span>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-1.5">
              {navItems.map((item) => {
                const Icon = item.icon;
                const isActive = location.pathname === item.to;

                return (
                  <NavLink
                    key={item.to}
                    to={item.to}
                    onClick={() => setMobileMenuOpen(false)}
                    className={`p-2.5 rounded-xl text-xs font-semibold transition flex items-center justify-between gap-2 ${
                      isActive
                        ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                        : 'bg-slate-950/70 text-slate-300 hover:text-white hover:bg-slate-800 border border-slate-800/80'
                    }`}
                  >
                    <div className="flex items-center gap-2 min-w-0">
                      <Icon className={`w-4 h-4 shrink-0 ${isActive ? 'text-white' : 'text-slate-400'}`} />
                      <span className="truncate">{item.label}</span>
                    </div>
                    {item.badge && (
                      <span className={`text-[10px] px-1.5 py-0.2 rounded-full border ${item.badgeColor} font-mono shrink-0`}>
                        {item.badge}
                      </span>
                    )}
                  </NavLink>
                );
              })}
            </div>
          </div>

          {/* Section 2: Interactive Modals & Sandboxes */}
          <div className="space-y-1.5 pt-2 border-t border-slate-800/80">
            <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 px-1 font-mono block">
              Interactive Tools &amp; Diagnostics
            </span>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-1.5 text-xs font-medium">
              <button
                onClick={() => { onOpenAssessment(); setMobileMenuOpen(false); }}
                className="p-2.5 rounded-xl bg-purple-500/10 hover:bg-purple-500/20 text-purple-300 border border-purple-500/30 flex items-center gap-2 transition"
              >
                <Award className="w-4 h-4 text-purple-400 shrink-0" />
                <span className="truncate">Diagnostic</span>
              </button>

              <button
                onClick={() => { onOpenTimeline(); setMobileMenuOpen(false); }}
                className="p-2.5 rounded-xl bg-amber-500/10 hover:bg-amber-500/20 text-amber-300 border border-amber-500/30 flex items-center gap-2 transition"
              >
                <History className="w-4 h-4 text-amber-400 shrink-0" />
                <span className="truncate">Timeline</span>
              </button>

              <button
                onClick={() => { onOpenPythonLab(); setMobileMenuOpen(false); }}
                className="p-2.5 rounded-xl bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 flex items-center gap-2 transition"
              >
                <Code2 className="w-4 h-4 text-emerald-400 shrink-0" />
                <span className="truncate">Python Lab</span>
              </button>

              <button
                onClick={() => { onOpenBookmarks(); setMobileMenuOpen(false); }}
                className="p-2.5 rounded-xl bg-amber-500/10 hover:bg-amber-500/20 text-amber-300 border border-amber-500/30 flex items-center justify-between gap-1.5 transition"
              >
                <div className="flex items-center gap-2 truncate">
                  <Bookmark className="w-4 h-4 text-amber-400 shrink-0" />
                  <span className="truncate">Bookmarks</span>
                </div>
                {bookmarkCount > 0 && (
                  <span className="text-[10px] px-1.5 py-0.2 rounded-full bg-amber-500/20 text-amber-300 font-mono font-bold">
                    {bookmarkCount}
                  </span>
                )}
              </button>

              <button
                onClick={() => { onOpenKinetic(); setMobileMenuOpen(false); }}
                className="p-2.5 rounded-xl bg-indigo-500/10 hover:bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 flex items-center gap-2 transition"
              >
                <Zap className="w-4 h-4 text-cyan-400 shrink-0" />
                <span className="truncate">Kinetic Sandbox</span>
              </button>

              <button
                onClick={() => { onOpenAbout(); setMobileMenuOpen(false); }}
                className="p-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 flex items-center gap-2 transition"
              >
                <Info className="w-4 h-4 text-indigo-400 shrink-0" />
                <span className="truncate">About Portal</span>
              </button>

              {isInstallable && (
                <button
                  onClick={() => { handleInstallClick(); setMobileMenuOpen(false); }}
                  className="p-2.5 rounded-xl bg-cyan-600/20 hover:bg-cyan-600/30 text-cyan-300 border border-cyan-500/40 flex items-center gap-2 col-span-2 sm:col-span-3 transition font-semibold"
                >
                  <Download className="w-4 h-4 text-cyan-300 shrink-0" />
                  <span>Install The Era of AI App</span>
                </button>
              )}
            </div>
          </div>
        </div>
      )}
    </header>
  );
}
