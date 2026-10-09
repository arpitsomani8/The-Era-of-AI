import json

ONE_HOT_ENCODING_UPDATE = {
    "def": "One-Hot Encoding (OHE) converts nominal categorical data into a set of binary indicator columns (0s and 1s), representing each unique category as an orthogonal, equidistant vector without imposing false numerical order.",
    "definition": "One-Hot Encoding (OHE) converts nominal categorical data into a set of binary indicator columns (0s and 1s), representing each unique category as an orthogonal, equidistant vector without imposing false numerical order.",
    "formula": "$$\\mathbf{x}_i \\in \\{c_1, \\dots, c_K\\} \\implies \\mathbf{e}_k = [0, \\dots, \\underbrace{1}_{k\\text{-th}}, \\dots, 0]^T \\in \\{0, 1\\}^K, \\quad d(\\mathbf{e}_j, \\mathbf{e}_k) = \\sqrt{2} \\quad (j \\neq k)$$",
    "formula_explanation": "",
    "logic": "Assigning arbitrary numbers to unordered categories (e.g. Red=1, Green=2, Blue=3) fools machine learning algorithms into assuming mathematical order (Blue > Red) and distance. One-hot encoding creates independent binary dimensions where every category is mutually orthogonal and equidistant (distance = √2).",
    "example": "Car color classification: Converting ['Red', 'Blue', 'Green'] into three distinct binary columns: `color_Blue`, `color_Green`, and `color_Red`. A green car is encoded as [0, 1, 0], ensuring no artificial hierarchy is learned by linear or neural models.",
    "simple_summary": "One-Hot Encoding turns text categories into binary columns of 0s and 1s, giving each unique choice its own column where only one column is 'hot' (1) at a time. It prevents models from making up fake rankings (like thinking Blue=3 is bigger than Red=1). For Linear Regression, always drop the first column to prevent mathematical crashes; for production pipelines, always use Scikit-Learn with handle_unknown='ignore'.",
    "core_terms": [
        {
            "term": "One-Hot Encoding (OHE)",
            "what_is_it": "• A method that converts nominal text categories into binary columns (0s and 1s), allocating an individual column for each unique category.\n• For any given row, exactly one column receives a 1 ('hot') while all others receive a 0 ('cold'), treating every category as an independent, equal dimension.",
            "analogy": "A voting ballot where each political candidate has their own checkbox: you place a single checkmark (1) next to your chosen candidate and leave all others blank (0).",
            "why_it_matters": "Prevents algorithms from hallucinating fake rankings (such as assuming 'Red=1, Green=2, Blue=3' means Blue is three times greater than Red)."
        },
        {
            "term": "The Dummy Variable Trap (Multicollinearity)",
            "what_is_it": "• A linear dependency problem where including all K binary columns creates perfect redundancy, because knowing K-1 columns always reveals the state of the final column (they sum to 1).\n• In linear and logistic regression, this creates a singular matrix that breaks mathematical inversion; resolved by dropping one baseline reference column (drop='first').",
            "analogy": "A coin toss record: if you record both 'Is_Heads' and 'Is_Tails', the second column provides zero new information—if Is_Heads is 0, it must be Tails!",
            "why_it_matters": "Essential for linear models to avoid mathematically singular design matrices, whereas tree models and neural nets safely retain all K columns."
        },
        {
            "term": "The High-Cardinality Explosion",
            "what_is_it": "• The architectural pitfall of applying OHE to features with hundreds or thousands of unique values (such as Zip Codes, User IDs, or Product SKUs).\n• Expands the dataset into a massive, highly sparse matrix that balloons memory consumption, slows down training, and causes decision trees to overfit.",
            "analogy": "Building a separate 50-lane highway with an individual dedicated lane for every single car brand in town rather than sharing general traffic lanes.",
            "why_it_matters": "Defines the boundary for OHE: use OHE for categories with under 50 values; switch to Target Encoding, Count Encoding, or Entity Embeddings for high cardinality."
        }
    ],
    "types_header": "Implementation Flavors & Production Encoders",
    "types_badge": "Encoding Strategies",
    "quick_types": [
        {
            "type": "OneHotEncoder(drop='first')",
            "definition": "Scikit-Learn configuration dropping the first level to avoid the dummy variable trap in linear models.",
            "looks_like": "OneHotEncoder(drop='first', sparse_output=False)"
        },
        {
            "type": "OneHotEncoder(handle_unknown='ignore')",
            "definition": "Production setting returning an all-zero vector for unseen test categories rather than crashing with an error.",
            "looks_like": "OneHotEncoder(handle_unknown='ignore')"
        },
        {
            "type": "pd.get_dummies() (Notebook EDA)",
            "definition": "Quick Pandas function for rapid exploratory analysis; unsuitable for production pipelines due to lack of state.",
            "looks_like": "df_ohe = pd.get_dummies(df['color'])"
        },
        {
            "type": "Target / Mean Encoding (> 50 Levels)",
            "definition": "High-cardinality alternative replacing categories with conditional target averages to prevent column explosion.",
            "looks_like": "TargetEncoder().fit_transform(X, y)"
        },
        {
            "type": "Entity Embeddings (Deep Learning)",
            "definition": "Neural network embedding layer mapping high-cardinality categories to dense, continuous vector spaces.",
            "looks_like": "nn.Embedding(num_categories, embedding_dim)"
        }
    ],
    "symbol_guide": [
        {
            "symbol": "x_i",
            "meaning": "Categorical Feature Input",
            "plain_english": "The raw nominal category observed for instance i, such as 'Red' or 'Berlin'"
        },
        {
            "symbol": "c_k",
            "meaning": "Category Level k",
            "plain_english": "One of the K distinct unique categories identified in the training feature"
        },
        {
            "symbol": "e_k",
            "meaning": "One-Hot Binary Vector",
            "plain_english": "A K-dimensional vector containing a 1 at index k and 0 across all other indices"
        },
        {
            "symbol": "K",
            "meaning": "Category Cardinality",
            "plain_english": "The total count of unique categorical values discovered in that column"
        },
        {
            "symbol": "d(e_j, e_k)",
            "meaning": "Pairwise Euclidean Distance",
            "plain_english": "The constant geometric separation of √2 (≈ 1.414) between any two distinct one-hot categories"
        }
    ],
    "numerical_example": "Encoding Automobile Colors Across 4 Vehicles: ['Red', 'Blue', 'Green', 'Red']\n\n1. Identify Unique Categories (Alphabetical ordering, K = 3):\n   • c₁ = 'Blue', c₂ = 'Green', c₃ = 'Red'\n\n2. Construct Full K-Dimensional One-Hot Vectors:\n   • Vehicle 1 ('Red'):   [Blue=0, Green=0, Red=1]\n   • Vehicle 2 ('Blue'):  [Blue=1, Green=0, Red=0]\n   • Vehicle 3 ('Green'): [Blue=0, Green=1, Red=0]\n   • Vehicle 4 ('Red'):   [Blue=0, Green=0, Red=1]\n\n3. Calculate Metric Distance Between Colors:\n   • Distance(Red, Blue) = √[(0 - 1)² + (0 - 0)² + (1 - 0)²] = √[1 + 0 + 1] = √2 ≈ 1.414\n   • Distance(Red, Green) = √[(0 - 0)² + (0 - 1)² + (1 - 0)²] = √2 ≈ 1.414\n   • Distance(Blue, Green) = √[(1 - 0)² + (0 - 1)² + (0 - 0)²] = √2 ≈ 1.414\n   (Every color is equidistant: no false hierarchies or unequal proximities!)\n\n4. Drop-First Formulation for Linear Regression (K - 1 = 2 columns, 'Blue' as reference):\n   • Vehicle 1 ('Red'):   [Green=0, Red=1]\n   • Vehicle 2 ('Blue'):  [Green=0, Red=0] (captured completely by the model intercept!)\n   • Vehicle 3 ('Green'): [Green=1, Red=0]",
    "pitfalls": "Common Pitfall: Using pandas.get_dummies() in production inference pipelines. get_dummies() is stateless; if a production batch lacks one of the training categories, it silently drops that column, altering feature dimensions and crashing the model. Always use Scikit-Learn's OneHotEncoder(handle_unknown='ignore') and fit it strictly on the training partition.",
    "core_logic": "Why this matters: Machine learning models operate on geometry and algebra. Integer encoding nominal categories creates artificial linear ordering and false distances. One-Hot Encoding preserves metric neutrality by embedding categories onto an orthogonal basis where every class is equidistant.",
    "architectural_logic": "In production ML systems, OneHotEncoder is bundled inside a Scikit-Learn ColumnTransformer or Feature Store pipeline. It is configured with handle_unknown='ignore' and sparse_output=True to safeguard inference endpoints against unseen categorical levels and optimize memory usage.",
    "connected_logic": [
        {
            "title": "Orthogonality & Equidistant Metric Space",
            "content": "• In distance-based algorithms (KNN, K-Means) and dot-product models (SVM, Perceptrons), integer encoding (Red=1, Green=2, Blue=3) forces Blue to be twice as far from Red as Green is.\n• One-hot vectors are mutually orthogonal unit basis vectors (e_j^T e_k = 0), ensuring every category pair is geometrically equidistant (d = √2), preserving objective metric neutrality."
        },
        {
            "title": "The Production Serving Failure of pd.get_dummies()",
            "content": "• Pandas get_dummies() is a stateless function that inspects only the batch currently residing in local memory.\n• If a production inference batch contains only a subset of categories or introduces an unseen category, get_dummies() alters the column count and ordering, immediately crashing model inference."
        },
        {
            "title": "Tree-Based Model Sparsity & Split Dilution",
            "content": "• When high-cardinality features are one-hot encoded into hundreds of binary columns, decision trees must evaluate hundreds of sparse, low-information splits.\n• This fragments the training data into tiny leaves, degrading tree depth efficiency and causing gradient boosted trees (XGBoost, LightGBM) to severely overfit compared to native categorical binning."
        },
        {
            "title": "Sparse Matrix Storage & Memory Efficiency",
            "content": "• Encoding dozens of categorical columns with moderate cardinality can easily generate thousands of columns that are 99% zeros.\n• Scikit-Learn's OneHotEncoder defaults to sparse_output=True (Scipy CSR matrix), storing only non-zero coordinates and preventing gigabytes of empty float allocations from crashing server RAM."
        }
    ],
    "key_takeaways": [
        "Metric Neutrality: Maps nominal categories onto an orthogonal basis where all categories are equidistant (distance = √2).",
        "Linear Model Prerequisite: Use drop='first' in unregularized linear regression to avoid the dummy variable trap and singular matrix crashes.",
        "Production Guardrail: Use Scikit-Learn OneHotEncoder(handle_unknown='ignore') rather than stateless pd.get_dummies to prevent production pipeline schema mismatches.",
        "Cardinality Boundary: Reserve OHE for categories with under 50 levels; switch to Target Encoding or Entity Embeddings for high cardinality."
    ],
    "definition_bullets": [
        "One-Hot Encoding: A categorical transformation that maps K nominal categories to K binary columns, setting exactly one column to 1 per instance.",
        "Dummy Variable Trap: A state of perfect multicollinearity occurring when all K binary indicator columns and an intercept term are included in linear models."
    ]
}

def update_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    found = False
    for item in data:
        if item.get('id') == 'concept_one_hot_encoding':
            item.update(ONE_HOT_ENCODING_UPDATE)
            found = True
            break
            
    if not found:
        print(f"Warning: concept_one_hot_encoding not found in {filepath}")
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
        if item.get('id') == 'concept_one_hot_encoding':
            item.update(ONE_HOT_ENCODING_UPDATE)
            break
            
    new_content = '"""\nConcepts Database: Data Preparation & Exploration (22 Concepts)\n"""\n\nDATA_CONCEPTS = ' + json.dumps(mod.DATA_CONCEPTS, indent=4, ensure_ascii=False) + '\n'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Successfully updated {filepath}")

update_concepts_data_prep()
