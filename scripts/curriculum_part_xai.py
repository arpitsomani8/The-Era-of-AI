# scripts/curriculum_part_xai.py
# 5 Explainable AI (XAI) Concepts

def get_xai_concepts():
    topic_id = "eval_xai"
    topic_label = "Explainable AI (XAI) & Model Interpretability"
    cat = "eval"
    cat_label = "Model Evaluation & Generalization"

    return [
        {
            "id": "concept_shap_game_theory",
            "title": "SHAP (Shapley Additive Explanations) & Game Theory",
            "topic_id": topic_id, "topic_label": topic_label, "category": cat, "category_label": cat_label,
            "raw_subtopic": "SHAP (Shapley Additive Explanations) & Game Theory", "raw_sub": "SHAP (Shapley Additive Explanations) & Game Theory",
            "def": "A unified game-theoretic approach to model interpretability (Lundberg & Lee) that computes the unique, axiomatic Shapley values of features across all possible coalition subsets, satisfying efficiency, symmetry, dummy, and additivity properties.",
            "definition": "A unified game-theoretic approach to model interpretability (Lundberg & Lee) that computes the unique, axiomatic Shapley values of features across all possible coalition subsets, satisfying efficiency, symmetry, dummy, and additivity properties.",
            "formula": "$$\\phi_i(v) = \\sum_{S \\subseteq N \\setminus \\{i\\}} \\frac{|S|!(|N| - |S| - 1)!}{|N|!} \\left( v(S \\cup \\{i\\}) - v(S) \\right), \\quad f(x) = \\phi_0 + \\sum_{i=1}^M \\phi_i$$",
            "formula_explanation": "",
            "logic": "Unlike heuristic feature importances that vary wildly between tree implementations, Shapley values are the *only* mathematical attribution method guaranteed to satisfy efficiency (sum of feature contributions equals prediction difference from base rate) and monotonicity.",
            "core_logic": "Unlike heuristic feature importances that vary wildly between tree implementations, Shapley values are the *only* mathematical attribution method guaranteed to satisfy efficiency (sum of feature contributions equals prediction difference from base rate) and monotonicity.",
            "architectural_logic": "",
            "example": "Healthcare ICU mortality prediction: An XGBoost model predicts an 85% risk of patient deterioration. TreeSHAP shows: Blood Pressure=+25%, Age=+15%, Oxygen Saturation=+30%, Base Rate=15%, explaining the clinical justification to the attending physician.",
            "tags": ["SHAP", "TreeSHAP", "Game Theory", "Explainability", "Shapley Values"],
            "simple_summary": "SHAP is based on Nobel-prize-winning game theory: imagine features are players on a soccer team. SHAP tests every possible combination of players to calculate exactly how many goals each individual player contributed to winning the match.",
            "core_terms": [
                {
                    "term": "Shapley Value (phi_i)",
                    "what_is_it": "The average marginal contribution of feature i to the model's prediction across all possible feature subsets.",
                    "analogy": "Dividing a company bonus fairly among employees based on their proven individual impact on revenue.",
                    "why_it_matters": "The gold-standard metric for fair, mathematically rigorous feature attribution."
                },
                {
                    "term": "Base Value (phi_0)",
                    "what_is_it": "The expected value of the model's prediction across the background training dataset: E[f(X)].",
                    "analogy": "The starting baseline score of an exam before questions are graded.",
                    "why_it_matters": "The reference point from which all positive and negative feature pushes are measured."
                },
                {
                    "term": "TreeSHAP",
                    "what_is_it": "A fast polynomial-time O(TLD^2) algorithm that computes exact Shapley values for decision trees instead of exponential O(2^M) brute force.",
                    "analogy": "Taking an express elevator directly to the top floor instead of climbing every flight of stairs in the skyscraper.",
                    "why_it_matters": "Makes exact Shapley calculations instantaneous on million-row production GBDT models."
                },
                {
                    "term": "SHAP Summary / Beeswarm Plot",
                    "what_is_it": "A global visualization plotting every individual data point's SHAP value colored by feature magnitude (high=red, low=blue).",
                    "analogy": "A scatter plot showing not just who has the most influence, but whether having a high or low value is good or bad.",
                    "why_it_matters": "Instantly reveals non-linearities, thresholds, and directional feature impacts across the entire population."
                }
            ],
            "symbol_guide": [
                {"symbol": "S", "meaning": "A subset coalition of features excluding feature i", "plain_english": "A team of features without feature i"},
                {"symbol": "v(S \\cup \\{i\\}) - v(S)", "meaning": "Marginal contribution of feature i to coalition S", "plain_english": "The improvement gained when feature i joins the team"},
                {"symbol": "\\phi_0", "meaning": "Baseline expected model prediction", "plain_english": "The average prediction across all training data"}
            ],
            "numerical_example": "Base mortality rate phi_0 = 0.10 (10%). For patient John: SHAP values are Age: +0.20, Oxygen: +0.35, White Blood Count: +0.15, Medication: -0.08. John's predicted mortality = 0.10 + 0.20 + 0.35 + 0.15 - 0.08 = 0.72 (72%). The sum of SHAP values matches the exact model output perfectly.",
            "pitfalls": "Novice Trap: Assuming high correlation implies high Shapley value. If two features are highly collinear (e.g. height in inches and height in cm), standard KernelSHAP will divide the credit between them, making both appear half as important as they truly are.",
            "key_takeaways": [],
            "definition_bullets": [
                "Shapley Values: Unique game-theoretic feature attributions based on marginal coalition contributions.",
                "Efficiency Axiom: Feature contributions sum up exactly to the difference between prediction and base rate.",
                "TreeSHAP: High-speed polynomial algorithm optimized for decision trees and random forests.",
                "Local & Global Explanations: Explains individual sample decisions and aggregates population behavior."
            ]
        },
        {
            "id": "concept_lime_local_surrogates",
            "title": "LIME (Local Interpretable Model-agnostic Explanations)",
            "topic_id": topic_id, "topic_label": topic_label, "category": cat, "category_label": cat_label,
            "raw_subtopic": "LIME (Local Interpretable Model-agnostic Explanations)", "raw_sub": "LIME (Local Interpretable Model-agnostic Explanations)",
            "def": "A model-agnostic interpretability framework (Ribeiro et al.) that explains individual black-box predictions by perturbing the input sample in its local neighborhood, weighting perturbations by distance, and fitting an interpretable surrogate model (e.g. sparse linear regression).",
            "definition": "A model-agnostic interpretability framework (Ribeiro et al.) that explains individual black-box predictions by perturbing the input sample in its local neighborhood, weighting perturbations by distance, and fitting an interpretable surrogate model (e.g. sparse linear regression).",
            "formula": "$$\\xi(x) = \\arg\\min_{g \\in \\mathcal{G}} \\mathcal{L}\\left(f, g, \\pi_x\\right) + \\Omega(g), \\quad \\pi_x(z) = \\exp\\left( -\\frac{D(x, z)^2}{\\sigma^2} \\right)$$",
            "formula_explanation": "",
            "logic": "Global black-box decision boundaries (e.g. deep neural networks, ensembles) are highly complex and non-linear. However, when zooming in to an infinitesimal local neighborhood around a single sample x, any smooth boundary looks approximately flat (linear). LIME fits a linear model in that local vicinity.",
            "core_logic": "Global black-box decision boundaries (e.g. deep neural networks, ensembles) are highly complex and non-linear. However, when zooming in to an infinitesimal local neighborhood around a single sample x, any smooth boundary looks approximately flat (linear). LIME fits a linear model in that local vicinity.",
            "architectural_logic": "",
            "example": "Computer vision image classification explanation: An InceptionV3 model predicts 'Wolf'. LIME segments the image into superpixels, turns superpixels on/off randomly, and discovers the model relied 100% on the background snow, exposing a spurious correlation.",
            "tags": ["LIME", "Local Surrogates", "Model-Agnostic", "Superpixels"],
            "simple_summary": "LIME explains a complicated model by slightly jiggling your data point in a hundred small ways and watching how the model's answer changes. It draws a simple straight line right around your specific point to show which knobs had the biggest effect.",
            "core_terms": [
                {
                    "term": "Local Surrogate Model g",
                    "what_is_it": "An intrinsically interpretable model (like Ridge regression or decision tree) trained on local perturbations.",
                    "analogy": "Using a simple flat paper map to navigate your immediate neighborhood, even though the Earth is a round sphere.",
                    "why_it_matters": "Provides easily readable linear weights for non-technical stakeholders."
                },
                {
                    "term": "Perturbation Sampling",
                    "what_is_it": "Generating synthetic samples in the immediate vicinity of x by adding Gaussian noise or turning off words/pixels.",
                    "analogy": "Testing a house's stability by gently nudging each wall to see which one wobbles.",
                    "why_it_matters": "Probes how the black box behaves in response to slight input variations."
                },
                {
                    "term": "Proximity Kernel (pi_x)",
                    "what_is_it": "An exponential distance weighting function giving high importance to perturbations close to x and near-zero weight to distant samples.",
                    "analogy": "Giving high weight to eyewitnesses who stood 5 feet away from an accident, and ignoring people who were 2 blocks away.",
                    "why_it_matters": "Forces the surrogate model to focus strictly on local fidelity."
                },
                {
                    "term": "Model-Agnosticism",
                    "what_is_it": "The ability to explain any machine learning model without needing access to its internal gradients, architecture, or weights.",
                    "analogy": "Testing a car's engine performance by pressing the gas pedal and checking the speedometer, without opening the hood.",
                    "why_it_matters": "Works on closed proprietary APIs, PyTorch, Scikit-Learn, and legacy C++ binaries alike."
                }
            ],
            "symbol_guide": [
                {"symbol": "f(x)", "meaning": "Black-box model prediction", "plain_english": "The complex model we are trying to explain"},
                {"symbol": "g(z)", "meaning": "Simple interpretable surrogate model", "plain_english": "e.g. linear equation y = w_1 x_1 + w_2 x_2"},
                {"symbol": "\\Omega(g)", "meaning": "Model complexity penalty", "plain_english": "Restricts explanation to top K features (e.g. max 5 words)"}
            ],
            "numerical_example": "Text classification: Sentence 'Great camera but terrible battery'. LIME generates 500 perturbed sentences dropping random words. When 'terrible' is removed, positive sentiment jumps by +0.72. When 'great' is removed, positive sentiment drops by -0.45. LIME's local surrogate weights: 'terrible' = -0.72, 'battery' = -0.15, 'great' = +0.45.",
            "pitfalls": "Novice Trap: High sampling variance and instability. Because LIME generates random perturbations, running LIME twice on the exact same input sample can produce slightly different explanation weights unless the random seed is fixed and perturbation count is sufficiently high (e.g. 5,000+).",
            "key_takeaways": [],
            "definition_bullets": [
                "Local Linearity: Complex non-linear decision boundaries appear approximately linear in localized neighborhoods.",
                "Perturbation Analysis: Probing black-box behavior by jiggling input features and recording output responses.",
                "Proximity Weighting: Prioritizing samples closest to the original observation via exponential kernels.",
                "Model Agnostic: Operates on any model architecture without requiring internal gradient access."
            ]
        },
        {
            "id": "concept_integrated_gradients_saliency",
            "title": "Integrated Gradients & Neural Saliency Maps",
            "topic_id": topic_id, "topic_label": topic_label, "category": cat, "category_label": cat_label,
            "raw_subtopic": "Integrated Gradients & Neural Saliency Maps", "raw_sub": "Integrated Gradients & Neural Saliency Maps",
            "def": "An axiomatic gradient-based attribution method for deep neural networks (Sundararajan et al.) that integrates feature gradients along the straight-line path from a neutral baseline x' to input x, satisfying completeness and implementation invariance.",
            "definition": "An axiomatic gradient-based attribution method for deep neural networks (Sundararajan et al.) that integrates feature gradients along the straight-line path from a neutral baseline x' to input x, satisfying completeness and implementation invariance.",
            "formula": "$$\\text{IG}_i(x) = (x_i - x'_i) \\times \\int_0^1 \\frac{\\partial F\\left( x' + \\alpha (x - x') \\right)}{\\partial x_i} d\\alpha, \\quad \\sum_{i=1}^d \\text{IG}_i(x) = F(x) - F(x')$$",
            "formula_explanation": "",
            "logic": "Standard raw input gradients (dF/dx) suffer from saturation: once a neuron's activation is fully saturated (e.g. ReLU flat region or sigmoid ceiling), the local gradient drops to zero even if the feature was overwhelmingly important. Integrated Gradients accumulates gradients across the entire journey from neutral baseline to input.",
            "core_logic": "Standard raw input gradients (dF/dx) suffer from saturation: once a neuron's activation is fully saturated (e.g. ReLU flat region or sigmoid ceiling), the local gradient drops to zero even if the feature was overwhelmingly important. Integrated Gradients accumulates gradients across the entire journey from neutral baseline to input.",
            "architectural_logic": "",
            "example": "Medical MRI brain tumor localization: Using a completely black MRI image as baseline x'. Integrating gradients as the image scales from black to John's scan highlights the exact millimeter tumor boundary that triggered the glioblastoma diagnosis.",
            "tags": ["Integrated Gradients", "Saliency Maps", "Deep Learning XAI", "Gradient Attribution"],
            "simple_summary": "Standard gradients have 'blind spots' when neural networks saturate. Integrated Gradients solves this by fading in the image from pure black to the full picture in 50 tiny steps, measuring how the prediction score builds up along the way.",
            "core_terms": [
                {
                    "term": "Gradient Saturation",
                    "what_is_it": "The phenomenon where a feature has pushed an activation function into its flat plateau, making the local derivative zero despite its high importance.",
                    "analogy": "A water glass that is already 100% full: adding more water doesn't register on the 'fill level' meter because it overflows.",
                    "why_it_matters": "Causes simple vanilla saliency maps to completely miss critical features."
                },
                {
                    "term": "Baseline / Reference (x')",
                    "what_is_it": "A neutral, information-free input representing the absence of features (e.g. all-black image, all-zero embedding, zero vector).",
                    "analogy": "The tare button on a kitchen scale that resets weight to zero before you add flour.",
                    "why_it_matters": "Defines what the model considers 'normal' before feature contributions are measured."
                },
                {
                    "term": "Completeness Axiom",
                    "what_is_it": "The guarantee that the sum of attributions across all input dimensions equals the exact difference between F(x) and F(x').",
                    "analogy": "Balancing your checkbook so that all individual transactions add up to the total monthly change in balance.",
                    "why_it_matters": "Ensures no attribution is lost or artificially inflated."
                },
                {
                    "term": "Riemann Sum Approximation",
                    "what_is_it": "Approximating the continuous path integral by evaluating gradients at m discrete steps (typically m = 50 to 300 steps) along alpha in [0, 1].",
                    "analogy": "Measuring temperature at 50 specific checkpoints along a road trip instead of taking an infinite continuous log.",
                    "why_it_matters": "Enables practical execution with standard PyTorch autograd in a few forward-backward passes."
                }
            ],
            "symbol_guide": [
                {"symbol": "x'", "meaning": "Neutral baseline reference vector", "plain_english": "e.g. all-black image or blank text embedding"},
                {"symbol": "\\alpha", "meaning": "Interpolation scalar from 0 to 1", "plain_english": "Fade-in slider moving from baseline to input"},
                {"symbol": "F(x)", "meaning": "Model output logit or probability", "plain_english": "Target class prediction score"}
            ],
            "numerical_example": "Baseline prediction F(x') = 0.05. Real sample prediction F(x) = 0.85. Total change = 0.80. Integrating gradients across m=50 interpolation steps yields: Feature 1 IG = +0.50, Feature 2 IG = +0.25, Feature 3 IG = +0.05. Sum = 0.50 + 0.25 + 0.05 = 0.80. Completeness is satisfied with zero error.",
            "pitfalls": "Novice Trap: Choosing a bad baseline! For NLP or tabular data, an all-zeros baseline might have unintended semantic meaning (e.g. zero embedding could correspond to a specific rare word token). Use distribution-averaged baselines or task-appropriate blanks.",
            "key_takeaways": [],
            "definition_bullets": [
                "Saturation Immunity: Accumulates gradients along path to overcome vanishing derivatives.",
                "Neutral Baseline: Information-free reference against which all attribution is measured.",
                "Completeness Guarantee: Attributions sum up exactly to the total score change.",
                "Riemann Sampling: Standard 50-step linear interpolation executing efficiently with modern autograd."
            ]
        },
        {
            "id": "concept_pdp_permutation_importance",
            "title": "Permutation Feature Importance & Partial Dependence Plots (PDP)",
            "topic_id": topic_id, "topic_label": topic_label, "category": cat, "category_label": cat_label,
            "raw_subtopic": "Permutation Feature Importance & Partial Dependence Plots (PDP)", "raw_sub": "Permutation Feature Importance & Partial Dependence Plots (PDP)",
            "def": "Global model-agnostic interpretability tools that quantify feature criticality by measuring validation score degradation when feature values are randomly shuffled (Permutation Importance), and map marginal response curves across feature values (Partial Dependence Plots / ICE).",
            "definition": "Global model-agnostic interpretability tools that quantify feature criticality by measuring validation score degradation when feature values are randomly shuffled (Permutation Importance), and map marginal response curves across feature values (Partial Dependence Plots / ICE).",
            "formula": "$$\\text{PFI}(j) = L(y, f(X^{\\text{perm-j}})) - L(y, f(X)), \\quad \\bar{f}_S(x_S) = \\frac{1}{n} \\sum_{i=1}^n f(x_S, x_{C}^{(i)})$$",
            "formula_explanation": "",
            "logic": "Default impurity-based importances in random forests (Gini gain) artificially favor high-cardinality continuous features over binary flags. Permutation importance tests real predictive power on held-out test data by breaking the relationship between feature and target.",
            "core_logic": "Default impurity-based importances in random forests (Gini gain) artificially favor high-cardinality continuous features over binary flags. Permutation importance tests real predictive power on held-out test data by breaking the relationship between feature and target.",
            "architectural_logic": "",
            "example": "Real estate appraisal pricing: PDP shows house price increases linearly from 1,000 to 3,000 sqft, plateaus from 3,000 to 5,000 sqft, and then curves upward exponentially, visualizing the non-linear relationship learned by the model.",
            "tags": ["Permutation Importance", "PDP", "ICE Plots", "Global Interpretability"],
            "simple_summary": "Permutation importance tests how important a feature is by randomly scrambling its column like a deck of cards: if the model's accuracy plummets, that feature was critical. Partial Dependence Plots draw a graph showing: as X goes up, does the prediction go up or down?",
            "core_terms": [
                {
                    "term": "Permutation Feature Importance",
                    "what_is_it": "Measuring the drop in model evaluation metric (e.g. drop in ROC-AUC or increase in MSE) after shuffling feature j's column values.",
                    "analogy": "Testing how important the drummer is to a rock band by replacing their drumbeats with random noise and seeing if the song falls apart.",
                    "why_it_matters": "Directly links feature importance to real test-set predictive performance."
                },
                {
                    "term": "Partial Dependence Plot (PDP)",
                    "what_is_it": "A line plot showing the marginal effect of one or two features on the model's predicted outcome while averaging out all other features.",
                    "analogy": "Graphing how your car's fuel efficiency changes as you increase speed from 20 mph to 90 mph, averaging across rain, snow, and sunny days.",
                    "why_it_matters": "Visualizes whether a feature's effect is linear, monotonic, threshold-based, or non-linear."
                },
                {
                    "term": "Individual Conditional Expectation (ICE)",
                    "what_is_it": "Plotting a separate curve for every individual row in the dataset before averaging them into the PDP.",
                    "analogy": "Showing the fuel efficiency curve of every individual car model rather than just the single fleet average line.",
                    "why_it_matters": "Uncovers hidden interaction effects that get smoothed away in average PDP lines."
                },
                {
                    "term": "High Cardinality Bias",
                    "what_is_it": "The flaw in tree split-gain importances that gives massive credit to unique IDs or zipcodes simply because they create many splits.",
                    "analogy": "Giving high points to an employee just because they sent 1,000 emails, even if none of the emails solved any problems.",
                    "why_it_matters": "Permutation importance on test data completely eliminates this bias."
                }
            ],
            "symbol_guide": [
                {"symbol": "X^{\\text{perm-j}}", "meaning": "Feature matrix with column j randomly permuted", "plain_english": "Scrambled column j"},
                {"symbol": "x_S", "meaning": "Feature(s) of interest being plotted", "plain_english": "e.g. House square footage"},
                {"symbol": "x_C", "meaning": "Complement set of all other features", "plain_english": "All other columns averaged out"}
            ],
            "numerical_example": "Baseline test ROC-AUC = 0.92. When column 'Credit_Score' is permuted: AUC drops to 0.74 (PFI = +0.18, huge impact). When column 'Application_Day_of_Week' is permuted: AUC stays at 0.919 (PFI = +0.001, negligible impact). The team safely drops Day_of_Week from the production pipeline.",
            "pitfalls": "Novice Trap: Permuting collinear features. If two features are highly correlated (e.g. 'Zipcode' and 'State'), shuffling one creates impossible synthetic combinations (e.g. Beverly Hills 90210 in the state of Maine), forcing the model to evaluate out-of-distribution ghost samples.",
            "key_takeaways": [],
            "definition_bullets": [
                "Permutation Importance: Measures real performance loss when feature correlation is severed.",
                "Impurity Bias Immunity: Overcomes tree Gini-split biases on high-cardinality features.",
                "Partial Dependence Curves: Visualizes marginal non-linear feature response trajectories.",
                "ICE Curves: Detects heterogeneous individual sample responses and interaction effects."
            ]
        },
        {
            "id": "concept_model_governance_compliance",
            "title": "Model Governance, Auditing & Regulatory AI Compliance",
            "topic_id": topic_id, "topic_label": topic_label, "category": cat, "category_label": cat_label,
            "raw_subtopic": "Model Governance, Auditing & Regulatory AI Compliance", "raw_sub": "Model Governance, Auditing & Regulatory AI Compliance",
            "def": "The organizational, legal, and engineering frameworks ensuring AI systems adhere to regulatory standards (EU AI Act, NIST AI RMF, EEOC), encompassing Model Cards, reproducible lineage tracking, bias audits, adversarial red-teaming, and right-to-explanation compliance.",
            "definition": "The organizational, legal, and engineering frameworks ensuring AI systems adhere to regulatory standards (EU AI Act, NIST AI RMF, EEOC), encompassing Model Cards, reproducible lineage tracking, bias audits, adversarial red-teaming, and right-to-explanation compliance.",
            "formula": "$$\\text{Adverse Impact Ratio (AIR)} = \\frac{\\text{Selection Rate}_{\\text{Protected}}}{\\text{Selection Rate}_{\\text{Reference}}} \\ge 0.80 \\; (\\text{Four-Fifths Rule})$$",
            "formula_explanation": "",
            "logic": "Deploying un-audited AI systems creates existential legal liabilities, regulatory fines (up to 7% of global turnover under EU AI Act), and systemic discrimination. Governance embeds cryptographic provenance, automated fairness checks, and human-in-the-loop audit trails into MLOps pipelines.",
            "core_logic": "Deploying un-audited AI systems creates existential legal liabilities, regulatory fines (up to 7% of global turnover under EU AI Act), and systemic discrimination. Governance embeds cryptographic provenance, automated fairness checks, and human-in-the-loop audit trails into MLOps pipelines.",
            "architectural_logic": "",
            "example": "Automated mortgage underwriting: A bank must provide adverse action notices within 30 days detailing the top 4 specific financial reasons (derived via SHAP) why a loan was denied, verified by compliance officers to meet Federal Fair Housing Act standards.",
            "tags": ["Governance", "Compliance", "Model Cards", "EU AI Act", "Auditing"],
            "simple_summary": "Model governance is the safety inspection and legal rulebook for AI: making sure models don't discriminate unfairly, documenting how they were built with 'nutrition labels' (Model Cards), and maintaining an 'Undo' and audit trail for regulators.",
            "core_terms": [
                {
                    "term": "Model Cards (Mitchell et al.)",
                    "what_is_it": "Standardized documentation outlining model intended use, training data demographics, benchmark metrics, limitations, and ethical considerations.",
                    "analogy": "The FDA Nutrition Facts label printed on the side of a cereal box.",
                    "why_it_matters": "Prevents models trained for one task from being dangerously misused on incompatible tasks."
                },
                {
                    "term": "Four-Fifths Rule (80% Rule)",
                    "what_is_it": "A mathematical employment guideline stating that the selection rate for a protected group must be at least 80% of the rate for the highest group.",
                    "analogy": "If 60% of male applicants pass an automated resume screen, at least 48% (0.80 × 60%) of female applicants must pass.",
                    "why_it_matters": "The legal threshold used by regulatory bodies to establish disparate impact discrimination."
                },
                {
                    "term": "Lineage Tracking & Provenance",
                    "what_is_it": "Cryptographically linking model binary weights to the exact training dataset git hash, code version, and hyperparameter config (e.g. MLflow/DVC).",
                    "analogy": "A flight data black box recorder tracking every cockpit decision before an airplane lands.",
                    "why_it_matters": "Enables bit-for-bit forensic reproducibility during external regulatory audits."
                },
                {
                    "term": "EU AI Act Risk Tiers",
                    "what_is_it": "The European Union's risk classification assigning strict conformity requirements to High-Risk AI (credit, hiring, law enforcement) and banning Unacceptable Risk AI.",
                    "analogy": "Strict vehicle safety certification requirements for commercial airplanes versus light rules for toy kites.",
                    "why_it_matters": "Violations carry massive financial penalties and immediate market bans."
                }
            ],
            "symbol_guide": [
                {"symbol": "\\text{AIR}", "meaning": "Adverse Impact Ratio", "plain_english": "Ratio of protected group selection rate to reference group rate"},
                {"symbol": "NIST AI RMF", "meaning": "National Institute of Standards & Technology AI Risk Framework", "plain_english": "Federal security and risk guidelines"},
                {"symbol": "\\ge 0.80", "meaning": "The 80% disparate impact safe harbor threshold", "plain_english": "Minimum acceptable parity bound"}
            ],
            "numerical_example": "Hiring algorithm evaluation: 1,000 male applicants, 300 hired (selection rate = 30.0%). 500 female applicants, 120 hired (selection rate = 24.0%). Adverse Impact Ratio = 24.0% / 30.0% = 0.80 (80.0%). Meets the 4/5ths threshold. If only 110 were hired (22.0%), AIR = 0.733 (< 0.80), triggering immediate regulatory audit for unlawful disparate impact.",
            "pitfalls": "Novice Trap: Assuming that removing demographic columns (e.g. dropping 'Race' and 'Gender') prevents discrimination! Proxy variables (e.g. zip code, hobbies, university name) recreate protected attributes with 95%+ fidelity, creating severe hidden bias.",
            "key_takeaways": [],
            "definition_bullets": [
                "Model Cards: Standardized nutrition labels detailing limitations and intended uses.",
                "Disparate Impact Auditing: Verifying Adverse Impact Ratios exceed the 80% legal threshold.",
                "Reproducible Lineage: Tracking training data hashes and code commits for regulatory review.",
                "Regulatory Compliance: Aligning high-risk pipelines with EU AI Act and NIST frameworks."
            ]
        }
    ]

print("XAI module ready.")
