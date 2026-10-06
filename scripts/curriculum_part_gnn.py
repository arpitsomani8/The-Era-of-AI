# scripts/curriculum_part_gnn.py
# 5 Graph Neural Network Concepts

def get_gnn_concepts():
    topic_id = "dl_gnn"
    topic_label = "Graph Neural Networks (GNN) & Geometric Deep Learning"
    cat = "dl"
    cat_label = "Deep Learning Foundations"

    return [
        {
            "id": "concept_graph_representations_adjacency",
            "title": "Graph Representations, Adjacency Matrices & Node Features",
            "topic_id": topic_id, "topic_label": topic_label, "category": cat, "category_label": cat_label,
            "raw_subtopic": "Graph Representations, Adjacency Matrices & Node Features", "raw_sub": "Graph Representations, Adjacency Matrices & Node Features",
            "def": "The foundational mathematical representation of non-Euclidean relational data defined by graph G = (V, E) with node feature tensor X (N x F), sparse adjacency matrix A (N x N), degree matrix D, and edge attribute tensor E_attr.",
            "definition": "The foundational mathematical representation of non-Euclidean relational data defined by graph G = (V, E) with node feature tensor X (N x F), sparse adjacency matrix A (N x N), degree matrix D, and edge attribute tensor E_attr.",
            "formula": "$$A_{ij} = \\begin{cases} 1 & \\text{if } (v_i, v_j) \\in E \\\\ 0 & \\text{otherwise} \\end{cases}, \\quad D_{ii} = \\sum_j A_{ij}, \\quad L = D - A, \\quad \\tilde{L} = D^{-\\frac{1}{2}} L D^{-\\frac{1}{2}}$$",
            "formula_explanation": "",
            "logic": "Unlike images with regular pixel grids or text with 1D token orders, graphs have arbitrary neighborhood sizes, no global coordinate system, and are permutation invariant: relabeling nodes cannot alter graph properties.",
            "core_logic": "Unlike images with regular pixel grids or text with 1D token orders, graphs have arbitrary neighborhood sizes, no global coordinate system, and are permutation invariant: relabeling nodes cannot alter graph properties.",
            "architectural_logic": "",
            "example": "Molecular chemistry modeling: A caffeine molecule represented as a graph where carbon/oxygen/nitrogen atoms are nodes with atomic number features, and covalent single/double bonds are edge attributes.",
            "tags": ["GNN", "Graph Representation", "Adjacency Matrix", "Laplacian"],
            "simple_summary": "A graph represents connected things: people in a social network, atoms in a medicine, or computers on the internet. An adjacency matrix is a spreadsheet checkbox showing who is connected to whom.",
            "core_terms": [
                {
                    "term": "Adjacency Matrix (A)",
                    "what_is_it": "A square N x N matrix where entry A_{ij} indicates whether an edge connects node i and node j.",
                    "analogy": "A flight route map table showing which airport hubs have direct non-stop flights between them.",
                    "why_it_matters": "The fundamental mathematical structure describing the topology of connections."
                },
                {
                    "term": "Node Feature Matrix (X)",
                    "what_is_it": "An N x F matrix where each row contains the feature attributes of a specific node.",
                    "analogy": "The user profile page for each member of a social network (age, location, interests).",
                    "why_it_matters": "Provides the semantic content that gets transformed and passed along edges."
                },
                {
                    "term": "Degree Matrix (D)",
                    "what_is_it": "A diagonal matrix where D_{ii} counts the total number of edges connected to node i.",
                    "analogy": "Counting how many total friends or followers each person has on their profile.",
                    "why_it_matters": "Used for normalizing message aggregations so popular celebrity nodes don't drown out smaller nodes."
                },
                {
                    "term": "Graph Laplacian (L)",
                    "what_is_it": "The matrix difference L = D - A, measuring how smoothly node signals diffuse across the graph.",
                    "analogy": "Measuring how heat spreads through connected metal pipes over time.",
                    "why_it_matters": "The core operator in spectral graph theory, spectral clustering, and Fourier transforms on graphs."
                }
            ],
            "symbol_guide": [
                {"symbol": "V, E", "meaning": "Set of vertices (nodes) and set of edges (links)", "plain_english": "Entities and relationships"},
                {"symbol": "N", "meaning": "Total number of nodes in graph", "plain_english": "e.g. 5,000 users or 50 atoms"},
                {"symbol": "L", "meaning": "Unnormalized Graph Laplacian (D - A)", "plain_english": "Measures difference between a node and its neighbors"}
            ],
            "numerical_example": "Graph with 3 nodes: Edge (1, 2) and Edge (2, 3). Adjacency A = [[0,1,0], [1,0,1], [0,1,0]]. Degrees: D_1=1, D_2=2, D_3=1. Degree matrix D = diag(1, 2, 1). Laplacian L = D - A = [[1,-1,0], [-1,2,-1], [0,-1,1]]. Row sums are always 0, proving conservation of flow.",
            "pitfalls": "Novice Trap: Storing adjacency matrix A as a dense 2D NumPy array for large graphs. For a graph of 1,000,000 users, an N x N dense float matrix requires 4 Terabytes of RAM! Production GNNs use sparse Coordinate format (COO / PyTorch Geometric edge_index) requiring only O(|E|) memory.",
            "key_takeaways": [],
            "definition_bullets": [
                "Adjacency Matrix: Square matrix encoding pairwise node connectivity.",
                "Node Feature Matrix: Tabular attributes representing internal node states.",
                "Degree Matrix: Diagonal matrix tracking edge counts per node.",
                "Sparse Edge Index: Memory-efficient COO format enabling GNN scaling to millions of nodes."
            ]
        },
        {
            "id": "concept_gcn_message_passing",
            "title": "Graph Convolutional Networks (GCN) & Message Passing",
            "topic_id": topic_id, "topic_label": topic_label, "category": cat, "category_label": cat_label,
            "raw_subtopic": "Graph Convolutional Networks (GCN) & Message Passing", "raw_sub": "Graph Convolutional Networks (GCN) & Message Passing",
            "def": "The localized spectral approximation of graph convolution (Kipf & Welling) and spatial Message Passing Neural Network (MPNN) paradigm that updates node representations through iterative neighborhood message transformation, aggregation, and state combination.",
            "definition": "The localized spectral approximation of graph convolution (Kipf & Welling) and spatial Message Passing Neural Network (MPNN) paradigm that updates node representations through iterative neighborhood message transformation, aggregation, and state combination.",
            "formula": "$$H^{(l+1)} = \\sigma\\left( \\tilde{D}^{-\\frac{1}{2}} \\tilde{A} \\tilde{D}^{-\\frac{1}{2}} H^{(l)} W^{(l)} \\right), \\quad m_v^{(l+1)} = \\sum_{u \\in \\mathcal{N}(v)} M\\left(h_u^{(l)}, h_v^{(l)}, e_{uv}\\right), \\quad h_v^{(l+1)} = U\\left(h_v^{(l)}, m_v^{(l+1)}\\right)$$",
            "formula_explanation": "",
            "logic": "Standard convolutions slide a fixed kernel over adjacent pixels. In graphs where neighbor counts vary from 1 to 10,000, GCN uses symmetric normalization D^(-1/2) A D^(-1/2) with self-loops so each node averages its own feature with its immediate neighbors.",
            "core_logic": "Standard convolutions slide a fixed kernel over adjacent pixels. In graphs where neighbor counts vary from 1 to 10,000, GCN uses symmetric normalization D^(-1/2) A D^(-1/2) with self-loops so each node averages its own feature with its immediate neighbors.",
            "architectural_logic": "",
            "example": "Citation network classification (Cora dataset): Predicting scientific research paper categories by aggregating keywords from directly cited and citing papers across 2 GCN message-passing hops.",
            "tags": ["GCN", "Message Passing", "MPNN", "Graph Convolution"],
            "simple_summary": "Message passing in a graph is like neighbors talking over their backyard fences: every round, each person collects news from their direct friends, summarizes it, and updates their own knowledge.",
            "core_terms": [
                {
                    "term": "Message Function M()",
                    "what_is_it": "A function that computes a message vector traveling from neighbor node u to target node v along edge e_{uv}.",
                    "analogy": "Writing a letter summarizing your recent news to mail to your friend.",
                    "why_it_matters": "Enables edge features (e.g. relationship type, distance) to influence node updates."
                },
                {
                    "term": "Aggregation Operator",
                    "what_is_it": "A permutation-invariant reduction function (sum, mean, max) pooling incoming neighbor messages.",
                    "analogy": "Pouring ingredients from multiple measuring cups into a single mixing bowl (order doesn't matter).",
                    "why_it_matters": "Guarantees that the model's output doesn't change if neighbor nodes are listed in a different order."
                },
                {
                    "term": "Self-Loop Addition (\\tilde{A} = A + I)",
                    "what_is_it": "Adding an identity matrix to adjacency A so each node treats itself as one of its own neighbors.",
                    "analogy": "Including your own personal opinion when listening to advice from your friend group.",
                    "why_it_matters": "Prevents nodes from completely replacing their own identity with only neighbor features."
                },
                {
                    "term": "Symmetric Degree Normalization",
                    "what_is_it": "Scaling by D^{-1/2} A D^{-1/2} so message weights depend inversely on the product of degrees: 1 / sqrt(d_u * d_v).",
                    "analogy": "Speaking at a reasonable volume so that loud chatter from a stadium doesn't deafen everyone.",
                    "why_it_matters": "Prevents numerical explosion in node embeddings as messages cascade across layers."
                }
            ],
            "symbol_guide": [
                {"symbol": "H^{(l)}", "meaning": "Node representation matrix at layer l", "plain_english": "Current embeddings of all nodes"},
                {"symbol": "W^{(l)}", "meaning": "Trainable weight matrix at layer l", "plain_english": "Linear projection applied to messages"},
                {"symbol": "\\tilde{A}", "meaning": "Adjacency matrix with self-loops added (A + I_N)", "plain_english": "Connections including self-connections"}
            ],
            "numerical_example": "Target node v has 2 neighbors. Neighbor 1 embedding = [1, 2], Neighbor 2 embedding = [3, 4], Target node v embedding = [2, 0]. Self-loops added. Symmetric normalized sum gives aggregate = (1/sqrt(3×3)) × [ (1+3+2), (2+4+0) ] = 1/3 × [6, 6] = [2, 2]. Multiplying by weight matrix W yields the next-layer embedding.",
            "pitfalls": "Novice Trap: Oversmoothing! Stacking more than 3-4 GCN layers causes node representations to converge to identical, indistinguishable averages across the entire graph. Use residual connections (ResGCN) or pair-norm to go deeper.",
            "key_takeaways": [],
            "definition_bullets": [
                "Message Passing: Iterative exchange of transformed vectors between adjacent graph neighbors.",
                "Permutation Invariance: Aggregation functions (sum/mean/max) unaffected by node ordering.",
                "Self-Loops: Ensuring a node preserves its own prior state during updates.",
                "Oversmoothing Hazard: Too many message hops causes all node embeddings in the graph to become identical."
            ]
        },
        {
            "id": "concept_gat_edge_attention",
            "title": "Graph Attention Networks (GAT) & Edge Attentions",
            "topic_id": topic_id, "topic_label": topic_label, "category": cat, "category_label": cat_label,
            "raw_subtopic": "Graph Attention Networks (GAT) & Edge Attentions", "raw_sub": "Graph Attention Networks (GAT) & Edge Attentions",
            "def": "An attention-driven graph neural network architecture (Veličković et al.) that dynamically learns anisotropic edge attention coefficients between connected node pairs via self-attention, extended to Multi-Head Graph Attention and edge-featured GATv2.",
            "definition": "An attention-driven graph neural network architecture (Veličković et al.) that dynamically learns anisotropic edge attention coefficients between connected node pairs via self-attention, extended to Multi-Head Graph Attention and edge-featured GATv2.",
            "formula": "$$\\alpha_{ij} = \\frac{\\exp\\left( \\text{LeakyReLU}\\left( \\mathbf{a}^T [W h_i \\parallel W h_j] \\right) \\right)}{\\sum_{k \\in \\mathcal{N}_i} \\exp\\left( \\text{LeakyReLU}\\left( \\mathbf{a}^T [W h_i \\parallel W h_k] \\right) \\right)}, \\quad h_i' = \\sigma\\left( \\sum_{j \\in \\mathcal{N}_i} \\alpha_{ij} W h_j \\right)$$",
            "formula_explanation": "",
            "logic": "GCN assigns fixed, topology-only weights based on degrees (1/sqrt(d_i d_j)), treating all neighbors equally regardless of their content. GAT dynamically assigns higher attention weights alpha_{ij} to neighbors whose features are most relevant to the task.",
            "core_logic": "GCN assigns fixed, topology-only weights based on degrees (1/sqrt(d_i d_j)), treating all neighbors equally regardless of their content. GAT dynamically assigns higher attention weights alpha_{ij} to neighbors whose features are most relevant to the task.",
            "architectural_logic": "",
            "example": "E-commerce fraud ring detection: A user is connected to 50 family/friend accounts and 1 flagged money-laundering mule account. GAT assigns 92% attention weight to the fraudulent connection, isolating the criminal nexus.",
            "tags": ["GAT", "Graph Attention", "Self-Attention", "Multi-Head"],
            "simple_summary": "In GCN, all friends have equal say based on degree. In GAT, the network listens closely to some friends and ignores others: it assigns personalized attention percentages (alphas) to each incoming connection.",
            "core_terms": [
                {
                    "term": "Attention Coefficients (alpha_{ij})",
                    "what_is_it": "Softmax-normalized scalar scores quantifying the relative importance of neighbor j's features to node i.",
                    "analogy": "Turning up the volume slider on the smartest person in the meeting room while turning down background chatter.",
                    "why_it_matters": "Enables anisotropic filtering: adapting weights based on feature content rather than static graph structure."
                },
                {
                    "term": "Multi-Head Graph Attention",
                    "what_is_it": "Computing K independent sets of attention coefficients in parallel and concatenating or averaging their outputs.",
                    "analogy": "Having multiple expert judges evaluate an Olympic figure skating routine from different angles.",
                    "why_it_matters": "Stabilizes the learning process and captures multifaceted relational dynamics."
                },
                {
                    "term": "GATv2 Dynamic Attention",
                    "what_is_it": "Fixing GAT's static ranking problem by placing the non-linearity before the projection vector: a^T LeakyReLU(W_1 h_i + W_2 h_j).",
                    "analogy": "Allowing the teacher to grade each student relative to the specific assignment prompt rather than by a fixed popularity list.",
                    "why_it_matters": "Allows every node to dynamically attend to any neighbor depending on query condition."
                },
                {
                    "term": "Inductive Capacity",
                    "what_is_it": "The ability of GAT to evaluate attention weights on completely unseen graphs without retraining, because attention depends only on local node pair features.",
                    "analogy": "A referee knowing the rules of basketball so well they can officiate a game between two brand new teams they've never seen before.",
                    "why_it_matters": "Enables deployment on evolving social graphs with millions of new users daily."
                }
            ],
            "symbol_guide": [
                {"symbol": "\\alpha_{ij}", "meaning": "Attention weight between node i and neighbor j", "plain_english": "Percentage of focus placed on neighbor j (sums to 1.0)"},
                {"symbol": "\\parallel", "meaning": "Concatenation operator", "plain_english": "Gluing two vectors side-by-side"},
                {"symbol": "\\mathbf{a}", "meaning": "Trainable attention mechanism weight vector", "plain_english": "Calculates compatibility score"}
            ],
            "numerical_example": "Node i has 2 neighbors. Raw compatibility logits: e_{i1} = 2.4, e_{i2} = 1.0. Softmax attention: alpha_{i1} = exp(2.4)/(exp(2.4)+exp(1.0)) = 11.02 / (11.02 + 2.72) = 0.802 (80.2%). alpha_{i2} = 0.198 (19.8%). Node i's new embedding is 80.2% driven by neighbor 1 and only 19.8% by neighbor 2.",
            "pitfalls": "Novice Trap: High GPU memory consumption. Because GAT computes attention scores for every edge in the graph, multi-head attention on dense graphs with millions of edges can trigger Out-Of-Memory (OOM) errors. Use edge sampling or neighborhood sampling.",
            "key_takeaways": [],
            "definition_bullets": [
                "Attention Coefficients: Content-based normalized weights governing message aggregation.",
                "Multi-Head Attention: Independent parallel attention heads stabilizing learning.",
                "GATv2: Dynamic expressive attention overcoming static neighbor ranking limitations.",
                "Inductive Generalization: Seamlessly applies to novel unseen nodes and dynamic graphs."
            ]
        },
        {
            "id": "concept_graphsage_inductive",
            "title": "Inductive Graph Representation (GraphSAGE)",
            "topic_id": topic_id, "topic_label": topic_label, "category": cat, "category_label": cat_label,
            "raw_subtopic": "Inductive Graph Representation (GraphSAGE)", "raw_sub": "Inductive Graph Representation (GraphSAGE)",
            "def": "An inductive framework for representation learning on massive dynamic graphs (Hamilton et al.) that trains localized neighborhood sampling and aggregation functions rather than memorizing individual node embeddings, scaling to billions of vertices.",
            "definition": "An inductive framework for representation learning on massive dynamic graphs (Hamilton et al.) that trains localized neighborhood sampling and aggregation functions rather than memorizing individual node embeddings, scaling to billions of vertices.",
            "formula": "$$h_{\\mathcal{N}(v)}^{(k)} = \\text{AGGREGATE}_k\\left( \\{ h_u^{(k-1)}, \\forall u \\in \\mathcal{S}_{\\mathcal{N}(v)} \\} \\right), \\quad h_v^{(k)} = \\sigma\\left( W^{(k)} \\cdot [h_v^{(k-1)} \\parallel h_{\\mathcal{N}(v)}^{(k)}] \\right)$$",
            "formula_explanation": "",
            "logic": "Transductive algorithms (like standard GCN or DeepWalk) require the entire graph topology during training and fail when new nodes join. GraphSAGE trains *aggregation functions* (e.g. Mean, Pool, LSTM) over fixed-size uniform neighborhood samples S_N(v), enabling instant embedding generation for brand new unseen nodes.",
            "core_logic": "Transductive algorithms (like standard GCN or DeepWalk) require the entire graph topology during training and fail when new nodes join. GraphSAGE trains *aggregation functions* (e.g. Mean, Pool, LSTM) over fixed-size uniform neighborhood samples S_N(v), enabling instant embedding generation for brand new unseen nodes.",
            "architectural_logic": "",
            "example": "Pinterest (PinSage): Embedding 3 billion image pins and 18 billion boards. PinSage samples 50 neighbors per pin and runs random-walk convolutions to generate real-time visual recommendation feeds with 100ms latency.",
            "tags": ["GraphSAGE", "Inductive Learning", "Neighborhood Sampling", "PinSage"],
            "simple_summary": "GraphSAGE solves the giant graph problem: instead of processing millions of friends, it randomly samples a small handful of friends (e.g., 10 friends for layer 1, 5 friends for layer 2). This keeps computation fixed and lets you embed brand new users immediately.",
            "core_terms": [
                {
                    "term": "Inductive Learning",
                    "what_is_it": "Learning a generalizable function that can generate embeddings for completely new nodes added to the graph tomorrow without retraining.",
                    "analogy": "Learning a recipe to bake any cake versus memorizing the exact taste of five specific cakes in your fridge.",
                    "why_it_matters": "Essential for real-world platforms where thousands of new users and items join every minute."
                },
                {
                    "term": "Neighborhood Sampling (S_N)",
                    "what_is_it": "Uniformly sampling a fixed number of neighbors (e.g. K_1 = 25, K_2 = 10) instead of using the entire unbounded neighborhood.",
                    "analogy": "Conducting a poll with 20 randomly selected voters rather than trying to interview all 10 million citizens.",
                    "why_it_matters": "Bounds memory and computation to a predictable constant, preventing neighbor explosion."
                },
                {
                    "term": "Pooling Aggregator",
                    "what_is_it": "Feeding neighbor vectors through an MLP and taking element-wise max-pooling: max(sigma(W_{pool} h_u + b)).",
                    "analogy": "A team highlighting the single strongest idea across each category from team brainstorming notes.",
                    "why_it_matters": "Captures distinct aspects of the neighborhood independently across dimensions."
                },
                {
                    "term": "Mini-batch Graph Training",
                    "what_is_it": "Constructing dynamic computation trees backward from target batch nodes, enabling standard SGD on massive web-scale graphs.",
                    "analogy": "Tracing branches of a family tree only for the 100 people in today's survey rather than loading the complete ancestry of the human race.",
                    "why_it_matters": "Allows training GNNs on multi-billion edge graphs using standard single GPUs."
                }
            ],
            "symbol_guide": [
                {"symbol": "\\mathcal{S}_{\\mathcal{N}(v)}", "meaning": "Sampled neighborhood set for node v", "plain_english": "A small random selection of v's friends (e.g. 15 friends)"},
                {"symbol": "\\text{AGGREGATE}", "meaning": "Permutation invariant pooling function", "plain_english": "Mean, LSTM, or Max-pooling over sampled neighbors"},
                {"symbol": "h_v^{(k)}", "meaning": "Node v's representation at step k", "plain_english": "Output vector after k hops of sampling"}
            ],
            "numerical_example": "Node v has 1,200 followers (high degree). Standard GCN requires computing 1,200 dot products. GraphSAGE fixes sample size K=10. Exactly 10 random follower vectors are sampled. The aggregator computes the mean vector in 0.05ms. Concatenating with node v's vector gives a fixed [128 + 128 = 256] dimension tensor, perfectly uniform across all batch rows.",
            "pitfalls": "Novice Trap: Using the LSTM aggregator without randomly shuffling the neighbors! LSTMs are not naturally symmetric or permutation invariant; shuffling input order during training is mandatory to prevent spurious sequence bias.",
            "key_takeaways": [],
            "definition_bullets": [
                "Inductive Capability: Generalizes to unseen nodes and evolving dynamic graphs without retraining.",
                "Fixed Neighborhood Sampling: Eliminates memory explosion by sampling a constant number of neighbors.",
                "Aggregator Functions: Mean, pooling, and LSTM aggregators summarizing local topology.",
                "Industrial Scalability: Powers web-scale recommendation engines across billions of vertices."
            ]
        },
        {
            "id": "concept_link_prediction_node_classification",
            "title": "Link Prediction & Node Classification Pipelines",
            "topic_id": topic_id, "topic_label": topic_label, "category": cat, "category_label": cat_label,
            "raw_subtopic": "Link Prediction & Node Classification Pipelines", "raw_sub": "Link Prediction & Node Classification Pipelines",
            "def": "The two primary downstream task paradigms in geometric deep learning: Node Classification (predicting categorical labels for individual vertices) and Link Prediction (predicting the existence, probability, or sign of missing relationships between vertex pairs).",
            "definition": "The two primary downstream task paradigms in geometric deep learning: Node Classification (predicting categorical labels for individual vertices) and Link Prediction (predicting the existence, probability, or sign of missing relationships between vertex pairs).",
            "formula": "$$\\text{Node}: \\hat{y}_v = \\text{Softmax}(W h_v^{(L)}), \\quad \\text{Link}: P((u,v) \\in E) = \\sigma\\left( h_u^T h_v \\right) \\text{ or } \\sigma\\left( \\text{MLP}([h_u \\parallel h_v]) \\right)$$",
            "formula_explanation": "",
            "logic": "In Node Classification, GNN embeddings are mapped directly to class logits using cross-entropy. In Link Prediction, negative edges are sampled from non-connected pairs, and the dot product or cosine distance between embeddings is trained via binary logistic loss.",
            "core_logic": "In Node Classification, GNN embeddings are mapped directly to class logits using cross-entropy. In Link Prediction, negative edges are sampled from non-connected pairs, and the dot product or cosine distance between embeddings is trained via binary logistic loss.",
            "architectural_logic": "",
            "example": "LinkedIn 'People You May Know': Link prediction models calculate the likelihood that user A will connect with user B by scoring their 2-hop GNN node embeddings, generating personalized connection recommendations.",
            "tags": ["Link Prediction", "Node Classification", "Downstream GNN", "Graph Tasks"],
            "simple_summary": "Node classification predicts what a node is (e.g. 'Is this bank account a fraudster?'). Link prediction predicts whether two nodes should be connected (e.g. 'Will Alice and Bob become friends on Facebook?').",
            "core_terms": [
                {
                    "term": "Node Classification",
                    "what_is_it": "Predicting the label y_v of a node (e.g. topic category, spam flag, protein function) using its GNN final embedding.",
                    "analogy": "Determining what department an employee belongs to by looking at who they talk to.",
                    "why_it_matters": "Standard task for fraud detection, document tagging, and protein folding classification."
                },
                {
                    "term": "Link Prediction",
                    "what_is_it": "Predicting whether an edge exists between two nodes: score(u, v) = sigma(z_u^T z_v).",
                    "analogy": "A matchmaker predicting whether two people on a blind date will get married.",
                    "why_it_matters": "Powers social friend suggestions, knowledge graph completion, and drug-target interaction discovery."
                },
                {
                    "term": "Negative Edge Sampling",
                    "what_is_it": "Selecting pairs of nodes (u, v) that do not have an edge in the real graph to serve as label=0 negative examples.",
                    "analogy": "Showing a student examples of incorrect answers so they learn what mistakes look like.",
                    "why_it_matters": "Essential for binary link prediction because real graphs contain only observed positive edges."
                },
                {
                    "term": "Graph-Level Pooling (Readout)",
                    "what_is_it": "Aggregating all node embeddings in an entire graph into a single global vector: h_G = Readout({h_v, forall v in V}).",
                    "analogy": "Calculating the total GDP of a country by summing the incomes of all its citizens.",
                    "why_it_matters": "Enables graph-level classification (e.g. 'Is this entire molecule toxic or safe?')."
                }
            ],
            "symbol_guide": [
                {"symbol": "h_v^{(L)}", "meaning": "Final GNN embedding of node v", "plain_english": "The rich summary vector for node v"},
                {"symbol": "P((u,v) \\in E)", "meaning": "Probability of link between u and v", "plain_english": "Score between 0.0 and 1.0 that an edge exists"},
                {"symbol": "\\text{Readout}", "meaning": "Graph-level aggregation function", "plain_english": "Global pooling (sum, mean, virtual node)"}
            ],
            "numerical_example": "User u embedding = [0.8, 0.6]. User v embedding = [0.7, 0.7]. Unconnected user w embedding = [-0.9, 0.1]. Link score (u, v) = sigma((0.8×0.7) + (0.6×0.7)) = sigma(0.56 + 0.42) = sigma(0.98) = 0.727 (72.7% chance to connect). Link score (u, w) = sigma(-0.72 + 0.06) = sigma(-0.66) = 0.341. Platform suggests v to u.",
            "pitfalls": "Novice Trap: Data leakage during link prediction evaluation! If you include the test edges in the adjacency matrix while generating node embeddings, the GNN will cheat by simply checking if the edge is already there. Test edges must strictly be removed from message passing.",
            "key_takeaways": [],
            "definition_bullets": [
                "Node Classification: Assigning categorical classes to individual graph vertices.",
                "Link Prediction: Estimating connection probability between arbitrary node pairs.",
                "Negative Sampling: Creating balanced 0-labels from unlinked pairs for contrastive binary loss.",
                "Evaluation Hygiene: Strictly masking test edges from message-passing graphs to prevent leakage."
            ]
        }
    ]

print("GNN module ready.")
