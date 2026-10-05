import React, { useState, useEffect } from 'react';
import { 
  X, 
  Minus, 
  Sparkles, 
  MessageSquare, 
  Volume2, 
  VolumeX, 
  Heart, 
  ChevronUp, 
  Bot,
  Brain,
  Flame,
  CheckCircle2,
  XCircle,
  RotateCcw
} from 'lucide-react';
import { useTheme } from '../context/ThemeContext';

export const COMPANION_QUIZ_QUESTIONS = [
  {
    question: "What scaling factor does Scaled Dot-Product Attention divide QK^T by?",
    options: ["d_k", "sqrt(d_k)", "2 * d_k", "d_model^2"],
    correct: 1,
    tip: "1/sqrt(d_k) keeps the dot-product variance around 1, preventing softmax gradients from saturating."
  },
  {
    question: "Which matrix is initialized to all zeros in standard LoRA?",
    options: ["Matrix A", "Matrix B", "Both A & B", "Neither"],
    correct: 1,
    tip: "B starts at 0 and A is Gaussian, guaranteeing Delta W = 0 at training step 0!"
  },
  {
    question: "What is the recommended token overlap percentage in standard RAG chunking?",
    options: ["0%", "10% – 20%", "50%", "80%"],
    correct: 1,
    tip: "10%–20% overlap (~50-100 tokens) prevents semantic boundary fracture between adjacent chunks."
  },
  {
    question: "Which optimizer decouples L2 weight decay directly from gradient updates?",
    options: ["SGD + Momentum", "RMSProp", "AdamW", "AdaGrad"],
    correct: 2,
    tip: "AdamW fixes standard Adam's broken L2 regularization by penalizing weights directly."
  },
  {
    question: "In FlashAttention, which ultra-fast on-chip GPU memory is used for online softmax tiling?",
    options: ["HBM (High Bandwidth Memory)", "SRAM", "PCIe Bus", "SSD Page File"],
    correct: 1,
    tip: "FlashAttention computes softmax in GPU SRAM, turning O(N^2) memory IO into O(N)!"
  },
  {
    question: "What landmark 1957 algorithm could not compute the non-linear XOR function?",
    options: ["Neocognitron", "Single-Layer Perceptron", "ResNet-18", "LSTM"],
    correct: 1,
    tip: "Rosenblatt's Perceptron was proved incapable of XOR by Minsky & Papert in 1969."
  },
  {
    question: "Which evaluation metric is mathematically equal to exp(Cross-Entropy Loss)?",
    options: ["BLEU Score", "Perplexity (PPL)", "F1 Score", "AUC-ROC"],
    correct: 1,
    tip: "Perplexity reflects the model's effective branching uncertainty over vocabulary tokens."
  },
  {
    question: "What does GRPO in DeepSeek-R1 eliminate compared to standard PPO?",
    options: ["The Critic / Value Model", "The Actor Model", "Reward Functions", "Tokens"],
    correct: 0,
    tip: "GRPO computes relative advantages by grouping sample rollouts, discarding the memory-heavy critic!"
  }
];

