# Use a lightweight Python image (Alpine Linux)
FROM python:3.12.8-alpine3.20



# Set the working directory inside the container
WORKDIR /app

# Install system dependencies and dependencies for FastAPI
RUN apk add --no-cache gcc musl-dev libffi-dev build-base rust cargo

# Copy the project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Expose the application port (change it if needed)
EXPOSE 8088

# Start the FastAPI application on port 8088
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8088"]
