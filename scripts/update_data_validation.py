import json

DATA_VALIDATION_UPDATE = {
    "def": "Data Type Validation ensures each column holds the correct primitive and contextual data type, while Formatting Consistency guarantees uniform syntax, regex patterns, and physical boundary constraints across all records.",
    "definition": "Data Type Validation ensures each column holds the correct primitive and contextual data type, while Formatting Consistency guarantees uniform syntax, regex patterns, and physical boundary constraints across all records.",
    "formula": "$$\\text{Valid}(x) = \\mathbb{I}\\Big(\\text{Type}(x) = T \\; \\wedge \\; x \\in [\\text{min}_C, \\text{max}_C] \\; \\wedge \\; \\text{RegexMatch}(x, \\mathcal{P}) \\; \\wedge \\; x \\in \\mathcal{S}_{\\text{domain}}\\Big)$$",
    "formula_explanation": "",
    "logic": "A value can match the expected primitive type but still be physically invalid (-5 is an integer, but not an age). Contextual typing preserves leading zeros on identifiers, while downcasting float64 to float32 prevents GPU memory crashes.",
    "example": "Customer payload validation: Ensuring zip codes preserve leading zeros ('07030' as string, not 7030 int), age satisfies 0 <= age <= 120, discount satisfies 0.0 <= discount <= 1.0, and timestamps conform to ISO 8601.",
    "simple_summary": "Type validation ensures columns have the right datatypes, while formatting consistency enforces uniform patterns. Identifiers like zip codes must stay strings to preserve leading zeros, and downcasting float64 to float32 cuts memory in half to avoid GPU OOM crashes.",
    "core_terms": [
        {
            "term": "Data Type Validation & Formatting Consistency",
            "what_is_it": "• Data Type Validation ensures every column holds the correct data type, while Formatting Consistency guarantees uniform syntax across all records.\n• Acts as a dual gatekeeper: preventing corrupted text strings ('twenty-five') in numerical columns and enforcing consistent conventions across dates and categories.",
            "analogy": "A passport control officer checking both that your document is a legitimate passport (type validation) and that the date format follows international standards (formatting consistency).",
            "why_it_matters": "Guarantees that downstream matrix operations, loss calculations, and neural activations receive valid, computable inputs."
        },
        {
            "term": "The Identifier Trap (Contextual Typing)",
            "what_is_it": "• The critical distinction between primitive machine storage types and contextual domain semantics.\n• Numeric identifiers like Zip codes ('07030'), phone numbers, and Social Security numbers are categorical labels—storing them as integers silently strips leading zeros and destroys data.",
            "analogy": "Writing down a phone number: you would never calculate the average of two phone numbers or add them together; treating them as numbers instead of text strings leads to instant data loss.",
            "why_it_matters": "Protects geographical routing, customer identification, and database joins from silent numeric truncation."
        },
        {
            "term": "Boundary & Domain Constraints",
            "what_is_it": "• Validation rules that check whether a syntactically correct data type adheres to realistic physical boundaries.\n• Catches values that are technically valid types but domain-impossible (e.g. Age = -5, Blood Pressure = 950, Discount = 1.45).",
            "analogy": "A thermostat set to 500°F: 500 is a valid number, but it is physically absurd for a living room temperature.",
            "why_it_matters": "Stops extreme garbage values from poisoning loss gradients and distorting distribution parameters."
        }
    ],
    "types_header": "Data Contract Layers & Failure Modes",
    "types_badge": "Schema Governance",
    "quick_types": [
        {
            "type": "Primitive Storage Downcasting",
            "definition": "Downcasting 64-bit defaults to float32 or int16. Slashes memory footprint by 50-75% to prevent GPU OOM crashes.",
            "looks_like": "df['price'] = df['price'].astype('float32')"
        },
        {
            "type": "Leading-Zero Identifiers",
            "definition": "Mandating categorical string types for Zip codes, SSNs, and phone numbers to prevent silent zero truncation.",
            "looks_like": "Zip: 07030 as str, NOT int 7030"
        },
        {
            "type": "Range & Boundary Asserts",
            "definition": "Enforcing physical domain boundaries (e.g. 0 <= Age <= 120, 0.0 <= Probability <= 1.0) on numerical columns.",
            "looks_like": "Assert: 0 <= df['age'] <= 120"
        },
        {
            "type": "ISO 8601 Standard Time",
            "definition": "Mandating uniform UTC ISO 8601 timestamps (YYYY-MM-DDTHH:MM:SSZ) to eliminate international date ambiguity.",
            "looks_like": "'2026-10-10T01:30:00Z' (UTC Standard)"
        },
        {
            "type": "Categorical Domain Enums",
            "definition": "Restricting categorical fields to a strict set of pre-approved values, rejecting unexpected or misspelled tokens.",
            "looks_like": "Status ∈ {'active', 'churned', 'paused'}"
        }
    ],
    "symbol_guide": [
        {
            "symbol": "Valid(x)",
            "meaning": "Boolean Validity Indicator",
            "plain_english": "Returns 1 if observation passes all contract assertions, 0 if rejected"
        },
        {
            "symbol": "Type(x) = T",
            "meaning": "Primitive Type Assertion",
            "plain_english": "Confirms value matches expected machine type (e.g. float32, int64, str)"
        },
        {
            "symbol": "[min_C, max_C]",
            "meaning": "Boundary Constraints",
            "plain_english": "Physical allowable range limits for column C (e.g. Age ∈ [0, 120])"
        },
        {
            "symbol": "RegexMatch(x, P)",
            "meaning": "Pattern Validation",
            "plain_english": "Evaluates string against strict regex P (ISO 8601 dates, email formats)"
        },
        {
            "symbol": "S_domain",
            "meaning": "Categorical Domain Set",
            "plain_english": "Permissible enum values (e.g. Status ∈ {'active', 'pending', 'canceled'})"
        },
        {
            "symbol": "I(·)",
            "meaning": "Indicator Function",
            "plain_english": "Evaluates composite multi-layer logical condition"
        }
    ],
    "numerical_example": "Validating an Incoming User Profile Record:\nRaw JSON Payload: {'zip': 7030, 'age': -5, 'discount': 1.45, 'timestamp': '04/05/2023'}\n\n1. Layer 1 & 2: Identifier Check on 'zip':\n   • Raw: 7030 (Stored as integer) --> Stripped leading zero!\n   • Fix: Force str with zero-padding: str(7030).zfill(5) --> '07030' (Restores valid NJ zip code).\n\n2. Layer 3: Physical Range Check on 'age':\n   • Value: -5 is an int, but fails constraint: 0 <= age <= 120.\n   • Outcome: Flagged as invalid boundary error --> Triggers schema rejection.\n\n3. Layer 3: Probability Range Check on 'discount':\n   • Value: 1.45 fails constraint: 0.0 <= discount <= 1.0 (Discount cannot exceed 100%).\n   • Outcome: Rejected by range contract.\n\n4. Layer 4: Timestamp Formatting:\n   • Ambiguous date '04/05/2023' parsed with explicit schema: pd.to_datetime('04/05/2023', format='%m/%d/%Y', utc=True) --> '2023-04-05T00:00:00Z' (Canonical ISO 8601).",
    "pitfalls": "Common Pitfall: Confusing primitive machine types with contextual semantics. Storing postal codes or phone numbers as integers strips leading zeros, corrupting location lookups. Additionally, relying on loose typing causes single stray strings ('N/A') to quietly upcast entire float columns into slow generic objects.",
    "core_logic": "Why this matters: Data contracts reject corrupt data before it contaminates feature stores or training pipelines. Boundary assertions ensure models learn from domain-valid distributions rather than corrupted negative ages or out-of-range probabilities.",
    "architectural_logic": "In production ML architectures, Data Contracts are enforced at two levels: Pydantic validates real-time incoming API inference payloads, while Pandera or Great Expectations asserts column schemas across batch ETL pipelines before features enter the feature store.",
    "connected_logic": [
        {
            "title": "Deep Learning Memory Optimization: Float32 vs. Float64",
            "content": "• Pandas and NumPy default to float64, consuming 8 bytes per cell and doubling model memory requirements unnecessarily.\n• Validating and downcasting features to float32 or bfloat16 cuts memory usage in half, allowing neural networks to double batch sizes without GPU out-of-memory errors."
        },
        {
            "title": "Pydantic Runtime Data Contracts in API & LLM Pipelines",
            "content": "• Modern AI web services validate real-time inference payloads at the API gateway using Pydantic BaseModel schemas.\n• Malformed inputs are rejected with descriptive 422 HTTP responses before unvalidated fields can reach machine learning inference code."
        },
        {
            "title": "Pandera DataFrame Contracts in Batch Feature Stores",
            "content": "• While Pydantic validates single records, Pandera enforces statistical and type contracts across distributed millions of rows in PySpark and Pandas.\n• Automatically asserts column types, null ratios, and distribution bounds during nightly ETL, blocking corrupt feature stores from deploying to production."
        },
        {
            "title": "Silent Object Column Contamination in Pandas",
            "content": "• A single stray text string ('N/A', '--') inside a column of 1,000,000 floats forces Pandas to silently upcast the entire series to generic object type.\n• This disables vectorized SIMD CPU operations, slows matrix computations by 100x, and causes PyTorch tensor conversion calls to crash."
        }
    ],
    "key_takeaways": [
        "Core Concept: Type validation checks machine representations; formatting consistency standardizes syntax; boundary rules verify physical realism.",
        "The Identifier Trap: Never store Zip codes, phone numbers, or SSNs as integers; always force string types to preserve leading zeros.",
        "Memory Leverage: Downcasting float64 to float32 cuts RAM by 50%, preventing GPU Out-of-Memory crashes in deep learning.",
        "Contract Tooling: Use Pydantic for real-time single-payload microservices and Pandera for large-scale DataFrame batch pipelines."
    ],
    "definition_bullets": [
        "Data Type Validation: The process of verifying that each field contains the expected primitive and semantic data type.",
        "Formatting Consistency: The systematic enforcement of uniform string syntax, regex patterns, and ISO date standards across a dataset."
    ]
}

def update_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    found = False
    for item in data:
        if item.get('id') == 'concept_data_validation':
            item.update(DATA_VALIDATION_UPDATE)
            found = True
            break
            
    if not found:
        print(f"Warning: concept_data_validation not found in {filepath}")
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
        if item.get('id') == 'concept_data_validation':
            item.update(DATA_VALIDATION_UPDATE)
            break
            
    new_content = '"""\nConcepts Database: Data Preparation & Exploration (22 Concepts)\n"""\n\nDATA_CONCEPTS = ' + json.dumps(mod.DATA_CONCEPTS, indent=4, ensure_ascii=False) + '\n'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Successfully updated {filepath}")

update_concepts_data_prep()
