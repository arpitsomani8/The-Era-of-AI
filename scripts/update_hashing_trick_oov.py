import json

HASHING_TRICK_UPDATE = {
    "def": "The Hash Trick & OOV Bucketing are feature engineering techniques that map high-cardinality categories, words, or unseen Out-of-Vocabulary (OOV) tokens directly into a fixed-width vector using deterministic hash functions without storing a vocabulary dictionary in memory.",
    "definition": "The Hash Trick & OOV Bucketing are feature engineering techniques that map high-cardinality categories, words, or unseen Out-of-Vocabulary (OOV) tokens directly into a fixed-width vector using deterministic hash functions without storing a vocabulary dictionary in memory.",
    "formula": "$$j = |h(x)| \\pmod B, \\quad \\tilde{\\mathbf{x}}_j = \\sum_{x \\in \\mathcal{D}} \\xi(x) \\cdot \\mathbb{I}(|h(x)| \\pmod B = j), \\quad \\xi(x) \\in \\{-1, +1\\}$$",
    "formula_explanation": "",
    "logic": "Storing multi-gigabyte vocabulary dictionaries for millions of web tokens, user IDs, or search queries causes severe memory bloat and pipeline crashes when novel unseen words appear. The Hashing Trick uses mathematical hash functions to fix the feature dimension to a constant B forever, with signed hashing (+1/-1) mathematically canceling out collision noise.",
    "example": "Search advertising query logs: Billions of search terms and misspelled queries are passed through FeatureHasher with B = 2^18 (262,144 buckets). Every seen query and novel typo deterministically maps to a valid bucket index between 0 and 262,143 without storing a dictionary file.",
    "simple_summary": "Instead of storing a giant dictionary of millions of words in RAM, the Hashing Trick calculates each word's bucket position using a fast mathematical hash function. It fixes your feature table width forever, never crashes on unseen words (OOV), and works on endless streaming data. The tradeoff is that hashing is a one-way street—you cannot turn a bucket index back into the original word.",
    "core_terms": [
        {
            "term": "The Hashing Trick (Feature Hashing)",
            "what_is_it": "• An algorithm that maps text categories, IDs, or words directly into a fixed-size vector of B buckets using a deterministic mathematical hash function: Index = |h(x)| mod B.\n• Replaces giant dictionary lookup tables with instant mathematical calculations, fixing feature matrix dimensions forever without needing to store words in RAM.",
            "analogy": "A coat check room with exactly 500 numbered hooks: guests calculate their hook number by hashing their name, so the attendant never has to keep a master guest ledger.",
            "why_it_matters": "Enables machine learning models to process millions of streaming user IDs, search queries, or web domains with zero vocabulary memory overhead."
        },
        {
            "term": "Hash Collisions & Signed Hashing",
            "what_is_it": "• A hash collision occurs when two completely different categories happen to map to the exact same bucket number.\n• Signed hashing solves collision bias by using a second hash function to randomly assign a +1 or -1 sign to each word, ensuring that collision errors cancel each other out across gradient updates.",
            "analogy": "Two people sharing the same coat hook, but one hangs their coat right-side up (+1) and the other upside down (-1) so their weights cancel out rather than falsely doubling.",
            "why_it_matters": "Mathematically guarantees that the expected inner product between hashed vectors is unbiased, preserving geometric distance without distorting model weights."
        },
        {
            "term": "Out-Of-Vocabulary (OOV) Bucketing",
            "what_is_it": "• The strategy for handling novel words, categories, or IDs that never appeared during training (e.g. brand-new slang, product IDs, or user typos).\n• Rather than throwing unseen words away or crashing inference servers with a KeyError, OOV bucketing maps unknown tokens to a dedicated pool of reserve hash buckets.",
            "analogy": "A post office sorting bin labeled 'Unrecognized Addresses' where unfamiliar mail is safely routed and processed instead of being shredded.",
            "why_it_matters": "Protects live production inference servers from crashing on unseen user inputs while giving the model a way to learn behavioral weights for novel tokens."
        }
    ],
    "types_header": "Hashing Implementations & Streaming Frameworks",
    "types_badge": "High-Cardinality Scaling",
    "quick_types": [
        {
            "type": "FeatureHasher (Scikit-Learn)",
            "definition": "High-speed transformer implementing signed MurmurHash3 directly to Scipy CSR sparse matrices.",
            "looks_like": "FeatureHasher(n_features=2**18, input_type='string')"
        },
        {
            "type": "Vowpal Wabbit (VW) Stream Hashing",
            "definition": "Industry-standard streaming ML engine utilizing 24-bit MurmurHash for real-time petabyte learning.",
            "looks_like": "vw -d train.vw -b 24 --loss_function logistic"
        },
        {
            "type": "Keras TextVectorization(OOV Mode)",
            "definition": "TensorFlow layer configuring max_tokens with reserved OOV indices for deep neural NLP pipelines.",
            "looks_like": "TextVectorization(max_tokens=20000, output_mode='int')"
        },
        {
            "type": "Dedicated OOV Sub-Bucketing",
            "definition": "Allocating K reserve buckets (e.g. 100 OOV bins) to hash unseen inference tokens instead of a single bucket.",
            "looks_like": "oov_bucket = hash(unseen_word) % num_oov_buckets"
        },
        {
            "type": "Subword Byte-Pair Hash (FastText)",
            "definition": "Hashing character n-grams to represent misspelled words and morphologically rich OOV terms.",
            "looks_like": "fasttext.train_unsupervised('data.txt', minn=3, maxn=6)"
        }
    ],
    "symbol_guide": [
        {
            "symbol": "j",
            "meaning": "Hash Bucket Index",
            "plain_english": "The computed column coordinate between 0 and B-1 where the feature is accumulated"
        },
        {
            "symbol": "h(x)",
            "meaning": "Primary Hash Function",
            "plain_english": "A fast, deterministic hashing algorithm such as MurmurHash3"
        },
        {
            "symbol": "B",
            "meaning": "Total Bucket Count",
            "plain_english": "The fixed dimensional size of the feature vector (e.g. B = 2^18 = 262,144)"
        },
        {
            "symbol": "ξ(x) (xi)",
            "meaning": "Sign Hash Function",
            "plain_english": "A secondary hash returning +1 or -1 with equal probability to eliminate collision bias"
        },
        {
            "symbol": "x",
            "meaning": "Input Token or Category",
            "plain_english": "The raw string or identifier being hashed, such as a user ID or search word"
        },
        {
            "symbol": "x̃_j (x_tilde_j)",
            "meaning": "Hashed Feature Coordinate",
            "plain_english": "The resulting numerical value accumulated at bucket index j"
        }
    ],
    "numerical_example": "Hashing 3 Tokens into a Fixed B = 4 Bucket Array:\nTokens: ['apple', 'banana', 'cherry']\n\n1. Calculate Primary Hash and Secondary Sign:\n   • 'apple':  |h('apple')| = 13,   sign ξ('apple') = +1\n   • 'banana': |h('banana')| = 22,  sign ξ('banana') = -1\n   • 'cherry': |h('cherry')| = 17,  sign ξ('cherry') = +1\n\n2. Compute Bucket Coordinates (j = |h(x)| mod 4):\n   • 'apple':  13 mod 4 = 1  → Bucket 1\n   • 'banana': 22 mod 4 = 2  → Bucket 2\n   • 'cherry': 17 mod 4 = 1  → Bucket 1 (Collision with 'apple'!)\n\n3. Accumulate Signed Feature Vector x̃ ∈ ℝ⁴:\n   • Bucket 0: 0\n   • Bucket 1: ξ('apple') + ξ('cherry') = (+1) + (+1) = +2\n   • Bucket 2: ξ('banana') = -1\n   • Bucket 3: 0\n   Final Hashed Vector: x̃ = [0, +2, -1, 0]\n\nOutcome: All tokens were mapped into a fixed 4-dimensional vector with zero vocabulary lookups, and signed hashing prevents directional bias during model weight updates.",
    "pitfalls": "Common Pitfall: Setting the bucket parameter (B) too small. If you hash 1,000,000 distinct words into only 1,000 buckets, each bucket contains 1,000 conflicting words, creating devastating collision noise that destroys predictive accuracy. Always choose B sufficiently large (typically 2^18 to 2^24 in production). Also, remember that hashing is one-way: you cannot reverse a bucket index back into the original word string.",
    "core_logic": "Why this matters: In web-scale machine learning, vocabulary sizes are unbounded and non-stationary. The Hashing Trick decouples feature engineering from static dictionary state, enabling models to train over streaming internet data with constant RAM and guaranteed bounded dimensions.",
    "architectural_logic": "In enterprise ad ranking and recommendation architectures (e.g. Vowpal Wabbit, FTRL-Proximal), FeatureHasher processes raw text and high-cardinality IDs directly into Scipy CSR sparse matrices. Fixed bucket size B allows zero-serialization online inference services to evaluate streaming requests in microseconds.",
    "connected_logic": [
        {
            "title": "High-Throughput Ad-Click Prediction (Vowpal Wabbit & CTR)",
            "content": "• In industrial search advertising (Google, Meta), models train on continuous streaming click logs containing billions of distinct search query tokens and user cookie IDs.\n• The Hashing Trick allows online learning algorithms (like FTRL-Proximal in Vowpal Wabbit) to update weights continuously without freezing training to expand dictionary tables."
        },
        {
            "title": "Unbiased Dot-Product Preservation via Signed Hashing",
            "content": "• In classical linear regression, collision cross-talk between uncorrelated features could bias inner products ⟨u, v⟩.\n• By pairing the primary hash h(x) with an independent Rademacher sign hash ξ(x) ∈ {-1, +1}, the expectation of cross-term products 𝔼[ξ(u) ξ(v)] = 0, guaranteeing mathematically unbiased dot products."
        },
        {
            "title": "Loss of Reversibility & Model Debuggability",
            "content": "• In high-stakes regulatory domains (credit scoring, clinical diagnosis), models must explain exactly which feature triggered a prediction (e.g. SHAP or coefficient weights).\n• The Hashing Trick is fundamentally a one-way irreversible compression; a model weight at Bucket 45,210 cannot be mapped back to a specific medical condition or customer name without an external inverted index."
        },
        {
            "title": "Subword Hashing for Robust Misspellings & Morphologies",
            "content": "• Standard dictionary tokenizers completely fail when user inputs contain novel slang, compound words, or character typos (e.g. 'amazzzing').\n• Libraries like FastText combine character n-gram hashing (e.g. hashing 'ama', 'maz', 'zzz') into bucket vectors, ensuring that unseen typos share overlapping hash activations with their root words."
        }
    ],
    "key_takeaways": [
        "Stateless Fixed Dimensions: Maps unbounded categories to a fixed width B forever without storing vocabulary dictionaries in memory.",
        "Signed Collision Balancing: Uses a secondary sign hash (+1/-1) so collision errors mathematically cancel out in expectation.",
        "Infinite Streaming Resilience: Seamlessly absorbs novel tokens, typos, and out-of-vocabulary (OOV) inputs without pipeline crashes.",
        "Irreversible Tradeoff: Fast and memory-efficient, but one-way; impossible to recover original word strings from hashed indices."
    ],
    "definition_bullets": [
        "The Hashing Trick: A dimensionality-reduction and encoding method that applies a hash function to map categorical tokens directly into a fixed-size vector space.",
        "OOV Bucketing: A strategy allocating designated hash buckets to represent unseen out-of-vocabulary tokens during model inference."
    ]
}

def update_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    found = False
    for item in data:
        if item.get('id') == 'concept_hashing_trick_oov':
            item.update(HASHING_TRICK_UPDATE)
            found = True
            break
            
    if not found:
        print(f"Warning: concept_hashing_trick_oov not found in {filepath}")
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
        if item.get('id') == 'concept_hashing_trick_oov':
            item.update(HASHING_TRICK_UPDATE)
            break
            
    new_content = '"""\nConcepts Database: Data Preparation & Exploration (22 Concepts)\n"""\n\nDATA_CONCEPTS = ' + json.dumps(mod.DATA_CONCEPTS, indent=4, ensure_ascii=False) + '\n'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Successfully updated {filepath}")

update_concepts_data_prep()
