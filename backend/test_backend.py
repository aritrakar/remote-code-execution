import pytest
from fastapi.testclient import TestClient
from app.main import app, Base, engine
import time

# Initialize the test client
client = TestClient(app)

# Create the database tables
Base.metadata.create_all(bind=engine)

def test_execute_code():
    response = client.post("/execute", json={"code": "print('Hello, World!')"})
    assert response.status_code == 200
    assert response.json()["output"] == "Hello, World!\n"
    assert response.json()["exit_code"] == 0

def test_execute_code_error():
    time.sleep(5)
    response = client.post("/execute", json={"code": "print('Hello, World!'\n"})
    assert response.status_code == 200
    assert "SyntaxError" in response.json()["output"]
    assert response.json()["exit_code"] == 1

def test_submit_code():
    time.sleep(5)
    response = client.post("/submit", json={"code": "print('Submit test')"})
    assert response.status_code == 200
    assert "submission_id" in response.json()
    assert response.json()["output"] == "Submit test\n"
    assert response.json()["exit_code"] == 0

def test_submit_code_error():
    time.sleep(5)
    response = client.post("/submit", json={"code": "print('Submit test'\n"})
    assert response.status_code == 200
    assert response.json()["exit_code"] == 1
    assert response.json()["submission_id"] == -1

def test_pandas():
    time.sleep(5)
    response = client.post("/execute", json={"code": "import pandas as pd\nprint(pd.__version__)"})
    assert response.status_code == 200
    assert response.json()["output"].startswith("2.")
    assert response.json()["exit_code"] == 0

def test_scipy():
    time.sleep(5)
    response = client.post("/execute", json={"code": "import scipy\nprint(scipy.__version__)"})
    assert response.status_code == 200
    assert response.json()["output"].startswith("1.")
    assert response.json()["exit_code"] == 0

if __name__ == "__main__":
    pytest.main()
