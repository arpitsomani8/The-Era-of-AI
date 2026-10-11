# -*- coding: utf-8 -*-
"""
Update interview questions q_0593, q_0594, q_0595 in src/data/interviewQuestions.json
to precisely reflect Dense Vector Embeddings & Semantic Geometry.
"""

import json

def update_interview_questions():
    with open('src/data/interviewQuestions.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    for q in data:
        if q.get('id') == 'q_0593':
            q['question'] = "What are Dense Vector Embeddings and Semantic Geometry, and how do they represent meaning intuitively?"
            q['answer'] = (
                "**Executive Summary:**\n"
                "A dense vector embedding is a learned numerical representation of an item (word, sentence, document, or image) as an ordered list of continuous real-valued numbers where most entries are non-zero (typically 384, 768, 1024, or 1536 dimensions). Semantic geometry describes how geometric proximity and directional alignment in that high-dimensional space reflect real-world relationships in meaning.\n\n"
                "**1. Dense Embeddings vs. Sparse Representations:**\n"
                "- **Sparse Representations (One-Hot, TF-IDF, BM25):** High-dimensional vectors where 99.9% of entries are zeros. Distinct words occupy mutually orthogonal axes: 'cardiac arrest' and 'heart attack' share zero overlapping features, producing a dot product of zero despite identical medical meaning.\n"
                "- **Dense Embeddings (Sentence-BERT, text-embedding-3):** Compact vectors where every coordinate carries a learned continuous value. 'I love dogs' and 'I like puppies' point in nearly identical directions, while 'The stock market fell today' points in a completely different direction.\n\n"
                "**2. Intuitive Analogy (GPS Coordinates for Meaning):**\n"
                "Think of an embedding as a GPS coordinate in a 768-dimensional 'map of human concepts'. On this semantic map, synonyms live on the same street, related topics live in the same neighborhood, and unrelated topics live thousands of miles away on separate islands.\n\n"
                "**3. Crucial Geometric Nuance:**\n"
                "- **Similarity is not identical wording:** 'The server is down' and 'The website is unavailable' share zero tokens but have high cosine similarity.\n"
                "- **High word overlap does not guarantee identical meaning:** 'The customer approved the payment' vs. 'The customer did not approve the payment' share 85% of words, but express opposite intent. Good embedding models capture subtle contextual differences through bidirectional transformer attention."
            )
            q['tip'] = "Use the GPS coordinate analogy: embeddings give every text an address on a high-dimensional map of meaning, where directional alignment reflects conceptual similarity."

        elif q.get('id') == 'q_0594':
            q['question'] = "How do Dot Product, Cosine Similarity, and Euclidean Distance differ mathematically, and how do you calculate them step-by-step?"
            q['answer'] = (
                "**1. Mathematical Formulations:**\n"
                "- **Dot Product:** Measures both directional alignment and vector magnitudes:\n"
                "  $$\\mathbf{a} \\cdot \\mathbf{b} = \\sum_{i=1}^d a_i b_i$$\n"
                "- **Cosine Similarity:** Measures the angle $\\theta$ between vectors, completely normalizing for lengths:\n"
                "  $$\\cos(\\theta) = \\frac{\\mathbf{a} \\cdot \\mathbf{b}}{\\|\\mathbf{a}\\|_2 \\|\\mathbf{b}\\|_2} = \\frac{\\sum a_i b_i}{\\sqrt{\\sum a_i^2} \\sqrt{\\sum b_i^2}}$$\n"
                "  Bounded in $[-1, 1]$: $1$ indicates identical direction, $0$ indicates orthogonality (unrelated), and $-1$ indicates opposite direction.\n"
                "- **Euclidean Distance ($L_2$):** Measures straight-line spatial distance:\n"
                "  $$d(\\mathbf{a}, \\mathbf{b}) = \\|\\mathbf{a} - \\mathbf{b}\\|_2 = \\sqrt{\\sum (a_i - b_i)^2}$$\n\n"
                "**2. The Unit Hypersphere Equivalence Proof:**\n"
                "When vectors are $L_2$-normalized to unit length ($\\|\\mathbf{a}\\| = \\|\\mathbf{b}\\| = 1$):\n"
                "$$\\|\\mathbf{a} - \\mathbf{b}\\|^2 = \\|\\mathbf{a}\\|^2 + \\|\\mathbf{b}\\|^2 - 2(\\mathbf{a} \\cdot \\mathbf{b}) = 1 + 1 - 2\\cos(\\theta) = 2 - 2\\cos(\\theta)$$\n"
                "Thus, for normalized embeddings, **dot product equals cosine similarity**, and maximizing cosine similarity is mathematically identical to minimizing Euclidean distance.\n\n"
                "**3. Step-by-Step Worked Numerical Example:**\n"
                "Given $\\mathbf{a} = [1, 2]$ and $\\mathbf{b} = [2, 4]$:\n"
                "- **Dot Product:** $\\mathbf{a} \\cdot \\mathbf{b} = (1 \\times 2) + (2 \\times 4) = 2 + 8 = 10.0$\n"
                "- **Magnitudes:** $\\|\\mathbf{a}\\| = \\sqrt{1^2 + 2^2} = \\sqrt{5} \\approx 2.236$; $\\|\\mathbf{b}\\| = \\sqrt{2^2 + 4^2} = \\sqrt{20} = 2\\sqrt{5} \\approx 4.472$\n"
                "- **Cosine Similarity:** $\\cos(\\theta) = \\frac{10.0}{\\sqrt{5} \\times \\sqrt{20}} = \\frac{10.0}{\\sqrt{100}} = \\frac{10.0}{10.0} = 1.0$\n"
                "*(Vectors point in the exact same direction despite length differences).*\n\n"
                "Now compare $\\mathbf{a} = [1, 2]$ with $\\mathbf{c} = [2, -1]$:\n"
                "- **Dot Product:** $\\mathbf{a} \\cdot \\mathbf{c} = (1 \\times 2) + (2 \\times -1) = 2 - 2 = 0.0$\n"
                "- **Cosine Similarity:** $\\cos(\\theta) = \\frac{0.0}{\\sqrt{5}\\sqrt{5}} = 0.0$\n"
                "*(Vectors are perpendicular / orthogonal, indicating unrelated semantic concepts).*"
            )
            q['tip'] = "Walk through the exact 3-step calculation: dot product (10), magnitudes (sqrt(5) and sqrt(20)), cosine similarity (1.0), and contrast with perpendicular vectors ([2, -1] yielding 0.0)."

        elif q.get('id') == 'q_0595':
            q['question'] = "How do you architect, scale, and monitor a high-throughput Semantic Search / RAG system using Dense Vector Embeddings in production?"
            q['answer'] = (
                "**1. Production Architectural Blueprint:**\n"
                "Deploying semantic search or RAG across millions of documents with sub-20ms SLAs requires decoupling offline ingestion from online query retrieval:\n"
                "- **Offline Ingestion Pipeline:** Documents are chunked (e.g. 512 tokens with 50-token overlap), passed through a bi-encoder (e.g. `all-MiniLM-L6-v2` or `text-embedding-3-small`), $L_2$-normalized to unit hyperspheres, and loaded into a vector index.\n"
                "- **Online Query Serving Path:** User queries are encoded using the identical frozen embedding model, projected to unit length, and searched via Approximate Nearest Neighbors (ANN).\n\n"
                "**2. Scaling via Approximate Nearest Neighbors (ANN) & Quantization:**\n"
                "- **Brute Force Linear Scan Fails:** Comparing a query against 10M documents in $\\mathcal{O}(N \\cdot d)$ requires seconds of compute.\n"
                "- **Hierarchical Navigable Small World (HNSW):** Navigates multi-layer proximity graphs in $\\mathcal{O}(\\log N)$ time, achieving 98%+ recall with $<5$ ms latency.\n"
                "- **Product Quantization (PQ):** Compresses 1536-d float32 vectors (6 KB each) into 64-byte codes, reducing RAM footprint by 90%.\n\n"
                "**3. Hybrid Search & Re-Ranking:**\n"
                "Dense embeddings capture broad semantic synonymy but struggle with exact part numbers, acronyms, or error codes. Production architectures combine dense ANN retrieval with sparse BM25 keyword search using Reciprocal Rank Fusion (RRF), followed by a cross-encoder re-ranker (e.g. `bge-reranker-large`) on the top 50 candidates.\n\n"
                "**4. Observability & Critical Production Pitfalls:**\n"
                "- **Never compare incompatible models:** Embeddings from different models (or versions) live in completely different vector spaces.\n"
                "- **Cosine similarity is not probability:** A score of 0.82 denotes angle, not an 82% statistical likelihood.\n"
                "- **Monitor embedding drift:** Track query distribution cosine shifts to catch evolving user terminology."
            )
            q['tip'] = "Structure your answer across 4 pillars: bi-encoder offline/online separation, HNSW/PQ vector scaling, hybrid search + cross-encoder re-ranking, and production drift observability."

    with open('src/data/interviewQuestions.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')
    print("Updated src/data/interviewQuestions.json successfully!")

if __name__ == '__main__':
    update_interview_questions()
