FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv to resolve dependencies fast
RUN pip install --no-cache-dir uv

# Copy requirements mapping
COPY pyproject.toml uv.lock ./

# Install dependencies directly into the system python env
RUN uv pip install --system --no-cache -r pyproject.toml

# Copy app code
COPY . /app/lumina_travel/

# Expose port 8080 (Cloud Run default)
EXPOSE 8080

# Start app using uvicorn
CMD ["uvicorn", "lumina_travel.app:app", "--host", "0.0.0.0", "--port", "8080"]
