import React, { useState, useMemo, useEffect } from 'react';
import { 
  X, 
  Sparkles, 
  Award, 
  Clock, 
  RotateCcw, 
  CheckCircle2, 
  AlertCircle, 
  ArrowRight, 
  Compass, 
  BookOpen, 
  FileText, 
  Layers, 
  TrendingUp, 
  BrainCircuit, 
  HelpCircle,
  Share2,
  Check
} from 'lucide-react';
import { MathText } from './KaTeXRenderer';

// 10 BALANCED DIAGNOSTIC ASSESSMENT QUESTIONS ACROSS 4 PILLARS
const DIAGNOSTIC_QUESTIONS = [
  // Pillar 1: Math Foundations
  {
    id: 1,
    pillar: 'math',
    pillarLabel: 'Math & Optimization',
    question: 'Why does Scaled Dot-Product Attention divide the query-key dot product by $\\sqrt{d_k}$?',
    options: [
      'To ensure the attention matrix has zero mean and unit variance',
      'To prevent the dot products from growing excessively large, which pushes softmax into regions with vanishing gradients',
      'To enforce symmetric attention weights between query and key tokens',
      'To reduce memory footprint in GPU High Bandwidth Memory'
    ],
    correctIndex: 1,
    explanation: 'If components of $q$ and $k$ are independent variables with mean 0 and variance 1, their dot product has mean 0 and variance $d_k$. For large dimensions (e.g. $d_k = 128$), magnitudes grow into hundreds, saturating softmax into a one-hot distribution where gradients vanish. Dividing by $\\sqrt{d_k}$ stabilizes variance to 1.0.'
  },
  {
    id: 2,
    pillar: 'math',
    pillarLabel: 'Math & Optimization',
    question: 'In L1 regularization (Lasso), why does the penalty produce sparse parameter weights (exact zeros), whereas L2 (Ridge) does not?',
    options: [
      'L1 penalty has a constant non-zero subgradient at the origin, creating sharp diamond-shaped contour corners on coordinate axes',
      'L1 regularization penalizes large weights with squared exponential force',
      'L1 penalty introduces momentum that forces oscillating parameters to zero',
      'L1 loss is strictly non-convex, leading to multiple saddle points'
    ],
    correctIndex: 0,
    explanation: 'L1 regularization penalty $\\lambda \\sum |w_i|$ has a constant derivative $\\pm \\lambda$ regardless of how small $|w_i|$ is. Geometrically, its diamond constraint boundary has sharp corners on the coordinate axes where the loss contours intersect, setting coefficients to exact zero.'
  },

  // Pillar 2: Classical Machine Learning
  {
    id: 3,
    pillar: 'ml',
    pillarLabel: 'Classical ML',
    question: 'When evaluating a model on an imbalanced dataset (e.g., 99% negative, 1% positive), why is the Precision-Recall (PR) AUC preferred over ROC AUC?',
    options: [
      'PR AUC evaluates True Positives against False Negatives rather than True Negatives, avoiding distortion from massive True Negative counts',
      'ROC AUC cannot be computed when the class imbalance ratio exceeds 10:1',
      'PR AUC is insensitive to probability threshold calibration',
      'Precision and Recall are always monotonic functions of one another'
    ],
    correctIndex: 0,
    explanation: 'The False Positive Rate in ROC is $\\text{FPR} = \\frac{\\text{FP}}{\\text{FP} + \\text{TN}}$. With a massive number of negative samples, large absolute False Positives still produce a tiny FPR, creating an illusion of high performance. PR curves omit True Negatives entirely.'
  },
  {
    id: 4,
    pillar: 'ml',
    pillarLabel: 'Classical ML',
    question: 'How does XGBoost prevent overfitting in deep gradient boosted decision trees compared to standard Gradient Boosting Machines (GBM)?',
    options: [
      'Uses second-order Taylor expansion (Hessian) and explicit L1/L2 leaf weight regularization penalty',
      'Eliminates all negative leaf weights via ReLU post-processing',
      'Replaces decision trees with randomized linear perceptrons',
      'Forces all boosting iterations to have equal learning rate weights'
    ],
    correctIndex: 0,
    explanation: 'XGBoost uses a 2nd-order Taylor expansion of the loss function incorporating both gradients $g_i$ and Hessians $h_i$, plus an objective penalty $\\gamma T + \\frac{1}{2}\\lambda \\sum w_j^2$ on leaf counts and weights.'
  },

  // Pillar 3: Deep Learning Foundations
  {
    id: 5,
    pillar: 'dl',
    pillarLabel: 'Deep Learning',
    question: 'Why do modern LLM architectures (e.g., LLaMA, GPT-4) use RMSNorm or Pre-LayerNorm instead of Post-LayerNorm?',
    options: [
      'Pre-LayerNorm maintains an uncorrupted residual identity path, enabling stable gradient backpropagation without warm-up instability',
      'Post-LayerNorm requires twice as many trainable affine scale parameters',
      'RMSNorm computes covariance matrices across channels, improving spatial invariance',
      'Pre-LayerNorm eliminates the need for non-linear activation functions'
    ],
    correctIndex: 0,
    explanation: 'In Pre-LN ($x + F(\\text{Norm}(x))$), the clean skip connection $x$ is preserved end-to-end, preventing gradients from decaying or exploding through layer norms during early training iterations.'
  },
  {
    id: 6,
    pillar: 'dl',
    pillarLabel: 'Deep Learning',
    question: 'What is the primary computational bottleneck of standard self-attention on modern GPU hardware (e.g., A100 / H100)?',
    options: [
      'Memory bandwidth bound: transferring $O(N^2)$ attention matrices between slow HBM and fast SRAM',
      'Compute bound: floating-point matrix multiplications (FLOPs) exceed Tensor Core throughput',
      'Cache thrashing in L2 CPU cache during PyTorch autograd tracing',
      'PCIe bus transfer latency between CPU host and GPU device'
    ],
    correctIndex: 0,
    explanation: 'Standard attention is memory-bandwidth bound. GPUs spend over 80% of time waiting for High Bandwidth Memory (HBM, 2 TB/s) reads/writes of the $N \\times N$ matrix, while SRAM (19 TB/s) compute units sit idle. FlashAttention resolves this via block tiling.'
  },

  // Pillar 4: GenAI & LLM Architecture
  {
    id: 7,
    pillar: 'genai',
    pillarLabel: 'GenAI & LLMs',
    question: 'In LoRA (Low-Rank Adaptation), how does rank decomposition parameterize the weight update $\\Delta W$?',
    options: [
      '$\\Delta W = \\frac{\\alpha}{r} (B \\times A)$ where $B \\in \\mathbb{R}^{d \\times r}$ and $A \\in \\mathbb{R}^{r \\times k}$ with $r \\ll \\min(d, k)$',
      '$\\Delta W = W_0 \\odot \\text{Dropout}(p)$',
      '$\\Delta W = \\text{SVD}(W_0)$ retaining top $r$ singular values',
      '$\\Delta W = B + A$ where $B$ is sparse and $A$ is dense'
    ],
    correctIndex: 0,
    explanation: 'LoRA freezes $W_0$ and trains two low-rank matrices $B$ and $A$. With $r = 8$ or $16$, trainable parameters drop by $10,000\\times$, and during inference, $\\Delta W$ can be pre-merged directly into $W_0 = W_0 + \\Delta W$ with 0 extra latency.'
  },
  {
    id: 8,
    pillar: 'genai',
    pillarLabel: 'GenAI & LLMs',
    question: 'What is the function of the auxiliary load balancing loss in Mixture-of-Experts (MoE) models (e.g. Mixtral 8x7B)?',
    options: [
      'Prevents router collapse by encouraging uniform token distribution across all $N$ expert networks',
      'Minimizes floating-point quantization errors in 4-bit weights',
      'Enforces orthogonality between expert attention matrices',
      'Aligns model outputs with human preference feedback (RLHF)'
    ],
    correctIndex: 0,
    explanation: 'Without load balancing loss ($\\alpha N \\sum f_i P_i$), the gating router quickly develops a self-reinforcing bias toward a few popular experts, starving other experts of gradient updates and causing severe distributed pipeline bottlenecks.'
  },
  {
    id: 9,
    pillar: 'genai',
    pillarLabel: 'GenAI & LLMs',
    question: 'Why does RoPE (Rotary Position Embedding) outperform absolute sinusoidal position embeddings for long-context extrapolation?',
    options: [
      'It encodes relative token distances purely as complex planar rotations ($q_m^T k_n = g(x_m, x_n, m-n)$) via inner products',
      'It eliminates positional information from value vectors $V$',
      'It multiplies attention weights by static exponential decay masks',
      'It stores a discrete lookup table for every possible context length'
    ],
    correctIndex: 0,
    explanation: 'RoPE applies an orthogonal rotation matrix $R_{\\Theta, m}^d$ to queries and keys. The inner product $(R_m q)^T (R_n k)$ depends exclusively on relative distance $(m - n)$, preserving shift invariance and enabling context extension methods like YaRN.'
  },
  {
    id: 10,
    pillar: 'genai',
    pillarLabel: 'GenAI & LLMs',
    question: 'In Retrieval-Augmented Generation (RAG), what is the primary role of a Cross-Encoder Re-ranker following dense vector search?',
    options: [
      'Jointly attends to Query and Candidate Document tokens simultaneously, capturing deep cross-attention semantics that bi-encoder cosine search misses',
      'Compresses retrieved passage tokens into 8-bit quantized embeddings',
      'Generates synthetic hypothetical documents to augment query vectors (HyDE)',
      'Computes sparse BM25 inverted indexes in local cache'
    ],
    correctIndex: 0,
    explanation: 'Bi-encoders embed query and document independently, missing rich token-to-token cross-attention interactions. A cross-encoder takes $(Query, Document)$ into a single self-attention sequence, dramatically boosting top-1 accuracy.'
  }
];

