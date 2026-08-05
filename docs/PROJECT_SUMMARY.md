# SAMDAS: Project Development Summary

## The Core Philosophy
Traditional cybersecurity focuses on keeping bad actors *out* of a network. SAMDAS inverts this paradigm. As AI agents become autonomous, the threat is no longer external—it is internal. SAMDAS assumes the AI itself is the bad actor. 

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
```
This forces a strict relationship. An individual thought cannot exist in the database unless it is permanently chained to a verified Root Hash session.

**Parameterized Security:**
We used `?` placeholders (e.g., `INSERT INTO root_hashes VALUES (?)`) to prevent **SQL Injection**, ensuring that even if an AI outputs malicious SQL code in its thoughts, the database treats it purely as harmless text.

---

## 3. The Nervous System (`main.py`)
To allow the outside world to communicate with our math engine and database, we wrapped them in a high-speed **FastAPI** web server.

**How we built it:**
We created API endpoints that act as the network layer. 
- `POST /api/v1/ledger/session`: Receives thoughts from the AI.
- `GET /api/v1/ledger/sessions`: Retrieves thoughts for human viewing.

**Data Bouncing (Pydantic):**
We used `BaseModel` to create strict data contracts. 
```python
class ThoughtSession(BaseModel):
    agent_id: str
    thoughts: List[str]
```
If an AI attempts to send a malicious payload (like an executable script instead of a list of text strings), Pydantic immediately rejects the HTTP request with a `400 Bad Request` before the data ever touches our engine.

---

## 4. The Control Plane Dashboard (`frontend/`)
To make the system observable, we built a decoupled frontend using Vanilla HTML, CSS, and Javascript. 

**How we built it:**
- **UI:** A modern, dark-mode cybersecurity dashboard.
- **Networking:** We enabled `CORSMiddleware` in FastAPI to allow the browser to talk to the local server safely. 
- **DOM Manipulation:** The `app.js` file uses the `fetch()` API to hit our `GET` route, pulls the JSON data, and dynamically renders HTML table rows (`<tr>`) to display the cryptographic sessions in real-time.

---

## 5. Inference Testing (`dummy_agent.py`)
To prove the architecture works end-to-end without spending money on massive GPU resources, we built a dummy integration test. 

**How we built it:**
Using the `requests` library, this Python script simulates an AI generating a step-by-step reasoning plan. It packages the plan into JSON and shoots it across the network to our FastAPI server, proving the communication pipelines are secure and functional.

---

## What is Next: The Auditor Engine
The current system successfully **records and locks** the data. The next frontier is **Evaluation**. 

We will build the Auditor Engine (`auditor_engine.py`). This component will pull the locked thoughts from the database using a SQL `JOIN` query, and evaluate them for malicious intent. 

For the Prototype Phase, this will be a lightning-fast **Heuristic Scanner** (rule-based keyword detection). 

For the Production Phase, this architecture perfectly supports dropping in a localized, fine-tuned Hugging Face Model (like DistilBERT) to act as a Semantic AI Judge.
