# scripts/audit_site.py
import os
import glob
import json
import re

print("=== 1. AUDITING ROUTES & INTERNAL LINKS ===")
jsx_files = glob.glob('src/**/*.jsx', recursive=True)
valid_routes = ['/', '/mindmap', '/syllabus', '/papers', '/projects', '/case-studies', '/interview', '/concepts', '/concept', '/playgrounds', '/playground']

links = []
for f in jsx_files:
    with open(f, 'r', encoding='utf-8') as fp:
        content = fp.read()
        for m in re.finditer(r'to=[\'"]([^\'"]+)[\'"]', content):
            links.append((f, m.group(1)))
        for m in re.finditer(r'navigate\([\'"]([^\'"]+)[\'"]\)', content):
            links.append((f, m.group(1)))
        for m in re.finditer(r'link:\s*[\'"]([^\'"]+)[\'"]', content):
            links.append((f, m.group(1)))

print(f"Total links found: {len(links)}")
broken_links = []
for src_f, l in links:
    base = l.split('?')[0].split('#')[0]
    if base.startswith('http') or base.startswith('mailto'):
        continue
    if base not in valid_routes:
        broken_links.append((src_f, l))

if broken_links:
    print(f"[WARN] FOUND {len(broken_links)} POTENTIALLY INVALID LINKS:")
    for f, l in broken_links:
        print(f"  {l} in {os.path.basename(f)}")
else:
    print("[OK] All internal routes match valid routes in App.jsx!")

print("\n=== 2. AUDITING DATA CROSS-REFERENCES ===")
# Check concepts
with open('src/data/concepts.json', 'r', encoding='utf-8') as f:
    concepts = json.load(f)
concept_ids = set(c.get('id') for c in concepts)
print(f"Total concepts: {len(concepts)}, unique IDs: {len(concept_ids)}")
if len(concepts) != len(concept_ids):
    print("⚠️ Duplicate concept IDs detected!")

# Check topics
with open('src/data/topics.json', 'r', encoding='utf-8') as f:
    topics = json.load(f)
topic_ids = set(t.get('id') for t in topics)
print(f"Total topics: {len(topics)}, unique IDs: {len(topic_ids)}")

# Check nodes
with open('src/data/allNodes.json', 'r', encoding='utf-8') as f:
    nodes = json.load(f)
node_ids = set(n.get('id') for n in nodes)
print(f"Total mindmap nodes: {len(nodes)}, unique IDs: {len(node_ids)}")

# Check papers
with open('src/data/papers.json', 'r', encoding='utf-8') as f:
    papers = json.load(f)
paper_ids = set(p.get('id') for p in papers)
print(f"Total papers: {len(papers)}, unique IDs: {len(paper_ids)}")

