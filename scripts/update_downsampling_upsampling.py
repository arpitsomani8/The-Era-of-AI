import json
import re

def main():
    # 1. Load concepts.json
    with open("src/data/concepts.json", "r", encoding="utf-8") as f:
        concepts = json.load(f)

    # 2. Load all_concepts.json
    with open("scripts/data_sources/all_concepts.json", "r", encoding="utf-8") as f:
        all_concepts = json.load(f)

    resampling_data = {
        "id": "concept_resampling_strategies",
        "title": "Downsampling vs Upsampling",
        "topic_id": "data_split",
        "topic_label": "Datasets, Splitting & Class Imbalance",
        "category": "data",
        "category_label": "Data Preprocessing & EDA",
        "raw_subtopic": "Downsampling the Majority vs Upsampling the Minority",
        "def": "Downsampling and upsampling are two resampling techniques used to balance imbalanced datasets—downsampling reduces majority class examples, while upsampling increases minority class examples.",
        "formula": "$$\\text{Balance Ratio} = \\frac{N_{\\text{minority}}}{N_{\\text{majority}}} \\quad \\xrightarrow{\\text{resample}} \\quad 1:1, \\; 1:4, \\;\\text{or} \\; 1:10$$",
        "logic": "When one class has far more rows than another (like 99% legitimate vs 1% fraud), models often ignore the rare class. Downsampling deletes majority rows to speed up training, while upsampling duplicates or creates new rare rows so the model has enough examples to learn.",
        "example": "Ad click prediction: You have 10,000 clicks (minority) and 1,000,000 non-clicks (majority). With downsampling, you keep all 10,000 clicks and randomly pick 40,000 non-clicks (a 1:4 ratio), speeding up training from hours to seconds while keeping strong predictive accuracy.",
        "tags": [
            "Downsampling",
            "Upsampling",
            "Class Imbalance",
            "EasyEnsemble",
            "Resampling"
        ],
        "definition": "Downsampling and upsampling are two resampling techniques used to balance imbalanced datasets—downsampling reduces majority class examples, while upsampling increases minority class examples.",
        "formula_explanation": "",
        "simple_summary": "Downsampling makes classes balanced by removing examples from the majority class. Upsampling makes classes balanced by adding or copying examples to the minority class. Downsampling is best when you have huge datasets and need fast training; upsampling is essential when your rare class is too small to afford losing any data.",
        "core_terms": [
            {
                "term": "Downsampling (Undersampling)",
                "what_is_it": "• Randomly removing examples from the majority class so its count matches or nears the minority class.\n• Blazing fast training and low memory usage, but throws away potentially useful real-world data.",
                "analogy": "Trimming a huge photo album: picking only a few representative pictures from a giant pile so it fits on a single shelf.",
                "why_it_matters": "Turns multi-hour training runs on millions of rows into quick multi-second runs without creating any fake data."
            },
            {
                "term": "Upsampling (Oversampling)",
                "what_is_it": "• Increasing the number of minority class examples by duplicating them or creating new synthetic examples.\n• Keeps 100% of your majority data, but simple copying can cause the model to memorize points (overfitting).",
                "analogy": "Making photocopies of rare book pages so multiple students in a classroom have a copy to read.",
                "why_it_matters": "Essential when the rare class is tiny (like only 50 disease cases) where downsampling would leave too few total rows to train."
            },
            {
                "term": "Partial Resampling (1:4 or 1:10)",
                "what_is_it": "• Rebalancing data to a practical ratio like 1:4 or 1:10 instead of forcing a strict 50/50 split.\n• Gives the model plenty of rare examples to learn from while keeping realistic proportions and saving compute.",
                "analogy": "Adding enough seasoning to taste the flavor without turning the entire soup into salt.",
                "why_it_matters": "Avoids extreme data loss from aggressive downsampling and prevents huge memory blowups from massive upsampling."
            }
        ],
        "types_header": "Comparison: Choosing the Right Resampling Strategy",
        "types_badge": "Resampling Options",
        "quick_types": [
            {
                "type": "Downsampling",
                "definition": "Removes majority class rows; best when you have massive datasets and need fast training.",
                "looks_like": "from sklearn.utils import resample; resample(majority, n_samples=len(minority))"
            },
            {
                "type": "Random Upsampling",
                "definition": "Duplicates existing minority rows; best when dataset is small and you cannot lose majority data.",
                "looks_like": "from imblearn.over_sampling import RandomOverSampler; RandomOverSampler()"
            },
            {
                "type": "SMOTE (Synthetic Upsampling)",
                "definition": "Creates new artificial points between nearby rare examples; best for continuous numeric data.",
                "looks_like": "from imblearn.over_sampling import SMOTE; SMOTE()"
            },
            {
                "type": "Balanced Ensemble (EasyEnsemble)",
                "definition": "Splits majority data into multiple chunks and trains separate downsampled models in parallel.",
                "looks_like": "from imblearn.ensemble import EasyEnsembleClassifier; EasyEnsembleClassifier()"
            },
            {
                "type": "Class Weights (No Resampling)",
                "definition": "Penalizes mistakes on the minority class more heavily without adding or removing any rows.",
                "looks_like": "model = RandomForestClassifier(class_weight='balanced')"
            }
        ],
        "symbol_guide": [
            {
                "symbol": "N_majority",
                "meaning": "Majority Class Count",
                "plain_english": "The number of examples in the common class (e.g., 990,000 legitimate transactions)"
            },
            {
                "symbol": "N_minority",
                "meaning": "Minority Class Count",
                "plain_english": "The number of examples in the rare class (e.g., 10,000 fraud transactions)"
            },
            {
                "symbol": "Resample Ratio",
                "meaning": "Target Class Ratio",
                "plain_english": "The balance you want in training (such as 1:1 for equal size, or 1:4 for partial rebalance)"
            },
            {
                "symbol": "P_calibrated",
                "meaning": "Calibrated Probability",
                "plain_english": "The adjusted probability reflecting real-world chances rather than the resampled training ratio"
            }
        ],
        "numerical_example": "Comparing Downsampling vs Upsampling with Real Numbers:\nSuppose your dataset has:\n• 10,000 fraud cases (minority class)\n• 990,000 legitimate cases (majority class)\nTotal = 1,000,000 records (1:99 ratio)\n\nOption A: 50/50 Downsampling\n• Keep: 10,000 fraud cases\n• Randomly pick: 10,000 legitimate cases\n• Result: 20,000 total rows. Blazing fast training, but you discarded 980,000 legitimate records (98.9% data loss!).\n\nOption B: 1:4 Partial Downsampling (Recommended)\n• Keep: 10,000 fraud cases\n• Randomly pick: 40,000 legitimate cases\n• Result: 50,000 total rows. Fast training with 4x more variety of legitimate cases retained.\n\nOption C: 50/50 Upsampling\n• Duplicate the 10,000 fraud cases up to 990,000\n• Result: 1,980,000 total rows. Zero data loss, but training dataset doubles and random duplicates risk severe overfitting.",
        "pitfalls": "Common Pitfall: Resampling before train/test split. If you upsample or downsample your entire dataset before splitting, data leakage occurs, giving misleadingly high evaluation scores. Always split first, apply resampling only to the training set, and evaluate on an untouched, naturally imbalanced test set. Also, remember that changing class ratios shifts predicted probabilities—apply probability calibration if exact real-world percentages are needed.",
        "core_logic": "Why this matters: In severely imbalanced datasets, models naturally get high accuracy by always guessing the majority class. Resampling levels the playing field during training so the loss function receives enough error signal to learn the patterns that define the rare class.",
        "architectural_logic": "In production pipelines, use imblearn.pipeline.Pipeline so resampling only happens inside training folds during cross-validation. For large-scale data, Balanced Ensembles (like EasyEnsemble or Balanced Random Forest) let you utilize 100% of majority data across multiple parallel models without training bottlenecks.",
        "connected_logic": [
            {
                "title": "Why Partial Resampling Beats 50/50",
                "content": "• Forcing a strict 1:1 split is rarely necessary and often throws away too much data or creates too many duplicates.\n• Moving an extreme 1:1,000 ratio up to 1:4 or 1:10 gives the model plenty of rare examples to learn while keeping training fast."
            },
            {
                "title": "Balanced Ensembles (EasyEnsemble)",
                "content": "• Instead of throwing away 90% of majority data, split the majority class into multiple random subsets.\n• Pair each subset with the minority class, train separate models, and average their predictions—keeping all majority data without slow training."
            },
            {
                "title": "The Overfitting Trap of Random Duplication",
                "content": "• Simply copying rare rows causes decision trees to create narrow leaves around exact duplicate coordinates.\n• If upsampling is necessary, SMOTE (synthetic interpolation) or cost-sensitive weighting is usually preferred over exact duplicates."
            },
            {
                "title": "Probability Calibration & Odds-Ratio Adjustment",
                "content": "• Resampling changes class proportions, making models output higher predicted probabilities than the true real-world rate.\n• The ranking order (ROC-AUC) stays accurate, but if you need true probabilities, recalibrate on untouched validation data using Platt scaling or isotonic regression."
            }
        ],
        "key_takeaways": [
            "Downsampling: Drops majority rows; fast and lightweight, best for massive datasets.",
            "Upsampling: Adds minority rows; zero data loss, essential when the rare class is very small.",
            "Partial Rebalance: A 1:4 or 1:10 ratio often works better than forcing a strict 50/50 split.",
            "Train Fold Only: Never resample test data; evaluate models on realistic, untouched data."
        ],
        "definition_bullets": [
            "Downsampling: Reducing majority class examples to balance training speed and memory.",
            "Upsampling: Increasing minority class examples to preserve majority data when rare samples are scarce."
        ]
    }

    # Update in concepts.json
    for c in concepts:
        if c.get("id") == "concept_resampling_strategies":
            c.update(resampling_data)
            print("Updated concept_resampling_strategies in concepts.json")
            break

    with open("src/data/concepts.json", "w", encoding="utf-8") as f:
        json.dump(concepts, f, indent=2, ensure_ascii=False)

    # Update in all_concepts.json
    for c in all_concepts:
        if c.get("id") == "concept_resampling_strategies":
            c.update(resampling_data)
            print("Updated concept_resampling_strategies in all_concepts.json")
            break

    with open("scripts/data_sources/all_concepts.json", "w", encoding="utf-8") as f:
        json.dump(all_concepts, f, indent=2, ensure_ascii=False)

    # Update in concepts_data_prep.py
    with open("scripts/data_sources/concepts_data_prep.py", "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r'\{\s*"id":\s*"concept_resampling_strategies".*?\},(?=\s*\{\s*"id":\s*"concept_cost_sensitive_weighting")'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        lines = json.dumps(resampling_data, indent=4, ensure_ascii=False).splitlines()
        indented_replacement = "\n".join("    " + line for line in lines) + ","
        new_content = content[:match.start()] + indented_replacement + content[match.end():]
        with open("scripts/data_sources/concepts_data_prep.py", "w", encoding="utf-8") as f:
            f.write(new_content)
        print("Updated concept_resampling_strategies in concepts_data_prep.py")
    else:
        print("Could not find regex match in concepts_data_prep.py")

if __name__ == "__main__":
    main()
