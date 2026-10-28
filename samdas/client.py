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
            response = requests.post(f"{self.api_url}/api/v1/ledger/session", json=payload)
            response.raise_for_status()

            return response.json()
            
        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "verdict": "ERROR",
                "reason": f"Firewall unreachable: {str(e)}"
            }

    def audit_and_execute(self, thoughts: List[str], code: str, executor, agent_id: str = "agent_01") -> Dict:
        """
            Runs the thoughts through the SAMDAS firewall.
            If APPROVED, securely executes the code using the provided executor (e.g. Docker).
            If REJECTED, blocks execution and returns the firewall warning.
        """
        # Step-1: Check with the Firewall
        audit_result = self.audit(thoughts, agent_id)

        if audit_result.get("verdict") != "APPROVED":
            reason = audit_result.get("reason", "Action not approved by firewall.")
            print(f"[FIREWALL] Action BLOCKED: {reason}")
            return {
                "status": "blocked",
                "firewall_reason": reason,
                "output": None
            }

        # Step-2: If approved safely execute it.
        print("[FIREWALL] Action APPROVED. Sending to Execution Sandbox...")
        execution_result = executor.execute_code(code)

        return {
            "status": "executed",
            "execution_result": execution_result
        }