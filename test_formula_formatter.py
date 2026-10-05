import re
from build_encyclopedia import TOPICS
from papers_data import PAPERS

def format_formula_to_latex(formula_str):
    if not formula_str:
        return ""
    if "$$" in formula_str or "$" in formula_str:
        return formula_str

    parts = formula_str.split(" | ")
    res_parts = []
    for p in parts:
        text = p.strip()
        label = ""
        colon_idx = text.find(": ")
        if 0 < colon_idx < 30:
            label = text[:colon_idx + 1] + " "
            text = text[colon_idx + 2:].strip()

        latex = text
        latex = latex.replace("λ", r"\lambda ")
        latex = latex.replace("θ", r"\theta ")
        latex = latex.replace("σ^2", r"\sigma^2 ")
        latex = latex.replace("σ²", r"\sigma^2 ")
        latex = latex.replace("σ", r"\sigma ")
        latex = latex.replace("μ", r"\mu ")
        latex = latex.replace("π", r"\pi ")
        latex = latex.replace("η", r"\eta ")
        latex = latex.replace("β_1", r"\beta_1 ")
        latex = latex.replace("β_2", r"\beta_2 ")
        latex = latex.replace("β_t", r"\beta_t ")
        latex = latex.replace("β", r"\beta ")
        latex = latex.replace("γ", r"\gamma ")
        latex = latex.replace("Ω", r"\Omega ")
        latex = latex.replace("∇_w", r"\nabla_w ")
        latex = latex.replace("∇", r"\nabla ")
        latex = latex.replace("∈", r"\in ")
        latex = latex.replace("≈", r"\approx ")
        latex = latex.replace("≠", r"\neq ")
        latex = latex.replace("≤", r"\le ")
        latex = latex.replace("≥", r"\ge ")
        latex = latex.replace("->", r"\to ")
        latex = latex.replace("·", r"\cdot ")
        latex = latex.replace("∑", r"\sum ")
        latex = re.sub(r'√([a-zA-Z0-9_]+)', r'\\sqrt{\1}', latex)
        latex = re.sub(r'√\((.*?)\)', r'\\sqrt{\1}', latex)
        latex = latex.replace("||", r"\|")
        latex = latex.replace(":=", r"\leftarrow ")
        
        # Fractions [A] / B
        latex = re.sub(r'\[([^\]]+)\]\s*/\s*([a-zA-Z0-9_\(\)]+)', r'\\frac{\1}{\2}', latex)
        latex = re.sub(r'\(([^)]+)\)\s*/\s*([a-zA-Z0-9_\(\)]+)', r'\\frac{\1}{\2}', latex)

        res_parts.append(f"{label}$${latex}$$")
    return "<br>".join(res_parts)

print("Testing Encyclopedia formulas:")
for t in TOPICS[:5]:
    raw = t.get("formula", "")
    print("TOPIC:", t["id"])
    print("RAW:", raw)
    print("LATEX:", format_formula_to_latex(raw))
    print("-" * 50)

print("Testing Papers formulas:")
for p in PAPERS[:5]:
    raw = p.get("formula", "")
    print("PAPER:", p["id"])
    print("RAW:", raw)
    print("LATEX:", format_formula_to_latex(raw))
    print("-" * 50)
