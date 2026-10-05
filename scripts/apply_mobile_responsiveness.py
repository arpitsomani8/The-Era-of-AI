"""
Script to apply comprehensive mobile-responsive styling, touch-gesture panning & pinch-to-zoom,
and bottom-sheet mobile drawer to generate_all.py, interview_questions.html, production_ai_case_studies.html,
and game_changing_ai_research_papers.html.
"""

import io

def update_generate_all():
    with io.open("generate_all.py", "r", encoding="utf-8") as f:
        code = f.read()

    # 1. Add no-scrollbar and mobile responsive styles in <style>
    mobile_css = """
    /* Mobile Responsive Optimizations */
    .no-scrollbar::-webkit-scrollbar {
      display: none;
    }
    .no-scrollbar {
      -ms-overflow-style: none;
      scrollbar-width: none;
    }
    @media (max-width: 640px) {
      .mobile-bottom-sheet {
        position: fixed !important;
        bottom: 0 !important;
        top: auto !important;
        left: 0 !important;
        right: 0 !important;
        width: 100% !important;
        max-width: 100% !important;
        max-height: 85vh !important;
        border-radius: 1.5rem 1.5rem 0 0 !important;
        transform: translateY(100%) !important;
      }
      .mobile-bottom-sheet.inspector-open {
        transform: translateY(0) !important;
      }
      .mobile-tab-text {
        font-size: 11px !important;
      }
    }
    @media (min-width: 641px) {
      .inspector-open {
        transform: translateX(0) !important;
      }
    }
    """

    if ".no-scrollbar" not in code:
        code = code.replace("</style>", f"{mobile_css}</style>")

    # 2. Make Navigation Bar horizontally scrollable with touch momentum
    old_nav_tabs = '<div id="navTabs" class="flex items-center bg-slate-900/80 p-1 rounded-xl border border-slate-700/60 shadow-inner">'
    new_nav_tabs = '<div id="navTabs" class="flex items-center overflow-x-auto no-scrollbar max-w-full space-x-1 bg-slate-900/80 p-1 rounded-xl border border-slate-700/60 shadow-inner flex-nowrap shrink-0">'
    
    if old_nav_tabs in code:
        code = code.replace(old_nav_tabs, new_nav_tabs)

    # Make each button shrink-0 and whitespace-nowrap
    code = code.replace('class="px-3.5 py-1.5 rounded-lg text-xs font-semibold transition flex items-center gap-1.5 bg-indigo-600 text-white shadow"',
                        'class="px-3 py-1.5 rounded-lg text-xs font-semibold transition flex items-center gap-1.5 bg-indigo-600 text-white shadow whitespace-nowrap shrink-0"')
    code = code.replace('class="px-3.5 py-1.5 rounded-lg text-xs font-semibold text-slate-300 hover:text-white transition flex items-center gap-1.5"',
                        'class="px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-300 hover:text-white transition flex items-center gap-1.5 whitespace-nowrap shrink-0"')
    code = code.replace('class="px-3.5 py-1.5 rounded-lg text-xs font-semibold text-slate-300 hover:text-white transition flex items-center gap-1.5 relative"',
                        'class="px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-300 hover:text-white transition flex items-center gap-1.5 relative whitespace-nowrap shrink-0"')

    # 3. Make Category Filters horizontally scrollable on mobile
    old_cat_filter = '<div class="flex items-center flex-wrap gap-1.5 text-xs">'
    new_cat_filter = '<div class="flex items-center overflow-x-auto no-scrollbar max-w-full space-x-1.5 pb-1 text-xs flex-nowrap">'
    code = code.replace(old_cat_filter, new_cat_filter)

    # 4. Update Inspector Drawer class to support mobile bottom sheet
    old_inspector = '<div id="inspectorPanel" class="absolute top-4 right-4 w-96 max-w-[calc(100vw-2rem)] max-h-[calc(100%-2rem)] bg-[var(--card,#1e293b)] border border-[var(--border,#334155)] rounded-2xl shadow-2xl p-5 overflow-y-auto flex flex-col gap-4 transform translate-x-full transition-transform duration-300 ease-out z-30">'
    new_inspector = """<div id="inspectorPanel" class="mobile-bottom-sheet absolute top-4 right-4 w-96 max-w-[calc(100vw-2rem)] max-h-[calc(100%-2rem)] bg-[var(--card,#1e293b)] border border-[var(--border,#334155)] rounded-2xl shadow-2xl p-5 overflow-y-auto flex flex-col gap-4 transform translate-x-full transition-transform duration-300 ease-out z-30">
      <div class="w-12 h-1.5 bg-slate-700 rounded-full mx-auto sm:hidden -mt-1 mb-1"></div>"""
    
    if old_inspector in code:
        code = code.replace(old_inspector, new_inspector)

    # Update openInspector and closeInspector JS to use class inspector-open
    old_open_insp = 'inspector.classList.remove("translate-x-full");'
    new_open_insp = 'inspector.classList.remove("translate-x-full"); inspector.classList.add("inspector-open");'
    if old_open_insp in code:
        code = code.replace(old_open_insp, new_open_insp)

    old_close_insp = 'inspector.classList.add("translate-x-full");'
    new_close_insp = 'inspector.classList.add("translate-x-full"); inspector.classList.remove("inspector-open");'
    if old_close_insp in code:
        code = code.replace(old_close_insp, new_close_insp)

    # 5. Add Touch Event Handlers for Mobile Touch Panning & Pinch-to-Zoom
    touch_support_js = """
    // Mobile Touch Gesture Support (Single-finger Pan & Two-finger Pinch Zoom)
    let lastTouchDist = 0;
    viewport.addEventListener("touchstart", (e) => {
      if (e.target.closest(".node-group")) return;
      if (e.touches.length === 1) {
        state.isDragging = true;
        state.startX = e.touches[0].clientX - state.panX;
        state.startY = e.touches[0].clientY - state.panY;
      } else if (e.touches.length === 2) {
        lastTouchDist = Math.hypot(
          e.touches[0].clientX - e.touches[1].clientX,
          e.touches[0].clientY - e.touches[1].clientY
        );
      }
    }, { passive: true });

    window.addEventListener("touchmove", (e) => {
      if (currentMainTab !== "mindmap") return;
      if (e.touches.length === 1 && state.isDragging) {
        state.panX = e.touches[0].clientX - state.startX;
        state.panY = e.touches[0].clientY - state.startY;
        updateTransform();
      } else if (e.touches.length === 2) {
        const dist = Math.hypot(
          e.touches[0].clientX - e.touches[1].clientX,
          e.touches[0].clientY - e.touches[1].clientY
        );
        if (lastTouchDist > 0) {
          const delta = (dist - lastTouchDist) * 0.006;
          zoom(delta);
        }
        lastTouchDist = dist;
      }
    }, { passive: true });

    window.addEventListener("touchend", () => {
      state.isDragging = false;
      lastTouchDist = 0;
    });
    """

    if "// Mobile Touch Gesture Support" not in code:
        code = code.replace('viewport.addEventListener("mousedown", (e) => {',
                            touch_support_js + '\n    viewport.addEventListener("mousedown", (e) => {')

    with io.open("generate_all.py", "w", encoding="utf-8") as f:
        f.write(code)

    print("Updated generate_all.py with mobile touch gestures and responsive design!")


