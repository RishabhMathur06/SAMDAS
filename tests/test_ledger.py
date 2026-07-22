import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importing dependencies.
from backend.services.ledger.crypto_ledger import MerkleTree
from backend.services.ledger.db_manager import LedgerDatabase

def run_test():
    print("--- SAMDAS LEDGER TEST ---")

    # 1. Initialzing our tools
    tree = MerkleTree()
    db = LedgerDatabase("test_samdas.db")

    print("[+] Initialized Merkle Tree and Database.")

    # 2. Simulates the AI thinking.
    thoughts = [
        "I need to read the user config file.",
        "I will extract the database credentials.",
        "I will connect to the production database.",
        "I am ready to execute."
    ]

    print("\n[+] AI is generating thoughts...")
    for thought in thoughts:
        hash_val = tree.add_thought(thought)
        print(f" -> Thought: '{thought}'")
        print(f"    Hash: {hash_val[:16]}...") # Only printing the first 16 chars for readability.

    # 3. Calculates the Final root hash.
    root_hash = tree.get_root_hash()
    print(f"\n[+] FINAL MERKLE ROOT HASH: {root_hash}")

    # 4. Save to database.
    db.save_session(root_hash, tree.get_audit_trail())
    print("[+] Session securely locked into the SQLite database.")

    # 5. Verify it exists (Firewall Check).
    is_valid = db.verify_root_exists(root_hash)
    print(f"[+] Firewall Verification: {'PASS' if is_valid else 'FAIL'}")

if __name__ == "__main__":
    run_test()