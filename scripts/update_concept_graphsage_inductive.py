# -*- coding: utf-8 -*-
"""
Script to modernize concept_graphsage_inductive in
src/data/concepts.json and scripts/data_sources/all_concepts.json.
"""

import json

new_concept = {
    "id": "concept_graphsage_inductive",
    "title": "Inductive Graph Representation (GraphSAGE)",
    "topic_id": "dl_gnn",
    "topic_label": "Graph Neural Networks (GNNs)",
    "category": "dl",
    "category_label": "Deep Learning Foundations",
    "raw_subtopic": "Inductive Graph Representation (GraphSAGE)",
    "raw_sub": "Inductive Graph Representation (GraphSAGE)",
    "def": "GraphSAGE (Graph Sample and Aggregate) is an inductive representation learning framework for dynamic and web-scale graphs that generates node embeddings by learning shared neighborhood aggregation and feature transformation functions rather than storing individual node lookup tables, scaling via localized fixed-size neighbor sampling.",
    "definition": "GraphSAGE (Hamilton et al., 2017) is an inductive framework for representation learning on large, dynamic, and evolving graphs. While traditional graph embedding algorithms (such as DeepWalk, node2vec, or transductive matrix factorization) learn a distinct embedding vector for each static node in an embedding table, GraphSAGE learns parameterized, generalizable aggregation and transformation functions that generate node representations on-the-fly from each node's local features and neighborhood topology. The GraphSAGE computation pipeline executes across four key stages: (1) Neighborhood Sampling: rather than computing over the entire, unbounded neighborhood of a node (which triggers exponential neighbor explosion in dense hub nodes), GraphSAGE uniformly samples a fixed number of neighbors S_k at each layer k; (2) Neighborhood Aggregation: a permutation-invariant aggregation operator (such as Mean, Pooling, or LSTM) collapses the sampled neighbor representations from layer k-1 into a single contextual neighborhood vector; (3) Ego-Neighbor Concatenation & Transformation: the node's own representation h_v^{k-1} is concatenated with the aggregated neighborhood vector [h_v^{k-1} || h_{N(v)}^k], multiplied by a trainable layer-specific weight matrix W^k, and passed through a non-linear activation (typically ReLU); and (4) Multilayer Receptive Field Expansion: repeating this process over K layers incorporates information from a K-hop sampled neighborhood. Because GraphSAGE learns shared aggregator parameters rather than node-specific vectors, it is fully inductive: newly added nodes (such as new social network users, new e-commerce products, or newly connected smart electricity meters) receive instant embeddings without retraining the model, requiring only their raw attributes and local network connections.",
    "simple_summary": "Think of traditional graph embeddings like a printed physical phonebook: every known resident has an entry, but if a new person moves into the neighborhood tomorrow, their name isn't in the book—you would have to reprint the entire directory from scratch (retrain the entire model). GraphSAGE takes an entirely different approach: instead of memorizing who everyone is, it learns a universal recipe for profiling anyone on demand. Its recipe is: 'Take this person's own resume, interview 10 of their closest colleagues, calculate their consensus opinion, glue the colleague consensus to their resume, and transform the combined profile through learned evaluation criteria.' When a brand-new electricity meter connects to an urban power grid tomorrow, GraphSAGE doesn't panic. It takes the meter's recent voltage and consumption readings, samples 5 nearby meters it connects to, averages their grid conditions, glues the two data streams together, and instantly outputs a high-quality embedding. Because it samples a fixed number of neighbors (say, 10 friends in layer 1 and 5 friends in layer 2) instead of querying thousands of connections, computation stays strictly bounded and fits comfortably on standard GPUs.",
    "definition_bullets": [
        "Inductive Paradigm: Learns shared aggregation and projection functions over local features and connections rather than memorizing fixed node embedding lookup tables.",
        "Four-Stage Pipeline: Neighbor sampling, neighborhood aggregation (Mean, Pooling, or LSTM), ego-neighbor feature concatenation, and non-linear weight transformation.",
        "Core Update Equation: h_v^(k) = sigma(W^(k) [h_v^(k-1) || AGG_k({h_u^(k-1) : u in N(v)})]), keeping the node's own signal separate from its neighborhood context.",
        "Fixed-Budget Neighborhood Sampling: Restricts neighbor expansion to a fixed sample size S_k per layer, bounding computational complexity and enabling mini-batch SGD on billion-node graphs.",
        "Zero-Retraining Inference: Instantly generates representations for previously unseen nodes added to dynamic graphs using only their raw attributes and accessible neighbors."
    ],
    "core_terms": [
        {
            "term": "Inductive Learning vs. Transductive Learning",
            "what_is_it": "The distinction between learning a generalizable representation function versus memorizing representations for a static, closed set of nodes.",
            "definition": "In transductive graph learning (DeepWalk, node2vec, standard matrix factorization), the model optimizes distinct embedding vectors for a fixed vertex set V; new nodes require retraining the entire model. In inductive learning (GraphSAGE), the model optimizes shared parameterized functions that map any node's features and sampled neighborhood into an embedding: f(x_v, N(v); Theta), instantly generalizing to unseen vertices.",
            "analogy": "Learning the culinary principles of baking cakes (inductive) so you can bake any new cake recipe, versus memorizing the taste of five specific cakes currently sitting in your refrigerator (transductive).",
            "why_it_matters": "Real-world web graphs, recommender systems, and IoT sensor networks evolve every second; models must handle new nodes in real-time without multi-hour retraining cycles."
        },
        {
            "term": "Neighborhood Sampling (S_k)",
            "what_is_it": "Uniformly sampling a fixed-size subset of neighbors at each message-passing layer to cap computation.",
            "definition": "Instead of aggregating over the full neighborhood N(v) whose size can range from 1 to 100,000+ (power-law degree distributions), GraphSAGE uniformly draws a fixed sample S_k (e.g., S_1 = 10, S_2 = 5) at layer k, ensuring a predictable receptive field size of Prod_{l=1}^K S_l per target node.",
            "analogy": "Polling 20 randomly selected citizens to gauge community sentiment instead of attempting to interview all 2 million city residents before making every decision.",
            "why_it_matters": "Eliminates the 'neighbor explosion' problem in dense graphs, bounds GPU memory consumption, and enables standard mini-batch stochastic gradient descent (SGD)."
        },
        {
            "term": "Ego-Neighbor Concatenation ([h_v || h_N(v)])",
            "what_is_it": "Gluing a node's own prior representation directly alongside its aggregated neighborhood representation.",
            "definition": "The operation [h_v^(k-1) || h_{N(v)}^k] that concatenates the node's ego-vector of dimension d with the neighborhood aggregate of dimension d into a 2d vector prior to linear projection W^k, preserving both ego-identity and relational context.",
            "analogy": "A job candidate's evaluation portfolio with two separate tabs: Tab A contains their personal exam scores, and Tab B contains letters of recommendation from colleagues—both tabs are reviewed simultaneously by the hiring panel.",
            "why_it_matters": "Prevents the node's own distinctive features from being diluted or washed out by neighbor averages, allowing the learned weights W^k to adaptively balance self-features against neighborhood influence."
        },
        {
            "term": "Mean Aggregator",
            "what_is_it": "The simplest and most efficient GraphSAGE aggregator that computes the element-wise average of neighbor representations.",
            "definition": "A neighborhood aggregation operator computing h_{N(v)}^k = (1 / |N(v)|) * sum_{u in N(v)} h_u^(k-1); when combined with self-concatenation, it serves as an efficient, highly performant inductive baseline.",
            "analogy": "A panel calculating the exact average score across all judges' scorecards for a contestant.",
            "why_it_matters": "Extremely fast, linear in neighbor count, requires no extra parameters inside the aggregator, and provides strong baseline performance across most homophilous graphs."
        },
        {
            "term": "Pooling Aggregator (MLP + Max-Pool)",
            "what_is_it": "A symmetric aggregator that feeds each neighbor vector through a shared feed-forward layer followed by element-wise max-pooling.",
            "definition": "A parameterized operator computing h_{N(v)}^k = max_{u in N(v)} { sigma(W_{pool} h_u^(k-1) + b) }, where max is applied element-wise across all neighbor feature dimensions, identifying the most salient signal per channel.",
            "analogy": "A team brainstorming session where each member proposes ideas, but the whiteboard records only the single best idea in each subject category.",
            "why_it_matters": "Captures distinct, non-linear aspects of neighborhood properties independently across feature dimensions, consistently outperforming simple linear averaging on complex multi-attribute graphs."
        },
        {
            "term": "LSTM Aggregator & Order Randomization",
            "what_is_it": "A highly expressive sequence-based aggregator applied to a randomly shuffled permutation of sampled neighbors.",
            "definition": "An aggregation function that feeds neighbor vectors sequentially into an LSTM cell: h_{N(v)}^k = LSTM([h_{pi(u)}^(k-1)]_{u in N(v)}), where pi is a uniform random permutation applied at each step to ensure symmetric invariance over unordered graph neighborhoods.",
            "analogy": "Reading a set of advisory notes in a randomly shuffled order through an analytical memory system so no individual contributor gets unfair priority.",
            "why_it_matters": "Offers the highest expressive capacity among aggregators, but requires explicit random neighbor shuffling to enforce permutation invariance on unordered graph neighborhoods."
        }
    ],
    "symbol_guide": [
        {
            "symbol": "h_v^(k)",
            "name": "Node v's Representation at Layer k",
            "meaning": "The d_k-dimensional hidden state vector for node v after k aggregation layers; h_v^(0) = x_v (raw input attributes).",
            "plain_english": "The learned profile of node v after incorporating k hops of network connections."
        },
        {
            "symbol": "N(v) / S_{N(v)}",
            "name": "Sampled Neighborhood of Node v",
            "meaning": "The uniformly sampled set of direct neighbors connected to node v at the current layer, capped at fixed budget S_k.",
            "plain_english": "A small, fixed random sample of connected neighbors (e.g., exactly 10 friends)."
        },
        {
            "symbol": "AGGREGATE_k",
            "name": "Neighborhood Aggregation Function",
            "meaning": "A permutation-invariant pooling operation (Mean, Pooling MLP, or Shuffled LSTM) summarizing neighbor states.",
            "plain_english": "The method used to combine all neighbor opinions into one summary vector."
        },
        {
            "symbol": "W^(k)",
            "name": "Trainable Weight Matrix at Layer k",
            "meaning": "A learnable matrix of dimensions (2 * d_{k-1}) x d_k projecting concatenated [ego || neighbor] representations.",
            "plain_english": "The learned parameters that decide how much weight to give self-features vs. neighbor context."
        },
        {
            "symbol": "||",
            "name": "Vector Concatenation Operator",
            "meaning": "Horizontal concatenation of two vectors side-by-side, doubling dimensionality from d to 2d before linear transformation.",
            "plain_english": "Stitching the node's own vector and the neighbor summary vector side-by-side."
        },
        {
            "symbol": "sigma",
            "name": "Non-linear Activation Function",
            "meaning": "Element-wise activation function applied to layer projections, almost universally chosen as ReLU: sigma(z) = max(0, z).",
            "plain_english": "The activation function that introduces non-linearity to learn complex patterns."
        },
        {
            "symbol": "S_k",
            "name": "Sampling Budget at Layer k",
            "meaning": "The hyperparameter specifying how many neighbors are sampled per node at hop k (e.g., S_1 = 10, S_2 = 5).",
            "plain_english": "The fixed number of neighbors to pick at each hop to keep calculations fast and predictable."
        }
    ],
    "formula": "$$\\text{Sampled Neighborhood Aggregation: } h_{\\mathcal{N}(v)}^{(k)} = \\text{AGGREGATE}_k\\left( \\left\\{ h_u^{(k-1)} : u \\in \\mathcal{S}_{\\mathcal{N}(v)} \\right\\} \\right)$$\n\n$$\\text{Concatenation & Layer Update: } h_v^{(k)} = \\sigma\\left( W^{(k)} \\cdot \\left[ h_v^{(k-1)} \\parallel h_{\\mathcal{N}(v)}^{(k)} \\right] \\right)$$\n\n$$\\text{Mean Aggregator: } h_{\\mathcal{N}(v)}^{(k)} = \\frac{1}{|\\mathcal{S}_{\\mathcal{N}(v)}|} \\sum_{u \\in \\mathcal{S}_{\\mathcal{N}(v)}} h_u^{(k-1)}$$\n\n$$\\text{Pooling Aggregator: } h_{\\mathcal{N}(v)}^{(k)} = \\max_{u \\in \\mathcal{S}_{\\mathcal{N}(v)}} \\left\\{ \\sigma\\left( W_{\\text{pool}} h_u^{(k-1)} + \\mathbf{b} \\right) \\right\\}$$\n\n$$\\text{LSTM Aggregator: } h_{\\mathcal{N}(v)}^{(k)} = \\text{LSTM}\\left( \\left[ h_{\\pi(u)}^{(k-1)} \\right]_{u \\in \\mathcal{S}_{\\mathcal{N}(v)}} \\right), \\quad \\pi \\sim \\text{Uniform Permutations}$$\n\n$$\\text{GCN-Style Aggregator: } h_v^{(k)} = \\sigma\\left( W \\cdot \\frac{1}{|\\mathcal{N}(v) \\cup \\{v\\}|} \\left( h_v^{(k-1)} + \\sum_{u \\in \\mathcal{N}(v)} h_u^{(k-1)} \\right) \\right)$$\n\n$$\\text{Computation Tree Size (K Layers): } |\\mathcal{V}_{\\text{tree}}(v)| \\le 1 + S_1 + S_1 S_2 + \\dots + \\prod_{k=1}^K S_k$$",
    "logic": "GraphSAGE resolves the fundamental scalability and inductive generalization bottlenecks of traditional Graph Neural Networks. In standard full-graph GCNs, computing a single node's representation requires accessing the entire adjacency matrix and propagating information across all nodes simultaneously. If a new node joins the network, the adjacency matrix shape changes, and node embeddings cannot be generated without re-running or retraining across the entire graph. Furthermore, for nodes with high degrees (such as celebrity accounts with millions of followers or high-capacity power substations), aggregating all neighbors becomes computationally prohibitive and causes explosive memory footprint O(d^K) across K layers.\n\nGraphSAGE solves this with two foundational innovations: (1) Parameterized Inductive Functions: Instead of learning static node embeddings, GraphSAGE trains shared aggregation functions (AGGREGATE) and projection weight matrices (W^(k)). These functions operate purely on a node's input features and its neighbors' feature distributions. At test time, an unseen node with known features and local edges can immediately pass through the trained pipeline to produce an embedding without modifying or retraining model weights. (2) Bounded Neighborhood Sampling: GraphSAGE samples a fixed, uniform number of neighbors S_k at each layer (e.g., S_1 = 10, S_2 = 5). This constructs a bounded, tree-structured computation graph rooted at target node v with a predictable maximum size of 1 + S_1 + S_1*S_2 nodes. This enables standard mini-batch stochastic gradient descent (SGD), allowing models to train on massive web-scale graphs with billions of edges on single GPUs.\n\nA crucial structural design in GraphSAGE is concatenation [h_v^(k-1) || h_{N(v)}^k] rather than simple summation or averaging. Suppose a node represents an electricity meter: its own features capture its recent voltage spikes and consumption levels, while its neighbors' aggregate captures regional power grid conditions. Concatenation guarantees that the model preserves both ego-state and neighborhood context separately, allowing the learned weights W^(k) to discover whether an anomaly is localized to the individual meter or widespread across the electrical feeder.",
    "example": "Consider an industrial smart electricity grid monitoring 500,000 smart meters across a metropolitan area. Each meter has features [voltage_variance, power_factor, active_load, harmonic_distortion]. The utility company trains a 2-layer GraphSAGE model with sampling budgets S_1 = 10 and S_2 = 5 to classify meters as 'normal', 'phase-fault', or 'power-theft'. During training, meters in District A are processed using mini-batch SGD. Next month, District B activates 10,000 brand-new meters that were never seen during training. Because GraphSAGE is inductive, the utility does not retrain the network: each new meter's raw sensor readings and connections to 10 neighboring meters are fed into the frozen MeanGraphSAGE layer, generating instant embeddings that correctly isolate an illegal bypass line within 50 milliseconds of commissioning.",
    "numerical_example": "Step 1: One-Layer Mean-Aggregator Numerical Calculation (Matching Lesson Walkthrough)\nSetup: Target node v has one-dimensional feature h_v^(0) = 4.\nTwo sampled neighbors: Neighbor u_1 with h_{u1}^(0) = 2, Neighbor u_2 with h_{u2}^(0) = 6.\nLearnable weights W = [0.5, 1.0]^T, bias b = 0, activation sigma = ReLU.\n\n  Step 1a: Compute the neighbor mean aggregate h_{N(v)}^(1)\n    h_{N(v)}^(1) = (h_{u1}^(0) + h_{u2}^(0)) / 2 = (2 + 6) / 2 = 8 / 2 = 4.0\n\n  Step 1b: Concatenate the node's own value with the neighbor aggregate\n    [h_v^(0) || h_{N(v)}^(1)] = [4.0, 4.0]  (dimension: 1 + 1 = 2)\n\n  Step 1c: Apply learned linear transformation W and ReLU activation\n    Linear product = [4.0, 4.0] @ [0.5, 1.0]^T\n                   = (4.0 * 0.5) + (4.0 * 1.0)\n                   = 2.0 + 4.0 = 6.0\n    h_v^(1) = ReLU(6.0) = 6.0\n\n  Key Insight: Notice that while the neighbor mean alone was 4.0, the updated representation is 6.0.\n  Because concatenation preserves the node's own value (4.0 * 0.5 = 2.0) alongside neighbor context (4.0 * 1.0 = 4.0),\n  the learned transformation adapts how much influence self-state vs. local context commands.\n\nStep 2: Two-Layer Neighborhood Expansion Budget\nSuppose a target node has sampling configuration:\n  Layer 1: S_1 = 10 sampled neighbors per node.\n  Layer 2: S_2 = 5 sampled neighbors per node.\nTotal computation tree size for 1 target node:\n  - Target node: 1 node\n  - Layer 1 sampled neighbors: 10 nodes\n  - Layer 2 sampled occurrences: 10 * 5 = 50 node occurrences\n  Total sampled occurrences = 1 + 10 + 50 = 61 node occurrences (upper bound; unique nodes may be fewer due to overlap).\n  Contrast with full-graph GCN on a hub with 2,000 neighbors: requires 2,000 + 2,000 * 2,000 = 4,002,001 nodes (explosion!).\n\nStep 3: Complete PyTorch Implementation (MeanGraphSAGELayer)\n```python\nimport torch\nimport torch.nn as nn\nimport torch.nn.functional as F\n\nclass MeanGraphSAGELayer(nn.Module):\n    def __init__(self, in_features, out_features):\n        super().__init__()\n        # Concatenation of [self || neighbors] requires 2 * in_features input dimension\n        self.linear = nn.Linear(2 * in_features, out_features)\n\n    def forward(self, x, neighbors):\n        # x: [num_nodes, in_features]\n        # neighbors: list of neighbor-index lists per node\n        aggregated = []\n        for node_neighbors in neighbors:\n            if len(node_neighbors) == 0:\n                # Zero vector if no neighbors are available\n                mean_neighbor = x.new_zeros(x.size(1))\n            else:\n                mean_neighbor = x[node_neighbors].mean(dim=0)\n            aggregated.append(mean_neighbor)\n\n        neighbor_features = torch.stack(aggregated)\n        # Concatenate own features and neighbor information along feature dimension\n        combined = torch.cat([x, neighbor_features], dim=1)\n        return F.relu(self.linear(combined))\n\n# --- Demonstration on 3 Training Nodes ---\n# X: Node 0 (feature=4.0), Node 1 (feature=2.0), Node 2 (feature=6.0)\nX = torch.tensor([[4.0], [2.0], [6.0]])\n# Graph connections: Node 0 connects to [1, 2]; Nodes 1 & 2 connect to [0]\nneighbors = [[1, 2], [0], [0]]\n\nlayer = MeanGraphSAGELayer(in_features=1, out_features=2)\noutput = layer(X, neighbors)\nprint('Output shape:', output.shape)  # torch.Size([3, 2])\n\n# --- Step 4: Inductive Inference on a Brand New Unseen Node 3 ---\n# Node 3 connects to existing Node 0 and Node 1 with new raw feature [5.0]\nx_new = torch.tensor([[5.0]])\nX_extended = torch.cat([X, x_new], dim=0)  # Shape: [4, 1]\nneighbors_new = [[1, 2], [0], [0], [0, 1]]  # Node 3 has neighbors [0, 1]\n\n# Compute embedding for new node 3 using FROZEN layer weights without retraining!\noutput_inductive = layer(X_extended, neighbors_new)\nprint('Unseen Node 3 embedding:', output_inductive[3])\n```",
    "types_header": "GraphSAGE Aggregators & Graph Learning Paradigms",
    "types_badge": "Framework Taxonomy",
    "quick_types": [
        {
            "type": "Mean Aggregator",
            "name": "Mean Aggregator",
            "definition": "Element-wise average of sampled neighbor representations: h_N(v) = (1/|N(v)|) sum h_u. Simple, parameter-free within aggregation, and mathematically equivalent to a linear first-order approximation.",
            "description": "Element-wise average of sampled neighbor representations: h_N(v) = (1/|N(v)|) sum h_u. Simple, parameter-free within aggregation, and mathematically equivalent to a linear first-order approximation.",
            "looks_like": "mean([h_1, h_2, ..., h_k]) -> [avg_1, avg_2, ..., avg_d]"
        },
        {
            "type": "Pooling Aggregator (MLP + Max-Pool)",
            "name": "Pooling Aggregator (MLP + Max-Pool)",
            "definition": "Applies a shared fully connected layer to each neighbor vector followed by element-wise max-pooling: max_{u} { sigma(W_pool h_u + b) }. Captures distinct dominant patterns across feature dimensions.",
            "description": "Applies a shared fully connected layer to each neighbor vector followed by element-wise max-pooling: max_{u} { sigma(W_pool h_u + b) }. Captures distinct dominant patterns across feature dimensions.",
            "looks_like": "max_elementwise(ReLU(W_pool @ h_u + b))"
        },
        {
            "type": "LSTM Aggregator",
            "name": "LSTM Aggregator",
            "definition": "Processes sampled neighbor vectors sequentially using a Long Short-Term Memory cell. Delivers high expressive capacity; requires randomly shuffling neighbor order to enforce permutation invariance.",
            "description": "Processes sampled neighbor vectors sequentially using a Long Short-Term Memory cell. Delivers high expressive capacity; requires randomly shuffling neighbor order to enforce permutation invariance.",
            "looks_like": "LSTM([h_{pi(1)}, h_{pi(2)}, ..., h_{pi(k)}]), pi ~ uniform permutation"
        },
        {
            "type": "GCN-Style Aggregator",
            "name": "GCN-Style Aggregator",
            "definition": "Combines a node's own representation directly into the neighborhood mean set {h_v} U {h_u} before applying a single weight matrix: sigma(W * mean({h_v} U N(v))), mimicking Kipf & Welling GCN convolution.",
            "description": "Combines a node's own representation directly into the neighborhood mean set {h_v} U {h_u} before applying a single weight matrix: sigma(W * mean({h_v} U N(v))), mimicking Kipf & Welling GCN convolution.",
            "looks_like": "sigma(W @ mean([h_v, h_u1, h_u2, ...]))"
        }
    ],
    "connected_logic": [
        {
            "title": "Inductive vs. Transductive Representation Learning",
            "description": "Why learning functions scales to real-world evolving networks while embedding tables fail.",
            "content": "• Transductive algorithms (DeepWalk, node2vec, matrix factorization) optimize a direct lookup matrix E in R^{|V| x d}. Adding node |V|+1 leaves the table without a vector; generating one requires retraining the full matrix.\n• Inductive GraphSAGE learns parameterized aggregator functions AGG_k and weight matrices W^k. The learned weights are functions of local features and connectivity patterns, not node IDs.\n• An unseen node with known attributes and local connections can immediately pass through the trained network to generate an embedding on-the-fly without retraining.",
            "points": [
                "Transductive algorithms (DeepWalk, node2vec, matrix factorization) optimize a direct lookup matrix E in R^{|V| x d}. Adding node |V|+1 leaves the table without a vector; generating one requires retraining the full matrix.",
                "Inductive GraphSAGE learns parameterized aggregator functions AGG_k and weight matrices W^k. The learned weights are functions of local features and connectivity patterns, not node IDs.",
                "An unseen node with known attributes and local connections can immediately pass through the trained network to generate an embedding on-the-fly without retraining."
            ]
        },
        {
            "title": "Fixed-Budget Neighborhood Sampling & Mini-Batch SGD",
            "description": "How GraphSAGE breaks the exponential neighbor explosion problem in web-scale graphs.",
            "content": "• In standard GCNs, high-degree hub nodes with thousands of edges cause exponential expansion O(d^L) across L layers, exhausting GPU memory during full-graph batching.\n• GraphSAGE uniformly samples a fixed number of neighbors S_l at each hop l (e.g., S_1 = 10, S_2 = 5), bounding the computation tree per target node to Prod_{l=1}^L S_l.\n• This predictable tree size enables standard mini-batch SGD: batches of 512 target nodes can be trained independently on standard GPUs, scaling to graphs with billions of edges (such as Pinterest PinSage).",
            "points": [
                "In standard GCNs, high-degree hub nodes with thousands of edges cause exponential expansion O(d^L) across L layers, exhausting GPU memory during full-graph batching.",
                "GraphSAGE uniformly samples a fixed number of neighbors S_l at each hop l (e.g., S_1 = 10, S_2 = 5), bounding the computation tree per target node to Prod_{l=1}^L S_l.",
                "This predictable tree size enables standard mini-batch SGD: batches of 512 target nodes can be trained independently on standard GPUs, scaling to graphs with billions of edges (such as Pinterest PinSage)."
            ]
        },
        {
            "title": "Ego-Neighbor Feature Concatenation vs. Averaging",
            "description": "Why preserving the node's own representation separate from its neighborhood is crucial.",
            "content": "• Simple averaging replaces a node's features with the average of its neighbors, diluting personal anomalies in dense neighborhoods.\n• GraphSAGE concatenates [h_v^(k-1) || h_{N(v)}^k], doubling feature dimensions before applying linear projection W^k.\n• This lets the model learn distinct weights for self-state vs. neighborhood state: W^k [h_v || h_{N(v)}] = W_self h_v + W_neigh h_{N(v)}, allowing the network to retain ego-specific anomalies even in dense clusters.",
            "points": [
                "Simple averaging replaces a node's features with the average of its neighbors, diluting personal anomalies in dense neighborhoods.",
                "GraphSAGE concatenates [h_v^(k-1) || h_{N(v)}^k], doubling feature dimensions before applying linear projection W^k.",
                "This lets the model learn distinct weights for self-state vs. neighborhood state: W^k [h_v || h_{N(v)}] = W_self h_v + W_neigh h_{N(v)}, allowing the network to retain ego-specific anomalies even in dense clusters."
            ]
        },
        {
            "title": "Zero-Retraining Dynamic Inference on Unseen Nodes",
            "description": "The exact operational pipeline for generating embeddings on newly joined graph vertices.",
            "content": "• When a new node joins (e.g., a new social user or new smart meter), extract its raw feature vector x_new in R^{d_0} using identical feature extractors.\n• Identify its accessible connected neighbors N(new) in the current graph.\n• Pass x_new and sampled neighbors through the frozen trained aggregators and weight matrices W^1, ..., W^K.\n• The resulting embedding can be fed directly to a frozen classification head or vector index (ANN) without retraining.",
            "points": [
                "When a new node joins (e.g., a new social user or new smart meter), extract its raw feature vector x_new in R^{d_0} using identical feature extractors.",
                "Identify its accessible connected neighbors N(new) in the current graph.",
                "Pass x_new and sampled neighbors through the frozen trained aggregators and weight matrices W^1, ..., W^K.",
                "The resulting embedding can be fed directly to a frozen classification head or vector index (ANN) without retraining."
            ]
        }
    ],
    "pitfalls": [
        "Confusing Sampling with Learning: Sampling chooses which subset of neighbors to query; the learned aggregator and projection matrices determine how representations are combined and transformed.",
        "Assuming an Unseen Node Needs No Data: Inductive models are not psychic; computing an embedding for a new node requires its raw input features and local connected edges in the graph.",
        "Averaging Away the Node's Own Information: Omitting concatenation and replacing a node's representation with neighbor averages destroys ego-state; concatenation [h_v || h_{N(v)}] preserves both signals.",
        "Using the LSTM Aggregator Without Shuffling: LSTMs are sequence models that depend on input order; failing to uniformly randomize neighbor ordering introduces arbitrary sequence bias into an unordered graph neighborhood.",
        "Sampling Too Few Neighbors: Setting sample sizes too small (e.g., S=1 or S=2) reduces compute but introduces high gradient variance and omits crucial graph context.",
        "Inconsistent Feature Preprocessing: Raw features of new test nodes must undergo the exact same scaling, one-hot encodings, and imputation used during training; mismatched distributions degrade inductive embeddings.",
        "Conflating Node Embeddings with Class Predictions: GraphSAGE outputs dense continuous embeddings; a downstream classification head (linear layer + cross-entropy) is required for discrete labels."
    ],
    "key_takeaways": [
        "GraphSAGE operates inductively by learning reusable neighborhood aggregation and feature transformation functions rather than storing static node embeddings.",
        "Fixed-budget neighborhood sampling (e.g., S_1 = 10, S_2 = 5) prevents explosive neighborhood expansion on dense hubs, enabling scalable mini-batch SGD on billion-edge graphs.",
        "The core update h_v^(k) = sigma(W^(k) [h_v^(k-1) || AGG_k({h_u})]) concatenates ego-features with neighborhood context, ensuring node-specific signals are never washed out.",
        "Inductive inference generates representations for brand-new nodes on-the-fly without model retraining, requiring only their raw attributes and local connected edges."
    ],
    "tags": [
        "GraphSAGE",
        "Inductive Learning",
        "Neighborhood Sampling",
        "Graph Neural Networks",
        "Node Embedding",
        "PyTorch Geometric",
        "PinSage",
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
