import React, { useEffect, useRef, useState, useCallback } from 'react';
import { 
  Sparkles, 
  ArrowRight, 
  Zap, 
  X, 
  Maximize2, 
  RotateCcw, 
  Compass, 
  Sliders, 
  Layers, 
  MousePointer, 
  Radio
} from 'lucide-react';
import { useTheme } from '../context/ThemeContext';

export default function KineticIntro({ isOpen, onClose }) {
  const canvasRef = useRef(null);
  const animFrameRef = useRef(null);
  const { theme } = useTheme();

  // Interactive Physics State
  const [gravityMode, setGravityMode] = useState('attract'); // 'attract' | 'repel'
  const [speedMultiplier, setSpeedMultiplier] = useState(1);
  const [particleCount, setParticleCount] = useState(120);
  const [colorPalette, setColorPalette] = useState('cosmic'); // 'cosmic' | 'emerald' | 'cyber' | 'solar'
  const [shockwaves, setShockwaves] = useState([]);
  const [isHudVisible, setIsHudVisible] = useState(true);

  // Shockwaves ref for access inside requestAnimationFrame
  const shockwavesRef = useRef([]);
  shockwavesRef.current = shockwaves;

  const palettes = {
    cosmic: ['#818cf8', '#38bdf8', '#c084fc', '#6366f1', '#e0e7ff'],
    emerald: ['#10b981', '#34d399', '#059669', '#6ee7b7', '#a7f3d0'],
    cyber: ['#ec4899', '#a855f7', '#06b6d4', '#f43f5e', '#fbcfe8'],
    solar: ['#f59e0b', '#fbbf24', '#f97316', '#ef4444', '#fef08a']
  };

  // Close on ESC key
  useEffect(() => {
    if (!isOpen) return;
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  // Main Canvas Simulation Engine
  useEffect(() => {
    if (!isOpen) return;

    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    const handleResize = () => {
      if (!canvas) return;
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    };
    window.addEventListener('resize', handleResize);

    let mouse = { x: -1000, y: -1000, active: false };
    const handleMouseMove = (e) => {
      mouse.x = e.clientX;
      mouse.y = e.clientY;
      mouse.active = true;
    };
    const handleMouseLeave = () => {
      mouse.active = false;
    };
    const handleClick = (e) => {
      // Spawn expanding shockwave ring on click
      setShockwaves((prev) => [
        ...prev.slice(-4), // keep up to 5 concurrent shockwaves
        {
          x: e.clientX,
          y: e.clientY,
          radius: 10,
          maxRadius: Math.max(width, height) * 0.45,
          alpha: 0.9,
          growthRate: 8 * speedMultiplier
        }
      ]);
    };

    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('mouseleave', handleMouseLeave);
    window.addEventListener('click', handleClick);

    // Initialize Particles
    const activeColors = palettes[colorPalette] || palettes.cosmic;
    const count = particleCount;
    const particles = [];
    const centerX = width / 2;
    const centerY = height / 2;

    for (let i = 0; i < count; i++) {
      const angle = Math.random() * Math.PI * 2;
      const dist = 30 + Math.random() * (Math.min(width, height) * 0.4);
      const speed = (0.8 + Math.random() * 2.2) * speedMultiplier;
      particles.push({
        x: centerX + Math.cos(angle) * dist,
        y: centerY + Math.sin(angle) * dist,
        vx: (Math.random() - 0.5) * speed,
        vy: (Math.random() - 0.5) * speed,
        radius: 1.5 + Math.random() * 3,
        color: activeColors[Math.floor(Math.random() * activeColors.length)],
        alpha: 0.3 + Math.random() * 0.7,
        pulseSpeed: 0.02 + Math.random() * 0.04,
        pulse: Math.random() * Math.PI
      });
    }

    const render = () => {
      // Subtle trail fade effect
      ctx.fillStyle = 'rgba(6, 9, 18, 0.22)';
      ctx.fillRect(0, 0, width, height);

      // Render Active Shockwaves
      setShockwaves((prevWaves) => {
        const nextWaves = [];
        for (const wave of prevWaves) {
          wave.radius += 6 * speedMultiplier;
          wave.alpha *= 0.96;

          if (wave.alpha > 0.02 && wave.radius < wave.maxRadius) {
            ctx.beginPath();
            ctx.arc(wave.x, wave.y, wave.radius, 0, Math.PI * 2);
            ctx.strokeStyle = activeColors[0];
            ctx.lineWidth = 2.5 * wave.alpha;
            ctx.globalAlpha = wave.alpha;
            ctx.stroke();

            // Repel particles caught in shockwave
            for (const p of particles) {
              const dx = p.x - wave.x;
              const dy = p.y - wave.y;
              const dist = Math.sqrt(dx * dx + dy * dy);
              if (Math.abs(dist - wave.radius) < 35) {
                const blastForce = 3 * wave.alpha * speedMultiplier;
                p.vx += (dx / (dist || 1)) * blastForce;
                p.vy += (dy / (dist || 1)) * blastForce;
              }
            }

            nextWaves.push(wave);
          }
        }
        return nextWaves;
      });

      // Update & Draw Particles
      for (let i = 0; i < particles.length; i++) {
        const p = particles[i];

        // Apply Velocity with speed multiplier
        p.x += p.vx * speedMultiplier;
        p.y += p.vy * speedMultiplier;

        // Mouse Gravitational Interaction
        if (mouse.active) {
          const mdx = mouse.x - p.x;
          const mdy = mouse.y - p.y;
          const mDist = Math.sqrt(mdx * mdx + mdy * mdy);

          if (mDist < 240 && mDist > 8) {
            const forceSign = gravityMode === 'attract' ? 1 : -1;
            const pullForce = (1 - mDist / 240) * 0.45 * forceSign * speedMultiplier;
            p.vx += (mdx / mDist) * pullForce;
            p.vy += (mdy / mDist) * pullForce;

            // Render glowing synaptic beam to cursor if nearby
            if (mDist < 160) {
              ctx.beginPath();
              ctx.moveTo(p.x, p.y);
              ctx.lineTo(mouse.x, mouse.y);
              ctx.strokeStyle = p.color;
              ctx.globalAlpha = (1 - mDist / 160) * 0.45;
              ctx.lineWidth = 1;
              ctx.stroke();
            }
          }
        }

        // Natural friction/drag
        p.vx *= 0.985;
        p.vy *= 0.985;

        // Bounce gently off screen boundaries
        if (p.x < 10) { p.x = 10; p.vx = Math.abs(p.vx); }
        if (p.x > width - 10) { p.x = width - 10; p.vx = -Math.abs(p.vx); }
        if (p.y < 10) { p.y = 10; p.vy = Math.abs(p.vy); }
        if (p.y > height - 10) { p.y = height - 10; p.vy = -Math.abs(p.vy); }

        // Particle Glow Pulse
        p.pulse += p.pulseSpeed;
        const currentAlpha = 0.35 + 0.45 * Math.sin(p.pulse);

        ctx.beginPath();
        ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        ctx.fillStyle = p.color;
        ctx.globalAlpha = currentAlpha;
        ctx.fill();

        // Connect nearby particles with synaptic neural links
        for (let j = i + 1; j < particles.length; j++) {
          const p2 = particles[j];
          const dx = p.x - p2.x;
          const dy = p.y - p2.y;
          const distSq = dx * dx + dy * dy;

          if (distSq < 110 * 110) {
            const dist = Math.sqrt(distSq);
            ctx.beginPath();
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(p2.x, p2.y);
            ctx.strokeStyle = p.color;
            ctx.globalAlpha = (1 - dist / 110) * 0.32;
            ctx.lineWidth = 0.8;
            ctx.stroke();
          }
        }
      }
      ctx.globalAlpha = 1.0;

      animFrameRef.current = requestAnimationFrame(render);
    };

    render();

    return () => {
      window.removeEventListener('resize', handleResize);
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mouseleave', handleMouseLeave);
      window.removeEventListener('click', handleClick);
      if (animFrameRef.current) {
        cancelAnimationFrame(animFrameRef.current);
      }
    };
  }, [isOpen, colorPalette, gravityMode, speedMultiplier, particleCount]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-hidden bg-slate-950/95 backdrop-blur select-none">
      {/* Simulation Canvas */}
      <canvas ref={canvasRef} className="absolute inset-0 w-full h-full block cursor-crosshair" />

      {/* Top Header Controls Bar */}
      <div className="absolute top-4 left-4 right-4 z-20 flex items-center justify-between pointer-events-none">
        {/* Left Branding */}
        <div className="flex items-center gap-3 pointer-events-auto bg-slate-900/80 backdrop-blur-md border border-slate-700/70 px-4 py-2 rounded-2xl shadow-xl">
          <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-indigo-500 to-cyan-400 p-[1.5px] shadow-md shadow-indigo-500/30">
            <div className="w-full h-full bg-slate-950 rounded-[10px] flex items-center justify-center">
              <Zap className="w-4 h-4 text-cyan-300 animate-pulse" />
            </div>
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-xs sm:text-sm font-bold text-white tracking-wide">
                Kinetic Neural Universe
              </h2>
              <span className="text-[10px] px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 font-mono">
                Interactive Physics
              </span>
            </div>
            <p className="text-[11px] text-slate-400 hidden sm:block">
              Click anywhere to pulse shockwaves • Hover to bend gravity
            </p>
          </div>
        </div>

        {/* Right Close & Return Button */}
        <div className="flex items-center gap-2 pointer-events-auto">
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white border border-indigo-400/40 text-xs font-semibold shadow-lg shadow-indigo-600/30 transition flex items-center gap-2 group"
            title="Return to The Era of AI portal (or press ESC)"
          >
            <span>Return to Portal</span>
            <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
          </button>
          
          <button
            onClick={onClose}
            className="p-2 rounded-xl bg-slate-900/80 hover:bg-slate-800 text-slate-400 hover:text-white border border-slate-700/60 shadow-lg transition"
            title="Close (ESC)"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Floating Physics Controls HUD (Bottom Bar) */}
      <div className="absolute bottom-6 left-1/2 -translate-x-1/2 z-20 w-full max-w-xl px-4 pointer-events-auto">
        <div className="bg-slate-900/90 backdrop-blur-md border border-slate-700/80 rounded-2xl p-3 shadow-2xl space-y-2.5">
          <div className="flex items-center justify-between text-xs pb-2 border-b border-slate-800/80">
            <span className="font-semibold text-slate-300 flex items-center gap-1.5 uppercase tracking-wider text-[11px]">
              <Sliders className="w-3.5 h-3.5 text-indigo-400" />
              Physics Controls & Neural Gravity
            </span>
            <div className="flex items-center gap-2 text-[10px] font-mono text-slate-400">
              <span>{particleCount} Nodes</span>
              <span>&bull;</span>
              <span>Click to Blast</span>
            </div>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs">
            {/* Gravity Mode Toggle */}
            <button
              onClick={() => setGravityMode(gravityMode === 'attract' ? 'repel' : 'attract')}
              className={`p-2 rounded-xl border font-medium flex items-center justify-center gap-1.5 transition ${
                gravityMode === 'attract'
                  ? 'bg-indigo-500/20 text-indigo-300 border-indigo-500/40 shadow-sm'
                  : 'bg-rose-500/20 text-rose-300 border-rose-500/40 shadow-sm'
              }`}
              title="Toggle between gravitational attraction and repulsion"
            >
              <MousePointer className="w-3.5 h-3.5" />
              <span>{gravityMode === 'attract' ? 'Attract Gravity' : 'Repel Shield'}</span>
            </button>

            {/* Speed Multiplier */}
            <button
              onClick={() => {
                if (speedMultiplier === 0.5) setSpeedMultiplier(1);
                else if (speedMultiplier === 1) setSpeedMultiplier(2);
                else setSpeedMultiplier(0.5);
              }}
              className="p-2 rounded-xl bg-slate-800 hover:bg-slate-750 text-slate-300 border border-slate-700/80 font-medium flex items-center justify-center gap-1.5 transition"
              title="Toggle particle speed multiplier"
            >
              <Zap className="w-3.5 h-3.5 text-amber-400" />
              <span>Speed: {speedMultiplier}x</span>
            </button>

            {/* Palette Selector */}
            <button
              onClick={() => {
                const keys = ['cosmic', 'emerald', 'cyber', 'solar'];
                const nextIdx = (keys.indexOf(colorPalette) + 1) % keys.length;
                setColorPalette(keys[nextIdx]);
              }}
              className="p-2 rounded-xl bg-slate-800 hover:bg-slate-750 text-slate-300 border border-slate-700/80 font-medium flex items-center justify-center gap-1.5 transition capitalize"
              title="Cycle color spectrum"
            >
              <Radio className="w-3.5 h-3.5 text-cyan-400" />
              <span>{colorPalette}</span>
            </button>

            {/* Particle Density */}
            <button
              onClick={() => {
                if (particleCount === 80) setParticleCount(140);
                else if (particleCount === 140) setParticleCount(200);
                else setParticleCount(80);
              }}
              className="p-2 rounded-xl bg-slate-800 hover:bg-slate-750 text-slate-300 border border-slate-700/80 font-medium flex items-center justify-center gap-1.5 transition"
              title="Change number of active synaptic nodes"
            >
              <Layers className="w-3.5 h-3.5 text-emerald-400" />
              <span>Density: {particleCount}</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
