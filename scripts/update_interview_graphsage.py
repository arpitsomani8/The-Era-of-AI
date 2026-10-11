# -*- coding: utf-8 -*-
"""
Update interview questions q_0962, q_0963, q_0964 in src/data/interviewQuestions.json
to precisely reflect Inductive Graph Representation Learning (GraphSAGE).
"""

import json

def update_interview_questions():
    with open('src/data/interviewQuestions.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    for q in data:
        if q.get('id') == 'q_0962':
            q['question'] = "What is Inductive Graph Representation Learning (GraphSAGE), and how does it generate embeddings for unseen nodes?"
            q['answer'] = (
                "**Executive Summary:**\n"
                "GraphSAGE (Graph Sample and Aggregate) is an inductive Graph Neural Network framework that learns reusable functions to generate node embeddings from raw node features and local neighborhood information, rather than memorizing a fixed embedding lookup table for static nodes.\n\n"
                "**1. Inductive vs. Transductive Learning:**\n"
                "- **Transductive Learning:** Classic algorithms (DeepWalk, node2vec, standard matrix factorization) learn a separate embedding vector for each node in a fixed graph. If a new node joins tomorrow, it has no vector in the lookup table; the model must be retrained from scratch.\n"
                "- **Inductive Learning:** GraphSAGE learns shared aggregation and transformation functions: $f(x_v, \\mathcal{N}(v); \\Theta)$. When an unseen node joins (e.g., a new user on a social network, a new product in an e-commerce catalog, or a new smart meter on an electricity grid), GraphSAGE generates its embedding instantly using its raw features and available connections without retraining.\n\n"
                "**2. The Four-Step GraphSAGE Pipeline:**\n"
                "1. **Sample Neighbors:** Sample a fixed, uniform number of neighbors $S_k$ at each layer rather than processing all connections (capping exponential hub growth).\n"
                "2. **Aggregate Information:** Combine sampled neighbor vectors using a permutation-invariant aggregator (Mean, Pooling MLP, or Shuffled LSTM).\n"
                "3. **Update Representation:** Concatenate the node's own vector with the neighborhood aggregate, then project with learned weights: $h_v^{(k)} = \\sigma\\left( W^{(k)} [h_v^{(k-1)} \\parallel h_{\\mathcal{N}(v)}^{(k)}] \\right)$.\n"
                "4. **Multilayer Expansion:** Repeat across $K$ layers to incorporate information from a $K$-hop sampled neighborhood tree.\n\n"
                "**3. Why Concatenate Ego and Neighbor Features?**\n"
                "Simply averaging a node's features with its neighbors washes out ego-identity. In an electricity network, a meter's own readings describe its personal voltage/consumption anomalies, while neighbor aggregates describe the local feeder status. Concatenation $[h_v^{(k-1)} \\parallel h_{\\mathcal{N}(v)}^{(k)}]$ preserves both signals separately, allowing learned weights $W^{(k)}$ to balance personal state against neighborhood context."
            )
            q['tip'] = "Anchor your answer on the core shift: moving from memorizing node embedding tables (transductive) to learning a reusable function of features and connections (inductive)."

        elif q.get('id') == 'q_0963':
            q['question'] = "What is the mathematical update rule of GraphSAGE, how do the 4 aggregator choices differ, and how does the numerical forward pass compute?"
            q['answer'] = (
                "**1. Mathematical Update Formulation:**\n"
                "At layer $k$, neighbor aggregation and node updates are computed as:\n"
                "$$h_{\\mathcal{N}(v)}^{(k)} = \\text{AGGREGATE}_k\\left( \\{ h_u^{(k-1)} : u \\in \\mathcal{S}_{\\mathcal{N}(v)} \\} \\right)$$\n"
                "$$h_v^{(k)} = \\sigma\\left( W^{(k)} \\cdot \\left[ h_v^{(k-1)} \\parallel h_{\\mathcal{N}(v)}^{(k)} \\right] \\right)$$\n"
                "where $\\parallel$ denotes vector concatenation, $\\mathcal{S}_{\\mathcal{N}(v)}$ is the sampled neighborhood, $W^{(k)} \\in \\mathbb{R}^{d_k \\times (2 d_{k-1})}$, and $\\sigma$ is typically ReLU.\n\n"
                "**2. The Four Aggregator Architectures:**\n"
                "- **Mean Aggregator:** $h_{\\mathcal{N}(v)}^{(k)} = \\frac{1}{|\\mathcal{S}|} \\sum_{u} h_u^{(k-1)}$. Simple, linear, parameter-free within aggregation, efficient baseline.\n"
                "- **Pooling Aggregator:** $h_{\\mathcal{N}(v)}^{(k)} = \\max_{u} \\{ \\sigma(W_{\\text{pool}} h_u^{(k-1)} + \\mathbf{b}) \\}$. Applies a shared MLP followed by element-wise max-pooling; captures distinct pattern peaks across channels.\n"
                "- **LSTM Aggregator:** $h_{\\mathcal{N}(v)}^{(k)} = \\text{LSTM}([h_{\\pi(u)}^{(k-1)}])$. High expressive capacity, but requires random neighbor order shuffling $\\pi$ to enforce permutation invariance over unordered graph neighborhoods.\n"
                "- **GCN-Style Aggregator:** $h_v^{(k)} = \\sigma\\left( W \\cdot \\text{MEAN}(\\{h_v^{(k-1)}\\} \\cup \\{h_u^{(k-1)} : u \\in \\mathcal{N}(v)\\}) \\right)$. Mimics Kipf & Welling convolutional pooling without explicit concatenation.\n\n"
                "**3. Step-by-Step Numerical Example (Mean Aggregator):**\n"
                "- **Given:** Target node $v$ with $h_v^{(0)} = 4$. Two sampled neighbors $u_1$ with $h_{u1}^{(0)} = 2$, and $u_2$ with $h_{u2}^{(0)} = 6$.\n"
                "- **Weights:** $W = [0.5, 1.0]^T$, zero bias, $\\sigma = \\text{ReLU}$.\n"
                "- **Step 1 (Neighbor Mean):** $h_{\\mathcal{N}(v)}^{(1)} = (2 + 6) / 2 = 8 / 2 = 4.0$.\n"
                "- **Step 2 (Concatenate):** $[h_v^{(0)} \\parallel h_{\\mathcal{N}(v)}^{(1)}] = [4.0, 4.0]$.\n"
                "- **Step 3 (Linear Projection & ReLU):** $\\text{Linear} = [4.0, 4.0] \\cdot [0.5, 1.0]^T = 4.0(0.5) + 4.0(1.0) = 2.0 + 4.0 = 6.0$.\n"
                "- **Final Embedding:** $h_v^{(1)} = \\text{ReLU}(6.0) = 6.0$.\n"
                "*(Notice: while the neighbor mean was 4.0, the final embedding is 6.0 because ego-state and neighborhood context combine through learned weights).*"
            )
            q['tip'] = "Walk through the exact 3-step calculation: neighbor mean (4.0), concatenation ([4, 4]), and linear dot product (4*0.5 + 4*1.0 = 6.0)."

        elif q.get('id') == 'q_0964':
            q['question'] = "How does neighbor sampling bound computational complexity in GraphSAGE, how do you architect it for web-scale serving, and what are common pitfalls?"
            q['answer'] = (
                "**1. Why Neighbor Sampling Scales (Complexity Bounding):**\n"
                "In full-graph GCNs, a node with degree $d$ expands to $O(d^K)$ nodes across $K$ layers. In dense power-law graphs (e.g., social influencers with $10^5$ followers), a single 2-hop update can span millions of vertices, causing GPU Out-Of-Memory (OOM) crashes.\n"
                "GraphSAGE bounds this by setting fixed sample sizes per layer (e.g., $S_1 = 10, S_2 = 5$):\n"
                "- Target node: 1 node\n"
                "- Layer 1 sampled neighbors: 10 nodes\n"
                "- Layer 2 sampled occurrences: $10 \\times 5 = 50$ occurrences\n"
                "- **Max Receptive Tree Size:** $1 + 10 + 50 = 61$ node occurrences (bounded constant).\n"
                "This enables standard mini-batch SGD: batches of target nodes can be sampled independently using dynamic computation trees via `torch_geometric.loader.NeighborLoader`.\n\n"
                "**2. Web-Scale Production Architecture (e.g., Pinterest PinSage):**\n"
                "- **Decoupled Architecture:** Offline batch trainer learns aggregator weights $W^{(k)}$ and pooling heads; an online graph feature service stores node attributes in Redis/Feast and graph edges in a distributed graph database.\n"
                "- **Real-time Inductive Serving:** When a new user or item arrives, query its local 2-hop edges, retrieve raw node features, sample fixed neighbors, and run the forward pass through the compiled ONNX/TensorRT model within $<15$ ms SLA.\n\n"
                "**3. Critical Production Pitfalls:**\n"
                "- **Unshuffled LSTM Aggregators:** LSTMs are sensitive to token sequence order; failure to randomly permute neighbor inputs violates graph permutation invariance.\n"
                "- **Assuming Unseen Nodes Need No Data:** Inductive models still require valid input feature vectors and local neighborhood connections.\n"
                "- **Feature Preprocessing Drift:** New test nodes must undergo the exact same normalization, imputation, and scaling applied to training nodes.\n"
                "- **Severe Under-Sampling:** Overly aggressive sampling (e.g., $S=1$) saves computation but blows up gradient variance and omits crucial topology context."
            )
            q['tip'] = "Emphasize how fixed sampling transforms GNN training from full-graph whole-matrix operations into standard mini-batch SGD with bounded memory."

    with open('src/data/interviewQuestions.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')
    print("Updated src/data/interviewQuestions.json successfully!")

if __name__ == '__main__':
    update_interview_questions()
