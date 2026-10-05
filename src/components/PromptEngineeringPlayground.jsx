import React, { useState, useEffect, useRef } from 'react';
import { 
  Sparkles, 
  Play, 
  RotateCcw, 
  Terminal, 
  Brain, 
  Wrench, 
  GitBranch, 
  Copy, 
  Check, 
  HelpCircle, 
  Sliders, 
  ChevronRight,
  Flame,
  Zap,
  Layers,
  ArrowRight
} from 'lucide-react';
import KaTeXRenderer from './KaTeXRenderer';

const PROMPT_STRATEGIES = [
  {
    id: 'zero_shot',
    name: 'Zero-Shot Direct',
    desc: 'The model receives instructions with no examples. Relies purely on internal pre-trained representations.',
    color: 'indigo'
  },
  {
    id: 'few_shot',
    name: 'Few-Shot (In-Context)',
    desc: 'Provides 2–3 demonstrations of input-output patterns to anchor formatting and domain constraints.',
    color: 'blue'
  },
  {
    id: 'cot',
    name: 'Chain-of-Thought (CoT)',
    desc: 'Injects "Let\'s think step-by-step" or explicit rationales, unlocking multi-step deduction capabilities.',
    color: 'emerald'
  },
  {
    id: 'react',
    name: 'ReAct (Reason + Act)',
    desc: 'Iterative Thought → Action (tool call) → Observation loop for dynamic external environment grounding.',
    color: 'amber'
  },
  {
    id: 'tot',
    name: 'Tree-of-Thoughts (ToT)',
    desc: 'System 2 branching search: explores multiple reasoning hypotheses, scores candidate steps, and backtracks.',
    color: 'rose'
  }
];

