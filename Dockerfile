# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python script
COPY github_summary.py .

# Set the command to run when the container starts
CMD ["python", "github_summary.py", "--owner", "kubernetes", "--repo", "kubernetes", "--sender", "your_email@example.com", "--receiver", "manager@example.com"]

