"""
Build Standalone Dedicated Concept Page: concept.html and concept/index.html
Allows viewing every single core concept / subtopic on its own dedicated page with:
- Simple Definition
- Mathematical Formula (KaTeX typeset)
- Important Logic & Intuition (When to Use)
- Simple Real-World Example
- Search and direct sidebar navigation across all 170 concepts
"""

import json
import os
import shutil
from all_concepts import ALL_CONCEPTS

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONCEPTS_JSON_STR = json.dumps(ALL_CONCEPTS, ensure_ascii=False)

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Core AI Concept Encyclopedia | The Era of AI</title>
  <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🧠</text></svg>">
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          colors: {
            brand: { 50: '#eef2ff', 100: '#e0e7ff', 500: '#6366f1', 600: '#4f46e5', 700: '#4338ca' }
          }
        }
      }
    }
  </script>
  <link rel="stylesheet" href="katex/katex.min.css">
  <script defer src="katex/katex.min.js"></script>
  <script defer src="katex/contrib/auto-render.min.js"></script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
    body { font-family: 'Inter', sans-serif; }
    code, pre { font-family: 'JetBrains Mono', monospace; }
    .no-scrollbar::-webkit-scrollbar { display: none; }
    .no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
    .katex { font-size: 1.15em !important; color: #f8fafc; }
    .katex-display { margin: 0.6em 0 !important; overflow-x: auto; overflow-y: hidden; padding: 0.4rem 0; }
    .formula-card {
      background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 27, 75, 0.6) 100%);
      border: 1px solid rgba(99, 102, 241, 0.3);
    }
    .logic-card {
      background: linear-gradient(135deg, rgba(30, 20, 10, 0.6) 0%, rgba(45, 26, 14, 0.4) 100%);
      border: 1px solid rgba(245, 158, 11, 0.3);
    }
    .example-card {
      background: linear-gradient(135deg, rgba(6, 40, 30, 0.6) 0%, rgba(6, 78, 59, 0.3) 100%);
      border: 1px solid rgba(16, 185, 129, 0.3);
    }
  </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col antialiased selection:bg-indigo-500 selection:text-white">

  <!-- Header Navigation -->
  <header class="sticky top-0 z-40 bg-slate-900/90 backdrop-blur-md border-b border-slate-800 px-4 py-3 flex items-center justify-between">
    <div class="flex items-center gap-3">
      <a href="index.html" class="flex items-center gap-2 text-white font-bold text-sm md:text-base hover:text-indigo-400 transition">
        <span class="text-xl">🌌</span>
        <span class="hidden sm:inline">The Era of AI</span>
        <span class="text-xs px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">Encyclopedia</span>
      </a>
      <span class="text-slate-600">/</span>
      <span id="headerCategoryBadge" class="text-xs px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-medium">Concept Page</span>
    </div>

    <div class="flex items-center gap-2">
      <a href="index.html#syllabus" class="text-xs px-3 py-1.5 rounded-lg bg-slate-800 text-slate-300 hover:text-white hover:bg-slate-700 transition flex items-center gap-1.5 border border-slate-700">
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16"/></svg>
        <span>Line-wise Syllabus</span>
      </a>
      <a href="index.html#mindmap" class="text-xs px-3 py-1.5 rounded-lg bg-indigo-600/80 text-white hover:bg-indigo-600 transition flex items-center gap-1.5">
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
        <span>Interactive Mind Map</span>
      </a>
      <button id="mobileMenuToggle" class="md:hidden p-1.5 rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/></svg>
      </button>
    </div>
  </header>

  <!-- Main Workspace -->
  <div class="flex-1 flex overflow-hidden">

    <!-- Sidebar: Concept Index -->
    <aside id="sidebar" class="w-80 border-r border-slate-800 bg-slate-900/60 flex flex-col shrink-0 fixed inset-y-0 left-0 z-30 pt-16 md:pt-0 md:static transform -translate-x-full md:translate-x-0 transition-transform duration-200">
      <div class="p-3 border-b border-slate-800 bg-slate-900/80">
        <div class="relative">
          <input type="text" id="conceptSearch" placeholder="Search 170+ concepts..." class="w-full text-xs bg-slate-950 border border-slate-700 rounded-lg pl-8 pr-3 py-2 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition">
          <svg class="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
        </div>
        <div class="flex items-center justify-between text-[11px] text-slate-400 mt-2 px-1">
          <span id="conceptCount">170 concepts</span>
          <span class="text-indigo-400 font-medium">8 Domains</span>
        </div>
      </div>

      <!-- Tree / List of Concepts -->
      <div id="conceptListContainer" class="flex-1 overflow-y-auto p-2 space-y-4 no-scrollbar">
        <!-- Rendered via JavaScript -->
      </div>
    </aside>

    <!-- Content Area: The Dedicated Concept Page -->
    <main class="flex-1 overflow-y-auto p-4 md:p-8 bg-slate-950">
      <div class="max-w-3xl mx-auto space-y-6 pb-20">

        <!-- Breadcrumbs & Category Bar -->
        <div class="flex items-center justify-between flex-wrap gap-2 text-xs">
          <div class="flex items-center gap-2 text-slate-400">
            <span id="conceptCategoryTag" class="px-2.5 py-0.5 rounded-full bg-slate-800 border border-slate-700 text-indigo-300 font-medium">Domain</span>
            <span>›</span>
            <span id="conceptTopicTag" class="text-slate-300 font-medium">Topic</span>
          </div>
          <div class="flex items-center gap-2">
            <button onclick="copyConceptUrl()" id="shareBtn" class="px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-300 text-xs flex items-center gap-1 transition">
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/></svg>
              <span>Copy Link</span>
            </button>
          </div>
        </div>

        <!-- Concept Header -->
        <div class="border-b border-slate-800 pb-5">
          <h1 id="conceptTitle" class="text-2xl md:text-3xl font-extrabold text-white tracking-tight leading-snug">
            Concept Title
          </h1>
          <p id="conceptSubtext" class="text-xs text-slate-400 mt-1 font-mono">
            Topic Canonical Terminology
          </p>
        </div>

        <!-- 1. Simple Definition -->
        <section class="space-y-2">
          <div class="flex items-center gap-2 text-xs uppercase tracking-wider font-bold text-blue-400">
            <span>📖 Simple Definition</span>
          </div>
          <div class="bg-slate-900/80 border border-slate-800/80 rounded-xl p-4 md:p-5">
            <p id="conceptDef" class="text-sm md:text-base text-slate-200 leading-relaxed font-normal">
              Loading definition...
            </p>
          </div>
        </section>

        <!-- 2. Mathematical Formula -->
        <section class="space-y-2" id="formulaContainerSection">
          <div class="flex items-center justify-between text-xs uppercase tracking-wider font-bold text-indigo-400">
            <span>🔢 Mathematical Formula & Formulation</span>
            <span class="text-[10px] lowercase font-normal px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-300 border border-indigo-500/20">KaTeX Formatted</span>
          </div>
          <div class="formula-card rounded-xl p-4 md:p-5 overflow-x-auto shadow-inner">
            <div id="conceptFormula" class="text-sm md:text-base text-center py-2 text-indigo-100">
              <!-- Rendered LaTeX -->
            </div>
            <p id="conceptFormulaExpl" class="text-xs text-slate-400 mt-3 pt-3 border-t border-slate-800/60 leading-relaxed">
              Formula explanation.
            </p>
          </div>
        </section>

        <!-- 3. Important Logic & Intuition -->
        <section class="space-y-2">
          <div class="flex items-center gap-2 text-xs uppercase tracking-wider font-bold text-amber-400">
            <span>💡 Important Logic & Intuition (When to Use)</span>
          </div>
          <div class="logic-card rounded-xl p-4 md:p-5">
            <p id="conceptLogic" class="text-xs md:text-sm text-amber-100/90 leading-relaxed font-normal">
              Loading logic explanation...
            </p>
          </div>
        </section>

        <!-- 4. Simple Real-World Example -->
        <section class="space-y-2">
          <div class="flex items-center gap-2 text-xs uppercase tracking-wider font-bold text-emerald-400">
            <span>🎯 Simple Real-World Example</span>
          </div>
          <div class="example-card rounded-xl p-4 md:p-5">
            <p id="conceptExample" class="text-xs md:text-sm text-emerald-100/90 leading-relaxed font-normal">
              Loading real-world example...
            </p>
          </div>
        </section>

        <!-- Previous / Next Navigation -->
        <div class="pt-6 border-t border-slate-800 flex items-center justify-between gap-4">
          <button id="prevConceptBtn" class="flex-1 max-w-[240px] px-3 py-2.5 rounded-lg bg-slate-900 border border-slate-800 hover:border-slate-700 text-left transition flex items-center gap-2">
            <span class="text-slate-500">←</span>
            <div class="truncate">
              <div class="text-[10px] text-slate-400 uppercase">Previous</div>
              <div id="prevConceptTitle" class="text-xs font-semibold text-slate-200 truncate">Prev Concept</div>
            </div>
          </button>

          <button id="nextConceptBtn" class="flex-1 max-w-[240px] px-3 py-2.5 rounded-lg bg-slate-900 border border-slate-800 hover:border-slate-700 text-right transition flex items-center justify-end gap-2">
            <div class="truncate">
              <div class="text-[10px] text-slate-400 uppercase">Next</div>
              <div id="nextConceptTitle" class="text-xs font-semibold text-slate-200 truncate">Next Concept</div>
            </div>
            <span class="text-slate-500">→</span>
          </button>
        </div>

      </div>
    </main>

  </div>

  <!-- Raw Concepts Database Embedded -->
  <script>
    const CONCEPTS_DATA = CONCEPTS_DATA_PLACEHOLDER;
    let currentConceptIndex = 0;

    // Normalizer
    function norm(s) {
      return (s || '').toLowerCase().replace(/[^a-z0-9]/g, '');
    }

    // Sidebar Index Renderer
    function renderSidebar(filterQuery = '') {
      const container = document.getElementById("conceptListContainer");
      container.innerHTML = "";

      const q = norm(filterQuery);
      const filtered = CONCEPTS_DATA.filter(c => {
        if (!q) return true;
        return norm(c.title).includes(q) || norm(c.raw_sub).includes(q) || norm(c.topic_label).includes(q) || norm(c.category_label).includes(q);
      });

      document.getElementById("conceptCount").textContent = `${filtered.length} of ${CONCEPTS_DATA.length} concepts`;

      // Group by Topic
      const grouped = {};
      filtered.forEach(c => {
        const key = c.topic_label || "Other Concepts";
        if (!grouped[key]) grouped[key] = [];
        grouped[key].push(c);
      });

      for (const [topic, items] of Object.entries(grouped)) {
        const section = document.createElement("div");
        section.className = "space-y-1";

        const title = document.createElement("div");
        title.className = "text-[11px] font-bold text-slate-400 px-2 uppercase tracking-wider flex items-center justify-between";
        title.innerHTML = `<span>${topic}</span> <span class="text-[9px] px-1.5 py-0.2 rounded bg-slate-800 text-slate-400">${items.length}</span>`;
        section.appendChild(title);

        items.forEach(item => {
          const btn = document.createElement("button");
          const isActive = CONCEPTS_DATA[currentConceptIndex]?.id === item.id;
          btn.className = `w-full text-left px-2.5 py-1.5 rounded-lg text-xs transition flex items-center justify-between group ${
            isActive
              ? "bg-indigo-600/30 text-indigo-300 font-semibold border border-indigo-500/40"
              : "text-slate-300 hover:bg-slate-800/80 hover:text-white"
          }`;
          btn.innerHTML = `<span class="truncate">${item.title}</span> <span class="text-[10px] text-slate-500 group-hover:text-slate-400 ml-1 shrink-0">➔</span>`;
          btn.onclick = () => {
            selectConceptById(item.id);
            if (window.innerWidth < 768) {
              document.getElementById("sidebar").classList.add("-translate-x-full");
            }
          };
          section.appendChild(btn);
        });

        container.appendChild(section);
      }
    }

    // Select Concept & Update UI
    function selectConceptByIndex(idx) {
      if (idx < 0 || idx >= CONCEPTS_DATA.length) return;
      currentConceptIndex = idx;
      const c = CONCEPTS_DATA[idx];

      document.title = `${c.title} | AI Encyclopedia`;
      document.getElementById("conceptTitle").textContent = c.title;
      document.getElementById("conceptSubtext").textContent = c.raw_sub || c.title;
      document.getElementById("headerCategoryBadge").textContent = c.category_label || "AI Core Concept";
      document.getElementById("conceptCategoryTag").textContent = c.category_label || "AI Domain";
      document.getElementById("conceptTopicTag").textContent = c.topic_label || "Topic";

      // 1. Definition
      document.getElementById("conceptDef").textContent = c.definition || c.def || "Core theoretical definition.";

      // 2. Formula
      const formulaEl = document.getElementById("conceptFormula");
      const formulaSec = document.getElementById("formulaContainerSection");
      const explEl = document.getElementById("conceptFormulaExpl");
      if (c.formula && c.formula.trim()) {
        formulaSec.style.display = "block";
        formulaEl.innerHTML = c.formula;
        explEl.textContent = c.formula_explanation || "Mathematical formulation and parameter variables defined above.";
        explEl.style.display = c.formula_explanation ? "block" : "none";
        triggerMath(formulaSec);
      } else {
        formulaSec.style.display = "none";
      }

      // 3. Logic
      document.getElementById("conceptLogic").textContent = c.logic || "Fundamental logic and inductive biases.";

      // 4. Example
      document.getElementById("conceptExample").textContent = c.example || "Practical industry application scenario.";

      // Navigation Prev / Next
      const prevBtn = document.getElementById("prevConceptBtn");
      const nextBtn = document.getElementById("nextConceptBtn");

      if (idx > 0) {
        prevBtn.style.visibility = "visible";
        document.getElementById("prevConceptTitle").textContent = CONCEPTS_DATA[idx - 1].title;
        prevBtn.onclick = () => selectConceptByIndex(idx - 1);
      } else {
        prevBtn.style.visibility = "hidden";
      }

      if (idx < CONCEPTS_DATA.length - 1) {
        nextBtn.style.visibility = "visible";
        document.getElementById("nextConceptTitle").textContent = CONCEPTS_DATA[idx + 1].title;
        nextBtn.onclick = () => selectConceptByIndex(idx + 1);
      } else {
        nextBtn.style.visibility = "hidden";
      }

      // Update URL without reload
      history.replaceState({ id: c.id }, "", `?id=${c.id}`);

      // Re-highlight sidebar
      renderSidebar(document.getElementById("conceptSearch").value);
    }

    function selectConceptById(id) {
      const idx = CONCEPTS_DATA.findIndex(c => c.id === id);
      if (idx !== -1) {
        selectConceptByIndex(idx);
        return;
      }
      const qNorm = norm(id);
      const matchIdx = CONCEPTS_DATA.findIndex(c => norm(c.id).includes(qNorm) || norm(c.raw_sub).includes(qNorm) || norm(c.title).includes(qNorm));
      if (matchIdx !== -1) {
        selectConceptByIndex(matchIdx);
      } else {
        selectConceptByIndex(0);
      }
    }

    function triggerMath(el) {
      if (window.renderMathInElement) {
        renderMathInElement(el, {
          delimiters: [
            { left: "$$", right: "$$", display: true },
            { left: "$", right: "$", display: false },
            { left: "\\\\(", right: "\\\\)", display: false },
            { left: "\\\\[", right: "\\\\]", display: true }
          ],
          throwOnError: false
        });
      }
    }

    function copyConceptUrl() {
      const url = window.location.href;
      navigator.clipboard.writeText(url).then(() => {
        const btn = document.getElementById("shareBtn");
        const orig = btn.innerHTML;
        btn.innerHTML = `<span class="text-emerald-400 font-bold">✓ Copied!</span>`;
        setTimeout(() => { btn.innerHTML = orig; }, 1800);
      });
    }

    // Initialize from URL query param or hash
    window.addEventListener("DOMContentLoaded", () => {
      const params = new URLSearchParams(window.location.search);
      let targetId = params.get("id");
      if (!targetId && window.location.hash) {
        targetId = window.location.hash.replace(/^#/, '').replace(/^concept\\//, '');
      }

      if (targetId) {
        selectConceptById(targetId);
      } else {
        selectConceptByIndex(0);
      }

      document.getElementById("conceptSearch").addEventListener("input", (e) => {
        renderSidebar(e.target.value);
      });

      document.getElementById("mobileMenuToggle").addEventListener("click", () => {
        document.getElementById("sidebar").classList.toggle("-translate-x-full");
      });

      // Periodic check to ensure KaTeX has rendered
      setTimeout(() => {
        const sec = document.getElementById("formulaContainerSection");
        if (sec) triggerMath(sec);
      }, 500);
    });
  </script>
</body>
</html>
"""

def build_standalone_concept_pages():
    final_html = HTML_TEMPLATE.replace("CONCEPTS_DATA_PLACEHOLDER", CONCEPTS_JSON_STR)
    
    out_file = os.path.join(SCRIPT_DIR, "concept.html")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(final_html)
    print(f"Generated standalone {out_file} ({len(final_html):,} bytes)")

    # Also make a concept/index.html folder route
    concept_dir = os.path.join(SCRIPT_DIR, "concept")
    os.makedirs(concept_dir, exist_ok=True)
    concept_index = os.path.join(concept_dir, "index.html")
    
    # In concept/index.html, adjust katex path to ../katex/
    sub_html = final_html.replace('href="katex/', 'href="../katex/').replace('src="katex/', 'src="../katex/')
    sub_html = sub_html.replace('href="index.html"', 'href="../index.html"')
    sub_html = sub_html.replace('href="index.html#syllabus"', 'href="../index.html#syllabus"')
    sub_html = sub_html.replace('href="index.html#mindmap"', 'href="../index.html#mindmap"')
    
    with open(concept_index, "w", encoding="utf-8") as f:
        f.write(sub_html)
    print(f"Generated standalone {concept_index} ({len(sub_html):,} bytes)")

if __name__ == "__main__":
    build_standalone_concept_pages()
