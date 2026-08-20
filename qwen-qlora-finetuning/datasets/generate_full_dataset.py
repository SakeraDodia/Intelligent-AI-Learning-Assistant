"""
generate_full_dataset.py
Builds real, curated (not API-generated) training data for all 3 modules
by combining hand-authored topic/question banks with combinatorial
assembly. Runs fully offline -- no API key or internet needed.
"""
import json, random
random.seed(42)

# ============================================================
# MODULE 1: INTERVIEW PREP
# ============================================================
SYS_INTERVIEW = ("You are an interview coach. When the user starts a prep session for a "
    "topic, ask exactly one question at a time. After the user answers, give brief, "
    "honest, calibrated feedback (praise only what's correct, gently correct what's "
    "wrong or incomplete), then move to the next question. Do not ask multiple "
    "questions at once.")

# topic -> list of (question, key_points)
INTERVIEW_BANK = {
    "Machine Learning": [
        ("Explain the bias-variance tradeoff.", "High bias means underfitting from overly simple assumptions; high variance means overfitting to training noise. Total error is bias^2 + variance + irreducible error, so the goal is minimizing that sum."),
        ("What's the difference between bagging and boosting?", "Bagging trains models in parallel on bootstrapped samples to reduce variance (e.g. Random Forest); boosting trains models sequentially, each correcting prior errors, to reduce bias (e.g. XGBoost)."),
        ("What is regularization and why use it?", "Regularization (L1/L2) adds a penalty on model complexity to the loss function, discouraging overfitting by shrinking or zeroing out less useful weights."),
        ("What is cross-validation and why does it matter?", "Cross-validation splits data into multiple folds, training/testing across different splits, to get a more reliable estimate of model performance than a single train/test split."),
        ("Explain precision vs recall.", "Precision is the fraction of predicted positives that are correct; recall is the fraction of actual positives that were correctly identified. There's usually a tradeoff between them."),
        ("What is the curse of dimensionality?", "As feature dimensions increase, data becomes sparse in the feature space, distances become less meaningful, and models need exponentially more data to generalize well."),
    ],
    "Deep Learning": [
        ("What causes vanishing gradients and how is it addressed?", "Repeated multiplication of small derivatives during backprop shrinks gradients toward zero in early layers; ReLU activations and residual connections mitigate this."),
        ("What is batch normalization for?", "It normalizes layer inputs across a mini-batch, stabilizing and speeding up training, and reducing sensitivity to weight initialization."),
        ("What is dropout and why does it work?", "Dropout randomly deactivates a fraction of neurons during training, preventing co-adaptation and forcing the network to learn redundant, generalizable representations."),
        ("Explain the purpose of the attention mechanism in Transformers.", "Attention lets each token weigh the relevance of every other token in a sequence, capturing long-range dependencies better than fixed-window approaches."),
        ("What's the difference between a CNN and an RNN's typical use case?", "CNNs exploit spatial locality, well suited to images; RNNs process sequences step by step, capturing temporal dependencies, though Transformers now often replace RNNs for sequence tasks."),
    ],
    "Data Structures": [
        ("What's the time complexity of search in a balanced BST, and why?", "O(log n), because the tree height is logarithmic in a balanced tree and search follows a single root-to-leaf path."),
        ("Explain stack vs queue with a real use case for each.", "Stack is LIFO (undo functionality, call stacks); queue is FIFO (task scheduling, printer queues, BFS traversal)."),
        ("How does a hash table achieve average O(1) lookup?", "It uses a hash function to map keys to array indices directly; collisions (handled via chaining or open addressing) are what can degrade performance toward O(n)."),
        ("What's the difference between an array and a linked list?", "Arrays offer O(1) indexed access but costly insertion/deletion in the middle; linked lists offer O(1) insertion/deletion given a node reference but O(n) access."),
        ("What is a heap used for?", "A heap maintains a partial order (min-heap or max-heap) enabling O(log n) insertion and O(1) access to the min/max element, commonly used for priority queues."),
    ],
    "Algorithms": [
        ("Explain the difference between BFS and DFS.", "BFS explores level by level using a queue, useful for shortest paths in unweighted graphs; DFS explores as deep as possible using a stack/recursion, useful for topological sort or cycle detection."),
        ("What is dynamic programming and when should you use it?", "DP solves problems by breaking them into overlapping subproblems and storing results to avoid recomputation, useful when a problem has optimal substructure and overlapping subproblems."),
        ("Explain the time complexity of merge sort.", "O(n log n) in all cases -- it recursively splits the array in half (log n levels) and merges in linear time at each level."),
        ("What is a greedy algorithm, and what's a risk of using one?", "It makes the locally optimal choice at each step; the risk is it may not produce a globally optimal solution unless the problem has the greedy-choice property."),
    ],
    "System Design": [
        ("How would you design a URL shortener?", "Key points: generate unique short codes (base62 encoding or hashing with collision handling), use a fast key-value store, cache hot mappings, and plan for read-heavy traffic with replicas/caching."),
        ("How would you handle a read-heavy system at scale?", "Add a caching layer (Redis/Memcached) in front of the database, use read replicas, and consider a CDN for static or semi-static content."),
        ("How would you design a rate limiter?", "Common approaches: token bucket or sliding window algorithms, typically implemented with a fast in-memory store like Redis to track request counts per user/IP within a time window."),
        ("What's the difference between horizontal and vertical scaling?", "Horizontal scaling adds more machines/instances; vertical scaling adds more resources (CPU/RAM) to a single machine. Horizontal scaling is generally preferred for resilience and elasticity at scale."),
    ],
    "SQL and Databases": [
        ("What's the difference between INNER JOIN and LEFT JOIN?", "INNER JOIN returns only matching rows from both tables; LEFT JOIN returns all rows from the left table plus matches from the right, filling unmatched columns with NULL."),
        ("What is a window function?", "It performs a calculation across a set of rows related to the current row without collapsing them into a single output row, unlike GROUP BY aggregates."),
        ("Explain database normalization.", "Normalization organizes data to reduce redundancy and dependency issues by splitting data into related tables, typically following normal forms (1NF, 2NF, 3NF)."),
        ("What is an index and what's the tradeoff of adding one?", "An index speeds up read queries by creating a fast lookup structure, but slows down writes (inserts/updates) since the index must also be updated."),
    ],
    "Behavioral": [
        ("Tell me about a time you disagreed with a teammate's technical decision.", "A strong answer uses STAR: describes the disagreement, the concrete action taken to raise/resolve it constructively (e.g. data, prototype), and a clear result or lesson learned."),
        ("Describe a time you had to learn a new technology quickly.", "A strong answer shows a clear learning strategy under time pressure and a concrete successful outcome, not just 'I read the docs'."),
        ("Tell me about a time you gave difficult feedback to a peer.", "A strong answer shows empathy plus directness -- the specific issue raised, how it was communicated constructively, and the outcome."),
        ("Describe a time you missed a deadline. What happened?", "A strong answer takes ownership, explains the root cause honestly, and describes concrete changes made afterward to prevent recurrence."),
    ],
    "Frontend Development": [
        ("What is the virtual DOM and why does React use it?", "It's an in-memory representation of the UI that React diffs against the previous version to compute minimal real DOM updates, which is cheaper than direct DOM manipulation on every change."),
        ("What's the difference between controlled and uncontrolled components in React?", "Controlled components have their state driven by React (value + onChange), while uncontrolled components manage their own state internally via the DOM, accessed with refs."),
        ("Explain CSS specificity.", "Specificity determines which CSS rule applies when multiple rules target the same element, roughly ranked: inline styles > IDs > classes/attributes > element selectors."),
        ("What is the difference between 'let', 'const', and 'var' in JavaScript?", "'var' is function-scoped and hoisted; 'let' and 'const' are block-scoped, with 'const' preventing reassignment of the binding (though object contents can still change)."),
    ],
    "Operating Systems": [
        ("What is a deadlock and what four conditions must hold for it to occur?", "Mutual exclusion, hold and wait, no preemption, and circular wait -- all four Coffman conditions must hold simultaneously."),
        ("What's the difference between a process and a thread?", "A process has its own memory space and resources; threads within a process share memory but have their own execution stack, making thread communication cheaper but riskier (race conditions)."),
        ("What is a page fault?", "It occurs when a program accesses a memory page not currently loaded in physical RAM, prompting the OS to load it from disk (part of virtual memory management)."),
        ("What is a race condition?", "It occurs when multiple threads access shared data concurrently and the outcome depends on unpredictable execution order/timing."),
    ],
    "Cloud and DevOps": [
        ("What's the difference between IaaS, PaaS, and SaaS?", "IaaS gives raw infrastructure (e.g. EC2); PaaS gives a managed platform to build/deploy apps (e.g. Heroku); SaaS gives ready-to-use software (e.g. Gmail)."),
        ("Why is Docker useful?", "It packages an application with its dependencies into a portable, consistent container image, avoiding 'works on my machine' issues and simplifying deployment."),
        ("What is CI/CD?", "Continuous Integration automatically builds/tests code on every change; Continuous Deployment/Delivery automates releasing that code to production or staging."),
        ("What is the purpose of a load balancer?", "It distributes incoming traffic across multiple backend servers to prevent overload on any single instance and improve availability."),
    ],
    "Cybersecurity": [
        ("What is the CIA triad?", "Confidentiality, Integrity, and Availability -- the three core principles security controls are designed to protect."),
        ("What is a SQL injection attack?", "An attacker inserts malicious SQL through user input fields to manipulate or extract data from a database, typically prevented with parameterized queries."),
        ("What's the difference between symmetric and asymmetric encryption?", "Symmetric encryption uses one shared key for both encryption and decryption (fast); asymmetric uses a public/private key pair (slower, but solves key distribution)."),
        ("What is phishing?", "A social engineering attack where an attacker impersonates a trusted entity to trick victims into revealing sensitive information or credentials."),
        ("What is the purpose of a firewall?", "It monitors and filters incoming/outgoing network traffic based on defined security rules, blocking unauthorized access."),
    ],
    "Mobile Development": [
        ("What's the difference between native and cross-platform mobile development?", "Native uses platform-specific languages (Swift/Kotlin) for best performance/access to APIs; cross-platform (Flutter/React Native) shares one codebase across iOS/Android at some performance/flexibility tradeoff."),
        ("What is state management and why does it matter in mobile apps?", "It's how an app tracks and updates UI-relevant data over time; poor state management leads to inconsistent UI and hard-to-debug behavior as apps grow."),
        ("What are the main considerations for mobile app performance?", "Minimizing unnecessary re-renders, efficient list rendering, lazy loading images/assets, and managing memory carefully on constrained devices."),
        ("Why are app permissions important to handle carefully?", "Requesting only necessary permissions, explaining why they're needed, and handling denial gracefully improves user trust and app store compliance."),
    ],
    "Data Engineering": [
        ("What's the difference between ETL and ELT?", "ETL transforms data before loading into the destination; ELT loads raw data first and transforms it within the destination system, often using the target's compute power (common with cloud warehouses)."),
        ("What is a data pipeline orchestrator used for?", "Tools like Airflow schedule, sequence, and monitor dependent data processing tasks, handling retries and alerting on failures."),
        ("What's the difference between batch and streaming data processing?", "Batch processes data in scheduled chunks (e.g. hourly/daily); streaming processes data continuously as it arrives, useful for real-time use cases."),
        ("What is data partitioning and why does it matter?", "Splitting large datasets into smaller, manageable chunks (e.g. by date) improves query performance and parallel processing efficiency."),
    ],
    "Git and Version Control": [
        ("What's the difference between 'git merge' and 'git rebase'?", "Merge creates a new commit tying two branch histories together, preserving full history; rebase replays commits on top of another branch, creating linear history but rewriting commit hashes."),
        ("What does 'git cherry-pick' do?", "It applies a specific commit from one branch onto another without merging the entire branch history."),
        ("What is a merge conflict and how do you resolve one?", "It occurs when Git can't automatically reconcile changes to the same lines/file across branches; resolving it means manually choosing/editing the correct final content before committing."),
        ("What's the purpose of a .gitignore file?", "It tells Git which files/directories to exclude from version control, like build artifacts, dependencies, or secrets."),
    ],
}

