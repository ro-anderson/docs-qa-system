# Base image
FROM python:3.11 AS base

# Set the working directory in the container
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y unzip curl

# Install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Update the PATH to include the Poetry binary
ENV PATH="/root/.local/bin:${PATH}"

# Copy only the pyproject.toml and poetry.lock (if it exists)
COPY pyproject.toml poetry.lock* /app/

# Configure poetry to not create virtual environment
RUN poetry config virtualenvs.create false

# Install the project dependencies (without dev dependencies)
RUN poetry install --no-interaction --no-ansi --without dev

# Copy the rest of the application
COPY . /app

# Verify dependencies are installed
RUN python -c "import qdrant_client; print('✓ qdrant_client installed')" && \
    python -c "import openai; print('✓ openai installed')" && \
    python -c "import langchain; print('✓ langchain installed')"

# batch_embedder image
FROM base AS batch_embedder

# Set the environment variable for the batch_embedder
ENV PYTHONPATH="/app/batch_embedder/app"

# Set the command to run the batch_embedder
CMD ["python", "batch_embedder/app/main.py"]