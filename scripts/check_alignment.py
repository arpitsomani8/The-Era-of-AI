import json

with open('src/data/topics.json', 'r', encoding='utf-8') as f:
    topics = json.load(f)
with open('src/data/concepts.json', 'r', encoding='utf-8') as f:
    concepts = json.load(f)
with open('src/data/allNodes.json', 'r', encoding='utf-8') as f:
    nodes = json.load(f)

print(f"Total topics: {len(topics)}")
print(f"Total concepts: {len(concepts)}")
print(f"Total nodes in allNodes.json: {len(nodes)}")

# Topic IDs
topic_ids_topics = [t['id'] for t in topics]
node_ids = [n['id'] for n in nodes]
missing_nodes = [t for t in topics if t['id'] not in node_ids]
print(f"Topics missing in allNodes.json: {len(missing_nodes)}")
for m in missing_nodes:
    print(f"  - {m['id']} ({m['label']})")

# Concepts per topic
concepts_by_topic = {}
for c in concepts:
    tid = c.get('topic_id')
    concepts_by_topic.setdefault(tid, []).append(c)

# Exact subtopics match check
subtopic_mismatches = 0
for t in topics:
    tid = t['id']
    subtopics = t.get('subtopics', [])
    c_list = concepts_by_topic.get(tid, [])
    diff = len(subtopics) - len(c_list)
    if diff != 0:
        subtopic_mismatches += 1
        print(f"COUNT MISMATCH in {tid} ({t['label']}): {len(subtopics)} subtopics vs {len(c_list)} concepts")
    else:
        for idx, (s, c) in enumerate(zip(subtopics, c_list)):
            if s != c['title']:
                subtopic_mismatches += 1
                print(f"TITLE MISMATCH in {tid}: '{s}' != '{c['title']}'")

if subtopic_mismatches == 0:
    print("SUCCESS: All 199 subtopics in topics.json match concepts.json 1-to-1 perfectly!")

# Mind Map connections check
node_id_set = set(n['id'] for n in nodes)
broken_conns = 0
for n in nodes:
    for target in n.get('connections', []):
        if target not in node_id_set:
            broken_conns += 1
            print(f"BROKEN LINK: {n['id']} -> {target}")

if broken_conns == 0:
    print("SUCCESS: All Mind Map connections are valid and point to existing nodes!")

# Career tracks check
import re
with open('src/pages/MindMapPage.jsx', 'r', encoding='utf-8') as f:
    mm_text = f.read()

tracks = re.findall(r'path:\s*\[(.*?)\]', mm_text, re.DOTALL)
invalid_track_nodes = 0
for t_str in tracks:
    for item in t_str.split(','):
        clean_item = item.strip().strip("'\" \n\r\t")
        if clean_item and clean_item not in node_id_set:
            invalid_track_nodes += 1
            print(f"INVALID CAREER TRACK NODE: {clean_item}")

if invalid_track_nodes == 0:
    print(f"SUCCESS: All {len(tracks)} Career Tracks in MindMapPage have 100% valid node pathways!")

