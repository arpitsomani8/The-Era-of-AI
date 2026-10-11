import json

MULTI_HOT_ENCODING_UPDATE = {
    "def": "Multi-Hot Encoding converts records with multiple co-occurring categories (such as tags, genres, or skills) into a single binary vector where multiple positions can be active (1) simultaneously.",
    "definition": "Multi-Hot Encoding converts records with multiple co-occurring categories (such as tags, genres, or skills) into a single binary vector where multiple positions can be active (1) simultaneously.",
    "formula": "$$\\mathbf{v}_i = \\sum_{c \\in \\mathcal{S}_i} \\mathbf{e}_c \\in \\{0, 1\\}^K, \\quad \\hat{y}_k = \\sigma(\\mathbf{w}_k^T \\mathbf{x} + b_k) = \\frac{1}{1 + e^{-(\\mathbf{w}_k^T \\mathbf{x} + b_k)}}$$",
    "formula_explanation": "",
    "logic": "Unlike One-Hot Encoding where classes are mutually exclusive (row sum strictly equals 1), Multi-Hot Encoding allows multiple categories to be true simultaneously. In multi-label neural networks, this architecture pairs with independent Sigmoid output heads and Binary Cross-Entropy loss across each tag neuron.",
    "example": "Movie streaming catalog: A film tagged as both Sci-Fi and Comedy is encoded over a 5-genre vocabulary as [Action:0, Comedy:1, Drama:0, Horror:0, Sci-Fi:1]. The model predicts independent probabilities for both genres without forcing them to compete.",
    "simple_summary": "While One-Hot Encoding allows only one active choice (row sum = 1), Multi-Hot Encoding lets a single record have multiple active tags at the same time (like a movie being both Comedy and Sci-Fi). In neural networks, it powers Multi-Label classification using independent Sigmoid neurons and Binary Cross-Entropy loss so tags don't cannibalize each other.",
    "core_terms": [
        {
            "term": "Multi-Hot Encoding (MultiLabelBinarizer)",
            "what_is_it": "• A feature encoding technique that converts lists or sets of multiple categorical tags into a single binary vector of 0s and 1s.\n• Unlike One-Hot Encoding where only one position is active (1), Multi-Hot Encoding allows multiple positions to be 1 simultaneously to represent all co-occurring attributes.",
            "analogy": "Selecting toppings at an ice cream shop: you are not forced to choose only chocolate OR sprinkles—you can check both boxes (Chocolate=1, Sprinkles=1, Cherries=0).",
            "why_it_matters": "Essential for modeling entities that naturally possess multiple attributes at once, such as movie genres, user skill sets, or medical symptoms."
        },
        {
            "term": "Multi-Class vs. Multi-Label Architecture",
            "what_is_it": "• Multi-Class predicts exactly one mutually exclusive category using a Softmax output layer where probabilities sum to 1.0.\n• Multi-Label predicts multiple co-occurring tags simultaneously, requiring independent Sigmoid activations on every output neuron and Binary Cross-Entropy loss across each tag.",
            "analogy": "A multiple-choice exam where only one answer is correct versus a checklist questionnaire where you can check 'all options that apply'.",
            "why_it_matters": "Prevents catastrophic architectural mistakes in neural networks: using Softmax on multi-label targets forces probabilities to compete against each other instead of predicting independently."
        },
        {
            "term": "Binary Bag-of-Words & Sparse Vectors",
            "what_is_it": "• The representation of text documents or large tag sets where a vocabulary of K words is mapped to a vector of 1s (word present) and 0s (word absent).\n• When vocabularies grow to tens of thousands of tokens, multi-hot vectors become 99.9% zeros, requiring sparse matrices or PyTorch's nn.EmbeddingBag to save memory.",
            "analogy": "A library catalog card marking which reference topics a book covers out of a master collection of 10,000 subjects.",
            "why_it_matters": "Bridges tabular categorical feature engineering with foundational Natural Language Processing and modern recommendation systems."
        }
    ],
    "types_header": "Encoding Tools & Multi-Label Network Layers",
    "types_badge": "Multi-Label Engineering",
    "quick_types": [
        {
            "type": "MultiLabelBinarizer",
            "definition": "Scikit-Learn transformer converting an iterable of iterables (lists of tags) into a 2D binary matrix.",
            "looks_like": "MultiLabelBinarizer().fit_transform(df['tags'])"
        },
        {
            "type": "Binary CountVectorizer",
            "definition": "NLP text vectorizer setting binary=True to produce binary multi-hot Bag-of-Words vectors.",
            "looks_like": "CountVectorizer(binary=True).fit_transform(corpus)"
        },
        {
            "type": "Multi-Label Sigmoid Head",
            "definition": "Neural network classification architecture applying independent Sigmoid units across output classes.",
            "looks_like": "outputs = torch.sigmoid(model(inputs))"
        },
        {
            "type": "BCEWithLogitsLoss",
            "definition": "PyTorch loss function computing Binary Cross-Entropy independently across all multi-hot target tags.",
            "looks_like": "nn.BCEWithLogitsLoss()(logits, multi_hot_targets)"
        },
        {
            "type": "nn.EmbeddingBag (Dense Aggregation)",
            "definition": "PyTorch module mapping sparse multi-hot tag indices to a single pooled dense vector via sum or mean.",
            "looks_like": "nn.EmbeddingBag(num_tags, dim, mode='mean')"
        }
    ],
    "symbol_guide": [
        {
            "symbol": "v_i",
            "meaning": "Multi-Hot Binary Vector",
            "plain_english": "The K-dimensional vector representing the combined active tags for record i"
        },
        {
            "symbol": "S_i",
            "meaning": "Active Tag Set",
            "plain_english": "The subset of categorical labels associated with instance i, e.g. {'Sci-Fi', 'Comedy'}"
        },
        {
            "symbol": "e_c",
            "meaning": "Standard Basis Vector",
            "plain_english": "The unit one-hot vector with a 1 at index c and 0 across all other indices"
        },
        {
            "symbol": "K",
            "meaning": "Vocabulary Size",
            "plain_english": "The total number of unique tags across the global catalog"
        },
        {
            "symbol": "ŷ_k (y_hat_k)",
            "meaning": "Predicted Tag Probability",
            "plain_english": "Independent sigmoid probability indicating whether tag k is present"
        },
        {
            "symbol": "σ (sigma)",
            "meaning": "Sigmoid Activation",
            "plain_english": "The logistic function converting raw logit scores to independent [0, 1] probabilities"
        }
    ],
    "numerical_example": "Encoding Multi-Genre Movies Across a 5-Genre Vocabulary:\nVocabulary (K = 5): [c₁='Action', c₂='Comedy', c₃='Drama', c₄='Horror', c₅='Sci-Fi']\n\n1. Movie 1 ('Spaceballs'): Tags = {'Comedy', 'Sci-Fi'}\n   • Binary Encoding: [Action:0, Comedy:1, Drama:0, Horror:0, Sci-Fi:1]\n   • Vector v₁ = [0, 1, 0, 0, 1] (Row sum = 2)\n\n2. Movie 2 ('The Godfather'): Tags = {'Drama'}\n   • Binary Encoding: [Action:0, Comedy:0, Drama:1, Horror:0, Sci-Fi:0]\n   • Vector v₂ = [0, 0, 1, 0, 0] (Row sum = 1)\n\n3. Neural Network Multi-Label Output (Independent Sigmoids on Movie 1):\n   Raw model logits z = [-2.1, +3.4, -1.8, -4.0, +2.9]\n   • Action: P = σ(-2.1) = 1 / (1 + e^(+2.1)) ≈ 0.11\n   • Comedy: P = σ(+3.4) = 1 / (1 + e^(-3.4)) ≈ 0.97 (Predicted Positive!)\n   • Drama:  P = σ(-1.8) = 1 / (1 + e^(+1.8)) ≈ 0.14\n   • Horror: P = σ(-4.0) = 1 / (1 + e^(+4.0)) ≈ 0.02\n   • Sci-Fi: P = σ(+2.9) = 1 / (1 + e^(-2.9)) ≈ 0.95 (Predicted Positive!)\n   Total sum of probabilities = 0.11 + 0.97 + 0.14 + 0.02 + 0.95 = 2.19 (unconstrained by zero-sum rules!).",
    "pitfalls": "Common Pitfall: Using a Softmax activation layer with Multi-Hot encoded targets. Softmax forces the entire output probability distribution to sum to 1.0, meaning that recognizing 'Comedy' actively cannibalizes and suppresses the probability of 'Sci-Fi'. Multi-Label tasks must always use independent Sigmoid activations and Binary Cross-Entropy loss across each tag neuron.",
    "core_logic": "Why this matters: Real-world entities (documents, products, medical patients) routinely carry multiple non-exclusive descriptors simultaneously. Multi-Hot encoding preserves all active descriptors within a fixed-width vector space, enabling models to learn overlapping categorical representations.",
    "architectural_logic": "In enterprise recommendation and retrieval systems, multi-hot features are converted to integer index lists and passed into PyTorch's nn.EmbeddingBag. The module retrieves low-dimensional dense embeddings for active tags and averages them directly on GPU memory, avoiding the allocation of massive sparse binary matrices.",
    "connected_logic": [
        {
            "title": "Recommender User Profiles & Candidate Retrieval",
            "content": "• In recommendation platforms (Netflix, YouTube), user interest profiles consist of dynamic, open-ended sets of historical topics and watched video tags.\n• Multi-hot representation allows dual-encoder two-tower networks to pool user preferences into fixed-size representations, matching candidate item embeddings via dot-product similarity."
        },
        {
            "title": "Sigmoid Decoupling vs. Softmax Probability Cannibalization",
            "content": "• Softmax normalizes activations by the denominator ∑ e^(z_i), forcing classes into zero-sum competition where increasing the probability of one tag directly suppresses all others.\n• Multi-label classification strictly requires independent Sigmoid units (σ(z_k)), allowing a movie to score 0.95 in Comedy and 0.92 in Sci-Fi without penalizing either genre."
        },
        {
            "title": "High-Cardinality Memory Exhaustion & EmbeddingBag",
            "content": "• When tags scale to tens of thousands of product attributes or medical codes, allocating multi-hot floating point arrays consumes gigabytes of memory.\n• Modern deep learning architectures replace dense multi-hot vectors with PyTorch's nn.EmbeddingBag, looking up only the active integer IDs and summing their low-dimensional embeddings directly in CUDA memory."
        },
        {
            "title": "Strict Vocabulary Freezing & Out-of-Vocabulary Tags",
            "content": "• Fitting MultiLabelBinarizer dynamically on test batches creates schema dimension mismatches if test records introduce novel tags or omit rare training classes.\n• In enterprise pipelines, the tag vocabulary is fixed on the training set, and unseen inference tags are systematically filtered using an explicit vocabulary lookup or mapped to an 'unknown_tag' index."
        }
    ],
    "key_takeaways": [
        "Multiple Active Labels: Represents non-mutually-exclusive categories where multiple positions are set to 1 simultaneously (row sum ≥ 0).",
        "Multi-Label Classification Head: Requires independent Sigmoid output neurons and Binary Cross-Entropy loss, not Softmax.",
        "Binary Bag-of-Words: Foundational representation in NLP for document-level vocabulary presence vectors.",
        "EmbeddingBag Optimization: High-cardinality multi-hot tag sets are efficiently pooled into dense vectors using nn.EmbeddingBag."
    ],
    "definition_bullets": [
        "Multi-Hot Encoding: A categorical encoding strategy mapping a set of co-occurring labels to a binary vector with multiple active 1s.",
        "Multi-Label Classification: A machine learning paradigm where an instance can be simultaneously assigned to zero, one, or multiple target classes."
    ]
}

def update_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    found = False
    for item in data:
        if item.get('id') == 'concept_multi_hot_encoding':
            item.update(MULTI_HOT_ENCODING_UPDATE)
            found = True
            break
            
    if not found:
        print(f"Warning: concept_multi_hot_encoding not found in {filepath}")
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
        if item.get('id') == 'concept_multi_hot_encoding':
            item.update(MULTI_HOT_ENCODING_UPDATE)
            break
            
    new_content = '"""\nConcepts Database: Data Preparation & Exploration (22 Concepts)\n"""\n\nDATA_CONCEPTS = ' + json.dumps(mod.DATA_CONCEPTS, indent=4, ensure_ascii=False) + '\n'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Successfully updated {filepath}")

update_concepts_data_prep()
