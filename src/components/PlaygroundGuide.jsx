import React, { useState } from 'react';
import { 
  Gamepad2, 
  Eye, 
  Lightbulb, 
  ChevronDown, 
  ChevronUp, 
  Lock, 
  Unlock, 
  Sparkles, 
  Brain, 
  Award, 
  ArrowRight,
  BookOpen,
  CheckCircle2
} from 'lucide-react';
import KaTeXRenderer from './KaTeXRenderer';

export const PLAYGROUND_GUIDES = {
  attention: {
    title: 'Multi-Head Attention Matrix Simulator',
    subtitle: 'Understand how query-key dot products dynamically route information between tokens.',
    steps: [
      {
        num: 1,
        title: 'Choose a Coreference Sentence',
        detail: 'Select the preset: "The animal didn\'t cross the street because it was too tired".'
      },
      {
        num: 2,
        title: 'Switch Attention Heads',
        detail: 'Toggle between Head 1 (Coreference), Head 2 (Syntactic), and Head 3 (Semantic) to see different learned subspace projections.'
      },
      {
        num: 3,
        title: 'Vary Softmax Temperature (T)',
        detail: 'Drag the Temperature slider from 0.2 (extremely sharp argmax) up to 2.0 (uniform hazy distribution).'
      }
    ],
    observations: [
      'In Head 1, look at the row for "it": notice how it attends heavily to "animal" rather than "street".',
      'When Temperature T < 0.5, the softmax distribution sharpens into near-binary choices (winner-take-all).',
      'When T > 1.5, attention weights dissolve into an equal blur across all tokens, losing semantic focus.',
      'Notice the diagonal values: Head 4 focuses almost entirely on self-tokens, acting as local identity preservation.'
    ],
    challenge: 'Why can\'t a single attention head simultaneously capture grammatical syntax AND long-range pronoun resolution? Why do modern LLMs (e.g. Llama 3) use 32 to 128 heads?',
    conclusion: {
      mathFormula: '$$\\text{MHA}(Q, K, V) = \\text{Concat}(\\text{head}_1, \\dots, \\text{head}_h) W^O, \\quad \\text{head}_i = \\text{softmax}\\left(\\frac{Q W_i^Q (K W_i^K)^T}{\\sqrt{d_k}}\\right) V W_i^V$$',
      mathExplanation: 'A single softmax matrix over QK^T can only create one probability distribution per token. If a token needs to connect with its direct grammatical verb AND resolve its antecedent pronoun 50 tokens earlier, a single head must compromise. Multi-Head Attention projects Q, K, and V into h distinct low-dimensional subspaces, allowing parallel representation of syntax, coreference, and facts simultaneously.',
      productionImpact: 'Modern LLMs (GPT-4, Claude 3.5, Llama 3) allocate heads specialized in: induction heads (in-context pattern copying), code delimiter matching, and conversational state tracking.',
      interviewRule: 'Rule of Thumb: Self-Attention allows tokens to look at each other; Multi-Head Attention allows them to look at each other in multiple different ways at the same time.'
    }
  },

  gradient: {
    title: 'Gradient Descent & Optimizer Physics Sandbox',
    subtitle: 'Explore why modern deep learning abandoned plain SGD for adaptive momentum optimizers.',
    steps: [
      {
        num: 1,
        title: 'Choose an Ill-Conditioned Valley',
        detail: 'Select the "Convex Paraboloid (Ill-conditioned)" or "Rosenbrock Banana Valley" landscape.'
      },
      {
        num: 2,
        title: 'Drop the Particle',
        detail: 'Click anywhere on the 2D contour map away from the center to set the starting position.'
      },
      {
        num: 3,
        title: 'Compare Plain SGD vs. AdamW',
        detail: 'First run Plain SGD, observe the trajectory, then hit Reset, switch to AdamW, and run again.'
      }
    ],
    observations: [
      'In the ill-conditioned valley, Plain SGD oscillates violently back and forth across the steep ravine walls with almost zero forward progress down the gentle floor.',
      'Momentum accumulates velocity along consistent directions, damping perpendicular oscillations and speeding along the valley.',
      'AdamW rescales step sizes adaptively per dimension, heading straight for the global minimum (0,0) in a smooth arc.'
    ],
    challenge: 'Why does Plain SGD take hundreds of iterations to traverse a narrow valley, and how does dividing gradients by sqrt(v_t) solve this mathematically?',
    conclusion: {
      mathFormula: '$$m_t = \\beta_1 m_{t-1} + (1 - \\beta_1) g_t, \\quad v_t = \\beta_2 v_{t-1} + (1 - \\beta_2) g_t^2, \\quad \\theta_t = \\theta_{t-1} - \\frac{\\eta}{\\sqrt{\\hat{v}_t} + \\epsilon} \\hat{m}_t - \\eta \\lambda \\theta_{t-1}$$',
      mathExplanation: 'When the Hessian matrix has an extreme condition number kappa = lambda_max / lambda_min >> 1, gradients along the steep direction are massive, while gradients along the ravine floor are miniscule. Plain SGD requires a tiny learning rate to avoid exploding along the steep axis, which makes progress along the flat axis painfully slow. AdamW divides by sqrt(v_t), normalizing gradient scales across all axes!',
      productionImpact: 'All modern frontier LLMs are trained using AdamW. Decoupling weight decay directly from gradient updates (Loschilov & Hutter) prevents L2 regularization from degrading adaptive learning rates.',
      interviewRule: 'Rule of Thumb: Momentum provides velocity through flat areas and escapes local saddle points; AdamW equalizes step sizes across steep ravines and flat plateaus.'
    }
  },

  neural: {
    title: 'Neural Network & Backpropagation Playground',
    subtitle: 'Watch weights update in real-time and observe why depth and non-linearities are mandatory.',
    steps: [
      {
        num: 1,
        title: 'Select XOR or Concentric Rings',
        detail: 'Pick the XOR or Rings dataset (classes cannot be separated by a single straight line).'
      },
      {
        num: 2,
        title: 'Test Zero Hidden Layers',
        detail: 'Set Hidden Layers to 0 (a single Perceptron) and click "Start Training". Observe the accuracy cap.'
      },
      {
        num: 3,
        title: 'Add Hidden Layers + ReLU',
        detail: 'Add 1 or 2 hidden layers (4–6 neurons each) with ReLU activation, then train again.'
      }
    ],
    observations: [
      'With 0 hidden layers, the decision boundary is strictly a straight flat plane. Accuracy remains stuck at ~50%.',
      'With hidden layers enabled, the decision boundary warps, bends, and curls into curves enclosing the target points.',
      'Notice weight line thickness: connections that learn strong features thicken and glow with higher gradient magnitudes.'
    ],
    challenge: 'Why is a 100-layer neural network with ONLY linear activations mathematically identical to a 1-layer model? What does ReLU actually do geometrically?',
    conclusion: {
      mathFormula: '$$W_2(W_1 x + b_1) + b_2 = (W_2 W_1) x + (W_2 b_1 + b_2) = W_{\\text{combined}} x + b_{\\text{combined}}$$ \\quad \\text{vs.} \\quad f(x) = \\max(0, W x + b)',
      mathExplanation: 'Matrix multiplication is strictly associative and linear. The composition of any number of linear transformations is always another single linear transformation. Non-linear activation functions like ReLU (max(0, z)) act as geometric hinge folds in space, folding and warping the coordinate grid so non-linear clusters become linearly separable in the final layer.',
      productionImpact: 'This is the Universal Approximation Theorem in action: with at least one non-linear hidden layer of sufficient width, a neural network can approximate any continuous function.',
      interviewRule: 'Rule of Thumb: Deep networks without non-linearities are just expensive linear regressions. Depth + non-linearities = hierarchical feature extraction.'
    }
  },

  tokenizer: {
    title: 'BPE Tokenizer & Word Embedding Projection',
    subtitle: 'Understand how subword tokenization prevents OOV and how vector arithmetic captures semantic concepts.',
    steps: [
      {
        num: 1,
        title: 'Test Frequent Subwords',
        detail: 'Type a sentence with repeating prefixes/suffixes (e.g. "unbearable and unbelievable") and click "Step Merge".'
      },
      {
        num: 2,
        title: 'Examine Token IDs',
        detail: 'Observe how single characters merge into pairs, and pairs merge into full subword tokens.'
      },
      {
        num: 3,
        title: 'Explore 2D Embedding Arithmetic',
        detail: 'In the PCA vector projection canvas, click vector combinations like King, Man, and Woman.'
      }
    ],
    observations: [
      'Common prefixes ("un-") and suffixes ("-able") quickly fuse into unified token IDs, reducing total sequence length.',
      'Rare or typo words are gracefully broken down into smaller pieces or individual characters rather than failing.',
      'In the vector space, the directional vector from "Man" to "Woman" is nearly parallel to the vector from "King" to "Queen".'
    ],
    challenge: 'Why do modern LLMs use Byte-Pair Encoding rather than whole-word tokenization? How does vector subtraction preserve semantic relationships?',
    conclusion: {
      mathFormula: '$$\\mathbf{v}_{\\text{King}} - \\mathbf{v}_{\\text{Man}} + \\mathbf{v}_{\\text{Woman}} \\approx \\mathbf{v}_{\\text{Queen}}, \\quad \\text{PMI}(w_i, w_j) = \\log \\frac{P(w_i, w_j)}{P(w_i) P(w_j)}$$',
      mathExplanation: 'Whole-word vocabularies explode to millions of words and crash on unseen words (Out-of-Vocabulary). Character-level tokenization produces sequences that are too long for attention O(N^2). BPE finds the optimal sweet spot: common words are 1 token, rare words are composed of subwords, and unknown strings fall back to bytes. Neural embeddings optimize dot products to match pointwise mutual information (PMI), making linear spatial offsets correspond directly to semantic relationships.',
      productionImpact: 'All frontier models (GPT-4o, Claude 3.5, Llama 3) use Byte-level BPE with 100k–128k token vocabularies. Larger vocabularies compress text into fewer tokens, cutting inference latency.',
      interviewRule: 'Rule of Thumb: BPE guarantees 0% Out-Of-Vocabulary rate; Word Embeddings map semantic similarity to spatial cosine distance.'
    }
  },

  rag: {
    title: '5-Stage RAG Pipeline Visualizer',
    subtitle: 'Inspect how enterprise Retrieval-Augmented Generation grounds LLMs in external knowledge.',
    steps: [
      {
        num: 1,
        title: 'Select a Query Scenario',
        detail: 'Choose between a Technical Query, Financial Query, or Medical Domain Question.'
      },
      {
        num: 2,
        title: 'Step Through the 5 Pipeline Stages',
        detail: 'Click through Ingestion → Chunking → Dense Vector Search → Cross-Encoder Reranking → Grounded LLM Generation.'
      },
      {
        num: 3,
        title: 'Compare Bi-Encoder vs. Cross-Encoder',
        detail: 'Observe how Stage 3 retrieves broad candidates while Stage 4 re-scores exact semantic matches.'
      }
    ],
    observations: [
      'If chunks are too small (<100 tokens), sentences lose surrounding context and return low semantic scores.',
      'If chunks are too large (>1000 tokens), the vector embedding becomes diluted and retrieval precision plummets.',
      'Notice that Stage 4 (Reranker) often reorders the candidates, moving the most precise answer to Rank #1 before prompt injection.'
    ],
    challenge: 'Why does vector database cosine search alone frequently retrieve irrelevant chunks? Why is a Cross-Encoder reranker needed before the final LLM?',
    conclusion: {
      mathFormula: '$$\\text{Bi-Encoder: } \\cos(E(q), E(d)) \\quad \\text{vs.} \\quad \\text{Cross-Encoder: } \\text{Transformer}([q; \\text{SEP}; d])$$',
      mathExplanation: 'Bi-encoders embed the query and document independently into single vector points without letting query tokens cross-attend to document tokens. This allows fast approximate search (HNSW over millions of docs in 5ms), but loses fine-grained nuances. Cross-encoders feed query and document together through full multi-head self-attention, capturing pairwise token interactions at the cost of higher compute.',
      productionImpact: 'State-of-the-art enterprise RAG systems use a two-tiered architecture: fast Bi-Encoder retrieval to fetch top-50 candidate chunks, followed by a Cross-Encoder (e.g. Cohere Rerank / BGE-Reranker) to filter the top-3 chunks for the LLM.',
      interviewRule: 'Rule of Thumb: Bi-encoders are for scalable retrieval across millions; Cross-encoders are for pinpoint reranking across dozens.'
    }
  },

  lora: {
    title: 'LoRA vs. Full Fine-Tuning Rank Explorer',
    subtitle: 'See how Low-Rank Adaptation democratizes fine-tuning of 70B parameter models on consumer GPUs.',
    steps: [
      {
        num: 1,
        title: 'Pick a Base Foundation Model',
        detail: 'Select Llama 3 70B, Llama 3 8B, or Mistral 7B from the model selector.'
      },
      {
        num: 2,
        title: 'Adjust Rank (r)',
        detail: 'Drag the rank slider from r=2 to r=64 and watch parameter count and VRAM calculations update in real-time.'
      },
      {
        num: 3,
        title: 'Toggle Target Attention Matrices',
        detail: 'Select which projection matrices to adapt (q_proj, k_proj, v_proj, o_proj, gate_proj).'
      }
    ],
    observations: [
      'At rank r=8, trainable parameters drop by over 99% compared to full fine-tuning (e.g., from 70B down to ~150M).',
      'Full Fine-Tuning requires massive VRAM for optimizer states (16 bytes per param in AdamW), whereas LoRA only stores optimizer states for the tiny A and B matrices.',
      'Notice Matrix B is initialized to all zeros and Matrix A is Gaussian, guaranteeing Delta W = 0 at training step 0.'
    ],
    challenge: 'Why can a tiny low-rank matrix decomposition W = W_0 + (alpha/r)*BA match full fine-tuning performance on complex downstream tasks?',
    conclusion: {
      mathFormula: '$$W = W_0 + \\Delta W = W_0 + \\frac{\\alpha}{r} B A, \\quad B \\in \\mathbb{R}^{d \\times r}, \\; A \\in \\mathbb{R}^{r \\times k}, \\quad r \\ll \\min(d, k)$$',
      mathExplanation: 'Aghajanyan et al. (2020) demonstrated that over-parametrized neural networks possess a remarkably low intrinsic dimension. The task-specific weight update Delta W does not require full rank; its effective degrees of freedom lie on a small sub-manifold. Setting r=8 or r=16 captures >95% of task performance while reducing parameter storage by 100x to 1000x.',
      productionImpact: 'In production, serving one base model with 50 different LoRA adapters saves millions of dollars in GPU cluster hosting costs. LoRA adapters can be merged directly into W_0 for zero-latency inference (W = W_0 + (alpha/r)*BA).',
      interviewRule: 'Rule of Thumb: Full fine-tuning updates the whole brain; LoRA trains a tiny specialized low-rank coprocessor while keeping the original brain frozen.'
    }
  },

  prompting: {
    title: 'Prompting & System 2 Reasoning Arena',
    subtitle: 'Witness how test-time reasoning compute transforms LLM accuracy on logic traps and arithmetic problems.',
    steps: [
      {
        num: 1,
        title: 'Select the Math Constraint Challenge',
        detail: 'Choose the "Math Constraint Trap" involving round-trip speeds (240 miles in 4 hrs outbound, 20 mph slower return).'
      },
      {
        num: 2,
        title: 'Execute Zero-Shot Direct',
        detail: 'Run Zero-Shot and observe the quick response and the common cognitive fallacy it triggers.'
      },
      {
        num: 3,
        title: 'Execute Chain-of-Thought or Tree-of-Thoughts',
        detail: 'Switch to Chain-of-Thought (CoT) and watch the step-by-step <think> trace derive the mathematically sound answer.'
      }
    ],
    observations: [
      'Zero-Shot falls directly into the classic arithmetic trap: computing the simple mean of speeds ((60+40)/2 = 50 mph) instead of distance over total time.',
      'CoT allocates intermediate reasoning tokens, computing return time (6 hrs), total time (10 hrs), and correct average speed (48 mph).',
      'Tree-of-Thoughts actively evaluates multiple branches, detects the arithmetic mean fallacy, and prunes the invalid branch.'
    ],
    challenge: 'Why do LLMs fail on simple math when answering directly, but succeed when allowed to generate reasoning tokens first?',
    conclusion: {
      mathFormula: '$$\\mathcal{O}(L \\cdot d^2) \\text{ compute per token} \\quad \\implies \\quad \\text{Compute}_{\\text{Test}} \\propto N_{\\text{reasoning\\_tokens}}$$ \\quad \\text{Harmonic Mean: } \\frac{2 v_1 v_2}{v_1 + v_2}',
      mathExplanation: 'An autoregressive transformer executes a fixed computational budget per token. When asked to produce the answer immediately, it must resolve the entire multi-step problem in a single forward pass without intermediate memory. Generating reasoning tokens allows the model to write intermediate state into the context window, essentially converting the transformer from a shallow fixed circuit into a multi-step Turing machine.',
      productionImpact: 'This is the foundation of modern reasoning frontiers (OpenAI o1/o3, DeepSeek-R1). Allocating more tokens to reasoning at inference time yields exponential gains on PhD-level STEM benchmarks without increasing model parameter size.',
      interviewRule: 'Rule of Thumb: Prompt tokens are the question; Reasoning tokens are the working scratchpad; Completion tokens are the final answer.'
    }
  }
};

