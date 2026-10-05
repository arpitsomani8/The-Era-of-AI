import React, { useState, useEffect, useRef } from 'react';
import { Volume2, VolumeX, Pause, Play, RotateCcw } from 'lucide-react';

// Utility to convert LaTeX equations into natural, spoken English
function cleanTextForSpeech(raw) {
  if (!raw) return '';
  let text = raw;

  // Remove markdown bold/italics
  text = text.replace(/[*_#`]/g, '');

  // Math symbol replacements
  text = text.replace(/\$\$/g, ' ');
  text = text.replace(/\$/g, ' ');
  text = text.replace(/\\text\{([^}]+)\}/g, '$1');
  text = text.replace(/\\frac\{([^}]+)\}\{([^}]+)\}/g, '$1 over $2');
  text = text.replace(/\\sum_\{[^}]+\}\^\{[^}]+\}/g, 'sum of');
  text = text.replace(/\\sum/g, 'sum');
  text = text.replace(/\\prod/g, 'product');
  text = text.replace(/\\sqrt\{([^}]+)\}/g, 'square root of $1');
  text = text.replace(/\\sqrt/g, 'square root');
  text = text.replace(/\\cdot/g, ' dot ');
  text = text.replace(/\\times/g, ' times ');
  text = text.replace(/\\approx/g, ' approximately equals ');
  text = text.replace(/\\neq/g, ' does not equal ');
  text = text.replace(/\\leq/g, ' is less than or equal to ');
  text = text.replace(/\\geq/g, ' is greater than or equal to ');
  text = text.replace(/\\int/g, 'integral');
  text = text.replace(/\\partial/g, 'partial');
  text = text.replace(/\\alpha/g, 'alpha');
  text = text.replace(/\\beta/g, 'beta');
  text = text.replace(/\\gamma/g, 'gamma');
  text = text.replace(/\\theta/g, 'theta');
  text = text.replace(/\\lambda/g, 'lambda');
  text = text.replace(/\\sigma/g, 'sigma');
  text = text.replace(/\\mu/g, 'mu');
  text = text.replace(/\\epsilon/g, 'epsilon');
  text = text.replace(/\\tau/g, 'tau');
  text = text.replace(/\\mathcal\{L\}/g, 'Loss');
  text = text.replace(/\\mathbb\{R\}/g, 'real numbers');
  text = text.replace(/\\in/g, ' in ');
  text = text.replace(/\\to/g, ' to ');
  text = text.replace(/\\dots/g, 'and so on');
  text = text.replace(/\\quad/g, ' ');
  text = text.replace(/\\implies/g, ' implies ');
  text = text.replace(/\\min/g, 'minimum ');
  text = text.replace(/\\max/g, 'maximum ');
  text = text.replace(/\\log/g, 'log ');
  text = text.replace(/\\exp/g, 'exponential of ');
  text = text.replace(/\\sin/g, 'sine ');
  text = text.replace(/\\cos/g, 'cosine ');

  // Clean backslashes & braces
  text = text.replace(/\\[a-zA-Z]+/g, ' ');
  text = text.replace(/[{}]/g, ' ');
  text = text.replace(/\s+/g, ' ').trim();

  return text;
}

