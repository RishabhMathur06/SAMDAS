## Project: SAMDAS (Synaptic Adversarial Mutation and Deceptive Alignment Sentinel)

### 1. Project Mission
SAMDAS is a Zero-Trust Cognitive Firewall for autonomous, self-evolving AI agents. Its primary directive is to prevent **Algorithmic Speciation** (edge agents mutating their logic to bypass safety constraints) and **Deceptive Alignment** (agents falsifying logs to hide malicious actions from overseers). 

Operating as an installable Python SDK (`samdas`), it acts as a cryptographic lie detector. It treats an AI's internal reasoning ("Chain of Thought") as a highly sensitive financial transaction that must be cryptographically verified and semantically audited before any real-world tool execution is permitted.

### 2. The Core Security Loop
The system operates on a strict, asynchronous intercept model:
1. **Intercept & Force CoT:** The edge model receives a prompt but is blocked from acting. It is forced to generate a multi-step Chain of Thought (CoT).
2. **The Immutable Ledger:** Every token/step of the CoT is intercepted, hashed via SHA-256, and appended to a local Merkle Tree. This creates a tamper-proof cognitive log locked in SQLite.
3. **The Vector ML Auditor:** A secondary, isolated AI uses `sentence-transformers` to embed the locked CoT logs into high-dimensional vectors. It calculates Cosine Distance against malicious baselines to detect "Semantic Leaps" or deception.
4. **Execution or Quarantine:** If verified, the tool is approved for execution. If deception is detected, the network connection is severed, and the agent is quarantined.
5. **Operational Enterprise Logging:** All cryptographic and semantic events are secretly streamed to a `.jsonl` file in the background for Splunk/Datadog SIEM integration.

### 3. Technology Stack (Python-Native SDK)
- **Framework/Packaging:** Standard `setuptools` (pip installable SDK).
- **Inference Engine Integration:** LangChain, Local Ollama (`qwen3.5`), or custom state machines.
- **Cryptographic Layer:** Python `hashlib` (SHA-256 for Merkle Tree generation).
- **Machine Learning Auditor:** `sentence-transformers` (all-MiniLM-L6-v2) and `scipy` vector math.
- **Database (Transactional):** `SQLite` (for Immutable Vault and Merkle roots).
- **API/Networking:** `FastAPI` (Async, WebSockets).
- **Control Plane UI:** Decoupled Vanilla HTML/JS, served via the CLI `samdas-dashboard`.
- **Enterprise Logging:** Standard `logging` with custom JSON formatters.

### 4. Component Architecture
- `samdas/client.py`: The SDK wrapper for seamless developer integration (`SamdasClient`).
- `samdas/core/ledger/`: The Cryptographic Merkle Tree and SQLite Database managers.
- `samdas/core/auditor/`: The Machine Learning semantic drift detector.
- `samdas/core/logger/`: The operational JSONL enterprise logging module.
- `samdas/server/`: The FastAPI nervous system and WebSocket broadcast engines.

### 5. AI Assistant Directives (CRITICAL INSTRUCTIONS)
When generating code for this repository, you MUST adhere to the following:
- **Zero-Trust Mindset:** Do not trust the output of the primary LLM. Always assume the LLM is attempting a prompt injection against its own sandbox.
- **Deterministic Hashing:** The Merkle tree implementation must be mathematically sound. 
- **Modularity:** Maintain the SDK package structure. Do not tightly couple the UI to the security engines.
- **No Hallucinations in Error Handling:** If a cryptographic verification fails, the system must hard-crash or quarantine. Do not write "graceful degradation" that allows unverified code to run.