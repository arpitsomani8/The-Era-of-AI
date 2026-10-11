# -*- coding: utf-8 -*-
"""
Script to modernize concept_graph_representations_adjacency in
src/data/concepts.json and scripts/data_sources/all_concepts.json.
"""

import json

new_concept = {
    "id": "concept_graph_representations_adjacency",
    "title": "Graph Representations, Adjacency Matrices & Node Features",
    "topic_id": "dl_gnn",
    "topic_label": "Graph Neural Networks (GNNs)",
    "category": "dl",
    "category_label": "Deep Learning Foundations",
    "raw_subtopic": "Graph Representations, Adjacency Matrices & Node Features",
    "def": "A graph G = (V, E) encodes pairwise relational structure through vertices V and edges E. The adjacency matrix A in R^{NxN} numerically encodes connectivity, with A_ij = 1 for edges and 0 otherwise (or weights for weighted graphs). The node feature matrix X in R^{NxF} assigns F-dimensional attribute vectors to each node. Together, A and X form the dual input representation consumed by every Graph Neural Network layer for neighborhood aggregation and feature transformation.",
    "definition": "In graph-structured machine learning, a graph G = (V, E) consists of a node set V = {v_1, ..., v_N} representing entities and an edge set E = {(v_i, v_j)} representing pairwise relationships. The complete combinatorial connectivity structure is encoded in the adjacency matrix A in R^{NxN}, where entry A_ij = 1 if an edge connects node i to node j, and A_ij = 0 otherwise. For undirected graphs, A is symmetric (A = A^T); directed graphs permit asymmetric matrices encoding one-way relationships. Weighted graphs generalize binary entries to real-valued weights reflecting edge strength, distance, or similarity. Beyond connectivity, each node v_i carries domain-specific attributes packed into row X_i of the feature matrix X in R^{NxF}, where F is the per-node feature dimensionality. Self-loops are incorporated by augmenting A with the identity matrix A_tilde = A + I, ensuring each node aggregates its own representation alongside neighbor contributions. The degree matrix D (diagonal, D_ii = sum_j A_ij) enables the symmetric GCN normalization A_hat = D_tilde^{-1/2} A_tilde D_tilde^{-1/2} that equalizes neighbor contributions across high- and low-degree nodes. For large-scale graphs where N can reach millions, dense matrix storage is replaced by edge-list representations (shape [2, |E|]) or sparse COO/CSR formats. Graph Neural Network layers consume (A, X) to perform neighborhood aggregation: each node's feature vector is updated by collecting, transforming, and summarizing the feature vectors of its neighbors as defined by A.",
    "simple_summary": "Imagine a city's electricity distribution network where each transformer substation is a node and each power cable between substations is an edge. To feed this network into a deep learning model, you cannot just dump a picture—you need mathematics. The adjacency matrix is like a spreadsheet with one row and one column per substation. You put a '1' wherever two substations are directly connected by a cable and '0' everywhere else. The node feature matrix is a second spreadsheet where each row corresponds to the same substation, and the columns record its attributes: average load, voltage level, installation year, anomaly history, and so on. Together, these two matrices let a Graph Neural Network answer questions that standard neural networks cannot: 'Is this substation behaving unusually given how its directly connected neighbors are behaving?' Normalization by node degree ensures busy, highly-connected hubs and quiet, isolated substations are treated fairly. For massive city-scale grids, we ditch the full matrix and instead just list the cable connections as pairs—this is the edge list format used by PyTorch Geometric.",
    "definition_bullets": [
        "Graph Formalism G = (V, E): Nodes V represent entities (users, meters, atoms) and edges E represent pairwise relationships (friendships, cables, chemical bonds).",
        "Adjacency Matrix A in R^{NxN}: Encodes connectivity as binary (0/1) or real-valued weights; symmetric for undirected graphs, asymmetric for directed; diagonal zeros unless self-loops are added.",
        "Node Feature Matrix X in R^{NxF}: Assigns an F-dimensional real-valued attribute vector to each of the N nodes; row ordering must exactly match the adjacency matrix's node ordering.",
        "Self-Loop Augmentation & GCN Normalization: A_tilde = A + I ensures nodes incorporate own features; A_hat = D_tilde^{-1/2} A_tilde D_tilde^{-1/2} normalizes by node degree to control aggregation scale.",
        "Sparse Edge-List Representation: For large N, stores only non-zero edge indices as a [2, |E|] tensor rather than a dense N x N matrix, critical for million-node graphs in PyTorch Geometric."
    ],
    "core_terms": [
        {
            "term": "Adjacency Matrix A",
            "what_is_it": "The primary N x N numerical encoding of graph connectivity structure.",
            "definition": "A real-valued matrix A in R^{NxN} where entry A_ij = 1 (or an edge weight) if an edge connects node i to node j, and A_ij = 0 otherwise; for undirected graphs A = A^T holds by definition.",
            "analogy": "A mileage table in a road atlas: rows are departure cities, columns are destination cities, and each cell shows the direct road distance (or 0 if no direct highway exists).",
            "why_it_matters": "Provides the complete relational blueprint that GNN layers use to determine which node feature vectors should be aggregated at each message-passing step."
        },
        {
            "term": "Node Feature Matrix X",
            "what_is_it": "An N x F matrix assigning attribute vectors to every node in the graph.",
            "definition": "A real-valued matrix X in R^{NxF} where row X_i in R^F is the feature vector of node i, encoding domain-specific attributes such as age, consumption, embedding, or one-hot category.",
            "analogy": "A patient record database where each row is one patient and each column is a clinical measurement; the hospital's ward adjacency (which wards are adjacent) is a separate structure.",
            "why_it_matters": "Supplies the raw information that GNN layers transform and propagate across graph edges; without X, the GNN would have no semantic signal beyond pure graph topology."
        },
        {
            "term": "Degree Matrix D",
            "what_is_it": "A diagonal N x N matrix recording each node's connection count.",
            "definition": "A diagonal matrix D in R^{NxN} where D_ii = sum_{j} A_ij equals the degree (number of neighbors) of node i; used to compute symmetric normalization of the adjacency matrix.",
            "analogy": "A flight-hub activity report: each airport has a diagonal cell showing how many direct routes it serves, encoding how well-connected it is.",
            "why_it_matters": "Enables GCN-style normalization that prevents highly connected nodes from dominating aggregation and low-degree nodes from receiving inflated signals."
        },
        {
            "term": "Symmetric GCN Normalization A_hat",
            "what_is_it": "The degree-normalized, self-loop-augmented adjacency matrix used in Graph Convolutional Networks.",
            "definition": "A_hat = D_tilde^{-1/2} A_tilde D_tilde^{-1/2}, where A_tilde = A + I and D_tilde is the degree matrix of A_tilde; entries A_hat_ij = 1 / sqrt(d_i * d_j) for connected nodes i and j.",
            "analogy": "Dividing each country's trade flow by the square root of both countries' total trade volumes, so large trading nations do not overwhelm small ones in global analysis.",
            "why_it_matters": "Ensures GNN feature propagation is scale-invariant with respect to node degree, preventing numerical explosion during deep stacking of graph convolutional layers."
        },
        {
            "term": "Edge-List / Sparse Graph Representation",
            "what_is_it": "A memory-efficient graph encoding storing only the indices of non-zero edges.",
            "definition": "A [2, |E|] integer tensor (or COO sparse format) listing source and destination node indices for each edge, supplemented by an optional edge-attribute tensor of shape [|E|, d_e].",
            "analogy": "A contact book recording only existing phone numbers rather than a full NxN table where 99.99% of cells would be empty and say 'no number'.",
            "why_it_matters": "Reduces memory from O(N^2) to O(|E|) and is the native format of PyTorch Geometric and DGL, enabling GNN training on real-world graphs with millions of nodes."
        }
    ],
    "symbol_guide": [
        {
            "symbol": "G = (V, E)",
            "name": "Graph",
            "meaning": "Mathematical graph with node set V = {v_1,...,v_N} and edge set E = {(v_i, v_j)}."
        },
        {
            "symbol": "A ∈ ℝ^{N×N}",
            "name": "Adjacency Matrix",
            "meaning": "N x N matrix encoding connectivity; A_ij = edge weight (or 1/0 for unweighted graphs)."
        },
        {
            "symbol": "X ∈ ℝ^{N×F}",
            "name": "Node Feature Matrix",
            "meaning": "Matrix of N node attribute vectors each of dimension F; row X_i is node i's features."
        },
        {
            "symbol": "D",
            "name": "Degree Matrix",
            "meaning": "Diagonal matrix where D_ii = sum_j A_ij; encodes node connectivity count."
        },
        {
            "symbol": "Ã = A + I",
            "name": "Self-Loop Augmented Adjacency",
            "meaning": "Adjacency with identity added; ensures nodes include their own representation during aggregation."
        },
        {
            "symbol": "Â = D̃^{-1/2} Ã D̃^{-1/2}",
            "name": "Normalized Adjacency (GCN)",
            "meaning": "Symmetric degree-normalized adjacency that controls information flow scale across node degrees."
        },
        {
            "symbol": "edge_index [2, |E|]",
            "name": "Edge-List Tensor",
            "meaning": "Sparse representation storing source and destination node indices for all |E| edges."
        }
    ],
    "formula": "$$\\text{Graph Definition: } G = (V, E), \\quad |V| = N, \\quad A \\in \\mathbb{R}^{N \\times N}, \\quad X \\in \\mathbb{R}^{N \\times F}$$\n\n$$\\text{Adjacency Entry (Unweighted): } A_{ij} = \\begin{cases} 1 & \\text{if } (v_i, v_j) \\in E \\\\ 0 & \\text{otherwise} \\end{cases}, \\quad \\text{Undirected: } A = A^\\top$$\n\n$$\\text{Node Degree: } d_i = \\sum_{j=1}^{N} A_{ij}, \\quad D_{ii} = d_i, \\quad D_{ij} = 0 \\text{ for } i \\neq j$$\n\n$$\\text{Self-Loop Augmentation: } \\tilde{A} = A + I_N, \\quad \\tilde{D}_{ii} = \\sum_{j} \\tilde{A}_{ij} = d_i + 1$$\n\n$$\\text{Symmetric GCN Normalization: } \\hat{A} = \\tilde{D}^{-1/2} \\tilde{A} \\tilde{D}^{-1/2}, \\quad \\hat{A}_{ij} = \\frac{\\tilde{A}_{ij}}{\\sqrt{\\tilde{d}_i \\cdot \\tilde{d}_j}}$$\n\n$$\\text{GCN Layer Update: } H^{(l+1)} = \\sigma\\left( \\hat{A} H^{(l)} W^{(l)} \\right), \\quad H^{(0)} = X$$",
    "logic": "Graph-structured data is pervasive across scientific and engineering domains: social networks, molecular chemistry, knowledge bases, power grids, and citation networks all share the property that entities have attributes and pairwise relationships simultaneously matter. Standard deep learning architectures—CNNs and transformers—assume inputs live on regular grids (pixels, tokens) or dense feature spaces. Graphs break this assumption: nodes have variable neighborhoods, and no global ordering exists across nodes. The adjacency matrix A and feature matrix X together constitute the minimal dual specification required by any graph learning algorithm. A captures who-is-connected-to-whom at the structural level; X captures what-each-entity-is at the attribute level. For undirected graphs, the symmetry property A = A^T reflects that relationships are mutual. Directed graphs permit A_ij = 1 while A_ji = 0, modeling asymmetric flows like web hyperlinks or payment transactions. Weighted graphs replace binary entries with real values representing edge capacities, affinities, or inverse distances. The degree matrix D, diagonal with D_ii = sum_j A_ij, measures each node's local connectivity. A hub node with 1000 connections would, without normalization, aggregate 1000 times more incoming information than a leaf node with 1 connection—causing gradient instabilities and biased representations. Symmetric GCN normalization A_hat = D_tilde^{-1/2} A_tilde D_tilde^{-1/2} addresses this by scaling each propagated message by 1/sqrt(d_i * d_j), distributing contributions proportionally to node degrees. Self-loops via A_tilde = A + I ensure a node's own feature vector participates in its aggregation, preventing purely neighbor-derived representations that lose the node's identity. For real-world scale graphs with millions of nodes, dense N x N matrix storage is infeasible. Sparse edge-list formats ([2, |E|] tensors in PyTorch Geometric) store only the O(|E|) non-zero entries, reducing memory from quadratic to linear in the number of edges.",
    "example": "Consider an electricity distribution network monitoring 5 transformer substations (A, B, C, D, E) connected by power cables. Each substation node carries features: [average_load_kWh, voltage_deviation_V, anomaly_count_30d, meter_age_years]. The adjacency matrix A records which substations share a direct cable. The feature matrix X rows encode each substation's sensor readings. A Graph Convolutional Network layer propagates: each substation computes a new embedding by summing the normalized feature vectors of its cable-connected neighbors plus its own features (via self-loop), then passes through a learnable weight matrix W and activation. A substation with consistently normal load surrounded by neighbors with anomalous spikes would develop an embedding distinguishable from an isolated anomalous substation—precisely the contextual awareness that makes GNNs superior to independent per-node classifiers for fault and theft detection.",
    "numerical_example": "Step 1: Build the Adjacency Matrix for the 5-Node Social Graph (Matching User Notes)\nNode order: A=0, B=1, C=2, D=3, E=4. Edges: (A,B), (B,C), (A,D), (C,D), (D,E).\nAdjacency Matrix A (5x5, undirected -> symmetric):\n       A  B  C  D  E\n  A  [ 0  1  0  1  0 ]\n  B  [ 1  0  1  0  0 ]\n  C  [ 0  1  0  1  0 ]\n  D  [ 1  0  1  0  1 ]\n  E  [ 0  0  0  1  0 ]\nVerify symmetry: A[0,1] = A[1,0] = 1 (A-B edge), A[3,4] = A[4,3] = 1 (D-E edge). Confirmed A = A^T.\n\nStep 2: Node Feature Matrix X (Matching User Notes)\nColumns: [Age, Weekly Hours Online].\nX:\n  A: [25, 10]\n  B: [32,  7]\n  C: [21, 15]\n  D: [40,  5]\n  E: [29,  8]\nShape: X in R^{5x2} (N=5 nodes, F=2 features). Critical: row 0 of A and row 0 of X both refer to node A.\n\nStep 3: Degree Computation & Degree Matrix D\n  Degrees: d_A = 2, d_B = 2, d_C = 2, d_D = 3, d_E = 1\n  D = diag([2, 2, 2, 3, 1])\n  D:\n  [ 2  0  0  0  0 ]\n  [ 0  2  0  0  0 ]\n  [ 0  0  2  0  0 ]\n  [ 0  0  0  3  0 ]\n  [ 0  0  0  0  1 ]\n\nStep 4: Self-Loop Augmentation A_tilde = A + I\n  A_tilde: add 1s along diagonal\n       A  B  C  D  E\n  A  [ 1  1  0  1  0 ]\n  B  [ 1  1  1  0  0 ]\n  C  [ 0  1  1  1  0 ]\n  D  [ 1  0  1  1  1 ]\n  E  [ 0  0  0  1  1 ]\n  Updated degrees D_tilde: d_A = 3, d_B = 3, d_C = 3, d_D = 4, d_E = 2\n\nStep 5: Symmetric GCN Normalization A_hat = D_tilde^{-1/2} A_tilde D_tilde^{-1/2}\n  D_tilde^{-1/2} = diag([1/sqrt(3), 1/sqrt(3), 1/sqrt(3), 1/sqrt(4), 1/sqrt(2)])\n                 = diag([0.5774, 0.5774, 0.5774, 0.5000, 0.7071])\n  Sample entry A_hat[A,B] (row 0, col 1):\n    A_hat[0,1] = D^{-1/2}[0,0] * A_tilde[0,1] * D^{-1/2}[1,1]\n               = 0.5774 * 1 * 0.5774 = 0.3333\n  Sample entry A_hat[A,A] (self-loop, row 0, col 0):\n    A_hat[0,0] = 0.5774 * 1 * 0.5774 = 0.3333\n  Sample entry A_hat[D,E] (row 3, col 4):\n    A_hat[3,4] = 0.5000 * 1 * 0.7071 = 0.3536\n\nStep 6: Python Implementation (Matching User Notes)\n```python\nimport numpy as np\n\n# Node order: A=0, B=1, C=2, D=3, E=4\nA = np.array([\n    [0, 1, 0, 1, 0],\n    [1, 0, 1, 0, 0],\n    [0, 1, 0, 1, 0],\n    [1, 0, 1, 0, 1],\n    [0, 0, 0, 1, 0]\n], dtype=np.float32)\n\nX = np.array([[25,10],[32,7],[21,15],[40,5],[29,8]], dtype=np.float32)\n\ndegrees = A.sum(axis=1)  # [2, 2, 2, 3, 1]\nA_tilde = A + np.eye(A.shape[0], dtype=np.float32)\nD_tilde = np.diag(A_tilde.sum(axis=1))\nd_inv_sqrt = np.diag(1.0 / np.sqrt(np.diag(D_tilde)))\nA_hat = d_inv_sqrt @ A_tilde @ d_inv_sqrt\n\nprint('A.shape:', A.shape)   # (5, 5)\nprint('X.shape:', X.shape)   # (5, 2)\nprint('Degrees:', degrees)   # [2. 2. 2. 3. 1.]\nprint('A_hat[0,0]:', A_hat[0,0])  # 0.3333\nprint('A_hat[0,1]:', A_hat[0,1])  # 0.3333\nprint('A_hat[3,4]:', A_hat[3,4])  # 0.3536\n\n# Sparse edge-list for PyTorch Geometric\nedge_index = np.array([[0,1],[1,2],[0,3],[2,3],[3,4]]).T  # shape (2, 5)\nprint('edge_index shape:', edge_index.shape)  # (2, 5)\n```",
    "types_header": "Graph Encoding Frameworks",
    "types_badge": "Graph Structure Representations",
    "quick_types": [
        {
            "name": "Undirected Unweighted Graph",
            "description": "Symmetric binary adjacency matrix A = A^T with entries in {0, 1}, modeling mutual relationships like social friendships or undirected power cables."
        },
        {
            "name": "Directed Weighted Graph",
            "description": "Asymmetric real-valued adjacency matrix encoding both direction (A_ij != A_ji) and strength (e.g. payment amounts, traffic flows, or signal intensities) simultaneously."
        },
        {
            "name": "Sparse Edge-List (PyTorch Geometric format)",
            "description": "Compact [2, |E|] integer tensor storing only non-zero edge source-destination index pairs, scaling from O(N^2) to O(|E|) memory for sparse real-world graphs."
        },
        {
            "name": "Normalized Adjacency (GCN A_hat)",
            "description": "Degree-normalized adjacency A_hat = D_tilde^{-1/2} A_tilde D_tilde^{-1/2} used in Graph Convolutional Networks to equalize aggregation contributions across varying node degrees."
        }
    ],
    "connected_logic": [
        {
            "title": "Adjacency Matrix as Connectivity Blueprint",
            "description": "Mathematical encoding of graph topology enabling GNN layers to identify each node's neighborhood.",
            "points": [
                "Binary A_ij in {0,1} for unweighted graphs; real A_ij > 0 for weighted edges indicating strength or distance.",
                "Symmetry A = A^T holds for undirected graphs; asymmetry A_ij != A_ji encodes directed message flows.",
                "Zero diagonal entries by default; self-loops added via A_tilde = A + I so each node aggregates its own features."
            ]
        },
        {
            "title": "Node Features as Semantic Signal",
            "description": "Domain-specific attribute encoding enabling GNNs to distinguish node identities beyond pure topology.",
            "points": [
                "Feature matrix X in R^{NxF} provides initial embeddings H^0 = X before any GNN message-passing layers.",
                "Features may include continuous measurements, one-hot encodings, text embeddings, or learned representations.",
                "Node ordering must be strictly consistent between A (row/column index) and X (row index) to prevent feature mis-assignment."
            ]
        },
        {
            "title": "Degree Normalization & GCN Propagation",
            "description": "Degree-aware scaling preventing aggregation instabilities and enabling deep GNN stacking.",
            "points": [
                "Degree matrix D_ii = sum_j A_ij measures connectivity; high-degree hub nodes aggregate from many neighbors.",
                "Symmetric normalization A_hat_ij = 1/sqrt(d_i * d_j) prevents hub dominance and low-degree node explosion.",
                "GCN layer H^{l+1} = sigma(A_hat H^l W^l) propagates normalized neighborhood information through learnable weight matrices."
            ]
        },
        {
            "title": "Sparse Representations for Real-World Graphs",
            "description": "Memory-efficient graph storage enabling GNN training on million-node real-world networks.",
            "points": [
                "Dense N x N adjacency for N=1,000,000 nodes requires 1 TB of float32 memory; infeasible for typical hardware.",
                "Edge-list format [2, |E|] reduces storage to O(|E|); typical real-world graphs are sparse with |E| << N^2.",
                "PyTorch Geometric's Data object stores edge_index ([2, |E|]), x ([N, F]), and optional edge_attr ([|E|, d_e])."
            ]
        }
    ],
    "pitfalls": [
        "Inconsistent Node Ordering Between A and X: If row 0 of the adjacency matrix refers to node A but row 0 of the feature matrix refers to node B, the GNN propagates incorrect neighbor information across all layers.",
        "Treating A_ij = 0 as Node Disconnection: Zero entries indicate no direct edge under the encoding convention, not graph disconnection—paths may exist through intermediate nodes.",
        "Assuming All Adjacency Matrices are Symmetric: Directed graphs produce asymmetric A where A_ij = 1 but A_ji = 0; always verify whether the library convention defines edges as row-to-column or column-to-row.",
        "Forgetting Self-Loops Before GCN Normalization: Without A_tilde = A + I, GCN aggregation excludes a node's own features; the node's representation becomes entirely neighbor-derived after each layer.",
        "Using Dense Adjacency for Large Sparse Graphs: Dense N x N storage scales as O(N^2), requiring terabytes for million-node graphs; use sparse edge-list or COO/CSR formats with PyTorch Geometric or DGL."
    ],
    "key_takeaways": [
        "A graph G = (V, E) is fully specified numerically by the adjacency matrix A in R^{NxN} (connectivity) and node feature matrix X in R^{NxF} (attributes), which together form the dual input to GNN layers.",
        "Undirected graphs require symmetric adjacency (A = A^T); adding self-loops via A_tilde = A + I ensures each node's own features participate in neighborhood aggregation.",
        "GCN symmetric normalization A_hat = D_tilde^{-1/2} A_tilde D_tilde^{-1/2} scales aggregated messages by 1/sqrt(d_i * d_j), preventing high-degree nodes from dominating and enabling stable deep stacking.",
        "Real-world graphs are sparse: use edge-list format [2, |E|] (PyTorch Geometric) instead of dense N x N matrices to reduce memory from O(N^2) to O(|E|)."
    ],
    "tags": [
        "Graph Neural Networks",
        "Adjacency Matrix",
        "Node Features",
        "GCN",
        "Graph Representation",
        "Sparse Graphs",
        "PyTorch Geometric",
        "Message Passing"
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
