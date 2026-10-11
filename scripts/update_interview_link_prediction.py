# -*- coding: utf-8 -*-
"""
Update interview questions q_0965, q_0966, q_0967 in src/data/interviewQuestions.json
to precisely reflect Link Prediction & Node Classification Pipelines.
"""

import json

def update_interview_questions():
    with open('src/data/interviewQuestions.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    for q in data:
        if q.get('id') == 'q_0965':
            q['question'] = "What is the difference between Node Classification and Link Prediction pipelines in Graph Neural Networks?"
            q['answer'] = (
                "**Executive Summary:**\n"
                "Node Classification and Link Prediction are the two primary downstream learning tasks in geometric deep learning. Both typically share the same Graph Neural Network encoder (GCN, GAT, GraphSAGE) to generate continuous node embeddings $\\mathbf{Z} = f_\\theta(X, A)$, but differ fundamentally in their prediction targets, heads, and evaluation protocols.\n\n"
                "**1. Node Classification (Predicting Entity Properties):**\n"
                "- **Question:** *What category does this individual node belong to?*\n"
                "- **Target:** A single target vertex $v \\in \\mathcal{V}$.\n"
                "- **Output:** Class logits or probability distribution over $C$ classes: $\\hat{\\mathbf{y}}_v = \\text{Softmax}(\\mathbf{z}_v W_c)$.\n"
                "- **Example:** Classifying an electricity meter as normal vs. suspicious, or identifying whether a user account is legitimate or a fraudulent money-laundering mule.\n\n"
                "**2. Link Prediction (Predicting Pairwise Relationships):**\n"
                "- **Question:** *Should these two nodes be connected, or how likely is an unobserved/future connection between them?*\n"
                "- **Target:** A candidate pair of vertices $(u, v) \\in \\mathcal{V} \\times \\mathcal{V}$.\n"
                "- **Output:** A scalar score or probability $p(u, v) = \\sigma(s(u, v)) \\in [0, 1]$.\n"
                "- **Example:** Recommending a product to a user on an e-commerce platform ('Will User A buy Product X?'), or predicting friendship formation ('People You May Know').\n\n"
                "**3. Decoupled Pipeline Architecture:**\n"
                "A modular pipeline feeds graph structure and raw node features into a shared GNN backbone. For node classification, node embeddings pass through a linear classifier with cross-entropy loss. For link prediction, pairs of embeddings pass through a link decoder (dot product or MLP) trained via binary cross-entropy with logits."
            )
            q['tip'] = "Anchor your answer on the prediction target: Node Classification predicts an attribute of ONE node, whereas Link Prediction predicts a relationship between a PAIR of nodes."

        elif q.get('id') == 'q_0966':
            q['question'] = "How are Node Classification and Link Prediction mathematically formulated and loss-optimized, and how does pairwise link scoring compute numerically?"
            q['answer'] = (
                "**1. Node Classification Mathematical Formulation:**\n"
                "Given GNN node representations $H = f_\\theta(X, A) \\in \\mathbb{R}^{N \\times d}$, a classification head projects each node to $C$ class logits: $Z = H W_c$. Training optimizes multiclass cross-entropy loss restricted to labeled nodes via a boolean `train_mask`:\n"
                "$$\\mathcal{L}_{\\text{node}} = -\\frac{1}{|\\mathcal{V}_{\\text{train}}|} \\sum_{v \\in \\mathcal{V}_{\\text{train}}} \\sum_{c=1}^C y_{vc} \\log \\hat{y}_{vc}$$\n\n"
                "**2. Link Prediction Decoders & Binary Loss:**\n"
                "A link decoder evaluates node pairs $(u, v)$ from embeddings $\\mathbf{z}_u, \\mathbf{z}_v$:\n"
                "- **Dot-Product Decoder (Symmetric):** $s(u, v) = \\mathbf{z}_u^\\top \\mathbf{z}_v$, mapped to probability $p(u, v) = \\sigma(s(u, v))$.\n"
                "- **Pairwise MLP Decoder (Asymmetric / Directed):** $s(u, v) = \\text{MLP}([\\mathbf{z}_u \\parallel \\mathbf{z}_v])$.\n"
                "Trained via Binary Cross-Entropy with Logits over observed positive edges ($y_{uv} = 1$) and sampled negative non-edges ($y_{uv} = 0$):\n"
                "$$\\mathcal{L}_{\\text{link}} = -\\frac{1}{M} \\sum_{(u, v)} \\left[ y_{uv} \\log \\sigma(s_{uv}) + (1 - y_{uv}) \\log (1 - \\sigma(s_{uv})) \\right]$$\n\n"
                "**3. Worked Numerical Example (Dot-Product Link Scoring):**\n"
                "- **Given:** Node embeddings $\\mathbf{z}_u = [1.0, 2.0]$ and $\\mathbf{z}_v = [2.0, 1.0]$.\n"
                "- **Step 1 (Compute Dot-Product Logit):**\n"
                "  $$s(u, v) = \\mathbf{z}_u^\\top \\mathbf{z}_v = (1.0 \\times 2.0) + (2.0 \\times 1.0) = 2.0 + 2.0 = 4.0$$\n"
                "- **Step 2 (Apply Sigmoid):**\n"
                "  $$p(u, v) = \\sigma(4.0) = \\frac{1}{1 + e^{-4.0}} = \\frac{1}{1 + 0.018316} \\approx 0.9820 \\; (98.2\\%$$\n"
                "- **Step 3 (Compute Loss for Positive Edge $y_{uv} = 1$):**\n"
                "  $$\\text{Loss} = -\\log(0.9820) \\approx 0.0182$$\n"
                "*(High probability correctly yielded near-zero loss for a true positive link).*"
            )
            q['tip'] = "Walk through the exact 3-step numerical calculation: dot product logit (4.0), sigmoid probability (0.982), and BCE loss (0.0182)."

        elif q.get('id') == 'q_0967':
            q['question'] = "How do you prevent data leakage in link prediction, handle extreme class imbalance, and architect production graph serving?"
            q['answer'] = (
                "**1. Preventing Data Leakage in Link Prediction (Anti-Leakage Hygiene):**\n"
                "The most catastrophic failure mode in link prediction is evaluation leakage. If a test edge $(u, v)$ is included in the message-passing adjacency graph $A$ (`edge_index`) during encoding, the GNN directly passes messages across the edge it is asked to predict. The model achieves near-perfect test metrics by memorizing the existing topological bridge, but completely fails in production.\n"
                "- **The Fix:** Strictly partition edges into $E_{\\text{train}}$, $E_{\\text{val}}$, and $E_{\\text{test}}$. The message-passing graph `edge_index` visible to the encoder must contain ONLY $E_{\\text{train}}$.\n"
                "- **Undirected Graphs:** Both forward $(u, v)$ and reverse $(v, u)$ directions must be removed simultaneously.\n"
                "- **Temporal Graphs:** Partition edges temporally (train on edges before timestamp $T_0$, evaluate on edges after $T_0$) to prevent future lookahead bias.\n\n"
                "**2. Negative Sampling & The Open-World Assumption:**\n"
                "Graphs exhibit positive-only observations: an unobserved edge does not guarantee zero relationship (it may simply be unformed). Uniformly sample unlinked node pairs $\\mathcal{S}_{\\text{neg}}$ as label-0 contrastive examples. In web-scale recommenders, blend uniform random negatives with hard 2-hop negatives to force fine-grained topological discrimination.\n\n"
                "**3. Evaluation Under Severe Class Imbalance:**\n"
                "In a 100,000-node graph, there are ~5 billion possible pairs, with only ~1 million real edges (0.02% positive rate). Predicting 'no link' everywhere yields 99.98% accuracy but zero business utility.\n"
                "- **Never rely on raw accuracy.**\n"
                "- **Classification Metrics:** Precision-Recall AUC (PR-AUC) and F1-score.\n"
                "- **Ranking & Retrieval Metrics:** Hits@K (fraction of true test links ranked in top K candidates) and Mean Reciprocal Rank (MRR).\n\n"
                "**4. Production Serving Architecture:**\n"
                "- **Decoupled Offline/Online Serving:** Offline batch jobs run the GNN encoder to generate and refresh node embeddings in a feature store (Feast/Redis).\n"
                "- **Sub-15ms Online Link Inference:** Candidate pairs are scored via fast dot-product decoders indexed in vector search engines (Faiss, Milvus, ScaNN) for sub-15ms nearest-neighbor link retrieval."
            )
            q['tip'] = "Highlight the distinction between edge_index (what the encoder observes) and train_pairs (what the loss evaluates), emphasizing why both directions of test edges must be excised."

    with open('src/data/interviewQuestions.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')
    print("Updated src/data/interviewQuestions.json successfully!")

if __name__ == '__main__':
    update_interview_questions()
