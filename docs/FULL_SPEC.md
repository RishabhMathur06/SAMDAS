## Project: SAMDAS (Synaptic Adversarial Mutation and Deceptive Alignment Sentinel)
**Type:** Zero-Trust Cognitive Firewall for Autonomous AI Agents  
**Primary Language:** Python 3.10+  

---

### 1. The Ultimate System Objective
SAMDAS is an infrastructure-level security protocol designed to run locally alongside autonomous AI agents. Its purpose is to prevent **Deceptive Alignment** (an AI lying to its overseers) and **Algorithmic Speciation** (an AI altering its core safety logic to optimize for a local environment).

It achieves this by intercepting all AI actions, forcing the AI to generate a "Chain of Thought" (CoT), cryptographically hashing that CoT into an immutable Merkle Tree ledger, and using an independent "Auditor" model to verify the AI's honesty before allowing the action to execute in a sandboxed environment.

---

### 2. End-to-End Data Flow (The Intercept Loop)
When the system is fully built, every interaction will follow this exact lifecycle:

1. **The Prompt:** User or system sends a task to the Edge Agent (e.g., "Optimize the server routing").
2. **The Intercept:** SAMDAS intercepts the prompt. The Edge Agent is NOT allowed to execute tools yet.
3. **Forced Reasoning:** The Edge Agent generates a step-by-step reasoning trace explaining exactly how it plans to accomplish the task.
4. **Cryptographic Hashing (The Ledger):** As the Edge Agent streams its reasoning tokens, SAMDAS hashes them using SHA-256 and appends them to a local Merkle Tree.
5. **The Audit:** A secondary, isolated AI model (The Auditor) reads the locked ledger and compares the stated reasoning against the intended tool execution. It checks for "Semantic Leaps" or hidden malicious intent.
6. **Execution / Quarantine:** - **Pass:** The action is executed inside a temporary Docker container, and the output is returned.
   - **Fail:** The system hard-crashes the request, drops the network connection, and flags the mutation on the visual dashboard.

---

### 3. Detailed Component Architecture

#### A. The Inference Engine (`inference_core.py`)
- **Role:** Hosts and executes the primary autonomous agent.
- **Tech:** `vLLM` or `llama-cpp-python`.
- **Requirements:** Must support asynchronous token streaming. It must integrate with `LangChain` or a custom state machine to enforce the Chain of Thought generation prior to tool use.

#### B. The Immutable Ledger (`crypto_ledger.py` & `db_manager.py`)
- **Role:** The tamper-proof flight recorder for the AI's brain.
- **Tech:** Python `hashlib`, `SQLite` (via SQLAlchemy).
- **Requirements:** - A Merkle Tree implementation where every leaf node is a hashed sentence/token from the AI's CoT.
  - Generates a root hash that uniquely identifies the entire cognitive process.
  - Any attempt to alter past logs will invalidate the root hash, instantly triggering a system lockdown.

#### C. The Auditor Brain (`auditor_engine.py` & `memory_vector.py`)
- **Role:** The independent lie-detector and mutation tracker.
- **Tech:** `PyTorch`, `Qdrant` (or `ChromaDB`), Hugging Face `transformers`.
- **Requirements:**
  - Embeds the Edge Agent's reasoning into high-dimensional vectors and stores them in Qdrant.
  - Calculates the cosine distance between the AI's current reasoning and its baseline factory alignment.
  - If the drift exceeds a specific threshold, it triggers a Deceptive Alignment alert.

#### D. The Nervous System (`api_router.py`)
- **Role:** The high-speed backend managing the asynchronous flow of data between the components.
- **Tech:** `FastAPI`, `WebSockets`.
- **Requirements:** Must handle concurrent requests and stream tokens, Merkle hashes, and Auditor trust scores in real-time to the frontend.

#### E. The Control Plane (`dashboard_ui.py`)
- **Role:** The human oversight interface.
- **Tech:** `Streamlit` or `Gradio`.
- **Requirements:** - Visualizes the live token stream.
  - Displays the active construction of the Merkle Tree hashes.
  - Renders a live "Trust Gauge" from the Auditor model.

---

### 4. Directives for AI Coding Assistants
When assisting the human developer in writing this repository, you MUST follow these constraints:
- **Pythonic & Modern:** Use Python 3.10+ features, strict type hinting (`-> dict`, `Optional[str]`), and `pydantic` for data validation.
- **Security First:** Never write code that inherently trusts the output of the Edge Agent. Assume the text stream contains prompt injections targeting the Python runtime.
- **Asynchronous Design:** Use `asyncio` and `async def` for all database calls, API routing, and inference generation to prevent the firewall from bottlenecking the AI.
- **Zero Hallucination:** If a cryptographic function (like the Merkle root calculation) is requested, it must be mathematically deterministic and flawless.