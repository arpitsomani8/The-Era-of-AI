import React, { useState, useEffect } from 'react';
import { Routes, Route, Navigate, useNavigate, useLocation } from 'react-router-dom';
import Navbar from './components/Navbar';
import SearchModal from './components/SearchModal';
import MindMapPage from './pages/MindMapPage';
import SyllabusPage from './pages/SyllabusPage';
import PapersPage from './pages/PapersPage';
import ProjectsPage from './pages/ProjectsPage';
import InterviewPage from './pages/InterviewPage';
import ConceptsPage from './pages/ConceptsPage';

// Component to handle backwards-compatible hash URLs (e.g., #interview, #papers)
function HashListener() {
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const hash = window.location.hash.replace('#', '').toLowerCase();
    if (!hash) return;

    if (hash === 'interview') navigate('/interview', { replace: true });
    else if (hash === 'papers') navigate('/papers', { replace: true });
    else if (hash === 'projects' || hash === 'casestudies') navigate('/projects', { replace: true });
    else if (hash === 'syllabus') navigate('/syllabus', { replace: true });
    else if (hash === 'concept' || hash === 'concepts') navigate('/concepts', { replace: true });
    else if (hash === 'mindmap') navigate('/mindmap', { replace: true });
  }, [navigate]);

  return null;
}

export default function App() {
  const [isSearchOpen, setIsSearchOpen] = useState(false);

  // Global keyboard shortcut: Cmd+K / Ctrl+K
  useEffect(() => {
    const handleKeyDown = (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        setIsSearchOpen((prev) => !prev);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  return (
    <div className="h-screen w-screen flex flex-col overflow-hidden bg-slate-950 text-slate-100 font-sans">
      <HashListener />
      
      {/* Top Main Navigation Header */}
      <Navbar onOpenSearch={() => setIsSearchOpen(true)} />

      {/* Main Routed Page Viewport */}
      <main className="relative flex-1 w-full h-full overflow-hidden flex flex-col">
        <Routes>
          <Route path="/" element={<Navigate to="/mindmap" replace />} />
          <Route path="/mindmap" element={<MindMapPage />} />
          <Route path="/syllabus" element={<SyllabusPage />} />
          <Route path="/papers" element={<PapersPage />} />
          <Route path="/projects" element={<ProjectsPage />} />
          <Route path="/case-studies" element={<ProjectsPage />} />
          <Route path="/interview" element={<InterviewPage />} />
          <Route path="/concepts" element={<ConceptsPage />} />
          <Route path="/concept" element={<ConceptsPage />} />
          <Route path="*" element={<Navigate to="/mindmap" replace />} />
        </Routes>
      </main>

      {/* Universal Search Modal (Cmd+K) */}
      <SearchModal
        isOpen={isSearchOpen}
        onClose={() => setIsSearchOpen(false)}
      />
    </div>
  );
}