export default function PlaygroundGuide({ activeTab }) {
  const [isRevealed, setIsRevealed] = useState(false);
  const [isExpanded, setIsExpanded] = useState(true);

  const guide = PLAYGROUND_GUIDES[activeTab];
  if (!guide) return null;

  return (
    <div className="bg-slate-900/90 border border-indigo-500/30 rounded-2xl overflow-hidden shadow-lg shadow-indigo-950/20 mb-6 transition-all">
      {/* Header Banner */}
      <div 
        onClick={() => setIsExpanded(!isExpanded)}
        className="p-4 sm:p-5 bg-gradient-to-r from-indigo-950/60 via-slate-900 to-slate-950 flex items-center justify-between cursor-pointer border-b border-indigo-500/20 select-none group"
      >
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-indigo-600/20 text-indigo-400 border border-indigo-500/40 flex items-center justify-center shrink-0 group-hover:scale-105 transition-transform">
            <Gamepad2 className="w-5 h-5 text-indigo-400" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-[10px] font-bold uppercase tracking-wider text-indigo-400 bg-indigo-500/10 px-2 py-0.5 rounded-full border border-indigo-500/30">
                Interactive Playbook &amp; Insights
              </span>
              <span className="text-xs text-slate-400 hidden sm:inline">&bull; First-time guide</span>
            </div>
            <h3 className="text-sm sm:text-base font-bold text-white tracking-tight mt-0.5">
              How to Play &amp; What to Observe: {guide.title}
            </h3>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <span className="text-xs text-slate-400 hidden md:inline font-medium">
            {isExpanded ? 'Collapse Guide' : 'Expand Guide'}
          </span>
          <div className="w-7 h-7 rounded-lg bg-slate-800 text-slate-300 flex items-center justify-center">
            {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
          </div>
        </div>
      </div>

      {/* Guide Body */}
      {isExpanded && (
        <div className="p-4 sm:p-6 space-y-6">
          {/* Top Grid: How to Play vs What to Observe */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            {/* Column 1: How to Play (Step-by-Step) */}
            <div className="bg-slate-950/70 border border-slate-800/80 rounded-xl p-4 space-y-3">
              <h4 className="text-xs font-bold uppercase tracking-wider text-cyan-300 flex items-center gap-1.5 font-mono">
                <Gamepad2 className="w-4 h-4 text-cyan-400" />
                <span>How to Play (Experiment Steps)</span>
              </h4>
              <div className="space-y-2.5">
                {guide.steps.map((step) => (
                  <div key={step.num} className="flex items-start gap-2.5 text-xs">
                    <span className="w-5 h-5 rounded-full bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 font-bold flex items-center justify-center shrink-0 mt-0.5 font-mono text-[11px]">
                      {step.num}
                    </span>
                    <div>
                      <span className="font-semibold text-white block">{step.title}</span>
                      <p className="text-slate-400 mt-0.5 leading-relaxed">{step.detail}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Column 2: What to Observe (Key Signals) */}
            <div className="bg-slate-950/70 border border-slate-800/80 rounded-xl p-4 space-y-3">
              <h4 className="text-xs font-bold uppercase tracking-wider text-amber-300 flex items-center gap-1.5 font-mono">
                <Eye className="w-4 h-4 text-amber-400" />
                <span>What to Observe (Visual Clues)</span>
              </h4>
              <ul className="space-y-2 text-xs">
                {guide.observations.map((obs, idx) => (
                  <li key={idx} className="flex items-start gap-2 text-slate-300 leading-relaxed">
                    <span className="w-1.5 h-1.5 rounded-full bg-amber-400 shrink-0 mt-1.5" />
                    <span>{obs}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          {/* Bottom Card: The Mental Challenge & Hidden Theoretical Conclusion */}
          <div className="bg-gradient-to-br from-indigo-950/40 to-slate-950 border border-indigo-500/30 rounded-xl p-4 sm:p-5 space-y-4">
            <div className="space-y-1.5">
              <span className="text-[11px] font-bold uppercase tracking-wider text-purple-400 font-mono flex items-center gap-1.5">
                <Brain className="w-4 h-4 text-purple-400" />
                <span>Theoretical Mystery &amp; Challenge</span>
              </span>
              <p className="text-xs sm:text-sm font-semibold text-slate-100 leading-relaxed italic bg-purple-950/20 p-3 rounded-lg border border-purple-500/20">
                &ldquo;{guide.challenge}&rdquo;
              </p>
            </div>

            {/* Reveal / Hide Toggle Button */}
            <div className="pt-1">
              {!isRevealed ? (
                <button
                  onClick={() => setIsRevealed(true)}
                  className="w-full sm:w-auto px-4 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 active:scale-[0.99] text-white font-semibold text-xs transition flex items-center justify-center gap-2 shadow-md shadow-indigo-600/30"
                >
                  <Unlock className="w-4 h-4 text-indigo-200" />
                  <span>Think about it, then click to Reveal Core Takeaway &amp; Mathematical Conclusion 💡</span>
                </button>
              ) : (
                <button
                  onClick={() => setIsRevealed(false)}
                  className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white border border-slate-700 text-xs font-medium transition flex items-center gap-1.5"
                >
                  <Lock className="w-3.5 h-3.5" />
                  <span>Hide Conclusion</span>
                </button>
              )}
            </div>

            {/* Revealed Rich Takeaway Section */}
            {isRevealed && (
              <div className="pt-4 border-t border-indigo-500/20 space-y-4 animate-fadeIn">
                <div className="flex items-center gap-2 text-xs font-bold text-emerald-300 uppercase tracking-wider font-mono">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                  <span>Mathematical Proof &amp; Deep Takeaways</span>
                </div>

                {/* Mathematical Formulation */}
                {guide.conclusion.mathFormula && (
                  <div className="p-3.5 bg-slate-950 rounded-xl border border-indigo-500/30 overflow-x-auto">
                    <span className="text-[10px] font-mono text-indigo-400 block mb-1 uppercase">Underlying Mathematical Formulation:</span>
                    <KaTeXRenderer math={guide.conclusion.mathFormula} block={true} />
                  </div>
                )}

                {/* Mathematical Justification */}
                <div className="text-xs sm:text-sm text-slate-300 leading-relaxed bg-slate-950/80 p-3.5 rounded-xl border border-slate-800">
                  <span className="font-semibold text-indigo-300 block mb-1">Why It Works Mathematically:</span>
                  {guide.conclusion.mathExplanation}
                </div>

                {/* Production Impact */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                  <div className="p-3 bg-slate-950/90 rounded-xl border border-slate-800">
                    <span className="font-bold text-amber-300 block mb-1 flex items-center gap-1">
                      <Sparkles className="w-3.5 h-3.5 text-amber-400" />
                      Production &amp; Frontier Impact:
                    </span>
                    <p className="text-slate-400 leading-relaxed">{guide.conclusion.productionImpact}</p>
                  </div>

                  <div className="p-3 bg-emerald-950/20 rounded-xl border border-emerald-500/30">
                    <span className="font-bold text-emerald-300 block mb-1 flex items-center gap-1">
                      <Award className="w-3.5 h-3.5 text-emerald-400" />
                      Interview Takeaway Rule:
                    </span>
                    <p className="text-emerald-200/90 font-medium leading-relaxed">{guide.conclusion.interviewRule}</p>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
