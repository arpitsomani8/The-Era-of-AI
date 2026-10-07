/**
 * High-fidelity Text-To-Speech (TTS) & Pronunciation Alignment Engine
 * Provides dual-voice selection (Female / Male), natural LaTeX-to-English conversion,
 * and synchronized sentence tracking for The Era of AI.
 */

const VOICE_STORAGE_KEY = 'era_of_ai_voice_gender';

/**
 * Get stored voice preference ('female' | 'male')
 */
export function getStoredVoiceGender() {
  if (typeof window === 'undefined') return 'female';
  try {
    const val = localStorage.getItem(VOICE_STORAGE_KEY);
    return val === 'male' ? 'male' : 'female';
  } catch {
    return 'female';
  }
}

/**
 * Store user voice preference and broadcast change event to all components
 */
export function setStoredVoiceGender(gender) {
  if (typeof window === 'undefined') return;
  const normalized = gender === 'male' ? 'male' : 'female';
  try {
    localStorage.setItem(VOICE_STORAGE_KEY, normalized);
  } catch (e) {
    console.warn('Unable to persist voice preference to localStorage:', e);
  }
  // Dispatch custom event so all active audio buttons across the app sync instantly
  window.dispatchEvent(new CustomEvent('era-voice-changed', { detail: normalized }));
}

/**
 * Convert technical mathematical formulations, LaTeX code, and markdown
 * into natural, conversational spoken English.
 */
export function cleanTextForSpeech(raw) {
  if (!raw || typeof raw !== 'string') return '';
  let text = raw;

  // 1. Remove markdown links [text](url) -> text
  text = text.replace(/\[([^\]]+)\]\([^)]+\)/g, '$1');

  // 2. Remove code blocks ```code``` -> 'code block'
  text = text.replace(/```[\s\S]*?```/g, ' ');

  // 3. Remove markdown headers, bold, italics, inline code backticks
  text = text.replace(/[#*_`]/g, '');

  // 4. Common Technical AI Acronyms - expand or add phonetic spacing
  const acronyms = [
    { regex: /\bLLMs\b/g, replace: 'large language models' },
    { regex: /\bLLM\b/g, replace: 'large language model' },
    { regex: /\bGPU\b/g, replace: 'G-P-U' },
    { regex: /\bGPUs\b/g, replace: 'G-P-Us' },
    { regex: /\bVRAM\b/g, replace: 'V-RAM' },
    { regex: /\bQPS\b/g, replace: 'queries per second' },
    { regex: /\bTTS\b/g, replace: 'text to speech' },
    { regex: /\bASR\b/g, replace: 'automatic speech recognition' },
    { regex: /\bRAG\b/g, replace: 'rag retrieval augmented generation' },
    { regex: /\bRLHF\b/g, replace: 'R-L-H-F reinforcement learning from human feedback' },
    { regex: /\bSGD\b/g, replace: 'stochastic gradient descent' },
    { regex: /\bAdamW\b/gi, replace: 'Adam-W' },
    { regex: /\bLoRA\b/g, replace: 'Lora low rank adaptation' },
    { regex: /\bRoPE\b/g, replace: 'Rope rotary position embeddings' },
    { regex: /\bKV-cache\b/gi, replace: 'K-V cache' },
    { regex: /\bMoE\b/g, replace: 'Mixture of Experts' },
    { regex: /\bSVD\b/g, replace: 'S-V-D singular value decomposition' },
    { regex: /\bPCA\b/g, replace: 'P-C-A principal component analysis' },
    { regex: /\bMSE\b/g, replace: 'mean squared error' },
    { regex: /\bRMSE\b/g, replace: 'root mean squared error' },
    { regex: /\bMAE\b/g, replace: 'mean absolute error' },
    { regex: /\bBPE\b/g, replace: 'byte pair encoding' },
    { regex: /\bAPI\b/g, replace: 'A-P-I' },
    { regex: /\bAPIs\b/g, replace: 'A-P-Is' },
    { regex: /\bvs\.\b/gi, replace: 'versus' },
    { regex: /\be\.g\.\b/gi, replace: 'for example' },
    { regex: /\bi\.e\.\b/gi, replace: 'that is' }
  ];

  for (const acr of acronyms) {
    text = text.replace(acr.regex, acr.replace);
  }

  // 5. LaTeX and Mathematical Notation replacements
  text = text.replace(/\$\$/g, ' ');
  text = text.replace(/\$/g, ' ');
  text = text.replace(/\\text\{([^}]+)\}/g, '$1');
  text = text.replace(/\\mathbf\{([^}]+)\}/g, '$1');
  text = text.replace(/\\mathcal\{L\}/g, 'Loss function');
  text = text.replace(/\\mathcal\{([A-Za-z])\}/g, '$1');
  text = text.replace(/\\mathbb\{R\}/g, 'real numbers');
  text = text.replace(/\\mathbb\{E\}/g, 'expected value');
  text = text.replace(/\\mathbb\{([A-Za-z])\}/g, '$1');
  text = text.replace(/\\frac\{([^}]+)\}\{([^}]+)\}/g, '$1 divided by $2');
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
  text = text.replace(/\\le\b/g, ' is less than or equal to ');
  text = text.replace(/\\ge\b/g, ' is greater than or equal to ');
  text = text.replace(/\\int/g, 'integral');
  text = text.replace(/\\partial/g, 'partial derivative of');
  text = text.replace(/\\nabla/g, 'gradient of');
  text = text.replace(/\\alpha/g, 'alpha');
  text = text.replace(/\\beta/g, 'beta');
  text = text.replace(/\\gamma/g, 'gamma');
  text = text.replace(/\\theta/g, 'theta');
  text = text.replace(/\\lambda/g, 'lambda');
  text = text.replace(/\\sigma/g, 'sigma');
  text = text.replace(/\\mu/g, 'mu');
  text = text.replace(/\\epsilon/g, 'epsilon');
  text = text.replace(/\\tau/g, 'tau');
  text = text.replace(/\\omega/g, 'omega');
  text = text.replace(/\\in\b/g, ' in ');
  text = text.replace(/\\to\b/g, ' to ');
  text = text.replace(/\\rightarrow/g, ' leads to ');
  text = text.replace(/\\dots/g, 'and so on');
  text = text.replace(/\\quad/g, ' ');
  text = text.replace(/\\implies/g, ' implies ');
  text = text.replace(/\\min/g, 'minimum ');
  text = text.replace(/\\max/g, 'maximum ');
  text = text.replace(/\\log/g, 'logarithm of ');
  text = text.replace(/\\exp/g, 'exponential of ');
  text = text.replace(/\\sin/g, 'sine ');
  text = text.replace(/\\cos/g, 'cosine ');
  text = text.replace(/\\forall/g, 'for all ');
  text = text.replace(/\\exists/g, 'there exists ');

  // 6. Clean residual backslash commands & braces
  text = text.replace(/\\[a-zA-Z]+/g, ' ');
  text = text.replace(/[{}]/g, ' ');
  text = text.replace(/[_^]/g, ' ');

  // 7. HTML entities
  text = text.replace(/&bull;/g, ', ');
  text = text.replace(/&amp;/g, ' and ');
  text = text.replace(/&lt;/g, ' less than ');
  text = text.replace(/&gt;/g, ' greater than ');
  text = text.replace(/<[^>]+>/g, ' ');

  // 8. Normalize spacing and punctuation
  text = text.replace(/\s+/g, ' ').trim();
  // Ensure string ends with a period if not present
  if (text && !/[.!?]$/.test(text)) {
    text += '.';
  }

  return text;
}

