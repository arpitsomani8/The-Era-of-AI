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
  VolumeX
} from 'lucide-react';

/**
 * Web Audio Synthesizer for cheerful, cute "Pika-Pika!" chirp effect
 */
function playPikaSound() {
  try {
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    if (!AudioCtx) return;
    const ctx = new AudioCtx();
    const now = ctx.currentTime;

    // Helper to generate a cute chirp syllable
    const createChirp = (startFreq, endFreq, startTime, duration, peakGain = 0.28, type = 'triangle') => {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = type;
      osc.frequency.setValueAtTime(startFreq, startTime);
      osc.frequency.exponentialRampToValueAtTime(endFreq, startTime + duration);

      gain.gain.setValueAtTime(0.001, startTime);
      gain.gain.linearRampToValueAtTime(peakGain, startTime + 0.03);
      gain.gain.exponentialRampToValueAtTime(0.001, startTime + duration);

      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start(startTime);
      osc.stop(startTime + duration);
    };

    // Syllable 1: "Pi-" (high frequency quick upward chime)
    createChirp(620, 950, now, 0.12, 0.3, 'triangle');

    // Syllable 2: "-ka!" (playful bouncy drop)
    createChirp(980, 680, now + 0.13, 0.16, 0.32, 'sine');

    // Syllable 3: "Pi-" (second iteration slightly higher & brighter)
    createChirp(680, 1100, now + 0.32, 0.13, 0.3, 'triangle');

    // Syllable 4: "-kaaa!" (gleeful cheerful resolution with warm harmonics)
    createChirp(1150, 780, now + 0.46, 0.28, 0.35, 'sine');

    // Electric sparkle shimmer on tail
    const spark = ctx.createOscillator();
    const sparkGain = ctx.createGain();
    spark.type = 'sawtooth';
    spark.frequency.setValueAtTime(1800, now + 0.08);
    spark.frequency.linearRampToValueAtTime(2600, now + 0.55);
    sparkGain.gain.setValueAtTime(0.001, now + 0.08);
    sparkGain.gain.linearRampToValueAtTime(0.06, now + 0.25);
    sparkGain.gain.exponentialRampToValueAtTime(0.001, now + 0.65);
    spark.connect(sparkGain);
    sparkGain.connect(ctx.destination);
    spark.start(now + 0.08);
    spark.stop(now + 0.65);
  } catch (err) {
    console.warn('AudioContext not allowed or supported', err);
  }

  // Optional cute SpeechSynthesis backup if available
  try {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      const utter = new SpeechSynthesisUtterance('Pika pika!');
      utter.pitch = 1.9;
      utter.rate = 1.4;
      utter.volume = 0.5;
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
    if (soundEnabled) playPikaSound();
    setTimeout(() => setIsSquishing(false), 500);
  };

  const handleEnterWorld = (e) => {
    e.preventDefault();
    if (isEntering) return;
    setIsEntering(true);
    setIsSquishing(true);
    if (soundEnabled) playPikaSound();

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
      {/* Background Ambient Electric Atmosphere */}
      <div className="fixed inset-0 pointer-events-none bg-[radial-gradient(ellipse_80%_80%_at_50%_-10%,rgba(250,204,21,0.12),rgba(99,102,241,0.15),rgba(2,6,23,0.98))]" />
      <div className="fixed inset-0 pointer-events-none bg-gradient-to-b from-slate-950/70 via-slate-950/90 to-slate-950" />

      {/* Entering Flash Overlay */}
      {isEntering && (
        <div className="fixed inset-0 z-50 pointer-events-none bg-gradient-to-tr from-amber-400/30 via-indigo-500/40 to-cyan-300/30 backdrop-blur-md animate-pulse" />
      )}

      {/* Main Container */}
      <div className="relative z-10 w-full max-w-4xl mx-auto px-4 sm:px-6 py-6 sm:py-10 md:py-12 flex flex-col items-center text-center space-y-6">
        
        {/* Top Badges & Sound Toggle */}
        <div className="flex items-center justify-between w-full max-w-md gap-2">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs font-semibold shadow-lg shadow-amber-500/10">
            <Zap className="w-3.5 h-3.5 text-amber-400 fill-amber-400 animate-bounce" />
            <span>Welcome to The Era of AI</span>
          </div>

          <button
            onClick={() => setSoundEnabled(!soundEnabled)}
            className="p-1.5 px-2.5 rounded-full bg-slate-900 border border-slate-700/80 hover:bg-slate-800 text-slate-400 hover:text-amber-300 text-xs font-medium flex items-center gap-1.5 transition"
            title={soundEnabled ? 'Mute Pika Sound' : 'Enable Pika Sound'}
          >
            {soundEnabled ? <Volume2 className="w-3.5 h-3.5 text-amber-400" /> : <VolumeX className="w-3.5 h-3.5 text-slate-500" />}
            <span className="text-[10px]">{soundEnabled ? 'Pika FX ON' : 'Muted'}</span>
          </button>
        </div>

        {/* Hero Headline */}
        <div className="space-y-2 max-w-2xl">
          <h1 className="text-3xl sm:text-4xl md:text-5xl font-black tracking-tight text-white leading-tight">
            The Era of <span className="bg-gradient-to-r from-amber-400 via-yellow-300 to-indigo-300 bg-clip-text text-transparent">AI</span>
          </h1>
          <p className="text-xs sm:text-sm md:text-base text-slate-300 font-normal leading-relaxed">
            Meet your squishy companion pointing the way into the machine learning universe.
          </p>
        </div>

        {/* Squishy Plush Pikachu Mascot Centerpiece */}
        <div className="relative flex flex-col items-center justify-center my-2">
          
          {/* Floating Speech Bubble */}
          <div className="relative mb-3 animate-bounce-slow">
            <div className="px-4 py-2 rounded-2xl bg-gradient-to-r from-amber-500/20 via-slate-900 to-indigo-500/20 border border-amber-400/50 text-xs sm:text-sm font-bold text-amber-200 shadow-xl shadow-amber-500/10 flex items-center gap-2 backdrop-blur-md">
              <Zap className="w-4 h-4 text-amber-400 fill-amber-400" />
              <span>Pika-pika! ⚡ Click the button below to enter!</span>
            </div>
            {/* Bubble Tail */}
            <div className="w-3 h-3 bg-slate-900 border-r border-b border-amber-400/50 transform rotate-45 mx-auto -mt-1.5" />
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
            title="Click me for a Pika squeak!"
          >
            {/* Background Halo Glow */}
            <div className="absolute inset-0 rounded-full bg-gradient-to-tr from-amber-500/30 via-yellow-400/20 to-indigo-500/30 filter blur-2xl scale-95 opacity-80 group-hover:opacity-100 transition-opacity" />

            {/* Electric Tail Spark Arcs (Top-Left behind the tail) */}
            <div className="absolute -top-4 -left-6 z-20 pointer-events-none animate-electric">
              <svg className="w-20 h-20 text-amber-300 filter drop-shadow-[0_0_8px_rgba(250,204,21,0.9)]" viewBox="0 0 100 100">
                <path 
                  d="M10,50 Q30,20 50,45 T85,15" 
                  fill="none" 
                  stroke="currentColor" 
                  strokeWidth="3.5" 
                  strokeLinecap="round"
                />
                <path 
                  d="M25,75 Q45,45 60,70 T95,40" 
                  fill="none" 
                  stroke="#38bdf8" 
                  strokeWidth="2.5" 
                  strokeLinecap="round" 
                  opacity="0.9"
                />
                <polygon points="50,15 40,35 60,35 48,55 70,25 55,25" fill="#fef08a" />
              </svg>
            </div>

            {/* Extra Floating Sparks */}
            <div className="absolute -top-2 right-4 z-20 pointer-events-none animate-ping opacity-75">
              <Zap className="w-4 h-4 text-amber-300 fill-amber-300" />
            </div>
            <div className="absolute top-1/2 -left-4 z-20 pointer-events-none animate-pulse">
              <Sparkles className="w-5 h-5 text-cyan-300" />
            </div>

            {/* Mascot Image Container with Rounded Soft Silhouette */}
            <div className="relative w-64 h-64 sm:w-72 sm:h-72 md:w-80 md:h-80 rounded-3xl overflow-hidden shadow-2xl shadow-amber-500/20 border-2 border-amber-400/40 ring-4 ring-amber-400/20 bg-slate-900/90 animate-squish">
              <img 
                src={`${import.meta.env.BASE_URL}pika_mascot.jpg`} 
                alt="Squishy Plush Electric Mascot"
                className="w-full h-full object-cover pointer-events-none transition-transform duration-300 group-hover:scale-105"
              />
              {/* Soft Vignette Overlay */}
              <div className="absolute inset-0 bg-gradient-to-t from-slate-950/80 via-transparent to-transparent pointer-events-none" />

              {/* Tap Indicator Tag */}
              <div className="absolute bottom-2 inset-x-0 text-center pointer-events-none">
                <span className="text-[10px] font-bold tracking-wider text-amber-200/90 bg-slate-950/80 px-2.5 py-0.5 rounded-full border border-amber-500/30">
                  ⚡ Squishy Plush Mascot • Tap for sound ⚡
                </span>
              </div>
            </div>
          </div>

          {/* Hand Pointing Down Indicator Arrow */}
          <div className="my-2 flex flex-col items-center justify-center animate-bounce text-amber-400">
            <span className="text-[10px] font-bold tracking-widest uppercase text-amber-300">Pointed Below</span>
            <div className="w-1.5 h-6 bg-gradient-to-b from-amber-400 to-transparent rounded-full mt-0.5" />
          </div>

          {/* THE GIANT GLOWING ELECTRIC ENTER BUTTON */}
          <div className="relative w-full max-w-md px-4 pt-1">
            <button
              onClick={handleEnterWorld}
              id="hero-center-enter-btn"
              className="w-full group relative inline-flex items-center justify-center gap-3.5 px-8 sm:px-10 py-4 sm:py-5 rounded-2xl bg-gradient-to-r from-amber-500 via-yellow-400 to-amber-500 hover:from-amber-400 hover:via-yellow-300 hover:to-yellow-400 text-slate-950 font-black text-lg sm:text-xl md:text-2xl shadow-[0_0_40px_rgba(250,204,21,0.55)] hover:shadow-[0_0_60px_rgba(250,204,21,0.9)] border-2 border-yellow-200 hover:scale-105 active:scale-95 transition-all duration-200 cursor-pointer animate-electric-pulse"
            >
              <Zap className="w-6 h-6 text-slate-950 fill-slate-950 animate-bounce shrink-0" />
              <span className="tracking-wide uppercase drop-shadow-sm font-extrabold">
                Enter the World of AI
              </span>
              <ArrowRight className="w-6 h-6 group-hover:translate-x-1.5 transition-transform shrink-0 text-slate-950" />
            </button>
            <p className="text-[11px] text-amber-300/80 mt-2 text-center font-medium">
              Plays cute &quot;Pika-Pika!&quot; chirp &amp; transitions into 2D Knowledge Graph
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
                  className={`p-3 rounded-xl bg-slate-900/60 hover:bg-slate-900 border transition-all text-left flex items-center justify-between group shadow-sm hover:border-amber-500/40 hover:scale-[1.02] ${portal.color}`}
                >
                  <div className="min-w-0 flex items-center gap-2.5">
                    <div className="w-7 h-7 rounded-lg bg-slate-800/80 flex items-center justify-center shrink-0">
                      <Icon className="w-3.5 h-3.5" />
                    </div>
                    <div className="min-w-0">
                      <h4 className="text-xs font-bold text-white group-hover:text-amber-300 truncate">
                        {portal.title}
                      </h4>
                      <p className="text-[10px] text-slate-400 truncate">
                        {portal.badge}
                      </p>
                    </div>
                  </div>
                  <ArrowRight className="w-3.5 h-3.5 text-slate-500 group-hover:text-amber-300 shrink-0 ml-1" />
                </Link>
              );
            })}
          </div>
        </div>

        {/* Key Curriculum Metrics Bar */}
        <div className="w-full max-w-3xl pt-4 border-t border-slate-800/80 flex items-center justify-around flex-wrap gap-4 text-center">
          <div>
            <div className="text-lg sm:text-xl font-black text-amber-300 font-mono">41</div>
            <div className="text-[10px] text-slate-400 uppercase tracking-wider font-semibold">Graph Nodes</div>
          </div>
          <div className="w-px h-6 bg-slate-800 hidden sm:block" />
          <div>
            <div className="text-lg sm:text-xl font-black text-amber-300 font-mono">34</div>
            <div className="text-[10px] text-slate-400 uppercase tracking-wider font-semibold">Syllabus Modules</div>
          </div>
          <div className="w-px h-6 bg-slate-800 hidden sm:block" />
          <div>
            <div className="text-lg sm:text-xl font-black text-amber-300 font-mono">170+</div>
            <div className="text-[10px] text-slate-400 uppercase tracking-wider font-semibold">Core Concepts</div>
          </div>
          <div className="w-px h-6 bg-slate-800 hidden sm:block" />
          <div>
            <div className="text-lg sm:text-xl font-black text-amber-300 font-mono">150+</div>
            <div className="text-[10px] text-slate-400 uppercase tracking-wider font-semibold">Interview Q&amp;A</div>
          </div>
          <div className="w-px h-6 bg-slate-800 hidden sm:block" />
          <div>
            <div className="text-lg sm:text-xl font-black text-amber-300 font-mono">22+</div>
            <div className="text-[10px] text-slate-400 uppercase tracking-wider font-semibold">Landmark Papers</div>
          </div>
        </div>

      </div>
    </div>
  );
}
