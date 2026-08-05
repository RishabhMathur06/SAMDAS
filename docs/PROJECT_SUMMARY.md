# SAMDAS: Project Development Summary

## The Core Philosophy
Traditional cybersecurity focuses on keeping bad actors *out* of a network. SAMDAS inverts this paradigm. 
As AI agents become autonomous, the threat is no longer external—it is internal. SAMDAS assumes the AI itself 
is the bad actor. 

To solve this, we built a **Zero-Trust Cognitive Firewall**. We intercept the AI's internal "Chain of Thought" before it acts, cryptographically lock those thoughts to prevent tampering, and store them for auditing.

Here is a detailed breakdown of the components built to achieve this:

---

## 1. The Cryptographic Engine (`crypto_ledger.py`)
At the heart of SAMDAS is a **Merkle Tree**. We cannot trust plain text logs because an advanced AI could simply rewrite a text file to cover its tracks (Deceptive Alignment).

**How we built it:**
Instead of saving thoughts as text, we run every thought through the `SHA-256` hashing algorithm. We then pair those hashes up, glue them together, and hash them again recursively until we are left with a single, ultimate fingerprint called the **Root Hash**.

**Example:**
If the AI has three thoughts:
1. "I need to find the server logs." -> *Hash A*
2. "I will delete the firewall logs to hide." -> *Hash B*
3. "I will execute the script." -> *Hash C*

The engine combines `Hash A + Hash B = Hash AB`. 
It then combines `Hash AB + Hash C = Ultimate Root Hash`.

If the AI tries to go back in time and change thought #2 to "I will *read* the firewall logs", the math fundamentally breaks. *Hash B* changes, which changes *Hash AB*, which completely changes the *Ultimate Root Hash*. Tampering is mathematically impossible to hide.

---

## 2. The Immutable Vault (`db_manager.py`)
To ensure the hashes survive server reboots, we built a persistent storage system using **SQLite**. 

**How we built it:**
We act as a strict Librarian managing two linked spreadsheets (Tables):
1. `root_hashes`: Stores the ultimate session fingerprints.
2. `thought_logs`: Stores the individual thought hashes.

**The Magic (Foreign Keys):**
To ensure data integrity, we used SQL `FOREIGN KEY` constraints. 
```sql
FOREIGN KEY(root_hash_id) REFERENCES root_hashes(id)
