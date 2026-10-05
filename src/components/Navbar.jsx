import React, { useState, useEffect } from 'react';
import { NavLink, useLocation } from 'react-router-dom';
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
  X
} from 'lucide-react';
import ThemeSwitcher from './ThemeSwitcher';
import { useProgress } from '../context/ProgressContext';
import papersData from '../data/papers.json';

export default function Navbar({ 
  onOpenSearch, 
  onOpenAbout, 
  onOpenKinetic, 
  onOpenBookmarks, 
  onOpenAssessment, 
  onOpenCheatsheet, 
  onOpenTimeline 
}) {
  const location = useLocation();
  const [logoError, setLogoError] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const { bookmarkCount, completedCount } = useProgress();
  const [deferredPrompt, setDeferredPrompt] = useState(null);
  const [isInstallable, setIsInstallable] = useState(false);

  // Close mobile drawer on route change
  useEffect(() => {
    setMobileMenuOpen(false);
  }, [location.pathname]);

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
      to: '/mindmap',
      label: 'Mind Map',
      icon: Network,
      color: 'indigo',
    },
    {
      to: '/syllabus',
      label: 'Line-wise Syllabus',
      icon: BookOpen,
      color: 'blue',
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
      to: '/projects',
      label: 'Case Studies',
      icon: Briefcase,
      color: 'emerald',
      badge: '5',
      badgeColor: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30',
    },
    {
      to: '/interview',
      label: 'Interview Vault',
      icon: HelpCircle,
      color: 'purple',
      badge: '150+',
      badgeColor: 'bg-purple-500/20 text-purple-300 border-purple-500/30',
    },
    {
      to: '/concepts',
      label: 'Core Concepts',
      icon: Layers,
      color: 'rose',
      badge: '170',
      badgeColor: 'bg-rose-500/20 text-rose-300 border-rose-500/30',
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
            to="/mindmap" 
            id="navbar-brand-logo"
            className="group flex items-center space-x-2.5 text-left focus:outline-none"
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
              <p className="text-[10px] text-slate-400 hidden xl:block">
                Interactive Knowledge Universe &bull; Syllabus &bull; Papers &bull; 150+ Questions
              </p>
            </div>
          </NavLink>
        </div>

        {/* Center Desktop Nav Tabs (Visible on xl+ screens) */}
        <nav className="hidden xl:flex items-center space-x-1 bg-slate-950/80 p-1 rounded-xl border border-slate-800 shadow-inner flex-nowrap shrink-0">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.to || (item.to === '/mindmap' && location.pathname === '/');

            return (
              <NavLink
                key={item.to}
                to={item.to}
                className={`px-2.5 py-1.5 rounded-lg text-xs font-semibold transition-all duration-150 flex items-center gap-1.5 whitespace-nowrap shrink-0 ${
                  isActive
                    ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                    : 'text-slate-300 hover:text-white hover:bg-slate-800/60'
                }`}
              >
                <Icon className={`w-3.5 h-3.5 ${isActive ? 'text-white' : 'text-slate-400'}`} />
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

          {/* Desktop Only Actions (hidden on small/medium screens to prevent wrapping) */}
          <div className="hidden xl:flex items-center space-x-1.5">
            {/* Bookmarks Toggle */}
            <button
              onClick={onOpenBookmarks}
              id="navbar-bookmarks-btn"
              className="relative p-1.5 px-2.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white border border-slate-700/60 transition flex items-center gap-1.5 text-xs font-medium shadow-sm group"
              title="Open Saved Bookmarks & Study Cheatsheet"
            >
              <Bookmark className={`w-3.5 h-3.5 transition-transform group-hover:scale-110 ${bookmarkCount > 0 ? 'text-amber-400 fill-amber-400' : 'text-slate-400'}`} />
              <span className="hidden 2xl:inline">Bookmarks</span>
              {bookmarkCount > 0 && (
                <span className="px-1.5 py-0.2 rounded-full bg-amber-500/20 text-amber-300 border border-amber-500/40 text-[10px] font-bold">
                  {bookmarkCount}
                </span>
              )}
            </button>

            {/* AI Readiness Assessment */}
            <button
              onClick={onOpenAssessment}
              id="navbar-assessment-btn"
              className="p-1.5 px-2 rounded-lg bg-purple-500/10 hover:bg-purple-500/25 text-purple-300 hover:text-white border border-purple-500/30 transition flex items-center gap-1.5 text-xs font-medium shadow-sm group"
              title="Take AI Readiness Diagnostic"
            >
              <Award className="w-3.5 h-3.5 text-purple-400 group-hover:scale-110 transition-transform" />
              <span>Diagnostic</span>
            </button>

            {/* Cheatsheet Builder */}
            <button
              onClick={onOpenCheatsheet}
              id="navbar-cheatsheet-btn"
              className="p-1.5 px-2 rounded-lg bg-cyan-500/10 hover:bg-cyan-500/25 text-cyan-300 hover:text-white border border-cyan-500/30 transition flex items-center gap-1.5 text-xs font-medium shadow-sm group"
              title="Custom Cheatsheet Builder & PDF Export"
            >
              <FileText className="w-3.5 h-3.5 text-cyan-400 group-hover:scale-110 transition-transform" />
              <span>Cheatsheet</span>
            </button>

            {/* History Timeline */}
            <button
              onClick={onOpenTimeline}
              id="navbar-timeline-btn"
              className="p-1.5 px-2 rounded-lg bg-amber-500/10 hover:bg-amber-500/25 text-amber-300 hover:text-white border border-amber-500/30 transition flex items-center gap-1.5 text-xs font-medium shadow-sm group"
              title="Interactive AI History Timeline (1950–2026)"
            >
              <History className="w-3.5 h-3.5 text-amber-400 group-hover:scale-110 transition-transform" />
              <span>Timeline</span>
            </button>

            {/* Kinetic Universe Sandbox */}
            <button
              onClick={onOpenKinetic}
              id="navbar-kinetic-btn"
              className="p-1.5 px-2 rounded-lg bg-indigo-500/10 hover:bg-indigo-500/25 text-indigo-300 hover:text-white border border-indigo-500/30 transition flex items-center gap-1.5 text-xs font-medium shadow-sm group"
              title="Kinetic Neural Universe"
            >
              <Zap className="w-3.5 h-3.5 text-cyan-400 group-hover:scale-110 transition-transform" />
              <span>Kinetic</span>
            </button>

            {/* About Portal */}
            <button
              onClick={onOpenAbout}
              id="navbar-about-btn"
              className="p-1.5 px-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white border border-slate-700/60 transition flex items-center gap-1.5 text-xs font-medium shadow-sm"
              title="About The Era of AI"
            >
              <Info className="w-3.5 h-3.5 text-indigo-400" />
            </button>

            {/* Install PWA Button */}
            {isInstallable && (
              <button
                onClick={handleInstallClick}
                id="navbar-install-app-btn"
                className="p-1.5 px-2.5 rounded-lg bg-cyan-500/20 hover:bg-cyan-500/30 text-cyan-300 hover:text-white border border-cyan-500/40 transition flex items-center gap-1.5 text-xs font-semibold shadow-sm animate-pulse"
                title="Install App"
              >
                <Download className="w-3.5 h-3.5 text-cyan-300" />
                <span>Install</span>
              </button>
            )}

            {(location.pathname === '/syllabus' || location.pathname === '/papers') && (
              <button
                onClick={handlePrint}
                id="navbar-print-btn"
                title="Print or Save as PDF"
                className="p-1.5 px-2.5 rounded-lg bg-gradient-to-r from-red-600 to-rose-600 hover:from-red-500 hover:to-rose-500 text-white font-semibold text-xs shadow-md shadow-red-500/20 transition flex items-center gap-1.5"
              >
                <Printer className="w-3.5 h-3.5" />
                <span className="hidden 2xl:inline">PDF</span>
              </button>
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
          <div className="space-y-1.5">
            <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 px-1 font-mono flex items-center justify-between">
              <span>Navigation Pages</span>
              <span className="text-slate-500 font-normal">7 Core Hubs</span>
            </span>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-1.5">
              {navItems.map((item) => {
                const Icon = item.icon;
                const isActive = location.pathname === item.to || (item.to === '/mindmap' && location.pathname === '/');

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
                onClick={() => { onOpenCheatsheet(); setMobileMenuOpen(false); }}
                className="p-2.5 rounded-xl bg-cyan-500/10 hover:bg-cyan-500/20 text-cyan-300 border border-cyan-500/30 flex items-center gap-2 transition"
              >
                <FileText className="w-4 h-4 text-cyan-400 shrink-0" />
                <span className="truncate">Cheatsheet</span>
              </button>

              <button
                onClick={() => { onOpenTimeline(); setMobileMenuOpen(false); }}
                className="p-2.5 rounded-xl bg-amber-500/10 hover:bg-amber-500/20 text-amber-300 border border-amber-500/30 flex items-center gap-2 transition"
              >
                <History className="w-4 h-4 text-amber-400 shrink-0" />
                <span className="truncate">Timeline</span>
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
