import React, { useState, useEffect } from 'react';
import { Routes, Route, Navigate, useNavigate, useLocation } from 'react-router-dom';
import Navbar from './components/Navbar';
import SearchModal from './components/SearchModal';
import AboutModal from './components/AboutModal';
import BookmarksDrawer from './components/BookmarksDrawer';
import KineticIntro from './components/KineticIntro';
import GardenCompanion from './components/GardenCompanion';
import AssessmentModal from './components/AssessmentModal';
import CheatsheetBuilderModal from './components/CheatsheetBuilderModal';
import TimelineModal from './components/TimelineModal';
import PythonSandboxModal from './components/PythonSandboxModal';
import LandingHeroPage from './pages/LandingHeroPage';
import KnowledgeHubPage from './pages/KnowledgeHubPage';
import MindMapPage from './pages/MindMapPage';
import SyllabusPage from './pages/SyllabusPage';
import PapersPage from './pages/PapersPage';
import ProjectsPage from './pages/ProjectsPage';
import InterviewPage from './pages/InterviewPage';
import ConceptsPage from './pages/ConceptsPage';
import PlaygroundsPage from './pages/PlaygroundsPage';

// Component to handle backwards-compatible hash URLs (e.g., #interview, #papers)
function HashListener() {
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const hash = window.location.hash.replace('#', '').toLowerCase();
    if (!hash) return;

    if (hash === 'home' || hash === 'hero') navigate('/', { replace: true });
    else if (hash === 'interview') navigate('/interview', { replace: true });
    else if (hash === 'papers') navigate('/papers', { replace: true });
    else if (hash === 'projects' || hash === 'casestudies') navigate('/projects', { replace: true });
    else if (hash === 'syllabus') navigate('/syllabus', { replace: true });
    else if (hash === 'concept' || hash === 'concepts') navigate('/concepts', { replace: true });
    else if (hash === 'mindmap') navigate('/mindmap', { replace: true });
  }, [navigate]);

  return null;
}

// Global UI Error Boundary to prevent any route crash from unmounting the app
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }
  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }
  componentDidCatch(error, errorInfo) {
    console.error('UI ErrorBoundary caught error:', error, errorInfo);
  }
  render() {
    if (this.state.hasError) {
      return (
        <div className="flex-1 w-full h-full flex flex-col items-center justify-center p-6 text-center bg-slate-950 text-slate-100">
          <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 max-w-md space-y-4 shadow-2xl">
            <h2 className="text-xl font-bold text-white">Mind Map Loading Alert</h2>
            <p className="text-xs text-slate-400 leading-relaxed">
              {this.state.error?.message || 'The interactive graph encountered a layout recovery event.'}
            </p>
            <button
              onClick={() => {
                this.setState({ hasError: false, error: null });
                window.location.reload();
              }}
              className="px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs transition shadow-lg shadow-indigo-600/30"
            >
              Reload Page
            </button>
          </div>
        </div>
      );
    }
    return this.props.children;
  }
}

