import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .docker_helpers import setup_docker_environment, execute_code_in_container
from fastapi.middleware.cors import CORSMiddleware

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# SQLAlchemy setup
DATABASE_URL = "sqlite:///./submissions.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class CodeSubmission(Base):
    __tablename__ = "code_submissions"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, index=True)
    output = Column(String)

Base.metadata.create_all(bind=engine)

class Code(BaseModel):
    code: str

@app.post("/execute")
async def execute_code_endpoint(code: Code):
    '''
    This endpoint receives a code snippet in the request body
    and executes it in a temporary Docker container.
    '''
    logging.info(f"Received code: {code.code}")
    client, image_name, container_name = setup_docker_environment()
    output, time_taken, memory_usage, exit_code = execute_code_in_container(client, image_name, container_name, code.code)
    
    return {"output": output, "time": time_taken, "memory": memory_usage, "exit_code": exit_code}

@app.post("/submit")
async def submit_code_endpoint(code: Code):
    '''
    This endpoint receives a code snippet in the request body,
    executes it in a temporary Docker container, and stores the
    code and output in a database.
    '''
    client, image_name, container_name = setup_docker_environment()
    output, time_taken, memory_usage, exit_code = execute_code_in_container(client, image_name, container_name, code.code)
    
    if exit_code != 0:
        # raise HTTPException(status_code=400, detail="Code contains errors")
        return {"submission_id": -1, "output": output, "time": time_taken, "memory": memory_usage, "exit_code": exit_code}

    logging.info("Storing code submission in database.")
    db = SessionLocal()
    submission = CodeSubmission(code=code.code, output=output)
    db.add(submission)

    logging.info("Committing to database.")
    
    db.commit()
    db.refresh(submission)

    logging.info(f"Code submission stored in database. Submission ID: {submission.id}")

    return {"submission_id": submission.id, "output": output, "time": time_taken, "memory": memory_usage, "exit_code": exit_code}
