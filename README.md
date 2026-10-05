# The Era of AI — Master Knowledge Graph & Portal

An interactive web application exploring the universe of Artificial Intelligence, Machine Learning, Deep Learning, Generative AI, and MLOps. Built with **React 18**, **Vite**, **Tailwind CSS**, and **KaTeX**.

---

## 🌟 Key Features

1. **Interactive Mind Map (`/mindmap`)**: 2D knowledge graph with smooth pan/zoom, domain filters, cross-domain interlinks, and deep node inspection with mathematical formulas, intuition, and real-world examples.
2. **Line-wise Master Syllabus (`/syllabus`)**: 34 comprehensive syllabus modules across Math, Data Preprocessing, Classical ML, Evaluation, Deep Learning, and Transformers, with KaTeX formulas, expand/collapse, and PDF export.
3. **Landmark Research Papers Hub (`/papers`)**: 22 seminal AI papers with problem breakdowns, breakthrough innovations, key equations, and direct arXiv access.
4. **Enterprise Case Studies (`/projects`)**: Production architectures, system diagrams, metrics, and copyable implementation code.
5. **Technical Interview Vault (`/interview`)**: 150+ categorized interview questions with difficulty tiers, company tags, comprehensive answers, and gotcha tips.
6. **Core AI Concept Encyclopedia (`/concepts`)**: 170 individual core concepts with instant search, category navigation, and shareable deep links.
7. **4 Appearance Themes**: Default Midnight Slate, Pure OLED Dark, Bright Day, and Brushed Metallic Green (with persistence in `localStorage`).
8. **Universal Search (`⌘K` / `Ctrl+K`)**: Instant search across all 170 concepts, 150 questions, 22 papers, and case studies.

---

## 📁 Project Directory Structure

```
The Era of AI/
├── src/                             # Core React application
│   ├── components/                  # Navbar, NodeInspector, SearchModal, ThemeSwitcher, KaTeXRenderer
│   ├── context/                     # ThemeContext (4 theme modes)
│   ├── data/                        # JSON datasets (allNodes, concepts, papers, projects, interview questions)
│   ├── pages/                       # MindMap, Syllabus, Papers, Projects, Interview, Concepts
│   ├── App.jsx                      # Router & App layout
│   ├── index.css                    # Tailwind directives & multi-theme styles
│   └── main.jsx                     # Vite React entry point
│
├── public/                          # Static assets & backwards-compatible URL redirects
│   ├── concept/
│   ├── interview/
│   ├── mindmap/
│   ├── papers/
│   ├── projects/
│   └── syllabus/
│
├── scripts/                         # Python data pipeline & generator tools
│   ├── data_sources/                # Raw concepts, paper archives, question categorizers
│   ├── build_encyclopedia.py
│   ├── build_interview_bank.py
│   ├── fetch_latest_papers.py
│   └── generate_all.py
│
├── legacy_exports/                  # Archived standalone static HTML & Markdown files
│   ├── ai_ml_dl_master_mindmap.html
│   ├── interview_questions.html
│   ├── game_changing_ai_research_papers.html
│   ├── production_ai_case_studies.html
│   └── concept.html
│
├── index.html                       # Vite HTML template
├── vite.config.js                   # Vite configuration
├── tailwind.config.js               # Tailwind CSS theme configuration
├── postcss.config.js                # PostCSS configuration
├── package.json                     # Dependencies & scripts
└── .gitignore                       # Ignored build & node artifacts
```

---

## 🚀 Getting Started

### Prerequisites
- Node.js (v18 or higher)
- npm

### Installation & Running Locally

```bash
# 1. Install dependencies
npm install

# 2. Start the local development server
npm run dev

# 3. Build for production
npm run build
```

Open your browser at: **`http://localhost:3000`**
