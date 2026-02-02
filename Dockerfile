FROM python:3.12-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:0.8.11 /uv /uvx /bin/

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_SYSTEM_PYTHON=1 \
    UV_NO_SYNC_VENV=1 \
    UV_COMPILE_BYTECODE=1

WORKDIR /app

COPY pyproject.toml uv.lock* ./

# Экспортируем зависимости в requirements.txt и устанавливаем их
RUN uv export --format=requirements-txt --output-file=requirements.txt \
    && uv pip install --system --requirement requirements.txt


FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:0.8.11 /uv /uvx /bin/
COPY --from=builder /usr/local/lib/python3.12 /usr/local/lib/python3.12
COPY --from=builder /usr/local/bin /usr/local/bin

WORKDIR /app

COPY . .

ENV PYTHONUNBUFFERED=1 \
    UV_SYSTEM_PYTHON=1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8200"]
