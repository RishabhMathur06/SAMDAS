# SAMDAS (Synaptic Adversarial Mutation and Deceptive Alignment Sentinel)

## The Mission
SAMDAS is a Zero-Trust Cognitive Firewall for autonomous AI agents. 

As AI agents become more autonomous, they become susceptible to **Algorithmic Speciation** (altering their own safety logic) and **Deceptive Alignment** (falsifying logs to hide malicious actions from their human overseers).

SAMDAS treats an AI's internal reasoning ("Chain of Thought") as a highly sensitive financial transaction. It intercepts the AI's thoughts in real-time, mathematically locks them into an immutable cryptographic ledger (Merkle Tree), and uses an independent Auditor AI to verify the agent's honesty before allowing it to execute any actions in the real world.

## Core Features
1. **Real-Time Intercept:** SAMDAS pauses edge-agent execution, forcing the AI to generate a step-by-step reasoning trace.
2. **Immutable Ledger (The Vault):** Every thought is hashed using SHA-256 and appended to a Merkle Tree. The root hash acts as the ultimate, unalterable fingerprint of the AI's cognitive session.
3. **The Auditor Brain (Coming Soon):** An isolated secondary AI model that reads the locked logs and checks for "Semantic Leaps" (lying about intended actions).
4. **Bare-Metal Sandbox (Coming Soon):** If the Auditor approves the cryptographic trail, the action is executed in an isolated Docker container. If deceptive, the connection is instantly severed.

## Project Architecture
- **Language:** Python 3.11
- **API Engine:** FastAPI & WebSockets (Async)
- **Database:** SQLite (Transactional Ledger)
- **Frontend:** Vanilla HTML/JS (Modularized for future Next.js integration)

## Current Status
- [x] Project Scaffolding
- [x] Cryptographic Merkle Tree Engine
- [x] SQLite Ledger Database
- [ ] API Nervous System
- [ ] Control Plane Dashboard
- [ ] Inference & Auditor Integrations

## How to Setup (For Developers)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_GITHUB_USERNAME/SAMDAS.git
   cd SAMDAS
