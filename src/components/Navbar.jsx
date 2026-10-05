import React from 'react';
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
  ExternalLink
} from 'lucide-react';
import ThemeSwitcher from './ThemeSwitcher';

export default function Navbar({ onOpenSearch, onOpenAbout }) {
  const location = useLocation();

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
      badge: '22',
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
      badgeColor: 'bg-purple-500/20 text-purple-300 border-purple-500/30 animate-pulse',
    },
    {
      to: '/concepts',
      label: 'Core Concepts',
      icon: Layers,
      color: 'rose',
      badge: '170',
      badgeColor: 'bg-rose-500/20 text-rose-300 border-rose-500/30',
    }
  ];

  const handlePrint = () => {
    window.print();
  };

  return (
    <header className="bg-slate-900/90 backdrop-blur-md border-b border-slate-800 px-4 py-2 flex flex-wrap items-center justify-between gap-3 z-30 shadow-lg shrink-0">
      {/* Brand & Logo */}
      <div className="flex items-center space-x-3">
        <NavLink 
          to="/mindmap" 
          id="navbar-brand-logo"
          className="group flex items-center space-x-3 text-left focus:outline-none"
        >
          <div className="relative w-9 h-9 rounded-xl overflow-hidden shadow-lg shadow-indigo-500/25 ring-1 ring-white/10 group-hover:scale-105 group-hover:ring-indigo-400/40 transition-all duration-200 shrink-0 bg-slate-900 flex items-center justify-center">
            <img 
              src={`${import.meta.env.BASE_URL}logo.png`} 
              alt="The Era of AI Logo" 
              className="w-full h-full object-cover"
              onError={(e) => {
                e.currentTarget.style.display = 'none';
                e.currentTarget.nextSibling.style.display = 'flex';
              }}
            />
            <div className="hidden w-full h-full items-center justify-center bg-gradient-to-tr from-indigo-600 via-indigo-500 to-purple-500 text-white">
              <Sparkles className="w-5 h-5" />
            </div>
          </div>
          <div>
            <span className="font-bold text-sm md:text-base tracking-tight text-white flex items-center gap-2 group-hover:text-indigo-300 transition-colors">
              The Era of AI
              <span className="hidden sm:inline-block text-[10px] font-semibold uppercase px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 tracking-wider">
                React Edition
              </span>
            </span>
            <p className="text-[11px] text-slate-400 hidden sm:block">
              Interactive Universe &bull; Syllabus &bull; Papers &bull; 150+ Questions
            </p>
          </div>
        </NavLink>
      </div>

      {/* Center Nav Tabs */}
      <nav className="flex items-center overflow-x-auto no-scrollbar max-w-full space-x-1 bg-slate-950/80 p-1 rounded-xl border border-slate-800 shadow-inner flex-nowrap shrink-0">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = location.pathname === item.to || (item.to === '/mindmap' && location.pathname === '/');

          return (
            <NavLink
              key={item.to}
              to={item.to}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all duration-150 flex items-center gap-1.5 whitespace-nowrap shrink-0 ${
                isActive
                  ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                  : 'text-slate-300 hover:text-white hover:bg-slate-800/60'
              }`}
            >
              <Icon className={`w-3.5 h-3.5 ${isActive ? 'text-white' : 'text-slate-400'}`} />
              <span>{item.label}</span>
              {item.badge && (
                <span className={`text-[10px] px-1.5 py-0.2 rounded-full border ${item.badgeColor} font-mono ml-0.5`}>
                  {item.badge}
                </span>
              )}
            </NavLink>
          );
        })}
      </nav>

      {/* Right Controls: Theme Switcher, Global Search, About & Print */}
      <div className="flex items-center space-x-2">
        <ThemeSwitcher />

        <button
          onClick={onOpenSearch}
          id="navbar-search-btn"
          className="p-1.5 px-3 rounded-lg bg-slate-800 hover:bg-slate-700/80 text-slate-300 hover:text-white border border-slate-700/60 transition flex items-center gap-2 text-xs font-medium shadow-sm"
          title="Universal Search (Ctrl+K / Cmd+K)"
        >
          <Search className="w-3.5 h-3.5 text-slate-400" />
          <span className="hidden md:inline">Quick Search</span>
          <kbd className="hidden lg:inline-block px-1.5 py-0.5 text-[10px] font-mono bg-slate-900 border border-slate-700 rounded text-slate-400">
            ⌘K
          </kbd>
        </button>

        <button
          onClick={onOpenAbout}
          id="navbar-about-btn"
          className="p-1.5 px-2.5 rounded-lg bg-slate-800 hover:bg-slate-700/80 text-slate-300 hover:text-white border border-slate-700/60 transition flex items-center gap-1.5 text-xs font-medium shadow-sm"
          title="About The Era of AI Portal"
        >
          <Info className="w-3.5 h-3.5 text-indigo-400" />
          <span className="hidden xl:inline">About</span>
        </button>

        {(location.pathname === '/syllabus' || location.pathname === '/papers') && (
          <button
            onClick={handlePrint}
            id="navbar-print-btn"
            title="Print or Save as PDF"
            className="p-1.5 px-3 rounded-lg bg-gradient-to-r from-red-600 to-rose-600 hover:from-red-500 hover:to-rose-500 text-white font-semibold text-xs shadow-md shadow-red-500/20 transition flex items-center gap-1.5"
          >
            <Printer className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Export PDF</span>
          </button>
        )}
      </div>
    </header>
  );
}
