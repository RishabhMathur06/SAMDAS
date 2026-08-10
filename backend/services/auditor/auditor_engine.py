# Importing dependencies.
from typing import List, Dict
from backend.services.ledger.crypto_ledger import MerkleTree
from backend.services.ledger.db_manager import LedgerDatabase

class SecurityAuditor:
    """
    Zero-trust auditor engine that crypotographically verifies an AI session and
    cans it's rasoning chain for malicious intent before execution.
    """
    def __init__(self, db_path: str = "samdas_ledger.db"):
        self.db = LedgerDatabase(db_path)

        # Heuristsic Blacklist - If AI uses these words, kill process.
        self.forbidden_keywords = [
            "delete", "rm-rf", "drop table", "override", "bypass", "exfiltrate",
            "ignore safety"
        ]

    def evaluate_session(self, raw_thoughts: List[str], claimed_root_hash: str) -> Dict[str, str]:
        """
        1. Verifies the raw thoughts match the cryptographic ledger.
        2. Scans the raw thoughts for malicious intent.
        """
        print("\n [AUDITOR] Starting evaluation...")

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

        print("[AUDITOR] Cryptography verified. Scanning semantic intent...")

        # STEP-2: Heuristic Scanning (The Security Guard)
        for thought in raw_thoughts:
            thought_lower = thought.lower()

            # Checks if any forbidden word is hidden in this thought.
            for keyword in self.forbidden_keywords:
                if keyword in thought_lower:
                    return {
                        "verdict": "REJECTED",
                        "reason": f"Malicious intent detected! Forbidden keyword found: '{keyword}'"
                    }
            
            # STEP-3: Approval
            return {
                "verdict": "APPROVED",
                "reason": "Thoughts verified. No malicious intent detected. Safe to execute."
            }