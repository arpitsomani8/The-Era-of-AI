import React, { useState, useEffect, useRef, useCallback } from 'react';
import { 
  Sparkles, 
  Volume2, 
  VolumeX, 
  X, 
  Palette, 
  Compass, 
  Anchor,
  MessageSquareQuote,
  ChevronLeft,
  ChevronRight,
  Shuffle
} from 'lucide-react';
import { useLocation } from 'react-router-dom';
import aeroThoughts from '../data/aeroThoughts.json';
import AudioExplainerButton from './AudioExplainerButton';

const COMPANION_DRESSES = [
  {
    id: 'aero',
    name: 'Cyber Explorer',
    bodyGrad: ['#6366f1', '#4338ca', '#312e81'],
    stroke: '#818cf8',
    coreColor: '#06b6d4',
    eyeColor: '#06b6d4',
    beaconColor: '#38bdf8',
    glowColor: 'rgba(99, 102, 241, 0.45)',
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
    glowColor: 'rgba(245, 158, 11, 0.45)',
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
    glowColor: 'rgba(236, 72, 153, 0.45)',
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
    glowColor: 'rgba(16, 185, 129, 0.45)',
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
    glowColor: 'rgba(244, 63, 94, 0.45)',
    type: 'antenna'
  }
];

// 100 Simple, logical, intuitive thoughts loaded from aeroThoughts.json
const COMPANION_THOUGHTS = aeroThoughts;

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

  // Responsive screen sizing: large desktop Aero, small mobile Aero
  const [isMobile, setIsMobile] = useState(() => {
    return typeof window !== 'undefined' ? window.innerWidth < 640 : false;
  });

  const aeroWidth = isMobile ? 62 : 115;
  const aeroHeight = isMobile ? 70 : 130;

  // Docked bottom-right coordinates with plenty of safe gutter from the screen edge
  const getDockPosition = useCallback(() => {
    const w = typeof window !== 'undefined' ? window.innerWidth : 1200;
    const h = typeof window !== 'undefined' ? window.innerHeight : 800;
    return {
      x: Math.max(16, w - (isMobile ? 96 : 175)),
      y: Math.max(68, h - (isMobile ? 105 : 185))
    };
  }, [isMobile]);

  // Anchor state: when anchored, Aero stays permanently at bottom-right and NEVER flies
  const [isAnchored, setIsAnchored] = useState(() => {
    try {
      return localStorage.getItem('aero_anchored') === 'true';
    } catch {
      return false;
    }
  });

  const [isRoaming, setIsRoaming] = useState(false); // True ONLY when flying full screen
  const [isHovered, setIsHovered] = useState(false);
  const [isWaving, setIsWaving] = useState(false);
  const [isClosed, setIsClosed] = useState(false);
  const [soundEnabled, setSoundEnabled] = useState(true);
  const [dressIndex, setDressIndex] = useState(0);
  const [thoughtIndex, setThoughtIndex] = useState(() => Math.floor(Math.random() * COMPANION_THOUGHTS.length));
  const [thoughtBoxOpen, setThoughtBoxOpen] = useState(false);

  const [sayingHi, setSayingHi] = useState(false);
  const selectedDress = COMPANION_DRESSES[dressIndex];
  const containerRef = useRef(null);
  const waveTimerRef = useRef(null);
  const hiTimerRef = useRef(null);
  const idleTimerRef = useRef(null);
  const animFrameRef = useRef(null);

  // Position and state tracking refs for 120 FPS buttery-smooth animation
  const posRef = useRef(getDockPosition());
  const targetRef = useRef(getDockPosition());
  const isRoamingRef = useRef(false);
  const isHoveredRef = useRef(false);
  const isAnchoredRef = useRef(isAnchored);

  isRoamingRef.current = isRoaming;
  isHoveredRef.current = isHovered;
  isAnchoredRef.current = isAnchored;

  // Pick a fresh random waypoint across the full screen
  const pickNewWaypoint = useCallback(() => {
    const minX = 24;
    const maxX = Math.max(minX + 80, window.innerWidth - aeroWidth - 60);
    const minY = 76; // Below top navbar
    const maxY = Math.max(minY + 80, window.innerHeight - aeroHeight - 50);

    const nextX = Math.round(minX + Math.random() * (maxX - minX));
    const nextY = Math.round(minY + Math.random() * (maxY - minY));

    targetRef.current = { x: nextX, y: nextY };
  }, [aeroWidth, aeroHeight]);

  // Window resize handler
  useEffect(() => {
    const handleResize = () => {
      const mobile = window.innerWidth < 640;
      setIsMobile(mobile);
      if (!isRoamingRef.current) {
        const dock = {
          x: Math.max(16, window.innerWidth - (mobile ? 96 : 175)),
          y: Math.max(68, window.innerHeight - (mobile ? 105 : 185))
        };
        posRef.current = dock;
        targetRef.current = dock;
        if (containerRef.current) {
          containerRef.current.style.transform = `translate3d(${dock.x}px, ${dock.y}px, 0px) rotate(0deg)`;
        }
      }
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  /**
   * 15-SECOND IDLE FLYING LOGIC:
   * 1. Flies ONLY when the screen has been idle with ZERO user interaction for 15 SECONDS.
   * 2. Any user interaction (mousemove, click, scroll, keypress) IMMEDIATELY stops flying
   *    and returns Aero back to bottom-right dock!
   * 3. IF ANCHORED (isAnchored === true):
   *    Aero NEVER flies AT ALL, even if the screen remains idle indefinitely!
   */
  useEffect(() => {
    const handleUserActivity = () => {
      // 1. If Aero is currently roaming, immediately stop flight and return to dock!
      if (isRoamingRef.current) {
        setIsRoaming(false);
        isRoamingRef.current = false;
        targetRef.current = getDockPosition();
      }

      // 2. Clear any pending idle countdown
      if (idleTimerRef.current) {
        clearTimeout(idleTimerRef.current);
        idleTimerRef.current = null;
      }

      // 3. If Aero is ANCHORED, HE NEVER FLIES AT ALL!
      if (isAnchoredRef.current) {
        return;
      }

      // 4. Otherwise, start a fresh 15-second idle timer
      idleTimerRef.current = setTimeout(() => {
        // Double check anchor condition before takeoff
        if (!isAnchoredRef.current) {
          setThoughtBoxOpen(false); // Close thought box before taking flight
          setIsRoaming(true);
          isRoamingRef.current = true;
          pickNewWaypoint();
          playAeroSynth('whoosh', soundEnabled);
        }
      }, 15000); // STRICTLY 15 SECONDS
    };

    const activityEvents = ['mousemove', 'mousedown', 'keydown', 'wheel', 'scroll', 'touchstart'];
    activityEvents.forEach((ev) => window.addEventListener(ev, handleUserActivity, { passive: true }));

    // Start idle countdown on mount (unless anchored)
    if (!isAnchoredRef.current) {
      handleUserActivity();
    }

    return () => {
      if (idleTimerRef.current) clearTimeout(idleTimerRef.current);
      activityEvents.forEach((ev) => window.removeEventListener(ev, handleUserActivity));
    };
  }, [pickNewWaypoint, getDockPosition, soundEnabled, isAnchored]);

  // High-performance 120 FPS Flight Animation Loop
  useEffect(() => {
    let lastTime = performance.now();

    const loop = (time) => {
      const dt = Math.min((time - lastTime) / 1000, 0.1);
      lastTime = time;

      if (containerRef.current) {
        if (isRoamingRef.current && !isHoveredRef.current && !isAnchoredRef.current) {
          // Free-Flight Motion Physics: Smoothly glide towards full-screen target waypoint
          const dx = targetRef.current.x - posRef.current.x;
          const dy = targetRef.current.y - posRef.current.y;
          const dist = Math.hypot(dx, dy);

          if (dist < 45) {
            // Reached target waypoint -> pick a new location across the full screen
            pickNewWaypoint();
          } else {
            const speed = isMobile ? 120 : 180; // px per second
            const moveStep = Math.min(dist, speed * dt);
            const dirX = dx / dist;
            const dirY = dy / dist;

            posRef.current.x += dirX * moveStep;
            posRef.current.y += dirY * moveStep;

            // Gentle banking tilt in direction of movement
            const bankAngle = Math.max(-16, Math.min(16, dirX * 14));
            // Subtle altitude hover bob
            const hoverBob = Math.sin(time * 0.004) * 3;

            containerRef.current.style.transform = `translate3d(${posRef.current.x}px, ${posRef.current.y + hoverBob}px, 0px) rotate(${bankAngle}deg)`;
          }
        } else {
          // Docked at bottom-right corner (or smoothly returning home)
          const dock = getDockPosition();
          posRef.current.x += (dock.x - posRef.current.x) * 0.15;
          posRef.current.y += (dock.y - posRef.current.y) * 0.15;
          containerRef.current.style.transform = `translate3d(${posRef.current.x}px, ${posRef.current.y}px, 0px) rotate(0deg)`;
        }
      }

      animFrameRef.current = requestAnimationFrame(loop);
    };

    animFrameRef.current = requestAnimationFrame(loop);
    return () => {
      if (animFrameRef.current) cancelAnimationFrame(animFrameRef.current);
    };
  }, [pickNewWaypoint, getDockPosition, isMobile]);

  const pickRandomThought = useCallback((e) => {
    if (e) e.stopPropagation();
    setThoughtIndex((prev) => {
      if (COMPANION_THOUGHTS.length <= 1) return 0;
      let next;
      do {
        next = Math.floor(Math.random() * COMPANION_THOUGHTS.length);
      } while (next === prev);
      return next;
    });
  }, []);

  // Star symbol / click on Aero: waves and says Hi, DOES NOT open thought box
  const triggerWave = (e) => {
    if (e) e.stopPropagation();
    if (waveTimerRef.current) clearTimeout(waveTimerRef.current);
    if (hiTimerRef.current) clearTimeout(hiTimerRef.current);
    setIsWaving(true);
    setSayingHi(true);
    playAeroSynth('wave', soundEnabled);
    waveTimerRef.current = setTimeout(() => {
      setIsWaving(false);
    }, 2200);
    hiTimerRef.current = setTimeout(() => {
      setSayingHi(false);
    }, 2200);
  };

  // Toggle Anchor: When anchored, Aero stays permanently at bottom-right dock and NEVER flies
  const handleToggleAnchor = (e) => {
    e.stopPropagation();
    const nextAnchored = !isAnchored;
    setIsAnchored(nextAnchored);
    isAnchoredRef.current = nextAnchored;

    try {
      localStorage.setItem('aero_anchored', String(nextAnchored));
    } catch {}

    if (nextAnchored) {
      // Instantly dock to bottom-right and cancel all idle flight timers
      if (idleTimerRef.current) clearTimeout(idleTimerRef.current);
      setIsRoaming(false);
      isRoamingRef.current = false;
      const dock = getDockPosition();
      posRef.current = dock;
      targetRef.current = dock;
      if (containerRef.current) {
        containerRef.current.style.transform = `translate3d(${dock.x}px, ${dock.y}px, 0px) rotate(0deg)`;
      }
      playAeroSynth('whoosh', soundEnabled);
    } else {
      // Unanchored: start fresh 15s idle timer
      playAeroSynth('wave', soundEnabled);
    }
  };

  // Cycle Dress: Decoupled from wave & thought box
  const handleCycleDress = (e) => {
    e.stopPropagation();
    setDressIndex((prev) => (prev + 1) % COMPANION_DRESSES.length);
    playAeroSynth('dress', soundEnabled);
  };

  // Next thought acts naturally as a random picker
  const nextThought = (e) => {
    if (e) e.stopPropagation();
    pickRandomThought();
  };

  const prevThought = (e) => {
    if (e) e.stopPropagation();
    setThoughtIndex((prev) => (prev - 1 + COMPANION_THOUGHTS.length) % COMPANION_THOUGHTS.length);
  };

  // Do not render companion on landing page /
  if (location.pathname === '/' || location.pathname === '') return null;
  if (isClosed) return null;

  // In idle flight mode, micro controls are hidden for clean roaming; visible when docked, hovered or waving
  const showControls = isHovered || isWaving || !isRoaming || isAnchored;

  // Current thought item
  const currentThought = COMPANION_THOUGHTS[thoughtIndex];

  return (
    <aside 
      ref={containerRef}
      aria-label="Aero Floating AI Companion"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      style={{ width: `${aeroWidth}px` }}
      className="fixed top-0 left-0 z-50 pointer-events-auto select-none flex flex-col items-center cursor-pointer will-change-transform"
      onClick={triggerWave}
    >
      {/* Speech greeting bubble when star / wave is triggered */}
      {sayingHi && !thoughtBoxOpen && (
        <div 
          onClick={(e) => e.stopPropagation()}
          className="absolute -top-11 px-3 py-1.5 rounded-full bg-slate-900/98 backdrop-blur-md border border-cyan-400/60 text-cyan-200 font-bold text-xs shadow-lg shadow-cyan-500/20 animate-in fade-in zoom-in-95 duration-200 flex items-center gap-1.5 z-40 whitespace-nowrap pointer-events-none"
        >
          <span>Hi there!</span>
          <span className="text-sm">👋</span>
        </div>
      )}

      {/* REAL COMIC THOUGHT BOX:
          - Beautiful, wide, spacious cloud container with comfortable 14px typography
          - Aligned right-0 with a fixed 60px safe margin from window edge, ensuring zero cut-off
          - Real comic thought bubble tail: descending circular bubbles pointing down to Aero's head
          - Stays open for reading until dismissed or toggled
      */}
      {thoughtBoxOpen && !isRoaming && (
        <div 
          onClick={(e) => e.stopPropagation()}
          className="absolute bottom-[115%] right-0 w-[300px] sm:w-[350px] max-w-[calc(100vw-36px)] p-4 sm:p-5 rounded-[28px] bg-slate-900/98 backdrop-blur-2xl border-2 border-indigo-400/50 text-slate-100 shadow-[0_20px_50px_rgba(0,0,0,0.8),0_0_30px_rgba(99,102,241,0.25)] text-left transition-all duration-300 animate-in fade-in slide-in-from-bottom-2 z-30"
        >
          {/* Header Bar */}
          <div className="flex items-center justify-between border-b border-slate-800 pb-2 mb-2.5 gap-2">
            <div className="flex items-center gap-1.5 min-w-0">
              <span className="text-base shrink-0">💭</span>
              <span className="text-xs font-bold text-indigo-300 tracking-wide shrink-0">
                Aero's Thought
              </span>
              <span className="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 truncate max-w-[100px]">
                {currentThought.badge}
              </span>
            </div>
            
            <div className="flex items-center gap-1.5 text-xs text-slate-400 shrink-0">
              <AudioExplainerButton
                variant="compact"
                label="Listen"
                title={currentThought.topic}
                text={`${currentThought.topic}. ${currentThought.thought}`}
              />
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  setThoughtBoxOpen(false);
                }}
                className="text-slate-400 hover:text-white p-1 rounded-lg hover:bg-slate-800 transition shrink-0"
                title="Close thought box"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* Topic Title */}
          <div className="text-sm sm:text-base font-bold text-white mb-1.5 flex items-center gap-1.5">
            <span>{currentThought.topic}</span>
          </div>

          {/* Thought Content: Generous line height & comfortable font size for full readability */}
          <p className="text-xs sm:text-[13.5px] text-slate-200 font-normal leading-relaxed mb-3">
            {currentThought.thought}
          </p>

          {/* Footer Controls & Pagination */}
          <div className="pt-2 border-t border-slate-800/90 flex items-center justify-between text-xs">
            <span className="text-[10px] font-mono font-medium text-cyan-300 bg-cyan-950/60 px-2 py-0.5 rounded border border-cyan-800/50">
              #{currentThought.tag}
            </span>

            <div className="flex items-center gap-1.5">
              <button
                onClick={prevThought}
                className="p-1 rounded-md text-slate-400 hover:text-white hover:bg-slate-800 transition"
                title="Previous thought"
              >
                <ChevronLeft className="w-4 h-4" />
              </button>
              <button
                onClick={nextThought}
                className="px-2.5 py-1 rounded-md text-xs font-semibold text-cyan-300 hover:text-cyan-200 hover:bg-cyan-500/20 transition flex items-center gap-1 border border-cyan-500/30"
                title="Next thought"
              >
                <span>Next</span>
                <ChevronRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>

          {/* Real Comic Thought Tail: 3 descending circles pointing directly to Aero's head */}
          <div className="absolute -bottom-5 right-[48px] flex flex-col items-center pointer-events-none gap-0.5">
            <div className="w-3.5 h-3.5 rounded-full bg-slate-900 border-2 border-indigo-400/60 shadow-md" />
            <div className="w-2.5 h-2.5 rounded-full bg-slate-900 border-2 border-indigo-400/60 shadow-sm" />
            <div className="w-1.5 h-1.5 rounded-full bg-indigo-300 shadow-xs" />
          </div>
        </div>
      )}

      {/* Floating Ambient Glow */}
      <div 
        className="absolute inset-0 rounded-full filter blur-2xl opacity-70 transition-opacity duration-300 pointer-events-none scale-110"
        style={{ backgroundColor: selectedDress.glowColor }}
      />

      {/* BIG AERO VECTOR SVG COMPANION (No garden, no child, purely Aero) */}
      <div 
        style={{ width: `${aeroWidth}px`, height: `${aeroHeight}px` }}
        className="relative flex items-center justify-center filter drop-shadow-[0_12px_22px_rgba(0,0,0,0.65)]"
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
            {/* Jet Flame & Glow */}
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

      {/* Floating Micro Controls: Visible on hover/docked, hidden during idle roaming */}
      <div 
        onClick={(e) => e.stopPropagation()} 
        className={`mt-1 flex items-center gap-1 p-1 rounded-full bg-slate-900/95 backdrop-blur-md border border-slate-700/80 shadow-xl transition-all duration-300 ${
          showControls 
            ? 'opacity-100 scale-100 pointer-events-auto' 
            : 'opacity-0 scale-90 pointer-events-none'
        }`}
      >
        {/* Wave Button */}
        <button
          onClick={triggerWave}
          className="p-1 rounded-full text-cyan-300 hover:bg-slate-800 transition"
          title="Wave at Aero 👋"
        >
          <Sparkles className="w-3.5 h-3.5" />
        </button>

        {/* Thought Box Toggle Button */}
        <button
          onClick={() => setThoughtBoxOpen(!thoughtBoxOpen)}
          className={`p-1 rounded-full transition ${
            thoughtBoxOpen 
              ? 'text-cyan-300 bg-cyan-500/20' 
              : 'text-indigo-300 hover:bg-slate-800'
          }`}
          title="Open Aero's Thought Box 💭"
        >
          <MessageSquareQuote className="w-3.5 h-3.5" />
        </button>

        {/* Anchor Toggle Button: When anchored, Aero stays permanently docked at bottom-right and NEVER flies */}
        <button
          onClick={handleToggleAnchor}
          className={`p-1 px-1.5 rounded-full transition flex items-center gap-1 ${
            isAnchored 
              ? 'bg-emerald-500/25 text-emerald-300 border border-emerald-500/40 shadow-sm' 
              : 'text-slate-400 hover:text-white hover:bg-slate-800'
          }`}
          title={isAnchored ? "Anchored in place (Will NOT fly even if screen is idle • Click to unlock)" : "Anchor Aero to corner dock (prevents flying when idle)"}
        >
          <Anchor className="w-3.5 h-3.5" />
          {isAnchored && <span className="text-[9px] font-bold pr-0.5">Anchored</span>}
        </button>

        {/* Roam Now Button (Disabled/hidden when anchored) */}
        {!isAnchored && (
          <button
            onClick={() => {
              setThoughtBoxOpen(false);
              setIsRoaming(true);
              isRoamingRef.current = true;
              pickNewWaypoint();
              playAeroSynth('whoosh', soundEnabled);
            }}
            className="p-1 rounded-full text-indigo-300 hover:bg-slate-800 transition"
            title="Fly full screen now 🚀 (Will also fly if idle for 15s)"
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
