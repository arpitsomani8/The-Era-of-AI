import json

MODE_IMPUTE_UPDATE = {
    "def": "Mode Imputation replaces missing categorical values with the most frequent category. Alternatively, creating an explicit 'None' or 'Unknown' category treats missingness as an informative feature state, preventing distortion of real-world business semantics.",
    "definition": "Mode Imputation replaces missing categorical values with the most frequent category. Alternatively, creating an explicit 'None' or 'Unknown' category treats missingness as an informative feature state, preventing distortion of real-world business semantics.",
    "formula": "$$\\hat{x}_i = \\text{Mode}(X) = \\arg\\max_{c \\in \\mathcal{C}} \\sum_{j \\in \\mathcal{O}} \\mathbb{I}(x_j = c), \\quad \\hat{x}_i = \\text{'None'}, \\quad \\mathbf{v}_{\\text{OOV}} = [0, 0, \\dots, 0]$$",
    "formula_explanation": "",
    "logic": "Categories cannot be averaged. Mode imputation works when missingness is tiny (< 5%) and a single class dominates. When missingness denotes absence (e.g. no VIP status, no allergies), creating an explicit 'None' category creates dedicated one-hot feature columns without amplifying class imbalance.",
    "example": "Customer VIP tier: Rather than mode-imputing 'Gold' to users who never signed up for rewards, replacing NaN with 'None' creates an explicit one-hot feature (VIP_None = 1), enabling the model to learn specific churn patterns for non-members.",
    "simple_summary": "Categories cannot be averaged: use Mode imputation when missingness is under 5% and one category dominates; use an explicit 'None' category when missingness carries meaning (no allergy, no VIP tier). In production, configure encoders with handle_unknown='ignore' to prevent unseen category crashes.",
    "core_terms": [
        {
            "term": "Mode Imputation",
            "what_is_it": "• Replaces missing categorical entries with the single most frequent category in that column: x̂ = argmax_c Count(c).\n• Best reserved strictly for low missingness rates (< 5%) where a single category overwhelmingly dominates the distribution (e.g. 95% of users in 'Seattle').",
            "analogy": "A popularity contest: if a ballot has a blank presidential vote, assuming they voted for the candidate who won by a 95% landslide.",
            "why_it_matters": "Provides a zero-parameter baseline, but risks heavily amplifying class imbalance and destroying genuine minority class patterns."
        },
        {
            "term": "Explicit Missing Category ('None' / 'Unknown')",
            "what_is_it": "• The practice of replacing NaN with an explicit string label ('None', 'Unknown', or 'Missing'), treating missingness as a legitimate independent state.\n• When passed into One-Hot Encoding, it creates a dedicated feature column (e.g. VIP_Tier_None = 1), enabling models to learn specific weights for missingness.",
            "analogy": "Marking 'No Allergies' on a medical clipboard rather than leaving the box blank or assuming the patient has the most common allergy.",
            "why_it_matters": "Essential when missingness is semantically meaningful—such as a user having no secondary phone, no allergies, or no luxury subscription."
        },
        {
            "term": "Unseen Category Handling (Out-of-Vocabulary)",
            "what_is_it": "• A production failure mode where live inference data presents a new categorical level that never existed in the training set (e.g. 'Paris' appears after training on NY, London, Tokyo).\n• Prevented by configuring OneHotEncoder with handle_unknown='ignore' (outputs all zeros) or consolidating rare training categories into an 'Other' bucket.",
            "analogy": "A postal worker encountering a foreign country name: instead of halting the entire mail facility, placing the letter into an 'International / Other' processing bin.",
            "why_it_matters": "Prevents production web servers from throwing catastrophic 500 runtime ValueErrors when new users register with novel attributes."
        }
    ],
    "types_header": "Categorical Imputation & Production Encoders",
    "types_badge": "Encoding Strategy",
    "quick_types": [
        {
            "type": "Dominant Mode Imputation",
            "definition": "Fills missing values with the most frequent category. Recommended strictly when missingness is < 5% and one class heavily dominates.",
            "looks_like": "df['city'].fillna(df['city'].mode()[0])"
        },
        {
            "type": "Explicit 'None' Category",
            "definition": "Replaces NaN with 'None' or 'Unknown' when missingness represents absence (e.g. no secondary driver, no food allergies).",
            "looks_like": "df['tier'].fillna('None') → dedicated column"
        },
        {
            "type": "Rare Class 'Other' Binning",
            "definition": "Consolidates low-frequency categories (< 1% frequency) into a shared 'Other' bucket to manage high cardinality.",
            "looks_like": "df['job'].replace(rare_jobs, 'Other')"
        },
        {
            "type": "handle_unknown='ignore'",
            "definition": "Scikit-Learn encoder setting that yields an all-zero vector for unseen test categories rather than crashing with a ValueError.",
            "looks_like": "OneHotEncoder(handle_unknown='ignore')"
        },
        {
            "type": "Not Applicable vs. Not Provided",
            "definition": "Differentiating structural inapplicability (e.g. pregnancy status for males) from user refusal to answer a survey question.",
            "looks_like": "'N/A' (structural) vs 'Refused' (informative)"
        }
    ],
    "symbol_guide": [
        {
            "symbol": "x̂_i",
            "meaning": "Imputed Category",
            "plain_english": "The assigned label replacing a missing categorical observation"
        },
        {
            "symbol": "Mode(X)",
            "meaning": "Most Frequent Value",
            "plain_english": "The category appearing with highest empirical frequency in training data"
        },
        {
            "symbol": "C",
            "meaning": "Permissible Category Set",
            "plain_english": "The unique collection of known categorical levels observed during training"
        },
        {
            "symbol": "c",
            "meaning": "Candidate Class Level",
            "plain_english": "Individual categorical option evaluated in the empirical frequency sum"
        },
        {
            "symbol": "'None'",
            "meaning": "Explicit Category Token",
            "plain_english": "Dedicated string assigned to represent missingness as an active feature state"
        },
        {
            "symbol": "v_OOV",
            "meaning": "Out-of-Vocabulary Vector",
            "plain_english": "All-zero encoding vector generated when an unknown category is ignored"
        }
    ],
    "numerical_example": "Imputing Customer VIP Tiers:\nRaw Training Column: ['Silver', 'Gold', NaN, 'Gold', 'Gold', NaN, 'Platinum'] (N = 7 customers)\n\n1. Strategy A: Mode Imputation (The Popularity Contest):\n   • Observed Counts: Gold (3), Silver (1), Platinum (1)\n   • Mode = 'Gold'\n   • Imputing NaN with 'Gold' assigns 2 non-VIP customers free Gold perks! Artificially inflates Gold from 60% to 71% of observed rows.\n\n2. Strategy B: Explicit 'None' Category (The Semantic Gold Standard):\n   • Replace NaN with 'None': ['Silver', 'Gold', 'None', 'Gold', 'Gold', 'None', 'Platinum']\n   • Unique Categories = 4: {'Gold', 'Silver', 'Platinum', 'None'}\n\n3. One-Hot Vector for Customer #3 (Originally NaN):\n   • Vector: [Gold=0, Silver=0, Platinum=0, None=1]\n   • Model now explicitly learns that 'None' users have a 3x higher churn rate than 'Gold' users!",
    "pitfalls": "Common Pitfall: Blindly using mode imputation on columns where missingness denotes absence (e.g. Allergy_Type or Secondary_Phone). This causes severe semantic errors (e.g. diagnosing patient with peanut allergies simply because peanut was the most common allergy). Use explicit 'None' or 'Missing' labels instead.",
    "core_logic": "Why this matters: Missingness in categorical data is frequently Missing Not At Random (MNAR). Encoding missingness as an explicit category preserves non-random signal, whereas forcing missing entries into the mode distorts natural class balances and blinds models to user dropout behavior.",
    "architectural_logic": "In production feature stores, categorical encoders must decouple training vocabulary from runtime inference. Encoders configured with handle_unknown='ignore' output robust zero-vectors for novel tokens, while upstream data contracts map unseen categories into designated 'Other' buckets.",
    "connected_logic": [
        {
            "title": "Class Imbalance Amplification: The Distortion of Dominant Labels",
            "content": "• Applying mode imputation to moderately balanced columns (e.g. Payment: 55% Card, 45% Cash) disproportionately inflates the majority label.\n• This introduces artificial class imbalance into training distributions, causing classification loss functions to over-predict the majority class."
        },
        {
            "title": "Semantic Inversion: When Missingness Denotes Ineligibility",
            "content": "• In credit scoring and insurance underwriting, missing values frequently denote the absence of a liability (e.g. no previous bankruptcies, no speeding tickets).\n• Imputing the mode would falsely brand safe applicants with infractions, whereas explicit 'None' encoding allows models to reward clean records."
        },
        {
            "title": "The Production 500 Out-of-Vocabulary Crash",
            "content": "• One-Hot encoders trained without unknown-category guards throw fatal runtime exceptions when receiving novel inference tokens (e.g. a new car manufacturer).\n• Production pipelines must enforce either frequency thresholding ('Other' bin) or silent zero-vector encoding (handle_unknown='ignore') to guarantee high-availability API uptime."
        },
        {
            "title": "High-Cardinality Target Encoding with Missing Bins",
            "content": "• In high-cardinality features (e.g. Zip codes, merchant IDs), one-hot encoding creates thousands of sparse columns.\n• Target encoders replace categories with conditional target means, where an explicit 'Missing' bin receives a smoothed prior mean to regularize sparse predictions."
        }
    ],
    "key_takeaways": [
        "Core Philosophy: Categories cannot be averaged; use Mode for dominant low-missingness data, and explicit 'None' when missingness carries meaning.",
        "Semantic Protection: Imputing the mode on optional fields (allergies, VIP tiers) falsely assigns traits to customers who simply opted out.",
        "Production Guardrail: Always configure Scikit-Learn OneHotEncoder with handle_unknown='ignore' to prevent unseen production categories from crashing servers.",
        "Cardinality Management: Group rare categories (< 1% frequency) into an 'Other' bin to bound feature dimension growth."
    ],
    "definition_bullets": [
        "Mode Imputation: Replacing missing categorical observations with the most frequently observed category in the training dataset.",
        "Explicit Missing Category: Assigning a dedicated token ('None' or 'Unknown') to treat missingness as an informative, distinct feature level."
    ]
}

def update_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    found = False
    for item in data:
        if item.get('id') == 'concept_mode_impute':
            item.update(MODE_IMPUTE_UPDATE)
            found = True
            break
            
    if not found:
        print(f"Warning: concept_mode_impute not found in {filepath}")
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
        if item.get('id') == 'concept_mode_impute':
            item.update(MODE_IMPUTE_UPDATE)
            break
            
    new_content = '"""\nConcepts Database: Data Preparation & Exploration (22 Concepts)\n"""\n\nDATA_CONCEPTS = ' + json.dumps(mod.DATA_CONCEPTS, indent=4, ensure_ascii=False) + '\n'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Successfully updated {filepath}")

update_concepts_data_prep()
