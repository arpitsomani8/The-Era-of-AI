# scripts/curriculum_domain_rl_ts_recsys.py
# Continued with Time Series and RecSys

from scripts.curriculum_domain_rl_ts_recsys import get_rl_concepts

def get_time_series_concepts():
    topic_id = "ml_time_series"
    topic_label = "Time Series Analysis & Forecasting Dynamics"
    cat = "ml"
    cat_label = "Classical Machine Learning"

    return [
        {
            "id": "concept_stationarity_acf_pacf",
            "title": "Stationarity, Autocorrelation (ACF/PACF) & Differencing",
            "topic_id": topic_id, "topic_label": topic_label, "category": cat, "category_label": cat_label,
            "raw_subtopic": "Stationarity, Autocorrelation (ACF/PACF) & Differencing", "raw_sub": "Stationarity, Autocorrelation (ACF/PACF) & Differencing",
            "def": "The bedrock criteria for statistical time-series modeling where the mean, variance, and autocovariance remain invariant over time, verified via Augmented Dickey-Fuller (ADF) tests, analyzed via ACF/PACF plots, and induced via lag differencing.",
            "definition": "The bedrock criteria for statistical time-series modeling where the mean, variance, and autocovariance remain invariant over time, verified via Augmented Dickey-Fuller (ADF) tests, analyzed via ACF/PACF plots, and induced via lag differencing.",
            "formula": "$$\\nabla^d X_t = (1 - B)^d X_t, \\quad \\text{ACF}(k) = \\frac{\\text{Cov}(X_t, X_{t-k})}{\\text{Var}(X_t)}, \\quad \\text{ADF}: \\Delta y_t = \\alpha + \\beta t + \\gamma y_{t-1} + \\sum_{i=1}^p \\delta_i \\Delta y_{t-i} + \\epsilon_t$$",
            "formula_explanation": "",
            "logic": "Non-stationary series have time-dependent moments, causing spurious regression correlations where two completely unrelated upward-trending series show artificial statistical significance.",
            "core_logic": "Non-stationary series have time-dependent moments, causing spurious regression correlations where two completely unrelated upward-trending series show artificial statistical significance.",
            "architectural_logic": "",
            "example": "Financial stock price modeling: Raw stock prices drift upward non-stationarily. First-order log differencing produces stationary percentage returns, enabling reliable volatility forecasting.",
            "tags": ["Time Series", "Stationarity", "ACF", "PACF", "Differencing"],
            "simple_summary": "Stationarity means the statistical 'weather' of a data stream doesn't change over time—its average and spread stay steady. Differencing subtracts today's value from yesterday's to remove trends.",
            "core_terms": [
                {
                    "term": "Stationarity",
                    "what_is_it": "A property where a time series has a constant mean, constant variance, and autocovariance that depends only on lag distance.",
                    "analogy": "A pendulum swinging steadily around a fixed resting point versus an elevator climbing higher and higher.",
                    "why_it_matters": "Almost all classical statistical forecasting models assume stationarity to make valid future inferences."
                },
                {
                    "term": "Autocorrelation Function (ACF)",
                    "what_is_it": "The correlation between a time series and a lagged version of itself across different time delays k.",
                    "analogy": "How closely today's temperature correlates with yesterday's, last Tuesday's, or last month's temperature.",
                    "why_it_matters": "Identifies recurring seasonal cycles and helps determine moving average (MA) order q."
                },
                {
                    "term": "Partial Autocorrelation Function (PACF)",
                    "what_is_it": "The correlation between X_t and X_{t-k} after removing the linear effects of all intermediate lags (X_{t-1} through X_{t-k+1}).",
                    "analogy": "Measuring your direct genetic resemblance to your grandparent, controlling for the traits inherited from your parent.",
                    "why_it_matters": "Determines the exact autoregressive (AR) order p for ARIMA."
                },
                {
                    "term": "Augmented Dickey-Fuller (ADF) Test",
                    "what_is_it": "A statistical hypothesis test where the null hypothesis is that the series possesses a unit root (is non-stationary).",
                    "analogy": "A medical blood test checking whether a patient has a fever (p-value < 0.05 confirms healthy stationarity).",
                    "why_it_matters": "Provides an objective mathematical benchmark for differencing decisions."
                }
            ],
            "symbol_guide": [
                {"symbol": "B", "meaning": "Backshift (Lag) operator", "plain_english": "B X_t = X_{t-1}"},
                {"symbol": "(1 - B)", "meaning": "First-order differencing", "plain_english": "X_t - X_{t-1}"},
                {"symbol": "\\rho_k", "meaning": "Autocorrelation at lag k", "plain_english": "Correlation between now and k steps in the past"}
            ],
            "numerical_example": "Raw series: [100, 105, 112, 118, 126] (clear upward trend, ADF p = 0.85). First differencing: [105-100=5, 112-105=7, 118-112=6, 126-118=8]. Mean stabilizes around 6.5, variance is stable, ADF p-value drops to 0.01 (reject null -> stationary).",
            "pitfalls": "Novice Trap: Over-differencing. Applying differencing d=2 or d=3 when d=1 was sufficient introduces artificial negative autocorrelation and inflates variance, ruining forecast accuracy.",
            "key_takeaways": [],
            "definition_bullets": [
                "Stationarity: Invariant mean and variance across chronological time windows.",
                "ACF: Correlation between series and lagged versions across multiple delays.",
                "PACF: Direct correlation between time points with intermediate lag effects removed.",
                "ADF Test: Hypothesis test to statistically confirm whether differencing is required."
            ]
        },
        {
            "id": "concept_arima_sarimax",
            "title": "ARIMA, SARIMAX & Exponential Smoothing",
            "topic_id": topic_id, "topic_label": topic_label, "category": cat, "category_label": cat_label,
            "raw_subtopic": "ARIMA, SARIMAX & Exponential Smoothing", "raw_sub": "ARIMA, SARIMAX & Exponential Smoothing",
            "def": "The cornerstone parametric time series forecasting models combining Autoregressive lags (p), Differencing integrations (d), Moving Average shock terms (q), Seasonal cycles (P,D,Q,s), and Exogenous covariates (X).",
            "definition": "The cornerstone parametric time series forecasting models combining Autoregressive lags (p), Differencing integrations (d), Moving Average shock terms (q), Seasonal cycles (P,D,Q,s), and Exogenous covariates (X).",
            "formula": "$$\\Phi_P(B^s) \\phi_p(B) (1-B)^d (1-B^s)^D X_t = \\beta^T Z_t + \\Theta_Q(B^s) \\theta_q(B) \\epsilon_t, \\quad \\text{Holt-Winters: } \\hat{y}_{t+h} = (l_t + h b_t) s_{t+h-m}$$",
            "formula_explanation": "",
            "logic": "ARIMA models express future values as a linear combination of past observations (AR) and past white-noise forecast errors (MA), while SARIMAX extends this with repeating seasonal periods and external business drivers (e.g. ad spend, temperature).",
            "core_logic": "ARIMA models express future values as a linear combination of past observations (AR) and past white-noise forecast errors (MA), while SARIMAX extends this with repeating seasonal periods and external business drivers (e.g. ad spend, temperature).",
            "architectural_logic": "",
            "example": "Electricity grid load forecasting: SARIMAX(1,1,1)(1,1,1)24 models hourly power consumption by combining 24-hour daily seasonality with exogenous temperature covariates.",
            "tags": ["ARIMA", "SARIMAX", "Exponential Smoothing", "Holt-Winters"],
            "simple_summary": "ARIMA predicts tomorrow by combining what happened yesterday (autoregression) with corrections from yesterday's prediction mistakes (moving average). SARIMAX adds seasonal repeats (like weekend peaks) and outside factors (like rainfall).",
            "core_terms": [
                {
                    "term": "Autoregressive (AR - p)",
                    "what_is_it": "Modeling the current value as a weighted sum of the previous p observations: phi_1 X_{t-1} + ... + phi_p X_{t-p}.",
                    "analogy": "Predicting tomorrow's temperature based primarily on the temperatures of the last 3 days.",
                    "why_it_matters": "Captures momentum and memory in sequential processes."
                },
                {
                    "term": "Integrated (I - d)",
                    "what_is_it": "The number of times raw data must be differenced to achieve stationarity.",
                    "analogy": "Looking at speed (change in distance) rather than absolute odometer mileage.",
                    "why_it_matters": "Enables the model to handle linear or polynomial trends."
                },
                {
                    "term": "Moving Average (MA - q)",
                    "what_is_it": "Modeling current value as a weighted sum of current and previous q random shock residuals: epsilon_t + theta_1 epsilon_{t-1}.",
                    "analogy": "Adjusting your steering wheel based on how hard recent gusts of wind knocked your car off course.",
                    "why_it_matters": "Allows rapid recovery from unexpected shocks."
                },
                {
                    "term": "Exogenous Regressors (X)",
                    "what_is_it": "External time-dependent predictor variables incorporated alongside the endogenous target series.",
                    "analogy": "Predicting umbrella sales by looking at past sales plus tomorrow's weather forecast.",
                    "why_it_matters": "Enables causal business levers (promotions, price changes) to directly drive forecasts."
                }
            ],
            "symbol_guide": [
                {"symbol": "(p, d, q)", "meaning": "Non-seasonal ARIMA order", "plain_english": "p = AR lags, d = differencing degree, q = MA error lags"},
                {"symbol": "(P, D, Q)_s", "meaning": "Seasonal order with periodicity s", "plain_english": "e.g. s = 12 for monthly data or s = 7 for daily data"},
                {"symbol": "\\epsilon_t", "meaning": "White noise error term", "plain_english": "Uncorrelated random shocks with zero mean and constant variance"}
            ],
            "numerical_example": "AR(1) model: X_t = 0.7 X_{t-1} + e_t. If yesterday's value X_{t-1} = 10, expected value for today is 0.7 × 10 = 7.0. If tomorrow is 2 steps out: 0.7² × 10 = 4.9. The forecast smoothly decays toward the historical mean.",
            "pitfalls": "Novice Trap: Forgetting that exogenous variables (X) must be known in advance for the entire forecast horizon! If you use 'Competitor Price' as an exogenous variable to forecast next month's sales, you must already have reliable forecasts of competitor prices for next month.",
            "key_takeaways": [],
            "definition_bullets": [
                "Autoregressive (p): Predicting using a linear combination of previous time steps.",
                "Integrated (d): Differencing degree applied to stabilize the mean.",
                "Moving Average (q): Incorporating past prediction errors to absorb shocks.",
                "Exogenous Inputs (X): External causal covariates that influence the target series."
            ]
        },
        {
            "id": "concept_modern_forecasting_prophet_tft",
            "title": "Modern Forecasting: Prophet & Temporal Fusion Transformers (TFT)",
            "topic_id": topic_id, "topic_label": topic_label, "category": cat, "category_label": cat_label,
            "raw_subtopic": "Modern Forecasting: Prophet & Temporal Fusion Transformers (TFT)", "raw_sub": "Modern Forecasting: Prophet & Temporal Fusion Transformers (TFT)",
            "def": "Next-generation forecasting frameworks replacing rigid linear assumptions with additive generalized models (Meta Prophet) and multi-horizon deep self-attention architectures (Temporal Fusion Transformers) that jointly learn static entity metadata, known future inputs, and observed past dynamics.",
            "definition": "Next-generation forecasting frameworks replacing rigid linear assumptions with additive generalized models (Meta Prophet) and multi-horizon deep self-attention architectures (Temporal Fusion Transformers) that jointly learn static entity metadata, known future inputs, and observed past dynamics.",
            "formula": "$$\\text{Prophet}: y(t) = g(t) + s(t) + h(t) + \\epsilon_t, \\quad \\text{TFT: } \\tilde{y}_t(q, \\tau) = \\text{QuantileOutput}\\left(\\text{SelfAttn}(\\text{LSTM}(\\mathbf{x}_{t-k:t}, \\mathbf{z}_{\\text{static}}))\\right)$$",
            "formula_explanation": "",
            "logic": "Classical ARIMA fits a single univariate series with high sensitivity to missing data. Prophet uses decomposable Bayesian curves with holiday changepoints, while TFT scales across thousands of related series simultaneously with interpretable multi-head attention.",
            "core_logic": "Classical ARIMA fits a single univariate series with high sensitivity to missing data. Prophet uses decomposable Bayesian curves with holiday changepoints, while TFT scales across thousands of related series simultaneously with interpretable multi-head attention.",
            "architectural_logic": "",
            "example": "Amazon cloud server demand forecasting: TFT ingests historical server CPU loads, static customer industry metadata, and known future holiday calendar schedules across 100,000 EC2 instances to predict P10, P50, and P90 capacity needs.",
            "tags": ["Prophet", "TFT", "Deep Forecasting", "Quantile Loss"],
            "simple_summary": "Modern forecasting uses decomposable curve-fitting (Prophet) that easily handles holidays and missing days, or giant neural attention networks (TFT) that forecast thousands of stores at once while outputting uncertainty ranges (P10, P50, P90).",
            "core_terms": [
                {
                    "term": "Decomposable Additive Model (Prophet)",
                    "what_is_it": "Deconstructing a time series into trend g(t), seasonality s(t), holiday effects h(t), and noise.",
                    "analogy": "Analyzing a song as bass line (trend) + recurring drum beat (seasonality) + cymbal crash (holiday).",
                    "why_it_matters": "Tolerates missing dates, handles irregular holidays seamlessly, and provides human-interpretable components."
                },
                {
                    "term": "Temporal Fusion Transformer (TFT)",
                    "what_is_it": "A specialized neural architecture combining gating layers, LSTM recurrent encoders, and multi-head self-attention for multi-horizon forecasting.",
                    "analogy": "An expert forecasting committee where specialized analysts review past history, future schedules, and corporate background before voting.",
                    "why_it_matters": "Learns complex cross-series temporal interactions across millions of related time series."
                },
                {
                    "term": "Quantile Loss (Pinball Loss)",
                    "what_is_it": "An asymmetric loss function that outputs probabilistic prediction intervals (e.g. 10th, 50th, 90th percentiles) rather than a single point estimate.",
                    "analogy": "A meteorologist saying: 'We will get at least 2 inches of rain (P10), most likely 5 inches (P50), and at most 9 inches (P90)'.",
                    "why_it_matters": "Crucial for risk management: under-forecasting hospital beds is far more costly than over-forecasting."
                },
                {
                    "term": "Variable Selection Network (VSN)",
                    "what_is_it": "A feature-gating mechanism inside TFT that dynamically suppresses irrelevant exogenous features per time step.",
                    "analogy": "Noise-cancelling headphones that mute irrelevant chatter so the model only focuses on key signals.",
                    "why_it_matters": "Prevents overfitting when hundreds of exogenous features are fed into deep models."
                }
            ],
            "symbol_guide": [
                {"symbol": "g(t)", "meaning": "Piecewise linear or logistic growth trend", "plain_english": "The long-term trajectory curve"},
                {"symbol": "s(t)", "meaning": "Fourier series seasonal periodicities", "plain_english": "Weekly and yearly repeating cycles"},
                {"symbol": "q", "meaning": "Target quantile percentile", "plain_english": "e.g. q = 0.90 predicts the 90th percentile ceiling"}
            ],
            "numerical_example": "Prophet decomposition of product sales: Base trend g(t) = 500 units. Day of week effect s(t) = +150 on Saturday, -80 on Tuesday. Black Friday holiday effect h(t) = +1,200. Expected sales for Black Friday Saturday = 500 + 150 + 1200 = 1,850 units.",
            "pitfalls": "Novice Trap: Relying solely on default Prophet changepoint parameters for complex financial data. Prophet defaults assume smoothly changing trends, which can over-smooth sudden market regime shifts or fit bogus trend extrapolation.",
            "key_takeaways": [],
            "definition_bullets": [
                "Decomposable Additive Model: Breaks series into trend, seasonality, and holiday components.",
                "Temporal Fusion Transformer: Deep attention architecture for cross-series multi-horizon prediction.",
                "Quantile Loss: Predicts full probability distribution intervals (P10, P50, P90).",
                "Variable Selection Networks: Automatically filters out noisy exogenous features."
            ]
        },
        {
            "id": "concept_time_series_feature_engineering",
            "title": "Time-Series Feature Engineering & Lag Variables",
            "topic_id": topic_id, "topic_label": topic_label, "category": cat, "category_label": cat_label,
            "raw_subtopic": "Time-Series Feature Engineering & Lag Variables", "raw_sub": "Time-Series Feature Engineering & Lag Variables",
            "def": "The specialized feature generation methodology that transforms unstructured chronological sequences into tabular ML feature matrices using backward lag features, rolling window aggregates, exponential moving averages, and cyclical trigonometric date encodings.",
            "definition": "The specialized feature generation methodology that transforms unstructured chronological sequences into tabular ML feature matrices using backward lag features, rolling window aggregates, exponential moving averages, and cyclical trigonometric date encodings.",
            "formula": "$$\\text{Lag}_k = X_{t-k}, \\quad \\text{RollingMean}_w = \\frac{1}{w} \\sum_{i=1}^w X_{t-i}, \\quad \\text{Cyclical: } [\\sin(2\\pi t / T), \\cos(2\\pi t / T)]$$",
            "formula_explanation": "",
            "logic": "Standard GBDTs (XGBoost, LightGBM) have no innate concept of sequential time or temporal order. Temporal feature engineering projects historical trajectories into static columns so decision trees can learn complex non-linear lag relationships.",
            "core_logic": "Standard GBDTs (XGBoost, LightGBM) have no innate concept of sequential time or temporal order. Temporal feature engineering projects historical trajectories into static columns so decision trees can learn complex non-linear lag relationships.",
            "architectural_logic": "",
            "example": "E-commerce grocery replenishment: Generating lag_1 (yesterday's sales), lag_7 (same day last week), rolling_mean_14 (2-week velocity), and month_sin/cos to train a LightGBM model that outperforms complex neural networks.",
            "tags": ["Feature Engineering", "Lag Variables", "Rolling Windows", "Cyclical Features"],
            "simple_summary": "Since decision trees like XGBoost can't look back in time on their own, feature engineering feeds them columns like 'what happened 1 hour ago', 'average over the last 7 days', and clock angles (sine/cosine) to represent time smoothly.",
            "core_terms": [
                {
                    "term": "Lag Variables (t-k)",
                    "what_is_it": "Shifting the target series backward in time by k steps so past values sit as feature columns at row t.",
                    "analogy": "Looking in your rearview mirror at where your car was 100 meters ago.",
                    "why_it_matters": "The primary signal in almost every tabular time series model."
                },
                {
                    "term": "Rolling Window Aggregations",
                    "what_is_it": "Computing rolling statistics (mean, std, min, max, skew) over the prior w time steps: [t-w to t-1].",
                    "analogy": "Calculating a baseball player's batting average over the last 30 games.",
                    "why_it_matters": "Smooths out point noise and captures short-term velocity and volatility."
                },
                {
                    "term": "Cyclical Trigonometric Encodings",
                    "what_is_it": "Mapping periodic calendar features (hour 0-23, month 1-12) onto a 2D circle using sine and cosine functions.",
                    "analogy": "The hands of an analog clock where 11:59 PM and 12:01 AM are right next to each other in distance.",
                    "why_it_matters": "Prevents artificial numeric cliffs where hour 23 and hour 0 appear 23 units apart instead of 1 unit apart."
                },
                {
                    "term": "Exponential Moving Average (EMA)",
                    "what_is_it": "A weighted moving average where weights decrease exponentially for older observations.",
                    "analogy": "Remembering what you ate yesterday clearly, but only having a fuzzy impression of what you ate 2 weeks ago.",
                    "why_it_matters": "Reacts faster to recent market shifts than a simple arithmetic moving average."
                }
            ],
            "symbol_guide": [
                {"symbol": "X_{t-k}", "meaning": "Value observed at k time steps prior to t", "plain_english": "e.g. sales 7 days ago"},
                {"symbol": "w", "meaning": "Window size for aggregation", "plain_english": "e.g. 7-day or 30-day window"},
                {"symbol": "T", "meaning": "Cycle period", "plain_english": "e.g. T = 24 for daily hours, T = 7 for weekly days"}
            ],
            "numerical_example": "Hour of day = 23 (11 PM). Standard numerical feature: 23. Hour 0 (midnight) is 0. Distance in tree = |23 - 0| = 23. Cyclical encoding: sin(2pi × 23/24) = -0.259, cos = 0.966. For hour 0: sin = 0.0, cos = 1.0. Euclidean distance on circle = sqrt((-0.259-0)² + (0.966-1)²) = 0.261. The model recognizes they are immediate neighbors!",
            "pitfalls": "Novice Trap: Lookahead leakage in rolling windows! Calculating rolling mean over [t-w to t] includes current value X_t, which leaks the exact label you are trying to predict. Rolling windows must strictly be shifted by at least 1 lag: [t-w to t-1].",
            "key_takeaways": [],
            "definition_bullets": [
                "Lag Variables: Past target values shifted into feature columns.",
                "Rolling Windows: Summary statistics over past time intervals to capture trends.",
                "Cyclical Encodings: Sine/cosine pairs preserving temporal continuity at period boundaries.",
                "Lookahead Hygiene: Shifting features backward to prevent future data leakage."
            ]
        },
        {
            "id": "concept_rolling_expanding_window_cv",
            "title": "Rolling-Window & Expanding-Window Cross Validation",
            "topic_id": topic_id, "topic_label": topic_label, "category": cat, "category_label": cat_label,
            "raw_subtopic": "Rolling-Window & Expanding-Window Cross Validation", "raw_sub": "Rolling-Window & Expanding-Window Cross Validation",
            "def": "Temporal cross-validation schemes that strictly respect chronological causality by enforcing that training folds always precede test folds in time, implemented via expanding windows (anchored start) or rolling windows (fixed memory horizon).",
            "definition": "Temporal cross-validation schemes that strictly respect chronological causality by enforcing that training folds always precede test folds in time, implemented via expanding windows (anchored start) or rolling windows (fixed memory horizon).",
            "formula": "$$\\text{Fold}_k: \\text{Train} = \\{X_1, \\dots, X_{T_k}\\}, \\quad \\text{Purge/Embargo} = \\{X_{T_k+1}, \\dots, X_{T_k+g}\\}, \\quad \\text{Test} = \\{X_{T_k+g+1}, \\dots, X_{T_k+g+H}\\}$$",
            "formula_explanation": "",
            "logic": "Standard k-fold cross-validation randomly shuffles rows, training on the future to predict the past. This causes catastrophic data leakage. Temporal validation simulates real-world production deployment: training strictly on past history and predicting into the unobserved future.",
            "core_logic": "Standard k-fold cross-validation randomly shuffles rows, training on the future to predict the past. This causes catastrophic data leakage. Temporal validation simulates real-world production deployment: training strictly on past history and predicting into the unobserved future.",
            "architectural_logic": "",
            "example": "High-frequency algorithmic trading: Backtesting an equity trading strategy over 2018-2023 using expanding window validation with a 2-day embargo period to prevent serial correlation leakage between trade executions.",
            "tags": ["Cross-Validation", "TimeSeriesSplit", "Expanding Window", "Data Leakage"],
            "simple_summary": "You can never shuffle time series data! Temporal cross-validation tests your model like real life: you train on the past and test on the future, then slide your test window forward step by step to verify performance across multiple market conditions.",
            "core_terms": [
                {
                    "term": "Expanding Window (Walk-Forward)",
                    "what_is_it": "Training start date remains fixed at t=0, while the training end date grows forward with each fold.",
                    "analogy": "A student accumulating more life experience year after year while taking annual exams.",
                    "why_it_matters": "Maximizes sample size as historical data accumulates."
                },
                {
                    "term": "Rolling Window (Fixed Horizon)",
                    "what_is_it": "Both start date and end date slide forward together, keeping the training window length strictly constant (e.g. always train on last 365 days).",
                    "analogy": "An athlete only training with drills from the current season, dropping drills from 5 years ago.",
                    "why_it_matters": "Prevents ancient, obsolete market regimes from distorting modern predictions."
                },
                {
                    "term": "Purging",
                    "what_is_it": "Removing training observations whose future outcome overlaps with the start of the test window.",
                    "analogy": "Erasing a question from study materials that is identical to question #1 on tomorrow's test.",
                    "why_it_matters": "Prevents label leakage in multi-day forecast horizons."
                },
                {
                    "term": "Embargoing",
                    "what_is_it": "Adding a buffer gap immediately following the test set before the next training set begins.",
                    "analogy": "A quarantine waiting period between hospital rooms.",
                    "why_it_matters": "Neutralizes autoregressive memory leakage caused by overlapping financial positions."
                }
            ],
            "symbol_guide": [
                {"symbol": "T_k", "meaning": "Training boundary timestamp for fold k", "plain_english": "The cutoff date between past training and future testing"},
                {"symbol": "g", "meaning": "Purge/Embargo gap width", "plain_english": "Buffer period to prevent spillover leakage"},
                {"symbol": "H", "meaning": "Forecast test horizon", "plain_english": "e.g. 7-day or 30-day forecast window"}
            ],
            "numerical_example": "5-fold TimeSeriesSplit on 6 years of data: Fold 1 trains Year 1, tests Year 2. Fold 2 trains Years 1-2, tests Year 3. Fold 3 trains Years 1-3, tests Year 4. Fold 4 trains Years 1-4, tests Year 5. Fold 5 trains Years 1-5, tests Year 6. Model average error across all 5 test years gives a realistic, un-leaked forecast accuracy.",
            "pitfalls": "Novice Trap: Using standard `train_test_split(shuffle=True)` from scikit-learn on time series data. Shuffling rows mixes future information into the training set, producing unrealistically high test accuracy (e.g. 99% R²) that immediately crashes to zero in real production.",
            "key_takeaways": [],
            "definition_bullets": [
                "Temporal Causality: Never train on future data to predict the past.",
                "Expanding Window: Training window grows chronologically with each validation fold.",
                "Rolling Window: Constant-size historical training window sliding through time.",
                "Purging & Embargoing: Buffering gaps to eliminate auto-correlated label spillovers."
            ]
        }
    ]

print("Time series concepts defined.")
