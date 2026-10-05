"""Category 1: Classical Machine Learning & Statistical Learning (Questions 1-25)"""

CAT1_QUESTIONS = [
    {
        "id": "ml_01",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "difficulty": "Mid / Senior",
        "company_tags": ["Google", "Meta", "Amazon", "Two Sigma"],
        "question": "What is the fundamental mathematical difference between L1 (Lasso) and L2 (Ridge) regularization? Why does L1 regularization drive weights strictly to zero (producing sparse models), while L2 only shrinks weights toward zero?",
        "answer": """**1. Mathematical Formulations:**
- **Ridge (L2):** $\\min_w \\frac{1}{2n} \\|y - Xw\\|_2^2 + \\frac{\\lambda}{2} \\sum_{j=1}^d w_j^2$
- **Lasso (L1):** $\\min_w \\frac{1}{2n} \\|y - Xw\\|_2^2 + \\lambda \\sum_{j=1}^d |w_j|$

**2. Geometric Intuition (The Constraint Surface):**
Under the Lagrangian formulation, optimization is equivalent to minimizing the Residual Sum of Squares (RSS) subject to a budget constraint:
- L2 constraint is a hypersphere $\\sum w_j^2 \\le C$. The smooth elliptical RSS contours typically contact the smooth hypersphere where all coordinates are non-zero.
- L1 constraint is a hyper-rhombus (diamond in 2D, cross-polytope in $d$-D) $\\sum |w_j| \\le C$. It has sharp **corners (vertices)** lying precisely on the coordinate axes (where $w_j = 0$). Expanding elliptical loss contours are geometrically far more likely to intersect a corner first, locking that weight strictly to zero.

**3. Gradient & Subgradient Dynamics:**
- **L2 gradient:** $\\frac{\\partial (\\lambda w^2)}{\\partial w} = 2\\lambda w$. As $w \\to 0$, the penalty force vanishes linearly with $w$. It gently nudges tiny weights but never pushes them to zero.
- **L1 subgradient:** $\\frac{\\partial (\\lambda |w|)}{\\partial w} = \\lambda \\cdot \\text{sign}(w)$ for $w \\neq 0$. The penalty exerts a constant force $\\pm \\lambda$ regardless of how small $w$ is, driving it until it hits $0$, where the subgradient interval is $[-\\lambda, \\lambda]$.

**Summary:** Use L1 for feature selection when features are mostly noise; use L2 when features are collinear and all contribute predictive signal.""",
        "tip": "Interviewers look for subgradients at $w=0$ and the 2D geometric diamond vs circle constraint surfaces."
    },
    {
        "id": "ml_02",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "difficulty": "Mid / Senior",
        "company_tags": ["Microsoft", "Google", "Apple"],
        "question": "Derive the Bias-Variance Decomposition for Mean Squared Error. What do the individual terms represent, and how do model complexity and sample size affect them?",
        "answer": """**Mathematical Derivation:**
Let $y = f(x) + \\epsilon$ with $\\mathbb{E}[\\epsilon] = 0$ and $\\text{Var}(\\epsilon) = \\sigma^2$. Let $\\hat{f}(x)$ be the model trained on dataset $\\mathcal{D}$.
$$\\mathbb{E}\\left[(y - \\hat{f}(x))^2\\right] = \\text{Bias}(\\hat{f}(x))^2 + \\text{Var}(\\hat{f}(x)) + \\sigma^2$$

**Derivation:**
1. $y - \\hat{f} = (f - \\mathbb{E}[\\hat{f}]) + (\\mathbb{E}[\\hat{f}] - \\hat{f}) + \\epsilon$
2. Expanding the square and taking expectations:
   - Term 1: $(f(x) - \\mathbb{E}[\\hat{f}(x)])^2 = \\text{Bias}(\\hat{f}(x))^2$ (Systematic error of simplifying assumptions)
   - Term 2: $\\mathbb{E}\\left[(\\hat{f}(x) - \\mathbb{E}[\\hat{f}(x)])^2\\right] = \\text{Var}(\\hat{f}(x))$ (Sensitivity to training set fluctuations)
   - Term 3: $\\mathbb{E}[\\epsilon^2] = \\sigma^2$ (Irreducible ambient noise)
   - Cross terms vanish due to independence of noise and $\\mathbb{E}[\\hat{f} - \\mathbb{E}[\\hat{f}]] = 0$.

**Dynamics:**
- High Bias (Underfitting): Simple models. Fix: add features, deeper trees, reduce regularization.
- High Variance (Overfitting): Overly complex models. Fix: more data, regularization, bagging.""",
        "tip": "State clearly that irreducible noise $\\sigma^2$ cannot be eliminated by any model regardless of architecture or data size."
    },
    {
        "id": "ml_03",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "difficulty": "Junior / Mid",
        "company_tags": ["Amazon", "Uber", "Meta"],
        "question": "Why does Logistic Regression optimize Log Loss (Binary Cross-Entropy) instead of Mean Squared Error (MSE)? What happens if you use MSE for classification?",
        "answer": """**1. Non-Convex Loss Surface with MSE:**
In logistic regression, $\\hat{y} = \\sigma(z) = \\frac{1}{1 + e^{-w^T x}}$.
With MSE: $L_{MSE} = \\frac{1}{2n}\\sum (y_i - \\sigma(w^T x_i))^2$.
Gradient: $\\frac{\\partial L_{MSE}}{\\partial w} = -(y - \\sigma(z)) \\sigma(z)(1 - \\sigma(z)) x$.
When the prediction is **confidently wrong** ($y=1$ but $z = -10 \\implies \\sigma(z) \\approx 0$), $\\sigma'(z) \\to 0$. Gradients vanish, trapping optimization in flat local plateaus.

**2. Convexity of Log Loss:**
Log Loss is the negative log-likelihood of Bernoulli distribution:
$$L_{CE} = -\\sum [y \\log(\\sigma(z)) + (1-y)\\log(1 - \\sigma(z))]$$
Gradient: $\\frac{\\partial L_{CE}}{\\partial w} = (\\sigma(z) - y) x$.
The $\\sigma'(z)$ cancels out!
- The loss surface is strictly **convex** (guaranteed global optimum).
- When confidently wrong, error $(\\sigma(z) - y) \\to \\pm 1$, providing strong corrective gradients.""",
        "tip": "Highlight that Log Loss is the negative log-likelihood under a Bernoulli likelihood assumption."
    },
    {
        "id": "ml_04",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "difficulty": "Mid",
        "company_tags": ["Google", "Bloomberg", "Goldman Sachs"],
        "question": "How do Decision Trees split continuous numerical features, and what is the difference between Gini Impurity and Information Gain (Entropy)?",
        "answer": """**1. Continuous Feature Splitting:**
1. Sort unique values of feature $X_j$: $v_1 < v_2 < \\dots < v_m$.
2. Compute midpoints as candidate thresholds: $t_k = \\frac{v_k + v_{k+1}}{2}$.
3. For each candidate threshold $t_k$, evaluate impurity reduction for $S_{left} = \\{x: x_j \\le t_k\\}$ and $S_{right} = \\{x: x_j > t_k\\}$.
4. Choose feature $j^*$ and threshold $t^*$ maximizing impurity reduction.

**2. Gini vs Entropy:**
- **Gini Impurity:** $I_G(p) = 1 - \\sum_{k=1}^K p_k^2$. Range: $[0, 0.5]$ (binary). Faster to compute (no logarithms).
- **Entropy:** $H(p) = -\\sum_{k=1}^K p_k \\log_2(p_k)$. Range: $[0, 1.0]$ (binary). Heavily penalizes impure mixtures.
In practice, performance differs by $<2\\%$. CART uses Gini; C4.5/ID3 use Entropy.""",
        "tip": "Mention histogram-based binning (e.g. LightGBM 256 bins) which reduces continuous split search from $O(N \\log N)$ to $O(K)$."
    },
    {
        "id": "ml_05",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "difficulty": "Mid / Senior",
        "company_tags": ["Meta", "ByteDance", "Stripe"],
        "question": "Compare Random Forest and Gradient Boosting (GBDT): What are the core architectural differences in how they construct ensembles and reduce error?",
        "answer": """**Random Forest (Bagging):**
- **Method:** Bootstrap Aggregation + Random Subspace feature sampling.
- **Trees:** Fully grown, deep, independent trees trained in parallel.
- **Error Reduction:** Primarily reduces **variance** via averaging uncorrelated trees: $\\text{Var}(\\bar{X}) = \\rho \\sigma^2 + \\frac{1-\\rho}{B}\\sigma^2$.
- **Overfitting:** Extremely robust as number of trees $B \\to \\infty$.

**Gradient Boosted Decision Trees (Boosting):**
- **Method:** Sequential additive modeling: $F_m(x) = F_{m-1}(x) + \\eta h_m(x)$.
- **Trees:** Shallow trees (depth 3-6) trained sequentially to predict pseudo-residuals (negative gradient of loss function).
- **Error Reduction:** Primarily reduces **bias** by learning what prior trees missed.
- **Overfitting:** Can overfit if tree count $M$ is too large without early stopping or shrinkage $\\eta$.""",
        "tip": "Emphasize parallelization: Random Forest trees train concurrently, while GBDT is fundamentally sequential."
    },
    {
        "id": "ml_06",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "difficulty": "Senior / Staff",
        "company_tags": ["Jane Street", "Citadel", "Two Sigma", "DoorDash"],
        "question": "How does XGBoost use second-order Taylor expansion to derive optimal leaf weights and split scoring? How does it handle missing values natively?",
        "answer": """**1. Second-Order Taylor Expansion:**
At step $t$, expand objective around $\\hat{y}^{(t-1)}$:
$$\\mathcal{L}^{(t)} \\approx \\sum_{i=1}^n \\left[ g_i f_t(x_i) + \\frac{1}{2} h_i f_t^2(x_i) \\right] + \\gamma T + \\frac{1}{2}\\lambda \\sum_{j=1}^T w_j^2$$
where $g_i = \\partial_{\\hat{y}^{(t-1)}} l(y_i, \\hat{y}^{(t-1)})$ and $h_i = \\partial^2_{\\hat{y}^{(t-1)}} l(y_i, \\hat{y}^{(t-1)})$.

**2. Optimal Leaf Weight & Split Score:**
Differentiating with respect to leaf weight $w_j$:
$$w_j^* = -\\frac{\\sum_{i \\in I_j} g_i}{\\sum_{i \\in I_j} h_i + \\lambda} = -\\frac{G_j}{H_j + \\lambda}$$
Split gain for Left ($L$) and Right ($R$) children:
$$\\text{Gain} = \\frac{1}{2} \\left[ \\frac{G_L^2}{H_L + \\lambda} + \\frac{G_R^2}{H_R + \\lambda} - \\frac{(G_L + G_R)^2}{H_L + H_R + \\lambda} \\right] - \\gamma$$

**3. Native Missing Value Handling:**
During split evaluation, missing samples are sent to Left, gain is evaluated; then sent to Right, gain is evaluated. The direction yielding highest gain is saved as the default path.""",
        "tip": "Explain that $\\lambda$ acts as an L2 regularizer on leaf weights, preventing extreme predictions when hessian sum $H_j$ is small."
    },
    {
        "id": "ml_07",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "difficulty": "Junior / Mid",
        "company_tags": ["Apple", "Amazon", "Capital One"],
        "question": "Why is feature scaling mandatory for KNN, SVM, and L2-regularized Logistic Regression, but completely irrelevant for Decision Trees and Random Forests?",
        "answer": """**1. Distance & Optimization Models (Require Scaling):**
- **KNN:** Computes Euclidean distance $d(u, v) = \\sqrt{\\sum (u_i - v_i)^2}$. Large-scale features ($[0, 10^6]$) dominate small-scale features ($[0, 1]$).
- **SVM:** Maximizes margin $\\frac{2}{\\|w\\|_2}$. Unscaled features distort margin orientation.
- **Regularized Models (Ridge/Lasso):** Penalty $\\lambda \\sum w_j^2$ penalizes all weights equally. Unscaled large features need tiny weights and escape penalization.
- **Gradient Descent:** Creates elongated contours, causing oscillations and slow convergence.

**2. Tree Models (Scale Invariant):**
- Decision trees split via monotonic threshold comparisons: $x_j \\le t$.
- Any monotonic transformation (multiplying by $10^6$, $\\log(x)$) preserves exact sample rank ordering. Thresholds simply rescale without altering impurity reduction.""",
        "tip": "State clearly that decision trees are invariant to any strictly monotonic feature transformation."
    },
    {
        "id": "ml_08",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "difficulty": "Mid / Senior",
        "company_tags": ["Google", "NVIDIA", "Meta"],
        "question": "What is the Kernel Trick in Support Vector Machines? Explain how it allows learning non-linear decision boundaries without computing explicit high-dimensional feature coordinates.",
        "answer": """**1. Dual Formulation of SVM:**
The optimization depends solely on pairwise inner products: $\\langle x_i, x_j \\rangle$.

**2. The Kernel Trick:**
To learn non-linear boundaries, we map inputs to a high-dimensional Hilbert space $\\mathcal{H}$ via $\\phi(x)$.
Instead of computing $\\phi(x)$ explicitly, a **Kernel function** computes the inner product directly:
$$K(x_i, x_j) = \\langle \\phi(x_i), \\phi(x_j) \\rangle$$

**3. RBF (Gaussian) Kernel:**
$$K(x, z) = \\exp(-\\gamma \\|x - z\\|^2)$$
Expanding the exponential via Taylor series shows that the RBF kernel implicitly maps inputs into an **infinite-dimensional** space, allowing non-linear boundaries with $O(d)$ compute per pair.""",
        "tip": "Cite Mercer's Theorem: Any symmetric, positive semi-definite kernel corresponds to an inner product in an RKHS."
    },
    {
        "id": "ml_09",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "difficulty": "Senior",
        "company_tags": ["Citadel", "Google Research", "OpenAI"],
        "question": "Explain the Curse of Dimensionality. Prove mathematically why Euclidean distance becomes ineffective as dimension $d \\to \\infty$.",
        "answer": """**1. Geometric Paradox:**
As dimension $d \\to \\infty$:
- Inscribed hypersphere volume relative to bounding hypercube approaches 0: $\\lim_{d \\to \\infty} \\frac{V_{sphere}}{V_{cube}} = 0$.
- Shell volume between radius $1-\\epsilon$ and $1$ approaches 1: $1 - (1-\\epsilon)^d \\to 1$. Almost all points lie on the extreme outer corners.

**2. Distance Concentration Phenomenon (Beyer et al., 1999):**
Under independent features:
$$\\lim_{d \\to \\infty} \\frac{D_{\\max} - D_{\\min}}{D_{\\min}} = 0$$
All points become equidistant from the query point. Distance-based algorithms (KNN, K-Means) lose discriminative contrast.""",
        "tip": "Explain that this is why high-dimensional embeddings rely on Cosine Similarity and dimensionality reduction (PCA, UMAP)."
    },
    {
        "id": "ml_10",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "difficulty": "Junior / Mid",
        "company_tags": ["Amazon", "Uber", "Spotify"],
        "question": "Why is K-Means clustering guaranteed to converge? Can it find the global optimum? How does K-Means++ initialization solve poor local optima?",
        "answer": """**1. Convergence (Coordinate Descent):**
Minimizes inertia: $J = \\sum_{k=1}^K \\sum_{i \\in C_k} \\|x_i - \\mu_k\\|^2$.
- Step 1 (Assignment): Assigning to nearest centroid decreases $J$ holding $\\mu$ fixed.
- Step 2 (Update): Recomputing centroid as cluster mean minimizes $J$ holding assignments fixed.
Since $J \\ge 0$ and the number of partitions ($K^N$) is finite, $J$ must monotonically decrease to a local minimum.

**2. K-Means++ Initialization:**
1. Pick first centroid $\\mu_1$ uniformly at random.
2. Select next centroid with probability proportional to squared distance to nearest existing centroid: $P(x) = \\frac{D(x)^2}{\\sum D(x')^2}$.
Guarantees an $O(\\log K)$ approximation ratio relative to the global optimum.""",
        "tip": "Highlight that K-Means assumes spherical, isotropic clusters with equal variance."
    },
    {
        "id": "ml_11",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "difficulty": "Mid / Senior",
        "company_tags": ["Goldman Sachs", "Google", "Two Sigma"],
        "question": "Derive Principal Component Analysis (PCA) mathematically. Why must data be centered ($mean=0$) before computing PCA?",
        "answer": """**1. Mathematical Derivation:**
Let $X$ be centered ($n \\times d$). We seek unit vector $u_1$ maximizing variance:
$$\\text{Var}(X u_1) = \\frac{1}{n} u_1^T X^T X u_1 = u_1^T \\Sigma u_1$$
Lagrangian with constraint $u_1^T u_1 = 1$:
$$\\mathcal{L}(u_1, \\lambda) = u_1^T \\Sigma u_1 - \\lambda(u_1^T u_1 - 1)$$
Derivative: $\\frac{\\partial \\mathcal{L}}{\\partial u_1} = 2\\Sigma u_1 - 2\\lambda u_1 = 0 \\implies \\Sigma u_1 = \\lambda u_1$.
The first principal component is the eigenvector of covariance matrix $\\Sigma$ corresponding to the largest eigenvalue $\\lambda_1$.

**2. Why Centering is Mandatory:**
Without centering, $\\frac{1}{n} X^T X$ computes the second raw moment rather than covariance. The first component will point toward the mean vector $\\mu$ rather than the direction of maximal internal spread.""",
        "tip": "Mention that in practice, PCA uses SVD ($X = U \\Sigma V^T$) rather than explicitly forming $X^T X$, for numerical stability."
    },
    {
        "id": "ml_12",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "difficulty": "Mid / Senior",
        "company_tags": ["Meta", "Apple", "Twitter/X"],
        "question": "What is the difference between Generative and Discriminative models? Use Naive Bayes and Logistic Regression as contrasting examples.",
        "answer": """**1. Definitions:**
- **Discriminative:** Models $P(Y | X)$ directly. Focuses solely on finding optimal decision boundaries. (Logistic Regression, SVM, Trees).
- **Generative:** Models joint distribution $P(X, Y) = P(X|Y)P(Y)$. Models how data is produced for each class. (Naive Bayes, GMM, Diffusion).

**2. Naive Bayes vs Logistic Regression:**
Both yield linear decision boundaries in log-odds.
- **Naive Bayes:** Assumes feature independence $P(X|Y) = \\prod P(x_j|Y)$. Converges with fewer samples ($O(\\log d)$), but higher asymptotic error if features correlate.
- **Logistic Regression:** Fits weights jointly via MLE. Requires more samples ($O(d)$), but achieves lower asymptotic error when features correlate.""",
        "tip": "Cite Ng & Jordan (2001) paper 'On Discriminative vs. Generative classifiers'."
    },
    {
        "id": "ml_13",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "difficulty": "Senior",
        "company_tags": ["Two Sigma", "AQR", "Citadel"],
        "question": "What happens in Linear Regression when features are highly multicollinear? How do you diagnose it, and what are 3 ways to solve it?",
        "answer": """**1. Consequences:**
In OLS $\\hat{w} = (X^T X)^{-1} X^T y$:
- $X^T X$ is near-singular (determinant $\\approx 0$).
- Condition number $\\kappa(X^T X) \\gg 1000$.
- Variance of coefficients explodes: $\\text{Var}(\\hat{w}_j) = \\frac{\\sigma^2}{(n-1)s_j^2} \\frac{1}{1 - R_j^2}$. Coefficients become wildly unstable.

**2. Diagnosis:**
- Variance Inflation Factor: $\\text{VIF}_j = \\frac{1}{1 - R_j^2} > 5-10$.
- Correlation matrix heatmap ($|r| > 0.85$).

**3. Remediation:**
1. Ridge Regression (adds $\\lambda I$ to $X^T X$, restoring invertibility).
2. Remove redundant features.
3. Principal Component Regression (PCR).""",
        "tip": "Note that multicollinearity does NOT harm overall prediction $R^2$; it destroys individual coefficient interpretability."
    },
    {
        "id": "ml_14",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "difficulty": "Mid",
        "company_tags": ["Google", "Meta"],
        "question": "What is the difference between Parametric and Non-Parametric Machine Learning models? Provide examples of each and explain their sample complexity trade-offs.",
        "answer": """**1. Parametric:**
- Fixed number of parameters independent of dataset size $N$.
- Examples: Linear Regression, Logistic Regression, Naive Bayes.
- Fast training/inference, interpretable; but limited capacity (high bias).

**2. Non-Parametric:**
- Parameter count grows with training sample size $N$. Does not assume a fixed functional form.
- Examples: KNN, Decision Trees, SVM (RBF kernel), Gaussian Processes.
- Highly flexible, models complex manifolds; but slower inference and requires regularization to avoid overfitting.""",
        "tip": "Emphasize that 'non-parametric' means parameters are not fixed a priori, not that there are zero parameters."
    },
    {
        "id": "ml_15",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "difficulty": "Senior",
        "company_tags": ["DeepMind", "Jane Street", "Apple"],
        "question": "How does the Expectation-Maximization (EM) algorithm work for Gaussian Mixture Models (GMM)? How is it related to K-Means?",
        "answer": """**1. Formulation:**
$p(x) = \\sum_{k=1}^K \\pi_k \\mathcal{N}(x | \\mu_k, \\Sigma_k)$.

**2. EM Steps:**
- **E-Step:** Compute soft responsibility $\\gamma_{ik} = \\frac{\\pi_k \\mathcal{N}(x_i | \\mu_k, \\Sigma_k)}{\\sum_j \\pi_j \\mathcal{N}(x_i | \\mu_j, \\Sigma_j)}$.
- **M-Step:** Update $\\mu_k = \\frac{\\sum \\gamma_{ik} x_i}{\\sum \\gamma_{ik}}$, $\\Sigma_k$, and $\\pi_k$.

**3. Connection to K-Means:**
K-Means is a degenerate GMM with isotropic spherical covariance $\\Sigma_k = \\sigma^2 I$. As $\\sigma^2 \\to 0$, soft responsibilities collapse into hard binary 0/1 assignments.""",
        "tip": "Explain that GMM handles non-spherical elliptical clusters with varying variance orientations."
    },
    {
        "id": "ml_16",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "difficulty": "Senior",
        "company_tags": ["OpenAI", "Meta", "Google"],
        "question": "Why can Early Stopping in gradient descent optimization be mathematically viewed as a form of L2 Regularization (Weight Decay)?",
        "answer": """**Bishop PRML Derivation:**
For quadratic error with Hessian eigenvalues $\\lambda_j$:
- After $\\tau$ gradient descent iterations: $w(\\tau) = \\sum [1 - (1 - \\eta \\lambda_j)^\\tau] (w^* \\cdot v_j) v_j$.
- With L2 weight decay $\\alpha$: $w_{L2} = \\sum \\left[ \\frac{\\lambda_j}{\\lambda_j + \\alpha} \\right] (w^* \\cdot v_j) v_j$.
Equating shrinkage factors: $1 - (1 - \\eta \\lambda_j)^\\tau \\approx \\frac{\\lambda_j}{\\lambda_j + \\frac{1}{\\tau \\eta}}$.
**Conclusion:** Stopping at iteration $\\tau$ is mathematically equivalent to L2 regularization with $\\alpha \\approx \\frac{1}{\\tau \\eta}$.""",
        "tip": "This shows deep mastery of optimization trajectories and spectral regularization."
    },
    {
        "id": "ml_17",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "difficulty": "Mid",
        "company_tags": ["Kaggle", "ByteDance", "Airbnb"],
        "question": "What is Target Encoding, why does naive Target Encoding cause catastrophic data leakage, and how do Out-of-Fold (OOF) and additive smoothing fix it?",
        "answer": """**1. Target Encoding:**
Replaces category $c$ with expected target: $\\hat{x}_c = \\mathbb{E}[y | x=c]$.

**2. Leakage Problem:**
If category $c$ appears once with $y=1$, encoding is $1.0$. A tree splits on $1.0$, memorizing the training target perfectly. Fails on test data.

**3. Fixes:**
- **Additive Smoothing:** $S_c = \\frac{n_c \\bar{y}_c + m \\bar{y}}{n_c + m}$. Shrinks small categories toward global target mean.
- **Out-of-Fold (OOF):** Encode each fold using only target statistics from other $K-1$ folds.
- **Ordered Target Encoding (CatBoost):** Computes statistics only from past samples in a random permutation.""",
        "tip": "CatBoost's ordered target encoding was a key factor in its tabular benchmark dominance."
    },
    {
        "id": "ml_18",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "difficulty": "Junior / Mid",
        "company_tags": ["Amazon", "Uber", "Palantir"],
        "question": "Explain the difference between Bagging, Boosting, and Stacking ensemble methods.",
        "answer": """**1. Bagging:** Trains homogeneous models in parallel on bootstrap samples. Aggregates via averaging/voting. Reduces **variance**. (Random Forest).
**2. Boosting:** Trains homogeneous models sequentially, each fitting pseudo-residuals of prior models. Reduces **bias**. (XGBoost, LightGBM).
**3. Stacking:** Trains heterogeneous models (trees, linear models, neural nets) in parallel. A meta-learner is trained on their out-of-fold predictions to make final predictions. Maximizes architectural diversity.""",
        "tip": "In Stacking, out-of-fold predictions MUST be used to train the meta-learner to avoid data leakage."
    },
    {
        "id": "ml_19",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "difficulty": "Mid / Senior",
        "company_tags": ["Two Sigma", "Citadel", "Millennium"],
        "question": "Why can't Linear Regression be solved using the Ordinary Least Squares formula $\\hat{w} = (X^T X)^{-1} X^T y$ when the number of features $d$ exceeds the number of samples $n$ ($d > n$)?",
        "answer": """**Linear Algebra Proof:**
- $X \\in \\mathbb{R}^{n \\times d} \\implies X^T X \\in \\mathbb{R}^{d \\times d}$.
- $\\text{rank}(X^T X) = \\text{rank}(X) \\le \\min(n, d) = n < d$.
- Because rank is strictly less than dimension $d$, $X^T X$ is **rank-deficient** and non-invertible (determinant is 0).
- The system is underdetermined with infinitely many interpolating solutions.
- Solved via Ridge Regularization $(X^T X + \\lambda I)^{-1} X^T y$ or Lasso.""",
        "tip": "Mention the Moore-Penrose pseudoinverse $X^+$ as the minimal $L_2$-norm solution."
    },
    {
        "id": "ml_20",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "difficulty": "Senior",
        "company_tags": ["Stripe", "Goldman Sachs"],
        "question": "What is Heteroskedasticity in regression analysis? How do you detect it in residual plots, and what are its statistical consequences?",
        "answer": """**1. Definition:**
Non-constant residual variance: $\\text{Var}(\\epsilon_i | x_i) = \\sigma_i^2$.

**2. Detection:**
Residual vs fitted plot shows a **funnel (cone) shape** expanding outwards. Formal tests: Breusch-Pagan, White's test.

**3. Consequences:**
OLS coefficients $\\hat{w}$ remain **unbiased**, but standard errors are invalid. Hypothesis tests (p-values, confidence intervals) are unreliable.

**4. Fix:**
Log transform $y$, use Huber-White robust standard errors, or Weighted Least Squares (WLS).""",
        "tip": "Emphasize that coefficients remain unbiased; only the standard errors become invalid."
    },
    {
        "id": "ml_21",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "difficulty": "Mid / Senior",
        "company_tags": ["Google", "Meta", "Netflix"],
        "question": "What is Simpson's Paradox? Provide a concrete machine learning / statistical example where an aggregated trend is reversed in subgroups.",
        "answer": """**1. Definition:**
A statistical phenomenon where a trend observed across multiple groups vanishes or reverses when groups are aggregated, caused by an unobserved **confounding variable**.

**2. Example:**
Ad CTR: Ad A beats Ad B on Mobile (10% vs 8%) and on Desktop (20% vs 18%).
However, Ad A ran mostly on Mobile (low CTR platform), while Ad B ran mostly on Desktop (high CTR platform). In aggregate, Ad B appears to have a higher total CTR!

**3. ML Implication:**
Failing to condition on the confounder causes models to learn spurious correlations and inverted causal effects.""",
        "tip": "Mention Pearl's causal DAGs and do-calculus as the mathematical framework to resolve confounding."
    },
    {
        "id": "ml_22",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "difficulty": "Senior / Staff",
        "company_tags": ["DeepMind", "Jane Street"],
        "question": "What is the difference between a convex and non-convex optimization problem? Why is convexity so prized in classical ML, and why do we accept non-convexity in Deep Learning?",
        "answer": """**1. Convex Optimization:**
Every local minimum is a global minimum. Guaranteed polynomial-time convergence. (OLS, Logistic Regression, SVM).

**2. Non-Convex Optimization:**
Loss surfaces contain saddle points, ravines, and countless local minima.
- In Deep Learning, non-linear activation composition creates non-convex surfaces, but grants Universal Approximation capability.
- In high dimensions, true local minima are rare; almost all critical points are saddle points with escape directions. Overparameterization ensures most local minima achieve near-global loss.""",
        "tip": "Cite Dauphin et al. (2014) regarding saddle points vs local minima in deep learning."
    },
    {
        "id": "ml_23",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "difficulty": "Mid / Senior",
        "company_tags": ["Microsoft", "Google"],
        "question": "What is the inductive bias of an ML model? Compare the inductive biases of Linear Models, Decision Trees, CNNs, and Transformers.",
        "answer": """**Inductive Bias:** Set of prior assumptions a model uses to generalize on unseen inputs.
- **Linear Models:** Assumes additive linear relationship.
- **Trees:** Assumes orthogonal, axis-aligned recursive partitioning.
- **CNNs:** Strong inductive bias: spatial locality (nearby pixels correlate) and translation equivariance (edges look the same anywhere).
- **Transformers:** Very weak inductive bias. All-to-all attention allows learning arbitrary relational graphs, but requires massive pre-training data.""",
        "tip": "Weak inductive bias yields higher capacity, but requires orders of magnitude more training data."
    },
    {
        "id": "ml_24",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "difficulty": "Mid",
        "company_tags": ["Amazon", "Uber", "Doordash"],
        "question": "Why does K-Nearest Neighbors (KNN) degrade severely in inference speed when dataset size $N$ is large, and how do KD-Trees and Ball Trees accelerate queries?",
        "answer": """**1. Brute-Force KNN:**
Computes distance to all $N$ points: $O(N \\cdot d)$. Unusable for millions of records.

**2. KD-Trees:**
Recursively splits space along axis-aligned hyperplanes. Average query $O(d \\log N)$. Degenerates to $O(N)$ when $d > 20$.

**3. Ball Trees:**
Partitions data into nested hyperspheres using the triangle inequality to prune distant branches. Far more robust in higher dimensions.""",
        "tip": "For high-dimensional embeddings ($d=1536$), exact tree search fails; systems use ANN graph indices (HNSW)."
    },
    {
        "id": "ml_25",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "difficulty": "Junior / Mid",
        "company_tags": ["Meta", "Apple", "Capital One"],
        "question": "What is the difference between hard-margin and soft-margin SVM? What is the role of the hyperparameter $C$?",
        "answer": """**1. Hard-Margin:** Requires perfect linear separability ($y_i(w^T x_i + b) \\ge 1$). Fails on overlapping data and sensitive to noise.
**2. Soft-Margin:** Introduces slack variables $\\xi_i \\ge 0$:
$$\\min \\frac{1}{2}\\|w\\|^2 + C \\sum \\xi_i \\quad \\text{s.t.} \\quad y_i(w^T x_i + b) \\ge 1 - \\xi_i$$
**3. Role of $C$:**
- Large $C$: Heavily penalizes slack violations. Produces narrow margins, fitting training points strictly (overfitting risk).
- Small $C$: Tolerates margin violations for a wider, more generalizable margin (underfitting risk).""",
        "tip": "Remember $C$ is inverse to regularization: large $C$ corresponds to small $\\lambda$."
    }
]
