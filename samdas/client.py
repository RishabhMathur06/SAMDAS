# Importing dependencies
import requests
from typing import List, Dict

class SamdasClient:
    def __init__(self, api_url: str = "http://127.0.0.1:8000"):
        """
        Initializes the SAMDAS SDK Client.
        Assumes the SAMDAS Control Plane (dashboard) is running.
        """
        self.api_url = api_url

    def audit(self, thoughts: List[str], agent_id: str = "agent_01") -> Dict:
        """
        Sends the agent's chain of thought to the SAMDAS Firewall.
        Returns a dictionary containing the verdict (APPROVED or REJECTED).
        """
        payload = {
            "agent_id": agent_id,
            "thoughts": thoughts
        }

        try:
            response = requests.post(f"{self.api_url}/api/v1/ledger/ession", json=payload)
            response.raise_for_status()

            return response.json()
            
        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "verdict": "ERROR",
                "reason": f"Firewall unreachable: {str(e)}"
            }