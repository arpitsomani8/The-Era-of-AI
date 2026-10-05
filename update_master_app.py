"""
Script to inject the Production Case Studies tab and full implementations into generate_all.py
and regenerate ai_ml_dl_master_mindmap.html.
"""

import io

with io.open("generate_all.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Import PROJECTS
if "from projects_data import PROJECTS" not in content:
    content = content.replace(
        "from papers_data import PAPERS",
        "from papers_data import PAPERS\nfrom projects_data import PROJECTS"
    )

# 2. Add Mermaid.js to <head>
if "mermaid.min.js" not in content:
    mermaid_tag = """  <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
  <script>mermaid.initialize({ startOnLoad: false, theme: 'dark' });</script>
"""
    content = content.replace("</head>", f"{mermaid_tag}</head>")

# 3. Add Tab 4 Button to Header
old_tab_papers = """      <button onclick="switchMainTab('papers')" id="tabBtn-papers" class="px-3.5 py-1.5 rounded-lg text-xs font-semibold text-slate-300 hover:text-white transition flex items-center gap-1.5 relative">
        <svg class="w-3.5 h-3.5 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/></svg>
        <span>Landmark Papers</span>
        <span class="w-2 h-2 rounded-full bg-amber-400 animate-pulse"></span>
      </button>"""

new_tabs = """      <button onclick="switchMainTab('papers')" id="tabBtn-papers" class="px-3.5 py-1.5 rounded-lg text-xs font-semibold text-slate-300 hover:text-white transition flex items-center gap-1.5 relative">
        <svg class="w-3.5 h-3.5 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/></svg>
        <span>Landmark Papers</span>
        <span class="w-2 h-2 rounded-full bg-amber-400 animate-pulse"></span>
      </button>

      <button onclick="switchMainTab('projects')" id="tabBtn-projects" class="px-3.5 py-1.5 rounded-lg text-xs font-semibold text-slate-300 hover:text-white transition flex items-center gap-1.5 relative">
        <svg class="w-3.5 h-3.5 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/></svg>
        <span>Production Case Studies</span>
        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
      </button>"""

if old_tab_papers in content:
    content = content.replace(old_tab_papers, new_tabs)
else:
    print("WARNING: Could not find old_tab_papers exactly, checking tabBtn-papers...")

# 4. Add Tab 4 Container (projectsTabContainer) right after papersTabContainer
papers_container_end = """        <!-- Papers List Container -->
        <div id="papersList" class="space-y-4"></div>
      </div>
    </div>"""

projects_container = """        <!-- Papers List Container -->
        <div id="papersList" class="space-y-4"></div>
      </div>
    </div>

    <!-- TAB 4: Production AI Case Studies & Real-World Projects Hub -->
    <div id="projectsTabContainer" class="hidden absolute inset-0 overflow-y-auto p-6 md:p-12 z-10 bg-[var(--background,#0b0f19)] text-[var(--foreground,#f8fafc)]">
      <div class="max-w-6xl mx-auto space-y-6 pb-20">
        <!-- Projects Header -->
        <div class="border-b border-slate-700 pb-5 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-xs font-semibold uppercase tracking-wider mb-2">
              Enterprise Case Studies
            </div>
            <h2 class="text-2xl md:text-3xl font-extrabold tracking-tight text-white">
              Full-Scale Production Implementations & Zero-to-One Architectures
            </h2>
            <p class="text-xs md:text-sm text-slate-400 mt-1">
              End-to-End System Designs, Interactive Flowcharts, Dynamic Schema Engines, Hybrid ML/RAG, Agentic Multimodal Studios & Copy-Pasteable Code.
            </p>
          </div>
        </div>

        <!-- Projects Search & Filter -->
        <div class="flex flex-wrap items-center justify-between gap-3 no-print">
          <div class="relative flex-1 min-w-[240px] max-w-md">
            <input id="projectSearchInput" type="text" placeholder="Search projects by title, tech stack (LightGBM, Pinecone, CLIP, SDXL, Kafka)..."
                   class="w-full bg-slate-900 border border-slate-700 text-xs text-white rounded-lg pl-8 pr-4 py-2 focus:outline-none focus:ring-2 focus:ring-emerald-500 placeholder-slate-500">
            <svg class="w-4 h-4 absolute left-2.5 top-2.5 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
          </div>

          <div class="flex items-center flex-wrap gap-1.5 text-xs">
            <button onclick="filterProjects('all')" class="px-2.5 py-1 rounded-md font-medium bg-emerald-600 text-white proj-btn active" data-cat="all">All (5)</button>
            <button onclick="filterProjects('hybrid_rag_ml')" class="px-2.5 py-1 rounded-md font-medium bg-slate-900 text-slate-400 hover:text-white border border-slate-700 proj-btn" data-cat="hybrid_rag_ml">Multi-Tenant & RAG</button>
            <button onclick="filterProjects('agentic_multimodal')" class="px-2.5 py-1 rounded-md font-medium bg-slate-900 text-slate-400 hover:text-white border border-slate-700 proj-btn" data-cat="agentic_multimodal">Agentic & Multimodal</button>
            <button onclick="filterProjects('streaming_graph')" class="px-2.5 py-1 rounded-md font-medium bg-slate-900 text-slate-400 hover:text-white border border-slate-700 proj-btn" data-cat="streaming_graph">Streaming & Graph ML</button>
          </div>
        </div>

        <!-- Projects List Container -->
        <div id="projectsList" class="space-y-8"></div>
      </div>
    </div>"""

if papers_container_end in content:
    content = content.replace(papers_container_end, projects_container)
else:
    print("WARNING: Could not find papers_container_end")

# 5. Add PROJECTS_DATA in JavaScript
old_js_consts = """    const PAPERS_DATA = __PAPERS_JSON__;"""
new_js_consts = """    const PAPERS_DATA = __PAPERS_JSON__;
    const PROJECTS_DATA = __PROJECTS_JSON__;

    let projectFilterCategory = "all";
    let projectSearchQuery = "";"""

if old_js_consts in content:
    content = content.replace(old_js_consts, new_js_consts)

# 6. Update switchMainTab in JavaScript
old_switch_tab = """    function switchMainTab(tab) {
      currentMainTab = tab;
      const mindmapTab = document.getElementById("mindmapTabContainer");
      const syllabusTab = document.getElementById("printableDocContainer");
      const papersTab = document.getElementById("papersTabContainer");
      const mindmapToolbar = document.getElementById("mindmapToolbar");

      // Reset tab button states
      document.querySelectorAll("#navTabs button").forEach(btn => {
        btn.className = "px-3.5 py-1.5 rounded-lg text-xs font-semibold text-slate-300 hover:text-white transition flex items-center gap-1.5";
      });

      const activeBtn = document.getElementById(`tabBtn-${tab}`);
      if (activeBtn) {
        activeBtn.className = "px-3.5 py-1.5 rounded-lg text-xs font-semibold transition flex items-center gap-1.5 bg-indigo-600 text-white shadow";
      }

      if (tab === "mindmap") {
        mindmapTab.classList.remove("hidden");
        syllabusTab.classList.add("hidden");
        papersTab.classList.add("hidden");
        mindmapToolbar.classList.remove("hidden");
      } else if (tab === "syllabus") {
        mindmapTab.classList.add("hidden");
        syllabusTab.classList.remove("hidden");
        papersTab.classList.add("hidden");
        mindmapToolbar.classList.add("hidden");
        buildLineWiseDocument();
      } else if (tab === "papers") {
        mindmapTab.classList.add("hidden");
        syllabusTab.classList.add("hidden");
        papersTab.classList.remove("hidden");
        mindmapToolbar.classList.add("hidden");
        renderPapersList();
      }
    }"""

new_switch_tab = """    function switchMainTab(tab) {
      currentMainTab = tab;
      const mindmapTab = document.getElementById("mindmapTabContainer");
      const syllabusTab = document.getElementById("printableDocContainer");
      const papersTab = document.getElementById("papersTabContainer");
      const projectsTab = document.getElementById("projectsTabContainer");
      const mindmapToolbar = document.getElementById("mindmapToolbar");

      // Reset tab button states
      document.querySelectorAll("#navTabs button").forEach(btn => {
        btn.className = "px-3.5 py-1.5 rounded-lg text-xs font-semibold text-slate-300 hover:text-white transition flex items-center gap-1.5";
      });

      const activeBtn = document.getElementById(`tabBtn-${tab}`);
      if (activeBtn) {
        const bgClass = tab === "projects" ? "bg-emerald-600" : (tab === "papers" ? "bg-amber-600" : "bg-indigo-600");
        activeBtn.className = `px-3.5 py-1.5 rounded-lg text-xs font-semibold transition flex items-center gap-1.5 ${bgClass} text-white shadow`;
      }

      if (tab === "mindmap") {
        mindmapTab.classList.remove("hidden");
        syllabusTab.classList.add("hidden");
        papersTab.classList.add("hidden");
        projectsTab.classList.add("hidden");
        mindmapToolbar.classList.remove("hidden");
      } else if (tab === "syllabus") {
        mindmapTab.classList.add("hidden");
        syllabusTab.classList.remove("hidden");
        papersTab.classList.add("hidden");
        projectsTab.classList.add("hidden");
        mindmapToolbar.classList.add("hidden");
        buildLineWiseDocument();
      } else if (tab === "papers") {
        mindmapTab.classList.add("hidden");
        syllabusTab.classList.add("hidden");
        papersTab.classList.remove("hidden");
        projectsTab.classList.add("hidden");
        mindmapToolbar.classList.add("hidden");
        renderPapersList();
      } else if (tab === "projects") {
        mindmapTab.classList.add("hidden");
        syllabusTab.classList.add("hidden");
        papersTab.classList.add("hidden");
        projectsTab.classList.remove("hidden");
        mindmapToolbar.classList.add("hidden");
        renderProjectsList();
      }
    }"""

if old_switch_tab in content:
    content = content.replace(old_switch_tab, new_switch_tab)

# 7. Add renderProjectsList and helpers before Mind Map Canvas Engine
render_projects_js = """
    // ----------------------------------------------------
    // ENTERPRISE PRODUCTION PROJECTS RENDERER
    // ----------------------------------------------------
    function escapeHtml(str) {
      if (!str) return "";
      return str
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
    }

    function renderProjectsList() {
      const container = document.getElementById("projectsList");
      if (!container) return;

      const filtered = PROJECTS_DATA.filter(p => {
        if (projectFilterCategory !== "all" && p.category !== projectFilterCategory) {
          return false;
        }
        if (projectSearchQuery.trim()) {
          const q = projectSearchQuery.toLowerCase();
          const matchTitle = p.title.toLowerCase().includes(q);
          const matchSub = p.subtitle.toLowerCase().includes(q);
          const matchTech = p.tech_stack.some(t => t.toLowerCase().includes(q));
          return matchTitle || matchSub || matchTech;
        }
        return true;
      });

      if (filtered.length === 0) {
        container.innerHTML = `<div class="p-8 text-center text-slate-500 bg-slate-900/50 rounded-xl border border-slate-800">No matching projects found. Try searching for LightGBM, Pinecone, or CLIP.</div>`;
        return;
      }

      let html = "";
      filtered.forEach((p, idx) => {
        const techChips = p.tech_stack.map(t => 
          `<span class="px-2 py-0.5 rounded-md bg-slate-800/90 text-slate-300 border border-slate-700 text-[11px] font-mono font-medium">${t}</span>`
        ).join("");

        const highlights = p.key_highlights.map(h => 
          `<li class="flex items-start gap-2 text-xs text-slate-300 leading-relaxed">
            <span class="text-emerald-400 mt-0.5 font-bold">✔</span>
            <span>${h}</span>
          </li>`
        ).join("");

        const components = p.system_components.map(c => 
          `<div class="bg-slate-950/60 p-3 rounded-xl border border-slate-800/80">
            <h5 class="text-xs font-bold text-indigo-300">${c.name}</h5>
            <p class="text-[11px] text-slate-400 mt-1 leading-relaxed">${c.desc}</p>
          </div>`
        ).join("");

        html += `
          <div class="print-card bg-slate-900/90 border border-slate-800 rounded-2xl p-6 md:p-8 space-y-6 shadow-xl transition hover:border-slate-700">
            <!-- Header -->
            <div class="space-y-3">
              <div class="flex flex-wrap items-center justify-between gap-3">
                <span class="px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-xs font-bold uppercase tracking-wider">
                  ${p.badge}
                </span>
                <div class="flex flex-wrap gap-1.5">
                  ${techChips}
                </div>
              </div>

              <div>
                <h3 class="text-xl md:text-2xl font-extrabold text-white tracking-tight">${p.title}</h3>
                <p class="text-xs md:text-sm text-slate-300 mt-1.5 leading-relaxed">${p.subtitle}</p>
              </div>
            </div>

            <!-- Highlights & Components -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-5">
              <div class="bg-slate-950/40 p-4 rounded-xl border border-slate-800/60 space-y-3">
                <h4 class="text-xs uppercase tracking-wider font-bold text-emerald-400 flex items-center gap-1.5">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                  Architectural Highlights & Capabilities
                </h4>
                <ul class="space-y-2">
                  ${highlights}
                </ul>
              </div>

              <div class="bg-slate-950/40 p-4 rounded-xl border border-slate-800/60 space-y-3">
                <h4 class="text-xs uppercase tracking-wider font-bold text-indigo-400 flex items-center gap-1.5">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/></svg>
                  Core System Components
                </h4>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                  ${components}
                </div>
              </div>
            </div>

            <!-- Architecture Diagram -->
            <div class="bg-slate-950/70 p-5 rounded-xl border border-slate-800/80 space-y-3">
              <div class="flex items-center justify-between">
                <h4 class="text-xs uppercase tracking-wider font-bold text-amber-400 flex items-center gap-1.5">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4"/></svg>
                  End-to-End System Architecture Flow
                </h4>
                <span class="text-[11px] text-slate-500 font-mono">Mermaid Flowchart</span>
              </div>
              <div class="mermaid bg-[#090d16] p-4 rounded-lg border border-slate-800 overflow-x-auto text-center text-xs">
${p.mermaid_diagram}
              </div>
            </div>

            <!-- Code Section -->
            <div class="space-y-2">
              <div class="flex flex-wrap items-center justify-between gap-3 bg-slate-950 px-4 py-2.5 rounded-t-xl border-t border-x border-slate-800">
                <div class="flex items-center space-x-2">
                  <span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span>
                  <span class="text-xs font-mono font-bold text-emerald-400">${p.id}.py</span>
                  <span class="text-[11px] text-slate-400 hidden sm:inline">&bull; Complete & Copy-Pasteable Implementation</span>
                </div>
                <div class="flex items-center space-x-2">
                  <button onclick="toggleProjectCode('${p.id}')" id="toggleProjBtn-${p.id}" class="px-2.5 py-1 text-slate-400 hover:text-white text-xs font-semibold rounded bg-slate-800/60 hover:bg-slate-800 transition">
                    Collapse Code
                  </button>
                  <button onclick="copyProjectCode('${p.id}')" id="copyProjBtn-${p.id}" class="px-3.5 py-1 text-xs font-semibold rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white flex items-center gap-1.5 shadow transition">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"/></svg>
                    <span>Copy Full Code</span>
                  </button>
                </div>
              </div>

              <div id="codeWrapper-${p.id}" class="relative">
                <pre class="bg-[#050811] p-4 rounded-b-xl border border-slate-800 text-[11px] font-mono text-emerald-300/90 overflow-x-auto max-h-[500px] leading-relaxed"><code id="codeBlock-${p.id}">${escapeHtml(p.code_snippet)}</code></pre>
              </div>
            </div>
          </div>
        `;
      });

      container.innerHTML = html;

      // Render mermaid diagrams
      setTimeout(() => {
        try {
          if (window.mermaid) {
            window.mermaid.run();
          }
        } catch (e) {
          console.warn("Mermaid error:", e);
        }
      }, 50);
    }

    function filterProjects(cat) {
      projectFilterCategory = cat;
      document.querySelectorAll(".proj-btn").forEach(btn => {
        if (btn.dataset.cat === cat) {
          btn.className = "px-2.5 py-1 rounded-md font-medium bg-emerald-600 text-white proj-btn active";
        } else {
          btn.className = "px-2.5 py-1 rounded-md font-medium bg-slate-900 text-slate-400 hover:text-white border border-slate-700 proj-btn";
        }
      });
      renderProjectsList();
    }

    function copyProjectCode(projId) {
      const codeElem = document.getElementById(`codeBlock-${projId}`);
      const btn = document.getElementById(`copyProjBtn-${projId}`);
      if (!codeElem || !btn) return;

      navigator.clipboard.writeText(codeElem.innerText).then(() => {
        const origHTML = btn.innerHTML;
        btn.innerHTML = `
          <svg class="w-3.5 h-3.5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
          <span>Copied!</span>
        `;
        btn.classList.remove("bg-emerald-600", "hover:bg-emerald-500");
        btn.classList.add("bg-teal-500");

        setTimeout(() => {
          btn.innerHTML = origHTML;
          btn.classList.remove("bg-teal-500");
          btn.classList.add("bg-emerald-600", "hover:bg-emerald-500");
        }, 2200);
      });
    }

    function toggleProjectCode(projId) {
      const wrapper = document.getElementById(`codeWrapper-${projId}`);
      const btn = document.getElementById(`toggleProjBtn-${projId}`);
      if (!wrapper || !btn) return;

      if (wrapper.classList.contains("hidden")) {
        wrapper.classList.remove("hidden");
        btn.innerText = "Collapse Code";
      } else {
        wrapper.classList.add("hidden");
        btn.innerText = "Expand Code";
      }
    }
"""

if "    // Mind Map Canvas Engine" in content:
    content = content.replace("    // Mind Map Canvas Engine", render_projects_js + "\n    // Mind Map Canvas Engine")

# 8. Add project search listener and init
old_init = """    document.getElementById("paperSearchInput").addEventListener("input", (e) => {
      paperSearchQuery = e.target.value;
      renderPapersList();
    });

    window.addEventListener("resize", () => {
      render();
    });

    render();
    buildLineWiseDocument();
    renderPapersList();"""

new_init = """    document.getElementById("paperSearchInput").addEventListener("input", (e) => {
      paperSearchQuery = e.target.value;
      renderPapersList();
    });

    document.getElementById("projectSearchInput").addEventListener("input", (e) => {
      projectSearchQuery = e.target.value;
      renderProjectsList();
    });

    window.addEventListener("resize", () => {
      render();
    });

    render();
    buildLineWiseDocument();
    renderPapersList();
    renderProjectsList();"""

if old_init in content:
    content = content.replace(old_init, new_init)

# 9. Update build_html()
old_build_html = """def build_html():
    nodes_json = json.dumps(ALL_NODES, indent=2)
    links_json = json.dumps(CROSS_LINKS, indent=2)
    papers_json = json.dumps(PAPERS, indent=2)
    html = HTML_TEMPLATE.replace("__NODES_JSON__", nodes_json).replace("__LINKS_JSON__", links_json).replace("__PAPERS_JSON__", papers_json)
    with open("ai_ml_dl_master_mindmap.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated ai_ml_dl_master_mindmap.html with Research Papers Tab successfully!")"""

new_build_html = """def build_html():
    nodes_json = json.dumps(ALL_NODES, indent=2)
    links_json = json.dumps(CROSS_LINKS, indent=2)
    papers_json = json.dumps(PAPERS, indent=2)
    projects_json = json.dumps(PROJECTS, indent=2)
    html = HTML_TEMPLATE.replace("__NODES_JSON__", nodes_json).replace("__LINKS_JSON__", links_json).replace("__PAPERS_JSON__", papers_json).replace("__PROJECTS_JSON__", projects_json)
    with open("ai_ml_dl_master_mindmap.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated ai_ml_dl_master_mindmap.html with Production Case Studies Tab successfully!")"""

if old_build_html in content:
    content = content.replace(old_build_html, new_build_html)

with io.open("generate_all.py", "w", encoding="utf-8") as f:
    f.write(content)

print("generate_all.py updated successfully!")
