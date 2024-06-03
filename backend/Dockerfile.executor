FROM python:3.11-slim

RUN pip install pandas scipy

WORKDIR /app

COPY execute_code.py /app/execute_code.py

CMD ["python", "/app/execute_code.py"]