export default function AudioExplainerButton({ 
  title = '', 
  definition = '', 
  intuition = '', 
  example = '',
  className = ''
}) {
  const [isSupported, setIsSupported] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [playbackRate, setPlaybackRate] = useState(1.0); // 1.0, 1.25, 1.5
  const utteranceRef = useRef(null);

  useEffect(() => {
    if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
      setIsSupported(true);
    }
  }, []);

  // Stop speech when component unmounts
  useEffect(() => {
    return () => {
      if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
        window.speechSynthesis.cancel();
      }
    };
  }, [title]);

  const handleTogglePlay = () => {
    if (!isSupported) return;

    const synth = window.speechSynthesis;

    // If currently paused, resume
    if (isPaused) {
      synth.resume();
      setIsPaused(false);
      setIsPlaying(true);
      return;
    }

    // If currently speaking, pause
    if (isPlaying) {
      synth.pause();
      setIsPaused(true);
      setIsPlaying(false);
      return;
    }

    // Start fresh speech
    synth.cancel();

    // Construct narration script
    const cleanTitle = cleanTextForSpeech(title);
    const cleanDef = cleanTextForSpeech(definition);
    const cleanInt = cleanTextForSpeech(intuition);
    const cleanEx = cleanTextForSpeech(example);

    let script = `${cleanTitle}. `;
    if (cleanDef) script += `${cleanDef}. `;
    if (cleanInt) script += `Key technical intuition: ${cleanInt}. `;
    if (cleanEx) script += `For example: ${cleanEx}.`;

    const utterance = new SpeechSynthesisUtterance(script);
    utteranceRef.current = utterance;
    utterance.rate = playbackRate;
    utterance.pitch = 1.0;

    // Choose a high-quality English voice if available
    const voices = synth.getVoices();
    const naturalVoice = voices.find(v => 
      (v.lang.startsWith('en') && (v.name.includes('Natural') || v.name.includes('Google') || v.name.includes('Samantha') || v.name.includes('Daniel') || v.name.includes('Microsoft')))
    ) || voices.find(v => v.lang.startsWith('en'));

    if (naturalVoice) {
      utterance.voice = naturalVoice;
    }

    utterance.onend = () => {
      setIsPlaying(false);
      setIsPaused(false);
    };

    utterance.onerror = () => {
      setIsPlaying(false);
      setIsPaused(false);
    };

    synth.speak(utterance);
    setIsPlaying(true);
    setIsPaused(false);
  };

  const handleStop = (e) => {
    e.stopPropagation();
    if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
      window.speechSynthesis.cancel();
    }
    setIsPlaying(false);
    setIsPaused(false);
  };

  const cycleSpeed = (e) => {
    e.stopPropagation();
    const speeds = [1.0, 1.25, 1.5];
    const nextIdx = (speeds.indexOf(playbackRate) + 1) % speeds.length;
    const newRate = speeds[nextIdx];
    setPlaybackRate(newRate);

    // If currently playing, restart with new rate seamlessly
    if (isPlaying || isPaused) {
      handleStop(e);
      setTimeout(() => {
        setPlaybackRate(newRate);
      }, 50);
    }
  };

  if (!isSupported) return null;

  return (
    <div className={`inline-flex items-center gap-1.5 ${className}`}>
      {/* Main Play / Pause Button */}
      <button
        onClick={handleTogglePlay}
        className={`px-2.5 py-1 rounded-lg border text-xs font-semibold transition flex items-center gap-1.5 shadow-sm active:scale-95 ${
          isPlaying
            ? 'bg-rose-500/20 text-rose-300 border-rose-500/50 shadow-rose-500/20'
            : isPaused
            ? 'bg-amber-500/20 text-amber-300 border-amber-500/50'
            : 'bg-slate-900 border-slate-700/80 text-slate-300 hover:text-white hover:bg-slate-800'
        }`}
        title={isPlaying ? 'Pause Audio Explainer' : isPaused ? 'Resume Audio Explainer' : 'Listen to Audio Explainer'}
      >
        {isPlaying ? (
          <>
            {/* Animated Equalizer Sound Wave Bars */}
            <div className="flex items-end gap-0.5 h-3.5 w-3.5 px-0.5">
              <span className="w-0.5 bg-rose-400 rounded-full animate-bounce h-2" style={{ animationDelay: '0ms' }} />
              <span className="w-0.5 bg-rose-400 rounded-full animate-bounce h-3.5" style={{ animationDelay: '150ms' }} />
              <span className="w-0.5 bg-rose-400 rounded-full animate-bounce h-2.5" style={{ animationDelay: '300ms' }} />
            </div>
            <span>Pause</span>
          </>
        ) : isPaused ? (
          <>
            <Play className="w-3.5 h-3.5 text-amber-400 fill-amber-400" />
            <span>Resume</span>
          </>
        ) : (
          <>
            <Volume2 className="w-3.5 h-3.5 text-rose-400" />
            <span>Audio Explainer</span>
          </>
        )}
      </button>

      {/* Speed & Stop Controls when active or paused */}
      {(isPlaying || isPaused) && (
        <div className="inline-flex items-center gap-1 bg-slate-900/90 border border-slate-700/70 rounded-lg p-0.5 animate-in fade-in zoom-in-95 duration-150">
          <button
            onClick={cycleSpeed}
            className="px-1.5 py-0.5 rounded text-[10px] font-mono font-bold text-slate-300 hover:text-white hover:bg-slate-800 transition"
            title="Cycle Voice Speed (1x, 1.25x, 1.5x)"
          >
            {playbackRate}x
          </button>
          <button
            onClick={handleStop}
            className="p-1 rounded text-slate-400 hover:text-rose-400 hover:bg-rose-500/10 transition"
            title="Stop Speech"
          >
            <VolumeX className="w-3 h-3" />
          </button>
        </div>
      )}
    </div>
  );
}
