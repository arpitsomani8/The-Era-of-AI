import React, { useState, useRef } from 'react';
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
  Bot
} from 'lucide-react';

/**
 * Web Audio Synthesizer for Aero's cheerful futuristic chime & robotic chirp
 */
function playAeroSound() {
  try {
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    if (!AudioCtx) return;
    const ctx = new AudioCtx();
    const now = ctx.currentTime;

    // Helper to generate a sweet harmonic chime note
    const playNote = (freq, startTime, duration, gainVal = 0.22, wave = 'sine') => {
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

    // Melodic Futuristic Chime (C6 -> E6 -> G6 -> C7)
    playNote(1046.5, now, 0.18, 0.2, 'sine');          // C6
    playNote(1318.5, now + 0.08, 0.2, 0.22, 'sine');   // E6
    playNote(1567.98, now + 0.16, 0.22, 0.25, 'triangle'); // G6
    playNote(2093.0, now + 0.26, 0.45, 0.28, 'sine');  // High C7 chime

    // Cute sub-bass thruster hum & electric sparkle
    const spark = ctx.createOscillator();
    const sparkGain = ctx.createGain();
    spark.type = 'sawtooth';
    spark.frequency.setValueAtTime(1400, now + 0.1);
    spark.frequency.exponentialRampToValueAtTime(2800, now + 0.5);
    sparkGain.gain.setValueAtTime(0.001, now + 0.1);
    sparkGain.gain.linearRampToValueAtTime(0.05, now + 0.25);
    sparkGain.gain.exponentialRampToValueAtTime(0.001, now + 0.55);
    spark.connect(sparkGain);
    sparkGain.connect(ctx.destination);
    spark.start(now + 0.1);
    spark.stop(now + 0.55);
  } catch (err) {
    console.warn('AudioContext not allowed or supported', err);
  }

  // Cheerful robotic voice greeting via SpeechSynthesis
  try {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      const utter = new SpeechSynthesisUtterance('Welcome to The Era of AI!');
      utter.pitch = 1.6;
      utter.rate = 1.25;
      utter.volume = 0.55;
      window.speechSynthesis.speak(utter);
    }
  } catch {
    // Ignore speech errors
  }
}

