# Use official Python 3.13 slim image
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install uv (Astral UV tool)
RUN curl -LsSf https://astral.sh/uv/install.sh | less

# Add uv to PATH
ENV PATH="/root/.uv/bin:$PATH"

# Copy only requirements to leverage caching
COPY pyproject.toml .

# Copy the entire project
COPY . .

# Install Python dependencies using uv
# RUN uv sync
RUN pip install -r requirements.txt

# Expose FastAPI default port
EXPOSE 8000

# Run FastAPI using uv and uvicorn
CMD ["uv", "run", "uvicorn", "agent.api_gateway:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

