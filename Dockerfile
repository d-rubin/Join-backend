# Build Stage
FROM --platform=linux/amd64 python:3.10-alpine AS builder

WORKDIR /app

# Installiere Build-Abhängigkeiten und Python-Pakete
RUN apk add --no-cache gcc musl-dev libffi-dev

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Production Stage
FROM --platform=linux/amd64 python:3.10-alpine

WORKDIR /app

# Nur die minimalen Runtimedateien kopieren
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin/python3 /usr/local/bin/python3
COPY --from=builder /usr/local/bin/gunicorn /usr/local/bin/gunicorn

ENV PATH="/root/.local/bin:$PATH"

COPY . .

EXPOSE 8000

ENTRYPOINT ["gunicorn"]
CMD ["--bind", "0.0.0.0:8000", "api.wsgi"]