const PRESET_CHALLENGES = {
  math: {
    title: 'Multi-Step Math & Constraint Problem',
    problem: 'A train travels 240 miles in 4 hours. On the return trip, it encounters bad weather and its speed is reduced by 20 mph. How long does the return trip take, and what is its average speed across the round trip?',
    prompts: {
      zero_shot: 'Calculate the return trip duration and round-trip average speed for a train traveling 240 miles in 4 hours, where return speed is reduced by 20 mph.',
      few_shot: `Example 1:
Q: A car travels 100 miles in 2 hours. Return speed drops by 10 mph. Return time?
A: Outbound speed = 100 / 2 = 50 mph. Return speed = 50 - 10 = 40 mph. Return time = 100 / 40 = 2.5 hours.

Now solve:
Q: A train travels 240 miles in 4 hours. Return speed drops by 20 mph. Return time and round-trip average speed?
A:`,
      cot: `Solve the following problem. Explain your full step-by-step reasoning before stating the final answer:
A train travels 240 miles in 4 hours. On the return trip, it encounters bad weather and its speed is reduced by 20 mph. How long does the return trip take, and what is the overall average speed across the entire 480-mile round trip?`,
      react: `Answer the question using the Thought -> Action -> Observation loop with available tools [Calculator, WebSearch].
Question: A train travels 240 miles in 4 hours. Return speed drops by 20 mph. Find return duration and total average speed.`,
      tot: `Explore at least 3 distinct calculation pathways for return duration and average speed. Evaluate each step for correctness, discard invalid arithmetic, and verify that average speed is NOT the simple arithmetic mean of the two speeds.`
    },
    outputs: {
      zero_shot: {
        text: 'The return trip takes 6 hours. The average speed is 50 mph.',
        reasoning: 'Outbound speed = 60 mph. Return speed = 40 mph. Return time = 240 / 40 = 6 hours. Average speed = (60 + 40) / 2 = 50 mph.',
        isCorrect: false, // Notice the classic trap! Average speed is total distance / total time = 480 / 10 = 48 mph, NOT 50 mph!
        trapNote: 'Trap triggered! Zero-shot commonly falls into the fallacy of averaging speeds: (60 + 40) / 2 = 50 mph instead of 480 / 10 = 48 mph.'
      },
      few_shot: {
        text: 'Return duration: 6 hours.\nAverage speed: 48 mph.',
        reasoning: 'Outbound: 240 mi / 4 hrs = 60 mph.\nReturn: 60 - 20 = 40 mph. Time = 240 / 40 = 6 hrs.\nRound trip total: 240 + 240 = 480 miles in 4 + 6 = 10 hours.\nAverage speed = 480 / 10 = 48 mph.',
        isCorrect: true
      },
      cot: {
        text: 'Final Answer: The return trip takes 6 hours, and the average speed for the round trip is 48 mph.',
        reasoning: `<think>
1. Identify Outbound Speed:
   v_1 = d / t_1 = 240 / 4 = 60 mph.

2. Determine Return Speed:
   v_2 = v_1 - 20 = 60 - 20 = 40 mph.

3. Calculate Return Duration:
   t_2 = d / v_2 = 240 / 40 = 6 hours.

4. Calculate Round-Trip Average Speed:
   Total Distance = 240 + 240 = 480 miles.
   Total Time = 4 + 6 = 10 hours.
   Average Speed = Total Distance / Total Time = 480 / 10 = 48 mph.
   *Verification check*: Note that Harmonic Mean (2 * v1 * v2) / (v1 + v2) = (2 * 60 * 40) / 100 = 48 mph. Matches!
</think>`,
        isCorrect: true
      },
      react: {
        text: 'The return trip takes 6 hours, and the overall average speed is 48 mph.',
        reasoning: `Thought 1: I need to compute outbound speed from 240 miles in 4 hours.
Action 1: Calculator(240 / 4)
Observation 1: 60.0

Thought 2: Return speed drops by 20 mph, so 60 - 20 = 40 mph. Now I need return time.
Action 2: Calculator(240 / 40)
Observation 2: 6.0

Thought 3: Average speed requires total distance (480 miles) divided by total time (4 + 6 = 10 hours).
Action 3: Calculator(480 / 10)
Observation 3: 48.0

Thought 4: Both figures are verified with exact calculator outputs. Ready to conclude.`,
        isCorrect: true
      },
      tot: {
        text: 'Optimal Branch Selected (Branch 1.2): Return trip = 6.0 hours. Round-trip average speed = 48.0 mph.',
        reasoning: `[Branch 1: Kinematic Time Aggregation] -> Score: 0.98 (Optimal)
├── Step 1: v_out = 60 mph, v_ret = 40 mph
├── Step 2: t_ret = 240 / 40 = 6 hours
└── Step 3: v_avg = 480 / (4 + 6) = 48 mph ✓

[Branch 2: Arithmetic Mean Heuristic] -> Score: 0.12 (Rejected)
├── Step 1: Compute (60 + 40) / 2 = 50 mph
└── Step 2: Evaluator check: Fails harmonic distance conservation. Backtracking...

[Branch 3: Harmonic Mean Formula] -> Score: 0.96 (Valid)
└── Step 1: 2 / (1/60 + 1/40) = 2 / (5/120) = 240 / 5 = 48 mph ✓`,
        isCorrect: true
      }
    }
  },
  logic: {
    title: 'Knights & Knaves Island Logic Puzzle',
    problem: 'On an island, Knights always tell the truth and Knaves always lie. You meet two inhabitants, Alice and Bob. Alice says: "At least one of us is a Knave." What are Alice and Bob?',
    prompts: {
      zero_shot: 'On an island of Knights (truth) and Knaves (liars), Alice says: "At least one of us is a Knave." What are Alice and Bob?',
      few_shot: `Example:
A says: "We are both knaves." If A is knight, statement is false (contradiction). So A is knave, meaning not both are knaves, so B is knight.

Now solve:
Alice says: "At least one of us is a Knave." Who is Alice and who is Bob?`,
      cot: 'Analyze the logic step-by-step using truth tables or proof by contradiction: Alice says "At least one of us is a Knave." Determine their identities.',
      react: 'Determine identities using formal propositional logic tool calls.',
      tot: 'Branch on Hypothesis A (Alice is Knight) vs Hypothesis B (Alice is Knave). Trace contradictions in each branch.'
    },
    outputs: {
      zero_shot: {
        text: 'Alice is a Knight and Bob is a Knave.',
        reasoning: 'If Alice were a Knave, her statement would be false, meaning neither is a Knave (both are Knights), which contradicts Alice being a Knave. Thus Alice is a Knight, so her statement is true, meaning Bob must be the Knave.',
        isCorrect: true
      },
      few_shot: {
        text: 'Alice is a Knight; Bob is a Knave.',
        reasoning: 'Assumption 1: Alice is a Knave -> Statement is false -> Both are Knights (Contradiction: Alice is both Knave and Knight). Hence Alice is Knight. Statement is true -> At least one is knave -> Since Alice is knight, Bob is knave.',
        isCorrect: true
      },
      cot: {
        text: 'Conclusion: Alice is a Knight, and Bob is a Knave.',
        reasoning: `<think>
Let A = 1 if Alice is Knight, 0 if Alice is Knave.
Let B = 1 if Bob is Knight, 0 if Bob is Knave.
Alice's statement S: (A == 0) OR (B == 0).

Case 1: Suppose Alice is a Knave (A = 0).
- By rule, Knaves always lie, so statement S must be False.
- Not(S) = Not((A == 0) OR (B == 0)) = (A == 1) AND (B == 1).
- This asserts A = 1 (Alice is a Knight).
- Contradiction: A cannot simultaneously be 0 and 1!
- Therefore, our initial assumption is false: Alice CANNOT be a Knave.

Case 2: Alice is a Knight (A = 1).
- By rule, Knights always tell the truth, so statement S must be True.
- S is True => (A == 0) OR (B == 0) is True.
- Since A = 1 (A == 0 is False), it strictly follows that (B == 0) must be True.
- Therefore, Bob is a Knave (B = 0).

Both conditions are completely consistent and have zero contradictions.
</think>`,
        isCorrect: true
      },
      react: {
        text: 'Alice is a Knight, Bob is a Knave.',
        reasoning: `Thought 1: Test hypothesis A = Knave.
Action 1: TruthVerifier(Alice == Knave, Statement == False)
Observation 1: Contradiction found. Inverts to Alice == Knight.

Thought 2: Test statement truth condition given Alice == Knight.
Action 2: LogicSolver(Statement: (Alice == Knave) OR (Bob == Knave), Known: Alice == Knight)
Observation 2: Implies Bob == Knave must be True.

Thought 3: Solution verified.`,
        isCorrect: true
      },
      tot: {
        text: 'Alice is a Knight, Bob is a Knave.',
        reasoning: `[Branch A: Alice = Knave]
├── Evaluation: S is False => Neither is Knave => Alice is Knight.
└── Status: Contradiction! Pruning branch A (Confidence: 0.0)

[Branch B: Alice = Knight]
├── Evaluation: S is True => At least one is Knave.
├── Step: Since Alice is Knight, Bob must be Knave.
└── Status: Verified consistent (Confidence: 1.0)`,
        isCorrect: true
      }
    }
  }
};

