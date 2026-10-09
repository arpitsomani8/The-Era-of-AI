import json

DEDUPLICATION_UPDATE = {
    "def": "Deduplication is the process of finding and merging duplicate records within the same dataset. Record Linkage (Entity Resolution) connects matching records across distinct datasets that lack a shared unique identifier.",
    "definition": "Deduplication is the process of finding and merging duplicate records within the same dataset. Record Linkage (Entity Resolution) connects matching records across distinct datasets that lack a shared unique identifier.",
    "formula": "$$J(A, B) = \\frac{|A \\cap B|}{|A \\cup B|}, \\quad \\text{Sim}_{\\text{cos}}(v_A, v_B) = \\frac{v_A \\cdot v_B}{\\|v_A\\|_2 \\|v_B\\|_2}, \\quad \\text{Comparisons}_{\\text{naive}} = \\frac{N(N - 1)}{2}$$",
    "formula_explanation": "",
    "logic": "Pairwise Cartesian comparison grows quadratically as N(N - 1)/2. Multi-pass blocking and fuzzy similarity metrics resolve noisy real-world entities into clean Golden Records without evaluating unviable pairs.",
    "example": "E-commerce and CRM consolidation: Merging 'Apple Computer Inc, Cupertino CA' and 'Apple Incorporated, Cupertino California' into unified Golden Entity #AAPL-101 using Jaccard token overlap (0.80) and Jaro-Winkler name similarity (0.88).",
    "simple_summary": "Deduplication cleans duplicates within one dataset; Record Linkage connects matching records across different datasets without shared keys. Blocking partitions records into candidate bins, while similarity metrics (Levenshtein, Jaro-Winkler, Embeddings) match messy real-world variations.",
    "core_terms": [
        {
            "term": "Deduplication & Record Linkage",
            "what_is_it": "• Deduplication finds and merges duplicate rows within the same dataset, while Record Linkage links matching entities across different datasets that lack a shared unique ID.\n• Resolves noisy variations (typos, abbreviations, format differences) into a single clean 'Golden Record' for each real-world entity.",
            "analogy": "A hospital combining emergency room records with outpatient clinic logs when patient names are spelled 'Jon Smyth' in one and 'John Smith' in the other.",
            "why_it_matters": "Prevents duplicate rows from acting as artificial sample weights, stops test set contamination, and ensures accurate business analytics."
        },
        {
            "term": "The Blocking Strategy (Candidate Partitioning)",
            "what_is_it": "• An indexing technique that groups records into candidate buckets (blocks), comparing only records within the same bucket.\n• Slashes comparison counts from quadratic to near-linear scale by eliminating obvious non-matching pairs upfront.",
            "analogy": "Sorting mail into postal zip code bins before sorting individual streets, rather than comparing every letter in the nation against every other letter.",
            "why_it_matters": "The essential engineering step that makes large-scale entity resolution computationally feasible in Big Data and LLM pipelines."
        },
        {
            "term": "String & Semantic Similarity Metrics",
            "what_is_it": "• Mathematical algorithms that calculate a match score from 0.0 (completely distinct) to 1.0 (identical) between two text fields.\n• Evaluates spelling variations via edit distance and token overlap, while neural embeddings capture semantic synonyms.",
            "analogy": "A human auditor using both a spelling checker (edit distance) and contextual knowledge that 'IBM' equals 'International Business Machines' (semantic embeddings).",
            "why_it_matters": "Supplies the quantitative feature signals used by probabilistic models and ML classifiers to decide matches."
        }
    ],
    "types_header": "Matching Techniques & Blocking Paradigms",
    "types_badge": "Linkage Methodologies",
    "quick_types": [
        {
            "type": "Standard Exact Blocking",
            "definition": "Partitions records sharing an identical key (e.g. Postal Code or Birth Year), evaluating pairs only within the same bin.",
            "looks_like": "Zip Code Bins: Only compare records in Zip 90210"
        },
        {
            "type": "Phonetic Blocking (Soundex/Metaphone)",
            "definition": "Encodes words by spoken phonetic sound, mapping misspelled names like 'Smith' and 'Smyth' to identical hash code S530.",
            "looks_like": "Soundex('Smith') == Soundex('Smyth') == 'S530'"
        },
        {
            "type": "Levenshtein Edit Distance",
            "definition": "Counts minimum single-character insertions, deletions, or substitutions to transform string A into string B.",
            "looks_like": "kitten → sitting = 3 character edits"
        },
        {
            "type": "Jaro-Winkler Distance (Names)",
            "definition": "Measures character transpositions with heavy bonus for matching prefixes. The gold standard for human first and last names.",
            "looks_like": "High score for prefix matches: 'Catherine' vs 'Katherine'"
        },
        {
            "type": "Semantic Vector Embeddings",
            "definition": "Dense neural embeddings (e.g. Sentence-BERT) computing cosine similarity to resolve aliases with zero shared characters.",
            "looks_like": "Cosine Sim: 'Big Blue' ↔ 'IBM' ≈ 0.94"
        }
    ],
    "symbol_guide": [
        {
            "symbol": "J(A, B)",
            "meaning": "Jaccard Similarity",
            "plain_english": "Token-overlap ratio between word sets A and B (bounded between 0 and 1)"
        },
        {
            "symbol": "|A ∩ B|",
            "meaning": "Intersection Count",
            "plain_english": "Number of distinct words or n-grams shared by both text records"
        },
        {
            "symbol": "|A ∪ B|",
            "meaning": "Union Count",
            "plain_english": "Total unique words or n-grams appearing across either record"
        },
        {
            "symbol": "Sim_cos",
            "meaning": "Cosine Similarity",
            "plain_english": "Angular alignment between deep neural embedding vectors v_A and v_B"
        },
        {
            "symbol": "v_A, v_B",
            "meaning": "Vector Embeddings",
            "plain_english": "Dense semantic representations generated by models like Sentence-BERT"
        },
        {
            "symbol": "N",
            "meaning": "Dataset Record Count",
            "plain_english": "Total number of raw data rows requiring deduplication or linkage"
        }
    ],
    "numerical_example": "Comparing Two Company Records:\nRecord A: 'Apple Computer Inc, Cupertino CA'\nRecord B: 'Apple Incorporated, Cupertino California'\n\n1. Preprocessing & Normalization:\n   • Strip punctuation & lowercase: A = {'apple', 'computer', 'inc', 'cupertino', 'ca'}\n   • Expand abbreviations: A = {'apple', 'computer', 'incorporated', 'cupertino', 'california'}\n   • Normalize B: B = {'apple', 'incorporated', 'cupertino', 'california'}\n\n2. Jaccard Token Overlap Calculation:\n   • Intersection A ∩ B = {'apple', 'incorporated', 'cupertino', 'california'} (Size = 4)\n   • Union A ∪ B = {'apple', 'computer', 'incorporated', 'cupertino', 'california'} (Size = 5)\n   • Jaccard Score: J(A, B) = 4 / 5 = 0.80 (80% token agreement).\n\n3. Jaro-Winkler Name Check:\n   • 'Apple Computer' vs 'Apple Incorporated' shares prefix 'Apple ' --> Jaro-Winkler score = 0.88.\n\n4. Decision: With combined score > 0.85 threshold, system merges both records into Golden Entity ID #AAPL-101.",
    "pitfalls": "Common Pitfall: Relying strictly on hardcoded exact match rules. Even a minor typo, transposed digits, or slight abbreviation ('St' vs 'Street') will cause deterministic checks to fail completely. Always combine blocking with fuzzy distance metrics and probability thresholds.",
    "core_logic": "Why this matters: Duplicated records act as unintentional high-loss sample weights that distort training distributions. In pretraining, duplicates cause language models to memorize text and leak private training sequences rather than learning general reasoning.",
    "architectural_logic": "In modern LLM data curation systems, Deduplication is executed via distributed MinHash + Locality-Sensitive Hashing (LSH) across petabytes of text. In enterprise RAG architectures, Record Linkage resolves customer data across fragmented SQL databases into unified entity vectors.",
    "connected_logic": [
        {
            "title": "LLM Pretraining: Web-Scale Deduplication with MinHash & LSH",
            "content": "• Web scrapes like Common Crawl contain massive duplicated content (boilerplate licenses, syndicated news), causing LLMs to memorize text and risk privacy leaks.\n• Foundation models (LLaMA, GPT-4) run MinHash with Locality-Sensitive Hashing (LSH) across petabytes of text, pruning duplicate documents before training commences."
        },
        {
            "title": "Benchmark Data Contamination Prevention",
            "content": "• When evaluation benchmarks (e.g. MMLU, GSM8K, HumanEval) accidentally appear in training corpuses, models achieve deceptively high scores by memorization.\n• Rigorous fuzzy 13-gram deduplication between pretraining corpuses and evaluation sets is required to certify legitimate AI reasoning capabilities."
        },
        {
            "title": "The 3 Linkage Paradigms: Rule-Based vs. Probabilistic vs. ML",
            "content": "• Deterministic rules (e.g. IF SSN matches) execute with high speed but shatter on typos, while probabilistic Fellegi-Sunter models weigh field agreement mathematically.\n• Modern deep learning pairs fine-tuned Transformer bi-encoders with vector databases, matching semantic aliases ('Big Blue' vs. 'IBM') that share zero common characters."
        },
        {
            "title": "FinTech Fraud Detection & Synthetic Entity Resolution",
            "content": "• Financial criminals exploit data silos by opening accounts with slight name permutations, shared burner phone numbers, and altered street addresses.\n• Graph-based entity resolution links disparate applications into unified fraud clusters, unmasking synthetic identity rings in real-time transaction pipelines."
        }
    ],
    "key_takeaways": [
        "Core Distinction: Deduplication merges duplicate records internally; Record Linkage connects matching entities across distinct datasets without shared keys.",
        "The Scaling Solution: Blocking (Standard, Soundex, MinHash LSH) slashes pairwise comparisons from impossible O(N²) down to scalable near-linear time.",
        "Matching Metrics: Leverages Levenshtein (edits), Jaro-Winkler (names), Jaccard (tokens), and Vector Embeddings (semantic synonyms).",
        "AI Mission-Critical: Essential for web text deduplication in LLMs, benchmark contamination prevention, and enterprise customer golden records."
    ],
    "definition_bullets": [
        "Deduplication: The process of finding, merging, and pruning redundant duplicate records within a single dataset.",
        "Record Linkage: The process of identifying and connecting records corresponding to the same entity across disparate databases without unique identifiers."
    ]
}

def update_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    found = False
    for item in data:
        if item.get('id') == 'concept_deduplication':
            item.update(DEDUPLICATION_UPDATE)
            found = True
            break
            
    if not found:
        print(f"Warning: concept_deduplication not found in {filepath}")
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
        if item.get('id') == 'concept_deduplication':
            item.update(DEDUPLICATION_UPDATE)
            break
            
    new_content = '"""\nConcepts Database: Data Preparation & Exploration (22 Concepts)\n"""\n\nDATA_CONCEPTS = ' + json.dumps(mod.DATA_CONCEPTS, indent=4, ensure_ascii=False) + '\n'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Successfully updated {filepath}")

update_concepts_data_prep()
