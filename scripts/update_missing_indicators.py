import json

MISSING_INDICATORS_UPDATE = {
    "def": "Missingness Indicator Flags create binary indicator columns ($m_i \\in \\{0, 1\\}$) alongside imputed features to explicitly record whether original values were missing, preserving the critical predictive signal of non-random missingness (MNAR).",
    "definition": "Missingness Indicator Flags create binary indicator columns ($m_i \\in \\{0, 1\\}$) alongside imputed features to explicitly record whether original values were missing, preserving the critical predictive signal of non-random missingness (MNAR).",
    "formula": "$$m_i = \\mathbb{I}(x_i \\in \\text{NaN}) = \\begin{cases} 1 & \\text{if } x_i \\text{ was missing} \\\\ 0 & \\text{if } x_i \\text{ was observed} \\end{cases}, \\quad \\hat{x}_i = \\begin{cases} x_i & \\text{if } m_i = 0 \\\\ \\tilde{x} & \\text{if } m_i = 1 \\end{cases}$$",
    "formula_explanation": "",
    "logic": "Imputation fills numerical gaps so algorithms don't crash, but it destroys the reason why data was missing. Adding a missingness indicator retains the unobserved human or clinical intent (Missing Not at Random), letting models decouple baseline numbers from missingness penalties.",
    "example": "Emergency ICU admission: Troponin heart enzyme test is missing because the doctor never ordered it. Imputing median 0.5 ng/mL prevents pipeline crashes, while Troponin_is_na = 1 informs the model that acute cardiac injury was not clinically suspected.",
    "simple_summary": "Imputation fills the gap so models can run; Missingness Indicators preserve why the gap existed in the first place. In real life, missing data is rarely random (MNAR)—it often signals deliberate human intent, clinical judgment, or equipment status. Creating a binary flag (1 = missing, 0 = present) ensures models don't lose that critical signal.",
    "core_terms": [
        {
            "term": "Missingness Indicator Flag (Binary Null Tracker)",
            "what_is_it": "• A companion binary feature (0 or 1) generated alongside an incomplete column to mark whether an observation was originally missing before imputation.\n• While standard imputation substitutes a plausible number (e.g. median) so models can compute, the flag explicitly preserves the information that a measurement was absent.",
            "analogy": "A medical chart marked with a neon sticker reading 'Lab test not ordered', even after an assistant writes in an estimated average baseline score.",
            "why_it_matters": "Allows downstream algorithms to learn separate mathematical weights for normal observed measurements versus the event of a missing record."
        },
        {
            "term": "MNAR (Missing Not at Random)",
            "what_is_it": "• A statistical missingness mechanism where the probability of a value being missing is directly driven by the unobserved value itself or human intent.\n• Common in voluntary surveys (e.g. high-earners skipping salary questions) or medical charts (tests ordered only for sick patients); standard imputation alone introduces severe bias on MNAR data.",
            "analogy": "In a survey asking 'How many times have you been caught speeding?', chronic speeders are substantially more inclined to skip the question than law-abiding drivers.",
            "why_it_matters": "Provides the theoretical foundation for indicator flags: missingness itself is a potent predictor that must not be erased."
        },
        {
            "term": "The Dimensionality Trap (Feature Bloat)",
            "what_is_it": "• The practical anti-pattern of creating binary indicators for every single column with nulls, dangerously doubling feature dimensions in wide datasets.\n• When a feature has only 2 missing values out of 100,000 rows (0.002%), the indicator column has near-zero variance, adding computational noise without predictive power.",
            "analogy": "Installing an automated emergency fire siren on a warehouse shelf just because one speck of dust fell on a single package.",
            "why_it_matters": "Establishes production threshold rules: only generate indicators for columns with substantial missingness (> 5%–10%) or confirmed domain-level human intent."
        }
    ],
    "types_header": "Indicator Flag Generation & Threshold Strategies",
    "types_badge": "Feature Engineering",
    "quick_types": [
        {
            "type": "Pandas .isna().astype(int)",
            "definition": "Direct Pandas approach creating an integer flag column before applying imputation fill methods.",
            "looks_like": "df['income_is_na'] = df['income'].isna().astype(int)"
        },
        {
            "type": "sklearn MissingIndicator",
            "definition": "Dedicated Scikit-Learn transformer that identifies missing positions and outputs a binary matrix.",
            "looks_like": "MissingIndicator(features='missing-only').fit_transform(X)"
        },
        {
            "type": "SimpleImputer(add_indicator=True)",
            "definition": "Unified Scikit-Learn parameter that imputes values and automatically appends missing indicator columns.",
            "looks_like": "SimpleImputer(strategy='median', add_indicator=True)"
        },
        {
            "type": "Substantial Threshold Rule (> 5%)",
            "definition": "Pragmatic filter that creates flags only for features exceeding a minimum missingness percentage to avoid bloat.",
            "looks_like": "cols = [c for c in X if X[c].isna().mean() >= 0.05]"
        },
        {
            "type": "Domain-Intent Behavioral Flags",
            "definition": "Manual indicators assigned to optional form inputs where omissions reveal customer preferences or opt-outs.",
            "looks_like": "df['skipped_salary'] = df['salary'].isna().astype(int)"
        }
    ],
    "symbol_guide": [
        {
            "symbol": "m_i",
            "meaning": "Missingness Indicator",
            "plain_english": "Binary flag (0 or 1) indicating whether entry i was missing or observed"
        },
        {
            "symbol": "x_i",
            "meaning": "Original Feature Value",
            "plain_english": "The raw input measurement or NaN prior to preprocessing"
        },
        {
            "symbol": "I(...)",
            "meaning": "Indicator Function",
            "plain_english": "Evaluates to 1 when the condition inside is true, and 0 otherwise"
        },
        {
            "symbol": "x̂_i",
            "meaning": "Final Feature Value",
            "plain_english": "Completed numerical value passed to downstream model inputs"
        },
        {
            "symbol": "x̃ (x_tilde)",
            "meaning": "Baseline Imputation Value",
            "plain_english": "Median, mean, or predicted multivariate estimate filling the null cell"
        }
    ],
    "numerical_example": "Emergency Cardiology Triage: Troponin Enzyme Test (Normal < 0.04 ng/mL, Suspected Infarction > 0.40 ng/mL):\nThree incoming patients arrive at emergency triage:\n• Patient A (Chest pain, tested): Troponin x₁ = 0.03 ng/mL\n• Patient B (Sprained wrist, test not ordered): Troponin x₂ = NaN\n• Patient C (Severe chest pain, tested): Troponin x₃ = 1.85 ng/mL\nObserved median replacement value: x̃ = (0.03 + 1.85) / 2 = 0.94 ng/mL.\n\n1. Generate Missingness Indicators (m_i):\n   • Patient A: m₁ = 0 (observed)\n   • Patient B: m₂ = 1 (missing / test omitted)\n   • Patient C: m₃ = 0 (observed)\n\n2. Impute Missing Feature Values (x̂_i):\n   • Patient A: x̂₁ = 0.03 ng/mL\n   • Patient B: x̂₂ = 0.94 ng/mL (median substitute prevents algorithm crash)\n   • Patient C: x̂₃ = 1.85 ng/mL\n\n3. Model Matrix Representation:\n   • Row A: [Troponin = 0.03, Troponin_is_na = 0]\n   • Row B: [Troponin = 0.94, Troponin_is_na = 1]\n   • Row C: [Troponin = 1.85, Troponin_is_na = 0]\n\nOutcome: In a linear model y = w₁·x̂ + w₂·m, the model assigns Patient B score: w₁·(0.94) + w₂·(1). By learning a strong negative weight for w₂, the model offsets the artificial 0.94 median spike, correctly predicting that Patient B does not have an acute myocardial infarction.",
    "pitfalls": "Common Pitfall: Creating missingness indicators after running imputation. If df.fillna() is executed before indicator generation, all null values become valid numbers and .isna() returns all zeros, permanently destroying the missingness footprint. Furthermore, avoid flagging columns with negligible missingness (< 0.1%) to prevent near-zero variance feature bloat.",
    "core_logic": "Why this matters: Data missingness is rarely accidental noise. When data is Missing Not at Random (MNAR), the fact that an entry is missing carries more predictive weight than the underlying number itself. Combining imputation with an indicator flag equips algorithms with both numerical continuity and behavioral intent.",
    "architectural_logic": "In enterprise machine learning systems, MissingIndicator is incorporated inside Scikit-Learn Pipeline or Feature Store definitions using features='missing-only', fitted exclusively on training splits to prevent data leakage and guarantee consistent feature schemas during online inference.",
    "connected_logic": [
        {
            "title": "Credit Underwriting & Voluntary Disclosures",
            "content": "• In digital lending, borrowers who deliberately omit optional fields (e.g. secondary collateral, employer contact) exhibit statistically higher default probabilities.\n• Pairing median imputation with an indicator flag allows tree models (XGBoost, LightGBM) to split directly on the omission flag, separating high-risk applicants from verified borrowers."
        },
        {
            "title": "ICU Telemetry & Clinical Ordering Bias",
            "content": "• Diagnostic tests like arterial blood gases or lactate levels are only ordered when an intensivist suspects imminent sepsis or respiratory failure (systematic MNAR).\n• An indicator flag explicitly captures clinical suspicion, preventing downstream survival models from confusing unmonitored stable patients with critically monitored patients."
        },
        {
            "title": "Preventing Inference Schema Mismatch & Data Leakage",
            "content": "• Generating indicators dynamically per batch causes inference crashes if a production batch has no missing values in a flagged training column (or vice versa).\n• Setting MissingIndicator(features='missing-only') on training splits locks the column schema, ensuring offline pipelines and online REST APIs maintain identical feature vector shapes."
        },
        {
            "title": "Tree-Based Native Splitting vs. Linear Models",
            "content": "• Modern gradient boosting libraries (LightGBM, XGBoost, CatBoost) natively handle NaNs by routing missing values to the optimal split child without needing manual flags.\n• Linear regressions, support vector machines, and neural networks lack native NaN routing; they strictly require explicit indicator flags alongside imputed values to learn missingness penalties."
        }
    ],
    "key_takeaways": [
        "Dual-Signal Power: Imputation fills the numerical gap so models don't crash; indicator flags preserve why the gap existed (MNAR intent).",
        "Execution Sequence: Always generate indicator flags before imputing baseline values, otherwise the missingness trail is permanently erased.",
        "Dimensionality Pruning: Restrict indicator creation to columns with substantial missingness (> 5%–10%) or domain-relevant opt-outs to avoid feature bloat.",
        "Pipeline Safety: Fit MissingIndicator strictly on training folds to prevent target leakage and guarantee immutable feature dimensions during inference."
    ],
    "definition_bullets": [
        "Missingness Indicator Flag: A binary boolean feature (0 or 1) recording whether an input value was null prior to imputation.",
        "MNAR (Missing Not at Random): A missingness mechanism where omission correlates directly with unobserved outcomes or user behavior."
    ]
}

def update_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    found = False
    for item in data:
        if item.get('id') == 'concept_missing_indicators':
            item.update(MISSING_INDICATORS_UPDATE)
            found = True
            break
            
    if not found:
        print(f"Warning: concept_missing_indicators not found in {filepath}")
        return False
        
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Successfully updated {filepath}")
    return True

# Update concepts.json and all_concepts.json
update_json_file('src/data/concepts.json')
update_json_file('scripts/data_sources/all_concepts.json')

# Update concepts_data_prep.py
def update_concepts_data_prep():
    filepath = 'scripts/data_sources/concepts_data_prep.py'
    import importlib.util
    spec = importlib.util.spec_from_file_location("concepts_data_prep", filepath)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    
    for item in mod.DATA_CONCEPTS:
        if item.get('id') == 'concept_missing_indicators':
            item.update(MISSING_INDICATORS_UPDATE)
            break
            
    new_content = '"""\nConcepts Database: Data Preparation & Exploration (22 Concepts)\n"""\n\nDATA_CONCEPTS = ' + json.dumps(mod.DATA_CONCEPTS, indent=4, ensure_ascii=False) + '\n'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Successfully updated {filepath}")

update_concepts_data_prep()
