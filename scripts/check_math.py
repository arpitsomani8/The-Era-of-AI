import re
import interview_questions_data

questions = interview_questions_data.INTERVIEW_QUESTIONS
print(f"Total questions: {len(questions)}")
math_inlines = []
math_displays = []

for q in questions:
    text = q['answer'] + ' ' + (q.get('tip') or '')
    displays = re.findall(r'\$\$([\s\S]*?)\$\$', text)
    # Remove displays to find inlines cleanly
    no_disp = re.sub(r'\$\$[\s\S]*?\$\$', '', text)
    inlines = re.findall(r'\$([^\$\n]+?)\$', no_disp)
    math_inlines.extend(inlines)
    math_displays.extend(displays)

print(f"Found {len(math_inlines)} inline math expressions, {len(math_displays)} display math expressions")
print("Top 10 inline samples:")
for s in math_inlines[:10]:
    print(" -", s)
print("Top 5 display samples:")
for s in math_displays[:5]:
    print(" -", s.strip())
