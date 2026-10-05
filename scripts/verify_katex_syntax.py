import re
import interview_questions_data

questions = interview_questions_data.INTERVIEW_QUESTIONS

errors = []
for q in questions:
    text = q['answer'] + ' ' + (q.get('tip') or '')
    
    # Check for unmatched $
    # Remove escaped \$ or code blocks first
    cleaned = re.sub(r'```[\s\S]*?```', '', text)
    cleaned = re.sub(r'`[^`]+`', '', cleaned)
    cleaned = cleaned.replace(r'\$', '')
    
    dollar_count = cleaned.count('$')
    if dollar_count % 2 != 0:
        errors.append(f"Odd number of dollar signs ({dollar_count}) in question {q['id']}: {q['question'][:50]}")

print(f"Total syntax check errors: {len(errors)}")
for e in errors[:10]:
    print(" -", e)
