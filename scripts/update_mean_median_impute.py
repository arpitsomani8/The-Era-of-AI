import json

MEAN_MEDIAN_UPDATE = {
    "def": "Mean and Median Imputation are univariate techniques that replace missing numerical values with the computed arithmetic average or 50th percentile of observed data. Choosing between them depends on distribution symmetry and outlier presence.",
    "definition": "Mean and Median Imputation are univariate techniques that replace missing numerical values with the computed arithmetic average or 50th percentile of observed data. Choosing between them depends on distribution symmetry and outlier presence.",
    "formula": "$$\\hat{x}_i = \\mu = \\frac{1}{N_{\\text{obs}}} \\sum_{j \\in \\mathcal{O}} x_j, \\quad \\hat{x}_i = \\tilde{x} = \\text{Median}(X_{\\mathcal{O}}), \\quad M_i = \\mathbb{I}(x_i \\text{ is NaN})$$",
    "formula_explanation": "",
    "logic": "Mean is optimal for symmetric Gaussian distributions, while Median is robust to skewed data and extreme outliers. However, flat imputation shrinks variance and weakens feature correlations, requiring companion missing indicator flags and strict train-only fitting.",
    "example": "Employee salary table: In a dataset with salaries [$30k, $35k, $40k, NaN, $45k, NaN, $250k], the $250k executive outlier drags the Mean to $80k (falsely inflating typical salaries), while Median stays anchored at $40k.",
    "simple_summary": "Mean imputation replaces missing values with the average (use only for symmetric bell curves); Median replaces them with the middle value (use for skewed data and outliers). Always fit imputers strictly on the training set to prevent data leakage and add missing indicator flags.",
    "core_terms": [
        {
            "term": "Mean Imputation",
            "what_is_it": "• Replaces missing entries with the arithmetic average of all observed values: x̂ = (1/N) ∑ xᵢ.\n• Best suited strictly for symmetrically distributed (bell-shaped Gaussian) data with zero extreme outliers (e.g. adult heights, blood pressure).",
            "analogy": "Filling in an absent student's exam score with the exact class average when test scores follow a balanced bell curve.",
            "why_it_matters": "Provides a fast, computationally lightweight baseline for symmetric numerical features, but gets heavily pulled by extreme values."
        },
        {
            "term": "Median Imputation",
            "what_is_it": "• Replaces missing values with the 50th percentile (the middle number after sorting observed observations).\n• Highly robust to skewed distributions and extreme outliers (e.g. household income, real estate prices, transaction amounts).",
            "analogy": "Estimating an missing house price in a neighborhood by picking the middle home value rather than letting a single $20M mansion inflate the estimate.",
            "why_it_matters": "The industry standard univariate imputer for real-world financial, tabular, and e-commerce data that naturally exhibits right-skew."
        },
        {
            "term": "The Missing Indicator Flag",
            "what_is_it": "• A companion binary column added alongside the imputed feature, marking 1 if the value was originally missing and 0 if observed.\n• Preserves the valuable signal of 'missingness'—because why a customer withheld data is often highly predictive of churn or fraud.",
            "analogy": "Placing a bookmark on a repaired page in an encyclopedia noting that the original text was restored from community estimates.",
            "why_it_matters": "Allows tree-based models and neural networks to exploit missingness patterns rather than treating imputed values as genuine observations."
        }
    ],
    "types_header": "Imputation Mechanics & Strategic Variants",
    "types_badge": "Imputation Strategies",
    "quick_types": [
        {
            "type": "Mean Imputation",
            "definition": "Arithmetic sum divided by observed count. Use strictly on Gaussian symmetric distributions without outliers.",
            "looks_like": "df['val'].fillna(df['val'].mean())"
        },
        {
            "type": "Median Imputation",
            "definition": "Middle sorted value (50th percentile). Immune to tail outliers; the standard for skewed tabular data.",
            "looks_like": "df['val'].fillna(df['val'].median())"
        },
        {
            "type": "Grouped Conditional Imputation",
            "definition": "Fills missing values with the median of relevant subgroups (e.g. salary grouped by job title) to preserve domain context.",
            "looks_like": "df.groupby('Role')['Salary'].transform('median')"
        },
        {
            "type": "Missing Indicator Feature",
            "definition": "Appends a binary column (1 = was NaN, 0 = was observed) to retain predictive missingness patterns.",
            "looks_like": "df['val_is_nan'] = df['val'].isna().astype(int)"
        },
        {
            "type": "Train-Only Imputer Fit",
            "definition": "Statistics are calculated strictly on training folds and transformed across both train and test splits to prevent data leakage.",
            "looks_like": "imputer.fit(X_train).transform(X_test)"
        }
    ],
    "symbol_guide": [
        {
            "symbol": "x̂_i",
            "meaning": "Imputed Value",
            "plain_english": "The replacement value substituted into row i for a missing feature"
        },
        {
            "symbol": "μ (mu)",
            "meaning": "Sample Mean",
            "plain_english": "Arithmetic average of all observed training data points"
        },
        {
            "symbol": "x̃ (x-tilde)",
            "meaning": "Sample Median",
            "plain_english": "50th percentile sorted middle value of observed training points"
        },
        {
            "symbol": "N_obs",
            "meaning": "Observed Sample Count",
            "plain_english": "Number of non-null rows available for calculating the central tendency"
        },
        {
            "symbol": "O",
            "meaning": "Observed Index Set",
            "plain_english": "The subset of row indices where the feature value is present"
        },
        {
            "symbol": "M_i",
            "meaning": "Missing Indicator",
            "plain_english": "Binary flag equal to 1 if row i was originally NaN, 0 if observed"
        }
    ],
    "numerical_example": "Imputing Missing Salaries with an Extreme Outlier:\nObserved Training Salaries: [$30k, $35k, $40k, NaN, $45k, NaN, $250k] (Executive outlier = $250k)\n\n1. Calculate Mean vs. Median on Observed Values (N_obs = 5):\n   • Observed: [30, 35, 40, 45, 250]\n   • Mean μ = (30 + 35 + 40 + 45 + 250) / 5 = 400 / 5 = $80k\n   • Median x̃ = Middle value of sorted list [30, 35, 40, 45, 250] = $40k\n\n2. Comparing the Imputation Quality:\n   • Using Mean ($80k): Fills missing entries with $80k—higher than 80% of actual employees due to the single $250k outlier!\n   • Using Median ($40k): Fills missing entries with $40k—perfectly representative of typical staff.\n\n3. Applying Missing Indicator Flags:\n   • Row with $30k --> Salary = 30k, Salary_is_missing = 0\n   • Row with NaN  --> Salary = 40k, Salary_is_missing = 1.",
    "pitfalls": "Common Pitfall: Fitting the imputer on the entire dataset before splitting into train and test sets. This causes severe Data Leakage because test set values contaminate the training mean or median. Always split your data first, fit SimpleImputer strictly on X_train, and transform both X_train and X_test.",
    "core_logic": "Why this matters: Dropping rows with missing values (dropna) shrinks dataset size and introduces severe selection bias. Univariate imputation preserves training sample counts, but practitioners must counteract variance shrinkage and covariance dilution by adding missing indicator flags.",
    "architectural_logic": "In production ML pipelines, imputation is encapsulated inside Scikit-Learn Pipelines or ColumnTransformers. The trained median scalars are serialized into inference artifacts, ensuring incoming single-row real-time inference requests are imputed using identical training baselines.",
    "connected_logic": [
        {
            "title": "Variance Shrinkage: Artificially Narrow Confidence Intervals",
            "content": "• Replacing dozens of missing observations with a single central value clusters data unnaturally at the center, shrinking variance: Var(X_after) < Var(X_before).\n• This artificially deflates standard errors, making statistical hypothesis tests, t-statistics, and linear model p-values dangerously overconfident."
        },
        {
            "title": "Covariance Dilution: Weakening Feature Correlations",
            "content": "• Substituting a flat median ignores dependent interactions between features (e.g. age vs. income, engine size vs. fuel consumption).\n• Imputing unconditional constants dilutes the joint covariance Cov(X, Y), weakening the predictive correlation signals that downstream models rely on."
        },
        {
            "title": "The Fatal Data Leakage Anti-Pattern in Preprocessing",
            "content": "• Computing the mean or median over the entire dataset before train/test splitting leaks test set target distributions into training features.\n• Production pipelines must compute statistics strictly on training splits (e.g. via Scikit-Learn SimpleImputer), storing the trained scalar for production inference."
        },
        {
            "title": "Grouped Hierarchical Imputation in Production Feature Stores",
            "content": "• In enterprise recommendation and pricing systems, unconditional medians produce unrealistic feature values across diverse customer segments.\n• Production feature pipelines compute hierarchical grouped medians (e.g. Region -> Category -> Subcategory) to impute missing attributes with localized fidelity."
        }
    ],
    "key_takeaways": [
        "Selection Rule: Use Mean strictly for symmetric, bell-shaped data; use Median for skewed distributions and data with outliers.",
        "The 3 Hidden Risks: Univariate imputation shrinks variance, weakens feature correlations, and risks severe data leakage if fit before splitting.",
        "Essential Companion: Always pair imputation with a Missing Indicator column to retain the predictive signal of missingness.",
        "Pipeline Discipline: Calculate imputation statistics exclusively on training sets and apply that frozen scalar to validation and test sets."
    ],
    "definition_bullets": [
        "Mean Imputation: Replacing missing values with the arithmetic average of available data, appropriate only for symmetric distributions.",
        "Median Imputation: Replacing missing values with the 50th percentile of available data, robust against skewness and extreme outliers."
    ]
}

def update_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    found = False
    for item in data:
        if item.get('id') == 'concept_mean_median_impute':
            item.update(MEAN_MEDIAN_UPDATE)
            found = True
            break
            
    if not found:
        print(f"Warning: concept_mean_median_impute not found in {filepath}")
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
        if item.get('id') == 'concept_mean_median_impute':
            item.update(MEAN_MEDIAN_UPDATE)
            break
            
    new_content = '"""\nConcepts Database: Data Preparation & Exploration (22 Concepts)\n"""\n\nDATA_CONCEPTS = ' + json.dumps(mod.DATA_CONCEPTS, indent=4, ensure_ascii=False) + '\n'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Successfully updated {filepath}")

update_concepts_data_prep()
