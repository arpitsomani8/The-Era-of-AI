import React, { useState, useRef, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { 
  Sparkles, 
  ArrowRight, 
  Network, 
  BookOpen, 
  FileText, 
  HelpCircle, 
  Layers,
  PlayCircle,
  Volume2,
  VolumeX,
  Bot,
  Palette,
  Info
} from 'lucide-react';
import allNodes from '../data/allNodes.json';
import topicsData from '../data/topics.json';
import conceptsData from '../data/concepts.json';
import interviewData from '../data/interviewQuestions.json';
import papersData from '../data/papers.json';
import AudioExplainerButton from '../components/AudioExplainerButton';

/**
 * Interactive Costume / Dress Wardrobe for Aero
 */
const AERO_DRESSES = [
  {
    id: 'aero',
    name: 'Cyber Explorer',
    bodyGrad: ['#6366f1', '#4338ca', '#312e81'],
    stroke: '#818cf8',
    coreColor: '#06b6d4',
    eyeColor: '#06b6d4',
    beaconColor: '#38bdf8',
    glowColor: 'rgba(99, 102, 241, 0.45)',
    chipGradient: 'from-indigo-500 to-cyan-400',
    type: 'antenna',
    tag: 'Quantum Blue'
  },
  {
    id: 'neon',
    name: 'Neon Sentinel',
    bodyGrad: ['#fbbf24', '#d97706', '#78350f'],
    stroke: '#fbbf24',
    coreColor: '#f59e0b',
    eyeColor: '#fbbf24',
    beaconColor: '#f59e0b',
    glowColor: 'rgba(245, 158, 11, 0.45)',
    chipGradient: 'from-amber-400 to-orange-500',
    type: 'halo',
    tag: 'Solar Mecha'
  },
  {
    id: 'catbot',
    name: 'Quantum Kitty',
    bodyGrad: ['#f472b6', '#c084fc', '#6b21a8'],
    stroke: '#f472b6',
    coreColor: '#ec4899',
    eyeColor: '#f472b6',
    beaconColor: '#fda4af',
    glowColor: 'rgba(236, 72, 153, 0.45)',
    chipGradient: 'from-pink-400 to-purple-500',
    type: 'cat',
    tag: 'Cyber Feline'
  },
  {
    id: 'matrix',
    name: 'Emerald Matrix',
    bodyGrad: ['#10b981', '#059669', '#064e3b'],
    stroke: '#34d399',
    coreColor: '#10b981',
    eyeColor: '#34d399',
    beaconColor: '#6ee7b7',
    glowColor: 'rgba(16, 185, 129, 0.45)',
    chipGradient: 'from-emerald-400 to-teal-500',
    type: 'antenna',
    tag: 'Neural Jade'
  },
  {
    id: 'phantom',
    name: 'Obsidian Stealth',
    bodyGrad: ['#475569', '#1e293b', '#0f172a'],
    stroke: '#f43f5e',
    coreColor: '#ef4444',
    eyeColor: '#fb7185',
    beaconColor: '#f43f5e',
    glowColor: 'rgba(244, 63, 94, 0.45)',
    chipGradient: 'from-slate-700 to-rose-500',
    type: 'antenna',
    tag: 'Titanium Red'
  }
];

/**
 * Web Audio Synthesizer for Aero's clean melodic chimes
 */
function playSynthSound(type = 'chime', soundEnabled = true) {
  if (!soundEnabled) return;
  try {
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    if (!AudioCtx) return;
    const ctx = new AudioCtx();
    const now = ctx.currentTime;

    const playTone = (freq, startTime, duration, gainVal = 0.18, wave = 'sine') => {
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
      playTone(523.25, now, 0.2, 0.15, 'sine');          // C5
      playTone(659.25, now + 0.08, 0.22, 0.18, 'sine');   // E5
      playTone(783.99, now + 0.16, 0.24, 0.2, 'triangle'); // G5
      playTone(1046.5, now + 0.24, 0.45, 0.22, 'sine');   // C6
    } else if (type === 'dress') {
      playTone(880, now, 0.12, 0.12, 'sine');
      playTone(1174.66, now + 0.06, 0.2, 0.15, 'triangle');
    } else {
      // Wave / click chime
      playTone(659.25, now, 0.18, 0.15, 'sine');
      playTone(880, now + 0.08, 0.25, 0.16, 'sine');
    }
  } catch (err) {
    console.debug('Audio not supported', err);
  }
}

export default function LandingHeroPage({ onOpenAbout }) {
  const navigate = useNavigate();
  const [isEntering, setIsEntering] = useState(false);
  const [soundEnabled, setSoundEnabled] = useState(true);
  const [isWaving, setIsWaving] = useState(true);
  const [selectedDress, setSelectedDress] = useState(AERO_DRESSES[0]);
  const [aeroOffset, setAeroOffset] = useState({ x: 0, y: 0 });
  const [tiltStyle, setTiltStyle] = useState({});
  const aeroContainerRef = useRef(null);
  const waveTimerRef = useRef(null);

  // Initially wave once on page load (1.8s) to welcome the user, then rest arm
  useEffect(() => {
    setIsWaving(true);
    waveTimerRef.current = setTimeout(() => {
      setIsWaving(false);
    }, 1800);

    return () => {
      if (waveTimerRef.current) clearTimeout(waveTimerRef.current);
    };
  }, []);

  // User-triggered wave on click
  const triggerWave = () => {
    if (waveTimerRef.current) clearTimeout(waveTimerRef.current);
    setIsWaving(true);
    playSynthSound('wave', soundEnabled);

    // Wave for 2.2 seconds, then return arm to relaxed posture
    waveTimerRef.current = setTimeout(() => {
      setIsWaving(false);
    }, 2200);
  };

  // Mouse move handler to make Big Aero movable and gently lean towards cursor
  const handleAeroMouseMove = (e) => {
    if (!aeroContainerRef.current) return;
    const rect = aeroContainerRef.current.getBoundingClientRect();
    const xRatio = (e.clientX - rect.left) / rect.width - 0.5;
    const yRatio = (e.clientY - rect.top) / rect.height - 0.5;

    setAeroOffset({
      x: Math.round(xRatio * 20),
      y: Math.round(yRatio * 15)
    });

    const rotateX = -yRatio * 12;
    const rotateY = xRatio * 12;
    setTiltStyle({
      transform: `perspective(900px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`
    });
  };

  const handleAeroMouseLeave = () => {
    setAeroOffset({ x: 0, y: 0 });
    setTiltStyle({
      transform: 'perspective(900px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)'
    });
  };

  const handleSelectDress = (dress) => {
    setSelectedDress(dress);
    playSynthSound('dress', soundEnabled);
    triggerWave();
  };

  const handleEnterWorld = (e) => {
    e.preventDefault();
    if (isEntering) return;
    setIsEntering(true);
    playSynthSound('enter', soundEnabled);

    setTimeout(() => {
      navigate('/mindmap');
    }, 550);
  };

  const portalCards = [
    {
      to: '/mindmap',
      title: 'Interactive Mind Map',
      subtitle: `${allNodes.length} interconnected domain nodes`,
      icon: Network,
      color: 'from-indigo-500/10 to-indigo-600/5 border-indigo-500/20 text-indigo-400'
    },
    {
      to: '/syllabus',
      title: 'Line-Wise Syllabus',
      subtitle: `${topicsData.length} structured curriculum modules`,
      icon: BookOpen,
      color: 'from-blue-500/10 to-blue-600/5 border-blue-500/20 text-blue-400'
    },
    {
      to: '/concepts',
      title: 'Core Concepts & Math',
      subtitle: `${conceptsData.length} in-depth technical breakdowns`,
      icon: Layers,
      color: 'from-rose-500/10 to-rose-600/5 border-rose-500/20 text-rose-400'
    },
    {
      to: '/interview',
      title: 'Interview Vault',
      subtitle: `${interviewData.length.toLocaleString()}+ math, coding & design questions`,
      icon: HelpCircle,
      color: 'from-purple-500/10 to-purple-600/5 border-purple-500/20 text-purple-400'
    },
    {
      to: '/papers',
      title: 'Research Publications',
      subtitle: `${papersData.length} milestone AI publications`,
      icon: FileText,
      color: 'from-amber-500/10 to-amber-600/5 border-amber-500/20 text-amber-400'
    },
    {
      to: '/playgrounds',
      title: 'ML Playgrounds',
      subtitle: 'Interactive attention & optimization labs',
      icon: PlayCircle,
      color: 'from-cyan-500/10 to-cyan-600/5 border-cyan-500/20 text-cyan-400'
    }
  ];

  return (
    <div className={`relative flex-1 w-full h-full overflow-y-auto bg-slate-950 text-slate-100 flex flex-col items-center justify-start select-none transition-all duration-500 ${
      isEntering ? 'opacity-0 scale-105 filter blur-sm pointer-events-none' : 'opacity-100 scale-100'
    }`}>
      {/* Background Ambient Glow */}
      <div className="fixed inset-0 pointer-events-none bg-[radial-gradient(ellipse_75%_65%_at_50%_-5%,rgba(99,102,241,0.18),rgba(15,23,42,0.98))]" />

      {/* Main Content Area */}
      <div className="relative z-10 w-full max-w-4xl mx-auto px-4 sm:px-6 py-6 sm:py-8 flex flex-col items-center text-center space-y-6">
        
        {/* Top Minimal Companion Badge & Audio Toggle */}
        <div className="flex items-center justify-between w-full max-w-md gap-3">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-900/80 border border-slate-800 text-slate-300 text-xs font-medium shadow-sm">
            <Bot className="w-3.5 h-3.5 text-indigo-400" />
            <span>Aero • Your AI Companion</span>
          </div>

          <div className="flex items-center gap-2">
            {onOpenAbout && (
              <button
                onClick={onOpenAbout}
                className="p-1 px-2.5 rounded-full bg-slate-900/80 border border-slate-800 hover:bg-slate-800 text-slate-300 hover:text-white text-xs font-medium flex items-center gap-1.5 transition shadow-sm"
                title="About The Era of AI (Project Overview, Stats & Author)"
              >
                <Info className="w-3.5 h-3.5 text-indigo-400" />
                <span className="text-[10px]">About</span>
              </button>
            )}

            <AudioExplainerButton
              variant="compact"
              label="Intro Audio"
              title="Welcome to The Era of AI"
              text="Welcome to The Era of AI. An open-source interactive research platform and comprehensive curriculum spanning artificial intelligence, deep learning, transformers, large language models, mathematical foundations, and enterprise case studies. Explore the interactive mind map, line-wise syllabus, interview question vault, landmark papers, and hands-on playgrounds."
            />

            <button
              onClick={() => setSoundEnabled(!soundEnabled)}
              className="p-1 px-2.5 rounded-full bg-slate-900/80 border border-slate-800 hover:bg-slate-800 text-slate-400 hover:text-slate-200 text-xs font-medium flex items-center gap-1.5 transition"
              title={soundEnabled ? 'Mute Chimes' : 'Enable Chimes'}
            >
              {soundEnabled ? <Volume2 className="w-3.5 h-3.5 text-cyan-400" /> : <VolumeX className="w-3.5 h-3.5 text-slate-500" />}
              <span className="text-[10px]">{soundEnabled ? 'Audio ON' : 'Muted'}</span>
            </button>
          </div>
        </div>

        {/* Clean, Refined Headline */}
        <div className="space-y-1.5 max-w-xl">
          <h1 className="text-3xl sm:text-4xl md:text-5xl font-black tracking-tight text-white leading-tight">
            The Era of <span className="bg-gradient-to-r from-cyan-400 via-indigo-300 to-purple-400 bg-clip-text text-transparent">AI</span>
          </h1>
          <p className="text-xs sm:text-sm text-slate-400 font-normal leading-relaxed">
            Welcome! Click Aero to wave, switch his high-tech outfits, or step inside the knowledge universe.
          </p>
        </div>

        {/* BIG AERO IN CENTER SCREEN (CLEAN STANDALONE VECTOR SVG) */}
        <div 
          ref={aeroContainerRef}
          onMouseMove={handleAeroMouseMove}
          onMouseLeave={handleAeroMouseLeave}
          onClick={triggerWave}
          style={tiltStyle}
          className="relative group cursor-pointer my-2 flex flex-col items-center justify-center transition-transform duration-150"
          title="Click Aero to wave!"
        >
          {/* Ambient Backlight Halo matching current dress */}
          <div 
            className="absolute inset-0 rounded-full filter blur-3xl opacity-60 group-hover:opacity-85 transition-all duration-500 pointer-events-none scale-110"
            style={{ backgroundColor: selectedDress.glowColor }}
          />

          {/* Large Aero SVG Container */}
          <div className="relative w-56 h-60 sm:w-64 sm:h-68 md:w-72 md:h-76 flex items-center justify-center">
            <svg viewBox="0 0 140 160" className="w-full h-full overflow-visible drop-shadow-[0_12px_24px_rgba(0,0,0,0.5)]">
              <defs>
                {/* Dynamic Robot Body Gradient based on selected dress */}
                <linearGradient id="aeroBodyGrad" x1="0" y1="0" x2="1" y2="1">
                  <stop offset="0%" stopColor={selectedDress.bodyGrad[0]} />
                  <stop offset="50%" stopColor={selectedDress.bodyGrad[1]} />
                  <stop offset="100%" stopColor={selectedDress.bodyGrad[2]} />
                </linearGradient>
              </defs>

              {/* Movable Aero Group with Cursor Offset */}
              <g transform={`translate(${aeroOffset.x}, ${aeroOffset.y})`} className="transition-transform duration-100 ease-out">
                
                {/* Thruster Shadow */}
                <ellipse cx="70" cy="144" rx="32" ry="7" fill="#000000" opacity="0.35" className="animate-pulse" />
                
                {/* Hovering Jet Motion Group */}
                <g className="animate-robot-hover">
                  
                  {/* Thruster Flame & Glow */}
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
                    fill="url(#aeroBodyGrad)"
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

                  {/* CatBot Ears (if dress type is cat) */}
                  {selectedDress.type === 'cat' && (
                    <g>
                      <polygon points="46,16 38,-4 58,10" fill={selectedDress.stroke} stroke="#fda4af" strokeWidth="1.5" />
                      <polygon points="76,10 96,-4 88,16" fill={selectedDress.stroke} stroke="#fda4af" strokeWidth="1.5" />
                      <polygon points="45,13 40,2 52,10" fill="#fdf2f8" />
                      <polygon points="82,10 94,2 89,13" fill="#fdf2f8" />
                    </g>
                  )}

                  {/* Neon Halo (if dress type is halo) */}
                  {selectedDress.type === 'halo' && (
                    <ellipse cx="70" cy="2" rx="26" ry="6" fill="none" stroke={selectedDress.stroke} strokeWidth="2.5" className="animate-pulse" opacity="0.95" />
                  )}

                  {/* Antenna (if dress type is antenna) */}
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

                  {/* Right Arm: Natural resting arm when idle, rises up & waves when isWaving is true */}
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
              </g>
            </svg>
          </div>

          {/* Interactive Wave Button */}
          <button
            onClick={(e) => {
              e.stopPropagation();
              triggerWave();
            }}
            className={`mt-2 px-3.5 py-1.5 rounded-full border text-xs font-semibold flex items-center gap-1.5 transition-all shadow-sm cursor-pointer ${
              isWaving 
                ? 'bg-indigo-600/30 border-cyan-400 text-cyan-200 shadow-[0_0_15px_rgba(6,182,212,0.3)] scale-105' 
                : 'bg-slate-900/90 hover:bg-slate-800 border-slate-700/80 text-slate-300 hover:text-white'
            }`}
            title="Click to make Aero wave"
          >
            <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
            <span>{isWaving ? 'Aero is waving! 👋' : 'Wave at Aero 👋'}</span>
          </button>
        </div>

        {/* INTERACTIVE DRESS / OUTFIT CHANGER */}
        <div className="flex flex-col items-center gap-2 pt-1">
          <div className="flex items-center gap-1.5 text-xs text-slate-400 font-medium">
            <Palette className="w-3.5 h-3.5 text-indigo-400" />
            <span>Choose Aero's Outfit:</span>
          </div>

          <div className="inline-flex items-center gap-2 p-1.5 rounded-2xl bg-slate-900/90 border border-slate-800/90 shadow-inner flex-wrap justify-center">
            {AERO_DRESSES.map((dress) => {
              const isSelected = selectedDress.id === dress.id;
              return (
                <button
                  key={dress.id}
                  onClick={() => handleSelectDress(dress)}
                  className={`px-3 py-1.5 rounded-xl text-xs font-semibold flex items-center gap-2 transition-all ${
                    isSelected 
                      ? 'bg-slate-800 text-white shadow-md border border-slate-700 scale-105' 
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50 border border-transparent'
                  }`}
                  title={`Equip ${dress.name} (${dress.tag})`}
                >
                  <span 
                    className={`w-3 h-3 rounded-full bg-gradient-to-r ${dress.chipGradient} shadow-sm shrink-0`} 
                  />
                  <span>{dress.name}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* SLEEK, ELEGANT, NON-FLASHY ENTER BUTTON */}
        <div className="pt-2 w-full max-w-sm">
          <button
            onClick={handleEnterWorld}
            id="hero-center-enter-btn"
            className="w-full group relative inline-flex items-center justify-center gap-3 px-8 py-3.5 sm:py-4 rounded-xl bg-slate-900/90 hover:bg-slate-800/90 border border-slate-700/80 hover:border-indigo-500/60 text-white font-semibold text-base sm:text-lg shadow-lg hover:shadow-indigo-500/20 hover:scale-[1.02] active:scale-[0.98] transition-all duration-200 cursor-pointer"
          >
            <Bot className="w-5 h-5 text-indigo-400 group-hover:text-cyan-300 transition-colors shrink-0" />
            <span className="tracking-wide text-white">
              Enter the World of AI
            </span>
            <ArrowRight className="w-4 h-4 text-slate-400 group-hover:text-white group-hover:translate-x-1 transition-all shrink-0" />
          </button>
          <p className="text-[11px] text-slate-400 mt-2 text-center font-normal">
            Step directly into the {allNodes.length}-node Interactive Knowledge Graph
          </p>
        </div>

        {/* Minimal Direct Jump Links */}
        <div className="w-full max-w-3xl pt-3">
          <div className="text-[11px] text-slate-500 font-semibold uppercase tracking-wider mb-2.5">
            Or jump directly into a hub:
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
            {portalCards.map((portal, idx) => {
              const Icon = portal.icon;
              return (
                <Link
                  key={idx}
                  to={portal.to}
                  className={`p-2.5 rounded-xl bg-slate-900/50 hover:bg-slate-900 border transition-all text-left flex items-center justify-between group hover:border-indigo-500/30 hover:scale-[1.01] ${portal.color}`}
                >
                  <div className="min-w-0 flex items-center gap-2">
                    <div className="w-6 h-6 rounded-lg bg-slate-800/80 flex items-center justify-center shrink-0">
                      <Icon className="w-3 h-3" />
                    </div>
                    <div className="min-w-0">
                      <h4 className="text-xs font-semibold text-white group-hover:text-cyan-300 truncate">
                        {portal.title}
                      </h4>
                      <p className="text-[10px] text-slate-400 truncate">
                        {portal.subtitle}
                      </p>
                    </div>
                  </div>
                  <ArrowRight className="w-3 h-3 text-slate-600 group-hover:text-cyan-300 shrink-0 ml-1" />
                </Link>
              );
            })}
          </div>
        </div>

        {/* Key Curriculum Metrics Bar */}
        <div className="w-full max-w-3xl pt-4 border-t border-slate-800/60 flex items-center justify-around flex-wrap gap-4 text-center">
          <div>
            <div className="text-lg sm:text-xl font-bold text-cyan-400 font-mono">{allNodes.length}</div>
            <div className="text-[10px] text-slate-500 uppercase tracking-wider font-medium">Graph Nodes</div>
          </div>
          <div className="w-px h-5 bg-slate-800 hidden sm:block" />
          <div>
            <div className="text-lg sm:text-xl font-bold text-cyan-400 font-mono">{topicsData.length}</div>
            <div className="text-[10px] text-slate-500 uppercase tracking-wider font-medium">Modules</div>
          </div>
          <div className="w-px h-5 bg-slate-800 hidden sm:block" />
          <div>
            <div className="text-lg sm:text-xl font-bold text-cyan-400 font-mono">{conceptsData.length}</div>
            <div className="text-[10px] text-slate-500 uppercase tracking-wider font-medium">Core Concepts</div>
          </div>
          <div className="w-px h-5 bg-slate-800 hidden sm:block" />
          <div>
            <div className="text-lg sm:text-xl font-bold text-cyan-400 font-mono">{interviewData.length.toLocaleString()}+</div>
            <div className="text-[10px] text-slate-500 uppercase tracking-wider font-medium">Interview Q&amp;A</div>
          </div>
          <div className="w-px h-5 bg-slate-800 hidden sm:block" />
          <div>
            <div className="text-lg sm:text-xl font-bold text-cyan-400 font-mono">{papersData.length}</div>
            <div className="text-[10px] text-slate-500 uppercase tracking-wider font-medium">Landmark Papers</div>
          </div>
        </div>

        {/* Project About & Published by Footer */}
        {onOpenAbout && (
          <div className="pt-2 pb-4 text-center">
            <button
              onClick={onOpenAbout}
              className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-slate-900/60 hover:bg-slate-800 border border-slate-800 hover:border-indigo-500/40 text-slate-400 hover:text-slate-200 text-xs transition shadow-sm group"
              title="View full project architecture, features, and author details"
            >
              <Info className="w-3.5 h-3.5 text-indigo-400 group-hover:scale-110 transition-transform" />
              <span>About The Era of AI &bull; Published by <strong className="text-slate-200">Arpit Somani</strong></span>
            </button>
          </div>
        )}

      </div>
    </div>
  );
}
