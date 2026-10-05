import React, { useState, useMemo } from 'react';
import { useSearchParams } from 'react-router-dom';
import { 
  Briefcase, 
  Search, 
  Code, 
  Copy, 
  Check, 
  Layers, 
  CheckCircle2, 
  Cpu, 
  ExternalLink,
  Bookmark
} from 'lucide-react';
import projectsData from '../data/projects.json';
import { useProgress } from '../context/ProgressContext';

export default function ProjectsPage() {
  const { toggleCompleted, isCompleted, toggleBookmark, isBookmarked } = useProgress();
  const [searchParams] = useSearchParams();
  const initialSearch = searchParams.get('search') || '';
  const [searchQuery, setSearchQuery] = useState(initialSearch);
  const [copiedId, setCopiedId] = useState(null);

  const filteredProjects = useMemo(() => {
    return projectsData.filter((proj) => {
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase();
        const matchTitle = proj.title?.toLowerCase().includes(q);
        const matchSub = proj.subtitle?.toLowerCase().includes(q);
        const matchArch = proj.architecture_summary?.toLowerCase().includes(q);
        const matchTech = proj.tech_stack?.some((t) => t.toLowerCase().includes(q));
        if (!matchTitle && !matchSub && !matchArch && !matchTech) return false;
      }
      return true;
    });
  }, [searchQuery]);

  const handleCopyCode = (id, code) => {
    navigator.clipboard.writeText(code);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  return (
    <div className="flex-1 w-full h-full overflow-y-auto bg-slate-950 text-slate-100 p-4 sm:p-6 md:p-10">
      <div className="max-w-5xl mx-auto space-y-8 pb-20">
        {/* Header */}
        <div className="border-b border-slate-800 pb-6">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-300 border border-emerald-500/30 text-xs font-semibold uppercase tracking-wider mb-2">
            <Briefcase className="w-3.5 h-3.5" />
            Production Case Studies
          </div>
          <h1 className="text-2xl sm:text-3xl md:text-4xl font-extrabold text-white tracking-tight">
            Enterprise AI Architectures & Implementations
          </h1>
          <p className="text-xs sm:text-sm text-slate-400 mt-1 max-w-3xl">
            Real-world end-to-end production AI deployments: multi-tenant agentic engines, fraud detection graph networks, clinical HIPAA RAG systems, and self-healing codebase agents.
          </p>
        </div>

        {/* Search Input */}
        <div className="relative max-w-md">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search projects by title, stack (e.g. Kafka, Ray, Qdrant)..."
            className="w-full bg-slate-900 border border-slate-800 text-xs sm:text-sm text-white rounded-xl pl-9 pr-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-emerald-500 placeholder-slate-500"
          />
          <Search className="w-4 h-4 absolute left-3 top-3 text-slate-500" />
          {searchQuery && (
            <button
              onClick={() => setSearchQuery('')}
              className="absolute right-3 top-2.5 text-slate-500 hover:text-white text-xs"
            >
              &times;
            </button>
          )}
        </div>

        {/* Projects List */}
        <div className="space-y-10">
          {filteredProjects.map((project, idx) => (
            <article
              key={project.id || idx}
              className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 sm:p-8 shadow-lg space-y-6"
            >
              {/* Top Banner */}
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 border-b border-slate-800/80 pb-4">
                <div>
                  <div className="flex items-center gap-2 mb-1.5 flex-wrap">
                    <span className="px-2.5 py-0.5 rounded-full text-[11px] font-bold uppercase tracking-wider bg-emerald-500/10 text-emerald-300 border border-emerald-500/30">
                      {project.badge || 'Production Ready'}
                    </span>
                    <span className="text-xs text-slate-400">
                      {project.category}
                    </span>
                    {isCompleted(`project-${project.id}`) && (
                      <span className="text-[10px] px-2 py-0.5 rounded-full font-semibold bg-emerald-500/15 text-emerald-300 border border-emerald-500/30 flex items-center gap-1">
                        <CheckCircle2 className="w-3 h-3 text-emerald-400" />
                        Studied
                      </span>
                    )}
                  </div>
                  <h2 className="text-xl sm:text-2xl font-bold text-white tracking-tight">
                    {project.title}
                  </h2>
                  <p className="text-xs sm:text-sm text-slate-400 mt-0.5">
                    {project.subtitle}
                  </p>
                </div>

                <div className="flex items-center gap-2 shrink-0">
                  <button
                    onClick={() => toggleCompleted(`project-${project.id}`)}
                    className={`px-3 py-1.5 rounded-lg border text-xs font-medium transition flex items-center gap-1.5 ${
                      isCompleted(`project-${project.id}`)
                        ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40'
                        : 'bg-slate-800 text-slate-400 hover:text-white border-slate-700'
                    }`}
                    title={isCompleted(`project-${project.id}`) ? 'Mark Incomplete' : 'Mark Case Study Studied'}
                  >
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    <span>{isCompleted(`project-${project.id}`) ? 'Studied' : 'Mark Done'}</span>
                  </button>

                  <button
                    onClick={() => toggleBookmark({
                      id: `project-${project.id}`,
                      type: 'concept',
                      title: project.title,
                      subtitle: `${project.category} Case Study`,
                      link: `/projects?search=${encodeURIComponent(project.title.slice(0, 20))}`
                    })}
                    className={`p-1.5 rounded-lg border transition ${
                      isBookmarked(`project-${project.id}`)
                        ? 'bg-amber-500/20 text-amber-300 border-amber-500/40'
                        : 'bg-slate-800 text-slate-400 hover:text-white border-slate-700'
                    }`}
                    title="Bookmark case study"
                  >
                    <Bookmark className={`w-4 h-4 ${isBookmarked(`project-${project.id}`) ? 'fill-amber-400 text-amber-400' : ''}`} />
                  </button>
                </div>
              </div>

              {/* Tech Stack Pills */}
              {project.tech_stack && (
                <div>
                  <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                    <Cpu className="w-3.5 h-3.5 text-emerald-400" />
                    Production Tech Stack:
                  </h3>
                  <div className="flex flex-wrap gap-1.5">
                    {project.tech_stack.map((tech, tIdx) => (
                      <span
                        key={tIdx}
                        className="px-2.5 py-1 rounded-md text-xs font-mono bg-slate-950 text-emerald-300 border border-slate-800"
                      >
                        {tech}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Architecture Summary */}
              {project.architecture_summary && (
                <div className="bg-slate-950/60 p-4 rounded-xl border border-slate-800">
                  <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-1.5 flex items-center gap-1.5">
                    <Layers className="w-3.5 h-3.5 text-indigo-400" />
                    Architecture & System Design
                  </h3>
                  <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
                    {project.architecture_summary}
                  </p>
                </div>
              )}

              {/* Key Highlights Grid */}
              {project.key_highlights && project.key_highlights.length > 0 && (
                <div>
                  <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-3">
                    Key Performance & Engineering Highlights:
                  </h3>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    {project.key_highlights.map((highlight, hIdx) => (
                      <div
                        key={hIdx}
                        className="p-3 rounded-xl bg-slate-950/40 border border-slate-800/80 flex items-start gap-2.5 text-xs"
                      >
                        <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                        <span className="text-slate-300 leading-relaxed">{highlight}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Code Snippet Card */}
              {project.code_snippet && (
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
                      <Code className="w-3.5 h-3.5 text-amber-400" />
                      {project.code_description || 'Core Implementation Code'}
                    </h3>
                    <button
                      onClick={() => handleCopyCode(project.id || idx, project.code_snippet)}
                      className="px-2.5 py-1 rounded-md bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white border border-slate-700 text-xs flex items-center gap-1.5 transition"
                    >
                      {copiedId === (project.id || idx) ? (
                        <>
                          <Check className="w-3.5 h-3.5 text-emerald-400" />
                          <span className="text-emerald-400">Copied!</span>
                        </>
                      ) : (
                        <>
                          <Copy className="w-3.5 h-3.5" />
                          <span>Copy Code</span>
                        </>
                      )}
                    </button>
                  </div>
                  <div className="bg-slate-950 border border-slate-800 rounded-xl p-4 overflow-x-auto text-xs font-mono text-emerald-300 leading-relaxed">
                    <pre>
                      <code>{project.code_snippet}</code>
                    </pre>
                  </div>
                </div>
              )}
            </article>
          ))}
        </div>
      </div>
    </div>
  );
}
