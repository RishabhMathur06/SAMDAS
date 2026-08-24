# Importing Dependencies
import hashlib
from typing import List, Optional
from samdas.core.logger.logger import firewall_logger

class MerkleTree:
    """
    A Cryptographic Merkle Tree to store and verify the AI's Chain-Of-Thought.
    Every thought (token/sentence) is hashed and added as a leaf node.
    """
    def __init__(self):
        self.leaves: List[str] = []

    def add_thought(self, thought: str) -> str:
        """
        Hashes a single thought using SHA-256 and appends it to the tree.
        """
        firewall_logger.info(f"Hashing incoming thought: '{thought[:30]}...'")
        thought_hash = self._hash(thought)
        self.leaves.append(thought_hash)

        return thought_hash

    def get_root_hash(self) -> Optional[str]:
        """
        Calculates the cryptographic root hash of all thoughts.
        If any past thoughts is altered, this root hash will completely change.
        """
        if not self.leaves:
            return None

        return self._calculate_merkle_root(self.leaves)

    def _calculate_merkle_root(self, hashes: List[str]) -> str:
        """
        Recursively calculates the Merkle Root from a list of hashes.
        """
        # Return when root hash is found.
        if(len(hashes)==1):
            return hashes[0]

        new_level = []
        # Processes hashes in pairs.
        for i in range(0, len(hashes), 2):
            left = hashes[i]

            # If there's odd no. of reasoning blocks duplicate 
            # the last hash (Standard Merkle behaviour).
            right = hashes[i+1] if i+1 < len(hashes) else left

            combined = left + right
            new_level.append(self._hash(combined))

        # Recursively stitch together all the hashed reasoning blocks 
        # at each level, to finally get the rot hash.
        return self._calculate_merkle_root(new_level)

    @staticmethod
    def _hash(data: str) -> str:
        """
        Helper to compute SHA-256 hash.
        """
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    def get_audit_trail(self) -> List[str]:
        """
        Returns the chronological sequence of all hashed thoughts.
        """
        return self.leaves