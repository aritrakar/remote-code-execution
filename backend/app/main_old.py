from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .database import SessionLocal, CodeExecution
from .helpers import execute_code_in_docker, execute_code_with_judge0

app = FastAPI()

# For CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Update with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Code(BaseModel):
    code: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/execute/")
async def execute_code(code: Code):
    try:
        print("Trying to run code")
        output = execute_code_in_docker(code.code)
        print("Code executed")
        return {"output": output}
    except Exception as e:
        print("Error in execute: ", e)
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/submit/")
async def submit_code(code: Code, db: Session = Depends(get_db)):
    try:
        output = execute_code_in_docker(code.code)

        # Save the code execution in the database
        db_code_execution = CodeExecution(code=code.code, output=output)
        db.add(db_code_execution)
        db.commit()
        db.refresh(db_code_execution)

        return {"id": db_code_execution.id, "output": output}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
