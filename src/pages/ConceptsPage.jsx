import React, { useState, useMemo, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { 
  Layers, 
  Search, 
  BookOpen, 
  Calculator, 
  Lightbulb, 
  Sparkles, 
  Tag, 
  ChevronRight,
  Share2,
  Check,
  Bookmark,
  CheckCircle2,
  Copy,
  Download,
  GraduationCap,
  AlertTriangle,
  HelpCircle,
  ArrowRight,
  Cpu,
  Zap,
  ListOrdered
} from 'lucide-react';
import conceptsData from '../data/concepts.json';
import KaTeXRenderer, { MathText } from '../components/KaTeXRenderer';
import { useProgress } from '../context/ProgressContext';
import AudioExplainerButton from '../components/AudioExplainerButton';

export default function ConceptsPage() {
  const { toggleCompleted, isCompleted, toggleBookmark, isBookmarked } = useProgress();
  const [searchParams, setSearchParams] = useSearchParams();
  const conceptIdParam = searchParams.get('id');
  const searchParam = searchParams.get('search');
  const topicParam = searchParams.get('topic');
  const categoryParam = searchParams.get('category');

  const [selectedConceptId, setSelectedConceptId] = useState(
    () => conceptIdParam || (conceptsData[0] ? conceptsData[0].id : null)
  );
  const [searchQuery, setSearchQuery] = useState(() => searchParam || '');
  const [activeCategory, setActiveCategory] = useState(() => categoryParam || 'all');
  const [copiedLink, setCopiedLink] = useState(false);
  const [copiedFormula, setCopiedFormula] = useState(false);

  const completedConceptsCount = useMemo(() => {
    return conceptsData.filter((c) => isCompleted(`concept-${c.id}`)).length;
  }, [isCompleted]);

  const completionPercentage = Math.round(
    (completedConceptsCount / (conceptsData.length || 1)) * 100
  );

  const handleExportRevisionGuide = () => {
    const masteredConcepts = conceptsData.filter((c) => isCompleted(`concept-${c.id}`));
    let md = `# The Era of AI — Concept Mastery Revision Guide\n`;
    md += `*Generated: ${new Date().toLocaleDateString()} • Progress: ${completedConceptsCount}/${conceptsData.length} Concepts (${completionPercentage}%)*\n\n`;
    
    if (masteredConcepts.length === 0) {
      md += `*No concepts marked as mastered yet. Click "Mark Done" on any concept in the encyclopedia to build your revision guide.*\n\n`;
    } else {
      md += `## 🏆 Mastered Concepts (${masteredConcepts.length})\n\n`;
      masteredConcepts.forEach((c, idx) => {
        md += `### ${idx + 1}. ${c.title} (${c.category_label || c.category})\n`;
        md += `- **Module:** ${c.topic_label}\n`;
        if (c.def) md += `- **Definition:** ${c.def}\n`;
        if (c.formula) md += `- **Formulation:** \`${c.formula}\`\n`;
        if (c.logic) md += `- **Key Intuition:** ${c.logic}\n`;
        md += `\n---\n\n`;
      });
    }

    const blob = new Blob([md], { type: 'text/markdown;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `The-Era-of-AI-Revision-Guide-${new Date().toISOString().slice(0, 10)}.md`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  // Sync state with URL search params whenever they change
  useEffect(() => {
    // 1. Direct Concept ID
    if (conceptIdParam) {
      const match = conceptsData.find((c) => c.id === conceptIdParam);
      if (match) {
        setSelectedConceptId(match.id);
        if (match.category) {
          setActiveCategory(match.category);
        }
        setSearchQuery('');
        return;
      }
    }

    // 2. Topic ID scoped
    if (topicParam) {
      const topicMatches = conceptsData.filter((c) => c.topic_id === topicParam);
      if (topicMatches.length > 0) {
        setSelectedConceptId(topicMatches[0].id);
        if (topicMatches[0].category) {
          setActiveCategory(topicMatches[0].category);
        }
        setSearchQuery('');
        return;
      }
    }

    // 3. Category scoped
    if (categoryParam) {
      setActiveCategory(categoryParam);
      const catMatches = conceptsData.filter((c) => c.category === categoryParam);
      if (catMatches.length > 0) {
        setSelectedConceptId(catMatches[0].id);
      }
      return;
    }

    // 4. Search query
    if (searchParam) {
      setSearchQuery(searchParam);
      setActiveCategory('all');
    }
  }, [conceptIdParam, topicParam, categoryParam, searchParam]);

  const categories = [
    { id: 'all', label: 'All Modules (170)' },
    { id: 'math', label: '1. Math Foundations' },
    { id: 'data', label: '2. Data Preprocessing' },
    { id: 'ml', label: '3. Classical ML' },
    { id: 'eval', label: '4. Model Evaluation' },
    { id: 'dl', label: '5. Deep Learning' },
    { id: 'genai', label: '6. Transformers & GenAI' },
    { id: 'mlops', label: '7. MLOps' }
  ];

  const filteredConcepts = useMemo(() => {
    return conceptsData.filter((c) => {
      if (activeCategory !== 'all' && c.category !== activeCategory) {
        return false;
      }
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase().trim();
        const tokens = q.split(/[\s,&]+/).filter((t) => t.length > 1);
        
        const title = (c.title || '').toLowerCase();
        const def = (c.def || '').toLowerCase();
        const topic = (c.topic_label || '').toLowerCase();
        const tags = (c.tags || []).join(' ').toLowerCase();
        const combined = `${title} ${def} ${topic} ${tags}`;

        if (title.includes(q) || combined.includes(q)) return true;
        if (tokens.length > 0 && tokens.some((t) => combined.includes(t))) return true;
        return false;
      }
      return true;
    });
  }, [activeCategory, searchQuery]);

  // Group filtered concepts by Sub-Topic / Module
  const groupedConcepts = useMemo(() => {
    const groups = [];
    const topicMap = new Map();

    filteredConcepts.forEach((concept) => {
      const topic = concept.topic_label || 'Other Concepts';
      if (!topicMap.has(topic)) {
        const group = {
          topic,
          topic_id: concept.topic_id,
          category: concept.category,
          category_label: concept.category_label,
          items: []
        };
        topicMap.set(topic, group);
        groups.push(group);
      }
      topicMap.get(topic).items.push(concept);
    });

    return groups;
  }, [filteredConcepts]);

  // Selected Concept resolution: prioritize match in filteredConcepts
  const selectedConcept = useMemo(() => {
    const foundInFiltered = filteredConcepts.find((c) => c.id === selectedConceptId);
    if (foundInFiltered) return foundInFiltered;

    if (filteredConcepts.length > 0) {
      return filteredConcepts[0];
    }

    return conceptsData.find((c) => c.id === selectedConceptId) || conceptsData[0];
  }, [selectedConceptId, filteredConcepts]);

  // Auto-scroll sidebar list to the selected concept
  useEffect(() => {
    if (selectedConcept?.id) {
      const el = document.getElementById(`concept-item-${selectedConcept.id}`);
      if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }
    }
  }, [selectedConcept?.id]);

  const handleSelect = (id) => {
    setSelectedConceptId(id);
    setSearchParams({ id });
  };

  const handleCopyLink = () => {
    navigator.clipboard.writeText(window.location.href);
    setCopiedLink(true);
    setTimeout(() => setCopiedLink(false), 2000);
  };

  return (
    <div className="flex-1 w-full h-full flex flex-col md:flex-row overflow-hidden bg-slate-950 text-slate-100">
      {/* Left Sidebar: 170 Concepts Directory */}
      <aside className="w-full md:w-80 lg:w-96 border-r border-slate-800 bg-slate-900/60 flex flex-col shrink-0 h-1/3 md:h-full">
        {/* Sidebar Header & Search */}
        <div className="p-4 border-b border-slate-800 space-y-3 bg-slate-950/40">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Layers className="w-4 h-4 text-rose-400" />
              <h2 className="text-sm font-bold text-white uppercase tracking-wider">
                Concept Encyclopedia
              </h2>
            </div>
            <span className="text-xs px-2 py-0.5 rounded-full bg-slate-800 text-slate-400 border border-slate-700 font-mono">
              {filteredConcepts.length}
            </span>
          </div>

          {/* Search Box */}
          <div className="relative">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search concepts by topic, formula, or keyword..."
              className="w-full bg-slate-900 border border-slate-800 text-xs text-white rounded-lg pl-8 pr-3 py-1.5 focus:outline-none focus:ring-2 focus:ring-rose-500 placeholder-slate-500"
            />
            <Search className="w-3.5 h-3.5 absolute left-2.5 top-2.5 text-slate-500" />
            {searchQuery && (
              <button
                onClick={() => setSearchQuery('')}
                className="absolute right-2.5 top-1.5 text-slate-500 hover:text-white text-xs"
              >
                &times;
              </button>
            )}
          </div>

          {/* Category Filter Pills */}
          <div className="flex items-center overflow-x-auto no-scrollbar space-x-1 pt-1 pb-0.5">
            {categories.map((cat) => (
              <button
                key={cat.id}
                onClick={() => setActiveCategory(cat.id)}
                className={`px-2 py-1 rounded-md text-[11px] font-medium whitespace-nowrap transition ${
                  activeCategory === cat.id
                    ? 'bg-rose-600 text-white shadow'
                    : 'bg-slate-900 text-slate-400 hover:text-white border border-slate-800'
                }`}
              >
                {cat.label}
              </button>
            ))}
          </div>
        </div>

        {/* Concept Items Scrollable List: Grouped by Sub-Topic / Module */}
        <div className="flex-1 overflow-y-auto p-2 space-y-3">
          {groupedConcepts.map((group, gIdx) => (
            <div key={gIdx} className="space-y-1">
              {/* Sub-Topic Header */}
              <div className="px-2 pt-1 pb-1 flex items-center justify-between text-[11px] font-bold text-slate-400 uppercase tracking-wider sticky top-0 bg-slate-900/95 backdrop-blur-sm z-10 border-b border-slate-800/80">
                <span className="truncate pr-1">{group.topic}</span>
                <span className="text-[10px] px-1.5 py-0.2 rounded-full bg-slate-800 text-slate-400 font-mono shrink-0">
                  {group.items.length}
                </span>
              </div>

              {/* Concepts within Sub-Topic */}
              <div className="space-y-0.5">
                {group.items.map((concept) => {
                  const isSelected = selectedConcept?.id === concept.id;
                  const isDone = isCompleted(`concept-${concept.id}`);

                  return (
                    <div
                      key={concept.id}
                      id={`concept-item-${concept.id}`}
                      onClick={() => handleSelect(concept.id)}
                      className={`p-2 rounded-xl cursor-pointer transition flex items-center justify-between gap-2 text-xs ${
                        isSelected
                          ? 'bg-rose-600/20 text-white border border-rose-500/40 shadow-sm font-semibold'
                          : 'text-slate-300 hover:bg-slate-800/60 hover:text-white border border-transparent'
                      }`}
                    >
                      <div className="min-w-0 flex items-center gap-2">
                        {isDone && (
                          <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 shrink-0" title="Mastered" />
                        )}
                        <span className="truncate text-xs">
                          {concept.title}
                        </span>
                      </div>
                      <ChevronRight
                        className={`w-3.5 h-3.5 shrink-0 transition-transform ${
                          isSelected ? 'text-rose-400 translate-x-0.5' : 'text-slate-600'
                        }`}
                      />
                    </div>
                  );
                })}
              </div>
            </div>
          ))}
        </div>
      </aside>

      {/* Main Content Area: Selected Concept Detail View */}
      <main className="flex-1 h-2/3 md:h-full overflow-y-auto p-4 sm:p-6 md:p-10">
        {selectedConcept ? (
          <div className="max-w-4xl mx-auto space-y-6 pb-20">
            {/* Curriculum Mastery Progress Banner */}
            <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-4 sm:p-5 flex flex-col lg:flex-row lg:items-center justify-between gap-4 no-print shadow-sm">
              <div className="flex items-center gap-3.5">
                <div className="w-10 h-10 rounded-xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 flex items-center justify-center shrink-0">
                  <CheckCircle2 className="w-5 h-5" />
                </div>
                <div>
                  <div className="text-sm font-bold text-white flex items-center gap-2.5 flex-wrap">
                    <span>Curriculum Mastery Progress</span>
                    <span className="text-emerald-400 font-mono text-xs bg-emerald-500/15 px-2.5 py-0.5 rounded-full border border-emerald-500/30">
                      {completedConceptsCount} / {conceptsData.length} Concepts ({completionPercentage}%)
                    </span>
                  </div>
                  <p className="text-xs text-slate-400 mt-0.5">
                    Mark modules and concepts as mastered to track your study roadmap and export personalized revision guides.
                  </p>
                </div>
              </div>

              <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 shrink-0">
                <div className="w-full sm:w-44 flex flex-col gap-1.5">
                  <div className="flex justify-between text-[11px] text-slate-400 font-mono">
                    <span>Progress</span>
                    <span className="text-emerald-300 font-bold">{completionPercentage}%</span>
                  </div>
                  <div className="w-full bg-slate-800/90 rounded-full h-2.5 overflow-hidden border border-slate-700/60 p-0.5">
                    <div 
                      className="bg-gradient-to-r from-rose-500 via-indigo-500 to-emerald-400 h-full transition-all duration-500 rounded-full"
                      style={{ width: `${completionPercentage}%` }}
                    />
                  </div>
                </div>

                <button
                  onClick={handleExportRevisionGuide}
                  title="Download Personalized Revision Guide (Markdown)"
                  className="px-3 py-2 rounded-xl bg-slate-800 hover:bg-indigo-600/30 text-slate-200 hover:text-white border border-slate-700 hover:border-indigo-500/50 text-xs font-semibold flex items-center justify-center gap-1.5 transition shadow-sm cursor-pointer"
                >
                  <Download className="w-3.5 h-3.5 text-indigo-400" />
                  <span>Export Revision Guide</span>
                </button>
              </div>
            </div>

            {/* Concept Header */}
            <div className="border-b border-slate-800 pb-5 space-y-2">
              <div className="flex flex-wrap items-center justify-between gap-3">
                <div className="flex items-center gap-2 flex-wrap">
                  <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider bg-rose-500/10 text-rose-300 border border-rose-500/30">
                    {selectedConcept.category_label || selectedConcept.category}
                  </span>
                  <span className="text-xs text-slate-400">
                    Module: <strong className="text-slate-200">{selectedConcept.topic_label}</strong>
                  </span>
                  {isCompleted(`concept-${selectedConcept.id}`) && (
                    <span className="text-[10px] px-2 py-0.5 rounded-full font-semibold bg-emerald-500/15 text-emerald-300 border border-emerald-500/30 flex items-center gap-1">
                      <CheckCircle2 className="w-3 h-3 text-emerald-400" />
                      Mastered
                    </span>
                  )}
                </div>

                <div className="flex items-center gap-2 flex-wrap">
                  {/* Audio / AI Voice Explainer */}
                  <AudioExplainerButton
                    title={selectedConcept.title}
                    definition={selectedConcept.def || selectedConcept.definition}
                    intuition={selectedConcept.logic}
                    example={selectedConcept.example}
                  />

                  {/* Mark as Mastered button */}
                  <button
                    onClick={() => toggleCompleted(`concept-${selectedConcept.id}`)}
                    className={`px-2.5 py-1 rounded-lg border text-xs font-medium transition flex items-center gap-1.5 ${
                      isCompleted(`concept-${selectedConcept.id}`)
                        ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40'
                        : 'bg-slate-900 border-slate-800 text-slate-300 hover:text-white hover:bg-slate-800'
                    }`}
                    title={isCompleted(`concept-${selectedConcept.id}`) ? 'Mark Incomplete' : 'Mark as Mastered'}
                  >
                    <CheckCircle2 className={`w-3.5 h-3.5 ${isCompleted(`concept-${selectedConcept.id}`) ? 'text-emerald-400' : ''}`} />
                    <span>{isCompleted(`concept-${selectedConcept.id}`) ? 'Mastered' : 'Mark Done'}</span>
                  </button>

                  {/* Bookmark button */}
                  <button
                    onClick={() => toggleBookmark({
                      id: `concept-${selectedConcept.id}`,
                      type: 'concept',
                      title: selectedConcept.title,
                      subtitle: `${selectedConcept.topic_label} (${selectedConcept.category})`,
                      link: `/concepts?id=${selectedConcept.id}`
                    })}
                    className={`px-2.5 py-1 rounded-lg border text-xs font-medium transition flex items-center gap-1.5 ${
                      isBookmarked(`concept-${selectedConcept.id}`)
                        ? 'bg-amber-500/20 text-amber-300 border-amber-500/40'
                        : 'bg-slate-900 border-slate-800 text-slate-300 hover:text-white hover:bg-slate-800'
                    }`}
                    title={isBookmarked(`concept-${selectedConcept.id}`) ? 'Remove Bookmark' : 'Bookmark Concept'}
                  >
                    <Bookmark className={`w-3.5 h-3.5 ${isBookmarked(`concept-${selectedConcept.id}`) ? 'fill-amber-400 text-amber-400' : ''}`} />
                    <span>{isBookmarked(`concept-${selectedConcept.id}`) ? 'Saved' : 'Save'}</span>
                  </button>

                  {/* Share button */}
                  <button
                    onClick={handleCopyLink}
                    className="px-2.5 py-1 rounded-lg bg-slate-900 border border-slate-800 hover:bg-slate-800 text-xs text-slate-300 hover:text-white transition flex items-center gap-1.5"
                    title="Copy direct link to this concept"
                  >
                    {copiedLink ? (
                      <>
                        <Check className="w-3.5 h-3.5 text-emerald-400" />
                        <span className="text-emerald-400">Link Copied!</span>
                      </>
                    ) : (
                      <>
                        <Share2 className="w-3.5 h-3.5 text-slate-400" />
                        <span>Share</span>
                      </>
                    )}
                  </button>
                </div>
              </div>

              <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight leading-snug">
                {selectedConcept.title}
              </h1>
            </div>

            {/* In-Page Quick Section Navigator */}
            <div className="flex items-center gap-1.5 overflow-x-auto no-scrollbar py-1.5 px-2 bg-slate-900/90 rounded-xl border border-slate-800 text-[11px] sticky top-0 z-20 backdrop-blur-md shadow-sm">
              <span className="text-[10px] font-bold text-slate-500 uppercase px-1.5 font-mono shrink-0">Portions:</span>
              <a href="#portion-logic" className="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-amber-300 hover:text-white transition flex items-center gap-1 shrink-0 font-medium">
                <Lightbulb className="w-3 h-3 text-amber-400" />
                <span>1. Logic</span>
              </a>
              {selectedConcept.core_terms && selectedConcept.core_terms.length > 0 && (
                <a href="#portion-terms" className="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-cyan-300 hover:text-white transition flex items-center gap-1 shrink-0 font-medium">
                  <Layers className="w-3 h-3 text-cyan-400" />
                  <span>2. Sub-Topics ({selectedConcept.core_terms.length})</span>
                </a>
              )}
              {selectedConcept.def && (
                <a href="#portion-definition" className="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-rose-300 hover:text-white transition flex items-center gap-1 shrink-0 font-medium">
                  <BookOpen className="w-3 h-3 text-rose-400" />
                  <span>3. Definition</span>
                </a>
              )}
              {selectedConcept.formula && (
                <a href="#portion-math" className="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-indigo-300 hover:text-white transition flex items-center gap-1 shrink-0 font-medium">
                  <Calculator className="w-3 h-3 text-indigo-400" />
                  <span>4. Math & Symbols</span>
                </a>
              )}
              <a href="#portion-arch" className="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-purple-300 hover:text-white transition flex items-center gap-1 shrink-0 font-medium">
                <Cpu className="w-3 h-3 text-purple-400" />
                <span>5. AI Architecture</span>
              </a>
              {selectedConcept.example && (
                <a href="#portion-example" className="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-emerald-300 hover:text-white transition flex items-center gap-1 shrink-0 font-medium">
                  <Sparkles className="w-3 h-3 text-emerald-400" />
                  <span>6. Real-World</span>
                </a>
              )}
              {selectedConcept.pitfalls && (
                <a href="#portion-traps" className="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-rose-400 hover:text-white transition flex items-center gap-1 shrink-0 font-medium">
                  <AlertTriangle className="w-3 h-3 text-rose-400" />
                  <span>7. Traps</span>
                </a>
              )}
              <a href="#portion-takeaways" className="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-emerald-400 hover:text-white transition flex items-center gap-1 shrink-0 font-medium">
                <CheckCircle2 className="w-3 h-3 text-emerald-400" />
                <span>8. Takeaways</span>
              </a>
            </div>

            {/* PORTION 1: Core Intuition & Underlying Logic */}
            <div id="portion-logic" className="bg-gradient-to-r from-amber-950/30 via-slate-900 to-indigo-950/30 rounded-2xl p-5 sm:p-6 border border-amber-500/30 shadow-md space-y-2.5 scroll-mt-14">
              <div className="flex items-center gap-2 text-amber-300 font-bold text-xs uppercase tracking-wider">
                <Lightbulb className="w-4 h-4 text-amber-400" />
                <span>Portion 1 &bull; Core Intuition &amp; Underlying Logic</span>
              </div>
              <p className="text-amber-100/95 text-sm sm:text-base font-medium leading-relaxed">
                {selectedConcept.core_logic || selectedConcept.logic || selectedConcept.simple_summary}
              </p>
            </div>

            {/* PORTION 2: Separate Term-by-Term Breakdown (Sub-Topics) */}
            {selectedConcept.core_terms && selectedConcept.core_terms.length > 0 && (
              <div id="portion-terms" className="space-y-3 scroll-mt-14">
                <div className="flex items-center justify-between">
                  <h3 className="text-xs font-bold text-cyan-300 uppercase tracking-wider flex items-center gap-2">
                    <Layers className="w-4 h-4 text-cyan-400" />
                    <span>Portion 2 &bull; Key Terms &amp; Sub-Topics Breakdown</span>
                  </h3>
                  <span className="text-[11px] text-slate-400 font-mono">
                    {selectedConcept.core_terms.length} separate {selectedConcept.core_terms.length === 1 ? 'term' : 'terms'}
                  </span>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5">
                  {selectedConcept.core_terms.map((termItem, idx) => (
                    <div 
                      key={idx}
                      className="bg-slate-900/90 rounded-2xl p-4 sm:p-5 border border-slate-700/80 hover:border-cyan-500/40 transition shadow-sm space-y-3 flex flex-col justify-between"
                    >
                      <div>
                        <div className="flex items-center gap-2 mb-2">
                          <span className="w-6 h-6 rounded-lg bg-cyan-500/20 text-cyan-300 text-xs font-mono font-bold flex items-center justify-center shrink-0 border border-cyan-500/30">
                            {idx + 1}
                          </span>
                          <h4 className="text-sm sm:text-base font-bold text-white tracking-tight">
                            {termItem.term}
                          </h4>
                        </div>
                        
                        <p className="text-xs sm:text-sm text-slate-200 leading-relaxed font-normal">
                          {termItem.what_is_it}
                        </p>
                      </div>

                      <div className="space-y-2 pt-2.5 border-t border-slate-800">
                        {termItem.analogy && (
                          <div className="text-[11px] sm:text-xs text-amber-200/90 bg-amber-950/40 p-2.5 rounded-xl border border-amber-500/25 flex items-start gap-2">
                            <Lightbulb className="w-3.5 h-3.5 text-amber-400 shrink-0 mt-0.5" />
                            <div>
                              <strong className="text-amber-300 font-semibold">Everyday Analogy:</strong> {termItem.analogy}
                            </div>
                          </div>
                        )}
                        {termItem.why_it_matters && (
                          <div className="text-[11px] sm:text-xs text-slate-300 flex items-start gap-1.5 pt-0.5">
                            <ArrowRight className="w-3.5 h-3.5 text-cyan-400 shrink-0 mt-0.5" />
                            <span><strong className="text-cyan-300 font-semibold">Why AI Needs It:</strong> {termItem.why_it_matters}</span>
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* PORTION 3: Formal Academic Definition & Scope */}
            {selectedConcept.def && (
              <div id="portion-definition" className="bg-slate-900/90 rounded-2xl p-5 sm:p-6 border border-slate-800 space-y-2 scroll-mt-14">
                <h3 className="text-xs font-bold text-rose-300 uppercase tracking-wider flex items-center gap-1.5">
                  <BookOpen className="w-3.5 h-3.5 text-rose-400" />
                  Portion 3 &bull; Formal Academic Definition &amp; Role
                </h3>
                <p className="text-slate-200 leading-relaxed text-sm sm:text-base">
                  <MathText text={selectedConcept.def} />
                </p>
              </div>
            )}

            {/* PORTION 4: Mathematical Formulation & Symbol Decoder */}
            {selectedConcept.formula && (
              <div id="portion-math" className="bg-slate-900/90 rounded-2xl p-5 sm:p-6 border border-indigo-500/25 space-y-4 scroll-mt-14">
                <div className="flex items-center justify-between">
                  <h3 className="text-xs font-bold text-indigo-300 uppercase tracking-wider flex items-center gap-1.5">
                    <Calculator className="w-3.5 h-3.5 text-indigo-400" />
                    Portion 4 &bull; Mathematical Formulation &amp; Symbol Decoder
                  </h3>

                  <button
                    onClick={() => {
                      navigator.clipboard.writeText(selectedConcept.formula);
                      setCopiedFormula(true);
                      setTimeout(() => setCopiedFormula(false), 2000);
                    }}
                    className="p-1 px-2.5 rounded-lg bg-slate-950 hover:bg-slate-800 border border-slate-800 text-[11px] text-slate-400 hover:text-white transition flex items-center gap-1"
                    title="Copy raw LaTeX equation"
                  >
                    {copiedFormula ? (
                      <>
                        <Check className="w-3 h-3 text-emerald-400" />
                        <span className="text-emerald-400">LaTeX Copied!</span>
                      </>
                    ) : (
                      <>
                        <Copy className="w-3 h-3" />
                        <span>Copy LaTeX</span>
                      </>
                    )}
                  </button>
                </div>

                <div className="p-4 bg-slate-950 rounded-xl border border-slate-800 overflow-x-auto text-center">
                  <KaTeXRenderer math={selectedConcept.formula} block={true} />
                </div>

                {/* Symbol-by-Symbol Decoder Table */}
                {selectedConcept.symbol_guide && selectedConcept.symbol_guide.length > 0 && (
                  <div className="space-y-2 pt-3 border-t border-slate-800/80">
                    <div className="flex items-center gap-1.5 text-xs font-bold text-indigo-300">
                      <HelpCircle className="w-3.5 h-3.5 text-indigo-400" />
                      <span>Symbol-by-Symbol Decoder:</span>
                    </div>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                      {selectedConcept.symbol_guide.map((sym, sIdx) => (
                        <div key={sIdx} className="p-2.5 rounded-xl bg-slate-950/70 border border-slate-800 text-xs flex items-start gap-2">
                          <code className="text-cyan-300 font-mono font-bold shrink-0 bg-slate-900 px-2 py-0.5 rounded border border-slate-700/80">
                            {sym.symbol}
                          </code>
                          <div className="min-w-0">
                            <div className="text-slate-200 font-semibold">{sym.meaning}</div>
                            <div className="text-[11px] text-slate-400 leading-tight mt-0.5">{sym.plain_english}</div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Step-by-Step Numerical Walkthrough */}
                {selectedConcept.numerical_example && (
                  <div className="p-4 rounded-xl bg-indigo-950/25 border border-indigo-500/20 text-xs sm:text-sm text-indigo-200/95 space-y-2">
                    <div className="font-bold text-indigo-300 flex items-center gap-1.5 text-xs uppercase tracking-wide">
                      <Calculator className="w-3.5 h-3.5 text-indigo-400" />
                      <span>Step-by-Step Numerical Calculation (Real Numbers):</span>
                    </div>
                    <p className="whitespace-pre-line font-mono text-xs sm:text-[13px] leading-relaxed text-slate-300 bg-slate-950/60 p-3 rounded-lg border border-indigo-950">
                      {selectedConcept.numerical_example}
                    </p>
                  </div>
                )}
              </div>
            )}

            {/* PORTION 5: Architectural Logic (Inside AI Networks) */}
            <div id="portion-arch" className="bg-slate-900/90 rounded-2xl p-5 sm:p-6 border border-purple-500/25 space-y-2.5 scroll-mt-14">
              <h3 className="text-xs font-bold text-purple-300 uppercase tracking-wider flex items-center gap-1.5">
                <Cpu className="w-3.5 h-3.5 text-purple-400" />
                Portion 5 &bull; Architectural Logic (How AI Models Use This Internally)
              </h3>
              <p className="text-slate-200 leading-relaxed text-sm sm:text-base">
                {selectedConcept.architectural_logic || selectedConcept.logic || "This concept is integrated into the core neural layer operations, guiding gradient descent and forward transformations."}
              </p>
            </div>

            {/* PORTION 6: Real-World Production Example */}
            {selectedConcept.example && (
              <div id="portion-example" className="bg-emerald-950/20 rounded-2xl p-5 sm:p-6 border border-emerald-500/25 space-y-2 scroll-mt-14">
                <h3 className="text-xs font-bold text-emerald-400 uppercase tracking-wider flex items-center gap-1.5">
                  <Sparkles className="w-3.5 h-3.5 text-emerald-400" />
                  Portion 6 &bull; Real-World Production Scenario
                </h3>
                <p className="text-emerald-100/90 leading-relaxed text-sm sm:text-base">
                  <MathText text={selectedConcept.example} />
                </p>
              </div>
            )}

            {/* PORTION 7: Common Novice Traps & Misconceptions */}
            {selectedConcept.pitfalls && (
              <div id="portion-traps" className="bg-rose-950/20 rounded-2xl p-4 sm:p-5 border border-rose-500/30 text-rose-200/90 space-y-1.5 scroll-mt-14">
                <div className="flex items-center gap-2 text-rose-400 font-bold text-xs uppercase tracking-wider">
                  <AlertTriangle className="w-4 h-4 text-rose-400 shrink-0" />
                  <span>Portion 7 &bull; Common Novice Traps &amp; Misconceptions</span>
                </div>
                <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
                  {selectedConcept.pitfalls}
                </p>
              </div>
            )}

            {/* PORTION 8: Key Takeaways & Revision Guide */}
            {selectedConcept.key_takeaways && selectedConcept.key_takeaways.length > 0 && (
              <div id="portion-takeaways" className="bg-slate-900/90 rounded-2xl p-4 sm:p-5 border border-emerald-500/30 space-y-2.5 scroll-mt-14">
                <div className="flex items-center gap-2 text-emerald-400 font-bold text-xs uppercase tracking-wider">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                  <span>Portion 8 &bull; Key Takeaways (Summary to Remember)</span>
                </div>
                <ul className="text-xs sm:text-sm text-slate-300 space-y-1.5 list-disc list-inside">
                  {selectedConcept.key_takeaways.map((point, kIdx) => (
                    <li key={kIdx} className="leading-relaxed">
                      {point}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Tags */}
            {selectedConcept.tags && selectedConcept.tags.length > 0 && (
              <div className="pt-2">
                <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                  <Tag className="w-3.5 h-3.5 text-slate-400" />
                  Related Keywords:
                </h4>
                <div className="flex flex-wrap gap-1.5">
                  {selectedConcept.tags.map((t, idx) => (
                    <span
                      key={idx}
                      className="px-2.5 py-1 rounded-lg text-xs bg-slate-900 text-slate-300 border border-slate-800"
                    >
                      #{t}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        ) : (
          <div className="h-full flex items-center justify-center text-slate-500 text-sm">
            Select a concept from the sidebar to inspect details.
          </div>
        )}
      </main>
    </div>
  );
}
