import json
import re

def main():
    # 1. Load concepts.json
    with open("src/data/concepts.json", "r", encoding="utf-8") as f:
        concepts = json.load(f)

    # 2. Load all_concepts.json
    with open("scripts/data_sources/all_concepts.json", "r", encoding="utf-8") as f:
        all_concepts = json.load(f)

    normal_eq_data = {
        "id": "concept_normal_equation",
        "title": "Analytical Solution (The Normal Equation)",
        "topic_id": "ml_linear",
        "topic_label": "Linear Regression & Core ML Concepts",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "raw_subtopic": "Analytical Solution (Closed-form Normal Equation)",
        "def": "The Normal Equation is a mathematical formula that calculates the optimal weights and bias for linear regression in a single step without using gradient descent.",
        "formula": "$$\\boldsymbol{\\theta} = (\\mathbf{X}^T \\mathbf{X})^{-1} \\mathbf{X}^T \\mathbf{y}$$",
        "logic": "Instead of guessing initial weights and taking hundreds of small gradient descent steps, the Normal Equation solves the calculus directly: it sets the derivative of the squared error to zero and solves for the exact best weights using matrix algebra.",
        "example": "Fitting a line through 100 house sales: Instead of looping through 1,000 training epochs, you compute (X^T X)^(-1) X^T y in NumPy. In less than 1 millisecond, it outputs the exact best slope and intercept.",
        "tags": [
            "Normal Equation",
            "Closed Form",
            "Linear Regression",
            "Matrix Inversion",
            "OLS"
        ],
        "definition": "The Normal Equation is a mathematical formula that calculates the optimal weights and bias for linear regression in a single step without using gradient descent.",
        "formula_explanation": "",
        "simple_summary": "Gradient descent reaches the best weights by taking small steps down a hill. The Normal Equation teleports straight to the bottom of the hill in a single calculation: θ = (X^T X)^(-1) X^T y. You don't need a learning rate or feature scaling. However, inverting a matrix takes heavy computer memory, making it ideal for small datasets (under 10,000 features) but impractical for massive neural networks.",
        "core_terms": [
            {
                "term": "Analytical Solution (Closed-Form)",
                "what_is_it": "• A mathematical formula that delivers the exact answer directly in one calculation.\n• Unlike iterative loops that take small steps toward a solution, an analytical formula solves it immediately.",
                "analogy": "Using the quadratic formula to solve an algebra problem directly instead of guessing numbers until one works.",
                "why_it_matters": "Gives you the exact mathematically optimal weights with zero iterations and zero learning rate tuning."
            },
            {
                "term": "Matrix Inversion (O(D^3) Cost)",
                "what_is_it": "• The computational bottleneck of the Normal Equation: calculating the inverse of the (X^T X) matrix.\n• As the number of features D grows, inverting the matrix takes time proportional to D cubed (D^3).",
                "analogy": "Untangling a string: easy with 5 knots, but exponentially harder and slower with 50,000 knots.",
                "why_it_matters": "Explains why the Normal Equation is super fast for 50 features, but completely impractical for deep neural networks with millions of parameters."
            },
            {
                "term": "Orthogonal Projection (Why 'Normal'?)",
                "what_is_it": "• Geometrically, 'normal' means perpendicular (at a 90-degree angle).\n• The best prediction is found by dropping a perpendicular shadow of your target vector directly onto the feature plane.",
                "analogy": "Dropping a ball straight down onto the floor: the shortest distance from the ceiling to the floor is a straight 90-degree line.",
                "why_it_matters": "Guarantees that the remaining prediction errors (residuals) are as small as physically possible."
            }
        ],
        "types_header": "Normal Equation vs Gradient Descent",
        "types_badge": "Optimization Comparison",
        "quick_types": [
            {
                "type": "Normal Equation (Closed-Form)",
                "definition": "Solves for weights in a single mathematical step; requires no learning rate and no feature scaling.",
                "looks_like": "theta = np.linalg.pinv(X_b) @ y"
            },
            {
                "type": "Gradient Descent (Iterative)",
                "definition": "Updates weights step-by-step; scales smoothly to millions of rows and features.",
                "looks_like": "w = w - learning_rate * grad"
            },
            {
                "type": "Scikit-Learn LinearRegression",
                "definition": "Uses this exact linear algebra pseudoinverse (via LAPACK) under the hood for OLS.",
                "looks_like": "model = LinearRegression().fit(X, y)"
            },
            {
                "type": "Moore-Penrose Pseudoinverse",
                "definition": "A robust matrix inverse used by NumPy (pinv) that works even when features are duplicate or collinear.",
                "looks_like": "np.linalg.pinv(X) instead of np.linalg.inv(X)"
            }
        ],
        "symbol_guide": [
            {
                "symbol": "θ (theta)",
                "meaning": "Parameter Vector",
                "plain_english": "The list of optimal weights and bias calculated by the formula"
            },
            {
                "symbol": "X",
                "meaning": "Feature Matrix",
                "plain_english": "The 2D table of inputs with an added column of 1s for the bias"
            },
            {
                "symbol": "X^T",
                "meaning": "Transpose of X",
                "plain_english": "The feature table flipped on its side (rows become columns)"
            },
            {
                "symbol": "(X^T X)^(-1)",
                "meaning": "Matrix Inverse",
                "plain_english": "The linear algebra equivalent of dividing by (X^T X)"
            }
        ],
        "numerical_example": "Solving a 1D Line with the Normal Equation:\nSuppose we have 2 data points:\n• Point 1: x = 1, y = 3\n• Point 2: x = 2, y = 5\n\nStep 1: Add a column of 1s for the bias (intercept):\n  X = [[1, 1], [1, 2]],   y = [3, 5]\n\nStep 2: Multiply X^T by X:\n  X^T X = [[1, 1], [1, 2]]^T @ [[1, 1], [1, 2]] = [[2, 3], [3, 5]]\n\nStep 3: Invert the 2x2 matrix:\n  (X^T X)^(-1) = [[5, -3], [-3, 2]]\n\nStep 4: Multiply by X^T y:\n  X^T y = [8, 13]\n  θ = [[5, -3], [-3, 2]] @ [8, 13] = [1, 2]\n\nResult:\n• Bias b = 1, Weight w = 2\n• Exact fitted equation: ŷ = 2x + 1\n• Check Point 1: 2(1) + 1 = 3 (Exact match!). Point 2: 2(2) + 1 = 5 (Exact match!).",
        "pitfalls": "Common Pitfall: Using the Normal Equation on huge feature sets or non-linear models. Inverting an (X^T X) matrix takes O(D^3) computation—if you have 50,000 features, matrix inversion can freeze your computer. Also, the Normal Equation is strictly designed for linear regression; you cannot use it for logistic regression, decision trees, or neural networks. In Scikit-Learn, if features are massive, switch from LinearRegression to SGDRegressor.",
        "core_logic": "Why this matters: In calculus, to find the minimum of a curve, you set its derivative to zero. For linear regression with squared errors, setting the derivative vector (gradient) to zero produces a linear system of equations known as the Normal Equations. Because the equations are linear, algebra allows us to solve for optimal weights directly without guessing.",
        "architectural_logic": "Under the hood, Scikit-Learn's LinearRegression does not actually calculate (X^T X)^(-1) directly because inverting can be numerically unstable if features are collinear. Instead, it uses Singular Value Decomposition (SVD) via scipy.linalg.lstsq, which stably computes the pseudoinverse in a single C/Fortran call.",
        "connected_logic": [
            {
                "title": "When to Use Normal Equation vs Gradient Descent",
                "content": "• Use Normal Equation: For small or medium tabular datasets (fewer than 10,000 features) where instant exact solutions are convenient.\n• Use Gradient Descent: When you have millions of rows or features, or when training non-linear models."
            },
            {
                "title": "Why No Feature Scaling is Needed",
                "content": "• Gradient descent needs feature scaling so it doesn't bounce wildly along steep dimensions.\n• The Normal Equation solves the math in one step, so feature scaling has zero effect on the final weights."
            },
            {
                "title": "Handling Redundant Features (Collinearity)",
                "content": "• If two features are identical, the matrix (X^T X) cannot be inverted normally (it is singular).\n• Using the Moore-Penrose pseudoinverse (pinv) resolves this gracefully by finding a valid minimum-norm solution."
            },
            {
                "title": "Adding Regularization: Ridge Regression",
                "content": "• When features are noisy, adding an L2 penalty λ creates Ridge Regression: w* = (X^T X + λI)^(-1) X^T y.\n• Adding λI guarantees the matrix is always invertible, preventing numeric instability."
            }
        ],
        "key_takeaways": [
            "Closed-Form Solution: Solves for linear regression weights in one mathematical step.",
            "No Hyperparameters: Requires no learning rate, no iterations, and no feature scaling.",
            "O(D^3) Limitation: Matrix inversion becomes too slow when feature count exceeds 10,000.",
            "Linear Regression Only: Works strictly for ordinary least-squares, not general ML models."
        ],
        "definition_bullets": [
            "Normal Equation: An analytical formula that directly computes the least-squares parameters for linear regression.",
            "Analytical Solution: Solving a mathematical problem directly with an exact formula rather than step-by-step guessing."
        ]
    }

    # Update in concepts.json
    for c in concepts:
        if c.get("id") == "concept_normal_equation":
            c.update(normal_eq_data)
            print("Updated concept_normal_equation in concepts.json")
            break

    with open("src/data/concepts.json", "w", encoding="utf-8") as f:
        json.dump(concepts, f, indent=2, ensure_ascii=False)

    # Update in all_concepts.json
    for c in all_concepts:
        if c.get("id") == "concept_normal_equation":
            c.update(normal_eq_data)
            print("Updated concept_normal_equation in all_concepts.json")
            break

    with open("scripts/data_sources/all_concepts.json", "w", encoding="utf-8") as f:
        json.dump(all_concepts, f, indent=2, ensure_ascii=False)

    # Update in concepts_ml.py
    with open("scripts/data_sources/concepts_ml.py", "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r'\{\s*"id":\s*"concept_normal_equation".*?\},(?=\s*\{\s*"id":\s*"concept_model_inference")'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        lines = json.dumps(normal_eq_data, indent=4, ensure_ascii=False).splitlines()
        indented_replacement = "\n".join("    " + line for line in lines) + ","
        new_content = content[:match.start()] + indented_replacement + content[match.end():]
        with open("scripts/data_sources/concepts_ml.py", "w", encoding="utf-8") as f:
            f.write(new_content)
        print("Updated concept_normal_equation in concepts_ml.py")
    else:
        print("Could not find regex match in concepts_ml.py")

if __name__ == "__main__":
    main()
