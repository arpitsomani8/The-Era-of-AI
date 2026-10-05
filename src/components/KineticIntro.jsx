import React, { useEffect, useRef, useState } from 'react';
import { Sparkles, ArrowRight, Zap } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';

export default function KineticIntro({ isOpen, onClose }) {
  const canvasRef = useRef(null);
  const animFrameRef = useRef(null);
  const [progress, setProgress] = useState(0);
  const { theme } = useTheme();

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
    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('mouseleave', handleMouseLeave);

    // Particle setup
    const particleCount = Math.min(100, Math.floor((width * height) / 14000));
    const particles = [];
    const centerX = width / 2;
    const centerY = height / 2;

    const colors = theme === 'metallic-green'
      ? ['#10b981', '#34d399', '#059669', '#6ee7b7']
      : theme === 'bright'
      ? ['#6366f1', '#3b82f6', '#ec4899', '#8b5cf6']
      : ['#818cf8', '#38bdf8', '#c084fc', '#f472b6'];

    for (let i = 0; i < particleCount; i++) {
      const angle = Math.random() * Math.PI * 2;
      const speed = 1.5 + Math.random() * 4.5;
      particles.push({
        x: centerX + (Math.random() - 0.5) * 50,
        y: centerY + (Math.random() - 0.5) * 50,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed,
        radius: 1.5 + Math.random() * 2.5,
        color: colors[Math.floor(Math.random() * colors.length)],
        alpha: 0.2 + Math.random() * 0.8,
        pulseSpeed: 0.02 + Math.random() * 0.04,
        pulse: Math.random() * Math.PI
      });
    }

    let startTime = Date.now();
    const duration = 2400; // 2.4 seconds

    const render = () => {
      const elapsed = Date.now() - startTime;
      const currentProgress = Math.min(100, Math.floor((elapsed / duration) * 100));
      setProgress(currentProgress);

      ctx.fillStyle = theme === 'bright' ? 'rgba(248, 250, 252, 0.25)' : 'rgba(9, 13, 22, 0.25)';
      ctx.fillRect(0, 0, width, height);

      // Kinetic Center shockwave
      const waveRadius = (elapsed * 0.45) % (Math.max(width, height) * 0.6);
      ctx.beginPath();
      ctx.arc(centerX, centerY, waveRadius, 0, Math.PI * 2);
      ctx.strokeStyle = theme === 'metallic-green' ? 'rgba(16, 185, 129, 0.15)' : 'rgba(99, 102, 241, 0.15)';
      ctx.lineWidth = 2;
      ctx.stroke();

      // Secondary rotating kinetic rings
      const rotAngle = elapsed * 0.0015;
      ctx.save();
      ctx.translate(centerX, centerY);
      ctx.rotate(rotAngle);
      ctx.beginPath();
      ctx.arc(0, 0, 90, 0, Math.PI * 1.5);
      ctx.strokeStyle = theme === 'metallic-green' ? '#34d399' : '#818cf8';
      ctx.lineWidth = 1.5;
      ctx.stroke();

      ctx.rotate(-rotAngle * 2.2);
      ctx.beginPath();
      ctx.arc(0, 0, 140, 0, Math.PI);
      ctx.strokeStyle = theme === 'metallic-green' ? '#059669' : '#c084fc';
      ctx.lineWidth = 1;
      ctx.stroke();
      ctx.restore();

      // Update and draw kinetic particles
      for (let i = 0; i < particles.length; i++) {
        const p = particles[i];
        p.x += p.vx;
        // Mouse gravitational attraction
        if (mouse.active) {
          const mdx = mouse.x - p.x;
          const mdy = mouse.y - p.y;
          const mDist = Math.sqrt(mdx * mdx + mdy * mdy);
          if (mDist < 180 && mDist > 5) {
            const pullForce = (1 - mDist / 180) * 0.4;
            p.vx += (mdx / mDist) * pullForce;
            p.vy += (mdy / mDist) * pullForce;

            // Draw synaptic beam to cursor
            ctx.beginPath();
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(mouse.x, mouse.y);
            ctx.strokeStyle = theme === 'metallic-green' ? '#34d399' : '#38bdf8';
            ctx.globalAlpha = (1 - mDist / 180) * 0.5;
            ctx.lineWidth = 1;
            ctx.stroke();
          }
        }

        // Gravitational drag toward expanding perimeter
        p.vx *= 0.98;
        p.vy *= 0.98;

        // Bounce from walls
        if (p.x < 0 || p.x > width) p.vx *= -1;
        if (p.y < 0 || p.y > height) p.vy *= -1;

        p.pulse += p.pulseSpeed;
        const currentAlpha = 0.3 + 0.5 * Math.sin(p.pulse);

        ctx.beginPath();
        ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        ctx.fillStyle = p.color;
        ctx.globalAlpha = Math.max(0.1, currentAlpha);
        ctx.fill();

        // Connect nearby kinetic particles with glowing lines
        for (let j = i + 1; j < particles.length; j++) {
          const p2 = particles[j];
          const dx = p.x - p2.x;
          const dy = p.y - p2.y;
          const dist = Math.sqrt(dx * dx + dy * dy);

          if (dist < 110) {
            ctx.beginPath();
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(p2.x, p2.y);
            ctx.strokeStyle = p.color;
            ctx.globalAlpha = (1 - dist / 110) * 0.35;
            ctx.lineWidth = 0.8;
            ctx.stroke();
          }
        }
      }
      ctx.globalAlpha = 1.0;

      if (currentProgress < 100) {
        animFrameRef.current = requestAnimationFrame(render);
      } else {
        // Automatically complete and close after small delay
        setTimeout(() => {
          onClose();
        }, 300);
      }
    };

    render();

    return () => {
      window.removeEventListener('resize', handleResize);
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mouseleave', handleMouseLeave);
      if (animFrameRef.current) {
        cancelAnimationFrame(animFrameRef.current);
      }
    };
  }, [isOpen, onClose, theme]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center overflow-hidden bg-slate-950 transition-opacity duration-700 animate-fadeIn">
      {/* Background Kinetic Canvas */}
      <canvas ref={canvasRef} className="absolute inset-0 w-full h-full block" />

      {/* Kinetic Foreground Elements */}
      <div className="relative z-10 flex flex-col items-center justify-center text-center px-4 max-w-lg select-none">
        {/* Animated Quantum Core Badge */}
        <div className="relative mb-6">
          <div className="w-20 h-20 rounded-2xl bg-gradient-to-tr from-indigo-600 via-purple-600 to-cyan-400 p-[2px] shadow-2xl shadow-indigo-500/50 animate-pulse">
            <div className="w-full h-full bg-slate-950 rounded-2xl flex items-center justify-center overflow-hidden">
              <img 
                src={`${import.meta.env.BASE_URL}logo.png`} 
                alt="The Era of AI Emblem"
                className="w-14 h-14 object-cover animate-spin-slow"
                style={{ animationDuration: '16s' }}
              />
            </div>
          </div>
          {/* Radial pulse rings */}
          <div className="absolute -inset-4 rounded-full border border-indigo-500/20 animate-ping opacity-30 pointer-events-none" />
        </div>

        {/* Cinematic Title Reveal */}
        <div className="space-y-2 mb-6">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 text-xs font-semibold tracking-widest uppercase">
            <Sparkles className="w-3.5 h-3.5 text-cyan-400 animate-bounce" />
            <span>Kinetic Knowledge Engine</span>
          </div>

          <h1 className="text-3xl sm:text-5xl font-black text-transparent bg-clip-text bg-gradient-to-r from-white via-indigo-200 to-cyan-400 tracking-tight drop-shadow-lg">
            The Era of AI
          </h1>

          <p className="text-xs sm:text-sm text-slate-300 tracking-wide font-light max-w-md">
            Connecting 41 Neural Nodes, 34 Curricula Tracks, and Landmark Research
          </p>
        </div>

        {/* Progress Bar & Indicators */}
        <div className="w-64 sm:w-80 space-y-2">
          <div className="h-1.5 w-full bg-slate-900 border border-slate-800 rounded-full overflow-hidden p-[1px]">
            <div 
              className="h-full bg-gradient-to-r from-indigo-500 via-purple-500 to-cyan-400 rounded-full transition-all duration-100 ease-out shadow-lg shadow-indigo-500/50"
              style={{ width: `${progress}%` }}
            />
          </div>

          <div className="flex items-center justify-between text-[11px] font-mono text-slate-400">
            <span className="flex items-center gap-1.5">
              <Zap className="w-3 h-3 text-amber-400 animate-pulse" />
              <span>Synaptic Graph Online</span>
            </span>
            <span className="text-indigo-400 font-semibold">{progress}%</span>
          </div>
        </div>

        {/* Direct Skip Button */}
        <button
          onClick={onClose}
          className="mt-8 px-5 py-2 rounded-xl bg-slate-900/80 hover:bg-indigo-600/30 text-slate-300 hover:text-white border border-slate-700/60 hover:border-indigo-500/50 text-xs font-medium transition flex items-center gap-2 group shadow-lg backdrop-blur"
        >
          <span>Enter Master Universe</span>
          <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform text-indigo-400" />
        </button>
      </div>
    </div>
  );
}
