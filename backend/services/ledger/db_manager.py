# Importing dependencies.
import sqlite3
from typing import List, Tuple

class LedgerDatabase:
    """
    Manages the SQLite database that acts as the permanent, 
    tamper-proof vault for our AI's cryptographic hashes.
    """
    def __init__(self, db_path: str = "samdas_ledger.db"):
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self):
        """
        Creates the database tables if they do not already exist.
        We store both the individual thought hashes and the final root hashes.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Table for final Merkle root.
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS root_hashes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    root_hash TEXT NOT NULL UNIQUE,
                    timestamp DATETIME DEAFULT CURRENT_TIMESTAMP
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS thought_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    root_hash_id INTEGER,
                    thought_hash TEXT NOT NULL,
                    sequence_number INTEGER NOT NULL,
                    FOREIGN KEY(root_hash_id) REFERENCES root_hashes(id)
                )
            """)

            conn.commit()

    def save_session(self, root_hash: str, thought_hashes: List[str]):
        """
        Locks an entire session of thoughts into the vault.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Save the root hash
            cursor.execute(
                "INSERT INTO root_hashes (root_hash) VALUES (?)",
                (root_hash,)
            )
            root_hash_id = cursor.lastrowid

            # Save all the individual thought leaves associated with
            # that Root Hash.
            for index, thought_hashes in enumerate(thought_hashes):
                cursor.execute(
                    """
                    INSERT INTO thought_logs (root_hash_id, thought_hash, sequence_number) VALUES (?, ?, ?)
                    """,
                    (root_hash_id, thought_hashes, index)
                )
            conn.commit()

    def verify_root_exists(self, root_hash: str) -> bool:
        """
        The SAMDAS firewall calls this to quickly check if a Root Hash is valid and exists.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM root_hashes WHERE root_hash = ?", (root_hash,))
            result = cursor.fetchone()

            return result is not None