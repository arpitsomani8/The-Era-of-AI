import React, { useState, useEffect, useRef, useCallback } from 'react';
import { 
  Sparkles, 
  Volume2, 
  VolumeX, 
  X, 
  Bot, 
  Palette, 
  Compass, 
  Anchor, 
  MessageSquare
} from 'lucide-react';
import { useLocation } from 'react-router-dom';

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
  },
  {
    question: "In Rotary Position Embedding (RoPE), how are relative token positions encoded?",
    options: ["Scalar addition to embeddings", "2D orthogonal rotation matrices", "Concatenating binary digits", "Learned absolute embeddings"],
    correct: 1,
    tip: "RoPE multiplies adjacent 2D vector pairs by rotation matrices, making inner products depend solely on (m - n)!"
  },
  {
    question: "What does Grouped-Query Attention (GQA) reduce compared to Multi-Head Attention?",
    options: ["Vocabulary size", "KV Cache GPU memory footprint", "Model depth", "Feedforward dimension"],
    correct: 1,
    tip: "GQA shares KV heads across query groups (e.g. 8:1 ratio in Llama 3), cutting memory bandwidth bottlenecks during generation."
  },
  {
    question: "In Mixture of Experts (MoE), what decides which expert MLPs process each token?",
    options: ["A Top-K Router Gating Network", "Random dropout selection", "Round-robin scheduler", "Hardcoded token modulo"],
    correct: 0,
    tip: "A learned softmax gating router evaluates token representations and selects the top-1 or top-2 most specialized experts."
  },
  {
    question: "What does setting temperature T < 1.0 do to the output Softmax distribution?",
    options: ["Flattens it towards uniform random", "Sharpens it towards argmax peak", "Inverts token probabilities", "Zeros out top predictions"],
    correct: 1,
    tip: "Dividing logits by T < 1.0 amplifies differences, making the model more deterministic and confident."
  },
  {
    question: "In Diffusion Models, what neural network objective is trained during the reverse denoising process?",
    options: ["Predicting the exact pixel output directly", "Predicting the injected Gaussian noise epsilon", "Classifying image categories", "Compressing images to 1 bit"],
    correct: 1,
    tip: "DDPM models are trained with MSE loss to predict the epsilon noise added to latent x_t at timestep t!"
  },
  {
    question: "What is the primary benefit of BitNet's 1.58-bit ternary quantization {-1, 0, 1}?",
    options: ["Eliminates GPU matrix multiplication in favor of integer addition", "Reduces dataset token count", "Increases vocabulary to 1 million", "Removes attention heads"],
    correct: 0,
    tip: "Multiplying by {-1, 0, 1} requires only sign flips and additions, drastically cutting datacenter power consumption!"
  },
  {
    question: "Which index structure enables sub-linear O(log N) approximate nearest neighbor vector search in Vector DBs?",
    options: ["Bubble Sort Tree", "Hierarchical Navigable Small World (HNSW)", "Single-linked list", "Hash map collision array"],
    correct: 1,
    tip: "HNSW builds multi-layer proximity graphs where top layers allow fast skips and bottom layers refine precision."
  },
  {
    question: "What does Direct Preference Optimization (DPO) optimize directly without an RL reward model?",
    options: ["Implicit log-likelihood ratio of chosen vs rejected responses", "The cross-attention mask", "Quantization bit width", "Token batch size"],
    correct: 0,
    tip: "DPO proves the optimal policy implicitly acts as its own Bradley-Terry reward model, bypassing unstable PPO loops."
  },
  {
    question: "In the Adam optimizer, what does the second moment vector (v_t) track?",
    options: ["Exponential moving average of squared gradients", "Gradient sign changes", "Total step count", "Model weight magnitude"],
    correct: 0,
    tip: "v_t estimates the uncentered gradient variance, allowing Adam to scale step sizes inversely with gradient magnitude."
  },
  {
    question: "What theoretical advantage does the Mamba-2 SSM architecture have over standard Transformers?",
    options: ["O(N) linear time and memory inference over unbounded sequences", "Zero matrix multiplications", "Uses no parameters", "Can only process text backwards"],
    correct: 0,
    tip: "State Space Models maintain a fixed-size recurrent state, avoiding the quadratic O(N^2) KV cache memory explosion."
  },
  {
    question: "What mathematical function is used to calculate Cross-Entropy Loss for multi-class classification?",
    options: ["-sum(y_i * log(p_i))", "sum(abs(y_i - p_i))", "sqrt(y_i^2 + p_i^2)", "y_i / p_i"],
    correct: 0,
    tip: "Cross-entropy measures the negative log-likelihood assigned by the model to the true target class distribution."
  }
];

