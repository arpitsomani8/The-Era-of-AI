"""
Standalone Builder for Interview Questions Portal & Markdown Compendium.
Outputs:
  - interview_questions.html
  - interview_questions.md
"""

import json
from interview_questions_data import INTERVIEW_QUESTIONS

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Master AI & ML Technical Interview Question Bank (150 Questions & Answers)</title>
  <script src="https://cdn.tailwindcss.com"></script>

  <!-- KaTeX for Mathematical Typesetting (Local + CDN Fallback) -->
  <link rel="stylesheet" href="katex/katex.min.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
  <script src="katex/katex.min.js"></script>
  <script src="katex/auto-render.min.js"></script>
  <script>
    if (typeof katex === 'undefined') {
      document.write('<script src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"><\\/script>');
      document.write('<script src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"><\\/script>');
    }
  </script>

  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
    body {
      font-family: 'Inter', sans-serif;
    }
    pre, code {
      font-family: 'JetBrains Mono', monospace;
    }
    ::-webkit-scrollbar {
      width: 8px;
      height: 8px;
    }
    ::-webkit-scrollbar-track {
      background: #090d16;
    }
    ::-webkit-scrollbar-thumb {
      background: #1e293b;
      border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
      background: #334155;
    }

    /* KaTeX equation display enhancements */
    .katex {
      font-size: 1.05em !important;
      text-rendering: geometricPrecision;
      color: #f1f5f9;
    }
    .katex-display {
      margin: 0.7em 0 !important;
      overflow-x: auto !important;
      overflow-y: hidden !important;
      padding: 0.4rem 0.25rem;
      scrollbar-width: thin;
      text-align: center;
    }
    .katex-display::-webkit-scrollbar {
      height: 4px;
    }
    .katex-display::-webkit-scrollbar-thumb {
      background: #8b5cf6;
      border-radius: 2px;
    }
    .katex .mord, .katex .mbin, .katex .mrel, .katex .mopen, .katex .mclose, .katex .mpunct {
      color: #f8fafc;
    }
    .katex .frac-line {
      border-bottom-width: 1.5px !important;
      border-color: #c4b5fd !important;
    }
    .katex-inline-formula {
      display: inline-block;
      padding: 0 1.5px;
      vertical-align: middle;
    }
    .formula-box {
      background: rgba(15, 23, 42, 0.7);
      border: 1px solid rgba(139, 92, 246, 0.25);
      border-radius: 0.6rem;
      padding: 0.6rem 0.8rem;
      margin: 0.5rem 0;
      overflow-x: auto;
    }
  </style>
