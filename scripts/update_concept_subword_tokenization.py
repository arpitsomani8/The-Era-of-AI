# -*- coding: utf-8 -*-
"""
Script to modernize tokenizers-bpe-wordpiece-sentencepiece in
src/data/concepts.json and scripts/data_sources/all_concepts.json.
"""

import json

new_concept = {
    "id": "tokenizers-bpe-wordpiece-sentencepiece",
    "topic_id": "genai_embed",
    "topic_label": "Tokenization & Vector Embeddings",
    "category": "genai",
    "category_label": "Generative AI & LLMs",
    "title": "Subword Tokenization (BPE, WordPiece, SentencePiece)",
    "raw_subtopic": "Subword Tokenization (BPE, WordPiece, SentencePiece)",
    "raw_sub": "Tokenizers (Byte-Pair Encoding BPE, WordPiece, SentencePiece)",
    "def": "Subword tokenization is a foundational Natural Language Processing technique that decomposes text into reusable sub-word fragments (prefixes, roots, suffixes, or character n-grams), finding the optimal Pareto frontier between whole-word vocabulary explosion and character-level sequence length dilation while eliminating Out-Of-Vocabulary (OOV) tokens.",
    "definition": "Subword tokenization is the universal text preprocessing paradigm powering modern Large Language Models and Transformer architectures (including GPT-4, BERT, T5, and LLaMA). A language model cannot ingest raw unicode strings directly; text must first be partitioned into a sequence of discrete symbolic tokens, which are then mapped to integer token IDs and looked up in a continuous embedding table E in R^{V x d_model}. Classical whole-word tokenizers suffer from two crippling flaws: (1) combinatorial vocabulary explosion, requiring millions of parameters to store rare words, and (2) complete failure on unseen words, producing Out-Of-Vocabulary ([UNK]) tokens for novel names, typos, or morphological variants (e.g., play vs. playing vs. replaying). Character-level tokenizers eliminate OOV tokens but dilate sequences by 4x to 6x, causing prohibitive quadratic compute and memory bloat in transformer self-attention O(T^2). Subword tokenization resolves this tension by learning a vocabulary of high-frequency words as whole tokens while systematically breaking rare or complex words into frequent subword components (e.g., 'unhappiness' -> 'un' + 'happi' + 'ness'). The three dominant subword methodologies are: (1) Byte Pair Encoding (BPE; Sennrich et al., 2016), which begins with base characters or bytes and iteratively executes greedy statistical merges of the most frequent adjacent symbol pairs; (2) WordPiece (Schuster & Nakajima, 2012; Devlin et al., 2018), which selects merges using a likelihood-oriented mutual information score and tokenizes via greedy longest-match-first with continuation markers (##); and (3) SentencePiece (Kudo & Richardson, 2018), an end-to-end tokenizer framework that treats raw text as an unsegmented stream, explicitly preserving whitespace using the meta-symbol _, supporting both merge-based BPE and probabilistic Unigram language modeling with subword regularization.",
    "simple_summary": "Think of tokenization like building toys with LEGO blocks. If you used whole-word tokenization, your toy factory would need a pre-molded, solid plastic piece for every single object in the universe: a mold for 'car', 'flying-car', 'red-car', and 'car-rental'. The moment someone invents a 'cyber-car', your factory crashes because you have no mold (an Out-Of-Vocabulary error), and your warehouse needs millions of molds. If you used character-level tokenization, you'd only have microscopic plastic atoms: building a simple word requires hundreds of steps, making the instruction manual so long that the model's memory blows up. Subword tokenization is the LEGO sweet spot: common objects like 'car' or 'learning' have their own pre-built blocks, while novel or rare words like 'unhappiness' are snapped together from standard modular pieces: [un] + [happi] + [ness]. The model never crashes on new words, keeps its vocabulary to a neat 32,000 to 100,000 pieces, and keeps sentences short enough for transformer attention to process efficiently.",
    "definition_bullets": [
        "The Subword Sweet Spot: Balances bounded vocabulary size V in [32k, 128k] against manageable sequence length T, avoiding both whole-word OOV failures and character-level quadratic attention bloat.",
        "Byte Pair Encoding (BPE): Iteratively merges the most frequent adjacent character/byte pairs argmax Count(uv) into compact tokens; powers GPT-4 (tiktoken) and LLaMA.",
        "WordPiece: Learns subwords by maximizing language model likelihood Score(u, v) = freq(uv) / (freq(u) * freq(v)) and decodes via greedy longest-match-first with ## continuation markers; powers BERT.",
        "SentencePiece Framework: Operates directly on raw untokenized text with visible whitespace marker _, supporting both merge-based BPE and probabilistic Unigram models for multilingual LLMs.",
        "Byte-Level Zero-OOV Guarantee: Byte-level tokenizers initialize from 256 base byte values, enabling encoding of any arbitrary UTF-8 string, code, or emoji without [UNK] tokens."
    ],
    "core_terms": [
        {
            "term": "Byte Pair Encoding (BPE)",
            "what_is_it": "A frequency-based iterative merging algorithm that builds a subword vocabulary from the bottom up.",
            "definition": "An algorithm originally devised for data compression (Gage, 1994) and adapted for NLP by Sennrich et al. (2016). Starting from base characters or bytes, it iteratively counts adjacent symbol pairs and replaces the most frequent pair with a newly created composite token until reaching a target vocabulary size V.",
            "analogy": "A stenographer who notices that 'th' appears constantly, creates a single custom key for 'th', then later creates a key for 'the', and finally 'there', compressing common keystrokes while keeping letters available for rare words.",
            "why_it_matters": "The standard tokenization engine for OpenAI GPT models (GPT-2 through GPT-4o via tiktoken), RoBERTa, and Meta LLaMA architectures."
        },
        {
            "term": "WordPiece & ## Continuation Prefix",
            "what_is_it": "The subword algorithm developed by Google that uses a likelihood objective and continuation markers for subwords.",
            "definition": "A subword algorithm (Schuster & Nakajima, 2012) that evaluates candidate pair merges using a normalized likelihood score: Score(u, v) = Count(uv) / (Count(u) * Count(v)). At inference time, it applies greedy longest-match-first tokenization and prepends '##' to any subword that continues an ongoing word (e.g., 'playing' -> 'play' + '##ing').",
            "analogy": "A jigsaw puzzle where pieces designed to attach in the middle of a picture have special interlocking tabs (##) indicating they cannot start on the border.",
            "why_it_matters": "The foundational tokenizer for Google BERT and related bidirectional encoder models, ensuring seamless tracking of word-piece boundaries."
        },
        {
            "term": "SentencePiece & Whitespace Meta-Symbol (_)",
            "what_is_it": "A language-agnostic tokenization library that treats sentences as raw character streams with explicit whitespace markers.",
            "definition": "An open-source tokenizer framework (Kudo & Richardson, 2018) that eschews language-specific rule-based pre-tokenization. It treats input text as a continuous raw stream where whitespace is encoded as a visible meta-symbol (typically U+2581 '_'), enabling completely reversible, lossless detokenization without heuristics.",
            "analogy": "A carpenter who marks cut lines with a visible pencil mark (_) so the pieces can be glued back together into the exact original board without guessing where the gaps were.",
            "why_it_matters": "Crucial for multilingual language models (T5, ALBERT, LLaMA, Mistral, Gemma) where non-segmented languages like Chinese, Japanese, or Thai lack whitespace boundaries."
        },
        {
            "term": "Unigram Subword Model & Subword Regularization",
            "what_is_it": "A top-down probabilistic subword model that treats tokenization as an optimal path search and supports data augmentation.",
            "definition": "A subword model (Kudo, 2018) that initializes with a massive candidate vocabulary and iteratively prunes tokens that minimally reduce corpus likelihood using Expectation-Maximization (EM). At inference, it finds the optimal segmentation using the Viterbi algorithm, or samples stochastically from multiple segmentations (Subword Regularization) during training.",
            "analogy": "A sculptor who starts with a giant block of marble and chips away the least important fragments until an optimal statue remains.",
            "why_it_matters": "Subword regularization trains models to be robust to noisy text, typos, and alternative morphological segmentations, significantly improving machine translation and ASR."
        },
        {
            "term": "Byte-Level BPE (BBPE)",
            "what_is_it": "A BPE variant whose base symbol inventory consists of the 256 possible bytes rather than unicode characters.",
            "definition": "An implementation of BPE (Radford et al., 2019) that operates directly on the UTF-8 byte representation of text. Because all unicode text decomposes into combinations of 256 base bytes, the vocabulary has zero Out-Of-Vocabulary (OOV) tokens, allowing models to process arbitrary languages, binary code, and emojis without [UNK].",
            "analogy": "Using the 256 fundamental color codes of digital displays to draw any image on earth, rather than needing an individual physical paint tube for every hue.",
            "why_it_matters": "Completely eliminates the [UNK] token from modern LLMs, allowing models to handle code, mathematical symbols, foreign scripts, and binary artifacts gracefully."
        },
        {
            "term": "Tokenizer Tax & Multilingual Inflation",
            "what_is_it": "The phenomenon where non-English languages are split into significantly more tokens for the same semantic content.",
            "definition": "A structural disparity caused by training tokenizers predominantly on English text. Non-English languages (such as Hindi, Arabic, Japanese, or Burmese) are fragmented into 2x to 5x more subwords per concept, effectively shrinking their available context window and inflating API inference costs.",
            "analogy": "An international shipping service charging 4x higher box fees for non-English packages because its conveyor belts were only calibrated for standard English parcel sizes.",
            "why_it_matters": "A critical fairness and efficiency consideration in global AI systems, driving modern models (e.g., LLaMA-3, Gemma-2) to expand vocabularies from 32k to 128k+ tokens."
        }
    ],
    "symbol_guide": [
        {
            "symbol": "V",
            "name": "Vocabulary Size",
            "meaning": "The total number of unique discrete subword tokens recognized by the model (typically 32,000 in LLaMA-1/2 up to 128,256 in LLaMA-3 and 100,000 in GPT-4).",
            "plain_english": "The total size of the dictionary of word pieces that the AI knows."
        },
        {
            "symbol": "Count(u, v)",
            "name": "Adjacent Pair Frequency",
            "meaning": "The total co-occurrence count of adjacent subword tokens u and v across the tokenization training corpus.",
            "plain_english": "How many times two symbols appear right next to each other in the text."
        },
        {
            "symbol": "Score_WordPiece(u, v)",
            "name": "WordPiece Likelihood Ratio",
            "meaning": "The mutual information merge score Count(uv) / (Count(u) * Count(v)) used to pick candidates in WordPiece.",
            "plain_english": "The formula that checks if two pieces appear together much more often than expected by chance."
        },
        {
            "symbol": "##",
            "name": "WordPiece Continuation Marker",
            "meaning": "Prefix attached to subword tokens indicating that the piece continues a previously started word rather than beginning a new one.",
            "plain_english": "A label meaning 'this piece attaches to the middle or end of the current word'."
        },
        {
            "symbol": "_ (U+2581)",
            "name": "SentencePiece Whitespace Symbol",
            "meaning": "The unicode lower one-eighth block meta-symbol explicitly representing a preceding space in raw text streams.",
            "plain_english": "A visible symbol that marks where an ordinary space belongs between words."
        },
        {
            "symbol": "E in R^{V x d_model}",
            "name": "Token Embedding Matrix",
            "meaning": "The learnable weight matrix mapping each discrete token ID to a dense d_model-dimensional continuous vector.",
            "plain_english": "The lookup table that turns integer token IDs into dense mathematical vectors."
        },
        {
            "symbol": "input_ids / attention_mask",
            "name": "Tokenizer Output Tensors",
            "meaning": "input_ids contains the integer indices of tokens; attention_mask contains 1s for real tokens and 0s for padding.",
            "plain_english": "The two primary arrays passed directly to a transformer model for forward execution."
        }
    ],
    "formula": "$$\\text{BPE Merge Selection Rule: } \\text{pair}^* = \\arg\\max_{(u, v)} \\text{Count}(u, v)$$\n\n$$\\text{WordPiece Mutual Information Score: } \\text{Score}(u, v) = \\frac{\\text{Count}(u, v)}{\\text{Count}(u) \\times \\text{Count}(v)}$$\n\n$$\\text{Unigram Sequence Probability: } P(X) = \\prod_{i=1}^M P(x_i), \\quad x^* = \\arg\\max_{x \\in \\mathcal{S}(X)} \\sum_{i=1}^{|x|} \\log P(x_i)$$\n\n$$\\text{Transformer Self-Attention Complexity: } \\text{FLOPs} \\approx 4 T^2 d_{\\text{model}} + 2 T d_{\\text{model}}^2, \\quad T = \\text{Number of Tokens}$$\n\n$$\\text{Embedding Parameter Footprint: } \\text{Params}_{\\text{embed}} = V \\times d_{\\text{model}}$$\n\n$$\\text{Lossless Detokenization: } \\text{detokenize}(\\text{tokenize}(S)) \\equiv S \\quad (\\text{enabled by } \\text{\\textvisiblespace} \\text{ preservation})$$",
    "logic": "Tokenization governs the fundamental interface between human language and neural computation. The choice of tokenization algorithm and vocabulary size directly determines model latency, parameter count, memory footprint, and downstream reasoning fidelity through three core mechanisms:\n\n1. Sequence Length vs. Attention Complexity: In Transformer architectures, standard multi-head self-attention scales quadratically with sequence length T (specifically O(T^2 * d_model)). A sentence of 20 English words produces ~25 tokens under subword tokenization, but ~100 tokens under character tokenization. Because 100^2 / 25^2 = 16, character-level tokenization demands 16x more attention compute and memory bandwidth for the exact same sentence. Subwords provide the optimal compression that keeps sequence length T short enough for deep transformers to scale.\n\n2. Vocabulary Size Trade-off: Increasing vocabulary size V allows more words and common phrases to be represented as single tokens, reducing overall sequence length T and cutting inference latency. However, every token in V requires a dedicated row in the input embedding matrix E in R^{V x d_model} and the final unembedding projection layer. In a 7B parameter model with d_model = 4096, expanding vocabulary from 32,000 to 128,000 adds (128,000 - 32,000) * 4096 * 2 ~= 786 million parameters (over 10% of total model capacity) purely in linear projection weights.\n\n3. The Tokenizer Tax and Morphology: Because BPE merges are driven by statistical corpus frequency, English text achieves high token efficiency (~1.3 tokens per word), whereas languages with non-Latin scripts (Hindi, Japanese, Arabic) or complex agglutinative morphology (Turkish, Finnish) are fragmented into smaller, unnatural byte chunks (often 3 to 6 tokens per word). Furthermore, tokenizers split multi-digit numbers irregularly (e.g. '384' might become ['38', '4'] while '484' becomes ['484']), which directly impairs the mathematical and arithmetic reasoning capacity of LLMs.",
    "example": "Consider the sentence: 'Unhappiness is unusual in international NLP.'\n\n1. BERT (WordPiece, bert-base-uncased, V=30,522):\n   Tokens: ['un', '##ha', '##ppiness', 'is', 'unusual', 'in', 'international', 'nl', '##p', '.']\n   Token IDs: [4895, 8740, 26978, 2003, 5156, 1999, 2244, 17953, 2365, 1012]\n   Notice the '##' continuation marker on '##ha', '##ppiness', and '##p'.\n\n2. Google T5 (SentencePiece Unigram, t5-small, V=32,100):\n   Tokens: ['_Un', 'happiness', '_is', '_unusual', '_in', '_international', '_N', 'LP', '.']\n   Notice the leading '_' symbol explicitly preserving space boundaries before words.\n\n3. GPT-4 (Byte-Level BPE, tiktoken cl100k_base, V=100,000):\n   Tokens: ['Unh', 'appiness', ' is', ' unusual', ' in', ' international', ' NLP', '.']\n   Notice leading spaces are captured inside tokens (e.g. ' is', ' unusual'), and common words like 'international' and 'NLP' are single tokens.",
    "numerical_example": "Step 1: Worked BPE Merge Walkthrough on a Tiny Corpus\nCorpus: 'low', 'lower', 'lowest', 'low'\nWord Frequencies:\n  'low': 2\n  'lower': 1\n  'lowest': 1\n\nInitial Base Vocabulary (Individual characters + end-of-word marker </w>):\n  V = {'l', 'o', 'w', 'e', 'r', 's', 't', '</w>'}\n\nSplit Words into Initial Tokens:\n  'l o w </w>'     (frequency 2)\n  'l o w e r </w>' (frequency 1)\n  'l o w e s t </w>' (frequency 1)\n\nIteration 1: Count Adjacent Pairs\n  ('l', 'o'): 2 + 1 + 1 = 4 occurrences  <-- HIGHEST FREQUENCY\n  ('o', 'w'): 2 + 1 + 1 = 4 occurrences  <-- TIE\n  ('w', '</w>'): 2 occurrences\n  ('w', 'e'): 1 + 1 = 2 occurrences\n  ('e', 'r'): 1 occurrence\n  ('e', 's'): 1 occurrence\n\nMerge the top pair ('l', 'o') -> 'lo':\n  New Token Added to Vocabulary: 'lo'\n  Corpus becomes:\n    'lo w </w>'     (freq 2)\n    'lo w e r </w>' (freq 1)\n    'lo w e s t </w>' (freq 1)\n\nIteration 2: Count Adjacent Pairs Again\n  ('lo', 'w'): 2 + 1 + 1 = 4 occurrences  <-- HIGHEST FREQUENCY\nMerge ('lo', 'w') -> 'low':\n  New Token Added to Vocabulary: 'low'\n  Corpus becomes:\n    'low </w>'     (freq 2)\n    'low e r </w>' (freq 1)\n    'low e s t </w>' (freq 1)\n\nIteration 3: Count Adjacent Pairs Again\n  ('low', '</w>'): 2 occurrences  <-- HIGHEST FREQUENCY\n  ('low', 'e'): 1 + 1 = 2 occurrences\nMerge ('low', '</w>') -> 'low</w>':\n  The complete common word 'low' is now a SINGLE token in the vocabulary!\n\nStep 2: Practical Python Inspection of Pretrained Tokenizers (Hugging Face)\n```python\n# Inspect BERT (WordPiece) vs T5 (SentencePiece)\nfrom transformers import AutoTokenizer\n\n# 1. WordPiece Tokenizer (BERT)\nbert_tok = AutoTokenizer.from_pretrained('bert-base-uncased')\ntext = 'Unhappiness is unusual in international NLP.'\nbert_tokens = bert_tok.tokenize(text)\nbert_ids = bert_tok.convert_tokens_to_ids(bert_tokens)\nprint('BERT WordPiece Tokens:', bert_tokens)\n# Output: ['un', '##ha', '##ppiness', 'is', 'unusual', 'in', 'international', 'nl', '##p', '.']\nprint('BERT Token IDs:', bert_ids)\n\n# 2. SentencePiece Tokenizer (T5)\nt5_tok = AutoTokenizer.from_pretrained('google-t5/t5-small')\nt5_tokens = t5_tok.tokenize(text)\nprint('T5 SentencePiece Tokens:', t5_tokens)\n# Output: ['_Un', 'happiness', '_is', '_unusual', '_in', '_international', '_N', 'LP', '.']\n\n# 3. Model-Ready Tensor Encoding\nencoded = bert_tok('I am learning tokenization.', return_tensors='pt')\nprint('input_ids tensor:', encoded['input_ids'])\nprint('attention_mask tensor:', encoded['attention_mask'])\n# input_ids includes [CLS] (101) at start and [SEP] (102) at end!\n```",
    "types_header": "Subword Tokenization Algorithms & Frameworks",
    "types_badge": "NLP & LLM Foundations",
    "quick_types": [
        {
            "type": "Byte Pair Encoding (BPE)",
            "name": "Byte Pair Encoding (BPE)",
            "definition": "Frequency-driven bottom-up pair merging algorithm that starts from characters and iteratively replaces the most frequent adjacent pair. Powers GPT-2, GPT-3, and early transformer models.",
            "description": "Frequency-driven bottom-up pair merging algorithm that starts from characters and iteratively replaces the most frequent adjacent pair. Powers GPT-2, GPT-3, and early transformer models.",
            "looks_like": "['l', 'o', 'w'] -> merge('l', 'o') -> ['lo', 'w'] -> merge('lo', 'w') -> ['low']"
        },
        {
            "type": "Byte-Level BPE (BBPE / tiktoken)",
            "name": "Byte-Level BPE (BBPE / tiktoken)",
            "definition": "Operates directly on the 256 raw UTF-8 byte values rather than unicode characters. Completely eliminates Out-Of-Vocabulary ([UNK]) tokens across arbitrary text, emojis, and binary code. Powers GPT-4 and LLaMA.",
            "description": "Operates directly on the 256 raw UTF-8 byte values rather than unicode characters. Completely eliminates Out-Of-Vocabulary ([UNK]) tokens across arbitrary text, emojis, and binary code. Powers GPT-4 and LLaMA.",
            "looks_like": "UTF-8 bytes [0x41, 0x6e, 0x74, 0x69] -> ['anti'] (zero OOV)"
        },
        {
            "type": "WordPiece",
            "name": "WordPiece",
            "definition": "Selects merges using a normalized likelihood mutual information score Count(uv) / (Count(u)*Count(v)) and tokenizes via greedy longest-match-first with ## continuation prefix. Powers Google BERT.",
            "description": "Selects merges using a normalized likelihood mutual information score Count(uv) / (Count(u)*Count(v)) and tokenizes via greedy longest-match-first with ## continuation prefix. Powers Google BERT.",
            "looks_like": "['playing'] -> ['play', '##ing'], ['player'] -> ['play', '##er']"
        },
        {
            "type": "SentencePiece (BPE & Unigram)",
            "name": "SentencePiece (BPE & Unigram)",
            "definition": "An end-to-end framework treating text as raw byte/character streams with explicit whitespace markers (_). Supports both BPE and probabilistic Unigram modeling with Subword Regularization. Powers T5, LLaMA, Mistral, and Gemma.",
            "description": "An end-to-end framework treating text as raw byte/character streams with explicit whitespace markers (_). Supports both BPE and probabilistic Unigram modeling with Subword Regularization. Powers T5, LLaMA, Mistral, and Gemma.",
            "looks_like": "'I love NLP' -> ['_I', '_love', '_NLP'] (lossless detokenization)"
        }
    ],
    "connected_logic": [
        {
            "title": "The Subword Sweet Spot: Vocabulary Size vs. Attention Complexity",
            "description": "Why subword tokenization is universally adopted over whole-word or character-level representations.",
            "content": "• Whole-word tokenizers require vocabularies of 1M+ words to cover a language, wasting gigabytes on rare word embedding rows, yet still failing on unseen words (producing [UNK] tokens).\n• Character-level tokenizers eliminate OOV tokens but dilate sequence length T by 4x to 6x. Because Transformer self-attention complexity is O(T^2), 4x sequence dilation causes a 16x compute and memory spike.\n• Subword tokenization strikes the optimal balance: common words remain single tokens, rare words decompose into reusable pieces, and vocabulary is bounded to [32k, 128k] tokens.",
            "points": [
                "Whole-word tokenizers require vocabularies of 1M+ words to cover a language, wasting gigabytes on rare word embedding rows, yet still failing on unseen words (producing [UNK] tokens).",
                "Character-level tokenizers eliminate OOV tokens but dilate sequence length T by 4x to 6x. Because Transformer self-attention complexity is O(T^2), 4x sequence dilation causes a 16x compute and memory spike.",
                "Subword tokenization strikes the optimal balance: common words remain single tokens, rare words decompose into reusable pieces, and vocabulary is bounded to [32k, 128k] tokens."
            ]
        },
        {
            "title": "Lossless Detokenization: SentencePiece Whitespace Preservation",
            "description": "How explicit whitespace representation enables exact text reconstruction without language-specific rules.",
            "content": "• Classical tokenizers rely on language-specific pre-tokenization rules (e.g., splitting on spaces or punctuation), which permanently loses exact spacing and fails on languages without spaces (Chinese, Japanese, Thai).\n• SentencePiece replaces whitespace with a visible meta-symbol _ (U+2581) before subword segmenting.\n• As a result, detokenization is a trivial string join followed by replacing _ with space, achieving 100% lossless text reconstruction across all languages.",
            "points": [
                "Classical tokenizers rely on language-specific pre-tokenization rules (e.g., splitting on spaces or punctuation), which permanently loses exact spacing and fails on languages without spaces (Chinese, Japanese, Thai).",
                "SentencePiece replaces whitespace with a visible meta-symbol _ (U+2581) before subword segmenting.",
                "As a result, detokenization is a trivial string join followed by replacing _ with space, achieving 100% lossless text reconstruction across all languages."
            ]
        },
        {
            "title": "Byte-Level BPE: The Mathematical Elimination of OOV Tokens",
            "description": "How base byte initialization guarantees zero unknown tokens for arbitrary unicode and binary inputs.",
            "content": "• Character-level BPE fails when encountering unicode codepoints not present in the training set (e.g. rare emoji, obscure symbols), falling back to [UNK].\n• Byte-Level BPE (BBPE; GPT-2/3/4, LLaMA) initializes its base vocabulary with the 256 distinct 8-bit byte values (0x00 to 0xFF).\n• Because any valid UTF-8 string or binary stream is a sequence of bytes, the tokenizer can represent any arbitrary input with zero unknown tokens.",
            "points": [
                "Character-level BPE fails when encountering unicode codepoints not present in the training set (e.g. rare emoji, obscure symbols), falling back to [UNK].",
                "Byte-Level BPE (BBPE; GPT-2/3/4, LLaMA) initializes its base vocabulary with the 256 distinct 8-bit byte values (0x00 to 0xFF).",
                "Because any valid UTF-8 string or binary stream is a sequence of bytes, the tokenizer can represent any arbitrary input with zero unknown tokens."
            ]
        },
        {
            "title": "The Multilingual Tokenizer Tax & Arithmetic Token Glitches",
            "description": "How statistical subword tokenizers create disparities in language processing and mathematical reasoning.",
            "content": "• Multilingual Tokenizer Tax: Tokenizers trained predominantly on English corpora allocate few subwords to non-English languages; a sentence in Hindi or Burmese requires 3x to 5x more tokens, shrinking effective context windows and increasing API latency and billing costs.\n• Arithmetic Token Fragmentation: Numbers are often split irregularly (e.g. '1234' -> ['12', '34'], but '1235' -> ['1', '235']), depriving transformers of consistent positional digit representations and degrading mathematical reasoning.\n• Modern architectures combat this by expanding vocabularies to 128k+ tokens and using regex digit splitting (e.g. splitting every digit into its own token).",
            "points": [
                "Multilingual Tokenizer Tax: Tokenizers trained predominantly on English corpora allocate few subwords to non-English languages; a sentence in Hindi or Burmese requires 3x to 5x more tokens, shrinking effective context windows and increasing API latency and billing costs.",
                "Arithmetic Token Fragmentation: Numbers are often split irregularly (e.g. '1234' -> ['12', '34'], but '1235' -> ['1', '235']), depriving transformers of consistent positional digit representations and degrading mathematical reasoning.",
                "Modern architectures combat this by expanding vocabularies to 128k+ tokens and using regex digit splitting (e.g. splitting every digit into its own token)."
            ]
        }
    ],
    "pitfalls": [
        "Assuming One Word Equals One Token: Words can break into multiple subwords; context window limits, pricing, and throughput depend entirely on token count, not word count.",
        "Assuming BPE Merges Always Follow Linguistic Morphemes: BPE optimizes purely for corpus frequency; it often creates arbitrary fragments that do not match grammatical stems or roots.",
        "Confusing SentencePiece with a Single Tokenization Algorithm: SentencePiece is a C++ library and training framework supporting both BPE and Unigram segmentation models.",
        "Assuming Continuation Markers Are Standard: ## is specific to WordPiece; SentencePiece uses _, and Byte-Level BPE uses raw byte characters like Ġ.",
        "Ignoring Special Tokens in Sequence Length Calculations: Transformers prepend and append special tokens ([CLS], [SEP], <s>, </s>, <|endoftext|>) that consume context budget and change output shapes.",
        "Evaluating Models by Word Count Instead of Token Count: Because different tokenizers segment languages at drastically different token ratios, benchmarks must compare per-token metrics.",
        "Assuming an Unknown Token [UNK] Always Exists: Byte-level tokenizers (GPT-4, LLaMA) represent all 256 byte values, entirely eliminating the need for [UNK] on UTF-8 text."
    ],
    "key_takeaways": [
        "Subword tokenization strikes the optimal balance between whole-word vocabulary explosion and character-level sequence dilation, bounding vocabulary to [32k, 128k] tokens.",
        "BPE builds vocabulary bottom-up via frequency merges; WordPiece uses a likelihood mutual information score; SentencePiece operates directly on raw text preserving whitespace with _.",
        "Byte-Level BPE initializes with all 256 byte values, mathematically eliminating Out-Of-Vocabulary ([UNK]) tokens for any valid UTF-8 string or code.",
        "Subword design directly impacts LLM performance: tokenization efficiency governs context window consumption, transformer quadratic attention cost, and multilingual fairness."
    ],
    "tags": [
        "Tokenization",
        "BPE",
        "WordPiece",
        "SentencePiece",
        "NLP",
        "LLMs",
        "Byte-Level BPE",
        "Transformers",
        "tiktoken",
        "Hugging Face",
        "Generative AI & LLMs"
    ]
}

def update_concepts_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        concepts = json.load(f)
    found = False
    for i, c in enumerate(concepts):
        if c.get('id') == new_concept['id']:
            concepts[i] = new_concept
            found = True
            break
    if not found:
        concepts.append(new_concept)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(concepts, f, indent=2, ensure_ascii=False)
        f.write('\n')
    print(f"Updated {filepath} successfully (found={found}, total={len(concepts)})")

if __name__ == '__main__':
    update_concepts_file('src/data/concepts.json')
    update_concepts_file('scripts/data_sources/all_concepts.json')