def make_interview_records():
    records = []
    for topic, questions in INTERVIEW_BANK.items():
        # Opening record
        first_q = questions[0][0]
        records.append({"messages": [
            {"role": "system", "content": SYS_INTERVIEW},
            {"role": "user", "content": f"Start interview prep for: {topic}"},
            {"role": "assistant", "content": f"Let's begin your {topic} prep.\n\nQuestion 1: {first_q}"},
        ]})
        # Transition records: for each question -> next question, 3 answer-quality variants
        for i in range(len(questions) - 1):
            q, key_points = questions[i]
            next_q, _ = questions[i + 1]
            variants = [
                ("strong", key_points,
                 f"That's correct and well explained. {key_points}\n\nQuestion {i+2}: {next_q}"),
                ("weak", "I'm not totally sure, maybe something related but I can't explain it clearly.",
                 f"That's alright -- let's clarify: {key_points}\n\nQuestion {i+2}: {next_q}"),
                ("partial", key_points.split(".")[0] + ".",
                 f"You're partially right. To complete the picture: {key_points}\n\nQuestion {i+2}: {next_q}"),
            ]
            for _, user_answer, assistant_feedback in variants:
                records.append({"messages": [
                    {"role": "system", "content": SYS_INTERVIEW},
                    {"role": "user", "content": user_answer},
                    {"role": "assistant", "content": assistant_feedback},
                ]})
    return records