const COMPANION_DRESSES = [
  {
    id: 'aero',
    name: 'Cyber Explorer',
    bodyGrad: ['#6366f1', '#4338ca', '#312e81'],
    stroke: '#818cf8',
    coreColor: '#06b6d4',
    eyeColor: '#06b6d4',
    beaconColor: '#38bdf8',
    glowColor: 'rgba(99, 102, 241, 0.4)',
    type: 'antenna'
  },
  {
    id: 'neon',
    name: 'Neon Sentinel',
    bodyGrad: ['#fbbf24', '#d97706', '#78350f'],
    stroke: '#fbbf24',
    coreColor: '#f59e0b',
    eyeColor: '#fbbf24',
    beaconColor: '#f59e0b',
    glowColor: 'rgba(245, 158, 11, 0.4)',
    type: 'halo'
  },
  {
    id: 'catbot',
    name: 'Quantum Kitty',
    bodyGrad: ['#f472b6', '#c084fc', '#6b21a8'],
    stroke: '#f472b6',
    coreColor: '#ec4899',
    eyeColor: '#f472b6',
    beaconColor: '#fda4af',
    glowColor: 'rgba(236, 72, 153, 0.4)',
    type: 'cat'
  },
  {
    id: 'matrix',
    name: 'Emerald Matrix',
    bodyGrad: ['#10b981', '#059669', '#064e3b'],
    stroke: '#34d399',
    coreColor: '#10b981',
    eyeColor: '#34d399',
    beaconColor: '#6ee7b7',
    glowColor: 'rgba(16, 185, 129, 0.4)',
    type: 'antenna'
  },
  {
    id: 'phantom',
    name: 'Obsidian Stealth',
    bodyGrad: ['#475569', '#1e293b', '#0f172a'],
    stroke: '#f43f5e',
    coreColor: '#ef4444',
    eyeColor: '#fb7185',
    beaconColor: '#f43f5e',
    glowColor: 'rgba(244, 63, 94, 0.4)',
    type: 'antenna'
  }
];

const COMPANION_TIPS = [
  "Hi! I'm Aero • Your AI Guide 🤖✨",
  "Press ⌘K or Ctrl+K anywhere to search 170+ concepts!",
  "Attention Is All You Need was published in 2017!",
  "LoRA freezes pretrained weights & trains low-rank matrices A & B.",
  "AdamW fixes Adam's L2 regularization bug.",
  "FlashAttention computes online softmax in fast GPU SRAM!",
  "Click any node in the Mind Map to inspect formulas & code.",
  "Check out 150+ technical interview questions in the Vault!"
];

/**
 * Web Audio Synthesizer for Aero's clean chimes
 */
