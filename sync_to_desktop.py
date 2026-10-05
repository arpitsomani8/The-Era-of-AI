import os
import shutil

src_dir = r"C:\Users\arpit\.gemini\antigravity\brain\080ca9ea-8e4c-4526-9530-293b439a74c2"
dest_dir = r"C:\Users\arpit\Desktop\The Era of AI"

os.makedirs(dest_dir, exist_ok=True)

# 1. Generate clean directory route redirects
routes = {
    "interview": "Interview Vault",
    "papers": "Landmark Research Papers",
    "projects": "Production AI Case Studies",
    "syllabus": "Line-wise Master Syllabus",
    "mindmap": "Interactive Mind Map"
}

for route, title in routes.items():
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Redirecting to {title}...</title>
  <meta http-equiv="refresh" content="0; url=../index.html#{route}">
  <script>window.location.replace("../index.html#{route}");</script>
</head>
<body style="background:#0b0f19;color:#94a3b8;font-family:system-ui,sans-serif;display:flex;align-items:center;justify-content:center;height:100vh;margin:0;">
  <p>Loading {title}...</p>
</body>
</html>
"""
    route_src = os.path.join(src_dir, route)
    os.makedirs(route_src, exist_ok=True)
    with open(os.path.join(route_src, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_content)

    route_dest = os.path.join(dest_dir, route)
    os.makedirs(route_dest, exist_ok=True)
    with open(os.path.join(route_dest, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Configured route: /{route}/ -> index.html#{route}")

# 2. Synchronize main web assets
files = [
    "ai_ml_dl_master_mindmap.html",
    "index.html",
    "interview_questions.html",
    "interview_questions.md",
    "game_changing_ai_research_papers.html",
    "production_ai_case_studies.html",
    "production_ai_case_studies.md",
    "ai_ml_dl_master_mindmap.md",
    "ai_ml_dl_master_research_papers.md",
    "interview_questions_data.py",
    "papers_data.py",
    "projects_data.py",
    "build_encyclopedia.py",
    "generate_all.py",
    "build_standalone_interview.py",
    "build_standalone_papers.py",
    "build_standalone_projects.py",
    "GITHUB_DEPLOYMENT_GUIDE.md",
    "concept.html",
    "all_concepts.json",
    "all_concepts.py",
    "concepts_math.py",
    "concepts_data_prep.py",
    "concepts_ml.py",
    "concepts_eval.py",
    "concepts_dl.py",
    "concepts_dl_arch.py",
    "concepts_genai.py",
    "concepts_mlops.py",
    "build_standalone_concept.py"
]

# Copy concept folder
src_concept = os.path.join(src_dir, "concept")
dest_concept = os.path.join(dest_dir, "concept")
if os.path.exists(src_concept):
    shutil.copytree(src_concept, dest_concept, dirs_exist_ok=True)
    print("Copied concept/ directory!")

for f in files:
    src_file = os.path.join(src_dir, f)
    dest_file = os.path.join(dest_dir, f)
    if os.path.exists(src_file):
        shutil.copy2(src_file, dest_file)
        print(f"Copied: {f}")

# 3. Synchronize KaTeX offline font & script assets
src_katex = os.path.join(src_dir, "katex")
dest_katex = os.path.join(dest_dir, "katex")
if os.path.exists(src_katex):
    shutil.copytree(src_katex, dest_katex, dirs_exist_ok=True)
    print("Copied katex directory with all fonts and scripts!")

print("All files & URL route endpoints synchronized to Desktop successfully!")
