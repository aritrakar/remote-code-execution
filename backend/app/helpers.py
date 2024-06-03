import docker
from fastapi import HTTPException
import requests
import os
from dotenv import load_dotenv

load_dotenv()

JUDGE0_API_URL = "http://localhost:8000/submissions/"
# JUDGE0_API_URL = "https://api.judge0.com/submissions/"
JUDGE0_API_KEY =  os.getenv("RAPIDAPI_KEY")


try:
    client = docker.from_env()
except docker.errors.DockerException as e:
    print("HERE")
    raise HTTPException(status_code=500, detail=f"Failed to connect to Docker: {e}")

def execute_code_in_docker(code: str):
    try:
        # Build the image
        # print("Building image")
        # client.images.build(path="../", tag="code-executor", rm=True)
        # print("Image built")

        # Run the container
        container = client.containers.run(
            image="code-executor:latest",
            stdin_open=True,
            detach=True,
        )
        print("Container created")
        container.start()
        print("Container started")
        container.exec_run(f"echo '{code}' | python /app/execute_code.py", stdin=True, stdout=True, stderr=True)
        print("Code executed")

        result = container.logs()
        container.stop()
        print("Container stopped")
        container.remove()
        print("Container removed")

        print("Logs (from helpers): ", result)

        return result.decode('utf-8')
    except Exception as e:
        print("Error in helper: ", e)
        raise HTTPException(status_code=400, detail=str(e))


def execute_code_with_judge0(source_code: str):
    payload = {
        "source_code": source_code,
        "language_id": 71,  # 71 corresponds to Python 3.8. Check Judge0 docs for language IDs.
        "stdin": "",
        "expected_output": "",
        "redirect_stderr_to_stdout": True
    }
    
    headers = {
        "Content-Type": "application/json",
        "X-RapidAPI-Key": JUDGE0_API_KEY  # Include this header only if the API key is required
    }

    try:
        response = requests.post(JUDGE0_API_URL, json=payload, headers=headers)
        if response.status_code != 201:
            raise HTTPException(status_code=response.status_code, detail="Failed to create submission")

        submission_url = JUDGE0_API_URL + response.json()["token"]
        result_response = requests.get(submission_url, headers=headers)
        while result_response.json().get("status", {}).get("description") == "In Queue":
            result_response = requests.get(submission_url, headers=headers)

        result = result_response.json()
        if result.get("stderr"):
            return result["stderr"]
        return result["stdout"]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
