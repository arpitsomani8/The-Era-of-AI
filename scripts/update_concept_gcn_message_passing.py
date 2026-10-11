# -*- coding: utf-8 -*-
"""
Script to modernize concept_gcn_message_passing in
src/data/concepts.json and scripts/data_sources/all_concepts.json.
"""

import json

new_concept = {
    "id": "concept_gcn_message_passing",
    "title": "Graph Convolutional Networks (GCN) & Message Passing",
    "topic_id": "dl_gnn",
    "topic_label": "Graph Neural Networks (GNNs)",
    "category": "dl",
    "category_label": "Deep Learning Foundations",
    "raw_subtopic": "Graph Convolutional Networks (GCN) & Message Passing",
    "def": "Message passing is the general GNN paradigm where nodes iteratively aggregate feature information from their local neighborhoods along graph edges. Graph Convolutional Networks (GCN; Kipf & Welling, 2017) implement message passing via the layer update H^{l+1} = sigma(A_hat H^l W^l), where A_hat = D_tilde^{-1/2} A_tilde D_tilde^{-1/2} is the symmetrically normalized adjacency matrix with self-loops, W^l is a learnable weight matrix, and sigma is a nonlinear activation, enabling nodes to learn representations that encode both their own features and their neighborhood's graph-contextualized information.",
    "definition": "In Graph Neural Networks, message passing is the foundational computational paradigm enabling nodes to iteratively exchange and aggregate feature information along graph edges. A general message-passing layer consists of three stages: (1) Message creation, where each node v_i computes messages m_{ij} = phi(h_i^l, h_j^l, e_{ij}) from its current embedding h_i^l and neighbors' embeddings h_j^l via a learned message function phi; (2) Neighborhood aggregation, where each node collects incoming messages via a permutation-invariant aggregation function (sum, mean, or max): a_i^{l+1} = AGG({m_{ij} : j in N(i)}); and (3) Node update, where aggregated information is combined with the current embedding via a learned update function h_i^{l+1} = UPDATE(h_i^l, a_i^{l+1}). The Graph Convolutional Network (GCN), introduced by Kipf & Welling (2017), is the canonical spectral-motivated instantiation of this framework using the layer rule H^{l+1} = sigma(A_hat H^l W^l), where A_hat = D_tilde^{-1/2} A_tilde D_tilde^{-1/2} is the symmetrically degree-normalized adjacency matrix incorporating self-loops (A_tilde = A + I), H^l in R^{N x F_l} is the node embedding matrix at layer l, W^l in R^{F_l x F_{l+1}} is a learnable weight matrix, and sigma is a nonlinear activation (typically ReLU). Each GCN layer expands a node's receptive field by one hop; after k layers, each node's representation encodes information from its k-hop neighborhood. GCNs are trained end-to-end via backpropagation for tasks including node classification, graph classification, and link prediction.",
    "simple_summary": "Imagine each electricity substation in a power grid can pass a note to its directly connected neighbors. The note summarizes its own sensor readings. Every station reads the notes it receives, combines them with its own, and creates a new summary. After one round of note-passing, each station knows about its immediate neighbors. After two rounds, it knows about neighbors-of-neighbors. This is exactly what message passing does in a Graph Neural Network. A Graph Convolutional Network (GCN) formalizes this process mathematically: each round of note-passing is one GCN layer, and the learnable weight matrix W decides which parts of each note are most informative. The normalized adjacency matrix A_hat prevents a substation with 50 connections from being overwhelmed by 50 incoming notes while a leaf node with 1 connection gets almost nothing. After training, each substation's final 'note summary' (its embedding) encodes both its own anomaly history AND the context of its neighborhood, enabling far more accurate fault and theft detection than analyzing each meter in isolation.",
    "definition_bullets": [
        "Message Passing Paradigm: Three-stage GNN computation—message creation phi(h_i, h_j, e_ij), neighborhood aggregation AGG({m_ij}), and node update UPDATE(h_i, a_i)—repeated across layers.",
        "GCN Layer Equation: H^{l+1} = sigma(A_hat H^l W^l) where A_hat = D_tilde^{-1/2} A_tilde D_tilde^{-1/2} is the symmetrically normalized adjacency with self-loops.",
        "Receptive Field Expansion: After k GCN layers, each node's embedding encodes information from its k-hop neighborhood, enabling multi-hop relational reasoning.",
        "Matrix Dimensionality: A_hat in R^{NxN}, H^l in R^{NxF_l}, W^l in R^{F_l x F_{l+1}} — output H^{l+1} preserves N rows (one per node) while mapping to F_{l+1} learned features.",
        "Task Versatility: GCN outputs support node classification (N x num_classes scores), graph classification (pooled scalar), and link prediction (pair-wise embedding similarity) tasks."
    ],
    "core_terms": [
        {
            "term": "Message Passing",
            "what_is_it": "The general iterative neighborhood communication paradigm underlying all GNN architectures.",
            "definition": "A computational framework where each node v_i creates messages from its embedding and edge features, sends them along edges to neighbors, and aggregates received messages to update its own representation: h_i^{l+1} = UPDATE(h_i^l, AGG({phi(h_i^l, h_j^l, e_ij) : j in N(i)})).",
            "analogy": "A telephone tree: each person passes on information they receive from their connections, summarizes all incoming calls, and updates their own understanding before passing updated summaries forward.",
            "why_it_matters": "Provides a general, task-agnostic formulation that unifies GCN, GraphSAGE, GAT, and MPNN under a single theoretical framework."
        },
        {
            "term": "GCN Layer Equation H^{l+1} = σ(Â H^l W^l)",
            "what_is_it": "The core spectral convolution operation of Graph Convolutional Networks.",
            "definition": "A layer-wise propagation rule computing H^{l+1} = sigma(A_hat H^l W^l), where A_hat is the symmetric GCN normalization, H^l carries current node embeddings, W^l is trained via backpropagation, and sigma (typically ReLU) introduces non-linearity.",
            "analogy": "A team meeting where each member reads summaries from connected teammates (A_hat aggregation), processes the combined knowledge through their own lens (W^l transformation), and only retains positive insights (ReLU activation).",
            "why_it_matters": "Enables simultaneous feature transformation and graph-aware aggregation in a single differentiable matrix operation, making GCNs trainable end-to-end via standard gradient descent."
        },
        {
            "term": "Neighborhood Aggregation",
            "what_is_it": "The permutation-invariant operation combining incoming neighbor messages.",
            "definition": "A function AGG that combines the multi-set of neighbor embeddings {h_j^l : j in N(i)} into a single aggregated vector a_i^{l+1}, using operations such as sum, mean, max, or learned attention weights that are invariant to the ordering of neighbors.",
            "analogy": "A poll aggregator computing an average opinion score from all survey respondents, regardless of the order in which survey forms were received.",
            "why_it_matters": "Permutation invariance is necessary because graphs have no canonical node ordering; the same graph structure should produce identical node embeddings regardless of how nodes are indexed."
        },
        {
            "term": "Receptive Field (k-hop Neighborhood)",
            "what_is_it": "The set of graph nodes whose features influence a node's embedding after k GCN layers.",
            "definition": "After k GCN layers, node v_i's embedding H_i^k depends on all features in its k-hop neighborhood N_k(v_i) = {v_j : shortest_path(v_i, v_j) <= k}, expanding by one hop per layer.",
            "analogy": "A rumor spreading from person to person: after 1 round, you hear only from direct friends; after 2 rounds, you hear from friends-of-friends; after k rounds, the rumor has traveled k social hops.",
            "why_it_matters": "Determining appropriate layer depth requires matching the desired receptive field to the relevant information propagation distance in the application graph."
        },
        {
            "term": "Over-smoothing",
            "what_is_it": "A GCN failure mode where deep stacking causes all node representations to converge.",
            "definition": "The phenomenon where repeatedly applying neighborhood aggregation across many GCN layers causes node embeddings to become increasingly similar (converging toward the same stationary distribution), reducing discriminative power for downstream tasks.",
            "analogy": "Mixing multiple paint colors repeatedly: after a few mixes you get a distinct blended color, but eventually all combinations converge to the same muddy grey regardless of starting colors.",
            "why_it_matters": "Limits practical GCN depth to 2-4 layers for most tasks; necessitates architectural remedies like residual connections, jumping knowledge, or PairNorm normalization."
        }
    ],
    "symbol_guide": [
        {
            "symbol": "H^(l) ∈ ℝ^{N×F_l}",
            "name": "Node Embedding Matrix at Layer l",
            "meaning": "N-row matrix of F_l-dimensional embeddings; H^(0) = X (raw node features)."
        },
        {
            "symbol": "W^(l) ∈ ℝ^{F_l×F_{l+1}}",
            "name": "Learnable Weight Matrix",
            "meaning": "Trainable parameters projecting F_l-dim embeddings into F_{l+1}-dim space via gradient descent."
        },
        {
            "symbol": "Â = D̃^{-1/2} Ã D̃^{-1/2}",
            "name": "Normalized Adjacency Matrix",
            "meaning": "Symmetrically degree-normalized adjacency with self-loops; entry A_hat_ij = 1/sqrt(d_i * d_j)."
        },
        {
            "symbol": "σ",
            "name": "Activation Function",
            "meaning": "Non-linear activation (typically ReLU) applied element-wise after linear transformation."
        },
        {
            "symbol": "N(i)",
            "name": "Neighborhood of Node i",
            "meaning": "Set of all nodes j connected to node i by a direct edge; excludes i itself unless self-loops added."
        },
        {
            "symbol": "train_mask",
            "name": "Training Node Mask",
            "meaning": "Boolean index tensor selecting labeled nodes used for loss computation in semi-supervised node classification."
        },
        {
            "symbol": "F_in → F_out",
            "name": "Feature Dimensionality Transform",
            "meaning": "Each GCN layer maps F_in input features to F_out output features while preserving N node rows."
        }
    ],
    "formula": "$$\\text{GCN Layer: } H^{(l+1)} = \\sigma\\left( \\hat{A} H^{(l)} W^{(l)} \\right), \\quad H^{(0)} = X$$\n\n$$\\text{Normalized Adjacency: } \\hat{A} = \\tilde{D}^{-1/2} \\tilde{A} \\tilde{D}^{-1/2}, \\quad \\tilde{A} = A + I, \\quad \\tilde{D}_{ii} = \\sum_j \\tilde{A}_{ij}$$\n\n$$\\text{Entry-Wise Normalization: } \\hat{A}_{ij} = \\frac{\\tilde{A}_{ij}}{\\sqrt{\\tilde{d}_i \\cdot \\tilde{d}_j}}$$\n\n$$\\text{General Message Passing: } h_i^{(l+1)} = \\text{UPDATE}\\!\\left( h_i^{(l)},\\; \\text{AGG}\\!\\left(\\left\\{ \\phi\\!\\left( h_i^{(l)}, h_j^{(l)}, e_{ij} \\right) : j \\in \\mathcal{N}(i) \\right\\}\\right) \\right)$$\n\n$$\\text{Matrix Dimensions: } \\underbrace{\\hat{A}}_{N \\times N} \\underbrace{H^{(l)}}_{N \\times F_{\\text{in}}} \\underbrace{W^{(l)}}_{F_{\\text{in}} \\times F_{\\text{out}}} = \\underbrace{H^{(l+1)}}_{N \\times F_{\\text{out}}}$$\n\n$$\\text{Node Classification Loss: } \\mathcal{L} = -\\sum_{i \\in \\mathcal{V}_{\\text{train}}} \\sum_{c=1}^{C} y_{ic} \\log \\hat{y}_{ic}$$",
    "logic": "Graph Convolutional Networks provide a principled extension of convolutional operations from regular grid domains (images, sequences) to irregular graph-structured data. In image CNNs, a convolutional filter slides over a fixed local neighborhood (e.g., a 3x3 pixel patch) with shared weights. In GCNs, the 'neighborhood' is defined by the graph's adjacency structure, which varies per node. The key insight of Kipf & Welling (2017) was to derive a simplified first-order approximation of spectral graph convolutions that reduces to the elegant layer-wise propagation rule H^{l+1} = sigma(A_hat H^l W^l). The symmetric normalization A_hat = D_tilde^{-1/2} A_tilde D_tilde^{-1/2} arises naturally from spectral graph theory: it is the normalized graph Laplacian's complement, whose eigenvalues lie in [0, 2], providing numerical stability during repeated matrix multiplications in deep networks. Adding self-loops via A_tilde = A + I ensures that a node's own current representation H_i^l participates in its own update, preventing the degenerate case where a node entirely forgets its starting features after multiple aggregation rounds. The weight matrix W^l plays the role of a standard linear transformation: it projects node embeddings from F_l dimensions into F_{l+1} dimensions, creating task-relevant feature representations. All N nodes share the same W^l, making GCNs parameter-efficient regardless of graph size. Stacking k GCN layers expands each node's receptive field to its k-hop neighborhood. However, too many layers trigger over-smoothing: the iterative averaging operations cause all embeddings to converge toward a stationary limit determined by the graph's spectral properties, destroying node-level discriminative information. In practice, 2-3 GCN layers often yield better task performance than deeper architectures. For node classification in semi-supervised settings, only a fraction of nodes need labels during training; gradients flow through the GCN's shared weights, indirectly incorporating information from all graph nodes via A_hat.",
    "example": "Consider a GCN applied to a molecular graph for drug toxicity prediction. Each atom is a node with features [atomic_number, formal_charge, num_hydrogens, aromaticity]. Carbon-carbon single bonds, double bonds, and aromatic bonds define weighted edges. After one GCN layer (H^1 = ReLU(A_hat X W^0)), each atom's embedding encodes both its atomic properties and a weighted summary of its bonded neighbors' properties. After a second layer, each embedding captures two-hop chemical environments—e.g., a carbon bonded to a nitrogen bonded to an oxygen. A global mean-pooling operation collapses the N x F_2 node embedding matrix into a single 1 x F_2 molecular fingerprint, which is passed to a classifier. The shared weights W^0 and W^1 are learned across thousands of training molecules via backpropagation with a binary cross-entropy loss on toxicity labels.",
    "numerical_example": "Step 1: Complete 2-Node GCN Forward Pass (Matching User Notes)\nSetup: 2 nodes connected by one edge. Node 1 feature = 1.0, Node 2 feature = 3.0.\n  A = [[0, 1], [1, 0]]  (undirected connection)\n  X = [[1], [3]]  (1 feature per node)\n\nStep 1a: Add self-loops  A_tilde = A + I\n  A_tilde = [[1, 1], [1, 1]]\n\nStep 1b: Compute degree matrix D_tilde (row sums of A_tilde)\n  d_1 = 1 + 1 = 2,  d_2 = 1 + 1 = 2\n  D_tilde = [[2, 0], [0, 2]]\n  D_tilde^{-1/2} = [[1/sqrt(2), 0], [0, 1/sqrt(2)]] = [[0.7071, 0], [0, 0.7071]]\n\nStep 1c: Compute A_hat = D_tilde^{-1/2} @ A_tilde @ D_tilde^{-1/2}\n  A_hat = [[0.7071, 0], [0, 0.7071]] @ [[1, 1], [1, 1]] @ [[0.7071, 0], [0, 0.7071]]\n  Inner product [[0.7071, 0.7071], [0.7071, 0.7071]] @ [[0.7071, 0], [0, 0.7071]]\n  A_hat = [[0.5, 0.5], [0.5, 0.5]]\n  Each node contributes exactly 0.5 weight to itself AND its neighbor (equal degree -> equal split).\n\nStep 1d: Aggregate features: A_hat @ X\n  A_hat @ X = [[0.5, 0.5], [0.5, 0.5]] @ [[1], [3]]\n  Node 1: 0.5 * 1 + 0.5 * 3 = 0.5 + 1.5 = 2.0\n  Node 2: 0.5 * 1 + 0.5 * 3 = 0.5 + 1.5 = 2.0\n  Both nodes receive identical aggregated value = 2.0 (both see same neighborhood).\n\nStep 1e: Apply learnable transformation W = [[2]] and ReLU activation\n  H^1 = ReLU(A_hat @ X @ W) = ReLU([[2.0], [2.0]] * 2) = ReLU([[4.0], [4.0]]) = [[4.0], [4.0]]\n\nStep 2: Matrix Dimensions for Real GCN (N=100 nodes, F_in=8, F_out=16)\n  A_hat:  (100, 100)  -  fixed graph structure\n  H^0:   (100, 8)    -  input feature matrix\n  W^0:   (8, 16)     -  LEARNABLE\n  H^1 = sigma(A_hat @ H^0 @ W^0): (100, 16)  -  updated embeddings\n  N rows preserved (one per node), feature dimension expands from 8 to 16.\n\nStep 3: PyTorch GCN Implementation (Matching User Notes)\n```python\nimport torch\nimport torch.nn as nn\nimport torch.nn.functional as F\n\nclass GCNLayer(nn.Module):\n    def __init__(self, in_features, out_features):\n        super().__init__()\n        self.linear = nn.Linear(in_features, out_features, bias=False)\n    def forward(self, x, adj_norm):\n        x = self.linear(x)      # W^l transformation: (N, F_in) -> (N, F_out)\n        x = adj_norm @ x         # Neighborhood aggregation: A_hat @ H\n        return F.relu(x)         # Non-linear activation\n\nclass GCN(nn.Module):\n    def __init__(self, in_features, hidden, num_classes):\n        super().__init__()\n        self.layer1 = GCNLayer(in_features, hidden)\n        self.layer2 = GCNLayer(hidden, num_classes)\n    def forward(self, x, adj_norm):\n        x = self.layer1(x, adj_norm)  # 1-hop neighborhood\n        x = self.layer2(x, adj_norm)  # 2-hop neighborhood\n        return x\n\n# Build normalized adjacency for 2-node graph\nA = torch.tensor([[0., 1.], [1., 0.]])\nX = torch.tensor([[1.], [3.]])\nA_tilde = A + torch.eye(2)\ndegrees = A_tilde.sum(dim=1)        # [2., 2.]\nd_inv_sqrt = degrees.pow(-0.5)       # [0.7071, 0.7071]\nD_inv_sqrt = torch.diag(d_inv_sqrt)\nA_hat = D_inv_sqrt @ A_tilde @ D_inv_sqrt  # [[0.5, 0.5], [0.5, 0.5]]\n\nmodel = GCN(in_features=1, hidden=4, num_classes=2)\noutput = model(X, A_hat)\nprint('Output shape:', output.shape)  # torch.Size([2, 2])\n```\n\nStep 4: Node Classification Training Loop\n```python\n# Semi-supervised node classification\ntrain_mask = torch.tensor([True, False])  # Only node 0 labeled\nlabels = torch.tensor([1, 0])             # Node 0 class=1\noptimizer = torch.optim.Adam(model.parameters(), lr=0.01)\n\nfor epoch in range(100):\n    model.train()\n    optimizer.zero_grad()\n    logits = model(X, A_hat)              # Shape: [N, num_classes]\n    loss = F.cross_entropy(logits[train_mask], labels[train_mask])\n    loss.backward()                        # Gradients flow through shared W\n    optimizer.step()\n    if epoch % 20 == 0:\n        print(f'Epoch {epoch}, Loss: {loss.item():.4f}')\n```\n\nStep 5: Over-Smoothing Intuition Across Layers\nStart with distinct embeddings: Node A = [1.0], Node B = [0.0]\n  After Layer 1 (mean aggregation A-B connected):\n    h_A^1 = 0.5*1.0 + 0.5*0.0 = 0.50,   h_B^1 = 0.5*1.0 + 0.5*0.0 = 0.50\n  After Layer 2:\n    h_A^2 = 0.5*0.50 + 0.5*0.50 = 0.50,  h_B^2 = 0.50 (already converged!)\n  After Layer 5 (with more nodes, convergence is gradual): all nodes -> same value\n  -> Embeddings become indistinguishable despite different initial features!",
    "types_header": "Graph Neural Network Propagation Architectures",
    "types_badge": "Message Passing & Convolution Variants",
    "quick_types": [
        {
            "name": "Graph Convolutional Network (GCN)",
            "description": "Spectral-inspired symmetric normalization H^{l+1} = sigma(A_hat H^l W^l); parameter-efficient with shared weights across all N nodes."
        },
        {
            "name": "Mean/Sum Aggregation Message Passing",
            "description": "Simple neighbor averaging h_i^{l+1} = sigma(W * mean({h_j : j in N(i) cup {i}})); intuitive and computationally efficient for homophilous graphs."
        },
        {
            "name": "Graph Attention Network (GAT)",
            "description": "Weighted aggregation using learned attention coefficients alpha_ij = softmax(e_ij) to adaptively weight neighbor contributions."
        },
        {
            "name": "GraphSAGE (Inductive Aggregation)",
            "description": "Inductive GNN that learns aggregation functions (mean, LSTM, pool) over sampled neighborhoods, enabling generalization to unseen nodes."
        }
    ],
    "connected_logic": [
        {
            "title": "GCN Layer Computation Flow",
            "description": "Sequential operations constituting one complete GCN message-passing layer.",
            "points": [
                "H^l W^l projects all N node embeddings from F_in to F_out dimensions via shared linear transformation.",
                "A_hat @ (H^l W^l) aggregates transformed neighbor features weighted by symmetric degree normalization.",
                "sigma(A_hat H^l W^l) applies element-wise ReLU, introducing non-linearity and enabling universal function approximation over graphs."
            ]
        },
        {
            "title": "Receptive Field & Multi-Layer Stacking",
            "description": "How each additional GCN layer expands the neighborhood information captured in node embeddings.",
            "points": [
                "After k layers, node v_i's embedding H_i^k encodes information from all nodes within k hops.",
                "2-3 layers suffice for most real-world graphs where informative signals are local; deeper stacking risks over-smoothing.",
                "Residual connections h^{l+1} = sigma(A_hat H^l W^l) + H^l mitigate over-smoothing by preserving layer-l identity."
            ]
        },
        {
            "title": "Semi-Supervised Node Classification",
            "description": "Training GCNs with partial node labels using shared weight propagation.",
            "points": [
                "A_hat propagates gradient information through the entire graph even when only a subset of nodes are labeled.",
                "train_mask boolean tensor selects labeled nodes for cross-entropy loss computation.",
                "At inference time, all N nodes receive updated embeddings even if most were unlabeled during training."
            ]
        },
        {
            "title": "Over-Smoothing, Over-Squashing & Practical Limitations",
            "description": "Fundamental pathological behaviors limiting GCN expressivity and scalability.",
            "points": [
                "Over-smoothing: repeated aggregation drives all embeddings toward graph-spectral stationary distribution, collapsing node discriminability.",
                "Over-squashing: exponentially growing k-hop neighborhoods compressed into fixed-size vectors cause information loss for long-range dependencies.",
                "Dense O(N^2) adjacency matrix operations become infeasible for large graphs; sparse operations and mini-batch neighbor sampling are required."
            ]
        }
    ],
    "pitfalls": [
        "Applying Activation After the Final GCN Layer: The last GCN layer typically outputs raw class logits for cross-entropy loss; applying ReLU would clip negative scores and distort loss computation.",
        "Ignoring Over-Smoothing When Stacking Many Layers: Adding more GCN layers does not monotonically improve performance; 2-4 layers typically optimize task performance before embeddings over-smooth.",
        "Using Dense Adjacency for Large Graphs: Dense N x N matrix multiplication scales as O(N^2 * F); sparse matrix operations in PyTorch Geometric or DGL reduce this to O(|E| * F).",
        "Forgetting to Recompute A_hat When Graph Changes: A_hat = D_tilde^{-1/2} A_tilde D_tilde^{-1/2} must be recomputed if edges are added or removed; stale normalization produces incorrect aggregation weights.",
        "Confusing GCN Normalization with Simple Mean Aggregation: A_hat_ij = 1/sqrt(d_i * d_j) differs from simple mean 1/d_i; high-degree hub nodes receive smaller contributions per neighbor in GCN versus equal 1/d_i weights in mean aggregation."
    ],
    "key_takeaways": [
        "Message passing is the universal GNN paradigm where nodes iteratively create, aggregate, and use neighbor messages to update their representations, expanding receptive fields by one graph hop per layer.",
        "GCN implements message passing as H^{l+1} = sigma(A_hat H^l W^l), with A_hat = D_tilde^{-1/2} A_tilde D_tilde^{-1/2} providing symmetric degree normalization and self-loops ensuring nodes include their own features.",
        "Matrix dimensions: A_hat (N x N) @ H^l (N x F_in) @ W^l (F_in x F_out) = H^{l+1} (N x F_out) — N rows (nodes) are always preserved; only feature dimension F changes.",
        "Over-smoothing limits practical GCN depth to 2-4 layers; deeper architectures require residual connections or alternative aggregation designs to prevent embedding collapse."
    ],
    "tags": [
        "Graph Neural Networks",
        "GCN",
        "Message Passing",
        "Neighborhood Aggregation",
        "Node Classification",
        "Over-Smoothing",
        "PyTorch Geometric",
        "Graph Convolution"
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

update_concepts_file('src/data/concepts.json')
update_concepts_file('scripts/data_sources/all_concepts.json')
