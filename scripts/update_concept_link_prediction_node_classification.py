# -*- coding: utf-8 -*-
"""
Script to modernize concept_link_prediction_node_classification in
src/data/concepts.json and scripts/data_sources/all_concepts.json.
"""

import json

new_concept = {
    "id": "concept_link_prediction_node_classification",
    "title": "Link Prediction & Node Classification Pipelines",
    "topic_id": "dl_gnn",
    "topic_label": "Graph Neural Networks (GNNs)",
    "category": "dl",
    "category_label": "Deep Learning Foundations",
    "raw_subtopic": "Link Prediction & Node Classification Pipelines",
    "raw_sub": "Link Prediction & Node Classification Pipelines",
    "def": "The two primary downstream learning paradigms in Graph Neural Networks: Node Classification (predicting categorical attribute labels for individual vertices) and Link Prediction (predicting the existence, probability, or future formation of relational edges between vertex pairs).",
    "definition": "In geometric deep learning, Node Classification and Link Prediction constitute the dual canonical downstream task formulations that convert learned latent graph representations into actionable business predictions. While both tasks typically share a common Graph Neural Network backbone encoder (such as GCN, GAT, or GraphSAGE) to map raw node features X in R^{N x F} and adjacency topology A into rich d-dimensional node representations H = f_theta(X, A) in R^{N x d}, their supervision mechanics, decoder architectures, and evaluation protocols differ fundamentally. In Node Classification, the objective is to learn a mapping from individual node representations to discrete class labels: logits Z = H W_c in R^{N x C}, optimized via multiclass cross-entropy loss over labeled training node masks V_train. In Link Prediction, the objective is to score candidate pairs of nodes (u, v) to estimate whether an edge currently exists or is likely to form in the future. Pairwise scoring is performed via decoders such as dot-product s(u, v) = z_u^T z_v, bilinear transformations s(u, v) = z_u^T W_r z_v, or non-linear multilayer perceptrons s(u, v) = MLP([z_u || z_v]), with predicted probabilities p(u, v) = sigma(s(u, v)) trained via binary cross-entropy with logits against positive observed edges and sampled negative non-edges. The central engineering challenge in link prediction is preventing data leakage: candidate test edges (and both (u, v) and (v, u) directions in undirected graphs) must be strictly excised from the message-passing adjacency matrix during encoding, ensuring the model cannot trivially detect edges by simply passing messages across them.",
    "simple_summary": "Think of a fraud detection platform at a major bank or social network: Node Classification answers 'What is this entity?' (e.g., 'Is this bank account a normal customer or a fraudulent money-laundering mule?'). It looks at the account's transaction history and summarizes how its direct connections behave to stamp a category label on that single account. Link Prediction answers 'Will these two entities connect?' (e.g., 'Is Account A covertly funneling stolen funds to Account B?' or 'Will Alice purchase Product X?'). It takes the profile summaries of two separate entities and compares them side-by-side to calculate a compatibility score. Crucially, both tasks can share the exact same 'brain'—a Graph Neural Network like GCN, GAT, or GraphSAGE that compresses messy graph connections into clean vector profiles. The most critical trap in link prediction is cheating: if you leave the wire connecting Account A and Account B inside the network while asking your model 'Are A and B connected?', the model will simply trace the wire and get 100% test accuracy without learning any real fraud patterns. Production-grade pipelines strictly hide test wires from the graph before testing the model's ability to predict them.",
    "definition_bullets": [
        "Node Classification Pipeline: Maps individual node embeddings h_v to discrete class distributions via linear projection Z = H W_c, trained with cross-entropy loss over boolean train masks.",
        "Link Prediction Pipeline: Scores candidate node pairs (u, v) using dot-product z_u^T z_v or pairwise MLP decoders, trained with binary cross-entropy against observed edges and sampled non-edges.",
        "Strict Edge Masking (Anti-Leakage): Withholding held-out test edges (both (u, v) and (v, u) directions in undirected graphs) from the message-passing adjacency matrix to prevent trivial target leakage.",
        "Negative Edge Sampling: Uniformly sampling unlinked node pairs under the open-world assumption to provide balanced label-0 contrastive supervision against positive observed edges.",
        "Shared Encoder Architecture: Decoupling the GNN representation encoder from task-specific classification heads and link decoders, supporting both single-task and joint multi-task training."
    ],
    "core_terms": [
        {
            "term": "Node Classification",
            "what_is_it": "The task of predicting a categorical label or continuous property for individual graph vertices.",
            "definition": "Given a graph G = (V, E, X) with labels known for a subset V_train subset V, learn a hypothesis h: V -> {1, ..., C} that accurately predicts labels for remaining vertices V_val and V_test using learned node embeddings H = GNN(X, A) and a linear classification head Z = H W_c.",
            "analogy": "Determining an employee's department and security clearance level by analyzing their resume attributes and who they collaborate with on daily project teams.",
            "why_it_matters": "The core paradigm for detecting fraudulent accounts, categorizing medical documents, predicting protein functions, and diagnosing malfunctioning smart meters."
        },
        {
            "term": "Link Prediction",
            "what_is_it": "The task of estimating the probability or likelihood that an edge exists or will form between two nodes.",
            "definition": "Given an observed graph G = (V, E_obs), score candidate node pairs (u, v) in V x V using a decoding function s(u, v) = g(z_u, z_v) to predict unobserved edges or future link formation, calibrated via binary logistic loss against positive edges and sampled negative pairs.",
            "analogy": "A matchmaker evaluating two people's personalities and shared friend networks to predict whether they would form a successful long-term relationship.",
            "why_it_matters": "Powers e-commerce recommendation systems ('Customers who bought X also bought Y'), social friend suggestions ('People You May Know'), and biomedical drug-target discovery."
        },
        {
            "term": "Message-Passing Edge Masking (Anti-Leakage)",
            "what_is_it": "The strict operational separation between graph topology used for feature propagation versus candidate edges used for supervision loss.",
            "definition": "The hygiene protocol ensuring that edges held out for validation or testing E_test are completely removed from the message-passing adjacency matrix A_train used by the GNN encoder: E_message = E_train, preventing the target relationship from leaking into node embeddings during evaluation.",
            "analogy": "Hiding the answers at the back of a math textbook before handing the test to a student, so they cannot simply copy the solution directly from the paper.",
            "why_it_matters": "Failing to remove test edges results in catastrophic data leakage: the model trivially detects connections because the edge was literally present during message aggregation, resulting in 99% validation scores that crash in production."
        },
        {
            "term": "Negative Edge Sampling",
            "what_is_it": "Selecting pairs of nodes that do not have an observed edge to serve as negative training examples.",
            "definition": "The procedure of uniformly sampling a set of non-connected vertex pairs S_neg subset {(u, v) in V x V : (u, v) not in E_obs} to assign label y_uv = 0, balancing the observed positive edges (y_uv = 1) in the binary cross-entropy loss under the open-world assumption.",
            "analogy": "Showing a student examples of incorrect puzzle connections alongside correct ones so they learn how to distinguish valid matches from mismatches.",
            "why_it_matters": "Real-world graphs only record observed positive connections; negative sampling creates the necessary contrastive signal for binary classification and metric learning."
        },
        {
            "term": "Dot-Product Decoder (z_u^T z_v)",
            "what_is_it": "A fast, parameter-free link decoder that scores node affinity using vector dot product.",
            "definition": "A pairwise scoring operator computing raw logit s(u, v) = z_u^T z_v = sum_{i=1}^d z_{ui} z_{vi}, mapped to probability p(u, v) = sigma(s(u, v)); symmetric (s(u, v) = s(v, u)) and ideal for undirected homophilous networks.",
            "analogy": "Checking how aligned two compass needles are: when both point in the same direction, the alignment score is high; when orthogonal, the score is zero.",
            "why_it_matters": "Computationally lightweight, requires zero additional parameters, and allows ultra-fast approximate nearest neighbor (ANN) retrieval at web scale."
        },
        {
            "term": "Pairwise MLP Decoder (MLP([z_u || z_v]))",
            "what_is_it": "A parameterized neural network decoder that models complex non-linear interactions between node pairs.",
            "definition": "A decoder that concatenates node representations [z_u || z_v] into a 2d vector and passes it through one or more feed-forward layers: s(u, v) = W_2 sigma(W_1 [z_u || z_v] + b_1) + b_2, capable of modeling asymmetric directed relationships.",
            "analogy": "A specialized committee conducting a formal compatibility interview between two candidates rather than just comparing their resumes side-by-side.",
            "why_it_matters": "Essential for directed graphs, heterogeneous bipartite networks (user-product interactions), and knowledge graphs where relationships are inherently asymmetric."
        }
    ],
    "symbol_guide": [
        {
            "symbol": "H = f_theta(X, A)",
            "name": "GNN Node Embedding Matrix",
            "meaning": "The N x d matrix of learned node representations generated by the GNN encoder (GCN, GAT, or GraphSAGE).",
            "plain_english": "The vector summaries for all nodes produced by message passing across the graph."
        },
        {
            "symbol": "s(u, v) = z_u^T z_v",
            "name": "Dot-Product Link Score Logit",
            "meaning": "Raw alignment score between node u's embedding z_u and node v's embedding z_v before sigmoid normalization.",
            "plain_english": "How well the profile vectors of node u and node v match."
        },
        {
            "symbol": "W_c in R^{d x C}",
            "name": "Node Classification Head Weights",
            "meaning": "Trainable weight matrix projecting d-dimensional node embeddings to C class logits.",
            "plain_english": "The final classifier weights that convert node embeddings into category scores."
        },
        {
            "symbol": "train_mask / val_mask / test_mask",
            "name": "Node / Edge Split Masks",
            "meaning": "Boolean tensors indexing which nodes or edges participate in training loss, validation tuning, or test evaluation.",
            "plain_english": "Checklists indicating which items are used for study, practice tests, and the final exam."
        },
        {
            "symbol": "S_neg",
            "name": "Sampled Negative Edge Set",
            "meaning": "Set of non-connected node pairs (u, v) treated as label y_uv = 0 for contrastive training.",
            "plain_english": "Randomly chosen pairs of entities that do NOT have a connection in the graph."
        },
        {
            "symbol": "L_node",
            "name": "Node Classification Cross-Entropy Loss",
            "meaning": "Supervised multiclass loss computed exclusively over labeled nodes in V_train: -sum y_ic log(p_ic).",
            "plain_english": "Penalty incurred when the model guesses the wrong category for a training node."
        },
        {
            "symbol": "L_link",
            "name": "Link Prediction BCEWithLogits Loss",
            "meaning": "Binary cross-entropy loss over positive edges and sampled negative pairs: -1/M sum [y log sigma(s) + (1-y) log (1-sigma(s))].",
            "plain_english": "Penalty incurred when the model misjudges whether a pair of nodes should be connected."
        }
    ],
    "formula": "$$\\text{GNN Node Representation: } H = f_\\theta(X, A) \\in \\mathbb{R}^{N \\times d}$$\n\n$$\\text{Node Classification Head: } Z = H W_c \\in \\mathbb{R}^{N \\times C}, \\quad \\hat{y}_v = \\text{Softmax}(Z_v)$$\n\n$$\\text{Node Cross-Entropy Loss: } \\mathcal{L}_{\\text{node}} = -\\frac{1}{|\\mathcal{V}_{\\text{train}}|} \\sum_{v \\in \\mathcal{V}_{\\text{train}}} \\sum_{c=1}^C y_{vc} \\log \\hat{y}_{vc}$$\n\n$$\\text{Dot-Product Link Score: } s(u, v) = \\mathbf{z}_u^\\top \\mathbf{z}_v, \\quad p(u, v) = \\sigma\\left( s(u, v) \\right) = \\frac{1}{1 + e^{-s(u, v)}}$$\n\n$$\\text{Pairwise MLP Link Score: } s(u, v) = W_2 \\sigma\\left( W_1 [\\mathbf{z}_u \\parallel \\mathbf{z}_v] + \\mathbf{b}_1 \\right) + b_2$$\n\n$$\\text{Link BCEWithLogits Loss: } \\mathcal{L}_{\\text{link}} = -\\frac{1}{M} \\sum_{(u, v) \\in \\mathcal{E}_{\\text{train}} \\cup \\mathcal{S}_{\\text{neg}}} \\left[ y_{uv} \\log \\sigma(s_{uv}) + (1 - y_{uv}) \\log (1 - \\sigma(s_{uv})) \\right]$$\n\n$$\\text{Multi-Task Joint Objective: } \\mathcal{L}_{\\text{total}} = \\lambda_{\\text{node}} \\mathcal{L}_{\\text{node}} + \\lambda_{\\text{link}} \\mathcal{L}_{\\text{link}}$$\n\n$$\\text{Ranking Metrics: } \\text{Hits}@K = \\frac{1}{|\\mathcal{E}_{\\text{test}}|} \\sum_{(u, v) \\in \\mathcal{E}_{\\text{test}}} \\mathbb{I}\\left( \\text{rank}(u, v) \\le K \\right), \\quad \\text{MRR} = \\frac{1}{|\\mathcal{E}_{\\text{test}}|} \\sum_{(u, v)} \\frac{1}{\\text{rank}(u, v)}$$",
    "logic": "The core design philosophy unifying Node Classification and Link Prediction pipelines is architectural decoupling: the Graph Neural Network (GCN, GAT, GraphSAGE) serves as a universal geometric representation backbone that compresses irregular graph connectivity and rich node attributes into continuous d-dimensional latent vectors H = f_theta(X, A). Once embeddings are computed, task-specific prediction heads and loss functions take over.\n\nIn Node Classification, each node embedding z_v is projected into class logits Z_v = z_v W_c. In standard transductive settings, the full graph adjacency matrix A and feature matrix X are visible to the message-passing layers during both training and evaluation, but loss gradients are restricted strictly to labeled nodes using boolean masks: train_mask selects which loss terms backpropagate into theta and W_c. The unlabelled validation and test nodes still actively propagate messages to assist their neighbors, but their own labels are never exposed during optimization.\n\nIn Link Prediction, the task shifts from classifying an isolated vector to evaluating a pairwise relationship between two vectors (z_u, z_v). This introduces fundamental differences in data preparation: (1) Anti-Leakage Edge Splitting: The observed edges E must be partitioned into E_train, E_val, and E_test. Crucially, during the forward pass of the GNN encoder, the message-passing graph edge_index must ONLY contain E_train. If test edges E_test were left in edge_index, the GNN would propagate messages directly across the edge it is asked to predict, resulting in 100% training accuracy that immediately collapses on real unobserved data. For undirected graphs, both (u, v) and (v, u) directions must be removed. (2) Negative Sampling: Because real graphs only contain observed positive edges (label 1), the training pipeline must sample non-edges (label 0) to provide contrastive supervision. Under the open-world assumption, an unobserved edge is not guaranteed to be impossible; it may simply be yet unformed. (3) Severe Class Imbalance: In a graph with N nodes, there are N(N-1)/2 candidate pairs, of which only a tiny fraction (often < 0.1%) are real edges. Consequently, standard accuracy is completely uninformative (a dummy model predicting 'no link' gets 99.9% accuracy). Robust link evaluation relies on Precision-Recall AUC (PR-AUC), ROC-AUC, and ranking metrics such as Hits@K and Mean Reciprocal Rank (MRR).",
    "example": "Consider a financial fraud detection pipeline monitoring 1,000,000 accounts on an e-commerce payment platform. Node features include [account_age, 30_day_volume, chargeback_count], and edges represent transaction fund transfers. The engineering team deploys a unified 2-layer GraphSAGE backbone with two task heads: (1) Node Classification: Identifies compromised or mule accounts using cross-entropy loss against 5,000 confirmed fraud labels from compliance audits; (2) Link Prediction: Predicts hidden collusion links between unlinked accounts using dot-product decoding against observed transactions and sampled negative account pairs. By joint training, the shared GNN representations capture both account-level suspicious behavior and relational laundering rings, stopping $4.2M in unauthorized transfers within 30 days.",
    "numerical_example": "Step 1: Node Classification Worked Example (5 Accounts, 3 Features, Train/Val/Test Masks)\nSetup: 5 account nodes with 3 raw features:\n  Node 0: [10, 100, 2] (Normal, class 0)\n  Node 1: [20, 200, 4] (Normal, class 0)\n  Node 2: [80, 900, 1] (Suspicious, class 1)\n  Node 3: [15, 150, 3] (Normal, class 0 - Validation)\n  Node 4: [90, 950, 1] (Suspicious, class 1 - Test)\n\nMasks:\n  train_mask = [True,  True,  True,  False, False]  (Nodes 0, 1, 2 used for loss)\n  val_mask   = [False, False, False, True,  False]  (Node 3 used for model checkpointing)\n  test_mask  = [False, False, False, False, True ]  (Node 4 reserved for final score)\n\nClassification Step:\n  Embedding H in R^{5 x 2}, Classifier W_c in R^{2 x 2}.\n  Suppose for Node 4, embedding is z_4 = [2.5, -1.2] and W_c = [[1.0, -1.0], [-1.0, 1.0]].\n  Logits = z_4 @ W_c = [2.5(1) + (-1.2)(-1), 2.5(-1) + (-1.2)(1)] = [2.5 + 1.2, -2.5 - 1.2] = [3.7, -3.7].\n  Class 0 Logit = 3.7, Class 1 Logit = -3.7.\n  Softmax Probability P(Class 0) = exp(3.7) / (exp(3.7) + exp(-3.7)) = 40.45 / (40.45 + 0.025) = 0.9994.\n\nStep 2: Link Prediction Worked Numerical Example (Matching Lesson Walkthrough)\nSetup: Given learned 2D embeddings for candidate nodes u and v:\n  z_u = [1.0, 2.0]\n  z_v = [2.0, 1.0]\n\n  Step 2a: Compute raw dot-product logit s(u, v)\n    s(u, v) = z_u^T z_v = (1.0 * 2.0) + (2.0 * 1.0) = 2.0 + 2.0 = 4.0\n\n  Step 2b: Apply sigmoid function to obtain link probability\n    p(u, v) = sigma(4.0) = 1 / (1 + exp(-4.0)) = 1 / (1 + 0.0183156) = 1 / 1.0183156 approx 0.9820 (98.2%)\n\n  Step 2c: Compute BCEWithLogits Loss for this positive link (y_uv = 1.0)\n    Loss = - [ 1.0 * log(0.9820) + 0.0 * log(1 - 0.9820) ] = - log(0.9820) = - (-0.01817) = 0.0182.\n    A very small loss because the model correctly predicted high probability for a real edge.\n\nStep 3: Complete PyTorch Implementation (Node Classification + Link Prediction Pipeline)\n```python\nimport torch\nimport torch.nn as nn\nimport torch.nn.functional as F\n\n# --- 1. Graph Setup (5 Nodes, 3 Features) ---\nX = torch.tensor([\n    [10., 100., 2.],\n    [20., 200., 4.],\n    [80., 900., 1.],\n    [15., 150., 3.],\n    [90., 950., 1.]\n])\nlabels = torch.tensor([0, 0, 1, 0, 1])  # 0 = normal, 1 = suspicious\n\n# Message passing edges (OBSERVED during encoding - anti-leakage enforced)\n# Edges: 0-1, 1-2, 2-3 (undirected)\nedge_index = torch.tensor([\n    [0, 1, 1, 2, 2, 3, 1, 0, 2, 1, 3, 2],\n    [1, 0, 2, 1, 3, 2, 0, 1, 1, 2, 2, 3]\n])\n\n# Masks for Node Classification\ntrain_mask = torch.tensor([True,  True,  True,  False, False])\nval_mask   = torch.tensor([False, False, False, True,  False])\ntest_mask  = torch.tensor([False, False, False, False, True])\n\n# Link supervision candidate pairs (source, destination, label)\n# Pair (0, 1) = positive (label 1), Pair (0, 4) = negative non-edge (label 0)\ntrain_pairs = torch.tensor([[0, 1], [0, 4], [1, 2], [1, 4]])\ntrain_link_labels = torch.tensor([1., 0., 1., 0.])\n\n# --- 2. GNN Encoder & Prediction Heads ---\nclass SimpleGNNEncoder(nn.Module):\n    def __init__(self, in_features, hidden_dim):\n        super().__init__()\n        self.linear = nn.Linear(in_features, hidden_dim)\n    def forward(self, x, edges):\n        # Simple mean message-passing aggregation\n        h = self.linear(x)\n        src, dst = edges[0], edges[1]\n        out = h.clone()\n        out.index_add_(0, dst, h[src])\n        return F.relu(out)\n\nclass JointGraphPipeline(nn.Module):\n    def __init__(self, in_features, hidden_dim, num_classes):\n        super().__init__()\n        self.encoder = SimpleGNNEncoder(in_features, hidden_dim)\n        self.node_classifier = nn.Linear(hidden_dim, num_classes)\n    def forward(self, x, edges):\n        z = self.encoder(x, edges)\n        return z\n    def decode_links(self, z, pairs):\n        src = z[pairs[:, 0]]\n        dst = z[pairs[:, 1]]\n        return (src * dst).sum(dim=1)  # Dot-product logits\n\n# --- 3. Combined Training Loop ---\nmodel = JointGraphPipeline(in_features=3, hidden_dim=4, num_classes=2)\noptimizer = torch.optim.Adam(model.parameters(), lr=0.02)\n\nfor epoch in range(100):\n    model.train()\n    optimizer.zero_grad()\n    embeddings = model(X, edge_index)\n\n    # Node classification loss\n    node_logits = model.node_classifier(embeddings)\n    node_loss = F.cross_entropy(node_logits[train_mask], labels[train_mask])\n\n    # Link prediction loss with BCEWithLogitsLoss\n    link_logits = model.decode_links(embeddings, train_pairs)\n    link_loss = F.binary_cross_entropy_with_logits(link_logits, train_link_labels)\n\n    # Joint loss\n    total_loss = node_loss + link_loss\n    total_loss.backward()\n    optimizer.step()\n\n# --- 4. Evaluation ---\nmodel.eval()\nwith torch.no_grad():\n    z = model(X, edge_index)\n    node_preds = model.node_classifier(z).argmax(dim=1)\n    test_node_acc = (node_preds[test_mask] == labels[test_mask]).float().mean().item()\n    test_link_probs = torch.sigmoid(model.decode_links(z, train_pairs))\n    print(f'Test Node Acc: {test_node_acc:.2f}')\n    print(f'Predicted Link Probabilities: {test_link_probs.tolist()}')\n```",
    "types_header": "Downstream Graph Learning Tasks & Decoders",
    "types_badge": "Task Paradigms",
    "quick_types": [
        {
            "type": "Node Classification Head",
            "name": "Node Classification Head",
            "definition": "A linear projection layer mapping node embeddings z_v to discrete class logits Z_v = z_v W_c, evaluated using multiclass cross-entropy loss over boolean train/val/test masks.",
            "description": "A linear projection layer mapping node embeddings z_v to discrete class logits Z_v = z_v W_c, evaluated using multiclass cross-entropy loss over boolean train/val/test masks.",
            "looks_like": "Softmax(Linear(z_v)) -> [p(Class 0), p(Class 1), ..., p(Class C)]"
        },
        {
            "type": "Dot-Product Link Decoder",
            "name": "Dot-Product Link Decoder",
            "definition": "Computes alignment between two node vectors via inner product: s(u, v) = z_u^T z_v. Symmetric, parameter-free, and ideal for homophilous undirected networks and fast vector search.",
            "description": "Computes alignment between two node vectors via inner product: s(u, v) = z_u^T z_v. Symmetric, parameter-free, and ideal for homophilous undirected networks and fast vector search.",
            "looks_like": "sigma(dot_product(z_u, z_v)) -> p(u, v) in [0, 1]"
        },
        {
            "type": "Pairwise MLP Link Decoder",
            "name": "Pairwise MLP Link Decoder",
            "definition": "Concatenates node vectors [z_u || z_v] and processes them through feed-forward layers: s(u, v) = MLP([z_u || z_v]). Capable of modeling asymmetric and directed relations.",
            "description": "Concatenates node vectors [z_u || z_v] and processes them through feed-forward layers: s(u, v) = MLP([z_u || z_v]). Capable of modeling asymmetric and directed relations.",
            "looks_like": "Linear(ReLU(Linear([z_u || z_v]))) -> logit"
        },
        {
            "type": "Graph-Level Readout (Pooling)",
            "name": "Graph-Level Readout (Pooling)",
            "definition": "Aggregates all node embeddings in an entire graph into a single vector h_G = Readout({h_v, forall v in V}) via sum, mean, or attention pooling for graph classification (e.g. molecular toxicity).",
            "description": "Aggregates all node embeddings in an entire graph into a single vector h_G = Readout({h_v, forall v in V}) via sum, mean, or attention pooling for graph classification (e.g. molecular toxicity).",
            "looks_like": "Readout([h_1, h_2, ..., h_N]) -> h_graph in R^d"
        }
    ],
    "connected_logic": [
        {
            "title": "Node Classification: Transductive Masking & Feature Propagation",
            "description": "How transductive training uses full-graph topology while strictly withholding supervision labels.",
            "content": "• In transductive node classification, all N nodes and their input features X participate in message passing across adjacency A.\n• Boolean masks (train_mask, val_mask, test_mask) decouple feature propagation from gradient computation.\n• Loss is computed only on train_mask nodes: L = -sum_{v in V_train} log p(y_v | X, A). Unlabeled nodes still pass messages to their neighbors, allowing semi-supervised signal to flow through graph edges.",
            "points": [
                "In transductive node classification, all N nodes and their input features X participate in message passing across adjacency A.",
                "Boolean masks (train_mask, val_mask, test_mask) decouple feature propagation from gradient computation.",
                "Loss is computed only on train_mask nodes: L = -sum_{v in V_train} log p(y_v | X, A). Unlabeled nodes still pass messages to their neighbors, allowing semi-supervised signal to flow through graph edges."
            ]
        },
        {
            "title": "Link Prediction: Strict Edge Splitting & Anti-Leakage Hygiene",
            "description": "Why candidate test edges must be completely purged from the message-passing adjacency graph.",
            "content": "• Observed edges E are partitioned into E_train (e.g. 70%), E_val (15%), and E_test (15%).\n• The GNN encoder's message-passing graph edge_index must contain ONLY E_train.\n• If test edge (u, v) is left in edge_index, the GNN encoder directly exchanges features between u and v, trivially leaking the target relation into their embeddings and destroying real-world predictive validity.\n• In undirected graphs, both (u, v) and (v, u) directions must be removed together.",
            "points": [
                "Observed edges E are partitioned into E_train (e.g. 70%), E_val (15%), and E_test (15%).",
                "The GNN encoder's message-passing graph edge_index must contain ONLY E_train.",
                "If test edge (u, v) is left in edge_index, the GNN encoder directly exchanges features between u and v, trivially leaking the target relation into their embeddings and destroying real-world predictive validity.",
                "In undirected graphs, both (u, v) and (v, u) directions must be removed together."
            ]
        },
        {
            "title": "Negative Sampling & The Open-World Assumption",
            "description": "Handling unobserved edges under the open-world assumption in real graphs.",
            "content": "• Real graphs exhibit positive-only observations: we know which users bought products, but an unobserved pair could simply be an undiscovered affinity rather than a true negative.\n• Negative sampling uniformly draws pairs (u, v) not in E_obs, treating them as label 0 for binary contrastive training.\n• In production recommender systems, hard negative sampling (selecting 2-hop unconnected pairs) forces the model to learn fine-grained discrimination beyond popularity bias.",
            "points": [
                "Real graphs exhibit positive-only observations: we know which users bought products, but an unobserved pair could simply be an undiscovered affinity rather than a true negative.",
                "Negative sampling uniformly draws pairs (u, v) not in E_obs, treating them as label 0 for binary contrastive training.",
                "In production recommender systems, hard negative sampling (selecting 2-hop unconnected pairs) forces the model to learn fine-grained discrimination beyond popularity bias."
            ]
        },
        {
            "title": "Evaluation Under Extreme Class Imbalance (AUC-ROC vs. PR-AUC & Hits@K)",
            "description": "Why standard accuracy fails and how to properly evaluate sparse link prediction pipelines.",
            "content": "• In a graph with 10,000 nodes, there are ~50 million possible pairs, of which only 50,000 are true edges (0.1% positive rate).\n• A naive model predicting 'no link' everywhere achieves 99.9% accuracy but provides zero utility.\n• For candidate classification, Precision-Recall AUC (PR-AUC) and F1-score evaluate performance without being inflated by overwhelming true negatives.\n• For ranking and retrieval, Hits@K (fraction of test edges ranked in top K candidates) and Mean Reciprocal Rank (MRR) evaluate real-world recommender utility.",
            "points": [
                "In a graph with 10,000 nodes, there are ~50 million possible pairs, of which only 50,000 are true edges (0.1% positive rate).",
                "A naive model predicting 'no link' everywhere achieves 99.9% accuracy but provides zero utility.",
                "For candidate classification, Precision-Recall AUC (PR-AUC) and F1-score evaluate performance without being inflated by overwhelming true negatives.",
                "For ranking and retrieval, Hits@K (fraction of test edges ranked in top K candidates) and Mean Reciprocal Rank (MRR) evaluate real-world recommender utility."
            ]
        }
    ],
    "pitfalls": [
        "Data Leakage from Test Edges in Message Passing: Including held-out target edges in the adjacency matrix allows the GNN to trivially pass messages across the link being evaluated; test edges must be strictly removed from message passing.",
        "Asymmetric Splitting in Undirected Graphs: Forgetting that (u, v) and (v, u) represent the same undirected edge; withholding only one direction leaves the reverse direction visible to the encoder.",
        "Treating Every Missing Link as a Definitive Negative: In real graphs (social networks, e-commerce), missing edges often represent unobserved future interactions rather than confirmed disinterest (Open-World Assumption).",
        "Tuning Hyperparameters on the Test Split: Modifying model architectures, threshold cutoffs, or loss weights based on test set metrics causes optimization leakage; always use validation masks for model selection.",
        "Ignoring Temporal Causality in Dynamic Graphs: Evaluating future link prediction with random edge splits allows the model to predict past connections using future graph state; always use time-respecting train/val/test splits.",
        "Relying on Accuracy Under Severe Class Imbalance: When only 0.1% of node pairs are connected, predicting 'no link' yields 99.9% accuracy but zero utility; rely on PR-AUC, F1-score, and Hits@K.",
        "Conflating Continuous Node Embeddings with Discrete Class Outputs: GNN encoders output dense vector representations; dedicated task heads (linear projection or MLP) with calibrated activations are required for downstream predictions."
    ],
    "key_takeaways": [
        "Node Classification predicts properties of individual nodes (Z = H W_c), while Link Prediction predicts pairwise relational likelihood (p = sigma(s(u, v))).",
        "Both tasks can share a unified GNN backbone encoder (GCN, GAT, GraphSAGE); only prediction heads, supervision labels, and loss functions differ.",
        "Anti-leakage edge hygiene is paramount in link prediction: test edges (both directions in undirected graphs) must be completely excised from the message-passing graph.",
        "Because graphs are sparse, standard accuracy is misleading; robust evaluation requires PR-AUC, F1-score, Hits@K, and Mean Reciprocal Rank (MRR)."
    ],
    "tags": [
        "Node Classification",
        "Link Prediction",
        "Graph Neural Networks",
        "Graph Pipelines",
        "Negative Sampling",
        "Data Leakage",
        "PyTorch Geometric",
        "Deep Learning"
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
