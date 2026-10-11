# -*- coding: utf-8 -*-
"""
Update interview questions q_0590, q_0591, q_0592 in src/data/interviewQuestions.json
to precisely reflect Subword Tokenization (BPE, WordPiece, SentencePiece).
"""

import json

def update_interview_questions():
    with open('src/data/interviewQuestions.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    for q in data:
        if q.get('id') == 'q_0590':
            q['question'] = "What is Subword Tokenization (BPE, WordPiece, SentencePiece), and why is it essential for modern Large Language Models?"
            q['answer'] = (
                "**Executive Summary:**\n"
                "Subword tokenization is the foundational preprocessing technique that converts raw text into discrete numeric tokens for Large Language Models. Instead of treating every whole word as a separate token, it breaks text into reusable sub-word chunks (roots, prefixes, suffixes, and character n-grams), finding the optimal balance between vocabulary size and sequence length.\n\n"
                "**1. The Whole-Word vs. Character-Level Dilemma:**\n"
                "- **Whole-Word Tokenization Fails:** Storing every possible word requires a massive vocabulary (millions of parameters) and completely fails when encountering new words, names, slang, or typos, throwing catastrophic Out-Of-Vocabulary (`[UNK]`) errors.\n"
                "- **Character-Level Tokenization Fails:** Breaking text into individual letters avoids unknown words, but makes input sequences 4x to 6x longer. Because Transformer self-attention complexity scales quadratically with sequence length ($\\mathcal{O}(T^2)$), character-level modeling multiplies attention compute by 16x to 36x.\n"
                "- **The Subword Sweet Spot:** Common words ('learning', 'the') remain single tokens, while rare or novel words ('unhappiness') decompose into familiar modular pieces: `['un', 'happi', 'ness']`. The model never encounters unknown words and maintains manageable sequence lengths.\n\n"
                "**2. Three Dominant Subword Approaches:**\n"
                "- **Byte Pair Encoding (BPE):** Greedily merges the most frequent adjacent character or byte pairs. Powers GPT-4 (tiktoken) and LLaMA.\n"
                "- **WordPiece:** Selects merges that maximize language model likelihood and tokenizes using greedy longest-match-first with `##` continuation markers. Powers BERT.\n"
                "- **SentencePiece:** An end-to-end tokenizer framework that treats raw text as an unsegmented stream, explicitly representing spaces with `_`, supporting both BPE and probabilistic Unigram models. Powers T5, Mistral, and Gemma."
            )
            q['tip'] = "Use the LEGO analogy: whole-word tokenization requires a unique pre-molded plastic toy for every object in the universe; character tokenization provides microscopic atoms; subword tokenization provides modular LEGO bricks."

        elif q.get('id') == 'q_0591':
            q['question'] = "How do BPE, WordPiece, and SentencePiece differ mathematically, and how does BPE construct its vocabulary step-by-step?"
            q['answer'] = (
                "**1. Mathematical Formulations & Objectives:**\n"
                "- **Byte Pair Encoding (BPE):** Merges based purely on statistical co-occurrence frequency:\n"
                "  $$\\text{pair}^* = \\arg\\max_{(u, v)} \\text{Count}(u, v)$$\n"
                "- **WordPiece (BERT):** Merges based on normalized mutual information likelihood ratio:\n"
                "  $$\\text{Score}(u, v) = \\frac{\\text{Count}(u, v)}{\\text{Count}(u) \\times \\text{Count}(v)}$$\n"
                "  WordPiece only merges a pair if the probability of co-occurrence is much higher than individual marginal probabilities.\n"
                "- **SentencePiece Unigram:** Top-down probabilistic language model. Initializes with a large vocabulary and iteratively prunes candidates that minimally impact sequence likelihood via Expectation-Maximization (EM):\n"
                "  $$P(X) = \\prod_{i=1}^M P(x_i), \\quad x^* = \\arg\\max_{x \\in \\mathcal{S}(X)} \\sum_{i=1}^{|x|} \\log P(x_i)$$\n\n"
                "**2. Step-by-Step BPE Vocabulary Construction (Numerical Walkthrough):**\n"
                "Given toy corpus: `'low'` (freq 2), `'lower'` (freq 1), `'lowest'` (freq 1):\n"
                "- **Initial Symbols:** `{'l', 'o', 'w', 'e', 'r', 's', 't', '</w>'}`\n"
                "- **Iteration 1:** Adjacent pair `('l', 'o')` appears 4 times (highest frequency). Merge to `'lo'`. Corpus becomes: `lo w </w>` (2), `lo w e r </w>` (1), `lo w e s t </w>` (1).\n"
                "- **Iteration 2:** Pair `('lo', 'w')` appears 4 times. Merge to `'low'`. Corpus becomes: `low </w>` (2), `low e r </w>` (1), `low e s t </w>` (1).\n"
                "- **Iteration 3:** Pair `('low', '</w>')` appears 2 times. Merge to `'low</w>'`. The common word `'low'` is now a single token!\n\n"
                "**3. Inference Decoding Mechanisms:**\n"
                "- **BPE:** Deterministically applies learned merge rules in the exact chronological order they were discovered.\n"
                "- **WordPiece:** Evaluates candidate prefixes via greedy longest-match-first, adding `##` for subwords continuing an ongoing word (`playing` $\\to$ `play` + `##ing`).\n"
                "- **SentencePiece:** Preserves whitespace using meta-symbol `_` (`_I _love _NLP`), allowing exact, lossless detokenization without language-specific pre-tokenization."
            )
            q['tip'] = "Walk through the BPE merge progression: ('l', 'o') -> 'lo', then ('lo', 'w') -> 'low', contrasting it with WordPiece's likelihood ratio and SentencePiece's whitespace preservation."

        elif q.get('id') == 'q_0592':
            q['question'] = "How does subword tokenization affect LLM performance, attention complexity, and multilingual serving in production systems?"
            q['answer'] = (
                "**1. Sequence Length vs. Quadratic Attention Complexity:**\n"
                "In Transformer architectures, self-attention scales quadratically with sequence length: $\\mathcal{O}(T^2 \\cdot d_{\\text{model}})$. Subword compression directly controls runtime compute:\n"
                "- A 20-word sentence produces $\\approx 25$ tokens under subword tokenization vs. $\\approx 100$ tokens under character tokenization.\n"
                "- Because $100^2 / 25^2 = 16$, subword tokenization reduces attention memory footprint and compute FLOPs by **16x**, enabling 128k+ token context windows.\n\n"
                "**2. Vocabulary Size ($V$) vs. Parameter Footprint Trade-off:**\n"
                "Expanding vocabulary size $V$ represents more words as single tokens, speeding up inference. However, each token adds a row to the input embedding matrix and output unembedding head:\n"
                "$$\\text{Params}_{\\text{embed}} = 2 \\times V \\times d_{\\text{model}}$$\n"
                "In a model with $d_{\\text{model}} = 4096$, expanding $V$ from 32,000 (LLaMA-1) to 128,256 (LLaMA-3) adds **788 million parameters** purely in embedding lookup tables.\n\n"
                "**3. Byte-Level BPE (BBPE) & Zero-OOV Guarantee:**\n"
                "Modern LLMs (GPT-4 via `tiktoken`, LLaMA) initialize their base vocabulary using the 256 distinct 8-bit byte values ($0\\text{x}00$ to $0\\text{xFF}$) of UTF-8. Because all unicode strings, emojis, source code, and binary artifacts decompose into bytes, Byte-Level BPE completely eliminates `[UNK]` tokens.\n\n"
                "**4. The Multilingual Tokenizer Tax & Production Monitoring:**\n"
                "- **The Tokenizer Tax:** Tokenizers trained predominantly on English corpora fragment non-English languages (Hindi, Arabic, Japanese) into 2x to 5x more subwords. This effectively shrinks their context window and inflates API inference costs.\n"
                "- **Production Monitoring:** Track token-to-word ratios, p95/p99 token sequence lengths, and out-of-distribution byte fallback rates to detect tokenizer drift and optimize KV cache memory allocations."
            )
            q['tip'] = "Frame the engineering trade-off across three vectors: quadratic attention compute O(T^2), embedding parameter footprint (2 * V * d_model), and the multilingual tokenizer tax."

    with open('src/data/interviewQuestions.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')
    print("Updated src/data/interviewQuestions.json successfully!")

if __name__ == '__main__':
    update_interview_questions()
