FROM python:3.14-slim AS builder

RUN pip install --no-cache-dir uv

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv export --no-dev --no-hashes > requirements.txt && sed -i '/^-e[[:space:]]*\./d' requirements.txt

FROM python:3.14-slim

WORKDIR /app

COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ./src .
COPY --from=common / /app/common

CMD ["python", "server.py"]