// SEO Manager for dynamic document titles and meta descriptions
function SEOManager() {
  const location = useLocation();

  useEffect(() => {
    const path = location.pathname.toLowerCase();
    let pageTitle = 'The Era of AI — Master Knowledge Graph & Portal';
    let metaDesc = 'Master AI & Machine Learning Knowledge Graph, Interactive Mind Map, Complete Syllabus, Landmark Research Papers Hub, Production Case Studies, and 150+ Interview Vault.';

    if (path === '/' || path === '') {
      pageTitle = 'The Era of AI — Enter the World of AI | Master Knowledge Portal';
      metaDesc = 'Explore the complete multidimensional universe of Artificial Intelligence and Machine Learning: interactive mind map, line-wise curriculum, research papers, and technical interview vault.';
    } else if (path.includes('/mindmap')) {
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
    } else if (path.includes('/playground')) {
      pageTitle = 'Interactive ML Playgrounds & Simulators — The Era of AI';
      metaDesc = 'Real-time multi-head attention matrix heatmaps and 2D gradient descent physics simulations with dynamic optimizers.';
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
  const location = useLocation();
  const [isSearchOpen, setIsSearchOpen] = useState(false);
  const [isAboutOpen, setIsAboutOpen] = useState(false);
  const [isBookmarksOpen, setIsBookmarksOpen] = useState(false);
  const [isAssessmentOpen, setIsAssessmentOpen] = useState(false);
  const [isCheatsheetOpen, setIsCheatsheetOpen] = useState(false);
  const [isTimelineOpen, setIsTimelineOpen] = useState(false);
  const [isPythonLabOpen, setIsPythonLabOpen] = useState(false);
  const [showKineticIntro, setShowKineticIntro] = useState(false);

  const handleCloseKinetic = () => {
    setShowKineticIntro(false);
  };

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
        onOpenKinetic={() => setShowKineticIntro(true)}
        onOpenBookmarks={() => setIsBookmarksOpen(true)}
        onOpenAssessment={() => setIsAssessmentOpen(true)}
        onOpenCheatsheet={() => setIsCheatsheetOpen(true)}
        onOpenTimeline={() => setIsTimelineOpen(true)}
        onOpenPythonLab={() => setIsPythonLabOpen(true)}
      />

      {/* Main Routed Page Viewport */}
      <main className="relative flex-1 w-full h-full overflow-hidden flex flex-col">
        <ErrorBoundary>
          <Routes>
            <Route path="/" element={<LandingHeroPage onOpenAbout={() => setIsAboutOpen(true)} />} />
            <Route path="/mindmap" element={<KnowledgeHubPage />} />
            <Route path="/syllabus" element={<KnowledgeHubPage />} />
            <Route path="/papers" element={<PapersPage />} />
            <Route path="/projects" element={<ProjectsPage />} />
            <Route path="/case-studies" element={<ProjectsPage />} />
            <Route path="/interview" element={<InterviewPage onOpenAssessment={() => setIsAssessmentOpen(true)} />} />
            <Route path="/concepts" element={<ConceptsPage />} />
            <Route path="/concept" element={<ConceptsPage />} />
            <Route path="/playgrounds" element={<PlaygroundsPage />} />
            <Route path="/playground" element={<PlaygroundsPage />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </ErrorBoundary>
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

      {/* AI Readiness Diagnostic Assessment Modal */}
      <AssessmentModal
        isOpen={isAssessmentOpen}
        onClose={() => setIsAssessmentOpen(false)}
      />

      {/* High-Yield Cheatsheet Builder & PDF Exporter Modal */}
      <CheatsheetBuilderModal
        isOpen={isCheatsheetOpen}
        onClose={() => setIsCheatsheetOpen(false)}
      />

      {/* Interactive AI History Timeline Modal (1950–2026) */}
      <TimelineModal
        isOpen={isTimelineOpen}
        onClose={() => setIsTimelineOpen(false)}
      />

      {/* In-Browser Python & AI Math Sandbox (WebAssembly Pyodide) */}
      <PythonSandboxModal
        isOpen={isPythonLabOpen}
        onClose={() => setIsPythonLabOpen(false)}
      />

      {/* Saved Bookmarks & Study Cheatsheet Slide-Over Drawer */}
      <BookmarksDrawer
        isOpen={isBookmarksOpen}
        onClose={() => setIsBookmarksOpen(false)}
        onOpenCheatsheet={() => {
          setIsBookmarksOpen(false);
          setIsCheatsheetOpen(true);
        }}
      />

      {/* Kinetic Physics Opening Visualization */}
      <KineticIntro
        isOpen={showKineticIntro}
        onClose={handleCloseKinetic}
      />

      {/* Interactive Corner Companion: Moving Robot & Child in Garden */}
      {location.pathname !== '/' && location.pathname !== '' && <GardenCompanion />}
    </div>
  );
}
