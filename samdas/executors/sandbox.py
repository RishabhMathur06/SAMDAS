# Importing dependencies.
import subprocess
import json

class DockerSandbox:
    """
        A bare-metal execution environmemnt.
        Spins up an isolated Docker container, runs the AI's code, captures the output and
        then immediately destroys the container.
    """
    def __init__(self, image: str = "python:3.11-slim"):
        self.image = image

    def execute_code(self, code: str) -> dict:
        """
            Executes raw python code inside the Docker container.
        """
        print(f"[SANDBOX] Spinning up isolated container ({self.image})...")

        # We construct a bash command to run docker.
        # --rm : Instantly destroys the container when it finishes.
        # -i : Keeps STDIN so we can pipe our code in.

        command = [
            "docker", "run", "--rm", "-i",
            self.image,
            "python", "-c", code
        ]

        try:
            # We use the subprocess module to run the terminal command securely.
            process = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=15  # Hard timeout of 15 secs so an AI can't run infinte loops.
            )

            # If the code threw a Python error inside the container.
            if process.returncode != 0:
                return {
                    "status": "error",
                    "output": process.stderr.strip()
                }

            # If the code executed successfully.
            return {
                "status": "success",
                "output": process.stdout.strip()
            }
        
        except subprocess.TimeoutExpired:
            return {
                "status": "error",
                "output": "Execution timed out (15s limit). Container terminated."
            }

        except Exception as e:
            return {
                "status": "error",
                "output": f"Sandbox failed to initialize: {str(e)}"
            }