export default function PromptEngineeringPlayground() {
  const [selectedChallengeKey, setSelectedChallengeKey] = useState('math');
  const [selectedStrategyId, setSelectedStrategyId] = useState('cot');
  const [isStreaming, setIsStreaming] = useState(false);
  const [displayedText, setDisplayedText] = useState('');
  const [displayedReasoning, setDisplayedReasoning] = useState('');
  const [copied, setCopied] = useState(false);

  const activeChallenge = PRESET_CHALLENGES[selectedChallengeKey];
  const activePrompt = activeChallenge.prompts[selectedStrategyId];
  const activeOutput = activeChallenge.outputs[selectedStrategyId];

  // Run simulation
  const handleRunExecution = () => {
    setIsStreaming(true);
    setDisplayedText('');
    setDisplayedReasoning('');

    const fullReasoning = activeOutput.reasoning || '';
    const fullText = activeOutput.text || '';

    let rIdx = 0;
    const rInterval = setInterval(() => {
      rIdx += 4;
      setDisplayedReasoning(fullReasoning.slice(0, rIdx));
      if (rIdx >= fullReasoning.length) {
        clearInterval(rInterval);
        // Start streaming final text
        let tIdx = 0;
        const tInterval = setInterval(() => {
          tIdx += 3;
          setDisplayedText(fullText.slice(0, tIdx));
          if (tIdx >= fullText.length) {
            clearInterval(tInterval);
            setIsStreaming(false);
          }
        }, 20);
      }
    }, 15);
  };

  useEffect(() => {
    // Initial display
    setDisplayedReasoning(activeOutput.reasoning || '');
    setDisplayedText(activeOutput.text || '');
  }, [selectedChallengeKey, selectedStrategyId]);

  const handleCopyPrompt = () => {
    navigator.clipboard.writeText(activePrompt);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  // Metrics calculation
  const promptTokens = Math.round(activePrompt.length / 4);
  const reasoningTokens = Math.round((activeOutput.reasoning || '').length / 4);
  const completionTokens = Math.round((activeOutput.text || '').length / 4);
  const totalTokens = promptTokens + reasoningTokens + completionTokens;

  return (
    <div className="space-y-6">
      {/* Playground Header Card */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 sm:p-6 shadow-sm">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 text-indigo-300 border border-indigo-500/30 text-xs font-semibold uppercase tracking-wider mb-2">
              <Brain className="w-3.5 h-3.5" />
              <span>Prompting &amp; System 2 Reasoning Arena</span>
            </div>
            <h2 className="text-xl sm:text-2xl font-bold text-white tracking-tight">
              Compare LLM Prompting Paradigms &amp; Test-Time Compute
            </h2>
            <p className="text-xs sm:text-sm text-slate-400 mt-1 max-w-2xl">
              Inspect how Zero-Shot, In-Context Few-Shot, Chain-of-Thought (CoT), ReAct Tool Loops, and Tree-of-Thoughts solve complex mathematical traps and logic riddles.
            </p>
          </div>

          {/* Preset Challenge Switcher */}
          <div className="flex items-center gap-2 bg-slate-950 p-1.5 rounded-xl border border-slate-800 shrink-0">
            <span className="text-xs text-slate-500 px-2 font-mono">Challenge:</span>
            <button
              onClick={() => setSelectedChallengeKey('math')}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition ${
                selectedChallengeKey === 'math'
                  ? 'bg-indigo-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              Math Constraint Trap
            </button>
            <button
              onClick={() => setSelectedChallengeKey('logic')}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition ${
                selectedChallengeKey === 'logic'
                  ? 'bg-indigo-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              Knights &amp; Knaves Logic
            </button>
          </div>
        </div>
      </div>

      {/* Strategy Selection Strip */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
        {PROMPT_STRATEGIES.map((strat) => {
          const isSelected = selectedStrategyId === strat.id;
          return (
            <button
              key={strat.id}
              onClick={() => setSelectedStrategyId(strat.id)}
              className={`p-3.5 rounded-xl border text-left transition-all ${
                isSelected
                  ? 'bg-slate-800/95 border-indigo-500/80 shadow-md shadow-indigo-500/10 ring-1 ring-indigo-500/40'
                  : 'bg-slate-900/60 border-slate-800 hover:border-slate-700 hover:bg-slate-900/90 text-slate-400'
              }`}
            >
              <div className="flex items-center justify-between mb-1">
                <span className={`text-xs font-bold ${isSelected ? 'text-indigo-300' : 'text-slate-300'}`}>
                  {strat.name}
                </span>
                {isSelected && (
                  <span className="w-2 h-2 rounded-full bg-indigo-400 animate-pulse" />
                )}
              </div>
              <p className="text-[11px] text-slate-400 leading-relaxed line-clamp-2">
                {strat.desc}
              </p>
            </button>
          );
        })}
      </div>

      {/* Arena Workspace Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        
        {/* Left Column: Prompt Formulation & Configuration (5 cols) */}
        <div className="lg:col-span-5 space-y-4">
          <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-4 sm:p-5 space-y-3.5 shadow-sm">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
                <Terminal className="w-3.5 h-3.5 text-indigo-400" />
                Prompt Formulation
              </span>
              <button
                onClick={handleCopyPrompt}
                className="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white border border-slate-700/60 text-xs font-medium transition flex items-center gap-1.5"
                title="Copy Prompt"
              >
                {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                <span>{copied ? 'Copied' : 'Copy'}</span>
              </button>
            </div>

            {/* Problem Statement Card */}
            <div className="p-3 rounded-xl bg-slate-950/80 border border-slate-800/80 text-xs text-slate-300 leading-relaxed">
              <span className="font-semibold text-slate-400 block mb-1 uppercase tracking-wider text-[10px]">
                Ground Truth Problem:
              </span>
              {activeChallenge.problem}
            </div>

            {/* Prompt Text Box */}
            <div className="space-y-1.5">
              <label className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
                Full Injected Prompt:
              </label>
              <textarea
                readOnly
                value={activePrompt}
                rows={7}
                className="w-full p-3 rounded-xl bg-slate-950 font-mono text-xs text-indigo-200 border border-slate-800 focus:outline-none resize-none leading-relaxed"
              />
            </div>

            {/* Run Button */}
            <button
              onClick={handleRunExecution}
              disabled={isStreaming}
              className="w-full py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 active:scale-[0.99] text-white font-semibold text-xs sm:text-sm transition flex items-center justify-center gap-2 shadow-lg shadow-indigo-600/30 disabled:opacity-50"
            >
              <Play className={`w-4 h-4 fill-white ${isStreaming ? 'animate-pulse' : ''}`} />
              <span>{isStreaming ? 'Generating Reasoning Tokens...' : 'Simulate LLM Execution'}</span>
            </button>
          </div>

          {/* Token & Compute Footprint Diagnostics */}
          <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-4 grid grid-cols-3 gap-2 text-center text-xs">
            <div className="p-2 rounded-xl bg-slate-950 border border-slate-800/60">
              <span className="text-[10px] text-slate-500 block uppercase font-mono">Prompt Tokens</span>
              <span className="text-sm font-bold text-white font-mono">{promptTokens}</span>
            </div>
            <div className="p-2 rounded-xl bg-slate-950 border border-slate-800/60">
              <span className="text-[10px] text-indigo-400 block uppercase font-mono">Reasoning Tokens</span>
              <span className="text-sm font-bold text-indigo-300 font-mono">{reasoningTokens}</span>
            </div>
            <div className="p-2 rounded-xl bg-slate-950 border border-slate-800/60">
              <span className="text-[10px] text-emerald-400 block uppercase font-mono">Total Tokens</span>
              <span className="text-sm font-bold text-emerald-300 font-mono">{totalTokens}</span>
            </div>
          </div>
        </div>

        {/* Right Column: Reasoning Trace & Output (7 cols) */}
        <div className="lg:col-span-7 space-y-4">
          <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 space-y-4 shadow-sm flex flex-col h-full min-h-[440px]">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <div className="flex items-center gap-2">
                <span className="text-xs font-bold uppercase tracking-wider text-slate-300 flex items-center gap-1.5">
                  <Sparkles className="w-3.5 h-3.5 text-amber-400" />
                  Model Reasoning &amp; Execution Trace
                </span>
                {isStreaming && (
                  <span className="text-[10px] px-2 py-0.5 rounded-full bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 animate-pulse font-mono">
                    Generating...
                  </span>
                )}
              </div>

              {/* Accuracy Status Badge */}
              <span className={`text-[11px] font-bold px-2.5 py-0.5 rounded-full border ${
                activeOutput.isCorrect
                  ? 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30'
                  : 'bg-rose-500/15 text-rose-300 border-rose-500/30'
              }`}>
                {activeOutput.isCorrect ? '✓ Correct Answer' : '✗ Fallacy / Trap Triggered'}
              </span>
            </div>

            {/* Trap Warning if applicable */}
            {activeOutput.trapNote && (
              <div className="p-3 bg-rose-950/40 border border-rose-500/40 rounded-xl text-xs text-rose-200 leading-relaxed flex items-start gap-2">
                <Flame className="w-4 h-4 text-rose-400 shrink-0 mt-0.5" />
                <div>
                  <span className="font-bold text-rose-300 block">Cognitive Shortcut Trap:</span>
                  {activeOutput.trapNote}
                </div>
              </div>
            )}

            {/* Hidden/Thinking Step-by-Step Block */}
            {displayedReasoning && (
              <div className="space-y-1.5">
                <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1 font-mono">
                  <Brain className="w-3 h-3 text-indigo-400" />
                  System 2 Internal Thought Trace (&lt;think&gt;)
                </span>
                <div className="p-3.5 rounded-xl bg-slate-950 border border-indigo-500/30 text-xs font-mono text-indigo-300/90 whitespace-pre-wrap leading-relaxed overflow-x-auto max-h-64 overflow-y-auto scrollbar-thin">
                  {displayedReasoning}
                </div>
              </div>
            )}

            {/* Final Model Response Card */}
            <div className="space-y-1.5 flex-1">
              <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1 font-mono">
                <Terminal className="w-3 h-3 text-emerald-400" />
                Final Output Statement
              </span>
              <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800 text-xs sm:text-sm text-slate-100 font-medium whitespace-pre-wrap leading-relaxed">
                {displayedText || (isStreaming ? 'Thinking...' : 'Click "Simulate LLM Execution" to run.')}
              </div>
            </div>

            {/* Architectural Insight Note */}
            <div className="pt-2 border-t border-slate-800/80 text-[11px] text-slate-400 flex items-center justify-between">
              <span className="flex items-center gap-1.5">
                <Zap className="w-3.5 h-3.5 text-amber-400" />
                <span>Test-time compute scaling permits smaller models to match larger models on hard reasoning tasks.</span>
              </span>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}
