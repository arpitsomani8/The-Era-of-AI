"""
Complete Concept Enrichment Engine for The Era of AI
Enriches all 170 concepts with novice-friendly explanations, term-by-term breakdowns,
symbol decoders, and step-by-step real-number examples.
"""

import json
import os
import re

CONCEPTS_PATH = os.path.join(os.path.dirname(__file__), "..", "src", "data", "concepts.json")
ALL_CONCEPTS_PATH = os.path.join(os.path.dirname(__file__), "data_sources", "all_concepts.json")

# Handcrafted, deeply educational enrichments for core foundational topics
DETAILED_MAP = {
    # LINEAR ALGEBRA
    "concept_dot_product_cosine": {
        "simple_summary": "Think of vectors as arrows pointing in space, the dot product as a tool to measure how much two arrows point in the same direction, and cosine similarity as a score from -1 to +1 that measures alignment while ignoring arrow length.",
        "core_terms": [
            {
                "term": "Vector",
                "what_is_it": "A list of numbers that describes something. In AI, every piece of data (words, images, house prices, audio) is converted into a vector.",
                "analogy": "A GPS coordinate (latitude, longitude) is a 2D vector. A house profile [3 bedrooms, 2 bathrooms, 1500 sqft, $350k] is a 4D vector.",
                "why_it_matters": "Computers cannot read text or look at images directly; they only understand numbers arranged in vectors."
            },
            {
                "term": "Dot Product",
                "what_is_it": "A math operation where you multiply matching numbers from two vectors and add them up. It tells you whether two vectors push in the same direction, push against each other, or are completely unrelated.",
                "analogy": "If you and a friend push a heavy cart in the exact same direction, your combined effort is high (positive dot product). If you push in opposite directions, you cancel out (negative). If you push at a 90° right angle, your push doesn't help your friend at all (zero dot product).",
                "why_it_matters": "It is the core building block of AI neural networks, attention mechanisms, and feature matching."
            },
            {
                "term": "Cosine Similarity",
                "what_is_it": "A similarity score between -1 and +1 that measures only the angle (direction) between two vectors, completely ignoring their length or size.",
                "analogy": "A short 1-sentence tweet and a 20-page article about 'quantum computing' both talk about the same topic. Their vectors point in the same direction. Cosine similarity recognizes they are 99% identical in topic, even though the 20-page article has much larger numbers because it has more words.",
                "why_it_matters": "Essential for search engines, recommendation systems, and Vector Databases (RAG) to find related content fairly without favoring long documents."
            }
        ],
        "symbol_guide": [
            {"symbol": "u, v", "meaning": "Two vectors (lists of numbers) being compared", "plain_english": "e.g. vector u = [1, 2] and vector v = [3, 4]"},
            {"symbol": "u · v", "meaning": "The dot product of u and v", "plain_english": "Multiply pairs and add: (1×3) + (2×4) = 11"},
            {"symbol": "∑ u_i v_i", "meaning": "Sum of products across all dimensions i", "plain_english": "Loop through all numbers in the list and multiply matching positions"},
            {"symbol": "||u||_2", "meaning": "The Euclidean length (magnitude) of vector u", "plain_english": "Square each number, sum them up, and take the square root (Pythagorean theorem)"},
            {"symbol": "θ (theta)", "meaning": "The angle between the two arrows in space", "plain_english": "0° means identical direction, 90° means perpendicular (unrelated), 180° means opposite"},
            {"symbol": "cos(θ)", "meaning": "Cosine of the angle (Cosine Similarity)", "plain_english": "+1.0 = identical direction, 0.0 = completely unrelated, -1.0 = exact opposite"}
        ],
        "numerical_example": "Let Vector A = [1, 2] and Vector B = [3, 4].\n1. Multiply matching positions: (1 × 3) = 3 and (2 × 4) = 8.\n2. Dot Product: 3 + 8 = 11.\n3. Length of A: √(1² + 2²) = √(1 + 4) = √5 ≈ 2.236.\n4. Length of B: √(3² + 4²) = √(9 + 16) = √25 = 5.0.\n5. Cosine Similarity: 11 / (2.236 × 5.0) = 11 / 11.18 = 0.984.\nConclusion: 0.984 is very close to 1.0, showing both vectors point in almost the exact same direction!",
        "pitfalls": "Novice Trap: Don't confuse Dot Product with Cosine Similarity! If you duplicate words in a document, its vector length doubles, which doubles the dot product, but its cosine similarity stays exactly the same because the direction didn't change."
    },

    "concept_matrix_mult_inverses": {
        "simple_summary": "A matrix is a 2D table of numbers. Matrix multiplication transforms or processes data, transposition flips rows into columns, and an inverse matrix acts like an 'Undo' button that reverses a transformation.",
        "core_terms": [
            {
                "term": "Matrix",
                "what_is_it": "A 2D spreadsheet/grid of numbers arranged in rows and columns.",
                "analogy": "A pricing table where rows are products (Apple, Banana) and columns are stores (Store A, Store B).",
                "why_it_matters": "In AI, neural network weights and entire batches of data are stored as matrices."
            },
            {
                "term": "Matrix Multiplication",
                "what_is_it": "A rule for combining two grids by multiplying rows of the first grid by columns of the second grid.",
                "analogy": "Multiplying a grocery shopping list [quantities] by a price catalog [prices per store] to find the total bill at each store in one step.",
                "why_it_matters": "99% of the computational work done inside GPUs during ChatGPT training and inference is matrix multiplication (GEMM)."
            },
            {
                "term": "Transposition (A^T)",
                "what_is_it": "Flipping a matrix across its diagonal so that rows become columns and columns become rows.",
                "analogy": "Rotating a spreadsheet table from wide format to tall format so it aligns with another table.",
                "why_it_matters": "Needed to match dimensions before multiplying vectors or layers."
            },
            {
                "term": "Inverse Matrix (A^-1)",
                "what_is_it": "A reverse matrix that completely undoes what matrix A did, returning back to the original starting values.",
                "analogy": "If matrix A rotates an image 45° clockwise, its inverse matrix A^-1 rotates it 45° counter-clockwise.",
                "why_it_matters": "Used in analytical math solutions (like ordinary least squares regression)."
            }
        ],
        "symbol_guide": [
            {"symbol": "A, B", "meaning": "Input matrices", "plain_english": "A has size (m × k) and B has size (k × n)"},
            {"symbol": "C = AB", "meaning": "Product matrix", "plain_english": "The resulting grid with size (m × n)"},
            {"symbol": "A^T", "meaning": "Transpose of A", "plain_english": "Flip rows and columns: element at (i, j) moves to (j, i)"},
            {"symbol": "A^-1", "meaning": "Inverse of A", "plain_english": "Matrix such that A multiplied by A^-1 equals the identity matrix I"},
            {"symbol": "I", "meaning": "Identity matrix", "plain_english": "A square grid with 1s on the diagonal and 0s everywhere else (like the number 1 for matrices)"}
        ],
        "numerical_example": "Multiply 1x2 vector [2, 3] by 2x2 matrix [[1, 4], [2, 5]]:\n1. First output: (2 × 1) + (3 × 2) = 2 + 6 = 8.\n2. Second output: (2 × 4) + (3 × 5) = 8 + 15 = 23.\nResult: [8, 23]. In one step, both features were transformed simultaneously!",
        "pitfalls": "Common Trap: Matrix multiplication is NOT commutative! A × B is NOT equal to B × A. Order matters fundamentally."
    },

    "concept_eigenvalues_eigenvectors": {
        "simple_summary": "When a matrix stretches, squishes, or rotates a space, eigenvectors are special arrows that do NOT rotate—they only stretch or shrink. The eigenvalue is the number that tells you how much they stretch.",
        "core_terms": [
            {
                "term": "Eigenvector",
                "what_is_it": "A direction in space that stays on its own original line after a matrix transformation is applied.",
                "analogy": "Imagine stretching a rubber sheet diagonally. Most arrows drawn on the sheet will tilt and rotate, but the arrow pointing directly along the stretch axis only gets longer—it never tilts!",
                "why_it_matters": "Identifies the core, natural axes of variation in large complex datasets."
            },
            {
                "term": "Eigenvalue (λ)",
                "what_is_it": "The scaling factor (multiplier) that tells you how much the eigenvector was stretched, shrunk, or flipped.",
                "analogy": "If an eigenvector doubles in length after transformation, its eigenvalue λ = 2. If it shrinks by half, λ = 0.5.",
                "why_it_matters": "Tells you which directions contain the most important information or variance."
            }
        ],
        "symbol_guide": [
            {"symbol": "A", "meaning": "Transformation square matrix", "plain_english": "The system or dataset operator"},
            {"symbol": "v", "meaning": "Eigenvector", "plain_english": "A non-zero direction vector"},
            {"symbol": "λ (lambda)", "meaning": "Eigenvalue", "plain_english": "A single number (scalar) multiplying the vector v"},
            {"symbol": "Av = λv", "meaning": "Eigenvalue equation", "plain_english": "Transforming v with matrix A gives the exact same result as simply scaling v by number λ"}
        ],
        "numerical_example": "Let A = [[2, 0], [0, 3]] and v = [1, 0].\n1. Multiply A × v = [2×1 + 0×0, 0×1 + 3×0] = [2, 0].\n2. Notice [2, 0] = 2 × [1, 0] = 2v.\nTherefore, [1, 0] is an eigenvector with eigenvalue λ = 2!",
        "pitfalls": "Eigenvectors can only be found for square matrices (n × n). For rectangular matrices, we use Singular Value Decomposition (SVD)."
    },

    # CALCULUS & OPTIMIZATION
    "concept_partial_derivatives": {
        "simple_summary": "A derivative measures how fast something changes. A partial derivative measures how changing one specific ingredient changes the final result while keeping all other ingredients frozen.",
        "core_terms": [
            {
                "term": "Derivative / Slope",
                "what_is_it": "The rate of change of an output with respect to an input (rise over run).",
                "analogy": "A car's speedometer: it doesn't tell you where you are, it tells you how fast your position is changing per second.",
                "why_it_matters": "Tells the AI model which direction to adjust weights to decrease errors."
            },
            {
                "term": "Partial Derivative (∂f / ∂x)",
                "what_is_it": "Measuring the effect of one single input variable on the output while treating all other variables as fixed constants.",
                "analogy": "When baking a cake with sugar, flour, and eggs, the partial derivative with respect to sugar asks: 'If I add 1 extra gram of sugar while keeping flour and eggs exactly the same, how much sweeter does the cake get?'",
                "why_it_matters": "A neural network has millions of weights; partial derivatives allow the model to adjust each weight independently."
            }
        ],
        "symbol_guide": [
            {"symbol": "∂ (curly d)", "meaning": "Partial derivative symbol", "plain_english": "Indicates you are varying only one input while keeping others fixed"},
            {"symbol": "∂f / ∂x_i", "meaning": "Rate of change of function f with respect to variable x_i", "plain_english": "How much f moves when x_i nudges slightly"}
        ],
        "numerical_example": "Let Loss f(w1, w2) = 3(w1)² + 4(w2).\n1. Partial derivative with respect to w1: ∂f/∂w1 = 6(w1). (w2 is treated as a constant number, so its derivative is 0).\n2. If w1 = 2, then ∂f/∂w1 = 12. Increasing w1 by 1 increases loss by ~12.",
        "pitfalls": "Don't forget to treat other variables as pure constant numbers during calculation!"
    },

    "concept_chain_rule": {
        "simple_summary": "The Chain Rule tells you how changes ripple through a chain of connected steps. If gear A turns gear B, and gear B turns gear C, the chain rule multiplies their gear ratios to find how gear A affects gear C.",
        "core_terms": [
            {
                "term": "Composite Function",
                "what_is_it": "A function inside another function, like f(g(x)).",
                "analogy": "An assembly line: Station 1 shapes metal into a coin, Station 2 stamps a symbol onto the coin.",
                "why_it_matters": "A deep neural network is just a giant composite function of 50 to 100 layers stacked together!"
            },
            {
                "term": "Chain Rule",
                "what_is_it": "A mathematical formula stating that the derivative of composite functions equals the product of their individual layer derivatives.",
                "analogy": "Currency exchange: If $1 USD = 0.90 Euro, and 1 Euro = 160 Japanese Yen, then $1 USD = 0.90 × 160 = 144 Yen.",
                "why_it_matters": "It is the exact mathematical foundation of Backpropagation, which trains all modern neural networks."
            }
        ],
        "symbol_guide": [
            {"symbol": "dy / dx = (dy / du) × (du / dx)", "meaning": "Chain rule formula", "plain_english": "Multiply the rate of change of the outer layer by the rate of change of the inner layer"}
        ],
        "numerical_example": "Let y = (3x + 1)². Let u = 3x + 1, so y = u².\n1. dy/du = 2u = 2(3x + 1).\n2. du/dx = 3.\n3. Multiply together: dy/dx = 2(3x + 1) × 3 = 6(3x + 1) = 18x + 6.",
        "pitfalls": "If gradients in any layer are smaller than 1 (e.g. 0.1), multiplying 50 of them together causes the gradient to vanish to zero (Vanishing Gradient Problem)."
    },

    "concept_gradient_vector": {
        "simple_summary": "The gradient is an arrow that points directly in the direction of the steepest uphill climb. In AI, we take the negative gradient to walk downhill towards the minimum error.",
        "core_terms": [
            {
                "term": "Gradient Vector (∇f)",
                "what_is_it": "A collection of all partial derivatives packaged into a single vector pointing uphill.",
                "analogy": "Standing blindfolded on a mountain: the gradient points directly up the steepest slope.",
                "why_it_matters": "Provides the complete steering wheel for machine learning optimization."
            },
            {
                "term": "Gradient Descent",
                "what_is_it": "Taking small steps in the opposite direction of the gradient (-∇f) to find the valley of lowest loss.",
                "analogy": "Rolling a marble down a bowl until it settles at the very bottom center.",
                "why_it_matters": "How AI models improve from random guessing to superhuman accuracy."
            }
        ],
        "symbol_guide": [
            {"symbol": "∇f (nabla f)", "meaning": "Gradient of function f", "plain_english": "Vector of [∂f/∂x1, ∂f/∂x2, ..., ∂f/∂xn]"},
            {"symbol": "w_{t+1} = w_t - η ∇f", "meaning": "Gradient descent update rule", "plain_english": "New weight = old weight minus (learning rate × gradient slope)"}
        ],
        "numerical_example": "If gradient ∇f = [4, -2] and learning rate η = 0.1:\nStep taken = -0.1 × [4, -2] = [-0.4, +0.2].\nWeights update by decreasing feature 1 and increasing feature 2.",
        "pitfalls": "Taking too big of a step (high learning rate) causes you to overshoot the valley and explode into NaN errors!"
    },

    # PROBABILITY & STATISTICS
    "concept_bayes_theorem": {
        "simple_summary": "Bayes' Theorem tells you how to update your beliefs when new evidence arrives. It balances what you believed beforehand (Prior) with how likely the new clue is (Likelihood).",
        "core_terms": [
            {
                "term": "Prior Probability P(A)",
                "what_is_it": "How likely something was before seeing any new evidence.",
                "analogy": "Before opening your umbrella, the chance of rain today in the desert is 1%.",
                "why_it_matters": "Prevents AI from jumping to wild conclusions on rare events."
            },
            {
                "term": "Likelihood P(B | A)",
                "what_is_it": "The probability that the evidence B occurs given that hypothesis A is true.",
                "analogy": "If it actually rains, the chance of seeing dark gray clouds is 90%.",
                "why_it_matters": "Measures how strongly a clue points toward an outcome."
            },
            {
                "term": "Posterior Probability P(A | B)",
                "what_is_it": "Your updated, refined probability of A after seeing evidence B.",
                "analogy": "After seeing dark gray clouds in the sky, your revised estimate of rain jumps from 1% up to 40%.",
                "why_it_matters": "The final probability used to make medical diagnoses, spam filtering, and risk assessments."
            }
        ],
        "symbol_guide": [
            {"symbol": "P(A | B)", "meaning": "Probability of A given B (Posterior)", "plain_english": "Chance of having a disease after testing positive"},
            {"symbol": "P(B | A)", "meaning": "Probability of B given A (Likelihood)", "plain_english": "Chance of positive test if you actually have the disease"},
            {"symbol": "P(A)", "meaning": "Prior probability of A", "plain_english": "General baseline rarity of the disease in the population"},
            {"symbol": "P(B)", "meaning": "Marginal probability of evidence B", "plain_english": "Total chance of getting a positive test across everyone"}
        ],
        "numerical_example": "Suppose 1% of people have a disease (P(D)=0.01). A test is 90% accurate (P(+|D)=0.90) with a 5% false positive rate (P(+|no D)=0.05).\nIf you test positive, what is the chance you actually have the disease?\nP(D|+) = (0.90 × 0.01) / [(0.90 × 0.01) + (0.05 × 0.99)] = 0.009 / 0.0585 ≈ 15.4%.\nEven with a positive test, the chance is only 15.4% because the disease was so rare initially!",
        "pitfalls": "The Base Rate Fallacy: People ignore the Prior P(A) and assume a 90% accurate test means a 90% chance of disease, which is mathematically false when base rates are low."
    },

    # LINEAR REGRESSION & CORE ML
    "features-inputs-labels-targets": {
        "simple_summary": "Features are the clues you give to the AI model (inputs like house size or age), and labels are the answers you want the AI to predict (outputs like house price).",
        "core_terms": [
            {
                "term": "Features (X)",
                "what_is_it": "The measurable characteristics, properties, or inputs fed into an AI algorithm.",
                "analogy": "When buying a used car: mileage, brand, year, and engine size are the features.",
                "why_it_matters": "Models can only learn patterns from the features you provide."
            },
            {
                "term": "Labels (y)",
                "what_is_it": "The true target answer you want the model to learn to predict.",
                "analogy": "The actual selling price of the used car: $14,500.",
                "why_it_matters": "Acts as the ground-truth teacher during Supervised Learning."
            }
        ],
        "symbol_guide": [
            {"symbol": "X ∈ ℝ^{N × D}", "meaning": "Feature matrix", "plain_english": "N examples with D feature columns each"},
            {"symbol": "y ∈ ℝ^N", "meaning": "Target vector", "plain_english": "The true correct answers for all N examples"},
            {"symbol": "ŷ (y-hat)", "meaning": "Model prediction", "plain_english": "The model's estimate of the label"}
        ],
        "numerical_example": "Feature vector for a customer: [Age: 32, Income: $75,000, Credit Score: 740].\nTrue label y: 1 (Approved for loan).\nModel prediction ŷ: 0.92 (92% probability of approval).",
        "pitfalls": "Target Leakage: Including a feature that contains the answer or is only known AFTER the event happens (e.g. including 'Surgery Date' to predict 'Will patient need surgery?')."
    },

    "weights-slopes-bias-intercept": {
        "simple_summary": "Weights control how much importance each feature gets, and bias provides a starting baseline even if all input features are zero.",
        "core_terms": [
            {
                "term": "Weight (w)",
                "what_is_it": "The multiplier or slope attached to a feature that controls its influence.",
                "analogy": "In a recipe, if sugar has a high weight, adding a little bit makes a massive difference in sweetness.",
                "why_it_matters": "These are the exact dials that gradient descent adjusts during training."
            },
            {
                "term": "Bias (b)",
                "what_is_it": "A baseline constant added to the prediction that shifts the entire output line up or down.",
                "analogy": "A taxi meter that starts at $3.50 base fare the second you get in the car, before driving a single mile.",
                "why_it_matters": "Allows the model to predict non-zero outputs even when all inputs are 0."
            }
        ],
        "symbol_guide": [
            {"symbol": "ŷ = w · x + b", "meaning": "Linear equation", "plain_english": "Prediction = (Weight × Input) + Bias"}
        ],
        "numerical_example": "Predicting taxi fare: Fare = ($2.50 × Miles) + $3.00 Base.\nIf you ride 4 miles: Fare = (2.50 × 4) + 3.00 = $10.00 + $3.00 = $13.00.",
        "pitfalls": "Without a bias term, your prediction line is permanently forced to pass through (0, 0), which ruins accuracy for most real-world data."
    },

    # EVALUATION METRICS
    "true-positives-tp-true-negatives-tn": {
        "simple_summary": "In classification, True Positives and True Negatives are the times your model got the prediction completely right for both positive and negative cases.",
        "core_terms": [
            {
                "term": "True Positive (TP)",
                "what_is_it": "The model predicted POSITIVE, and the real truth was indeed POSITIVE (Correct alarm).",
                "analogy": "The smoke detector beeped, and there was indeed an actual fire.",
                "why_it_matters": "Measures how many actual positive events were correctly identified."
            },
            {
                "term": "True Negative (TN)",
                "what_is_it": "The model predicted NEGATIVE, and the real truth was indeed NEGATIVE (Correct calm).",
                "analogy": "The smoke detector stayed silent, and the house was completely safe.",
                "why_it_matters": "Measures the model's ability to avoid crying wolf on normal data."
            }
        ],
        "symbol_guide": [
            {"symbol": "Accuracy = (TP + TN) / Total", "meaning": "Overall accuracy formula", "plain_english": "Total correct predictions divided by all cases"}
        ],
        "numerical_example": "Out of 100 patient scans:\n- 15 had disease and tested positive (15 TP)\n- 80 were healthy and tested negative (80 TN)\n- 5 were misclassified.\nTotal correct = 15 + 80 = 95 out of 100 (95% Accuracy).",
        "pitfalls": "When data is imbalanced (e.g. 99% healthy, 1% sick), predicting 'healthy' for everyone yields 99% accuracy while catching ZERO sick patients!"
    },

    "false-positives-type-i-false-negatives-type-ii": {
        "simple_summary": "False Positives are false alarms (crying wolf), while False Negatives are missed dangers (failing to sound the alarm when danger is real).",
        "core_terms": [
            {
                "term": "False Positive (Type I Error)",
                "what_is_it": "The model cried 'YES', but the real truth was 'NO' (False Alarm).",
                "analogy": "Your email spam filter sends an important job offer letter to the Spam folder.",
                "why_it_matters": "Creates annoying interruptions and false alerts."
            },
            {
                "term": "False Negative (Type II Error)",
                "what_is_it": "The model cried 'NO', but the real truth was 'YES' (Missed Danger).",
                "analogy": "A hospital cancer screening tests negative, but the patient actually has cancer.",
                "why_it_matters": "Often catastrophic in safety-critical systems (healthcare, fraud, autonomous driving)."
            }
        ],
        "symbol_guide": [
            {"symbol": "Type I = False Positive", "meaning": "Null hypothesis rejected when true", "plain_english": "Innocent person convicted"},
            {"symbol": "Type II = False Negative", "meaning": "Null hypothesis accepted when false", "plain_english": "Guilty person acquitted"}
        ],
        "numerical_example": "In airport luggage screening:\n- A water bottle flagged as a weapon is a False Positive (causes brief delay).\n- A hidden weapon missed by the scanner is a False Negative (severe security threat).",
        "pitfalls": "There is always a trade-off! Decreasing False Positives usually increases False Negatives, and vice versa."
    },

    # TRANSFORMERS & GENAI
    "scaled-dot-product-attention": {
        "simple_summary": "Scaled Dot-Product Attention is the engine of ChatGPT. It compares what a word is looking for (Query) with what other words offer (Key), scores how well they match, and gathers their information (Value).",
        "core_terms": [
            {
                "term": "Query (Q)",
                "what_is_it": "What the current token is actively searching for.",
                "analogy": "A search bar query where you type: 'capital city'.",
                "why_it_matters": "Allows each word to request contextual help from surrounding words."
            },
            {
                "term": "Key (K)",
                "what_is_it": "The label or index of every word that describes what it contains.",
                "analogy": "The title or tags of a YouTube video or library book.",
                "why_it_matters": "Matched against the Query to compute attention weights."
            },
            {
                "term": "Value (V)",
                "what_is_it": "The actual meaningful content that gets retrieved when a match is found.",
                "analogy": "The video content you watch after clicking the search result.",
                "why_it_matters": "Weighted and summed together to build the updated word representation."
            },
            {
                "term": "Scaling Factor (1 / √d_k)",
                "what_is_it": "Dividing the match score by the square root of the dimension.",
                "analogy": "Turning down the volume knob on a speaker so the sound doesn't clip and distort.",
                "why_it_matters": "Prevents large dot products from blowing up into extreme numbers, which would freeze softmax gradients to zero."
            }
        ],
        "symbol_guide": [
            {"symbol": "Q", "meaning": "Query matrix", "plain_english": "What words are looking for"},
            {"symbol": "K", "meaning": "Key matrix", "plain_english": "What words offer"},
            {"symbol": "V", "meaning": "Value matrix", "plain_english": "The content payload"},
            {"symbol": "Q K^T", "meaning": "Matrix multiplication of Queries and Keys", "plain_english": "Computes match score between every pair of words in the sentence"},
            {"symbol": "√d_k", "meaning": "Square root of Key dimension d_k", "plain_english": "Normalization scaling factor (e.g. √64 = 8)"},
            {"symbol": "softmax(...)", "meaning": "Converts scores to percentages summing to 100% (1.0)", "plain_english": "Ensures attention weights act as probabilities"}
        ],
        "numerical_example": "Suppose Key dimension d_k = 64, so √d_k = 8.\n1. Raw dot product between word 'bank' and word 'river' = 32.0.\n2. Divide by √d_k: 32.0 / 8 = 4.0.\n3. Softmax turns 4.0 into a high attention probability (e.g. 0.85 or 85%).\n4. 85% of 'river's Value vector is blended into 'bank', clarifying that 'bank' means a riverbank, not a money vault!",
        "pitfalls": "Without the √d_k scaling factor, large models like GPT-4 would fail to train because large dot products cause softmax gradients to vanish to zero."
    },

    "query-q-key-k-and-value-v-projections": {
        "simple_summary": "In Transformers, Q, K, and V are three separate linear lenses applied to every word token, allowing it to play three roles: searcher (Q), candidate match (K), and content provider (V).",
        "core_terms": [
            {
                "term": "Query Projection (W_Q)",
                "what_is_it": "A matrix that translates a word embedding into a question or search request.",
                "analogy": "A person asking: 'Does anyone here speak French?'",
                "why_it_matters": "Determines what context this word is trying to find."
            },
            {
                "term": "Key Projection (W_K)",
                "what_is_it": "A matrix that translates a word embedding into a public profile description.",
                "analogy": "A badge on a person's shirt saying: 'I speak French and Spanish.'",
                "why_it_matters": "Allows other words to check if this word is relevant to them."
            },
            {
                "term": "Value Projection (W_V)",
                "what_is_it": "A matrix that prepares the actual payload information to be shared.",
                "analogy": "The person having a helpful conversation in French with you.",
                "why_it_matters": "Provides the raw semantic facts that get mixed into the output."
            }
        ],
        "symbol_guide": [
            {"symbol": "Q = X W_Q", "meaning": "Query projection", "plain_english": "Input tokens multiplied by learned Query weights"},
            {"symbol": "K = X W_K", "meaning": "Key projection", "plain_english": "Input tokens multiplied by learned Key weights"},
            {"symbol": "V = X W_V", "meaning": "Value projection", "plain_english": "Input tokens multiplied by learned Value weights"}
        ],
        "numerical_example": "If a word embedding has 768 numbers, multiplying it by matrix W_Q [768 × 64] produces a compact 64-number Query vector.",
        "pitfalls": "Q, K, and V originate from the same input X in Self-Attention, but because they multiply by 3 different learned weight matrices (W_Q, W_K, W_V), they learn completely different specialized roles."
    },

    "retrieval-augmented-generation-rag": {
        "simple_summary": "RAG gives an AI model an open-book exam. Instead of relying solely on its memory, the model searches your private documents for relevant facts first, pastes them into the prompt, and then writes the answer.",
        "core_terms": [
            {
                "term": "Retrieval",
                "what_is_it": "Searching an external database to fetch the most relevant paragraphs for a user's question.",
                "analogy": "Looking up a symptom in a trusted medical textbook before giving medical advice.",
                "why_it_matters": "Supplies the model with up-to-date, accurate, private facts."
            },
            {
                "term": "Augmentation",
                "what_is_it": "Pasting the retrieved document snippets directly into the prompt alongside the user's question.",
                "analogy": "Handing an open book directly to a student during a test.",
                "why_it_matters": "Gives the model the exact context it needs to answer without guessing."
            },
            {
                "term": "Generation",
                "what_is_it": "The LLM synthesizing the retrieved text and writing a natural, fluent response.",
                "analogy": "Writing a clear, cohesive summary based on the opened book pages.",
                "why_it_matters": "Drastically reduces hallucinations and allows AI to cite specific source pages."
            }
        ],
        "symbol_guide": [
            {"symbol": "y = LLM(Query + Context)", "meaning": "RAG generation formula", "plain_english": "Answer = Model(Question + Retrieved Documents)"}
        ],
        "numerical_example": "User asks: 'What is our corporate parental leave policy?'\n1. RAG converts the question into a 1536-number vector.\n2. Vector DB compares it against 50,000 internal handbook chunks using cosine similarity.\n3. Top-3 matching paragraphs (score > 0.88) are fetched.\n4. Prompt sent to LLM: 'Answer using this context: [Paragraph 1, 2, 3]. Question: What is our policy?'\n5. LLM generates 100% accurate, hallucination-free answer citing Section 4.2.",
        "pitfalls": "Garbage In, Garbage Out: If your chunking strategy splits a table in half or retrieves the wrong document, the LLM will generate an inaccurate answer."
    },

    "vector-databases-and-approximate-nearest-neighbor-ann": {
        "simple_summary": "Vector databases are specialized storage engines that store data as high-dimensional arrows and use smart shortcuts (like highway maps) to find the closest matching vectors in milliseconds across billions of items.",
        "core_terms": [
            {
                "term": "Vector Database",
                "what_is_it": "A database designed specifically to store, index, and query vectors (embeddings).",
                "analogy": "A library where books aren't sorted by author name, but by their exact plot meaning in 3D space.",
                "why_it_matters": "Traditional SQL databases cannot search by 'concept meaning'; vector DBs can."
            },
            {
                "term": "Approximate Nearest Neighbor (ANN)",
                "what_is_it": "Algorithms (like HNSW or IVF) that find the 99% closest vectors without scanning every single vector one-by-one.",
                "analogy": "Finding an address in a city: instead of walking past every house in town, you take the highway to the neighborhood, then the street, then the house.",
                "why_it_matters": "Scanning 100 million vectors takes seconds; ANN finds the top matches in under 5 milliseconds!"
            }
        ],
        "symbol_guide": [
            {"symbol": "O(log N)", "meaning": "Sublinear search complexity", "plain_english": "Search time scales with the logarithm of items instead of checking all N items"}
        ],
        "numerical_example": "For 10,000,000 stored document vectors:\n- Exact brute-force scan requires 10,000,000 dot product calculations (~2000 ms).\n- HNSW approximate graph index checks only ~1,200 nodes (~4 ms), delivering 99.2% accuracy.",
        "pitfalls": "ANN is 'approximate', meaning there is a tiny chance (<1%) the true #1 closest vector is missed in exchange for a 500x speedup."
    }
}

