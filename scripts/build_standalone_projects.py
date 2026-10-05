"""
Standalone Builder for Production AI Case Studies Portal and Markdown Reference.
Generates:
  - production_ai_case_studies.html (Dedicated rich portal with copy-to-clipboard, filters, Mermaid diagrams)
  - production_ai_case_studies.md (Comprehensive markdown guide for reference)
"""

import json
import html as html_lib
from projects_data import PROJECTS

def build_standalone_projects_html():
    projects_json = json.dumps(PROJECTS, indent=2)
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Enterprise AI Case Studies & Full Implementations | Production Architectures</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
  <script>
    mermaid.initialize({{ startOnLoad: false, theme: 'dark' }});
  </script>

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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
    body {{
      font-family: 'Inter', sans-serif;
    }}
    pre, code {{
      font-family: 'JetBrains Mono', monospace;
    }}
    .katex {{
      font-size: 1.05em !important;
      color: #f1f5f9;
    }}
    ::-webkit-scrollbar {{
      width: 8px;
      height: 8px;
    }}
    ::-webkit-scrollbar-track {{
      background: #090d16;
    }}
    ::-webkit-scrollbar-thumb {{
      background: #1e293b;
      border-radius: 4px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
      background: #334155;
    }}
    .mermaid-box svg {{
      max-width: 100%;
      height: auto;
    }}
  </style>
