import React, { useState, useRef, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { 
  Sparkles, 
  ArrowRight, 
  Network, 
  BookOpen, 
  FileText, 
  Briefcase, 
  HelpCircle, 
  Layers,
  PlayCircle,
  Zap,
  Volume2,
  VolumeX,
  Bot,
  Brain,
  Flame,
  Sun,
  Moon,
  CloudRain,
  Sunset,
  ChevronUp,
  MessageSquare
} from 'lucide-react';
import { COMPANION_QUIZ_QUESTIONS } from '../components/GardenCompanion';

/**
 * Web Audio Synthesizer for Aero's sound effects (no external audio files needed)
 */
function playSynthSound(type = 'chime', soundEnabled = true) {
  if (!soundEnabled) return;
  try {
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    if (!AudioCtx) return;
    const ctx = new AudioCtx();
    const now = ctx.currentTime;

    const playTone = (freq, startTime, duration, gainVal = 0.2, wave = 'sine') => {
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

    if (type === 'enter') {
      // Grand celebratory chime (C6 -> E6 -> G6 -> C7)
      playTone(1046.5, now, 0.22, 0.22, 'sine');
      playTone(1318.5, now + 0.08, 0.25, 0.25, 'sine');
      playTone(1567.98, now + 0.16, 0.28, 0.28, 'triangle');
      playTone(2093.0, now + 0.26, 0.5, 0.32, 'sine');

      // Electric sparkle resonance
      const spark = ctx.createOscillator();
      const sparkGain = ctx.createGain();
      spark.type = 'sawtooth';
      spark.frequency.setValueAtTime(1400, now + 0.1);
      spark.frequency.exponentialRampToValueAtTime(3200, now + 0.6);
      sparkGain.gain.setValueAtTime(0.001, now + 0.1);
      sparkGain.gain.linearRampToValueAtTime(0.04, now + 0.25);
      sparkGain.gain.exponentialRampToValueAtTime(0.001, now + 0.6);
      spark.connect(sparkGain);
      sparkGain.connect(ctx.destination);
      spark.start(now + 0.1);
      spark.stop(now + 0.6);
    } else if (type === 'chime') {
      playTone(587.33, now, 0.25, 0.15, 'sine');
      playTone(880, now + 0.08, 0.3, 0.18, 'sine');
    } else if (type === 'whoosh') {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(260, now);
      osc.frequency.exponentialRampToValueAtTime(620, now + 0.25);
      osc.frequency.exponentialRampToValueAtTime(200, now + 0.5);
      gain.gain.setValueAtTime(0.05, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.5);
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start(now);
      osc.stop(now + 0.5);
    } else if (type === 'correct') {
      playTone(587.33, now, 0.15, 0.16, 'sine');
      playTone(880, now + 0.08, 0.2, 0.18, 'sine');
      playTone(1174.66, now + 0.18, 0.35, 0.22, 'sine');
    } else if (type === 'wrong') {
      playTone(220, now, 0.22, 0.16, 'sawtooth');
      playTone(160, now + 0.1, 0.25, 0.16, 'sawtooth');
    }
  } catch (err) {
    console.debug('AudioContext not allowed or supported', err);
  }
}

export default function LandingHeroPage() {
  const navigate = useNavigate();
  const [isEntering, setIsEntering] = useState(false);
  const [soundEnabled, setSoundEnabled] = useState(true);
  
  // Interactive Aero states
  const [isWaving, setIsWaving] = useState(true);
  const [isAirplaneFlying, setIsAirplaneFlying] = useState(false);
  const [petalsBurst, setPetalsBurst] = useState(false);
  const [aeroOffset, setAeroOffset] = useState({ x: 0, y: 0 });
  const [tiltStyle, setTiltStyle] = useState({});
  const sceneRef = useRef(null);

  // Weather / Atmosphere: 'sunset' | 'cosmic' | 'day' | 'rain'
  const [atmosphere, setAtmosphere] = useState('sunset');

  // Welcome tips & trivia cycling
  const welcomeTips = [
    {
      title: "Welcome Greeting",
      text: "Hi there! 👋 Aero and Little Leo welcome you to The Era of AI! Explore the multidimensional universe of machine learning.",
      author: "Aero the AI Bot"
    },
    {
      title: "Shortcut Pro Tip",
      text: "Press ⌘K or Ctrl+K anywhere to instantly search across 170+ concepts and papers!",
      author: "Navigation Tip"
    },
    {
      title: "Interactive Mind Map",
      text: "Explore 41 domain nodes with clickable mathematical formulations and cross-domain links!",
      author: "Graph Feature"
    },
    {
      title: "Did You Know?",
      text: "Attention Is All You Need was published in 2017, revolutionizing Natural Language Processing and spawning modern LLMs!",
      author: "AI History Trivia"
    },
    {
      title: "Curriculum & Vault",
      text: "Master 34 modules from linear algebra to GenAI, plus 150+ technical interview questions!",
      author: "Learning Roadmap"
    },
    {
      title: "Live arXiv Paper Feeds",
      text: "Our research pipeline automatically indexes and summarizes milestone AI papers daily!",
      author: "Automated Feed"
    }
  ];
  const [currentTipIndex, setCurrentTipIndex] = useState(0);

  // Mode: 'tips' or 'quiz'
  const [companionMode, setCompanionMode] = useState('tips');
  const [quizIndex, setQuizIndex] = useState(0);
  const [selectedQuizOption, setSelectedQuizOption] = useState(null);
  const [quizStreak, setQuizStreak] = useState(0);
  const [quizFeedback, setQuizFeedback] = useState(null);

  // Auto-cycle tips periodically
  useEffect(() => {
    const timer = setInterval(() => {
      if (companionMode === 'tips') {
        setCurrentTipIndex((prev) => (prev + 1) % welcomeTips.length);
      }
    }, 8000);
    return () => clearInterval(timer);
  }, [companionMode, welcomeTips.length]);

  // Mouse move handler to make Aero movable & lean towards pointer
  const handleSceneMouseMove = (e) => {
    if (!sceneRef.current) return;
    const rect = sceneRef.current.getBoundingClientRect();
    const xRatio = (e.clientX - rect.left) / rect.width - 0.5; // -0.5 to 0.5
    const yRatio = (e.clientY - rect.top) / rect.height - 0.5; // -0.5 to 0.5

    // Move Aero smoothly in response to mouse
    setAeroOffset({
      x: Math.round(xRatio * 32),
      y: Math.round(yRatio * 20)
    });

    // Gentle 3D perspective tilt
    const rotateX = -yRatio * 10;
    const rotateY = xRatio * 10;
    setTiltStyle({
      transform: `perspective(900px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`
    });
  };

  const handleSceneMouseLeave = () => {
    setAeroOffset({ x: 0, y: 0 });
    setTiltStyle({
      transform: 'perspective(900px) rotateX(0deg) rotateY(0deg)'
    });
  };

  const triggerWave = () => {
    setIsWaving(false);
    playSynthSound('chime', soundEnabled);
    setTimeout(() => setIsWaving(true), 50);
  };

  const launchAirplane = () => {
    if (isAirplaneFlying) return;
    setIsAirplaneFlying(true);
    playSynthSound('whoosh', soundEnabled);
    setTimeout(() => {
      setIsAirplaneFlying(false);
    }, 2200);
  };

  const triggerPetals = () => {
    setPetalsBurst(true);
    playSynthSound('chime', soundEnabled);
    setTimeout(() => setPetalsBurst(false), 1600);
  };

  const handleNextTip = () => {
    setCurrentTipIndex((prev) => (prev + 1) % welcomeTips.length);
    triggerWave();
  };

  const handleSelectQuizOption = (optIndex) => {
    if (selectedQuizOption !== null) return;
    setSelectedQuizOption(optIndex);
    const q = COMPANION_QUIZ_QUESTIONS[quizIndex];
    if (optIndex === q.correct) {
      setQuizFeedback('correct');
      setQuizStreak((prev) => prev + 1);
      playSynthSound('correct', soundEnabled);
      triggerPetals();
    } else {
      setQuizFeedback('wrong');
      setQuizStreak(0);
      playSynthSound('wrong', soundEnabled);
    }
  };

  const handleNextQuizQuestion = () => {
    setSelectedQuizOption(null);
    setQuizFeedback(null);
    setQuizIndex((prev) => (prev + 1) % COMPANION_QUIZ_QUESTIONS.length);
  };

  const handleEnterWorld = (e) => {
    e.preventDefault();
    if (isEntering) return;
    setIsEntering(true);
    triggerWave();
    playSynthSound('enter', soundEnabled);

    // Cheerful speech synthesis
    try {
      if ('speechSynthesis' in window && soundEnabled) {
        window.speechSynthesis.cancel();
        const utter = new SpeechSynthesisUtterance('Entering The World of AI!');
        utter.pitch = 1.4;
        utter.rate = 1.2;
        utter.volume = 0.6;
        window.speechSynthesis.speak(utter);
      }
    } catch {
      // Ignore speech errors
    }

    setTimeout(() => {
      navigate('/mindmap');
    }, 650);
  };

  const getSkyBgClass = () => {
    switch (atmosphere) {
      case 'day': return 'bg-gradient-to-b from-sky-500 via-sky-300 to-indigo-100';
      case 'sunset': return 'bg-gradient-to-b from-orange-600 via-pink-600 to-indigo-950';
      case 'rain': return 'bg-gradient-to-b from-slate-900 via-cyan-950 to-slate-950';
      case 'cosmic':
      default: return 'bg-gradient-to-b from-indigo-950 via-slate-900 to-slate-950';
    }
  };

  const portalCards = [
    {
      to: '/mindmap',
      title: 'Interactive Mind Map',
      subtitle: '41 domain nodes & cross-domain links',
      icon: Network,
      color: 'from-indigo-500/20 to-indigo-600/10 border-indigo-500/30 text-indigo-400',
      badge: 'Interactive 2D Graph'
    },
    {
      to: '/syllabus',
      title: 'Line-Wise Syllabus',
      subtitle: '34 modules from linear algebra to GenAI',
      icon: BookOpen,
      color: 'from-blue-500/20 to-blue-600/10 border-blue-500/30 text-blue-400',
      badge: 'Core Curriculum'
    },
    {
      to: '/papers',
      title: 'Landmark Research Papers',
      subtitle: '22+ milestone papers with arXiv feeds',
      icon: FileText,
      color: 'from-amber-500/20 to-amber-600/10 border-amber-500/30 text-amber-400',
      badge: 'Daily arXiv'
    },
    {
      to: '/concepts',
      title: 'Core Concepts & Math',
      subtitle: '170+ in-depth technical breakdowns',
      icon: Layers,
      color: 'from-rose-500/20 to-rose-600/10 border-rose-500/30 text-rose-400',
      badge: 'Deep Derivations'
    },
    {
      to: '/interview',
      title: 'Interview Vault',
      subtitle: '150+ math, coding & design questions',
      icon: HelpCircle,
      color: 'from-purple-500/20 to-purple-600/10 border-purple-500/30 text-purple-400',
      badge: '150+ QA Vault'
    },
    {
      to: '/playgrounds',
      title: 'ML Playgrounds & Labs',
      subtitle: 'Attention heatmaps & Python sandbox',
      icon: PlayCircle,
      color: 'from-cyan-500/20 to-cyan-600/10 border-cyan-500/30 text-cyan-400',
      badge: 'WebAssembly Pyodide'
    }
  ];

  const currentTip = welcomeTips[currentTipIndex];

  return (
    <div className={`relative flex-1 w-full h-full overflow-y-auto bg-slate-950 text-slate-100 flex flex-col items-center justify-start select-none transition-all duration-700 ${
      isEntering ? 'opacity-0 scale-105 filter blur-sm pointer-events-none' : 'opacity-100 scale-100'
    }`}>
      {/* Background Ambient Cosmic Atmosphere */}
      <div className="fixed inset-0 pointer-events-none bg-[radial-gradient(ellipse_80%_80%_at_50%_-10%,rgba(99,102,241,0.22),rgba(56,189,248,0.15),rgba(2,6,23,0.98))]" />
      <div className="fixed inset-0 pointer-events-none bg-gradient-to-b from-slate-950/70 via-slate-950/90 to-slate-950" />

      {/* Main Container */}
      <div className="relative z-10 w-full max-w-4xl mx-auto px-4 sm:px-6 py-6 sm:py-8 flex flex-col items-center text-center space-y-5">
        
        {/* Top Badges & Audio Toggle */}
        <div className="flex items-center justify-between w-full max-w-xl gap-2">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-indigo-500/10 border border-indigo-500/30 text-indigo-300 text-xs font-semibold shadow-lg shadow-indigo-500/10">
            <Bot className="w-3.5 h-3.5 text-cyan-400 animate-bounce" />
            <span>Meet Aero &amp; Little Leo • Your AI Guides</span>
          </div>

          <button
            onClick={() => setSoundEnabled(!soundEnabled)}
            className="p-1.5 px-2.5 rounded-full bg-slate-900 border border-slate-700/80 hover:bg-slate-800 text-slate-400 hover:text-cyan-300 text-xs font-medium flex items-center gap-1.5 transition"
            title={soundEnabled ? 'Mute Chimes' : 'Enable Chimes'}
          >
            {soundEnabled ? <Volume2 className="w-3.5 h-3.5 text-cyan-400" /> : <VolumeX className="w-3.5 h-3.5 text-slate-500" />}
            <span className="text-[10px]">{soundEnabled ? 'Audio ON' : 'Muted'}</span>
          </button>
        </div>

        {/* Hero Headline */}
        <div className="space-y-1.5 max-w-2xl">
          <h1 className="text-3xl sm:text-4xl md:text-5xl font-black tracking-tight text-white leading-tight">
            The Era of <span className="bg-gradient-to-r from-cyan-400 via-indigo-300 to-purple-400 bg-clip-text text-transparent">AI</span>
          </h1>
          <p className="text-xs sm:text-sm text-slate-300 font-normal leading-relaxed">
            Welcome! Move your cursor to watch Aero fly, tap the actions to play, or hit the glowing button to enter the knowledge universe.
          </p>
        </div>

        {/* LIVE MOVABLE WAVING AERO & LITTLE LEO WELCOME CONSOLE (VECTOR SVG DIORAMA) */}
        <div 
          ref={sceneRef}
          onMouseMove={handleSceneMouseMove}
          onMouseLeave={handleSceneMouseLeave}
          style={tiltStyle}
          className="relative w-full max-w-xl rounded-3xl overflow-hidden border-2 border-cyan-500/40 bg-slate-900 shadow-[0_0_50px_rgba(99,102,241,0.25)] ring-4 ring-indigo-500/20 transition-transform duration-200"
        >
          {/* Header Bar: Atmosphere Weather Selector & Aero Status */}
          <div className="px-4 py-2 bg-slate-950/90 border-b border-slate-800/80 flex items-center justify-between text-xs">
            <div className="flex items-center gap-2">
              <span className="relative flex h-2.5 w-2.5">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75" />
                <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-cyan-500" />
              </span>
              <span className="font-bold text-white tracking-wide text-xs">
                Aero AI &amp; Little Leo
              </span>
              <span className="text-[10px] text-cyan-300/80 font-mono hidden sm:inline">
                • Interactive Garden
              </span>
            </div>

            {/* Atmosphere Weather Pills */}
            <div className="flex items-center gap-1 bg-slate-900/90 p-0.5 rounded-lg border border-slate-800">
              <button
                onClick={() => setAtmosphere('sunset')}
                className={`p-1 rounded-md transition ${atmosphere === 'sunset' ? 'bg-orange-500/30 text-orange-300' : 'text-slate-400 hover:text-white'}`}
                title="Sunset Sky"
              >
                <Sunset className="w-3.5 h-3.5" />
              </button>
              <button
                onClick={() => setAtmosphere('cosmic')}
                className={`p-1 rounded-md transition ${atmosphere === 'cosmic' ? 'bg-indigo-500/30 text-indigo-300' : 'text-slate-400 hover:text-white'}`}
                title="Cosmic Night"
              >
                <Moon className="w-3.5 h-3.5" />
              </button>
              <button
                onClick={() => setAtmosphere('day')}
                className={`p-1 rounded-md transition ${atmosphere === 'day' ? 'bg-amber-500/30 text-amber-300' : 'text-slate-400 hover:text-white'}`}
                title="Sunny Day"
              >
                <Sun className="w-3.5 h-3.5" />
              </button>
              <button
                onClick={() => setAtmosphere('rain')}
                className={`p-1 rounded-md transition ${atmosphere === 'rain' ? 'bg-cyan-500/30 text-cyan-300' : 'text-slate-400 hover:text-white'}`}
                title="Rain Garden"
              >
                <CloudRain className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>

          {/* SVG Garden Diorama Canvas */}
          <div className={`relative w-full h-56 sm:h-64 ${getSkyBgClass()} transition-colors duration-700 overflow-hidden flex items-end justify-center cursor-pointer`}
               onClick={triggerWave}
               title="Move mouse to guide Aero • Click anywhere to wave!">
            
            {/* Stars & Floating Sparkles in Sky */}
            <div className="absolute inset-0 opacity-60 pointer-events-none">
              <div className="absolute top-3 left-8 w-1 h-1 rounded-full bg-cyan-300 animate-ping" style={{ animationDuration: '3s' }} />
              <div className="absolute top-10 right-14 w-1.5 h-1.5 rounded-full bg-amber-300 animate-ping" style={{ animationDuration: '2.5s' }} />
              <div className="absolute top-16 left-1/3 w-1 h-1 rounded-full bg-purple-300 animate-ping" style={{ animationDuration: '4s' }} />
              <div className="absolute top-6 left-2/3 w-1.5 h-1.5 rounded-full bg-emerald-300 animate-ping" style={{ animationDuration: '3.5s' }} />
            </div>

            {/* Flying Flower Petals Burst Animation */}
            {petalsBurst && (
              <div className="absolute inset-0 pointer-events-none z-30 animate-pulse">
                {[
                  { left: '20%', top: '40%', color: '#f472b6', rot: '15deg' },
                  { left: '45%', top: '25%', color: '#38bdf8', rot: '-20deg' },
                  { left: '70%', top: '35%', color: '#fef08a', rot: '45deg' },
                  { left: '35%', top: '55%', color: '#c084fc', rot: '-10deg' },
                  { left: '80%', top: '50%', color: '#fb7185', rot: '30deg' }
                ].map((p, idx) => (
                  <div
                    key={idx}
                    className="absolute w-3 h-3 rounded-full animate-bounce"
                    style={{
                      left: p.left,
                      top: p.top,
                      backgroundColor: p.color,
                      transform: `rotate(${p.rot})`,
                      boxShadow: `0 0 10px ${p.color}`
                    }}
                  />
                ))}
              </div>
            )}

            {/* Responsive Scalable SVG Diorama */}
            <svg viewBox="0 0 400 180" className="w-full h-full overflow-visible">
              <defs>
                {/* Grass Gradients */}
                <linearGradient id="landingGrassGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#059669" />
                  <stop offset="100%" stopColor="#064e3b" />
                </linearGradient>

                {/* Robot Metallic Gradient */}
                <linearGradient id="landingRobotBodyGrad" x1="0" y1="0" x2="1" y2="1">
                  <stop offset="0%" stopColor="#6366f1" />
                  <stop offset="50%" stopColor="#4338ca" />
                  <stop offset="100%" stopColor="#312e81" />
                </linearGradient>

                {/* Flower Petal Gradient */}
                <linearGradient id="landingPetalGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#f472b6" />
                  <stop offset="100%" stopColor="#ec4899" />
                </linearGradient>
              </defs>

              {/* Sky Elements based on Atmosphere */}
              {atmosphere === 'day' && (
                <g className="day-sky">
                  <circle cx="330" cy="34" r="22" fill="#fef08a" opacity="0.3" className="animate-pulse" />
                  <circle cx="330" cy="34" r="14" fill="#facc15" />
                  <g fill="#ffffff" opacity="0.85">
                    <path d="M 60 28 Q 72 18 86 22 Q 98 16 112 26 Q 118 33 105 36 Q 75 38 60 28 Z" />
                    <path d="M 210 22 Q 220 15 232 17 Q 245 12 255 21 Q 260 27 248 30 Q 225 32 210 22 Z" opacity="0.8" />
                  </g>
                </g>
              )}

              {atmosphere === 'sunset' && (
                <g className="sunset-sky">
                  <circle cx="300" cy="46" r="26" fill="#f97316" opacity="0.4" className="animate-pulse" />
                  <circle cx="300" cy="46" r="16" fill="#ea580c" />
                  <path d="M 40 42 Q 120 36 180 40 Q 130 46 40 44 Z" fill="#fda4af" opacity="0.5" />
                  <path d="M 220 38 Q 290 32 360 40 Q 310 44 220 41 Z" fill="#f43f5e" opacity="0.45" />
                </g>
              )}

              {atmosphere === 'cosmic' && (
                <g className="cosmic-sky">
                  <path
                    d="M 335 20 A 13 13 0 1 0 348 33 A 11 11 0 1 1 335 20 Z"
                    fill="#fef08a"
                    opacity="0.95"
                  />
                  <circle cx="338" cy="22" r="1.5" fill="#fef9c3" className="animate-ping" style={{ animationDuration: '3s' }} />
                </g>
              )}

              {atmosphere === 'rain' && (
                <g className="rain-sky">
                  <path d="M 35 15 Q 65 5 95 12 Q 130 6 165 20 Q 140 28 45 25 Z" fill="#334155" opacity="0.85" />
                  <path d="M 200 12 Q 240 4 285 14 Q 340 8 365 22 Q 300 28 210 24 Z" fill="#334155" opacity="0.85" />
                  {[20, 55, 90, 130, 165, 205, 240, 280, 315, 355, 385].map((rx, idx) => (
                    <line
                      key={idx}
                      x1={rx}
                      y1={24 + (idx % 4) * 8}
                      x2={rx - 10}
                      y2={60 + (idx % 4) * 8}
                      stroke="#38bdf8"
                      strokeWidth="1.2"
                      strokeDasharray="4,6"
                      opacity="0.65"
                      className="animate-pulse"
                    />
                  ))}
                </g>
              )}

              {/* Rolling Grassy Hills */}
              <path
                d="M -20 180 Q 90 135 200 150 T 420 180 Z"
                fill="url(#landingGrassGrad)"
                opacity="0.95"
              />
              <path
                d="M -20 180 Q 150 145 280 155 T 420 180 Z"
                fill="#047857"
                opacity="0.75"
              />

              {/* Glowing Garden Flowers */}
              <g className="flowers">
                <circle cx="45" cy="155" r="4.5" fill="url(#landingPetalGrad)" />
                <circle cx="45" cy="155" r="1.5" fill="#fef08a" />
                <line x1="45" y1="155" x2="45" y2="170" stroke="#10b981" strokeWidth="1.5" />

                <circle cx="105" cy="160" r="5" fill="#c084fc" />
                <circle cx="105" cy="160" r="2" fill="#fef08a" />
                <line x1="105" y1="160" x2="105" y2="172" stroke="#10b981" strokeWidth="1.5" />

                <circle cx="340" cy="162" r="4.5" fill="#38bdf8" />
                <circle cx="340" cy="162" r="1.5" fill="#ffffff" />
                <line x1="340" y1="162" x2="340" y2="174" stroke="#10b981" strokeWidth="1.5" />

                <circle cx="375" cy="158" r="4" fill="url(#landingPetalGrad)" />
                <circle cx="375" cy="158" r="1.5" fill="#fef08a" />
                <line x1="375" y1="158" x2="375" y2="170" stroke="#10b981" strokeWidth="1.5" />
              </g>

              {/* Holographic Fluttering Butterflies */}
              <g className="animate-butterfly" transform="translate(160, 65)">
                <ellipse cx="-4" cy="-2" rx="5" ry="3.5" fill="#f472b6" opacity="0.85" transform="rotate(-25)" />
                <ellipse cx="4" cy="-2" rx="5" ry="3.5" fill="#f472b6" opacity="0.85" transform="rotate(25)" />
                <ellipse cx="0" cy="0" rx="1" ry="4" fill="#ffffff" />
              </g>
              <g className="animate-butterfly-slow" transform="translate(230, 95)">
                <ellipse cx="-3" cy="-1.5" rx="4" ry="2.5" fill="#38bdf8" opacity="0.85" transform="rotate(-30)" />
                <ellipse cx="3" cy="-1.5" rx="4" ry="2.5" fill="#38bdf8" opacity="0.85" transform="rotate(30)" />
                <ellipse cx="0" cy="0" rx="0.8" ry="3" fill="#ffffff" />
              </g>

              {/* 1. LITTLE LEO (The Child Waving & Playing in the Garden) */}
              <g id="childCharacter" transform="translate(265, 110)">
                {/* Shadow */}
                <ellipse cx="15" cy="52" rx="14" ry="4" fill="#000000" opacity="0.3" />

                {/* Legs sitting on grass */}
                <path d="M 6 42 Q 10 50 16 50 T 26 50" fill="none" stroke="#1e293b" strokeWidth="5" strokeLinecap="round" />

                {/* Torso / Warm Golden Jacket */}
                <path d="M 8 26 L 22 26 L 25 43 L 5 43 Z" fill="#f59e0b" rx="3" />

                {/* Collar */}
                <path d="M 9 26 Q 15 29 21 26" fill="none" stroke="#ef4444" strokeWidth="3" strokeLinecap="round" />

                {/* Head */}
                <circle cx="15" cy="15" r="10" fill="#fed7aa" />

                {/* Hair */}
                <path d="M 6 14 Q 15 4 24 14 Q 22 8 15 7 Q 8 8 6 14 Z" fill="#78350f" />

                {/* Happy Face */}
                <circle cx="12" cy="15" r="1.2" fill="#1e293b" />
                <circle cx="18" cy="15" r="1.2" fill="#1e293b" />
                <path d="M 13 18 Q 15 20 17 18" fill="none" stroke="#1e293b" strokeWidth="1" strokeLinecap="round" />

                {/* Arm reaching out and waving towards Aero */}
                <path d="M 7 28 Q -2 22 -6 18" fill="none" stroke="#fed7aa" strokeWidth="3.5" strokeLinecap="round" className="animate-reach" />
                <circle cx="-7" cy="17" r="2.5" fill="#fed7aa" />

                {/* Other arm resting on knee */}
                <path d="M 23 28 Q 28 34 25 40" fill="none" stroke="#f59e0b" strokeWidth="3.5" strokeLinecap="round" />
              </g>

              {/* 2. AERO THE AI BOT (Hovering, Movable, Waving Arm, Blinking Eyes) */}
              <g 
                id="robotCharacter" 
                transform={`translate(${90 + aeroOffset.x}, ${85 + aeroOffset.y})`}
                className="transition-transform duration-100 ease-out cursor-pointer"
                onClick={(e) => {
                  e.stopPropagation();
                  triggerWave();
                }}
              >
                {/* Thruster Flame Shadow */}
                <ellipse cx="20" cy="72" rx="15" ry="3.5" fill="#000000" opacity="0.35" className="animate-pulse" />
                
                {/* Hovering Group */}
                <g className="animate-robot-hover">
                  {/* Jet Flame & Glow */}
                  <ellipse cx="20" cy="52" rx="6" ry="3" fill="#38bdf8" opacity="0.85" />
                  <polygon points="16 52, 24 52, 20 63" fill="#06b6d4" className="animate-pulse" />
                  <polygon points="18 52, 22 52, 20 59" fill="#ffffff" />

                  {/* Body / Chassis */}
                  <rect
                    x="5"
                    y="24"
                    width="30"
                    height="26"
                    rx="8"
                    fill="url(#landingRobotBodyGrad)"
                    stroke="#818cf8"
                    strokeWidth="1.5"
                  />
                  
                  {/* Core Reactor */}
                  <circle cx="20" cy="37" r="4.5" fill="#06b6d4" className="animate-pulse" />
                  <circle cx="20" cy="37" r="2" fill="#ffffff" />

                  {/* Robot Head */}
                  <rect
                    x="7"
                    y="6"
                    width="26"
                    height="18"
                    rx="6"
                    fill="#1e1b4b"
                    stroke="#818cf8"
                    strokeWidth="1.5"
                  />

                  {/* Antenna with Pulsing Beacon */}
                  <line x1="20" y1="6" x2="20" y2="0" stroke="#818cf8" strokeWidth="1.5" />
                  <circle cx="20" cy="0" r="2.5" fill="#38bdf8" className="animate-ping" style={{ animationDuration: '1.8s' }} />
                  <circle cx="20" cy="0" r="2" fill="#38bdf8" />

                  {/* Visor Screen with Animated Blinking Eyes */}
                  <rect x="10" y="10" width="20" height="10" rx="3" fill="#020617" />
                  <g className="animate-visor-blink">
                    <ellipse cx="15" cy="15" rx="2.5" ry="3" fill="#06b6d4" />
                    <ellipse cx="25" cy="15" rx="2.5" ry="3" fill="#06b6d4" />
                    <circle cx="16" cy="14" r="1" fill="#ffffff" />
                    <circle cx="26" cy="14" r="1" fill="#ffffff" />
                  </g>

                  {/* Left Arm (Resting) */}
                  <path d="M 5 28 Q 0 34 2 40" fill="none" stroke="#6366f1" strokeWidth="3" strokeLinecap="round" />

                  {/* Right Arm: MOVABLE & WAVING ARM */}
                  <g className={isWaving ? "animate-wave" : ""}>
                    <path d="M 35 28 Q 44 20 46 10" fill="none" stroke="#6366f1" strokeWidth="3.5" strokeLinecap="round" />
                    <circle cx="47" cy="9" r="3" fill="#38bdf8" />
                    <circle cx="47" cy="9" r="1.5" fill="#ffffff" />
                  </g>
                </g>
              </g>

              {/* Paper Airplane Flying from Child to Robot */}
              {isAirplaneFlying && (
                <g className="animate-pulse">
                  <path d="M 310 115 Q 260 65 200 80" fill="none" stroke="#e0e7ff" strokeWidth="1.8" strokeDasharray="3,3" opacity="0.85" />
                  <polygon points="0,0 14,4 0,8 3,4" fill="#ffffff" stroke="#6366f1" strokeWidth="1" transform="translate(240, 82) rotate(-165)" />
                </g>
              )}
            </svg>

            {/* Click to wave prompt overlay tag */}
            <div className="absolute bottom-2.5 inset-x-0 flex justify-center pointer-events-none">
              <span className="text-[10px] font-bold tracking-wide text-cyan-200/90 bg-slate-950/85 backdrop-blur-md px-3 py-1 rounded-full border border-cyan-500/30 shadow-md">
                🤖 Movable Waving Aero • Click or hover to interact ✨
              </span>
            </div>
          </div>

          {/* Console Bottom Area: Tips & Interactive Buttons */}
          <div className="p-3.5 bg-slate-950/95 border-t border-slate-800/80 text-left">
            {companionMode === 'tips' ? (
              <>
                {/* Speech / Tip Card */}
                <div className="flex items-start gap-2.5 mb-2.5">
                  <div className="w-7 h-7 rounded-lg bg-indigo-500/20 border border-indigo-500/30 flex items-center justify-center shrink-0 mt-0.5 text-cyan-400">
                    <MessageSquare className="w-3.5 h-3.5" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between">
                      <span className="text-[11px] font-bold text-cyan-300">
                        {currentTip.title}
                      </span>
                      <span className="text-[10px] font-mono text-slate-500">
                        {currentTipIndex + 1}/{welcomeTips.length}
                      </span>
                    </div>
                    <p className="text-xs text-slate-200 mt-0.5 leading-relaxed font-normal">
                      {currentTip.text}
                    </p>
                  </div>
                </div>

                {/* Interactive Action Buttons */}
                <div className="flex items-center justify-between gap-1.5 pt-1 text-xs flex-wrap">
                  <div className="flex items-center gap-1.5 flex-wrap">
                    <button
                      onClick={triggerWave}
                      className="px-2.5 py-1 rounded-lg bg-slate-900 hover:bg-indigo-600/30 text-slate-200 hover:text-white border border-slate-700/60 transition flex items-center gap-1 text-[11px] font-medium"
                      title="Wave back at Aero"
                    >
                      <Sparkles className="w-3 h-3 text-cyan-400" />
                      <span>Wave 👋</span>
                    </button>

                    <button
                      onClick={launchAirplane}
                      className="px-2.5 py-1 rounded-lg bg-slate-900 hover:bg-cyan-600/30 text-slate-200 hover:text-white border border-slate-700/60 transition flex items-center gap-1 text-[11px] font-medium"
                      title="Fly paper airplane between Leo & Aero"
                    >
                      <span>Fly Plane ✈️</span>
                    </button>

                    <button
                      onClick={triggerPetals}
                      className="px-2.5 py-1 rounded-lg bg-slate-900 hover:bg-pink-600/30 text-slate-200 hover:text-white border border-slate-700/60 transition flex items-center gap-1 text-[11px] font-medium"
                      title="Bloom garden flowers"
                    >
                      <span>Bloom 🌸</span>
                    </button>

                    <button
                      onClick={() => {
                        setCompanionMode('quiz');
                        playSynthSound('chime', soundEnabled);
                      }}
                      className="px-2.5 py-1 rounded-lg bg-gradient-to-r from-amber-500/20 to-orange-500/20 hover:from-amber-500/30 hover:to-orange-500/30 text-amber-300 border border-amber-500/40 font-semibold text-[11px] flex items-center gap-1 shadow-sm"
                      title="Test your AI knowledge with Aero's quick quiz"
                    >
                      <Brain className="w-3 h-3 text-amber-400" />
                      <span>Quiz Me! 🧠</span>
                    </button>
                  </div>

                  <button
                    onClick={handleNextTip}
                    className="px-3 py-1 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-medium transition text-[11px] flex items-center gap-1 shadow-sm ml-auto"
                  >
                    <span>Next</span>
                    <ChevronUp className="w-3 h-3 rotate-90" />
                  </button>
                </div>
              </>
            ) : (
              /* Quick-Fire Quiz Mode */
              <div className="space-y-2 animate-in fade-in duration-200">
                <div className="flex items-center justify-between text-[11px] border-b border-slate-800 pb-1.5">
                  <div className="flex items-center gap-1.5 font-bold text-amber-300">
                    <Brain className="w-3.5 h-3.5 text-amber-400" />
                    <span>Aero's AI Quiz</span>
                    <span className="text-[10px] font-mono text-slate-400 font-normal">
                      (Q{quizIndex + 1}/{COMPANION_QUIZ_QUESTIONS.length})
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    {quizStreak > 0 && (
                      <span className="flex items-center gap-1 text-[10px] font-mono font-bold text-orange-400 bg-orange-500/15 border border-orange-500/30 px-1.5 py-0.5 rounded-full">
                        <Flame className="w-3 h-3 text-orange-400 fill-orange-400" />
                        {quizStreak} Streak
                      </span>
                    )}
                    <button
                      onClick={() => setCompanionMode('tips')}
                      className="text-[10px] text-slate-400 hover:text-white px-2 py-0.5 rounded hover:bg-slate-800 transition"
                    >
                      Back to Tips
                    </button>
                  </div>
                </div>

                <p className="text-xs text-white font-semibold leading-snug">
                  {COMPANION_QUIZ_QUESTIONS[quizIndex].question}
                </p>

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

                {selectedQuizOption !== null && (
                  <div className="flex items-center justify-between gap-2 pt-1 border-t border-slate-800">
                    <p className="text-[11px] text-cyan-200/90 leading-tight">
                      {COMPANION_QUIZ_QUESTIONS[quizIndex].tip}
                    </p>
                    <button
                      onClick={handleNextQuizQuestion}
                      className="px-3 py-1 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-[11px] shrink-0"
                    >
                      Next Question &gt;
                    </button>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Hand Pointing Down Indicator Arrow */}
        <div className="flex flex-col items-center justify-center animate-bounce text-cyan-400 pt-1">
          <span className="text-[10px] font-bold tracking-widest uppercase text-cyan-300">Enter Here</span>
          <div className="w-1.5 h-5 bg-gradient-to-b from-cyan-400 to-transparent rounded-full mt-0.5" />
        </div>

        {/* THE GIANT GLOWING ELECTRIC ENTER BUTTON */}
        <div className="relative w-full max-w-md px-4">
          <button
            onClick={handleEnterWorld}
            id="hero-center-enter-btn"
            className="w-full group relative inline-flex items-center justify-center gap-3.5 px-8 sm:px-10 py-4 sm:py-5 rounded-2xl bg-gradient-to-r from-cyan-500 via-indigo-600 to-purple-600 hover:from-cyan-400 hover:via-indigo-500 hover:to-purple-500 text-white font-black text-lg sm:text-xl md:text-2xl shadow-[0_0_40px_rgba(6,182,212,0.55)] hover:shadow-[0_0_60px_rgba(56,189,248,0.85)] border-2 border-cyan-200 hover:scale-105 active:scale-95 transition-all duration-200 cursor-pointer animate-electric-pulse"
          >
            <Bot className="w-6 h-6 text-white animate-bounce shrink-0" />
            <span className="tracking-wide uppercase drop-shadow-sm font-extrabold">
              Enter the World of AI
            </span>
            <ArrowRight className="w-6 h-6 group-hover:translate-x-1.5 transition-transform shrink-0 text-white" />
          </button>
          <p className="text-[11px] text-cyan-300/80 mt-2 text-center font-medium">
            Chimes with Aero &amp; transitions into 2D Knowledge Graph
          </p>
        </div>

        {/* Quick Direct Section Cards */}
        <div className="w-full max-w-3xl pt-2">
          <div className="text-xs text-slate-400 font-semibold uppercase tracking-wider mb-3">
            Or jump directly into any section:
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-2.5">
            {portalCards.map((portal, idx) => {
              const Icon = portal.icon;
              return (
                <Link
                  key={idx}
                  to={portal.to}
                  className={`p-3 rounded-xl bg-slate-900/60 hover:bg-slate-900 border transition-all text-left flex items-center justify-between group shadow-sm hover:border-cyan-500/40 hover:scale-[1.02] ${portal.color}`}
                >
                  <div className="min-w-0 flex items-center gap-2.5">
                    <div className="w-7 h-7 rounded-lg bg-slate-800/80 flex items-center justify-center shrink-0">
                      <Icon className="w-3.5 h-3.5" />
                    </div>
                    <div className="min-w-0">
                      <h4 className="text-xs font-bold text-white group-hover:text-cyan-300 truncate">
                        {portal.title}
                      </h4>
                      <p className="text-[10px] text-slate-400 truncate">
                        {portal.badge}
                      </p>
                    </div>
                  </div>
                  <ArrowRight className="w-3.5 h-3.5 text-slate-500 group-hover:text-cyan-300 shrink-0 ml-1" />
                </Link>
              );
            })}
          </div>
        </div>

        {/* Key Curriculum Metrics Bar */}
        <div className="w-full max-w-3xl pt-4 border-t border-slate-800/80 flex items-center justify-around flex-wrap gap-4 text-center">
          <div>
            <div className="text-lg sm:text-xl font-black text-cyan-300 font-mono">41</div>
            <div className="text-[10px] text-slate-400 uppercase tracking-wider font-semibold">Graph Nodes</div>
          </div>
          <div className="w-px h-6 bg-slate-800 hidden sm:block" />
          <div>
            <div className="text-lg sm:text-xl font-black text-cyan-300 font-mono">34</div>
            <div className="text-[10px] text-slate-400 uppercase tracking-wider font-semibold">Syllabus Modules</div>
          </div>
          <div className="w-px h-6 bg-slate-800 hidden sm:block" />
          <div>
            <div className="text-lg sm:text-xl font-black text-cyan-300 font-mono">170+</div>
            <div className="text-[10px] text-slate-400 uppercase tracking-wider font-semibold">Core Concepts</div>
          </div>
          <div className="w-px h-6 bg-slate-800 hidden sm:block" />
          <div>
            <div className="text-lg sm:text-xl font-black text-cyan-300 font-mono">150+</div>
            <div className="text-[10px] text-slate-400 uppercase tracking-wider font-semibold">Interview Q&amp;A</div>
          </div>
          <div className="w-px h-6 bg-slate-800 hidden sm:block" />
          <div>
            <div className="text-lg sm:text-xl font-black text-cyan-300 font-mono">22+</div>
            <div className="text-[10px] text-slate-400 uppercase tracking-wider font-semibold">Landmark Papers</div>
          </div>
        </div>

      </div>
    </div>
  );
}