function playAeroSynth(type = 'chime', soundEnabled = true) {
  if (!soundEnabled) return;
  try {
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    if (!AudioCtx) return;
    const ctx = new AudioCtx();
    const now = ctx.currentTime;

    const playTone = (freq, startTime, duration, gainVal = 0.15, wave = 'sine') => {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = wave;
      osc.frequency.setValueAtTime(freq, startTime);
      gain.gain.setValueAtTime(0.001, startTime);
      gain.gain.linearRampToValueAtTime(gainVal, startTime + 0.02);
      gain.gain.exponentialRampToValueAtTime(0.001, startTime + duration);
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start(startTime);
      osc.stop(startTime + duration);
    };

    if (type === 'wave') {
      playTone(659.25, now, 0.18, 0.15, 'sine');
      playTone(880, now + 0.08, 0.25, 0.16, 'sine');
    } else if (type === 'whoosh') {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(260, now);
      osc.frequency.exponentialRampToValueAtTime(540, now + 0.2);
      gain.gain.setValueAtTime(0.04, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.35);
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start(now);
      osc.stop(now + 0.35);
    } else if (type === 'dress') {
      playTone(880, now, 0.1, 0.12, 'sine');
      playTone(1174.66, now + 0.06, 0.18, 0.14, 'triangle');
    }
  } catch (err) {
    console.debug('Audio error', err);
  }
}

