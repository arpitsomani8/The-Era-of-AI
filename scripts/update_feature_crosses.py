import json

FEATURE_CROSSES_UPDATE = {
    "def": "Feature Crosses (Feature Conjunctions) are synthetic features created by multiplying or combining two or more features together, capturing non-linear feature interactions that simple additive models cannot detect.",
    "definition": "Feature Crosses (Feature Conjunctions) are synthetic features created by multiplying or combining two or more features together, capturing non-linear feature interactions that simple additive models cannot detect.",
    "formula": "$$x_{AB} = x_A \\otimes x_B, \\quad \\hat{y} = w_0 + w_A x_A + w_B x_B + w_{AB} (x_A \\cdot x_B)$$",
    "formula_explanation": "",
    "logic": "A standard linear model evaluates features independently along straight hyperplanes. Crossing features combines them multiplicatively, enabling ultra-fast linear and logistic models to learn non-linear curved decision boundaries and solve classic non-linear challenges like the XOR problem without requiring deep neural networks.",
    "example": "Real estate appraisal: Crossing binned latitude with binned longitude creates discrete 2D spatial neighborhood tiles. A house with high latitude alone is not necessarily expensive, but high latitude AND high longitude (San Francisco) commands premium prices.",
    "simple_summary": "A Feature Cross combines two or more features into one new feature (like 'City × Device' or 'Latitude × Longitude') to capture how they interact. This allows fast, simple linear models to solve non-linear problems (like XOR gates) without deep learning. However, crossing categories with many options can cause a feature explosion, requiring L1 regularization or hashing.",
    "core_terms": [
        {
            "term": "Feature Crosses (Interaction Terms)",
            "what_is_it": "• A synthetic feature formed by combining (multiplying or conjoining) two or more existing features to capture their joint interactive relationship.\n• Instead of treating variables as completely independent, it allows an algorithm to see that the effect of Feature A depends heavily on the specific value of Feature B.",
            "analogy": "Pairing food and wine: red wine is great and steak is great, but pairing 'Red Wine × Steak' creates a distinct dining experience that simple addition cannot capture.",
            "why_it_matters": "Enables lightning-fast linear models to learn complex, non-linear decision boundaries (like solving the classic XOR problem) without requiring deep neural networks."
        },
        {
            "term": "The 3 Types of Feature Crosses",
            "what_is_it": "• Categorical × Categorical: A Cartesian pairing of discrete text categories (e.g. 'Device=Mobile' × 'Browser=Safari').\n• Binned × Binned: Discretizing two continuous axes into a 2D spatial grid (e.g. 'Binned Latitude' × 'Binned Longitude' to define neighborhood boundaries).\n• Categorical × Continuous: Multiplying a category dummy by a continuous number, allowing the slope to tilt differently for each category.",
            "analogy": "A city street grid: combining '5th Avenue' with '42nd Street' pinpoints the exact intersection (The New York Public Library), which neither street name alone can identify.",
            "why_it_matters": "Provides machine learning engineers with a structured menu for engineering multi-dimensional interactions across diverse tabular data types."
        },
        {
            "term": "Combinatorial Explosion & Sparsity",
            "what_is_it": "• The architectural pitfall where crossing high-cardinality features causes the number of possible columns to multiply exponentially (K₁ × K₂).\n• Crossing 1,000 cities with 500 product categories creates 500,000 binary features, where 99.9% of pairs appear only once or never, causing severe overfitting and memory thrashing.",
            "analogy": "Creating a custom cocktail named after every single customer and drink combination in a bar: the menu would have 500,000 pages, with most drinks never ordered again.",
            "why_it_matters": "Governs modern production design: prune useless crosses using L1 Lasso regularization, the Hashing Trick, or replace explicit crosses with dense neural embeddings."
        }
    ],
    "types_header": "Interaction Types & Modern Pruning Tools",
    "types_badge": "Feature Conjunctions",
    "quick_types": [
        {
            "type": "Categorical Cartesian Cross",
            "definition": "Joining two nominal strings to create distinct interaction tokens (e.g. 'City=NYC_Device=iOS').",
            "looks_like": "df['city_device'] = df['city'] + '_' + df['device']"
        },
        {
            "type": "2D Binned Spatial Grid",
            "definition": "Crossing binned latitude and binned longitude to model hyperlocal real-estate geographic tiles.",
            "looks_like": "df['geo_tile'] = df['lat_bin'].astype(str) + '_' + df['lon_bin'].astype(str)"
        },
        {
            "type": "PolynomialFeatures(interaction_only=True)",
            "definition": "Scikit-Learn transformer generating multiplicative interaction terms (x_i · x_j) without squared powers.",
            "looks_like": "PolynomialFeatures(interaction_only=True, include_bias=False)"
        },
        {
            "type": "L1 Lasso Pruning (Sparseness Filter)",
            "definition": "Regularization technique driving non-predictive crossed feature weights to exactly zero to prevent overfitting.",
            "looks_like": "LogisticRegression(penalty='l1', solver='liblinear')"
        },
        {
            "type": "Feature Hashing (Hashing Trick)",
            "definition": "Compressing millions of high-cardinality feature crosses into a bounded integer vector via MurmurHash3.",
            "looks_like": "FeatureHasher(n_features=50000, input_type='string')"
        }
    ],
    "symbol_guide": [
        {
            "symbol": "x_AB",
            "meaning": "Synthetic Crossed Feature",
            "plain_english": "The interactive conjunction resulting from combining features A and B"
        },
        {
            "symbol": "x_A, x_B",
            "meaning": "Base Features",
            "plain_english": "The individual input variables, which may be binary, binned, or continuous"
        },
        {
            "symbol": "⊗ (tensor cross)",
            "meaning": "Interaction Operator",
            "plain_english": "The conjunction or Cartesian product operator generating the crossed feature"
        },
        {
            "symbol": "w_AB",
            "meaning": "Interaction Weight",
            "plain_english": "The model coefficient learning the specific conditional effect of the conjunction"
        },
        {
            "symbol": "w_A, w_B",
            "meaning": "Main Effect Weights",
            "plain_english": "The individual linear coefficients assigned to features A and B independently"
        },
        {
            "symbol": "w_0",
            "meaning": "Model Intercept",
            "plain_english": "The baseline bias term when all feature inputs are zero"
        }
    ],
    "numerical_example": "Solving the Classic XOR Gate with a Feature Cross:\nFour binary observations that no single straight line can separate:\n• Point 1: [x₁ = 0, x₂ = 0] → Label y = 0\n• Point 2: [x₁ = 1, x₂ = 0] → Label y = 1\n• Point 3: [x₁ = 0, x₂ = 1] → Label y = 1\n• Point 4: [x₁ = 1, x₂ = 1] → Label y = 0\n\n1. Standard Linear Model (Failure):\n   ŷ = w₁·x₁ + w₂·x₂ + w₀. Points 2 and 3 force positive weights (w₁ > 0, w₂ > 0). When both inputs are 1 (Point 4), ŷ = w₁ + w₂ + w₀ > 0 (predicts y = 1, which is WRONG!). A linear plane cannot isolate the diagonal.\n\n2. Add Multiplicative Feature Cross: x₃ = x₁ · x₂\n   • Point 1: [x₁=0, x₂=0, x₃=0]\n   • Point 2: [x₁=1, x₂=0, x₃=0]\n   • Point 3: [x₁=0, x₂=1, x₃=0]\n   • Point 4: [x₁=1, x₂=1, x₃=1]\n\n3. Evaluate Solved Linear Model: Let w₀ = -0.5, w₁ = +1.0, w₂ = +1.0, w₃ = -2.0\n   • Point 1 (0, 0): -0.5 + 0 + 0 + 0 = -0.5 ≤ 0 → Predicts 0 (Correct!)\n   • Point 2 (1, 0): -0.5 + 1.0 + 0 + 0 = +0.5 > 0 → Predicts 1 (Correct!)\n   • Point 3 (0, 1): -0.5 + 0 + 1.0 + 0 = +0.5 > 0 → Predicts 1 (Correct!)\n   • Point 4 (1, 1): -0.5 + 1.0 + 1.0 - 2.0 = -0.5 ≤ 0 → Predicts 0 (Correct!)\n\nOutcome: The cross term x₁·x₂ enables a lightweight linear classifier to solve the non-linear XOR problem with 100% accuracy.",
    "pitfalls": "Common Pitfall: Blindly crossing high-cardinality features without regularization. Crossing 1,000 postal codes with 1,000 product categories generates 1,000,000 binary features. If a specific cross appears only once in the entire dataset, a model can memorize that single record, leading to catastrophic overfitting and Out-Of-Memory (OOM) crashes. Always pair large feature crosses with L1 regularization or the Hashing Trick.",
    "core_logic": "Why this matters: Real-world physical, biological, and economic phenomena are rarely additive; variables amplify or inhibit each other conditionally. Feature crosses allow linear models to capture these non-linear synergies while preserving sub-millisecond scoring latencies.",
    "architectural_logic": "In enterprise recommendation and ad-ranking architectures (e.g. Google's Wide & Deep, Deep & Cross Networks), explicit feature crosses are stored in sparse feature stores or hashed via MurmurHash. The linear 'wide' component memorizes high-value specific historical conjunctions while deep embedding layers generalize across unseen pairs.",
    "connected_logic": [
        {
            "title": "Click-Through Rate (CTR) & Ad Ranking Systems",
            "content": "• In search advertising, click likelihood depends on the precise pairing of user query intent and ad creative (e.g. 'Query=Running Shoes' × 'AdCategory=Footwear').\n• Crossing billions of ad-query pairs powered Google's Wide & Deep architecture, allowing memorization of lucrative historical combinations while deep layers generalize."
        },
        {
            "title": "Geospatial Real Estate & Hyperlocal Neighborhoods",
            "content": "• Neither high latitude nor high longitude alone dictates real estate prices; expensive luxury zones (e.g. San Francisco or Manhattan) exist only at specific coordinate intersections.\n• Crossing binned latitude with binned longitude creates distinct neighborhood grid tiles, enabling linear valuation models to price zip codes without complex non-linear spatial kernels."
        },
        {
            "title": "Feature Interaction in Tree Ensembles vs. Linear Models",
            "content": "• While decision trees naturally capture interactions through sequential branch splits (e.g. first splitting on Age, then on Income), tree depth restricts higher-order crosses.\n• Explicitly providing feature crosses gives linear models and shallow trees direct shortcuts to key interactions, saving tree depth budget and reducing training latency."
        },
        {
            "title": "Deep & Cross Networks (DCN) & Explicit High-Order Bounding",
            "content": "• Standard deep neural networks learn implicit non-linear interactions across dense layers, but lack explicit bounded polynomial interaction degrees.\n• Deep & Cross Networks (DCN) introduce explicit cross layers where x_(l+1) = x_0 · x_l^T · w_l + b_l + x_l, calculating bounded degree-d feature interactions efficiently without combinatorial column explosion."
        }
    ],
    "key_takeaways": [
        "Non-Linear Synergy: Multiplicatively combines features to capture conditional interactions that simple addition cannot represent.",
        "XOR Solver: Enables fast linear models to separate non-linear diagonal data distributions by adding interaction dimensions.",
        "Combinatorial Explosion Risk: Crossing high-cardinality features causes sparse feature bloat; must be controlled via L1 regularization or feature hashing.",
        "Production Recommenders: Core component of Google's Wide & Deep and DCN systems, balancing memorization of specific crosses with general neural embeddings."
    ],
    "definition_bullets": [
        "Feature Cross: A synthetic feature created by multiplying or conjoining two or more individual features to capture their non-linear interaction.",
        "Cartesian Conjunction: The set of all pairwise combination buckets generated by crossing two discrete categorical or binned features."
    ]
}

def update_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    found = False
    for item in data:
        if item.get('id') == 'concept_feature_crosses':
            item.update(FEATURE_CROSSES_UPDATE)
            found = True
            break
            
    if not found:
        print(f"Warning: concept_feature_crosses not found in {filepath}")
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
        if item.get('id') == 'concept_feature_crosses':
            item.update(FEATURE_CROSSES_UPDATE)
            break
            
    new_content = '"""\nConcepts Database: Data Preparation & Exploration (22 Concepts)\n"""\n\nDATA_CONCEPTS = ' + json.dumps(mod.DATA_CONCEPTS, indent=4, ensure_ascii=False) + '\n'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Successfully updated {filepath}")

update_concepts_data_prep()
