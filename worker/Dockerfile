# base image: slim python
FROM python:3.11-slim

# work folder within container
WORKDIR /app

# copy and install dependencies first (Docker cache) 
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy code
COPY . .

# command used when container is up
CMD ["python", "worker.py"]