</head>
<body class="bg-[#0b0f19] text-[#f8fafc] min-h-screen flex flex-col">

  <!-- Navbar -->
  <header class="bg-[#111827]/90 backdrop-blur-md border-b border-slate-800 sticky top-0 z-30 px-6 py-3.5 flex items-center justify-between">
    <div class="flex items-center space-x-3">
      <div class="p-2 rounded-xl bg-gradient-to-tr from-emerald-600 to-teal-500 text-white shadow-lg shadow-emerald-500/20">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/></svg>
      </div>
      <div>
        <h1 class="font-extrabold text-lg text-white tracking-tight flex items-center gap-2">
          Enterprise AI Production Systems
          <span class="px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 text-[11px] font-semibold">Zero-to-One Blueprints</span>
        </h1>
        <p class="text-xs text-slate-400">Architectures &bull; System Components &bull; Copy-Pasteable Python Code</p>
      </div>
    </div>

    <div class="flex items-center space-x-3 overflow-x-auto no-scrollbar py-1">
      <nav class="flex items-center overflow-x-auto no-scrollbar space-x-1 bg-slate-900/80 p-1 rounded-xl border border-slate-700/60 shadow-inner flex-nowrap shrink-0 text-xs">
        <a href="index.html#mindmap" class="px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-300 hover:text-white transition flex items-center gap-1.5 whitespace-nowrap">
          <svg class="w-3.5 h-3.5 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7"/></svg>
          <span>Mind Map</span>
        </a>
        <a href="index.html#syllabus" class="px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-300 hover:text-white transition flex items-center gap-1.5 whitespace-nowrap">
          <svg class="w-3.5 h-3.5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h7"/></svg>
          <span>Syllabus</span>
        </a>
        <a href="game_changing_ai_research_papers.html" class="px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-300 hover:text-white transition flex items-center gap-1.5 whitespace-nowrap">
          <svg class="w-3.5 h-3.5 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/></svg>
          <span>Landmark Papers</span>
        </a>
        <a href="production_ai_case_studies.html" class="px-3 py-1.5 rounded-lg text-xs font-semibold bg-emerald-600 text-white shadow transition flex items-center gap-1.5 whitespace-nowrap">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/></svg>
          <span>Case Studies</span>
        </a>
        <a href="interview_questions.html" class="px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-300 hover:text-white transition flex items-center gap-1.5 whitespace-nowrap">
          <svg class="w-3.5 h-3.5 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
          <span>Interview Vault</span>
        </a>
      </nav>
    </div>
  </header>

  <!-- Main Container -->
  <main class="max-w-6xl mx-auto p-6 md:p-10 flex-1 space-y-8 w-full">
    
    <!-- Hero Banner -->
    <div class="rounded-2xl p-6 md:p-8 bg-gradient-to-r from-slate-900 via-slate-900 to-indigo-950/40 border border-slate-800 shadow-2xl relative overflow-hidden">
      <div class="relative z-10 max-w-3xl space-y-3">
        <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-xs font-semibold uppercase tracking-wider">
          🛠️ Production Code & Architecture Suite
        </div>
        <h2 class="text-3xl md:text-4xl font-extrabold text-white tracking-tight leading-tight">
          Real-World AI Architectures & Implementations
        </h2>
        <p class="text-slate-300 text-sm md:text-base leading-relaxed">
          From multi-tenant hybrid ML platforms and multimodal agentic fashion studios to sub-15ms fraud streaming engines and self-healing DevOps agents. Every project includes architectural flowcharts, component breakdowns, and complete, copy-pasteable Python code.
        </p>
      </div>
    </div>

    <!-- Filters & Search -->
    <div class="flex flex-wrap items-center justify-between gap-4">
      <div class="relative flex-1 min-w-[260px] max-w-md">
        <input id="projectSearchInput" type="text" placeholder="Search projects by tech (LightGBM, Pinecone, CLIP, SDXL, Kafka)..."
               class="w-full bg-slate-900 border border-slate-700 text-xs text-white rounded-xl pl-9 pr-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-emerald-500 placeholder-slate-500">
        <svg class="w-4 h-4 absolute left-3 top-3 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
      </div>

      <div class="flex items-center flex-wrap gap-2 text-xs">
        <button onclick="filterCategory('all')" class="px-3 py-1.5 rounded-lg font-semibold bg-emerald-600 text-white proj-filter-btn active" data-cat="all">All Projects (5)</button>
        <button onclick="filterCategory('hybrid_rag_ml')" class="px-3 py-1.5 rounded-lg font-semibold bg-slate-900 text-slate-400 hover:text-white border border-slate-700 proj-filter-btn" data-cat="hybrid_rag_ml">Multi-Tenant & RAG</button>
        <button onclick="filterCategory('agentic_multimodal')" class="px-3 py-1.5 rounded-lg font-semibold bg-slate-900 text-slate-400 hover:text-white border border-slate-700 proj-filter-btn" data-cat="agentic_multimodal">Agentic & Multimodal</button>
        <button onclick="filterCategory('streaming_graph')" class="px-3 py-1.5 rounded-lg font-semibold bg-slate-900 text-slate-400 hover:text-white border border-slate-700 proj-filter-btn" data-cat="streaming_graph">Streaming & Graph ML</button>
      </div>
    </div>

    <!-- Project List -->
    <div id="projectsListContainer" class="space-y-10"></div>
  </main>

  <footer class="border-t border-slate-800 py-6 text-center text-xs text-slate-500">
    Enterprise AI Production Reference Architecture Suite &bull; Ready for deployment and production engineering.
  </footer>

  <script>
    const PROJECTS = {projects_json};
    let currentCategory = "all";
    let searchQuery = "";

    function renderProjects() {{
      const container = document.getElementById("projectsListContainer");
      if (!container) return;

      const filtered = PROJECTS.filter(p => {{
        if (currentCategory !== "all" && p.category !== currentCategory) return false;
        if (searchQuery.trim()) {{
          const q = searchQuery.toLowerCase();
          const matchTitle = p.title.toLowerCase().includes(q);
          const matchSub = p.subtitle.toLowerCase().includes(q);
          const matchTech = p.tech_stack.some(t => t.toLowerCase().includes(q));
          return matchTitle || matchSub || matchTech;
        }}
        return true;
      }});

      if (filtered.length === 0) {{
        container.innerHTML = `
          <div class="text-center py-16 bg-slate-900/50 rounded-2xl border border-slate-800 text-slate-400">
            <p class="text-base font-semibold">No matching production projects found.</p>
            <p class="text-xs mt-1 text-slate-500">Try searching for LightGBM, Pinecone, CLIP, or Kafka.</p>
          </div>
        `;
        return;
      }}

      let html = "";
      filtered.forEach((p, index) => {{
        const techChips = p.tech_stack.map(t => 
          `<span class="px-2 py-0.5 rounded-md bg-slate-800/90 text-slate-300 border border-slate-700 text-[11px] font-mono font-medium">${{t}}</span>`
        ).join("");

        const highlights = p.key_highlights.map(h => 
          `<li class="flex items-start gap-2 text-xs text-slate-300 leading-relaxed">
            <span class="text-emerald-400 mt-0.5 font-bold">✔</span>
            <span>${{h}}</span>
          </li>`
        ).join("");

        const components = p.system_components.map(c => 
          `<div class="bg-slate-950/60 p-3 rounded-xl border border-slate-800/80">
            <h5 class="text-xs font-bold text-indigo-300">${{c.name}}</h5>
            <p class="text-[11px] text-slate-400 mt-1 leading-relaxed">${{c.desc}}</p>
          </div>`
        ).join("");

        html += `
          <article id="project-${{p.id}}" class="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 md:p-8 space-y-6 shadow-xl transition hover:border-slate-700 scroll-mt-20">
            
            <!-- Header Section -->
            <div class="space-y-3">
              <div class="flex flex-wrap items-center justify-between gap-3">
                <span class="px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-xs font-bold uppercase tracking-wider">
                  ${{p.badge}}
                </span>
                <div class="flex flex-wrap gap-1.5">
                  ${{techChips}}
                </div>
              </div>

              <div>
                <h3 class="text-xl md:text-2xl font-extrabold text-white tracking-tight">${{p.title}}</h3>
                <p class="text-xs md:text-sm text-slate-300 mt-1.5 leading-relaxed">${{p.subtitle}}</p>
              </div>
            </div>

            <!-- Highlights & Components Grid -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-5">
              <div class="bg-slate-950/40 p-4 rounded-xl border border-slate-800/60 space-y-3">
                <h4 class="text-xs uppercase tracking-wider font-bold text-emerald-400 flex items-center gap-1.5">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                  Architectural Pillars & Capabilities
                </h4>
                <ul class="space-y-2">
                  ${{highlights}}
                </ul>
              </div>

              <div class="bg-slate-950/40 p-4 rounded-xl border border-slate-800/60 space-y-3">
                <h4 class="text-xs uppercase tracking-wider font-bold text-indigo-400 flex items-center gap-1.5">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/></svg>
                  Core System Components
                </h4>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                  ${{components}}
                </div>
              </div>
            </div>

            <!-- Architecture Flowchart -->
            <div class="bg-slate-950/70 p-5 rounded-xl border border-slate-800/80 space-y-3">
              <div class="flex items-center justify-between">
                <h4 class="text-xs uppercase tracking-wider font-bold text-amber-400 flex items-center gap-1.5">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4"/></svg>
                  End-to-End System Architecture Flow
                </h4>
                <span class="text-[11px] text-slate-500 font-mono">Mermaid Flowchart</span>
              </div>
              <div class="mermaid mermaid-box bg-[#090d16] p-4 rounded-lg border border-slate-800 overflow-x-auto text-center">
${{p.mermaid_diagram}}
              </div>
            </div>

            <!-- Copy-Pasteable Code Implementation -->
            <div class="space-y-2">
              <div class="flex flex-wrap items-center justify-between gap-3 bg-slate-950 px-4 py-2.5 rounded-t-xl border-t border-x border-slate-800">
                <div class="flex items-center space-x-2">
                  <span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span>
                  <span class="text-xs font-mono font-bold text-emerald-400">${{p.id}}.py</span>
                  <span class="text-[11px] text-slate-400 hidden sm:inline">&bull; Complete & Copy-Pasteable Implementation</span>
                </div>
                <div class="flex items-center space-x-2">
                  <button onclick="toggleCode('${{p.id}}')" id="toggleBtn-${{p.id}}" class="px-2.5 py-1 text-slate-400 hover:text-white text-xs font-semibold rounded bg-slate-800/60 hover:bg-slate-800 transition">
                    Collapse Code
                  </button>
                  <button onclick="copyCode('${{p.id}}')" id="copyBtn-${{p.id}}" class="px-3.5 py-1 text-xs font-semibold rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white flex items-center gap-1.5 shadow transition">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"/></svg>
                    <span>Copy Full Code</span>
                  </button>
                </div>
              </div>

              <div id="codeBlockWrapper-${{p.id}}" class="relative">
                <pre class="bg-[#050811] p-4 rounded-b-xl border border-slate-800 text-[11px] font-mono text-emerald-300/90 overflow-x-auto max-h-[500px] leading-relaxed"><code id="codeText-${{p.id}}">${{html_lib.escape(p.code_snippet)}}</code></pre>
              </div>
            </div>

          </article>
        `;
      }});

      container.innerHTML = html;

      // Render math equations
      if (typeof renderMathInElement === 'function') {{
        try {{
          renderMathInElement(container, {{
            delimiters: [
              {{ left: '$$', right: '$$', display: true }},
              {{ left: '$', right: '$', display: false }}
            ],
            throwOnError: false
          }});
        }} catch(e) {{}}
      }}

      // Re-render mermaid diagrams
      setTimeout(() => {{
        try {{
          mermaid.run();
        }} catch (err) {{
          console.warn("Mermaid render error:", err);
        }}
      }}, 50);
    }}

    function filterCategory(cat) {{
      currentCategory = cat;
      document.querySelectorAll(".proj-filter-btn").forEach(btn => {{
        if (btn.dataset.cat === cat) {{
          btn.className = "px-3 py-1.5 rounded-lg font-semibold bg-emerald-600 text-white proj-filter-btn active";
        }} else {{
          btn.className = "px-3 py-1.5 rounded-lg font-semibold bg-slate-900 text-slate-400 hover:text-white border border-slate-700 proj-filter-btn";
        }}
      }});
      renderProjects();
    }}

    function copyCode(projId) {{
      const codeElem = document.getElementById(`codeText-${{projId}}`);
      const copyBtn = document.getElementById(`copyBtn-${{projId}}`);
      if (!codeElem || !copyBtn) return;

      navigator.clipboard.writeText(codeElem.innerText).then(() => {{
        const origHTML = copyBtn.innerHTML;
        copyBtn.innerHTML = `
          <svg class="w-3.5 h-3.5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
          <span>Copied to Clipboard!</span>
        `;
        copyBtn.classList.remove("bg-emerald-600", "hover:bg-emerald-500");
        copyBtn.classList.add("bg-teal-500");

        setTimeout(() => {{
          copyBtn.innerHTML = origHTML;
          copyBtn.classList.remove("bg-teal-500");
          copyBtn.classList.add("bg-emerald-600", "hover:bg-emerald-500");
        }}, 2200);
      }}).catch(err => {{
        console.error("Clipboard copy failed:", err);
      }});
    }}

    function toggleCode(projId) {{
      const wrapper = document.getElementById(`codeBlockWrapper-${{projId}}`);
      const btn = document.getElementById(`toggleBtn-${{projId}}`);
      if (!wrapper || !btn) return;

      if (wrapper.classList.contains("hidden")) {{
        wrapper.classList.remove("hidden");
        btn.innerText = "Collapse Code";
      }} else {{
        wrapper.classList.add("hidden");
        btn.innerText = "Expand Code";
      }}
    }}

    document.getElementById("projectSearchInput").addEventListener("input", (e) => {{
      searchQuery = e.target.value;
      renderProjects();
    }});

    function handleInitialRoute() {{
      const hash = window.location.hash.replace(/^#[/]?/, '');
      if (hash) {{
        const found = PROJECTS.find((p, idx) => p.id === hash || ('proj-' + (idx + 1)) === hash || p.title.toLowerCase().includes(hash.toLowerCase()));
        if (found) {{
          setTimeout(() => {{
            const el = document.getElementById(`project-${{found.id}}`);
            if (el) {{
              el.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
              el.classList.add('ring-2', 'ring-emerald-500');
              setTimeout(() => el.classList.remove('ring-2', 'ring-emerald-500'), 3000);
            }}
          }}, 200);
        }}
      }}
    }}

    window.addEventListener("DOMContentLoaded", () => {{
      renderProjects();
      handleInitialRoute();
    }});
    window.addEventListener("hashchange", () => {{
      handleInitialRoute();
    }});
    renderProjects();
    handleInitialRoute();
  </script>
</body>
</html>
"""
    with open("production_ai_case_studies.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated production_ai_case_studies.html successfully!")


def build_standalone_projects_markdown():
    md = "# Enterprise AI Production Systems & Zero-to-One Case Studies\n\n"
    md += "A comprehensive engineering guide containing end-to-end production architectures, component breakdowns, operational failure modes & mitigations, and complete, runnable Python implementations for real-world enterprise AI systems.\n\n"
    md += "---\n\n"

    for p in PROJECTS:
        md += f"## {p['title']}\n\n"
        md += f"> **{p['subtitle']}**\n\n"
        md += f"- **🏷️ Category**: `{p['category']}` | **🛡️ Platform Badge**: `{p['badge']}`\n"
        md += f"- **💻 Tech Stack**: {', '.join([f'`{t}`' for t in p['tech_stack']])}\n\n"
        
        md += "### 🚀 Architectural Highlights & Core Capabilities\n\n"
        for h in p["key_highlights"]:
            md += f"- {h}\n"
        md += "\n"

        md += "### 🧩 Core System Components\n\n"
        for c in p["system_components"]:
            md += f"#### {c['name']}\n{c['desc']}\n\n"

        md += "### 📐 System Architecture Flow\n\n"
        md += "```mermaid\n"
        md += p["mermaid_diagram"] + "\n"
        md += "```\n\n"

        md += f"### 💻 Complete Copy-Pasteable Implementation (`{p['id']}.py`)\n\n"
        md += f"{p['code_description']}\n\n"
        md += f"```python\n{p['code_snippet'].strip()}\n```\n\n"
        md += "---\n\n"

    with open("production_ai_case_studies.md", "w", encoding="utf-8") as f:
        f.write(md)
    print("Generated production_ai_case_studies.md successfully!")


if __name__ == "__main__":
    build_standalone_projects_html()
    build_standalone_projects_markdown()
