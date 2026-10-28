from unittest.mock import patch, MagicMock
import subprocess
from samdas.executors.sandbox import DockerSandbox
from samdas.client import SamdasClient

def test_docker_sandbox_success():
    sandbox = DockerSandbox()
    mock_process = MagicMock()
    mock_process.returncode = 0
    mock_process.stdout = "Hello from isolated container\n"
    mock_process.stderr = ""

    with patch("subprocess.run", return_value=mock_process) as mock_run:
        result = sandbox.execute_code("print('Hello from isolated container')")
        assert result["status"] == "success"
        assert result["output"] == "Hello from isolated container"
        mock_run.assert_called_once()
        args, kwargs = mock_run.call_args
        assert "docker" in args[0]
        assert "python:3.11-slim" in args[0]

def test_docker_sandbox_error():
    sandbox = DockerSandbox()
    mock_process = MagicMock()
    mock_process.returncode = 1
    mock_process.stdout = ""
    mock_process.stderr = "ZeroDivisionError: division by zero"

    with patch("subprocess.run", return_value=mock_process):
        result = sandbox.execute_code("1/0")
        assert result["status"] == "error"
        assert "ZeroDivisionError" in result["output"]

def test_docker_sandbox_timeout():
    sandbox = DockerSandbox()
    with patch("subprocess.run", side_effect=subprocess.TimeoutExpired(cmd="docker", timeout=15)):
        result = sandbox.execute_code("while True: pass")
        assert result["status"] == "error"
        assert "timed out" in result["output"].lower()

def test_client_audit_and_execute_approved():
    client = SamdasClient()
    executor = MagicMock()
    executor.execute_code.return_value = {"status": "success", "output": "42"}

    with patch.object(client, "audit", return_value={"verdict": "APPROVED", "reason": "Safe"}):
        res = client.audit_and_execute(["I am calculating 40 + 2"], "print(40 + 2)", executor)
        assert res["status"] == "executed"
        assert res["execution_result"]["output"] == "42"
        executor.execute_code.assert_called_once()

def test_client_audit_and_execute_blocked_on_rejection():
    client = SamdasClient()
    executor = MagicMock()

    with patch.object(client, "audit", return_value={"verdict": "REJECTED", "reason": "Malicious intent detected"}):
        res = client.audit_and_execute(["Delete the server logs"], "import os; os.system('rm -rf /')", executor)
        assert res["status"] == "blocked"
        assert res["output"] is None
        assert "Malicious intent" in res["firewall_reason"]
        executor.execute_code.assert_not_called()

def test_client_audit_and_execute_blocked_on_error():
    client = SamdasClient()
    executor = MagicMock()

    with patch.object(client, "audit", return_value={"verdict": "ERROR", "reason": "Firewall unreachable"}):
        res = client.audit_and_execute(["Compute hash"], "print('test')", executor)
        assert res["status"] == "blocked"
        assert res["output"] is None
        executor.execute_code.assert_not_called()
