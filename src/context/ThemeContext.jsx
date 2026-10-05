import React, { createContext, useContext, useState, useEffect } from 'react';

const ThemeContext = createContext();

export const THEMES = [
  {
    id: 'default',
    name: 'Default Slate',
    description: 'Deep navy midnight slate with indigo accents',
    iconColor: '#6366f1',
    badgeBg: 'bg-indigo-500/20 text-indigo-300 border-indigo-500/40',
    dotColor: 'bg-indigo-500',
    surfaceColor: '#0f172a'
  },
  {
    id: 'dark',
    name: 'Pure OLED Dark',
    description: 'Pitch black high-contrast OLED night mode',
    iconColor: '#ffffff',
    badgeBg: 'bg-zinc-800 text-zinc-100 border-zinc-700',
    dotColor: 'bg-zinc-100',
    surfaceColor: '#000000'
  },
  {
    id: 'bright',
    name: 'Bright Day',
    description: 'Clean modern daylight theme with crisp readability',
    iconColor: '#4f46e5',
    badgeBg: 'bg-slate-200 text-slate-800 border-slate-300',
    dotColor: 'bg-amber-400',
    surfaceColor: '#ffffff'
  },
  {
    id: 'metallic-green',
    name: 'Metallic Green',
    description: 'Brushed titanium emerald & obsidian cyber green',
    iconColor: '#10b981',
    badgeBg: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40',
    dotColor: 'bg-emerald-400',
    surfaceColor: '#052e1f'
  }
];

export function ThemeProvider({ children }) {
  const [theme, setThemeState] = useState(() => {
    return localStorage.getItem('the_era_of_ai_theme') || 'default';
  });

  const setTheme = (newTheme) => {
    setThemeState(newTheme);
    localStorage.setItem('the_era_of_ai_theme', newTheme);
  };

  useEffect(() => {
    const root = document.documentElement;
    root.setAttribute('data-theme', theme);
    if (theme === 'bright') {
      root.classList.remove('dark');
      root.classList.add('light');
    } else {
      root.classList.remove('light');
      root.classList.add('dark');
    }
  }, [theme]);

  return (
    <ThemeContext.Provider value={{ theme, setTheme, themes: THEMES }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
}
