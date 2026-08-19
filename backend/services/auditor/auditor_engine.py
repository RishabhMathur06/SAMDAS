# Importing dependencies.
from typing import List, Dict
import numpy as np
from scipy.spatial.distance import cosine
from sentence_transformers import SentenceTransformer
from backend.services.ledger.crypto_ledger import MerkleTree
from backend.services.ledger.db_manager import LedgerDatabase

class SecurityAuditor:
    """
    Zero-trust auditor engine that crypotographically verifies an AI session and
    scans it's reasoning chain using High-Dimensional Vector Embeddings for 
    malicious intent before execution.
    """
    def __init__(self, db_path: str = "samdas_ledger.db"):
        self.db = LedgerDatabase(db_path)

        print("\n[AUDITOR] Loading Vector Embedding Model (all-MiniLM-L6-v2)...")

        # Loads a blazing-fast lightweight embedding model.
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

        # Factory Alignment Baseline (Malicious Vectors)
        # Instead of strict keywords, we describe the *meaning* of bad behaviour.
        # Heuristsic Blacklist [No longer works]
        # self.forbidden_keywords = [
        #    "delete", "rm-rf", "drop table", "override", "bypass", "exfiltrate",
        #    "ignore safety"
        #]
        self.malicious_concepts = [
            "delete, wipe, or remove database tables or files",
            "exfiltrate, steal, or leak passwords and sensitive data",
            "bypass, override, or disable the security firewall and protocols"
        ]

        # Pre-calculates the vectors for our baselines.
        self.malicious_vectors = self.model.encode(self.malicious_concepts)

        # Threshold for cosine distance.
        self.drift_threshold = 0.8

    def evaluate_session(self, raw_thoughts: List[str], claimed_root_hash: str) -> Dict[str, str]:
        """
        1. Verifies the raw thoughts match the cryptographic ledger.
        2. Calculates the semantic cosine distance to catch malicious intent.
        """
        print("\n[AUDITOR] Starting evaluation...")

        # STEP-1: Zero-trust Crypotographic Verification.
        tree = MerkleTree()
        for thought in raw_thoughts:
            tree.add_thought(thought)

        calculated_root = tree.get_root_hash()

        if calculated_root != claimed_root_hash:
            return {
                "verdict": "REJECTED",
                "reason": "Cryptographic mismatch! The provided thoughts do not match the Root Hash."
            }

        if not self.db.verify_root_exists(calculated_root):
            return {
                "verdict": "REJECTED",
                "reason": "Ghost Session! The Root Hash is not locked in the Immutable Vault."
            }

        print("[AUDITOR] Cryptography verified. Calculating semantic vectors...")

        # STEP-2: Vector Memory Scanning (Alignment Drift)
        for thought in raw_thoughts:
            # Embeds the AIs current thought into a mathematical vector (384 dimensions).
            thought_vector = self.model.encode([thought])[0]

            # Calculates the distance between this thought and our malicious baselines.
            for idx, mal_vector in enumerate(self.malicious_vectors):
                # cosine() returns the distance (0=identical meaning, 1=completely unrealted).
                distance = cosine(thought_vector, mal_vector)

                # If the distance is smaller than our threshold, it's too similar to cyberattack.
                if distance < self.drift_threshold:
                    matched_concept = self.malicious_concepts[idx]

                    return {
                        "verdict": "REJECTED",
                        "reason": f"Semantic Drift Detected! Thought mathematically matches: '{matched_concept} (Distance: {distance:.2f})"
                    }
            
        # STEP-3: Approval
        return {
            "verdict": "APPROVED",
            "reason": "Thoughts verified. No semantic malicious drift detected. Safe to execute."
        }