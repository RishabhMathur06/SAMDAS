# SAMDAS (Synaptic Adversarial Mutation and Deceptive Alignment Sentinel)

## The Mission
SAMDAS is a Zero-Trust Cognitive Firewall for autonomous AI agents. 

As AI agents become more autonomous, they become susceptible to **Algorithmic Speciation** (altering their own safety logic) and **Deceptive Alignment** (falsifying logs to hide malicious actions from their human overseers).

SAMDAS treats an AI's internal reasoning ("Chain of Thought") as a highly sensitive financial transaction. It intercepts the AI's thoughts in real-time, mathematically locks them into an immutable cryptographic ledger (Merkle Tree), and uses an independent Auditor AI to verify the agent's honesty before allowing it to execute any actions in the real world.

## Core Features
1. **Real-Time Intercept:** SAMDAS pauses edge-agent execution, forcing the AI to generate a step-by-step reasoning trace.
2. **Immutable Ledger (The Vault):** Every thought is hashed using SHA-256 and appended to a Merkle Tree. The root hash acts as the ultimate, unalterable fingerprint of the AI's cognitive session.
3. **The ML Auditor Brain:** Uses `sentence-transformers` to generate dense vector embeddings of the AI's thoughts. It calculates the Cosine Distance against a baseline of known malicious concepts to mathematically detect semantic drift and deceptive alignment.
4. **Real-Time WebSocket Dashboard:** A Push-architecture control plane that streams cryptographic verdicts to a web UI in real-time, providing zero-latency alerting for security admins.
5. **Operational Enterprise Logging:** Built-in logging that secretly streams structured JSON lines (`.jsonl`) to a background file for Splunk/Datadog integration, while maintaining a clean developer console.
6. **Bare-Metal Sandbox (Coming Soon):** If the Auditor approves the cryptographic trail, the action is executed in an isolated Docker container. If deceptive, the connection is instantly severed.

## Project Architecture
- **Language:** Python 3.11
- **Inference Engine:** LangChain + Ollama (`qwen3.5`) for 100% localized, air-gapped AI reasoning.
- **Machine Learning Auditor:** `sentence-transformers` (all-MiniLM-L6-v2) and `scipy` for Cosine Distance vector math.
- **API Engine:** FastAPI (Async) with `websockets` for live Push architecture.
- **Database:** SQLite (Transactional Ledger)
- **Frontend:** Vanilla HTML/CSS/JS (Real-Time Control Plane Dashboard)

## Current Status
- [x] Project Scaffolding
- [x] Cryptographic Merkle Tree Engine
- [x] SQLite Ledger Database
- [x] API Nervous System
- [x] Control Plane Dashboard
- [x] Live WebSockets Dashboard Streaming (Push Architecture)
- [x] Machine Learning Auditor Engine (Vector Semantic Embeddings & Cosine Distance)
- [x] Live AI Agent Integration (LangChain + Local Ollama LLMs)
- [x] Operational Logging Module (JSONL Enterprise formatting)

## Directory Structure
```text
SAMDAS/
├── samdas/                              # The Python SDK Package
│   ├── client.py                        # SDK Wrapper (SamdasClient)
│   ├── cli.py                           # CLI entry points
│   ├── server/
│   │   └── main.py                      # FastAPI Nervous System
│   ├── core/
│   │   ├── auditor/                     
│   │   │   └── auditor_engine.py        # Evaluates AI thoughts
│   │   ├── logger/
│   │   │   └── logger.py                # Operational JSON logger
│   │   └── ledger/
│   │       ├── crypto_ledger.py         # Merkle Tree Math Engine
│   │       └── db_manager.py            # SQLite Vault Manager
│   └── ui/                              # Control Plane Dashboard
│       ├── css/style.css
│       ├── js/app.js
│       └── index.html                       
├── examples/
│   └── langchain_agent.py               # Autonomous agent using the SDK
├── tests/
│   └── test_ledger.py                   # Local bare-metal tests
├── README.md                            # Project documentation
└── setup.py                             # Python package definition
```

## How to Setup (For Developers)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_GITHUB_USERNAME/SAMDAS.git
   cd SAMDAS
   ```

2. **Setup the Virtual Environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
3. **Install the SDK:**
   ```bash
   pip install -e .
   ```

4. **Install and Pull Local LLM:**
   Make sure you have [Ollama](https://ollama.com/) installed, then run:
   ```bash
   ollama pull qwen3.5
   ```

5. **Start the Control Plane:**
   ```bash
   samdas-dashboard
   ```

6. **Launch the Dashboard:**
   Open a new terminal and run:
   ```bash
   open samdas/ui/index.html
   ```

7. **Trigger the Autonomous Agent:**
   In another terminal, run:
   ```bash
   python examples/langchain_agent.py
   ```