export default function AssessmentModal({ isOpen, onClose }) {
  const [currentIdx, setCurrentIdx] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState({}); // { [questionId]: optionIndex }
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [timeLeft, setTimeLeft] = useState(600); // 10 minutes (600s)
  const [copiedResult, setCopiedResult] = useState(false);

  // Timer countdown
  useEffect(() => {
    if (!isOpen || isSubmitted) return;
    const timer = setInterval(() => {
      setTimeLeft(prev => {
        if (prev <= 1) {
          setIsSubmitted(true);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
    return () => clearInterval(timer);
  }, [isOpen, isSubmitted]);

  // Pillar Scores Breakdown
  const scores = useMemo(() => {
    const pillars = {
      math: { label: 'Math & Optimization', correct: 0, total: 2 },
      ml: { label: 'Classical ML', correct: 0, total: 2 },
      dl: { label: 'Deep Learning', correct: 0, total: 2 },
      genai: { label: 'GenAI & LLMs', correct: 0, total: 4 }
    };

    let totalCorrect = 0;
    DIAGNOSTIC_QUESTIONS.forEach(q => {
      if (selectedAnswers[q.id] === q.correctIndex) {
        totalCorrect++;
        if (pillars[q.pillar]) pillars[q.pillar].correct++;
      }
    });

    const percent = Math.round((totalCorrect / DIAGNOSTIC_QUESTIONS.length) * 100);

    let tier = 'Aspiring AI Builder';
    let tierColor = 'text-cyan-400';
    let tierBadge = 'bg-cyan-500/20 text-cyan-300 border-cyan-500/40';

    if (percent >= 90) {
      tier = 'Principal Research / Staff AI Engineer';
      tierColor = 'text-purple-400';
      tierBadge = 'bg-purple-500/20 text-purple-300 border-purple-500/40';
    } else if (percent >= 70) {
      tier = 'Senior AI / Machine Learning Engineer';
      tierColor = 'text-emerald-400';
      tierBadge = 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40';
    } else if (percent >= 50) {
      tier = 'Core ML Practitioner & Systems Builder';
      tierColor = 'text-amber-400';
      tierBadge = 'bg-amber-500/20 text-amber-300 border-amber-500/40';
    }

    return {
      pillars,
      totalCorrect,
      totalQuestions: DIAGNOSTIC_QUESTIONS.length,
      percent,
      tier,
      tierColor,
      tierBadge
    };
  }, [selectedAnswers]);

  const currentQ = DIAGNOSTIC_QUESTIONS[currentIdx];

  const handleSelectOption = (qId, optionIdx) => {
    if (isSubmitted) return;
    setSelectedAnswers(prev => ({
      ...prev,
      [qId]: optionIdx
    }));
  };

  const handleReset = () => {
    setSelectedAnswers({});
    setIsSubmitted(false);
    setCurrentIdx(0);
    setTimeLeft(600);
  };

  const handleCopyReport = () => {
    const report = `🏆 The Era of AI — Technical Diagnostic Assessment Report\nScore: ${scores.totalCorrect}/10 (${scores.percent}%)\nReadiness Tier: ${scores.tier}\n- Math & Optimization: ${scores.pillars.math.correct}/${scores.pillars.math.total}\n- Classical ML: ${scores.pillars.ml.correct}/${scores.pillars.ml.total}\n- Deep Learning: ${scores.pillars.dl.correct}/${scores.pillars.dl.total}\n- GenAI & LLMs: ${scores.pillars.genai.correct}/${scores.pillars.genai.total}\nTested at: http://localhost:3000/`;
    navigator.clipboard.writeText(report);
    setCopiedResult(true);
    setTimeout(() => setCopiedResult(false), 2000);
  };

  if (!isOpen) return null;

  // Format time MM:SS
  const formatTime = (secs) => {
    const m = Math.floor(secs / 60);
    const s = secs % 60;
    return `${m}:${s < 10 ? '0' : ''}${s}`;
  };

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-slate-950/85 backdrop-blur-md flex items-center justify-center p-3 sm:p-6 animate-fadeIn">
      <div className="bg-slate-900 border border-slate-700/80 rounded-3xl w-full max-w-4xl shadow-2xl overflow-hidden flex flex-col max-h-[92vh]">
        {/* Header Bar */}
        <div className="p-4 sm:p-5 border-b border-slate-800 flex items-center justify-between bg-slate-900/90 shrink-0">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-purple-500/10 text-purple-400 border border-purple-500/30 flex items-center justify-center shrink-0">
              <BrainCircuit className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-sm sm:text-base font-bold text-white tracking-wide">
                  AI Technical Readiness Diagnostic
                </h2>
                <span className="text-[10px] px-2 py-0.5 rounded-full bg-purple-500/20 text-purple-300 border border-purple-500/30 font-mono">
                  10 Questions
                </span>
              </div>
              <p className="text-[11px] text-slate-400 hidden sm:block">
                Evaluates Math, Classical ML, Deep Learning, and GenAI Architecture
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            {/* Timer Badge */}
            {!isSubmitted && (
              <div className="flex items-center gap-1.5 px-3 py-1 rounded-xl bg-slate-950 border border-slate-800 text-xs font-mono text-cyan-300">
                <Clock className="w-3.5 h-3.5 text-cyan-400" />
                <span>{formatTime(timeLeft)}</span>
              </div>
            )}

            <button
              onClick={onClose}
              className="p-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white border border-slate-700 transition"
              title="Close modal"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Content Body: Assessment Questions OR Results Report */}
        <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-6">
          {!isSubmitted ? (
            /* ========================================================= */
            /* QUESTION TAKING VIEW */
            /* ========================================================= */
            <div className="space-y-5">
              {/* Stepper Dots Bar */}
              <div className="flex items-center justify-between gap-1 pb-1">
                {DIAGNOSTIC_QUESTIONS.map((q, idx) => {
                  const isAnswered = selectedAnswers[q.id] !== undefined;
                  const isCurrent = idx === currentIdx;

                  return (
                    <button
                      key={q.id}
                      onClick={() => setCurrentIdx(idx)}
                      className={`flex-1 h-2 rounded-full transition-all ${
                        isCurrent
                          ? 'bg-purple-500 ring-2 ring-purple-400/40'
                          : isAnswered
                          ? 'bg-emerald-500'
                          : 'bg-slate-800'
                      }`}
                      title={`Question ${idx + 1} (${q.pillarLabel})`}
                    />
                  );
                })}
              </div>

              {/* Question Card */}
              <div className="bg-slate-950 rounded-2xl p-5 sm:p-6 border border-slate-800 space-y-4">
                <div className="flex items-center justify-between text-xs">
                  <span className="px-2.5 py-1 rounded-full bg-slate-800 text-purple-300 font-semibold font-mono">
                    Question {currentIdx + 1} of 10 &bull; {currentQ.pillarLabel}
                  </span>
                  <span className="text-slate-500 font-mono text-[11px]">
                    {Object.keys(selectedAnswers).length} / 10 Answered
                  </span>
                </div>

                <h3 className="text-base sm:text-xl font-bold text-white leading-relaxed">
                  <MathText text={currentQ.question} />
                </h3>

                {/* Multiple Choice Options */}
                <div className="space-y-2.5 pt-2">
                  {currentQ.options.map((opt, optIdx) => {
                    const isSelected = selectedAnswers[currentQ.id] === optIdx;

                    return (
                      <button
                        key={optIdx}
                        onClick={() => handleSelectOption(currentQ.id, optIdx)}
                        className={`w-full p-3.5 rounded-xl border text-left transition flex items-start gap-3 ${
                          isSelected
                            ? 'bg-purple-600/20 text-white border-purple-500 shadow-md shadow-purple-600/10'
                            : 'bg-slate-900 hover:bg-slate-850 text-slate-300 border-slate-800 hover:border-slate-700'
                        }`}
                      >
                        <span className={`w-6 h-6 rounded-lg text-xs font-mono font-bold flex items-center justify-center shrink-0 mt-0.5 ${
                          isSelected ? 'bg-purple-600 text-white' : 'bg-slate-800 text-slate-400'
                        }`}>
                          {String.fromCharCode(65 + optIdx)}
                        </span>
                        <div className="text-xs sm:text-sm leading-relaxed">
                          <MathText text={opt} />
                        </div>
                      </button>
                    );
                  })}
                </div>
              </div>

              {/* Bottom Question Navigation Controls */}
              <div className="flex items-center justify-between pt-2">
                <button
                  onClick={() => setCurrentIdx(prev => Math.max(0, prev - 1))}
                  disabled={currentIdx === 0}
                  className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 disabled:opacity-30 text-white text-xs font-medium transition"
                >
                  Previous
                </button>

                {currentIdx < DIAGNOSTIC_QUESTIONS.length - 1 ? (
                  <button
                    onClick={() => setCurrentIdx(prev => Math.min(DIAGNOSTIC_QUESTIONS.length - 1, prev + 1))}
                    className="px-5 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-white text-xs font-semibold shadow-md shadow-purple-600/25 transition flex items-center gap-1.5"
                  >
                    <span>Next</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </button>
                ) : (
                  <button
                    onClick={() => setIsSubmitted(true)}
                    className="px-6 py-2 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white text-xs font-bold shadow-lg shadow-emerald-600/25 transition flex items-center gap-2"
                  >
                    <Award className="w-4 h-4" />
                    <span>Submit & Generate Diagnostic Report</span>
                  </button>
                )}
              </div>
            </div>
          ) : (
            /* ========================================================= */
            /* RESULTS & RADAR SKILL REPORT VIEW */
            /* ========================================================= */
            <div className="space-y-6 animate-fadeIn">
              {/* Score & Tier Banner */}
              <div className="bg-gradient-to-br from-slate-900 to-slate-950 p-6 rounded-3xl border border-slate-800 flex flex-col sm:flex-row items-center justify-between gap-6 shadow-xl">
                <div className="flex items-center gap-4">
                  <div className="w-16 h-16 rounded-2xl bg-purple-500/10 border border-purple-500/30 flex items-center justify-center shrink-0">
                    <Award className="w-8 h-8 text-purple-400" />
                  </div>
                  <div className="space-y-1">
                    <span className={`text-[11px] font-bold uppercase tracking-wider px-3 py-0.5 rounded-full border ${scores.tierBadge}`}>
                      {scores.tier}
                    </span>
                    <h3 className="text-2xl sm:text-3xl font-black text-white">
                      {scores.totalCorrect} / 10 Correct ({scores.percent}%)
                    </h3>
                    <p className="text-xs text-slate-400">
                      Completed in {formatTime(600 - timeLeft)} &bull; Comprehensive skill profile generated
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-2 shrink-0">
                  <button
                    onClick={handleCopyReport}
                    className="px-3.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 text-xs font-medium transition flex items-center gap-1.5"
                  >
                    {copiedResult ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Share2 className="w-3.5 h-3.5" />}
                    <span>{copiedResult ? 'Report Copied!' : 'Share Score'}</span>
                  </button>

                  <button
                    onClick={handleReset}
                    className="px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-white text-xs font-semibold transition flex items-center gap-1.5 shadow-md shadow-purple-600/25"
                  >
                    <RotateCcw className="w-3.5 h-3.5" />
                    <span>Retake Diagnostic</span>
                  </button>
                </div>
              </div>

              {/* 4 Pillars Breakdown & Visual SVG Radar / Bar Graphic */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* Visual SVG Radar Web */}
                <div className="bg-slate-950 p-5 rounded-2xl border border-slate-800 flex flex-col items-center justify-center space-y-2">
                  <span className="text-xs font-bold text-slate-300 uppercase tracking-wider self-start flex items-center gap-1.5">
                    <Compass className="w-3.5 h-3.5 text-purple-400" />
                    AI Knowledge Radar Chart
                  </span>

                  <svg className="w-60 h-60" viewBox="-120 -120 240 240">
                    {/* Concentric Radar Rings */}
                    {[0.25, 0.5, 0.75, 1.0].map(r => (
                      <circle
                        key={`ring-${r}`}
                        cx="0"
                        cy="0"
                        r={r * 80}
                        fill="none"
                        stroke="rgba(255, 255, 255, 0.08)"
                        strokeDasharray="3,3"
                      />
                    ))}

                    {/* Radar Cross Axes */}
                    <line x1="0" y1="-85" x2="0" y2="85" stroke="rgba(255, 255, 255, 0.1)" />
                    <line x1="-85" y1="0" x2="85" y2="0" stroke="rgba(255, 255, 255, 0.1)" />

                    {/* Axis Labels */}
                    <text x="0" y="-92" textAnchor="middle" fill="#c084fc" fontSize="9" fontWeight="bold">Math</text>
                    <text x="96" y="3" textAnchor="start" fill="#38bdf8" fontSize="9" fontWeight="bold">ML</text>
                    <text x="0" y="100" textAnchor="middle" fill="#fb7185" fontSize="9" fontWeight="bold">Deep Learning</text>
                    <text x="-96" y="3" textAnchor="end" fill="#34d399" fontSize="9" fontWeight="bold">GenAI</text>

                    {/* Computed User Polygon */}
                    {(() => {
                      const pMath = scores.pillars.math.correct / scores.pillars.math.total;
                      const pML = scores.pillars.ml.correct / scores.pillars.ml.total;
                      const pDL = scores.pillars.dl.correct / scores.pillars.dl.total;
                      const pGenAI = scores.pillars.genai.correct / scores.pillars.genai.total;

                      const ptMath = [0, -Math.max(10, pMath * 80)];
                      const ptML = [Math.max(10, pML * 80), 0];
                      const ptDL = [0, Math.max(10, pDL * 80)];
                      const ptGenAI = [-Math.max(10, pGenAI * 80), 0];

                      const pointsStr = `${ptMath[0]},${ptMath[1]} ${ptML[0]},${ptML[1]} ${ptDL[0]},${ptDL[1]} ${ptGenAI[0]},${ptGenAI[1]}`;

                      return (
                        <>
                          <polygon
                            points={pointsStr}
                            fill="rgba(168, 85, 247, 0.25)"
                            stroke="#c084fc"
                            strokeWidth="2.5"
                          />
                          {[ptMath, ptML, ptDL, ptGenAI].map((pt, i) => (
                            <circle key={i} cx={pt[0]} cy={pt[1]} r="4" fill="#ffffff" stroke="#c084fc" strokeWidth="2" />
                          ))}
                        </>
                      );
                    })()}
                  </svg>
                </div>

                {/* Pillar Score Bars */}
                <div className="bg-slate-950 p-5 rounded-2xl border border-slate-800 space-y-4 flex flex-col justify-center">
                  <span className="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
                    <TrendingUp className="w-3.5 h-3.5 text-emerald-400" />
                    Pillar Mastery Percentages
                  </span>

                  {Object.entries(scores.pillars).map(([k, p]) => {
                    const pct = Math.round((p.correct / p.total) * 100);

                    return (
                      <div key={k} className="space-y-1">
                        <div className="flex justify-between text-xs">
                          <span className="text-slate-300 font-medium">{p.label}</span>
                          <span className="font-mono text-purple-300 font-bold">{p.correct}/{p.total} ({pct}%)</span>
                        </div>
                        <div className="h-2 w-full bg-slate-900 rounded-full overflow-hidden">
                          <div 
                            className="h-full bg-gradient-to-r from-purple-500 to-cyan-400 rounded-full transition-all duration-500"
                            style={{ width: `${pct}%` }}
                          />
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Detailed Question Review List */}
              <div className="space-y-3">
                <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
                  <BookOpen className="w-3.5 h-3.5 text-cyan-400" />
                  Detailed Question Explanations & Proofs:
                </h4>

                <div className="space-y-3">
                  {DIAGNOSTIC_QUESTIONS.map((q, idx) => {
                    const userAns = selectedAnswers[q.id];
                    const isCorrect = userAns === q.correctIndex;

                    return (
                      <div 
                        key={q.id}
                        className={`p-4 rounded-2xl border text-xs space-y-2 ${
                          isCorrect 
                            ? 'bg-slate-950/70 border-emerald-500/30' 
                            : 'bg-slate-950/70 border-rose-500/30'
                        }`}
                      >
                        <div className="flex items-center justify-between">
                          <span className="font-mono text-slate-400 font-bold">
                            Question #{idx + 1} &bull; {q.pillarLabel}
                          </span>
                          <span className={`px-2 py-0.5 rounded-full font-mono font-bold text-[10px] ${
                            isCorrect ? 'bg-emerald-500/20 text-emerald-300' : 'bg-rose-500/20 text-rose-300'
                          }`}>
                            {isCorrect ? 'Correct' : 'Needs Review'}
                          </span>
                        </div>

                        <p className="font-semibold text-white text-xs sm:text-sm">
                          <MathText text={q.question} />
                        </p>

                        <div className="text-slate-300 space-y-1 pt-1 border-t border-slate-800/80">
                          <div>
                            <span className="text-slate-500">Correct Answer: </span>
                            <strong className="text-emerald-400">
                              <MathText text={q.options[q.correctIndex]} />
                            </strong>
                          </div>
                          {!isCorrect && userAns !== undefined && (
                            <div>
                              <span className="text-slate-500">Your Choice: </span>
                              <span className="text-rose-400">
                                <MathText text={q.options[userAns]} />
                              </span>
                            </div>
                          )}
                        </div>

                        <div className="p-3 bg-slate-900 rounded-xl border border-slate-800 text-[11px] text-slate-400 leading-relaxed">
                          <strong className="text-purple-300 block mb-0.5">Proof / Explanation:</strong>
                          <MathText text={q.explanation} />
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