# Check interview questions
with open('src/data/interviewQuestions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)
q_ids = set(q.get('id') for q in questions)
print(f"Total interview questions: {len(questions)}, unique IDs: {len(q_ids)}")
if len(questions) != len(q_ids):
    print(f"[WARN] Duplicate question IDs detected! {len(questions)} items vs {len(q_ids)} unique IDs")

# Check if all concept topic_ids exist in topics.json
missing_topics = set()
for c in concepts:
    tid = c.get('topic_id')
    if tid and tid not in topic_ids:
        missing_topics.add(tid)
if missing_topics:
    print(f"[WARN] Concepts reference non-existent topic_ids: {missing_topics}")
else:
    print("[OK] All concept topic_ids exist in topics.json!")

# Check if node topic references exist
missing_node_topics = set()
for n in nodes:
    tids = n.get('topic_ids', [])
    for tid in tids:
        if tid not in topic_ids:
            missing_node_topics.add(tid)
if missing_node_topics:
    print(f"[WARN] MindMap nodes reference non-existent topic_ids: {missing_node_topics}")
else:
    print("[OK] All node topic references exist in topics.json!")

print("\n=== 3. AUDITING LOOKUP TABLES & CROSSLINKS ===")
with open('src/utils/conceptLookup.js', 'r', encoding='utf-8') as f:
    js_lines = f.readlines()

for idx, line in enumerate(js_lines):
    m = re.search(r':\s*"([^"]+)"', line)
    if m:
        cid = m.group(1)
        if cid not in concept_ids:
            print(f"[WARN] conceptLookup.js line {idx+1}: '{cid}' not found in concepts.json! Line: {line.strip()}")

# Check crossLinks.json
with open('src/data/crossLinks.json', 'r', encoding='utf-8') as f:
    crosslinks = json.load(f)

bad_source = [cl for cl in crosslinks if cl.get('from') not in node_ids]
bad_target = [cl for cl in crosslinks if cl.get('to') not in node_ids]
if bad_source or bad_target:
    print(f"[WARN] crossLinks has invalid node references: from {bad_source}, to {bad_target}")
else:
    print(f"[OK] All {len(crosslinks)} crossLinks connect valid mindmap nodes!")

# Check projects.json
with open('src/data/projects.json', 'r', encoding='utf-8') as f:
    projects = json.load(f)
print(f"[OK] {len(projects)} case study projects loaded.")

# Check CAREER_TRACKS in MindMapPage.jsx
with open('src/pages/MindMapPage.jsx', 'r', encoding='utf-8') as f:
    mmp_code = f.read()

paths = re.findall(r'path:\s*\[([^\]]+)\]', mmp_code)
bad_track_nodes = []
for p in paths:
    for it in [x.strip().strip("'\"") for x in p.split(',')]:
        if it and it not in node_ids:
            bad_track_nodes.append(it)

if bad_track_nodes:
    print(f"[WARN] MindMap CAREER_TRACKS contains invalid node IDs: {bad_track_nodes}")
else:
    print("[OK] All MindMap CAREER_TRACKS node IDs exist in allNodes.json!")

print("\n=== 4. AUDITING PUBLIC ASSETS & METADATA ===")
public_files = glob.glob('public/**/*', recursive=True)
print(f"Public files count: {len(public_files)}")
for p in public_files:
    if os.path.isfile(p):
        print(f"  {os.path.relpath(p, 'public')} ({os.path.getsize(p)} bytes)")

print("\n=== 5. CHECKING COMPONENT IMPORTS IN JSX ===")
all_jsx = glob.glob('src/**/*.jsx', recursive=True) + glob.glob('src/**/*.js', recursive=True)
import_errors = []
for f in all_jsx:
    with open(f, 'r', encoding='utf-8') as fp:
        lines = fp.readlines()
        for idx, line in enumerate(lines):
            # check import ... from '...'
            m = re.search(r'import\s+.*\s+from\s+[\'"]([^\'"]+)[\'"]', line)
            if m:
                path = m.group(1)
                if path.startswith('.'):
                    # relative path
                    dirpath = os.path.dirname(f)
                    target = os.path.normpath(os.path.join(dirpath, path))
                    # Check if file exists with .jsx, .js, .json, or index.js/jsx
                    exists = False
                    for ext in ['', '.jsx', '.js', '.json', '/index.js', '/index.jsx']:
                        if os.path.exists(target + ext):
                            exists = True
                            break
                    if not exists:
                        import_errors.append((f, idx + 1, path))

if import_errors:
    print(f"[WARN] Found {len(import_errors)} unresolved relative imports:")
    for f, line_no, imp in import_errors:
        print(f"  {os.path.relpath(f, 'src')}:{line_no} -> {imp}")
else:
    print(f"[OK] All relative imports across {len(all_jsx)} JS/JSX files resolve cleanly!")

print("\n=== 6. CHECKING FOR STALE HARDCODED NUMBERS IN USER-FACING CODE ===")
stale_findings = []
stale_patterns = ['170', '150+', '180+', '22 landmark', '22+', '41 node', '41 domain', '41-node', '34 module', '34 curriculum', '34+ module', '7 tracks']

for f in all_jsx:
    with open(f, 'r', encoding='utf-8') as fp:
        lines = fp.readlines()
    for idx, l in enumerate(lines):
        for pat in stale_patterns:
            if pat in l.lower():
                # Ignore coordinate/styling
                if not any(k in l for k in ['x=', 'y=', 'width=', 'height=', 'min-w-', '1706.03762', 'board states']):
                    stale_findings.append((f, idx + 1, pat, l.strip()))

if stale_findings:
    print(f"[WARN] Found {len(stale_findings)} potential stale number references:")
    for f, lno, pat, content in stale_findings:
        print(f"  {os.path.relpath(f, 'src')}:{lno} ({pat}) -> {content}")
else:
    print("[OK] Zero stale hardcoded numbers found across all UI files!")

print("\nAudit completed.")