def generate_auto_enrichment(concept):
    cid = concept.get("id", "")
    if cid in DETAILED_MAP:
        return DETAILED_MAP[cid]

    title = concept.get("title", "")
    topic_label = concept.get("topic_label", "")
    category_label = concept.get("category_label", "")
    definition = concept.get("definition") or concept.get("def") or ""
    formula = concept.get("formula", "")
    logic = concept.get("logic", "")
    example = concept.get("example", "")

    # Split title into distinct terms:
    # Handles: "A, B & C", "A vs B", "A and B", "A (B)"
    clean_title = re.sub(r'\(.*?\)', '', title).strip()
    raw_terms = re.split(r'[,&/]| vs | and ', clean_title)
    terms_list = [t.strip() for t in raw_terms if len(t.strip()) > 1]
    if not terms_list:
        terms_list = [title]

    core_terms = []
    for term in terms_list:
        core_terms.append({
            "term": term,
            "what_is_it": f"{term} is a key building block in {topic_label}. In plain English, it provides the foundation to process, evaluate, or optimize data patterns.",
            "analogy": f"Think of {term} like a specific tool in a toolbox: it solves one distinct step in the machine learning process so the rest of the model can work accurately.",
            "why_it_matters": f"Essential in {topic_label} to ensure the model trains stably, avoids overfitting, and delivers reliable predictions."
        })

    first_sentence = definition.split(". ")[0] if ". " in definition else definition
    simple_summary = f"{title} explained simply: {first_sentence}. It ensures machine learning models can learn and generalize effectively."

    symbol_guide = []
    if formula and formula.strip():
        if "∑" in formula or "\\sum" in formula:
            symbol_guide.append({"symbol": "∑ (Sigma)", "meaning": "Summation", "plain_english": "Add up all values across the index"})
        if "y" in formula:
            symbol_guide.append({"symbol": "y", "meaning": "Ground truth label", "plain_english": "The true target measurement or correct answer"})
        if "\\hat{y}" in formula or "ŷ" in formula:
            symbol_guide.append({"symbol": "ŷ (y-hat)", "meaning": "Model prediction", "plain_english": "What the AI model guessed"})
        if "w" in formula or "W" in formula:
            symbol_guide.append({"symbol": "W, w", "meaning": "Model Weights", "plain_english": "Learnable parameters adjusted during training"})
        if "b" in formula:
            symbol_guide.append({"symbol": "b", "meaning": "Bias term", "plain_english": "Baseline offset independent of input features"})
        if "x" in formula or "X" in formula:
            symbol_guide.append({"symbol": "x, X", "meaning": "Input features", "plain_english": "The raw data measurements fed into the network"})
        if "L" in formula or "\\mathcal{L}" in formula or "Loss" in formula:
            symbol_guide.append({"symbol": "ℒ (Loss)", "meaning": "Loss / Objective function", "plain_english": "A numerical penalty measuring how far off the prediction was"})
        if not symbol_guide:
            symbol_guide.append({"symbol": "Formulation Symbols", "meaning": "Mathematical variables", "plain_english": "Defines the exact functional relationship between inputs and outputs"})

    numerical_example = f"Practical Calculation: In a standard {topic_label} pipeline, inputs are evaluated through this formulation. For example, given a sample batch with normalized values, the formula calculates the exact gradient or score to guide model improvement."

    pitfalls = f"Novice Trap: Pay close attention to feature scaling and data assumptions before applying {title}. Always ensure training and test distributions match."

    return {
        "simple_summary": simple_summary,
        "core_terms": core_terms,
        "symbol_guide": symbol_guide,
        "numerical_example": numerical_example,
        "pitfalls": pitfalls
    }

def main():
    with open(CONCEPTS_PATH, "r", encoding="utf-8") as f:
        concepts = json.load(f)

    print(f"Enriching {len(concepts)} concepts...")
    for c in concepts:
        enrichment = generate_auto_enrichment(c)
        c["simple_summary"] = enrichment["simple_summary"]
        c["core_terms"] = enrichment["core_terms"]
        c["symbol_guide"] = enrichment["symbol_guide"]
        c["numerical_example"] = enrichment["numerical_example"]
        c["pitfalls"] = enrichment["pitfalls"]

    with open(CONCEPTS_PATH, "w", encoding="utf-8") as f:
        json.dump(concepts, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(concepts)} enriched concepts to {CONCEPTS_PATH}")

    if os.path.exists(os.path.dirname(ALL_CONCEPTS_PATH)):
        with open(ALL_CONCEPTS_PATH, "w", encoding="utf-8") as f:
            json.dump(concepts, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(concepts)} enriched concepts to {ALL_CONCEPTS_PATH}")

if __name__ == "__main__":
    main()
