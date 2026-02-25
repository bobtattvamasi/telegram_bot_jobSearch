FROM python:3.11-slim

WORKDIR /app

# Copy dependency files first for layer caching
COPY pyproject.toml ./

# Install production dependencies only
RUN pip install --no-cache-dir .

# Copy source code
COPY src/ ./src/

# Create data directory for SQLite
RUN mkdir -p /app/data

# Run as non-root user
RUN useradd --create-home appuser && chown -R appuser:appuser /app
USER appuser

CMD ["python", "-m", "src"]
