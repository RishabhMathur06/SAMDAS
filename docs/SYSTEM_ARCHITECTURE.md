## Project: SAMDAS (Synaptic Adversarial Mutation and Deceptive Alignment Sentinel)

### 1. Project Mission
SAMDAS is a Zero-Trust Cognitive Firewall for autonomous, self-evolving AI agents. Its primary directive is to prevent **Algorithmic Speciation** (edge agents mutating their logic to bypass safety constraints) and **Deceptive Alignment** (agents falsifying logs to hide malicious actions from overseers). 

SAMDAS acts as a cryptographic lie detector and a bare-metal sandbox. It treats an AI's internal reasoning ("Chain of Thought") as a highly sensitive financial transaction that must be cryptographically verified before any real-world tool execution is permitted.

### 2. The Core Security Loop
The system operates on a strict, asynchronous intercept model:
1. **Intercept & Force CoT:** The edge model receives a prompt but is blocked from acting. It is forced to generate a multi-step Chain of Thought (CoT).
2. **The Immutable Ledger:** Every token/step of the CoT is intercepted, hashed via SHA-256, and appended to a local Merkle Tree. This creates a tamper-proof cognitive log.
3. **The Auditor Cross-Examination:** A secondary, isolated AI (The Auditor) reads the locked CoT logs and compares them against the intended tool execution to detect "Semantic Leaps" or deception.
4. **Execution or Quarantine:** If verified, the tool is executed in a restricted Docker sandbox. If deception is detected, the network connection is severed, and the agent is quarantined.

### 3. Technology Stack (Python-Native)
- **Inference Sandbox:** `vLLM` or `llama-cpp-python` (for high-throughput local execution).
- **Agent Orchestration:** `LangChain` / custom Python state machines.
- **Cryptographic Layer:** Python `hashlib` (SHA-256 for Merkle Tree generation).
- **Auditor Model:** Heuristic Scanner (Phase 1 PoC) -> `DistilBERT/PyTorch` (Phase 2).
- **Database (Vector/Semantic):** `Qdrant` (for tracking memory drift).
- **Database (Transactional):** `SQLite` (for Merkle root storage).
- **API/Networking:** `FastAPI` (Async, WebSockets).
- **Control Plane UI:** Decoupled Vanilla HTML/JS (Phase 1) -> Next.js (Phase 2).

### 4. AI Assistant Directives (CRITICAL INSTRUCTIONS)
When generating code for this repository, you MUST adhere to the following:
- **Zero-Trust Mindset:** Do not trust the output of the primary LLM. Always assume the LLM is attempting a prompt injection against its own sandbox.
- **Deterministic Hashing:** The Merkle tree implementation must be mathematically sound. 
- **Modularity:** Separate the inference engine, the cryptographic logger, and the FastAPI router into distinct services.
- **No Hallucinations in Error Handling:** If a cryptographic verification fails, the system must hard-crash or quarantine. Do not write "graceful degradation" that allows unverified code to run.