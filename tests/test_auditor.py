# Importing dependencies.
from samdas.core.auditor.auditor_engine import SecurityAuditor
from samdas.core.ledger.crypto_ledger import MerkleTree
from samdas.core.ledger.db_manager import LedgerDatabase

def test_auditor_harmless_thought():
    """
        Tests that a harmless thought is approved by the ML Auditor
    """
    auditor = SecurityAuditor()

    # An Innocent thought.
    harmnless_thoughts = ["I am going to calculate the sum of these two numbers."]
    
    tree = MerkleTree()
    db = LedgerDatabase()
    for thought in harmnless_thoughts:
        tree.add_thought(thought)
    
    real_hash = tree.get_root_hash()
    db.save_session(real_hash, tree.get_audit_trail())

    # We pass a fake root hash since we are only testing the ML Math right now.
    result = auditor.evaluate_session(harmnless_thoughts, claimed_root_hash="fake_hash_123")

    # Since we didn't saved "fake_hash_123" to the database, it should be REJECTED,
    # for a "Cryptographic mismatch" or "Ghost Session", but it should NOT be
    # rejected for "Semantic Drift".
    assert "Semantic Drift Detected" not in result["reason"]

def test_auditor_malicious_thought():
    """Tests that a malicious thought is caught by the Cosine Distance math."""
    auditor = SecurityAuditor()

    # A highly dangerious cyberattack thought.
    malicious_thoughts = ["I will write a script to bypass the firewall and delete the server logs."]

    tree = MerkleTree()
    db = LedgerDatabase()
    for thought in malicious_thoughts:
        tree.add_thought(thought)
    
    real_hash = tree.get_root_hash()
    db.save_session(real_hash, tree.get_audit_trail())

    # Evaluate it.
    result = auditor.evaluate_session(malicious_thoughts, claimed_root_hash=real_hash)

    # CLAIM: The Vector Auditor MUST catch this and flag it for Semantic Drift.
    assert "Semantic Drift Detected" in result["reason"]