</head>
<body class="bg-[#0b0f19] text-[#f8fafc] min-h-screen flex flex-col">

  <!-- Navbar -->
  <header class="bg-[#111827]/90 backdrop-blur-md border-b border-slate-800 sticky top-0 z-30 px-6 py-3.5 flex items-center justify-between">
    <div class="flex items-center space-x-3">
      <div class="p-2 rounded-xl bg-gradient-to-tr from-purple-600 to-indigo-500 text-white shadow-lg shadow-purple-500/20">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
      </div>
      <div>
        <h1 class="font-extrabold text-lg text-white tracking-tight flex items-center gap-2">
          AI & Machine Learning Interview Vault
          <span class="px-2 py-0.5 rounded-full bg-purple-500/20 text-purple-400 border border-purple-500/30 text-[11px] font-semibold">150 Questions & Answers</span>
        </h1>
        <p class="text-xs text-slate-400">FAANG/MAANG &bull; AI Labs (OpenAI, DeepMind) &bull; Quant Hedge Funds &bull; Hidden Answers Initially</p>
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
        <a href="production_ai_case_studies.html" class="px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-300 hover:text-white transition flex items-center gap-1.5 whitespace-nowrap">
          <svg class="w-3.5 h-3.5 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/></svg>
          <span>Case Studies</span>
        </a>
        <a href="interview_questions.html" class="px-3 py-1.5 rounded-lg text-xs font-semibold bg-purple-600 text-white shadow transition flex items-center gap-1.5 whitespace-nowrap">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
          <span>Interview Vault</span>
        </a>
      </nav>
    </div>
  </header>

  <!-- Main Container -->
  <main class="max-w-6xl mx-auto p-6 md:p-10 flex-1 space-y-8 w-full">

    <!-- Hero Banner -->
    <div class="rounded-2xl p-6 md:p-8 bg-gradient-to-r from-slate-900 via-purple-950/40 to-slate-900 border border-slate-800 shadow-2xl relative overflow-hidden">
      <div class="relative z-10 max-w-3xl space-y-3">
        <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-purple-500/20 text-purple-300 border border-purple-500/30 text-xs font-semibold uppercase tracking-wider">
          🎯 Comprehensive 150-Question Technical Vault
        </div>
        <h2 class="text-3xl md:text-4xl font-extrabold text-white tracking-tight leading-tight">
          AI, Machine Learning, LLMs & Quant Interview Master Bank
        </h2>
        <p class="text-slate-300 text-sm md:text-base leading-relaxed">
          Curated collection of 150 real interview questions asked at Google, Meta, OpenAI, Anthropic, Jane Street, and Citadel. Answers are initially hidden for flashcard study. Reveal solutions one-by-one or toggle all answers at once. All formulas render with complete LaTeX mathematical typesetting.
        </p>
      </div>
    </div>

    <!-- Controls Bar -->
    <div class="flex flex-wrap items-center justify-between gap-4 bg-slate-900/60 p-4 rounded-xl border border-slate-800">
      <div class="relative flex-1 min-w-[260px] max-w-md">
        <input id="qSearchInput" type="text" placeholder="Search 150 questions (e.g. RoPE, AdamW, KV-cache, Monty Hall, L1)..."
               class="w-full bg-slate-950 border border-slate-700 text-xs text-white rounded-xl pl-9 pr-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-purple-500 placeholder-slate-500">
        <svg class="w-4 h-4 absolute left-3 top-3 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
      </div>

      <div class="flex items-center space-x-2 text-xs">
        <button onclick="revealAllAnswers()" class="px-3.5 py-1.5 rounded-lg bg-purple-600/30 hover:bg-purple-600 text-purple-300 hover:text-white border border-purple-500/40 font-semibold transition flex items-center gap-1.5">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
          <span>Reveal All Answers</span>
        </button>
        <button onclick="hideAllAnswers()" class="px-3.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold border border-slate-700 transition flex items-center gap-1.5">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l18 18"/></svg>
          <span>Hide All Answers</span>
        </button>
      </div>
    </div>

    <!-- Category Filters -->
    <div class="flex items-center flex-wrap gap-2 text-xs" id="categoryFilters">
      <button onclick="filterCategory('all')" class="px-3 py-1.5 rounded-lg font-semibold bg-purple-600 text-white q-cat-btn active" data-cat="all">All (150)</button>
      <button onclick="filterCategory('ml')" class="px-3 py-1.5 rounded-lg font-semibold bg-slate-900 text-slate-400 hover:text-white border border-slate-700 q-cat-btn" data-cat="ml">Classical ML (25)</button>
      <button onclick="filterCategory('dl')" class="px-3 py-1.5 rounded-lg font-semibold bg-slate-900 text-slate-400 hover:text-white border border-slate-700 q-cat-btn" data-cat="dl">Deep Learning (25)</button>
      <button onclick="filterCategory('genai_llm')" class="px-3 py-1.5 rounded-lg font-semibold bg-slate-900 text-slate-400 hover:text-white border border-slate-700 q-cat-btn" data-cat="genai_llm">Transformers & LLMs (25)</button>
      <button onclick="filterCategory('rag')" class="px-3 py-1.5 rounded-lg font-semibold bg-slate-900 text-slate-400 hover:text-white border border-slate-700 q-cat-btn" data-cat="rag">RAG & Vector Search (20)</button>
      <button onclick="filterCategory('metrics_data')" class="px-3 py-1.5 rounded-lg font-semibold bg-slate-900 text-slate-400 hover:text-white border border-slate-700 q-cat-btn" data-cat="metrics_data">Metrics & Preprocessing (20)</button>
      <button onclick="filterCategory('system_mlops')" class="px-3 py-1.5 rounded-lg font-semibold bg-slate-900 text-slate-400 hover:text-white border border-slate-700 q-cat-btn" data-cat="system_mlops">MLOps & System Design (20)</button>
      <button onclick="filterCategory('logic_prob')" class="px-3 py-1.5 rounded-lg font-semibold bg-slate-900 text-slate-400 hover:text-white border border-slate-700 q-cat-btn" data-cat="logic_prob">Logic & Probability (15)</button>
    </div>

    <!-- Questions Container -->
    <div id="questionsList" class="space-y-4"></div>
  </main>

  <footer class="border-t border-slate-800 py-6 text-center text-xs text-slate-500">
    Master AI/ML Technical Interview Question Vault &bull; 150 In-Depth Questions, Proofs & Solutions
  </footer>

  <script>
    const QUESTIONS = __QUESTIONS_JSON__;
    let currentCategory = "all";
    let searchQuery = "";
    let openQuestions = new Set();
    let solvedQuestions = new Set();

    function triggerMathRender(rootElement) {
      const target = rootElement || document.body;
      if (typeof renderMathInElement === 'function') {
        try {
          renderMathInElement(target, {
            delimiters: [
              { left: '$$', right: '$$', display: true },
              { left: '$', right: '$', display: false },
              { left: '\\(', right: '\\)', display: false },
              { left: '\\[', right: '\\]', display: true }
            ],
            throwOnError: false,
            errorColor: '#f43f5e'
          });
        } catch (e) {
          console.warn('KaTeX rendering error:', e);
        }
      } else {
        fallbackFormatFormulas(target);
      }
    }

    function fallbackFormatFormulas(target) {
      if (!target) return;
      const walker = document.createTreeWalker(target, NodeFilter.SHOW_TEXT, null, false);
      const nodesToReplace = [];
      let n;
      while (n = walker.nextNode()) {
        if (n.nodeValue && n.nodeValue.includes('$')) {
          nodesToReplace.push(n);
        }
      }
      nodesToReplace.forEach(node => {
        const parent = node.parentNode;
        if (!parent || parent.tagName === 'SCRIPT' || parent.tagName === 'STYLE') return;
        const original = node.nodeValue;
        const replaced = original.replace(/\\$([^\\$\\n]+?)\\$/g, function(_, eq) {
          let clean = eq
            .replace(/\\\\frac\\{([^}]+)\\}\\{([^}]+)\\}/g, '<span style="display:inline-flex;flex-direction:column;vertical-align:middle;text-align:center;font-size:0.9em;padding:0 2px;"><span style="border-bottom:1.5px solid #818cf8;padding:0 2px;">$1</span><span style="padding:0 2px;">$2</span></span>')
            .replace(/\\lambda/g, 'λ')
            .replace(/\\theta/g, 'θ')
            .replace(/\\sigma/g, 'σ')
            .replace(/\\mu/g, 'μ')
            .replace(/\\pi/g, 'π')
            .replace(/\\eta/g, 'η')
            .replace(/\\beta/g, 'β')
            .replace(/\\gamma/g, 'γ')
            .replace(/\\Omega/g, 'Ω')
            .replace(/\\min/g, 'min')
            .replace(/\\max/g, 'max')
            .replace(/\\sum/g, '∑')
            .replace(/\\partial/g, '∂')
            .replace(/\\le|\\leq/g, '≤')
            .replace(/\\ge|\\geq/g, '≥')
            .replace(/\\to/g, '→')
            .replace(/\\pm/g, '±')
            .replace(/\\neq/g, '≠')
            .replace(/\\cdot/g, '·')
            .replace(/\\in/g, '∈')
            .replace(/\\approx/g, '≈')
            .replace(/\\\\sqrt\\{([^}]+)\\}/g, '√($1)')
            .replace(/\\\\|/g, '‖')
            .replace(/\\^2/g, '²')
            .replace(/_\\{([^}]+)\\}/g, '<sub>$1</sub>')
            .replace(/_([a-zA-Z0-9])/g, '<sub>$1</sub>');
          return `<span class="math-fallback font-serif text-indigo-200">${clean}</span>`;
        });
        if (replaced !== original) {
          const span = document.createElement('span');
          span.innerHTML = replaced;
          parent.replaceChild(span, node);
        }
      });
    }

    function formatMarkdown(text) {
      if (!text) return "";
      
      // 1. Protect display math $$ ... $$ and inline math $ ... $
      const mathTokens = [];
      
      let tokenized = text.replace(/\\$\\$([\\s\\S]*?)\\$\\$/g, function(_, math) {
        const key = `@@@MATH_DISP_${mathTokens.length}@@@`;
        mathTokens.push({ type: 'display', code: math });
        return key;
      });

      tokenized = tokenized.replace(/\\$([^\\$\\n]+?)\\$/g, function(_, math) {
        const key = `@@@MATH_INL_${mathTokens.length}@@@`;
        mathTokens.push({ type: 'inline', code: math });
        return key;
      });

      // 2. Format standard Markdown safely
      let html = tokenized
        .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
        .replace(/\\*\\*(.*?)\\*\\*/g, '<strong class="text-white font-bold">$1</strong>')
        .replace(/\\*(.*?)\\*/g, '<em class="text-slate-300 italic">$1</em>')
        .replace(/`([^`]+)`/g, '<code class="px-1.5 py-0.5 rounded bg-slate-800 text-purple-300 text-xs font-mono">$1</code>')
        .replace(/\\n\\n/g, '<div class="my-2.5"></div>')
        .replace(/\\n- /g, '<br>&bull; ')
        .replace(/\\n/g, '<br>');

      // 3. Restore math expressions with renderable KaTeX delimiters
      html = html.replace(/@@@MATH_DISP_(\\d+)@@@/g, function(_, id) {
        const item = mathTokens[parseInt(id, 10)];
        return `<div class="katex-display-box formula-box text-center">$$${item.code}$$</div>`;
      });

      html = html.replace(/@@@MATH_INL_(\\d+)@@@/g, function(_, id) {
        const item = mathTokens[parseInt(id, 10)];
        return `<span class="katex-inline-formula">$${item.code}$</span>`;
      });

      return html;
    }

    function renderQuestions() {
      const container = document.getElementById("questionsList");
      if (!container) return;

      const filtered = QUESTIONS.filter(q => {
        if (currentCategory !== "all" && q.category !== currentCategory) return false;
        if (searchQuery.trim()) {
          const term = searchQuery.toLowerCase();
          const matchQ = q.question.toLowerCase().includes(term);
          const matchA = q.answer.toLowerCase().includes(term);
          const matchCat = q.category_label.toLowerCase().includes(term);
          const matchCompany = q.company_tags.some(c => c.toLowerCase().includes(term));
          return matchQ || matchA || matchCat || matchCompany;
        }
        return true;
      });

      if (filtered.length === 0) {
        container.innerHTML = `
          <div class="text-center py-16 bg-slate-900/50 rounded-2xl border border-slate-800 text-slate-400">
            <p class="text-base font-semibold">No questions matching your search filter.</p>
            <p class="text-xs mt-1 text-slate-500">Try searching for keywords like 'RoPE', 'AdamW', 'L1', 'Bayes', or 'KV-cache'.</p>
          </div>
        `;
        return;
      }

      let html = "";
      filtered.forEach((q, idx) => {
        const isOpen = openQuestions.has(q.id);
        const isSolved = solvedQuestions.has(q.id);
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
          <div class="bg-slate-900/90 border ${isSolved ? 'border-emerald-600/40' : 'border-slate-800'} rounded-2xl p-5 md:p-6 space-y-4 shadow-lg transition hover:border-slate-700">
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

              <div class="flex items-center space-x-2">
                <label class="flex items-center space-x-1.5 cursor-pointer text-xs text-slate-400 hover:text-white">
                  <input type="checkbox" onchange="toggleSolved('${q.id}')" ${isSolved ? 'checked' : ''}
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
            <div class="pt-1">
              <button onclick="toggleAnswer('${q.id}')" id="btn-${q.id}"
                      class="px-4 py-2 rounded-xl text-xs font-semibold flex items-center gap-2 transition ${isOpen ? 'bg-slate-800 text-slate-300 hover:text-white' : 'bg-purple-600 hover:bg-purple-500 text-white shadow-lg shadow-purple-600/20'}">
                <svg class="w-4 h-4 transform transition-transform ${isOpen ? 'rotate-180' : ''}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                </svg>
                <span>${isOpen ? 'Hide Detailed Answer' : '💡 Reveal Answer & Explanation'}</span>
              </button>
            </div>

            <!-- Answer Section (Hidden Initially) -->
            <div id="ans-${q.id}" class="${isOpen ? '' : 'hidden'} pt-2 space-y-4 border-t border-slate-800/80">
              <div class="bg-slate-950/80 p-5 rounded-xl border border-slate-800 text-slate-200 text-xs md:text-sm leading-relaxed space-y-2">
                ${formatMarkdown(q.answer)}
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
      triggerMathRender(container);
    }

    function toggleAnswer(id) {
      if (openQuestions.has(id)) {
        openQuestions.delete(id);
      } else {
        openQuestions.add(id);
        history.replaceState(null, '', '#q-' + id);
      }
      renderQuestions();
    }

    function revealAllAnswers() {
      QUESTIONS.forEach(q => openQuestions.add(q.id));
      renderQuestions();
    }

    function hideAllAnswers() {
      openQuestions.clear();
      renderQuestions();
    }

    function toggleSolved(id) {
      if (solvedQuestions.has(id)) {
        solvedQuestions.delete(id);
      } else {
        solvedQuestions.add(id);
      }
      renderQuestions();
    }

    function filterCategory(cat) {
      currentCategory = cat;
      document.querySelectorAll(".q-cat-btn").forEach(btn => {
        if (btn.dataset.cat === cat) {
          btn.className = "px-3 py-1.5 rounded-lg font-semibold bg-purple-600 text-white q-cat-btn active";
        } else {
          btn.className = "px-3 py-1.5 rounded-lg font-semibold bg-slate-900 text-slate-400 hover:text-white border border-slate-700 q-cat-btn";
        }
      });
      renderQuestions();
    }

    document.getElementById("qSearchInput").addEventListener("input", (e) => {
      searchQuery = e.target.value;
      renderQuestions();
    });

    function handleInitialRoute() {
      const hash = window.location.hash.replace(/^#[/]?/, '');
      if (hash) {
        const rawId = hash.replace(/^q-?/, '');
        const found = QUESTIONS.find((q, idx) => q.id === rawId || String(idx + 1) === rawId || q.id === `ml_${rawId.padStart(2, '0')}`);
        if (found) {
          openQuestions.add(found.id);
          renderQuestions();
          setTimeout(() => {
            const el = document.getElementById(`q-${found.id}`);
            if (el) {
              el.scrollIntoView({ behavior: 'smooth', block: 'center' });
              el.classList.add('ring-2', 'ring-purple-500');
              setTimeout(() => el.classList.remove('ring-2', 'ring-purple-500'), 3000);
            }
          }, 200);
        }
      }
    }

    window.addEventListener("DOMContentLoaded", () => {
      renderQuestions();
      handleInitialRoute();
    });
    window.addEventListener("hashchange", () => {
      handleInitialRoute();
    });
    renderQuestions();
    handleInitialRoute();
  </script>
</body>
</html>
"""

def build_standalone_interview_html():
    questions_json = json.dumps(INTERVIEW_QUESTIONS)
    html = HTML_TEMPLATE.replace("__QUESTIONS_JSON__", questions_json)
    with open("interview_questions.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated interview_questions.html successfully!")


def build_standalone_interview_markdown():
    md = "# Master AI, Machine Learning, Deep Learning & Quant Technical Interview Vault (150 Questions)\n\n"
    md += "A curated bank of 150 top-tier interview questions and hidden answers asked at Google, Meta, OpenAI, Anthropic, Jane Street, and Citadel.\n\n"
    md += "> **Tip**: In markdown readers supporting HTML5, answers are enclosed within `<details><summary>Click to Reveal Answer</summary>...</details>` so you can test your knowledge in flashcard mode!\n\n"
    md += "---\n\n"

    categories = [
        ("1. Classical Machine Learning & Statistical Foundations", "ml"),
        ("2. Deep Learning Foundations & Training Dynamics", "dl"),
        ("3. Transformers, Large Language Models (LLMs) & Generative AI", "genai_llm"),
        ("4. RAG, Embeddings & Vector Search", "rag"),
        ("5. Evaluation Metrics, Data Preprocessing & Statistical Testing", "metrics_data"),
        ("6. Production MLOps, System Design & Latency Optimization", "system_mlops"),
        ("7. Logical Brainteasers, Probability Puzzles & Quantitative Reasoning", "logic_prob")
    ]

    for title, cat_id in categories:
        md += f"## {title}\n\n"
        cat_questions = [q for q in INTERVIEW_QUESTIONS if q["category"] == cat_id]

        for idx, q in enumerate(cat_questions, 1):
            md += f"### Q{idx}. {q['question']}\n\n"
            md += f"- **Difficulty**: `{q['difficulty']}` | **Category**: `{q['category_label']}`\n"
            md += f"- **Target Companies**: {', '.join([f'`{c}`' for c in q['company_tags']])}\n\n"
            md += "<details>\n<summary><b>💡 Click to Reveal Complete Answer & Explanation</b></summary>\n\n"
            md += f"{q['answer']}\n\n"
            if q.get("tip"):
                md += f"> **⭐ Interviewer Evaluation Tip:** {q['tip']}\n\n"
            md += "</details>\n\n"
            md += "---\n\n"

    with open("interview_questions.md", "w", encoding="utf-8") as f:
        f.write(md)
    print("Generated interview_questions.md successfully!")


if __name__ == "__main__":
    build_standalone_interview_html()
    build_standalone_interview_markdown()
