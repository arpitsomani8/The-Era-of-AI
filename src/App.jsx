import React, { useState, useEffect } from 'react';
import { Routes, Route, Navigate, useNavigate, useLocation } from 'react-router-dom';
import Navbar from './components/Navbar';
import SearchModal from './components/SearchModal';
import AboutModal from './components/AboutModal';
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

// SEO Manager for dynamic document titles and meta descriptions
function SEOManager() {
  const location = useLocation();

  useEffect(() => {
    const path = location.pathname.toLowerCase();
    let pageTitle = 'The Era of AI — Master Knowledge Graph & Portal';
    let metaDesc = 'Master AI & Machine Learning Knowledge Graph, Interactive Mind Map, Complete Syllabus, Landmark Research Papers Hub, Production Case Studies, and 150+ Interview Vault.';

    if (path.includes('/mindmap')) {
      pageTitle = 'Interactive Mind Map — The Era of AI | 41 Domain Graph Nodes';
      metaDesc = 'Explore the 2D interactive knowledge graph of AI, Classical ML, Deep Learning, and Transformers with dynamic cross-links and mathematical foundations.';
    } else if (path.includes('/syllabus')) {
      pageTitle = 'Line-Wise Syllabus & Curriculum — The Era of AI | 7 Tracks';
      metaDesc = 'Comprehensive line-wise curriculum covering Mathematical Foundations, Preprocessing, Classical ML, Evaluation, Deep Learning, and GenAI.';
    } else if (path.includes('/papers')) {
      pageTitle = 'Landmark AI & ML Research Papers — The Era of AI | Daily Updated';
      metaDesc = 'Curated collection of 22+ milestone AI papers from Attention Is All You Need to DeepSeek-R1 with daily arXiv tracking and summaries.';
    } else if (path.includes('/projects') || path.includes('/case-studies')) {
      pageTitle = 'Production ML & LLM Case Studies — The Era of AI';
      metaDesc = '5 end-to-end industrial architectures, fraud detection engines, enterprise RAG systems, and medical vision pipelines.';
    } else if (path.includes('/interview')) {
      pageTitle = '150+ AI & ML Technical Interview Vault — The Era of AI';
      metaDesc = 'Comprehensive vault of 150+ technical interview questions with mathematical proofs, Python implementations, and deep architectural explanations.';
    } else if (path.includes('/concept')) {
      pageTitle = 'Core Concepts & Deep Technical Guides — The Era of AI';
      metaDesc = 'In-depth mathematical formulations, code implementations, and visual explanations across all machine learning and deep learning domains.';
    }

    document.title = pageTitle;

    const descTag = document.querySelector('meta[name="description"]');
    if (descTag) descTag.setAttribute('content', metaDesc);

    const ogTitle = document.querySelector('meta[property="og:title"]');
    if (ogTitle) ogTitle.setAttribute('content', pageTitle);

    const twitterTitle = document.querySelector('meta[name="twitter:title"]');
    if (twitterTitle) twitterTitle.setAttribute('content', pageTitle);
  }, [location.pathname]);

  return null;
}

export default function App() {
  const [isSearchOpen, setIsSearchOpen] = useState(false);
  const [isAboutOpen, setIsAboutOpen] = useState(false);

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
      <SEOManager />
      
      {/* Top Main Navigation Header */}
      <Navbar 
        onOpenSearch={() => setIsSearchOpen(true)} 
        onOpenAbout={() => setIsAboutOpen(true)}
      />

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

      {/* About Portal Modal (Features Thumbnail & Logo) */}
      <AboutModal
        isOpen={isAboutOpen}
        onClose={() => setIsAboutOpen(false)}
      />
    </div>
  );
}
