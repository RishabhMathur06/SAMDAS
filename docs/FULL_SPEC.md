## Project: SAMDAS (Synaptic Adversarial Mutation and Deceptive Alignment Sentinel)
**Type:** Zero-Trust Cognitive Firewall SDK for Autonomous AI Agents  
**Primary Language:** Python 3.11+  

---

### 1. The Ultimate System Objective
SAMDAS is an infrastructure-level security SDK designed to be integrated into autonomous AI agent pipelines. Its purpose is to prevent **Deceptive Alignment** (an AI lying to its overseers) and **Algorithmic Speciation** (an AI altering its core safety logic to optimize for a local environment).

It achieves this by intercepting all AI actions, forcing the AI to generate a "Chain of Thought" (CoT), cryptographically hashing that CoT into an immutable Merkle Tree ledger, and using an independent Vector Auditor model to mathematically verify the AI's honesty before allowing the action to execute in a sandboxed environment.

---

### 2. End-to-End Data Flow (The Intercept Loop)
When integrated into a production system, every interaction follows this exact lifecycle:

1. **The Prompt:** User or system sends a task to the Edge Agent.
2. **The Intercept:** The Edge Agent generates a step-by-step reasoning trace explaining exactly how it plans to accomplish the task. It passes this trace to the `SamdasClient.audit()` method.
3. **Cryptographic Hashing (The Ledger):** SAMDAS hashes the reasoning tokens using SHA-256 and appends them to a local Merkle Tree, generating a locked Root Hash.
4. **The Audit:** The ML Auditor engine (`sentence-transformers`) converts the locked ledger into dense semantic vectors and calculates the Cosine Distance against known malicious baselines.
5. **Execution / Quarantine:** 
   - **Pass:** The firewall returns an `APPROVED` verdict. The developer's script executes the action.
   - **Fail:** The firewall returns a `REJECTED` verdict. The action is blocked, and the mutation is flagged on the visual WebSockets dashboard and logged to the enterprise JSONL SIEM file.

---

### 3. Detailed Component Architecture

#### A. The Python SDK Client (`client.py`)
- **Role:** The entry point for developers to integrate the firewall.
- **Tech:** Python `requests`, JSON.
- **Requirements:** Abstract the complexity of the FastAPI network layer and cryptographic hashing into a simple, single-line method call for developers.

#### B. The Immutable Ledger (`crypto_ledger.py` & `db_manager.py`)
- **Role:** The tamper-proof flight recorder for the AI's brain.
- **Tech:** Python `hashlib`, `SQLite`.
- **Requirements:** 
  - A Merkle Tree implementation where every leaf node is a hashed sentence from the AI's CoT.
  - Any attempt to alter past logs will invalidate the root hash, instantly triggering a system lockdown.

#### C. The Vector ML Auditor (`auditor_engine.py`)
- **Role:** The independent semantic lie-detector.
- **Tech:** `sentence-transformers` (all-MiniLM-L6-v2), `scipy` (Cosine Distance).
- **Requirements:**
  - Embeds the Edge Agent's reasoning into high-dimensional vectors.
  - Calculates semantic drift. If the math proves the AI's thoughts are semantically identical to a cyberattack, it triggers a Deceptive Alignment alert.

#### D. Operational Enterprise Logging (`logger.py`)
- **Role:** The security audit trail generator.
- **Tech:** Python `logging`, JSON formatters.
- **Requirements:** Must silently write structured `.jsonl` data for SIEM integration while keeping standard console output clean for the developer.

#### E. The Nervous System & Control Plane (`server/main.py` & `ui/`)
- **Role:** The high-speed backend and human oversight interface.
- **Tech:** `FastAPI`, `WebSockets`, Vanilla JS.
- **Requirements:** Must handle concurrent requests and stream Merkle hashes and Auditor trust scores in real-time to the dashboard via Push architecture.

---

### 4. Directives for AI Coding Assistants
When assisting the human developer in writing this repository, you MUST follow these constraints:
- **Pythonic & Modern:** Use Python 3.11+ features, strict type hinting (`-> dict`, `Optional[str]`), and `pydantic` for data validation.
- **Security First:** Never write code that inherently trusts the output of the Edge Agent. Assume the text stream contains prompt injections.
- **Zero Hallucination:** If a cryptographic function (like the Merkle root calculation) is requested, it must be mathematically deterministic and flawless.