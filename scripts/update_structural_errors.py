import json

STRUCTURAL_ERRORS_UPDATE = {
    "def": "Structural errors are inconsistencies in how data is written, formatted, or categorized across rows, even though the raw information is present. Resolving them ensures consistent categories, valid numerical data types, and reliable machine learning predictions.",
    "definition": "Structural errors are inconsistencies in how data is written, formatted, or categorized across rows, even though the raw information is present. Resolving them ensures consistent categories, valid numerical data types, and reliable machine learning predictions.",
    "formula": "$$x_{\\text{clean}} = \\text{Map}\\Big(\\text{RegexReplace}\\big(\\text{Strip}(\\text{Lower}(x_{\\text{raw}})), \\text{pattern}, \\text{repl}\\big)\\Big), \\quad z = \\frac{x_{\\text{clean}} - \\mu}{\\sigma}$$",
    "formula_explanation": "",
    "logic": "Inconsistent casing and typos trigger Cardinality Explosion in one-hot encoding, while formatted glyphs ($1,250) force numeric columns into object strings. Systematic canonicalization and unit harmonization restore statistical integrity.",
    "example": "Standardizing customer data: Transforming casing (' jaipur ' -> 'Jaipur'), stripping currency glyphs ('$75,000.50' -> 75000.50 float), and resolving date ambiguity ('04/05/2023' -> '2023-04-05T00:00:00Z' ISO 8601).",
    "simple_summary": "Structural errors happen when data formatting, naming, or units are inconsistent. Typos explode categorical cardinality, while currency symbols turn numbers into strings. Cleaning whitespace, canonicalizing categories, and enforcing ISO schemas protects models from silent corruption.",
    "core_terms": [
        {
            "term": "Structural Errors",
            "what_is_it": "• Inconsistencies in how data is formatted, capitalized, typed, or represented across rows, even though the raw information is present.\n• Arises when merging disparate databases, ingesting web forms, or accepting manual user input without strict validation.",
            "analogy": "A filing cabinet where the same client is filed under 'Smith, John', 'john smith', and 'J. Smith Inc' across three different drawers.",
            "why_it_matters": "Inconsistent entries artificially fragment statistical samples, causing machine learning algorithms to treat identical concepts as distinct categories."
        },
        {
            "term": "Cardinality Explosion",
            "what_is_it": "• An artificial ballooning of unique category counts caused by typos, casing variations ('USA', 'U.S.A.', 'us'), and trailing whitespace.\n• When passed into one-hot encoding, a simple 3-class feature explodes into dozens of sparse columns, triggering the Curse of Dimensionality and severe overfitting.",
            "analogy": "A survey with 3 answer options ('Yes', 'No', 'Maybe') where sloppy text input creates 15 different variations, fragmenting respondent counts.",
            "why_it_matters": "Dilutes training signals, inflates memory consumption, and severely degrades tree-based models and linear classifiers."
        },
        {
            "term": "Type & Unit Desynchronization",
            "what_is_it": "• When numeric values are imported as string objects due to formatting glyphs ('$1,250.00', '15%') or mixed measurement units (miles vs. km).\n• Blocks numerical gradient computation and distorts normalization scales unless symbols are stripped and units harmonized.",
            "analogy": "The 1999 NASA Mars Climate Orbiter disaster: a $125M spacecraft crashed into Mars because one engineering team logged thrust in imperial pounds-force while another expected metric Newtons.",
            "why_it_matters": "Blindly forcing conversion with pd.to_numeric(errors='coerce') silently erases valid data into missing NaN values."
        }
    ],
    "types_header": "Structural Error Varieties & Remediation",
    "types_badge": "Data Sanitation",
    "quick_types": [
        {
            "type": "Casing & Typos",
            "definition": "Inconsistent capitalizations and misspellings ('jaipur', 'Jaipur', 'JAIPUR'). Solved via str.lower() and dictionary mapping.",
            "looks_like": "['M', 'Male', 'man'] → 'male'"
        },
        {
            "type": "Invisible Whitespace",
            "definition": "Trailing spaces, tabs, and non-breaking spaces (\\u00a0) causing lookup failures. Solved via str.strip().",
            "looks_like": "'Yes ' vs 'Yes' → str.strip()"
        },
        {
            "type": "Currency & Punctuation Glyphs",
            "definition": "Dollar signs and commas forcing numeric columns into object strings. Solved via regex replacement before float casting.",
            "looks_like": "'$1,250.00' → regex sub → 1250.00 (float)"
        },
        {
            "type": "Date Format Ambiguity",
            "definition": "Regional day/month swaps (DD/MM vs MM/DD) and missing timezones. Solved via explicit ISO 8601 parsing.",
            "looks_like": "'04/05/2023' → explicit format='%Y-%m-%d'"
        },
        {
            "type": "Delimiter Collisions",
            "definition": "Unescaped commas in CSV text shifting downstream columns to the right. Solved via quotechar parsing or TSV formats.",
            "looks_like": "Unquoted comma splits 1 column into 2"
        }
    ],
    "symbol_guide": [
        {
            "symbol": "x_raw",
            "meaning": "Raw Text Value",
            "plain_english": "The uncleaned input string containing whitespace, casing, or glyphs"
        },
        {
            "symbol": "x_clean",
            "meaning": "Canonical Value",
            "plain_english": "Standardized output mapped to a consistent domain representation"
        },
        {
            "symbol": "Strip()",
            "meaning": "Whitespace Trimming",
            "plain_english": "Function removing leading, trailing, and non-breaking whitespace"
        },
        {
            "symbol": "Lower()",
            "meaning": "Case Normalization",
            "plain_english": "Function converting characters to uniform lowercase or title case"
        },
        {
            "symbol": "RegexReplace",
            "meaning": "Pattern Substitution",
            "plain_english": "Regular expression stripping currency symbols, commas, or escaped delimiters"
        },
        {
            "symbol": "Map()",
            "meaning": "Canonical Mapping",
            "plain_english": "Dictionary mapping known typos, aliases, and abbreviations to a target key"
        }
    ],
    "numerical_example": "Cleaning a Messy Salary & Location Record:\nRaw Row: {'City': ' jaipur ', 'Salary': '$75,000.50', 'StartDate': '04/05/2023'}\n\n1. Whitespace & Text Standardization:\n   • ' jaipur '.strip().title() --> 'Jaipur' (Resolves casing and invisible whitespace).\n\n2. Currency String to Numeric Float Conversion:\n   • Raw: '$75,000.50' (Imported by Pandas as string object)\n   • Regex: re.sub(r'[$,]', '', '$75,000.50') --> '75000.50'\n   • Type Cast: float('75000.50') --> 75000.50 (Enables gradient and mean calculations).\n\n3. Date Parsing & Disambiguation:\n   • Ambiguity: Is 04/05/2023 April 5th (US) or May 4th (Intl)?\n   • Parsing: pd.to_datetime('04/05/2023', format='%m/%d/%Y', utc=True) --> '2023-04-05T00:00:00Z' (Canonical ISO 8601 timestamp).",
    "pitfalls": "Common Pitfall: Blindly calling pd.to_numeric(df['col'], errors='coerce'). Any string with a dollar sign, comma, or percentage is immediately converted into NaN. Always strip formatting glyphs via regex before coercing types to prevent silent data loss.",
    "core_logic": "Why this matters: Machine learning models assume homogeneous feature representations. Casing typos trigger high-cardinality overfitting in one-hot encoders, while unparsed string numbers completely disable gradient descent and loss optimization.",
    "architectural_logic": "In enterprise ML architectures, structural error prevention is shifted left using schema contracts (Pydantic / Great Expectations) at ingestion. In data warehouses, automated dbt tests validate categorical uniqueness and ISO date formats before features enter feature stores.",
    "connected_logic": [
        {
            "title": "The Silent NaN Trap of Naive Coercion",
            "content": "• Calling pd.to_numeric(df['price'], errors='coerce') blindly replaces any string containing currency signs or commas with NaN.\n• This silently destroys valid observations and inflates missing-data ratios, turning a simple formatting problem into an artificial imputation crisis."
        },
        {
            "title": "Time-Travel Data Leakage via Timezone Drift",
            "content": "• Merging international sensor logs without explicit UTC standardization causes records from Tokyo (+9h) and New York (-5h) to mix chronological order.\n• In time-series forecasting, this introduces temporal data leakage—allowing models to train on future records when predicting the past."
        },
        {
            "title": "Feature Normalization Distortion & Skew",
            "content": "• Failing to harmonize measurement units (e.g. mixing grams with kilograms or Celsius with Fahrenheit) severely distorts population mean μ and variance σ².\n• Downstream Z-score standardizers and distance-based algorithms (KNN, K-Means, SVM) produce completely warped cluster boundaries and weight updates."
        },
        {
            "title": "Schema Enforcement & Pydantic Validation in Production",
            "content": "• Modern ML inference pipelines prevent structural errors by enforcing runtime data contracts with Pydantic or Great Expectations.\n• Incoming JSON payloads are validated against strict types, enums, and regex bounds before reaching neural network inference layers."
        }
    ],
    "key_takeaways": [
        "Core Definition: Structural errors occur when data is present but corrupted by formatting, casing, whitespace, or unit inconsistencies.",
        "Cardinality Danger: Typos and casing explode unique category counts, triggering dimensionality disasters in one-hot encoding.",
        "Silent NaN Risk: Never use blind coercion (errors='coerce') without regex-stripping currency symbols and commas first.",
        "Production Shield: Modern data pipelines enforce schemas at ingestion using Pydantic, Great Expectations, and ISO 8601 standards."
    ],
    "definition_bullets": [
        "Structural Errors: Inconsistencies in data formatting, naming, and types that distort categorical cardinality and numeric computation.",
        "Canonicalization: The process of mapping messy real-world variations and abbreviations into a standardized, agreed-upon format."
    ]
}

def update_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    found = False
    for item in data:
        if item.get('id') == 'concept_structural_errors':
            item.update(STRUCTURAL_ERRORS_UPDATE)
            found = True
            break
            
    if not found:
        print(f"Warning: concept_structural_errors not found in {filepath}")
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
        if item.get('id') == 'concept_structural_errors':
            item.update(STRUCTURAL_ERRORS_UPDATE)
            break
            
    new_content = '"""\nConcepts Database: Data Preparation & Exploration (22 Concepts)\n"""\n\nDATA_CONCEPTS = ' + json.dumps(mod.DATA_CONCEPTS, indent=4, ensure_ascii=False) + '\n'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Successfully updated {filepath}")

update_concepts_data_prep()
