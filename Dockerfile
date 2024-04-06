# Use the official Python image as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backup script into the container at /app
COPY backup_script.py .

COPY api_tokens.json .

COPY backup.log .

COPY backup-service.json .

COPY test.txt .

# Command to run the backup script
CMD ["python", "backup_script.py"]
