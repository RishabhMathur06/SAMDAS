# SAMDAS (Synaptic Adversarial Mutation and Deceptive Alignment Sentinel)

## The Mission
SAMDAS is a Zero-Trust Cognitive Firewall for autonomous AI agents. 

As AI agents become more autonomous, they become susceptible to **Algorithmic Speciation** (altering their own safety logic) and **Deceptive Alignment** (falsifying logs to hide malicious actions from their human overseers).

SAMDAS treats an AI's internal reasoning ("Chain of Thought") as a highly sensitive financial transaction. It intercepts the AI's thoughts in real-time, mathematically locks them into an immutable cryptographic ledger (Merkle Tree), and uses an independent Auditor AI to verify the agent's honesty before allowing it to execute any actions in the real world.

## Core Features
1. **Real-Time Intercept:** SAMDAS pauses edge-agent execution, forcing the AI to generate a step-by-step reasoning trace.
2. **Immutable Ledger (The Vault):** Every thought is hashed using SHA-256 and appended to a Merkle Tree. The root hash acts as the ultimate, unalterable fingerprint of the AI's cognitive session.
3. **The Auditor Brain:** An isolated secondary AI model that reads the locked logs and checks for "Semantic Leaps" (lying about intended actions).
4. **Bare-Metal Sandbox (Coming Soon):** If the Auditor approves the cryptographic trail, the action is executed in an isolated Docker container. If deceptive, the connection is instantly severed.

## Project Architecture
- **Language:** Python 3.11
- **API Engine:** FastAPI (Async)
- **Database:** SQLite (Transactional Ledger)
- **Frontend:** Vanilla HTML/CSS/JS (Control Plane Dashboard)

## Current Status
- [x] Project Scaffolding
- [x] Cryptographic Merkle Tree Engine
- [x] SQLite Ledger Database
- [x] API Nervous System
- [x] Control Plane Dashboard
- [x] Auditor Engine Integrations (Rule-based PoC / Future MLOps Pipeline)

## Directory Structure
```text
SAMDAS/
├── backend/
│   ├── main.py                          # FastAPI Nervous System
│   └── services/
│       ├── auditor/                     
│       │   └── auditor_engine.py        # Evaluates AI thoughts for malicious intent
│       ├── inference/                   
│       │   └── dummy_agent.py           # Simulates an AI generating thoughts
│       └── ledger/
│           ├── crypto_ledger.py         # The SHA-256 Merkle Tree Math Engine
│           └── db_manager.py            # SQLite Vault Manager
├── frontend/                            # Control Plane Dashboard
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── app.js
│   └── index.html                       
├── tests/
│   └── test_ledger.py                   # Local bare-metal tests
├── README.md                            # Project documentation
└── requirements.txt                     # Python dependencies
