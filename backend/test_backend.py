import pytest
from fastapi.testclient import TestClient
from app.main import app, CodeSubmission, Base, engine

# Initialize the test client
client = TestClient(app)

# Create the database tables
Base.metadata.create_all(bind=engine)

def test_execute_code():
    response = client.post("/execute", json={"code": "print('Hello, World!')"})
    assert response.status_code == 200
    assert response.json() == {"output": "Hello, World!\n"}

def test_execute_code_error():
    response = client.post("/execute", json={"code": "print('Hello, World!'\n"})
    assert response.status_code == 200
    assert "SyntaxError" in response.json()["output"]

def test_submit_code():
    response = client.post("/submit", json={"code": "print('Submit test')"})
    assert response.status_code == 200
    assert "submission_id" in response.json()
    assert response.json()["output"] == "Submit test\n"

def test_submit_code_error():
    response = client.post("/submit", json={"code": "print('Submit test'\n"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Code contains errors"}

def test_pandas():
    response = client.post("/execute", json={"code": "import pandas as pd\nprint(pd.__version__)"})
    assert response.status_code == 200
    assert response.json()["output"].startswith("2.")

def test_scipy():
    response = client.post("/execute", json={"code": "import scipy\nprint(scipy.__version__)"})
    assert response.status_code == 200
    assert response.json()["output"].startswith("1.")

if __name__ == "__main__":
    pytest.main()
