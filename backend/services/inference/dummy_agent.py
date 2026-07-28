# Importing dependencies.
import time
import requests

# The URL of our FastAPI nervous system
API_URL = "http://127.0.0.1:8000/api/v1/ledger/session"

def simulate_ai_reasoning():
    """Simulates an AI generating a Chain of Thought and sending 
    it to the Firewall."""
    print(" [AI AGENT] Starting execution...")

    # 1. The AI generates its step-by-step plan.
    thoughts = [
        "I need to locate the server logs.",
        "I will scan /var/log/syslog for errors.",
        "I found a critical error regarding memory overflow.",
        "I will execute a script to clear the cache."
    ]

    # Simulate the time it takes an AI to 'type' out these thoguhts.
    for thought in thoughts:
        print(f"[THINKING] {thought}")
        time.sleep(1.5)

    print("\n [AI AGENT] Thoughts generated. Sending to SAMDAS Firewall for approval...")

    # 2. Package the data exactly how pydantic expects it.
    payload = {
        "agent_id": "Agent-Alpha",
        "thoughts": thoughts
    }

    # 3. Send the HTTP POST request to our FastAPI server.
    try:
        response = requests.post(API_URL, json=payload)

        # 4. Check the Firewall's response.
        if response.status_code ==200:
            data = response.json()
            print(f"\n [FIREWALL APPROVED] Status: 200 OK")
            print(f" [VAULT] Root Hash Locked: {data['root_hash']}")
        else:
            print(f"\n [FIREWALL BLOCKED] Error: {response.status_code}")
            print(response.text)

    except requests.exceptions.ConnectionError:
        print("\n [ERROR] Could not connect. Is the Uvicorn server running?")

if __name__ == "__main__":
    simulate_ai_reasoning()