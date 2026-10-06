# scripts/curriculum_part_audio.py
# 5 Audio & Speech AI Concepts

def get_audio_concepts():
    topic_id = "genai_audio_speech"
    topic_label = "Audio, Speech AI & Voice Intelligence"
    cat = "genai"
    cat_label = "Transformers & Generative AI"

    return [
        {
            "id": "concept_audio_preprocessing_spectrograms",
            "title": "Audio Preprocessing: Mel-Spectrograms, STFT & Waveforms",
            "topic_id": topic_id, "topic_label": topic_label, "category": cat, "category_label": cat_label,
            "raw_subtopic": "Audio Preprocessing: Mel-Spectrograms, STFT & Waveforms", "raw_sub": "Audio Preprocessing: Mel-Spectrograms, STFT & Waveforms",
            "def": "The signal processing pipeline transforming continuous 1D acoustic pressure waveforms into 2D time-frequency visual representations via Short-Time Fourier Transforms (STFT) warped across the perceptual logarithmic Mel scale.",
            "definition": "The signal processing pipeline transforming continuous 1D acoustic pressure waveforms into 2D time-frequency visual representations via Short-Time Fourier Transforms (STFT) warped across the perceptual logarithmic Mel scale.",
            "formula": "$$X(\\tau, \\omega) = \\sum_{n=-\\infty}^{\\infty} x[n] w[n-\\tau] e^{-j \\omega n}, \\quad m = 2595 \\log_{10}\\left(1 + \\frac{f}{700}\\right), \\quad S_{\\text{Mel}} = \\log\\left( |X(\\tau, \\omega)|^2 M^T + \\epsilon \\right)$$",
            "formula_explanation": "",
            "logic": "Human hearing does not perceive pitch linearly: we are exquisitely sensitive to pitch changes at low frequencies (200-2,000 Hz) and insensitive at high frequencies (10,000+ Hz). The Mel scale warps raw Hertz into triangular filterbanks mimicking the cochlea, turning 1D audio into 2D image-like tensors that CNNs and Vision Transformers can process.",
            "core_logic": "Human hearing does not perceive pitch linearly: we are exquisitely sensitive to pitch changes at low frequencies (200-2,000 Hz) and insensitive at high frequencies (10,000+ Hz). The Mel scale warps raw Hertz into triangular filterbanks mimicking the cochlea, turning 1D audio into 2D image-like tensors that CNNs and Vision Transformers can process.",
            "architectural_logic": "",
            "example": "OpenAI Whisper audio input: Audio sampled at 16,000 Hz is chunked into 30-second windows (480,000 samples) and converted into an 80-channel log-Mel spectrogram (80 x 3000 matrix) fed directly into the Transformer encoder.",
            "tags": ["Audio AI", "STFT", "Mel-Spectrogram", "Signal Processing"],
            "simple_summary": "Sound starts as a wiggly line of air pressure. Audio preprocessing uses math (Fourier Transform) to break that wiggle into musical notes over time, creating a colorful heat-map picture called a Mel-spectrogram that neural networks can look at like an image.",
            "core_terms": [
                {
                    "term": "Sampling Rate (Hz)",
                    "what_is_it": "The number of discrete audio amplitude measurements recorded per second (e.g. 16,000 Hz for voice, 44,100 Hz for CD audio).",
                    "analogy": "The frame rate of a video camera: 16k snapshots per second captures human speech clearly.",
                    "why_it_matters": "Determines the highest audible frequency according to the Nyquist theorem (Max Freq = Sample Rate / 2)."
                },
                {
                    "term": "Short-Time Fourier Transform (STFT)",
                    "what_is_it": "Sliding a small window (e.g. 25ms window every 10ms hop) along the waveform to calculate the frequency spectrum over time.",
                    "analogy": "Reading sheet music measure by measure to see which chords are playing at each second.",
                    "why_it_matters": "Preserves both timing and pitch simultaneously."
                },
                {
                    "term": "Mel Scale Filterbanks",
                    "what_is_it": "A set of overlapping triangular bandpass filters that compresses higher frequencies logarithmically to match human ear perception.",
                    "analogy": "A piano keyboard where low keys are wide apart and high treble keys are squeezed close together.",
                    "why_it_matters": "Reduces dimensionality from 1,024 FFT bins down to 80 or 128 perceptually rich Mel channels."
                },
                {
                    "term": "Hop Length & Window Length",
                    "what_is_it": "Window length is the duration of audio evaluated per FFT slice; hop length is the distance the window steps forward.",
                    "analogy": "Taking overlapping photos as you pan a panorama camera across a landscape.",
                    "why_it_matters": "Governs the time-versus-frequency resolution tradeoff (Heisenberg-Gabor limit)."
                }
            ],
            "symbol_guide": [
                {"symbol": "x[n]", "meaning": "Raw discrete 1D audio sample array", "plain_english": "The amplitude numbers in the sound file"},
                {"symbol": "w[n]", "meaning": "Windowing function (e.g. Hann window)", "plain_english": "Smooths window edges to avoid spectral leakage artifacts"},
                {"symbol": "S_{\\text{Mel}}", "meaning": "Log-compressed Mel-frequency spectrogram", "plain_english": "The 2D heatmap matrix passed to neural network"}
            ],
            "numerical_example": "1 second of speech at 16,000 Hz = 16,000 samples. Window = 400 samples (25ms), Hop = 160 samples (10ms). Number of time frames = 16,000 / 160 = 100 frames. Applying 80 Mel filters produces a clean 2D tensor of shape [80 Mel bins, 100 time frames] in under 1ms on GPU.",
            "pitfalls": "Novice Trap: Inconsistent sample rates during inference! If your model was trained on 16kHz audio and you pass 44.1kHz audio without resampling, the pitch will shift up drastically (sounding like chipmunks) and word error rate will soar to 100%.",
            "key_takeaways": [],
            "definition_bullets": [
                "Sampling Rate: Frequency of digital audio measurement governed by the Nyquist limit.",
                "STFT: Converting 1D time-domain signals into 2D time-frequency energy distributions.",
                "Mel Scale: Biological frequency warping matching human auditory resolution.",
                "Log Compression: Dynamic range normalization preventing loud sounds from drowning out whispers."
            ]
        },
        {
            "id": "concept_asr_whisper_architecture",
            "title": "Automatic Speech Recognition (ASR & Whisper Architecture)",
            "topic_id": topic_id, "topic_label": topic_label, "category": cat, "category_label": cat_label,
            "raw_subtopic": "Automatic Speech Recognition (ASR & Whisper Architecture)", "raw_sub": "Automatic Speech Recognition (ASR & Whisper Architecture)",
            "def": "The deep sequence-to-sequence encoder-decoder architecture (OpenAI Whisper) trained on 680,000+ hours of weakly supervised multilingual audio that jointly performs speech recognition, language identification, phrase timestamping, and translation.",
            "definition": "The deep sequence-to-sequence encoder-decoder architecture (OpenAI Whisper) trained on 680,000+ hours of weakly supervised multilingual audio that jointly performs speech recognition, language identification, phrase timestamping, and translation.",
            "formula": "$$P(Y|X) = \\prod_{i=1}^U P(y_i | y_{<i}, \\text{Encoder}(S_{\\text{Mel}})), \\quad \\text{Prompt}: [\\text{<|startoftranscript|>}, \\text{<|en|>}, \\text{<|transcribe|>}, \\text{<|notimestamps|>}]$$",
            "formula_explanation": "",
            "logic": "Previous ASR required separate acoustic models, pronunciation lexicons, language models, and CTC alignment layers. Whisper unifies everything into a single standard Transformer encoder-decoder that treats speech transcription as a sequence-to-sequence translation task from acoustic spectrogram patches to BPE text tokens.",
            "core_logic": "Previous ASR required separate acoustic models, pronunciation lexicons, language models, and CTC alignment layers. Whisper unifies everything into a single standard Transformer encoder-decoder that treats speech transcription as a sequence-to-sequence translation task from acoustic spectrogram patches to BPE text tokens.",
            "architectural_logic": "",
            "example": "Multilingual podcast transcription: Ingesting an accented audio interview in Spanish, auto-detecting `<|es|>`, and producing both native Spanish subtitles and translated English text with word-level timestamps in a single pass.",
            "tags": ["ASR", "Whisper", "Speech-to-Text", "Multilingual"],
            "simple_summary": "Whisper is an end-to-end AI listener: it takes a picture of the audio (spectrogram), feeds it through an encoder to understand the sounds, and uses a decoder to type out the words in English or 98 other languages with timestamps.",
            "core_terms": [
                {
                    "term": "Audio Transformer Encoder",
                    "what_is_it": "Two 1D convolutional layers with stride 2 that downsample the spectrogram, followed by stacked Transformer encoder blocks.",
                    "analogy": "An attentive ear processing acoustic soundwaves into internal semantic sound thoughts.",
                    "why_it_matters": "Extracts deep phonetic and contextual representations invariant to speaker accent."
                },
                {
                    "term": "Autoregressive Text Decoder",
                    "what_is_it": "A standard causal Transformer decoder that generates subword text tokens conditioned on encoder cross-attention.",
                    "analogy": "A court stenographer listening to the audio and typing out words in order on a keyboard.",
                    "why_it_matters": "Combines speech decoding with a powerful internal language model that auto-corrects homophones based on context."
                },
                {
                    "term": "Special Control Tokens",
                    "what_is_it": "Prompt tokens governing task behavior: <|startoftranscript|>, <|es|>, <|translate|>, <|0.00|>, <|30.00|>.",
                    "analogy": "Setting mode switches on a tape recorder: language, transcription vs translation, and timestamp mode.",
                    "why_it_matters": "Enables multi-task flexibility without changing the network weights."
                },
                {
                    "term": "Word Error Rate (WER)",
                    "what_is_it": "The industry standard evaluation metric: (Substitutions + Deletions + Insertions) / Total Words.",
                    "analogy": "Counting how many typos a typist made out of 100 spoken words.",
                    "why_it_matters": "The primary benchmark for comparing ASR model accuracy."
                }
            ],
            "symbol_guide": [
                {"symbol": "S_{\\text{Mel}}", "meaning": "80-channel log-Mel spectrogram input", "plain_english": "The visual audio spectrogram"},
                {"symbol": "y_i", "meaning": "Decoded BPE text token at position i", "plain_english": "The transcribed word or subword"},
                {"symbol": "\\text{WER}", "meaning": "Word Error Rate metric", "plain_english": "Lower is better (e.g. 5% WER is human parity)"}
            ],
            "numerical_example": "Reference ground truth: 'The quick brown fox jumps'. Whisper prediction: 'The fast brown fox jump'. Edits: 1 Substitution ('quick' -> 'fast') + 1 Substitution ('jumps' -> 'jump'). Total words = 5. WER = (1 + 1) / 5 = 2/5 = 40.0%. If Whisper transcribed 'The quick brown fox jumps', WER = 0.0%.",
            "pitfalls": "Novice Trap: Hallucination during silent or music-only audio segments. Because the decoder is an autoregressive language model, long pauses or background static can cause Whisper to hallucinate repetitive loops (e.g. 'Thank you for watching!'). Setting `condition_on_previous_text=False` and checking compression ratio mitigates this.",
            "key_takeaways": [],
            "definition_bullets": [
                "Unified Architecture: Single encoder-decoder replacing complex multi-stage ASR pipelines.",
                "Weak Supervision Scale: Trained on 680,000 hours of diverse, noisy internet audio.",
                "Multi-Task Tokens: Handles transcription, translation, language ID, and timestamps.",
                "Word Error Rate: Standard evaluation counting substitutions, deletions, and insertions."
            ]
        },
        {
            "id": "concept_ctc_loss_mechanics",
            "title": "CTC (Connectionist Temporal Classification) Loss Mechanics",
            "topic_id": topic_id, "topic_label": topic_label, "category": cat, "category_label": cat_label,
            "raw_subtopic": "CTC (Connectionist Temporal Classification) Loss Mechanics", "raw_sub": "CTC (Connectionist Temporal Classification) Loss Mechanics",
            "def": "An alignment-free objective function for sequence problems where input length exceeds output length (e.g. 1,000 audio frames to 20 text characters), introducing a blank token <epsilon> and collapsing duplicate characters to dynamically marginalize all valid alignments via forward-backward dynamic programming.",
            "definition": "An alignment-free objective function for sequence problems where input length exceeds output length (e.g. 1,000 audio frames to 20 text characters), introducing a blank token <epsilon> and collapsing duplicate characters to dynamically marginalize all valid alignments via forward-backward dynamic programming.",
            "formula": "$$\\mathcal{L}_{\\text{CTC}} = -\\ln \\sum_{\\pi \\in \\mathcal{B}^{-1}(Y)} P(\\pi | X), \\quad \\mathcal{B}(\\text{\"h - e - e - l - - l - o\"}) = \\text{\"hello\"}$$",
            "formula_explanation": "",
            "logic": "Speech has no natural boundary tags: when someone says 'hello', a speaker might draw out the 'e' for 40 frames and the 'l' for 15 frames. CTC solves this without requiring frame-by-frame phonetic timestamps by defining a collapse mapping B that sums probabilities over all paths that simplify to 'hello'.",
            "core_logic": "Speech has no natural boundary tags: when someone says 'hello', a speaker might draw out the 'e' for 40 frames and the 'l' for 15 frames. CTC solves this without requiring frame-by-frame phonetic timestamps by defining a collapse mapping B that sums probabilities over all paths that simplify to 'hello'.",
            "architectural_logic": "",
            "example": "Wav2Vec 2.0 / Conformer real-time transcription: The model outputs predictions at every 20ms audio frame. CTC collapses repeated letters and blank tokens, enabling streaming speech transcription without needing an autoregressive decoder.",
            "tags": ["CTC Loss", "Speech Alignment", "Wav2Vec", "Dynamic Programming"],
            "simple_summary": "In speech, a person might say 'Heeeeellloooo' over 100 frames. CTC loss inserts blank spaces (<blank>) and collapses duplicates so that 'h-e-e-e-l-l-o' automatically turns into the clean word 'hello' without human alignment.",
            "core_terms": [
                {
                    "term": "Blank Token (<epsilon>)",
                    "what_is_it": "A special null character indicating silence or transitions between phonemes.",
                    "analogy": "The space bar or a musical rest between distinct notes.",
                    "why_it_matters": "Distinguishes between deliberate double letters (e.g. 'b-o-o-k' vs a held 'o')."
                },
                {
                    "term": "Collapse Operator B()",
                    "what_is_it": "A function that removes consecutive duplicate characters first, then removes all blank tokens.",
                    "analogy": "An automatic spelling corrector that turns 'c-c-a-a-t-t' into 'cat'.",
                    "why_it_matters": "Allows thousands of different frame-level timing paths to map to the identical text transcript."
                },
                {
                    "term": "Forward-Backward CTC Algorithm",
                    "what_is_it": "A dynamic programming algorithm that efficiently sums probabilities over all valid alignment paths in O(T * |Y|) time.",
                    "analogy": "Finding all paths through a subway network that lead to the final destination without testing every route manually.",
                    "why_it_matters": "Avoids brute-force calculation across an exponential number of possible alignments."
                },
                {
                    "term": "Conditional Independence Assumption",
                    "what_is_it": "CTC assumes predictions at time step t are conditionally independent of step t-1 given the input audio.",
                    "analogy": "Typing letters while looking at audio waveforms without paying attention to the grammar of previous words.",
                    "why_it_matters": "Enables ultra-fast parallel GPU inference, but makes CTC prone to spelling errors without an external language model."
                }
            ],
            "symbol_guide": [
                {"symbol": "\\pi", "meaning": "A frame-level character alignment path", "plain_english": "e.g. ['h', 'h', '-', 'e', 'l', 'l', 'o']"},
                {"symbol": "\\mathcal{B}^{-1}(Y)", "meaning": "Set of all valid paths collapsing to label Y", "plain_english": "All legal ways to spell target text Y"},
                {"symbol": "P(\\pi|X)", "meaning": "Probability of path pi given input audio X", "plain_english": "Product of frame-level softmax outputs"}
            ],
            "numerical_example": "Target word: 'HI'. Audio length T = 3 frames. Possible valid paths that collapse to 'HI': ['H', 'I', '-'], ['H', '-', 'I'], ['-', 'H', 'I'], ['H', 'H', 'I'], ['H', 'I', 'I']. CTC computes the sum of probabilities across these 5 paths. If their sum is 0.85, CTC loss = -ln(0.85) = 0.162.",
            "pitfalls": "Novice Trap: Forgetting how CTC handles repeated letters! 'HELLO' requires a blank token between the two 'l's (e.g. 'l - l'). If there is no blank token, 'l l' collapses to a single 'l', transcribing 'HELO' instead of 'HELLO'.",
            "key_takeaways": [],
            "definition_bullets": [
                "Alignment-Free Training: Eliminates requirement for expensive frame-level phonetic labels.",
                "Blank Character: Disambiguates consecutive identical letters from prolonged sounds.",
                "Collapse Mapping: Maps diverse temporal timing trajectories to unique canonical text.",
                "Non-Autoregressive Speed: Emits entire transcript in parallel in a single GPU pass."
            ]
        },
        {
            "id": "concept_tts_neural_synthesizers",
            "title": "Text-to-Speech (TTS) & Neural Audio Synthesizers",
            "topic_id": topic_id, "topic_label": topic_label, "category": cat, "category_label": cat_label,
            "raw_subtopic": "Text-to-Speech (TTS) & Neural Audio Synthesizers", "raw_sub": "Text-to-Speech (TTS) & Neural Audio Synthesizers",
            "def": "The two-stage or end-to-end generative neural architecture that converts text phonemes into natural, expressive human speech, comprising an acoustic model (VITS, FastSpeech 2) and a neural vocoder (HiFi-GAN, WaveGlow) generating high-fidelity raw audio waveforms.",
            "definition": "The two-stage or end-to-end generative neural architecture that converts text phonemes into natural, expressive human speech, comprising an acoustic model (VITS, FastSpeech 2) and a neural vocoder (HiFi-GAN, WaveGlow) generating high-fidelity raw audio waveforms.",
            "formula": "$$\\text{Acoustic}: \\text{Text} \\xrightarrow{\\text{Phonemizer}} \\mathbf{p} \\xrightarrow{\\text{FastSpeech}} S_{\\text{Mel}}, \\quad \\text{Vocoder}: x_{\\text{wave}} = G_{\\text{HiFi}}(S_{\\text{Mel}}), \\quad \\mathcal{L}_{\\text{Adv}} + \\lambda_{\\text{fm}} \\mathcal{L}_{\\text{FM}} + \\lambda_{\\text{mel}} \\mathcal{L}_{\\text{Mel}}$$",
            "formula_explanation": "",
            "logic": "Converting text directly to 44,100 samples/sec waveform is intractable due to long-range coherence issues. Modern TTS decomposes the task: the acoustic model generates intermediate 80-channel Mel spectrograms, and a high-speed neural vocoder (GAN) inverts the spectrogram back into 44.1kHz audio.",
            "core_logic": "Converting text directly to 44,100 samples/sec waveform is intractable due to long-range coherence issues. Modern TTS decomposes the task: the acoustic model generates intermediate 80-channel Mel spectrograms, and a high-speed neural vocoder (GAN) inverts the spectrogram back into 44.1kHz audio.",
            "architectural_logic": "",
            "example": "ElevenLabs / ChatTTS voice cloning: Ingests 5 seconds of sample voice audio, extracts a speaker reference embedding, and synthesizes brand new text with matching timbre, emotional cadence, and natural breathing pauses.",
            "tags": ["TTS", "Neural Vocoder", "HiFi-GAN", "Voice Cloning", "VITS"],
            "simple_summary": "TTS turns text into human speech. First, an acoustic model turns words into phonemes and predicts how long each sound lasts. Then, a neural vocoder (HiFi-GAN) turns that musical picture into real sound waves vibrating your speakers.",
            "core_terms": [
                {
                    "term": "Grapheme-to-Phoneme (G2P)",
                    "what_is_it": "Converting written alphabet letters into phonetic pronunciation symbols (e.g. 'colonel' -> /'kɜrnəl/).",
                    "analogy": "Reading the phonetic pronunciation guide in a physical dictionary.",
                    "why_it_matters": "Resolves silent letters and irregular spelling rules in English and other languages."
                },
                {
                    "term": "Duration & Pitch Predictors",
                    "what_is_it": "Neural sub-modules that predict the exact millisecond length (duration) and melodic pitch contour (F0) for each phoneme.",
                    "analogy": "A conductor marking whether a musical note should be held for a quarter note or whole note, and how high to sing it.",
                    "why_it_matters": "Prevents synthesized voices from sounding like flat, robotic monotone."
                },
                {
                    "term": "Neural Vocoder (HiFi-GAN)",
                    "what_is_it": "A Generative Adversarial Network that inverts 2D Mel-spectrograms into high-fidelity 1D raw audio waveforms (44.1kHz).",
                    "analogy": "An ultra-high-definition audio printer that turns an audio blueprint into actual vibrating air molecules.",
                    "why_it_matters": "Replaces slow autoregressive WaveNet with 100x faster real-time synthesis."
                },
                {
                    "term": "Speaker Conditioning (d-vector)",
                    "what_is_it": "A compact embedding vector representing a speaker's unique vocal tract anatomy, accent, and timbre.",
                    "analogy": "The unique fingerprint or DNA profile of a person's voice.",
                    "why_it_matters": "Enables zero-shot voice cloning from just a few seconds of reference audio."
                }
            ],
            "symbol_guide": [
                {"symbol": "G_{\\text{HiFi}}", "meaning": "HiFi-GAN generator network", "plain_english": "The neural vocoder synthesizing raw audio"},
                {"symbol": "F_0", "meaning": "Fundamental frequency / pitch contour", "plain_english": "The pitch height of the vocal cords"},
                {"symbol": "\\mathcal{L}_{\\text{FM}}", "meaning": "Feature matching discriminator loss", "plain_english": "Ensures acoustic textures sound natural and crisp"}
            ],
            "numerical_example": "Text: 'Hello world'. G2P outputs 8 phonemes. Duration predictor allocates 25 frames (250ms) to 'Hel', 15 frames to 'lo', 30 frames to 'world'. Acoustic model emits [80, 70] Mel spectrogram. HiFi-GAN upsamples 70 frames × 256 stride = 17,920 raw audio samples (1.12 seconds at 16kHz) in 12ms on GPU.",
            "pitfalls": "Novice Trap: Phase mismatch in audio inversion. Standard spectrograms discard phase information. Attempting to use the classic mathematical Griffin-Lim algorithm produces metallic, robotic, buzzy audio; using a pre-trained neural vocoder like HiFi-GAN is essential for human-like naturalness.",
            "key_takeaways": [],
            "definition_bullets": [
                "Two-Stage Pipeline: Acoustic model generates spectrograms; neural vocoder inverts to waveform.",
                "Grapheme-to-Phoneme: Resolves irregular spelling into unambiguous phonetic symbols.",
                "HiFi-GAN Vocoder: Fast multi-period adversarial synthesis producing 44.1kHz audio.",
                "Speaker Conditioning: Enables zero-shot voice cloning via reference voice embeddings."
            ]
        },
        {
            "id": "concept_streaming_voice_agents",
            "title": "Real-Time Streaming Voice Agents & Audio Embeddings",
            "topic_id": topic_id, "topic_label": topic_label, "category": cat, "category_label": cat_label,
            "raw_subtopic": "Real-Time Streaming Voice Agents & Audio Embeddings", "raw_sub": "Real-Time Streaming Voice Agents & Audio Embeddings",
            "def": "The end-to-end full-duplex conversational AI architecture (e.g. OpenAI GPT-4o voice mode, Kyutai Moshi) combining Voice Activity Detection (VAD), chunked streaming ASR, low-latency LLM generation, and streaming TTS with interruptibility and sub-300ms turn-taking latency.",
            "definition": "The end-to-end full-duplex conversational AI architecture (e.g. OpenAI GPT-4o voice mode, Kyutai Moshi) combining Voice Activity Detection (VAD), chunked streaming ASR, low-latency LLM generation, and streaming TTS with interruptibility and sub-300ms turn-taking latency.",
            "formula": "$$\\text{Latency} = T_{\\text{VAD}} (20\\text{ms}) + T_{\\text{ASR\\_stream}} (80\\text{ms}) + T_{\\text{LLM\\_TTFT}} (120\\text{ms}) + T_{\\text{TTS\\_first\\_chunk}} (60\\text{ms}) \\approx 280\\text{ms}$$",
            "formula_explanation": "",
            "logic": "Cascaded audio systems (recording full user audio -> transcribing -> LLM -> generating full MP3 -> playing) take 3-5 seconds, feeling clunky and unnatural. Streaming voice agents operate in full duplex: chunks of audio are streamed over WebSockets, the LLM streams tokens, and TTS begins speaking after the first 3 tokens, enabling human-like interruptible conversations.",
            "core_logic": "Cascaded audio systems (recording full user audio -> transcribing -> LLM -> generating full MP3 -> playing) take 3-5 seconds, feeling clunky and unnatural. Streaming voice agents operate in full duplex: chunks of audio are streamed over WebSockets, the LLM streams tokens, and TTS begins speaking after the first 3 tokens, enabling human-like interruptible conversations.",
            "architectural_logic": "",
            "example": "Customer support phone agent: User interrupts the AI mid-sentence with 'Wait, actually change my booking to Tuesday'. VAD detects user speech in 30ms, immediately cuts off the AI's audio playback, and routes the new intent seamlessly.",
            "tags": ["Voice Agents", "Full Duplex", "VAD", "Streaming AI", "Low Latency"],
            "simple_summary": "Conversational voice agents talk back and forth like real humans on a phone call. Instead of waiting for you to finish your whole paragraph, they stream audio continuously and can be interrupted mid-sentence the moment you speak.",
            "core_terms": [
                {
                    "term": "Voice Activity Detection (VAD)",
                    "what_is_it": "An ultra-fast neural binary classifier (Silero VAD) running every 20ms to detect whether the user is actively speaking or silent.",
                    "analogy": "An automatic microphone mute switch that only unmutes when speech frequencies are detected.",
                    "why_it_matters": "Determines turn-taking boundaries without forcing users to click a 'Done Speaking' button."
                },
                {
                    "term": "Full Duplex Communication",
                    "what_is_it": "Simultaneous two-way audio streaming where both human and AI can send and receive sound at the exact same moment.",
                    "analogy": "A natural telephone call versus a walkie-talkie where only one person can speak at a time ('Over').",
                    "why_it_matters": "Enables natural conversational interruptions and responsive backchanneling ('uh-huh', 'I see')."
                },
                {
                    "term": "Barge-In / Interruptibility",
                    "what_is_it": "The ability of the system to immediately cancel ongoing TTS audio playback and flush LLM generation queues when user speech is detected.",
                    "analogy": "Pausing your speech immediately when someone raises their hand or begins talking in a conversation.",
                    "why_it_matters": "Eliminates annoying scenarios where the AI keeps rambling over the user."
                },
                {
                    "term": "Chunked Streaming TTS",
                    "what_is_it": "Synthesizing audio sentence by sentence or clause by clause as LLM tokens arrive, streaming audio packets to client speakers.",
                    "analogy": "Starting to watch a movie while it downloads, rather than waiting for the entire 2-hour file to finish.",
                    "why_it_matters": "Reduces perceived audio latency from 3,000ms down to sub-300ms."
                }
            ],
            "symbol_guide": [
                {"symbol": "T_{\\text{TTFT}}", "meaning": "Time To First Token", "plain_english": "How fast the LLM produces its first word"},
                {"symbol": "WebSocket / WebRTC", "meaning": "Real-time bidirectional transport protocols", "plain_english": "Low-latency streaming connections over the internet"},
                {"symbol": "VAD Threshold", "meaning": "Probability boundary for active voice (e.g. 0.5)", "plain_english": "Filters out background coughs and keyboard clicks"}
            ],
            "numerical_example": "User finishes speaking at t=0ms. Silero VAD confirms silence at t=25ms. Streaming Whisper transcribes final words at t=90ms. Groq/Llama-3 LLM emits first 4 tokens at t=190ms. Cartesia/ElevenLabs streaming TTS produces first 50ms audio chunk at t=260ms. User hears AI voice in 260ms (well under the 300ms human conversational threshold).",
            "pitfalls": "Novice Trap: Acoustic echo feedback loop! If the AI's own spoken audio playing through the device speaker leaks into the user's microphone, the VAD will think the user is talking and trigger an infinite barge-in interrupt loop. Hardware Acoustic Echo Cancellation (AEC) or software reference masking is required.",
            "key_takeaways": [],
            "definition_bullets": [
                "Full Duplex: Simultaneous two-way streaming enabling natural interruption and turn-taking.",
                "Voice Activity Detection: Continuous millisecond audio monitoring determining speech boundaries.",
                "Barge-In Logic: Instantly halts AI audio output the moment user begins talking.",
                "Sub-300ms Latency Budget: Chaining streaming ASR, low TTFT LLM, and streaming chunked TTS."
            ]
        }
    ]

print("Audio module ready.")
