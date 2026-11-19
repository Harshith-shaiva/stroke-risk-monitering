# Dockerfile
# Multi-stage build for the Stroke Risk Monitoring API.
# Stage 1: install dependencies
# Stage 2: lean runtime image

# ── Stage 1: builder ──────────────────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /build

COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --prefix=/install --no-cache-dir -r requirements.txt


# ── Stage 2: runtime ─────────────────────────────────────────────────────────
FROM python:3.11-slim AS runtime

# Non-root user for security
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application source
COPY app/       ./app/
COPY config.py  .
COPY run.py     .

# Owned by non-root user
RUN chown -R appuser:appgroup /app
USER appuser

# Expose Flask default port
EXPOSE 5000

ENV FLASK_ENV=production \
    PORT=5000

CMD ["python", "run.py"]