export default function LandingHeroPage() {
  const navigate = useNavigate();
  const [isEntering, setIsEntering] = useState(false);
  const [isSquishing, setIsSquishing] = useState(false);
  const [soundEnabled, setSoundEnabled] = useState(true);
  const [tiltStyle, setTiltStyle] = useState({});
  const cardRef = useRef(null);

  const handleMascotMouseMove = (e) => {
    if (!cardRef.current) return;
    const rect = cardRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left - rect.width / 2;
    const y = e.clientY - rect.top - rect.height / 2;
    const rotateX = (-y / (rect.height / 2)) * 12;
    const rotateY = (x / (rect.width / 2)) * 12;
    setTiltStyle({
      transform: `perspective(800px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`
    });
  };

  const handleMascotMouseLeave = () => {
    setTiltStyle({
      transform: 'perspective(800px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)'
    });
  };

  const handleMascotClick = () => {
    setIsSquishing(true);
    if (soundEnabled) playAeroSound();
    setTimeout(() => setIsSquishing(false), 500);
  };

  const handleEnterWorld = (e) => {
    e.preventDefault();
    if (isEntering) return;
    setIsEntering(true);
    setIsSquishing(true);
    if (soundEnabled) playAeroSound();

    // Smooth transition into the Mind Map after sound and animation
    setTimeout(() => {
      navigate('/mindmap');
    }, 700);
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

  return (
    <div className={`relative flex-1 w-full h-full overflow-y-auto bg-slate-950 text-slate-100 flex flex-col items-center justify-start select-none transition-all duration-700 ${
      isEntering ? 'opacity-0 scale-105 filter blur-sm pointer-events-none' : 'opacity-100 scale-100'
    }`}>
      {/* Background Ambient Electric/Cosmic Atmosphere */}
      <div className="fixed inset-0 pointer-events-none bg-[radial-gradient(ellipse_80%_80%_at_50%_-10%,rgba(99,102,241,0.2),rgba(56,189,248,0.15),rgba(2,6,23,0.98))]" />
      <div className="fixed inset-0 pointer-events-none bg-gradient-to-b from-slate-950/70 via-slate-950/90 to-slate-950" />

      {/* Entering Flash Overlay */}
      {isEntering && (
        <div className="fixed inset-0 z-50 pointer-events-none bg-gradient-to-tr from-cyan-400/30 via-indigo-500/40 to-purple-500/30 backdrop-blur-md animate-pulse" />
      )}

      {/* Main Container */}
      <div className="relative z-10 w-full max-w-4xl mx-auto px-4 sm:px-6 py-6 sm:py-10 md:py-12 flex flex-col items-center text-center space-y-6">
        
        {/* Top Badges & Audio Toggle */}
        <div className="flex items-center justify-between w-full max-w-md gap-2">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-indigo-500/10 border border-indigo-500/30 text-indigo-300 text-xs font-semibold shadow-lg shadow-indigo-500/10">
            <Bot className="w-3.5 h-3.5 text-cyan-400 animate-bounce" />
            <span>Meet Aero • Your AI Knowledge Companion</span>
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
        <div className="space-y-2 max-w-2xl">
          <h1 className="text-3xl sm:text-4xl md:text-5xl font-black tracking-tight text-white leading-tight">
            The Era of <span className="bg-gradient-to-r from-cyan-400 via-indigo-300 to-purple-400 bg-clip-text text-transparent">AI</span>
          </h1>
          <p className="text-xs sm:text-sm md:text-base text-slate-300 font-normal leading-relaxed">
            Aero the AI Bot is hovering by your side, ready to guide you through the multidimensional machine learning universe.
          </p>
        </div>

        {/* Squishy Plush Aero Mascot Centerpiece */}
        <div className="relative flex flex-col items-center justify-center my-2">
          
          {/* Floating Speech Bubble */}
          <div className="relative mb-3 animate-bounce-slow">
            <div className="px-4 py-2 rounded-2xl bg-gradient-to-r from-indigo-500/20 via-slate-900 to-cyan-500/20 border border-cyan-400/50 text-xs sm:text-sm font-bold text-cyan-200 shadow-xl shadow-cyan-500/10 flex items-center gap-2 backdrop-blur-md">
              <Sparkles className="w-4 h-4 text-cyan-300" />
              <span>Hi there! 🤖✨ Press the glowing button below to enter!</span>
            </div>
            {/* Bubble Tail */}
            <div className="w-3 h-3 bg-slate-900 border-r border-b border-cyan-400/50 transform rotate-45 mx-auto -mt-1.5" />
          </div>

          {/* Interactive Mascot Card with Electric Lightning Effects */}
          <div 
            ref={cardRef}
            onMouseMove={handleMascotMouseMove}
            onMouseLeave={handleMascotMouseLeave}
            onClick={handleMascotClick}
            style={tiltStyle}
            className={`relative group cursor-pointer transition-transform duration-200 select-none ${
              isSquishing ? 'scale-95' : 'hover:scale-105'
            }`}
            title="Click Aero for a friendly chime!"
          >
            {/* Background Halo Glow */}
            <div className="absolute inset-0 rounded-full bg-gradient-to-tr from-cyan-500/30 via-indigo-500/25 to-purple-500/30 filter blur-2xl scale-95 opacity-80 group-hover:opacity-100 transition-opacity" />

            {/* Electric Antenna Energy Spark (Top of head) */}
            <div className="absolute -top-6 inset-x-0 mx-auto w-24 h-24 z-20 pointer-events-none animate-electric flex items-center justify-center">
              <svg className="w-20 h-20 text-cyan-300 filter drop-shadow-[0_0_10px_rgba(56,189,248,0.9)]" viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="14" fill="none" stroke="currentColor" strokeWidth="2.5" strokeDasharray="6,4" />
                <path d="M42,50 L48,40 L52,48 L58,38" fill="none" stroke="#fef08a" strokeWidth="3" strokeLinecap="round" />
                <circle cx="50" cy="50" r="4" fill="#ffffff" />
              </svg>
            </div>

            {/* Extra Floating Sparkles & Fireflies */}
            <div className="absolute top-1/4 -right-4 z-20 pointer-events-none animate-ping opacity-75">
              <Sparkles className="w-4 h-4 text-cyan-300" />
            </div>
            <div className="absolute bottom-1/4 -left-4 z-20 pointer-events-none animate-pulse">
              <Zap className="w-4 h-4 text-purple-300 fill-purple-300" />
            </div>

            {/* Mascot Image Container with Rounded Soft Silhouette */}
            <div className="relative w-64 h-64 sm:w-72 sm:h-72 md:w-80 md:h-80 rounded-3xl overflow-hidden shadow-2xl shadow-indigo-500/25 border-2 border-cyan-400/40 ring-4 ring-indigo-500/20 bg-slate-900/90 animate-squish">
              <img 
                src={`${import.meta.env.BASE_URL}aero_mascot.jpg`} 
                alt="Aero the Squishy Plush AI Companion Bot"
                className="w-full h-full object-cover pointer-events-none transition-transform duration-300 group-hover:scale-105"
              />
              {/* Soft Vignette Overlay */}
              <div className="absolute inset-0 bg-gradient-to-t from-slate-950/80 via-transparent to-transparent pointer-events-none" />

              {/* Tap Indicator Tag */}
              <div className="absolute bottom-2 inset-x-0 text-center pointer-events-none">
                <span className="text-[10px] font-bold tracking-wider text-cyan-200/90 bg-slate-950/80 px-2.5 py-0.5 rounded-full border border-cyan-500/30">
                  🤖 Aero AI Bot • Tap for chime ⚡
                </span>
              </div>
            </div>
          </div>

          {/* Hand Pointing Down Indicator Arrow */}
          <div className="my-2 flex flex-col items-center justify-center animate-bounce text-cyan-400">
            <span className="text-[10px] font-bold tracking-widest uppercase text-cyan-300">Pointed Below</span>
            <div className="w-1.5 h-6 bg-gradient-to-b from-cyan-400 to-transparent rounded-full mt-0.5" />
          </div>

          {/* THE GIANT GLOWING ELECTRIC ENTER BUTTON */}
          <div className="relative w-full max-w-md px-4 pt-1">
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
