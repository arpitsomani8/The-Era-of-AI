"""
Generator script to compile 150 In-Depth AI/ML/DL/LLM/System Design/Quant Interview Questions & Answers.
Outputs:
  - interview_questions_data.py
"""

import json
import os

# Let's craft the 150 questions structured across the 7 categories.
# We will write the full generator to ensure complete, rigorous content.

QUESTIONS = [
    # =========================================================================
    # CATEGORY 1: Classical Machine Learning & Statistical Foundations (1-25)
    # =========================================================================
    {
        "id": "ml_01",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "difficulty": "Mid / Senior",
        "company_tags": ["Google", "Meta", "Amazon", "Two Sigma"],
        "question": "What is the fundamental mathematical difference between L1 (Lasso) and L2 (Ridge) regularization? Why does L1 regularization drive weights strictly to zero (producing sparse models), while L2 only shrinks weights toward zero?",
        "answer": """**1. Mathematical Objective Functions:**
- **Ridge (L2):** $\\min_w \\frac{1}{2n} \\|y - Xw\\|_2^2 + \\frac{\\lambda}{2} \\sum_{j=1}^d w_j^2$
- **Lasso (L1):** $\\min_w \\frac{1}{2n} \\|y - Xw\\|_2^2 + \\lambda \\sum_{j=1}^d |w_j|$

**2. Geometric Intuition (The Constraint Surface):**
When formulated as constrained optimization via Lagrange multipliers:
- L2 constraint is a hypersphere $\\sum w_j^2 \\le C$. The smooth, circular loss contours of the RSS typically touch the smooth L2 ball along the curved edges, where none of the coordinates are zero.
- L1 constraint is a hyper-rhombus (diamond in 2D, cross-polytope in $d$-D) $\\sum |w_j| \\le C$. It possesses sharp **corners (vertices)** that lie precisely on the coordinate axes (where one or more $w_j = 0$). Elliptical RSS contours expanding outwards are geometrically far more likely to intersect a sharp corner first, locking that weight strictly to zero.

**3. Gradient & Subgradient Dynamics:**
- **L2 gradient:** $\\frac{\\partial (\\lambda w^2)}{\\partial w} = 2\\lambda w$. As $w \\to 0$, the penalty force vanishes linearly with $w$. It gently nudges tiny weights but never pushes them across zero.
- **L1 subgradient:** $\\frac{\\partial (\\lambda |w|)}{\\partial w} = \\lambda \\cdot \\text{sign}(w)$ for $w \\neq 0$. The penalty exerts a constant force $\\pm \\lambda$ regardless of how small $w$ is, driving it relentlessly until it hits $0$, where the subgradient interval is $[-\\lambda, \\lambda]$.

**Key Takeaway:** Use L1 when feature selection is required and features are suspected to be mostly noise; use L2 when features are collinear and all contribute predictive signal.""",
        "tip": "Interviewers love when you mention subgradients at $w=0$ and sketch the 2D geometric diamond vs circle constraint surfaces."
    },
    {
        "id": "ml_02",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "difficulty": "Mid / Senior",
        "company_tags": ["Microsoft", "Google", "Apple"],
        "question": "Derive the Bias-Variance Decomposition for Mean Squared Error. What do the individual terms represent, and how do model complexity and sample size affect them?",
        "answer": """**Mathematical Derivation:**
Let true data generation be $y = f(x) + \\epsilon$, where $\\mathbb{E}[\\epsilon] = 0$ and $\\text{Var}(\\epsilon) = \\sigma^2$ (irreducible noise).
Let $\\hat{f}(x)$ be the model trained on dataset $\\mathcal{D}$. The expected prediction error at test point $x$ across random datasets $\\mathcal{D}$ is:
$$\\mathbb{E}\\left[(y - \\hat{f}(x))^2\\right] = \\text{Bias}(\\hat{f}(x))^2 + \\text{Var}(\\hat{f}(x)) + \\sigma^2$$

**Derivation Steps:**
1. Expand error: $y - \\hat{f} = (f - \\mathbb{E}[\\hat{f}]) + (\\mathbb{E}[\\hat{f}] - \\hat{f}) + \\epsilon$
2. Square and take expectations:
   - Term 1: $(f(x) - \\mathbb{E}[\\hat{f}(x)])^2 = \\text{Bias}(\\hat{f}(x))^2$ (Systematic error of simplifying assumptions)
   - Term 2: $\\mathbb{E}\\left[(\\hat{f}(x) - \\mathbb{E}[\\hat{f}(x)])^2\\right] = \\text{Var}(\\hat{f}(x))$ (Sensitivity to fluctuations in the training set)
   - Term 3: $\\mathbb{E}[\\epsilon^2] = \\sigma^2$ (Irreducible ambient noise)
   - Cross terms vanish because $\\epsilon$ is independent of $\\mathcal{D}$ and $\\mathbb{E}[\\hat{f} - \\mathbb{E}[\\hat{f}]] = 0$.

**Dynamics:**
- **High Bias (Underfitting):** Simple models (linear regression on non-linear data). Fix: Add polynomial features, deeper trees, reduce regularization.
- **High Variance (Overfitting):** Complex models (unpruned decision trees, deep nets with few samples). Fix: Collect more data, apply L1/L2 regularization, dropout, bagging.""",
        "tip": "State clearly that irreducible noise $\\sigma^2$ cannot be eliminated by any machine learning model regardless of architecture or data size."
    },
    {
        "id": "ml_03",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "difficulty": "Junior / Mid",
        "company_tags": ["Amazon", "Uber", "Meta"],
        "question": "Why does Logistic Regression optimize Log Loss (Binary Cross-Entropy) instead of Mean Squared Error (MSE)? What happens if you use MSE for classification?",
        "answer": """**1. Non-Convex Loss Surface with MSE:**
In logistic regression, the prediction is non-linear: $\\hat{y} = \\sigma(z) = \\frac{1}{1 + e^{-w^T x}}$.
If you plug this into MSE:
$$L_{MSE}(w) = \\frac{1}{2n} \\sum_{i=1}^n (y_i - \\sigma(w^T x_i))^2$$
The gradient with respect to $w$ is:
$$\\frac{\\partial L_{MSE}}{\\partial w} = -(y - \\sigma(z)) \\cdot \\sigma'(z) \\cdot x = -(y - \\sigma(z)) \\cdot \\sigma(z)(1 - \\sigma(z)) \\cdot x$$
Because of the $\\sigma(z)(1 - \\sigma(z))$ term, when a prediction is **confidently wrong** (e.g., $y=1$ but $z = -10 \\implies \\sigma(z) \\approx 0$), $\\sigma'(z) \\to 0$. The gradient vanishes! The optimization gets trapped in flat local plateaus.

**2. Convexity and Maximum Likelihood of Log Loss:**
Log Loss is derived directly from the Maximum Likelihood Estimation (MLE) of the Bernoulli distribution:
$$L_{CE}(w) = -\\sum [y \\log(\\sigma(z)) + (1-y)\\log(1 - \\sigma(z))]$$
Taking the derivative with respect to $w$:
$$\\frac{\\partial L_{CE}}{\\partial w} = (\\sigma(z) - y) \\cdot x$$
The $\\sigma'(z)$ term is canceled out by the derivative of $\\log(\\sigma(z))$.
- The loss surface is strictly **convex**, guaranteeing that gradient descent converges to the unique global optimum.
- If the model is confidently wrong, the error $(\\sigma(z) - y) \\to \\pm 1$, producing a strong gradient that quickly corrects the parameters.""",
        "tip": "Highlight that Log Loss is the negative log-likelihood under a Bernoulli likelihood assumption, making it the statistically optimal loss."
    },
    {
        "id": "ml_04",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "difficulty": "Mid",
        "company_tags": ["Google", "Bloomberg", "Goldman Sachs"],
        "question": "How do Decision Trees split continuous numerical features, and what is the difference between Gini Impurity and Information Gain (Entropy)?",
        "answer": """**1. Splitting Continuous Features:**
1. Sort the unique values of feature $X_j$: $v_1 < v_2 < \\dots < v_m$.
2. Compute candidate split thresholds as midpoints: $t_k = \\frac{v_k + v_{k+1}}{2}$.
3. For each candidate threshold $t_k$, evaluate the split quality (Gini gain or Information Gain) of partitioning samples into $S_{left} = \\{x: x_j \\le t_k\\}$ and $S_{right} = \\{x: x_j > t_k\\}$.
4. Choose the feature $j^*$ and threshold $t^*$ that maximizes impurity reduction.

**2. Gini Impurity vs Entropy:**
- **Gini Impurity:** $I_G(p) = 1 - \\sum_{k=1}^K p_k^2 = \\sum_{k=1}^K p_k(1 - p_k)$
  - Measures the probability of misclassifying a randomly chosen element if it were randomly labeled according to the class distribution.
  - Range for binary classification: $[0, 0.5]$.
- **Entropy:** $H(p) = -\\sum_{k=1}^K p_k \\log_2(p_k)$
  - Originates from Information Theory; measures the average information/surprise in bits.
  - Range for binary classification: $[0, 1.0]$.

**Differences & Trade-offs:**
- Gini is computationally faster because it does not require computing logarithms.
- Entropy penalizes mixed probabilities slightly more heavily. In practice, tree performance differs by less than 2% between them. CART uses Gini; C4.5/ID3 use Entropy.""",
        "tip": "Mention that sorting $N$ samples takes $O(N \\log N)$, but histogram-based tree algorithms (like LightGBM) bin continuous values into 256 discrete bins to reduce split finding to $O(K)$."
    },
    {
        "id": "ml_05",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "difficulty": "Mid / Senior",
        "company_tags": ["Meta", "ByteDance", "Stripe"],
        "question": "Compare Random Forest and Gradient Boosting (GBDT): What are the core architectural differences in how they construct ensembles and reduce error?",
        "answer": """**Random Forest (Bagging):**
- **Principle:** Bootstrap Aggregation + Random Subspace Method.
- **Tree Construction:** Independent, parallel trees grown deep (low bias, high variance).
- **Error Reduction:** Primarily reduces **variance** without increasing bias:
  $$\\text{Var}(\\bar{X}) = \\rho \\sigma^2 + \\frac{1 - \\rho}{B} \\sigma^2$$
  Feature subsampling reduces pairwise tree correlation $\\rho$, driving ensemble variance down.
- **Overfitting:** Resistant to overfitting as number of trees $B \\to \\infty$.

**Gradient Boosted Decision Trees (Boosting):**
- **Principle:** Sequential additive modeling: $F_m(x) = F_{m-1}(x) + \\eta \\cdot h_m(x)$.
- **Tree Construction:** Shallow trees (stumps or max_depth 3-6) trained sequentially to predict the pseudo-residuals (negative gradient of loss function) of the previous ensemble:
  $$r_{im} = -\\left[\\frac{\\partial L(y_i, F(x_i))}{\\partial F(x_i)}\\right]_{F=F_{m-1}}$$
- **Error Reduction:** Primarily reduces **bias** by learning what previous trees got wrong, while keeping variance low via small learning rate $\\eta$ and shallow depth.
- **Overfitting:** Can easily overfit if number of trees $M$ is too large without early stopping or shrinkage $\\eta$.""",
        "tip": "Explain that Random Forest trees are completely independent and can be trained in parallel across CPU cores, whereas GBDT trees must be trained sequentially."
    },
    {
        "id": "ml_06",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "difficulty": "Senior / Staff",
        "company_tags": ["Jane Street", "Citadel", "Two Sigma", "DoorDash"],
        "question": "How does XGBoost use second-order Taylor expansion to derive optimal leaf weights and split scoring? How does it handle missing values natively?",
        "answer": """**1. Second-Order Taylor Expansion:**
At step $t$, the objective to minimize is:
$$\\mathcal{L}^{(t)} = \\sum_{i=1}^n l(y_i, \\hat{y}_i^{(t-1)} + f_t(x_i)) + \\Omega(f_t)$$
where $\\Omega(f) = \\gamma T + \\frac{1}{2}\\lambda \\sum_{j=1}^T w_j^2$.
Expanding $l$ with a second-order Taylor series around $\\hat{y}^{(t-1)}$:
$$\\mathcal{L}^{(t)} \\approx \\sum_{i=1}^n \\left[ l(y_i, \\hat{y}_i^{(t-1)}) + g_i f_t(x_i) + \\frac{1}{2} h_i f_t^2(x_i) \\right] + \\gamma T + \\frac{1}{2}\\lambda \\sum_{j=1}^T w_j^2$$
where $g_i = \\partial_{\\hat{y}^{(t-1)}} l(y_i, \\hat{y}^{(t-1)})$ (gradient) and $h_i = \\partial^2_{\\hat{y}^{(t-1)}} l(y_i, \\hat{y}^{(t-1)})$ (hessian).

Let $I_j = \\{i : q(x_i) = j\\}$ be the sample indices assigned to leaf $j$. Grouping by leaf:
$$\\tilde{\\mathcal{L}}^{(t)} = \\sum_{j=1}^T \\left[ \\left(\\sum_{i \\in I_j} g_i\\right) w_j + \\frac{1}{2}\\left(\\sum_{i \\in I_j} h_i + \\lambda\\right) w_j^2 \\right] + \\gamma T$$

**2. Optimal Leaf Weight & Split Score:**
Differentiating with respect to $w_j$ and setting to 0:
$$w_j^* = -\\frac{\\sum_{i \\in I_j} g_i}{\\sum_{i \\in I_j} h_i + \\lambda} = -\\frac{G_j}{H_j + \\lambda}$$
Substituting $w_j^*$ back gives the optimal leaf quality:
$$J(q) = -\\frac{1}{2} \\sum_{j=1}^T \\frac{G_j^2}{H_j + \\lambda} + \\gamma T$$
The gain from splitting a node into Left ($L$) and Right ($R$) is:
$$\\text{Gain} = \\frac{1}{2} \\left[ \\frac{G_L^2}{H_L + \\lambda} + \\frac{G_R^2}{H_R + \\lambda} - \\frac{(G_L + G_R)^2}{H_L + H_R + \\lambda} \\right] - \\gamma$$

**3. Native Missing Value Handling:**
During split evaluation, XGBoost assigns all missing samples to the Left child, computes gain; then assigns all missing samples to the Right child, computes gain. It chooses the direction that yields the highest gain and memorizes this as the **default direction** for that split during inference.""",
        "tip": "Explain that $\\lambda$ acts as an L2 regularizer on leaf weights, preventing extreme predictions when hessian sum $H_j$ is small."
    },
    {
        "id": "ml_07",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "difficulty": "Junior / Mid",
        "company_tags": ["Apple", "Amazon", "Capital One"],
        "question": "Why is feature scaling mandatory for KNN, SVM, and L2-regularized Logistic Regression, but completely irrelevant for Decision Trees and Random Forests?",
        "answer": """**1. Distance-Based and Optimization-Based Algorithms (Require Scaling):**
- **K-Nearest Neighbors (KNN):** Computes Euclidean distance $d(u, v) = \\sqrt{\\sum (u_i - v_i)^2}$. A feature with range $[0, 1,000,000]$ (e.g. salary) will mathematically dominate a feature with range $[0, 1]$ (e.g. age ratio), rendering the smaller feature completely invisible.
- **Support Vector Machines (SVM):** Maximizes the geometric margin $\\frac{2}{\\|w\\|_2}$. Without scaling, the margin boundary is skewed by large-scale features.
- **Regularized Regression (L1/L2):** The penalty $\\lambda \\sum w_j^2$ penalizes all weights equally. Unscaled features with huge magnitudes naturally require tiny weights ($w_j \\approx 0.0001$), so the regularization penalty barely affects them, while heavily penalizing small-scale features.
- **Gradient Descent:** Unscaled features create elongated elliptical contours, causing gradient oscillations and slow convergence.

**2. Tree-Based Algorithms (Scale Invariant):**
- Decision Trees split features using monotonic threshold comparisons: $x_j \\le t$.
- If you multiply feature $X_j$ by $10^6$ or take $\\log(X_j)$, the relative ordering of all data points remains identical. The tree will simply pick the scaled threshold $10^6 \\cdot t$. The impurity reduction (Gini/Entropy) is completely unaffected.""",
        "tip": "State clearly that decision trees are invariant to any monotonic transformation of features."
    },
    {
        "id": "ml_08",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "difficulty": "Mid / Senior",
        "company_tags": ["Google", "NVIDIA", "Meta"],
        "question": "What is the Kernel Trick in Support Vector Machines? Explain how it allows learning non-linear decision boundaries without computing explicit high-dimensional feature coordinates.",
        "answer": """**1. The Dual Formulation of SVM:**
The soft-margin SVM dual optimization problem depends solely on the **inner products** between data points:
$$\\max_\\alpha \\sum_{i=1}^n \\alpha_i - \\frac{1}{2} \\sum_{i=1}^n \\sum_{j=1}^n \\alpha_i \\alpha_j y_i y_j \\langle x_i, x_j \\rangle \\quad \\text{s.t.} \\quad 0 \\le \\alpha_i \\le C, \\sum \\alpha_i y_i = 0$$

**2. The Kernel Trick:**
If data is not linearly separable in input space $\\mathbb{R}^d$, we map it into a higher-dimensional feature space $\\mathcal{H}$ via mapping $\\phi(x)$.
In the dual problem, we replace $\\langle x_i, x_j \\rangle$ with $\\langle \\phi(x_i), \\phi(x_j) \\rangle$.
Computing $\\phi(x)$ explicitly can be computationally prohibitive or infinite-dimensional.
A **Kernel Function** $K(x_i, x_j) = \\langle \\phi(x_i), \\phi(x_j) \\rangle$ computes the exact inner product in $\\mathcal{H}$ directly using coordinates in the original low-dimensional space $\\mathbb{R}^d$.

**3. Example (Radial Basis Function / Gaussian Kernel):**
$$K(x, z) = \\exp\\left(-\\gamma \\|x - z\\|^2\\right)$$
By Taylor expanding the exponential function:
$$e^{2\\gamma x^T z} = \\sum_{k=0}^\\infty \\frac{(2\\gamma)^k}{k!} (x^T z)^k$$
The RBF kernel implicitly maps input vectors into an **infinite-dimensional** Hilbert space, allowing SVMs to draw complex non-linear decision boundaries with $O(d)$ compute per pair.""",
        "tip": "Cite Mercer's Theorem: Any symmetric, positive semi-definite function $K(x, z)$ corresponds to an inner product in some reproducing kernel Hilbert space (RKHS)."
    },
    {
        "id": "ml_09",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "difficulty": "Senior",
        "company_tags": ["Citadel", "Google Research", "OpenAI"],
        "question": "Explain the Curse of Dimensionality. Prove mathematically why Euclidean distance becomes ineffective as dimension $d \\to \\infty$.",
        "answer": """**1. The Geometric Paradox of High Dimensions:**
As dimension $d \\to \\infty$, the volume of a hypercube of side $1$ is $1^d = 1$, but the volume of an inscribed hypersphere of radius $r = 0.5$ is:
$$V_{\\text{sphere}}(d) = \\frac{\\pi^{d/2}}{\\Gamma(d/2 + 1)} r^d \\xrightarrow[d \\to \\infty]{} 0$$
Almost $100\\%$ of the volume of a high-dimensional cube is concentrated in its sharp corners outside the sphere!
Similarly, the volume of a spherical shell between radius $1 - \\epsilon$ and $1$ is $1 - (1 - \\epsilon)^d \\to 1$. All data points lie on the outer surface (boundary) of the space.

**2. Distance Concentration Phenomenon (Beyer et al., 1999):**
Under mild conditions, for independent, identically distributed features:
$$\\lim_{d \\to \\infty} \\frac{D_{\\max} - D_{\\min}}{D_{\\min}} = 0$$
where $D_{\\max}$ and $D_{\\min}$ are the maximum and minimum Euclidean distances from any query point to points in the dataset.
- In high dimensions, every point is essentially at the **exact same distance** to every other point.
- Distance-based algorithms like KNN, K-Means, and density-based clustering lose discriminative power because nearest and farthest neighbors differ by an infinitesimally small ratio.""",
        "tip": "Explain that this is why high-dimensional vector search relies on Cosine Similarity (angular distance on normalized hyperspheres) and dimensionality reduction (PCA, UMAP)."
    },
    {
        "id": "ml_10",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "difficulty": "Junior / Mid",
        "company_tags": ["Amazon", "Uber", "Spotify"],
        "question": "Why is K-Means clustering guaranteed to converge? Can it find the global optimum? How does K-Means++ initialization solve poor local optima?",
        "answer": """**1. Convergence Guarantee (Coordinate Descent):**
K-Means minimizes the Within-Cluster Sum of Squares (WCSS / Inertia):
$$J = \\sum_{k=1}^K \\sum_{i \\in C_k} \\|x_i - \\mu_k\\|^2$$
In each iteration:
1. **Assignment Step:** Assign each $x_i$ to nearest centroid $\\mu_k$. This monotonically decreases (or maintains) $J$ holding $\\mu$ fixed.
2. **Update Step:** Set $\\mu_k = \\frac{1}{|C_k|} \\sum_{i \\in C_k} x_i$. Setting the centroid to the cluster mean is the unique minimum of $\\sum \\|x_i - \\mu\\|^2$, decreasing $J$ holding assignments fixed.
Because $J \\ge 0$ (bounded below) and the number of possible partitions of $N$ points into $K$ clusters is finite ($K^N$), the sequence of $J$ values must strictly decrease and terminate at a local minimum.

**2. Local Minima Sensitivity:**
Standard random initialization can easily lead to terrible local minima (e.g., splitting a single dense cluster or trapping two clusters together). Finding the global minimum of K-Means is NP-hard.

**3. K-Means++ Initialization:**
1. Choose first center $\\mu_1$ uniformly at random from dataset.
2. For each remaining point $x$, compute $D(x) = \\min_{j} \\|x - \\mu_j\\|^2$ (distance to nearest existing centroid).
3. Select next centroid $\\mu_{next}$ with probability proportional to squared distance:
   $$P(x) = \\frac{D(x)^2}{\\sum_{x'} D(x')^2}$$
4. Repeat until $K$ centroids are chosen.
**Guarantee:** K-Means++ guarantees an expected approximation ratio of $O(\\log K)$ relative to the optimal clustering, virtually eliminating bad initialization traps.""",
        "tip": "Highlight that K-Means assumes spherical, isotropic clusters with equal variance; it struggles with elongated or varying-density clusters."
    },
    {
        "id": "ml_11",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "difficulty": "Mid / Senior",
        "company_tags": ["Goldman Sachs", "Google", "Two Sigma"],
        "question": "Derive Principal Component Analysis (PCA) mathematically. Why must data be centered ($mean=0$) before computing PCA?",
        "answer": """**1. Mathematical Derivation (Maximizing Variance):**
Let $X \\in \\mathbb{R}^{n \\times d}$ be a centered data matrix ($\\mathbb{E}[X] = 0$).
We wish to project $X$ onto a unit vector $u_1 \\in \\mathbb{R}^d$ ($\\|u_1\\|^2 = u_1^T u_1 = 1$) such that the sample variance of the projected data $z_1 = X u_1$ is maximized:
$$\\text{Var}(z_1) = \\frac{1}{n} z_1^T z_1 = \\frac{1}{n} u_1^T X^T X u_1 = u_1^T \\Sigma u_1$$
where $\\Sigma = \\frac{1}{n} X^T X$ is the empirical covariance matrix.

Set up the Lagrangian with multiplier $\\lambda$:
$$\\mathcal{L}(u_1, \\lambda) = u_1^T \\Sigma u_1 - \\lambda (u_1^T u_1 - 1)$$
Take the derivative with respect to $u_1$ and set to 0:
$$\\frac{\\partial \\mathcal{L}}{\\partial u_1} = 2 \\Sigma u_1 - 2 \\lambda u_1 = 0 \\implies \\Sigma u_1 = \\lambda u_1$$
This is the standard **eigenvalue equation**!
- The first principal component $u_1$ is the eigenvector of covariance matrix $\\Sigma$ corresponding to the largest eigenvalue $\\lambda_1$.
- The variance captured by $u_1$ is $u_1^T \\Sigma u_1 = u_1^T (\\lambda_1 u_1) = \\lambda_1$.

**2. Why Centering is Mandatory:**
If data is not centered, the sample covariance formula $\\frac{1}{n} X^T X$ actually computes the **second raw moment** $\\mathbb{E}[X X^T]$ rather than the central covariance $\\mathbb{E}[(X - \\mu)(X - \\mu)^T]$.
The first principal component will point directly toward the data mean vector $\\mu$ rather than along the direction of maximum internal variance.""",
        "tip": "Mention that in practice, PCA is computed using Singular Value Decomposition (SVD) of $X = U \\Sigma V^T$ rather than explicitly forming $X^T X$, for numerical stability."
    },
    {
        "id": "ml_12",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "difficulty": "Mid / Senior",
        "company_tags": ["Meta", "Apple", "Twitter/X"],
        "question": "What is the difference between Generative and Discriminative models? Use Naive Bayes and Logistic Regression as contrasting examples.",
        "answer": """**1. Core Definitions:**
- **Discriminative Models:** Model the conditional distribution $P(Y | X)$ directly. They focus exclusively on learning the optimal decision boundary between classes.
  - Examples: Logistic Regression, SVM, Decision Trees, Neural Networks.
- **Generative Models:** Model the joint distribution $P(X, Y) = P(X | Y) P(Y)$. They model how the data is generated for each class, then apply Bayes' Rule:
  $$P(Y|X) = \\frac{P(X|Y) P(Y)}{\\sum_{y'} P(X|y') P(y')}$$
  - Examples: Naive Bayes, Linear Discriminant Analysis (LDA), Gaussian Mixture Models (GMM), VAEs, Diffusion Models.

**2. Naive Bayes vs Logistic Regression (The Canonical Pair):**
Both model the log-odds as a linear function of $X$:
$$\\log \\frac{P(Y=1|X)}{P(Y=0|X)} = w^T X + b$$
- **Naive Bayes:** Assumes conditional independence between features given the class: $P(X|Y) = \\prod_{j=1}^d P(x_j|Y)$.
  - **Sample Complexity:** Reaches its asymptotic error faster with fewer samples ($O(\\log d)$ samples) because it estimates parameters independently per feature.
- **Logistic Regression:** Does not assume feature independence; fits weights jointly via maximum likelihood.
  - **Asymptotic Error:** Achieves lower asymptotic error than Naive Bayes when given abundant training data ($O(d)$ samples) because it accounts for feature correlations.""",
        "tip": "Refer to Ng & Jordan (2001) paper 'On Discriminative vs. Generative classifiers' comparing Naive Bayes and Logistic Regression sample efficiency."
    },
    {
        "id": "ml_13",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "difficulty": "Senior",
        "company_tags": ["Two Sigma", "AQR", "Citadel"],
        "question": "What happens in Linear Regression when features are highly multicollinear? How do you diagnose it, and what are 3 ways to solve it?",
        "answer": """**1. The Problem with Multicollinearity:**
In Ordinary Least Squares, $\\hat{w} = (X^T X)^{-1} X^T y$.
When features are collinear (e.g., $x_2 \\approx 2 x_1$):
- $X^T X$ becomes nearly singular (determinant $\\det(X^T X) \\approx 0$).
- Condition number $\\kappa(X^T X) = \\frac{\\lambda_{\\max}}{\\lambda_{\\min}} \\gg 1000$.
- The variance of weight estimates explodes:
  $$\\text{Var}(\\hat{w}_j) = \\sigma^2 [(X^T X)^{-1}]_{jj} = \\frac{\\sigma^2}{(n-1) s_j^2} \\cdot \\frac{1}{1 - R_j^2}$$
  Individual coefficient values become wildly unstable, change signs erratically, and lose interpretability.

**2. Diagnosis:**
- **Variance Inflation Factor (VIF):** Regress feature $x_j$ on all other features to get $R_j^2$:
  $$\\text{VIF}_j = \\frac{1}{1 - R_j^2}$$
  Rule of thumb: $\\text{VIF} > 5 \\text{ to } 10$ indicates severe multicollinearity.
- **Correlation Matrix Heatmap:** High pairwise Pearson correlation $|r| > 0.85$.
- **Condition Number:** Eigenvalue ratio $\\sqrt{\\lambda_{\\max} / \\lambda_{\\min}} > 30$.

**3. Remediation Strategies:**
1. **L2 Regularization (Ridge):** Adds $\\lambda I$ to $X^T X$, making $(X^T X + \\lambda I)$ strictly invertible and well-conditioned.
2. **Feature Removal / Consolidation:** Drop redundant features or aggregate them into an index.
3. **PCA (Principal Component Regression):** Transform correlated features into orthogonal principal components.""",
        "tip": "Clarify that multicollinearity does NOT degrade overall prediction accuracy or $R^2$; it destroys individual coefficient interpretability and stability."
    },
    {
        "id": "ml_14",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "difficulty": "Mid",
        "company_tags": ["Google", "Meta"],
        "question": "What is the difference between Parametric and Non-Parametric Machine Learning models? Provide examples of each and explain their sample complexity trade-offs.",
        "answer": """**1. Parametric Models:**
- **Definition:** Summarize data through a fixed number of parameters that does **not** grow with sample size $N$.
- **Mechanism:** Makes strong structural assumptions about the functional form $f(X; \\theta)$.
- **Examples:** Linear Regression ($d+1$ weights), Logistic Regression, Naive Bayes, Linear Discriminant Analysis.
- **Trade-offs:** Fast training and inference, low memory footprint, highly interpretable; but limited capacity (high bias) if the functional form assumption is wrong.

**2. Non-Parametric Models:**
- **Definition:** The number of effective parameters is free to grow with the size of the training dataset $N$. They do not assume a predefined mathematical functional form.
- **Examples:** K-Nearest Neighbors (memorizes all $N$ points), Decision Trees (tree depth grows with $N$), Support Vector Machines with RBF kernel (depends on support vector count), Gaussian Processes.
- **Trade-offs:** Flexible, can model arbitrarily complex surfaces (low bias); but slower inference, higher memory footprint, and prone to overfitting if not regularized.""",
        "tip": "Make sure to emphasize that 'non-parametric' does not mean 'zero parameters'; it means parameters are not fixed a priori."
    },
    {
        "id": "ml_15",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "difficulty": "Senior",
        "company_tags": ["DeepMind", "Jane Street", "Apple"],
        "question": "How does the Expectation-Maximization (EM) algorithm work for Gaussian Mixture Models (GMM)? How is it related to K-Means?",
        "answer": """**1. Gaussian Mixture Model Formulation:**
Models data distribution as a weighted sum of $K$ multivariate Gaussians:
$$p(x) = \\sum_{k=1}^K \\pi_k \\mathcal{N}(x | \\mu_k, \\Sigma_k), \\quad \\sum \\pi_k = 1$$
Direct maximum likelihood has no closed-form solution due to hidden latent cluster assignments $z_i \\in \\{1, \\dots, K\\}$.

**2. EM Algorithm Steps:**
- **E-Step (Expectation):** Compute the posterior probability (responsibility) that Gaussian $k$ generated point $x_i$:
  $$\\gamma_{ik} = P(z_i = k | x_i) = \\frac{\\pi_k \\mathcal{N}(x_i | \\mu_k, \\Sigma_k)}{\\sum_{j=1}^K \\pi_j \\mathcal{N}(x_i | \\mu_j, \\Sigma_j)}$$
- **M-Step (Maximization):** Update Gaussian parameters using the soft responsibilities $\\gamma_{ik}$:
  $$N_k = \\sum_{i=1}^n \\gamma_{ik}, \\quad \\mu_k^{new} = \\frac{1}{N_k} \\sum_{i=1}^n \\gamma_{ik} x_i$$
  $$\\Sigma_k^{new} = \\frac{1}{N_k} \\sum_{i=1}^n \\gamma_{ik} (x_i - \\mu_k^{new})(x_i - \\mu_k^{new})^T, \\quad \\pi_k^{new} = \\frac{N_k}{n}$$

**3. Connection to K-Means:**
K-Means is a special, degenerate case of GMM:
- Covariance matrices are fixed to spherical isotropic noise: $\\Sigma_k = \\sigma^2 I$.
- Mixture weights are equal: $\\pi_k = 1/K$.
- As $\\sigma^2 \\to 0$, the soft responsibilities $\\gamma_{ik}$ become hard binary indicators $\\in \\{0, 1\\}$ assigning each point strictly to its closest centroid.""",
        "tip": "Explain that GMM handles non-spherical clusters with elliptical covariance orientations, providing probabilistic cluster membership."
    },
    {
        "id": "ml_16",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "difficulty": "Senior",
        "company_tags": ["OpenAI", "Meta", "Google"],
        "question": "Why can Early Stopping in gradient descent optimization be mathematically viewed as a form of L2 Regularization (Weight Decay)?",
        "answer": """**Mathematical Equivalence (Bishop, PRML):**
Consider quadratic loss around the optimum $w^*$:
$$E(w) \\approx E(w^*) + \\frac{1}{2} (w - w^*)^T H (w - w^*)$$
where $H$ is the Hessian matrix with eigenvectors $v_j$ and eigenvalues $\\lambda_j$.

**1. Gradient Descent Trajectory:**
Starting at $w_0 = 0$ with learning rate $\\eta$, after $\\tau$ iterations:
$$w(\\tau) = \\sum_j \\left[ 1 - (1 - \\eta \\lambda_j)^\\tau \\right] (w^* \\cdot v_j) v_j$$

**2. L2 Regularization Closed-Form:**
Minimizing $E(w) + \\frac{1}{2} \\alpha w^T w$ gives:
$$w_{L2} = \\sum_j \\left[ \\frac{\\lambda_j}{\\lambda_j + \\alpha} \\right] (w^* \\cdot v_j) v_j$$

**3. Comparison:**
Equating the shrinkage factors for small $\\eta \\lambda$:
$$1 - (1 - \\eta \\lambda_j)^\\tau \\approx 1 - e^{-\\tau \\eta \\lambda_j} \\approx \\frac{\\lambda_j}{\\lambda_j + \\frac{1}{\\tau \\eta}}$$
Comparing this to the L2 weight decay parameter $\\alpha$:
$$\\alpha \\approx \\frac{1}{\\tau \\eta}$$
- **Early Stopping at iteration $\\tau$ is mathematically equivalent to L2 regularization with $\\lambda = \\frac{1}{\\tau \\eta}$.**
- Stopping early prevents weights along directions with small eigenvalues (slowly converging noise directions) from growing large, exactly like weight decay!""",
        "tip": "This is a quintessential senior machine learning theory question that bridges optimization dynamics and statistical regularization."
    },
    {
        "id": "ml_17",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "difficulty": "Mid",
        "company_tags": ["Kaggle", "ByteDance", "Airbnb"],
        "question": "What is Target Encoding, why does naive Target Encoding cause catastrophic data leakage, and how do Out-of-Fold (OOF) and additive smoothing fix it?",
        "answer": """**1. Concept:**
For high-cardinality categorical features (e.g. 5,000 ZIP codes), one-hot encoding creates extreme sparsity.
Target encoding replaces each category $c$ with the expected target value:
$$\\hat{x}_c = \\mathbb{E}[y | x = c] = \\frac{\\sum_{i \\in c} y_i}{n_c}$$

**2. The Target Leakage Catastrophe:**
If category $c$ appears only once in the dataset with label $y=1$, naive target encoding assigns $x_c = 1.0$.
A tree model can trivially achieve $100\\%$ training accuracy by splitting on $x_c = 1.0$, memorizing training labels rather than learning general patterns. During testing, unseen or rare categories fail completely.

**3. Solutions:**
- **Additive Smoothing (M-estimate):** Shrinks small sample categories toward the global target mean $\\bar{y}$:
  $$S_c = \\frac{n_c \\cdot \\bar{y}_c + m \\cdot \\bar{y}}{n_c + m}$$
  where $m$ is a smoothing weight. If $n_c$ is tiny, $S_c \\approx \\bar{y}$.
- **Out-of-Fold (OOF) Target Encoding:** Split training data into $K$ folds. Encode fold $k$ using only statistics computed from the remaining $K-1$ folds.
- **Ordered Target Encoding (CatBoost):** Computes category mean using only observations that arrived prior to the current sample in a random permutation.""",
        "tip": "CatBoost won Kaggle tabular competitions precisely because its ordered target encoding prevents this leakage on streaming and cross-validation splits."
    },
    {
        "id": "ml_18",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "difficulty": "Junior / Mid",
        "company_tags": ["Amazon", "Uber", "Palantir"],
        "question": "Explain the difference between Bagging, Boosting, and Stacking ensemble methods.",
        "answer": """**1. Bagging (Bootstrap Aggregating):**
- **Architecture:** Trains $B$ homogeneous models independently in parallel on bootstrap samples (sampling with replacement) of the training dataset.
- **Aggregation:** Averaging (regression) or majority voting (classification).
- **Goal:** Reduces **variance** without altering bias.
- **Example:** Random Forest.

**2. Boosting:**
- **Architecture:** Trains homogeneous base learners sequentially. Each subsequent learner focuses on the residual errors or misclassified instances of the prior ensemble.
- **Aggregation:** Weighted sum of base learner predictions: $F(x) = \\sum \\eta_m h_m(x)$.
- **Goal:** Primarily reduces **bias** by learning hard examples.
- **Examples:** AdaBoost, Gradient Boosting, XGBoost, LightGBM.

**3. Stacking (Stacked Generalization):**
- **Architecture:** Trains heterogeneous base models (e.g. LightGBM, Logistic Regression, Random Forest, Neural Network) in parallel.
- **Aggregation:** A meta-learner (e.g. Ridge Regression) is trained to combine the out-of-fold predictions of the base learners to produce the final target prediction.
- **Goal:** Maximizes predictive diversity by blending fundamentally different model families.""",
        "tip": "Emphasize that in Stacking, out-of-fold cross-validation predictions MUST be used to train the meta-learner to avoid severe data leakage."
    },
    {
        "id": "ml_19",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "difficulty": "Mid / Senior",
        "company_tags": ["Two Sigma", "Citadel", "Millennium"],
        "question": "Why can't Linear Regression be solved using the Ordinary Least Squares formula $\\hat{w} = (X^T X)^{-1} X^T y$ when the number of features $d$ exceeds the number of samples $n$ ($d > n$)?",
        "answer": """**1. Linear Algebra Proof:**
- Let $X \\in \\mathbb{R}^{n \\times d}$. The matrix $X^T X \\in \\mathbb{R}^{d \\times d}$.
- The rank of a matrix product is bounded by the rank of its factors:
  $$\\text{rank}(X^T X) = \\text{rank}(X) \\le \\min(n, d)$$
- When $d > n$, $\\text{rank}(X^T X) \\le n < d$.
- Because the $d \\times d$ matrix $X^T X$ has rank at most $n$, it is **rank-deficient**. It has at least $d - n$ zero eigenvalues.
- Therefore, $\\det(X^T X) = 0$, meaning $(X^T X)$ is **singular and not invertible**.

**2. Geometric & Optimization Implication:**
When $d > n$, the linear system $X w = y$ is underdetermined. There are infinitely many weight vectors $w$ that achieve exact zero training loss ($R^2 = 1.0$).
- OLS has no unique solution.
- Solutions require either dimensionality reduction (PCA), sparsity constraints ($L_1$ Lasso), or Ridge Regularization $(X^T X + \\lambda I)^{-1} X^T y$, which adds $\\lambda > 0$ to all eigenvalues, guaranteeing invertibility.""",
        "tip": "Mention the Moore-Penrose pseudoinverse $X^+$ as the minimal $L_2$-norm solution among the infinite valid interpolators."
    },
    {
        "id": "ml_20",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "difficulty": "Senior",
        "company_tags": ["Stripe", "Goldman Sachs"],
        "question": "What is Heteroskedasticity in regression analysis? How do you detect it in residual plots, and what are its statistical consequences?",
        "answer": """**1. Definition:**
A core Gauss-Markov assumption of Ordinary Least Squares is **homoskedasticity** (constant residual variance across all observation levels):
$$\\text{Var}(\\epsilon_i | x_i) = \\sigma^2 \\quad \\forall i$$
**Heteroskedasticity** occurs when residual variance varies with $x_i$: $\\text{Var}(\\epsilon_i | x_i) = \\sigma_i^2$ (e.g. income vs food expenditure; higher income brackets exhibit much larger variance in spending).

**2. Detection:**
- **Residual vs Fitted Plot:** Residuals display a distinctive **funnel (cone) shape**, fanning out as $\\hat{y}$ increases.
- **Statistical Tests:**
  - Breusch-Pagan Test: Regresses squared residuals $e_i^2$ on predictors $X$.
  - White's Test: Tests for general non-linear heteroskedasticity.

**3. Statistical Consequences:**
- OLS coefficient estimates $\\hat{w}$ remain **unbiased and consistent**.
- However, OLS is **no longer BLUE** (Best Linear Unbiased Estimator).
- The standard error formulas for $w$ are invalid, leading to severely biased p-values and confidence intervals (falsely inflated significance).

**4. Solutions:**
- Apply log or Box-Cox transformation to the target variable: $\\log(y)$.
- Use Huber-White **Heteroskedasticity-Consistent (HC) Robust Standard Errors**.
- Fit Weighted Least Squares (WLS), weighting each point by $1/\\sigma_i^2$.""",
        "tip": "Be sure to state clearly that coefficients remain unbiased; only the standard errors and hypothesis tests become untrustworthy."
    },
    {
        "id": "ml_21",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "difficulty": "Mid / Senior",
        "company_tags": ["Google", "Meta", "Netflix"],
        "question": "What is Simpson's Paradox? Provide a concrete machine learning / statistical example where an aggregated trend is reversed in subgroups.",
        "answer": """**1. Definition:**
Simpson's Paradox is a statistical phenomenon where a trend appears in multiple individual groups of data, but disappears or completely reverses when the groups are aggregated together. It is caused by an unobserved or ignored **confounding variable** that influences group allocation.

**2. Concrete Example (Medical Recovery Rate):**
Comparing Treatment A vs Treatment B across 800 patients with Mild vs Severe conditions:
- **Mild Cases:**
  - Treatment A: 81/90 recovered (90%)
  - Treatment B: 270/300 recovered (90%)
- **Severe Cases:**
  - Treatment A: 192/240 recovered (80%)
  - Treatment B: 56/70 recovered (80%)
*In both subgroups, Treatment A and B have identical recovery rates!*

Now consider an aggressive variant:
- **Treatment A** was primarily administered to severe patients: 273/330 total recovered (**82.7%**).
- **Treatment B** was primarily administered to mild patients: 326/370 total recovered (**88.1%**).
In aggregate, Treatment B looks superior (88.1% vs 82.7%), yet conditionally Treatment A is equal or better.

**3. Implication for Machine Learning:**
If an ML model is trained on aggregated tabular data without conditioning on the confounder (severity), it will learn a spurious correlation and make harmful real-world decisions.""",
        "tip": "Explain that causal diagrams (DAGs) and Pearl's do-calculus are required to properly control for confounders and resolve Simpson's Paradox."
    },
    {
        "id": "ml_22",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "difficulty": "Senior / Staff",
        "company_tags": ["DeepMind", "Jane Street"],
        "question": "What is the difference between a convex and non-convex optimization problem? Why is convexity so prized in classical ML, and why do we accept non-convexity in Deep Learning?",
        "answer": """**1. Convex Optimization:**
A set $\\mathcal{C}$ is convex if $\\forall x, y \\in \\mathcal{C}, \\theta \\in [0, 1] \\implies \\theta x + (1-\\theta)y \\in \\mathcal{C}$.
A function $f: \\mathcal{C} \\to \\mathbb{R}$ is convex if:
$$f(\\theta x + (1-\\theta)y) \\le \\theta f(x) + (1-\\theta)f(y)$$
- **Key Property:** Every local minimum is guaranteed to be a **global minimum**.
- **Classical ML Examples:** Linear Regression (OLS), Logistic Regression (Log Loss), Support Vector Machines (Quadratic Programming).
- Guaranteed polynomial-time convergence with zero sensitivity to initialization.

**2. Non-Convex Optimization in Deep Learning:**
Deep neural networks compose non-linear activation functions across multiple matrix multiplications, generating highly non-convex loss surfaces filled with saddle points, ravines, and countless local minima.
- We accept non-convexity because non-linear deep representations achieve vastly superior representational capacity (Universal Approximation).
- **Why it works in practice:** In ultra-high dimensional spaces, true local minima are rare; almost all critical points are **saddle points** with escape directions. Furthermore, overparameterization ensures that most local minima achieve loss values nearly identical to the global optimum.""",
        "tip": "Mention the work of Dauphin et al. (2014) showing that saddle points, rather than bad local minima, are the primary obstacle in non-convex neural net optimization."
    },
    {
        "id": "ml_23",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "difficulty": "Mid / Senior",
        "company_tags": ["Microsoft", "Google"],
        "question": "What is the inductive bias of an ML model? Compare the inductive biases of Linear Models, Decision Trees, CNNs, and Transformers.",
        "answer": """**1. Definition:**
Inductive bias is the set of explicit or implicit assumptions a learning algorithm uses to predict outputs on unseen inputs before seeing any training data. Without inductive bias, an algorithm has no basis to generalize beyond exact memorized training samples.

**2. Inductive Biases Across Architectures:**
- **Linear Regression / Logistic Regression:** Assumes that the relationship between inputs and output log-odds is strictly additive and linear.
- **Decision Trees:** Assumes that the data can be recursively partitioned using orthogonal, axis-aligned hyperplanes.
- **Convolutional Neural Networks (CNNs):**
  - *Translation Invariance / Equivariance:* A feature (e.g. edge or cat eye) is identical regardless of where it appears in the image.
  - *Locality:* Nearby pixels are strongly correlated; distant pixels are independent.
- **Transformers:** Possesses very **weak inductive bias**. Every token can attend to every other token anywhere in the sequence from layer 1.
  - Advantage: Can learn arbitrary complex relational patterns.
  - Trade-off: Requires massive pre-training datasets to learn basic spatial or sequential inductive rules that CNNs and RNNs assume out-of-the-box.""",
        "tip": "Highlight that as inductive bias decreases, model capacity increases, but required training data volume scales exponentially."
    },
    {
        "id": "ml_24",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "difficulty": "Mid",
        "company_tags": ["Amazon", "Uber", "Doordash"],
        "question": "Why does K-Nearest Neighbors (KNN) degrade severely in inference speed when dataset size $N$ is large, and how do KD-Trees and Ball Trees accelerate queries?",
        "answer": """**1. Exhaustive KNN Complexity:**
Standard brute-force KNN computes the distance from query point $q$ to every single training point $x_i$ ($i = 1, \\dots, N$).
- Time complexity: $O(N \\cdot d)$.
- Memory: Must store the entire training dataset in RAM.
- At $N = 10,000,000$, a single query takes hundreds of milliseconds.

**2. KD-Trees (K-Dimensional Trees):**
- A binary search tree that recursively splits points along axis-aligned hyperplanes alternating across dimensions $1, \\dots, d$.
- Query complexity: $O(d \\log N)$ on average for low dimensions.
- **Failure Mode:** In high dimensions ($d > 20$), the search must backtrack through almost every branch of the tree, degenerating back to brute-force $O(N)$.

**3. Ball Trees:**
- Partitions data into nested hyperspheres (balls) rather than axis-aligned boxes.
- Uses the triangle inequality $d(q, x) \\ge |d(q, c) - r|$ to prune entire subtrees that cannot contain a nearest neighbor.
- Far superior to KD-Trees in medium-to-high dimensions.""",
        "tip": "Note that for high-dimensional production embeddings ($d=512, 1536$), exact search is abandoned in favor of Approximate Nearest Neighbor (ANN) graphs like HNSW."
    },
    {
        "id": "ml_25",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "difficulty": "Junior / Mid",
        "company_tags": ["Meta", "Apple", "Capital One"],
        "question": "What is the difference between hard-margin and soft-margin SVM? What is the role of the hyperparameter $C$?",
        "answer": """**1. Hard-Margin SVM:**
Assumes the training data is linearly separable:
$$\\min_w \\frac{1}{2}\\|w\\|^2 \\quad \\text{s.t.} \\quad y_i (w^T x_i + b) \\ge 1 \\quad \\forall i$$
- Strictly prohibits any misclassification or points inside the margin.
- If data is not perfectly separable, no solution exists. Extremely sensitive to outliers.

**2. Soft-Margin SVM (Cortes & Vapnik, 1995):**
Introduces slack variables $\\xi_i \\ge 0$ allowing points to violate the margin:
$$\\min_{w, b, \\xi} \\frac{1}{2}\\|w\\|^2 + C \\sum_{i=1}^n \\xi_i \\quad \\text{s.t.} \\quad y_i (w^T x_i + b) \\ge 1 - \\xi_i$$
- $\\xi_i = 0$: Point is on or outside the correct margin.
- $0 < \\xi_i \\le 1$: Point is within the margin boundary but correctly classified.
- $\\xi_i > 1$: Point is misclassified.

**3. Role of Hyperparameter $C$:**
- **Large $C$ (Hard margin behavior):** High penalty on slack violations. Forces smaller margins to classify training points correctly. High variance (overfitting risk).
- **Small $C$ (Soft margin behavior):** Tolerates more misclassifications in exchange for a wider, more robust margin. High bias (underfitting risk).""",
        "tip": "Remember that $C$ is inverse to the regularization parameter: large $C$ corresponds to small regularization $\\lambda$."
    }
]

print(f"Total initial questions in builder: {len(QUESTIONS)}")