/**
 * Split clean text into distinct sentences for live subtitle alignment
 */
export function splitIntoSentences(text) {
  if (!text) return [];
  // Match sentences ending in punctuation
  const matches = text.match(/[^.!?]+[.!?]+(?:\s|$)|[^.!?]+$/g);
  if (!matches) return [text];
  return matches.map(s => s.trim()).filter(Boolean);
}

/**
 * Resolve the optimal browser TTS voice matching gender preference.
 */
export function pickVoiceForGender(voices, gender = 'female') {
  if (!voices || voices.length === 0) return null;
  const enVoices = voices.filter(v => v.lang && v.lang.toLowerCase().startsWith('en'));
  const candidatePool = enVoices.length > 0 ? enVoices : voices;

  const femaleKeywords = [
    'zira', 'samantha', 'victoria', 'jenny', 'karen', 'aria', 'serena',
    'cynthia', 'eva', 'susan', 'hazel', 'heera', 'catherine', 'linda',
    'female', 'google us english'
  ];
  const maleKeywords = [
    'david', 'daniel', 'alex', 'george', 'guy', 'mark', 'richard',
    'oliver', 'james', 'ryan', 'male', 'google uk english male'
  ];

  if (gender === 'female') {
    // 1. Natural / Online high-fidelity female
    const naturalFemale = candidatePool.find(v =>
      femaleKeywords.some(k => v.name.toLowerCase().includes(k)) &&
      (v.name.includes('Natural') || v.name.includes('Online'))
    );
    if (naturalFemale) return naturalFemale;

    // 2. Named female voice
    const namedFemale = candidatePool.find(v =>
      femaleKeywords.some(k => v.name.toLowerCase().includes(k))
    );
    if (namedFemale) return namedFemale;

    // 3. Fallback: English voice that is not explicitly male
    const notMale = candidatePool.find(v =>
      !maleKeywords.some(k => v.name.toLowerCase().includes(k))
    );
    if (notMale) return notMale;

    return candidatePool[0];
  } else {
    // Male
    // 1. Natural / Online high-fidelity male
    const naturalMale = candidatePool.find(v =>
      maleKeywords.some(k => v.name.toLowerCase().includes(k)) &&
      (v.name.includes('Natural') || v.name.includes('Online'))
    );
    if (naturalMale) return naturalMale;

    // 2. Named male voice
    const namedMale = candidatePool.find(v =>
      maleKeywords.some(k => v.name.toLowerCase().includes(k))
    );
    if (namedMale) return namedMale;

    // 3. Fallback: English voice that is not explicitly female
    const notFemale = candidatePool.find(v =>
      !femaleKeywords.some(k => v.name.toLowerCase().includes(k))
    );
    if (notFemale) return notFemale;

    return candidatePool[0];
  }
}

/**
 * Calibrated pitch for distinct natural voice timbre:
 * Female: 1.05 (clear, articulate, bright)
 * Male: 0.90 (deep, warm, resonant)
 */
export function getPitchForGender(gender) {
  return gender === 'male' ? 0.90 : 1.05;
}
