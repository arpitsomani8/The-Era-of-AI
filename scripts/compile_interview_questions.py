"""
Compiler script to assemble the complete 150 questions into interview_questions_data.py
"""

from questions_cat1_ml import CAT1_QUESTIONS
from questions_cat2_dl import CAT2_QUESTIONS
from questions_cat3_llm import CAT3_QUESTIONS
from questions_cat4_rag import CAT4_QUESTIONS
from questions_cat5_metrics import CAT5_QUESTIONS
from questions_cat6_system import CAT6_QUESTIONS
from questions_cat7_logic import CAT7_QUESTIONS
import io

ALL_QUESTIONS = (
    CAT1_QUESTIONS +
    CAT2_QUESTIONS +
    CAT3_QUESTIONS +
    CAT4_QUESTIONS +
    CAT5_QUESTIONS +
    CAT6_QUESTIONS +
    CAT7_QUESTIONS
)

print(f"Total compiled questions: {len(ALL_QUESTIONS)}")

with io.open("interview_questions_data.py", "w", encoding="utf-8") as f:
    f.write('"""\nMaster AI/ML/DL/LLM/System Design/Quant Interview Questions & Answers\n')
    f.write('150 top-tier interview questions with hidden answers and expert explanations.\n"""\n\n')
    f.write(f"INTERVIEW_QUESTIONS = {repr(ALL_QUESTIONS)}\n")

print("Generated interview_questions_data.py successfully!")
