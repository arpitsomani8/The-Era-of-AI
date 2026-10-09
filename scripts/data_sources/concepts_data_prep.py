"""
Concepts Database: Data Preparation & Exploration (22 Concepts)
"""

DATA_CONCEPTS = [
    {
        "id": "concept_deduplication",
        "title": "Deduplication & Record Linkage",
        "topic_id": "data_scrub",
        "topic_label": "Data Scrubbing & Cleaning",
        "category": "data",
        "category_label": "Data Preprocessing & EDA",
        "raw_subtopic": "Deduplication (Dropping duplicate user sessions/records)",
        "def": "Deduplication is the process of finding and merging duplicate records within the same dataset. Record Linkage (Entity Resolution) connects matching records across distinct datasets that lack a shared unique identifier.",
        "formula": "$$J(A, B) = \\frac{|A \\cap B|}{|A \\cup B|}, \\quad \\text{Sim}_{\\text{cos}}(v_A, v_B) = \\frac{v_A \\cdot v_B}{\\|v_A\\|_2 \\|v_B\\|_2}, \\quad \\text{Comparisons}_{\\text{naive}} = \\frac{N(N - 1)}{2}$$",
        "logic": "Pairwise Cartesian comparison grows quadratically as N(N - 1)/2. Multi-pass blocking and fuzzy similarity metrics resolve noisy real-world entities into clean Golden Records without evaluating unviable pairs.",
        "example": "E-commerce and CRM consolidation: Merging 'Apple Computer Inc, Cupertino CA' and 'Apple Incorporated, Cupertino California' into unified Golden Entity #AAPL-101 using Jaccard token overlap (0.80) and Jaro-Winkler name similarity (0.88).",
        "tags": [
            "Deduplication",
            "Data Cleaning",
            "Data Hygiene",
            "Data Leakage"
        ],
        "definition": "Deduplication is the process of finding and merging duplicate records within the same dataset. Record Linkage (Entity Resolution) connects matching records across distinct datasets that lack a shared unique identifier.",
        "formula_explanation": "",
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
    },
    {
        "id": "concept_structural_errors",
        "title": "Fixing Structural Errors",
        "topic_id": "data_scrub",
        "topic_label": "Data Scrubbing & Cleaning",
        "category": "data",
        "category_label": "Data Preprocessing & EDA",
        "raw_subtopic": "Fixing Structural Errors (Encoding, whitespace, case)",
        "def": "Structural errors are inconsistencies in how data is written, formatted, or categorized across rows, even though the raw information is present. Resolving them ensures consistent categories, valid numerical data types, and reliable machine learning predictions.",
        "formula": "$$x_{\\text{clean}} = \\text{Map}\\Big(\\text{RegexReplace}\\big(\\text{Strip}(\\text{Lower}(x_{\\text{raw}})), \\text{pattern}, \\text{repl}\\big)\\Big), \\quad z = \\frac{x_{\\text{clean}} - \\mu}{\\sigma}$$",
        "logic": "Inconsistent casing and typos trigger Cardinality Explosion in one-hot encoding, while formatted glyphs ($1,250) force numeric columns into object strings. Systematic canonicalization and unit harmonization restore statistical integrity.",
        "example": "Standardizing customer data: Transforming casing (' jaipur ' -> 'Jaipur'), stripping currency glyphs ('$75,000.50' -> 75000.50 float), and resolving date ambiguity ('04/05/2023' -> '2023-04-05T00:00:00Z' ISO 8601).",
        "tags": [
            "Data Quality",
            "Text Normalization",
            "Structural Errors",
            "Preprocessing"
        ],
        "definition": "Structural errors are inconsistencies in how data is written, formatted, or categorized across rows, even though the raw information is present. Resolving them ensures consistent categories, valid numerical data types, and reliable machine learning predictions.",
        "formula_explanation": "",
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
    },
    {
        "id": "concept_outlier_detection",
        "title": "Outlier Detection (IQR, Isolation Forest & Z-Score)",
        "topic_id": "data_scrub",
        "topic_label": "Data Scrubbing & Cleaning",
        "category": "data",
        "category_label": "Data Preprocessing & EDA",
        "raw_subtopic": "Outlier Detection (IQR Rule, Isolation Forest, Z-score)",
        "def": "Identifying data points that deviate so significantly from the remaining observations as to arouse suspicions that they were generated by a different mechanism, sensor fault, or error.",
        "formula": "$$\\text{IQR} = Q_3 - Q_1, \\quad \\text{Fence} = [Q_1 - 1.5 \\cdot \\text{IQR}, \\; Q_3 + 1.5 \\cdot \\text{IQR}], \\quad Z = \\frac{x - \\mu}{\\sigma}$$",
        "logic": "Linear models and MSE loss are exceptionally vulnerable to extreme outliers because errors are squared. A single typo like age 999 produces a gradient thousands of times larger than real samples, pulling decision boundaries away from genuine data.",
        "example": "Real estate appraisal: A house recorded with 3 bedrooms and an impossible price of $1 (judicial transfer) or $99,999,999 is detected as an outlier and isolated before training.",
        "tags": [
            "Outliers",
            "IQR",
            "Z-Score",
            "Isolation Forest",
            "Data Cleaning"
        ]
    },
    {
        "id": "concept_data_validation",
        "title": "Data Type Validation & Formatting Consistency",
        "topic_id": "data_scrub",
        "topic_label": "Data Scrubbing & Cleaning",
        "category": "data",
        "category_label": "Data Preprocessing & EDA",
        "raw_subtopic": "Data Type Validation & Formatting Consistency",
        "def": "Enforcing schema contracts that guarantee every column conforms to expected primitive types, date formats, non-empty bounds, and permissible domain ranges.",
        "formula": "$$\\text{Schema}(x) = \\begin{cases} \\text{Valid} & \\text{if } x \\in \\text{Domain}(C) \\wedge \\text{Type}(x) == T \\\\ \\text{Error} & \\text{otherwise} \\end{cases}$$",
        "logic": "Unchecked CSV ingestion frequently interprets numerical IDs as strings, timestamps as text, or negative prices as valid numbers, causing downstream silent failures during matrix computations.",
        "example": "A timestamp column containing a mixture of '2026-10-05', '05/10/2026', and Unix epochs is parsed into uniform UTC ISO-8601 timestamps.",
        "tags": [
            "Schema",
            "Data Contracts",
            "Validation",
            "Data Engineering"
        ]
    },
    {
        "id": "concept_mean_median_impute",
        "title": "Mean & Median Imputation",
        "topic_id": "data_impute",
        "topic_label": "Missing Value Imputation",
        "category": "data",
        "category_label": "Data Preprocessing & EDA",
        "raw_subtopic": "Mean & Median Imputation (For numerical columns)",
        "def": "Replacing missing numerical feature values with the computed arithmetic mean or median of the non-missing observations in the training set.",
        "formula": "$$\\hat{x}_i = \\mu = \\frac{1}{n} \\sum_{j \\in \\text{obs}} x_j \\quad \\text{or} \\quad \\hat{x}_i = \\text{Median}(X_{\\text{obs}})$$",
        "logic": "Median is robust to skewed distributions and outliers, whereas mean is sensitive. Caution: Imputation reduces feature variance and can distort covariances; always append a missingness indicator flag.",
        "example": "Predicting customer churn: For users who did not report their household income, replace missing values with the median income ($62,000) rather than dropping those user accounts.",
        "tags": [
            "Imputation",
            "Missing Values",
            "Median",
            "Mean"
        ]
    },
    {
        "id": "concept_mode_impute",
        "title": "Mode Imputation & Missing Categories",
        "topic_id": "data_impute",
        "topic_label": "Missing Value Imputation",
        "category": "data",
        "category_label": "Data Preprocessing & EDA",
        "raw_subtopic": "Mode Imputation (For categorical values)",
        "def": "Replacing missing values in categorical columns with the most frequently occurring value (mode), or assigning them to an explicit 'Unknown' / 'Missing' category.",
        "formula": "$$\\hat{x}_i = \\arg\\max_c \\sum_{j=1}^n \\mathbb{I}(x_j == c) \\quad \\text{or} \\quad \\hat{x}_i = \\text{'Unknown'}$$",
        "logic": "In many domains, missingness is not random (MNAR: Missing Not At Random). Creating a dedicated 'Unknown' category allows tree models to split on missingness as a deliberate informative signal.",
        "example": "Medical triage app: A missing 'Allergy' field is imputed as 'Unknown' rather than assuming 'None', alerting the physician that patient history was not yet taken.",
        "tags": [
            "Categorical Imputation",
            "Mode",
            "Missing Values"
        ]
    },
    {
        "id": "concept_knn_mice_impute",
        "title": "KNN & Iterative MICE Imputation",
        "topic_id": "data_impute",
        "topic_label": "Missing Value Imputation",
        "category": "data",
        "category_label": "Data Preprocessing & EDA",
        "raw_subtopic": "KNN & Iterative MICE Imputation (Multivariate)",
        "def": "Multivariate imputation techniques where missing entries in a column are modeled and predicted using the non-missing values of all other correlating features in that row.",
        "formula": "$$\\hat{x}_{ij} = \\frac{\\sum_{k \\in \\text{KNN}(i)} w_k x_{kj}}{\\sum w_k}, \\quad x_j^{(t+1)} = f(X_{-j}^{(t)}; \\theta_j)$$",
        "logic": "Mean imputation ignores correlation. If a person's height is missing, but their weight, gender, and age are known, KNN or MICE predicts their height based on similar people, preserving multivariate covariance.",
        "example": "Clinical trial data: If blood pressure is missing, MICE runs an iterative regression using cholesterol, age, BMI, and heart rate to estimate an accurate substitute.",
        "tags": [
            "MICE",
            "KNN Imputation",
            "Multivariate",
            "Advanced Preprocessing"
        ]
    },
    {
        "id": "concept_missing_indicators",
        "title": "Missingness Indicator Flags",
        "topic_id": "data_impute",
        "topic_label": "Missing Value Imputation",
        "category": "data",
        "category_label": "Data Preprocessing & EDA",
        "raw_subtopic": "Missingness Indicator Flags (Binary column tracking nulls)",
        "def": "Creating an accompanying binary boolean column ($m_i \\in \\{0, 1\\}$) alongside an imputed feature that explicitly records whether the original value was missing.",
        "formula": "$$m_i = \\begin{cases} 1 & \\text{if } x_i \\text{ was null/NaN} \\\\ 0 & \\text{if } x_i \\text{ was present} \\end{cases}, \\quad x_i \\leftarrow \\text{Impute}(x_i)$$",
        "logic": "The fact that a value was missing is often far more predictive than the imputed number itself. A missing income may signal unemployment or unwillingness to disclose high wealth.",
        "example": "Credit scoring: A user who leaves 'Number of existing credit cards' blank gets imputed with median 2, but `is_missing_credit_cards = 1` tells the model they omitted the field.",
        "tags": [
            "Missing Indicator",
            "Feature Engineering",
            "Data Imputation"
        ]
    },
    {
        "id": "concept_min_max_scaling",
        "title": "Min-Max Normalization (Linear Scaling)",
        "topic_id": "data_scale",
        "topic_label": "Feature Scaling & Transformations",
        "category": "data",
        "category_label": "Data Preprocessing & EDA",
        "raw_subtopic": "Linear Scaling / Min-Max Normalization (Maps to [0, 1])",
        "def": "A linear transformation that rescales numerical feature values into a fixed bound, typically between 0 and 1 (or -1 and 1).",
        "formula": "$$x_{\\text{scaled}} = \\frac{x - x_{\\min}}{x_{\\max} - x_{\\min}} \\in [0, 1]$$",
        "logic": "Essential when algorithms require bounded inputs (such as image pixel channels $[0, 255] \\to [0.0, 1.0]$) or when neural network activations like Sigmoid operate best over narrow numerical ranges.",
        "example": "Image preprocessing: Pixel color values ranging from 0 to 255 are divided by 255.0 to map them into $[0.0, 1.0]$ before passing into convolutional layers.",
        "tags": [
            "MinMax Scaler",
            "Normalization",
            "Feature Scaling"
        ]
    },
    {
        "id": "concept_z_score_scaling",
        "title": "Z-score Standardization",
        "topic_id": "data_scale",
        "topic_label": "Feature Scaling & Transformations",
        "category": "data",
        "category_label": "Data Preprocessing & EDA",
        "raw_subtopic": "Standardization / Z-score Normalization (Zero mean, unit variance)",
        "def": "Transforming feature values such that the resulting distribution has a mean of 0 ($\\mu=0$) and a standard deviation of 1 ($\\sigma=1$).",
        "formula": "$$z = \\frac{x - \\mu}{\\sigma}, \\quad \\mu = \\frac{1}{n}\\sum x_i, \\quad \\sigma = \\sqrt{\\frac{1}{n}\\sum (x_i - \\mu)^2}$$",
        "logic": "Prevents features with large raw numerical scales (e.g. Annual Income in dollars, $10^5$) from completely dominating features with small scales (e.g. Age in years, $10^1$) during gradient descent and distance calculations.",
        "example": "Customer segmentation: Comparing 'Annual Spend' ($12,000) and 'Items Bought' (3) without scaling makes KNN measure only dollar differences. Standardizing both to $\\mathcal{N}(0, 1)$ balances their influence.",
        "tags": [
            "Z-score",
            "StandardScaler",
            "Normalization",
            "Gradient Descent"
        ]
    },
    {
        "id": "concept_outlier_clipping",
        "title": "Outlier Clipping & Winsorization",
        "topic_id": "data_scale",
        "topic_label": "Feature Scaling & Transformations",
        "category": "data",
        "category_label": "Data Preprocessing & EDA",
        "raw_subtopic": "Outlier Clipping / Capping (Truncating extreme values)",
        "def": "Capping extreme values at fixed minimum and maximum percentile thresholds (e.g. 1st and 99th percentiles) rather than discarding the rows.",
        "formula": "$$x_{\\text{clipped}} = \\min(\\max(x, \\text{lower\\_bound}), \\text{upper\\_bound})$$",
        "logic": "Google ML Crash Course Principle: Extreme values stretch linear scales and ruin standard normalization. Clipping preserves the data point's direction (it remains large) without letting a single fluke value distort model weights.",
        "example": "Rooms per person in housing data: A fraternity house reports 50 rooms per person. Clipping caps any value above 4.0 to 4.0, preserving the fact that it is spacious without throwing gradient descent into chaos.",
        "tags": [
            "Clipping",
            "Winsorization",
            "Outlier Treatment"
        ]
    },
    {
        "id": "concept_log_scaling",
        "title": "Log Scaling & Power Transforms",
        "topic_id": "data_scale",
        "topic_label": "Feature Scaling & Transformations",
        "category": "data",
        "category_label": "Data Preprocessing & EDA",
        "raw_subtopic": "Log Scaling (Compressing extreme long-tail power law distributions)",
        "def": "Applying a logarithmic function $\\log(x + 1)$ to compress severe right-skewed power law distributions into a compact, bell-shaped normal curve.",
        "formula": "$$x_{\\text{log}} = \\ln(x + 1) \\quad \\text{or Box-Cox: } y^{(\\lambda)} = \\begin{cases} \\frac{y^\\lambda - 1}{\\lambda} & \\text{if } \\lambda \\neq 0 \\\\ \\ln(y) & \\text{if } \\lambda = 0 \\end{cases}$$",
        "logic": "Features like income, book sales, or web page visits follow 80/20 power laws where 99% of values are small and 1% are massive. Log transform compresses the long right tail, improving linear model fit.",
        "example": "Twitter follower count: Accounts vary from 10 followers to 100,000,000 followers. Taking $\\log_{10}(\\text{followers} + 1)$ transforms the values from $[1, 8]$, allowing smooth gradient updates.",
        "tags": [
            "Log Transform",
            "Power Law",
            "Box-Cox",
            "Skewed Data"
        ]
    },
    {
        "id": "concept_robust_scaler",
        "title": "Robust Scaler (Median & IQR)",
        "topic_id": "data_scale",
        "topic_label": "Feature Scaling & Transformations",
        "category": "data",
        "category_label": "Data Preprocessing & EDA",
        "raw_subtopic": "Robust Scaler (Using Median & IQR for heavy outlier resistance)",
        "def": "A scaling algorithm that removes the median and scales data according to the Interquartile Range (IQR between the 25th and 75th percentiles).",
        "formula": "$$x_{\\text{robust}} = \\frac{x - \\text{Median}(X)}{\\text{IQR}(X)} = \\frac{x - Q_2}{Q_3 - Q_1}$$",
        "logic": "StandardScaler uses mean and standard deviation, which are heavily distorted by outliers. RobustScaler uses median and IQR, meaning outliers do not influence the computed center and spread of the scaling factors.",
        "example": "Financial transaction logs: Fraud transactions with astronomical amounts ($5,000,000) won't skew the scaling parameters applied to normal everyday purchases ($20 to $100).",
        "tags": [
            "RobustScaler",
            "Median",
            "IQR",
            "Outlier Resistant"
        ]
    },
    {
        "id": "concept_one_hot_encoding",
        "title": "One-Hot Encoding (OHE)",
        "topic_id": "data_fe",
        "topic_label": "Categorical Data & Feature Crosses",
        "category": "data",
        "category_label": "Data Preprocessing & EDA",
        "raw_subtopic": "One-Hot Encoding (OHE for low-cardinality categories)",
        "def": "Representing a categorical feature with $K$ distinct values as a binary vector of length $K$, where exactly one element is 1 and all others are 0.",
        "formula": "$$\\text{Category } k \\implies e_k = [0, \\dots, 0, 1, 0, \\dots, 0]^T \\in \\{0, 1\\}^K$$",
        "logic": "Assigning integers (e.g. Red=1, Green=2, Blue=3) implies a false numerical order (Blue is 'greater than' Red). One-hot encoding treats each category as completely orthogonal and independent.",
        "example": "Car color feature: Transforming ['Red', 'Green', 'Blue'] into three separate binary features: `is_red`, `is_green`, and `is_blue`.",
        "tags": [
            "One-Hot Encoding",
            "Categorical Data",
            "Feature Engineering"
        ]
    },
    {
        "id": "concept_binning_bucketing",
        "title": "Binning & Bucketing",
        "topic_id": "data_fe",
        "topic_label": "Categorical Data & Feature Crosses",
        "category": "data",
        "category_label": "Data Preprocessing & EDA",
        "raw_subtopic": "Binning / Bucketing (Converting continuous values into discrete ranges)",
        "def": "Converting continuous numerical features into discrete ordinal or categorical buckets (bins).",
        "formula": "$$b = \\text{Bin}(x) = k \\quad \\text{if } t_k \\le x < t_{k+1}$$",
        "logic": "Allows linear models to learn non-linear relationships with continuous features (e.g., treating ages 0-17, 18-64, and 65+ with separate independent weights).",
        "example": "Human age: Rather than assuming income rises strictly linearly with every year of age, bucket age into [0-18, 19-25, 26-40, 41-65, 65+], letting the model fit retirement dynamics naturally.",
        "tags": [
            "Binning",
            "Bucketing",
            "Feature Discretization"
        ]
    },
    {
        "id": "concept_feature_crosses",
        "title": "Feature Crosses (Conjunctions)",
        "topic_id": "data_fe",
        "topic_label": "Categorical Data & Feature Crosses",
        "category": "data",
        "category_label": "Data Preprocessing & EDA",
        "raw_subtopic": "Feature Crosses (Conjunction of features A × B)",
        "def": "Creating a new synthetic feature by multiplying or crossing two or more categorical or binned features together: $\\text{Feature}_A \\times \\text{Feature}_B$.",
        "formula": "$$x_{AB} = x_A \\otimes x_B \\implies \\hat{y} = w_{AB} (x_A \\times x_B)$$",
        "logic": "Google ML Crash Course Flagship Concept: Linear models cannot learn non-linear decision boundaries like XOR. Crossing features allows linear learners to fit non-linear interactions without needing a deep neural network.",
        "example": "Housing price: Crossing `binned_latitude` × `binned_longitude` creates precise neighborhood tiles. A house in high-latitude AND high-longitude is priced high (San Francisco), while either alone is cheap.",
        "tags": [
            "Feature Crosses",
            "Google MLCC",
            "Non-linear Modeling",
            "Linear Models"
        ]
    },
    {
        "id": "concept_multi_hot_encoding",
        "title": "Multi-Hot Encoding",
        "topic_id": "data_fe",
        "topic_label": "Categorical Data & Feature Crosses",
        "category": "data",
        "category_label": "Data Preprocessing & EDA",
        "raw_subtopic": "Multi-Hot Encoding (For items with multiple tags, e.g. genres)",
        "def": "A binary vector representation of a set of categories where multiple entries can be set to 1 simultaneously to represent multiple co-occurring tags.",
        "formula": "$$v = \\sum_{k \\in \\text{tags}} e_k, \\quad v \\in \\{0, 1\\}^K$$",
        "logic": "Used when an entity can simultaneously belong to multiple categories without mutually exclusive constraints.",
        "example": "A film that is both a Sci-Fi and a Comedy is encoded over a 5-genre vector as: `[Action:0, Comedy:1, Drama:0, Horror:0, Sci-Fi:1]`.",
        "tags": [
            "Multi-Hot",
            "Categorical Features",
            "Tagging"
        ]
    },
    {
        "id": "concept_hashing_trick_oov",
        "title": "Hash Trick & OOV Bucketing",
        "topic_id": "data_fe",
        "topic_label": "Categorical Data & Feature Crosses",
        "category": "data",
        "category_label": "Data Preprocessing & EDA",
        "raw_subtopic": "Out-of-Vocabulary (OOV) Bucketing & Hash Trick",
        "def": "Using a hash function to map unbounded or high-cardinality categorical strings directly to a fixed number of bins $B$, resolving Out-of-Vocabulary (OOV) errors without keeping a lookup vocabulary table.",
        "formula": "$$\\text{bin\\_index} = \\text{Hash}(x) \\pmod B$$",
        "logic": "In web ad serving with hundreds of millions of search queries, maintaining an explicit string-to-integer dictionary requires gigabytes of RAM. The hash trick bounds memory to $B$ buckets while handling unseen strings gracefully.",
        "example": "Hashing search keywords into $10^6$ buckets: Both seen words and brand-new typos hash to a valid integer between 0 and 999,999, preventing production lookup crashes.",
        "tags": [
            "Hash Trick",
            "Feature Hashing",
            "OOV",
            "High Cardinality"
        ]
    },
    {
        "id": "concept_data_leakage_hygiene",
        "title": "Train, Val & Test Hygiene (Preventing Leakage)",
        "topic_id": "data_split",
        "topic_label": "Datasets, Splitting & Class Imbalance",
        "category": "data",
        "category_label": "Data Preprocessing & EDA",
        "raw_subtopic": "Train, Validation, and Test Set Hygiene (Preventing leakage)",
        "def": "Strict partitioning rules ensuring that no test set information (such as mean/std scaling parameters or future temporal records) contaminates the training phase.",
        "formula": "$$\\mathcal{D}_{\\text{train}} \\cap \\mathcal{D}_{\\text{test}} = \\emptyset, \\quad \\mu_{\\text{scaler}} = \\text{Fit}(\\mathcal{D}_{\\text{train}}), \\quad \\text{Transform}(\\mathcal{D}_{\\text{test}}; \\mu_{\\text{scaler}})$$",
        "logic": "Google ML Crash Course Principle: Scaling the whole dataset before splitting computes mean and variance using test data. This subtle leakage produces unrealistic test metrics that evaporate immediately after production deployment.",
        "example": "Time-series forecasting: Using customer transactions from 2026 to predict 2025 sales causes future leakage. Always use temporal splits: train on past months, test strictly on future months.",
        "tags": [
            "Data Leakage",
            "Dataset Splitting",
            "ML Best Practices"
        ]
    },
    {
        "id": "concept_stratified_kfold",
        "title": "Stratified K-Fold Cross-Validation",
        "topic_id": "data_split",
        "topic_label": "Datasets, Splitting & Class Imbalance",
        "category": "data",
        "category_label": "Data Preprocessing & EDA",
        "raw_subtopic": "Stratified K-Fold Cross-Validation (Preserving class proportions)",
        "def": "A cross-validation partitioning technique that guarantees every single validation fold contains the exact same percentage of target class labels as the full dataset.",
        "formula": "$$P(Y = c \\mid \\text{Fold}_k) = P(Y = c \\mid \\mathcal{D}) \\quad \\forall k \\in [1, K]$$",
        "logic": "Standard random splitting on imbalanced datasets can produce folds with zero minority positive examples, making evaluation metrics like Recall or ROC-AUC completely uncomputable.",
        "example": "Rare cancer detection (1% positive): A dataset of 1,000 patients has 10 positive cases. Stratified 5-fold CV ensures each fold has exactly 2 positive patients and 198 negative patients.",
        "tags": [
            "Cross Validation",
            "Stratified K-Fold",
            "Class Imbalance"
        ]
    },
    {
        "id": "concept_smote_oversampling",
        "title": "SMOTE (Synthetic Minority Over-sampling)",
        "topic_id": "data_split",
        "topic_label": "Datasets, Splitting & Class Imbalance",
        "category": "data",
        "category_label": "Data Preprocessing & EDA",
        "raw_subtopic": "SMOTE (Synthetic Minority Over-sampling Technique)",
        "def": "An over-sampling technique that generates synthetic minority samples by finding nearest neighbors in feature space and interpolating new points along the connecting line segments.",
        "formula": "$$x_{\\text{new}} = x_i + \\lambda (x_{zi} - x_i), \\quad \\lambda \\sim \\text{Uniform}(0, 1)$$",
        "logic": "Naive duplication of minority samples leads to severe overfitting. SMOTE synthesizes realistic plausible points in the feature space, expanding the decision boundary around minority examples.",
        "example": "Credit card fraud: Taking two genuine fraudulent transactions close to each other in feature space ($amount, $distance), SMOTE generates a synthetic transaction halfway between them.",
        "tags": [
            "SMOTE",
            "Over-sampling",
            "Class Imbalance"
        ]
    },
    {
        "id": "concept_resampling_strategies",
        "title": "Downsampling vs Upsampling",
        "topic_id": "data_split",
        "topic_label": "Datasets, Splitting & Class Imbalance",
        "category": "data",
        "category_label": "Data Preprocessing & EDA",
        "raw_subtopic": "Downsampling the Majority vs Upsampling the Minority",
        "def": "Balancing class distributions by randomly discarding majority class examples (downsampling) or duplicating/synthesizing minority class examples (upsampling).",
        "formula": "$$\\text{Ratio} = \\frac{N_{\\text{minority}}}{N_{\\text{majority}}} \\to 1:1 \\quad \\text{or} \\quad 1:10$$",
        "logic": "When training on billions of clicks where only 0.1% are positive, downsampling the 99.9% non-clicks drastically speeds up training without losing predictive variance. Re-calibrate probabilities afterwards!",
        "example": "Ad click prediction: Retain all 1,000,000 clicked ads, and randomly sample only 5% of the 1,000,000,000 unclicked ads to train the logistic regression model in minutes instead of days.",
        "tags": [
            "Downsampling",
            "Upsampling",
            "Imbalance",
            "Re-calibration"
        ]
    },
    {
        "id": "concept_cost_sensitive_weighting",
        "title": "Cost-Sensitive Training & Loss Weighting",
        "topic_id": "data_split",
        "topic_label": "Datasets, Splitting & Class Imbalance",
        "category": "data",
        "category_label": "Data Preprocessing & EDA",
        "raw_subtopic": "Loss Weighting (Cost-sensitive training)",
        "def": "Assigning higher loss penalties to errors on the minority class during optimization, forcing the model to prioritize avoiding false negatives.",
        "formula": "$$\\mathcal{L} = -\\sum_{i=1}^n \\left[ w_1 y_i \\log(\\hat{y}_i) + w_0 (1 - y_i) \\log(1 - \\hat{y}_i) \\right], \\quad w_1 = \\frac{N}{2 \\cdot N_{\\text{pos}}}$$",
        "logic": "Avoids the artificial distortion of data distributions caused by resampling. Modifies the gradient loss directly so false negatives generate 10x or 100x stronger corrective gradient steps.",
        "example": "Cancer diagnosis: Missing a cancer patient (False Negative) has catastrophic consequences. Giving positive cancer cases a loss weight of $w=50$ penalizes missed diagnoses 50 times more than false alarms.",
        "tags": [
            "Loss Weighting",
            "Cost-Sensitive",
            "Class Imbalance"
        ]
    }
]