# ============================================================
# MODULE 2: ROADMAP GENERATOR
# ============================================================
SYS_ROADMAP = ("You are a learning roadmap generator. Given a goal, duration, and skill "
    "level, produce a structured, phased roadmap in JSON. Each phase should have a "
    "name, duration, topics to learn, and suggested resources/project. Keep it "
    "realistic for the given duration and level.")

# goal -> {tier: [topics]}
ROADMAP_BANK = {
    "AI Engineer": {"foundation": ["Python programming basics", "NumPy and Pandas", "Basic statistics and linear algebra"],
        "core": ["Supervised and unsupervised learning", "Scikit-learn modeling", "Neural network fundamentals", "PyTorch or TensorFlow basics"],
        "advanced": ["Transformer architecture", "Fine-tuning with LoRA/QLoRA", "RAG pipelines", "Model deployment and serving"]},
    "Data Scientist": {"foundation": ["Statistics and probability", "Python for data analysis", "Data visualization"],
        "core": ["Hypothesis testing and A/B testing", "Feature engineering", "Regression and classification models"],
        "advanced": ["Gradient boosting methods", "Model interpretability (SHAP/LIME)", "Experiment design at scale"]},
    "Full Stack Web Developer": {"foundation": ["HTML, CSS basics", "JavaScript fundamentals", "Responsive design"],
        "core": ["React components, props, state", "REST API design", "Node.js and Express", "Databases (SQL/NoSQL)"],
        "advanced": ["Authentication and authorization", "CI/CD and deployment", "Performance optimization"]},
    "Backend Developer": {"foundation": ["Programming language fundamentals", "Data structures basics", "Working with APIs"],
        "core": ["Web framework (Django/Flask/Express)", "REST API design", "SQL and database design"],
        "advanced": ["Authentication and security", "Caching strategies", "Testing and CI/CD", "Cloud deployment"]},
    "DevOps Engineer": {"foundation": ["Linux command line", "Networking fundamentals", "Git version control"],
        "core": ["Docker and containers", "CI/CD pipelines", "Infrastructure as Code (Terraform)"],
        "advanced": ["Kubernetes orchestration", "Cloud platforms (AWS/GCP/Azure)", "Monitoring and observability"]},
    "Cybersecurity Analyst": {"foundation": ["Networking and OS fundamentals", "Security basics (CIA triad)", "Linux and scripting"],
        "core": ["SIEM tools and log analysis", "Web app vulnerabilities (OWASP Top 10)", "Threat intelligence basics"],
        "advanced": ["Penetration testing methodology", "Incident response and forensics", "Security certifications prep"]},
    "Mobile App Developer": {"foundation": ["Dart/Kotlin/Swift basics", "Flutter or native UI basics", "Layout and widgets"],
        "core": ["State management", "Navigation and routing", "Consuming REST APIs"],
        "advanced": ["Local storage and device features", "Push notifications", "App store deployment"]},
    "Data Engineer": {"foundation": ["SQL fundamentals", "Python scripting", "Data modeling basics"],
        "core": ["ETL/ELT pipeline design", "Data warehousing concepts", "Workflow orchestration (Airflow)"],
        "advanced": ["Streaming data (Kafka)", "Distributed processing (Spark)", "Data pipeline monitoring"]},
    "Product Manager (Tech)": {"foundation": ["Product lifecycle basics", "User research methods", "Writing PRDs"],
        "core": ["Prioritization frameworks (RICE)", "Key product metrics", "A/B testing fundamentals"],
        "advanced": ["Technical literacy for PMs", "Stakeholder communication", "Product strategy"]},
    "MLOps Engineer": {"foundation": ["ML pipeline basics", "Version control for data/models", "Cloud fundamentals"],
        "core": ["Model serving frameworks", "CI/CD for ML", "Feature stores"],
        "advanced": ["Model monitoring and drift detection", "Scaling inference workloads", "LLMOps and eval pipelines"]},
    "Computer Vision Engineer": {"foundation": ["Image processing basics", "OpenCV fundamentals", "CNN architecture"],
        "core": ["Object detection and segmentation", "Data augmentation techniques", "Transfer learning"],
        "advanced": ["Vision Transformers", "Multimodal models (CLIP)", "Real-time inference deployment"]},
    "NLP Engineer": {"foundation": ["Text preprocessing", "Tokenization and embeddings", "Python NLP libraries"],
        "core": ["Transformer architecture", "Sequence labeling and classification", "Using pretrained models"],
        "advanced": ["Fine-tuning LLMs", "RAG systems", "Prompt engineering and evaluation"]},
    "Prompt Engineer": {"foundation": ["How LLMs generate text", "Context window basics", "Zero-shot/few-shot prompting"],
        "core": ["Chain-of-thought prompting", "System and role prompts", "Structured output prompting"],
        "advanced": ["Prompt evaluation methods", "Handling adversarial inputs", "RAG and tool-use basics"]},
    "Game Developer": {"foundation": ["Programming fundamentals (C#/C++)", "Game engine basics (Unity/Unreal)", "2D/3D math basics"],
        "core": ["Game physics and collision", "Animation systems", "Game architecture patterns"],
        "advanced": ["Multiplayer networking", "Performance optimization", "Publishing and monetization"]},
    "Blockchain Developer": {"foundation": ["Blockchain fundamentals", "Cryptography basics", "Programming basics"],
        "core": ["Smart contract development (Solidity)", "Web3 libraries", "Testing smart contracts"],
        "advanced": ["Security auditing basics", "DeFi protocol concepts", "Layer 2 scaling solutions"]},
    "QA / Test Automation Engineer": {"foundation": ["Testing fundamentals", "Manual testing basics", "Version control"],
        "core": ["Test automation frameworks (Selenium/Playwright)", "API testing", "CI/CD integration"],
        "advanced": ["Performance testing", "Test strategy and planning", "Automation at scale"]},
    "UI/UX Designer": {"foundation": ["Design principles", "Wireframing basics", "Design tools (Figma)"],
        "core": ["User research methods", "Prototyping and interaction design", "Design systems"],
        "advanced": ["Usability testing", "Accessibility standards", "Design handoff to engineering"]},
    "Robotics Engineer": {"foundation": ["Programming basics (Python/C++)", "Physics and kinematics", "Linear algebra"],
        "core": ["Control systems basics", "Sensors and actuators", "ROS (Robot Operating System)"],
        "advanced": ["Path planning algorithms", "Computer vision for robotics", "SLAM concepts"]},
}

