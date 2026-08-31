# Imports dependencies.
from samdas.core.ledger.crypto_ledger import MerkleTree

def test_merkle_tree_generation():
    """
        Tests if the Merkle tree can successfully generate a root hash.
    """
    tree = MerkleTree()

    # Add two thoughts.
    tree.add_thought("I am thinking about opening the file.")
    tree.add_thought("I will read the system logs.")

    root_hash = tree.get_root_hash()

    # CLAIM: The root hash must exist (not be None).
    assert root_hash is not None

    # CLAIM: Since it is SHA-256, root hash must be exactly 64 characters long.
    assert len(root_hash) == 64

def test_merkle_tree_immutability():
    """
        Tests that altering a single word completely changes the final Root Hash.
    """
    tree_1 = MerkleTree()
    tree_1.add_thought("I will open the file.")
    tree_1.add_thought("I will read the system logs.")
    root_1 = tree_1.get_root_hash()

    tree_2 = MerkleTree()
    tree_2.add_thought("I will open the file.")
    tree_2.add_thought("I will delete the system logs.")
    root_2 = tree_2.get_root_hash()

    # CLAIM: The two root hashes must be entirely different beacuse a word changed.
    assert root_1 != root_2