def update_standalone_files():
    # Update interview_questions.html with mobile scrollbar and padding
    with io.open("interview_questions.html", "r", encoding="utf-8") as f:
        html = f.read()

    # Make categories scrollable horizontally on mobile
    html = html.replace(
        '<div class="flex items-center flex-wrap gap-2 text-xs" id="categoryFilters">',
        '<div class="flex items-center overflow-x-auto no-scrollbar max-w-full space-x-2 pb-1 text-xs flex-nowrap" id="categoryFilters">'
    )
    html = html.replace('class="px-3 py-1.5 rounded-lg font-semibold', 'class="px-3 py-1.5 rounded-lg font-semibold shrink-0 whitespace-nowrap')
    
    with io.open("interview_questions.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Updated interview_questions.html with mobile-friendly filters!")

    # Update production_ai_case_studies.html
    with io.open("production_ai_case_studies.html", "r", encoding="utf-8") as f:
        html = f.read()

    html = html.replace(
        '<div class="flex items-center flex-wrap gap-2 text-xs">',
        '<div class="flex items-center overflow-x-auto no-scrollbar max-w-full space-x-2 pb-1 text-xs flex-nowrap">'
    )
    html = html.replace('class="px-3 py-1.5 rounded-lg font-semibold', 'class="px-3 py-1.5 rounded-lg font-semibold shrink-0 whitespace-nowrap')

    with io.open("production_ai_case_studies.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Updated production_ai_case_studies.html with mobile-friendly filters!")


if __name__ == "__main__":
    update_generate_all()
    update_standalone_files()
