FROM python:3.12-slim AS base

WORKDIR /app

RUN groupadd -r botuser && useradd -r -g botuser botuser

COPY pyproject.toml .
RUN pip install --no-cache-dir . && \
    pip install --no-cache-dir .[dev]

COPY . .

RUN chown -R botuser:botuser /app
USER botuser

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

CMD ["python", "-m", "src.bot"]