export default function GardenCompanion() {
  const [isMinimized, setIsMinimized] = useState(false);
  const [isClosed, setIsClosed] = useState(false);
  const [currentTipIndex, setCurrentTipIndex] = useState(0);
  const [isWaving, setIsWaving] = useState(true);
  const [robotMood, setRobotMood] = useState('happy'); // 'happy', 'curious', 'love'
  const { theme } = useTheme();

  // Mode: 'tips' or 'quiz'
  const [companionMode, setCompanionMode] = useState('tips');
  const [quizIndex, setQuizIndex] = useState(0);
  const [selectedQuizOption, setSelectedQuizOption] = useState(null);
  const [quizStreak, setQuizStreak] = useState(0);
  const [quizScore, setQuizScore] = useState(0);
  const [quizFeedback, setQuizFeedback] = useState(null); // 'correct' | 'wrong' | null

  const companionTips = [
    {
      text: "Hi there! 👋 Welcome to The Era of AI!",
      author: "Aero the AI Bot",
      mood: "happy"
    },
    {
      text: "Did you know? Attention Is All You Need was published by 8 researchers in 2017!",
      author: "AI History Trivia",
      mood: "curious"
    },
    {
      text: "Tip: Click any node in the Mind Map to inspect its full mathematical formulation!",
      author: "Navigation Tip",
      mood: "happy"
    },
    {
      text: "Humans + AI = Infinite Creativity & Discovery in the garden of science! 🌿🌸",
      author: "Harmony Note",
      mood: "love"
    },
    {
      text: "Press ⌘K or Ctrl+K anywhere to instantly search across 170+ concepts and papers!",
      author: "Shortcut Pro Tip",
      mood: "curious"
    },
    {
      text: "Check out our daily research papers crawler — automated by GitHub Actions every morning!",
      author: "Live Data Feed",
      mood: "happy"
    }
  ];

  // Rotate greeting speech bubble
  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTipIndex((prev) => (prev + 1) % companionTips.length);
    }, 9000);
    return () => clearInterval(timer);
  }, []);

  const handleNextTip = () => {
    setCurrentTipIndex((prev) => (prev + 1) % companionTips.length);
    triggerWave();
  };

  const [soundEnabled, setSoundEnabled] = useState(false);
  const [isAirplaneFlying, setIsAirplaneFlying] = useState(false);
  const [petalsBurst, setPetalsBurst] = useState(false);

  // Web Audio API Synthesizer (No external assets required)
  const playSound = (type = 'chime') => {
    if (!soundEnabled) return;
    try {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (!AudioCtx) return;
      const ctx = new AudioCtx();

      if (type === 'chime') {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(587.33, ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(880, ctx.currentTime + 0.12);
        gain.gain.setValueAtTime(0.08, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.35);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start();
        osc.stop(ctx.currentTime + 0.35);
      } else if (type === 'whoosh') {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(260, ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(620, ctx.currentTime + 0.25);
        osc.frequency.exponentialRampToValueAtTime(200, ctx.currentTime + 0.5);
        gain.gain.setValueAtTime(0.04, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.5);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start();
        osc.stop(ctx.currentTime + 0.5);
      } else if (type === 'correct') {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(587.33, ctx.currentTime);
        osc.frequency.setValueAtTime(880, ctx.currentTime + 0.1);
        osc.frequency.setValueAtTime(1174.66, ctx.currentTime + 0.2);
        gain.gain.setValueAtTime(0.08, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.45);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start();
        osc.stop(ctx.currentTime + 0.45);
      } else if (type === 'wrong') {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(220, ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(160, ctx.currentTime + 0.25);
        gain.gain.setValueAtTime(0.05, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.25);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start();
        osc.stop(ctx.currentTime + 0.25);
      }
    } catch {
      // Audio context might be restricted before gesture
    }
  };

  const triggerWave = () => {
    setIsWaving(false);
    playSound('chime');
    setTimeout(() => setIsWaving(true), 50);
  };

  const launchAirplane = () => {
    if (isAirplaneFlying) return;
    setIsAirplaneFlying(true);
    playSound('whoosh');
    setTimeout(() => {
      setIsAirplaneFlying(false);
    }, 2000);
  };

  const triggerPetals = () => {
    setPetalsBurst(true);
    playSound('chime');
    setTimeout(() => setPetalsBurst(false), 1500);
  };

  const handleSelectQuizOption = (optIndex) => {
    if (selectedQuizOption !== null) return;
    setSelectedQuizOption(optIndex);
    const q = COMPANION_QUIZ_QUESTIONS[quizIndex];
    if (optIndex === q.correct) {
      setQuizFeedback('correct');
      setQuizScore((prev) => prev + 1);
      setQuizStreak((prev) => prev + 1);
      playSound('correct');
      triggerPetals();
      setRobotMood('love');
    } else {
      setQuizFeedback('wrong');
      setQuizStreak(0);
      playSound('wrong');
      setRobotMood('curious');
    }
  };

  const handleNextQuizQuestion = () => {
    setSelectedQuizOption(null);
    setQuizFeedback(null);
    setRobotMood('happy');
    setQuizIndex((prev) => (prev + 1) % COMPANION_QUIZ_QUESTIONS.length);
  };

  const handleResetQuiz = () => {
    setSelectedQuizOption(null);
    setQuizFeedback(null);
    setQuizScore(0);
    setQuizStreak(0);
    setQuizIndex(0);
    setRobotMood('happy');
  };

  if (isClosed) return null;

  // Minimized floating badge
  if (isMinimized) {
    return (
      <div className="fixed bottom-4 right-4 z-40 animate-bounce-slow">
        <button
          onClick={() => setIsMinimized(false)}
          className="relative p-2.5 rounded-2xl bg-slate-900/90 hover:bg-slate-800 text-white border border-indigo-500/50 shadow-2xl shadow-indigo-500/30 flex items-center gap-2 group transition-all duration-200"
          title="Open AI Companion & Garden"
        >
          {/* Small animated waving robot icon */}
          <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-indigo-600 to-cyan-400 p-[1.5px] flex items-center justify-center">
            <div className="w-full h-full bg-slate-950 rounded-[10px] flex items-center justify-center">
              <Bot className="w-4 h-4 text-cyan-300 animate-pulse" />
            </div>
          </div>
          <span className="text-xs font-semibold text-slate-200 pr-1 group-hover:text-indigo-300">
            Hi! 👋
          </span>
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping absolute -top-0.5 -right-0.5" />
        </button>
      </div>
    );
  }

  const currentTip = companionTips[currentTipIndex];

  return (
    <div className="fixed bottom-4 right-4 z-40 max-w-[340px] sm:max-w-[380px] w-full select-none animate-slideUp">
      <div className="relative bg-slate-900/95 backdrop-blur-xl border border-slate-700/80 rounded-2xl shadow-2xl overflow-hidden text-slate-100 flex flex-col">
        {/* Top Header Bar */}
        <div className="px-3.5 py-2 bg-slate-950/80 border-b border-slate-800/80 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="flex h-2 w-2 relative">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
              <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500" />
            </span>
            <span className="text-xs font-bold text-white tracking-tight flex items-center gap-1.5">
              <span>Aero &amp; Little Leo</span>
              <span className="text-[10px] text-indigo-400 font-normal">&bull; Harmony Garden</span>
            </span>
          </div>

          <div className="flex items-center gap-1">
            {/* Audio Toggle */}
            <button
              onClick={() => {
                const next = !soundEnabled;
                setSoundEnabled(next);
                if (next) playSound('chime');
              }}
              aria-label={soundEnabled ? 'Mute companion audio' : 'Enable companion audio'}
              className={`p-1 rounded-md transition ${
                soundEnabled
                  ? 'text-cyan-400 bg-cyan-500/10'
                  : 'text-slate-500 hover:text-slate-300 hover:bg-slate-800'
              }`}
              title={soundEnabled ? 'Mute chimes' : 'Enable gentle chimes'}
            >
              {soundEnabled ? <Volume2 className="w-3.5 h-3.5" /> : <VolumeX className="w-3.5 h-3.5" />}
            </button>

            <button
              onClick={() => setIsMinimized(true)}
              aria-label="Minimize companion"
              className="p-1 rounded-md text-slate-400 hover:text-white hover:bg-slate-800 transition"
              title="Minimize to corner"
            >
              <Minus className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={() => setIsClosed(true)}
              aria-label="Close companion"
              className="p-1 rounded-md text-slate-400 hover:text-white hover:bg-slate-800 transition"
              title="Close"
            >
              <X className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        {/* Animated Garden Scene SVG */}
        <div className="relative w-full h-44 bg-gradient-to-b from-indigo-950/60 via-slate-900/80 to-slate-950 overflow-hidden flex items-end justify-center">
          {/* Subtle cosmic night garden backdrop */}
          <div className="absolute inset-0 opacity-40 pointer-events-none">
            {/* Stars & fireflies */}
            <div className="absolute top-3 left-6 w-1 h-1 rounded-full bg-cyan-300 animate-ping" style={{ animationDuration: '3s' }} />
            <div className="absolute top-8 right-12 w-1.5 h-1.5 rounded-full bg-amber-300 animate-ping" style={{ animationDuration: '2.5s' }} />
            <div className="absolute top-14 left-1/3 w-1 h-1 rounded-full bg-purple-300 animate-ping" style={{ animationDuration: '4s' }} />
            <div className="absolute top-6 left-2/3 w-1.5 h-1.5 rounded-full bg-emerald-300 animate-ping" style={{ animationDuration: '3.5s' }} />
          </div>

          {/* SVG Garden Diorama with Robot and Child */}
          <svg viewBox="0 0 400 180" className="w-full h-full overflow-visible">
            <defs>
              {/* Garden Grass Gradient */}
              <linearGradient id="grassGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#059669" />
                <stop offset="100%" stopColor="#064e3b" />
              </linearGradient>

              {/* Robot Metallic Gradient */}
              <linearGradient id="robotBodyGrad" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0%" stopColor="#6366f1" />
                <stop offset="50%" stopColor="#4338ca" />
                <stop offset="100%" stopColor="#312e81" />
              </linearGradient>

              {/* Visor Cyan Glow */}
              <linearGradient id="visorGrad" x1="0" y1="0" x2="1" y2="0">
                <stop offset="0%" stopColor="#06b6d4" />
                <stop offset="100%" stopColor="#38bdf8" />
              </linearGradient>

              {/* Flower Petal Gradient */}
              <linearGradient id="petalGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#f472b6" />
                <stop offset="100%" stopColor="#ec4899" />
              </linearGradient>
            </defs>

            {/* Hill 1 & Lush Rolling Lawn */}
            <path
              d="M -20 180 Q 90 135 200 150 T 420 180 Z"
              fill="url(#grassGrad)"
              opacity="0.9"
            />
            <path
              d="M -20 180 Q 150 145 280 155 T 420 180 Z"
              fill="#047857"
              opacity="0.7"
            />

            {/* Glowing Garden Flowers */}
            <g className="flowers">
              {/* Flower 1 */}
              <circle cx="50" cy="155" r="4" fill="url(#petalGrad)" />
              <circle cx="50" cy="155" r="1.5" fill="#fef08a" />
              <line x1="50" y1="155" x2="50" y2="168" stroke="#10b981" strokeWidth="1.5" />

              {/* Flower 2 */}
              <circle cx="110" cy="160" r="5" fill="#c084fc" />
              <circle cx="110" cy="160" r="2" fill="#fef08a" />
              <line x1="110" y1="160" x2="110" y2="172" stroke="#10b981" strokeWidth="1.5" />

              {/* Flower 3 */}
              <circle cx="340" cy="162" r="4.5" fill="#38bdf8" />
              <circle cx="340" cy="162" r="1.5" fill="#ffffff" />
              <line x1="340" y1="162" x2="340" y2="174" stroke="#10b981" strokeWidth="1.5" />

              {/* Flower 4 */}
              <circle cx="370" cy="158" r="4" fill="url(#petalGrad)" />
              <circle cx="370" cy="158" r="1.5" fill="#fef08a" />
              <line x1="370" y1="158" x2="370" y2="170" stroke="#10b981" strokeWidth="1.5" />
            </g>

            {/* Glowing Holographic Butterfly */}
            <g className="animate-butterfly" transform="translate(160, 65)">
              <ellipse cx="-4" cy="-2" rx="5" ry="3.5" fill="#f472b6" opacity="0.85" transform="rotate(-25)" />
              <ellipse cx="4" cy="-2" rx="5" ry="3.5" fill="#f472b6" opacity="0.85" transform="rotate(25)" />
              <ellipse cx="0" cy="0" rx="1" ry="4" fill="#ffffff" />
            </g>

            {/* Secondary Butterfly near child */}
            <g className="animate-butterfly-slow" transform="translate(230, 95)">
              <ellipse cx="-3" cy="-1.5" rx="4" ry="2.5" fill="#38bdf8" opacity="0.85" transform="rotate(-30)" />
              <ellipse cx="3" cy="-1.5" rx="4" ry="2.5" fill="#38bdf8" opacity="0.85" transform="rotate(30)" />
              <ellipse cx="0" cy="0" rx="0.8" ry="3" fill="#ffffff" />
            </g>

            {/* 1. THE CHILD ("Little Leo") Playing in Garden */}
            <g id="childCharacter" transform="translate(265, 110)">
              {/* Shadow */}
              <ellipse cx="15" cy="52" rx="14" ry="4" fill="#000000" opacity="0.3" />

              {/* Legs sitting / kneeling on grass */}
              <path d="M 6 42 Q 10 50 16 50 T 26 50" fill="none" stroke="#1e293b" strokeWidth="5" strokeLinecap="round" />

              {/* Torso / Colorful Jacket */}
              <path d="M 8 26 L 22 26 L 25 43 L 5 43 Z" fill="#f59e0b" rx="3" />

              {/* Scarf / Collar */}
              <path d="M 9 26 Q 15 29 21 26" fill="none" stroke="#ef4444" strokeWidth="3" strokeLinecap="round" />

              {/* Head */}
              <circle cx="15" cy="15" r="10" fill="#fed7aa" />

              {/* Hair */}
              <path d="M 6 14 Q 15 4 24 14 Q 22 8 15 7 Q 8 8 6 14 Z" fill="#78350f" />

              {/* Happy Eyes & Smile */}
              <circle cx="12" cy="15" r="1.2" fill="#1e293b" />
              <circle cx="18" cy="15" r="1.2" fill="#1e293b" />
              <path d="M 13 18 Q 15 20 17 18" fill="none" stroke="#1e293b" strokeWidth="1" strokeLinecap="round" />

              {/* Arm reaching out towards butterfly/robot */}
              <path d="M 7 28 Q -2 22 -6 18" fill="none" stroke="#fed7aa" strokeWidth="3.5" strokeLinecap="round" className="animate-reach" />
              {/* Hand */}
              <circle cx="-7" cy="17" r="2.5" fill="#fed7aa" />

              {/* Other Arm resting on knee */}
              <path d="M 23 28 Q 28 34 25 40" fill="none" stroke="#f59e0b" strokeWidth="3.5" strokeLinecap="round" />
            </g>

            {/* 2. THE ROBOT ("Aero") Hovering & Waving */}
            <g 
              id="robotCharacter" 
              transform="translate(90, 85)"
              className="cursor-pointer"
              onClick={triggerWave}
            >
              {/* Thruster Flame & Shadow */}
              <ellipse cx="20" cy="72" rx="15" ry="3.5" fill="#000000" opacity="0.3" className="animate-pulse" />
              
              {/* Hovering Group with floating CSS animation */}
              <g className="animate-robot-hover">
                {/* Thruster Glow & Jet Flame */}
                <ellipse cx="20" cy="52" rx="6" ry="3" fill="#38bdf8" opacity="0.8" />
                <polygon points="16 52, 24 52, 20 62" fill="#06b6d4" className="animate-pulse" />
                <polygon points="18 52, 22 52, 20 58" fill="#ffffff" />

                {/* Robot Body / Chassis */}
                <rect x="5" y="24" width="30" height="26" rx="8" fill="url(#robotBodyGrad)" stroke="#818cf8" strokeWidth="1.5" />
                
                {/* Chest Core Reactor */}
                <circle cx="20" cy="37" r="4.5" fill="#06b6d4" className="animate-pulse" />
                <circle cx="20" cy="37" r="2" fill="#ffffff" />

                {/* Robot Head */}
                <rect x="7" y="6" width="26" height="18" rx="6" fill="#1e1b4b" stroke="#818cf8" strokeWidth="1.5" />

                {/* Antenna */}
                <line x1="20" y1="6" x2="20" y2="0" stroke="#818cf8" strokeWidth="1.5" />
                <circle cx="20" cy="0" r="2.5" fill={companionMode === 'quiz' ? '#f59e0b' : '#38bdf8'} className="animate-ping" style={{ animationDuration: '1.8s' }} />
                <circle cx="20" cy="0" r="2" fill={companionMode === 'quiz' ? '#f59e0b' : '#38bdf8'} />

                {/* Visor Screen with Animated Blinking Eyes */}
                <rect x="10" y="10" width="20" height="10" rx="3" fill="#020617" />
                <g className="animate-visor-blink">
                  <ellipse cx="15" cy="15" rx="2.5" ry="3" fill={quizFeedback === 'correct' ? '#10b981' : quizFeedback === 'wrong' ? '#f43f5e' : companionMode === 'quiz' ? '#fbbf24' : '#06b6d4'} />
                  <ellipse cx="25" cy="15" rx="2.5" ry="3" fill={quizFeedback === 'correct' ? '#10b981' : quizFeedback === 'wrong' ? '#f43f5e' : companionMode === 'quiz' ? '#fbbf24' : '#06b6d4'} />
                  <circle cx="16" cy="14" r="1" fill="#ffffff" />
                  <circle cx="26" cy="14" r="1" fill="#ffffff" />
                </g>

                {/* Left Arm (Resting/Stabilizing) */}
                <path d="M 5 28 Q 0 34 2 40" fill="none" stroke="#6366f1" strokeWidth="3" strokeLinecap="round" />

                {/* Right Arm: WAVING ARM (CSS animated waving) */}
                <g className={isWaving ? "animate-wave" : ""}>
                  <path d="M 35 28 Q 44 20 46 10" fill="none" stroke="#6366f1" strokeWidth="3.5" strokeLinecap="round" />
                  {/* Robot Hand with Friendly Palm */}
                  <circle cx="47" cy="9" r="3" fill="#38bdf8" />
                  <circle cx="47" cy="9" r="1.5" fill="#ffffff" />
                </g>
              </g>
            </g>

            {/* Paper Airplane Flying from Child to Robot */}
            {isAirplaneFlying && (
              <g className="animate-pulse">
                <path d="M 310 115 Q 260 65 200 80" fill="none" stroke="#e0e7ff" strokeWidth="1.5" strokeDasharray="3,3" opacity="0.7" />
                <polygon points="0,0 14,4 0,8 3,4" fill="#ffffff" stroke="#6366f1" strokeWidth="1" transform="translate(240, 82) rotate(-165)" />
                <circle cx="230" cy="85" r="2" fill="#38bdf8" className="animate-ping" />
              </g>
            )}

            {/* Floating Petals Burst from Flowers */}
            {petalsBurst && (
              <g>
                <circle cx="50" cy="140" r="3" fill="#f472b6" opacity="0.9" />
                <circle cx="55" cy="125" r="2.5" fill="#ec4899" opacity="0.8" />
                <circle cx="100" cy="135" r="3" fill="#38bdf8" opacity="0.9" />
                <circle cx="105" cy="120" r="2" fill="#38bdf8" opacity="0.8" />
                <circle cx="270" cy="135" r="3" fill="#f472b6" opacity="0.9" />
                <circle cx="275" cy="122" r="2.5" fill="#fbcfe8" opacity="0.8" />
              </g>
            )}

            {/* Sparkles of Knowledge / Synergy between Robot and Child */}
            <g className="knowledge-sparkles" opacity="0.8">
              <path d="M 180 110 Q 210 100 240 115" fill="none" stroke="#818cf8" strokeDasharray="3,3" strokeWidth="1" opacity="0.4" />
              <circle cx="200" cy="105" r="1.5" fill="#38bdf8" className="animate-ping" style={{ animationDuration: '2s' }} />
              <circle cx="225" cy="108" r="1.5" fill="#f472b6" className="animate-ping" style={{ animationDuration: '2.4s' }} />
            </g>
          </svg>
        </div>

        {/* Dialogue / Speech Bubble or Quiz Interface */}
        <div className="p-3 bg-slate-950/95 border-t border-slate-800/80 space-y-2.5">
          {companionMode === 'tips' ? (
            <>
              <div className="flex items-start gap-2.5">
                <div className="w-6 h-6 rounded-lg bg-indigo-500/20 text-indigo-400 border border-indigo-500/30 flex items-center justify-center shrink-0 mt-0.5">
                  <MessageSquare className="w-3.5 h-3.5" />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <span className="text-[11px] font-bold text-indigo-300">
                      {currentTip.author}
                    </span>
                    <span className="text-[10px] text-slate-500 font-mono">
                      {currentTipIndex + 1}/{companionTips.length}
                    </span>
                  </div>
                  <p className="text-xs text-slate-200 mt-0.5 leading-relaxed font-normal">
                    {currentTip.text}
                  </p>
                </div>
              </div>

              {/* Interactive Button Strip */}
              <div className="flex items-center justify-between gap-1.5 pt-1 text-xs flex-wrap">
                <div className="flex items-center gap-1.5 flex-wrap">
                  <button
                    onClick={triggerWave}
                    className="px-2 py-1 rounded-lg bg-slate-800 hover:bg-indigo-600/30 text-slate-300 hover:text-white border border-slate-700/60 transition flex items-center gap-1 text-[11px] font-medium"
                    title="Wave back at Aero"
                  >
                    <Sparkles className="w-3 h-3 text-cyan-400" />
                    <span>Wave 👋</span>
                  </button>

                  <button
                    onClick={launchAirplane}
                    className="px-2 py-1 rounded-lg bg-slate-800 hover:bg-cyan-600/30 text-slate-300 hover:text-white border border-slate-700/60 transition flex items-center gap-1 text-[11px] font-medium"
                    title="Little Leo throws a paper airplane to Aero"
                  >
                    <span>Fly Plane ✈️</span>
                  </button>

                  <button
                    onClick={triggerPetals}
                    className="px-2 py-1 rounded-lg bg-slate-800 hover:bg-pink-600/30 text-slate-300 hover:text-white border border-slate-700/60 transition flex items-center gap-1 text-[11px] font-medium"
                    title="Bloom garden flowers"
                  >
                    <span>Bloom 🌸</span>
                  </button>

                  {/* Switch to Quiz Mode Button */}
                  <button
                    onClick={() => {
                      setCompanionMode('quiz');
                      playSound('chime');
                    }}
                    className="px-2 py-1 rounded-lg bg-gradient-to-r from-amber-500/20 to-orange-500/20 hover:from-amber-500/30 hover:to-orange-500/30 text-amber-300 border border-amber-500/40 font-semibold text-[11px] flex items-center gap-1 shadow-sm"
                    title="Start Quick-Fire AI Quiz Mini-Game"
                  >
                    <Brain className="w-3 h-3 text-amber-400" />
                    <span>Quiz Me! 🧠</span>
                  </button>
                </div>

                <button
                  onClick={handleNextTip}
                  className="px-2.5 py-1 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-medium transition text-[11px] flex items-center gap-1 shadow-sm ml-auto"
                >
                  <span>Next</span>
                  <ChevronUp className="w-3 h-3 rotate-90" />
                </button>
              </div>
            </>
          ) : (
            /* Quiz Mode Interface */
            <div className="space-y-2.5 animate-in fade-in duration-200">
              {/* Quiz Header Bar */}
              <div className="flex items-center justify-between text-[11px] border-b border-slate-800 pb-1.5">
                <div className="flex items-center gap-1.5 font-bold text-amber-300">
                  <Brain className="w-3.5 h-3.5 text-amber-400" />
                  <span>Aero's Quick-Fire Quiz</span>
                  <span className="text-[10px] font-mono text-slate-400 font-normal">
                    (Q{quizIndex + 1}/{COMPANION_QUIZ_QUESTIONS.length})
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  {quizStreak > 0 && (
                    <span className="flex items-center gap-1 text-[10px] font-mono font-bold text-orange-400 bg-orange-500/15 border border-orange-500/30 px-1.5 py-0.2 rounded-full">
                      <Flame className="w-3 h-3 text-orange-400 fill-orange-400" />
                      {quizStreak} Streak
                    </span>
                  )}
                  <button
                    onClick={() => setCompanionMode('tips')}
                    className="text-[10px] text-slate-400 hover:text-white px-1.5 py-0.5 rounded hover:bg-slate-800 transition"
                  >
                    Back to Tips
                  </button>
                </div>
              </div>

              {/* Question Text */}
              <p className="text-xs text-white font-semibold leading-snug">
                {COMPANION_QUIZ_QUESTIONS[quizIndex].question}
              </p>

              {/* 4 Answer Options */}
              <div className="grid grid-cols-2 gap-1.5">
                {COMPANION_QUIZ_QUESTIONS[quizIndex].options.map((opt, oIdx) => {
                  const isSelected = selectedQuizOption === oIdx;
                  const isCorrect = oIdx === COMPANION_QUIZ_QUESTIONS[quizIndex].correct;
                  const hasAnswered = selectedQuizOption !== null;

                  let btnStyle = 'bg-slate-900 border-slate-800 text-slate-300 hover:border-slate-700 hover:text-white';
                  if (hasAnswered) {
                    if (isCorrect) {
                      btnStyle = 'bg-emerald-500/20 border-emerald-500/60 text-emerald-300 font-bold';
                    } else if (isSelected) {
                      btnStyle = 'bg-rose-500/20 border-rose-500/60 text-rose-300 font-bold';
                    } else {
                      btnStyle = 'bg-slate-900/40 border-slate-800/40 text-slate-600 opacity-60';
                    }
                  }

                  return (
                    <button
                      key={oIdx}
                      disabled={hasAnswered}
                      onClick={() => handleSelectQuizOption(oIdx)}
                      className={`p-1.5 rounded-lg border text-left text-[11px] transition flex items-center gap-1.5 ${btnStyle}`}
                    >
                      <span className="w-4 h-4 rounded-full bg-slate-800 border border-slate-700 text-[9px] font-mono flex items-center justify-center shrink-0">
                        {String.fromCharCode(65 + oIdx)}
                      </span>
                      <span className="truncate">{opt}</span>
                    </button>
                  );
                })}
              </div>

              {/* Answer Feedback / Tip */}
              {selectedQuizOption !== null && (
                <div className={`p-2 rounded-lg border text-[11px] leading-snug flex items-start gap-2 ${
                  quizFeedback === 'correct'
                    ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-200'
                    : 'bg-amber-500/10 border-amber-500/30 text-amber-200'
                }`}>
                  {quizFeedback === 'correct' ? (
                    <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                  ) : (
                    <Sparkles className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
                  )}
                  <div className="flex-1">
                    <span className="font-bold">
                      {quizFeedback === 'correct' ? 'Correct! 🌟 ' : 'Good try! 💡 '}
                    </span>
                    {COMPANION_QUIZ_QUESTIONS[quizIndex].tip}
                  </div>
                </div>
              )}

              {/* Quiz Footer Controls */}
              {selectedQuizOption !== null && (
                <div className="flex items-center justify-between pt-1">
                  <span className="text-[10px] text-slate-400 font-mono">
                    Score: {quizScore} / {COMPANION_QUIZ_QUESTIONS.length}
                  </span>
                  <button
                    onClick={handleNextQuizQuestion}
                    className="px-3 py-1 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs transition flex items-center gap-1 shadow-sm"
                  >
                    <span>Next Question</span>
                    <ChevronUp className="w-3 h-3 rotate-90" />
                  </button>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
