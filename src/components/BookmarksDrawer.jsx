import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  X, 
  Bookmark, 
  Trash2, 
  Download, 
  ExternalLink, 
  Lightbulb, 
  FileText, 
  HelpCircle, 
  Compass, 
  CheckCircle2,
  Sparkles
} from 'lucide-react';
import { useProgress } from '../context/ProgressContext';
import { useTheme } from '../context/ThemeContext';

export default function BookmarksDrawer({ isOpen, onClose }) {
  const navigate = useNavigate();
  const { theme } = useTheme();
  const { 
    bookmarkedItems, 
    removeBookmark, 
    clearBookmarks, 
    exportBookmarksToMarkdown,
    bookmarkCount 
  } = useProgress();

  const [activeFilter, setActiveFilter] = useState('all');

  if (!isOpen) return null;

  const filteredItems = bookmarkedItems.filter((item) => {
    if (activeFilter === 'all') return true;
    return item.type === activeFilter;
  });

  const counts = {
    all: bookmarkedItems.length,
    concept: bookmarkedItems.filter((i) => i.type === 'concept').length,
    paper: bookmarkedItems.filter((i) => i.type === 'paper').length,
    interview: bookmarkedItems.filter((i) => i.type === 'interview').length,
    syllabus: bookmarkedItems.filter((i) => i.type === 'syllabus').length,
  };

  const getItemIcon = (type) => {
    switch (type) {
      case 'concept':
        return <Lightbulb className="w-4 h-4 text-amber-400" />;
      case 'paper':
        return <FileText className="w-4 h-4 text-cyan-400" />;
      case 'interview':
        return <HelpCircle className="w-4 h-4 text-purple-400" />;
      case 'syllabus':
        return <Compass className="w-4 h-4 text-emerald-400" />;
      default:
        return <Bookmark className="w-4 h-4 text-indigo-400" />;
    }
  };

  const handleNavigate = (link) => {
    if (!link) return;
    onClose();
    navigate(link);
  };

  return (
    <div className="fixed inset-0 z-50 overflow-hidden flex justify-end animate-fadeIn">
      {/* Backdrop */}
      <div 
        className="fixed inset-0 bg-slate-950/70 backdrop-blur-sm transition-opacity" 
        onClick={onClose} 
      />

      {/* Slide-over Drawer */}
      <aside 
        className="relative w-full max-w-md h-full bg-slate-900 border-l border-slate-800 shadow-2xl flex flex-col z-10 animate-slideLeft text-slate-100"
        aria-label="Bookmarks and Saved Items"
      >
        {/* Drawer Header */}
        <div className="p-4 sm:p-5 border-b border-slate-800/80 bg-slate-950/60 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-xl bg-indigo-500/20 text-indigo-400 border border-indigo-500/30 flex items-center justify-center">
              <Bookmark className="w-4 h-4 fill-indigo-400" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="font-bold text-base text-white">Study Bookmarks</h2>
                <span className="px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/40 text-xs font-semibold">
                  {bookmarkCount}
                </span>
              </div>
              <p className="text-[11px] text-slate-400">Personal study vault & quick revision</p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition"
            aria-label="Close bookmarks drawer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Filter Tabs */}
        <div className="px-4 py-2.5 bg-slate-950/40 border-b border-slate-800/60 flex items-center gap-1.5 overflow-x-auto no-scrollbar text-xs">
          {[
            { id: 'all', label: 'All', count: counts.all },
            { id: 'concept', label: 'Concepts', count: counts.concept },
            { id: 'paper', label: 'Papers', count: counts.paper },
            { id: 'interview', label: 'Questions', count: counts.interview },
            { id: 'syllabus', label: 'Syllabus', count: counts.syllabus },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveFilter(tab.id)}
              className={`px-2.5 py-1 rounded-lg font-medium transition shrink-0 flex items-center gap-1.5 ${
                activeFilter === tab.id
                  ? 'bg-indigo-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
              }`}
            >
              <span>{tab.label}</span>
              <span className={`text-[10px] px-1.5 py-0.2 rounded-full ${
                activeFilter === tab.id ? 'bg-indigo-800/80 text-white' : 'bg-slate-800 text-slate-400'
              }`}>
                {tab.count}
              </span>
            </button>
          ))}
        </div>

        {/* Bookmarked Items List */}
        <div className="flex-1 overflow-y-auto p-4 space-y-2.5">
          {filteredItems.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center text-center p-6 space-y-3">
              <div className="w-12 h-12 rounded-2xl bg-slate-800/80 border border-slate-700/60 flex items-center justify-center text-slate-500">
                <Bookmark className="w-6 h-6" />
              </div>
              <p className="text-sm font-semibold text-slate-300">
                {activeFilter === 'all' ? 'No bookmarks saved yet' : `No ${activeFilter} bookmarks yet`}
              </p>
              <p className="text-xs text-slate-400 max-w-xs leading-relaxed">
                Click the bookmark ribbon icon on any concept, research paper, syllabus module, or interview question to assemble your personalized revision list.
              </p>
            </div>
          ) : (
            filteredItems.map((item) => (
              <div
                key={item.id}
                className="group relative p-3 rounded-xl bg-slate-800/60 hover:bg-slate-800 border border-slate-700/50 hover:border-indigo-500/50 transition-all flex flex-col gap-1.5"
              >
                <div className="flex items-start justify-between gap-2">
                  <div className="flex items-start gap-2 min-w-0">
                    <div className="p-1.5 rounded-lg bg-slate-900/80 border border-slate-700/50 shrink-0 mt-0.5">
                      {getItemIcon(item.type)}
                    </div>
                    <div className="min-w-0">
                      <span className="text-[10px] uppercase font-bold tracking-wider text-slate-400 block">
                        {item.type}
                      </span>
                      <h3 
                        onClick={() => handleNavigate(item.link)}
                        className="text-xs sm:text-sm font-semibold text-slate-200 group-hover:text-indigo-300 transition cursor-pointer truncate"
                      >
                        {item.title}
                      </h3>
                      {item.subtitle && (
                        <p className="text-[11px] text-slate-400 line-clamp-1">
                          {item.subtitle}
                        </p>
                      )}
                    </div>
                  </div>

                  <div className="flex items-center gap-1 shrink-0">
                    {item.link && (
                      <button
                        onClick={() => handleNavigate(item.link)}
                        className="p-1 rounded-md text-slate-400 hover:text-indigo-300 hover:bg-indigo-500/10 transition"
                        title="Jump to item"
                      >
                        <ExternalLink className="w-3.5 h-3.5" />
                      </button>
                    )}
                    <button
                      onClick={() => removeBookmark(item.id)}
                      className="p-1 rounded-md text-slate-400 hover:text-rose-400 hover:bg-rose-500/10 transition"
                      title="Remove bookmark"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>

        {/* Footer Actions */}
        {bookmarkedItems.length > 0 && (
          <div className="p-4 border-t border-slate-800/80 bg-slate-950/70 flex items-center justify-between gap-2">
            <button
              onClick={exportBookmarksToMarkdown}
              className="flex-1 py-2 px-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-xs flex items-center justify-center gap-2 shadow-sm transition"
            >
              <Download className="w-3.5 h-3.5" />
              <span>Export Cheatsheet (.md)</span>
            </button>

            <button
              onClick={() => {
                if (window.confirm('Clear all saved bookmarks?')) {
                  clearBookmarks();
                }
              }}
              className="py-2 px-3 rounded-xl bg-slate-800 hover:bg-rose-900/40 text-slate-400 hover:text-rose-300 border border-slate-700/60 font-medium text-xs transition"
              title="Clear all bookmarks"
            >
              <Trash2 className="w-3.5 h-3.5" />
            </button>
          </div>
        )}
      </aside>
    </div>
  );
}