export default function GardenCompanion() {
  const location = useLocation();

  // Screen sizing
  const [windowSize, setWindowSize] = useState(() => ({
    w: typeof window !== 'undefined' ? window.innerWidth : 1200,
    h: typeof window !== 'undefined' ? window.innerHeight : 800
  }));
  const isMobile = windowSize.w < 640;

  // Responsive Aero dimensions
  const aeroWidth = isMobile ? 68 : 118;
  const aeroHeight = isMobile ? 78 : 132;

  // Docked bottom-right coordinates
  const getDockPosition = useCallback(() => {
    const w = typeof window !== 'undefined' ? window.innerWidth : 1200;
    const h = typeof window !== 'undefined' ? window.innerHeight : 800;
    return {
      x: Math.max(16, w - (isMobile ? 84 : 140)),
      y: Math.max(68, h - (isMobile ? 96 : 155))
    };
  }, [isMobile]);

  const [position, setPosition] = useState(getDockPosition);
  const [velocity, setVelocity] = useState({ vx: 1.3, vy: 0.8 });
  const [isRoaming, setIsRoaming] = useState(false); // Free-flight patrol
  const [isHovered, setIsHovered] = useState(false);
  const [isWaving, setIsWaving] = useState(false);
  const [isClosed, setIsClosed] = useState(false);
  const [soundEnabled, setSoundEnabled] = useState(true);
  const [dressIndex, setDressIndex] = useState(0);
  const [currentTipIndex, setCurrentTipIndex] = useState(0);
  const [showSpeech, setShowSpeech] = useState(true);

  const selectedDress = COMPANION_DRESSES[dressIndex];
  const waveTimerRef = useRef(null);
  const idleTimerRef = useRef(null);
  const animFrameRef = useRef(null);
  const posRef = useRef(position);
  posRef.current = position;
  const velRef = useRef(velocity);
  velRef.current = velocity;

  // Window resize listener
  useEffect(() => {
    const handleResize = () => {
      setWindowSize({
        w: window.innerWidth,
        h: window.innerHeight
      });
      if (!isRoaming) {
        setPosition(getDockPosition());
      }
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, [isRoaming, getDockPosition]);

  // Idle Detection: After 5 seconds of inactivity, Aero takes off into free-flight patrol
  useEffect(() => {
    const resetIdle = () => {
      if (idleTimerRef.current) clearTimeout(idleTimerRef.current);
      idleTimerRef.current = setTimeout(() => {
        setIsRoaming(true);
        playAeroSynth('whoosh', soundEnabled);
      }, 5500);
    };

    window.addEventListener('mousemove', resetIdle);
    window.addEventListener('keydown', resetIdle);
    window.addEventListener('scroll', resetIdle);
    resetIdle();

    return () => {
      if (idleTimerRef.current) clearTimeout(idleTimerRef.current);
      window.removeEventListener('mousemove', resetIdle);
      window.removeEventListener('keydown', resetIdle);
      window.removeEventListener('scroll', resetIdle);
    };
  }, [soundEnabled]);

  // Free-Flight Motion Physics Engine
  useEffect(() => {
    if (!isRoaming || isHovered) {
      if (animFrameRef.current) cancelAnimationFrame(animFrameRef.current);
      return;
    }

    const minX = 16;
    const maxX = Math.max(minX, window.innerWidth - aeroWidth - 16);
    const minY = 68; // Stay below top navbar
    const maxY = Math.max(minY, window.innerHeight - aeroHeight - 20);

    const step = () => {
      let { x, y } = posRef.current;
      let { vx, vy } = velRef.current;

      x += vx;
      y += vy;

      // Wall reflections with soft bounce
      if (x <= minX) {
        x = minX;
        vx = Math.abs(vx);
      } else if (x >= maxX) {
        x = maxX;
        vx = -Math.abs(vx);
      }

      if (y <= minY) {
        y = minY;
        vy = Math.abs(vy);
      } else if (y >= maxY) {
        y = maxY;
        vy = -Math.abs(vy);
      }

      velRef.current = { vx, vy };
      posRef.current = { x, y };
      setPosition({ x, y });

      animFrameRef.current = requestAnimationFrame(step);
    };

    animFrameRef.current = requestAnimationFrame(step);

    return () => {
      if (animFrameRef.current) cancelAnimationFrame(animFrameRef.current);
    };
  }, [isRoaming, isHovered, aeroWidth, aeroHeight]);

  // Rotate tips periodically
  useEffect(() => {
    const tipTimer = setInterval(() => {
      setCurrentTipIndex((prev) => (prev + 1) % COMPANION_TIPS.length);
    }, 7000);
    return () => clearInterval(tipTimer);
  }, []);

  const triggerWave = () => {
    if (waveTimerRef.current) clearTimeout(waveTimerRef.current);
    setIsWaving(true);
    setShowSpeech(true);
    playAeroSynth('wave', soundEnabled);
    waveTimerRef.current = setTimeout(() => {
      setIsWaving(false);
    }, 2200);
  };

  const handleDockAero = (e) => {
    e.stopPropagation();
    setIsRoaming(false);
    setPosition(getDockPosition());
    playAeroSynth('whoosh', soundEnabled);
  };

  const handleCycleDress = (e) => {
    e.stopPropagation();
    setDressIndex((prev) => (prev + 1) % COMPANION_DRESSES.length);
    playAeroSynth('dress', soundEnabled);
    triggerWave();
  };

  // Do not render floating corner Aero on landing welcome page (since Big Aero is already center)
  if (location.pathname === '/' || location.pathname === '') return null;
  if (isClosed) return null;

  // Calculate tilt angle in flight direction
  const flightTilt = isRoaming && !isHovered ? Math.max(-14, Math.min(14, velRef.current.vx * 8)) : 0;

  return (
    <aside 
      aria-label="Aero Floating AI Companion"
      style={{
        transform: `translate3d(${position.x}px, ${position.y}px, 0px) rotate(${flightTilt}deg)`,
        transition: isRoaming && !isHovered ? 'none' : 'transform 0.4s ease-out'
      }}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      className="fixed top-0 left-0 z-50 pointer-events-auto select-none flex flex-col items-center cursor-pointer group"
      onClick={triggerWave}
    >
      {/* Floating Speech Bubble Above Aero */}
      {showSpeech && (
        <div 
          onClick={(e) => {
            e.stopPropagation();
            setCurrentTipIndex((prev) => (prev + 1) % COMPANION_TIPS.length);
          }}
          className={`absolute bottom-[105%] left-1/2 -translate-x-1/2 max-w-[220px] sm:max-w-[260px] p-2 sm:p-2.5 rounded-2xl bg-slate-900/95 backdrop-blur-xl border border-indigo-500/40 text-slate-100 shadow-2xl shadow-indigo-500/25 flex items-start gap-2 text-left mb-1 transition-all duration-300 animate-in fade-in slide-in-from-bottom-2 ${
            isMobile ? 'text-[10px]' : 'text-xs'
          }`}
          title="Click to cycle next tip"
        >
          <Bot className="w-3.5 h-3.5 text-cyan-400 shrink-0 mt-0.5" />
          <p className="font-medium text-slate-200 leading-snug line-clamp-2">
            {COMPANION_TIPS[currentTipIndex]}
          </p>
          <button
            onClick={(e) => {
              e.stopPropagation();
              setShowSpeech(false);
            }}
            className="text-slate-500 hover:text-white p-0.5 rounded ml-auto shrink-0"
            title="Dismiss speech"
          >
            <X className="w-3 h-3" />
          </button>
        </div>
      )}

      {/* Floating Ambient Glow */}
      <div 
        className="absolute inset-0 rounded-full filter blur-2xl opacity-70 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none scale-110"
        style={{ backgroundColor: selectedDress.glowColor }}
      />

      {/* BIG AERO VECTOR SVG COMPANION (No garden, no child, purely Aero) */}
      <div 
        style={{ width: `${aeroWidth}px`, height: `${aeroHeight}px` }}
        className="relative flex items-center justify-center filter drop-shadow-[0_10px_20px_rgba(0,0,0,0.6)]"
      >
        <svg viewBox="0 0 140 160" className="w-full h-full overflow-visible">
          <defs>
            <linearGradient id="floatingAeroBodyGrad" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0%" stopColor={selectedDress.bodyGrad[0]} />
              <stop offset="50%" stopColor={selectedDress.bodyGrad[1]} />
              <stop offset="100%" stopColor={selectedDress.bodyGrad[2]} />
            </linearGradient>
          </defs>

          {/* Jet Thruster Shadow */}
          <ellipse cx="70" cy="144" rx="30" ry="6" fill="#000000" opacity="0.3" className="animate-pulse" />

          {/* Hovering Motion Group */}
          <g className="animate-robot-hover">
            {/* Jet Flame */}
            <ellipse cx="70" cy="106" rx="12" ry="5" fill={selectedDress.beaconColor} opacity="0.85" />
            <polygon points="62 106, 78 106, 70 128" fill={selectedDress.coreColor} className="animate-pulse" />
            <polygon points="65 106, 75 106, 70 119" fill="#ffffff" />

            {/* Robot Body / Chassis */}
            <rect
              x="40"
              y="50"
              width="60"
              height="52"
              rx="16"
              fill="url(#floatingAeroBodyGrad)"
              stroke={selectedDress.stroke}
              strokeWidth="2.5"
            />
            
            {/* Chest Core Reactor */}
            <circle cx="70" cy="76" r="9" fill={selectedDress.coreColor} className="animate-pulse" />
            <circle cx="70" cy="76" r="4" fill="#ffffff" />

            {/* Robot Head */}
            <rect
              x="44"
              y="14"
              width="52"
              height="36"
              rx="12"
              fill="#0f172a"
              stroke={selectedDress.stroke}
              strokeWidth="2.5"
            />

            {/* Headgear based on dress */}
            {selectedDress.type === 'cat' && (
              <g>
                <polygon points="46,16 38,-4 58,10" fill={selectedDress.stroke} stroke="#fda4af" strokeWidth="1.5" />
                <polygon points="76,10 96,-4 88,16" fill={selectedDress.stroke} stroke="#fda4af" strokeWidth="1.5" />
                <polygon points="45,13 40,2 52,10" fill="#fdf2f8" />
                <polygon points="82,10 94,2 89,13" fill="#fdf2f8" />
              </g>
            )}

            {selectedDress.type === 'halo' && (
              <ellipse cx="70" cy="2" rx="26" ry="6" fill="none" stroke={selectedDress.stroke} strokeWidth="2.5" className="animate-pulse" opacity="0.95" />
            )}

            {selectedDress.type === 'antenna' && (
              <>
                <line x1="70" y1="14" x2="70" y2="2" stroke={selectedDress.stroke} strokeWidth="2.5" />
                <circle cx="70" cy="2" r="4.5" fill={selectedDress.beaconColor} className="animate-ping" style={{ animationDuration: '1.8s' }} />
                <circle cx="70" cy="2" r="3.5" fill={selectedDress.beaconColor} />
              </>
            )}

            {/* Visor Screen with Animated Blinking Eyes */}
            <rect x="50" y="22" width="40" height="20" rx="6" fill="#020617" />
            <g className="animate-visor-blink">
              <ellipse cx="60" cy="32" rx="4.5" ry="5.5" fill={selectedDress.eyeColor} />
              <ellipse cx="80" cy="32" rx="4.5" ry="5.5" fill={selectedDress.eyeColor} />
              <circle cx="62" cy="30" r="1.8" fill="#ffffff" />
              <circle cx="82" cy="30" r="1.8" fill="#ffffff" />
            </g>

            {/* Left Arm (Resting) */}
            <path d="M 40 58 Q 30 70 34 82" fill="none" stroke={selectedDress.bodyGrad[0]} strokeWidth="6" strokeLinecap="round" />

            {/* Right Arm: Natural resting or waving */}
            {isWaving ? (
              <g className="animate-aero-wave">
                <path d="M 100 58 Q 118 40 122 20" fill="none" stroke={selectedDress.bodyGrad[0]} strokeWidth="6.5" strokeLinecap="round" />
                <circle cx="124" cy="18" r="5.5" fill={selectedDress.beaconColor} />
                <circle cx="124" cy="18" r="2.5" fill="#ffffff" />
              </g>
            ) : (
              <g className="transition-all duration-300">
                <path d="M 100 58 Q 110 70 106 82" fill="none" stroke={selectedDress.bodyGrad[0]} strokeWidth="6" strokeLinecap="round" />
                <circle cx="106" cy="82" r="4.5" fill={selectedDress.beaconColor} />
                <circle cx="106" cy="82" r="2" fill="#ffffff" />
              </g>
            )}
          </g>
        </svg>
      </div>

      {/* Floating Micro Controls (Appear on hover/interaction) */}
      <div 
        onClick={(e) => e.stopPropagation()} 
        className="mt-1 flex items-center gap-1 p-1 rounded-full bg-slate-900/90 backdrop-blur-md border border-slate-700/80 shadow-lg transition-opacity duration-200"
      >
        {/* Wave Button */}
        <button
          onClick={triggerWave}
          className="p-1 rounded-full text-cyan-300 hover:bg-slate-800 transition"
          title="Wave at Aero 👋"
        >
          <Sparkles className="w-3.5 h-3.5" />
        </button>

        {/* Roam / Dock Toggle Button */}
        {isRoaming ? (
          <button
            onClick={handleDockAero}
            className="p-1 rounded-full text-amber-300 hover:bg-slate-800 transition"
            title="Dock Aero to Bottom-Right Anchor ⚓"
          >
            <Anchor className="w-3.5 h-3.5" />
          </button>
        ) : (
          <button
            onClick={() => {
              setIsRoaming(true);
              playAeroSynth('whoosh', soundEnabled);
            }}
            className="p-1 rounded-full text-indigo-300 hover:bg-slate-800 transition"
            title="Free-Flight Patrol Mode 🚀"
          >
            <Compass className="w-3.5 h-3.5" />
          </button>
        )}

        {/* Outfit Cycle Button */}
        <button
          onClick={handleCycleDress}
          className="p-1 rounded-full text-purple-300 hover:bg-slate-800 transition"
          title={`Outfit: ${selectedDress.name} (Click to switch)`}
        >
          <Palette className="w-3.5 h-3.5" />
        </button>

        {/* Audio Toggle Button */}
        <button
          onClick={() => setSoundEnabled(!soundEnabled)}
          className="p-1 rounded-full text-slate-400 hover:text-white transition"
          title={soundEnabled ? 'Mute Chimes' : 'Enable Chimes'}
        >
          {soundEnabled ? <Volume2 className="w-3.5 h-3.5 text-cyan-400" /> : <VolumeX className="w-3.5 h-3.5" />}
        </button>

        {/* Close Button */}
        <button
          onClick={() => setIsClosed(true)}
          className="p-1 rounded-full text-slate-500 hover:text-rose-400 transition"
          title="Hide Aero"
        >
          <X className="w-3 h-3" />
        </button>
      </div>
    </aside>
  );
}
