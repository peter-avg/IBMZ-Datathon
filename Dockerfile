# Use a specific Python version to match your local environment
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file
COPY requirements_api_gateway.txt ./

# Install the Python packages
RUN pip install -r requirements_api_gateway.txt

# Copy your application code into the container
COPY ./API_Gateway ./API_Gateway

# Expose the port the server will run on
EXPOSE 8000

# Command to start your FastAPI server
CMD ["uvicorn", "API_Gateway.api_gateway:app", "--host", "0.0.0.0", "--port", "8000"]