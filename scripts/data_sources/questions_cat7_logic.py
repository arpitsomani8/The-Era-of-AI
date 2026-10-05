"""Category 7: Logical Brainteasers, Probability Puzzles & Quantitative Reasoning (Questions 136-150)"""

CAT7_QUESTIONS = [
    {
        "id": "logic_136",
        "category": "logic_prob",
        "category_label": "Logic & Probability Puzzles",
        "difficulty": "Mid / Senior",
        "company_tags": ["Google", "Jane Street", "Citadel", "Two Sigma"],
        "question": "The Monty Hall Problem: You are on a game show with 3 closed doors. Behind one door is a sports car; behind the other two are goats. You pick Door 1. The host (who knows what is behind every door) opens Door 3, revealing a goat. The host offers you the option to switch to Door 2. Should you switch? Prove mathematically using Bayes' Theorem why switching doubles your probability of winning.",
        "answer": """**1. The Intuitive Answer:**
**YES, you must ALWAYS switch.** Switching gives a **$2/3$ win probability**, whereas staying with Door 1 leaves you with only a **$1/3$ win probability**.

**2. Proof via Bayes' Theorem:**
Let $C_i$ be the event that the Car is behind Door $i$ ($P(C_1) = P(C_2) = P(C_3) = 1/3$).
Let $H_3$ be the event that the Host opens Door 3.
We seek $P(C_2 | H_3)$ (probability the car is behind Door 2 given the host opened Door 3):
$$P(C_2 | H_3) = \\frac{P(H_3 | C_2) P(C_2)}{P(H_3)}$$

Evaluate the conditional probabilities of host behavior:
- If Car is at Door 1 ($C_1$): Host can open Door 2 or Door 3 with equal probability: $P(H_3 | C_1) = 1/2$.
- If Car is at Door 2 ($C_2$): Host *cannot* open Door 1 (your pick) and *cannot* open Door 2 (has the car). The host is **forced** to open Door 3: $P(H_3 | C_2) = 1$.
- If Car is at Door 3 ($C_3$): Host cannot reveal the car: $P(H_3 | C_3) = 0$.

Total probability of host opening Door 3:
$$P(H_3) = P(H_3|C_1)P(C_1) + P(H_3|C_2)P(C_2) + P(H_3|C_3)P(C_3) = \\left(\\frac{1}{2} \\cdot \\frac{1}{3}\\right) + \\left(1 \\cdot \\frac{1}{3}\\right) + 0 = \\frac{1}{6} + \\frac{1}{3} = \\frac{1}{2}$$

Now apply Bayes' Theorem:
- **Probability if you STAY with Door 1:**
  $$P(C_1 | H_3) = \\frac{P(H_3 | C_1) P(C_1)}{P(H_3)} = \\frac{\\frac{1}{2} \\cdot \\frac{1}{3}}{\\frac{1}{2}} = \\mathbf{\\frac{1}{3}}$$
- **Probability if you SWITCH to Door 2:**
  $$P(C_2 | H_3) = \\frac{P(H_3 | C_2) P(C_2)}{P(H_3)} = \\frac{1 \\cdot \\frac{1}{3}}{\\frac{1}{2}} = \\mathbf{\\frac{2}{3}}$$
By switching, your winning probability increases from $33.3\\%$ to $66.7\\%$!""",
        "tip": "Explain that the host's privileged knowledge concentrates the entire $2/3$ probability of the remaining two doors onto Door 2."
    },
    {
        "id": "logic_137",
        "category": "logic_prob",
        "category_label": "Logic & Probability Puzzles",
        "difficulty": "Junior / Mid",
        "company_tags": ["Amazon", "Google", "Facebook"],
        "question": "The Birthday Paradox: How many people must be in a room before there is a greater than 50% probability that at least two share the exact same birthday? How does this mathematically explain hash collisions in hash tables?",
        "answer": """**1. Mathematical Calculation:**
Instead of computing the probability of a match directly, compute the complement: the probability that **all $n$ people have distinct birthdays**.
Assuming 365 equally likely days:
- Person 1: $365/365$
- Person 2: $364/365$
- Person $n$: $(365 - n + 1) / 365$
$$P(\\text{All distinct}) = \\prod_{k=0}^{n-1} \\left( 1 - \\frac{k}{365} \\right)$$
Using the Taylor approximation $1 - x \\approx e^{-x}$:
$$P(\\text{All distinct}) \\approx \\prod_{k=0}^{n-1} e^{-k/365} = \\exp\\left( -\\sum_{k=0}^{n-1} \\frac{k}{365} \\right) = \\exp\\left( -\\frac{n(n-1)}{2 \\times 365} \\right)$$
We want $P(\\text{At least one match}) = 1 - P(\\text{All distinct}) \\ge 0.50$:
$$e^{-\\frac{n(n-1)}{730}} \\le 0.5 \\implies \\frac{n(n-1)}{730} \\ge \\ln(2) \\approx 0.693$$
$$n^2 \\approx 730 \\times 0.693 \\approx 506 \\implies n \\approx \\sqrt{506} \\approx \\mathbf{23\\text{ people!}}$$
With just **23 people**, there is a **$50.7\\%$ chance** of a shared birthday. With 70 people, probability exceeds $99.9\\%$.

**2. Application to Hash Table Collisions (Birthday Attack):**
People intuitively compare 23 to 365 and think the probability should be tiny ($23/365 \\approx 6\\%$). But birthday matching compares **pairs of people**:
$$\\binom{23}{2} = \\frac{23 \\times 22}{2} = 253\\text{ pairwise comparisons!}$$
In cryptography and hash tables with $N$ possible hash buckets, collisions do not require $N$ items; collisions occur with $50\\%$ probability after only **$\\approx \\sqrt{N}$ insertions** (e.g. an $n$-bit hash function provides only $n/2$ bits of collision security).""",
        "tip": "Highlight the square root bound: $\\approx 1.177 \\sqrt{N}$ is the general formula for a 50% collision probability across $N$ bins."
    },
    {
        "id": "logic_138",
        "category": "logic_prob",
        "category_label": "Logic & Probability Puzzles",
        "difficulty": "Mid / Senior",
        "company_tags": ["Jane Street", "Citadel", "Optiver"],
        "question": "The Rare Disease False Positive Paradox: A disease affects 1 in 1,000 people. A diagnostic test has 99% Sensitivity (True Positive Rate) and 95% Specificity (True Negative Rate). If a randomly selected person tests positive, what is the exact probability that they actually have the disease? (Show the step-by-step Bayes calculation).",
        "answer": """**1. Setup Probabilities:**
- Prior probability of disease: $P(D) = 0.001$, so $P(\\neg D) = 0.999$.
- Sensitivity: $P(+ | D) = 0.99$.
- Specificity: $P(- | \\neg D) = 0.95$, which implies False Positive Rate $P(+ | \\neg D) = 1 - 0.95 = 0.05$.

**2. Bayes' Theorem Calculation:**
We want $P(D | +)$ (probability of having disease given a positive test):
$$P(D | +) = \\frac{P(+ | D) P(D)}{P(+)}$$
Using Law of Total Probability for denominator $P(+)$:
$$P(+) = P(+ | D)P(D) + P(+ | \\neg D)P(\\neg D)$$
$$P(+) = (0.99 \\times 0.001) + (0.05 \\times 0.999) = 0.00099 + 0.04995 = 0.05094$$

Now compute posterior:
$$P(D | +) = \\frac{0.00099}{0.05094} = \\mathbf{0.01943 \\quad (\\approx 1.94\\%!)}$$

**3. The Intuitive Explanation (Natural Frequencies):**
Take 100,000 people:
- **100 people** actually have the disease. 99 test positive, 1 tests negative.
- **99,900 people** do NOT have the disease. 5% test positive anyway = **4,995 false alarms!**
- Total positive tests: $99 + 4,995 = 5,094$.
- Out of 5,094 positive tests, only 99 actually have the disease: $\\frac{99}{5094} \\approx 1.94\\%$!
Despite a 99% accurate test, an overwhelming **$98\\%$ of positive results are false alarms** due to the extreme rarity (base rate) of the disease.""",
        "tip": "Interviewers use this to test whether you succumb to the Base Rate Fallacy. Explaining with 100,000 natural frequencies is crystal-clear."
    },
    {
        "id": "logic_139",
        "category": "logic_prob",
        "category_label": "Logic & Probability Puzzles",
        "difficulty": "Mid / Senior",
        "company_tags": ["Citadel", "Two Sigma", "Jane Street"],
        "question": "Expected Value of Coin Toss Sequences: What is the expected number of fair coin tosses required to observe the sequence HH (Heads-Heads) versus HT (Heads-Tails)? Why are they different (6 vs 4) even though both individual sequences have probability 1/4?",
        "answer": """**1. Why They Differ (The Overlap / Reset Property):**
- In **HH**, if you toss H and then T, you fail and your progress is **completely destroyed**; you must start over from scratch. Furthermore, if you get HHH, the second H can serve as the first H of the next HH pair.
- In **HT**, if you toss H and then H, you have not failed completely! You are still holding an 'H', so a 'T' on the very next toss will complete HT immediately!

**2. Calculating Expected Tosses for HT (Markov Chain):**
Let $E_0$ be expected tosses from start, $E_H$ be expected tosses after seeing H:
$$E_0 = 1 + \\frac{1}{2} E_H + \\frac{1}{2} E_0 \\implies \\frac{1}{2} E_0 = 1 + \\frac{1}{2} E_H \\implies E_0 = 2 + E_H$$
From state H:
- Toss T ($1/2$): Done (0 remaining steps).
- Toss H ($1/2$): Still in state H (remain in $E_H$).
$$E_H = 1 + \\frac{1}{2}(0) + \\frac{1}{2} E_H \\implies \\frac{1}{2} E_H = 1 \\implies E_H = 2$$
Substitute back:
$$E_{HT} = 2 + 2 = \\mathbf{4\\text{ tosses}}$$

**3. Calculating Expected Tosses for HH:**
Let $E_0$ be start, $E_H$ be state holding H:
$$E_0 = 2 + E_H$$
From state H:
- Toss H ($1/2$): Done (0 remaining steps).
- Toss T ($1/2$): Failed! Flips back to start $E_0$!
$$E_H = 1 + \\frac{1}{2}(0) + \\frac{1}{2} E_0 = 1 + \\frac{1}{2}(2 + E_H) = 2 + \\frac{1}{2} E_H \\implies \\frac{1}{2} E_H = 2 \\implies E_H = 4$$
Substitute back:
$$E_{HH} = 2 + 4 = \\mathbf{6\\text{ tosses}}$$
Expected tosses for **HH is 6**, while expected tosses for **HT is 4**!""",
        "tip": "Setting up the 2-state Markov chain equations demonstrates mastery of stochastic processes."
    },
    {
        "id": "logic_140",
        "category": "logic_prob",
        "category_label": "Logic & Probability Puzzles",
        "difficulty": "Mid / Senior",
        "company_tags": ["Google", "Meta", "Amazon"],
        "question": "Reservoir Sampling: You are receiving a stream of data of unknown total length $N$ (too massive to fit in memory). How do you select exactly $k$ items uniformly at random such that every element has an exact probability of $k/N$ of being chosen? Prove by induction.",
        "answer": """**1. The Algorithm (Algorithm R - Jeffrey Vitter, 1985):**
1. Store the first $k$ items from the stream directly into the reservoir array $R[0 \\dots k-1]$.
2. For each subsequent item $i$ arriving from the stream ($i = k+1, k+2, \\dots, N$):
   - Generate a random integer $j$ uniformly in the range $[1, i]$.
   - If $j \\le k$: Replace item $R[j-1]$ with the new item $i$.
   - If $j > k$: Discard item $i$.
3. When stream terminates, array $R$ contains $k$ uniformly random items.

**2. Proof by Mathematical Induction:**
- **Base Case ($i = k$):**
  The first $k$ items are in the reservoir with probability $k/k = 1.0$.
- **Inductive Step:**
  Assume that after step $n-1$, every item has probability $\\frac{k}{n-1}$ of being in the reservoir.
  At step $n$, new item $n$ is chosen with probability $\\frac{k}{n}$.
  For an existing item already in the reservoir to survive, two independent conditions must hold:
  1. It was already in the reservoir at step $n-1$ (Probability $= \\frac{k}{n-1}$).
  2. It is NOT evicted by the new item arriving at step $n$.
     - Probability new item enters: $\\frac{k}{n}$.
     - Probability that our specific item is chosen to be replaced: $\\frac{1}{k}$.
     - Probability our item is evicted: $\\frac{k}{n} \\times \\frac{1}{k} = \\frac{1}{n}$.
     - Probability our item survives: $1 - \\frac{1}{n} = \\frac{n-1}{n}$.

  Total probability that existing item is in reservoir after step $n$:
  $$P = \\left(\\frac{k}{n-1}\\right) \\times \\left(\\frac{n-1}{n}\\right) = \\mathbf{\\frac{k}{n}}$$
By mathematical induction, every element from $1$ to $N$ has an exact equal probability $\\frac{k}{N}$ of being in the reservoir.""",
        "tip": "Reservoir sampling is the standard data engineering solution for generating random training mini-batches from unbounded streaming Kafka topics."
    },
    {
        "id": "logic_141",
        "category": "logic_prob",
        "category_label": "Logic & Probability Puzzles",
        "difficulty": "Mid / Senior",
        "company_tags": ["Jane Street", "Two Sigma", "DE Shaw"],
        "question": "1D Random Walk: A drunk person takes steps on a 1D number line starting at position 0. At each step, they move $+1$ with probability $0.5$ and $-1$ with probability $0.5$. What is their expected displacement after $N$ steps, and what is their expected Root-Mean-Square (RMS) distance from the origin?",
        "answer": """**1. Setup:**
Let $X_i$ be the step at time $i$: $P(X_i = +1) = 0.5$, $P(X_i = -1) = 0.5$.
Position after $N$ steps is $S_N = \\sum_{i=1}^N X_i$.
- $\\mathbb{E}[X_i] = (+1)(0.5) + (-1)(0.5) = 0$.
- $\\text{Var}(X_i) = \\mathbb{E}[X_i^2] - (\\mathbb{E}[X_i])^2 = 1 - 0 = 1$.

**2. Expected Displacement:**
$$\\mathbb{E}[S_N] = \\sum_{i=1}^N \\mathbb{E}[X_i] = \\mathbf{0}$$
On average, the person ends up at the origin.

**3. Expected Root-Mean-Square (RMS) Distance:**
Compute the second moment $\\mathbb{E}[S_N^2]$:
$$\\mathbb{E}[S_N^2] = \\mathbb{E}\\left[ \\left(\\sum_{i=1}^N X_i\\right)^2 \\right] = \\sum_{i=1}^N \\mathbb{E}[X_i^2] + 2 \\sum_{i < j} \\mathbb{E}[X_i X_j]$$
Since steps are independent, $\\mathbb{E}[X_i X_j] = \\mathbb{E}[X_i] \\mathbb{E}[X_j] = 0$.
$$\\mathbb{E}[S_N^2] = \\sum_{i=1}^N (1) = N$$
The Root-Mean-Square distance is:
$$\\text{RMS} = \\sqrt{\\mathbb{E}[S_N^2]} = \\mathbf{\\sqrt{N}}$$
- After 100 steps, expected distance from origin is $\\sqrt{100} = 10$.
- After 10,000 steps, expected distance is $\\sqrt{10,000} = 100$.
- This $\\sqrt{N}$ diffusion scaling is the fundamental law underlying Brownian motion, financial volatility scaling ($\\sigma \\sqrt{t}$), and physics diffusion.""",
        "tip": "Mention that in 1D and 2D random walks, the probability of eventually returning to the origin is 1.0 (Pólya's Recurrence Theorem), but in 3D it drops to ~34%."
    },
    {
        "id": "logic_142",
        "category": "logic_prob",
        "category_label": "Logic & Probability Puzzles",
        "difficulty": "Quant / Research",
        "company_tags": ["Jane Street", "Citadel", "HRT"],
        "question": "The 100 Prisoners and 100 Boxes Problem: 100 prisoners (numbered 1 to 100) are condemned to death. In a room are 100 closed boxes containing shuffled numbers from 1 to 100. Each prisoner can open up to 50 boxes to find their own number. They cannot communicate after entering. If EVERY prisoner finds their own number, they are all freed; if even one fails, all are executed. Random guessing yields a survival probability of $(1/2)^{100} \\approx 8 \\times 10^{-31}$. How can the prisoners achieve a $>30\\%$ survival probability using permutation cycle decomposition?",
        "answer": """**1. The Loop Strategy:**
1. Each prisoner goes to the box labeled with **their own number**.
2. They open it and look at the number inside ($k$).
3. If $k$ is their number, they succeed!
4. If not, they go to **box number $k$** and open it.
5. They repeat this chain, following the pointers, up to 50 boxes.

**2. Mathematical Proof via Permutation Cycles:**
The 100 boxes represent a random permutation $\\sigma \\in S_{100}$. Every finite permutation decomposes uniquely into disjoint **cycles** (e.g. $1 \\to 7 \\to 23 \\to 1$).
- A prisoner will find their number if and only if their number belongs to a cycle of **length $\\le 50$**!
- ALL 100 prisoners will survive if and only if the permutation contains **NO cycles of length $> 50$**.

**3. Probability Calculation:**
A permutation can contain at most one cycle of length $L > 50$ (since two such cycles would require $>100$ elements).
The number of permutations of length 100 containing a cycle of length $L$ is:
$$\\binom{100}{L} \\times (L - 1)! \\times (100 - L)! = \\frac{100!}{L}$$
Dividing by the total number of permutations ($100!$):
$$P(\\text{Cycle of length } L) = \\frac{1}{L}$$
The probability that there exists a cycle of length $> 50$ is:
$$P(\\text{Failure}) = \\sum_{L=51}^{100} \\frac{1}{L} \\approx \\int_{50}^{100} \\frac{1}{x} dx = \\ln(100) - \\ln(50) = \\ln(2) \\approx 0.6931$$
The probability that all 100 prisoners survive is:
$$P(\\text{Survival}) = 1 - \\ln(2) = 1 - 0.6931 = \\mathbf{0.3069 \\quad (\\approx 31.18\\%!)}$$
By exploiting cycle correlation, they boost survival from $10^{-31}$ to over **$31\\%$**!""",
        "tip": "This is widely considered the most beautiful probability puzzle ever conceived for quant hedge fund interviews."
    },
    {
        "id": "logic_143",
        "category": "logic_prob",
        "category_label": "Logic & Probability Puzzles",
        "difficulty": "Mid / Senior",
        "company_tags": ["Google", "Meta", "Amazon"],
        "question": "Simpson's Reversal in Click-Through Rates (CTR): Construct an exact numerical table showing two ad campaigns A and B where Campaign A has a strictly higher CTR on Mobile and a strictly higher CTR on Desktop, yet Campaign B has a higher overall CTR in aggregate.",
        "answer": """**1. Numerical Proof Table:**

| Segment | Campaign A Clicks / Impr | Campaign A CTR | Campaign B Clicks / Impr | Campaign B CTR | Higher CTR |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Mobile** | $100 / 1,000$ | **$10.0\\%$** | $9 / 100$ | $9.0\\%$ | **A wins!** |
| **Desktop** | $90 / 300$ | **$30.0\\%$** | $560 / 2,000$ | $28.0\\%$ | **A wins!** |
| **TOTAL** | **$190 / 1,300$** | **$14.6\\%$** | **$569 / 2,100$** | **$27.1\\%$** | **B wins!** |

**2. Explanation:**
- On Mobile: Campaign A ($10\\%$) beats Campaign B ($9\\%$).
- On Desktop: Campaign A ($30\\%$) beats Campaign B ($28\\%$).
- **In Total: Campaign B ($27.1\\%$) crushes Campaign A ($14.6\\%$)!**

**3. Why it Happens (Unequal Confounding Weights):**
Desktop users inherently convert at much higher rates ($28-30\\%$) than mobile users ($9-10\\%$).
- Campaign B ran **$95\\%$ of its ads on Desktop** ($2,000 / 2,100$), so its aggregate is heavily weighted toward high desktop conversion.
- Campaign A ran **$77\\%$ of its ads on Mobile** ($1,000 / 1,300$), so its aggregate is dragged down by low mobile baseline rates.
Aggregating across heterogeneous cohorts without segment-weight normalization produces an inverted, false verdict.""",
        "tip": "Having these exact numbers memorized or quickly reconstructible instantly proves your quantitative mastery."
    },
    {
        "id": "logic_144",
        "category": "logic_prob",
        "category_label": "Logic & Probability Puzzles",
        "difficulty": "Mid / Senior",
        "company_tags": ["Jane Street", "Two Sigma", "SIG"],
        "question": "The Two Envelopes Paradox: Two envelopes contain money. One has $X$, the other has $2X$. You choose an envelope and open it to find $100. The other envelope contains either $50 or $200 with equal probability (1/2 each). The expected value of switching is $0.5(50) + 0.5(200) = 125 > 100$. By this logic, you should ALWAYS switch, even before opening the envelope! What is the mathematical fallacy?",
        "answer": """**1. The Fallacy:**
The paradox stems from an invalid assumption of a **uniform prior probability distribution over all positive real numbers**:
$$P(X = x) = \\text{constant for all } x \\in (0, \\infty)$$
In probability theory, a uniform distribution over the infinite interval $(0, \\infty)$ is an **improper prior** (it cannot sum or integrate to 1.0).

**2. Rigorous Bayesian Resolution:**
Let $P(X)$ be any valid, integrable prior probability distribution over the smaller amount $X$.
When you open an envelope and see value $V = 100$:
The other envelope contains $V/2 = 50$ (if $X=50$, you opened $2X$) or $2V = 200$ (if $X=100$, you opened $X$).
The posterior probability that the other envelope is larger ($X = V$) is:
$$P(\\text{Other is } 2V | V) = \\frac{P(X = V)}{P(X = V) + P(X = V/2)}$$
- For the probability to remain $1/2$ for all possible values $V$, we must have $P(X = V) = P(X = V/2)$ for all $V$.
- This implies $P(X)$ is constant across all powers of 2 from $0$ to $\\infty$, which has infinite integral and cannot exist!
- For any realistic, finite probability distribution (e.g. human wealth), as $V$ grows large, $P(X = V)$ is strictly smaller than $P(X = V/2)$. The probability of the other envelope being smaller increases, exactly counteracting the $2X$ multiplier and keeping the expected net gain of switching at **strictly $0$**.""",
        "tip": "Explain that the fallacy is treating $P(X = V/2) = P(X = V) = 0.5$ as constant for all $V$, which violates the Kolmogorov axioms of probability."
    },
    {
        "id": "logic_145",
        "category": "logic_prob",
        "category_label": "Logic & Probability Puzzles",
        "difficulty": "Junior / Mid",
        "company_tags": ["Google", "Apple", "Microsoft"],
        "question": "The Burning Ropes Timer: You have two ropes. Each rope takes exactly 60 minutes to burn completely from one end to the other. However, the ropes burn at non-uniform, unpredictable rates (e.g. 90% of the rope could burn in the first 5 minutes). How can you measure exactly 45 minutes?",
        "answer": """**1. Solution Steps:**
1. **At Time $t = 0$:**
   - Light **Rope 1 at BOTH ends simultaneously**.
   - Light **Rope 2 at ONE end only**.
2. **At Time $t = 30\\text{ minutes}$:**
   - Because Rope 1 was burning from both ends, the two flame fronts travel toward each other and meet, burning Rope 1 completely in exactly **30 minutes** (regardless of non-uniform burning rates!).
   - At this exact moment, exactly 30 minutes have elapsed.
   - Rope 2 has 30 minutes of burn time remaining.
   - **Immediately light the OTHER end of Rope 2!**
3. **At Time $t = 45\\text{ minutes}$:**
   - Rope 2 is now burning from both ends with 30 minutes of fuel left.
   - The remaining burn time is halved: $30 / 2 = \\mathbf{15\\text{ minutes}}$.
   - When Rope 2 burns out completely, exactly $30 + 15 = \\mathbf{45\\text{ minutes}}$ have elapsed!""",
        "tip": "Clarify why lighting both ends always halves burn time: two independent flame fronts consume fuel at twice the net rate regardless of density variations."
    },
    {
        "id": "logic_146",
        "category": "logic_prob",
        "category_label": "Logic & Probability Puzzles",
        "difficulty": "Mid",
        "company_tags": ["Jane Street", "Citadel", "Goldman Sachs"],
        "question": "Russian Roulette Probability: A 6-chamber revolver has 2 adjacent bullets loaded side-by-side in chambers 1 and 2. The other 4 chambers are empty. The cylinder is spun once. Player 1 points the gun at their head, pulls the trigger, and clicks on an empty chamber (click!). Now it is Player 2's turn. The host gives Player 2 a choice: pull the trigger immediately, or spin the cylinder first. What is the mathematically optimal choice?",
        "answer": """**1. Option A: Spin the Cylinder:**
Spinning resets the cylinder randomly.
There are 2 bullets in 6 chambers:
$$P(\\text{Bullet | Spin}) = \\frac{2}{6} = \\mathbf{\\frac{1}{3} \\approx 33.3\\%}$$

**2. Option B: Shoot Immediately (Do Not Spin):**
Let the chambers in circular order be $[B_1, B_2, E_3, E_4, E_5, E_6]$.
Player 1 survived on an empty chamber.
Player 1 must have landed on one of the 4 empty chambers: $E_3, E_4, E_5,$ or $E_6$.
Let us evaluate where Player 2 lands on the very next chamber:
- If Player 1 was on $E_3 \\implies$ Player 2 gets $E_4$ (Safe!)
- If Player 1 was on $E_4 \\implies$ Player 2 gets $E_5$ (Safe!)
- If Player 1 was on $E_5 \\implies$ Player 2 gets $E_6$ (Safe!)
- If Player 1 was on $E_6 \\implies$ Player 2 gets $B_1$ (BULLET!)
Out of the 4 possible starting empty chambers, only **1 leads to a bullet**, while **3 lead to empty chambers**!
$$P(\\text{Bullet | Do Not Spin}) = \\mathbf{\\frac{1}{4} = 25.0\\%}$$

**Conclusion:**
Player 2 should **NEVER spin**! Shooting immediately gives a $25\\%$ death probability, whereas spinning increases death probability to $33.3\\%$. Conditioning on Player 1's safe click reveals valuable sequential information.""",
        "tip": "Explain that Player 1's safe click eliminated the dangerous chamber right before the first bullet, leaving only 1 transition to a bullet out of 4."
    },
    {
        "id": "logic_147",
        "category": "logic_prob",
        "category_label": "Logic & Probability Puzzles",
        "difficulty": "Mid / Senior",
        "company_tags": ["Jane Street", "Optiver", "Akuna"],
        "question": "Coin Toss Tournament (Penney's Game): You toss a fair coin repeatedly until either HHT or HTH appears. Player 1 chooses sequence HHT; Player 2 chooses sequence HTH. What is the exact probability that Player 1 wins? Why is Penney's Game non-transitive?",
        "answer": """**1. Penney's Game Non-Transitivity:**
Like Rock-Paper-Scissors, for any 3-toss sequence chosen by Player 1, Player 2 can always choose a sequence that beats it with $>50\\%$ probability!

**2. Analysis of HHT vs HTH:**
Let us trace the coin toss sequence:
- If the first toss is T, it has no effect (neither sequence contains leading T); we wait for the first H.
- When the first H appears:
  - If the next two tosses are HT, sequence is HHT? No, if next toss is T, we have HT:
    - If the third toss is H $\\implies$ **HTH (Player 2 wins immediately!)**.
    - If the third toss is T $\\implies$ HTT.
  - What if the sequence starts with **HH**?
    - Once HH appears, **Player 1 is guaranteed to win!**
    - Why? Because to win, Player 2 needs HTH. But to get HTH after HH, you would have to toss T (yielding HHT, which means Player 1 wins before Player 2 can even toss their final H!).
- Therefore:
  - If we reach HH before HT $\\implies$ Player 1 wins.
  - Probability that HH occurs before HT in a string starting with H is:
    $$P(\\text{Second toss is H}) = 1/2$$
    - If second toss is H $\\implies$ HH $\\implies$ Player 1 wins ($100\\%$).
    - If second toss is T $\\implies$ HT. Third toss:
      - If H ($1/2$) $\\implies$ HTH (Player 2 wins).
      - If T ($1/2$) $\\implies$ HTT (resets to waiting for next H).
Solving the Markov equations:
$$P(\\text{Player 1 wins}) = \\mathbf{\\frac{2}{3} \\approx 66.7\\%}$$
Player 1 has a massive **$2:1$ advantage**!""",
        "tip": "Penney's game is famous because sequence A beats B, B beats C, C beats D, and D beats A (non-transitive cycles)."
    },
    {
        "id": "logic_148",
        "category": "logic_prob",
        "category_label": "Logic & Probability Puzzles",
        "difficulty": "Senior / Quant",
        "company_tags": ["Jane Street", "Citadel", "DeepMind"],
        "question": "The Ant on a Rubber Rope: An ant starts at one end of a 1 km rubber rope and crawls toward the other end at 1 cm/sec. At the end of every second, the rope is instantly stretched uniformly by an additional 1 km (so after 1 second it is 2 km, after 2 seconds 3 km, etc.). The ant's crawl distance is also stretched proportionally with the rope. Will the ant ever reach the end of the rope? Prove mathematically.",
        "answer": """**1. The Counter-Intuitive Answer:**
**YES, the ant is mathematically guaranteed to reach the end of the rope!**

**2. Proof via Fractional Distance (Harmonic Series):**
Instead of tracking absolute distance in centimeters, track the **fraction of the rope's total length** $f$ the ant traverses:
- At second 1: Rope length is $1\\text{ km} = 100,000\\text{ cm}$. Ant crawls $1\\text{ cm}$.
  $$\\text{Fraction gained} = \\frac{1}{100,000}$$
- When the rope stretches from 1 km to 2 km, the ant's relative position is preserved (if it was 1% along the rope, it remains 1% along the rope).
- At second 2: Rope length is $2\\text{ km} = 200,000\\text{ cm}$. Ant crawls another $1\\text{ cm}$.
  $$\\text{Fraction gained} = \\frac{1}{200,000} = \\frac{1}{100,000} \\times \\frac{1}{2}$$
- At second $n$: Rope length is $n\\text{ km}$.
  $$\\text{Fraction gained} = \\frac{1}{100,000} \\times \\frac{1}{n}$$

Total fractional distance traversed after $N$ seconds:
$$F(N) = \\sum_{n=1}^N \\frac{1}{100,000 \\cdot n} = \\frac{1}{100,000} \\sum_{n=1}^N \\frac{1}{n}$$
- The sum $\\sum_{n=1}^N \\frac{1}{n}$ is the famous **Harmonic Series**, which is proven to **diverge to infinity**:
  $$\\lim_{N \\to \\infty} \\sum_{n=1}^N \\frac{1}{n} = \\infty$$
- Since the series diverges without bound, $F(N)$ must eventually reach and exceed $1.0$ (100% of the rope)!
- Using approximation $\\sum_{n=1}^N \\frac{1}{n} \\approx \\ln(N)$:
  $$\\frac{\\ln(N)}{100,000} = 1 \\implies \\ln(N) = 100,000 \\implies N = e^{100,000}\\text{ seconds}$$
While the time required is astronomically large, the ant is guaranteed to finish in finite time.""",
        "tip": "This puzzle tests whether a candidate can transform an absolute coordinates problem into a fractional/relative invariant."
    },
    {
        "id": "logic_149",
        "category": "logic_prob",
        "category_label": "Logic & Probability Puzzles",
        "difficulty": "Junior / Mid",
        "company_tags": ["Goldman Sachs", "Google", "Amazon"],
        "question": "Estimating Pi via Monte Carlo: How do you estimate Pi using uniform random sampling in a 2D bounding square? What is the standard error convergence rate as sample size $N \\to \\infty$?",
        "answer": """**1. The Algorithm:**
1. Inscribe a circle of radius $r=1$ inside a square with side length $2r = 2$ centered at the origin:
   - Area of circle: $A_{\\text{circle}} = \\pi r^2 = \\pi$.
   - Area of bounding square: $A_{\\text{square}} = (2r)^2 = 4$.
2. The theoretical ratio of areas is:
   $$\\frac{A_{\\text{circle}}}{A_{\\text{square}}} = \\frac{\\pi}{4} \\implies \\pi = 4 \\times \\frac{A_{\\text{circle}}}{A_{\\text{square}}}$$
3. Generate $N$ independent uniform random points: $(x_i, y_i) \\sim U(-1, 1) \\times U(-1, 1)$.
4. Count how many points fall inside the circle: $x_i^2 + y_i^2 \\le 1$ ($M$ points).
5. Estimate $\\hat{\\pi}$:
   $$\\hat{\\pi} = 4 \\times \\frac{M}{N}$$

**2. Convergence Rate (Standard Error):**
Each point is a Bernoulli trial with success probability $p = \\pi/4$.
The sample proportion $\\hat{p} = M/N$ has variance:
$$\\text{Var}(\\hat{p}) = \\frac{p(1 - p)}{N} = \\frac{\\frac{\\pi}{4}(1 - \\frac{\\pi}{4})}{N}$$
The Standard Error (SE) of our $\\pi$ estimate is:
$$\\text{SE}(\\hat{\\pi}) = 4 \\sqrt{\\frac{p(1 - p)}{N}} = O\\left( \\frac{1}{\\sqrt{N}} \\right)$$
- To gain **1 additional decimal digit of accuracy** ($10\\times$ error reduction), you must increase sample size by **$100\\times$** ($N \\to 100N$).
- Demonstrates the fundamental $O(1/\\sqrt{N})$ convergence rate of all Monte Carlo methods.""",
        "tip": "Emphasize that the $O(1/\\sqrt{N})$ Monte Carlo rate is independent of dimension, making it superior to grid integration in high dimensions."
    },
    {
        "id": "logic_150",
        "category": "logic_prob",
        "category_label": "Logic & Probability Puzzles",
        "difficulty": "Junior / Mid",
        "company_tags": ["Google", "Microsoft", "Amazon"],
        "question": "The 9 Coins and Balance Scale Puzzle: You have 9 coins that look identical. 8 coins have identical weight, but 1 coin is counterfeit and heavier. You have a two-pan balance scale with no weights. What is the minimum number of weighings guaranteed to find the heavy coin? Prove why 2 weighings is optimal using ternary information theory.",
        "answer": """**1. The Minimum Weighings:**
The heavy coin can be guaranteed in **exactly 2 weighings**.

**2. Step-by-Step Procedure (Ternary Divide-and-Conquer):**
Divide the 9 coins into 3 equal groups of 3: **Group A (3), Group B (3), Group C (3)**.

- **Weighing 1:** Place **Group A on left pan, Group B on right pan** (leave Group C aside).
  - *Case 1 (Left tilts down):* Heavy coin is in **Group A**.
  - *Case 2 (Right tilts down):* Heavy coin is in **Group B**.
  - *Case 3 (Pans balance equally):* Heavy coin is in **Group C**.
  *After 1 weighing, we have isolated the heavy coin to exactly 3 candidate coins!*

- **Weighing 2:** Take the 3 candidate coins ($C_1, C_2, C_3$). Place **$C_1$ on left pan, $C_2$ on right pan** (leave $C_3$ aside).
  - *Case 1 (Left tilts down):* $C_1$ is the heavy coin.
  - *Case 2 (Right tilts down):* $C_2$ is the heavy coin.
  - *Case 3 (Pans balance equally):* $C_3$ is the heavy coin!

**3. Information-Theoretic Proof of Optimality:**
A balance scale has **3 possible outcomes** per weighing: Left tilt, Right tilt, or Balance ($b=3$ base states, 1 trit of information).
With $k$ weighings, the maximum number of distinguishable states is $3^k$:
- $k = 1 \\implies 3^1 = 3$ states (cannot distinguish 9 coins).
- $k = 2 \\implies 3^2 = 9$ states (can distinguish up to 9 coins).
- $k = 3 \\implies 3^3 = 27$ states (can solve up to 27 coins).
Therefore, **2 weighings** is mathematically optimal and minimal.""",
        "tip": "Explain that the scale gives ternary feedback ($3^k$), so dividing into 3 equal groups maximizes entropy at each step."
    }
]
