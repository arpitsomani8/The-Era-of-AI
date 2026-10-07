# scripts/curriculum_part_recsys.py
# 5 Recommender Systems Concepts

def get_recsys_concepts():
    topic_id = "ml_recsys"
    topic_label = "Recommender Systems (RecSys) & Retrieval Architecture"
    cat = "ml"
    cat_label = "Classical Machine Learning"

    return [
        {
            "id": "concept_collaborative_filtering_svd",
            "title": "Collaborative Filtering & Matrix Factorization (SVD & ALS)",
            "topic_id": topic_id, "topic_label": topic_label, "category": cat, "category_label": cat_label,
            "raw_subtopic": "Collaborative Filtering & Matrix Factorization (SVD & ALS)", "raw_sub": "Collaborative Filtering & Matrix Factorization (SVD & ALS)",
            "def": "The seminal recommendation methodology decomposing a sparse user-item interaction matrix R (size M x N) into low-rank latent user factors P and item factors Q via Singular Value Decomposition (SVD) or Alternating Least Squares (ALS).",
            "definition": "The seminal recommendation methodology decomposing a sparse user-item interaction matrix R (size M x N) into low-rank latent user factors P and item factors Q via Singular Value Decomposition (SVD) or Alternating Least Squares (ALS).",
            "formula": "$$\\min_{P, Q} \\sum_{(u,i) \\in \\mathcal{K}} (r_{ui} - p_u^T q_i)^2 + \\lambda (\\|p_u\\|_2^2 + \\|q_i\\|_2^2), \\quad \\hat{r}_{ui} = \\mu + b_u + b_i + p_u^T q_i$$",
            "formula_explanation": "",
            "logic": "Direct user-user similarity requires O(M^2) memory and fails on sparse 99.9% empty matrices. Matrix factorization compresses users and items into a shared d-dimensional latent embedding space, predicting missing interactions via dot products.",
            "core_logic": "Direct user-user similarity requires O(M^2) memory and fails on sparse 99.9% empty matrices. Matrix factorization compresses users and items into a shared d-dimensional latent embedding space, predicting missing interactions via dot products.",
            "architectural_logic": "",
            "example": "Netflix Prize ($1M challenge): Simon Funk's SVD algorithm decomposed 100M movie ratings into 50 latent factors (e.g. action intensity, comedic tone, director style) to predict unseen user ratings.",
            "tags": ["RecSys", "Matrix Factorization", "SVD", "ALS", "Collaborative Filtering"],
            "simple_summary": "Collaborative filtering recommends movies by finding people with similar tastes. Matrix factorization uncovers hidden taste profiles (like 'loves 80s sci-fi') and matches user preferences to movie attributes using dot products.",
            "core_terms": [
                {
                    "term": "User Latent Factors (p_u)",
                    "what_is_it": "A d-dimensional vector representing a user's hidden preference profile across latent genres and qualities.",
                    "analogy": "A flavor profile checklist: [sweet: 0.9, spicy: 0.1, salty: 0.7].",
                    "why_it_matters": "Summarizes thousands of historical clicks into a compact, continuous vector."
                },
                {
                    "term": "Item Latent Factors (q_i)",
                    "what_is_it": "A d-dimensional vector representing an item's manifestation of those same latent dimensions.",
                    "analogy": "A dish recipe profile: [sweet: 0.85, spicy: 0.05, salty: 0.65].",
                    "why_it_matters": "Direct dot product with p_u gives the predicted affinity score."
                },
                {
                    "term": "Alternating Least Squares (ALS)",
                    "what_is_it": "An optimization algorithm that fixes Q to solve for P with closed-form linear regression, then fixes P to solve for Q, alternating until convergence.",
                    "analogy": "Two partners taking turns adjusting furniture until both are satisfied with the room layout.",
                    "why_it_matters": "Embarrassingly parallelizable across distributed Spark clusters and naturally handles implicit feedback (clicks/views)."
                },
                {
                    "term": "Global and Entity Biases (b_u, b_i)",
                    "what_is_it": "Baseline deviations accounting for users who always rate harsh/generous, and items that are universally acclaimed/hated.",
                    "analogy": "A grumpy food critic whose average rating is 2 stars versus a blockbuster movie that everyone rates 5 stars.",
                    "why_it_matters": "Prevents rating style differences from distorting true latent taste alignment."
                }
            ],
            "symbol_guide": [
                {"symbol": "r_{ui}", "meaning": "Observed rating from user u for item i", "plain_english": "e.g. 5 stars or 1 (clicked)"},
                {"symbol": "p_u^T q_i", "meaning": "Dot product between user vector and item vector", "plain_english": "The personalized match score"},
                {"symbol": "\\lambda", "meaning": "L2 regularization penalty", "plain_english": "Prevents overfitting on users with very few ratings"}
            ],
            "numerical_example": "Baseline rating mu = 3.5. User bias b_u = -0.3 (harsh critic). Movie bias b_i = +0.5 (beloved classic). User vector p_u = [0.8, 0.2]. Movie vector q_i = [0.7, 0.4]. Dot product = (0.8×0.7) + (0.2×0.4) = 0.56 + 0.08 = 0.64. Predicted rating = 3.5 - 0.3 + 0.5 + 0.64 = 4.34 stars.",
            "pitfalls": "Novice Trap: Treating implicit feedback (clicks, watch time) as explicit ratings. A user not clicking an item doesn't mean they hate it—they probably never saw it! Standard squared loss must be replaced by weighted implicit ALS (Hu, Koren, Volinsky).",
            "key_takeaways": [],
            "definition_bullets": [
                "User Latent Factors: Dense embedding summarizing user preferences.",
                "Item Latent Factors: Dense embedding mapping item characteristics.",
                "Alternating Least Squares: Convex alternating optimization suitable for massive distributed clusters.",
                "Baseline Biases: Separating systemic rating tendencies from genuine personalized taste."
            ]
        },
        {
            "id": "concept_two_tower_retrieval",
            "title": "Two-Tower Neural Retrieval Architectures",
            "topic_id": topic_id, "topic_label": topic_label, "category": cat, "category_label": cat_label,
            "raw_subtopic": "Two-Tower Neural Retrieval Architectures", "raw_sub": "Two-Tower Neural Retrieval Architectures",
            "def": "A dual-encoder deep neural architecture featuring an independent User/Query Tower and Candidate/Item Tower that map disparate multimodal features into a shared metric embedding space optimized via in-batch negative contrastive loss for Approximate Nearest Neighbor (ANN) vector retrieval.",
            "definition": "A dual-encoder deep neural architecture featuring an independent User/Query Tower and Candidate/Item Tower that map disparate multimodal features into a shared metric embedding space optimized via in-batch negative contrastive loss for Approximate Nearest Neighbor (ANN) vector retrieval.",
            "formula": "$$\\text{Score}(u, i) = \\langle f_{\\theta}(x_u), g_{\\phi}(x_i) \\rangle, \\quad \\mathcal{L} = -\\sum_{u=1}^B \\log \\frac{\\exp(\\langle u, i^+ \\rangle / \\tau)}{\\sum_{j=1}^B \\exp(\\langle u, j \\rangle / \\tau)}$$",
            "formula_explanation": "",
            "logic": "Scoring 100 million items with a complex neural network is impossible in real time. The Two-Tower model decouples computation: item tower embeddings are pre-computed offline and indexed in FAISS/Pinecone; online inference requires only a single user tower forward pass followed by a 5ms sublinear vector search.",
            "core_logic": "Scoring 100 million items with a complex neural network is impossible in real time. The Two-Tower model decouples computation: item tower embeddings are pre-computed offline and indexed in FAISS/Pinecone; online inference requires only a single user tower forward pass followed by a 5ms sublinear vector search.",
            "architectural_logic": "",
            "example": "YouTube video candidate retrieval: User tower ingests watch history, search queries, and device info. Video tower ingests video title, channel, and thumbnail embeddings. Top 1,000 video candidates are retrieved from a catalog of 1 billion videos in under 10ms.",
            "tags": ["Two-Tower", "Candidate Retrieval", "Vector Search", "Contrastive Loss"],
            "simple_summary": "Two-Tower models use two separate neural networks: one encodes everything about the user, and the other encodes everything about the video or product. Because item vectors are calculated ahead of time, finding top recommendations takes milliseconds using vector search.",
            "core_terms": [
                {
                    "term": "Query / User Tower",
                    "what_is_it": "The neural network that encodes real-time context (user demographics, recent clicks, query string, time of day) into embedding vector u.",
                    "analogy": "A personal shopping assistant who learns what you are looking for today.",
                    "why_it_matters": "Runs in real time on every incoming search request or page refresh."
                },
                {
                    "term": "Candidate / Item Tower",
                    "what_is_it": "The neural network that encodes static and dynamic item features (product description, category, price, popularity) into embedding vector v.",
                    "analogy": "A warehouse catalog tagger stamping a flavor barcode on every item on the shelves.",
                    "why_it_matters": "Runs offline in batch; billions of items can be indexed without slowing down user requests."
                },
                {
                    "term": "In-Batch Negatives",
                    "what_is_it": "Using the positive items of other users in the same training mini-batch as negative items for user u.",
                    "analogy": "Assuming that the shoes your classmate bought are not what you are shopping for today.",
                    "why_it_matters": "Provides thousands of negative training examples for free without expensive negative sampling."
                },
                {
                    "term": "Approximate Nearest Neighbor (ANN)",
                    "what_is_it": "Vector indexing structures (HNSW, IVF-PQ) that find vectors with highest dot product in O(log N) sublinear time.",
                    "analogy": "Looking up a topic in a library index card catalog rather than inspecting every single book on every shelf.",
                    "why_it_matters": "Enables millisecond retrieval across catalogs of 100 million+ items."
                }
            ],
            "symbol_guide": [
                {"symbol": "f_\\theta(x_u)", "meaning": "User tower embedding output (size d)", "plain_english": "e.g. 128-dimensional user vector"},
                {"symbol": "g_\\phi(x_i)", "meaning": "Item tower embedding output (size d)", "plain_english": "e.g. 128-dimensional item vector"},
                {"symbol": "\\tau", "meaning": "Softmax temperature parameter", "plain_english": "Scales logits to calibrate prediction confidence"}
            ],
            "numerical_example": "Batch size B = 512. Computing all pairwise dot products yields a [512, 512] similarity matrix. Diagonal elements are positive user-item pairs; all 512 × 511 off-diagonal elements serve as in-batch negative pairs. Softmax cross-entropy trains the user tower to push diagonal values close to 1.0 and off-diagonals to 0.0.",
            "pitfalls": "Novice Trap: Adding cross-features that combine user and item information (e.g. 'user_age minus item_target_age') inside the towers. Doing this destroys the independence between towers and makes offline pre-computation impossible!",
            "key_takeaways": [],
            "definition_bullets": [
                "User Tower: Computes online user query embeddings from real-time session context.",
                "Item Tower: Generates offline item embeddings stored in vector index databases.",
                "In-Batch Negatives: Efficient contrastive training using concurrent batch samples as negatives.",
                "ANN Retrieval: Sublinear logarithmic search finding top candidate matches in milliseconds."
            ]
        },
        {
            "id": "concept_deep_cross_wide_deep",
            "title": "Deep & Cross Networks (DCN) & Wide & Deep Learning",
            "topic_id": topic_id, "topic_label": topic_label, "category": cat, "category_label": cat_label,
            "raw_subtopic": "Deep & Cross Networks (DCN) & Wide & Deep Learning", "raw_sub": "Deep & Cross Networks (DCN) & Wide & Deep Learning",
            "def": "Production click-through rate (CTR) prediction architectures that jointly train a linear memorization component with a deep representation component (Wide & Deep), extended by explicit polynomial feature crossing layers (DCN-v2) without manual feature engineering.",
            "definition": "Production click-through rate (CTR) prediction architectures that jointly train a linear memorization component with a deep representation component (Wide & Deep), extended by explicit polynomial feature crossing layers (DCN-v2) without manual feature engineering.",
            "formula": "$$\\text{Wide & Deep}: P(Y=1|x) = \\sigma(w^T [x, \\phi(x)] + w_{\\text{deep}}^T a^{(L)} + b), \\quad \\text{DCN Cross Layer}: x_{l+1} = x_0 x_l^T w_l + b_l + x_l$$",
            "formula_explanation": "",
            "logic": "Standard feedforward layers implicitly approximate feature interactions, but are inefficient at learning degree-2 and degree-3 polynomial combinations (e.g. 'device=iOS AND app=TikTok AND hour=22'). The Cross network explicitly computes bounded degree interactions at each layer with linear parameter complexity.",
            "core_logic": "Standard feedforward layers implicitly approximate feature interactions, but are inefficient at learning degree-2 and degree-3 polynomial combinations (e.g. 'device=iOS AND app=TikTok AND hour=22'). The Cross network explicitly computes bounded degree interactions at each layer with linear parameter complexity.",
            "architectural_logic": "",
            "example": "Google Play App Store recommendations: Wide linear model memorizes specific historical co-occurrence rules ('install Netflix -> install Hulu'), while the Deep MLP generalizes to novel apps via embedding similarities.",
            "tags": ["Wide & Deep", "DCN", "CTR Prediction", "Feature Crossing"],
            "simple_summary": "Wide & Deep combines two brains: the 'Wide' brain is an elephant that memorizes specific past combinations that worked, while the 'Deep' brain is an explorer that generalizes to new things. DCN automatically multiplies features together to find winning recipes.",
            "core_terms": [
                {
                    "term": "Memorization (Wide Component)",
                    "what_is_it": "A generalized linear model trained on sparse categorical features and cross-product transformations.",
                    "analogy": "A veteran grocer who knows that customers who buy beer on Friday always buy potato chips.",
                    "why_it_matters": "Directly captures strong historical rules with high confidence."
                },
                {
                    "term": "Generalization (Deep Component)",
                    "what_is_it": "A multi-layer perceptron (MLP) trained on dense continuous embeddings of categorical features.",
                    "analogy": "A sommelier suggesting a wine you've never tried because it shares tasting notes with wines you like.",
                    "why_it_matters": "Recommends relevant items that have zero historical co-occurrence data."
                },
                {
                    "term": "Cross Network Layer (x_{l+1})",
                    "what_is_it": "A layer that multiplies the original input x_0 by the current layer output x_l, creating polynomial interaction terms.",
                    "analogy": "Mixing three primary colors to get secondary and tertiary colors systematically.",
                    "why_it_matters": "Increases feature interaction degree by 1 at each layer with zero manual feature engineering."
                },
                {
                    "term": "Click-Through Rate (CTR)",
                    "what_is_it": "The probability that a user will click on an ad or recommended item: P(Click = 1 | User, Item, Context).",
                    "analogy": "The batting average of a baseball player.",
                    "why_it_matters": "The core revenue optimization metric for online advertising and e-commerce."
                }
            ],
            "symbol_guide": [
                {"symbol": "x_0", "meaning": "Raw concatenated input feature vector", "plain_english": "Initial user and item features"},
                {"symbol": "x_l", "meaning": "Output of cross layer l", "plain_english": "Accumulated feature crosses of degree l"},
                {"symbol": "\\phi(x)", "meaning": "Cross-product feature transformations", "plain_english": "Combinations like (Gender=F × Category=Shoes)"}
            ],
            "numerical_example": "Input feature vector x_0 of dimension 100. In standard MLP, learning degree-3 interactions requires huge layer widths. In DCN with 3 cross layers, layer 1 produces degree-2 crosses, layer 2 produces degree-3 crosses, and layer 3 produces degree-4 crosses. Total additional parameters = 3 × 100 = 300 weights, achieving 0.005 higher AUC in CTR prediction.",
            "pitfalls": "Novice Trap: Training the Wide and Deep components separately and averaging their predictions. Wide & Deep must be trained *jointly* with backpropagation so the Wide component only needs to memorize rare exception residuals that the Deep component misses.",
            "key_takeaways": [],
            "definition_bullets": [
                "Wide Component: Memorizes specific historical correlation rules.",
                "Deep Component: Generalizes to unseen user-item pairs via dense embeddings.",
                "Cross Layers: Automatically forms explicit polynomial feature combinations.",
                "Joint Optimization: Balances memorization precision with generalization diversity."
            ]
        },
        {
            "id": "concept_candidate_gen_vs_ranking",
            "title": "Candidate Generation vs Heavy Ranking Stages",
            "topic_id": topic_id, "topic_label": topic_label, "category": cat, "category_label": cat_label,
            "raw_subtopic": "Candidate Generation vs Heavy Ranking Stages", "raw_sub": "Candidate Generation vs Heavy Ranking Stages",
            "def": "The industry-standard multi-stage recommendation funnel that cascades from lightweight candidate retrieval (filtering 100M items down to 1,000 in 10ms) to heavy multi-task neural ranking, feature interaction modeling, and final business diversity reranking.",
            "definition": "The industry-standard multi-stage recommendation funnel that cascades from lightweight candidate retrieval (filtering 100M items down to 1,000 in 10ms) to heavy multi-task neural ranking, feature interaction modeling, and final business diversity reranking.",
            "formula": "$$\\text{Funnel}: N_{\\text{catalog}} (10^8) \\xrightarrow[\\text{ANN / Filtering}]{<10\\text{ms}} N_{\\text{candidates}} (10^3) \\xrightarrow[\\text{Deep Ranking}]{<30\\text{ms}} N_{\\text{scored}} (10^2) \\xrightarrow[\\text{Rerank / Diversity}]{<5\\text{ms}} K (10)$$",
            "formula_explanation": "",
            "logic": "No single model can balance global scale with granular scoring accuracy. Decoupling into a high-recall retrieval stage followed by a high-precision ranking stage satisfies real-world SLA latency budgets (<50ms end-to-end) while optimizing complex multi-task objectives.",
            "core_logic": "No single model can balance global scale with granular scoring accuracy. Decoupling into a high-recall retrieval stage followed by a high-precision ranking stage satisfies real-world SLA latency budgets (<50ms end-to-end) while optimizing complex multi-task objectives.",
            "architectural_logic": "",
            "example": "TikTok 'For You' Page: Ingests 500 million candidate videos. Candidate generation retrieves 2,000 videos from graph walk, collaborative filtering, and Two-Tower ANN. The Heavy Ranker scores 2,000 videos across 6 tasks (like, finish, comment, share). The Reranker deduplicates creators and ensures fresh variety.",
            "tags": ["RecSys Funnel", "Candidate Retrieval", "Heavy Ranking", "Reranking"],
            "simple_summary": "Recommending from 100 million items is like hiring for a company: first, an automated resume scanner filters 100,000 applicants down to 500 (Candidate Generation); next, senior interviewers conduct in-depth evaluations of those 500 (Ranking); finally, HR balances diversity and salary constraints for the top 5 (Reranking).",
            "core_terms": [
                {
                    "term": "Candidate Retrieval Stage",
                    "what_is_it": "High-recall, ultra-fast filtering that trims the entire catalog from millions down to hundreds using simple heuristics and vector search.",
                    "analogy": "Casting a wide fishing net across the ocean to catch a school of fish.",
                    "why_it_matters": "Prioritizes recall: if a great item is missed here, the ranker will never even see it."
                },
                {
                    "term": "Heavy Ranking Stage",
                    "what_is_it": "Complex deep neural networks (MMoE, DCN) utilizing thousands of real-time features to compute fine-grained engagement probabilities.",
                    "analogy": "A master chef carefully tasting and inspecting the fish to pick the single best cut for sashimi.",
                    "why_it_matters": "Prioritizes precision and calibration for accurate revenue/engagement ordering."
                },
                {
                    "term": "Reranking & Policy Layer",
                    "what_is_it": "The final stage applying business constraints: deduplication, author diversity, exploration slots, ad injection, and freshness boosts.",
                    "analogy": "An editor arranging the newspaper front page so it's not filled with 5 articles about the exact same story.",
                    "why_it_matters": "Prevents echo-chamber fatigue and balances user experience with monetization."
                },
                {
                    "term": "Multi-Gate Mixture-of-Experts (MMoE)",
                    "what_is_it": "A multi-task deep ranking architecture predicting multiple targets simultaneously (e.g. P(Click), P(Like), P(Share), P(Buy)).",
                    "analogy": "A panel of expert advisors where one predicts clicks, another predicts purchase intent, and a third predicts return rates.",
                    "why_it_matters": "Prevents optimizing only for clickbait by factoring in meaningful retention metrics."
                }
            ],
            "symbol_guide": [
                {"symbol": "N_{catalog}", "meaning": "Total item catalog universe", "plain_english": "e.g. 100,000,000 products or videos"},
                {"symbol": "N_{candidates}", "meaning": "Filtered candidate pool", "plain_english": "e.g. top 1,000 items passed to ranker"},
                {"symbol": "K", "meaning": "Final items displayed on screen", "plain_english": "e.g. 10 items shown on mobile carousel"}
            ],
            "numerical_example": "Catalog: 50,000,000 products. Stage 1: Two-Tower vector search + trending filter selects 800 candidates in 8ms. Stage 2: 12-layer DCN-v2 scores all 800 candidates using 1,200 real-time features in 22ms. Stage 3: Maximal Marginal Relevance (MMR) selects 12 diverse products across 4 categories in 2ms. Total pipeline latency = 32ms.",
            "pitfalls": "Novice Trap: Trying to run the heavy deep ranking model over the entire catalog. Scoring 10M items with an MLP takes minutes and crashes GPU memory; a multi-stage architecture is non-negotiable.",
            "key_takeaways": [],
            "definition_bullets": [
                "Candidate Retrieval: Fast, high-recall filtering reducing millions of items to hundreds.",
                "Heavy Ranking: Precision-optimized deep neural networks with rich cross-features.",
                "Reranking Layer: Enforcing diversity, business rules, freshness, and safety policies.",
                "Multi-Task Objectives: Balancing clicks, watch time, shares, and purchases simultaneously."
            ]
        },
        {
            "id": "concept_recsys_eval_ndcg_mrr",
            "title": "RecSys Evaluation Metrics: NDCG, MRR & Hit Rate@K",
            "topic_id": topic_id, "topic_label": topic_label, "category": cat, "category_label": cat_label,
            "raw_subtopic": "RecSys Evaluation Metrics: NDCG, MRR & Hit Rate@K", "raw_sub": "RecSys Evaluation Metrics: NDCG, MRR & Hit Rate@K",
            "def": "Ranking-specific offline evaluation metrics that quantify order sensitivity, positional decay, and relevance calibration across top-K recommendations, led by Normalized Discounted Cumulative Gain (NDCG), Mean Reciprocal Rank (MRR), and Hit Rate@K.",
            "definition": "Ranking-specific offline evaluation metrics that quantify order sensitivity, positional decay, and relevance calibration across top-K recommendations, led by Normalized Discounted Cumulative Gain (NDCG), Mean Reciprocal Rank (MRR), and Hit Rate@K.",
            "formula": "$$\\text{DCG@K} = \\sum_{i=1}^K \\frac{2^{rel_i} - 1}{\\log_2(i + 1)}, \\quad \\text{NDCG@K} = \\frac{\\text{DCG@K}}{\\text{IDCG@K}}, \\quad \\text{MRR} = \\frac{1}{|U|} \\sum_{u=1}^{|U|} \\frac{1}{\\text{rank}_u^*}$$",
            "formula_explanation": "",
            "logic": "Standard accuracy and MSE ignore user browsing behavior: users rarely scroll past item #5. NDCG discounts rewards logarithmically by screen position, penalizing models heavily if a highly relevant item is placed down at rank #10 instead of rank #1.",
            "core_logic": "Standard accuracy and MSE ignore user browsing behavior: users rarely scroll past item #5. NDCG discounts rewards logarithmically by screen position, penalizing models heavily if a highly relevant item is placed down at rank #10 instead of rank #1.",
            "architectural_logic": "",
            "example": "Search engine evaluation: A user searches for 'Python docs'. Model A places official docs at rank 1 (MRR = 1.0). Model B places docs at rank 4 (MRR = 1/4 = 0.25). NDCG@5 rewards Model A with a near-perfect 0.98 score while penalizing Model B to 0.42.",
            "tags": ["NDCG", "MRR", "Hit Rate", "Ranking Metrics", "Evaluation"],
            "simple_summary": "In search and feeds, position matters enormously—nobody clicks on item #10. NDCG gives you huge points if the best item is at #1, fewer points if it's at #3, and almost zero points if it's buried at the bottom.",
            "core_terms": [
                {
                    "term": "Cumulative Gain (CG)",
                    "what_is_it": "The raw sum of relevance scores of items in the top-K list, completely ignoring their position order.",
                    "analogy": "Counting the total number of gold coins in your bag regardless of where they are placed.",
                    "why_it_matters": "A baseline measure of total relevance quantity."
                },
                {
                    "term": "Discounted Cumulative Gain (DCG@K)",
                    "what_is_it": "Summing relevance scores divided by log2(position + 1), so rewards decay sharply down the list.",
                    "analogy": "A prize ceremony where 1st place gets $1,000, 2nd place gets $500, and 10th place gets $5.",
                    "why_it_matters": "Accurately reflects real user eye-tracking drop-off curves."
                },
                {
                    "term": "Ideal DCG (IDCG@K)",
                    "what_is_it": "The maximum theoretically possible DCG score obtained by sorting all test items in perfect descending relevance order.",
                    "analogy": "A student achieving 100% on the answer key.",
                    "why_it_matters": "Acts as the normalization denominator so NDCG is always bounded between 0.0 and 1.0."
                },
                {
                    "term": "Mean Reciprocal Rank (MRR)",
                    "what_is_it": "The average of 1 / rank of the first relevant item found by the user.",
                    "analogy": "How many pages of a phonebook you had to flip before finding the right number.",
                    "why_it_matters": "The standard metric for navigational search and question-answering systems where only one correct answer matters."
                }
            ],
            "symbol_guide": [
                {"symbol": "rel_i", "meaning": "Relevance grade of item at rank position i", "plain_english": "e.g. 0 = ignored, 1 = clicked, 2 = purchased"},
                {"symbol": "\\text{rank}_u^*", "meaning": "Position of the very first relevant item", "plain_english": "e.g. rank = 2 gives reciprocal rank 1/2 = 0.5"},
                {"symbol": "K", "meaning": "Cutoff threshold", "plain_english": "e.g. Top-5 or Top-10 evaluated positions"}
            ],
            "numerical_example": "User relevance: Item A = 3 (perfect), Item B = 2 (good), Item C = 0 (bad). Model predicted order: [B, C, A]. DCG@3 = (2² - 1)/log2(2) + (2^0 - 1)/log2(3) + (2³ - 1)/log2(4) = 3/1 + 0 + 7/2 = 3 + 3.5 = 6.5. Perfect order: [A, B, C]. IDCG@3 = 7/1 + 3/1.585 + 0 = 7 + 1.89 = 8.89. NDCG@3 = 6.5 / 8.89 = 0.731.",
            "pitfalls": "Novice Trap: Optimizing solely for offline NDCG without monitoring catalog diversity and novelty. A model that only recommends Harry Potter and Marvel movies achieves high historical NDCG, but kills platform user retention because users discover nothing new (Filter Bubble).",
            "key_takeaways": [],
            "definition_bullets": [
                "Discounted Cumulative Gain: Logarithmically penalizes relevant items placed low in the list.",
                "Ideal DCG: Theoretical perfect sorting benchmark used to normalize scores to [0, 1].",
                "Mean Reciprocal Rank: Evaluates how fast the user encounters the very first correct match.",
                "Hit Rate@K: Percentage of users who found at least one relevant item in the top-K recommendations."
            ]
        }
    ]

print("RecSys module ready.")
