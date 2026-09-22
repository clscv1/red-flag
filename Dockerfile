FROM python:3.13-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./
COPY src ./src
COPY web ./web

RUN uv sync --frozen --no-dev

ENV HOST=0.0.0.0
ENV PORT=8080
EXPOSE 8080

CMD ["sh", "-c", "uv run red-flag --host $HOST --port $PORT"]
