FROM python:3.12-slim AS base

ENV PYTHONUNBUFFERED=1
WORKDIR /build

# Create requirements.txt file
FROM base AS uv
COPY --from=ghcr.io/astral-sh/uv:0.5.0 /uv /uvx /bin/
COPY uv.lock pyproject.toml ./
RUN uv export --no-dev --no-hashes -o /requirements.txt --no-install-workspace --frozen
RUN uv export --only-group dev --no-hashes -o /requirements-dev.txt --no-install-workspace --frozen

FROM base AS final
COPY --from=uv /requirements.txt .

# Create venv, add it to path and install requirements
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"
RUN pip install -r requirements.txt

# Install uvicorn server
RUN pip install uvicorn[standard]

# Copy the rest of app
COPY app app
COPY alembic alembic
COPY alembic.ini .
COPY pyproject.toml .
COPY init.sh .

EXPOSE 3000

# Make the init script executable
RUN chmod +x ./init.sh

ENTRYPOINT ["./init.sh"]

CMD ["/venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000", "--workers", "1"]
