import React, { useState, useEffect, useRef, useCallback } from 'react';
import { Volume2, VolumeX, Pause, Play, RotateCcw, User, Sparkles } from 'lucide-react';
import { 
  getStoredVoiceGender, 
  setStoredVoiceGender, 
  cleanTextForSpeech, 
  splitIntoSentences, 
  pickVoiceForGender, 
  getPitchForGender 
} from '../utils/audioSpeech';

export default function AudioExplainerButton({ 
  title = '', 
  definition = '', 
  intuition = '', 
  example = '',
  formula = '',
  formula_explanation = '',
  text = '',
  label = 'Audio Explainer',
  variant = 'default', // 'default', 'compact', 'minimal'
  showVoiceToggle = undefined,
  className = ''
}) {
  const shouldShowVoiceToggle = showVoiceToggle !== undefined ? showVoiceToggle : (variant !== 'compact');
  const [isSupported, setIsSupported] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [playbackRate, setPlaybackRate] = useState(1.0); // 1.0, 1.25, 1.5
  const [voiceGender, setVoiceGender] = useState(getStoredVoiceGender());
  const [availableVoices, setAvailableVoices] = useState([]);

  const utteranceRef = useRef(null);
  const sentencesRef = useRef([]);
  const currentSentenceIdxRef = useRef(0);
  const isPlayingRef = useRef(false);

  // Initialize SpeechSynthesis and voice list
  useEffect(() => {
    if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
      setIsSupported(true);

      const loadVoices = () => {
        const v = window.speechSynthesis.getVoices();
        if (v && v.length > 0) {
          setAvailableVoices(v);
        }
      };

      loadVoices();
      if (window.speechSynthesis.onvoiceschanged !== undefined) {
        window.speechSynthesis.onvoiceschanged = loadVoices;
      }
    }
  }, []);

  // Sync voice preference across all button instances in real-time
  useEffect(() => {
    const handleVoiceChange = (e) => {
      const newGender = e.detail || getStoredVoiceGender();
      setVoiceGender(newGender);
    };

    window.addEventListener('era-voice-changed', handleVoiceChange);
    return () => {
      window.removeEventListener('era-voice-changed', handleVoiceChange);
    };
  }, []);

  // Stop speech when component unmounts or title changes
  useEffect(() => {
    return () => {
      if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
        window.speechSynthesis.cancel();
      }
      isPlayingRef.current = false;
    };
  }, [title, text]);

  // Construct complete clean text script from props
  const getFullScript = useCallback(() => {
    if (text) {
      return cleanTextForSpeech(text);
    }
    const cleanTitle = cleanTextForSpeech(title);
    const cleanDef = cleanTextForSpeech(definition);
    const cleanForm = cleanTextForSpeech(formula);
    const cleanFormExp = cleanTextForSpeech(formula_explanation);
    const cleanInt = cleanTextForSpeech(intuition);
    const cleanEx = cleanTextForSpeech(example);

    const parts = [];
    if (cleanTitle) parts.push(cleanTitle);
    if (cleanDef) parts.push(cleanDef);
    if (cleanForm) parts.push(`Mathematical equation: ${cleanForm}`);
    if (cleanFormExp) parts.push(`Equation breakdown: ${cleanFormExp}`);
    if (cleanInt) parts.push(`Key technical intuition: ${cleanInt}`);
    if (cleanEx) parts.push(`For example: ${cleanEx}`);

    return parts.join('. ');
  }, [text, title, definition, intuition, example, formula, formula_explanation]);

  // Play a specific sentence index in queue (ensures browser doesn't cut out on long texts)
  const speakSentence = useCallback((index, sentences, gender, rate) => {
    if (!('speechSynthesis' in window)) return;
    const synth = window.speechSynthesis;

    if (index >= sentences.length || !isPlayingRef.current) {
      setIsPlaying(false);
      setIsPaused(false);
      isPlayingRef.current = false;
      return;
    }

    currentSentenceIdxRef.current = index;
    const rawSentence = sentences[index];

    const utterance = new SpeechSynthesisUtterance(rawSentence);
    utteranceRef.current = utterance;
    utterance.rate = rate;
    utterance.pitch = getPitchForGender(gender);

    const voices = synth.getVoices().length > 0 ? synth.getVoices() : availableVoices;
    const selectedVoice = pickVoiceForGender(voices, gender);
    if (selectedVoice) {
      utterance.voice = selectedVoice;
    }

    utterance.onend = () => {
      if (isPlayingRef.current) {
        // Speak next sentence seamlessly
        speakSentence(index + 1, sentences, gender, rate);
      }
    };

    utterance.onerror = (e) => {
      if (e.error !== 'canceled' && e.error !== 'interrupted') {
        console.warn('Speech synthesis error:', e);
      }
      if (isPlayingRef.current) {
        speakSentence(index + 1, sentences, gender, rate);
      }
    };

    synth.speak(utterance);
  }, [availableVoices]);

  const handleTogglePlay = (e) => {
    e?.stopPropagation();
    if (!isSupported) return;

    const synth = window.speechSynthesis;

    // Resume if paused
    if (isPaused) {
      synth.resume();
      setIsPaused(false);
      setIsPlaying(true);
      isPlayingRef.current = true;
      return;
    }

    // Pause if currently playing
    if (isPlaying) {
      synth.pause();
      setIsPaused(true);
      setIsPlaying(false);
      isPlayingRef.current = false;
      return;
    }

    // Start fresh playback
    synth.cancel();
    const fullScript = getFullScript();
    if (!fullScript) return;

    const sentences = splitIntoSentences(fullScript);
    if (sentences.length === 0) return;

    sentencesRef.current = sentences;
    isPlayingRef.current = true;
    setIsPlaying(true);
    setIsPaused(false);

    speakSentence(0, sentences, voiceGender, playbackRate);
  };

  const handleStop = (e) => {
    e?.stopPropagation();
    if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
      window.speechSynthesis.cancel();
    }
    isPlayingRef.current = false;
    setIsPlaying(false);
    setIsPaused(false);
  };

  // Toggle voice between Female & Male
  const handleToggleVoiceGender = (e) => {
    e?.stopPropagation();
    const nextGender = voiceGender === 'female' ? 'male' : 'female';
    setVoiceGender(nextGender);
    setStoredVoiceGender(nextGender);

    // If currently speaking, restart current sentence with the new voice seamlessly
    if (isPlaying || isPaused) {
      const currentIdx = currentSentenceIdxRef.current;
      const sentences = sentencesRef.current;
      if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
        window.speechSynthesis.cancel();
      }
      setTimeout(() => {
        isPlayingRef.current = true;
        setIsPlaying(true);
        setIsPaused(false);
        speakSentence(currentIdx, sentences, nextGender, playbackRate);
      }, 50);
    }
  };

  // Cycle speed (1x -> 1.25x -> 1.5x)
  const cycleSpeed = (e) => {
    e?.stopPropagation();
    const speeds = [1.0, 1.25, 1.5];
    const nextIdx = (speeds.indexOf(playbackRate) + 1) % speeds.length;
    const newRate = speeds[nextIdx];
    setPlaybackRate(newRate);

    // If currently playing, restart current sentence with new rate
    if (isPlaying || isPaused) {
      const currentIdx = currentSentenceIdxRef.current;
      const sentences = sentencesRef.current;
      if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
        window.speechSynthesis.cancel();
      }
      setTimeout(() => {
        isPlayingRef.current = true;
        setIsPlaying(true);
        setIsPaused(false);
        speakSentence(currentIdx, sentences, voiceGender, newRate);
      }, 50);
    }
  };

  if (!isSupported) return null;

  const isFemale = voiceGender === 'female';

  return (
    <div className={`inline-flex items-center gap-1.5 flex-nowrap whitespace-nowrap ${className}`}>
      {/* Main Play / Pause Button */}
      <button
        onClick={handleTogglePlay}
        className={`rounded-lg border font-semibold transition flex items-center gap-1.5 shadow-sm active:scale-95 cursor-pointer shrink-0 ${
          variant === 'compact'
            ? 'px-2 py-1 text-[11px]'
            : 'px-2.5 py-1 text-xs'
        } ${
          isPlaying
            ? 'bg-rose-500/20 text-rose-300 border-rose-500/50 shadow-rose-500/20 ring-1 ring-rose-500/30'
            : isPaused
            ? 'bg-amber-500/20 text-amber-300 border-amber-500/50'
            : 'bg-slate-900 border-slate-700/80 text-slate-300 hover:text-white hover:bg-slate-800'
        }`}
        title={isPlaying ? 'Pause Audio Explainer' : isPaused ? 'Resume Audio Explainer' : `Listen with ${isFemale ? 'Female' : 'Male'} Voice`}
      >
        {isPlaying ? (
          <>
            {/* Animated Equalizer Sound Wave Bars */}
            <div className="flex items-end gap-0.5 h-3.5 w-3 px-0.5">
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
            <span>{label}</span>
          </>
        )}
      </button>

      {/* Dual Voice Toggle: Sleek compact icon button without bulky text */}
      {shouldShowVoiceToggle && (
        <button
          onClick={handleToggleVoiceGender}
          className={`p-1 px-1.5 rounded-lg border text-xs font-medium transition flex items-center justify-center shrink-0 cursor-pointer ${
            isFemale
              ? 'bg-pink-950/40 text-pink-300 border-pink-500/40 hover:bg-pink-900/50'
              : 'bg-blue-950/40 text-blue-300 border-blue-500/40 hover:bg-blue-900/50'
          }`}
          title={`Narrator Voice: ${isFemale ? 'Female' : 'Male'} (Click to switch to ${isFemale ? 'Male' : 'Female'})`}
          aria-label={`Voice: ${isFemale ? 'Female' : 'Male'}`}
        >
          <span className="text-xs leading-none">{isFemale ? '👩' : '👨'}</span>
        </button>
      )}

      {/* Speed & Stop Controls when active or paused */}
      {(isPlaying || isPaused) && (
        <div className="inline-flex items-center gap-1 bg-slate-900/90 border border-slate-700/80 rounded-lg p-0.5 shrink-0 animate-in fade-in zoom-in-95 duration-150">
          <button
            onClick={cycleSpeed}
            className="px-1.5 py-0.5 rounded text-[10px] font-mono font-bold text-slate-300 hover:text-white hover:bg-slate-800 transition cursor-pointer"
            title="Cycle Voice Speed (1.0x, 1.25x, 1.5x)"
          >
            {playbackRate}x
          </button>
          <button
            onClick={handleStop}
            className="p-1 rounded text-slate-400 hover:text-rose-400 hover:bg-rose-500/10 transition cursor-pointer"
            title="Stop Speech"
          >
            <VolumeX className="w-3 h-3" />
          </button>
        </div>
      )}
    </div>
  );
}
