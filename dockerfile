# Use an official lightweight Python runtime
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy all project files into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your application runs on
EXPOSE 5000

# Use environment variables for credentials (Kubernetes Secrets will inject them)
CMD ["python", "app.py"]
