import React, { useState, useRef, useEffect } from 'react';
import { Palette, Sun, Moon, Sparkles, Check, Gem } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';

export default function ThemeSwitcher() {
  const { theme, setTheme, themes } = useTheme();
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef(null);

  // Close dropdown when clicking outside
  useEffect(() => {
    function handleClickOutside(event) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const getThemeIcon = (id) => {
    switch (id) {
      case 'dark':
        return <Moon className="w-4 h-4 text-zinc-100" />;
      case 'bright':
        return <Sun className="w-4 h-4 text-amber-500" />;
      case 'metallic-green':
        return <Gem className="w-4 h-4 text-emerald-400" />;
      default:
        return <Sparkles className="w-4 h-4 text-indigo-400" />;
    }
  };

  const currentThemeObj = themes.find((t) => t.id === theme) || themes[0];

  return (
    <div className="relative inline-block text-left" ref={dropdownRef}>
      {/* Trigger Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="p-1.5 px-2.5 rounded-lg bg-slate-800 hover:bg-slate-700/80 text-slate-200 border border-slate-700/70 transition flex items-center gap-2 text-xs font-semibold shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
        title="Change Theme (Default, Dark, Bright, Metallic Green)"
        aria-label="Theme selector"
        aria-expanded={isOpen}
      >
        <span className="flex items-center gap-1.5">
          {getThemeIcon(theme)}
          <span className="hidden sm:inline font-medium">{currentThemeObj.name}</span>
        </span>
        <span
          className={`w-2 h-2 rounded-full ${currentThemeObj.dotColor} shadow-sm shrink-0`}
        />
      </button>

      {/* Dropdown Menu */}
      {isOpen && (
        <div className="absolute right-0 mt-2 w-64 rounded-2xl bg-slate-900 border border-slate-700/80 shadow-2xl p-2 z-50 animate-in fade-in zoom-in-95 duration-150">
          <div className="px-3 py-2 border-b border-slate-800/80 mb-1 flex items-center justify-between">
            <span className="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
              <Palette className="w-3.5 h-3.5 text-indigo-400" />
              Theme Appearance
            </span>
            <span className="text-[10px] text-slate-400 font-mono">4 Themes</span>
          </div>

          <div className="space-y-1">
            {themes.map((t) => {
              const isSelected = theme === t.id;

              return (
                <button
                  key={t.id}
                  onClick={() => {
                    setTheme(t.id);
                    setIsOpen(false);
                  }}
                  className={`w-full text-left p-2.5 rounded-xl transition flex items-center justify-between group ${
                    isSelected
                      ? 'bg-slate-800 text-white border border-slate-700/80 shadow-sm'
                      : 'text-slate-300 hover:bg-slate-800/50 hover:text-white'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <div
                      className="w-7 h-7 rounded-lg flex items-center justify-center border border-slate-700 shadow-inner shrink-0"
                      style={{ backgroundColor: t.surfaceColor }}
                    >
                      {getThemeIcon(t.id)}
                    </div>
                    <div>
                      <div className="text-xs font-semibold flex items-center gap-1.5">
                        <span>{t.name}</span>
                        {t.id === 'metallic-green' && (
                          <span className="text-[9px] px-1.5 py-0.2 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 font-mono">
                            Favorite
                          </span>
                        )}
                      </div>
                      <div className="text-[10px] text-slate-400 leading-tight">
                        {t.description}
                      </div>
                    </div>
                  </div>

                  {isSelected && (
                    <Check className="w-4 h-4 text-indigo-400 shrink-0 ml-2" />
                  )}
                </button>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
