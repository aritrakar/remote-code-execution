# backend/Dockerfile
FROM python:3.9

# Install Docker
RUN apt-get update && \
    apt-get install -y docker.io

# Set the working directory
WORKDIR /app

# Copy the backend code
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port
EXPOSE 8000

# Run the backend application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
