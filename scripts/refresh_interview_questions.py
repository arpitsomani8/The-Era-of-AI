# -*- coding: utf-8 -*-
"""
Refresh Interview Questions Bank
Generates a comprehensive, curated question vault with:
1. 🌱 0-2 Years Experience (Freshers & Entry-Level): 100% NON-MATHEMATICAL, intuitive, real-world scenario questions.
2. 🚀 2-4 Years Experience (Mid-Level Engineers): Applied modeling, trade-offs, debugging, and metrics.
3. 🏛️ 5+ Years Experience (Senior & Staff / Architect): System design, distributed training, low-latency serving, and MLOps.
"""

import json
import os

INTERVIEW_PATH = os.path.join(os.path.dirname(__file__), "..", "src", "data", "interviewQuestions.json")

# Build the curated list of questions
def build_questions():
    questions = []

    # =========================================================================
    # 🌱 0–2 YEARS EXPERIENCE (FRESHERS, ENTRY-LEVEL, ENTRY-LEVEL)
    # 100% NON-MATHEMATICAL, CLEAR INTUITION, REAL-WORLD SCENARIOS
    # =========================================================================

    fresher_questions = [
        {
            "id": "fresher_01",
            "category": "ml",
            "category_label": "Classical Machine Learning",
            "experience_level": "0-2",
            "experience_label": "0–2 Yrs (Junior / Fresher)",
            "difficulty": "Junior / Fresher",
            "company_tags": ["Google", "Amazon", "Microsoft", "TCS", "Infosys"],
            "question": "What is the fundamental difference between Supervised Learning, Unsupervised Learning, and Reinforcement Learning?",
            "answer": "**Quick Answer:**\nThe key difference lies in the type of feedback the algorithm receives while learning.\n\n**1. Supervised Learning (Learning with a Teacher):**\n- The model is trained on labeled data where the correct answers are already known.\n- The model learns the mapping from inputs (features) to the correct output (label).\n- *Example:* Predicting house prices based on size and location, or classifying emails as Spam or Not Spam.\n\n**2. Unsupervised Learning (Learning without a Teacher):**\n- The data has no labels and no correct answers.\n- The model searches for natural patterns, groupings, or similarities on its own.\n- *Example:* Customer segmentation (grouping shoppers with similar buying habits) or topic clustering.\n\n**3. Reinforcement Learning (Learning through Trial & Error):**\n- An agent interacts with an environment and learns by receiving rewards for good moves and penalties for mistakes.\n- *Example:* Training an AI to play Chess, navigate a robotic vacuum, or park a self-driving car.",
            "tip": "In an interview, start with the 1-sentence distinction ('Supervised has correct answers, Unsupervised finds hidden patterns, Reinforcement learns from rewards and penalties') before giving an everyday example for each."
        },
        {
            "id": "fresher_02",
            "category": "ml",
            "category_label": "Classical Machine Learning",
            "experience_level": "0-2",
            "experience_label": "0–2 Yrs (Junior / Fresher)",
            "difficulty": "Junior / Fresher",
            "company_tags": ["Meta", "Amazon", "Google", "Flipkart"],
            "question": "What is the difference between Classification and Regression in machine learning? Give real-world examples of both.",
            "answer": "**Quick Answer:**\nClassification predicts a discrete category or class, whereas Regression predicts a continuous numerical quantity.\n\n**1. Classification (Categorical Output):**\n- The answer belongs to a specific group or label.\n- Binary Classification: Two possible outcomes (Yes/No, Spam/Not Spam, Fraud/Legitimate).\n- Multiclass Classification: More than two categories (Cat, Dog, or Bird; Low, Medium, or High risk).\n- *Example:* An algorithm that looks at a chest X-ray and predicts whether pneumonia is Present or Absent.\n\n**2. Regression (Continuous Numerical Output):**\n- The answer is an actual number on a continuous scale.\n- *Example:* Predicting tomorrow's temperature in degrees Celsius (e.g. 24.5°C), the sales revenue of a store next month ($120,500), or the price of a used car ($18,200).\n\n**Rule of Thumb:** If the question asks 'Which one is it?', it is classification. If the question asks 'How much or how many?', it is regression.",
            "tip": "Interviewers frequently ask trick questions like 'Is predicting credit score classification or regression?' (It's regression because the score is a continuous number, though it can be bucketed into risk tiers)."
        },
        {
            "id": "fresher_03",
            "category": "metrics_data",
            "category_label": "Metrics & Data",
            "experience_level": "0-2",
            "experience_label": "0–2 Yrs (Junior / Fresher)",
            "difficulty": "Junior / Fresher",
            "company_tags": ["Google", "Microsoft", "Uber", "Apple"],
            "question": "Why do we split data into Training, Validation, and Test sets? Why can't we just test on the training data?",
            "answer": "**Quick Answer:**\nTesting on training data is like giving a student the exact exam questions and answers to study, and then testing them on those identical questions. They will get 100%, but you have no idea if they truly understood the subject or simply memorized the answers.\n\n**The 3 Data Splits:**\n1. **Training Set (typically 70–80%):**\n   - Used directly by the model to adjust its weights and learn patterns.\n2. **Validation Set (typically 10–15%):**\n   - Used by the engineer to tune hyperparameters (like tree depth or learning rate) and choose the best model architecture.\n3. **Test Set (typically 10–15%):**\n   - Kept locked away in a 'vault' until the very end.\n   - Used strictly once to evaluate final, unbiased real-world generalization on completely unseen data.\n\n**The Danger:** If you evaluate on training data, an overfitted model will score 99% accuracy in your notebook but fail completely when real customers use it.",
            "tip": "Always mention that the Test set must never be used to make modeling choices or tune parameters; otherwise, you cause data snooping / test leakage."
        },
        {
            "id": "fresher_04",
            "category": "ml",
            "category_label": "Classical Machine Learning",
            "experience_level": "0-2",
            "experience_label": "0–2 Yrs (Junior / Fresher)",
            "difficulty": "Junior / Fresher",
            "company_tags": ["Amazon", "Google", "Meta", "Netflix"],
            "question": "What is Overfitting and Underfitting? How do you recognize and fix them in practice?",
            "answer": "**Quick Answer:**\n- **Overfitting** means the model memorized the training data (including its random noise) and fails on new data.\n- **Underfitting** means the model is too simple to capture even the basic patterns in the data.\n\n**1. Overfitting (High Variance):**\n- *Symptom:* 99% accuracy on Training data, but only 65% accuracy on Validation data.\n- *Analogy:* A student who memorized the exact numbers in textbook practice problems and fails when the exam changes the numbers.\n- *How to fix:* Collect more training data, remove noisy features, simplify the model (reduce tree depth), add Regularization (L1/L2), or use Dropout.\n\n**2. Underfitting (High Bias):**\n- *Symptom:* Poor accuracy on both Training data (60%) and Validation data (58%).\n- *Analogy:* Trying to predict stock market trends using only a straight ruler.\n- *How to fix:* Use a more powerful model (e.g. Random Forest instead of simple linear regression), add more informative features (feature engineering), or train for more epochs.",
            "tip": "Interviewers love the 'Gap' diagnostic: if Training score is high and Validation score is low, the gap indicates overfitting!"
        },
        {
            "id": "fresher_05",
            "category": "metrics_data",
            "category_label": "Metrics & Data",
            "experience_level": "0-2",
            "experience_label": "0–2 Yrs (Junior / Fresher)",
            "difficulty": "Junior / Fresher",
            "company_tags": ["Google", "Meta", "Healthcare Startups", "Stripe"],
            "question": "What is the difference between Precision and Recall? In what real-world scenarios is Recall more important than Precision?",
            "answer": "**Quick Answer:**\n- **Precision** answers: *'Out of all instances the model predicted as positive, how many were actually positive?'*\n- **Recall** answers: *'Out of all actual positive instances in the real world, how many did the model successfully catch?'*\n\n**Real-World Scenario: Cancer Detection (Recall is Critical):**\n- A False Negative means a patient with cancer is told they are healthy. They go home untreated, and the disease progresses fatally.\n- A False Positive means a healthy patient is flagged for a follow-up biopsy. It causes anxiety and an extra test, but does not cost a life.\n- In medical diagnostics, we prioritize **Recall** (catching 99%+ of true cancer cases), even if precision drops slightly.\n\n**Real-World Scenario: Spam Filtering (Precision is Critical):**\n- A False Positive means an important job offer email is sent directly to the Spam folder and you miss it.\n- A False Negative means an occasional spam newsletter slips into your inbox (mild annoyance).\n- For email spam, we prioritize **Precision** (ensuring emails flagged as spam are definitely spam).",
            "tip": "Remember this simple mnemonic: High Recall = 'Cast a wide net, miss nothing'. High Precision = 'Be very selective, only fire when 100% sure'."
        },
        {
            "id": "fresher_06",
            "category": "metrics_data",
            "category_label": "Metrics & Data",
            "experience_level": "0-2",
            "experience_label": "0–2 Yrs (Junior / Fresher)",
            "difficulty": "Junior / Fresher",
            "company_tags": ["Amazon", "Microsoft", "Uber"],
            "question": "What is a Confusion Matrix, and what do True Positive, False Positive, True Negative, and False Negative mean?",
            "answer": "**Quick Answer:**\nA Confusion Matrix is a 2x2 table that summarizes the prediction outcomes of a classification model against actual ground truth.\n\n**The 4 Core Quadrants (Using Disease Detection as an example):**\n1. **True Positive (TP) - Correctly Caught:**\n   - The patient actually has the disease, and the model correctly predicts 'Positive'.\n2. **True Negative (TN) - Correctly Cleared:**\n   - The patient is healthy, and the model correctly predicts 'Negative'.\n3. **False Positive (FP) - False Alarm (Type I Error):**\n   - The patient is healthy, but the model incorrectly predicts 'Positive'.\n4. **False Negative (FN) - Missed Case (Type II Error):**\n   - The patient actually has the disease, but the model incorrectly predicts 'Negative'.\n\n**Key Formulas in Plain English:**\n- **Accuracy:** (TP + TN) / Total (Overall correct percentage).\n- **Precision:** TP / (TP + FP) (Quality of positive claims).\n- **Recall:** TP / (TP + FN) (Coverage of real positive cases).",
            "tip": "If asked about Type I vs Type II errors: Type I is False Positive (a false alarm); Type II is False Negative (a missed danger)."
        },
        {
            "id": "fresher_07",
            "category": "genai_llm",
            "category_label": "GenAI & LLMs",
            "experience_level": "0-2",
            "experience_label": "0–2 Yrs (Junior / Fresher)",
            "difficulty": "Junior / Fresher",
            "company_tags": ["OpenAI", "Google", "Microsoft", "Anthropic"],
            "question": "What is an 'Embedding' or 'Vector' in modern AI in simple terms? Why are they so important?",
            "answer": "**Quick Answer:**\nComputers cannot understand the meaning of words, images, or audio directly; they only understand numbers. An **embedding** is a list of numbers (a vector) that captures the underlying semantic meaning of a piece of data.\n\n**Everyday Analogy:**\nImagine describing a house using 3 numbers: `[Bedrooms, Bathrooms, Price in thousands]`. A 3-bedroom, 2-bath house for $350k is vector `[3, 2, 350]`. A similar house has vector `[3, 2, 360]`.\nBecause the numbers are close, a computer knows the two houses are similar.\n\n**Why Embeddings are Revolutionary:**\n- In language models, text is converted into vectors of ~1,536 numbers.\n- Words or sentences with similar meanings end up close together in geometric space.\n- *Example:* The vector for 'Apple' will be close to 'Banana' (both are fruits). In a financial context, 'Apple' will be close to 'Microsoft' (both are tech companies).\n- Embeddings power Google Search, Spotify song recommendations, and Vector Databases in RAG.",
            "tip": "Highlight that embeddings allow computers to calculate mathematical distance between concepts (e.g., using Cosine Similarity)."
        },
        {
            "id": "fresher_08",
            "category": "genai_llm",
            "category_label": "GenAI & LLMs",
            "experience_level": "0-2",
            "experience_label": "0–2 Yrs (Junior / Fresher)",
            "difficulty": "Junior / Fresher",
            "company_tags": ["OpenAI", "Meta", "Google"],
            "question": "What is a 'Token' in Large Language Models like ChatGPT, and why do models count tokens instead of words?",
            "answer": "**Quick Answer:**\nA token is the atomic piece of text processed by language models. A token can be a whole word, part of a word (subword), a punctuation mark, or a single letter.\n\n**Why Tokens Instead of Words?**\n1. **Handling Unknown Words:** If models only used full words, encountering a novel slang word or typo would crash the system. With tokens, rare words are broken into known syllables (e.g. 'unbelievable' becomes `un` + `believ` + `able`).\n2. **Multilingual Efficiency:** Different languages share common subwords and root fragments.\n3. **Code & Punctuation:** Spaces, tabs, and syntax brackets (like `{}` and `[]`) can be single tokens.\n\n**Rule of Thumb for English:**\n- 1 token is roughly 0.75 words (or ~4 characters).\n- 100 tokens ≈ 75 English words.\n- A standard 1,000-word essay requires roughly ~1,330 tokens.",
            "tip": "Explain that APIs (like OpenAI and Anthropic) bill users per million input and output tokens because GPU memory is allocated per token processed."
        },
        {
            "id": "fresher_09",
            "category": "genai_llm",
            "category_label": "GenAI & LLMs",
            "experience_level": "0-2",
            "experience_label": "0–2 Yrs (Junior / Fresher)",
            "difficulty": "Junior / Fresher",
            "company_tags": ["Google", "Microsoft", "Amazon", "Salesforce"],
            "question": "What is Prompt Engineering? Explain the difference between Zero-Shot, One-Shot, and Few-Shot Prompting.",
            "answer": "**Quick Answer:**\nPrompt Engineering is the practice of crafting and structuring inputs to get the most accurate, reliable, and formatted responses from a Large Language Model without changing its weights.\n\n**1. Zero-Shot Prompting (No Examples):**\n- You give a direct command without providing any sample demonstrations.\n- *Example:* 'Classify the sentiment of this review: \"The screen was cracked on arrival.\"'\n- Relies entirely on what the model already knows.\n\n**2. One-Shot Prompting (One Example):**\n- You provide exactly one example of the desired input and output format before asking your question.\n- *Example:*\n  Review: 'Loved the camera!' -> Sentiment: Positive\n  Review: 'Battery died after 10 minutes.' -> Sentiment: [Model responds 'Negative']\n\n**3. Few-Shot Prompting (Multiple Examples):**\n- You provide 3 to 5 examples showing the exact style, reasoning, or JSON schema you want.\n- Dramatically reduces hallucinations and enforces strict output formats without any coding.",
            "tip": "Mention 'Chain-of-Thought' prompting ('Think step-by-step') as another powerful technique that tells the model to write out intermediate logic before concluding."
        },
        {
            "id": "fresher_10",
            "category": "rag",
            "category_label": "RAG & Vector DB",
            "experience_level": "0-2",
            "experience_label": "0–2 Yrs (Junior / Fresher)",
            "difficulty": "Junior / Fresher",
            "company_tags": ["OpenAI", "Databricks", "Snowflake", "AWS"],
            "question": "What is Retrieval-Augmented Generation (RAG) in simple terms? What problem does it solve?",
            "answer": "**Quick Answer:**\nRAG is like giving an AI model an open-book reference manual right before it answers a question.\n\n**The Problem It Solves:**\n1. **Knowledge Cutoff:** An LLM only knows information up to the day it was trained. It does not know yesterday's news.\n2. **Private Data:** An LLM does not know your company's internal PDFs, HR policies, or customer records.\n3. **Hallucinations:** When an LLM doesn't know a fact, it often invents a convincing lie.\n\n**How RAG Works in 3 Steps:**\n1. **Retrieve:** When a user asks a question, the system searches a Vector Database of private company documents and pulls the top 3 most relevant paragraphs.\n2. **Augment:** The system pastes those 3 paragraphs into the prompt alongside the user's question: *'Answer the question using ONLY the provided text below.'*\n3. **Generate:** The LLM reads the verified facts and generates an accurate, cited answer.\n\n**Benefit:** Zero expensive model retraining required; documents can be updated in real time in the database.",
            "tip": "Use the 'open-book exam' analogy! It explains RAG to any non-technical interviewer immediately."
        },
        {
            "id": "fresher_11",
            "category": "genai_llm",
            "category_label": "GenAI & LLMs",
            "experience_level": "0-2",
            "experience_label": "0–2 Yrs (Junior / Fresher)",
            "difficulty": "Junior / Fresher",
            "company_tags": ["Google", "Meta", "Anthropic"],
            "question": "What is an AI Hallucination? Why do LLMs hallucinate, and how can we prevent it?",
            "answer": "**Quick Answer:**\nA hallucination occurs when an AI generates statements that sound completely confident and grammatically fluent, but are factually fabricated or non-existent.\n\n**Why Do LLMs Hallucinate?**\n- LLMs are statistical next-token prediction machines, not knowledge search engines.\n- They are trained to predict: *'What is the most linguistically plausible next word?'*, not *'Is this statement verifiably true?'*.\n- If a model encounters a topic with sparse training data, it strings together plausible-sounding sentences that have no basis in reality.\n\n**How to Prevent Hallucinations in Production:**\n1. **Use RAG (Retrieval-Augmented Generation):** Force the model to ground its response in retrieved private documents.\n2. **Lower the Temperature:** Set temperature to 0.0 or 0.2 to make responses deterministic and focused.\n3. **Explicit Guardrail Prompts:** Add instructions like: *'If you do not know the answer based on the context, state \"I do not know\". Do not speculate.'*\n4. **Structured Output Verification:** Validate citations and facts against an external database.",
            "tip": "Mention the famous legal case where a lawyer used ChatGPT and submitted fake court case citations to a federal judge as a warning story."
        },
        {
            "id": "fresher_12",
            "category": "metrics_data",
            "category_label": "Metrics & Data",
            "experience_level": "0-2",
            "experience_label": "0–2 Yrs (Junior / Fresher)",
            "difficulty": "Junior / Fresher",
            "company_tags": ["Amazon", "Google", "Stripe", "Kaggle"],
            "question": "What is Data Leakage in Machine Learning? Give an example of how it can happen accidentally.",
            "answer": "**Quick Answer:**\nData Leakage occurs when information from outside the training dataset (usually from the test set or from the future) is accidentally introduced during model training, giving deceptively high training scores that fail in production.\n\n**Common Real-World Examples:**\n1. **Pre-processing before splitting (The Beginner Mistake):**\n   - Normalizing features (calculating mean and standard deviation) on the entire dataset *before* creating train and test splits.\n   - *Result:* The training set already 'knows' the mean of the test set.\n2. **Target Leakage (Peeking at the Future):**\n   - Building a model to predict whether a hospital patient has pneumonia, and including a feature called 'Pneumonia Medicine Prescribed'.\n   - At training time, the model achieves 100% accuracy. But in production, you want to predict pneumonia *before* the doctor prescribes medicine!\n\n**How to Prevent It:**\n- Always split data into Train and Test sets *first* before doing any scaling, imputation, or feature engineering.\n- Verify that every feature in your dataset would realistically be available at the exact second the prediction is made.",
            "tip": "State clearly: 'Fit your preprocessing scalers ONLY on training data; only transform the test data'."
        },
        {
            "id": "fresher_13",
            "category": "ml",
            "category_label": "Classical Machine Learning",
            "experience_level": "0-2",
            "experience_label": "0–2 Yrs (Junior / Fresher)",
            "difficulty": "Junior / Fresher",
            "company_tags": ["Microsoft", "Google", "Amazon"],
            "question": "What is Gradient Descent in simple terms? Explain the intuition of Learning Rate.",
            "answer": "**Quick Answer:**\nGradient Descent is an optimization algorithm used to train machine learning models by iteratively adjusting their weights to minimize errors (loss).\n\n**The Foggy Mountain Analogy:**\n- Imagine you are blindfolded on a foggy mountain and your goal is to reach the lowest valley (minimum error).\n- You cannot see the bottom, but you can feel the slope of the ground under your shoes.\n- You take a step in the direction where the ground slopes downward most steeply.\n- You repeat this step after step until the ground is flat under your feet (you reached the minimum).\n\n**The Learning Rate (Step Size):**\n- **Learning Rate Too High (Giant Steps):** You take huge leaps. You might jump right over the valley and end up higher on the opposite mountain (training diverges or oscillates wildly).\n- **Learning Rate Too Low (Tiny Baby Steps):** You take steps of 1 millimeter. It will take you 10 years to reach the bottom (training takes forever and might get stuck in a tiny dip).\n- **Optimal Learning Rate:** Moderately sized steps that consistently guide you downhill to the lowest point efficiently.",
            "tip": "Use the Google ML Crash Course analogy of the hiker on a foggy mountain; interviewers love visual, intuitive explanations."
        },
        {
            "id": "fresher_14",
            "category": "metrics_data",
            "category_label": "Metrics & Data",
            "experience_level": "0-2",
            "experience_label": "0–2 Yrs (Junior / Fresher)",
            "difficulty": "Junior / Fresher",
            "company_tags": ["Uber", "Lyft", "Flipkart", "Capital One"],
            "question": "What is Feature Scaling (Normalization vs Standardization), and why is it necessary for certain algorithms?",
            "answer": "**Quick Answer:**\nFeature scaling puts different numerical features onto a similar scale so that features with large raw numbers don't unfairly dominate features with small numbers.\n\n**Why It Is Necessary:**\nImagine predicting house prices using two features:\n- Feature 1: Number of Bedrooms (ranges from 1 to 5).\n- Feature 2: Square Footage (ranges from 500 to 5,000).\nAlgorithms that calculate distance (like KNN, K-Means) or gradient updates will treat a change of 100 sqft as 100x more important than an extra bedroom, simply because the raw numbers are bigger!\n\n**Two Common Techniques:**\n1. **Min-Max Normalization:** Scales numbers into a fixed range from 0 to 1.\n   - Formula intuition: `(Value - Min) / (Max - Min)`.\n   - Best when data has a bounded range and no extreme outliers.\n2. **Standardization (Z-Score):** Centers data around a mean of 0 with a standard deviation of 1.\n   - Formula intuition: `(Value - Mean) / StdDev`.\n   - Much more robust to extreme outliers.\n\n**Algorithms that Require Scaling:** Gradient Descent, KNN, SVM, Logistic Regression, Neural Networks. (Decision Trees and Random Forests do *not* require scaling).",
            "tip": "Always mention that Tree-based algorithms (Random Forest, XGBoost) are scale-invariant because they split on single features independently."
        },
        {
            "id": "fresher_15",
            "category": "ml",
            "category_label": "Classical Machine Learning",
            "experience_level": "0-2",
            "experience_label": "0–2 Yrs (Junior / Fresher)",
            "difficulty": "Junior / Fresher",
            "company_tags": ["Walmart", "Target", "Amazon"],
            "question": "How do Decision Trees work, and why do Random Forests usually perform better than a single Decision Tree?",
            "answer": "**Quick Answer:**\nA Decision Tree makes predictions by asking a series of sequential Yes/No questions. A Random Forest combines the predictions of hundreds of different trees to make a collective, highly accurate decision.\n\n**1. Decision Tree:**\n- Like a flowchart: *'Is income > $50k?'* -> If Yes, *'Is credit score > 700?'* -> If Yes, approve loan.\n- **Problem:** Single decision trees easily overfit. If a tree grows too deep, it creates hyper-specific branches that memorize the training data.\n\n**2. Random Forest (Wisdom of the Crowd):**\n- An ensemble of hundreds of decision trees trained on random subsets of data and random subsets of features.\n- Each individual tree makes its own prediction.\n- For classification, the forest takes the majority vote. For regression, it averages the predictions.\n- **Why it performs better:** While individual trees might make random errors, their errors cancel each other out when averaged together, reducing variance without increasing bias.",
            "tip": "Explain the concept of 'Wisdom of the Crowds': guessing the weight of an ox at a county fair is more accurate when 500 people average their guesses than asking a single expert."
        },
        {
            "id": "fresher_16",
            "category": "dl",
            "category_label": "Deep Learning",
            "experience_level": "0-2",
            "experience_label": "0–2 Yrs (Junior / Fresher)",
            "difficulty": "Junior / Fresher",
            "company_tags": ["NVIDIA", "Google", "Tesla"],
            "question": "Why do Deep Learning models train on GPUs (Graphics Processing Units) instead of standard CPUs?",
            "answer": "**Quick Answer:**\nCPUs are designed to do a few complex tasks sequentially, whereas GPUs are designed to do thousands of simple mathematical operations (matrix additions and multiplications) simultaneously in parallel.\n\n**The Chef vs Assembly Line Analogy:**\n- **CPU (Master Chef):** Highly skilled, can cook complex 5-star recipes, but works on 4 to 16 tasks at a time.\n- **GPU (Army of 5,000 Kitchen Assistants):** Each assistant can only do one simple task (like chopping an onion or peeling a potato), but 5,000 of them work at the exact same instant.\n\n**Why Neural Networks Need GPUs:**\n- Training a neural network requires multiplying massive grids of numbers (matrices) millions of times.\n- Each multiplication is independent of the others.\n- A GPU with 10,000 CUDA cores can compute all these multiplications in one single clock cycle, speeding up training by 50x to 100x compared to a multi-core CPU.",
            "tip": "State that GPU parallelism is the primary hardware catalyst that enabled the modern Deep Learning and Generative AI boom."
        },
        {
            "id": "fresher_17",
            "category": "dl",
            "category_label": "Deep Learning",
            "experience_level": "0-2",
            "experience_label": "0–2 Yrs (Junior / Fresher)",
            "difficulty": "Junior / Fresher",
            "company_tags": ["Google", "Meta", "Apple"],
            "question": "What is an Activation Function in Neural Networks? Why can't we just use linear layers without them?",
            "answer": "**Quick Answer:**\nAn activation function decides whether an artificial neuron should 'fire' and introduces non-linearity into the network.\n\n**Why Non-Linearity is Essential:**\n- In math, if you multiply a number by 2, and then multiply by 3, it is the same as multiplying by 6 in one step: `Linear(Linear(x)) = Linear(x)`.\n- Without non-linear activation functions, a 100-layer deep neural network collapses mathematically into a single linear regression equation!\n- The real world is non-linear (curved, complex, multidimensional). Activation functions allow neural networks to bend, fold, and twist coordinate space to learn complex shapes.\n\n**Common Activation Functions in Practice:**\n1. **ReLU (Rectified Linear Unit):** `f(x) = max(0, x)`. If positive, pass through; if negative, output zero. Fast and widely used.\n2. **Sigmoid:** Squashes numbers into a 0 to 1 range (useful for probabilities).\n3. **GELU:** Smooth variation of ReLU used in modern Transformers (GPT, BERT).",
            "tip": "State clearly: 'Without activation functions, stacking 100 layers is mathematically identical to a single-layer model'."
        },
        {
            "id": "fresher_18",
            "category": "metrics_data",
            "category_label": "Metrics & Data",
            "experience_level": "0-2",
            "experience_label": "0–2 Yrs (Junior / Fresher)",
            "difficulty": "Junior / Fresher",
            "company_tags": ["Amazon", "Uber", "Intuit"],
            "question": "How do you handle Missing Values in a dataset? What are the tradeoffs of dropping vs imputing?",
            "answer": "**Quick Answer:**\nYou can either drop the missing rows/columns or fill them in (imputation). The right choice depends on the percentage of missing data and whether the data is missing at random.\n\n**1. Dropping Missing Data:**\n- **Drop Columns:** If a column is missing >60% of its values and is not critical, drop the feature.\n- **Drop Rows:** If only 1% of rows have missing values, dropping them is quick and safe.\n- *Tradeoff:* Easy, but wastes data and can introduce severe selection bias if missingness is non-random.\n\n**2. Imputing (Filling in Values):**\n- **Numerical Features:** Fill with the **Median** (safer than Mean because median is resistant to outliers) or Mean.\n- **Categorical Features:** Fill with the **Mode** (most frequent category) or create a new category called `'Unknown'`.\n- **Advanced:** Use KNN Imputation or model-based prediction to estimate missing values based on similar rows.\n\n**Best Practice:** Always create a binary indicator column `feature_is_missing` (0 or 1). Often, the fact that a user did not provide an answer is a predictive signal in itself!",
            "tip": "Always mention checking whether data is Missing Completely at Random (MCAR) or Missing Not at Random (MNAR)."
        },
        {
            "id": "fresher_19",
            "category": "metrics_data",
            "category_label": "Metrics & Data",
            "experience_level": "0-2",
            "experience_label": "0–2 Yrs (Junior / Fresher)",
            "difficulty": "Junior / Fresher",
            "company_tags": ["Stripe", "PayPal", "American Express"],
            "question": "What is Class Imbalance (e.g. 99% legitimate, 1% fraud), and why is standard Accuracy misleading on imbalanced datasets?",
            "answer": "**Quick Answer:**\nClass Imbalance occurs when one class dramatically outnumbers the other. Standard accuracy is completely useless on imbalanced data because a dumb model that predicts 'No Fraud' 100% of the time achieves 99% accuracy while catching zero fraud!\n\n**The 99% Fraud Trap:**\n- If you have 10,000 credit card transactions and only 50 are fraudulent (0.5%).\n- A model that automatically outputs 'Legitimate' for every single transaction gets **99.5% accuracy**.\n- But your business loses millions of dollars because literally every fraudulent charge succeeded!\n\n**How to Handle Class Imbalance:**\n1. **Stop using Accuracy:** Use **PR-AUC (Precision-Recall AUC)**, F1-Score, or Recall.\n2. **Resampling:**\n   - Oversample the minority class (e.g. using SMOTE to generate synthetic fraud examples).\n   - Undersample the majority class.\n3. **Class Weights:** Tell the loss function that missing a fraud case costs 100x more than misclassifying a legitimate transaction.",
            "tip": "State: 'Never use accuracy on imbalanced datasets; always evaluate Precision, Recall, and PR-AUC'."
        },
        {
            "id": "fresher_20",
            "category": "ml",
            "category_label": "Classical Machine Learning",
            "experience_level": "0-2",
            "experience_label": "0–2 Yrs (Junior / Fresher)",
            "difficulty": "Junior / Fresher",
            "company_tags": ["Google", "Meta", "Microsoft"],
            "question": "What is the difference between a Model Parameter and a Hyperparameter?",
            "answer": "**Quick Answer:**\n- **Parameters** are learned automatically by the model from the training data.\n- **Hyperparameters** are external settings chosen manually by the machine learning engineer before training begins.\n\n**Comparison Table:**\n- **Parameters (Internal & Learned):**\n  - Weights ($w$) and biases ($b$) in a neural network.\n  - Split criteria and thresholds in a decision tree.\n  - The model adjusts these automatically using optimization algorithms like Gradient Descent.\n\n- **Hyperparameters (External & Configured):**\n  - Learning rate (e.g. 0.001).\n  - Number of epochs (e.g. 50).\n  - Batch size (e.g. 32).\n  - Maximum tree depth in Random Forest (e.g. 10).\n  - Number of hidden layers in a neural network.\n\n**Analogy:** Tuning a racecar. The tire pressure, gear ratio, and fuel mix chosen by the mechanic before the race are *hyperparameters*. The speed, engine temperature, and RPM reached on the track are *parameters*.",
            "tip": "Explain that hyperparameter tuning uses techniques like Grid Search, Random Search, or Bayesian Optimization (Optuna)."
        },
        {
            "id": "fresher_21",
            "category": "dl",
            "category_label": "Deep Learning",
            "experience_level": "0-2",
            "experience_label": "0–2 Yrs (Junior / Fresher)",
            "difficulty": "Junior / Fresher",
            "company_tags": ["Amazon", "Google", "Meta"],
            "question": "What is the difference between an Epoch, a Batch Size, and an Iteration in neural network training?",
            "answer": "**Quick Answer:**\n- **Epoch:** One complete pass through the entire training dataset.\n- **Batch Size:** The number of training examples processed together in one forward/backward pass.\n- **Iteration (or Step):** One weight update, equal to processing one batch.\n\n**Concrete Example:**\nSuppose you have a dataset of 1,000 images and you set a Batch Size of 100:\n1. To see all 1,000 images, your model must process 10 batches (1,000 / 100 = 10 iterations).\n2. After completing those 10 iterations, the model has completed **1 Epoch**.\n3. If you train for 20 Epochs, the model will run a total of 200 iterations (20 × 10).",
            "tip": "Interviewers check if you know why we use Mini-batches instead of the whole dataset at once (because loading all data into GPU memory causes Out-of-Memory crashes)."
        },
        {
            "id": "fresher_22",
            "category": "dl",
            "category_label": "Deep Learning",
            "experience_level": "0-2",
            "experience_label": "0–2 Yrs (Junior / Fresher)",
            "difficulty": "Junior / Fresher",
            "company_tags": ["Google", "Tesla", "Apple"],
            "question": "What is Transfer Learning, and why is it so widely used in modern Computer Vision and NLP?",
            "answer": "**Quick Answer:**\nTransfer learning takes a model that was already trained on a massive generic dataset (like ImageNet or Wikipedia) and repurposes its learned features for a specific target task.\n\n**Why It Is So Powerful:**\n- Training a vision model from scratch requires millions of labeled photos and weeks of expensive GPU compute.\n- Early layers of a vision network learn universal basics: edges, curves, shadows, and textures.\n- With transfer learning, you freeze those early feature layers and only train the final output layer on your 500 specialized medical X-ray photos.\n- *Result:* 95%+ accuracy with 100x less training data and 100x less compute cost.",
            "tip": "Mention that almost all production AI today (ResNet, BERT, Llama fine-tuning) is built on Transfer Learning."
        },
        {
            "id": "fresher_23",
            "category": "metrics_data",
            "category_label": "Metrics & Data",
            "experience_level": "0-2",
            "experience_label": "0–2 Yrs (Junior / Fresher)",
            "difficulty": "Junior / Fresher",
            "company_tags": ["Stripe", "Uber", "Microsoft"],
            "question": "What is the difference between a Loss Function and an Evaluation Metric?",
            "answer": "**Quick Answer:**\n- A **Loss Function** is used by the algorithm during training to calculate gradients and update weights.\n- An **Evaluation Metric** is used by humans and business stakeholders to measure real-world performance.\n\n**Key Differences:**\n1. **Differentiability:** A loss function *must* be mathematically differentiable (have smooth slopes) so gradient descent can calculate derivatives. Metrics (like Accuracy or F1-Score) do not need to be differentiable.\n2. **Human Readability:** Loss numbers (e.g. 0.0382 cross-entropy) mean nothing to a product manager. F1-score of 92% or Precision of 95% provides actionable business clarity.\n3. *Example:* In binary classification, the model optimizes **Binary Cross-Entropy Loss**, but the team reports **ROC-AUC and Recall**.",
            "tip": "Explain that accuracy cannot be used directly as a loss function because its derivative is zero almost everywhere."
        },
        {
            "id": "fresher_24",
            "category": "ml",
            "category_label": "Classical Machine Learning",
            "experience_level": "0-2",
            "experience_label": "0–2 Yrs (Junior / Fresher)",
            "difficulty": "Junior / Fresher",
            "company_tags": ["Google", "Meta", "Accenture"],
            "question": "What is Bias in Artificial Intelligence, and give two common examples of how it can happen accidentally.",
            "answer": "**Quick Answer:**\nAI bias occurs when an algorithm produces systematically prejudiced results that unfairly disadvantage certain demographic groups.\n\n**Two Common Ways Bias Occurs:**\n1. **Historical Bias in the Real World:**\n   - Machine learning algorithms learn by mimicking historical data. If past human hiring practices favored male candidates, an AI resume screener will learn to penalize female candidates even if the word 'gender' is removed.\n2. **Sampling & Representation Bias:**\n   - If a facial recognition system is trained on a dataset where 85% of photos are light-skinned men, the model achieves 99% accuracy on light-skinned men, but fails with high error rates on dark-skinned women due to severe under-representation.\n\n**The Golden Rule:** The algorithm is a mirror of its training data. Biased data produces biased predictions.",
            "tip": "Mention that fairness requires evaluating model accuracy separately across diverse data slices (disaggregated evaluation)."
        },
        {
            "id": "fresher_25",
            "category": "metrics_data",
            "category_label": "Metrics & Data",
            "experience_level": "0-2",
            "experience_label": "0–2 Yrs (Junior / Fresher)",
            "difficulty": "Junior / Fresher",
            "company_tags": ["Amazon", "Kaggle", "Salesforce"],
            "question": "What is K-Fold Cross Validation, and why is it better than a single Train-Test split?",
            "answer": "**Quick Answer:**\nK-Fold Cross Validation splits the dataset into K equal parts (folds). The model is trained K times, each time using K-1 folds for training and the remaining 1 fold for testing, ensuring every single data point is tested on exactly once.\n\n**Why It Is Better Than a Single Split:**\n1. **Eliminates 'Lucky' Splits:** In a single 80/20 train/test split, by pure coincidence your test set might contain only the easiest examples, giving a false sense of high accuracy.\n2. **Maximal Data Utilization:** In small datasets (e.g. 500 rows), holding out 20% leaves too few examples to train on. In 5-fold cross-validation, 100% of the data is used for testing across the 5 iterations.\n3. **Variance Estimate:** It yields K accuracy scores, giving both the mean performance and standard deviation (e.g. 88% ± 2.1%), showing model consistency.",
            "tip": "State that K=5 or K=10 is the universal industry standard."
        },
        {
            "id": "fresher_26",
            "category": "metrics_data",
            "category_label": "Metrics & Data",
            "experience_level": "0-2",
            "experience_label": "0–2 Yrs (Junior / Fresher)",
            "difficulty": "Junior / Fresher",
            "company_tags": ["Shopify", "Walmart", "Ebay"],
            "question": "What is the difference between One-Hot Encoding and Label Encoding for categorical data?",
            "answer": "**Quick Answer:**\n- **Label Encoding:** Assigns each category a sequential integer (e.g. `Red=1, Blue=2, Green=3`).\n- **One-Hot Encoding:** Creates a new binary (0 or 1) column for each distinct category.\n\n**When to Use Which:**\n1. **Use Label (Ordinal) Encoding:** When the category has a natural order (e.g. `Small=1, Medium=2, Large=3`, or `Junior=1, Mid=2, Senior=3`).\n2. **Use One-Hot Encoding:** When categories have NO natural ranking (e.g. Country: `USA, Canada, Mexico`, or Color: `Red, Green, Blue`).\n\n**The Danger of Misuse:** If you label encode non-ordered colors as `Red=1, Blue=2, Green=3`, a linear regression model will mistakenly assume that `Green (3) > Red (1)` or that `Red + Blue = Green`!",
            "tip": "Mention the downside of One-Hot Encoding: if a column has 10,000 unique zip codes, one-hot encoding creates 10,000 new columns (curse of dimensionality)."
        },
        {
            "id": "fresher_27",
            "category": "ml",
            "category_label": "Classical Machine Learning",
            "experience_level": "0-2",
            "experience_label": "0–2 Yrs (Junior / Fresher)",
            "difficulty": "Junior / Fresher",
            "company_tags": ["Google", "Bloomberg", "Two Sigma"],
            "question": "What is the difference between Correlation and Causation? Give an example of why confusing them ruins ML models.",
            "answer": "**Quick Answer:**\n- **Correlation** means two variables tend to move together.\n- **Causation** means a change in one variable directly causes a change in the other.\n\n**The Classic Ice Cream & Drowning Example:**\n- In summer, ice cream sales increase dramatically.\n- In summer, swimming pool drownings also increase dramatically.\n- There is a high mathematical correlation between ice cream sales and drownings.\n- But banning ice cream will NOT save a single life! Both are independently caused by a third confounding variable: **Hot Summer Weather**.\n\n**Why This Matters in ML:**\nA model trained on correlated historical data might suggest giving patients fewer blood tests because patients who receive 10 blood tests die more often (failing to recognize that severely ill patients receive more tests!).",
            "tip": "Explain that machine learning finds statistical correlations; proving causation requires randomized controlled trials (A/B testing)."
        },
        {
            "id": "fresher_28",
            "category": "ml",
            "category_label": "Classical Machine Learning",
            "experience_level": "0-2",
            "experience_label": "0–2 Yrs (Junior / Fresher)",
            "difficulty": "Junior / Fresher",
            "company_tags": ["Microsoft", "Meta", "Amazon"],
            "question": "What is the Bias-Variance Tradeoff in simple words? Explain it using the Dartboard Analogy without complex math.",
            "answer": "**Quick Answer:**\nThe Bias-Variance Tradeoff describes the balance between a model being too simple (High Bias) vs too sensitive to training noise (High Variance).\n\n**The Dartboard Analogy (Aiming for the Bullseye):**\n1. **Low Bias, Low Variance (The Goal):** All darts cluster tightly right in the bullseye center. The model makes accurate, consistent predictions.\n2. **High Bias, Low Variance (Underfitting):** All darts cluster tightly together, but far off to the top-right corner. The model is consistent, but consistently wrong due to oversimplified assumptions.\n3. **Low Bias, High Variance (Overfitting):** Darts are scattered all over the board in every direction. On average they center around the bullseye, but individual shots are erratic and unstable.\n4. **High Bias, High Variance (Worst Case):** Darts are scattered erratically far away from the bullseye.",
            "tip": "Use the dartboard visual! It is universally recognized by tech interviewers."
        },
        {
            "id": "fresher_29",
            "category": "genai_llm",
            "category_label": "GenAI & LLMs",
            "experience_level": "0-2",
            "experience_label": "0–2 Yrs (Junior / Fresher)",
            "difficulty": "Junior / Fresher",
            "company_tags": ["OpenAI", "Anthropic", "Cohere"],
            "question": "What is the difference between Prompting and Fine-Tuning an LLM? When should a team choose one over the other?",
            "answer": "**Quick Answer:**\n- **Prompting:** Instructing the model using text input without changing its weights. Fast, cheap, and immediate.\n- **Fine-Tuning:** Updating the model's actual internal weights on a specialized dataset. Slower and requires training compute, but bakes specific style, jargon, or syntax permanently into the model.\n\n**When to Use Prompting (Start Here First!):**\n- 90% of real-world use cases.\n- General Q&A, drafting emails, summarizing text, or prototyping a new product.\n- If you need external facts, combine prompting with RAG.\n\n**When to Use Fine-Tuning:**\n- Teaching the model a hyper-specialized vocabulary or output format (e.g. customized SQL dialect or medical terminology).\n- Slashing prompt token costs (baking instructions into weights eliminates the need for long 2,000-token system prompts on every call).\n- Lowering latency: A fine-tuned 7B model can beat a generic 70B model on specialized tasks.",
            "tip": "The standard engineering advice is: 'Prompt first, add RAG second, fine-tune only when necessary'."
        },
        {
            "id": "fresher_30",
            "category": "rag",
            "category_label": "RAG & Vector DB",
            "experience_level": "0-2",
            "experience_label": "0–2 Yrs (Junior / Fresher)",
            "difficulty": "Junior / Fresher",
            "company_tags": ["Pinecone", "MongoDB", "Databricks"],
            "question": "What is a Vector Database (like Pinecone, Chroma, or Milvus), and why can't we just use standard SQL databases for AI search?",
            "answer": "**Quick Answer:**\nA Vector Database is built specifically to store high-dimensional numerical vectors (embeddings) and perform lightning-fast similarity searches across millions of items.\n\n**Why Standard SQL Databases Struggle:**\n- SQL databases (Postgres, MySQL) excel at exact keyword matches (`WHERE status = 'Active'` or `WHERE price < 50`).\n- But in modern AI, you search by **semantic meaning**, not exact keywords!\n- *Example:* If a user searches for 'affordable vacation', SQL `LIKE '%vacation%'` will miss an article titled 'Budget Beach Getaway' because none of the words match.\n- A Vector Database converts both the query and documents into vectors and finds the nearest neighbors in geometric space in 5 milliseconds using Approximate Nearest Neighbor (ANN) indexing.",
            "tip": "Mention that many relational databases (like PostgreSQL with the pgvector extension) are now adding vector capabilities."
        }
    ]

    # Add existing questions and enrich them with experience_level tags
    # Load existing questions
    with open(INTERVIEW_PATH, 'r', encoding='utf-8') as f:
        existing = json.load(f)

    # Classify existing questions into 2-4 and 5+
    enriched_existing = []
    for q in existing:
        diff = q.get('difficulty', '')
        # Map difficulties to experience levels
        if 'Junior' in diff:
            q['experience_level'] = '0-2'
            q['experience_label'] = '0–2 Yrs (Junior / Fresher)'
        elif 'Senior' in diff or 'Staff' in diff or 'Quant' in diff:
            q['experience_level'] = '5+'
            q['experience_label'] = '5+ Yrs (Senior / Lead)'
        else:
            q['experience_level'] = '2-4'
            q['experience_label'] = '2–4 Yrs (Mid-Level)'
        enriched_existing.append(q)

    # Combine novice questions first, then enriched existing
    final_questions = fresher_questions + enriched_existing

    # Deduplicate by ID
    seen_ids = set()
    unique_questions = []
    for q in final_questions:
        if q['id'] not in seen_ids:
            seen_ids.add(q['id'])
            unique_questions.append(q)

    print(f"Total questions generated: {len(unique_questions)}")
    c_0_2 = sum(1 for q in unique_questions if q.get('experience_level') == '0-2')
    c_2_4 = sum(1 for q in unique_questions if q.get('experience_level') == '2-4')
    c_5_plus = sum(1 for q in unique_questions if q.get('experience_level') == '5+')
    print(f"Breakdown: 0-2 Yrs: {c_0_2} | 2-4 Yrs: {c_2_4} | 5+ Yrs: {c_5_plus}")

    with open(INTERVIEW_PATH, 'w', encoding='utf-8') as f:
        json.dump(unique_questions, f, indent=2, ensure_ascii=False)
    print("Saved updated interviewQuestions.json")

if __name__ == '__main__':
    build_questions()
