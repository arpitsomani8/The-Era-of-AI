import json
from papers_data import PAPERS

papers_json = json.dumps(PAPERS, indent=2)

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Landmark & Game-Changing AI Research Papers Compendium</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>

  <!-- KaTeX for Mathematical Typesetting (Local + CDN Fallback) -->
  <link rel="stylesheet" href="katex/katex.min.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
  <script src="katex/katex.min.js"></script>
  <script src="katex/auto-render.min.js"></script>
  <script>
    if (typeof katex === 'undefined') {{
      document.write('<script src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"><\\/script>');
      document.write('<script src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"><\\/script>');
    }}
  </script>

  <style>
    ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
    ::-webkit-scrollbar-track {{ background: #1e293b; }}
    ::-webkit-scrollbar-thumb {{ background: #475569; border-radius: 3px; }}
    
    /* KaTeX mathematical styling */
    .katex {{
      font-size: 1.05em !important;
      text-rendering: geometricPrecision;
      color: #f1f5f9;
    }}
    .katex-display {{
      margin: 0.6em 0 !important;
      overflow-x: auto !important;
      overflow-y: hidden !important;
      padding: 0.4rem 0.25rem;
      scrollbar-width: thin;
      text-align: center;
    }}
    .katex-display::-webkit-scrollbar {{
      height: 4px;
    }}
    .katex-display::-webkit-scrollbar-thumb {{
      background: #6366f1;
      border-radius: 2px;
    }}
    .katex .mord, .katex .mbin, .katex .mrel, .katex .mopen, .katex .mclose, .katex .mpunct {{
      color: #f8fafc;
    }}
    .katex .frac-line {{
      border-bottom-width: 1.5px !important;
      border-color: #a5b4fc !important;
    }}

    @media print {{
      @page {{ margin: 1.2cm; size: A4 portrait; }}
      body {{ background: white !important; color: #0f172a !important; }}
      .no-print {{ display: none !important; }}
      .print-card {{
        page-break-inside: avoid !important;
        break-inside: avoid !important;
        border: 1px solid #cbd5e1 !important;
        background: white !important;
        color: #0f172a !important;
        margin-bottom: 1.25rem !important;
        box-shadow: none !important;
      }}
    }}
  </style>
</head>
<body class="bg-[#0b0f19] text-[#f8fafc] font-sans antialiased min-h-screen p-4 md:p-10 select-none">
  <div class="max-w-5xl mx-auto space-y-6 pb-20">
    <div class="border-b border-slate-700 pb-5 flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-500/20 text-amber-300 border border-amber-500/30 text-xs font-semibold uppercase tracking-wider mb-2">
          Landmark Research Compendium
        </div>
        <h1 class="text-2xl md:text-3xl font-extrabold tracking-tight text-white">
          Game-Changing AI & Machine Learning Research Papers
        </h1>
        <p class="text-xs md:text-sm text-slate-400 mt-1">
          From "Attention Is All You Need" to ResNet, LoRA, DPO, and Diffusion — with Direct arXiv Links, Problems Solved, and Historical Legacy.
        </p>
      </div>
      <div class="no-print flex items-center gap-3 overflow-x-auto no-scrollbar py-1">
        <nav class="flex items-center overflow-x-auto no-scrollbar space-x-1 bg-slate-900/80 p-1 rounded-xl border border-slate-700/60 shadow-inner flex-nowrap shrink-0 text-xs">
          <a href="index.html#mindmap" class="px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-300 hover:text-white transition flex items-center gap-1.5 whitespace-nowrap">
            <svg class="w-3.5 h-3.5 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7"/></svg>
            <span>Mind Map</span>
          </a>
          <a href="index.html#syllabus" class="px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-300 hover:text-white transition flex items-center gap-1.5 whitespace-nowrap">
            <svg class="w-3.5 h-3.5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h7"/></svg>
            <span>Syllabus</span>
          </a>
          <a href="game_changing_ai_research_papers.html" class="px-3 py-1.5 rounded-lg text-xs font-semibold bg-amber-600 text-white shadow transition flex items-center gap-1.5 whitespace-nowrap">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/></svg>
            <span>Landmark Papers</span>
          </a>
          <a href="production_ai_case_studies.html" class="px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-300 hover:text-white transition flex items-center gap-1.5 whitespace-nowrap">
            <svg class="w-3.5 h-3.5 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/></svg>
            <span>Case Studies</span>
          </a>
          <a href="interview_questions.html" class="px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-300 hover:text-white transition flex items-center gap-1.5 whitespace-nowrap">
            <svg class="w-3.5 h-3.5 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            <span>Interview Vault</span>
          </a>
        </nav>
      </div>
    </div>

    <!-- Search & Filter Controls -->
    <div class="flex flex-wrap items-center justify-between gap-3 no-print">
      <div class="relative flex-1 min-w-[240px] max-w-md">
        <input id="paperSearchInput" type="text" placeholder="Search papers (e.g. Vaswani, Attention, LoRA, ResNet)..."
               class="w-full bg-slate-900 border border-slate-700 text-xs text-white rounded-lg pl-8 pr-4 py-2 focus:outline-none focus:ring-2 focus:ring-amber-500 placeholder-slate-500">
        <svg class="w-4 h-4 absolute left-2.5 top-2.5 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
      </div>

      <div class="flex items-center flex-wrap gap-1.5 text-xs">
        <button onclick="filterPapers('all')" class="px-2.5 py-1 rounded-md font-medium bg-amber-600 text-white paper-btn active" data-cat="all">All (22)</button>
        <button onclick="filterPapers('transformer')" class="px-2.5 py-1 rounded-md font-medium bg-slate-900 text-slate-400 hover:text-white border border-slate-700 paper-btn" data-cat="transformer">Transformers & Attention</button>
        <button onclick="filterPapers('llm')" class="px-2.5 py-1 rounded-md font-medium bg-slate-900 text-slate-400 hover:text-white border border-slate-700 paper-btn" data-cat="llm">LLMs & Scaling</button>
        <button onclick="filterPapers('vision_dl')" class="px-2.5 py-1 rounded-md font-medium bg-slate-900 text-slate-400 hover:text-white border border-slate-700 paper-btn" data-cat="vision_dl">Vision & Foundations</button>
        <button onclick="filterPapers('generative')" class="px-2.5 py-1 rounded-md font-medium bg-slate-900 text-slate-400 hover:text-white border border-slate-700 paper-btn" data-cat="generative">Diffusion & GANs</button>
        <button onclick="filterPapers('alignment')" class="px-2.5 py-1 rounded-md font-medium bg-slate-900 text-slate-400 hover:text-white border border-slate-700 paper-btn" data-cat="alignment">Alignment & RLHF</button>
      </div>
    </div>

    <!-- Paper Cards -->
    <div id="papersList" class="space-y-4"></div>
  </div>

  <script>
    const PAPERS_DATA = {papers_json};
    let currentFilter = 'all';
    let searchQuery = '';

    function triggerMathRender(rootElement) {{
      const target = rootElement || document.body;
      if (typeof renderMathInElement === 'function') {{
        try {{
          renderMathInElement(target, {{
            delimiters: [
              {{ left: '$$', right: '$$', display: true }},
              {{ left: '$', right: '$', display: false }},
              {{ left: '\\(', right: '\\)', display: false }},
              {{ left: '\\[', right: '\\]', display: true }}
            ],
            throwOnError: false,
            errorColor: '#f43f5e'
          }});
        }} catch (e) {{
          console.warn('KaTeX rendering error:', e);
        }}
      }}
    }}

    function render() {{
      const container = document.getElementById("papersList");
      const filtered = PAPERS_DATA.filter(p => {{
        if (currentFilter !== 'all' && p.category !== currentFilter) return false;
        if (searchQuery.trim()) {{
          const q = searchQuery.toLowerCase();
          return p.title.toLowerCase().includes(q) || p.authors.toLowerCase().includes(q) || p.one_liner.toLowerCase().includes(q) || p.breakthrough.toLowerCase().includes(q);
        }}
        return true;
      }});

      if (filtered.length === 0) {{
        container.innerHTML = `<div class="p-8 text-center text-slate-500 bg-slate-900/50 rounded-xl border border-slate-800">No matching research papers found.</div>`;
        return;
      }}

      let html = "";
      filtered.forEach((p, idx) => {{
        const pId = p.id || ('paper-' + (idx + 1));
        html += `
          <div id="paper-${{pId}}" class="print-card bg-slate-900/80 border border-slate-800 rounded-2xl p-5 shadow-lg space-y-3 transition hover:border-slate-700 scroll-mt-20">
            <div class="flex items-start justify-between flex-wrap gap-2">
              <div class="space-y-1">
                <div class="flex items-center flex-wrap gap-2">
                  <span class="px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 border border-amber-500/30 text-[11px] font-bold">
                    ${{p.year}}
                  </span>
                  <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700 text-[11px] font-medium">
                    ${{p.institution}}
                  </span>
                  <span class="text-xs text-slate-400 italic">
                    ${{p.authors}}
                  </span>
                </div>
                <h3 class="text-base md:text-lg font-bold text-white hover:text-indigo-300 transition flex items-center gap-2">
                  <a href="${{p.url}}" target="_blank" rel="noopener noreferrer" class="hover:underline flex items-center gap-1.5">
                    <span>${{p.title}}</span>
                    <svg class="w-4 h-4 text-slate-400 hover:text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg>
                  </a>
                </h3>
              </div>
              <a href="${{p.url}}" target="_blank" rel="noopener noreferrer" class="no-print px-3 py-1.5 rounded-lg bg-indigo-600/30 hover:bg-indigo-600 text-indigo-300 hover:text-white border border-indigo-500/40 text-xs font-semibold flex items-center gap-1 transition">
                <span>Read on arXiv</span>
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
              </a>
            </div>

            <div class="p-2.5 rounded-lg bg-amber-950/30 border border-amber-800/40 text-amber-200 text-xs font-medium">
              💡 <span class="font-semibold text-amber-100">Key Takeaway:</span> ${{p.one_liner}}
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
              <div class="bg-slate-950/40 p-3 rounded-lg border border-slate-800/80">
                <span class="font-semibold text-rose-400 uppercase text-[10px] tracking-wider block mb-1">The Problem It Solved</span>
                <p class="text-slate-300 leading-relaxed">${{p.problem}}</p>
              </div>

              <div class="bg-slate-950/40 p-3 rounded-lg border border-slate-800/80">
                <span class="font-semibold text-emerald-400 uppercase text-[10px] tracking-wider block mb-1">The Game-Changing Breakthrough</span>
                <p class="text-slate-300 leading-relaxed">${{p.breakthrough}}</p>
              </div>
            </div>

            <div class="bg-slate-950/60 p-3 rounded-lg border border-slate-800 text-xs text-indigo-200 overflow-x-auto">
              <span class="text-indigo-400 font-sans font-semibold text-[10px] uppercase tracking-wider block mb-0.5">Core Mathematical Formulation / Mechanism:</span>
              <div class="my-1">${{p.formula}}</div>
            </div>

            <div class="text-xs text-slate-300 pt-1 border-t border-slate-800/80 flex items-start gap-2">
              <span class="text-purple-400 font-semibold flex-shrink-0">🚀 Modern Legacy:</span>
              <span class="text-slate-300">${{p.impact}}</span>
            </div>
          </div>
        `;
      }});

      container.innerHTML = html;
      triggerMathRender(container);
    }}

    function filterPapers(cat) {{
      currentFilter = cat;
      document.querySelectorAll(".paper-btn").forEach(btn => {{
        btn.className = btn.dataset.cat === cat
          ? "px-2.5 py-1 rounded-md font-medium bg-amber-600 text-white paper-btn active"
          : "px-2.5 py-1 rounded-md font-medium bg-slate-900 text-slate-400 hover:text-white border border-slate-700 paper-btn";
      }});
      render();
    }}

    document.getElementById("paperSearchInput").addEventListener("input", (e) => {{
      searchQuery = e.target.value;
      render();
    }});

    function handleInitialRoute() {{
      const hash = window.location.hash.replace(/^#[/]?/, '');
      if (hash) {{
        const found = PAPERS_DATA.find((p, idx) => p.id === hash || ('paper-' + (idx + 1)) === hash || p.title.toLowerCase().includes(hash.toLowerCase()));
        if (found) {{
          setTimeout(() => {{
            const pId = found.id || ('paper-' + (PAPERS_DATA.indexOf(found) + 1));
            const el = document.getElementById(`paper-${{pId}}`);
            if (el) {{
              el.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
              el.classList.add('ring-2', 'ring-amber-500');
              setTimeout(() => el.classList.remove('ring-2', 'ring-amber-500'), 3000);
            }}
          }}, 200);
        }}
      }}
    }}

    window.addEventListener("DOMContentLoaded", () => {{
      render();
      handleInitialRoute();
    }});
    window.addEventListener("hashchange", () => {{
      handleInitialRoute();
    }});
    render();
    handleInitialRoute();
  </script>
</body>
</html>
"""

with open("game_changing_ai_research_papers.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Generated game_changing_ai_research_papers.html successfully!")
