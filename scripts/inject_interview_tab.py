"""
Script to inject the 5th Tab: Interview Q&A Vault (150 Questions) into generate_all.py.
"""

import io

with io.open("generate_all.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Import INTERVIEW_QUESTIONS
if "from interview_questions_data import INTERVIEW_QUESTIONS" not in content:
    content = content.replace(
        "from projects_data import PROJECTS",
        "from projects_data import PROJECTS\nfrom interview_questions_data import INTERVIEW_QUESTIONS"
    )

# 2. Add Tab 5 Button to Header
old_tab_proj = """      <button onclick="switchMainTab('projects')" id="tabBtn-projects" class="px-3.5 py-1.5 rounded-lg text-xs font-semibold text-slate-300 hover:text-white transition flex items-center gap-1.5 relative">
        <svg class="w-3.5 h-3.5 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/></svg>
        <span>Production Case Studies</span>
        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
      </button>"""

new_tabs_proj = """      <button onclick="switchMainTab('projects')" id="tabBtn-projects" class="px-3.5 py-1.5 rounded-lg text-xs font-semibold text-slate-300 hover:text-white transition flex items-center gap-1.5 relative">
        <svg class="w-3.5 h-3.5 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/></svg>
        <span>Production Case Studies</span>
        <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
      </button>

      <button onclick="switchMainTab('interview')" id="tabBtn-interview" class="px-3.5 py-1.5 rounded-lg text-xs font-semibold text-slate-300 hover:text-white transition flex items-center gap-1.5 relative">
        <svg class="w-3.5 h-3.5 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
        <span>Interview Vault (150+)</span>
        <span class="w-2 h-2 rounded-full bg-purple-400 animate-pulse"></span>
      </button>"""

if old_tab_proj in content:
    content = content.replace(old_tab_proj, new_tabs_proj)
else:
    print("WARNING: Could not find old_tab_proj")

# 3. Add Tab 5 Container right after projectsTabContainer
projects_container_end = """        <!-- Projects List Container -->
        <div id="projectsList" class="space-y-8"></div>
      </div>
    </div>"""

interview_container = """        <!-- Projects List Container -->
        <div id="projectsList" class="space-y-8"></div>
      </div>
    </div>

    <!-- TAB 5: Technical Interview Question & Answer Bank (150 Questions) -->
    <div id="interviewTabContainer" class="hidden absolute inset-0 overflow-y-auto p-6 md:p-12 z-10 bg-[var(--background,#0b0f19)] text-[var(--foreground,#f8fafc)]">
      <div class="max-w-6xl mx-auto space-y-6 pb-20">
        <!-- Header -->
        <div class="border-b border-slate-700 pb-5 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-purple-500/20 text-purple-300 border border-purple-500/30 text-xs font-semibold uppercase tracking-wider mb-2">
              🎯 150 Technical Interview Questions & Answers
            </div>
            <h2 class="text-2xl md:text-3xl font-extrabold tracking-tight text-white">
              AI, Machine Learning, LLMs & Quant Interview Master Vault
            </h2>
            <p class="text-xs md:text-sm text-slate-400 mt-1">
              Top-Tier Questions from FAANG/MAANG, Frontier AI Labs (OpenAI, DeepMind), and Quant Funds (Jane Street, Citadel). Answers are hidden by default for active recall testing.
            </p>
          </div>

          <div class="flex items-center space-x-2 text-xs no-print">
            <button onclick="revealAllInterviewAnswers()" class="px-3 py-1.5 rounded-lg bg-purple-600/30 hover:bg-purple-600 text-purple-300 hover:text-white border border-purple-500/40 font-semibold transition flex items-center gap-1.5">
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
              <span>Reveal All</span>
            </button>
            <button onclick="hideAllInterviewAnswers()" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold border border-slate-700 transition flex items-center gap-1.5">
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l18 18"/></svg>
              <span>Hide All</span>
            </button>
          </div>
        </div>

        <!-- Search & Filter Controls -->
        <div class="space-y-3 no-print">
          <div class="relative max-w-md">
            <input id="qSearchInput" type="text" placeholder="Search 150 questions (e.g. RoPE, AdamW, KV-cache, Monty Hall, L1)..."
                   class="w-full bg-slate-900 border border-slate-700 text-xs text-white rounded-lg pl-8 pr-4 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500 placeholder-slate-500">
            <svg class="w-4 h-4 absolute left-2.5 top-2.5 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
          </div>

          <div class="flex items-center flex-wrap gap-1.5 text-xs">
            <button onclick="filterInterviewCategory('all')" class="px-2.5 py-1 rounded-md font-medium bg-purple-600 text-white q-cat-btn active" data-cat="all">All (150)</button>
            <button onclick="filterInterviewCategory('ml')" class="px-2.5 py-1 rounded-md font-medium bg-slate-900 text-slate-400 hover:text-white border border-slate-700 q-cat-btn" data-cat="ml">Classical ML (25)</button>
            <button onclick="filterInterviewCategory('dl')" class="px-2.5 py-1 rounded-md font-medium bg-slate-900 text-slate-400 hover:text-white border border-slate-700 q-cat-btn" data-cat="dl">Deep Learning (25)</button>
            <button onclick="filterInterviewCategory('genai_llm')" class="px-2.5 py-1 rounded-md font-medium bg-slate-900 text-slate-400 hover:text-white border border-slate-700 q-cat-btn" data-cat="genai_llm">Transformers & LLMs (25)</button>
            <button onclick="filterInterviewCategory('rag')" class="px-2.5 py-1 rounded-md font-medium bg-slate-900 text-slate-400 hover:text-white border border-slate-700 q-cat-btn" data-cat="rag">RAG & Vector Search (20)</button>
            <button onclick="filterInterviewCategory('metrics_data')" class="px-2.5 py-1 rounded-md font-medium bg-slate-900 text-slate-400 hover:text-white border border-slate-700 q-cat-btn" data-cat="metrics_data">Metrics & Preprocessing (20)</button>
            <button onclick="filterInterviewCategory('system_mlops')" class="px-2.5 py-1 rounded-md font-medium bg-slate-900 text-slate-400 hover:text-white border border-slate-700 q-cat-btn" data-cat="system_mlops">MLOps & System Design (20)</button>
            <button onclick="filterInterviewCategory('logic_prob')" class="px-2.5 py-1 rounded-md font-medium bg-slate-900 text-slate-400 hover:text-white border border-slate-700 q-cat-btn" data-cat="logic_prob">Logic & Probability (15)</button>
          </div>
        </div>

        <!-- Questions List Container -->
        <div id="questionsContainer" class="space-y-4"></div>
      </div>
    </div>"""

if projects_container_end in content:
    content = content.replace(projects_container_end, interview_container)
else:
    print("WARNING: Could not find projects_container_end")

# 4. In JS: Add QUESTIONS_DATA
old_js_vars = """    const PROJECTS_DATA = __PROJECTS_JSON__;

    let projectFilterCategory = "all";
    let projectSearchQuery = "";"""

new_js_vars = """    const PROJECTS_DATA = __PROJECTS_JSON__;
    const QUESTIONS_DATA = __QUESTIONS_JSON__;

    let projectFilterCategory = "all";
    let projectSearchQuery = "";

    let interviewFilterCategory = "all";
    let interviewSearchQuery = "";
    let openQuestionsSet = new Set();
    let solvedQuestionsSet = new Set();"""

if old_js_vars in content:
    content = content.replace(old_js_vars, new_js_vars)

# 5. In JS: Update switchMainTab
old_switch = """      } else if (tab === "projects") {
        mindmapTab.classList.add("hidden");
        syllabusTab.classList.add("hidden");
        papersTab.classList.add("hidden");
        projectsTab.classList.remove("hidden");
        mindmapToolbar.classList.add("hidden");
        renderProjectsList();
      }
    }"""

new_switch = """      } else if (tab === "projects") {
        mindmapTab.classList.add("hidden");
        syllabusTab.classList.add("hidden");
        papersTab.classList.add("hidden");
        projectsTab.classList.remove("hidden");
        if (interviewTab) interviewTab.classList.add("hidden");
        mindmapToolbar.classList.add("hidden");
        renderProjectsList();
      } else if (tab === "interview") {
        mindmapTab.classList.add("hidden");
        syllabusTab.classList.add("hidden");
        papersTab.classList.add("hidden");
        projectsTab.classList.add("hidden");
        if (interviewTab) interviewTab.classList.remove("hidden");
        mindmapToolbar.classList.add("hidden");
        renderQuestionsList();
      }
    }"""

# We also need to get interviewTab in switchMainTab:
content = content.replace(
    'const projectsTab = document.getElementById("projectsTabContainer");',
    'const projectsTab = document.getElementById("projectsTabContainer");\n      const interviewTab = document.getElementById("interviewTabContainer");'
)

if old_switch in content:
    content = content.replace(old_switch, new_switch)
else:
    print("WARNING: Could not find old_switch")

# 6. Add renderQuestionsList and helper functions before Mind Map Canvas Engine
render_q_js = """
    // ----------------------------------------------------
    // 150 INTERVIEW QUESTIONS & ANSWERS RENDERER
    // ----------------------------------------------------
    function formatAnswerMarkdown(text) {
      if (!text) return "";
      return text
        .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
        .replace(/\\*\\*(.*?)\\*\\*/g, '<strong class="text-white font-bold">$1</strong>')
        .replace(/\\*(.*?)\\*/g, '<em class="text-slate-300 italic">$1</em>')
        .replace(/`([^`]+)`/g, '<code class="px-1.5 py-0.5 rounded bg-slate-800 text-purple-300 text-xs font-mono">$1</code>')
        .replace(/\\n\\n/g, '<div class="my-2"></div>')
        .replace(/\\n- /g, '<br>&bull; ')
        .replace(/\\n/g, '<br>');
    }

    function renderQuestionsList() {
      const container = document.getElementById("questionsContainer");
      if (!container) return;

      const filtered = QUESTIONS_DATA.filter(q => {
        if (interviewFilterCategory !== "all" && q.category !== interviewFilterCategory) {
          return false;
        }
        if (interviewSearchQuery.trim()) {
          const term = interviewSearchQuery.toLowerCase();
          const matchQ = q.question.toLowerCase().includes(term);
          const matchA = q.answer.toLowerCase().includes(term);
          const matchCat = q.category_label.toLowerCase().includes(term);
          const matchCompany = q.company_tags.some(c => c.toLowerCase().includes(term));
          return matchQ || matchA || matchCat || matchCompany;
        }
        return true;
      });

      if (filtered.length === 0) {
        container.innerHTML = `<div class="p-8 text-center text-slate-500 bg-slate-900/50 rounded-xl border border-slate-800">No matching questions found. Try searching for 'RoPE', 'AdamW', 'L1', or 'Monty Hall'.</div>`;
        return;
      }

      let html = "";
      filtered.forEach((q, idx) => {
        const isOpen = openQuestionsSet.has(q.id);
        const isSolved = solvedQuestionsSet.has(q.id);
        const companyChips = q.company_tags.map(c => 
          `<span class="px-2 py-0.5 rounded-md bg-slate-800/80 text-slate-300 border border-slate-700 text-[10px] font-medium">${c}</span>`
        ).join("");

        const diffColors = {
          "Junior / Mid": "bg-blue-500/20 text-blue-300 border-blue-500/30",
          "Mid / Senior": "bg-indigo-500/20 text-indigo-300 border-indigo-500/30",
          "Senior": "bg-purple-500/20 text-purple-300 border-purple-500/30",
          "Senior / Staff": "bg-pink-500/20 text-pink-300 border-pink-500/30",
          "Quant / Research": "bg-amber-500/20 text-amber-300 border-amber-500/30"
        };
        const diffClass = diffColors[q.difficulty] || "bg-slate-800 text-slate-300 border-slate-700";

        html += `
          <div class="print-card bg-slate-900/90 border ${isSolved ? 'border-emerald-600/40' : 'border-slate-800'} rounded-2xl p-5 md:p-6 space-y-4 shadow-lg transition hover:border-slate-700">
            <!-- Header Row -->
            <div class="flex items-start justify-between flex-wrap gap-2">
              <div class="flex items-center flex-wrap gap-2">
                <span class="px-2.5 py-0.5 rounded-full text-[11px] font-bold border ${diffClass}">
                  ${q.difficulty}
                </span>
                <span class="px-2.5 py-0.5 rounded-full bg-slate-800 text-slate-300 border border-slate-700 text-[11px] font-semibold">
                  ${q.category_label}
                </span>
                <div class="flex items-center gap-1">
                  ${companyChips}
                </div>
              </div>

              <div class="flex items-center space-x-2 no-print">
                <label class="flex items-center space-x-1.5 cursor-pointer text-xs text-slate-400 hover:text-white">
                  <input type="checkbox" onchange="toggleInterviewSolved('${q.id}')" ${isSolved ? 'checked' : ''}
                         class="rounded border-slate-700 text-emerald-500 focus:ring-emerald-500">
                  <span class="${isSolved ? 'text-emerald-400 font-semibold' : ''}">${isSolved ? 'Mastered' : 'Mark Solved'}</span>
                </label>
              </div>
            </div>

            <!-- Question Title -->
            <h3 class="text-base md:text-lg font-bold text-white leading-snug">
              <span class="text-purple-400 font-mono mr-1.5">Q${idx + 1}.</span> ${q.question}
            </h3>

            <!-- Toggle Answer Button -->
            <div class="pt-1 no-print">
              <button onclick="toggleInterviewAnswer('${q.id}')" id="btn-ans-${q.id}"
                      class="px-4 py-2 rounded-xl text-xs font-semibold flex items-center gap-2 transition ${isOpen ? 'bg-slate-800 text-slate-300 hover:text-white' : 'bg-purple-600 hover:bg-purple-500 text-white shadow-lg shadow-purple-600/20'}">
                <svg class="w-4 h-4 transform transition-transform ${isOpen ? 'rotate-180' : ''}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                </svg>
                <span>${isOpen ? 'Hide Detailed Answer' : '💡 Reveal Answer & Explanation'}</span>
              </button>
            </div>

            <!-- Answer Section (Hidden Initially) -->
            <div id="ans-box-${q.id}" class="${isOpen ? '' : 'hidden'} print:block pt-2 space-y-4 border-t border-slate-800/80">
              <div class="bg-slate-950/80 p-5 rounded-xl border border-slate-800 text-slate-200 text-xs md:text-sm leading-relaxed space-y-2">
                ${formatAnswerMarkdown(q.answer)}
              </div>

              ${q.tip ? `
                <div class="p-3.5 rounded-xl bg-amber-950/30 border border-amber-800/40 text-amber-200 text-xs flex items-start gap-2.5">
                  <span class="text-base flex-shrink-0">⭐</span>
                  <div>
                    <strong class="text-amber-100 font-semibold block mb-0.5">Interviewer Evaluation Tip:</strong>
                    <span>${q.tip}</span>
                  </div>
                </div>
              ` : ''}
            </div>
          </div>
        `;
      });

      container.innerHTML = html;
    }

    function toggleInterviewAnswer(id) {
      if (openQuestionsSet.has(id)) {
        openQuestionsSet.delete(id);
      } else {
        openQuestionsSet.add(id);
      }
      renderQuestionsList();
    }

    function revealAllInterviewAnswers() {
      QUESTIONS_DATA.forEach(q => openQuestionsSet.add(q.id));
      renderQuestionsList();
    }

    function hideAllInterviewAnswers() {
      openQuestionsSet.clear();
      renderQuestionsList();
    }

    function toggleInterviewSolved(id) {
      if (solvedQuestionsSet.has(id)) {
        solvedQuestionsSet.delete(id);
      } else {
        solvedQuestionsSet.add(id);
      }
      renderQuestionsList();
    }

    function filterInterviewCategory(cat) {
      interviewFilterCategory = cat;
      document.querySelectorAll(".q-cat-btn").forEach(btn => {
        if (btn.dataset.cat === cat) {
          btn.className = "px-2.5 py-1 rounded-md font-medium bg-purple-600 text-white q-cat-btn active";
        } else {
          btn.className = "px-2.5 py-1 rounded-md font-medium bg-slate-900 text-slate-400 hover:text-white border border-slate-700 q-cat-btn";
        }
      });
      renderQuestionsList();
    }
"""

if "    // Mind Map Canvas Engine" in content:
    content = content.replace("    // Mind Map Canvas Engine", render_q_js + "\n    // Mind Map Canvas Engine")

# 7. Add question search listener and render call
old_render_init = """    render();
    buildLineWiseDocument();
    renderPapersList();
    renderProjectsList();"""

new_render_init = """    document.getElementById("qSearchInput").addEventListener("input", (e) => {
      interviewSearchQuery = e.target.value;
      renderQuestionsList();
    });

    render();
    buildLineWiseDocument();
    renderPapersList();
    renderProjectsList();
    renderQuestionsList();"""

if old_render_init in content:
    content = content.replace(old_render_init, new_render_init)

# 8. Update build_html
old_b_html = """def build_html():
    nodes_json = json.dumps(ALL_NODES, indent=2)
    links_json = json.dumps(CROSS_LINKS, indent=2)
    papers_json = json.dumps(PAPERS, indent=2)
    projects_json = json.dumps(PROJECTS, indent=2)
    html = HTML_TEMPLATE.replace("__NODES_JSON__", nodes_json).replace("__LINKS_JSON__", links_json).replace("__PAPERS_JSON__", papers_json).replace("__PROJECTS_JSON__", projects_json)
    with open("ai_ml_dl_master_mindmap.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated ai_ml_dl_master_mindmap.html with Production Case Studies Tab successfully!")"""

new_b_html = """def build_html():
    nodes_json = json.dumps(ALL_NODES, indent=2)
    links_json = json.dumps(CROSS_LINKS, indent=2)
    papers_json = json.dumps(PAPERS, indent=2)
    projects_json = json.dumps(PROJECTS, indent=2)
    questions_json = json.dumps(INTERVIEW_QUESTIONS, indent=2)
    html = (HTML_TEMPLATE
            .replace("__NODES_JSON__", nodes_json)
            .replace("__LINKS_JSON__", links_json)
            .replace("__PAPERS_JSON__", papers_json)
            .replace("__PROJECTS_JSON__", projects_json)
            .replace("__QUESTIONS_JSON__", questions_json))
    with open("ai_ml_dl_master_mindmap.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated ai_ml_dl_master_mindmap.html with Interview Questions Vault successfully!")"""

if old_b_html in content:
    content = content.replace(old_b_html, new_b_html)

with io.open("generate_all.py", "w", encoding="utf-8") as f:
    f.write(content)

print("generate_all.py injected with Interview Q&A Tab successfully!")
