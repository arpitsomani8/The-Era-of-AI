import json
import re

def main():
    # 1. Load concepts.json
    with open("src/data/concepts.json", "r", encoding="utf-8") as f:
        concepts = json.load(f)

    # 2. Load all_concepts.json
    with open("scripts/data_sources/all_concepts.json", "r", encoding="utf-8") as f:
        all_concepts = json.load(f)

    # 3. Load concepts_ml.py
    with open("scripts/data_sources/concepts_ml.py", "r", encoding="utf-8") as f:
        py_content = f.read()

    tuning_data = {
        "id": "concept_hyperparameter_tuning_bayesian",
        "title": "Hyperparameter Tuning (Grid Search, Random Search & Bayesian Optuna)",
        "topic_id": "ml_opt",
        "topic_label": "Gradient Descent & Hyperparameters",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "raw_subtopic": "Hyperparameter Tuning (Grid Search, Random Search & Bayesian Optuna)",
        "def": "Hyperparameter tuning is the systematic process of testing different external configuration settings (like learning rate, tree depth, and batch size) to discover the combination that performs best on validation data.",
        "formula": "$$\\theta^* = \\arg\\max_{\\theta \\in \\Theta} f(\\theta), \\quad \\text{TPE Acquisition: } \\frac{p(\\theta \\mid y < y^*)}{p(\\theta \\mid y \\ge y^*)}$$",
        "logic": "Parameters (weights and biases) are learned automatically by the model from training data, while hyperparameters must be configured by the engineer before training starts. Because testing every combination takes too long, search strategies evolved from blind exhaustive grids to random sampling, and finally to intelligent Bayesian optimization (Optuna) that learns from previous trials.",
        "example": "Tuning an XGBoost model: Grid Search over 5 learning rates and 5 tree depths requires 25 full training runs. Random Search tests 10 diverse combinations and finds a better result in half the time. Optuna (Bayesian TPE) tests 15 smart combinations, learns which regions work best, prunes bad runs early, and hits peak validation accuracy in a fraction of the time.",
        "tags": [
            "Hyperparameters",
            "Grid Search",
            "Random Search",
            "Bayesian Optimization",
            "Optuna",
            "TPE",
            "Model Tuning"
        ],
        "definition": "Hyperparameter tuning is the systematic process of testing different external configuration settings (like learning rate, tree depth, and batch size) to discover the combination that performs best on validation data.",
        "formula_explanation": "",
        "simple_summary": "Imagine tuning a high-performance race car. Parameters are the engine parts that adjust themselves automatically as the car drives. Hyperparameters are the external dials the mechanic sets beforehand—like tire pressure and suspension stiffness. Grid Search tests every dial combination mechanically; Random Search tries a handful of random settings and often finds great results faster; Bayesian Optimization (like Optuna) acts like an expert race engineer who studies the lap times of each past test run to guess even better dial settings next time.",
        "core_terms": [
            {
                "term": "Parameters vs. Hyperparameters",
                "what_is_it": "• Parameters (W, b): Internal numbers the model learns on its own from data using gradient descent.\n• Hyperparameters (η, B, depth): External dials the engineer sets before training starts to control how the model learns.",
                "analogy": "Parameters are the student's memorized facts; Hyperparameters are the study habits (hours per day, lighting, breaks) set by the teacher.",
                "why_it_matters": "The golden rule of ML: models optimize their own parameters, but engineers must optimize hyperparameters."
            },
            {
                "term": "The Exploration vs. Exploitation Dilemma",
                "what_is_it": "• Exploitation: Searching close to the best known settings found so far to squeeze out tiny improvements.\n• Exploration: Venturing into unexamined areas of hyperparameter space with high uncertainty where a much better minimum might hide.",
                "analogy": "Deciding where to eat dinner: going to your favorite familiar restaurant (exploitation) vs trying a brand-new restaurant that might be amazing (exploration).",
                "why_it_matters": "Bayesian optimization uses mathematical acquisition functions to balance both, avoiding getting stuck in local traps."
            },
            {
                "term": "Surrogate Modeling & TPE (Optuna)",
                "what_is_it": "• Training a full model is expensive. Bayesian optimization builds a lightweight probabilistic estimate (surrogate model, like Tree-structured Parzen Estimator / TPE) of the loss surface.\n• Uses this surrogate model to predict which untested hyperparameter setting has the highest chance of beating the current best score.",
                "analogy": "A gold prospector sketching a map of where past digs hit gold to predict where the next vein lies.",
                "why_it_matters": "Allows Optuna to find top-tier hyperparameters in 10x to 50x fewer trial iterations than blind search."
            }
        ],
        "symbol_guide": [
            {
                "symbol": "θ",
                "meaning": "Hyperparameter Configuration",
                "plain_english": "A specific set of settings, e.g. {learning_rate: 0.01, max_depth: 6}"
            },
            {
                "symbol": "f(θ)",
                "meaning": "Objective Validation Score",
                "plain_english": "The performance score (like validation accuracy or loss) achieved using settings θ"
            },
            {
                "symbol": "θ*",
                "meaning": "Optimal Hyperparameters",
                "plain_english": "The winning combination of settings that achieves the highest validation score"
            },
            {
                "symbol": "y*",
                "meaning": "Best Score Threshold",
                "plain_english": "The benchmark score dividing historical trials into top performers vs bottom performers"
            },
            {
                "symbol": "EI(θ)",
                "meaning": "Expected Improvement",
                "plain_english": "The probability and expected magnitude that a new configuration will beat the current best score"
            }
        ],
        "numerical_example": "Comparison of Tuning Strategies on 2 Hyperparameters (Learning Rate & Tree Depth):\n\nSetup: 3 Learning Rates (0.1, 0.01, 0.001) and 3 Depths (3, 6, 9)\n\n1. Grid Search (3 × 3 = 9 trials):\n• Tests all 9 grid combinations rigidly.\n• If tree depth has little impact on the problem, it tests each learning rate 3 times redundantly, wasting 6 out of 9 trials!\n\n2. Random Search (9 trials across continuous distributions):\n• Tests 9 unique randomly sampled learning rates.\n• Tests 3x more distinct learning rate values than Grid Search in the same number of trials, vastly increasing odds of finding the sweet spot!\n\n3. Optuna Bayesian Optimization (15 trials with ASHA pruning):\n• Trials 1 to 5: Broad exploration; discovers that learning rates > 0.05 produce terrible scores.\n• Trials 6 to 10: Concentrates samples inside [0.005, 0.02]; automatically prunes 3 slow runs early.\n• Trials 11 to 15: Pinpoints the optimal setting (lr = 0.012, depth = 7), beating Grid Search while using 60% less total compute time!",
        "pitfalls": "Common Mistakes to Avoid:\n1. Tuning on the Test Set: Evaluating hyperparameters on test data causes subtle data leakage; always tune on validation folds and keep the test set locked until final evaluation.\n2. Using Grid Search on large search spaces: Combinatorial explosion causes 5 parameters with 4 values each to explode into 4⁵ = 1,024 training runs!\n3. Assuming all hyperparameters matter equally: In practice, learning rate matters immensely, while parameters like random seed or subsample ratio have minor impact; Random Search exploits this asymmetry.\n4. Skipping automated pruning: Running poor trials all the way to 100 epochs burns cloud budget; use Optuna's MedianPruner or Hyperband to terminate hopeless runs by epoch 5.\n5. Searching on a linear scale instead of log scale: Parameters spanning multiple orders of magnitude (like learning rate from 1e-5 to 1e-1) must be sampled with log=True, or 90% of trials will wastefully cluster above 0.01.",
        "core_logic": "Why this matters: Hyperparameters govern the geometry and optimization trajectory of training. Setting them poorly causes underfitting, instability, or severe overfitting. Automated tuning transforms hyperparameter selection from manual guesswork into a rigorous, reproducible engineering process.",
        "architectural_logic": "In modern production pipelines, Optuna is integrated with PyTorch and LightGBM: study = optuna.create_study(direction='maximize', pruner=optuna.pruners.HyperbandPruner()). Inside the objective function, trial.suggest_float('lr', 1e-4, 1e-1, log=True) guides sampling, while trial.report() and trial.should_prune() eliminate unpromising runs.",
        "key_takeaways": [
            "Parameters vs. Hyperparameters: Parameters are learned by the model; hyperparameters are set by the engineer.",
            "Random Beats Grid: Random Search tests far more distinct values of critical hyperparameters than rigid grids.",
            "Bayesian Optimization Learns: Optuna uses past trial history (TPE) to balance exploration and exploitation.",
            "Automated Pruning Saves 80% Compute: Halting unpromising training runs early slashes cloud training costs."
        ],
        "definition_bullets": [
            "Hyperparameter Tuning: The systematic optimization of external configuration settings to maximize validation performance.",
            "Bayesian Optimization: A sequential model-based optimization method that uses past trial outcomes to select promising future configurations."
        ],
        "types_header": "The 3 Major Hyperparameter Search Strategies",
        "types_badge": "Search Paradigms",
        "quick_types": [
            {
                "type": "Grid Search (Exhaustive & Deterministic)",
                "definition": "Tests every single combination in a predefined grid; systematic and reproducible, but suffers from exponential explosion on large spaces.",
                "looks_like": "GridSearchCV(param_grid)"
            },
            {
                "type": "Random Search (Stochastic Sampling)",
                "definition": "Samples configurations randomly from probability distributions; statistically superior to Grid Search on multi-parameter spaces.",
                "looks_like": "RandomizedSearchCV(n_iter=20)"
            },
            {
                "type": "Bayesian Optimization / Optuna (Sequential Learning)",
                "definition": "Builds a probabilistic surrogate model (TPE) of the objective surface, learning from past trials to pick the smartest next candidate.",
                "looks_like": "optuna.create_study(sampler=TPESampler())"
            },
            {
                "type": "Automated Pruning (Hyperband / ASHA)",
                "definition": "An early-stopping algorithm that terminates unpromising trials after a few epochs, reallocating compute to winning configurations.",
                "looks_like": "optuna.pruners.HyperbandPruner()"
            }
        ],
        "connected_logic": [
            {
                "title": "Why Random Search Statistically Beats Grid Search",
                "content": "• Bengio & Bergstra (2012) proved that only a small subset of hyperparameters truly impact model accuracy for any given problem.\n• In 9 grid trials across 2 parameters, Grid Search only evaluates 3 distinct values of each parameter.\n• In 9 random trials, Random Search evaluates 9 unique values of the critical parameter, covering the space with far higher resolution without extra compute."
            },
            {
                "title": "How Optuna's TPE (Tree-structured Parzen Estimator) Works",
                "content": "• Instead of modeling the loss surface with heavy Gaussian Processes, TPE splits past trials into two groups: the top 15% best runs (good) and the remaining 85% (bad).\n• It fits two probability densities: l(θ) for good configurations, and g(θ) for bad configurations.\n• It picks candidate settings that maximize the ratio l(θ) / g(θ)—choosing parameters most likely to produce elite results."
            },
            {
                "title": "Automated Pruning with ASHA / Hyperband in Optuna",
                "content": "• If a trial has mediocre validation score at epoch 3, it is virtually guaranteed not to become the global champion at epoch 100.\n• Optuna's trial.report(score, epoch) and trial.should_prune() compare current performance against historical median runs.\n• Unpromising runs are killed immediately, saving up to 80% of GPU compute time and cloud costs."
            },
            {
                "title": "Logarithmic Scaling for Multi-Scale Hyperparameters",
                "content": "• Hyperparameters like Learning Rate (1e-5 to 1e-1) or Regularization Lambda span multiple orders of magnitude.\n• Searching uniformly on a linear scale wastes 90% of trials testing numbers between 0.01 and 0.1.\n• Always sample on a log-uniform scale (trial.suggest_float('lr', 1e-5, 1e-1, log=True)) so 0.0001 gets tested as thoroughly as 0.01."
            }
        ]
    }

    # 1. Update in concepts.json
    for c in concepts:
        if c.get("id") == "concept_hyperparameter_tuning_bayesian":
            c.update(tuning_data)
            print("Updated concept_hyperparameter_tuning_bayesian in concepts.json")
            break

    with open("src/data/concepts.json", "w", encoding="utf-8") as f:
        json.dump(concepts, f, indent=2, ensure_ascii=False)

    # 2. Update in all_concepts.json
    # Note: If all_concepts had concept_lr_schedules, replace it with tuning_data
    found = False
    for i, c in enumerate(all_concepts):
        if c.get("id") == "concept_hyperparameter_tuning_bayesian" or c.get("id") == "concept_lr_schedules":
            all_concepts[i] = tuning_data
            found = True
            print("Updated/Replaced in all_concepts.json")
            break
    if not found:
        all_concepts.append(tuning_data)

    with open("scripts/data_sources/all_concepts.json", "w", encoding="utf-8") as f:
        json.dump(all_concepts, f, indent=2, ensure_ascii=False)

    # 3. Update in concepts_ml.py
    # Replace concept_lr_schedules or concept_hyperparameter_tuning_bayesian
    pattern = r'\{\s*"id":\s*"(concept_lr_schedules|concept_hyperparameter_tuning_bayesian)".*?\},(?=\s*\{\s*"id":\s*"concept_sigmoid")'
    match = re.search(pattern, py_content, re.DOTALL)
    if match:
        lines = json.dumps(tuning_data, indent=4, ensure_ascii=False).splitlines()
        indented_replacement = "\n".join("    " + line for line in lines) + ","
        py_content = py_content[:match.start()] + indented_replacement + py_content[match.end():]
        with open("scripts/data_sources/concepts_ml.py", "w", encoding="utf-8") as f:
            f.write(py_content)
        print("Updated concept_hyperparameter_tuning_bayesian in concepts_ml.py")
    else:
        print("Could not find regex match in concepts_ml.py")

if __name__ == "__main__":
    main()
