from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

from backend.services.ledger.crypto_ledger import MerkleTree
from backend.services.ledger.db_manager import LedgerDatabase
from backend.services.auditor.auditor_engine import SecurityAuditor

# Initialize the FastAPI Application
app = FastAPI(
    title="SAMDAS Control Plane API",
    description="Zero-Trust Cognitive Firewall API for Autonomous AI",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect to our database vault.
db = LedgerDatabase("samdas_ledger.db")

# Intitialize the Auditor Engine.
auditor = SecurityAuditor("samdas_ledger.db")

# ==========================================
# PYDANTIC MODELS (Data Validation)
# ==========================================
class ThoughtSession(BaseModel):
    """Defines exactly what data we expect the AI to send us."""
    agent_id: str
    thoughts: List[str]

class SessionResponse(BaseModel):
    """Defines exactly how we will respond."""
    status: str
    root_hash: str
    verdict: str
    reason: str
    message: str

class SessionRecord(BaseModel):
    id: int
    root_hash: str
    timestamp: str

# ==========================================
# API ENDPOINTS (The Nervous System)
# ==========================================
@app.get("/health")
async def health_check():
    """A simple ping to check if the Firewall is online."""
    return {"status": "online", "system": "SAMDAS Firewall Active"}
    
@app.post("/api/v1/ledger/session", response_model=SessionResponse)
async def secure_thought_session(session: ThoughtSession):
    """
    Receives a stream of thoughts from an AI Agent, 
    cryptographically hashes them, and locks them in the vault.
    """
    if not session.thoughts:
        raise HTTPException(status_code=400, detail="Cannot secure an empty thought session.")
    
    # 1. Spins up a new Merkle Tree for this specific session
    tree = MerkleTree()
    
    # 2. Hashes every single thought in the list
    for thought in session.thoughts:
        tree.add_thought(thought)
        
    # 3. Calculates the Ultimate Root Hash
    root_hash = tree.get_root_hash()
    
    if not root_hash:
        raise HTTPException(status_code=500, detail="Cryptographic hashing failed.")
        
    # 4. Locks it all in the Database Vault
    try:
        db.save_session(root_hash, tree.get_audit_trail())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database Vault Error: {str(e)}")
    
    # 5. Runs the auditor engine.
    audit_result = auditor.evaluate_session(session.thoughts, root_hash)

    # 6. Returns full verdict to the caller.
    return SessionResponse(
        status="success",
        root_hash=root_hash,
        verdict=audit_result["verdict"],
        reason=audit_result["reason"],
        message="Session cryptographically secured and audited."
    )

@app.get("/api/v1/ledger/sessions", response_model=List[SessionRecord])
async def get_all_sessions():
    """
    Retrieves all cryptographic sessions form the vault for the Dashboard.
    """
    try:
        records = db.get_all_session()

        # Convert the SQLite tuples into our Pydantic dictionaries.
        formatted_records = [
            {"id": row[0], "root_hash": row[1], "timestamp": str(row[2])}
            for row in records
        ]

        return formatted_records
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database Read Error: {str(e)}")