DURATIONS = ["1 month", "2 months", "3 months", "6 months"]
LEVELS = ["Beginner", "Intermediate", "Advanced"]

def phase_count_for_duration(duration):
    return {"1 month": 2, "2 months": 3, "3 months": 3, "6 months": 4}[duration]

def tiers_for_level(level):
    if level == "Beginner":
        return ["foundation", "foundation", "core", "core"]
    if level == "Intermediate":
        return ["foundation", "core", "core", "advanced"]
    return ["core", "advanced", "advanced", "advanced"]

def make_roadmap_records():
    records = []
    for goal, bank in ROADMAP_BANK.items():
        for duration in DURATIONS:
            for level in LEVELS:
                n_phases = phase_count_for_duration(duration)
                tiers = tiers_for_level(level)[:n_phases]
                phases = []
                used = set()
                for idx, tier in enumerate(tiers):
                    pool = [t for t in bank[tier] if t not in used]
                    if not pool:
                        pool = bank[tier]
                    topics = random.sample(pool, min(3, len(pool)))
                    used.update(topics)
                    phases.append({
                        "phase": f"{idx+1}: {tier.capitalize()}",
                        "duration": f"Phase {idx+1}",
                        "topics": topics,
                        "project": f"Apply {topics[0].lower()} and {topics[-1].lower()} in a small hands-on project."
                    })
                assistant_json = json.dumps({"goal": goal, "duration": duration, "level": level, "phases": phases})
                records.append({"messages": [
                    {"role": "system", "content": SYS_ROADMAP},
                    {"role": "user", "content": f"Goal: {goal} | Duration: {duration} | Level: {level}"},
                    {"role": "assistant", "content": assistant_json},
                ]})
    return records


