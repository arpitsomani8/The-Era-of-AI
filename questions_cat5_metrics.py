"""Category 5: Evaluation Metrics, Data Preprocessing & Statistical Testing (Questions 96-115)"""

CAT5_QUESTIONS = [
    {
        "id": "metrics_96",
        "category": "metrics_data",
        "category_label": "Evaluation Metrics & Preprocessing",
        "difficulty": "Junior / Mid",
        "company_tags": ["Google", "Amazon", "Meta", "Apple"],
        "question": "Compare Precision, Recall, and F1-Score. Give concrete real-world business scenarios where you must prioritize Recall over Precision, and vice versa.",
        "answer": """**1. Mathematical Definitions:**
- **Precision:** $\\frac{TP}{TP + FP}$ (Out of all positive predictions, what fraction was actually correct? Penalty for false alarms).
- **Recall (Sensitivity):** $\\frac{TP}{TP + FN}$ (Out of all actual positive cases, what fraction did the model find? Penalty for missed cases).
- **F1-Score:** Harmonic mean: $2 \\cdot \\frac{\\text{Precision} \\cdot \\text{Recall}}{\\text{Precision} + \\text{Recall}}$. Uses harmonic mean because it heavily penalizes extreme trade-offs (e.g. Precision=1.0, Recall=0.01 yields F1 $\\approx 0.02$, whereas arithmetic mean would be 0.505).

**2. Prioritize Recall over Precision (Cost of FN $\\gg$ Cost of FP):**
- **Cancer Detection / Medical Screening:** A false negative (missing a malignant tumor) results in patient death. A false positive merely triggers a harmless follow-up biopsy. We want Recall $> 99\\%$.
- **Airport Weapon / Explosives Scanner:** Missing a concealed weapon on an airplane is catastrophic.

**3. Prioritize Precision over Recall (Cost of FP $\\gg$ Cost of FN):**
- **Spam Email Filter:** A false positive means a critical legal contract or family email is banished to the junk folder. Users tolerate occasional spam reaching their inbox (false negatives) far more than missing important real emails.
- **YouTube Copyright Takedown Bots:** Falsely terminating a legitimate creator's channel causes immense PR and legal liability.""",
        "tip": "Explain why the harmonic mean is used for F1 instead of the arithmetic mean: it forces both precision and recall to be balanced."
    },
    {
        "id": "metrics_97",
        "category": "metrics_data",
        "category_label": "Evaluation Metrics & Preprocessing",
        "difficulty": "Mid / Senior",
        "company_tags": ["Stripe", "Visa", "PayPal", "Meta"],
        "question": "Why is PR-AUC (Precision-Recall Area Under Curve) significantly more informative than ROC-AUC when evaluating highly imbalanced datasets (e.g. 0.1% fraud)?",
        "answer": """**1. ROC-AUC vs PR-AUC Definitions:**
- **ROC Curve:** Plots True Positive Rate (Recall) vs False Positive Rate:
  $$\\text{TPR} = \\frac{TP}{TP + FN}, \\quad \\text{FPR} = \\frac{FP}{FP + TN}$$
- **PR Curve:** Plots Precision vs Recall:
  $$\\text{Precision} = \\frac{TP}{TP + FP}, \\quad \\text{Recall} = \\frac{TP}{TP + FN}$$

**2. The True Negative (TN) Delusion in ROC-AUC:**
Consider a fraud dataset with $1,000,000$ non-fraud transactions and $1,000$ fraud transactions (0.1% fraud rate):
Suppose a model produces **$10,000$ false positives** (FP):
$$\\text{FPR} = \\frac{10,000}{10,000 + 990,000} = \\frac{10,000}{1,000,000} = 0.01 \\quad (1\\%!)$$
Because $TN$ is massive ($1,000,000$), the denominator of FPR drowns out the false positives.
- The ROC-AUC curve looks magnificent (e.g. $\\text{ROC-AUC} = 0.98$).
- **The Reality:** Out of $11,000$ positive alerts, $10,000$ are false alarms! Precision is a disastrous:
  $$\\text{Precision} = \\frac{1,000}{1,000 + 10,000} = 0.09 \\quad (9\\%!)$$
  91% of user transactions alerted are legitimate customers blocked!
- **PR-AUC ignores $TN$ entirely.** It directly penalizes the 10,000 false alarms in the denominator of Precision ($TP + FP$), exposing the model's actual catastrophic production performance.""",
        "tip": "Rule of thumb: If positive class prevalence is $< 5\\%$, always report PR-AUC and Average Precision (AP), never ROC-AUC alone."
    },
    {
        "id": "metrics_98",
        "category": "metrics_data",
        "category_label": "Evaluation Metrics & Preprocessing",
        "difficulty": "Mid / Senior",
        "company_tags": ["Two Sigma", "Google", "Databricks"],
        "question": "What is Data Leakage in machine learning? Explain the 3 most common leakage pitfalls and how to prevent them in production pipelines.",
        "answer": """**1. Definition:**
Data leakage occurs when information from outside the training dataset (especially information from the test set or future events) is inadvertently used to train the model, producing artificially inflated cross-validation metrics that fail completely in production.

**2. 3 Common Leakage Pitfalls:**
1. **Preprocessing / Scaling Before Train-Test Split (Global Preprocessing):**
   - *Mistake:* Computing global mean/std or fitting an imputer across the entire dataset before splitting into train/test:
     $$x_{scaled} = \\frac{x - \\mu_{global}}{\\sigma_{global}}$$
     The training set now has implicit access to test set distribution parameters.
   - *Fix:* Fit scalers, imputers, and encoders strictly on the training partition: `scaler.fit(X_train)`, then call `scaler.transform(X_test)`.
2. **Temporal Leakage (Time-Travel Features):**
   - *Mistake:* Using a future feature to predict a past event (e.g. using customer lifetime value at day 90 to predict churn at day 30, or using random K-fold CV on time-series data).
   - *Fix:* Strict point-in-time feature extraction and `TimeSeriesSplit` (Walk-Forward validation).
3. **Group Leakage (Patient / User Correlation):**
   - *Mistake:* An individual patient has 20 X-ray scans. Random splitting places 15 scans in train and 5 scans in test. The model memorizes patient anatomy rather than disease pathology.
   - *Fix:* Use `GroupKFold` on `patient_id` so an entity's data never spans both train and test.""",
        "tip": "Mention scikit-learn `Pipeline` objects as the standard engineering defense against preprocessing leakage."
    },
    {
        "id": "metrics_99",
        "category": "metrics_data",
        "category_label": "Evaluation Metrics & Preprocessing",
        "difficulty": "Mid / Senior",
        "company_tags": ["Meta", "Amazon", "Apple"],
        "question": "Compare methods for handling Extreme Class Imbalance: Downsampling, Oversampling (SMOTE), Class Weights, and Focal Loss.",
        "answer": """**1. Resampling:**
- **Random Downsampling:** Discards majority class samples to achieve balance. Fast, but discards vast amounts of useful information.
- **SMOTE (Synthetic Minority Over-sampling Technique):** Synthesizes artificial minority samples by interpolating between nearest minority neighbors in feature space:
  $$x_{new} = x_i + \\lambda (x_{zi} - x_i), \\quad \\lambda \\sim U(0, 1)$$
  - *Risk:* In high dimensions or overlapping spaces, SMOTE synthesizes unrealistic noise points across decision boundaries.

**2. Cost-Sensitive Learning (Class Weights):**
Weights minority samples heavily in standard cross-entropy loss:
$$w_{pos} = \\frac{N_{total}}{2 \\cdot N_{pos}}$$
Simple and preserves all data, but linear weighting does not differentiate between easy vs hard minority examples.

**3. Focal Loss (Lin et al., RetinaNet, 2017):**
Dynamically downweights the loss assigned to easy, well-classified examples:
$$\\text{FL}(p_t) = -\\alpha_t (1 - p_t)^\\gamma \\log(p_t)$$
where $\\gamma$ is the focusing parameter (typically $\\gamma = 2.0$).
- If an example is well-classified ($p_t = 0.99$), the modulating factor $(1 - p_t)^2 = (0.01)^2 = 0.0001$. Its loss contribution is scaled down by **$10,000\\times$**!
- Forces model gradients to concentrate exclusively on hard, ambiguous false negatives. State-of-the-art for dense object detection and extreme fraud classification.""",
        "tip": "Explain that Focal Loss was invented because millions of easy background pixels overwhelmed gradients in one-stage object detectors."
    },
    {
        "id": "metrics_100",
        "category": "metrics_data",
        "category_label": "Evaluation Metrics & Preprocessing",
        "difficulty": "Mid",
        "company_tags": ["Google", "Bloomberg"],
        "question": "What is the difference between Mean Absolute Error (MAE), Mean Squared Error (MSE), and Huber Loss? When should each be used?",
        "answer": """**1. Formulations:**
- **MAE ($L_1$ Loss):** $\\frac{1}{n} \\sum |y_i - \\hat{y}_i|$
  - Gradient is constant $\\pm 1$.
  - Robust to extreme outliers.
  - Predicts the **conditional median** of the distribution.
  - Non-differentiable at $0$.
- **MSE ($L_2$ Loss):** $\\frac{1}{n} \\sum (y_i - \\hat{y}_i)^2$
  - Gradient is proportional to error: $2(y - \\hat{y})$.
  - Heavily penalizes large errors quadratically. Extremely sensitive to outliers.
  - Predicts the **conditional mean** of the distribution.
- **Huber Loss (Smooth $L_1$):**
  $$L_\\delta(y, \\hat{y}) = \\begin{cases} \\frac{1}{2}(y - \\hat{y})^2 & \\text{for } |y - \\hat{y}| \\le \\delta \\\\ \\delta (|y - \\hat{y}| - \\frac{1}{2}\\delta) & \\text{otherwise} \\end{cases}$$
  - Quadratic (MSE) for small errors (smooth convergence around 0).
  - Linear (MAE) for large errors (robust against wild outliers). Combining the best of both worlds!""",
        "tip": "Connect the loss function directly to the statistical statistic: MSE predicts the mean; MAE predicts the median; Quantile loss predicts the percentile."
    },
    {
        "id": "metrics_101",
        "category": "metrics_data",
        "category_label": "Evaluation Metrics & Preprocessing",
        "difficulty": "Junior / Mid",
        "company_tags": ["Uber", "DoorDash"],
        "question": "What is Mean Absolute Percentage Error (MAPE)? What is its fatal mathematical flaw, and what metric solves it?",
        "answer": """**1. Formula:**
$$\\text{MAPE} = \\frac{100\\%}{n} \\sum_{i=1}^n \\left| \\frac{y_i - \\hat{y}_i}{y_i} \\right|$$
Measures percentage relative error. Highly popular in business reporting because it is unit-free and easy for non-technical executives to interpret.

**2. The Fatal Flaw (Division by Zero & Asymmetric Penalties):**
- **Division by Zero:** If actual value $y_i = 0$ (e.g. zero sales for a product on Sunday), MAPE involves division by zero and explodes to $\\infty$.
- **Asymmetric Penalty:**
  - If actual $y = 100$ and model predicts $\\hat{y} = 200$ (overprediction), error is $100\\%$.
  - If actual $y = 100$ and model predicts $\\hat{y} = 0$ (underprediction), error can never exceed $100\\%$.
  - MAPE severely penalizes positive over-forecasts while giving an artificial pass to under-forecasting zero.

**3. Solutions:**
- **Symmetric MAPE (sMAPE):**
  $$\\text{sMAPE} = \\frac{100\\%}{n} \\sum \\frac{|y_i - \\hat{y}_i|}{(|y_i| + |\\hat{y}_i|) / 2}$$
  Bounds percentage error between $[0, 200\\%]$.
- **Weighted MAPE (WAPE):** $\\frac{\\sum |y_i - \\hat{y}_i|}{\\sum y_i}$ (Aggregates errors before dividing, avoiding zero-division).""",
        "tip": "In demand forecasting interviews, suggest WAPE over MAPE to show real-world operational maturity."
    },
    {
        "id": "metrics_102",
        "category": "metrics_data",
        "category_label": "Evaluation Metrics & Preprocessing",
        "difficulty": "Mid",
        "company_tags": ["Goldman Sachs", "Citadel", "Capital One"],
        "question": "When should you use Stratified K-Fold, Group K-Fold, and TimeSeriesSplit (Walk-Forward) cross-validation?",
        "answer": """- **Stratified K-Fold:**
  - *When to use:* Imbalanced classification problems (e.g. 1% positive class).
  - *Mechanism:* Ensures that every single fold contains the exact same percentage proportion of target classes as the overall population. Standard K-fold could produce a fold with zero positive samples.
- **Group K-Fold:**
  - *When to use:* Non-independent, clustered observations (e.g. multiple transactions per customer, multiple medical images per patient).
  - *Mechanism:* Ensures that all observations from a specific group/entity exist exclusively in the training fold OR the test fold, never split across both. Prevents identity memorization leakage.
- **TimeSeriesSplit (Walk-Forward / Expanding Window):**
  - *When to use:* Sequential, financial, or time-series data.
  - *Mechanism:* Training data is restricted to historical past; validation is strictly the future:
    - Fold 1: Train on Months 1-3, Validate on Month 4.
    - Fold 2: Train on Months 1-4, Validate on Month 5.
    - Fold 3: Train on Months 1-5, Validate on Month 6.
  - *Never* use standard random K-fold on time series; it causes massive look-ahead leakage.""",
        "tip": "Emphasize that using standard K-fold on time-series data is the #1 reason quant trading strategies fail in live production."
    },
    {
        "id": "metrics_103",
        "category": "metrics_data",
        "category_label": "Evaluation Metrics & Preprocessing",
        "difficulty": "Junior / Mid",
        "company_tags": ["Amazon", "Google"],
        "question": "Compare Outlier Detection methods: IQR (Interquartile Range), Z-Score, and Isolation Forest. When is each appropriate?",
        "answer": """- **Z-Score Method ($z = \\frac{x - \\mu}{\\sigma}$):**
  - Assumes feature is **normally distributed**. Points with $|z| > 3$ ($>3$ standard deviations from mean) are flagged.
  - *Flaw:* The mean and standard deviation themselves are distorted by extreme outliers!
- **IQR (Tukey's Fences):**
  - Non-parametric: $\\text{IQR} = Q_3 - Q_1$. Outliers are points $< Q_1 - 1.5 \\text{ IQR}$ or $> Q_3 + 1.5 \\text{ IQR}$.
  - Robust against skewed distributions because median and quartiles are resistant to extreme values. Fast for single 1D numerical features.
- **Isolation Forest (Liu et al., 2008):**
  - Multi-dimensional, non-parametric tree ensemble.
  - *Principle:* Recursively isolates points by randomly picking a feature and random split value.
  - *Logic:* Anomalies are few and topologically isolated, meaning they are isolated near the **shallow root** of the tree (short average path length $h(x)$). Normal cluster points require many deep splits.
  - *Strength:* Handles multi-dimensional non-linear feature interactions seamlessly.""",
        "tip": "Use Isolation Forest for complex multivariate anomaly detection; use IQR for simple univariate feature cleaning."
    },
    {
        "id": "metrics_104",
        "category": "metrics_data",
        "category_label": "Evaluation Metrics & Preprocessing",
        "difficulty": "Junior / Mid",
        "company_tags": ["Microsoft", "Meta"],
        "question": "Compare Feature Scaling techniques: Min-Max Normalization, Standardization (Z-score), and RobustScaler. When should you choose RobustScaler?",
        "answer": """- **Min-Max Normalization:**
  $$x' = \\frac{x - x_{\\min}}{x_{\\max} - x_{\\min}}$$
  - Binds features strictly to $[0, 1]$ (or $[-1, 1]$).
  - *Flaw:* Extreme outliers crush all normal data points into an infinitesimally narrow band (e.g. $[0, 0.01]$).
- **Standardization (StandardScaler):**
  $$z = \\frac{x - \\mu}{\\sigma}$$
  - Centers data to mean $0$, unit variance $1$.
  - Does not bound features to a fixed range. Still sensitive to outliers during mean/variance computation.
- **RobustScaler:**
  $$x' = \\frac{x - \\text{median}}{\\text{IQR}} = \\frac{x - Q_2}{Q_3 - Q_1}$$
  - Centers around the median and scales by the Interquartile Range.
  - **Best choice when dataset contains severe outliers:** Outliers cannot distort the median or the 25th-75th percentile spread.""",
        "tip": "Mention that RobustScaler is standard in financial econometric pipelines where fat-tailed distributions and flash-crashes occur."
    },
    {
        "id": "metrics_105",
        "category": "metrics_data",
        "category_label": "Evaluation Metrics & Preprocessing",
        "difficulty": "Mid / Senior",
        "company_tags": ["Google", "Meta", "Netflix"],
        "question": "Differentiate between Missing Data mechanisms: MCAR, MAR, and MNAR. Why is dropping rows dangerous when data is MNAR?",
        "answer": """**1. Missing Completely at Random (MCAR):**
- Missingness is completely independent of both observed and unobserved data: $P(M | Y_{obs}, Y_{mis}) = P(M)$.
- *Example:* A lab technician randomly drops a test tube on the floor.
- Complete case analysis (dropping rows) is unbiased, but reduces statistical power.

**2. Missing at Random (MAR):**
- Missingness depends systematically on **observed data**, but not on the missing value itself: $P(M | Y_{obs}, Y_{mis}) = P(M | Y_{obs})$.
- *Example:* Men are less likely to report depression symptoms, but within the recorded gender attribute, missingness is random.
- Solved via Multiple Imputation (MICE) conditioned on observed variables.

**3. Missing Not at Random (MNAR - Non-Ignorable):**
- Missingness depends directly on the **unobserved missing value itself**: $P(M | Y_{obs}, Y_{mis}) = P(M | Y_{mis})$.
- *Example:* Patients with extreme drug addiction or ultra-high income refuse to disclose their status on a survey.
- **Danger:** Dropping rows or using mean imputation creates severe, catastrophic **selection bias** that skews model parameters and draws false causal conclusions. Requires explicit selection modeling (Heckman correction).""",
        "tip": "Cite Donald Rubin's 1976 seminal framework for missing data mechanisms."
    },
    {
        "id": "metrics_106",
        "category": "metrics_data",
        "category_label": "Evaluation Metrics & Preprocessing",
        "difficulty": "Mid / Senior",
        "company_tags": ["Databricks", "Amazon"],
        "question": "What is MICE (Multivariate Imputation by Chained Equations)? Why is it statistically superior to Mean or Median imputation?",
        "answer": """**1. The Flaw of Mean/Median Imputation:**
- Mean imputation artificially reduces feature variance ($\\text{Var}(X) \\downarrow$).
- Distorts correlation relationships between features.
- Treats imputed numbers as absolute certain facts, ignoring imputation uncertainty.

**2. MICE Algorithm (Fully Conditional Specification):**
Operates under the assumption that missing values can be predicted using all other variables:
1. Impute temporary placeholder means for all missing values.
2. For each feature $X_j$ with missing values:
   - Treat $X_j$ as the target variable $y$.
   - Treat all other features $X_{-j}$ as predictors.
   - Train a regression model (e.g. Bayesian Ridge or Random Forest) on observed samples: $X_j \\sim X_{-j}$.
   - Predict and replace the missing values in $X_j$.
3. Cycle through all features $j = 1, \\dots, p$ iteratively for 10-20 cycles until imputed values stabilize.
- **Statistical Superiority:** Preserves complex multivariate relationships, covariance matrices, and variance distributions across features.""",
        "tip": "Mention scikit-learn's `IterativeImputer` as the standard implementation of MICE in Python."
    },
    {
        "id": "metrics_107",
        "category": "metrics_data",
        "category_label": "Evaluation Metrics & Preprocessing",
        "difficulty": "Junior / Mid",
        "company_tags": ["Apple", "Amazon", "Capital One"],
        "question": "What is the Central Limit Theorem (CLT)? What are the exact conditions required for it to hold, and why is it fundamental to A/B testing?",
        "answer": """**1. Formal Definition:**
Let $X_1, X_2, \\dots, X_n$ be independent and identically distributed (i.i.d.) random variables with arbitrary population distribution having finite mean $\\mu$ and finite variance $\\sigma^2$.
As sample size $n \\to \\infty$, the normalized sample mean $\\bar{X}_n = \\frac{1}{n} \\sum X_i$ converges in distribution to a standard Normal distribution:
$$\\sqrt{n} \\left( \\frac{\\bar{X}_n - \\mu}{\\sigma} \\right) \\xrightarrow{d} \\mathcal{N}(0, 1)$$

**2. Exact Conditions:**
1. Finite population variance $\\sigma^2 < \\infty$ (fails on heavy-tailed distributions like Cauchy or Pareto with $\\alpha \\le 2$).
2. Observations must be independent (fails on temporal or correlated samples).

**3. Why it is Fundamental to A/B Testing:**
User metrics in online experiments (e.g. revenue per user, time spent) are heavily skewed, non-normal distributions with massive zero-spikes.
Because of the CLT, the **difference in sample means** between Variant A and Variant B ($\\bar{X}_B - \\bar{X}_A$) is guaranteed to be asymptotically normally distributed when $n > 1000$, enabling valid two-sample Z-tests and t-tests without knowing the underlying user revenue distribution!""",
        "tip": "Emphasize that the CLT applies to the distribution of the sample mean, NOT to the raw individual data points!"
    },
    {
        "id": "metrics_108",
        "category": "metrics_data",
        "category_label": "Evaluation Metrics & Preprocessing",
        "difficulty": "Mid / Senior",
        "company_tags": ["Meta", "Google", "Netflix"],
        "question": "What is a p-value in hypothesis testing? Differentiate between Type I ($\\alpha$) and Type II ($\\beta$) errors, and define Statistical Power.",
        "answer": """**1. Exact Definition of p-value:**
The probability of observing a test statistic at least as extreme as the one calculated from the sample data, **assuming the Null Hypothesis ($H_0$) is strictly true**.
- *Common Misconception:* It is NOT the probability that the null hypothesis is true! It is $P(\\text{Data} | H_0)$, not $P(H_0 | \\text{Data})$.

**2. Type I vs Type II Errors:**
- **Type I Error ($\\alpha$ - False Positive):** Rejecting the Null Hypothesis when it was actually true (e.g. concluding a drug works when it is completely ineffective). Standard: $\\alpha = 0.05$.
- **Type II Error ($\\beta$ - False Negative):** Failing to reject the Null Hypothesis when it was actually false (e.g. missing a genuinely effective new feature).

**3. Statistical Power ($1 - \\beta$):**
The probability of correctly rejecting the Null Hypothesis when an actual effect exists:
$$\\text{Power} = 1 - \\beta = P(\\text{Reject } H_0 | H_1 \\text{ is true})$$
Standard target: $80\\%$ or $90\\%$ power. A low-power test has a high risk of abandoning winning features.""",
        "tip": "State clearly: 'A p-value is $P(\\text{extreme data} | H_0)$, never $P(H_0 | \\text{data})$'. Interviewers penalize imprecise definitions."
    },
    {
        "id": "metrics_109",
        "category": "metrics_data",
        "category_label": "Evaluation Metrics & Preprocessing",
        "difficulty": "Senior",
        "company_tags": ["Meta", "Netflix", "Booking.com"],
        "question": "How do you calculate required Sample Size for an A/B test? Explain how Significance Level ($\\alpha$), Power ($1-\\beta$), and Minimum Detectable Effect (MDE) dictate sample size.",
        "answer": """**1. Sample Size Formula (Two-Sample Z-Test for Proportions):**
$$n = \\frac{2 \\left( Z_{1 - \\alpha/2} + Z_{1 - \\beta} \\right)^2 \\sigma^2}{\\text{MDE}^2}$$
where:
- $Z_{1 - \\alpha/2}$: Critical value for significance level (e.g. 1.96 for $\\alpha=0.05$).
- $Z_{1 - \\beta}$: Critical value for statistical power (e.g. 0.84 for $80\\%$ power, 1.28 for $90\\%$ power).
- $\\sigma^2$: Variance of metric ($p(1-p)$ for conversion rate).
- $\\text{MDE} = \\mu_B - \\mu_A$: Minimum Detectable Effect (smallest practical lift we care to detect).

**2. Relationships & Trade-offs:**
- **Inverse Square Relationship with MDE ($n \\propto 1 / \\text{MDE}^2$):** If you want to detect a lift of $1\\%$ instead of $2\\%$ (half the MDE), you need **$4\\times$ as much sample size**!
- Higher Power ($90\\%$ vs $80\\%$) requires larger sample size.
- Lower Significance (e.g. $\\alpha = 0.01$ to be extra confident) increases required sample size.""",
        "tip": "Explain that MDE is a business decision: what is the minimum revenue/conversion lift worth engineering effort?"
    },
    {
        "id": "metrics_110",
        "category": "metrics_data",
        "category_label": "Evaluation Metrics & Preprocessing",
        "difficulty": "Mid / Senior",
        "company_tags": ["Google", "Meta", "Spotify"],
        "question": "What is the Multiple Testing Problem in experimentation? Compare Bonferroni Correction and False Discovery Rate (Benjamini-Hochberg).",
        "answer": """**1. The Multiple Testing Crisis:**
If you test a single metric at $\\alpha = 0.05$, the false positive probability is $5\\%$.
If an A/B test tracks 20 independent metrics or you test 20 variants:
$$P(\\text{At least one False Positive}) = 1 - (1 - 0.05)^{20} = 1 - 0.358 = \\mathbf{64.2\\%!}$$
You are almost guaranteed to find a 'statistically significant' winning metric by pure chance!

**2. Bonferroni Correction (Controls Family-Wise Error Rate - FWER):**
Enforces that the probability of making *even one* false positive across all $m$ tests is $\\le \\alpha$:
$$\\alpha' = \\frac{\\alpha}{m}$$
- For 20 tests: test each metric at $\\alpha' = 0.05 / 20 = 0.0025$.
- *Criticism:* Extremely conservative; drastically reduces statistical power, causing massive false negatives (Type II error).

**3. Benjamini-Hochberg Procedure (Controls False Discovery Rate - FDR):**
Controls the expected proportion of false positives among all rejected null hypotheses: $\\mathbb{E}[FP / (TP + FP)] \\le q$.
1. Sort $m$ p-values in ascending order: $p_{(1)} \\le p_{(2)} \\dots \\le p_{(m)}$.
2. Find largest index $k$ such that $p_{(k)} \\le \\frac{k}{m} q$.
3. Reject all null hypotheses for $i = 1, \\dots, k$.
Far more powerful than Bonferroni while maintaining rigorous error control.""",
        "tip": "Recommend Benjamini-Hochberg over Bonferroni when testing large product dashboards with dozens of secondary metrics."
    },
    {
        "id": "metrics_111",
        "category": "metrics_data",
        "category_label": "Evaluation Metrics & Preprocessing",
        "difficulty": "Mid / Senior",
        "company_tags": ["Stripe", "Amazon", "Two Sigma"],
        "question": "Explain Covariate Shift, Prior Probability Shift, and Concept Drift using joint probability decomposition $P(X, Y) = P(X) P(Y|X)$.",
        "answer": """Using Bayes' factorization $P(X, Y) = P(X) P(Y|X) = P(Y) P(X|Y)$:

**1. Covariate Shift (Feature Drift):**
- Input distribution $P(X)$ changes: $P_{train}(X) \\neq P_{test}(X)$.
- Conditional mapping $P(Y | X)$ remains **constant**.
- *Example:* Facial recognition model trained on images of young adults is deployed in retirement homes. The physical laws mapping facial wrinkles to identity haven't changed, but the demographic age distribution $P(X)$ shifted.
- *Fix:* Importance weighting $\\frac{P_{test}(X)}{P_{train}(X)}$.

**2. Prior Probability Shift (Label Drift):**
- Target distribution $P(Y)$ changes: $P_{train}(Y) \\neq P_{test}(Y)$.
- Class-conditional distribution $P(X | Y)$ remains constant.
- *Example:* COVID-19 outbreak causes the baseline prevalence of fever ($Y$) to surge from 0.1% to 15%, while symptoms given COVID $P(X|Y)$ remain unchanged.

**3. Concept Drift (Relationship Drift - Most Dangerous):**
- The true underlying relationship $P(Y | X)$ changes: $P_{train}(Y | X) \\neq P_{test}(Y | X)$.
- Feature distribution $P(X)$ can remain identical.
- *Example:* Macroeconomic inflation or interest rate hikes: a credit applicant with a USD 50,000 salary ($X$) could easily afford mortgage repayments in 2020, but defaults ($Y$) in 2024.
- *Fix:* Mandatory model retraining on fresh rolling window data.""",
        "tip": "Write out the joint distributions $P(X, Y)$ explicitly to clearly demonstrate the mathematical distinction."
    },
    {
        "id": "metrics_112",
        "category": "metrics_data",
        "category_label": "Evaluation Metrics & Preprocessing",
        "difficulty": "Senior",
        "company_tags": ["Capital One", "Stripe", "American Express"],
        "question": "What is the Population Stability Index (PSI)? How is it calculated, and what threshold values signal model drift requiring retraining?",
        "answer": """**1. Definition:**
A quantitative metric based on symmetric Kullback-Leibler (KL) divergence that measures how much a feature or model output distribution has shifted between a reference (Baseline / Training) dataset $B$ and a target (Production / Current) dataset $T$.

**2. Calculation Formula:**
1. Bin the continuous variable into $K$ buckets (typically $K=10$ deciles based on baseline percentiles).
2. Compute the fraction of actual observations falling in bucket $i$ for Baseline ($B_i$) and Target ($T_i$).
3. Compute PSI across all $K$ buckets:
   $$\\text{PSI} = \\sum_{i=1}^K (T_i - B_i) \\times \\ln\\left( \\frac{T_i}{B_i} \\right)$$

**3. Industry Standard Thresholds:**
- **$\\text{PSI} < 0.1$:** No significant change. Model distribution is stable.
- **$0.1 \\le \\text{PSI} < 0.2$:** Moderate drift. Model behavior is changing; requires monitoring and investigation.
- **$\\text{PSI} \\ge 0.2$:** Significant distributional drift! The model is making decisions on populations substantially different from training data. **Automated trigger for model retraining.**""",
        "tip": "PSI is the foundational drift metric in financial banking risk governance (Basel / SR 11-7)."
    },
    {
        "id": "metrics_113",
        "category": "metrics_data",
        "category_label": "Evaluation Metrics & Preprocessing",
        "difficulty": "Junior / Mid",
        "company_tags": ["Amazon", "Uber"],
        "question": "What is the difference between Micro-averaged F1, Macro-averaged F1, and Weighted F1 in multi-class classification?",
        "answer": """- **Macro-Averaged F1:**
  Computes the F1-score independently for each class $k$, then takes the unweighted arithmetic mean:
  $$\\text{Macro\\_F1} = \\frac{1}{K} \\sum_{k=1}^K F1_k$$
  - Treats all classes equally regardless of frequency. Gives minority classes equal influence. **Best for detecting poor minority class performance.**
- **Micro-Averaged F1:**
  Aggregates global $TP, FP, FN$ across all classes first, then computes overall F1:
  $$\\text{Micro\\_Precision} = \\frac{\\sum TP_k}{\\sum TP_k + \\sum FP_k}$$
  - For standard single-label multi-class classification, **Micro-F1 is mathematically identical to Accuracy!**
- **Weighted F1:**
  Weights each class's F1-score by its actual prevalence (support) in the dataset:
  $$\\text{Weighted\\_F1} = \\sum_{k=1}^K \\frac{N_k}{N_{total}} F1_k$$
  - Accounts for class imbalance, but can hide terrible performance on tiny minority classes.""",
        "tip": "State clearly that Micro-F1 equals Accuracy in single-label multi-class problems; interviewers frequently verify this."
    },
    {
        "id": "metrics_114",
        "category": "metrics_data",
        "category_label": "Evaluation Metrics & Preprocessing",
        "difficulty": "Mid",
        "company_tags": ["Google", "Spotify"],
        "question": "What is NDCG (Normalized Discounted Cumulative Gain) in Ranking and Recommendation Systems? Derive DCG and IDCG.",
        "answer": """**1. Cumulative Gain (CG):** Sum of relevance scores of top $K$ items: $\\text{CG}_K = \\sum_{i=1}^K rel_i$. (Fails to penalize placing relevant items at the bottom).

**2. Discounted Cumulative Gain (DCG):**
Applies a logarithmic discount penalty for items placed lower down the ranked list:
$$\\text{DCG}_K = \\sum_{i=1}^K \\frac{2^{rel_i} - 1}{\\log_2(i + 1)}$$
where $rel_i$ is the relevance score (e.g. 0 to 4 stars) of the item at position $i$.
- Items placed at position 1 receive full credit ($\\log_2(2) = 1$).
- Items placed at position 10 receive divided credit ($\\log_2(11) = 3.46$).

**3. Ideal DCG (IDCG) and Normalized DCG (NDCG):**
- $\\text{IDCG}_K$: The theoretical maximum DCG achieved by sorting all retrieved items in **perfect descending order of relevance**.
- **NDCG:**
  $$\\text{NDCG}_K = \\frac{\\text{DCG}_K}{\\text{IDCG}_K}$$
Bounds metric strictly between $[0, 1.0]$. An NDCG of 1.0 indicates a flawless ranking order.""",
        "tip": "NDCG is the universal gold standard metric for search engines (Google, Bing) and recommendation feeds (Netflix)."
    },
    {
        "id": "metrics_115",
        "category": "metrics_data",
        "category_label": "Evaluation Metrics & Preprocessing",
        "difficulty": "Senior",
        "company_tags": ["Google", "Meta", "Uber"],
        "question": "What is Calibration in classification models? How do Brier Score and Expected Calibration Error (ECE) measure it, and how does Platt Scaling fix uncalibrated models?",
        "answer": """**1. Concept of Calibration:**
A model is well-calibrated if predicted probabilities reflect true empirical frequencies:
When a model predicts a probability of $0.80$ for 100 patient samples, exactly $80$ of those patients should actually have the disease.
- Modern deep neural networks (unlike classical logistic regression) are notoriously **uncalibrated and overconfident** (Guo et al., 2017) due to weight decay and cross-entropy over-optimization.

**2. Measurement Metrics:**
- **Brier Score:** Mean squared error of probabilities: $\\frac{1}{n} \\sum (\\hat{p}_i - y_i)^2$.
- **Expected Calibration Error (ECE):**
  Groups predictions into $M$ confidence bins (e.g. $[0.7, 0.8]$):
  $$\\text{ECE} = \\sum_{m=1}^M \\frac{|B_m|}{n} |\\text{acc}(B_m) - \\text{conf}(B_m)|$$
  Measures weighted average gap between model accuracy and confidence.

**3. Post-Processing Calibration (Platt Scaling & Temperature Scaling):**
Fits a scalar temperature $T > 0$ on validation logits before softmax:
$$\\hat{p}_i = \\frac{\\exp(z_i / T)}{\\sum \\exp(z_j / T)}$$
- Optimizing $T$ via NLL smooths overconfident predictions without altering logit rank ordering (accuracy is preserved, calibration improves dramatically).""",
        "tip": "Explain that Temperature Scaling is standard practice for medical and self-driving systems where probability calibration is safety-critical."
    }
]
