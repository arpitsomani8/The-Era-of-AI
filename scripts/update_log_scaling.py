import json

LOG_SCALING_UPDATE = {
    "def": "Log Scaling and Power Transforms (Box-Cox and Yeo-Johnson) are non-linear transformations that reshape skewed, long-tailed feature distributions into symmetrical, bell-shaped Gaussian curves by compressing explosive values and stabilizing variance.",
    "definition": "Log Scaling and Power Transforms (Box-Cox and Yeo-Johnson) are non-linear transformations that reshape skewed, long-tailed feature distributions into symmetrical, bell-shaped Gaussian curves by compressing explosive values and stabilizing variance.",
    "formula": "$$x_{\\text{log1p}} = \\ln(1 + x), \\quad y^{(\\lambda)}_{\\text{Box-Cox}} = \\begin{cases} \\frac{y^\\lambda - 1}{\\lambda} & \\lambda \\neq 0 \\\\ \\ln(y) & \\lambda = 0 \\end{cases}, \\quad \\psi(\\lambda, y)_{\\text{Yeo-Johnson}}$$",
    "formula_explanation": "",
    "logic": "Linear scalers (Min-Max, StandardScaler) shift and shrink axes, but they never change distribution shape; skewed data stays skewed. Log and power transforms bend space non-linearly: they decelerate explosive growth, compress massive long tails, eliminate heteroscedasticity, and convert multiplicative relationships into simple additive ones.",
    "example": "E-commerce customer spend: Orders range from $2 to $50,000, heavily right-skewed. Taking np.log1p(spend) compresses the range into [1.09, 10.82], turning an extreme 80/20 power law into a smooth Gaussian distribution that linear and neural models can learn without gradient explosions.",
    "simple_summary": "Linear scalers only resize your data without changing its shape—if your data is heavily lopsided, it stays lopsided. Log scaling (log1p) and Power Transforms (Box-Cox and Yeo-Johnson) physically bend the numbers to turn extreme, lopsided spikes into balanced, bell-shaped curves. Yeo-Johnson is the universal modern default because it handles positives, zeros, and negative numbers.",
    "core_terms": [
        {
            "term": "Log Scaling (log1p & Compressing Long Tails)",
            "what_is_it": "• Replacing raw numbers with their logarithm (ln(1 + x)) to compress explosive right-skewed features like salary, web views, or follower counts.\n• Leaves small numbers relatively untouched while dramatically shrinking gigantic numbers, and adding 1 (log1p) safely handles zero values without crashing into negative infinity.",
            "analogy": "The Richter scale for earthquakes: an earthquake of magnitude 7 is 10 times stronger than a 6, and 100 times stronger than a 5, fitting both tiny tremors and massive catastrophes onto a simple 1-to-10 chart.",
            "why_it_matters": "Turns extreme exponential distributions into manageable linear ranges, preventing high-magnitude outliers from destabilizing regression models."
        },
        {
            "term": "Box-Cox Power Transform (Auto-Tuning Power Curves)",
            "what_is_it": "• A parametric statistical transform that automatically searches for the best exponent (λ) using Maximum Likelihood Estimation to reshape skewed data into a symmetrical bell curve.\n• Strict Requirement: Only works on strictly positive numbers (x > 0); if your data contains zero or negative values, Box-Cox will crash.",
            "analogy": "A tailor adjusting pants with an adjustable sliding belt buckle (λ) until the fit is completely symmetrical, but the belt only fits adults (positive numbers).",
            "why_it_matters": "Automatically discovers the optimal mathematical power curve without manual guessing, maximizing model normality."
        },
        {
            "term": "Yeo-Johnson Power Transform (The Universal Scaler)",
            "what_is_it": "• The modern, universal upgrade to Box-Cox that works seamlessly on all real numbers—strictly positive, zero, AND negative values.\n• Automatically optimizes its power parameter (λ) to reduce skewness and stabilize variance, making it the premier default power transform in machine learning.",
            "analogy": "A universal electrical travel adapter that safely plugs into any wall outlet across the world, whether the power is positive, zero, or reversed.",
            "why_it_matters": "Removes the positive-only restriction of Box-Cox, allowing data scientists to normalize features with profit/loss metrics, temperature, or net changes."
        }
    ],
    "types_header": "Transform Methods & Input Capabilities",
    "types_badge": "Non-Linear Geometry",
    "quick_types": [
        {
            "type": "np.log1p(x) [Natural Log + 1]",
            "definition": "Vectorized log transform with 1 added; handles positive values and zero cleanly without returning -inf.",
            "looks_like": "df['views_log'] = np.log1p(df['views'])"
        },
        {
            "type": "PowerTransformer(method='box-cox')",
            "definition": "Scikit-Learn transformer finding optimal λ via MLE; strictly requires positive numbers (x > 0).",
            "looks_like": "PowerTransformer(method='box-cox').fit_transform(X)"
        },
        {
            "type": "PowerTransformer(method='yeo-johnson')",
            "definition": "Universal Scikit-Learn power transformer handling positive, zero, and negative values smoothly.",
            "looks_like": "PowerTransformer(method='yeo-johnson').fit_transform(X)"
        },
        {
            "type": "Square Root Transform (np.sqrt)",
            "definition": "Mild power transform (λ = 0.5) frequently used on Poisson count data (e.g. daily accidents, retail visits).",
            "looks_like": "df['counts_sqrt'] = np.sqrt(df['counts'])"
        },
        {
            "type": "Inverse Transform (expm1)",
            "definition": "Reversing log-predictions back into real-world dollar or count units at inference time.",
            "looks_like": "y_pred_dollars = np.expm1(y_pred_log)"
        }
    ],
    "symbol_guide": [
        {
            "symbol": "x_log1p",
            "meaning": "Log1p Transformed Value",
            "plain_english": "The resulting value after calculating ln(1 + x), safe for zero inputs"
        },
        {
            "symbol": "x, y",
            "meaning": "Raw Feature Observation",
            "plain_english": "The original unscaled numerical measurement before non-linear transformation"
        },
        {
            "symbol": "λ (lambda)",
            "meaning": "Power Transformation Parameter",
            "plain_english": "The exponent auto-tuned via Maximum Likelihood Estimation to maximize normality"
        },
        {
            "symbol": "y^(λ)",
            "meaning": "Box-Cox Transformed Output",
            "plain_english": "Variance-stabilized output value valid strictly for positive values y > 0"
        },
        {
            "symbol": "ψ(λ, y)",
            "meaning": "Yeo-Johnson Transformed Output",
            "plain_english": "Universal power transform output valid across positive, zero, and negative values"
        }
    ],
    "numerical_example": "Transforming Website Traffic Across Accounts:\nRaw view counts: [0, 9, 99, 999, 9999] (Spans 4 orders of magnitude from 0 to 10,000)\n\n1. Log1p Transformation (x_log = ln(1 + x)):\n   • Account 1 (0 views): ln(1 + 0) = ln(1) = 0.000 (safely preserved, zero stays zero!)\n   • Account 2 (9 views): ln(1 + 9) = ln(10) ≈ 2.303\n   • Account 3 (99 views): ln(1 + 100) ≈ 4.605\n   • Account 4 (999 views): ln(1 + 1000) ≈ 6.908\n   • Account 5 (9999 views): ln(1 + 10000) ≈ 9.210\n   Spacing: Equal multiplicative steps (×10) now become uniform additive steps (+2.30)!\n\n2. Box-Cox Calculation with λ = 0.5 (Square Root Scale, y > 0):\n   • y = 9: y^(0.5) = (√9 - 1) / 0.5 = (3 - 1) / 0.5 = 4.0\n   • y = 25: y^(0.5) = (√25 - 1) / 0.5 = (5 - 1) / 0.5 = 8.0\n   • y = 49: y^(0.5) = (√49 - 1) / 0.5 = (7 - 1) / 0.5 = 12.0\n\nOutcome: Wild exponential gaps are compressed into balanced linear increments, converting power law chaos into a well-behaved distribution for gradient descent.",
    "pitfalls": "Common Pitfall: Calling np.log() on zero or negative values, which yields -inf and NaN values that silently corrupt downstream model weights. Always use np.log1p() for non-negative data with zeros. For data containing negative numbers or where optimal power tuning is needed, never force Box-Cox (which throws a ValueError on values <= 0); use Yeo-Johnson instead.",
    "core_logic": "Why this matters: In tabular and linear machine learning, skewed distributions violate homoscedasticity and cause long-tail observations to exert excessive leverage on regression lines. Non-linear transforms stabilize variance across the range and reshape features to satisfy Gaussian assumptions.",
    "architectural_logic": "In production ML pipelines, PowerTransformer is serialized inside Scikit-Learn Pipeline objects. Parameter λ is learned strictly on training splits via Maximum Likelihood Estimation, and inverse transformations (inverse_transform or np.expm1) are executed on model predictions before surfacing results to end-user applications.",
    "connected_logic": [
        {
            "title": "Homoscedasticity & Constant Residual Variance",
            "content": "• In ordinary least squares (OLS) regression, right-skewed targets cause prediction error variance to balloon as predicted values increase (heteroscedasticity).\n• Applying a log or power transform stabilizes conditional error variance across the entire dynamic range, satisfying classical Gauss-Markov assumptions for valid statistical inference."
        },
        {
            "title": "Multiplicative Relationships Converted to Additive Models",
            "content": "• Real-world phenomena like viral network growth, compound interest, or marketing elasticity scale multiplicatively: Y = A · X₁^(β₁) · X₂^(β₂).\n• Taking logarithms converts multiplicative dynamics into linear sums: ln(Y) = ln(A) + β₁·ln(X₁) + β₂·ln(X₂), enabling simple linear models to capture complex non-linear physics."
        },
        {
            "title": "The Zero-Value Barrier & Shift Offsets",
            "content": "• When features contain true structural zeros (e.g. 0 past purchases, 0 days delinquent), raw ln(x) fails with a domain error (-inf).\n• While log1p cleanly solves zeros at x = 0, negative values strictly require Yeo-Johnson or an explicit positive shift constant (x + |x_min| + 1) before fitting parametric Box-Cox models."
        },
        {
            "title": "Strict Train-Fold Fitting for Parameter λ",
            "content": "• Estimating the optimal Box-Cox or Yeo-Johnson power parameter λ using Maximum Likelihood on the combined dataset leaks validation distribution shapes into training.\n• Production pipelines encapsulate PowerTransformer inside Scikit-Learn Pipelines, fitting λ strictly on training folds and storing it for immutable test and inference scoring."
        }
    ],
    "key_takeaways": [
        "Non-Linear Reshaping: Unlike linear scalers, log and power transforms bend space to turn skewed, long-tailed data into symmetrical bell curves.",
        "Zero-Safe Log1p: Use np.log1p(x) = ln(1 + x) to compress right-skewed data that includes zeros without producing negative infinity.",
        "Box-Cox Positivity Constraint: Automatically finds optimal power λ via MLE, but strictly requires positive inputs (x > 0).",
        "Yeo-Johnson Universal Scope: The modern standard power transform handling positive, zero, and negative values smoothly."
    ],
    "definition_bullets": [
        "Log Scaling: Applying logarithmic compression (such as log1p) to shrink explosive right-skewed long tails into manageable linear scales.",
        "Power Transforms: Parametric transformations (Box-Cox, Yeo-Johnson) that auto-tune an exponent λ to transform arbitrary distributions into Gaussian shapes."
    ]
}

def update_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    found = False
    for item in data:
        if item.get('id') == 'concept_log_scaling':
            item.update(LOG_SCALING_UPDATE)
            found = True
            break
            
    if not found:
        print(f"Warning: concept_log_scaling not found in {filepath}")
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
        if item.get('id') == 'concept_log_scaling':
            item.update(LOG_SCALING_UPDATE)
            break
            
    new_content = '"""\nConcepts Database: Data Preparation & Exploration (22 Concepts)\n"""\n\nDATA_CONCEPTS = ' + json.dumps(mod.DATA_CONCEPTS, indent=4, ensure_ascii=False) + '\n'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Successfully updated {filepath}")

update_concepts_data_prep()