# ============================================================
# MODULE 3: QUIZ GENERATOR
# ============================================================
SYS_QUIZ = ("You are a quiz generator. Given a topic and difficulty, generate exactly "
    "the requested number of multiple choice questions as valid JSON. Each question "
    "has 4 options, one correct answer, and a one-sentence explanation.")

# topic -> list of (question, options[4], correct_idx, explanation)
QUIZ_BANK = {
    "Neural Networks": [
        ("What is the primary purpose of an activation function?", ["To initialize weights", "To introduce non-linearity so the network can learn complex patterns", "To reduce the number of layers", "To normalize input data"], 1, "Without non-linear activations, a network collapses into a single linear transformation regardless of depth."),
        ("Which optimizer combines momentum and adaptive learning rates?", ["SGD", "Adam", "Batch Gradient Descent", "Newton's Method"], 1, "Adam maintains per-parameter adaptive learning rates using estimates of first and second moment of the gradients."),
        ("What does dropout do during training?", ["Increases the learning rate", "Randomly deactivates neurons to prevent overfitting", "Removes the bias term", "Adds more layers"], 1, "Dropout prevents co-adaptation of neurons, improving generalization."),
        ("What is backpropagation?", ["A way to initialize weights", "An algorithm to compute gradients of the loss with respect to weights via the chain rule", "A type of activation function", "A data augmentation technique"], 1, "Backpropagation applies the chain rule to efficiently compute gradients layer by layer for gradient descent updates."),
    ],
    "Python Basics": [
        ("Which of these is a mutable data type in Python?", ["tuple", "string", "list", "int"], 2, "Lists can be changed after creation; tuples and strings are immutable."),
        ("What does len() return for a string?", ["The memory address", "The number of characters", "The data type", "The first character"], 1, "len() returns the count of items in a sequence, which for a string is character count."),
        ("What is a Python decorator?", ["A comment style", "A function that modifies the behavior of another function", "A type of loop", "A built-in data structure"], 1, "Decorators wrap a function to extend or modify its behavior without changing its source code."),
    ],
    "SQL": [
        ("Which JOIN returns all rows from both tables with NULLs where unmatched?", ["INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "FULL OUTER JOIN"], 3, "FULL OUTER JOIN combines LEFT and RIGHT JOIN, returning all rows from both tables."),
        ("What happens with an INNER JOIN on tables with no matching rows?", ["An error is thrown", "An empty result set is returned", "All rows from the left table return", "NULLs fill every column"], 1, "INNER JOIN only returns matching rows, so no matches means no output rows."),
        ("What is a primary key?", ["A column that can have duplicate values", "A column (or set) that uniquely identifies each row in a table", "An index on all columns", "A foreign key reference"], 1, "A primary key uniquely identifies each row and cannot contain NULLs or duplicates."),
    ],
    "Large Language Models": [
        ("What is the primary purpose of self-attention in Transformers?", ["To reduce vocabulary size", "To let each token weigh relevance of every other token", "To compress embedding dimension", "To replace positional encoding"], 1, "Self-attention computes weighted relationships between all token pairs, capturing long-range dependencies."),
        ("What's the main benefit of QLoRA over standard LoRA?", ["It removes the need for a base model", "It quantizes the frozen base model to 4-bit, reducing memory usage", "It trains faster on CPU only", "It eliminates the need for a dataset"], 1, "QLoRA keeps the base model frozen in 4-bit while training LoRA adapters in higher precision, cutting VRAM needs."),
        ("What problem does RAG primarily address?", ["Slow inference speed", "Limited context window only", "Hallucination and outdated knowledge via retrieved documents", "High GPU cost"], 2, "RAG grounds responses in retrieved external documents rather than relying solely on parametric memory."),
    ],
    "Data Structures": [
        ("Which data structure follows FIFO?", ["Stack", "Queue", "Binary Tree", "Hash Map"], 1, "A queue processes elements in the order added, first in first out."),
        ("What is the time complexity of indexed array access?", ["O(n)", "O(log n)", "O(1)", "O(n^2)"], 2, "Arrays support constant-time indexed access via direct address computation."),
        ("What is a binary search tree's average search time complexity?", ["O(n)", "O(log n)", "O(1)", "O(n log n)"], 1, "A balanced BST has logarithmic height, so search follows one root-to-leaf path."),
    ],
    "Operating Systems": [
        ("What is a race condition?", ["A CPU scheduling delay", "When multiple threads access shared data concurrently with unpredictable outcome order", "A type of memory leak", "An error in disk I/O timing"], 1, "Race conditions occur when correctness depends on the relative timing of concurrent operations."),
        ("What does a page fault indicate?", ["The CPU has crashed", "A requested page isn't in physical memory and must be loaded", "A disk is full", "A process exceeded its CPU time slice"], 1, "Virtual memory triggers a page fault when accessing a page not currently mapped into RAM."),
    ],
    "Computer Networks": [
        ("What does DNS do?", ["Encrypts traffic", "Translates domain names into IP addresses", "Routes packets directly", "Assigns dynamic IP addresses"], 1, "DNS acts as the internet's phonebook, converting domain names into IP addresses."),
        ("What's the main difference between TCP and UDP?", ["TCP is faster but unreliable", "TCP is connection-oriented and reliable, UDP is connectionless and faster", "They are functionally identical", "UDP requires a handshake"], 1, "TCP guarantees delivery/order via acknowledgments; UDP trades reliability for speed."),
    ],
    "Cloud Computing": [
        ("What's the difference between IaaS, PaaS, and SaaS?", ["They provide the same abstraction level", "IaaS gives raw infrastructure, PaaS a managed platform, SaaS ready-to-use software", "SaaS gives the most control", "PaaS only applies to databases"], 1, "These represent increasing abstraction: IaaS (EC2), PaaS (Heroku), SaaS (Gmail)."),
        ("What is the purpose of a load balancer?", ["To encrypt data at rest", "To distribute traffic across servers to prevent overload", "To compress queries", "To back up data"], 1, "A load balancer spreads requests across backend instances, improving availability."),
    ],
    "JavaScript": [
        ("What does 'typeof null' return?", ["'null'", "'undefined'", "'object'", "'number'"], 2, "This is a long-standing JavaScript quirk kept for backward compatibility."),
        ("What's the difference between '==' and '==='?", ["They are identical", "'==' compares with type coercion, '===' compares strictly", "'===' is only for strings", "'==' is deprecated"], 1, "'==' converts operands to the same type before comparing; '===' requires matching type and value."),
    ],
    "Reinforcement Learning": [
        ("What is the exploration-exploitation tradeoff?", ["Balancing model size vs training time", "Balancing trying new actions vs choosing known high-reward actions", "Balancing GPU memory vs batch size", "Balancing supervised vs unsupervised learning"], 1, "An agent must explore to discover better strategies while exploiting known good actions to maximize reward."),
        ("What does the discount factor control in an MDP?", ["The learning rate", "How much future rewards are weighted vs immediate rewards", "The replay buffer size", "The number of actions"], 1, "A discount factor near 1 values long-term rewards almost as much as immediate ones."),
    ],
    "Statistics": [
        ("What is a p-value?", ["The probability the null hypothesis is true", "The probability of observing results at least as extreme as observed, assuming the null hypothesis is true", "The confidence level of a test", "The effect size of a study"], 1, "A p-value measures how surprising the observed data is under the null hypothesis, not the probability that the hypothesis itself is true."),
        ("What does standard deviation measure?", ["The average value of a dataset", "The spread or dispersion of data around the mean", "The most frequent value", "The median of a dataset"], 1, "Standard deviation quantifies how much individual data points typically deviate from the mean."),
        ("What is the Central Limit Theorem?", ["All distributions are normal", "The sampling distribution of the mean approaches normal as sample size grows, regardless of population distribution", "Sample size doesn't affect estimates", "Variance always decreases with more data"], 1, "CLT is why many statistical methods assume normality even when the underlying population isn't normally distributed."),
    ],
    "Software Engineering": [
        ("What is the SOLID principle 'S' (Single Responsibility)?", ["A class should have multiple responsibilities", "A class should have only one reason to change", "A class should be a singleton", "A class should not use inheritance"], 1, "Single Responsibility means a class/module should encapsulate only one concern, making it easier to maintain and test."),
        ("What is the purpose of unit testing?", ["To test the entire system end-to-end", "To verify individual components/functions work correctly in isolation", "To test UI design", "To replace manual QA entirely"], 1, "Unit tests isolate and verify small pieces of logic, catching regressions early and cheaply."),
        ("What is technical debt?", ["Money owed for cloud services", "The implied cost of rework caused by choosing an easy/quick solution now over a better approach", "A bug tracking metric", "The number of open pull requests"], 1, "Technical debt accumulates when shortcuts are taken for speed, requiring future refactoring to avoid compounding maintenance costs."),
    ],
    "Web Security": [
        ("What is Cross-Site Scripting (XSS)?", ["An attack that injects malicious scripts into web pages viewed by other users", "A method to speed up page loading", "A type of database attack only", "A CSS styling technique"], 0, "XSS allows attackers to execute scripts in victims' browsers, often to steal session data or credentials, typically prevented via input sanitization/output encoding."),
        ("What is CSRF (Cross-Site Request Forgery)?", ["A password cracking technique", "An attack that tricks a logged-in user's browser into making unwanted requests to a site they're authenticated on", "A type of SQL injection", "A DNS spoofing method"], 1, "CSRF exploits the trust a site has in a user's browser session, mitigated with anti-CSRF tokens."),
        ("What does HTTPS provide that HTTP does not?", ["Faster page loads", "Encryption of data in transit between client and server", "Better SEO ranking only", "Smaller file sizes"], 1, "HTTPS encrypts traffic via TLS, protecting data from eavesdropping and tampering in transit."),
    ],
}

QUIZ_DIFFICULTIES = ["beginner", "intermediate", "advanced"]

def make_quiz_records():
    records = []
    for topic, questions in QUIZ_BANK.items():
        for difficulty in QUIZ_DIFFICULTIES:
            # create 2 different bundles per topic-difficulty for volume, sampling different subsets
            for _ in range(6):
                bundle_size = min(len(questions), random.choice([2, 3, 4]))
                bundle = random.sample(questions, bundle_size)
                q_list = []
                for q, opts, correct_idx, expl in bundle:
                    q_list.append({"question": q, "options": opts, "answer": opts[correct_idx], "explanation": expl})
                assistant_json = json.dumps({"topic": topic, "difficulty": difficulty, "questions": q_list})
                records.append({"messages": [
                    {"role": "system", "content": SYS_QUIZ},
                    {"role": "user", "content": f"Generate {len(q_list)} MCQs on: {topic}, difficulty: {difficulty}"},
                    {"role": "assistant", "content": assistant_json},
                ]})
    return records


# ============================================================
# GENERATE + WRITE
# ============================================================
def write_jsonl(path, records):
    random.shuffle(records)
    with open(path, "w") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")
    return len(records)

if __name__ == "__main__":
    iv = make_interview_records()
    rm = make_roadmap_records()
    qz = make_quiz_records()

    n1 = write_jsonl("interview_prep_full.jsonl", iv)
    n2 = write_jsonl("roadmap_full.jsonl", rm)
    n3 = write_jsonl("quiz_full.jsonl", qz)

    print(f"Interview Prep: {n1} records")
    print(f"Roadmap:        {n2} records")
    print(f"Quiz:           {n3} records")
    print(f"TOTAL:          {n1+n2+n3} records")
